# tools/

Everything in the case-study layer of this site is generated, so it stays
consistent. Nothing here ships to the browser.

| File | What it does |
| --- | --- |
| `artifacts_lib.py` | Drawing primitives for the case-study artefacts — wireframes, journey maps, swimlanes, charts, device frames. |
| `gen_ux.py` | Renders the 13 artefacts for the three UX/UI case studies into `assets/cs/`. |
| `gen_fe.py` | Renders the 9 artefacts for the three frontend case studies into `assets/cs/`. |
| `gen_og.py` | Renders the 12 Open Graph cards into `assets/og/` (1200 × 630 PNG). |
| `shell.py` | The single page shell: navigation, footer, SEO head, JSON-LD, section helpers. Every case study is built from it, which is why they are identical in structure. |
| `build_ux_pages.py` | Builds `case-study-engage`, `case-study-tobi-bursary`, `case-study-stance`. |
| `build_fe_pages.py` | Builds `case-study-servicewaze`, `case-study-design-system`, `case-study-seo-performance`. |
| `build_hub.py` | Builds the merged Work page (`case-studies.html`) from `showcase-data.json`. |
| `render.js` | SVG → PNG, used only by `gen_og.py`. Needs `npm i @resvg/resvg-js`. |

## Rebuild everything

```bash
python3 tools/gen_ux.py
python3 tools/gen_fe.py
python3 tools/build_ux_pages.py
python3 tools/build_fe_pages.py
python3 tools/build_hub.py
npm i @resvg/resvg-js && python3 tools/gen_og.py   # only when the OG cards change
```

## Why the artefacts are SVG

They are design deliverables, not photographs: wireframes, affinity walls,
service blueprints, token graphs, waterfalls. Drawing them as vector keeps them
sharp at any zoom, keeps the whole set under 400 KB, and means every number on
them is text a screen reader and a search engine can read.
