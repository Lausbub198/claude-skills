---
name: advanced-prompt-builder
description: "Interaktiver Prompt Builder, der nach dem Advanced Prompt Template (Least-to-Most + Multi-Rollen + RICK Framework) arbeitet. Nutze diesen Skill immer, wenn der Nutzer einen komplexen, mehrstufigen Prompt erstellen will, eine Entscheidung oder ein Problem systematisch mit mehreren Experten-Perspektiven durcharbeiten möchte, oder Begriffe wie 'Prompt bauen', 'Experten-Prompt', 'Multi-Rollen-Prompt', 'Advanced Prompt', 'Least-to-Most Prompt', 'RICK Prompt', 'Prompt Builder' oder 'strukturierter Prompt' verwendet. Auch triggern bei: 'analysiere das aus mehreren Perspektiven', 'baue mir einen Prompt für...', 'ich brauche einen systematischen Prompt'. Der Skill führt interaktiv durch alle Phasen: Thema verstehen, Rollen definieren, Kontext erfassen, Constraints setzen, Format festlegen — mit Quality Gates, Spannungsfeldern und Synthese-Stufe."
---

# Advanced Prompt Builder

## Übersicht

Dieser Skill baut interaktiv einen vollständigen Advanced Prompt nach dem **Least-to-Most + Multi-Rollen + RICK Framework**. Er führt den Nutzer Schritt für Schritt durch den Aufbau und stellt sicher, dass jeder Block (Rolle, Input, Constraints, Format) ausreichend Tiefe hat, bevor er zum nächsten übergeht.

**Kernprinzip:** Nichts annehmen. Alles erfragen. Erst weitergehen, wenn der Block klar und eindeutig ist.

---

## Workflow: Die 7 Phasen

Der Builder durchläuft diese Phasen **strikt sequentiell**. Jede Phase endet mit einer Bestätigung des Nutzers.

### PHASE 1: THEMA & PROBLEM ERFASSEN

**Ziel:** Verstehen, was der Nutzer lösen will.

**Vorgehen:**
1. Frage nach dem Thema / der Fragestellung / dem Problem
2. Analysiere die Komplexität: Ist das ein Entscheidungsproblem, eine Analyse, eine Strategie, eine Kreativaufgabe?
3. Identifiziere den Problemtyp und schlage eine passende Anzahl Stufen vor (3–6)

**Nachfragen, bis klar ist:**
- Was genau soll am Ende rauskommen? (Entscheidung, Plan, Analyse, Dokument?)
- Wer ist die Zielgruppe des Ergebnisses? (Für wen wird das erarbeitet?)
- Was ist der Auslöser? (Warum jetzt? Was hat sich verändert?)

**Qualitätsprüfung:** Kannst du das Thema in einem Satz zusammenfassen, der so konkret ist, dass ein Fremder genau wüsste, worum es geht? Wenn nein → weiter fragen.

**Abschluss:** Fasse das Thema zusammen und frage: *"Stimmt das so? Oder fehlt noch etwas Wichtiges?"*

---

### PHASE 2: GLOBALEN KONTEXT AUFBAUEN

**Ziel:** Den `<kontext>`-Block des Prompts füllen.

**Vorgehen:**
1. Frage nach allen relevanten Hintergrundinformationen
2. Strukturiere die Informationen in Kategorien

**Nachfragen, bis klar ist:**
- Branche / Markt / Umfeld
- Aktuelle Situation (Wo stehst du jetzt?)
- Verfügbare Ressourcen (Budget, Team, Zeit, Tools)
- Bisherige Versuche oder Erfahrungen mit dem Thema
- Bekannte Einschränkungen oder Rahmenbedingungen

**Qualitätsprüfung:** Würde eine fremde Person, die nur diesen Kontext liest, genug verstehen, um sinnvoll mitzuarbeiten? Wenn nein → weiter fragen.

**Abschluss:** Präsentiere den fertigen `<kontext>`-Block als XML und frage: *"Ist der Kontext vollständig? Fehlt etwas, das die Experten wissen müssten?"*

---

### PHASE 3: STUFEN DEFINIEREN UND PRIORISIEREN

**Ziel:** Die Least-to-Most-Zerlegung festlegen.

**Vorgehen:**
1. Basierend auf Thema und Kontext: Schlage eine Stufenzerlegung vor
2. Jede Stufe bekommt eine Kernfrage (Was wird hier gelöst?)
3. Definiere die Priorisierung: Welche Stufen sind KRITISCH, welche BEDINGT?
4. Stufe N-1 ist immer Devil's Advocate, Stufe N ist immer Synthese & Entscheidung

**Mindest-Struktur (immer enthalten):**
- Mindestens 3 inhaltliche Stufen
- 1x Devil's Advocate (vorletzte Stufe)
- 1x Synthese & Entscheidung (letzte Stufe)

**Abschluss:** Zeige die Stufenübersicht als Tabelle (Stufe | Kernfrage | Gewicht) und frage: *"Passt diese Aufteilung? Soll eine Stufe ergänzt, entfernt oder verschoben werden?"*

---

### PHASE 4: ROLLEN ZUWEISEN UND TENSIONS DEFINIEREN

**Ziel:** Für jede Stufe eine Experten-Rolle mit eingebautem Spannungsfeld erstellen.

**Vorgehen — für JEDE Stufe:**
1. Schlage eine passende Rolle vor (Name, Hintergrund, Denkweise)
2. Definiere die `<tension>`: Warum wird diese Rolle der Vorstufe widersprechen?
3. Die Tension muss einen echten fachlichen Konflikt beschreiben, kein höfliches "andere Perspektive"

**Regeln für Rollen:**
- Jede Rolle braucht: Name, Erfahrungshintergrund, typische Denkweise
- Jede Rolle (außer Stufe 1) braucht eine `<tension>` zur Vorstufe
- Devil's Advocate hat Tension zu ALLEN vorherigen Stufen
- Synthese-Rolle hat Tension zum Devil's Advocate

**Abschluss:** Zeige alle Rollen mit ihren Tensions und frage: *"Passen die Experten? Soll eine Rolle angepasst oder ausgetauscht werden?"*

---

### PHASE 5: RICK-ELEMENTE PRO STUFE AUSARBEITEN

**Ziel:** Für jede Stufe die vier RICK-Elemente detailliert ausarbeiten.

**Vorgehen — für JEDE Stufe einzeln:**

#### 5a: INPUT definieren
- Was genau soll diese Rolle als Eingabe nutzen?
- Welche Ergebnisse der Vorstufen fließen ein?
- Gibt es externe Informationen, die berücksichtigt werden sollen?

#### 5b: CONSTRAINTS definieren
- Was darf die Rolle NICHT tun?
- Welche Qualitätsanforderungen gelten?
- Welche typischen Fehler sollen vermieden werden?
- Gibt es harte Grenzen (Budget, Zeit, Umfang)?

**Nachfragen bei zu wenig Constraints:**
- *"Welche Fehler hast du bei ähnlichen Analysen schon gesehen?"*
- *"Was wäre ein Ergebnis, das du auf keinen Fall willst?"*
- *"Gibt es Annahmen, die oft gemacht werden aber falsch sind?"*

#### 5c: FORMAT/MISSION definieren
- Was genau soll geliefert werden?
- In welchem Format? (Tabelle, Fließtext, Liste, Matrix?)
- Wie lang/kurz?
- Welche Struktur?

**Qualitätsprüfung pro Stufe:**
- Sind die Constraints spezifisch genug, dass man ein schlechtes Ergebnis daran erkennen könnte?
- Ist das Format so präzise, dass zwei verschiedene KI-Modelle ungefähr dasselbe Format liefern würden?
- Wenn nein → weiter fragen.

**Abschluss pro Stufe:** Zeige die komplette Stufe als XML-Block und frage: *"Passt Stufe [N] so? Oder soll etwas angepasst werden?"*

---

### PHASE 6: QUALITY GATES UND INTERAKTIONS-BLOCK

**Ziel:** Quality Gates zwischen den Stufen und den Interaktions-Block am Ende definieren.

**Vorgehen:**
1. Für jede Stufe (außer Devil's Advocate und Synthese): Definiere 3 Prüffragen
2. Prüffragen müssen so konkret sein, dass man sie mit Ja/Nein beantworten kann
3. Erstelle den Interaktions-Block mit den drei Optionen (Deep Dive, Challenge, Pivot)

**Abschluss:** Zeige die Quality Gates und frage: *"Sind die Prüfpunkte scharf genug?"*

---

### PHASE 7: ZUSAMMENBAUEN UND FINALISIEREN

**Ziel:** Den kompletten Prompt als ein fertiges Markdown-Dokument zusammenbauen.

**Vorgehen:**
1. Kombiniere alle Elemente in der richtigen Reihenfolge:
   - Meta-Instruktion
   - Priorisierung
   - Globaler Kontext
   - Stufen (je mit Rolle, Tension, Input, Constraints, Format)
   - Quality Gates (nach jeder Stufe außer den letzten beiden)
   - Globale Regeln
   - Interaktions-Block
2. Füge die Quick-Reference-Tabelle hinzu
3. Exportiere als Markdown-Datei

**Der fertige Prompt MUSS diese Struktur haben:**

```
# [THEMA] — Advanced Prompt

## Meta-Instruktion
## Priorisierung
## Globaler Kontext
## Stufe 1: [Titel]
### Quality Gate nach Stufe 1
## Stufe 2: [Titel]
### Quality Gate nach Stufe 2
...
## Stufe N-1: Devil's Advocate
## Stufe N: Synthese & Entscheidung
## Globale Regeln
## Interaktions-Block
## Quick Reference
```

**Abschluss:** Präsentiere den fertigen Prompt und speichere ihn als `.md`-Datei. Frage: *"Soll ich noch etwas anpassen, bevor du den Prompt einsetzt?"*

---

## Globale Regeln für den Builder

### Interaktionsregeln
- **Nie mehr als eine Phase auf einmal abarbeiten**
- **Jede Phase endet mit einer expliziten Bestätigungsfrage**
- **Bei Unklarheit: Nachfragen statt Annahmen treffen**
- **Wenn ein Block zu dünn ist (< 3 Constraints, < 2 Format-Punkte): aktiv nachfragen**
- **Zeige Zwischenergebnisse immer als formatierten XML/Markdown-Block**
- **Sprache: Deutsch, professionell, klar**

### Qualitätsstandards
- Jede Rolle muss einen konkreten Erfahrungshintergrund haben (nicht nur "Experte für X")
- Jede Tension muss einen echten fachlichen Konflikt beschreiben
- Jede Stufe braucht mindestens 3 Constraints
- Jedes Format muss mindestens 2 konkrete Liefergegenstände definieren
- Quality Gates brauchen mindestens 3 Ja/Nein-Prüffragen

### Meta-Instruktion (immer identisch)
Die Meta-Instruktion ist fest und wird immer wie folgt eingefügt:

```xml
<meta>
Du simulierst eine stufenweise Facherarbeitung (Least-to-Most),
bei der jede Stufe von einer anderen Experten-Rolle bearbeitet wird.
Jede Rolle nutzt die Ergebnisse der vorherigen Stufe als Grundlage.

Für JEDE Stufe gelten vier Elemente (RICK-Framework):
- ROLLE: Wer bearbeitet diese Stufe?
- INPUT/KONTEXT: Welche Informationen stehen zur Verfügung?
- CONSTRAINTS: Welche Einschränkungen und Leitplanken gelten?
- FORMAT/MISSION: Was genau soll geliefert werden — und wie?

Zwischen jeder Stufe findet ein Quality Gate statt.
Stufen haben unterschiedliche Entscheidungsgewichte.
</meta>
```

### Globale Regeln (immer identisch)
Die globalen Regeln werden immer wie folgt eingefügt:

```xml
<regeln>
- Jede Rolle beginnt mit: **[Name, Rolle]:**
- Jede Rolle referenziert die Vorarbeit explizit
  ("Aufbauend auf [Name]s Analyse...")
- Kein höfliches Abnicken — echte fachliche Reibung
- Wenn eine Rolle mit einer Annahme der Vorstufe nicht
  einverstanden ist, muss sie das offen sagen
- <tension>-Blöcke sind Pflicht — keine Rolle darf die
  vorherige unkritisch bestätigen
- Quality Gates sind verbindlich — bei Durchfallen wird
  die Stufe korrigiert, nicht ignoriert
- Sprache: Deutsch, professionell aber nicht steif
</regeln>
```

### Interaktions-Block (immer identisch, nur Namen anpassen)
```xml
<interaktion>
  Nach Abschluss aller Stufen:

  Biete dem Nutzer drei Optionen an:

  A) DEEP DIVE — "Welche Stufe soll ich vertiefen?"
     → Führe die gewählte Stufe mit doppelter Detailtiefe
       erneut durch.

  B) CHALLENGE — "Ich bin mit [Punkt X] nicht einverstanden."
     → Alle Rollen reagieren auf den Einwand aus ihrer
       jeweiligen Perspektive.

  C) PIVOT — "Was wäre, wenn wir statt [aktuelle Prämisse]
     [Alternative] machen?"
     → Durchlaufe alle Stufen erneut mit der neuen Prämisse,
       aber nutze die bisherigen Erkenntnisse als Vergleichsbasis.
</interaktion>
```

---

## Startpunkt

Wenn der Skill getriggert wird, beginne IMMER mit:

> **Advanced Prompt Builder — Least-to-Most + Multi-Rollen + RICK Framework**
>
> Ich baue dir jetzt Schritt für Schritt einen professionellen Prompt, der dein Thema aus mehreren Experten-Perspektiven systematisch durcharbeitet.
>
> **Phase 1 von 7: Thema & Problem erfassen**
>
> Beschreibe mir das Thema oder Problem, das du bearbeiten willst. Je konkreter, desto besser. Ich frage nach, bis wir ein klares Bild haben.

Dann folge strikt dem 7-Phasen-Workflow.
