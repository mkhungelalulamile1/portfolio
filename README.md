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

## Independent product case studies

The Work hub contains three original, clearly-labelled product concepts. They are not client claims: prototype targets and assumptions are visibly distinguished from measured outcomes.

1. `case-study-engage` — Mali, a B2C fintech concept
2. `case-study-stance` — LedgerLane, a B2B fintech concept
3. `case-study-tobi-bursary` — Loop, a SaaS approval-workflow concept

## Local preview

```bash
python3 -m http.server 3000
```

## Deploy

Vercel. `vercel.json` holds clean URLs, redirects (including `/designops` and
`/design-ops` → the dashboard) and cache headers.
