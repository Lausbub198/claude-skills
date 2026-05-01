# telepro-script

Erstellt fertige Teleprompter-Skripte im [TelePro](https://github.com/a7wwiri/TelePro)-Markdown-Format für BUILT YouTube-Videos.

---

## Was der Skill macht

- Schreibt **neue Skripte** zu einem Thema — strukturiert, im richtigen Format, direkt kopierbereit
- **Konvertiert Rohtexte** (Fließtext, Stichpunkte, JSON aus `youtube-production`) ins TelePro-Format
- Wählt automatisch das richtige **Videoformat** (Sonne / Planet-Demo / Planet-Explainer)
- Erzwingt konsequent **Kaffeegespräch-Stil** — kein Nachrichtensprecher, kein poliertes Corporate-Speak
- Strukturiert jeden Hook nach dem **PAS-Framework** (Pain → Agitate → Solution) mit Video-Roadmap-Vorschau
- Fügt immer eine **Key Takeaways**-Sektion und ein menschliches **CTA**-Template ein

---

## Installation

```bash
cp -r telepro-script ~/.claude/skills/
```

Claude Code picks up the skill automatically on the next session.

---

## Verwendung

### Neues Skript schreiben

```
Schreib mir ein TelePro-Skript für ein Planet-Demo Video über [Thema].
```

```
Ich brauche ein Teleprompter-Skript für ein Sonne-Video über [Thema] — Zielgruppe: Mittelständler.
```

### Rohtext konvertieren

```
Wandle diesen Rohtext in ein TelePro-Skript um: [Text]
```

```
Hier ist mein Entwurf für ein Video über [Thema] — mach daraus ein Teleprompter-Skript im TelePro-Format.
```

### Aus youtube-production

```
Konvertiere dieses youtube-production JSON in ein TelePro-Skript: [JSON]
```

---

## TelePro-Format

Das erzeugte Skript folgt der TelePro-Markdown-Syntax:

```markdown
[NOTE: SKRIPT-INFO — Format: Planet-Demo | ~5 Min | Zielgruppe: Mittelständler | Sektionen: 5]

# Hook [NOTE: Direkt in die Kamera]

##Du kennst das: Du postest ein Video, die Kommentare kommen rein — und dann sitzt du da.
##Manuell antworten. Jeden Tag. Immer wieder.
##Das muss nicht so sein.

[PAUSE:2]

##Ich zeige dir heute drei Dinge: wie die Automatisierung funktioniert, wie du Claude einrichtest — und was das für dein Engagement bedeutet.

# Was & Warum

##Also — warum macht das überhaupt Sinn?

[SLOW]
##YouTube liebt Engagement. Je schneller du antwortest, desto mehr pusht der Algorithmus dein Video.
[/SLOW]

# Key Takeaways

##Was nimmst du heute mit?

[FAST]
##Erstens: n8n + Claude lassen sich in unter einer Stunde einrichten.
##Zweitens: Der System-Prompt entscheidet über Qualität — nimm dir dafür Zeit.
##Drittens: Du sparst echte Stunden pro Woche.
[/FAST]

# CTA [NOTE: Entspannt, direkt in die Kamera]

##Wenn du den Workflow haben willst — Link in der Beschreibung.
##Wenn du Fragen hast — schreib sie in die Kommentare.
##Ich lese mit und antworte.
##Und wenn du mehr Videos wie dieses willst — Kanal abonnieren hilft uns wirklich weiter.
##Danke fürs Zuschauen. Wir sehen uns beim nächsten Video.
```

Vollständige Formatdokumentation: [`references/skript-format.md`](./references/skript-format.md)

---

## Videoformate

| Format | Länge | Struktur |
|--------|-------|----------|
| **Sonne** | 15–20 Min | Hook → Problem/Kontext → Hauptteil (3–5 Blöcke) → Key Takeaways → CTA |
| **Planet-Demo** | 4–8 Min | Hook → Was & Warum → Demo → Key Takeaways → CTA |
| **Planet-Explainer** | 5–15 Min | Hook → Kernthese → Erklärung (1–3 Blöcke) → Praktische Implikation → Key Takeaways → CTA |

---

## Zielgruppe

Optimiert für den **BUILT YouTube-Kanal** — deutschsprachige Mittelständler und Unternehmer, technisch neugierig aber ohne Entwickler-Hintergrund.

---

## Voraussetzungen

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
- [TelePro](https://github.com/a7wwiri/TelePro) für die Darstellung der erzeugten Skripte (optional)
