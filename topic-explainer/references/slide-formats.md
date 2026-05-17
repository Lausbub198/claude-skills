# Didaktische Format-Auswahl

Du hast pro Folie/Sektion mehrere Formate zur Auswahl. Das Ziel: Abwechslung schaffen, ohne willkürlich zu sein. Wähle nach didaktischer Funktion.

## Präsentations-Modus vs. Handout-Modus

Bevor du Format-Kategorien wählst, klär den Modus (wird in Phase 1 mit dem User entschieden):

### Handout-Modus (Default für selbsterklärendes Material)
Die Folie wird **gelesen, nicht vorgetragen**. Sie muss alleine funktionieren.

- Ganze Sätze, eingebettete Erklärungen, alle Beispiele sichtbar
- Pro Folie 50–150 Wörter ist OK
- Alle Format-Optionen unten (Absatz, Bullet, Tabelle, Analogie, Schritt-für-Schritt, Q&A) sind in voller Länge erlaubt

### Präsentations-Modus
Der Sprecher trägt vor. Die Folie ist **Erinnerung und Visualisierung** — nicht Skript.

- Pro Folie **max. ~30 Wörter** Text gesamt
- Format-Optionen werden gekürzt:
  - **Absatz** → ein kurzer Kernsatz (max 12 Wörter)
  - **Bullet-Liste** → max 3 Bullets, je 3–5 Wörter
  - **Vergleich** → Tabelle nur mit Stichworten, keine Sätze
  - **Analogie** → nur die Bild-Idee, nicht die Erklärung ("Wie Autocomplete — aber gigantisch")
  - **Schritt-für-Schritt** → nummerierte Stichworte, max 5 Wörter pro Schritt
- Visual nimmt mehr Raum ein als Text
- Falls der User es möchte: Speaker Notes als separater Block je Folie (siehe Hybrid)

### Hybrid-Modus
Sparse Folie wie Präsentation, aber zusätzlich ein **Speaker Notes:**-Block mit 2–4 Sätzen direkt darunter — das, was der Sprecher dazu sagt. So bekommt der Sprecher seinen Spickzettel und die Folie bleibt clean.

**Beispiel-Folie im Hybrid-Modus:**

```
### Folie 5: Der Trick mit der Attention

**Inhalt:**
Das Modell schaut auf alle Wörter — und gewichtet, was gerade wichtig ist.

**Speaker Notes:**
Hier ist der Aha-Moment. Stell dir den Satz "Die Katze, die ich gestern gesehen habe, schläft" vor. Für "schläft" muss das Modell wissen, dass die Katze schläft — nicht das Gestern. Attention verteilt Aufmerksamkeit auf alle anderen Wörter. Hohe Scores = starke Verbindung.

**Visual:**
[Diagramm: Satz horizontal, "schläft" mit orange Glow, dickste teal Linie zur "Katze"…]
```

---


## Format-Katalog

### 1. Kurzer Absatz (3–4 Sätze)
**Nimm wenn:** Du eine Idee, ein Konzept oder eine Definition vermitteln willst, die einen kleinen Erzählbogen braucht. Gut für Einstiegsfolien, Begriffsklärungen, Schluss-Sektionen mit Ausblick.

**Vermeide wenn:** Der Inhalt mehr als 3 unabhängige Punkte hat — dann Liste.

**Mini-Beispiel:**
> Ein KI-Modell ist im Grunde ein riesiger Mustererkenner. Es hat Millionen von Beispielen gesehen — Texte, Bilder, Code — und merkt sich, welche Bausteine oft zusammen auftreten. Wenn du ihm eine neue Aufgabe gibst, rät es einfach die wahrscheinlichste Antwort. Klingt simpel — funktioniert verblüffend gut.

---

### 2. Bullet-Liste (3–6 Punkte)
**Nimm wenn:** Du eine Aufzählung gleichrangiger Punkte hast — Vorteile, Funktionen, Schritte, Eigenschaften.

**Vermeide wenn:** Die Punkte aufeinander aufbauen (dann Schritt-für-Schritt) oder es nur 2 Punkte sind (dann Vergleich oder Absatz).

**Mini-Beispiel:**
> **Was ein LLM gut kann:**
> - Texte zusammenfassen
> - In andere Sprachen übersetzen
> - Code-Snippets schreiben
> - Fragen aus großen Dokumenten beantworten

---

### 3. Vergleichstabelle (2–3 Spalten)
**Nimm wenn:** Du zwei Dinge gegenüberstellst — vorher/nachher, klassisch/modern, Option A/Option B, Mythos/Realität.

**Vermeide wenn:** Es nur eine Sache zu erklären gibt.

**Mini-Beispiel:**
> | Klassische Suche | KI-Chat |
> |---|---|
> | Keywords eingeben | Natürliche Frage stellen |
> | Liste von Links | Direkte Antwort |
> | Du klickst dich durch | Antwort kommt sofort |

---

### 4. Analogie-Box ("Stell dir vor…")
**Nimm wenn:** Das Konzept abstrakt ist und ein 20-Jähriger keinen Anker hat. Vergleich mit etwas aus dem Alltag.

**Vermeide wenn:** Das Konzept selbst schon konkret/anschaulich ist.

**Mini-Beispiel:**
> **Stell dir vor:** Ein LLM ist wie ein Kellner, der eine Million Speisekarten auswendig kann. Du sagst "ich will was Italienisches, leicht, scharf" — und er empfiehlt dir blitzschnell ein Gericht. Er hat es nie gekocht. Er kennt nur die Muster.

---

### 5. Schritt-für-Schritt-Liste (nummeriert)
**Nimm wenn:** Eine Reihenfolge wichtig ist — ein Prozess, eine Anleitung, eine Entstehungsgeschichte.

**Vermeide wenn:** Die Reihenfolge egal ist (dann normale Bullet-Liste).

**Mini-Beispiel:**
> **So entsteht eine KI-Antwort:**
> 1. Du tippst eine Frage
> 2. Die KI zerlegt sie in kleine Bausteine (Tokens)
> 3. Sie rät, was als Nächstes kommen sollte
> 4. Sie tut das Wort für Wort, bis die Antwort fertig ist

---

### 6. Diagrammbeschreibung (als Inhalt selbst)
**Nimm wenn:** Eine Beziehung oder ein Aufbau am besten visuell wirkt UND du das Bild selbst auch im Inhaltsblock erklären willst (z.B. weil die Folie sonst leer wirkt).

**Vermeide wenn:** Du eh schon ein separates Visual hast — dann reicht eine kurze Bildunterschrift.

**Mini-Beispiel:**
> **Aufbau:** Drei Kästen nebeneinander. Links "Eingabe" (Sprechblase mit Frage), Mitte "Modell" (Wolke mit "LLM" beschriftet), rechts "Ausgabe" (Sprechblase mit Antwort). Pfeile von links nach rechts. Unter dem Mittel-Kasten ein Annotation: "Hier passiert die Magie — Mustererkennung."

---

### 7. Frage → Antwort (Q&A)
**Nimm wenn:** Du eine wahrscheinliche User-Frage proaktiv aufgreifen willst, z.B. "Aber ist das nicht teuer?" oder "Was ist mit Datenschutz?".

**Vermeide wenn:** Das nicht zur Stelle in der Lerngeschichte passt — Q&A wirkt aufgesetzt, wenn man es überall macht.

**Mini-Beispiel:**
> **Frage:** Halluziniert die KI nicht ständig?
> **Antwort:** Manchmal ja — und genau deshalb prüft man wichtige Antworten immer noch. Aber: je besser das Modell und je präziser die Frage, desto seltener passiert es.

---

## Abwechslungs-Rezept

Wenn du 6–9 Folien hast, sollte dein Format-Mix etwa so aussehen:

- 1–2× Absatz
- 1–2× Bullet-Liste
- 1× Analogie
- 1× Vergleich oder Q&A
- 1× Schritt-für-Schritt (wenn Prozess vorkommt)
- Rest: Mix

**Daumenregel:** Zwei Folien in Folge dürfen nie das gleiche Format haben. Wenn doch — refactor.
