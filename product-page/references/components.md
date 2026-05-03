# Component Patterns

HTML patterns for all reusable components in the product-page skill. Paste verbatim and fill in the content.

---

## Terminal block

Shows fake command-line output. Use for code examples, pipeline steps, CLI commands, and config files.

```html
<div class="term">
  <div class="term-bar">
    <span class="td td-r"></span>
    <span class="td td-a"></span>
    <span class="td td-g"></span>
    <span class="term-label">filename.ts — bash</span>
  </div>
  <div class="term-body">
    <pre>
<span class="cc"># comment line</span>
<span class="ck">const</span> <span class="ct">name</span> = <span class="cs">'value'</span>
<span class="cf">functionName</span>(<span class="cn">argument</span>)
</pre>
  </div>
</div>
```

**Syntax color classes (Dracula-inspired):**
| Class | Color   | Use for                          |
|-------|---------|----------------------------------|
| `.ck` | Pink    | Keywords (`const`, `let`, `if`)  |
| `.cf` | Green   | Function names                   |
| `.cs` | Yellow  | String literals                  |
| `.ct` | Cyan    | Type names, variable names       |
| `.cc` | Gray    | Comments (also add `font-style:italic`) |
| `.cn` | Purple  | Numbers, booleans, constants     |
| `.cp` | Light   | Parameters, misc                 |

**Gherkin syntax classes:**
| Class | Use for                     |
|-------|-----------------------------|
| `.gk` | Given/When/Then/And keywords |
| `.gc` | Context (noun phrases)      |
| `.gv` | Values in quotes            |
| `.gt` | Plain text                  |

---

## Card grid (.cols3)

Three-column grid that collapses to 2 cols at 880px and 1 col at 540px.

```html
<div class="cols3">
  <div class="card reveal d1">
    <div style="font-size:1.4rem;margin-bottom:.7rem">🔵</div>
    <div class="h3" style="margin-bottom:.5rem">Card Title</div>
    <p class="body">Card description text goes here. Keep it to 2-3 sentences.</p>
  </div>
  <div class="card reveal d2">
    <div style="font-size:1.4rem;margin-bottom:.7rem">🟢</div>
    <div class="h3" style="margin-bottom:.5rem">Card Title</div>
    <p class="body">Card description text goes here.</p>
  </div>
  <div class="card reveal d3">
    <div style="font-size:1.4rem;margin-bottom:.7rem">🟡</div>
    <div class="h3" style="margin-bottom:.5rem">Card Title</div>
    <p class="body">Card description text goes here.</p>
  </div>
</div>
```

Use `.d1`, `.d2`, `.d3` delay classes to stagger the reveal animation.

---

## File tree

Shows a project's directory structure. Mix `.ftd` (directory), `.ftf` (file), `.ftn` (new file), `.fta` (modified) colors.

```html
<div class="term">
  <div class="term-bar">
    <span class="td td-r"></span><span class="td td-a"></span><span class="td td-g"></span>
    <span class="term-label">project structure</span>
  </div>
  <div class="term-body">
    <div class="ftree">
      <div><span class="ftd">src/</span></div>
      <div>&nbsp;&nbsp;<span class="ftd">components/</span></div>
      <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="ftn">Button.tsx</span></div>
      <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="ftf">Header.tsx</span></div>
      <div>&nbsp;&nbsp;<span class="ftd">utils/</span></div>
      <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="fta">helpers.ts</span></div>
      <div><span class="ftf">package.json</span></div>
    </div>
  </div>
</div>
```

**File color semantics:**
- `.ftd` blue — directory
- `.ftf` dim — unchanged file
- `.ftn` green — new file
- `.fta` amber — modified file

---

## Status badge / pill

Inline status indicator with colored dot.

```html
<span class="status s-green">DONE</span>
<span class="status s-red">PENDING</span>
<span class="status s-amber">IN PROGRESS</span>
<span class="status s-blue">ACTIVE</span>
<span class="status s-purple">REVIEW</span>
```

---

## Section badge

Use at the top of each section to label the phase/number.

```html
<div class="badge reveal"
  style="background:var(--blue-g);border:1px solid var(--blue-b);color:var(--blue);margin-bottom:1.4rem">
  Phase 01 · Section Title
</div>
```

Replace `--blue` with the accent color for this section (`--amber`, `--green`, `--red`, `--purple`, `--cyan`).

---

## Skill tags row

Shows a row of monospace tool/skill names at the bottom of a section.

```html
<div style="margin-top:1.5rem;display:flex;gap:.5rem;flex-wrap:wrap" class="reveal d4">
  <span class="skill-tag">tool-name-1</span>
  <span class="skill-tag">tool-name-2</span>
  <span class="skill-tag">tool-name-3</span>
</div>
```

---

## Checklist inside a card

Use inside a `.card` to show a list of requirements or steps.

```html
<div class="card reveal d2" style="margin-top:1.5rem">
  <div style="display:flex;flex-direction:column;gap:.6rem">
    <div style="display:flex;align-items:center;gap:.7rem;font-size:.9rem">
      <span style="color:var(--green)">✓</span>
      <span>First item</span>
    </div>
    <div style="display:flex;align-items:center;gap:.7rem;font-size:.9rem">
      <span style="color:var(--green)">✓</span>
      <span>Second item</span>
    </div>
    <div style="display:flex;align-items:center;gap:.7rem;font-size:.9rem;color:var(--text-muted)">
      <span style="color:var(--text-muted)">○</span>
      <span>Pending item</span>
    </div>
  </div>
</div>
```

---

## Audit row block

Shows a compact result list with colored rows (critical / warning / ok).

```html
<div style="display:flex;flex-direction:column;gap:.4rem;margin-top:1rem">
  <div class="audit-row audit-crit">
    <span class="audit-label">CRITICAL</span>
    <span>Description of the critical issue</span>
  </div>
  <div class="audit-row audit-warn">
    <span class="audit-label">WARN</span>
    <span>Description of the warning</span>
  </div>
  <div class="audit-row audit-ok">
    <span class="audit-label">OK</span>
    <span>Everything checks out here</span>
  </div>
</div>
```

---

## Pipeline overview (final section)

Always the last section. Shows the full flow as a vertical step list.

```html
<section class="phase" id="sN">
  <div class="phase-bg-num">0N</div>
  <div class="container">
    <div style="text-align:center;max-width:700px;margin:0 auto 4rem">
      <div class="badge reveal"
        style="background:var(--green-g);border:1px solid var(--green-b);color:var(--green);margin-bottom:1.4rem">
        Full Pipeline
      </div>
      <h2 class="h1 reveal d1">End-to-End Overview</h2>
      <p class="body-lg reveal d2">The complete flow from start to finish.</p>
    </div>

    <div class="pipe-track">

      <div class="pipe-step reveal">
        <div class="pipe-icon" style="background:var(--amber-g);border-color:var(--amber-b);color:var(--amber)">01</div>
        <div class="pipe-body">
          <div class="pipe-title">Step One Title</div>
          <div class="pipe-desc">What happens in this step and why it matters.</div>
          <div class="pipe-tags">
            <span class="skill-tag">tool-a</span>
            <span class="skill-tag">tool-b</span>
          </div>
        </div>
      </div>

      <div class="pipe-step reveal d1">
        <div class="pipe-icon" style="background:var(--blue-g);border-color:var(--blue-b);color:var(--blue)">02</div>
        <div class="pipe-body">
          <div class="pipe-title">Step Two Title</div>
          <div class="pipe-desc">What happens in this step.</div>
          <div class="pipe-tags">
            <span class="skill-tag">tool-c</span>
          </div>
        </div>
      </div>

      <!-- repeat for each step, cycling through accent colors -->

    </div>
  </div>
</section>
```

**Pipe-step connector:** The CSS adds a vertical line between `.pipe-step` elements automatically via `.pipe-step+.pipe-step .pipe-icon::before`. No extra markup needed.

**Accent color cycling suggestion:** amber → blue → purple → red → green → cyan → repeat

---

## Split layout variants

Three grid variants for text + visual side-by-side:

```html
<!-- Equal 50/50 -->
<div class="split">
  <div><!-- text --></div>
  <div class="reveal-r d2"><!-- visual --></div>
</div>

<!-- 55/45: text heavier -->
<div class="split-55">
  <div><!-- text --></div>
  <div class="reveal-r d2"><!-- visual --></div>
</div>

<!-- 45/55: visual heavier -->
<div class="split-45">
  <div><!-- text --></div>
  <div class="reveal-r d2"><!-- visual --></div>
</div>
```

All three collapse to single column at 880px via base.css.

---

## Reveal animation classes

Apply to any element to animate it in when it enters the viewport:

| Class      | Direction           |
|------------|---------------------|
| `.reveal`  | Fade up             |
| `.reveal-l`| Fade from left      |
| `.reveal-r`| Fade from right     |

Combine with delay classes `.d1`–`.d6` for staggered entry:

```html
<div class="reveal d1">first</div>
<div class="reveal d2">second</div>
<div class="reveal d3">third</div>
```

**Hero elements:** Use `.fade-in` with inline `animation-delay` instead of `.reveal` — hero content must be visible immediately without scrolling, and IntersectionObserver fires asynchronously which would cause a flash of invisible content.

```html
<h1 class="fade-in" style="animation-delay:.15s">Title</h1>
<p  class="fade-in" style="animation-delay:.28s">Subtitle</p>
```
