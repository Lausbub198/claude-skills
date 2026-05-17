---
name: scroll-deck
description: Builds a single-file, zero-dependency scrolling HTML presentation — the kind used to present a methodology, tool, pipeline, or product with a dark techy aesthetic. Each section reveals on scroll, content builds top to bottom, and a fixed right-side nav tracks progress. Use this skill whenever the user wants to present a process, product, or workflow as a web page that scrolls vertically (NOT a slide deck — for slide decks use frontend-slides instead). Trigger on phrases like "scroll-deck", "web-Folie", "scrollende Präsentation", "Produktseite erstellen", "product page", "landing page für mein Tool", "HTML Präsentation die man runterscrollt", "erkläre meinen Prozess als Webseite", "methodology page", or any request for a web-based visual presentation of a pipeline or workflow.
---

# Scroll-Deck Skill

Builds a polished, single-file HTML scroll-deck that presents a product, methodology, or workflow as a vertically-scrolling web experience. Content reveals as the user scrolls, each section tells one part of the story, and the page works in any browser with zero dependencies beyond Google Fonts.

This is the pattern captured from `softwareschmiede.html` in TelePro — use it verbatim.

## When to use this vs. frontend-slides

- **product-page** → continuous vertical scroll, sections build up, variable content density, product marketing feel
- **frontend-slides** → snap-scroll, one slide = one screen, keyboard navigation, presentation feel

## Workflow

### Step 1 — Gather content structure

Ask (or infer from context) these things before writing any code:

1. **Product/topic name** — the hero title (e.g. "Die Softwareschmiede")
2. **Tagline** — one sentence that captures the value (e.g. "Aus Ideen wird Software — deterministisch, testgetrieben, reproduzierbar.")
3. **Skill/tool tags** — 5-8 key tools shown in the hero (e.g. spec-creator, opsx:bdd)
4. **Sections** — 6-9 phases/sections. For each: a short title, the main message (1-2 sentences), what visual to show (terminal block with code? cards? file tree?)
5. **Language** — German or English (default: match user's language)

If the user has already described their content in the conversation, extract it directly rather than asking again.

### Step 2 — Choose accent colors per section

Each section gets one accent color from the palette. Use them to signal meaning, not randomly:
- `--amber` → requirements, input, starting point
- `--blue` → spec, design, structure
- `--purple` → breakdown, transformation, splitting
- `--red` → tests (RED phase), pending, not-yet-done
- `--green` → success, done, implementation, archive
- `--cyan` → verification, checking, review

### Step 2.5 — Pick a theme (optional)

By default, the deck uses the built-in dark techy palette (Dracula-inspired).
If the user wants a branded or stylized deck, switch to a theme from `assets/themes/`:

| Theme        | Vibe                                                | Background          | Extra font       |
| :----------- | :-------------------------------------------------- | :------------------ | :--------------- |
| default      | Dark techy, Dracula syntax, blue/cyan/coral mix     | `#06090F` near-black| —                |
| `built`      | BUILT brand — KI für den Mittelstand                | `#0A0E1A` Midnight  | Space Grotesk    |
| `cariad`     | CARIAD Master V1.4 — light enterprise               | `#FFFFFF` white     | —                |
| `blueprint`  | Engineering schematic, mono-Pulse-Blue, sharp       | `#0B1426` deep navy | —                |
| `consulting` | Premium consulting, navy + gold mono                | `#0D1A47` royal navy| —                |
| `editorial`  | Magazine print, cream paper, near-black ink, coral  | `#F2EDE4` cream     | —                |
| `terminal`   | Retro CRT, amber phosphor, monospace everything     | `#000` pure black   | —                |

**Trigger phrase detection** (match user's prompt before asking):

| Theme        | Trigger phrases / keywords                                                                                                          |
| :----------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| `built`      | "BUILT", "BUILT theme", "BUILT brand", "BUILT-Branding", *„Gebaut, nicht gekauft"*, "Mittelstand", "KI für den Mittelstand", BUILT channel content |
| `cariad`     | "CARIAD", "CARIAD theme", "CARIAD-Stil", "CARIAD Master", "CARIAD violet", "FK CARIAD", "VW.OS", any CARIAD/Volkswagen ecosystem context |
| `blueprint`  | "blueprint", "im blueprint Stil", "Engineering Stil", "schematic", "architecture deck"                                              |
| `consulting` | "consulting", "premium", "McKinsey-Stil", "Bain", "BCG", "executive deck", "gold accent", "konservativ"                             |
| `editorial`  | "editorial", "magazin", "magazine", "print", "Zeitschrift", "Reportage", "hell", "light theme", "cream paper"                       |
| `terminal`   | "terminal", "CRT", "retro", "amber", "phosphor", "hacker", "old-school", "tty"                                                      |

**When a theme is selected:**
1. Read `assets/themes/README.md` for theme-specific rules (e.g. BUILT's 3-accent rule, CARIAD's mode variants)
2. Read `assets/themes/<theme>.css` and embed it AFTER `base.css` in a second `<style>` block
3. Add any extra Google Fonts the theme requires (only `built` needs Space Grotesk) to `<head>`

### Step 3 — Build the HTML file

Load the CSS boilerplate from `assets/base.css` verbatim — do not rewrite it. Add your HTML on top.
If a theme is selected, embed its override CSS in a second `<style>` block AFTER base.css.

**File structure:**
```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Product Name]</title>
  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <!-- ONLY IF theme=built: also add Space Grotesk -->
  <!-- <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet"> -->
  <style>
    /* === PASTE base.css VERBATIM HERE === */
  </style>
  <!-- ONLY IF a theme is selected, add a second style block AFTER base.css -->
  <!-- <style>/* === PASTE themes/<theme>.css VERBATIM HERE === */</style> -->
</head>
<body>
  <!-- Phase Nav -->
  <!-- Hero (s0) -->
  <!-- Sections (s1...sN) -->
  <!-- Pipeline overview (sN+1) -->
  <script>/* paste base JS verbatim */</script>
</body>
</html>
```

For the base CSS and JS, read `assets/base.css` and `assets/base.js`.

### Step 4 — Build each section

See `references/components.md` for the exact HTML patterns for each component (terminal, cards, file tree, split layout, pipeline tracker, etc.).

## Section anatomy

Every phase section follows this skeleton:

```html
<section class="phase [phase-alt]" id="sN">
  <div class="phase-bg-num">0N</div>
  <div class="container">

    <!-- Option A: split layout (text left, visual right) -->
    <div class="split[-55|-45]">
      <div>
        <div class="badge reveal" style="background:var(--ACCENT-g);border:1px solid var(--ACCENT-b);color:var(--ACCENT);margin-bottom:1.4rem">
          Phase 0N · Section Title
        </div>
        <h2 class="h1 reveal d1">Headline</h2>
        <p class="body-lg reveal d2">Body text...</p>
        <!-- cards / checklist / etc -->
        <div style="margin-top:1.5rem;display:flex;gap:.5rem;flex-wrap:wrap" class="reveal d4">
          <span class="skill-tag">skill-name</span>
        </div>
      </div>
      <div class="reveal-r d2">
        <!-- terminal or other visual -->
      </div>
    </div>

    <!-- Option B: centered header + grid below -->
    <div style="text-align:center;margin-bottom:...">
      <div class="badge reveal">Phase 0N · Title</div>
      <h2 class="h1 reveal d1">Headline</h2>
      <p class="body-lg reveal d2">Body...</p>
    </div>
    <div class="cols3 reveal d3"><!-- cards --></div>

  </div>
</section>
```

Alternate `.phase` and `.phase-alt` for visual rhythm (`.phase-alt` has slightly lighter background).

## Hero anatomy

The hero content must be centered both horizontally AND vertically (in the middle of the viewport). Use `display:flex; align-items:center; justify-content:center; min-height:100vh` on the hero section, and `text-align:center` on `.hero-inner`.

```html
<section class="hero" id="s0">
  <div class="hero-grid"></div>
  <div class="hero-glow1"></div>
  <div class="hero-glow2"></div>
  <div class="hero-inner">
    <div class="hero-eyebrow fade-in" style="animation-delay:.05s">Category label</div>
    <h1 class="hero-title fade-in" style="animation-delay:.15s">Product<br>Name</h1>
    <p class="hero-sub fade-in" style="animation-delay:.28s">Tagline sentence.</p>
    <div class="hero-tags fade-in" style="animation-delay:.42s">
      <span class="hero-tag">tool-1</span>
      <span class="hero-tag">tool-2</span>
    </div>
    <div class="hero-scroll fade-in" style="animation-delay:.58s">
      <span class="scroll-bar"></span>SCROLL TO EXPLORE
    </div>
  </div>
</section>
```

## Phase nav

Generate one dot per section (s0…sN):

```html
<nav class="phase-nav" id="phaseNav">
  <button class="pn-dot active" data-section="s0" data-label="Start"
    onclick="document.getElementById('s0').scrollIntoView({behavior:'smooth'})"></button>
  <div class="pn-seg"></div>
  <!-- repeat for each section -->
</nav>
```

## Final pipeline section

Always end with a summary section showing the full pipeline as a vertical step list using `.pipe-track` and `.pipe-step`. See `references/components.md` for the pattern.

## Quality checklist

Before finishing:
- [ ] Hero title is bold and large enough to dominate — `font-size: clamp(3.5rem, 9.5vw, 9rem)`
- [ ] Each section has at least one visual (terminal or cards) — not just text
- [ ] Terminal blocks have real-looking content, not placeholder `// TODO`
- [ ] All skill tags at the bottom of sections use `<span class="skill-tag">`
- [ ] Phase nav has correct section count (s0 to sN)
- [ ] Sections alternate `.phase` / `.phase-alt`
- [ ] Mobile: `.split` collapses to single column at 880px (handled by base.css)
- [ ] File saved as `[kebab-name].html` in the project directory
