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
