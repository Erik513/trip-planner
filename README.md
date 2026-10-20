# Reiseplaner / Trip Planner

Reise-Infos, Einkaufsliste, To-dos und Packliste in einer Seite – auf Deutsch und Englisch (Umschalter „DE | EN“).
Trip info, shopping list, to-dos and packing list in one page – in German and English.

**Online:** https://erik513.github.io/trip-planner/

## Funktionen

- **Reise-Infos:** Reise & Unterkunft, Hin- und Rückfahrt mit Treffpunkt und Etappen (Ankunftszeit wird berechnet), Links zu Google Maps / Apple Karten.
- **Einkaufsliste, To-dos, Packliste** mit Kategorien, Drag & Drop, Vorschlägen und „Rückgängig“.
- **Teilen:** Der Link-Knopf teilt die Seite samt Reise-Infos (als Code hinter dem `#`); beim Öffnen wird nachgefragt, ob sie übernommen werden sollen. Alternativ „Exportieren“/„Importieren“ mit Code.
- **Speicherung:** automatisch im Browser (`localStorage`), pro Gerät; kein Konto, kein Server, läuft offline. Einkaufsliste, To-dos und Packliste werden nicht geteilt.
- Heller und dunkler Modus, für Handy (ab 375 px) und Desktop.

## Entwickeln

Quelltext ist `src/app.html`; danach `python3 build.py` ausführen (baut `index.html` mit eingebetteten Schriften) und `index.html` mitcommitten.
Details und Konventionen stehen in [CLAUDE.md](CLAUDE.md).
