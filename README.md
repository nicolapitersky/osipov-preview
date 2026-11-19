# osipov.uk preview

Public review preview of proposed new osipov.uk versions, hosted on GitHub Pages.
The live site at https://osipov.uk is unchanged; its source lives in a separate
private repository. Nothing here deploys to production.

## Architecture

One shared template generates every version:

- `template.html` + `hub-template.html` — shared page skeletons
- `content/<version>.html` — per-version body sections
- `writing.json` — the writing/interviews feed (verified public records only:
  canonical URLs, exact displayed titles and dates; no slug inference)
- `styles.css` — shared styles
- `build.py` — regenerates `index.html` and `<version>/index.html`

Run `python3 build.py` after editing any input, then commit the outputs.

Add a variant: one entry in `VERSIONS` in `build.py` plus one
`content/<name>.html` fragment, rebuild, commit. The hub lists it automatically.

Update writing: edit `writing.json`, rebuild, commit.

## Weekly writing reconciliation

Weekly check of Igor's public LinkedIn against the feed:

1. Open each canonical URL in `writing.json` and confirm the exact displayed
   title and publication date still match.
2. Check Igor's public LinkedIn activity for newly published articles or
   posts not yet listed.
3. Add new items with their canonical linkedin.com URL, exact title and date
   from the published page (never inferred from the slug), plus a verbatim
   line as the blurb. Update `last_reconciled`.
4. Run `python3 build.py`, commit all changed outputs.

Public records only: no drafts, editor URLs or private material.
