# lulasync.app

Portfolio of **Lulamile Mkhungela** — UX/UI and product designer, and frontend
developer. Johannesburg, South Africa.

Static site: hand-written HTML, CSS and JavaScript. No framework, no build step
for the pages that ship.

## Structure

```
index.html                     Home
case-studies.html              Work — the single hub for case studies + showcase
case-study-*.html              Six case studies (3 design, 3 frontend)
design-ops.html                Live DesignOps pipeline dashboard
services.html  bundles.html    Offer and pricing
about.html  contact.html       Who and how
showcase.html                  Redirect → /case-studies (kept for old links)
assets/case-study.css          The shared design system for every case study
assets/case-study.js           The shared interaction layer
assets/cs/                     Case-study artefacts (SVG)
assets/og/                     Open Graph cards
tools/                         Generators — see tools/README.md
```

## The six case studies

**UX/UI and product design**

1. `case-study-engage` — Engage: 25 000 people, one home screen
2. `case-study-tobi-bursary` — A bot that said sorry, and a form nobody finished
3. `case-study-stance` — Insurance for the cars everyone else refused

**Frontend engineering**

4. `case-study-servicewaze` — Built for one bar of signal (offline-first PWA)
5. `case-study-design-system` — Figma variables to Angular, zero drift
6. `case-study-seo-performance` — Rebuilding this site

## Local preview

```bash
python3 -m http.server 3000
```

## Deploy

Vercel. `vercel.json` holds clean URLs, redirects (including `/designops` and
`/design-ops` → the dashboard) and cache headers.
