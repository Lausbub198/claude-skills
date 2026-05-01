# TelePro Skript-Format

## Grundprinzip

**Nur Zeilen mit `##` werden im Prompter angezeigt.**  
Alles andere (Überschriften, Pausen, Bilder, Notizen, leere Zeilen, normaler Text) ist Struktur oder wird ignoriert.

---

## Struktur-Elemente

### Sektion / Überschrift

```
# Titel der Sektion
```

- Beginnt mit `# ` (Rautezeichen + Leerzeichen)
- Erscheint im Prompter in **Cyan** (wenn „Überschriften anzeigen" aktiv)
- Wird in der Sektions-Outline aufgelistet (Sprungmarke)
- Darf Inline-Markup (`**…**`, `!!…!!`) und `[NOTE:…]` enthalten

### Sprechtext

```
##Das ist der Text, den du liest.
##Kein Leerzeichen zwischen ## und Text!
```

- Beginnt mit `##` direkt gefolgt vom Text (kein Leerzeichen nach `##`)
- Wird im Prompter in **Weiß** angezeigt
- Darf Inline-Markup enthalten

---

## Inline-Markup

Inline-Markup funktioniert nur innerhalb von `##`-Zeilen und `# `-Überschriften.

### Betont — Blau

```
##Das ist **wichtig** zu sagen.
```

`**Wort**` → wird in Blau dargestellt

### Trigger / Nicht-vergessen — Rot

```
##Jetzt kommt !!der entscheidende Moment!!.
```

`!!Wort!!` → wird in Koralle/Rot dargestellt

---

## Pausen

### Atempause

```
---
```

Exakt drei Bindestriche auf einer eigenen Zeile. Kurzer visueller Indikator im Prompter, kein Countdown.

### Timed Pause mit Countdown

```
[PAUSE:3]
[PAUSE:5]
```

Stoppt den Scroll für N Sekunden und zeigt einen Countdown an. N = beliebige ganze Zahl (Sekunden).

---

## Geschwindigkeits-Zonen

```
[SLOW]
##Dieser Text wird langsamer gelesen.
##Noch eine langsame Zeile.
[/SLOW]

[FAST]
##Hier geht es schneller.
[/FAST]
```

- `[SLOW]` / `[/SLOW]` — reduziert die Scroll-Geschwindigkeit (Faktor in Settings einstellbar)
- `[FAST]` / `[/FAST]` — erhöht die Scroll-Geschwindigkeit
- Gilt für alle Zeilen innerhalb des Blocks, einschließlich `# `-Überschriften

---

## Bilder

```
[IMG:storage://uuid-des-bildes]
[IMG:storage://uuid-des-bildes|duration=8]
```

- Bild aus der Bibliothek — per Drag & Drop oder über den **🖼 Bild**-Button einfügen
- Beim Erreichen des oberen Bildrandes stoppt der Scroll automatisch
- Countdown läuft für die eingestellte Dauer, danach geht der Scroll weiter
- `|duration=8` überschreibt die globale Standard-Dauer aus den Settings
- Die UUID wird beim Einfügen automatisch generiert — nicht manuell eingeben

---

## Operator-Notizen

Notizen sind **niemals im Prompter sichtbar**. Sie erscheinen im Notiz-Overlay (rechts oben im Prompter), wenn die zugehörige Zeile die Leseposition passiert.

### Standalone-Notiz (eigene Zeile)

```
[NOTE: Kamera-Cut hier!]
[NOTE: Pause, bis Applaus aufhört]
```

### Inline-Notiz (an Überschrift oder Sprechtext angehängt)

```
# Einleitung [NOTE: Kurze Anmoderation, max 30 Sek.]
##Das ist der Text. [NOTE: Langsam sprechen]
```

Der Notiztext wird aus der Zeile herausgelöst und separat angezeigt — er ist nicht Teil des vorgelesenen Textes.

---

## Was ignoriert wird

```
Das hier ist normaler Text ohne ##-Prefix.
Er wird im Editor angezeigt, im Prompter komplett ignoriert.

Auch leere Zeilen werden ignoriert.
```

Solcher Text kann als Regie-Beschreibung oder Kommentar genutzt werden, ohne das er je im Prompter auftaucht.

---

## Vollständiges Beispiel

```markdown
# Begrüßung [NOTE: Publikum anschauen]

##Guten Abend, meine Damen und Herren.
##Herzlich willkommen zu unserem heutigen Event.

---

[SLOW]
##Wir freuen uns, dass Sie **alle** heute hier sind.
[/SLOW]

[PAUSE:3]

# Hauptthema

##Heute sprechen wir über !!das wichtigste Thema!! des Jahres.

[IMG:storage://abc-123|duration=6]

##Nach diesem Bild geht es weiter mit dem nächsten Punkt.

[FAST]
##Kurze schnelle Zusammenfassung der Punkte eins, zwei und drei.
[/FAST]
```

---

## Schnell-Referenz

| Marker | Bedeutung |
|---|---|
| `# Titel` | Sektion (Cyan, Sprungmarke) |
| `##Text` | Sprechtext (Weiß) — kein Leerzeichen nach `##` |
| `**Wort**` | Betont (Blau) |
| `!!Wort!!` | Nicht vergessen (Rot) |
| `---` | Atempause |
| `[PAUSE:N]` | N Sekunden Pause mit Countdown |
| `[SLOW]…[/SLOW]` | Langsamer Block |
| `[FAST]…[/FAST]` | Schneller Block |
| `[IMG:storage://id]` | Bild (Vollbild, Scroll pausiert) |
| `[IMG:storage://id\|duration=N]` | Bild mit eigener Haltezeit in Sekunden |
| `[NOTE: Text]` | Operator-Notiz (nie im Prompter sichtbar) |
