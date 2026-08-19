#!/usr/bin/env python3
"""Generates the 1200x630 Open Graph cards, in the site's own visual language."""
import os, sys, subprocess, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from artifacts_lib import esc, FONT

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "assets", "og")
os.makedirs(OUT, exist_ok=True)

INK = "#0A0705"
CARD = "#100E0C"
BORDER = "#241F19"
PAPER = "#F5EDD8"
DIM = "#8D8578"
GOLD = "#F0A500"
FIRE = "#E04E14"
PURPLE = "#8B5CF6"
CYAN = "#00C2FF"

CARDS = [
    ("home", "Lulamile Mkhungela", "DESIGN THAT SURVIVES", "CONTACT WITH CODE.",
     "UX/UI and product design · frontend engineering · Johannesburg", GOLD,
     [("6", "case studies"), ("50+", "shipped pieces"), ("2", "disciplines, one person")]),
    ("case-studies", "Work", "THREE ABOUT DESIGN.", "THREE ABOUT CODE.",
     "Six end-to-end case studies, plus 50+ shipped interfaces", GOLD,
     [("3", "UX / UI &amp; product"), ("3", "frontend engineering"), ("100%", "measured twice")]),
    ("engage", "UX, UI and product design", "25 000 PEOPLE.", "ONE HOME SCREEN.",
     "Vodacom Engage — research, IA, prototype, shipped interface", PURPLE,
     [("48s → 19s", "time to task"), ("11 → 4", "destinations"), ("+34%", "self-service")]),
    ("tobi", "Conversation and service design", "A BOT THAT SAID SORRY,", "A FORM NOBODY FINISHED.",
     "3 400 transcripts, a service blueprint and a 42-field form rebuilt", PURPLE,
     [("41 → 68%", "contained"), ("38 → 61%", "completed"), ("40 → 9 min", "to apply")]),
    ("stance", "Product strategy and UX", "INSURANCE FOR THE CARS", "EVERYONE ELSE REFUSED.",
     "Stance — market research to a live product in ten weeks", PURPLE,
     [("27 → 9", "questions"), ("4 min", "to a price"), ("Live", "in production")]),
    ("servicewaze", "Frontend engineering", "BUILT FOR", "ONE BAR OF SIGNAL.",
     "ServiceWaze — an offline-first Angular PWA", CYAN,
     [("1.2s", "FCP on 3G"), ("171 KB", "JS shipped"), ("96", "Lighthouse")]),
    ("design-system", "Design systems and DesignOps", "FIGMA VARIABLES TO", "ANGULAR, ZERO DRIFT.",
     "Meridian — token pipeline, 80+ components, six blocking CI checks", CYAN,
     [("213 → 0", "hard-coded"), ("91%", "adoption"), ("64 → 11", "QA comments")]),
    ("seo-performance", "Frontend and technical SEO", "I AUDITED MY OWN SITE", "AND DID NOT LIKE IT.",
     "5.8 MB → 240 KB, and the page measures itself while you read", CYAN,
     [("41 → 99", "Lighthouse"), ("−96%", "page weight"), ("0", "cookies")]),
    ("design-ops", "Live artefact", "THE PIPELINE,", "RUNNING.",
     "DesignOps dashboard — tokens, drift, coverage and platform emitters", CYAN,
     [("4", "platform outputs"), ("6", "blocking checks"), ("0", "hand-typed hex")]),
    ("services", "Services", "ONE PERSON,", "BOTH HALVES OF THE JOB.",
     "Research, interface design and the frontend that ships it", GOLD,
     [("UX", "research and IA"), ("UI", "design systems"), ("Code", "Angular · PWA")]),
    ("about", "About", "I DESIGN IT,", "THEN I BUILD IT.",
     "Lulamile Mkhungela — Johannesburg, South Africa", GOLD,
     [("9 yrs", "designing"), ("6 yrs", "shipping frontend"), ("1", "very long CV")]),
    ("contact", "Contact", "TELL ME THE FLOW", "THAT MATTERS MOST.",
     "I reply within about 30 minutes during South African hours", GOLD,
     [("~30 min", "reply time"), ("Free", "first review"), ("ZA", "based, remote-friendly")]),
]


def card(slug, eyebrow, l1, l2, sub, accent, kpis):
    W, H = 1200, 630
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">'
    s += f'<rect width="{W}" height="{H}" fill="{INK}"/>'
    # accent glow
    s += (f'<defs><radialGradient id="g" cx="15%" cy="0%" r="90%">'
          f'<stop offset="0%" stop-color="{accent}" stop-opacity=".22"/>'
          f'<stop offset="60%" stop-color="{accent}" stop-opacity="0"/></radialGradient>'
          f'<linearGradient id="ln" x1="0" y1="0" x2="1" y2="0">'
          f'<stop offset="0%" stop-color="{FIRE}"/><stop offset="50%" stop-color="{GOLD}"/>'
          f'<stop offset="100%" stop-color="{FIRE}"/></linearGradient></defs>')
    s += f'<rect width="{W}" height="{H}" fill="url(#g)"/>'
    s += f'<rect x="0" y="0" width="{W}" height="6" fill="url(#ln)"/>'
    # logo
    s += f'<rect x="72" y="62" width="42" height="42" rx="11" fill="{accent}"/>'
    s += f'<text x="93" y="92" font-size="22" font-weight="900" fill="{INK}" text-anchor="middle">L</text>'
    s += f'<text x="128" y="92" font-size="24" font-weight="800" fill="{PAPER}" letter-spacing="1">LulaSync</text>'
    # eyebrow
    s += f'<rect x="72" y="150" width="30" height="3" fill="{accent}"/>'
    s += f'<text x="112" y="156" font-size="15" font-weight="800" fill="{accent}" letter-spacing="2.4">{eyebrow.upper()}</text>'
    # headline
    s += f'<text x="72" y="252" font-size="62" font-weight="800" fill="{PAPER}" letter-spacing="-.5">{l1}</text>'
    s += f'<text x="72" y="322" font-size="62" font-weight="800" fill="{accent}" letter-spacing="-.5">{l2}</text>'
    # sub
    s += f'<text x="72" y="378" font-size="21" font-weight="500" fill="{DIM}">{sub}</text>'
    # kpi row
    for i, (b, l) in enumerate(kpis):
        x = 72 + i * 356
        s += f'<rect x="{x}" y="428" width="332" height="112" rx="16" fill="{CARD}" stroke="{BORDER}" stroke-width="2"/>'
        s += f'<text x="{x+26}" y="490" font-size="40" font-weight="800" fill="{accent}">{b}</text>'
        s += f'<text x="{x+26}" y="518" font-size="17" font-weight="600" fill="{DIM}">{l}</text>'
    s += f'<text x="72" y="592" font-size="17" font-weight="600" fill="{DIM}">lulasync.app</text>'
    s += f'<text x="{W-72}" y="592" font-size="17" font-weight="600" fill="{DIM}" text-anchor="end">Lulamile Mkhungela · Johannesburg, South Africa</text>'
    return s + "</svg>"


if __name__ == "__main__":
    for slug, eyebrow, l1, l2, sub, accent, kpis in CARDS:
        svg = card(slug, eyebrow, l1, l2, sub, accent, kpis)
        tmp = os.path.join(tempfile.gettempdir(), slug + ".svg")
        open(tmp, "w", encoding="utf-8").write(svg)
        png = os.path.join(OUT, slug + ".png")
        subprocess.run(["node", os.path.join(os.path.dirname(__file__), "render.js"), tmp, png, "1200"],
                       check=True, capture_output=True)
        print("og:", slug, os.path.getsize(png) // 1024, "KB")
