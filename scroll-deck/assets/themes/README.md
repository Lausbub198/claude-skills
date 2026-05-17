# Scroll-Deck Themes

Themes override the default `base.css` palette + selected component styles.
Loaded as a second `<style>` block AFTER the verbatim `base.css`.

## How to apply a theme

In the generated HTML:

```html
<head>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <!-- ONLY for theme=built: also add Space Grotesk -->
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    /* === base.css verbatim === */
  </style>
  <style>
    /* === themes/<theme>.css verbatim === */
  </style>
</head>
```

Reading the theme file:
`Read('/Users/a7wwiri/.claude/skills/scroll-deck/assets/themes/<theme>.css')`

## Theme catalog

| Theme         | File             | Background          | Accent              | Vibe                                          |
| :------------ | :--------------- | :------------------ | :------------------ | :-------------------------------------------- |
| _(default)_   | (base.css only)  | `#06090F` near-black| Dracula mix         | Dark techy, multi-accent                      |
| `built`       | `built.css`      | `#0A0E1A` Midnight  | Electric Coral      | BUILT brand — KI für den Mittelstand          |
| `cariad`      | `cariad.css`     | `#FFFFFF` white     | Blue-Violet `#442EE0`| CARIAD Master V1.4 (Blue/White/Dark modes)   |
| `blueprint`   | `blueprint.css`  | `#0B1426` deep navy | Pulse Blue mono     | Engineering schematic, sharp corners          |
| `consulting`  | `consulting.css` | `#0D1A47` royal navy| Gold `#C9A84C` mono | Premium consulting, conservative              |
| `editorial`   | `editorial.css`  | `#F2EDE4` cream     | Coral `#FF6B4A`     | Magazine print, light theme, near-black ink   |
| `terminal`    | `terminal.css`   | `#000` pure black   | Amber `#E8A000` mono| Retro CRT, mono-everything, scanlines         |

---

## Theme-specific guidance

### `built` — BUILT Design System v4.0

Brand of Andreas Nürenberg ("KI für den Mittelstand"). Canonical source:
BUILT_Brandbook_v4_0.md.

**Three rules (Brandbook-enforced):**
1. Background is **Midnight** `#0A0E1A`, never pure black.
2. **Pick ONE dominant accent per surface** — Coral = wow/brand, Pulse Blue = AI active, Signal Cyan = solved. Mixing all three loudly is off-brand.
3. **No pure white text.** Use Warm White `#F0EDE8`. No emoji in body. No filled icons.

**Section accent cycle:**
- **Coral** (`--red`/`--amber`) → start, brand intro, CTA, the "wow" moment
- **Pulse Blue** (`--blue`) → spec, architecture, AI activity, in-progress
- **Signal Cyan** (`--cyan`) → success, verification, "Problem gelöst"
- `--purple` (Beacon Yellow) and `--green` (Power Green) are **Booster** colors — sparingly only

**Brand promise:** Wrap *„Gebaut, nicht gekauft."* with `.built-promise` class and italicize "Gebaut" in Coral.

**Extra font:** Space Grotesk (loaded via Google Fonts link in `<head>`).

---

### `cariad` — CARIAD Master V1.4

Light enterprise design system. CARIAD has **3 modes** (Blue/White/Dark) — the
default in `cariad.css` is **White** mode. To switch:

- **Blue mode** — uncomment the BLUE MODE block at the bottom of `cariad.css` (background becomes `#442EE0` Blue-Violet)
- **Dark mode** — uncomment the DARK MODE block (background becomes `#1D0638` Deep Purple-Navy)

**Palette:**
- Primary: `#442EE0` Blue-Violet (brand)
- Secondary: `#1EEF97` CARIAD Green (links, success)
- Accents: `#FBAE40` Orange, `#FEF04A` Yellow, `#EE4C40` Red/Coral
- Text: `#1D0638` Deep Purple-Navy (on white) / White (on Blue/Dark modes)
- Charcoal: `#373741` (secondary text)

**Typography:** CARIAD spec calls for "FK CARIAD Light" (proprietary). The theme
falls back to **Inter 300/400** — visually close, free, web-available.

**Layout note:** Original CARIAD slides use **left-aligned** headlines at most
weights. The scroll-deck pattern keeps centered hero — that's a stylistic
divergence, not a conflict with the spec.

---

### `blueprint` — Engineering Schematic

Mono-accent **Pulse Blue** on deep technical navy. All cards/badges/tags use
`border-radius: 0` (sharp corners — blueprint paper feel). Hero uses a 40 px
schematic grid overlay.

**When to use:** architecture decks, system-design docs, technical specs that
want to feel like an engineering whiteboard, not a brand surface.

---

### `consulting` — Premium Consulting

Royal navy `#0D1A47` background, gold `#C9A84C` as the only accent. All status
pills collapse to gold mono. Includes a thin gold accent bar (`body::before`)
at the very top of the page — the "premium" tell.

**When to use:** executive decks, board presentations, investor materials,
high-end client-facing reports.

---

### `editorial` — Magazine Print

**The only light-theme**: cream paper `#F2EDE4` background, near-black ink
`#1A1A1A` text, coral `#FF6B4A` accent. Inter Black 900 for headlines, sharp
corners everywhere — feels like a print magazine spread.

Terminal blocks stay dark for contrast (an editorial "callout box").

**When to use:** long-form essays, methodology articles, reportage-style
content, anything that should feel like *FT Weekend* or *NZZ Folio*.

---

### `terminal` — CRT Amber

Pure black background, amber phosphor `#E8A000` text, **monospace everywhere**
(headings included). Optional CRT scanline overlay rendered via `body::after`.
Hero title has a soft glow text-shadow to mimic CRT bloom.

**When to use:** hacker/retro aesthetic, dev-tool branding, anything that
wants to evoke 80s green-screen workstations (in amber rather than green).

---

## Guidelines when generating with any theme

- **Read `base.css` first** — every theme is an override, not a replacement.
- **Embed verbatim** — do not rewrite either file, even if the lines look long. Future updates flow through cleanly.
- **Match section accent semantics**: even in mono-accent themes (terminal, consulting, blueprint, editorial), preserve the `--amber`/`--blue`/etc. var names so badges still work — the theme collapses them to its accent internally.
- **Don't mix two themes.** Only ever paste one `<theme>.css` block after `base.css`.
