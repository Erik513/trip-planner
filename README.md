# Trip Planner

Trip info, shopping list, to-dos and packing list in one page – available in English and German (English by default, switch with the "EN | DE" toggle).

**Live:** https://erik513.github.io/trip-planner/

A single-page trip planner built as **one HTML file** (no framework, no build tool except `build.py`), hosted on GitHub Pages.
It works offline, without an account and without a server.

## Sections

1. **Trip info** – trip & accommodation (destination with weather link, accommodation, address, check-in/-out, collapsible notes),
   **outbound trip** and **return trip** (date, optional meeting point, legs). Export/import as a code (see "Sharing").
2. **To-dos & shopping** – one section with two tabs ("To-dos" and "Shopping", each with its done/total counter). The "+" button right of the tabs appends an empty entry
   to the visible list and focuses it (an entry left empty is removed again); "Uncheck all" and "Clear all" in the section header act on the visible list.
   Entries can be reordered by dragging the handle (or Alt + arrow keys), shared code: `makeSortable`. The chosen tab is remembered (`state.tab`).
3. **Packing list** – table grouped by category (default: Clothing, Toiletries, Health, Tech, Documents & money, Food, Misc);
   "Load suggestions" adds typical items without quantities.
   The "+" button in the category row (next to the counter, away from the drag handle) appends an empty item at the bottom of that category and focuses it (an item left empty is removed again).
   The last table row "+ New category" appends an empty category and focuses its name (a category left without name and items is removed again).
   Items can be dragged within and across categories; whole categories can be reordered with the handle at the left of the category row
   (drag, or Alt + arrow keys) – the items move with their category.

### Legs (outbound/return trip)

- Row 1 start, row 2 destination (full width), row 3 transport · time · duration · calculated arrival.
- Duration as `H:MM` (also understands `1,5`, `90m`, `2h 15m`); arrival = own time, or arrival of the previous leg/meeting point + duration.
- A new leg takes the destination and the arrival of the previous one (rounded up to 5 minutes) as start/time.
- "Use" buttons inside the fields: leg 1 "Meeting point" (+ "Destination" in the start field of the return trip), from leg 2 on
  "Previous destination"; on the outbound trip "Destination" in the destination field. Links to Google Maps / Apple Maps.
- Tick off each box; the first open box is highlighted green – across the whole outbound trip first, then the return trip.
- "Copy from outbound" creates the return trip in reverse. Reorder by dragging the number (Alt + arrow keys).

## Sharing

- Header: small buttons to the left of the progress tag – "EN | DE" and share (chain icon). Deliberately small and subtle
  (`.langsw`, `.icon-btn`), not styled like the progress tag.
- **Share button:** shares the page address via `navigator.share`, otherwise copies it to the clipboard. The address always carries
  the chosen language (`#lang=de`) and, if trip info exists, the export code (`#lang=de&TRIP:…`). (Sharing needs the page to be served over http(s); a locally opened file cannot share.)
- **Opening a link:** the language from the link is adopted only if the device has no own language choice yet. If it contains trip info, a notice at the top asks "Apply?" / "Dismiss"; only after confirmation the trip info is
  replaced (with "Undo"), then the hash is removed.
- **Export/import:** code `TRIP:` + lz-string `compressToEncodedURIComponent` of a compact JSON. The earlier German-era formats
  (`URLAUB:`, `URLAUB-INFO:`, `URLAUB-B:`) are still accepted on import. Ticks are not included.
- Only the trip info is shared; shopping list, to-dos and packing list stay local. There is no synchronisation between devices –
  whoever changes something shares again. Backup/export of the other lists and real-time sync are intentionally not provided.

## Install as an app (PWA)

The page is an installable web app: open https://erik513.github.io/trip-planner/ on the phone and choose "Add to Home Screen"
(iPhone: Share → Add to Home Screen; Android/Chrome: menu → Install app). It then starts like a normal app and works offline.
Data stays in the browser storage of that address, so always use the installed app or the live address, not a downloaded
copy of the HTML file (files opened from the file manager have no reliable storage).

- Header: a small "Install" button (with a download icon, next to the share button) opens a dialog with tabs **Android / iPhone & iPad / Computer**
  (the tab of the current device is preselected) and short step-by-step instructions. Where the browser offers installation (`beforeinstallprompt`,
  Chrome/Edge/Android) the Android tab also has a one-tap "Install automatically" button. iPhone/iPad cannot install by button, so there only the steps are shown.
  The header button is hidden once the app runs installed (`display-mode: standalone`).
- `manifest.webmanifest` – name, colours, icons, `display: standalone`.
- `sw.js` – service worker: pages are fetched network-first and revalidated with the server on every start (`cache: "no-cache"`, so updates arrive immediately), the cache is the offline fallback.
  Bump `CACHE` in `sw.js` when the list of cached files changes. It is registered at the end of the script (only on http/https).
- At startup the app asks the browser for persistent storage (`navigator.storage.persist()`) so it does not clear the data on its own.
  iOS Safari removes website data after a long time without use, except for apps added to the Home Screen – the install dialog says so.
- Import accepts the code or the whole shared link (the code is extracted from it).
- `icons/` – app icons (192/512 px, maskable, plus the 180 px apple-touch-icon).
- `build.py` adds the manifest/icon/theme-colour tags to the generated `index.html`.

## Storage

- `localStorage` in the browser (key `trip-planner-v1`, language `trip-planner-lang`) – per browser, device and address.
- `migrate(state)` upgrades old data (including the former German data keys such as `ziel`/`rueck` and the old storage key `packliste-v2`) –
  when changing the data model, extend it there instead of breaking old data.
- The code also contains a path for the Claude Artifact database (`window.claude.use("db")`). Outside Claude, `window.claude`
  does not exist and this branch is skipped. Do not remove it as long as the Claude version is still used.

## Development

```
src/app.html      Source (HTML + CSS + JS in one file) – develop here
build.py          builds index.html from it: fonts + lz-string embedded, works offline
vendor/           lz-string.min.js (1.5.0) and woff2 fonts (Bricolage Grotesque, Figtree, JetBrains Mono)
index.html        Result for GitHub Pages – do NOT edit by hand, always rebuild
manifest.webmanifest, sw.js, icons/    PWA files (edited by hand, served as they are)
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
- Item names (to-dos, shopping, packing items, category names) are auto-growing textareas (`autoGrow`/`growAll`), so long texts wrap instead of being cut off;
  Enter confirms, pasted line breaks become spaces.
- Trip info fields (single-line inputs in `#infoGrid`) whose text is longer than the field scroll back and forth (`refreshMarquee`/`marqueeTick`, driven by `scrollLeft`);
  the effect only runs while the field is not focused and is off with `prefers-reduced-motion`.
- Touch devices (`@media (pointer:coarse)`): the tap targets are bigger (buttons, handles, checkboxes, delete crosses); desktop keeps the compact look.
- Consistent design: colours only via CSS variables in `:root` (light + dark mode), custom checkboxes,
  small buttons `.ghost.sm`. Must work on a phone (390 px) without horizontal scrolling.

### Testing

No test framework. What has worked: open `index.html` with Playwright (Python), click through the flows, check desktop (900 px),
phone (390 px) and dark mode via screenshots, catch `pageerror` – each in both languages.
