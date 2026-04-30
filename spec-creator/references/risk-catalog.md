# Risk Catalog — Common Implementation Risks

This is a catalog of implementation risks that frequently appear in software specs. Use it as inspiration when identifying RISK-N items for a new spec. Pattern-match against the feature set.

## Format for documenting a risk

```markdown
### RISK-N: <Short Name> (HIGH | MEDIUM | LOW)

**Problem:** What can go wrong, in concrete terms.

**Mitigation:** Specific approach to prevent or contain.

**Test Strategy:** How to verify the mitigation works.
```

## Severity guide

- **HIGH:** Failure breaks core functionality. Must be addressed before V1.
- **MEDIUM:** Failure degrades quality. Should be addressed.
- **LOW:** Failure annoys but doesn't break. Document for awareness.

---

## Category: Timing & Synchronization

### Risk pattern: Audio latency
**When relevant:** App plays audio in sync with visual events (countdowns, beeps, voice).

**Common form:**
```
**Problem:** `<audio>`-Tag has 100-300ms latency between play() and 
actual sound output. Sync becomes unreliable.

**Mitigation:** Use Web Audio API (OscillatorNode) instead. 
audioContext.currentTime is sample-accurate.

**Test Strategy:** Record audio + screen capture, measure offset 
between visual trigger and audio onset in waveform editor. Must be 
< 1 frame (16ms at 60fps).
```

### Risk pattern: Frame budget overrun
**When relevant:** Smooth scroll, animations, real-time UI updates.

**Common form:**
```
**Problem:** Rendering more than 16ms per frame drops below 60 FPS.
At 5000+ words with 10+ images, layout reflow can spike.

**Mitigation:** 
- Use transform: translateY() instead of changing top
- Lazy-render off-screen blocks
- Throttle position updates to 250ms

**Test Strategy:** Browser DevTools Performance Profiler with full 
script load + 10 images. No red bars (long tasks).
```

### Risk pattern: Race conditions in async messaging
**When relevant:** BroadcastChannel, WebSocket, postMessage between windows/workers.

**Common form:**
```
**Problem:** State updates can arrive out of order. Hotkey events 
from receiver and state pushes from sender can cross paths.

**Mitigation:** Version state updates monotonically. Receiver only 
applies updates with version > lastApplied. Sender processes events 
in arrival order.

**Test Strategy:** Hotkey spam test (10× same key in 1 second). 
Verify receiver state doesn't oscillate or revert.
```

---

## Category: Browser Quirks

### Risk pattern: Storage quota exhaustion
**When relevant:** Apps that store user-generated content locally (IndexedDB, LocalStorage).

**Common form:**
```
**Problem:** Browser quota varies (typically 50% of disk, but 
implementation-defined). Large media (4K screenshots, video) 
exhausts quickly.

**Mitigation:** 
- Auto-compress on import (max 2048×2048 for images)
- Separate thumbnails for browsing
- navigator.storage.estimate() before each write
- User warning < 100MB free with cleanup suggestion

**Test Strategy:** Import 50 large items, observe quota counter and 
warning trigger.
```

### Risk pattern: Autoplay restrictions
**When relevant:** Apps that play audio without user interaction trigger.

**Common form:**
```
**Problem:** Modern browsers block AudioContext until first user 
gesture. AudioContext.state is 'suspended' until then.

**Mitigation:** 
- Initialize AudioContext on first user click/keydown
- audioContext.resume() before play
- Handle 'suspended' state gracefully

**Test Strategy:** Open app in Incognito, trigger sync event 
without prior interaction. Should fail gracefully with user 
message, not silently break.
```

### Risk pattern: Focus handling across windows
**When relevant:** Apps with multiple windows or iframes that share state.

**Common form:**
```
**Problem:** macOS spaces/multiple monitors cause focus to be 
ambiguous. Background tabs don't receive keyboard events. 
Background tabs throttle setInterval.

**Mitigation:** 
- Visibility API (document.visibilityState) to detect background
- Use requestAnimationFrame instead of setInterval (less throttled)
- Both windows handle hotkeys independently if both can have focus

**Test Strategy:** Open both windows, drag one to second monitor, 
verify hotkeys work regardless of which has focus.
```

---

## Category: Concurrency

### Risk pattern: Multi-window sync failure
**When relevant:** Apps with multiple windows sharing state.

**Common form:**
```
**Problem:** User accidentally closes the master/sender window 
while the slave/receiver is still running. State loss possible.

**Mitigation:** 
- Heartbeat every 1s, ACK every 1s
- After 3 missed ACKs: warn user, buffer locally
- On reconnect: merge local buffer with master state

**Test Strategy:** Start session, close master window mid-stream, 
reopen, verify all events buffered are merged correctly.
```

### Risk pattern: IndexedDB transaction conflicts
**When relevant:** Apps doing many concurrent IDB writes.

**Common form:**
```
**Problem:** Concurrent transactions on same store can cause 
unhandled errors in older Safari versions.

**Mitigation:** 
- Serialize writes through a single queue
- Use transaction modes correctly (readonly vs readwrite)
- Handle TransactionInactiveError explicitly

**Test Strategy:** Run 50 concurrent saves, check no errors logged.
```

---

## Category: Data Integrity

### Risk pattern: Schema migration on existing data
**When relevant:** Apps that persist data and evolve schemas across versions.

**Common form:**
```
**Problem:** v2 schema is incompatible with v1 data. Users 
upgrading lose data or app crashes.

**Mitigation:** 
- Schema version field in every persisted record
- Migration functions for each version step
- Run migrations on app start before any reads

**Test Strategy:** Save data in v1, upgrade to v2, verify all data 
readable and intact.
```

### Risk pattern: Floating-point drift in iterative calculations
**When relevant:** Apps that accumulate small floating-point updates over time (scroll positions, timers).

**Common form:**
```
**Problem:** Adding small dt values frame-by-frame drifts from 
mathematically expected values. Position can become slightly 
off-grid.

**Mitigation:** 
- Periodically snap to integer positions
- Recalculate from absolute time, not deltas, when possible
- Avoid comparing floats with ==

**Test Strategy:** Run for 10 minutes continuous scroll, verify 
position is still pixel-aligned.
```

---

## Category: Layout & Math

### Risk pattern: Anchored element positioning
**When relevant:** Apps where an element needs to "lock" at a specific position relative to scroll/viewport.

**Common form:**
```
**Problem:** Anchoring an element to a specific viewport position 
during scroll requires precise math. Off-by-one pixels cause 
visible jump.

**Mitigation:** 
- Calculate target position explicitly (offsetTop, getBoundingClientRect)
- Set scroll position to anchor point (not approach asymptotically)
- Verify via assertion: scrollPosition === expectedAnchorPosition

**Test Strategy:** Visual inspection at 60fps recording. No frame 
should show element jump.
```

### Risk pattern: Easing function timing
**When relevant:** Apps with smooth transitions (fades, speed changes).

**Common form:**
```
**Problem:** Linear interpolation can feel mechanical. Wrong easing 
causes visible discontinuity at start/end.

**Mitigation:** 
- Use cubic-bezier or named easings (ease-out, ease-in-out)
- Match transition duration to perceived motion (300-500ms typical)
- Test on slow hardware

**Test Strategy:** Slow-mo recording at 240fps shows smooth 
acceleration/deceleration without jarring transitions.
```

---

## Category: External Dependencies

### Risk pattern: Third-party hardware compatibility
**When relevant:** Apps that interface with specific hardware (controllers, displays, capture cards).

**Common form:**
```
**Problem:** Stream Deck / Soomfon controller modifier combos 
(Option+F5) might be intercepted by macOS or other apps.

**Mitigation:** 
- Diagnostic mode (?mode=hotkey-test) shows what's received
- Document common conflicts (macOS System Settings → Keyboard)
- Allow alternative hotkey configuration in Settings (V2)

**Test Strategy:** Test with actual Stream Deck on macOS, all 
hotkeys must register. Repeat after disabling/enabling system 
shortcuts to verify diagnostic correctly identifies conflicts.
```

### Risk pattern: File format compatibility
**When relevant:** Apps that import/export to industry-standard formats (DRX, EDL, FCPXML).

**Common form:**
```
**Problem:** Format spec is incomplete. Different versions of 
DaVinci/Premiere accept slightly different variants. Edge cases 
(empty markers, special characters) may fail silently.

**Mitigation:** 
- Use simplest valid format (don't use undocumented features)
- Test with actual target software, not just format validators
- Provide fallback formats (CSV is universally readable)

**Test Strategy:** Round-trip: export from app, import in DaVinci 18 
+ DaVinci 19, verify all markers visible at correct timecodes.
```

---

## How to identify risks for a new spec

Walk the feature set and ask:
1. **Where does timing matter?** → audio sync, animation, user response time
2. **Where do windows/processes/components communicate?** → race conditions, message loss
3. **Where does data persist?** → quota, schema migration, transaction safety
4. **Where does math get tricky?** → layout calculations, easing, floating-point
5. **Where do external systems plug in?** → hardware, file formats, browser quirks

For each "where" question, if the answer is "yes, in feature X", consider naming a risk.

## Risk count sanity check

For a typical 5-7 day project with 10-15 features:
- 4-7 named risks is appropriate
- < 3 means you probably missed some
- > 10 means you're naming non-risks (every feature isn't a risk)

If you're unsure whether something is a risk, ask: "Could a competent implementer build this naively and have it fail in production?" If yes → name it.
