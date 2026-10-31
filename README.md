# anagh-sinha.github.io

Personal academic site. Served by GitHub Pages at <https://anagh-sinha.github.io>.

The whole site is one file, `index.html`, with no build step, no dependencies and no
framework. Edit it, commit, and the change is live in about a minute.

## Adding a figure

Every figure is written but hidden, so the page never shows an empty box. Each one
looks like this:

```html
<figure class="pending">
  <div class="slot"><span>Figure slot — hd-ecg-pipeline.png<br>…</span></div>
  <figcaption>Figure 1. Repolarization metric extraction across the high-density lead set.</figcaption>
</figure>
```

To publish it:

1. Commit the image into `images/` using the filename named in the slot
   (`images/hd-ecg-pipeline.png`). Export around 1600 px wide — PNG for plots and
   diagrams, JPEG for photographs.
2. Replace the `<div class="slot">…</div>` line with:
   `<img src="images/hd-ecg-pipeline.png" alt="…">`
3. Delete `class="pending"` from the `<figure>` tag.

Write real alt text. It is what a screen reader announces and what search engines read.

Figures currently waiting on images:

| Filename | Section |
|---|---|
| `hd-ecg-pipeline.png` | Repolarization markers for SCD risk |
| `ecg-annotation.png` | Automated delineation |
| `dry-electrode.png` | Dry nanomaterial electrodes |

Ten figures are already in place, recovered from the previous WordPress site, resized to
1600 px and flattened onto white (several were transparent PNGs whose black text would
otherwise vanish on a dark background).

## Adding a project

Copy an existing `<article class="entry">` block into the right group and fill in the
same parts: a date in `.entry-when`, the title, the lab and supervisor in `.venue`,
then paragraphs. Where something broke, open that paragraph with
`<span class="runin">The obstacle.</span>` — it is the convention the page uses to mark
the part that transfers. End with a `.meta` line listing tools and any links.

## The CV

The CV section links to `cv.pdf` at the repository root. Commit the PDF under exactly
that name and the link works; re-commit over it on each update and the link keeps working.

## Design notes

- Colours are defined once as custom properties in `:root`, with a dark set repeated in
  two blocks (`prefers-color-scheme` and `[data-theme="dark"]`). Change a colour in all
  three places or the themes drift apart.
- One measure (`--measure`) controls text column width everywhere.
- Fonts are Spectral and IBM Plex Sans from Google Fonts. Everything else is inline.
- `.nojekyll` stops GitHub from running Jekyll over the file, which is unnecessary here.
