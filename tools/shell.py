#!/usr/bin/env python3
"""Builds every case-study page from one shell so navigation, SEO,
footer, spacing and typography are identical across the site."""
import os, json, datetime

ROOT = os.path.join(os.path.dirname(__file__), "..")
SITE = "https://lulasync.app"
TODAY = "2026-08-19"

NAV = [("Home", "index.html"), ("Work", "case-studies.html"),
       ("Services", "services.html"), ("About", "about.html"), ("Contact", "contact.html")]


def nav_html(active):
    links = "".join(
        f'\n      <a href="./{h}" class="nav-link{" active" if h == active else ""}">{n}</a>'
        for n, h in NAV)
    mob = "".join(
        f'\n      <a href="./{h}" class="mobile-nav-link{" active" if h == active else ""}">{n}</a>'
        for n, h in NAV)
    return f'''  <nav class="ls-nav">
    <a href="./index.html" class="nav-logo"><img src="./assets/portfolio/icon-192.png" alt="" width="34" height="34" />
      <span>Lula<span class="gold">Sync</span></span></a>
    <div class="nav-links">{links}
    </div>
    <div class="nav-actions">
      <button class="theme-toggle" type="button" aria-label="Switch theme">&#127769;</button>
      <button class="hamburger" id="menuBtn" type="button" aria-label="Open menu"><span></span><span></span><span></span></button>
    </div>
  </nav>
  <div class="grad-line"></div>
  <div class="mobile-overlay" id="mobileOverlay">
    <button class="close-btn" id="closeBtn" type="button" aria-label="Close menu">&#10005;</button>
    <div>{mob}
    </div>
  </div>'''


FOOTER = '''  <footer class="ls-footer">
    <div class="footer-grid">
      <div>
        <a href="./index.html" class="nav-logo"><img src="./assets/portfolio/icon-192.png" alt="" width="34" height="34" />
          <span>Lula<span class="gold">Sync</span></span></a>
        <p class="footer-desc">Lulamile Mkhungela — UX/UI and product design, plus the frontend to make it real.
          Johannesburg, South Africa.</p>
      </div>
      <div>
        <p class="footer-col-title">Design case studies</p>
        <div class="footer-links">
          <a class="footer-link" href="./case-study-engage.html">Engage — enterprise app</a>
          <a class="footer-link" href="./case-study-tobi-bursary.html">TOBi &amp; the bursary journey</a>
          <a class="footer-link" href="./case-study-stance.html">Stance — insuring modified cars</a>
        </div>
      </div>
      <div>
        <p class="footer-col-title">Frontend case studies</p>
        <div class="footer-links">
          <a class="footer-link" href="./case-study-servicewaze.html">ServiceWaze — offline-first PWA</a>
          <a class="footer-link" href="./case-study-design-system.html">Meridian — Figma to Angular</a>
          <a class="footer-link" href="./case-study-seo-performance.html">Rebuilding this site</a>
        </div>
      </div>
      <div>
        <p class="footer-col-title">Explore</p>
        <div class="footer-links">
          <a class="footer-link" href="./case-studies.html">All work</a>
          <a class="footer-link" href="./design-ops.html">DesignOps dashboard</a>
          <a class="footer-link" href="./services.html">Services</a>
          <a class="footer-link" href="./about.html">About</a>
          <a class="footer-link" href="./contact.html">Contact</a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <p class="footer-copy">Measured without cookies —
        <a href="./case-study-seo-performance.html" style="color:var(--gold);text-decoration:none">see how</a>
      </p>
      <p class="footer-copy">&copy; 2017–<span data-year>2026</span> LulaSync · Built by Lulamile in South Africa</p>
      <p class="footer-copy">Designing and building useful products for real people.</p>
    </div>
  </footer>'''


def person_ld():
    return {
        "@type": "Person",
        "@id": f"{SITE}/#lulamile",
        "name": "Lulamile Mkhungela",
        "jobTitle": ["UX/UI Designer", "Product Designer", "Frontend Developer"],
        "url": f"{SITE}/",
        "email": "mailto:mkhungela.lulamile1@gmail.com",
        "telephone": "+27837195064",
        "address": {"@type": "PostalAddress", "addressLocality": "Johannesburg",
                    "addressRegion": "Gauteng", "addressCountry": "ZA"},
        "sameAs": ["https://www.linkedin.com/in/lulamile-mkhungela/",
                   "https://github.com/LulamileMkhungela"],
    }


def shell(*, slug, title, desc, og, body, active="case-studies.html", ld_extra=None, page_class=""):
    graph = [person_ld(), {
        "@type": "WebSite", "@id": f"{SITE}/#website", "name": "LulaSync — Lulamile Mkhungela",
        "url": f"{SITE}/", "inLanguage": "en-ZA", "publisher": {"@id": f"{SITE}/#lulamile"}}]
    if ld_extra:
        graph += ld_extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="en-ZA" data-theme="dark">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#0A0705" />
  <link rel="icon" href="./assets/portfolio/icon-192.png" type="image/png" />
  <link rel="manifest" href="./manifest.json" />
  <script>(function () {{ try {{ var t = localStorage.getItem('ls-theme') || 'dark'; document.documentElement.setAttribute('data-theme', t); document.documentElement.style.colorScheme = t; }} catch (e) {{ }} }})();</script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="./assets/case-study.css" />

  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="author" content="Lulamile Mkhungela" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
  <link rel="canonical" href="{SITE}/{slug}" />

  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="LulaSync — Lulamile Mkhungela" />
  <meta property="og:locale" content="en_ZA" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{SITE}/{slug}" />
  <meta property="og:image" content="{SITE}/{og}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{title}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{SITE}/{og}" />

  <script type="application/ld+json">
{ld}
  </script>
</head>

<body{f' class="{page_class}"' if page_class else ''}>
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="read-bar" aria-hidden="true"></div>

{nav_html(active)}

{body}

{FOOTER}

  <script src="./assets/case-study.js" defer></script>
  <script src="./assets/analytics.js" defer></script>
</body>

</html>
'''


# ══════════════════════════════════════════════════════════════════════════
#  Case-study helpers
# ══════════════════════════════════════════════════════════════════════════
def hero(*, disc, disc_label, h1, standfirst, meta, kpis):
    metas = "".join(f'\n        <div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in meta)
    kpi = "".join(f'\n        <div class="hero-kpi"><b>{b}</b><span>{s}</span></div>' for b, s in kpis)
    return f'''    <header class="cs-top wrap">
      <p class="disc disc-{disc}">{disc_label}</p>
      <h1>{h1}</h1>
      <p class="standfirst">{standfirst}</p>
      <dl class="meta-list">{metas}
      </dl>
      <div class="hero-kpis">{kpi}
      </div>
    </header>'''


def chapters(items):
    ls = "".join(f'\n      <a class="chapter-link" href="#{i}">{n}</a>' for i, n in items)
    return f'''    <nav class="chapters" aria-label="Sections of this case study">
      <div class="chapters-inner">{ls}
      </div>
    </nav>'''


def fig(src, alt, tag, cap, zoom=True):
    z = ' zoomable' if zoom else ''
    hint = '<span class="zoom-hint">click to enlarge</span>' if zoom else ''
    return f'''<figure class="art-fig">
          <img class="{z.strip()}" src="./{src}" alt="{alt}" loading="lazy" decoding="async" />
          <figcaption><b>{tag}</b><span>{cap}</span>{hint}</figcaption>
        </figure>'''


def section(num, sid, title, sub, inner, tint=False):
    return f'''    <section class="cs-section reveal{' tint' if tint else ''}" id="{sid}">
      <div class="sec-head"><span class="n">{num}</span>
        <h2>{title}</h2>
      </div>
      <p class="sec-sub">{sub}</p>
      {inner}
    </section>'''


def rail(steps):
    """steps: list of (num, title, desc, pane_html)"""
    btns = "".join(
        f'''\n        <button class="rail-step" type="button" role="tab" data-step="s{i}">
          <span class="num">{n}</span><span><span class="t">{t}</span><span class="d">{d}</span></span>
        </button>''' for i, (n, t, d, _) in enumerate(steps))
    panes = "".join(f'\n        <div class="rail-pane" data-step="s{i}">{p}</div>'
                    for i, (_, _, _, p) in enumerate(steps))
    return f'''<div class="rail" data-rail>
        <div class="rail-steps" role="tablist" aria-label="Process steps">{btns}
        </div>
        <div>{panes}
        </div>
      </div>'''


def facts(items):
    return '<div class="facts">' + "".join(
        f'<div><b>{b}</b><span>{s}</span></div>' for b, s in items) + '</div>'


def notes(items):
    """items: list of (kind, heading, paragraphs)"""
    out = '<div class="duo">'
    for kind, h, ps in items:
        body = "".join(f'<p>{p}</p>' for p in ps)
        out += f'<div class="note {kind}"><h4>{h}</h4>{body}</div>'
    return out + '</div>'


def honest(heading, items):
    lis = "".join(f'<li>{i}</li>' for i in items)
    return f'<div class="honest"><h4>{heading}</h4><ul>{lis}</ul></div>'


def nextprev(prev, nxt):
    cards = ""
    if prev:
        cards += f'<a class="next-card" href="./{prev[0]}"><span>Previous</span><b>{prev[1]}</b></a>'
    if nxt:
        cards += f'<a class="next-card" href="./{nxt[0]}"><span>Next case study</span><b>{nxt[1]}</b></a>'
    cards += '<a class="next-card" href="./case-studies.html"><span>Index</span><b>All six case studies &amp; the showcase</b></a>'
    return f'''    <section class="cs-section reveal" id="more">
      <div class="cta-band">
        <h3 class="display">WANT THIS<br /><span class="gold">ON YOUR PRODUCT?</span></h3>
        <p>Tell me the one flow that matters most to your business and what it currently costs you. I will come back
          with what I would research first and what I would ship first.</p>
        <div class="cta-actions">
          <a class="btn btn-primary" href="./contact.html">Start a conversation</a>
          <a class="btn btn-outline" href="./case-studies.html">See all work</a>
        </div>
      </div>
      <div class="cs-nav-next">{cards}</div>
    </section>'''
