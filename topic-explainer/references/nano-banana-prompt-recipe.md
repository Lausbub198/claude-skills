# Nano Banana 2 Prompt-Rezept

Nano Banana 2 ist Googles Bildgenerator (Gemini Flash). Er versteht englische, beschreibende Prompts gut, wenn sie wie ein Foto-Briefing formuliert sind: Was ist im Bild, wie ist es aufgebaut, wie ist es beleuchtet, welcher Stil.

## Die vier Pflicht-Keywords

Jeder Prompt MUSS am Ende diese vier Stil-Keywords als kommagetrennte Liste enthalten:

```
dark modern minimalist, cinematic, teal and orange, walnut wood
```

Reihenfolge: ist egal, aber alle vier müssen drin sein. **Wenn auch nur einer fehlt, ist der Prompt unbrauchbar** — die Bilder sehen sonst nicht zueinander passend aus.

## Prompt-Aufbau (5 Bausteine)

```
[Subject] in [Composition], [Lighting], [Material/Texture detail], [Style keywords]
```

1. **Subject** — was/wer ist im Bild? Konkret. ("a single matte black microphone" — nicht "a microphone")
2. **Composition** — Wo im Bild, Perspektive. ("centered, low angle, shallow depth of field", "extreme close-up", "wide establishing shot")
3. **Lighting** — Wie ist es beleuchtet. ("rim light from the left, soft ambient fill", "single warm key light, deep shadows")
4. **Material/Texture** — kleine Details die das Bild greifbar machen. ("brushed metal", "subtle smoke in the background", "rain droplets on glass")
5. **Style keywords** — die vier Pflicht-Keywords + ggf. weitere ("photorealistic", "shot on 35mm", "8k")

## Was du vermeiden solltest

- Text/Schrift im Bild — Nano Banana 2 ist nicht gut darin, lesbaren Text zu rendern. Wenn du Beschriftungen brauchst, mach lieber ein Diagramm.
- Gesichter von realen Personen — keine Promis, keine namentlich bekannten Personen.
- Übertriebene Adjektiv-Salate — 5 starke Worte schlagen 20 schwache.
- Conflicting moods — "joyful, melancholic, energetic" geht nicht. Ein Mood pro Bild.

## Beispiel-Prompts für typische Folien-Visuals

### Konzept-Hero (Einstiegsfolie, atmosphärisch)
```
A single glowing data orb floating above a dark walnut wood table, centered composition, low angle, soft rim light from teal source behind, warm orange ambient bounce on the wood grain, subtle dust particles in the air, dark modern minimalist, cinematic, teal and orange, walnut wood, photorealistic, shallow depth of field
```

### Process-Backdrop (Hintergrund für eine Schritt-Liste, abstrakt)
```
Abstract dark anthracite background with subtle vertical light streaks in teal, orange highlights in the lower third, walnut wood texture barely visible at the edges, very minimal, cinematic wide composition, dark modern minimalist, cinematic, teal and orange, walnut wood, no text, no people
```

### Object-Symbol (steht für ein Konzept, z.B. "Sicherheit" oder "KI")
```
A matte black padlock resting on dark walnut wood, extreme close-up, single warm orange key light from upper left, deep shadows, brushed metal texture, ambient teal reflection on the lock body, dark modern minimalist, cinematic, teal and orange, walnut wood, photorealistic, 35mm lens
```

### Character-Vignette (Person im Bild, Schulterhöhe von hinten o.ä.)
```
Silhouette of a person from behind, sitting at a walnut wood desk, looking at a glowing teal screen, warm orange backlight from a window on the right, deep ambient shadows, minimal scene, no faces visible, cinematic atmosphere, dark modern minimalist, cinematic, teal and orange, walnut wood, photorealistic, shot on 35mm
```

### Comparison-Split (zwei Konzepte gegenüber, z.B. "alt vs. neu")
```
Split composition, left side a worn old paper folder on dark wood, right side a floating glowing teal hologram of the same folder, centered camera, dramatic orange rim light on both objects, deep dark background, dark modern minimalist, cinematic, teal and orange, walnut wood, photorealistic, shallow depth of field
```

---

## Zwei Bild-Familien: Atmosphäre ODER Erklär-Skizze

Es gibt **zwei verschiedene Arten von Visuals** in einem Deck. Sie haben unterschiedliche Aufgaben — und unterschiedliche Stile.

### Familie 1 — **Atmosphäre** (das Cinematic-Hero, oben gezeigt)
Aufgabe: Stimmung setzen, Aufmerksamkeit holen, ein Konzept symbolisch verdichten.
**Nimm wenn:** Einstiegsfolie, Übergangs-Folie, Abschluss-Folie, eine Folie die emotional aufladen soll.
Stil: photorealistisch, atmosphärisch, ein Objekt im Fokus, dramatic light. Keine Beschriftungen, keine Erklärung — nur Vibe.

### Familie 2 — **Erklär-Skizze** (didaktisch, NEU)
Aufgabe: Den Folieninhalt visuell ERKLÄREN. Das Visual selbst trägt zum Verständnis bei.
**Nimm wenn:** Eine Folie ein Konzept, einen Prozess, eine Zerlegung, eine Beziehung erklärt. Also: 80 % aller didaktischen Folien.
Stil: vier konkrete Optionen unten (A/B/C/D). Mit beschrifteten Mini-Elementen, Pfeilen, kleinen Mockups.

**Daumenregel:**
- Pro Deck **maximal 1–2 Atmosphäre-Visuals** (Intro + Outro reichen).
- Der Rest = Erklär-Skizzen. Wenn das Visual nichts beiträgt zum Verständnis, ist es Deko — und Deko sollte selten sein.

---

## Erklär-Skizzen — die vier Stile

Alle vier behalten die **Brand-Konstanten** (`dark, anthracite, teal and orange, walnut wood`), variieren aber den Render-Stil. Wähle pro Folie den passenden.

### Stil A — **Engineer's Sketchbook** (handgezeichnet, organisch)
Wirkt wie eine Seite aus einem Engineer-Moleskine, das auf Walnussholz liegt. Tinte + leichter Aquarell-Wash. Am authentischsten "von Hand gedacht".
**Nimm wenn:** Konzept-Erklärung, "so funktioniert es"-Folie, Workshop-Vibe.

Template (Beispiel: Tokens):
```
A page from an engineer's sketchbook lying on dark walnut wood, cinematic side lighting from upper left, hand-drawn ink illustration showing the German word "unglaublich" with three vertical scissors-cut marks splitting it into three pieces "un | glaub | lich", arrows below pointing down to three small numbered boxes "847" "1923" "612", loose pen sketch with subtle teal and orange watercolor washes, slight pencil shading, handwritten caption "Tokens — die kleinsten Bausteine", dark anthracite background, walnut wood desk visible at the edges, dark modern minimalist, cinematic, teal and orange, walnut wood
```

### Stil B — **Editorial Tech Illustration** (NYT-Vibe, polished)
Polierte Flat-/Vektor-Illustration wie eine NYT/The-Verge-Tech-Section. Stilisiert, aber konkret. Wirkt "redaktionell" und sauber.
**Nimm wenn:** Folie soll professionell/publikationsreif wirken (Pitch, Sales, externe Präsentation).

Template (Beispiel: Tokens):
```
Editorial-style flat illustration: the word "unglaublich" rendered large in clean type at the top, breaking apart mid-word into three floating segments "un", "glaub", "lich" connected by glowing teal arrows pointing down to three rounded number cards "847", "1923", "612" on a dark anthracite background, walnut wood texture as a thin baseline strip, warm orange accent dots, soft drop shadows, minimal labels, New York Times tech section aesthetic, dark modern minimalist, cinematic, teal and orange, walnut wood
```

### Stil C — **Premium Schematic Diagram** (Boxen + Pfeile, Apple-Keynote-Vibe)
Reines Schema (Boxen, Pfeile, Labels) — aber kinematisch beleuchtet und tief gerendert. Maximal didaktisch, am nüchternsten.
**Nimm wenn:** Architektur, Pipeline, Datenfluss, Komponenten-Beziehung. Wenn "nüchtern und glasklar" gewünscht ist.

Template (Beispiel: Tokens):
```
A clean schematic diagram on a dark anthracite background: at the top a single rounded rectangle labeled "unglaublich" in white type, a thick teal arrow pointing down to three smaller rounded rectangles in a row labeled "un", "glaub", "lich", below each a second teal arrow to a small dark card with a glowing orange number "847", "1923", "612", thin walnut wood baseline grain at the bottom edge, dramatic single light source from upper right casting subtle long shadows behind each card, generous negative space, no other elements, dark modern minimalist, cinematic, teal and orange, walnut wood
```

### Stil D — **3-Panel Mini-Comic** (Vorher → Mitte → Nachher)
Dreigeteilter Mini-Strip, der einen Prozess in drei Stufen zeigt. Am stärksten bei "etwas verändert sich"-Folien.
**Nimm wenn:** Vorher/Nachher, Transformations-Sequenz, vor-Schnitt vs. nach-Schnitt, alt vs. neu.

Template (Beispiel: Tokens):
```
Three-panel horizontal comic strip on a dark walnut wood surface, soft cinematic lighting: Panel 1 (left) shows a small speech bubble with the word "unglaublich"; Panel 2 (center) shows the same word with three teal vertical cut-lines splitting it into "un|glaub|lich"; Panel 3 (right) shows three small orange number cards "847", "1923", "612" stacked vertically; each panel framed with a thin walnut border, arrows between panels, hand-illustrated outline style with light watercolor fills, dark modern minimalist, cinematic, teal and orange, walnut wood
```

---

## Stil-Wahl-Tabelle — schnell entscheiden

| Folien-Typ | Empfohlener Stil |
|---|---|
| Einstieg / Outro / emotionaler Moment | **Cinematic-Hero** (oben) |
| Konzept erklären, "so funktioniert es" | **A — Sketchbook** |
| Pitch / externe Präsi / publikationsreif | **B — Editorial** |
| Architektur, Pipeline, Datenfluss | **C — Schematic** |
| Vorher → Nachher, Transformation | **D — 3-Panel Comic** |
| Reine Vergleichstabelle / Hierarchie | **Diagramm-Beschreibung** (siehe nächster Abschnitt) |

**Konsistenz-Tipp:** Pro Deck **nicht mehr als 2 verschiedene Erklär-Stile mischen** (z.B. A + C). Sonst wirkt das Deck unruhig. Cinematic-Hero zählt separat und darf zusätzlich rein für Intro/Outro.

---

## Anpassen der Templates auf dein Konzept

Die vier Templates oben sind für "Tokens" geschrieben. Für ein anderes Konzept ersetzt du:

1. **Das Subject** (in Stil A das "Wort unglaublich", in Stil C die "rounded rectangle labeled X")
2. **Die konkreten Elemente** (was wird zerlegt/verbunden/dargestellt)
3. **Die Caption** (in Stil A der handschriftliche Text unten)

Alles andere — Render-Stil-Vokabular, Brand-Keywords, Lighting — **bleibt unverändert**. So bleibt der Look konsistent über alle Folien.

---

## Wann KEIN Bild, sondern ein Diagramm?

- Wenn die Folie eine **Beziehung** zeigt (A führt zu B, X enthält Y).
- Wenn die Folie einen **Prozess** zeigt (Schritt 1 → 2 → 3).
- Wenn die Folie eine **Hierarchie** oder **Struktur** zeigt.
- Wenn die Folie eine **Vergleichstabelle** ist.

In diesen Fällen schreibst du im `[Visual]`-Block die Diagrammbeschreibung: welche Elemente, wie angeordnet, welche Verbindungen, ggf. Farb-Hinweis (anthrazit/teal/orange als Akzent, walnut als Hintergrund-Hint für stilistische Konsistenz).
