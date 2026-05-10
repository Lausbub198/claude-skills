---
name: youtube-production
description: "Konsolidierter YouTube-Produktions-Skill für ALLE BUILT-Videoformate (Sonne 15–20 Min, Planet-Demo 4–8 Min, Planet-Explainer 5–15 Min). Produziert 8 standardisierte Artefakte (A1 Konzept bis A8 Upload-Paket) über eine mehrstufige Pipeline mit internem Persona-System. Zwei Modi: INTERAKTIV (Artefakt für Artefakt mit Creator-Freigabe) und AUTONOM (Pre-Flight-Check → dann alle Artefakte ohne Zwischenstopps). JSON-Schema-basierte Ausgabe. Trigger: 'Video Skript', 'Skript erstellen', 'neues Video', 'youtube-production', 'Sonne erstellen', 'Planet erstellen', 'Demo Skript', 'Explainer Skript'."
metadata:
  tags: youtube, video, skript, production, built, mittelstand, ki, sonne, planet, demo, explainer
---

# BUILT — YouTube Production Skill

> **Brand-Referenz:** `/Users/a7wwiri/Projects/brand_knowledge/BUILT_Brandbook_v4_0.md`
> **JSON-Schema:** `/Users/a7wwiri/.claude/skills/youtube-production/schema/video_skript_schema.json`
> **Produktionsplan:** `/Users/a7wwiri/Projects/brand_knowledge/PRODUKTIONSPLAN_Season_1.md`
> **YouTube-Strategie:** `/Users/a7wwiri/Projects/brand_knowledge/YOUTUBE_STRATEGIE_2026.md`

> ⛔ **OUTPUT-PFLICHT — GILT IMMER, AUCH NACH KONTEXT-KOMPRIMIERUNG:**
> 1. Primär-Output: **JSON-Datei** — Dateiname = Titel des Videos (kleingeschrieben, Sonderzeichen → `-`/`_`).
> 2. Speicherort JSON: `/Users/a7wwiri/Projects/vs/[Ordner]/[video_titel].json`
> 3. Nach dem Schreiben: **Validierung** → `python3 .../validate_script.py <datei>` — Pipeline stoppt bei Fehlern.
> 4. Nach 0 Fehlern: **Firebase-Upload** → `node .../upload-script.mjs <datei>`
> 5. Zusätzlich nach erfolgreichem Upload: **3 Markdown-Dateien** in denselben Ordner schreiben (siehe "Markdown-Artefakte"):
>    - `01-[slug]-setup.md` — nur bei Videos mit Demo-Environment-Setup
>    - `03-demo-pack.md` — nur bei Videos mit Live-Demo
>    - `04-b-roll-production-list.md` — alle Formate
> 6. `02-teleprompter-script.md` wird **NICHT** hier generiert — das ist Aufgabe des `telepro-script` Skills.
> 7. Erst dann ist ein Video-Paket vollständig.

Dieser Skill produziert **8 standardisierte Artefakte** für jedes BUILT-Video — unabhängig vom Format.
Er ersetzt die drei bisherigen Skills (youtube-content, youtube-demo-content, youtube-short-content).

---

## Artefakte-Übersicht

| # | Artefakt | Inhalt |
|---|----------|--------|
| A1 | Konzept | Titel, Zielgruppe, Kernversprechen, Magic Moment, Zielperson, Stack |
| A2 | Roadmap | Zuschauer-Roadmap mit Phasen, Preconditions, WOW-Momenten |
| A3 | Skript | Passagen mit Teleprompter-Text, Regieanweisungen, Block-Typen |
| A4 | Bilder | Grafik- und B-Roll-Beschreibungen (Inhalt, kein Brand-Styling) |
| A5 | Prompts | Vollständige Claude-Prompts (copy-paste-ready als Blueprint) |
| A6 | Rehearsal | Setup, Troubleshooting, Checklisten für den Dreh |
| A7 | Spickzettel | Thematische Blöcke als Übersicht für die Live-Aufnahme |
| A8 | Upload-Paket | Titel, Beschreibung, Tags, Thumbnail-Briefing, Endscreen |

---

## Markdown-Artefakte

Nach dem JSON werden drei zusätzliche Markdown-Dateien generiert — menschenlesbare, direkt im Dreh verwendbare Versionen des JSON-Inhalts. Sie destillieren jeweils einen Teil der JSON-Artefakte in ein eigenständiges Dokument.

### `01-[slug]-setup.md` — Demo-Environment-Setup
**Wann:** Nur bei Videos, bei denen vor dem Dreh eine externe Umgebung aufgebaut werden muss (Test-Accounts, Demo-Daten, externe Services).
**Quelle im JSON:** `a6_rehearsal.pre_production_setup`

Struktur:
```
# [Thema] Test-Setup
## [Zeitaufwand] · BUILT

> Zeitaufwand + Wann machen

## VORAUSSETZUNGEN (Tabelle: Item / Status / Wo besorgen)

## SCHRITT 1–N: [Jeder Setup-Schritt nummeriert mit Zeitangabe]

## Pre-Take Validierung (Pflicht!)
  - Exakter Test-Prompt (copy-paste-ready)
  - Checkliste: Check / Erwartetes Ergebnis / Status ☐

## TROUBLESHOOTING
  - Probleme + Fixes als ### Blöcke

## GO/NO-GO-ENTSCHEIDUNG
  - ✅ GO-Kriterien
  - ⚠️ NO-GO-Kriterien + Plan B

## ESTIMATED TOTAL EFFORT (Tabelle + Empfehlung)
```

---

### `03-demo-pack.md` — Demo-Choreographie
**Wann:** Nur bei Videos mit Live-Demo (alle Sonnen + Planet-Demos).
**Quelle im JSON:** `a5_prompts` + Demo-Abschnitte von `a6_rehearsal`

Struktur:
```
# Demo-Pack — [Demo-Titel]
## BUILT · Video Slot: [Zeitraum] · Modus: [Hybrid/Live/Pre-recorded]

> Hybrid-Definition falls relevant

## VORAB-CHECK
  - Verweis auf 01-setup.md + Go/No-Go-Grenzwert

## DREHTAG-REIHENFOLGE (Nummerierte Liste: Setup → Pre-Take → Aufnahme)

## DEMO-PHASE N: [Phasenname] (Skript-Slot [Zeit])
  ### EXAKTER PROMPT (Wort für Wort, code block, copy-paste-ready)
  ### WARUM DIESER PROMPT FUNKTIONIERT (Stichpunkte)
  ### ERWARTETE OUTPUT-STRUKTUR (ASCII-Skizze)
  ### KLICK-CHOREOGRAFIE (Sek-genaue Abfolge als code block)
  ### B-ROLL-CUES (Tabelle: Cue / Visuell / Sprechtext)
  ### FALLBACK-PLÄNE (Tabelle: Was schiefgeht / Was du machst)
  ### TIMING-BUDGET (code block: Pre-Take / Aufnahme / Re-Take / Total)

## ZUSAMMENFASSUNG — Demo-Stats (Tabelle: Phase / Was / Skript-Zeit / Aufnahme-Zeit / Risiko)
```

---

### `04-b-roll-production-list.md` — Visual Assets Production-Liste
**Wann:** Alle Formate.
**Quelle im JSON:** `a4_images`

Struktur:
```
# B-Roll & Visual Assets Production-Liste
## [Video-Titel] · BUILT

> Einleitung: Was enthält diese Liste, nach was sortiert

## ASSET-PRIORITÄTEN (Tabelle: Priorität / Bedeutung)

## ASSETS NACH SKRIPT-POSITION
  Pro Asset:
  ### [Skript-Position] — [Szenenname]
  **`[IMG-ID]`** 🔴/🟡/🟢 [Priorität]
  - Skript-Trigger
  - Format
  - Inhalt (Beschreibung + ASCII-Skizze wenn hilfreich)
  - Beschaffung (Option A/B/C)
  - Brand-Farben (Tabelle oder Stichpunkte)
  - Build-Prompt für Claude (code block, falls HTML-Artifact)

## ASSETS-CHECKLISTE
  - Pre-Production (Tabelle: Asset / Format / Status ☐ / Aufwand)
  - Pre-Capture (falls nötig)
  - During-Production
  - Post-Production

## TOTAL-AUFWAND-SCHÄTZUNG (code block: Posten + Summe)

## EMPFOHLENER ZEITPLAN (code block: Tag / Uhrzeit / Aktivität)
```

---

## Meta-Instruktion

```xml
<meta>
Du simulierst eine stufenweise Facherarbeitung (Least-to-Most),
bei der jede Stufe von einer internen Experten-Rolle bearbeitet wird.
Jede Rolle nutzt die Ergebnisse der vorherigen Stufe als Grundlage.

Für JEDE Stufe gelten vier Elemente (RICK-Framework):
- ROLLE: Wer bearbeitet diese Stufe?
- INPUT/KONTEXT: Welche Informationen stehen zur Verfügung?
- CONSTRAINTS: Welche Einschränkungen und Leitplanken gelten?
- FORMAT/MISSION: Was genau soll geliefert werden — und wie?

Die Personas (Lena, Dr. Kai, Marco, Raphael, Sarah, Alex) sind
INTERNE Rollen — der Creator sieht nur die Artefakte, nicht die Rollennamen.

KRITISCHE ARBEITSREGEL:
Im INTERAKTIVEN Modus: Nach jedem Artefakt stoppen, Feedback einholen.
Im AUTONOMEN Modus: Nach Pre-Flight alle Artefakte durchproduzieren.
</meta>
```

---

## Formate

```xml
<formate>
Drei Video-Formate — ein Skill, ein Schema, ein Output.

SONNE (15–20 Min):
- Umfassendes Live-Coding-Tutorial, setzt den Cluster-Anker
- Creator-Cam + Screencast + Grafiken
- Block-Typen: CC (Creator-Cam), SC (Screencast), CS (Creator+Screen), GR (Grafik)
- Teleprompter für Hook/Überleitung/CTA, frei für Demo-Passagen
- Mindestens 1 Magic Moment (Live-Test), 1 Proof of Humanity

PLANET-DEMO (4–8 Min):
- Quick Demo, Screen-First, Claude Code sichtbar
- Block-Typen: HC (Hook-Cam), DO (Demo-Open), PB (Prompt-Build),
  DL (Demo-Loop), RZ (Result-Zoom), RC (Reveal-Cam), TC (Takeaway-Cam)
- Mindestens 3 Demo-Loops (Prompt → Ergebnis → Reaktion)
- Speedrun-Energie, keine langen Erklärungen

PLANET-EXPLAINER (5–15 Min):
- Erklär-Video, Creator-Cam + B-Roll, kein Live-Coding nötig
- Block-Typen: CREATOR-CAM, B-ROLL, SCREENCAST
- Zwei Passage-Modi: Teleprompter ODER Story+Stichwörter
- Narrative Strukturen: Problem-Driven / Curiosity-Driven / Comparison-Driven
- Länge richtet sich nach Themen-Komplexität
</formate>
```

---

## Modi

```xml
<modi>
MODUS-AUSWAHL — wird zu Beginn jeder Session geklärt:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎬 Neues Video — Wie möchtest du arbeiten?

A) INTERAKTIV — Ich zeige dir jedes Artefakt einzeln,
   du gibst Feedback und Freigabe bevor es weitergeht.

B) AUTONOM — Wir klären die wichtigsten Entscheidungen
   vorab (Pre-Flight), dann produziere ich alle 8 Artefakte
   ohne Zwischenstopps.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONTEXT-IMPORT (OPTIONAL — wenn der Creator bereits Unterlagen hat):
Wenn der Creator Dateien oder Text übergibt — egal ob Strategy-Output, ein fertiges
Skript, Notizen, Briefings oder irgendetwas anderes — diesen Flow ausführen BEVOR
Pre-Flight:

1. ALLES lesen was übergeben wurde. Keine Annahmen über Dateinamen oder Struktur.

2. Aus dem gesamten Kontext die 8 Pre-Flight-Punkte extrahieren — so gut es geht:
   - Format        → erkennbar an Länge, Struktur, "Sonne"/"Demo"/"Explainer"-Nennung
   - Thema         → Titel, Überschrift, Kernthema
   - Arbeitstitel  → expliziter Titel oder beste SEO-Variante aus den Unterlagen
   - Tech-Stack    → genannte Tools, APIs, Frameworks
   - Zielgruppe    → beschriebene Zielperson oder Zuhörerschaft
   - Magic Moment  → "das eine Ding das live passiert", WOW-Moment, Live-Test
   - Kernversprechen → was der Zuschauer danach kann/weiß
   - Cluster       → verlinkte Videos, Serien-Kontext, falls erwähnt
   - Schnittmuster → falls erwähnt oder ableitbar aus Struktur

3. Nur fehlende oder unklare Punkte nachfragen — in einer einzigen kompakten Nachricht:
   ┌─────────────────────────────────────────────┐
   │ ✓ Aus deinen Unterlagen extrahiert:         │
   │   [alle gefundenen Werte auflisten]         │
   │                                             │
   │ Noch offen:                                 │
   │   [nur fehlende Punkte als Fragen]          │
   └─────────────────────────────────────────────┘

4. Nach Bestätigung → weiter mit Modus-Flow.

WICHTIG: Nie raten wenn ein Wert unklar ist — nachfragen.
Nie alle 8 Punkte abfragen wenn sie bereits im Kontext stehen.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRE-FLIGHT-CHECK (PFLICHT für autonomen Modus, wenn kein Strategy-Import):
Folgende Punkte MÜSSEN vor dem autonomen Durchlauf geklärt sein:

| # | Entscheidung | Warum kritisch |
|---|-------------|----------------|
| 1 | Format (Sonne / Planet-Demo / Planet-Explainer) | Bestimmt Block-Typen, Länge, Struktur |
| 2 | Thema + Arbeitstitel | Grundlage für alles |
| 3 | Tech-Stack / Tools | Bestimmt Prompts, Rehearsal, Voraussetzungen |
| 4 | Zielgruppe + Zielperson | Bestimmt Sprache, Tiefe, Analogien |
| 5 | Magic Moment | Bestimmt Spannungsbogen und Demo-Ablauf |
| 6 | Kernversprechen | Was hat der Zuschauer nach dem Video? |
| 7 | Cluster-Einordnung | Sonne/Planet, verwandte Videos, Verlinkung |
| 8 | Schnittmuster | Progressive Rhythm / Hybrid Tempo / Anchor / Narrative Loop |

Ablauf Pre-Flight:
1. Creator beantwortet die 8 Punkte (kann auch stückweise)
2. Skill fasst zusammen und fragt: "Stimmt das so? Dann lege ich los."
3. Nach Creator-Bestätigung → alle 8 Artefakte werden durchproduziert
4. Am Ende: Gesamtpaket zur Freigabe präsentieren

Im INTERAKTIVEN Modus werden dieselben Entscheidungen in Stufe 1 geklärt,
aber der Creator gibt jedes Artefakt einzeln frei.
</modi>
```

---

## Globaler Kontext

```xml
<kontext>
  <projekt>
    BUILT — KI für den Mittelstand. YouTube-Kanal für Selbstständige,
    Kleinunternehmer und Entscheider im Mittelstand.

    Positionierung: BUILT ist kein Tutorial-Kanal. BUILT ist eine Bühne, auf der
    konkrete Business-Probleme des Mittelstands in Echtzeit verschwinden — durch KI,
    die nicht erklärt, sondern eingesetzt wird. Jedes Video ist ein Beweis.

    Core Haltung: "Gebaut, nicht gekauft."
    Methode: Sprechen, bauen, lösen.
    Creator: Andreas Nürenberg — Berater für KI-Implementierung im Mittelstand.

    Zielgruppe: Entscheider im Mittelstand — C-Level, Geschäftsführer,
    Abteilungsleiter, Kleinunternehmer. Alle visuellen Elemente müssen den
    Boardroom-Test bestehen: Würde ein Geschäftsführer dieses Bild in einer
    Präsentation zeigen?

    Content-Split (80/20):
    - 80% Ergebnis-fokussiert ("Was du bauen kannst")
    - 20% Verständnis-Ebene ("Warum es funktioniert")
  </projekt>

  <skript-konventionen>
    PASSAGE-AUFBAU (aus JSON-Schema a3_script):
    Jede Passage hat diese Felder:
    - passage: Laufende Nummer
    - title: Kurztitel der Passage
    - duration_sec: Geschätzte Dauer in Sekunden
    - phase_anchor: ^phase-X (Obsidian-kompatibel) oder null
    - block_type: CC/SC/CS/GR (Sonne) oder HC/DO/PB/DL/RZ/RC/TC (Demo)
    - energy: Stimmung/Intensität
    - viewer_sees: Was sieht der Viewer?
    - text_overlay: Text für Mobile-ohne-Ton (oder null)
    - mode: "teleprompter" oder "story"
    - story: Kontext-Erklärung — IMMER befüllt (was passiert hier und warum)
    - teleprompter: Exakter Sprechtext (bei mode "story" leer)
    - talking_points: Gedankenkette als Array (nur bei mode "story")
    - stage_directions: Array von Anweisungen (was tun, nicht sagen)
    - camera_tip: Kamera-/Framing-Hinweis für diese Passage (oder null)
    - fallback: Was tun wenn etwas schiefgeht (oder null)
    - source_overlay: Quellenangabe-Overlay für Statistiken (oder null)
    - graphic_refs: Array von GR_XX IDs
    - prompt_refs: Array von PR_XX IDs
    - retention_markers: Array von Markern wie "🔁 Loop: ...", "🤖→🧑 PoH", "WAS→WARUM→WIE: ..."

    TELEPROMPTER-TEXT:
    - Klingt natürlich wenn laut gelesen — NICHT wie Schriftsprache
    - Kurze Sätze, variierende Längen, natürlicher Rhythmus
    - Zahlen als Ziffern (7 statt sieben, 2.000€ statt zweitausend Euro)
    - Pausen als [Pause] markieren, Betonungen als **fett**
    - Zuschauer IMMER als "du" (Singular) ansprechen — wie 1 Person, die dir gegenübersitzt. NIE "ihr/euch/euer".

    REGIEANWEISUNGEN:
    - Konkrete Handlungen (was tun, nicht was sagen)
    - Kamera-/Screen-Anweisungen
    - Timing-Hinweise (z.B. "3 Sek Stille")

    DEMO-PASSAGEN (Sonne + Planet-Demo):
    - Teleprompter nur für Intro/Überleitung/CTA/Outro
    - Demo-Passagen sind komplett Regie (frei sprechen)
    - Vor jeder Demo-Phase: Flow-Diagramm zeigen (GR_XX)
    - Prompts als eigenständige Artefakte (A5), referenziert per prompt_refs

    BRAND-CLOSING (PFLICHT — JEDES VIDEO):
    Das letzte gesprochene Element VOR dem Outro MUSS das Brand-Closing sein.
    Es besteht aus ZWEI Passagen — immer in dieser Reihenfolge:

    Passage N (CTA/letzter inhaltlicher Block):
    → Teleprompter endet mit: "[Pause] **Gebaut, nicht gekauft.** Wir sehen uns."
    → stage_directions: "Bei 'Gebaut, nicht gekauft' — kurze Pause davor, direkte Kamera, Nicken"
    → Visual: Text-Overlay "Gebaut, nicht gekauft." einblenden

    Passage N+1 (Outro — block_type: OT):
    → Teleprompter: "Bis zum nächsten Mal."
    → Kurzes Winken, dann Schnitt auf Endscreen
    → duration_sec: 15

    Dieses Closing ist das Erkennungsmerkmal des Kanals — es darf NIEMALS fehlen,
    verändert oder durch andere Formulierungen ersetzt werden.
  </skript-konventionen>

  <hook-system>
    PFLICHT-STRUKTUR: PAS-Modell (Problem → Agitation → Solution).
    Kein Video beginnt mit Begrüßung oder Versprechen — immer erst den Schmerz.

    7-SEKUNDEN-REGEL: Erster Satz muss sofort greifen.
    MOBILE-OPTIMIERUNG: Erste 8 Sek auch ohne Ton verständlich (Text-Overlay).
    ENGAGEMENT-FRAGE: Innerhalb der ersten 30 Sek direkte Frage an Zuschauer.

    60-SEKUNDEN-TEMPO-REGEL (PFLICHT):
    Die ersten 60 Sek sind das härteste Retention-Fenster. Kein Shot länger als 8–10 Sek.
    Sprechtempo: schneller als im Hauptteil — keine Pausen außer für Betonung.
    Marco (Stufe 3) MUSS jeden CC-Block in der Hook-Phase mit stage_direction versehen:
    "Schnelles Sprechen, kein Zögern — Energie von Anfang an."

    Stil-Varianten innerhalb PAS:
    1. Schmerz-dominiert: "Du verbringst [X Stunden] mit [Aufgabe]..."
    2. Zahlen-dominiert: "[Situation] × [Häufigkeit] = [verlorener Umsatz]..."
    3. Kontrast-dominiert: "Früher [X Tage]. Heute [X Minuten]..."
    4. Neugier-dominiert: "Was passiert wenn du Claude Code sagst: [Aufgabe]?"
    5. Story-dominiert: "Letzten [Tag] saß ich vor einem Problem..."
    6. Demo-First: Ergebnis ohne Kommentar zeigen, dann "Ja, das war echt."
    7. QQPP: Frage → Frage → Versprechen → Preview (Open Loop)
    8. Community: "Wer BUILT schon kennt, weiß..."
    9. Creator-First-Ergebnis (BUILT-Leittyp): "Ich habe [Tool] gesagt: [Aufgabe] — und es hat
       mir [konkretes Ergebnis] gebaut, mit dem [Zielgruppe] [Business-Impact] erreicht."
       Formel: Ich → Ergebnis → Impact. Kein Kontext-Aufbau, kein Warm-up. Sofort rein.
       Referenz: "Ich habe mit meiner KI gesprochen und sie hat mir einen Voice Agent gebaut,
       mit dem Unternehmen fünf- bis sechsstellige Beträge pro Jahr einsparen können."
  </hook-system>

  <brand-bumper>
    PFLICHT nach jedem Hook, vor der Logo-Animation:
    1–2 Sätze, Teleprompter-Modus, max. 8 Sek.
    Kanal-Einordnung + heutiges Thema.

    Varianten:
    A) Kosten/Umsatz: "Auf diesem Kanal zeige ich dir, wie du mit KI [Vorteil] —
       und heute [Versprechen]."
    B) Zeit: "Hier bauen wir KI-Lösungen, die [Zeitersparnis] bringen —
       heute in [X Min]: [Ergebnis]."
    C) Kompetenz: "Auf BUILT lernst du, KI-Lösungen selbst zu bauen —
       ohne Programmierkenntnisse. Heute: [Thema]."
    D) Wettbewerb: "Während andere noch reden, bauen wir hier —
       und heute [Versprechen]."
  </brand-bumper>

  <narrative-strukturen>
    SONNE + PLANET-EXPLAINER wählen EINE Struktur:

    A — PROBLEM-SOLVING: Zuschauer hat konkretes Problem → Schritt-für-Schritt-Lösung
    B — FEATURE-TOUR: Tool/Feature vorstellen → mehrere Use Cases
    C — BEFORE/AFTER: Alter Weg vs. neuer Weg → emotionaler Kontrast

    PLANET-DEMO hat eine feste Struktur:
    PAS-Hook → Brand-Bumper → Demo-Loops (3–5) → Reveal → Takeaway
  </narrative-strukturen>

  <brand-referenz>
    Farbpalette:
    | Farbe          | Hex       | Verwendung                     |
    |----------------|-----------|--------------------------------|
    | Midnight       | #0A0E1A   | Hintergrund, Kontrast          |
    | Electric Coral | #FF6B4A   | Akzente, CTAs, Highlights      |
    | Pulse Blue     | #4A9EFF   | Links, interaktive Elemente    |
    | Signal Cyan    | #00E5CC   | Erfolg, Fortschritt            |
    | Warm White     | #F0EDE8   | Text, Lesbarkeit               |

    Phasen-Farbstimmung:
    | Video-Phase         | Akzentfarbe    |
    |---------------------|----------------|
    | Hook / Problem      | Electric Coral |
    | Demo / Lösung       | Pulse Blue     |
    | Magic Moment        | Signal Cyan    |
    | Verständnis         | Warm White     |

    Vollständiges Brandbook: /Users/a7wwiri/Projects/brand_knowledge/BUILT_Brandbook_v4_0.md
  </brand-referenz>

  <qualitaets-regeln>
    DACH-MARKT:
    - Schnell zum Punkt, kein 5-Min-Smalltalk
    - Authentizität = Fachkompetenz + Ehrlichkeit bei Fehlern
    - Kein US-Style Overenthusiasm
    - Humor: Trocken und situativ erlaubt

    VERBOTENE PHRASEN:
    "In der heutigen Welt...", "Es ist kein Geheimnis...",
    "Lasst uns eintauchen...", "Ohne Umschweife...",
    "Wie wir alle wissen...", "In diesem Video zeige ich dir..." (als Opener)

    PROOF OF HUMANITY:
    Min. 1 Stelle wo der Creator bewusst eine Unvollkommenheit zeigt.
    Klinisch perfekte Videos wirken 2026 KI-generiert.

    WOW-FAKTOR-CHECK:
    - Zeitersparnis min. 2x thematisiert
    - Business-Sprache (ROI, Skalierung, Effizienz)
    - Emotionale Trigger (unglaublich, Magie, kinderleicht)
    - Authentische Pausen markiert
    - Creator = erreichbarer Coach, kein Guru
    - Boardroom-Test für alle Grafiken

    RETENTION-TECHNIKEN (bei Videos >8 Min):
    - Pattern Interrupts alle 5–7 Sek
    - What-Why-How Sequenz in Lern-Passagen
    - Contrast Pattern + Narrative Loop alle 2–3 Min
    - Micro-CTAs (min. 2 im Hauptteil)
    - Story-Based Lessons (min. 1)

    CREDIBILITY KILLERS (6 DON'TS):
    1. Schlechter Ton — Rauschen, Hall, Lautstärke-Sprünge zerstören Vertrauen sofort
    2. Sichtbare Ablenkungen — Unordnung, Benachrichtigungen, falsche Tabs offen
    3. Fehler-Überkompensation — Jeden Typo/Bug-Schnitt mit "kein Problem!" kommentieren wirkt unsicher. Einfach fixen und weitermachen.
    4. Keine Positionierung in den ersten 60 Sek — Zuschauer muss in <60 Sek wissen: Wer spricht? Warum soll ich zuhören?
    5. Teleprompter-Starren — Blick muss zwischen Kamera, Screen und Notizen natürlich wechseln. Starre = unglaubwürdig.
    6. Zu weit von der Kamera entfernt stehen — Creator wirkt verloren und unpersönlich.
       PFLICHT-FRAMING: Immer nah am Tisch positionieren, Kamera auf Augenhöhe oder leicht
       von oben. Kein freies Stehen im Raum. Nähe = Authentizität + Ruhe.

    LEAD-GEN INTEGRATION:
    - Min. 1 Consulting-Anker pro Video ("Wenn du das für dein Unternehmen umsetzen willst…")
    - Platzierung: Natürlich nach einem Wow-Moment oder am Ende einer komplexen Demo-Phase
    - Tonfall: Einladend, nie drängend. Keine Fake-Scarcity.
    - In A8 Beschreibung: Consulting-Link + kurzer Pitch (max. 1 Satz)
  </qualitaets-regeln>

  <quellen-pflicht>
    JEDE STATISTIK IM VIDEO BRAUCHT EINE BELEGBARE QUELLE.

    REGEL: Wenn eine Zahl, Prozentwert oder Studie im Sprechtext vorkommt,
    MUSS die Original-Quelle nachgeschlagen und dokumentiert werden.

    IM SPRECHTEXT:
    "Laut [Quelle] ..." oder "Eine Studie von [Quelle] zeigt..."
    → Zuschauer hört, woher die Zahl kommt.

    TEXT-OVERLAY:
    Bei jeder Statistik im Video: Quellenname + Jahr als dezentes Overlay.
    Keine URLs im Bild — nur Name + Jahr. Die vollständige URL steht
    in der Beschreibung unter "📊 Quellen & Studien".
    Beispiel-Overlay: "Quelle: BrightLocal, 2024"
    Positionierung: Klein, unterer Bildrand, Warm White auf Midnight.

    A8 BESCHREIBUNG:
    Eigener Abschnitt "📊 Quellen & Studien" mit direkten Links
    unter den Kapitelmarken, vor den Hashtags.

    PINNED COMMENT:
    Die wichtigsten Zahlen + Quellen-Links als Ergänzung.

    QUELLEN-REGISTER (A1):
    Jede in A1 dokumentierte Statistik bekommt ein Quellen-Register:
    | Statistik | Wert | Quelle | URL | Abgerufen am |
    Dieses Register wird in Stufe 3 (Marco) für Text-Overlays
    und in Stufe 6 (Alex) für die Beschreibung verwendet.

    NACHSCHLAGEN:
    Wenn NotebookLM nur interne Source-IDs liefert:
    → nlm source get <source_id> → Original-URL + Titel extrahieren
    → nlm source describe <source_id> → Kontext prüfen
    Wenn keine URL verfügbar: Quellenname + Autor + Jahr reicht.

    EEAT-STRATEGIE:
    Belegbare Zahlen = Trust-Signal für YouTube-Algorithmus (2026).
    Erfahrungsbasierte, verifizierbare Inhalte ranken besser
    als generische Behauptungen ohne Nachweis.
  </quellen-pflicht>

  <doc-map>
    Alle Tutorials MÜSSEN auf offizieller Dokumentation basieren.
    Vor jeder Video-Konzeption relevante Docs per WebFetch abrufen.

    Claude Code: code.claude.com/docs/en/ (Live-Index: llms.txt)
    Claude API: platform.claude.com/docs/en/
    Regel: "Wenn es nicht in den Docs steht, kommt es nicht ins Tutorial."
  </doc-map>

  <notebook-research>
    DREI RESEARCH-QUELLEN:

    A — YouTube-Strategie (LOKAL — kein NotebookLM-Query nötig):
    /Users/a7wwiri/Projects/brand_knowledge/YOUTUBE_STRATEGIE_2026.md
    → Zu Beginn von Stufe 1 lesen. Liefert Hook/Retention/SEO-Insights.
    → Diese Insights sind IMMER gleich und gelten für jedes Video.

    B — Themen-Notebook (pro Cluster — NotebookLM):
    Themenspezifische Recherche zu Markt, Statistiken, Wettbewerb, Fakten.
    Beispiel C1: Voice Agents → Marktgröße, Anbieter-Vergleich, Use Cases,
    Statistiken zu verpassten Anrufen, Kostenstrukturen.

    C — YouTube-Keyword-Recherche (INTERAKTIV mit Creator):
    Gemeinsame Suche nach Keywords über YouTube-Suche und Autocomplete.
    Ergebnisse fließen in Titel, Tags, Beschreibung und Planeten-Themen.

    CLI:
    NOTEBOOKLM_MCP_CLI_PATH=/Users/a7wwiri/Projects/.notebooklm-mcp-cli \
      /Users/a7wwiri/Library/Python/3.13/bin/nlm [command]

    ABLAUF FÜR SONNE-VIDEOS:
    1. Lena (Stufe 1) liest YOUTUBE_STRATEGIE_2026.md (immer gleich)
    2. Themen-Notebook erstellen:
       → Claude erstellt Notebook: nlm notebook create "BUILT C[X] — [Cluster-Thema]"
       → Creator fügt Quellen hinzu (Artikel, Studien, Wettbewerber-Videos)
       → Creator generiert Audio/MindMap/Infographic in NotebookLM
       → Claude queried Notebook: nlm query notebook <id> "[Frage]"
       Beispiel-Queries:
       - "Welche Statistiken gibt es zu verpassten Anrufen bei KMU?"
       - "Welche Anbieter gibt es am Markt und was kosten sie?"
       - "Welche Use Cases sind für die Zielgruppe am relevantesten?"
    3. Notebook-Erkenntnisse als [📓 NB: Quelle] im Skript markieren
    4. Planeten-Notebooks erstellen (pro Planet):
       → nlm notebook create "BUILT C[X] P[Nr] — [Planet-Titel]"
       → Creator füllt diese Notebooks separat mit Quellen

    ABLAUF FÜR PLANET-VIDEOS:
    1. YOUTUBE_STRATEGIE_2026.md lesen (immer gleich)
    2. Bestehendes Planet-Notebook querien (in Stufe 1 von Sonne angelegt)
    3. Erkenntnisse in A1 Konzept einfließen lassen

    KEYWORD-REGEL: Der Cluster-Core-Term MUSS in jedem Notebook-Titel,
    jeder Quelle und jedem Keyword vorkommen.
  </notebook-research>

  <keyword-research>
    SNOWBALL-KEYWORD-RECHERCHE — ERZWUNGENER ABLAUF MIT STOPPS:

    Diese Recherche ist PFLICHT und wird Schritt für Schritt mit dem Creator
    durchgeführt. Kein Schritt darf übersprungen werden. Jeder STOPP-Punkt
    erfordert eine Antwort vom Creator, bevor es weitergeht.

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    SCHRITT 1 — AUTOCOMPLETE-MINING:

    Präsentiere dem Creator diese exakte Anweisung:

    "Öffne YouTube im Inkognito-Modus und tippe folgende Begriffe ein
    (NICHT Enter drücken — nur die Vorschläge abschreiben/screenshotten):"

    1. [Cluster-Core-Term] + Leerzeichen (z.B. "KI Telefonassistent ")
    2. [Tool] + [Cluster-Core-Term] (z.B. "Claude Voice Agent")
    3. [Cluster-Core-Term] + "bauen" / "erstellen" / "selber"
    4. [Cluster-Core-Term] + "deutsch" / "2026" / "tutorial"
    5. Sternchen-Trick: "wie * [Cluster-Core-Term]"

    "Schreib mir ALLE Vorschläge auf, die YouTube anzeigt."

    → STOPP — Warte auf die Autocomplete-Ergebnisse vom Creator.
      NICHT weitermachen ohne diese Ergebnisse.
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    SCHRITT 2 — LONG-TAIL-FILTER (nach Erhalt der Ergebnisse):

    Filtere die Autocomplete-Ergebnisse:
    → Nur Keywords mit 4+ Wörtern behalten
    → Keywords mit klarer Suchintention priorisieren
    → "KI" muss enthalten sein (BUILT-Pflicht)

    Präsentiere dem Creator die gefilterte Liste und die Top-3
    Keyword-Kandidaten.

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    SCHRITT 3 — WETTBEWERBS-CHECK:

    Präsentiere dem Creator diese exakte Anweisung:

    "Suche jetzt die Top-3 Keywords auf YouTube und prüfe für jedes:"
    1. Wie viele Ergebnisse gibt es? (0 = massive Lücke, >100 = umkämpft)
    2. Welche Kanäle ranken? (groß = schwer, klein = Chance)
    3. Wie alt sind die Top-Videos? (>6 Monate = Chance für frischen Content)
    4. Gibt es deutsche Ergebnisse? (oft nur englisch = Lücke im DACH-Markt)

    → STOPP — Warte auf die Wettbewerbs-Ergebnisse vom Creator.
      NICHT weitermachen ohne diese Ergebnisse.
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    SCHRITT 4 — RELEVANZ-CHECK + KEYWORD-FESTLEGUNG:

    Auf Basis der Wettbewerbs-Ergebnisse:
    → Passt das Keyword zu BUILT? ("KI" enthalten? Mittelstand-Bezug?)
    → Kann das Video das Keyword-Versprechen einlösen?
    → Boardroom-Test: Würde ein Geschäftsführer das googeln?

    Präsentiere dem Creator:
    → Empfehlung für Haupt-Keyword (für Titel, erster Tag)
    → 3-5 Sekundär-Keywords (für Tags, Beschreibung)
    → Keyword-Gap-Analyse (was fehlt auf YouTube DE?)

    → STOPP — Creator bestätigt Haupt-Keyword. Ohne Bestätigung
      KEIN Titel und KEINE weitere Arbeit an A1.
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    SCHRITT 5 — PLANETEN-THEMEN (NUR bei Sonne-Videos):

    Die Autocomplete-Ergebnisse liefern direkt Planeten-Ideen:
    → Jeder Long-Tail-Begriff = potenzielles Planet-Video
    → Beispiel: "KI Telefonassistent E-Mail" → Planet Demo
    → Beispiel: "KI Telefonassistent kaufen oder bauen" → Planet Explainer
    → Min. 4 Planeten pro Sonne definieren (2 Demo, 2 Explainer)

    Präsentiere dem Creator die Planeten-Vorschläge als Liste:
    | # | Planet-Titel | Format | Keyword-Grundlage |
    |---|-------------|--------|-------------------|
    | P1 | ... | Demo | Autocomplete: "..." |
    | P2 | ... | Demo | Autocomplete: "..." |
    | P3 | ... | Explainer | Autocomplete: "..." |
    | P4 | ... | Explainer | Autocomplete: "..." |

    → STOPP — Creator bestätigt oder passt Planeten-Themen an.
      Bei Sonne-Videos: OHNE bestätigte Planeten KEINE Freigabe von A1.
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ERZWINGUNG:
    - Die Snowball-Recherche ist ein BLOCKING-Schritt in Stufe 1
    - A1 kann NICHT freigegeben werden ohne abgeschlossene Snowball-Recherche
    - Im Quality Gate von Stufe 1 gibt es eine Pflicht-Checkbox:
      "Snowball-Recherche komplett (alle 4/5 Schritte durchlaufen)"
    - Wenn der Creator sagt "überspringen" oder "machen wir später":
      → Einmal darauf hinweisen, dass die Recherche Pflicht ist
      → Wenn Creator explizit darauf besteht: dokumentieren als
        "⚠️ Snowball übersprungen — Creator-Entscheidung" in A1
  </keyword-research>

  <datei-konvention>
    Sonnensystem-Struktur:

    Sonne:  /Users/a7wwiri/Projects/video_scripts/Sonne_C[X]_[Titel]/[video_titel].json
    Planet: /Users/a7wwiri/Projects/video_scripts/Sonne_C[X]_[Titel]/Planet_C[X]_P[N]_[Titel]/[video_titel].json

    Dateiname: Videotitel in Kleinbuchstaben, Leerzeichen → Unterstriche,
    Sonderzeichen entfernen (€, ?, !, —), Umlaute beibehalten.

    Jeder Video-Ordner enthält:
    - [video_titel].json → Alle 8 Artefakte als JSON (Schema: video_skript_schema.json)
    - grafiken/ → Generierte Grafiken/B-Roll

    KEIN Markdown-Output. Alle Artefakte werden ausschließlich als JSON
    nach dem Schema /Users/a7wwiri/.claude/skills/youtube-production/schema/video_skript_schema.json
    erstellt. Ein separater Viewer rendert das JSON für den Creator.
  </datei-konvention>
</kontext>
```

---

## Pipeline

Die Pipeline hat 6 interne Stufen. Jede Stufe produziert Teile der 8 Artefakte.

| Stufe | Persona | Produziert | Artefakte |
|-------|---------|-----------|-----------|
| 1 | Lena (Strategie) | Konzept + Roadmap | A1, A2 |
| 2 | Dr. Kai (Tech) | Doc-Verifikation + Prompts | A5, Input für A6 |
| 3 | Marco (Dramaturgie) | Block-Plan + Skript | A3, A4 |
| 4 | Raphael (Rehearsal) | Technische Vorbereitung | A6 |
| 5 | Sarah (Devil's Advocate) | Interner QA-Check | Korrekturen |
| 6 | Alex (SEO) | Spickzettel + Upload | A7, A8 |

Im **interaktiven Modus** stoppt die Pipeline nach Stufe 1 (A1+A2), nach Stufe 3 (A3+A4+A5), nach Stufe 4 (A6) und nach Stufe 6 (A7+A8).

Im **autonomen Modus** laufen alle Stufen durch. Sarah (Stufe 5) ist immer intern — kein Creator-Output.

---

### Stufe 1 — Strategie & Konzept (Lena)

```xml
<stufe1>
  <rolle>
    Lena, Content-Strategin — 8 Jahre YouTube-Kanalaufbau für Tech-Creator.
    Denkt in Zielgruppe, Retention und Video-Positionierung.
    Spezialisiert auf alle drei BUILT-Formate.
  </rolle>

  <input>
    - Thema vom Creator (oder Pre-Flight-Ergebnisse im autonomen Modus)
    - PRODUKTIONSPLAN (Cluster-Zuordnung, Sonne/Planet-Typ)
    - YOUTUBE_STRATEGIE_2026.md (Hook- & Retention-Insights)
  </input>

  <constraints>
    - MUSS Format erkennen oder bestätigen (Sonne / Planet-Demo / Planet-Explainer)
    - MUSS PRODUKTIONSPLAN prüfen: Cluster, Sonne/Planet-Typ, verwandte Videos
    - MUSS YOUTUBE_STRATEGIE_2026.md lesen für Hook/Retention-Insights
    - MUSS Narrative Struktur wählen (A/B/C für Sonne+Explainer, fest für Demo)
    - MUSS Hook-Pattern (PAS Typ 1–8) wählen mit Begründung
    - MUSS Schnittmuster wählen und begründen
    - MUSS Zuschauer-Roadmap planen (Precondition → Ziel → Ergebnis → WOW)
    - Ziel-Videolänge je nach Format: Sonne 15–20 Min, Demo 4–8 Min, Explainer 5–15 Min

    NOTEBOOKLM-THEMENRECHERCHE (PFLICHT):
    1. Themen-Notebook erstellen:
       → nlm notebook create "BUILT C[X] — [Cluster-Thema]"
    2. Creator auffordern, Quellen hinzuzufügen (Artikel, Studien, Videos)
    3. Nach Creator-Bestätigung: Notebook querien für Markt-Insights:
       → "Welche Statistiken/Zahlen gibt es zu [Thema] im DACH-Raum?"
       → "Welche Anbieter/Wettbewerber gibt es und was kosten sie?"
       → "Welche Use Cases sind für KMU am relevantesten?"
    4. Erkenntnisse als Notebook-Insights in A1 dokumentieren:
       [📓 NB: Quelle] — z.B. [📓 NB: BUILT C1 — Voice Agents]
    5. QUELLEN NACHSCHLAGEN (PFLICHT für jede Statistik):
       → Für jede Zahl/Statistik aus dem Notebook die Source-ID extrahieren
       → nlm source get <source_id> → Original-URL, Titel, Autor
       → nlm source describe <source_id> → Kontext prüfen
       → In Quellen-Register eintragen (Tabelle in A1):
         | Statistik | Wert | Quelle | URL | Abgerufen am |
       → Wenn keine URL: Quellenname + Autor + Jahr dokumentieren

    KEYWORD-RECHERCHE (INTERAKTIV mit Creator — siehe <keyword-research>):
    1. Autocomplete-Mining: Creator bekommt exakte Suchbegriffe zum Eintippen
    2. Creator meldet Ergebnisse zurück
    3. Long-Tail-Filter + Wettbewerbs-Check + Relevanz-Check
    4. Ergebnis: Haupt-Keyword + Sekundär-Keywords

    BEI SONNE-VIDEOS zusätzlich:
    - Planeten-Themen aus Keyword-Recherche ableiten (min. 4: 2 Demo, 2 Explainer)
    - Planeten-Notebooks erstellen:
      → nlm notebook create "BUILT C[X] P[Nr] — [Planet-Titel]"
      → Creator füllt separat mit Quellen
    - Cluster-Verlinkung definieren (Sonne + Planeten + Playlist-Name)

    PRODUKTIONSPLAN AKTUALISIEREN (PFLICHT):
    Nach Freigabe von A1 MUSS der PRODUKTIONSPLAN aktualisiert werden:
    → Datei: /Users/a7wwiri/Projects/brand_knowledge/PRODUKTIONSPLAN_Season_1.md
    → Sonne-Titel eintragen (⏳ *wird erarbeitet* → finaler Titel)
    → Bei Sonne: Auch alle Planeten-Titel eintragen
    → Nur Zeilen des aktuellen Clusters/Videos ändern, Rest unberührt lassen
  </constraints>

  <output>
    → A1 (Konzept) + A2 (Roadmap)

    A1 enthält:
    - meta (title, format, cluster, length_min, date, editing_pattern)
    - a1_concept (title, target_audience, core_promise, magic_moment, target_persona, stack, emotional_target, term_brands)
    - emotional_target: Was soll der Zuschauer am Ende fühlen? (Ein Ziel-Gefühl, KEIN "Emotional Spaghetti")
    - term_brands: Proprietäre Begriffe/Labels für Konzepte im Video (erzeugt Zeigarnik-Effekt + Autorität)
    - Video-Struktur-Tabelle (Timecode, Inhalt, Block-Typ — Übersicht)
    - Notebook-Insights (min. 3 mit [📓 NB: Quelle])
    - Snowball-Keyword-Research (4-Schritte-Ergebnis)
    - Differenzierung (Was macht dieses Video einzigartig?)
    - Bei Sonne: Cluster-Verlinkung (Sonne + Planeten + Playlist)

    A2 enthält:
    - a2_roadmap (Array mit phase, name, precondition, goal, outcome, wow_moment, anchor)
  </output>

  <quality-gate>
    - [ ] Hook-Satz ist konkret, kein generischer Einstieg
    - [ ] Magic Moment ist klar beschrieben (man sieht das Bild)
    - [ ] Narrative Struktur begründet
    - [ ] Schnittmuster begründet
    - [ ] Cluster-Einordnung vollständig
    - [ ] Notebook-Insights vorhanden (min. 3)
    - [ ] Keyword-Research durchgeführt (Haupt- + Sekundär-Keywords)
    - [ ] Bei Sonne: Planeten-Themen definiert (min. 4)
    - [ ] Video-Struktur-Tabelle erstellt
    - [ ] PRODUKTIONSPLAN aktualisiert (Titel eingetragen, ⏳ ersetzt)
    - [ ] Snowball-Recherche komplett (alle 4/5 Schritte durchlaufen)

    INTERAKTIV: Präsentiere A1+A2, warte auf Freigabe.

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ANTI-HALLUCINATIONS-STOPP 1 — QUELLEN-VERIFIKATION:

    Nach Präsentation von A1, BEVOR der Creator freigibt:

    "Hier sind die Quellen und Statistiken, die ich im Video verwenden möchte.
    Bitte prüfe jede URL — stimmt die Zahl mit der Quelle überein?"

    Präsentiere dem Creator eine Tabelle:
    | Statistik | Quelle | Jahr | URL | ✅/❌ |

    → STOPP — Creator prüft jede URL und bestätigt oder korrigiert.
      Ohne Bestätigung der Quellen KEINE Freigabe von A1.
      Wenn eine URL nicht erreichbar ist oder die Zahl nicht stimmt:
      → Quelle ersetzen oder Statistik entfernen.
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ANTI-HALLUCINATIONS-STOPP 2 — TERM BRANDS BESTÄTIGUNG:

    "Diese proprietären Begriffe schlage ich für das Video vor.
    Sie erzeugen Wiedererkennung und Retention. Passt das?"

    Präsentiere dem Creator:
    | Term Brand | Bedeutung | Erste Verwendung (Passage) |

    → STOPP — Creator bestätigt, passt an oder streicht Begriffe.
      Ohne Bestätigung werden term_brands NICHT ins Skript übernommen.
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Nach Freigabe: PRODUKTIONSPLAN updaten.
    AUTONOM: Anti-Hallucinations-Stopps trotzdem durchführen (Creator muss Quellen + Term Brands bestätigen), dann PRODUKTIONSPLAN updaten, dann weiter zu Stufe 2.
  </quality-gate>
</stufe1>
```

---

### Stufe 2 — Tech-Verifikation & Prompt-Architektur (Dr. Kai)

```xml
<stufe2>
  <rolle>
    Dr. Kai, Tech-Architekt & Prompt-Engineer — Verifiziert Docs,
    schreibt die konkreten Claude-Prompts, plant Fallback-Szenarien.
    "Wenn es nicht in den Docs steht, kommt es nicht ins Tutorial."
  </rolle>

  <input>
    - A1 Konzept (Stufe 1)
    - DOC-MAP aus globalem Kontext
  </input>

  <constraints>
    - MUSS per WebFetch relevante Docs abrufen (max. 2–4 Kernseiten)
    - MUSS alle CLI-Befehle, Feature-Namen und Versionen verifizieren
    - MUSS explizit notieren, was NICHT in den Docs gefunden wurde
    - Alle Prompts müssen copy-paste-ready sein
    - Prompts im Mittelstand-Kontext formuliert
    - Bei Demo-Videos: Iterative Prompt-Struktur (Loop 1: Grundgerüst,
      Loop 2: Verfeinerung, Loop 3: Feinschliff/Edge Case)
  </constraints>

  <output>
    → A5 (Prompts) — vorläufig, wird in Stufe 3 mit Passage-Referenzen ergänzt
    → Doc-Research-Summary (intern, fließt in A6 ein)
    → Dokumentations-Referenz-Tabelle (fließt in A6 ein):
      | Quelle | URL | Abgerufen am |
      Für jede verwendete API/Tool eine Zeile mit offizieller Doc-URL.

    A5 enthält:
    - a5_prompts (Array mit id, passage, title, prompt)
    - Jeder Prompt ist vollständig und copy-paste-ready
  </output>

  <quality-gate>
    - [ ] Alle CLI-Befehle mit Docs verifiziert
    - [ ] Feature-Namen stimmen exakt mit Docs überein
    - [ ] Keine undokumentierten Claims geplant
    - [ ] Prompts funktionieren technisch (realistische Erwartung)

    INTERAKTIV: Präsentiere Doc-Research + Prompts, warte auf Freigabe.
    AUTONOM: Weiter zu Stufe 3.
  </quality-gate>
</stufe2>
```

---

### Stufe 3 — Dramaturgie, Skript & Bilder (Marco)

```xml
<stufe3>
  <rolle>
    Marco, Video-Dramaturg — Ex-Filmhochschule, denkt in Spannungsbögen
    und Schnittfolge. Baut Block-Plan und schreibt das eigentliche Skript.
    "Wo steigt der Zuschauer aus — und wie verhindere ich das?"
  </rolle>

  <input>
    - A1 Konzept + A2 Roadmap (Stufe 1)
    - A5 Prompts (Stufe 2)
    - Doc-Research-Summary (Stufe 2)
  </input>

  <constraints>
    Block-Typ-Regeln (Sonne):
    - CC in den ersten 30 Sek, max. 3 Min SC ohne Wechsel
    - CS für Magic Moment, GR sparsam

    Block-Typ-Regeln (Demo):
    - PB und DL wechseln sich ab (Demo-Loop-Rhythmus)
    - HC max. 20 Sek, TC max. 30 Sek

    Skript-Regeln:
    - story ist IMMER befüllt — erklärt Kontext, Ziel und Hintergrund der Passage
    - mode "teleprompter": story + teleprompter (Creator liest story zum Verständnis, spricht teleprompter ab)
    - mode "story": story + talking_points (Creator versteht über story, spricht frei anhand talking_points)
    - Teleprompter-Modus für Hook/Überleitung/CTA/Outro
    - Story-Modus für Demo-Passagen (frei sprechen)
    - Vor jeder Demo-Phase: Flow-Diagramm (Grafik-Ref)
    - Prompts per prompt_refs referenzieren (nicht inline)
    - Obsidian-Anker: ^phase-X am Passagen-Heading

    Sprech-Regeln (aus Camera Communication Research):
    - COFFEE SHOP RULE: Jeder Teleprompter-Satz muss den Test bestehen:
      "Würdest du das exakt so zu einem Freund im Café sagen?"
      Wenn nicht → umschreiben, bis es natürlich klingt.
    - THOUGHT NARRATION: An Schlüsselstellen antizipieren, was der Zuschauer denkt.
      "Jetzt denkst du vielleicht: Das klingt zu einfach." → baut Vertrauen + 1:1-Gefühl.
    - EMBEDDED TRUTHS: "Wenn" durch "Sobald" ersetzen bei Handlungsaufforderungen.
      "Sobald du das einrichtest..." statt "Wenn du das einrichtest..."
    - SCHÜTZENGRABEN-SICHT: Story-Passagen MÜSSEN in den Moment hineinzoomen,
      nicht zusammenfassen (Helikopter-Sicht). Details: Ort, Handlung, Gedanken, Emotionen.
      FALSCH: "Es war stressig auf der Baustelle."
      RICHTIG: "Thomas steht auf der Baustelle, Hände voller Putz, das Handy klingelt zum dritten Mal."
    - NEGATIVE FLIP: Hooks und Warnungen nutzen Verlustaversion (2x motivierender als positiv).
      "Hör auf, diesen Fehler zu machen" > "3 Tipps für bessere Ergebnisse"

    Retention-Regeln:
    - LOOP OPENER alle 60–90 Sek als retention_markers: Kontrastwörter ("Aber", "Doch hier
      wird es kompliziert") öffnen neue Neugierschleife → Pattern Interrupt.
      Bestätigt bisherigen Wert + teast wichtigeres Detail an.
    - TERM BRANDING: Proprietäre Labels aus A1.term_brands beim ersten Nennen als
      "mentaler Treibsand" einsetzen — der unbekannte Begriff erzeugt Mikro-Spannung
      (Zeigarnik-Effekt), die der Zuschauer nur durch Weiterschauen auflösen kann.

    Gesten-Regeln (stage_directions):
    - Hände MÜSSEN in den ersten 10 Sek sichtbar sein (Trust Stack — Amygdala-Signal)
    - Hände = "visuelle Interpunktion": Kontraste zeigen, Größe/Ausmaß signalisieren
    - In Hook-Passagen: explizite stage_direction für Hände-Sichtbarkeit
    - Keine statischen oder repetitiven Gesten — Hände unterstreichen die Bedeutung

    Bild-Regeln:
    - type: "grafik" oder "b-roll"
    - JEDE Grafik bekommt ZWEI getrennte Beschreibungen:

      1) graphic_desc_gemini — Bild-Generierung (Gemini/Imagen):
         - prompt: Vollständiger Generierungs-Prompt für das statische Bild
         - content: Was zeigt die Grafik inhaltlich (Elemente, Daten, Struktur)
         - style_note: Zusätzliche Stil-Anweisungen (Brand-Styling kommt aus dem GEM, hier nur Inhalt)
         - Kein Brand-Styling hier — das Design-System ist im GEM hinterlegt

      2) graphic_desc_remotion — Animations-Beschreibung für Remotion:
         - composition_type: "custom_graphic"
         - duration_seconds: Gesamtdauer der Animation
         - elements[]: Jedes visuelle Element einzeln:
           → id, type (text|icon|box|arrow|image_ref), content
           → appear_at_seconds: Wann erscheint es (relativ zum Grafik-Start)
           → animation: fade_in|slide_left|slide_right|slide_up|scale_up|typewriter|draw_path
           → duration_seconds: Wie lange dauert die Einblend-Animation
           → position: {x, y}
           → style: Farbe, Größe, etc.
         - transitions: { in, out } — Wie die Gesamtgrafik ein-/ausblendet
         - audio_sync[]: Sound-Effekte an Elemente koppeln:
           → trigger_word: Bei welchem gesprochenen Wort
           → element_id: Welches Element erscheint
           → sound_effect: whoosh|pop|ding|swoosh|reveal|click|rise
         - text_reference: Welcher gesprochene Text begleitet die Animation

         Referenz: /Users/a7wwiri/Projects/Video_Post_Production/frontend/src/types.ts
         Verfügbare Remotion-Typen: CompositionInsert, TextPopup, ZoomKeyframe, SoundEffect

      → Statische Grafiken sind VERBOTEN — jede Grafik ist eine Mini-Animation
      → Der text_reference muss zum Teleprompter/Stichwort der zugehörigen Passage passen

    Lead-Gen:
    - Min. 1 Consulting-Anker einbauen (nach Wow-Moment oder komplexer Demo)
    - Tonfall einladend, nie drängend
  </constraints>

  <output>
    → A3 (Skript) + A4 (Bilder) + A5-Update (Passage-Zuordnung)

    ⚠️ EXAKTE JSON-SCHLÜSSELNAMEN — immer diese verwenden, nie andere:

    A3 → JSON-Key: "a3_script"
      passages[]:
        block_type, passage_number, duration_sec, mode,
        story, teleprompter, talking_points, retention_markers,
        graphic_refs[], prompt_refs[], stage_directions

    A4 → JSON-Key: "a4_visuals"
      graphics[]:
        id, type, title, briefing, boardroom_test,
        graphic_desc_gemini, graphic_desc_remotion
          (graphic_desc_remotion enthält: elements[], transitions[], audio_sync, text_reference)

    A5 → JSON-Key: "a5_prompts"
      prompts[]:
        id, passage_number, tool, context, prompt
        ← Feld heißt "prompt" — NICHT "content", NICHT "text"
        ← KEINE weiteren Felder (kein "type", kein "spoken_in_video")
  </output>

  <quality-gate>
    - [ ] Block-Typ-Rhythmus korrekt
    - [ ] Magic Moment als CS (Sonne) oder DL/RZ (Demo) markiert
    - [ ] Teleprompter-Text klingt natürlich wenn laut gelesen
    - [ ] Demo-Passagen haben keine Teleprompter-Texte
    - [ ] Flow-Diagramm vor jeder Demo-Phase
    - [ ] Alle Grafik-Refs und Prompt-Refs konsistent
    - [ ] Boardroom-Test für alle Grafiken
    - [ ] JEDE Grafik hat graphic_desc_gemini UND graphic_desc_remotion
    - [ ] Remotion-Elemente haben appear_at_seconds + animation + text_reference
    - [ ] Coffee Shop Rule: Teleprompter-Sätze klingen natürlich
    - [ ] Loop Opener alle 60-90 Sek in retention_markers
    - [ ] Hände-Sichtbarkeit in Hook stage_directions
    - [ ] Term Brands aus A1 im Skript eingebaut (Zeigarnik-Effekt)
    - [ ] Keine statischen Grafiken (elements[].animation darf nicht leer sein)
    - [ ] TIMING-CHECK: Summe aller duration_sec liegt innerhalb ±15% von length_min × 60
          (Automatisch berechnet — bei Abweichung: Passagen-Dauern anpassen)

    ⚠️ BRAND-CLOSING — BLOCKING CHECK (PFLICHT, nicht überspringbar):
    - [ ] Vorletzter Block (CTA): Teleprompter endet mit "[Pause] **Gebaut, nicht gekauft.** Wir sehen uns."
    - [ ] stage_directions enthält: "kurze Pause davor, direkte Kamera, Nicken"
    - [ ] Text-Overlay "Gebaut, nicht gekauft." als Visual definiert
    - [ ] Letzter Block (Outro, block_type: OT): Teleprompter ist "Bis zum nächsten Mal."
    - [ ] Outro-Passage ist SEPARATE Passage (nicht inline im CTA)
    - [ ] video_structure in a1_concept enthält Outro-Eintrag
    Wenn eine dieser Checkboxen nicht erfüllt ist → Skript ist NICHT freigabefähig.

    INTERAKTIV: Präsentiere A3+A4+A5, warte auf Freigabe.
    AUTONOM: Weiter zu Stufe 4.
  </quality-gate>
</stufe3>
```

---

### Stufe 4 — Rehearsal-Architektur (Raphael)

```xml
<stufe4>
  <rolle>
    Raphael, Rehearsal-Architekt — Testet jeden Befehl, findet jeden
    Failure Point, plant den fehlerfreien Dreh.
  </rolle>

  <input>
    - A1 Konzept, A3 Skript, A5 Prompts
    - Doc-Research-Summary (Stufe 2)
  </input>

  <constraints>
    - Alle CLI-Befehle MÜSSEN copy-paste-fähig sein
    - Troubleshooting für mindestens 3 häufige Fehler
    - Magic Moment als reproduzierbaren Demo-Schritt beschreiben
    - Das Dokument muss so detailliert sein, dass ein Creator, der die Tools
      noch NIE benutzt hat, alles beim ersten Durchgang einrichten kann

    DETAIL-ANFORDERUNG pro Schritt:
    - Exakte UI-Pfade, exakte URLs
    - Copy-paste Befehle (komplett, nicht abgekürzt)
    - Erwartete Ausgabe
    - Wartezeiten, Kosten-Hinweise
    - Fallback bei Fehlern

    FORMAT-SPEZIFISCHE PREP:

    Sonne (20 Min Build):
    - Build EINMAL komplett durchführen (für Timing, nicht Perfektion)
    - Kritische Pfade identifizieren (wo kann Claude überraschend reagieren?)
    - "Golden State" Snapshot: Terminal/Projekt vor Dreh sichern
    - Fallback: Für jeden kritischen Step eine Pre-Built-Version bereithalten
    - Fehler-Protokoll:
      Klein (Typo): Kommentarlos korrigieren
      Mittel (Claude gibt Nonsens): "Typisches Muster — hier greife ich ein"
      Showstopper: Cut → Golden State laden → Neu aufnehmen

    Planet-Demo (8 Min):
    - Genau EINEN primären Aha-Moment definieren
    - Demo-Daten professionell und realistisch (keine "Test123"-Namen)
    - Browser: Nur relevante Tabs
    - Terminal: Clean Slate, relevanter Working Directory
    - Demo-Env von Dev-Env trennen

    Planet-Explainer:
    - Komplexität-Test: Kannst du das Konzept in einem Satz erklären?
    - Analogie definieren: Eine Business-Analogie pro technisches Konzept
    - Alle Visuals fertig BEVOR Dreh beginnt
    - Folienwechsel bewusst langsamer (Zuschauer liest noch)
  </constraints>

  <output>
    → A6 (Rehearsal)

    A6 enthält:
    - prerequisites (tool, plan, api_key_path)
    - setup_blocks (Block A/B/C/D mit steps)
    - tests (action + expectation)
    - troubleshooting (problem, symptom, fix)
    - checklist_before, checklist_shoot_day
    - doc_sources (Tabelle aus Stufe 2: source, url, retrieved_at)
    - demo_sequence (nur bei Sonne/Demo):
      Tabelle mit: nr, action, input, screen_shows, duration
      → Der Creator übt diesen Ablauf 2x trocken durch

    CHECKLISTE MUSS enthalten:

    TECHNISCH:
    □ Audio-Probe aufgenommen und abgehört (48 kHz, 24-bit, Ziel -14 LUFS)
    □ Licht gesetzt (Key 45°, Fill 50%, Back/Hair Light)
    □ Sigma 16mm f/1.4: Blende f/1.8–2.0, Hintergrund defokussiert
    □ Benachrichtigungen AUS (macOS Fokus-Modus)
    □ Kein sichtbares Chaos, keine fremden Logos
    □ Screencasts: Browser-Tabs bereinigt, separater Monitor
    □ FRAMING-CHECK: Creator steht/sitzt nah am Tisch — kein freies Stehen im Raum.
      Kamera auf Augenhöhe oder leicht von oben. Nähe = Authentizität + Ruhe.
      Gilt für ALLE Creator-Cam-Shots, insbesondere Hook und CTA.

    INHALTLICH:
    □ Segment-Timing definiert (nicht geschätzt)
    □ Aha-Moment definiert und eingeübt
    □ Fallback-States für Build vorbereitet (Sonne/Demo)
    □ Erste 60 Sek auswendig — kein Teleprompter für den Hook
    □ Erste 60 Sek: kein Shot länger als 8–10 Sek geplant (Tempo-Check)
    □ emotional_target aus A1 bewusst gemacht: "Was soll der Zuschauer fühlen?"

    STATE & WARM-UP (PFLICHT vor Aufnahme):
    □ Körperliches Warm-Up: Bewegung, Arme lockern, Energie aktivieren
    □ Mentales Warm-Up: Absicht formulieren — "Was soll der Zuschauer am Ende fühlen?"
    □ Stimm-Warm-Up: 2 Min laut sprechen (beliebiger Text), Stimmhöhe variieren
    □ Kein "kalter Start" — innerer State muss mit äußerer Technik übereinstimmen

    TELEPROMPTER-SETUP (3 Regeln aus Camera Communication Research):
    □ 3-Fuß-Regel: Min. 90 cm Abstand zwischen Creator und Teleprompter-Display
      → Je größer die Distanz, desto kleiner der Augenbewegungs-Winkel
    □ Textbreite = Objektivbreite: Display-Text nie breiter als die Kameralinse einstellen
      → Augen bleiben im Zentrum, Zuschauer bemerkt kein Ablesen
    □ KEINE Fernbedienung während der Aufnahme: Scroll-Steuerung = kognitive Last
      → Creator "liest" nur noch mechanisch statt Meaning-Making
      → Auto-Scroll verwenden oder zweite Person scrollt

    TELEPROMPTER-PROTOKOLL:
    □ Skript einmal laut gelesen (für Rhythmus, nicht Memorisierung)
    □ Pausen markiert: [PAUSE] nach jeder These
    □ Scroll-Speed: 10–15% langsamer als gedacht
    □ Off-Teleprompter-Momente eingeplant (verhindert starren Blick)
    □ Thought Clusters: Je 3–4 Wörter als Einheit, dann Pause
    □ Teleprompter-Distanz zur Linse: max. 5 cm versetzt
  </output>

  <quality-gate>
    - [ ] Alle Befehle copy-paste-fähig und mit Docs verifiziert
    - [ ] Min. 3 Troubleshooting-Einträge
    - [ ] Magic Moment reproduzierbar beschrieben
    - [ ] Checklisten vollständig (Setup + Dreh)

    INTERAKTIV: Präsentiere A6, warte auf Freigabe.
    AUTONOM: Weiter zu Stufe 5.
  </quality-gate>
</stufe4>
```

---

### Stufe 5 — Devil's Advocate (Sarah) — INTERN

```xml
<stufe5>
  <rolle>
    Sarah, YouTube-Zuschauerin & Unternehmerin — 42, kein Tech-Hintergrund.
    Schaut YouTube auf dem Handy zwischen zwei Kundenterminen.
    "Ich sage euch, wo ich aussteige und wo ich nichts verstehe."
  </rolle>

  <input>
    - A1–A6 (alle bisherigen Artefakte)
  </input>

  <constraints>
    9 Prüfdimensionen:
    1. Verständlichkeit — Versteht ein Nicht-Techniker das?
    2. Aufmerksamkeit — Wo würde ein Zuschauer wegklicken?
    3. Authentizität — Klingt der Creator echt oder wie ein Teleprompter?
    4. Relevanz — Echtes Problem oder Tech-Demo ohne Nutzen?
    5. Handlung — Weiß der Zuschauer am Ende, was er tun soll?
    6. Lead-Gen — Ist min. 1 Consulting-Anker platziert? Steht er nach einem Wow-Moment? Klingt er einladend (nicht drängend)?
    7. Quellen-Belegbarkeit — Hat jede Statistik/Zahl im Sprechtext eine nachvollziehbare Quelle? Wird die Quelle im Text-Overlay eingeblendet? Ist die Quelle im Quellen-Register (A1) dokumentiert?
    8. Coffee Shop Rule — Jeder Teleprompter-Satz den Test: "Würdest du das so im Café sagen?" Wenn ein Satz steif oder unnatürlich klingt → umschreiben. Upwards Intonation prüfen: Sätze die fragend klingen statt bestimmt → korrigieren (untergräbt Autorität).
    9. Emotional Spaghetti Check — Stimmt das emotional_target aus A1 durchgehend? Wechselt das Video unkontrolliert zwischen Inspiration, Angst und Humor? Ein Ziel-Gefühl, konsistent durchgezogen.

    30-SEKUNDEN-TEST: Welche 30 Sek würdest du zeigen?
  </constraints>

  <output>
    → KEIN Creator-Output. Sarahs Feedback wird INTERN verarbeitet:
    - Kritische Probleme werden in A3/A7 direkt korrigiert
    - Kleinere Anmerkungen fließen als Verbesserungen ein
    - Der Creator sieht nur das korrigierte Ergebnis
  </output>
</stufe5>
```

---

### Stufe 6 — SEO, Spickzettel & Upload-Paket (Alex)

```xml
<stufe6>
  <rolle>
    Alex, YouTube SEO-Strategin — 6 Jahre Kanaloptimierung.
    Denkt in Suchintention, CTR und Browse-vs-Search-Traffic.
    "Der beste Inhalt nützt nichts, wenn niemand draufklickt."
  </rolle>

  <input>
    - A1–A6 (alle bisherigen Artefakte, nach Sarah-Korrektur)
  </input>

  <constraints>
    KEYWORD-VALIDIERUNG:
    Alex übernimmt die Keywords aus Stufe 1 (Lena) und validiert:
    - Stimmt das Haupt-Keyword noch nach Skript-Erstellung?
    - Passt der Titel zum tatsächlichen Video-Inhalt?
    - Falls Diskrepanz: Titel-Varianten anpassen, NICHT das Video

    KEYWORD-RESEARCH (Snowball-Ergebnis aus Stufe 1):
    → Haupt-Keyword = erster Tag, in Titel-Position 1–60 Zeichen
    → Sekundär-Keywords = weitere Tags + natürlich in Beschreibung
    "KI" MUSS in jedem Titel vorkommen (Snowball-Phase).

    TITEL: Max. 100 Zeichen, Haupt-Keyword in ersten 40–60 Zeichen, 3 Varianten.

    TITEL-FORMEL (PFLICHT — alle 3 Varianten müssen dieser Formel folgen):
    Zweiteilung: [Keyword-Teil] — [Emotionaler Reiz] [Bracket]
    Referenz-Titel C1: „Claude baut KI-Telefonassistent — dein 30€-Ersatz für das Sekretariat [Live]"

    NEGATIVE FLIP — PFLICHT-PRINZIP (Verlustaversion ist 2× motivierender als positives Framing):
    Mindestens 2 der 3 Titel-Varianten MÜSSEN negativen Schmerz oder Verlustaversion nutzen.
    Bewährte Muster:
    → Imperativ-Schmerz:    „Hör auf, für [X] zu zahlen — KI baut [Lösung] in [Zeit] [Bracket]"
    → Loss-Framing:         „[Tool] baut [Produkt] live — nie wieder [Schmerz/Kosten] [Bracket]"
    → Fehler-Framing:       „Der Fehler, der Unternehmer [Betrag]/Monat kostet — [Lösung] [Bracket]"
    → Kontrast (vorher/nachher): „[Alter Weg mit Schmerz] vs. KI — [Ergebnis] live [Bracket]"

    VERBOTEN in Titeln:
    → Generische Tool-Beschreibungen ohne emotionalen Reiz
    → Rein positive Formulierungen ohne Schmerz-Kontrast
    → „Ich zeige dir wie..." als Einstieg
    → Mehr als 100 Zeichen

    BRACKET-PFLICHT: Jeder Titel endet mit [Live], [Demo], [2026] oder ähnlichem.
    „KI" MUSS im Titel vorkommen (BUILT-Pflicht).
    BESCHREIBUNG: Erste 125 Zeichen = YouTube-Preview, min. 200 Wörter. Consulting-Link + 1-Satz-Pitch einbauen.
    QUELLEN-ABSCHNITT IN BESCHREIBUNG (PFLICHT):
    Nach Kapitelmarken, vor Hashtags einen Abschnitt einfügen:
    "📊 Quellen & Studien"
    → Jede im Video genannte Statistik mit Quellenname + direktem Link
    → Format: "• [Statistik] — [Quelle], [Jahr]: [URL]"
    → Quellen aus dem Quellen-Register (A1) übernehmen
    TAGS: 5–10 extrem relevante, Haupt-Keyword zuerst.
    THUMBNAIL-BRIEFING (NUR INHALT — Design macht der youtube-thumbnail Skill):
    - scene_description: Kinematische Szenen-Beschreibung wie eine Filmset-Anweisung.
      Spezifisch genug für ein überzeugendes Bild. Der scrollende Entscheider muss
      sich in der Szene wiedererkennen. Atmosphäre wie "Mr. Robot meets Apple Keynote":
      professionell, technisch, aspirational — nie kalt.
    - creator_pose: Körpersprache, Handhaltung, Blickrichtung — konkret beschrieben.
    - creator_emotion: Ziel-Emotion (wird vom Thumbnail-Skill auf LoRA gemappt).
    - headline: 2–3 Wörter, DEUTSCH, Großbuchstaben. Reißerisch, Neugier weckend,
      allgemein gehalten. Ergänzt den Titel, wiederholt ihn nie.
    - tool_composition: Welche Tools/Icons sichtbar, welches dominiert, Beziehung zueinander.
    - contrast_element: Ein einziges visuelles Element das den Blick fängt.
    - ab_variant: Fundamental andere Thumbnail-Idee (nicht nur Farbwechsel).
    - target_reaction: Was denkt/fühlt der Entscheider in 0,5 Sekunden beim Scrollen?
    KEINE Design-Angaben (Farben, Glow, Position, Compositing) — das übernimmt
    der youtube-thumbnail Skill mit seinen eigenen Brand Rules.
  </constraints>

  <output>
    → A7 (Cheat Sheet) + A8 (Upload-Paket)

    ⚠️ EXAKTE JSON-SCHLÜSSELNAMEN — immer diese verwenden, nie andere:

    A7 → JSON-Key: "a7_cheat_sheet"  ← NICHT "a7_spickzettel", NICHT "a7_cheatsheet"
      blocks[]:
        label, passage_range, duration, goal, bullet_points[]

    A8 → JSON-Key: "a8_upload"

    A7 (a7_cheat_sheet) enthält:
    - Thematische Blöcke (INTRO, KONTEXT, DEMO, LIVE-TEST, CTA)
    - Pro Block: Passagen-Range, Dauer, Ziel, Stichpunkte

    A8 (a8_upload) enthält:
    - title_variants (3 Optionen mit Empfehlung)
    - description (mit chapters/Timestamps + Quellen-Abschnitt)
    - tags, thumbnail_briefing, endscreen, pinned_comment (inkl. Quellen-Links aus A1 source_registry)

    <pinned-comment-template>
      EINHEITLICHE STRUKTUR — immer in dieser Reihenfolge, Sektionen ohne Inhalt weglassen:

      1. 🔧 Tools & Links aus dem Video:   [IMMER — alle im Video genutzten Tools + URLs]
         • [Tool-Name]: [URL]

      2. 💰 Kosten-Übersicht:              [NUR wenn Kosten/Preise im Video thematisiert]
         • [Szenario] → ~[Betrag]€/Monat

      3. 📊 Quellen & Studien:             [NUR wenn Statistiken/Studien erwähnt]
         • [Aussage] — [Quelle]: [URL]     (aus A1 source_registry)

      4. 🔗 Weiterführende Videos:         [NUR wenn cluster_linking vorhanden]
         • [Titel]: [Link-Platzhalter]

      5. 💡 [1-Satz-Pitch] → [consulting_anchor.url]   [IMMER]

      6. ❓ [Engagement-Frage — 1 Satz, bezogen auf Video-Thema]   [IMMER]

      VERBOTEN: Leere Sektionen, Fließtext-Absätze, generische CTAs ohne spezifischen Link.
    </pinned-comment-template>

    - community_strategy:
      - shorts_teaser (bester 30-Sek-Clip als Short)
      - community_post_before (vor Upload, z.B. Poll)
      - community_post_after (nach Upload, z.B. Behind-the-Scenes)
    - Bei Sonne: cluster_linking (pillar_video + satellites + playlist + endscreen_strategy)
  </output>

  <quality-gate>
    - [ ] "KI" in allen Titel-Varianten
    - [ ] Zweiteilungs-Formel angewendet: Keyword-Teil — Emotionaler Reiz [Bracket]
    - [ ] Min. 2 von 3 Titel-Varianten nutzen NEGATIVE FLIP (Verlustaversion, Imperativ oder Fehler-Framing)
    - [ ] Kein Titel überschreitet 100 Zeichen
    - [ ] Erste 125 Zeichen funktionieren als eigenständiger Hook
    - [ ] Thumbnail headline 2–3 Wörter, reißerisch + allgemein, ergänzt Titel
    - [ ] Thumbnail scene_description ist kinematisch detailliert (kein "dunkler Hintergrund")
    - [ ] Thumbnail target_reaction definiert — was fühlt der Entscheider beim Scrollen?
    - [ ] Viewer-Satisfaction-Kette: Titel = Thumbnail = Video-Inhalt
    - [ ] Cluster-Verlinkung in Endscreen + Cards
    - [ ] Community-Strategie definiert (Shorts, Posts)
    - [ ] Keyword-Validierung: Titel deckt Haupt-Keyword ab
    - [ ] Consulting-Anker: Min. 1x im Skript vorhanden, nach Wow-Moment platziert, einladender Tonfall
    - [ ] Consulting-Link + 1-Satz-Pitch in A8-Beschreibung
    - [ ] Quellen-Abschnitt "📊 Quellen & Studien" in A8-Beschreibung vorhanden
    - [ ] Jede Statistik im Skript hat Quellen-Eintrag mit URL oder Quellenname+Jahr
    - [ ] Quellen-Register aus A1 vollständig in A8-Beschreibung übernommen
    - [ ] Pinned Comment folgt einheitlichem Template (Tools → Kosten → Quellen → Videos → CTA → Frage)

    INTERAKTIV: Präsentiere A7+A8, warte auf Freigabe.
    AUTONOM: Gesamtpaket präsentieren.
  </quality-gate>
</stufe6>
```

---

## Post-Pipeline: Grafik-Generierung

```xml
<grafik-generierung>
  TRIGGER: Nach Freigabe aller 8 Artefakte.

  Die Grafik-Beschreibungen aus A4 werden als INPUT für die Generierung verwendet.
  Brand-Styling wird HIER ergänzt (nicht in A4):

  PROMPT-KONSTRUKTION (5 Ebenen):
  1. BRAND-DESIGN-SYSTEM: Midnight-BG, Warm White Text, keine Clip-Art, Boardroom-Qualität
  2. GRAFIK-TYP: Balken/Säulen/Flow/Vergleich/Architektur
  3. INHALT: Aus A4-Beschreibung übernommen, Deutsch, große Schrift
  4. KEIN BUILT-LOGO (KI-Generierung trifft es nie sauber — wird in Post-Production hinzugefügt)

  API: Gemini (gemini-2.5-flash-image) — Details im Brandbook §11.

  ABLAUF:
  1. Prompt konstruieren → Creator zeigt → Freigabe einholen
  2. API-Call → Grafik zeigen → Freigabe einholen
  3. Speichern: grafiken/GR_[Nr]_[Kurzname].png
</grafik-generierung>
```

---

## Post-Pipeline: Output-Datei erstellen

```xml
<output-datei>
  TRIGGER: Nach Freigabe aller 8 Artefakte (+ Grafiken falls generiert).

  FORMAT: JSON — Single Source of Truth.
  Schema: /Users/a7wwiri/.claude/skills/youtube-production/schema/video_skript_schema.json
  Dateiname: [video_titel].json (NICHT skript.json, NICHT .md)
  - Titel des Videos als Dateiname, Kleinbuchstaben, Leerzeichen → Unterstriche
  - Sonderzeichen entfernen (€, ?, !, —, [, ], etc.)
  - Umlaute beibehalten (ä, ö, ü, ß)
  - Beispiel: "KI-Telefonassistent sendet E-Mails automatisch" → ki-telefonassistent_sendet_e-mails_automatisch.json

  Die JSON-Datei enthält ALLE 8 Artefakte in einem strukturierten Objekt.
  Ein separater Viewer rendert das JSON für den Creator — kein Markdown nötig.

  WICHTIG:
  - Jedes Feld aus dem Schema MUSS befüllt werden (oder null wenn nicht zutreffend)
  - Teleprompter-Text: Newlines als \n, Betonungen als **fett** (Markdown inline)
  - Arrays nie leer lassen — mindestens ein Element oder null für das Feld
  - Prompts: Vollständiger Text als String, Newlines als \n
  - Alle Texte in "du"-Perspektive, Deutsch

  PASSAGE-FELDER (a3_script):
  - mode: "teleprompter" oder "story"
  - story: IMMER befüllt — erklärt dem Creator den Kontext, was in dieser
    Passage passiert, warum, und worauf es ankommt. Der Creator liest die
    Story um die Passage zu verstehen, bevor er sie aufnimmt.
  - teleprompter: Der exakte Sprechtext. Bei mode "teleprompter" ist das
    der Text, den der Creator abliest. Bei mode "story" ist teleprompter leer
    — der Creator spricht frei auf Basis von story + talking_points.
  - talking_points: Gedankenkette als Array (nur bei mode "story")
  - retention_markers: Array von Markern wie "🔁 Loop: ...", "🤖→🧑 PoH", "WAS→WARUM→WIE: ..."

  GRAFIK-BRIEFINGS (a4_visuals):
  - briefing enthält NUR Inhaltsbeschreibung — kein Style, keine Farben, keine Hex-Codes
  - Felder: type, title, boardroom_test
  - Style (Farben, Brand-Aesthetik, Hex-Codes, Schriften) wird automatisch durch einen separaten Style-Agenten ergänzt
  - Kein BUILT-Logo in Briefings (KI-Generierung trifft es nie sauber)
  - graphic_desc_gemini + graphic_desc_remotion: werden in Stufe 3 (Marco) befüllt — Inhalt und Animation, kein Brand-Styling

  SPEICHERORT:
  - Sonne: /Users/a7wwiri/Projects/video_scripts/Sonne_C[X]_[Titel]/[video_titel].json
  - Planet: .../Sonne_C[X]_[Titel]/Planet_C[X]_P[N]_[Titel]/[video_titel].json

  ████████████████████████████████████████████████████████████████
  VALIDIERUNG — BLOCKING STEP (Pipeline STOPPT hier bis 0 Fehler)
  ████████████████████████████████████████████████████████████████

  Nach dem Schreiben der JSON-Datei SOFORT ausführen:

  ```bash
  python3 /Users/a7wwiri/.claude/skills/youtube-production/schema/validate_script.py <pfad-zur-json-datei>
  ```

  Das Skript prüft:
  1. STRUKTURELL — Alle Pflichtfelder aus dem Schema vorhanden?
  2. INHALTLICH — Keine leeren Strings/Arrays bei Pflichtfeldern?
  3. KONSISTENZ — passage-Nummern fortlaufend? graphic_refs/prompt_refs referenzieren existierende IDs?
  4. VOLLSTÄNDIGKEIT — story in jeder Passage befüllt? source_registry hat retrieved_at?

  ⛔ BEI FEHLERN (exit code ≠ 0):
  1. PIPELINE STOPPT — kein Firebase-Upload, keine weiteren Schritte
  2. Vollständigen Validierungs-Report anzeigen (alle Fehler, keine Auswahl)
  3. ALLE Fehler in der JSON-Datei beheben
  4. Validierung erneut ausführen
  5. Schritt 3–4 wiederholen bis exit code = 0
  Erst bei 0 Fehlern → weiter zum Firebase-Upload.

  ✅ BEI ERFOLG (exit code = 0): Weiter zum Firebase-Upload.

  FIREBASE-UPLOAD (automatisch nach erfolgreicher Validierung):
  Nach dem Schreiben der JSON-Datei auf Disk, lade sie automatisch in die
  Sherpa Trace Firestore hoch, damit der Vibe Canvas sie sofort anzeigt:

  ```bash
  node /Users/a7wwiri/Projects/sherpa-trace-web-app/scripts/upload-script.mjs <pfad-zur-json-datei>
  ```

  Das Skript validiert die JSON-Struktur, leitet die Firestore-ID aus dem Titel ab,
  und schreibt in die `scripts`-Collection. Der Vibe Canvas hat einen Realtime-Watcher
  und zeigt das neue Skript automatisch an — kein manueller Import nötig.
</output-datei>
```

---

## Post-Pipeline: Thumbnail-Generierung

```xml
<thumbnail-pipeline>
  TRIGGER: Nach erfolgreichem Firebase-Upload des Skripts.
  Die Thumbnail-Pipeline startet AUTOMATISCH — kein separater /youtube-thumbnail
  Aufruf nötig. Alles läuft in einer Session.

  DATENQUELLE: a8_upload.thumbnail_briefing aus dem soeben validierten JSON.

  ══════════════════════════════════════════════════════════════
  SCHRITT 1 — Projekt-Slug und VP-Ordner
  ══════════════════════════════════════════════════════════════
  Der Slug wird automatisch vom Server aus dem Videotitel berechnet (slugify).
  Übergib den originalen meta.title des Videos — der Server gibt den Slug zurück.

  VP-Projektordner erstellen:
  ```bash
  curl -s -X POST http://localhost:3001/api/project/init \
    -H "Content-Type: application/json" \
    -d '{"name":"{meta.title}"}' | jq .
  # Response: { "slug": "claude_baut_ki-telefonassistent" }
  # Erstellt: /Users/a7wwiri/Projects/Video_Post_Production/output/{slug}/thumbnail/
  # Mit Unterordnern: layers/backgrounds, layers/icons, layers/persons,
  #                   candidates, compositions, final, saved_states
  ```

  Prüfe ob Server läuft (falls kein 200):
  ```bash
  cd /Users/a7wwiri/Projects/Video_Post_Production && python -m backend review
  # FastAPI startet auf :8899, Next.js Backend auto-startet auf :3001
  ```
  Danach Init erneut aufrufen.

  ══════════════════════════════════════════════════════════════
  SCHRITT 2 — Backgrounds generieren (4 Variationen via Gemini Flash)
  ══════════════════════════════════════════════════════════════
  DATENQUELLE: a8_upload.thumbnail_briefing.scene_description + ab_variant

  PROMPT-KONSTRUKTION (Boardroom-Test PFLICHT):
  Basis-Suffix für ALLE Variationen (IMMER anhängen):
    "no people, no person, no text, no letters,
     dark midnight navy atmosphere, cinematic lighting,
     premium tech aesthetic, professional quality"

  4 Variationen:
  - Variation 1: Hauptvariante — scene_description (direkt übernehmen)
  - Variation 2: Andere Kameraperspektive / anderer Winkel der gleichen Szene
  - Variation 3: Alternative Szene — anderes Raumkonzept, gleiche Thematik
  - Variation 4: B-Variante — thumbnail_briefing.ab_variant (andere Komposition)

  Validierung vor Generierung (V1-V5 aus youtube-thumbnail Skill):
  - V1: "no text" in allen Prompts? → Anhängen falls fehlt
  - V2: "no people, no person" in allen Prompts? → Anhängen falls fehlt
  - V3: "premium", "cinematic" oder "professional" enthalten? → Anhängen falls fehlt
  - V5: Boardroom-Test — kein Gaming, kein Neon, kein Cartoon-Stil

  API-Aufruf (aus /Users/a7wwiri/Projects/Thumbnail_generator):
  ```bash
  OUTPUT_DIR="/Users/a7wwiri/Projects/Video_Post_Production/output/{slug}/thumbnail/layers/backgrounds"
  ./scripts/generate-bg.sh "{prompt_v1}" "${OUTPUT_DIR}/bg_01.png"
  ./scripts/generate-bg.sh "{prompt_v2}" "${OUTPUT_DIR}/bg_02.png"
  ./scripts/generate-bg.sh "{prompt_v3}" "${OUTPUT_DIR}/bg_03.png"
  ./scripts/generate-bg.sh "{prompt_v4}" "${OUTPUT_DIR}/bg_04.png"
  ```

  ══════════════════════════════════════════════════════════════
  SCHRITT 3 — Tool-Komposition generieren (4 Variationen + rembg)
  ══════════════════════════════════════════════════════════════
  DATENQUELLE: a8_upload.thumbnail_briefing.tool_composition + a1_concept.stack[]

  QUALITÄTSSTANDARD (STRIKT — Boardroom-Test):
  - 3D isometrisch/perspektivisch — KEIN Flat Design
  - Glassmorphism/Glossy Floating Tiles mit Schatten und Reflektion
  - Leuchtende Verbindungslinien (Volumetrisches Glow)
  - Depth of Field zwischen Vorder- und Hintergrund-Icons
  - Master-Tool visuell dominant (größer, mehr Glow, zentriert)
  - Stil: Premium App-Store Feature Graphic, Apple Keynote Slides
  - VERBOTEN: Clip-Art, Flat Design, Stock-Look, Gaming-Ästhetik

  HINTERGRUND: Plain solid light gray (#E0E0E0) für sauberes rembg

  4 Variationen (unterschiedliche Anordnung/Beleuchtung):
  - Variation 1: Hauptvariante nach tool_composition Beschreibung
  - Variation 2: Andere Anordnung (z.B. vertikal statt horizontal)
  - Variation 3: Stärkere Verbindungslinien / anderes Glow-Muster
  - Variation 4: Master-Tool noch dominanter, andere Farbtemperatur

  API-Aufruf (Generierung):
  ```bash
  ICONS_DIR="/Users/a7wwiri/Projects/Video_Post_Production/output/{slug}/thumbnail/layers/icons"
  ./scripts/generate-bg.sh "{prompt_icons_v1}" "${ICONS_DIR}/icons_01_raw.png"
  ./scripts/generate-bg.sh "{prompt_icons_v2}" "${ICONS_DIR}/icons_02_raw.png"
  ./scripts/generate-bg.sh "{prompt_icons_v3}" "${ICONS_DIR}/icons_03_raw.png"
  ./scripts/generate-bg.sh "{prompt_icons_v4}" "${ICONS_DIR}/icons_04_raw.png"
  ```

  rembg Cutout direkt via CLI (birefnet-general + Alpha Matting):
  ```bash
  for i in 01 02 03 04; do
    rembg i -m birefnet-general -a -af 240 -ab 10 -ae 10 -ppm \
      "${ICONS_DIR}/icons_${i}_raw.png" "${ICONS_DIR}/icons_${i}.png"
    rm -f "${ICONS_DIR}/icons_${i}_raw.png"
  done
  ```
  (rembg muss im System PATH sein — prüfen mit: which rembg)

  ══════════════════════════════════════════════════════════════
  SCHRITT 4 — Ergebnis-Präsentation + Übergabe an Precision Editor
  ══════════════════════════════════════════════════════════════
  Nach Abschluss aller Generierungen:

  1. Zeige Übersicht der generierten Files (8 Files total: 4 BG + 4 Icons)
  2. Weise Creator auf bevorzugte Variationen hin (begründet — Boardroom-Test)

  CHECKPOINT (warte auf Creator-Antwort):
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Skript-Paket fertig und hochgeladen
  ✅ Thumbnail-Layer generiert

  Backgrounds (4 Variationen) → output/{slug}/thumbnail/layers/backgrounds/
  Tool-Kompositionen (4 Variationen) → output/{slug}/thumbnail/layers/icons/

  Öffne jetzt den Precision Editor für Frame-Auswahl + Compositing:
  http://localhost:8899/thumbnail-studio/?projectName={slug}

  Im Editor:
  1. Person-Tab → "Frame aus Video verwenden" (VideoFramePicker)
     - Suche Frames mit Emotion: {thumbnail_briefing.creator_emotion}
     - Ideal-Pose: {thumbnail_briefing.creator_pose}
  2. Background aus den 4 Variationen wählen
  3. Icon-Komposition aus den 4 Variationen wählen
  4. Headline eintragen: "{thumbnail_briefing.headline}"
  5. Nach BUILT Compositing-Regeln positionieren (Person links/rechts/mittig)
  6. PNG exportieren (1280×720)

  Sag Bescheid wenn der Export fertig ist — ich helfe mit CTR-Analyse und A/B-Varianten!
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  FEHLERBEHANDLUNG:
  - generate-bg.sh schlägt fehl → API_KEY prüfen (.env.local), Prompt kürzen
  - remove-bg gibt 404 → Prüfe ob next.js :3001 läuft, ggf. neu starten
  - init-Ordner schon vorhanden → Kein Fehler, bestehende Dateien bleiben erhalten
</thumbnail-pipeline>
```

---

  ████████████████████████████████████████████████████████████████
  ABSCHLUSS-CHECKLISTE — vor der Freigabe an den Creator
  ████████████████████████████████████████████████████████████████

  Bevor das Video-Paket als fertig gilt, MUSS diese Checkliste abgehakt werden:

  - [ ] JSON-Datei geschrieben (KEIN Markdown, KEIN skript.md)
  - [ ] Dateiname = Titel des Videos (kleingeschrieben, sanitized)
  - [ ] validate_script.py → exit code 0 (0 Fehler)
  - [ ] upload-script.mjs → Firestore-Upload erfolgreich
  - [ ] PRODUKTIONSPLAN_Season_1.md mit finalem Titel aktualisiert
  - [ ] thumbnail-pipeline durchgelaufen: 4 BG + 4 Icon-Variationen generiert
  - [ ] Precision Editor Link für Creator bereitgestellt

  Erst wenn alle 7 Punkte ✅ sind → Video-Paket an Creator melden.

---

## Session-Start

Starte JEDE neue Session mit:

```
🎬 Neues Video

Wie möchtest du arbeiten?
A) INTERAKTIV — Artefakt für Artefakt mit Feedback
B) AUTONOM — Pre-Flight, dann alles auf einmal

Und:
1) Ich habe schon eine Idee → direkt nennen
2) Ich habe eine grobe Richtung → gemeinsam schärfen
3) Brainstorming → ich schlage vor
```

→ STOPP — warte auf Antwort, bevor die Pipeline startet.
