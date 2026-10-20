# Trip Planner

Trip info, shopping list, to-dos and packing list in one page – available in English and German (English by default, switch with the "EN | DE" toggle).

**Live:** https://erik513.github.io/trip-planner/

A single-page trip planner built as **one HTML file** (no framework, no build tool except `build.py`), hosted on GitHub Pages.
It works offline, without an account and without a server.

## Sections

1. **Trip info** – trip & accommodation (destination with weather link, accommodation, address, check-in/-out, collapsible notes),
   **outbound trip** and **return trip** (date, optional meeting point, legs). Export/import as a code (see "Sharing").
2. **Shopping list** – only appears after clicking "Shopping" (in the to-do row), disappears with "Shopping done".
3. **To-dos**
4. **Packing list** – table grouped by category (default: Clothing, Toiletries, Health, Tech, Documents & money, Food, Misc);
   "Load suggestions" adds typical items without quantities.

### Legs (outbound/return trip)

- Row 1 start, row 2 destination (full width), row 3 transport · time · duration · calculated arrival.
- Duration as `H:MM` (also understands `1,5`, `90m`, `2h 15m`); arrival = own time, or arrival of the previous leg/meeting point + duration.
- A new leg takes the destination and the arrival of the previous one (rounded up to 5 minutes) as start/time.
- "Use" buttons inside the fields: leg 1 "Meeting point" (+ "Destination" in the start field of the return trip), from leg 2 on
  "Previous destination"; on the outbound trip "Destination" in the destination field. Links to Google Maps / Apple Maps.
- Tick off each box; the first open box is highlighted green – across the whole outbound trip first, then the return trip.
- "Copy from outbound" creates the return trip in reverse. Reorder by dragging the number (Alt + arrow keys).

## Sharing

- Header: small buttons to the left of the progress tag – "EN | DE", share (chain icon), download. Deliberately small and subtle
  (`.langsw`, `.icon-btn`), not styled like the progress tag.
- **Share button:** shares the page address via `navigator.share`, otherwise copies it to the clipboard. The address always carries
  the chosen language (`#lang=de`) and, if trip info exists, the export code (`#lang=de&TRIP:…`). When opened locally (`file://`), the HTML file is shared if the device supports it.
- **Opening a link:** the language from the link is adopted only if the device has no own language choice yet. If it contains trip info, a notice at the top asks "Apply?" / "Dismiss"; only after confirmation the trip info is
  replaced (with "Undo"), then the hash is removed.
- **Download button:** saves the page as `Trip-Planner.html`. The current trip info (or a received link's trip info that has not been applied yet) is
  embedded in the file (`window.EMBEDDED_HASH`); when the file is opened, it asks "Apply?" once, just like a received link
  (remembered in `localStorage` key `trip-planner-seen`). Shopping list, to-dos and packing list are not included.
- **Export/import:** code `TRIP:` + lz-string `compressToEncodedURIComponent` of a compact JSON. The earlier German-era formats
  (`URLAUB:`, `URLAUB-INFO:`, `URLAUB-B:`) are still accepted on import. Ticks are not included.
- Only the trip info is shared; shopping list, to-dos and packing list stay local. There is no synchronisation between devices –
  whoever changes something shares again. Backup/export of the other lists and real-time sync are intentionally not provided.

## Storage

- `localStorage` in the browser (key `trip-planner-v1`, language `trip-planner-lang`) – per browser, device and address.
- `migrate(state)` upgrades old data (including the former German data keys such as `ziel`/`rueck` and the old storage key `packliste-v2`) –
  when changing the data model, extend it there instead of breaking old data.
- The code also contains a path for the Claude Artifact database (`window.claude.use("db")`) and Claude downloads
  (`use("downloads")`). Outside Claude, `window.claude` does not exist and these branches are skipped.
  Do not remove them as long as the Claude version is still used.

## Development

```
src/app.html      Source (HTML + CSS + JS in one file) – develop here
build.py          builds index.html from it: fonts + lz-string embedded, works offline
vendor/           lz-string.min.js (1.5.0) and woff2 fonts (Bricolage Grotesque, Figtree, JetBrains Mono)
index.html        Result for GitHub Pages – do NOT edit by hand, always rebuild
```

After every change to `src/app.html`: run `python3 build.py`, then commit `index.html` along with it.
Code comments are written in English.

### Languages (i18n)

- All texts live in `I18N` (`de`/`en`) at the top of the script in `src/app.html`; use `T("key", {placeholders})`.
  **Always add new texts in both languages** – never hard-code text in HTML/JS.
- Static HTML texts: `data-i18n="key"` (text content) or `data-i18n-attr="aria-label:key;title:key"`;
  `applyStatic()` applies them (runs on every `render()`).
- Chosen language: `localStorage` `trip-planner-lang`; default = English.
- `SUGGEST` (default categories + packing suggestions) and `MODES` (transport modes) are bilingual lists `[de, en]`;
  `translateDefaults()` translates default names on language switch, anything typed by the user stays.
- Data format, storage key `trip-planner-v1` and export prefix `TRIP:` are language-independent and must not change.
- Code identifiers (functions, variables, CSS classes, ids, data keys) are English; German appears only in UI texts and in the
  legacy-migration code.

### Interaction conventions (please keep)

- **Everything saves automatically** (`save()`); the state lives in `state`; `render()` redraws everything.
- Buttons that currently do nothing are **disabled** (`updateButtons()`).
- Destructive actions: first click "arms" (red), second click performs it; afterwards a toast offers **Undo**.
- Every heading is **collapsible** (`data-col`); collapsed sections hide the buttons next to the heading.
- Times: custom field with two lists (hours 00–23, minutes 00–55 in steps of 5).
- Date fields show "Do, 22.10.2026" / "Thu, 22 Oct 2026" (native date input invisible on top).
- Consistent design: colours only via CSS variables in `:root` (light + dark mode), custom checkboxes,
  small buttons `.ghost.sm`. Must work on a phone (390 px) without horizontal scrolling.

### Testing

No test framework. What has worked: open `index.html` with Playwright (Python), click through the flows, check desktop (900 px),
phone (390 px) and dark mode via screenshots, catch `pageerror` – each in both languages.
