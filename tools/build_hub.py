#!/usr/bin/env python3
"""Builds the single merged Work page (case-studies.html).

This replaces the old case-studies.html + showcase.html pair, which were
duplicating each other in the top navigation.
"""
import os, sys, json, html
sys.path.insert(0, os.path.dirname(__file__))
from shell import *  # noqa

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = json.load(open(os.path.join(os.path.dirname(__file__), "showcase-data.json"), encoding="utf-8"))
A = "assets/cs/"


def esc(t):
    return html.escape(str(t), quote=True)


# ── The six case studies ──────────────────────────────────────────────────
CASES = [
    dict(tag="design", flag="UX / UI &amp; product", href="case-study-engage.html",
         img=A + "engage-05-ui.svg", alt="Engage shipped interface screens",
         client="Vodacom", role="UX research · IA · UI",
         title="Engage — 25 000 people, one home screen",
         blurb="Everybody had it installed, nobody used it. Research, a rebuilt information architecture, three rounds of flat testing and a shipped interface.",
         kpis=[("48s→19s", "time to task"), ("11→4", "destinations"), ("+34%", "self-service")]),
    dict(tag="design", flag="UX / UI &amp; product", href="case-study-tobi-bursary.html",
         img=A + "tobi-04-form.svg", alt="Bursary form redesign from 42 fields to four steps",
         client="Support + bursary programme", role="Conversation &amp; service design",
         title="A bot that said sorry, and a form nobody finished",
         blurb="3 400 transcripts read by hand, a service blueprint drawn with the people who run it, and a 42-field form rebuilt as four steps that save themselves.",
         kpis=[("41→68%", "contained"), ("38→61%", "completed"), ("40→9min", "to apply")]),
    dict(tag="design", flag="UX / UI &amp; product", href="case-study-stance.html",
         img=A + "stance-02-flow.svg", alt="Stance quote flow and modification picker",
         client="Stance Insurance", role="Product strategy · UX · UI",
         title="Insurance for the cars everyone else refused",
         blurb="South Africa’s modified-car owners were being declined or quietly under-insured. Market research to a live product with a four-minute quote, in ten weeks.",
         kpis=[("27→9", "questions"), ("4 min", "to a price"), ("Live", "in production")]),
    dict(tag="dev", flag="Frontend engineering", href="case-study-servicewaze.html",
         img=A + "sw-01-states.svg", alt="Six ServiceWaze interface states",
         client="ServiceWaze · own product", role="Designer + frontend developer",
         title="Built for one bar of signal",
         blurb="An Angular PWA where the interesting engineering is everything that happens when the network does not answer. Six states designed before the happy path.",
         kpis=[("1.2s", "FCP on 3G"), ("171 KB", "JS shipped"), ("96", "Lighthouse")]),
    dict(tag="dev", flag="Frontend engineering", href="case-study-design-system.html",
         img=A + "ds-01-pipeline.svg", alt="Design token pipeline from Figma to four platforms",
         client="Multi-product platform", role="System lead + frontend",
         title="Figma variables to Angular, zero drift",
         blurb="213 hard-coded colours, four products out of sync and a six-week brand refresh. A token pipeline, 80+ components and six blocking CI checks made the next one take two days.",
         kpis=[("213→0", "hard-coded"), ("91%", "adoption"), ("64→11", "QA comments")]),
    dict(tag="dev", flag="Frontend engineering", href="case-study-seo-performance.html",
         img=A + "perf-01-audit.svg", alt="Lighthouse before and after audit",
         client="This website", role="Designer · developer · analyst",
         title="I audited my own site and did not like it",
         blurb="6.4 seconds to show anything is an argument against hiring me. 5.8 MB became 240 KB — and the page measures itself while you read it.",
         kpis=[("41→99", "Lighthouse"), ("−96%", "page weight"), ("0", "cookies")]),
]


def case_card(c):
    kpis = "".join(f'<div><b>{b}</b><span>{s}</span></div>' for b, s in c["kpis"])
    return f'''        <a class="case-card reveal" data-tags="{c['tag']}" href="./{c['href']}">
          <div class="shot"><img src="./{c['img']}" alt="{c['alt']}" loading="lazy" decoding="async" />
            <span class="flag flag-{c['tag']}">{c['flag']}</span>
          </div>
          <div class="cc-body">
            <div class="cc-meta"><span class="cl">{c['client']}</span><span class="rl">{c['role']}</span></div>
            <h3>{c['title']}</h3>
            <p>{c['blurb']}</p>
            <div class="cc-kpis">{kpis}</div>
            <span class="cc-go">Read the case study</span>
          </div>
        </a>'''


def tile(t, sub, img, href, ext=True, tags=""):
    rel = ' target="_blank" rel="noopener noreferrer"' if ext and href.startswith("http") else ""
    arrow = " &#8599;" if ext and href.startswith("http") else ""
    dt = f' data-tags="{tags}"' if tags else ""
    return f'''          <a class="tile"{dt} href="{href}"{rel}>
            <img src="{img}" alt="{esc(t)}" loading="lazy" decoding="async" />
            <span class="tl"><b>{esc(t)}{arrow}</b><span>{esc(sub)}</span></span>
          </a>'''


def panel(pid, lead_h2, lead_p, count_note, tiles_html, filters=None):
    f = ""
    if filters:
        fid = pid + "Grid"
        btns = "".join(
            f'<button type="button" class="{"on" if i == 0 else ""}" data-filter="{v}">{n}</button>'
            for i, (v, n) in enumerate(filters))
        f = f'<div class="filters" data-filters="{fid}">{btns}</div>'
        tiles_html = f'<div class="tile-grid" id="{fid}">{tiles_html}\n        </div>'
    else:
        tiles_html = f'<div class="tile-grid">{tiles_html}\n        </div>'
    return f'''      <div class="hub-panel" id="panel-{pid}" role="tabpanel">
        <div class="hub-lead">
          <div>
            <h2>{lead_h2}</h2>
            <p>{lead_p}</p>
          </div>
          <p style="font-size:.72rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--dim)">{count_note}</p>
        </div>
        {f}
        {tiles_html}
      </div>'''


ROOT_IMG_FIX = {"./sk.png": "./assets/portfolio/sk-auto.png"}


def build():
    d = DATA
    # ── UI design tiles, grouped by sector ────────────────────────────────
    ui_tiles = "\n".join(
        tile(i["title"], i["sub"], i["img"], i["href"], ext=False,
             tags=(i["uitype"] or "").split(" ")[0])
        for i in d["panel-uidesign"])
    sectors = sorted({(i["uitype"] or "").split(" ")[0] for i in d["panel-uidesign"] if i["uitype"]})
    nice = {"fintech": "Fintech", "insurance": "Insurance", "healthcare": "Healthcare", "retail": "Retail",
            "automotive": "Automotive", "hospitality": "Hospitality", "logistics": "Logistics",
            "education": "Education", "realestate": "Property", "hr": "HR", "manufacturing": "Manufacturing",
            "saas": "SaaS", "government": "Public sector"}
    ui_filters = [("all", "All sectors")] + [(s, nice.get(s, s.title())) for s in sectors]

    live_tiles = "\n".join(
        tile(i["client"] or i["title"], i["title"], ROOT_IMG_FIX.get(i["img"], i["img"]), i["href"]) for i in d["panel-realapps"])
    build_tiles = "\n".join(
        tile(i["client"] or i["title"], i["sub"][:96], i["img"], i["href"]) for i in d["panel-frontend"])
    web_tiles = "\n".join(
        tile(i["title"], i["sub"] or "Web design", i["img"], i["href"]) for i in d["panel-webdesign"])
    hack_tiles = "\n".join(
        tile(i["client"], i["title"], i["img"], i["href"]) for i in d["panel-articles"])

    figma_tiles = "\n".join([
        tile("DesignOps dashboard", "Live page · token pipeline, drift and coverage",
             "./assets/portfolio/design-ops.png", "./design-ops.html", ext=False),
        tile("Meridian design system", "Figma · token graph, components and platform emitters",
             "./assets/portfolio/design-op.png",
             "https://www.figma.com/make/gkTm2bYYnzAmDBwWbWE7kb/Innovative-Design-System-Creation?t=871NF4mO6SlkhYAP-1"),
        tile("Collection of projects", "Figma · product UI and Angular screens, open to review",
             "./assets/portfolio/figma.png",
             "https://www.figma.com/design/SeCP6cuxXX8UyhnOn2wYcJ/Collection-Of-Projects?node-id=8949-77053&p=f"),
        tile("UX resource library", "Notion · the bookmarks and templates I actually use",
             "./assets/portfolio/ux-resources.png",
             "https://chartreuse-scale-c4a.notion.site/Lula-Creatives-UX-Resources-Bookmarks-1e2962b93ef1809dbe07c896db79ad65"),
    ])

    counts = {
        "cases": len(CASES), "ui": len(d["panel-uidesign"]), "live": len(d["panel-realapps"]),
        "builds": len(d["panel-frontend"]), "figma": 4, "web": len(d["panel-webdesign"]),
        "hack": len(d["panel-articles"]),
    }

    tabs = [("cases", "Case studies", counts["cases"]), ("uidesign", "UI design", counts["ui"]),
            ("liveapps", "Live apps", counts["live"]), ("builds", "Frontend builds", counts["builds"]),
            ("figma", "Figma &amp; DesignOps", counts["figma"]), ("webdesign", "Web design", counts["web"]),
            ("hackathons", "Hackathons", counts["hack"])]
    tabs_html = "".join(
        f'\n        <button class="hub-tab" type="button" role="tab" data-panel="{i}">{n}<span class="c">{c}</span></button>'
        for i, n, c in tabs)

    cases_html = "\n".join(case_card(c) for c in CASES)

    body = f'''  <main id="main">
    <header class="cs-top wrap">
      <p class="eyebrow">Work</p>
      <h1>SIX CASE STUDIES.<br /><span class="gold">ONE PERSON, BOTH HALVES.</span></h1>
      <p class="standfirst">Three about research, structure and interface design. Three about the code that makes them
        real. Every one has something to click and a number I measured twice.</p>
      <div class="role-tags">
        <span class="role-tag role-design">&#10022; 3 × UX / UI &amp; product design</span>
        <span class="role-tag role-dev">&#8984; 3 × frontend engineering</span>
        <span class="role-tag role-other">&#10022; Plus 50+ shipped pieces in the showcase tabs</span>
      </div>
    </header>

    <div class="hub-tabs">
      <div class="hub-tabs-inner" role="tablist" aria-label="Work categories">{tabs_html}
      </div>
    </div>

    <section class="cs-section" style="border-top:none;padding-top:34px">
      <div class="hub-panel on" id="panel-cases" role="tabpanel">
        <div class="hub-lead">
          <div>
            <h2>THE SIX, IN FULL</h2>
            <p>Each one is written the same way: what the evidence said, what I decided, what I made, what shipped, and
              what changed afterwards — including the parts that did not work.</p>
          </div>
          <div class="filters" data-filters="caseGrid" style="margin:0">
            <button type="button" class="on" data-filter="all">All six</button>
            <button type="button" data-filter="design">UX / UI &amp; product</button>
            <button type="button" data-filter="dev">Frontend</button>
          </div>
        </div>
        <div class="case-grid" id="caseGrid">
{cases_html}
        </div>

        <div class="how" style="margin-top:40px">
          <div><b>01</b><span>Discover</span>
            <p>Talk to people, read the tickets, watch the analytics. Find the real problem before designing the
              visible one.</p>
          </div>
          <div><b>02</b><span>Frame</span>
            <p>One problem statement, a few principles, and a measure of success agreed before any pixels move.</p>
          </div>
          <div><b>03</b><span>Design &amp; test</span>
            <p>Flows, wireframes and prototypes tested flat, so only ideas that survive get polished.</p>
          </div>
          <div><b>04</b><span>Build &amp; hand over</span>
            <p>UI, tokens, component specs and frontend code. I stay in the sprint and review the pull requests.</p>
          </div>
          <div><b>05</b><span>Measure</span>
            <p>Re-run the benchmark. Publish what improved and what did not, then fix the next thing.</p>
          </div>
        </div>
      </div>

{panel("uidesign", "UI ACROSS EVERY SECTOR",
       "Product interfaces for mobile, web, admin and SaaS — South African and global. Filter by sector; click any tile to open the full-size frame.",
       f"{counts['ui']} interfaces", ui_tiles, ui_filters)}

{panel("liveapps", "SHIPPED AND RUNNING",
       "Small business products designed, built and deployed. Every one of these is a live URL you can open right now.",
       f"{counts['live']} live apps", live_tiles)}

{panel("builds", "FRONTEND BUILDS",
       "Open-source and in-progress products. Angular, PWAs, offline-first patterns — the code is public.",
       f"{counts['builds']} repositories", build_tiles)}

{panel("figma", "FIGMA &amp; DESIGNOPS",
       "The working files and the tooling around them: a live token-pipeline dashboard, the Meridian system, and the resource library I actually use.",
       "4 links", figma_tiles)}

{panel("webdesign", "WEB DESIGN",
       "Client and project websites. Clear structure, brand fit, mobile first.",
       f"{counts['web']} sites", web_tiles)}

{panel("hackathons", "HACKATHONS",
       "48-hour builds, mostly social impact. Rough by definition, and useful for showing how fast an idea can be made concrete.",
       f"{counts['hack']} entries", hack_tiles)}
    </section>

    <section class="cs-section reveal">
      <div class="cta-band">
        <h3 class="display">WANT THIS APPLIED<br /><span class="gold">TO YOUR PRODUCT?</span></h3>
        <p>Tell me the flow that matters most to your business and what it currently costs you. I will come back with
          what I would research first and what I would ship first.</p>
        <div class="cta-actions">
          <a class="btn btn-primary" href="./contact.html">Start a conversation</a>
          <a class="btn btn-outline" href="./services.html">See services &amp; rates</a>
          <a class="btn btn-ghost" href="./about.html">About me</a>
        </div>
      </div>
    </section>
  </main>'''

    ld = [{
        "@type": "CollectionPage", "@id": f"{SITE}/case-studies#page",
        "name": "Work — case studies and showcase",
        "description": "Six end-to-end case studies plus a showcase of shipped interfaces, live apps and frontend builds.",
        "isPartOf": {"@id": f"{SITE}/#website"},
        "about": {"@id": f"{SITE}/#lulamile"},
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/{c['href'].replace('.html', '')}",
                 "name": html.unescape(c["title"])}
                for i, c in enumerate(CASES)],
        },
    }, {
        "@type": "BreadcrumbList", "@id": f"{SITE}/case-studies#breadcrumbs",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Work", "item": f"{SITE}/case-studies"},
        ]}]

    out = shell(
        slug="case-studies",
        title="Work — six case studies in UX/UI design and frontend engineering",
        desc="Three UX/UI and product design case studies, three frontend engineering case studies, and a showcase of 50+ shipped interfaces, live apps and builds by Lulamile Mkhungela.",
        og="assets/og/case-studies.png", body=body, ld_extra=ld)
    open(os.path.join(ROOT, "case-studies.html"), "w", encoding="utf-8").write(out)
    print("wrote case-studies.html", len(out))


if __name__ == "__main__":
    build()
