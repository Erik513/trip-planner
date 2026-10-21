# Trip Planner

Trip info, to-dos, shopping list and packing list in one page – available in English and German (English by default, switch with the "EN | DE" toggle).

**Live:** https://erik513.github.io/trip-planner/

A single-page trip planner built as **one HTML file** (no framework, no build tool except `build.py`), hosted on GitHub Pages.
It works offline, without an account and without a server.

## Sections

1. **Trip info** – trip & accommodation (destination with a weather icon button (appears once the field has been left), accommodation, address with a map-pin menu (also only once the field has been left), check-in/-out, collapsible notes),
   **outbound trip** and **return trip** (date, optional meeting point, legs). Export/import as a code (see "Sharing").
2. **To-dos & shopping** – one section with two tabs ("To-dos" and "Shopping", each with its done/total counter). The "+" button below the list (next to the trash button) appends an empty entry
   to the visible list and focuses it (an entry left empty is removed again); the trash button below the list acts on the visible list only and are named after it ("Clear to-dos" / "Clear shopping", with a matching confirmation).
   Entries can be reordered by dragging the handle (or Alt + arrow keys), shared code: `makeSortable`. The chosen tab is remembered (`state.tab`).
3. **Packing list** – table grouped by category (default: Clothing, Toiletries, Health, Tech, Documents & money, Hand luggage, Food, Misc);
   "Load suggestions" adds typical items without quantities.
   The "+" button in the category row (next to the counter, away from the drag handle) appends an empty item at the bottom of that category and focuses it (an item left empty is removed again).
   The last table row "+ New category" (with the trash button for the whole list next to it) appends an empty category and focuses its name (a category left without name and items is removed again).
   Items can be dragged within and across categories; whole categories can be reordered with the handle at the left of the category row
   (drag, or Alt + arrow keys) – the items move with their category.

### Legs (outbound/return trip)

- Card layout (same on phone and desktop): a header row with the number (drag handle) or the meeting point symbol, the **transport** picker (a compact button; it opens the list of common modes `MODES` plus a free "Other …" field, no browser datalist) or the title "Meeting point",
  the done checkbox and the delete cross; below start and destination (on phones stacked), time and duration, and the **arrival** field (a normal box, the time in the accent colour); a map-pin button right of the duration field (shown once a route is known; the meeting point card has one right of its place field) opens a small menu with Google Maps / Apple Maps links plus the apps that fit the transport mode (Waze for car legs, the DB timetable for train legs; `updateMaps()`) (the transport mode is passed on; for public transport with a trip date and leg time Google gets the departure time through its unofficial URL form); the "+ Stopover" button sits right of the arrival field, which fills the whole width once the leg has a stopover.
  On wide screens "+ Stopover" and "+ Leg" sit in the same row as time and duration (columns 3 and 4), on phones they follow below; the arrival text is always bottom right.
  "+ Meeting point" sits right next to the section title ("Outbound" / "Return"), it disappears once there is a meeting point.
  A ticked card (meeting point, leg, stopover) is locked: all its fields and buttons (including the map pin) are disabled except the checkbox; unticking unlocks it again (`updateCurrent()`).
  The meeting point card has the place with a map-pin button in one row and below it the time plus a "+ Leg" button (inserts a leg after the meeting point). Every leg card has the same button next to "+ Stopover" and inserts the new leg right after itself (start and time are taken over); the stand-alone "+ Leg" under the list only shows while there is neither a meeting point nor a leg; it takes place on the trip date (no separate date field).
- Duration as `H:MM`: only digits and one colon can be typed (`cleanDur`); without a colon the last two digits become the minutes (`230` → `2:30`, handy on numeric keypads). Arrival = the leg's own time + duration; without a time of its own a leg shows no arrival.
- A new leg takes the destination and the arrival of the previous one (rounded up to 5 minutes) as start/time.
- "Use" chips next to the "Start"/"Destination" labels: leg 1 "Meeting point" (+ "Destination" at the start of the return trip), from leg 2 on
  "Previous destination"; on the outbound trip "Destination" at the destination. The chips only show when there is something to copy and the field does not already contain it.
  Next to the "Time" label a chip "← End" takes over the predecessor's end time (the stopover's "until", else the previous leg's arrival rounded up to 5 minutes); on the first leg "← ◉" takes the meeting point's time.
- **Stopover** ("+ Stopover" at the bottom left of a leg card; on the outbound trip hidden when the leg's destination is the trip's destination address; the return trip always shows it): a card between two legs with place (with its own map-pin menu), "from" and "until" time and the computed waiting time.
  It is stored on the leg it follows (`leg.stop = {place, from, until, d}`), so it moves with that leg when legs are reordered. Place and "from" are pre-filled
  (destination and arrival of the leg); the stopover's "until" time fills the next leg's time (and keeps it in sync until that time is set by hand: an empty time, the previous "until", the stopover's "from" or the leg's rounded arrival still count as automatic). "Copy from outbound" keeps the stopover
  place between the reversed legs (times are cleared). In the export code a stopover is stored as elements 6–8 of the leg array (the `TRIP:` format stays compatible).
- Tick off each box; the first open box is highlighted green – across the whole outbound trip first, then the return trip.
- "Copy from outbound" creates the return trip in reverse. Reorder by dragging the number (Alt + arrow keys).

## Sharing

- Header: small buttons of equal height to the left of the progress tag – install, "EN | DE", light/dark (moon/sun) and share (chain icon). Deliberately small and subtle
  (`.langsw`, `.icon-btn`), not styled like the progress tag.
- **Share button:** shares the page address via `navigator.share`, otherwise copies it to the clipboard. The address always carries
  the chosen language (`#lang=de`) and, if trip info exists, the export code (`#lang=de&TRIP:…`). (Sharing needs the page to be served over http(s); a locally opened file cannot share.)
- **Opening a link:** the language from the link is adopted only if the device has no own language choice yet. If it contains trip info, a notice at the top asks "Apply?" / "Dismiss"; only after confirmation the trip info is
  replaced (with "Undo"), then the hash is removed.
- **Export/import:** code `TRIP:` + lz-string `compressToEncodedURIComponent` of a compact JSON. The earlier German-era formats
  (`URLAUB:`, `URLAUB-INFO:`, `URLAUB-B:`) are still accepted on import. Ticks are not included.
- Only the trip info is shared; to-dos, shopping list and packing list stay local. There is no synchronisation between devices –
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

- `localStorage` in the browser (key `trip-planner-v1`, language `trip-planner-lang`, theme `trip-planner-theme`) – per browser, device and address.
- Default categories introduced later (Food, Hand luggage) are added once to existing data by `migrate` (flags `v2cats`, `v3cats`); a deleted one does not come back.
- `migrate(state)` upgrades old data (including the former German data keys such as `ziel`/`rueck` and the old storage key `packliste-v2`) –
- Safety net: `sanitize(state)` repairs a damaged stored state (null entries, wrong types) before `migrate`; `save()` keeps the previous version under `trip-planner-v1-prev`; if the first `render()` still fails, the app rolls back to that version, otherwise a rescue panel shows the raw data and offers a reset. All drag handlers capture the pointer on their container (the moved row and its handle are re-inserted while dragging, which can detach a touch pointer) and only commit a result that still contains exactly the same entries.
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
- Light/dark mode: follows the device until the moon/sun button is used; the choice is stored per browser (`trip-planner-theme`) and only affects this app
  (`data-theme` on `<html>`, applied by a tiny script in the `<head>` of `index.html` to avoid a flash; the CSS tokens live in `:root`).
- `SUGGEST` (default categories + packing suggestions) and `MODES` (transport modes) are bilingual lists `[de, en]`;
  `translateDefaults()` translates default names on language switch, anything typed by the user stays.
- Data format, storage key `trip-planner-v1` and export prefix `TRIP:` are language-independent and must not change.
- Code identifiers (functions, variables, CSS classes, ids, data keys) are English; German appears only in UI texts and in the
  legacy-migration code.

### Interaction conventions (please keep)

- **Everything saves automatically** (`save()`); the state lives in `state`; `render()` redraws everything.
- Buttons that currently do nothing are **hidden**, not disabled (`updateButtons()`, fewer controls on phones); an empty button row (`.sec-btns`) is hidden too.
- Destructive actions: first click "arms" (red), second click performs it; afterwards a toast offers **Undo**.
- Every heading is **collapsible** (`data-col`); collapsed sections hide the buttons next to the heading.
- Times: custom field with two lists (hours 00–23, minutes 00–55 in steps of 5).
- Date fields show "Do, 22.10.2026" / "Thu, 22 Oct 2026" (native date input invisible on top).
- Item names (to-dos, shopping, packing items, category names) are auto-growing textareas (`autoGrow`/`growAll`), so long texts wrap instead of being cut off;
  Enter confirms, pasted line breaks become spaces.
  The trip notes are a multi-line textarea that also grows with its content (`.auto-grow`, no manual resize handle), at least 3 lines high.
- Trip info fields (single-line inputs in `#infoGrid`) whose text is longer than the field scroll back and forth (`refreshMarquee`/`marqueeTick`, driven by `scrollLeft`);
  the effect only runs while the field is not focused and is off with `prefers-reduced-motion`.
- Text fields of the lists use `enterkeyhint="done"`, so the phone keyboard confirms instead of jumping to the next field.
- Layout is grid based: fields that sit side by side must share their top edge. Label rows in a leg card are always as high as a chip (`calc(var(--btn-h) - 10px)`), whether a chip is shown or not; do not add elements that make one cell of a row taller than its neighbours.
- Buttons share one style (CSS block "Buttons: one style everywhere"): outlined = neutral, light accent fill = "add" actions, accent filled = primary (`.tdone`), icon buttons are square, chips (`.unit`) are the compact variant. The height comes from `--btn-h` (34px, 42px on touch, 40px inside leg cards next to the fields). New buttons must use these classes instead of getting their own sizing.
- Buttons are kept short to save space: "clear" buttons show a trash icon (the name is in the tooltip/`aria-label`; while a confirmation is pending they show the question as text, see `refreshClearBtn`),
  "add" buttons start with "+" ("+ Leg", "+ Meeting point", "+ Suggestions"), "copy from outbound" is "⇄ Outbound"; the full text is always the tooltip and `aria-label`.
- Touch devices (`@media (pointer:coarse)`): the tap targets are bigger (buttons, handles, checkboxes, delete crosses); desktop keeps the compact look.
- Consistent design: colours only via CSS variables in `:root` (light + dark mode), custom checkboxes,
  small buttons `.ghost.sm`. Must work on a phone (390 px) without horizontal scrolling.

### Testing

No test framework. What has worked: open `index.html` with Playwright (Python), click through the flows, check desktop (900 px),
phone (390 px) and dark mode via screenshots, catch `pageerror` – each in both languages.
