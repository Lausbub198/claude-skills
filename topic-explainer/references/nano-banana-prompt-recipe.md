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

## Wann KEIN Bild, sondern ein Diagramm?

- Wenn die Folie eine **Beziehung** zeigt (A führt zu B, X enthält Y).
- Wenn die Folie einen **Prozess** zeigt (Schritt 1 → 2 → 3).
- Wenn die Folie eine **Hierarchie** oder **Struktur** zeigt.
- Wenn die Folie eine **Vergleichstabelle** ist.

In diesen Fällen schreibst du im `[Visual]`-Block die Diagrammbeschreibung: welche Elemente, wie angeordnet, welche Verbindungen, ggf. Farb-Hinweis (anthrazit/teal/orange als Akzent, walnut als Hintergrund-Hint für stilistische Konsistenz).
