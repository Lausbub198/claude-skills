# Handoff an andere Skills

Nach Phase 2 fragst du den User, wie das Material weiterverarbeitet werden soll. Hier ist, was du je nach Antwort tust.

## Option (a): Plain Markdown

Speichere das gesamte Material in eine Datei im aktuellen Working-Directory:

```
topic-explainer-output-<thema-slug>.md
```

`<thema-slug>` = lowercase, Bindestriche statt Leerzeichen, keine Umlaute (ae/oe/ue), max 50 Zeichen.

Struktur der Datei:

```markdown
# [Thema]

> Schwerpunkt: [vom User gewählter Fokus]
> Zielgruppe: 20-jährige Anfänger ohne Vorwissen
> Stil-Keywords für Bilder: dark modern minimalist, cinematic, teal and orange, walnut wood

---

## Folie 1: [Titel]

**Inhalt:** ...

**Visual:** ...

---

## Folie 2: [Titel]
...
```

Sag dem User den Dateipfad und biete an, dass er die Datei selbst weiterverwenden kann.

---

## Option (b): scroll-deck

scroll-deck erwartet ein klar strukturiertes Briefing. Übergib es mit diesen Feldern:

- **Projektname / Tagline** — leite aus dem Thema ab
- **Tools / Bausteine** — falls relevant (sonst weglassen)
- **Sektionen** — pro Sektion: title, messaging (kurzer Erklärtext), visual (Bild-Prompt oder Diagrammbeschreibung)

Konkret rufst du es so auf, indem du dem User signalisierst, dass du jetzt scroll-deck nutzt:

```
"Ich übergebe jetzt an scroll-deck und baue daraus eine scrollende HTML-Webseite. Einen Moment…"
```

Dann ruf den scroll-deck-Skill auf und übergib das Material als Briefing. scroll-deck wird die Folien als scrollende Sektionen rendern (ein Reveal pro Sektion, fixed right-side nav).

**Wichtig:** scroll-deck erwartet, dass die Sektionen narrativ aufeinander aufbauen — passt zu unserem didaktischen Bogen. Die Bild-Prompts werden NICHT von scroll-deck gerendert; der User muss die Bilder separat generieren und in die HTML einbinden.

---

## Option (c): frontend-slides

frontend-slides ist für klassische Präsentationen (ein Slide pro Viewport, mit Animation). Übergib:

- **Purpose** — "teaching" (Standard für topic-explainer)
- **Length** — leite aus der Sektionszahl ab (6-9 Sektionen = ~10-12 Slides inkl. Title/Section-Dividers)
- **Content state** — "finished" (wir haben den Content komplett)
- **Aesthetic / style** — übergib die vier Stil-Keywords: dark modern minimalist, cinematic, teal and orange, walnut wood

Signalisier dem User:

```
"Ich übergebe jetzt an frontend-slides und baue eine animierte HTML-Präsentation. Einen Moment…"
```

frontend-slides wird die Folien rendern und einen passenden Look anwenden.

---

## Option (d): Nur Bild-Prompts

Extrahiere alle `[Visual]`-Blöcke, die ein Bild-Prompt sind (nicht die reinen Diagrammbeschreibungen). Speichere in:

```
image-prompts-<thema-slug>.md
```

Struktur:

```markdown
# Bild-Prompts für [Thema]

> Style-Keywords (in jedem Prompt enthalten): dark modern minimalist, cinematic, teal and orange, walnut wood
> Generator: Nano Banana 2 (Gemini Flash)

---

## Prompt 1 — Folie [Nr.]: [Folientitel]

```
[Englischer Prompt]
```

---

## Prompt 2 — Folie [Nr.]: [Folientitel]

```
[Englischer Prompt]
```
```

Sag dem User den Dateipfad. Erinnere: die Prompts sind copy-paste-bereit für Nano Banana 2 (Google AI Studio, Gemini API o.ä.).
