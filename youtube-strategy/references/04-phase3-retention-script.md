# Phase 3: Retention-Engineered Script (TelePro-Format)

Write a video script that maximizes watch time through structural retention engineering.
The goal: 50-60% average view duration (70%+ for priority suggested placement).

Phase 3 outputs **directly in TelePro markdown** — no conversion step needed.
The output is saved as `telepro-script.md` and is ready for the TelePro editor.

## Why Retention Engineering Matters

- **33% of viewers leave in the first 30 seconds** if the video doesn't hook them
- **YouTube's algorithm heavily weights watch time** — it's the #1 ranking factor
- **Rehooks every 60-90 seconds** pull drifting viewers back in
- **Open loops** create a "curiosity gap" — the brain can't leave until the loop closes
- **Pattern interrupts** prevent habituation (the brain tunes out predictable content)

## The Retention Structure

Every script follows this skeleton:

```
# Hook [TIME: 0:00]        — PAS-Framework (Pain → Agitate → Solution) + Video-Roadmap + Brand-Bumper
# [Chapter 1] [TIME: x:xx] — Mini-Hook + Content + [REHOOK] at the end
# [Chapter 2] [TIME: x:xx] — Mini-Hook + Content + [REHOOK] at the end
...
# Key Takeaways [TIME: x:xx]
# CTA [TIME: x:xx]
```

## How Retention Elements Map to TelePro Format

Retention markers use the same bracket format as all other TelePro markers (`[SLOW]`, `[FAST]`, `[PAUSE:N]`).
No `//` prefix — these are first-class TelePro tags, not comments.

| Retention Element | TelePro Expression |
|---|---|
| Open Loop | `[OPEN LOOP]` … `[/OPEN LOOP]` — wraps the spoken line that opens the tension |
| Close Loop | `[CLOSE LOOP]` … `[/CLOSE LOOP]` — wraps the spoken line that resolves the tension |
| Rehook | `[REHOOK]` … `[/REHOOK]` — wraps the transitional spoken line at chapter end |
| Pattern Interrupt | `[NOTE: PATTERN INTERRUPT — Kamera-Wechsel / Screen-Switch / Demo-Start]` |
| Cold Open Hook | First lines of `# Hook` — no intro, straight into PAS |
| Chapter Mini-Hook | First line of each `# Chapter` section — teases what's coming |

## Process

### Step 1: Define the Script Parameters

Clarify with the user:
- **Topic** (from Fundament: Topic Research)
- **Target length** (10 min, 15 min, 20 min?)
- **Format** (Planet-Explainer, Planet-Demo, Sonne — see telepro-script skill for definitions)
- **Key insight** from Phase 1 (Competitive Analysis — what patterns to apply?)

### Step 2: Generate the Script with Claude

Use the `claude` CLI to generate the script. The prompt must specify:

```
Du bist ein YouTube-Skript-Autor, der Retention-optimierten Content für einen
deutschsprachigen KI/Developer-Tools-Kanal schreibt.

Schreibe ein vollständiges Skript auf Deutsch über [TOPIC].
Ziellänge: [LENGTH] Minuten.
Format: [FORMAT] (Planet-Explainer / Planet-Demo / Sonne)

STIL — KAFFEEGESPRÄCH, KEIN NACHRICHTENSPRECHER:
Schreibe wie jemand, der seinem besten Freund beim Kaffee etwas erklärt, das ihn
wirklich begeistert. Keine polierten Moderatoren-Sätze. Direkte Fragen an den
Zuschauer. Konkrete Alltagsbeispiele. Sätze dürfen mit "Und" oder "Also" anfangen.
Süddeutsche Umgangssprache ist ok ("halt", "eigentlich"). Keine präzisen Zeitangaben
die man nicht einhalten kann ("in 5 Minuten"). Kein Tutorial-Modus im Teleprompter
(Bildschirmnavigation gehört nicht ins Skript).

AUSGABEFORMAT — TELEPRO MARKDOWN:
- Sektionsheader: `# Sektionsname [TIME: 0:00]`
- Gesprochener Text: normaler Fließtext, kein Prefix
- Kommentare/Regieanweisungen: `// Kommentar` (nie gesprochen)
- Operator-Notizen: `[NOTE: ...]` (nie im Prompter sichtbar)
- Bild-Placeholder: `[IMG:storage://PLACEHOLDER-beschreibung]`
- Pausen: `[PAUSE:N]` nur an echten strukturellen Brüchen
- Tempo: `[SLOW]...[/SLOW]` für komplizierte/emotionale Stellen, `[FAST]...[/FAST]` für Aufzählungen
- Betonung: `**Wort**` max. 2–3 pro Sektion, `!!Text!!` nur für echte CTAs/Warnungen

RETENTION-ANFORDERUNGEN:
1. HOOK — PAS-Framework: Starte mit SCHMERZ (nicht Traumszenario). Dann Agitate.
   Dann Solution. Kein "Willkommen zu einem neuen Video." Direkt rein.
   Nach PAS: Video-Roadmap ("Ich zeige dir heute drei Dinge: X, Y, Z").
   Nach Roadmap: Brand-Bumper (zwei Zeilen: "Hier bauen wir KI-Lösungen, die dir
   echte Zeit zurückgeben." + "Heute: [Thema]"). Keine Zeitangabe im Bumper.

2. OPEN LOOPS — Mindestens 4. Jeder Loop MUSS vor Videoende geschlossen werden.
   `[OPEN LOOP]` … `[/OPEN LOOP]` umschließt die gesprochene Zeile, die den Spannungsbogen öffnet.
   `[CLOSE LOOP]` … `[/CLOSE LOOP]` umschließt die gesprochene Zeile, die ihn auflöst.

3. REHOOKS — Mindestens eine pro 90 Sekunden an Kapitelgrenzen.
   `[REHOOK]` … `[/REHOOK]` umschließt die gesprochene Übergangszeile.

4. PATTERN INTERRUPTS — Alle 3–4 Minuten.
   Als `[NOTE: PATTERN INTERRUPT — Kamera-Wechsel / Demo-Start / Screen-Switch]`

5. CHAPTER-STRUKTUR — Jedes Kapitel hat einen eigenen Mini-Hook (erste Zeile teased
   was kommt) und eine Mini-Resolution (letzter inhaltlicher Satz schließt das Kapitel).

6. KEY TAKEAWAYS — Pflichtsektion vor CTA. Mindestens 3 konkrete Learnings. Mit [FAST].

7. CTA — Dezent, kein Verkäufer-Modus. Struktur:
   - Konkrete erste Handlung (niedrigschwellig)
   - BUILT-Hinweis (ein Einzeiler, kein Gesprächsangebot)
   - Kommentare, Abo
   - "Gebaut, nicht gekauft. Wir sehen uns."

METADATEN-NOTIZ am Anfang des Skripts (vor dem Hook):
`[NOTE: SKRIPT-INFO — Format: [Format] | ~[X] Min | Zielgruppe: [Zielgruppe] | Sektionen: [N]]`
```

### Step 3: Review and Adapt

After Claude generates the script:

1. **Hook check (first 30s):** Read the cold open out loud. Does it start with PAIN? Does it make you want to keep watching? If not, iterate.
2. **PAS check:** Pain → Agitate → Solution clearly present? Solution leads into Video-Roadmap?
3. **Open loop audit:** Count the `[OPEN LOOP]` tags. At least 4? Each one has a matching `[CLOSE LOOP]` before video ends?
4. **Rehook density:** Count `[REHOOK]` tags. At least one every 90 seconds?
5. **Kaffeegespräch check:** Does it sound like a human or a news anchor? Fix any "Heute betrachten wir..."-style sentences.
6. **Personality injection:** Add your specific stories, opinions, concrete examples from your own experience.

### Step 4: Save Output

Save as `telepro-script.md` in the topic slug directory. This file is ready for the TelePro editor — no further conversion needed.

The file also serves directly as the proxy transcript for the SEO Phase 2 cross-check.

## Output Template

```markdown
[NOTE: SKRIPT-INFO — Format: Planet-Explainer | ~10 Min | Zielgruppe: Deutsche Entwickler | Sektionen: 6]

# Hook [TIME: 0:00]
// [NOTE: Kein Warm-up — direkt rein. Terminal/Screen im Hintergrund.]

[Pain — konkreter Schmerz, den die Zielgruppe kennt]

[PAUSE:2]

[Agitate — warum das wirklich nervt / teuer / sinnlos ist]

[SLOW]
[Solution — das Versprechen, direkt und konkret]
[/SLOW]

[PAUSE:2]

[OPEN LOOP]
[Video-Roadmap: "Ich zeige dir heute drei Dinge: X, Y, Z."]
[/OPEN LOOP]

Hier bauen wir KI-Lösungen, die dir echte Zeit zurückgeben.
Heute: [Thema des Videos].

# [Kapitel 1 — Kontext/Problem] [TIME: 1:30]
[NOTE: Grafik/Screen einblenden]

[Mini-Hook — erste Zeile teased was in diesem Kapitel kommt]

[IMG:storage://PLACEHOLDER-diagram-beschreibung]

[Content...]

[OPEN LOOP]
[gesprochene Zeile die den Spannungsbogen öffnet]
[/OPEN LOOP]

[REHOOK]
[Übergangszeile die nächsten Abschnitt anteasert]
[/REHOOK]

# [Kapitel 2] [TIME: 3:00]
[NOTE: PATTERN INTERRUPT — Screen-Switch / Demo-Start]

[Mini-Hook]

[Content...]

[SLOW]
[Kernaussage des Kapitels]
[/SLOW]

[REHOOK]
[Übergangszeile]
[/REHOOK]

# [Kapitel 3] [TIME: 5:00]

[Mini-Hook]

[Content...]

[CLOSE LOOP]
[Spoken line that resolves the previously opened loop]
[/CLOSE LOOP]

[NOTE: PATTERN INTERRUPT — Kamera-Wechsel, direkt in die Linse]

[REHOOK]
[Übergangszeile]
[/REHOOK]

# Key Takeaways [TIME: 8:30]
// [NOTE: Kamera, ruhig, direkt — kein Screen]

Also — was nimmst du heute mit?

[FAST]
Erstens: [konkretes Learning].
Zweitens: [konkretes Learning].
Drittens: [konkretes Learning].
[/FAST]

[SLOW]
Und das Wichtigste: [übergeordnetes Fazit in einem Satz].
[/SLOW]

# CTA [TIME: 9:15]
// [NOTE: Direkt in die Kamera, entspannt, leicht lächeln — kein Verkäufer-Modus]

Wenn du heute konkret starten willst — [niedrigschwellige erste Handlung].

Wenn du das **richtig** machen willst — dann brauchst du [Tool/Lösung aus dem Video].
Genau das machen wir bei BUILT. Link ist in der Beschreibung.

Wenn du Fragen hast — schreib sie in die Kommentare.
Ich lese mit und antworte.

Und wenn du mehr Videos wie dieses nicht verpassen willst — Kanal abonnieren.
Das kostet dich nichts, aber es bedeutet auch, dass wir weiter solche Inhalte machen können.

Gebaut, nicht gekauft. Wir sehen uns.
```

## Success Criteria

- [ ] `[NOTE: SKRIPT-INFO]` am Anfang vorhanden
- [ ] Hook startet mit SCHMERZ — PAS-Framework (Pain → Agitate → Solution)
- [ ] Video-Roadmap nach PAS ("Ich zeige dir heute: X, Y, Z")
- [ ] Brand-Bumper nach Roadmap (zwei Zeilen, keine Zeitangabe)
- [ ] Mindestens 4 `[OPEN LOOP]`…`[/OPEN LOOP]` Paare, alle mit passendem `[CLOSE LOOP]`…`[/CLOSE LOOP]` vor Videoende
- [ ] `[REHOOK]`…`[/REHOOK]` mindestens alle 90 Sekunden
- [ ] `[NOTE: PATTERN INTERRUPT — ...]` alle 3–4 Minuten
- [ ] `[TIME: x:xx]` in jedem Sektionsheader
- [ ] `[SLOW]`, `[FAST]`, `[PAUSE:N]` sinnvoll eingesetzt
- [ ] Kaffeegespräch-Stil — kein Nachrichtensprecher
- [ ] Keine präzisen Zeitangaben die man nicht einhalten kann
- [ ] Key Takeaways-Sektion vorhanden (mind. 3 Punkte, mit `[FAST]`)
- [ ] CTA-Sektion vorhanden mit "Gebaut, nicht gekauft. Wir sehen uns."
- [ ] Script saved to `<topic-slug>/telepro-script.md`

## Downstream Integration

This TelePro script serves two purposes directly:

1. **Production:** Copy `telepro-script.md` into the TelePro editor — no conversion step needed.
2. **SEO Phase 2 cross-check:** The spoken lines in `telepro-script.md` serve as the proxy
   transcript for the metadata validation in Phase 2. No separate `telepro-script` skill
   conversion is needed — the Phase 3 output IS the TelePro script.
