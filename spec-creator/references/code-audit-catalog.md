# Code Audit Catalog — Defect Patterns to Find in Existing Drafts

This document is referenced from `upgrade-process.md` Phase 1b. It expands each of the seven audit checks with detailed defect examples, root causes, and the correct patterns to replace them with.

Use this catalog whenever you do a code-level audit of an existing draft. Open it as reference, walk through each check methodically.

## Table of Contents

- [Check 1: Async Lifecycle Race Conditions](#check-1-async-lifecycle-race-conditions)
- [Check 2: File-System Watch Noise](#check-2-file-system-watch-noise)
- [Check 3: WebSocket / Network Reconnect Strategy](#check-3-websocket--network-reconnect-strategy)
- [Check 4: React Rendering Performance](#check-4-react-rendering-performance)
- [Check 5: Stream Backpressure](#check-5-stream-backpressure)
- [Check 6: Persistence Schema Versioning](#check-6-persistence-schema-versioning)
- [Check 7: Hotkey / Focus / preventDefault](#check-7-hotkey--focus--preventdefault)

---

## How to read this catalog

For each check:
- **Trigger phrase:** what to grep/search for in the draft
- **Defect signature:** the wrong pattern with explanation
- **Correct signature:** the right pattern with explanation
- **Why it matters:** what breaks in production
- **Severity:** how to rank the resulting RISK

---

## Check 1: Async Lifecycle Race Conditions

**Trigger phrases:** `chokidar.watch`, `fs.watch`, `db.connect`, `redis.createClient`, `mongoose.connect`, `WebSocket(`, any async resource initialization.

### Defect Signature

```typescript
const watcher = chokidar.watch(path, opts)
watcher.on('add', handleAdd)
watcher.on('change', handleChange)

// IMMEDIATELY after watch():
session.active = true
broadcast('session:ready')
```

The `chokidar.watch()` call is synchronous but the watcher is **not actually ready** to receive events. On macOS with fsevents, initial directory scanning of large projects (50k+ files) takes 5-30 seconds. Events that fire during this window are silently dropped.

### Correct Signature

```typescript
function startWatcher(path: string): Promise<chokidar.FSWatcher> {
  return new Promise((resolve) => {
    const watcher = chokidar.watch(path, opts)
    
    watcher.on('ready', () => {
      session.active = true  // ← Set AFTER ready
      resolve(watcher)
    })
    
    watcher.on('add', handleAdd)
    watcher.on('change', handleChange)
  })
}

// Caller:
async function startSession() {
  const watcher = await startWatcher(path)  // ← Wait for ready
  broadcast('session:ready')
}
```

### Why it matters

Without the `ready` await: the first 5-30 seconds of a session lose events. User edits a file during boot → NDJSON log misses entries → CutBot generates incorrect timeline.

### Severity

**HIGH** — corrupts core data flow silently.

---

## Check 2: File-System Watch Noise

**Trigger phrases:** `chokidar.watch(path + '/.next')`, `chokidar.watch(path + '/dist')`, any directory-level watch on a build-output directory.

### Defect Signature

```typescript
chokidar.watch(projectPath + '/.next/', {
  persistent: true
})
```

Build tools like Next.js, Vite, Webpack write to their output directories on **every Hot-Reload** during development, not just on production builds. A directory-level watch sees:
- 50+ writes during one Hot-Reload cycle
- BUILD_ID file change (the actual build-done signal)
- Sourcemap regenerations
- Cache file rotations

The watcher fires on all of them, making distinguishing "build started" vs "build done" vs "Hot-Reload noise" impossible.

### Correct Signature

```typescript
const targets = [
  join(projectPath, '.next/BUILD_ID'),       // build-done signal
  join(projectPath, '.next/trace'),          // build-started signal
  join(projectPath, '.next/error-debug.log'), // build-error signal
]

const watcher = chokidar.watch(targets, {
  persistent: true,
  ignoreInitial: true,
  awaitWriteFinish: { stabilityThreshold: 200, pollInterval: 50 },
})

// + debounce on build-start to filter Hot-Reload bursts
let buildStartTimer: NodeJS.Timeout | null = null
watcher.on('all', (eventType, filePath) => {
  if (filePath.endsWith('trace')) {
    if (buildStartTimer) clearTimeout(buildStartTimer)
    buildStartTimer = setTimeout(triggerBuildStart, 1000)  // 1s debounce
  }
})
```

### Why it matters

Without specific paths + debounce: build-status widget flickers between `idle ↔ running ↔ idle` constantly during `next dev`. False signals downstream.

### Severity

**MEDIUM** — UX degraded but data isn't corrupted.

---

## Check 3: WebSocket / Network Reconnect Strategy

**Trigger phrases:** `setTimeout(reconnect, 3000)`, `setTimeout(connect, X)` where X is fixed, `ws.onclose` followed by immediate reconnect attempt without backoff.

### Defect Signature

```typescript
ws.onclose = () => {
  setTimeout(() => connect(), 3000)  // Fixed 3s retry
}
// No max-attempt cap
// No exponential backoff
// Same connection logic on first try and 100th try
```

Under network instability (Wi-Fi roaming, server restart loop), this creates a retry storm. If the server is overloaded, the storm makes recovery harder. Without a cap, the loop runs forever — no failure UI ever shows.

### Correct Signature

```typescript
const MAX_ATTEMPTS = 10
const BASE_DELAY = 1000   // 1s
const MAX_DELAY = 8000    // 8s

let attempt = 0

function connect() {
  const ws = new WebSocket(URL)
  
  ws.onopen = () => { attempt = 0 }  // Reset on success
  
  ws.onclose = () => {
    if (attempt >= MAX_ATTEMPTS) {
      showFailureUI()
      return
    }
    
    // Exponential backoff: 1, 2, 4, 8, 8, 8, ...
    const delay = Math.min(BASE_DELAY * Math.pow(2, attempt), MAX_DELAY)
    attempt += 1
    setTimeout(connect, delay)
  }
}
```

### Why it matters

Without backoff + cap: under server instability, every client hammers the server with retries, preventing recovery. User never sees a "give up" message — just a forever-spinning UI.

### Severity

**MEDIUM** — visible during instability, hidden during normal operation.

---

## Check 4: React Rendering Performance

**Trigger phrases:** Any component that receives props from frequent state updates (WebSocket messages, intervals, etc.) and:
- Renders SVG with multiple elements
- Renders a list of 5+ items
- Has computed-heavy `render()` body (Math, regex, JSON.parse)

### Defect Signature

```typescript
function VelocitySparkline({ velocity, latestDelta }) {
  const max = Math.max(...velocity)
  return (
    <svg>
      {velocity.map((v, i) => (
        <line key={i} x1={i*5} y1={16} x2={i*5} y2={16 - (v/max)*12} />
      ))}
      <text>+{latestDelta} LOC/30s</text>
    </svg>
  )
}
```

Three problems:
1. No `React.memo` — re-renders on every parent state change, not just when `velocity` actually changes
2. 10 separate `<line>` DOM elements — high reconciliation cost
3. No comparator on the props that are stable across most updates

### Correct Signature

```typescript
import { memo } from 'react'

function VelocitySparklineImpl({ velocity, latestDelta }) {
  // Single SVG path string instead of N elements
  const max = Math.max(...velocity, 1)
  const pathData = velocity.map((v, i) => {
    const x = i * 6
    const y = 16 - (v / max) * 12
    return `M${x},16 L${x},${y} L${x+5},${y} L${x+5},16 Z`
  }).join(' ')
  
  return (
    <svg width="60" height="16">
      <path d={pathData} fill="var(--signal-cyan)" />
      <text>+{latestDelta} LOC/30s</text>
    </svg>
  )
}

export const VelocitySparkline = memo(VelocitySparklineImpl, (prev, next) => {
  if (prev.latestDelta !== next.latestDelta) return false
  if (prev.velocity.length !== next.velocity.length) return false
  // Sliding window: only the last value can change
  return prev.velocity[prev.velocity.length - 1] === next.velocity[next.velocity.length - 1]
})
```

### Why it matters

Without `memo` + custom comparator: in a 60-min session with 100+ parent re-renders, this component re-renders every time even though its props are stable. Cumulative cost shows up as frame drops.

### Severity

**MEDIUM** — only visible in long sessions or on low-end hardware.

---

## Check 5: Stream Backpressure

**Trigger phrases:** `createWriteStream`, `fs.createWriteStream`, `Response.write`, `stream.write(`, NDJSON logging, log files.

### Defect Signature

```typescript
const stream = createWriteStream(path, { flags: 'a' })

function logEvent(event) {
  stream.write(JSON.stringify(event) + '\n')  // ignores return value
}

function closeLogger() {
  stream.end()  // not awaited
}
```

Three problems:
1. `stream.write()` returns `false` when buffer is full — caller must wait for `drain`
2. Default `highWaterMark` (16KB) is small — fills quickly under burst load
3. `stream.end()` is async — caller doesn't know when file is actually flushed

Under burst writes (50+ events/sec on slow disk), Node accumulates events in memory. Memory grows. Process can OOM.

### Correct Signature

```typescript
let backpressure = false

const stream = createWriteStream(path, { 
  flags: 'a',
  highWaterMark: 64 * 1024  // larger buffer
})

stream.on('drain', () => { backpressure = false })

function logEvent(event) {
  const ok = stream.write(JSON.stringify(event) + '\n')
  if (!ok) backpressure = true
  // events still buffer; we just track the flag
}

async function closeLogger() {
  // Wait for drain if needed
  if (backpressure) {
    await new Promise(resolve => stream.once('drain', resolve))
  }
  // stream.end() with callback
  await new Promise((resolve, reject) => {
    stream.end(err => err ? reject(err) : resolve())
  })
}

// Crash safety
process.on('SIGINT', () => closeLogger().finally(() => process.exit(0)))
process.on('SIGTERM', () => closeLogger().finally(() => process.exit(0)))
```

### Why it matters

Without backpressure handling: process can run out of memory under disk-bound load. Without await on `end()`: file may be truncated when process exits. Without SIGINT handler: Ctrl+C loses last events.

### Severity

**LOW to MEDIUM** — only matters under stress or crash, but data integrity is at stake.

---

## Check 6: Persistence Schema Versioning

**Trigger phrases:** `IndexedDB`, NDJSON, JSON files for state persistence, log files read by external tools (CutBot, analytics, downstream).

### Defect Signature

```typescript
// First line of NDJSON log:
{"type": "session:start", "data": {"sessionName": "X", "acts": [...]}}

// No schemaVersion anywhere
```

When the schema evolves (add field, rename field, change type), there's no way for the reader to know which version it's looking at. Old logs become unreadable. New logs crash old readers.

### Correct Signature

```typescript
// Constant in the writer:
export const SCHEMA_VERSION = '1.0'

// First line:
logEvent('session:start', {
  schemaVersion: SCHEMA_VERSION,
  sessionName: 'X',
  acts: [...]
})

// Reader (CutBot, etc.):
function readLog(path) {
  const firstLine = readFirstLine(path)
  const event = JSON.parse(firstLine)
  
  if (!event.data.schemaVersion) {
    throw new Error('Log missing schemaVersion — unsupported pre-1.0 format')
  }
  
  const major = event.data.schemaVersion.split('.')[0]
  if (major !== '1') {
    throw new Error(`Unsupported major version: ${event.data.schemaVersion}`)
  }
  
  // proceed
}
```

### Why it matters

Without schema versioning: silent data loss when the schema changes. Implementer of the reader doesn't know what fields to expect. Downstream tools (CutBot) generate incorrect output without knowing why.

### Severity

**HIGH** — corruption is silent and downstream.

---

## Check 7: Hotkey / Focus / preventDefault

**Trigger phrases:** `window.addEventListener('keydown', ...)`, `document.addEventListener('keydown', ...)`, especially for Cmd+digit, Cmd+S, Ctrl+S, Cmd+0.

### Defect Signature

```typescript
window.addEventListener('keydown', (e) => {
  if (e.metaKey && e.code === 'Digit5') {
    onActChange(5)
  }
})
```

Three problems:
1. No `document.hasFocus()` check — fires when DevStage is in a background tab
2. No input-field check — fires when user is typing in a Settings modal
3. No `e.preventDefault()` — Cmd+5 also switches browser tab; Cmd+0 also resets browser zoom

### Correct Signature

```typescript
window.addEventListener('keydown', (e) => {
  // Guard 1: app must have system focus
  if (!document.hasFocus()) return
  
  // Guard 2: user must not be typing
  const target = e.target as HTMLElement
  if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable) {
    return
  }
  
  // Guard 3: only meta+digit
  if (!e.metaKey) return
  
  if (e.code === 'Digit0') {
    e.preventDefault()  // block browser zoom reset
    onActReset()
    return
  }
  
  const match = /^Digit([1-9])$/.exec(e.code)
  if (match) {
    e.preventDefault()  // block browser tab switch
    onActChange(parseInt(match[1], 10))
  }
})
```

### Why it matters

Without guards: hotkey fires while user is typing in input → app state mutates unexpectedly. Without `preventDefault`: Cmd+0 resets browser zoom AND triggers app action — user sees both happen, confused. Cmd+1-9 switches browser tab AND triggers act change — user loses context.

### Severity

**LOW** — annoying, not data-corrupting. But the fix is one line per guard, so always do it.

---

## How to use this catalog during an audit

When you reach Phase 1b in `upgrade-process.md`:

1. Open this file
2. For each of the seven checks, search the draft for the trigger phrases
3. For each match, compare against defect/correct signatures
4. Record findings in the FINDING-N format from upgrade-process.md
5. After all seven checks done, present findings to user

If the draft is short (< 500 lines), this takes 5-10 minutes. If long (1000+), 15-25 minutes. The time is well-spent — without it, the upgraded spec is structurally complete but technically broken.

## Adding new checks

This catalog grows over time as new defect patterns emerge. When you find a new defect pattern in a real spec audit, add it here as a new check (Check 8, 9, ...) following the same format. Future audits will benefit.

Suggested expansion areas (not yet documented):
- IndexedDB transaction handling
- Web Audio API initialization (autoplay restrictions)
- Drag-and-drop event handling (preventDefault on dragover)
- localStorage quota management
- Image/blob memory leaks (URL.revokeObjectURL)
- Focus trap in modals
- ResizeObserver / IntersectionObserver cleanup
