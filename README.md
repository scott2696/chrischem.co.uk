# chrischem.co.uk

UK online casino and betting affiliate site. Static HTML, clean URLs, built from
source fragments by a small Python builder.

## Build

```bash
python3 _build/gen_images.py    # favicons, avatars, operator wordmarks, OG image
python3 _build/gen_reviews.py   # regenerates the 8 operator review fragments
python3 _build/build.py         # renders all pages + sitemap.xml + robots.txt
```

`build.py` is the only thing that writes public files. It reads
`_build/pages/*.html` (JSON front matter in `<!--@ … @-->`), maps the authored
markup onto the template's classes, and writes `{url}index.html` — so every URL
is a directory and no page has a `.html` extension.

## Layout

| Path | What it is |
|---|---|
| `_build/build.py` | Renderer: nav, hero, leaderboard, schema, footer, sitemap, robots |
| `_build/gen_reviews.py` | Per-operator editorial copy → review fragments |
| `_build/gen_images.py` | All generated imagery |
| `_build/operators.json` | Single source of truth for operator facts + affiliate links |
| `_build/pages/*.html` | Authored content fragments, ordered by filename prefix |
| `assets/css/home.css` | The whole stylesheet. Arthouse template classes, instrument aesthetic |
| `logos/`, `images/` | Brand artwork, author avatars, OG image |
| `research/` | Competitor analysis and keyword strategy |

## Editing

- **Change an offer, licence or link:** edit `_build/operators.json`, rebuild.
  Fragments reference operators with `{{aff:slug}}` / `{{affs:slug}}` (sports
  link) and `{{op:slug:Field}}`, so nothing is hard-coded in the copy.
- **Add a page:** drop a fragment in `_build/pages/` with front matter, and add
  it to `NAV` / `FOOTER` in `build.py` if it belongs in the chrome.
- **Add an operator:** add it to `operators.json`, add copy to `COPY` in
  `gen_reviews.py`, add a logo to `logos/` (or let `gen_images.py` make a
  wordmark), then add it to the relevant `itemlist` front matter.

Authored markup is deliberately simple — `<div class="table-scroll">`,
`<div class="callout tip|warn|note|law">`, `<div class="faq"><details>`,
`<div class="toplist"><article class="op-card">` — and `transform()` in
`build.py` maps it onto the template classes (`.datatable`, `.callout`,
`.snippet`, `.afl-row`, `.opcard`, `.cardgrid`, `.toc`).

## Template and design

Markup follows the Arthouse template class system: `.site-header` / `.hero` /
`main > .wrap > .content` / `.afl-list` / `.opcard` / `.datatable` / `.callout` /
`.snippet` / `.toc` / `.cardgrid` / `.faq` / `.rg` / `.site-footer`.

The aesthetic is deliberately not the template's cinema treatment. It is an
**engraved instrument panel**: warm paper ground (`--paper`), deep petrol-green
chrome (`--petrol`), brass (`--brass`) and signal-mint (`--mint`) accents,
Archivo for display and IBM Plex Mono for data readouts. The hero replaces the
template's film-sprocket `.ticks` with a brass measurement `.scale` along its
base, a graph-paper engraving, and `.gauges` stat readouts pulled from the
page's authored `hero-stats`. Prose sits at 840px; leaderboards, tables and card
grids break out to 1060px on desktop.

If you change a `<div>` to another tag in `transform()`, consume its closing
`</div>` in the same regex — `main()` asserts div balance on every page and will
fail the build if you don't.

## Notes

- **Canonicals are self-referencing.** `CANONICAL_TO_HOME` in `build.py` flips
  this to point every page at `/`, but that would tell Google the money pages
  are duplicates and drop them from the index. Left off deliberately.
- **Operators are offshore-licensed** (Curaçao, Anjouan) and not UKGC licensed.
  Every page says so, and the footer carries the GamStop warning and the
  National Gambling Helpline number. Keep that in any new page.
- **Logos must be cropped to their artwork** before use — `object-fit: contain`
  letterboxes a padded square into the 96×48 tile and the brand renders tiny.
