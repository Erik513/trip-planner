# Reiseplaner

Ein einseitiger Reiseplaner als **eine HTML-Datei** (kein Framework, kein Build-Tool außer `build.py`).
Gehostet über GitHub Pages: https://erik513.github.io/trip-planner/
Sprache der Oberfläche und der Code-Kommentare: **Deutsch**.

## Struktur

```
src/app.html      Quelltext (HTML + CSS + JS in einer Datei) – hier wird entwickelt
build.py          baut daraus index.html: Schriften + lz-string eingebettet, läuft offline
vendor/           lz-string.min.js (1.5.0) und woff2-Schriften (Bricolage Grotesque, Figtree, JetBrains Mono)
index.html        Ergebnis für GitHub Pages – NICHT von Hand bearbeiten, immer neu bauen
```

Nach jeder Änderung an `src/app.html`: `python3 build.py`, dann `index.html` committen.

## Kapitel der Seite

1. **Reise-Infos** – Reise & Unterkunft (Reisezielort mit Wetter-Link zu wetter.com, Unterkunft, Zieladresse,
   Check-in/-out, ausklappbare Notizen), **Hinfahrt** und **Rückfahrt** (Datum, optionaler Treffpunkt, Etappen).
   Export/Import als Code (`URLAUB:` + lz-string `compressToEncodedURIComponent` eines kompakten JSON;
   alte Formate `URLAUB-INFO:` / `URLAUB-B:` werden beim Import weiter unterstützt). Haken werden nicht exportiert.
2. **Einkaufsliste** – erscheint nur nach Klick auf „Einkaufen“ (in der To-do-Zeile), weg mit „Einkauf abgeschlossen“.
3. **To-dos**
4. **Packliste** – Tabelle nach Kategorien (Standard: Kleidung, Hygiene & Bad, Gesundheit, Technik,
   Dokumente & Geld, Lebensmittel, Sonstiges), „Vorschläge laden“ füllt typische Gegenstände ohne Anzahl.

## Etappen (Hin-/Rückfahrt)

- Zeile 1 Start, Zeile 2 Ziel (volle Breite), Zeile 3 Fortbewegung · Uhrzeit · Dauer · berechnete Ankunft.
- Dauer als `H:MM` (versteht auch `1,5`, `90m`, `2h 15m`); Ankunft = eigene Uhrzeit bzw. Ankunft der vorigen
  Etappe/Treffpunkt + Dauer.
- Neue Etappe übernimmt Ziel und (auf 5 Min. aufgerundete) Ankunft der vorigen als Start/Uhrzeit.
- Übernehmen-Knöpfe im Feld: Etappe 1 „Treffpunkt“ (+ bei Rückfahrt „Reiseziel“ im Start), ab Etappe 2
  „Vorheriges Ziel“; bei der Hinfahrt „Reiseziel“ im Ziel. Links zu Google Maps / Apple Karten.
- Abhaken pro Box; grün markiert ist die erste offene Box – erst über die ganze Hinfahrt, dann die Rückfahrt.
- „Aus Hinfahrt übernehmen“ legt die Rückfahrt umgekehrt an. Sortieren per Drag an der Nummer (Alt+Pfeile).

## Bedien-Konventionen (bitte beibehalten)

- **Alles speichert automatisch** (`save()`), Zustand liegt in `state`; `render()` zeichnet alles neu.
- Knöpfe, die gerade nichts bewirken, sind **deaktiviert** (`updateButtons()`).
- Destruktive Aktionen: erster Klick „scharf“ (rot), zweiter Klick führt aus; danach Toast mit **Rückgängig**.
- Jede Überschrift ist **ein-/ausklappbar** (`data-col`), eingeklappt sind die Knöpfe daneben ausgeblendet.
- Uhrzeiten: eigenes Feld mit zwei Listen (Std 00–23, Min 00–55 in 5er-Schritten).
- Datumsfelder zeigen „Do, 22.10.2026“ (natives Datumsfeld unsichtbar darüber).
- Einheitliches Design: Farben nur über CSS-Variablen in `:root` (heller + dunkler Modus), Checkboxen eigen gestylt,
  kleine Knöpfe `.ghost.sm`. Muss auf dem Handy (390 px) ohne seitliches Scrollen funktionieren.

## Speicherung

- Standalone/GitHub Pages: `localStorage` (Schlüssel `packliste-v2`) – pro Browser/Gerät.
- Der Code enthält zusätzlich einen Pfad für die Claude-Artifact-Datenbank (`window.claude.use("db")`) und den
  Claude-Download (`use("downloads")`). Außerhalb von Claude ist `window.claude` nicht vorhanden; diese Zweige
  werden dann einfach übersprungen. Nicht entfernen, solange die Claude-Version weiter genutzt wird.
- `migrate(state)` hebt alte Datenstände an – bei Datenmodell-Änderungen dort ergänzen statt alte Daten zu brechen.

## Testen

Kein Test-Framework. Bewährt: Playwright (Python) gegen `index.html` öffnen, Abläufe durchklicken,
Desktop (900 px) und Handy (390 px) sowie Dunkelmodus per Screenshot prüfen, `pageerror` abfangen.
