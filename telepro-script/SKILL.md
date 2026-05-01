---
name: telepro-script
description: >
  Erstellt fertige TelePro-Teleprompter-Skripte im korrekten TelePro-Markdown-Format für BUILT YouTube-Videos.
  Verwende diesen Skill IMMER wenn der Nutzer: ein Teleprompter-Skript, einen Prompter-Text oder einen TelePro-Text
  erstellen möchte; ein Thema oder Skript in TelePro-Format umwandeln will; Phrasen wie "schreib das als Teleprompter",
  "TelePro Skript", "Prompter Text", "formuliere das für den Teleprompter" oder "als Skript für mein Video" verwendet.
  Auch triggern wenn ein bestehendes Video-Skript (z.B. aus youtube-production A3) in TelePro-Format überführt werden soll.
metadata:
  tags: teleprompter, telepro, youtube, skript, built, prompter, video
---

# TelePro Script Creator

Dieser Skill erzeugt Teleprompter-Skripte im TelePro-Markdown-Format für BUILT YouTube-Videos.

**Format-Referenz:** `references/skript-format.md` — lies diese Datei immer, bevor du anfängst zu schreiben.

---

## Ablauf

### Schritt 1 — Input klären

Sammle folgende Informationen (nicht alles muss explizit genannt sein — inferiere aus dem Kontext):

| Parameter | Default wenn nicht angegeben |
|-----------|------------------------------|
| **Thema / Titel** | (pflichtfeld — bei Fehlen kurz nachfragen) |
| **Format** | Sonne (15–20 Min) / Planet-Demo (4–8 Min) / Planet-Explainer (5–15 Min) |
| **Zielgruppe** | Mittelständische Unternehmer, technisch neugierig aber kein Dev-Background |
| **Ton** | Kaffeegespräch mit bestem Freund — direkt, warm, ein bisschen ungeschliffen |
| **Schlüsselpunkte** | Aus Kontext ableiten |
| **Rohskript vorhanden?** | Ja (konvertieren) / Nein (neu schreiben) |

Wenn ein Rohskript oder ein JSON aus `youtube-production` vorliegt, extrahiere daraus die gesprochenen Passagen und überführe sie ins TelePro-Format.

### Schritt 2 — Struktur planen

Lege die Sektionen (`# Titel`) als Übersicht fest, bevor du in die Zeilen gehst:

**Struktur für SONNE (15–20 Min):**
```
# Hook
# Problem / Kontext
# Was wir bauen / Was wir uns anschauen
# [Demo-Sektionen 1–N]
# Ergebnis
# Key Takeaways
# CTA
```

**Struktur für PLANET-DEMO (4–8 Min):**
```
# Hook
# Was & Warum
# Demo
# Key Takeaways
# CTA
```

**Struktur für PLANET-EXPLAINER (5–15 Min):**
```
# Hook
# Kernthese
# Erklärung [1–3 Blöcke]
# Praktische Implikation
# Key Takeaways
# CTA
```

### Schritt 3 — Skript schreiben

Schreibe den vollständigen TelePro-Text. Jede Zeile die gesprochen wird, beginnt mit `##` direkt gefolgt vom Text (kein Leerzeichen).

---

## Der wichtigste Stil-Grundsatz: Kaffeegespräch, kein Nachrichtensprecher

Das ist die Seele des Skripts. Stell dir vor, du sitzt mit deinem besten Freund beim Kaffee und erklärst ihm etwas, das dich wirklich begeistert. Du redest nicht wie eine Moderatorin im Fernsehen — du redest wie ein Mensch.

Das bedeutet:
- **Keine perfekt polierten Sätze.** Ein guter Satz fängt manchmal mit "Und" oder "Also" an. Das ist kein Fehler — das ist Sprache.
- **Direkte Fragen an den Zuschauer.** "Kennst du das?", "Du fragst dich jetzt warum?", "Klingt verrückt, oder?"
- **Den Zuschauer mitnehmen.** "Stell dir das mal vor.", "Ich erkläre dir das kurz.", "Ich wette, du hast genau das schon erlebt."
- **Denk-Pausen und Wendungen.** "Und weißt du was das Verrückte daran ist?", "Warte kurz — das ist wichtig.", "Aber jetzt kommt der entscheidende Teil."
- **Ankündigen, was kommt.** Am Anfang jeder größeren Sektion kurz sagen, was man gleich zeigt. Das hilft dem Zuschauer, den Faden nicht zu verlieren.
- **Konkrete Beispiele.** Abstrakte Konzepte landen nicht — ein konkretes Bild aus dem Alltag des Zuschauers landet.

**Kaffee-Modus vs. Nachrichtensprecher — der Unterschied:**

| Nachrichtensprecher ❌ | Kaffeegespräch ✅ |
|---|---|
| `##Heute betrachten wir drei Anwendungsfälle.` | `##Ich zeige dir heute drei Dinge — und eins davon hat mich selbst überrascht.` |
| `##KI-Agenten sind autonome Systeme, die...` | `##Also — ein KI-Agent ist im Grunde wie ein Mitarbeiter, der nie schläft.` |
| `##Dies ermöglicht eine Effizienzsteigerung.` | `##Das heißt konkret: Was früher einen Tag gedauert hat, geht jetzt in einer Stunde.` |
| `##Abonnieren Sie unseren Kanal.` | `##Wenn du mehr davon willst — Kanal abonnieren, das hilft uns wirklich weiter.` |

---

## Weitere Schreibregeln

- **Kurze Sätze, aber nicht abgehackt.** Sätze können 2–3 Teile haben, wenn sie natürlich fließen. Max. ~25 Wörter pro Zeile, aber lieber natürlich als mechanisch kurz.
- **Ein Gedanke, eine Zeile.** Trenne verschiedene Gedanken auf separate `##`-Zeilen auf.
- **Kein `---` (Trennstriche).** Diese werden nicht verwendet — der Fluss kommt durch Sprache, nicht durch Trennzeichen.
- **Pausen gezielt einsetzen.** `[PAUSE:N]` nur an echten strukturellen Brüchen (z.B. nach dem Hook, nach einer Kernaussage), nicht als allgemeine Atempause zwischen Sätzen.
- **Tempo variieren.** `[SLOW]…[/SLOW]` für komplizierte oder emotionale Stellen, `[FAST]…[/FAST]` für Aufzählungen.
- **Betonung gezielt.** `**Wort**` nur für wirklich tragende Begriffe (max. 2–3 pro Sektion). `!!Nicht vergessen!!` nur für echte Call-to-Actions oder Warnungen.
- **Bilder als Placeholder.** `[IMG:storage://PLACEHOLDER-beschreibung]` wo visueller Content geplant ist.
- **Operator-Notizen.** Regieanweisungen als `[NOTE: ...]` — nie im Prompter sichtbar.

---

## Hook — PAS-Framework + Video-Roadmap

Der Hook besteht aus zwei Teilen: **PAS** + **Video-Roadmap**.

### Teil 1: PAS (Pain → Agitate → Solution)

Der Hook startet **immer mit dem Schmerz** — nicht mit einem Traumszenario, nicht mit der Lösung. Der Zuschauer muss sich im ersten Satz wiedererkennen.

```
Pain:     Den konkreten Schmerz benennen, den die Zielgruppe jetzt gerade kennt.
          "Du verbringst jeden Montag zwei Stunden damit, Rechnungen abzutippen."
          
Agitate:  Zeigen warum das wirklich nervt / teuer ist / sinnlos ist.
          "Das sind 100 Stunden im Jahr. Für etwas, das keine einzige Entscheidung braucht."
          
Solution: Das Versprechen — direkt und konkret.
          "Ich zeige dir heute, wie ein KI-Agent genau das für dich übernimmt."
```

**Falsch ❌ — Traumszenario zuerst:**
```
##Stell dir vor, du hast einen Mitarbeiter, der nie krank wird.
##Der nie Urlaub macht...
```
Das klingt wie ein Werbespot. Der Zuschauer fühlt sich nicht angesprochen — er wartet ab.

**Richtig ✅ — Schmerz zuerst:**
```
##Du kennst das: Rechnungen kommen rein, jemand muss die Daten raustippen, eintragen, abhaken.
##Jeden Tag. Immer wieder. Fehler passieren trotzdem.
##Das muss nicht so sein — und ich zeige dir heute warum.
```

Die ersten 3–5 `##`-Zeilen müssen sitzen. Kein Warm-up, kein "Willkommen zu einem neuen Video." Direkt rein.

### Teil 2: Video-Roadmap (Pflichtfeld)

Nach der PAS-Auflösung folgt eine kurze Vorschau auf das Video — was der Zuschauer gleich lernt. Das hält ihn drin.

```
##Ich zeige dir heute drei Dinge: wie KI-Agenten wirklich funktionieren, wo sie in deinem 
##Betrieb sofort Sinn machen — und wo du noch warten solltest.
```

Die Roadmap muss **konkret** sein ("drei Dinge: X, Y, Z"), nicht vage ("ich erkläre dir alles dazu"). Sie gibt dem Zuschauer das Gefühl: "Das lohnt sich bis zum Ende."

---

## Metadaten-Notiz am Anfang

Direkt nach dem ersten Abschnitt (nach dem Hook oder am Skript-Anfang) eine zusammenfassende Notiz für den Operator einfügen — **nicht** als HTML-Kommentar, sondern als `[NOTE:]`:

```
[NOTE: SKRIPT-INFO — Format: Planet-Demo | ~5 Min | Zielgruppe: Mittelständler ohne Dev-Background | Sektionen: 4]
```

Zusätzlich können relevante Produktions-Hinweise als weitere `[NOTE:]`-Zeilen am Anfang oder an den Übergängen eingefügt werden (z.B. Kamera-Hinweise, Screen-Recording-Starts).

---

## Key Takeaways — Pflichtsektion

Jedes Video braucht eine **Key Takeaways**-Sektion vor dem CTA. Sie fasst die wichtigsten Punkte zusammen — mindestens 3, gerne mehr wenn der Content es hergibt. Schnell, knapp, mit `[FAST]`.

```markdown
# Key Takeaways [NOTE: Zusammenfassung — klar und knapp halten]

##Also — was nimmst du heute mit?

[FAST]
##Erstens: [Punkt 1 — konkretes Learning].
##Zweitens: [Punkt 2 — konkretes Learning].
##Drittens: [Punkt 3 — konkretes Learning].
[/FAST]

[SLOW]
##Und das Wichtigste: [übergeordnetes Fazit in einem Satz].
[/SLOW]
```

---

## CTA — Standard-Template

Die CTA schließt immer in diesem Stil ab — menschlich, direkt, nicht verkäuferisch:

```markdown
# CTA [NOTE: Direkt in die Kamera, entspannt, leicht lächeln — kein Verkäufer-Modus]

##Wenn du heute konkret weitermachen willst — [konkrete Handlung, z.B. Link in Beschreibung].

##Wenn du Fragen hast — schreib sie in die Kommentare.
##Ich lese mit und antworte.

##Und wenn du mehr Videos wie dieses willst — Kanal abonnieren hilft uns wirklich weiter.
##Das kostet dich nichts, aber es bedeutet, dass wir weiter solche Inhalte machen können.

##Danke fürs Zuschauen. Wir sehen uns beim nächsten Video.
```

Anpassen: nur die erste Zeile variiert je nach Video (was der Zuschauer als nächstes tun soll). Der Rest bleibt.

---

## Qualitätscheckliste (intern vor Output)

- [ ] Jede gesprochene Zeile beginnt mit `##` (kein Leerzeichen danach)
- [ ] Sektionen mit `# Titel` strukturiert
- [ ] Kein `---` (Atemstriche) verwendet
- [ ] `[PAUSE:N]` nur an echten strukturellen Brüchen
- [ ] Hook startet mit SCHMERZ (nicht Traumszenario) — PAS-Framework
- [ ] Hook endet mit Video-Roadmap ("Ich zeige dir heute: X, Y, Z")
- [ ] Sprache klingt wie Kaffeegespräch, nicht wie Nachrichtensprecher
- [ ] Mindestens 3–5 direkte Zuschauer-Ansprachen ("Du", Fragen, Einbeziehung)
- [ ] Konkrete Beispiele aus dem Alltag der Zielgruppe
- [ ] Key Takeaways-Sektion vorhanden (alle Formate)
- [ ] CTA in Standard-Template-Stil
- [ ] Metadaten-`[NOTE:]` am Anfang vorhanden

---

## Output-Format

Gib das fertige Skript als **Markdown-Codeblock** aus, direkt kopierbereit für den TelePro-Editor.

Keine zusätzlichen Erklärungen oder Metadaten außerhalb des Codeblocks — nur das Skript.

---

## Beispiel-Sequenz (Kaffeegespräch-Stil)

```markdown
[NOTE: SKRIPT-INFO — Format: Planet-Demo | ~5 Min | Zielgruppe: Mittelständler | Sektionen: 4]

# Hook [NOTE: Direkt in die Kamera, entspannt stehen]

##Stell dir vor, du postest ein Video — und alle Kommentare werden automatisch beantwortet.
##Nicht von einem stupiden Bot, der generischen Unsinn schreibt.
##Sondern von einer KI, die klingt wie du. Deine Worte. Dein Ton.

[PAUSE:2]

##Ich zeige dir heute genau, wie das geht — mit zwei Tools, die du heute noch einrichten kannst.

# Was & Warum [NOTE: Ruhiger Erklär-Modus]

##Das Problem kennst du wahrscheinlich.
##Du postest ein Video, die Kommentare kommen rein — und dann sitzt du da und antwortest manuell.
##Stundenlang. Jedes Mal wieder.

##Und weißt du was? Das macht einen Unterschied. Nicht nur für dich — für den Algorithmus.
##YouTube liebt Engagement. Je schneller du antwortest, desto mehr pusht YouTube dein Video.

[SLOW]
##Also: Automatisch antworten ist nicht lazy. Es ist strategisch.
[/SLOW]
```
