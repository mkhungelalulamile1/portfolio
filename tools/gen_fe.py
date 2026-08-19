#!/usr/bin/env python3
"""Artefacts for the three frontend engineering case studies."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from artifacts_lib import *  # noqa

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "cs")
os.makedirs(OUT, exist_ok=True)
P = lambda n: os.path.join(OUT, n)

DARK = "#0E0E10"
DARK_2 = "#17171A"
DARK_3 = "#212126"
DTEXT = "#F0EDE6"
DMUTE = "#94908A"


# ══════════════════════════════════════════════════════════════════════════
# SERVICEWAZE 01 — six states
# ══════════════════════════════════════════════════════════════════════════
def sw_states():
    W, H = 1200, 700
    s = text(48, 52, "Six states, designed before the happy path", 23, TEXT, 800)
    s += text(48, 76, "A status app is mostly not-loaded. I drew the awkward states first, then the one everybody screenshots.", 12, MUTE, 600)

    def shell(x, y, w, h, title_txt, badge=None, badge_c=GOLD):
        g = rect(x, y, w, h, 14, DARK, "#26262B", 1.4)
        g += f'<rect x="{x}" y="{y}" width="{w}" height="38" rx="14" fill="{DARK_2}"/>'
        g += f'<rect x="{x}" y="{y+24}" width="{w}" height="14" fill="{DARK_2}"/>'
        g += text(x + 14, y + 24, title_txt, 10.5, DTEXT, 800)
        if badge:
            c, cw = chip(x + w - 14 - (len(badge) * 5.6 + 16), y + 9, badge, "none", badge_c, badge_c, 8.5, 8, 18)
            g += c
        return g

    cards = [
        ("Fresh", "live", GOOD),
        ("Stale", "4 min old", GOLD),
        ("Offline", "no network", FIRE),
        ("Loading", "skeleton", DMUTE),
        ("Partial", "3 of 5 sources", GOLD),
        ("Empty", "no suburb yet", DMUTE),
    ]
    rows = [
        ("Electricity", "Stage 2 from 18:00", GOLD),
        ("Water", "No interruptions", GOOD),
        ("Air quality", "Moderate · 62 AQI", GOLD),
        ("Transport", "Gautrain on time", GOOD),
    ]
    for i, (name, badge, bc) in enumerate(cards):
        cx = 48 + (i % 3) * 372
        cy = 116 + (i // 3) * 254
        s += shell(cx, cy, 348, 226, "Midrand, Gauteng", badge, bc)
        if name == "Loading":
            for k in range(4):
                s += rect(cx + 14, cy + 52 + k * 40, 320, 30, 8, DARK_2, "none", 0)
                s += rect(cx + 26, cy + 62 + k * 40, 120 - k * 14, 8, 4, DARK_3, "none", 0)
        elif name == "Empty":
            s += f'<circle cx="{cx+174}" cy="{cy+104}" r="24" fill="none" stroke="#33333A" stroke-width="2.4"/>'
            s += f'<path d="M{cx+166} {cy+104} l6 6 l12 -14" stroke="#33333A" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
            s += text(cx + 174, cy + 148, "Pick a suburb to start", 10.5, DMUTE, 700, "middle")
            s += rect(cx + 104, cy + 162, 140, 30, 8, GOLD, "none", 0)
            s += text(cx + 174, cy + 182, "Use my location", 9.6, "#17140F", 800, "middle")
        else:
            n = 2 if name == "Partial" else 4
            for k in range(4):
                ry = cy + 52 + k * 40
                on = k < n
                s += rect(cx + 14, ry, 320, 32, 8, DARK_2, "#26262B", 1)
                col = rows[k][2] if on else "#3A3A40"
                if name == "Offline":
                    col = "#4A4A52" if k else GOLD
                s += f'<circle cx="{cx+32}" cy="{ry+16}" r="5.5" fill="{col}"/>'
                s += text(cx + 48, ry + 20, rows[k][0], 10, DTEXT if on else "#5C5C64", 700)
                val = rows[k][1] if on else "Could not reach source"
                if name == "Offline":
                    val = "Last seen 22 min ago" if k == 0 else "Not available offline"
                if name == "Stale":
                    val = rows[k][1]
                s += text(cx + 320, ry + 20, val, 9.2, DMUTE if on else "#4E4E56", 600, "end")
            if name == "Stale":
                s += rect(cx + 14, cy + 214 - 32, 320, 26, 7, "#241D07", GOLD, 1)
                s += text(cx + 26, cy + 200, "Shown from cache · tap to refresh", 8.8, GOLD, 700)
            if name == "Offline":
                s += rect(cx + 14, cy + 182, 320, 26, 7, "#2A1512", FIRE, 1)
                s += text(cx + 26, cy + 200, "You are offline. This is what we last knew.", 8.8, "#F0A18C", 700)
            if name == "Partial":
                s += rect(cx + 14, cy + 182, 320, 26, 7, "#241D07", GOLD, 1)
                s += text(cx + 26, cy + 200, "2 sources timed out. Retrying in 30s.", 8.8, GOLD, 700)
        s += text(cx, cy - 8, f"{i+1:02d} · {name}".upper(), 9.5, MUTE, 800, ls=1)

    s += rect(48, 630, 1104, 54, 12, GOLD_SOFT, GOLD, 1.4)
    s += text(68, 654, "Rule", 11.5, TEXT, 800)
    s += text(116, 654, "the app never shows a blank screen and never shows a stale number without saying it is stale. Both are one component with a state prop.", 11.5, MUTE, 600)
    s += text(68, 674, "Every state has a written copy string, a colour token and an aria-live announcement. Nothing here is decoration.", 10.4, MUTE, 600)
    write(P("sw-01-states.svg"), svg(W, H, s, title="ServiceWaze six interface states"))


# ══════════════════════════════════════════════════════════════════════════
# SERVICEWAZE 02 — offline-first architecture
# ══════════════════════════════════════════════════════════════════════════
def sw_arch():
    W, H = 1200, 646
    s = text(48, 52, "Offline-first, because the network is the feature", 23, TEXT, 800)
    s += text(48, 76, "Angular 17 standalone components, a hand-written service worker, IndexedDB, and one rule about freshness.", 12, MUTE, 600)

    def box(x, y, w, h, t, sub, fill=PAPER, stroke=LINE, accent=None):
        g = rect(x, y, w, h, 12, fill, stroke, 1.5)
        if accent:
            g += f'<rect x="{x}" y="{y}" width="{w}" height="4" rx="2" fill="{accent}"/>'
        g += text(x + 16, y + 28, t, 12, TEXT, 800)
        body, _ = wrap_text(x + 16, y + 46, sub, int(w / 5.6), 9.6, MUTE, 600, 12.5)
        return g + body

    s += box(48, 118, 210, 96, "UI layer", "Standalone components. Pure inputs, no HTTP, no dates. Trivially testable.", PAPER, LINE, PURPLE)
    s += arrow(258, 166, 300, 166, MUTE)
    s += box(300, 118, 210, 96, "Signal store", "One state object per suburb: data, fetchedAt, source, status.", PAPER, LINE, CYAN)
    s += arrow(510, 166, 552, 166, MUTE)
    s += box(552, 118, 230, 96, "Resource gateway", "Decides cache vs. network. The only place that knows about time.", GOLD_SOFT, GOLD, GOLD)
    s += arrow(782, 166, 824, 166, MUTE)
    s += box(824, 118, 150, 96, "Service worker", "Stale-while-revalidate for reads, queue for writes.", PAPER, LINE, GOOD)
    s += arrow(974, 166, 1010, 166, MUTE)
    s += box(1010, 118, 142, 96, "5 public APIs", "Eskom, city water, SAWS, AQI, transport.", PAPER, LINE, FIRE)

    s += arrow(667, 214, 667, 258, CYAN, 2, dash="5 4")
    s += box(552, 258, 230, 84, "IndexedDB", "Last good payload per source, with its timestamp. Survives a cold start.", CYAN_SOFT, CYAN, CYAN)

    # freshness rule
    s += rect(48, 258, 470, 172, 14, PAPER, LINE, 1.4)
    s += text(70, 288, "The freshness rule, written once", 13, TEXT, 800)
    tiers = [("< 2 min", "Fresh — show it plainly", GOOD),
             ("2–15 min", "Stale — show it, say how old", GOLD),
             ("> 15 min", "Last known — say so, offer refresh", FIRE),
             ("no cache", "Empty state, never a spinner forever", MUTE)]
    for i, (k, v, c) in enumerate(tiers):
        ty = 310 + i * 30
        s += f'<rect x="70" y="{ty-11}" width="72" height="20" rx="10" fill="{c}" opacity=".14"/>'
        s += text(106, ty + 3, k, 9.4, c, 800, "middle")
        s += text(154, ty + 3, v, 10.4, MUTE, 600)

    # code
    s += rect(812, 258, 340, 172, 14, "#101014", "#26262B", 1.4)
    s += text(834, 286, "gateway.ts — the whole decision", 10, DMUTE, 800)
    code = [
        ("const age = now - cached.fetchedAt;", DTEXT),
        ("if (age < FRESH) return cached.value;", "#8FCFA8"),
        ("void revalidate();      // fire & forget", "#6E6A64"),
        ("if (age < STALE) return stale(cached);", "#E8C46A"),
        ("if (offline) return lastKnown(cached);", "#F0A18C"),
        ("return await network();", DTEXT),
    ]
    for i, (ln, c) in enumerate(code):
        s += text(834, 312 + i * 19, ln, 9.6, c, 500, font=MONO)

    s += rect(48, 452, 1104, 84, 12, CANVAS, LINE, 1.4)
    s += text(70, 480, "What this bought", 12, TEXT, 800)
    wins = [("0", "spinners that never end"), ("100%", "screens usable offline"),
            ("1", "place that knows about time"), ("38", "tests on the gateway alone"),
            ("2.1 KB", "of that logic, gzipped")]
    for i, (b, l) in enumerate(wins):
        wx = 70 + i * 218
        s += text(wx, 508, b, 19, GOLD, 800)
        s += text(wx, 524, l, 9.8, MUTE, 700)
        if i:
            s += f'<line x1="{wx-22}" y1="{490}" x2="{wx-22}" y2="{528}" stroke="{LINE}" stroke-width="1"/>' 

    s += rect(48, 552, 1104, 62, 12, PAPER, LINE, 1.4)
    s += text(70, 578, "The mistake I made first", 12, TEXT, 800)
    s += text(70, 598, "Version one cached in the components. Three components disagreed about what “now” meant and the UI flickered. Moving time into one gateway fixed a class of bug, not a bug.", 11, MUTE, 600)
    write(P("sw-02-arch.svg"), svg(W, H, s, title="ServiceWaze offline-first architecture"))


# ══════════════════════════════════════════════════════════════════════════
# SERVICEWAZE 03 — performance budget
# ══════════════════════════════════════════════════════════════════════════
def sw_perf():
    W, H = 1200, 560
    s = text(48, 52, "A budget, not a hope", 23, TEXT, 800)
    s += text(48, 76, "Set on day one, enforced in CI. The build fails if the main bundle crosses 180 KB gzipped.", 12, MUTE, 600)

    s += rect(48, 112, 540, 260, 14, PAPER, LINE, 1.4)
    s += text(70, 142, "JavaScript shipped, week by week", 12.5, TEXT, 800)
    s += text(70, 160, "gzipped, main entry point", 10, MUTE, 600)
    pts = [96, 118, 143, 162, 177, 171]
    s += line_chart(90, 186, 470, 130, pts, GOLD, ["w1", "w3", "w5", "w7", "w9", "ship"])
    # budget line
    by = 186 + 130 - (180 / (max(pts) * 1.15)) * 130
    s += f'<line x1="90" y1="{by:.0f}" x2="560" y2="{by:.0f}" stroke="{FIRE}" stroke-width="1.6" stroke-dasharray="6 4"/>'
    s += text(90, by - 8, "budget · 180 KB gzipped", 9.4, FIRE, 800)
    s += text(70, 352, "Two features were cut at week 9 rather than raise the number.", 10.2, MUTE, 600)

    s += rect(604, 112, 548, 260, 14, PAPER, LINE, 1.4)
    s += text(626, 142, "Lighthouse, mid-range Android on throttled 3G", 12.5, TEXT, 800)
    s += text(626, 160, "median of 5 runs, production build", 10, MUTE, 600)
    for i, (v, cap, sub) in enumerate([(96, "96", "Performance"), (100, "100", "Accessibility"),
                                       (100, "100", "Best practices"), (100, "100", "SEO")]):
        s += gauge(690 + i * 130, 250, 40, v, GOOD if v >= 90 else GOLD, cap, sub)

    metrics = [("1.2s", "First contentful paint"), ("1.9s", "Largest contentful paint"),
               ("0.01", "Cumulative layout shift"), ("48ms", "Interaction to next paint"),
               ("171 KB", "JS gzipped"), ("0", "Blocking third-party scripts")]
    for i, (b, l) in enumerate(metrics):
        s += kpi_tile(48 + i * 186, 396, 170, 66, b, l, GOLD)

    s += rect(48, 478, 1104, 62, 12, CANVAS, LINE, 1.4)
    s += text(70, 504, "How it is kept", 12, TEXT, 800)
    s += text(70, 526, "GitHub Action runs Lighthouse CI and size-limit on every pull request. A regression is a red check, not a conversation three months later.", 11.2, MUTE, 600)
    write(P("sw-03-perf.svg"), svg(W, H, s, title="ServiceWaze performance budget and results"))


# ══════════════════════════════════════════════════════════════════════════
# MERIDIAN 01 — pipeline
# ══════════════════════════════════════════════════════════════════════════
def ds_pipeline():
    W, H = 1200, 620
    s = text(48, 52, "One source of truth, four places it lands", 23, TEXT, 800)
    s += text(48, 76, "Figma variables are the source. Everything downstream is generated. Nobody types a hex value by hand.", 12, MUTE, 600)

    stages = [
        ("Figma variables", "3 collections, 2 modes\nlight / dark", PURPLE, PURPLE_SOFT),
        ("tokens.json", "exported by a plugin\ncommitted to git", CYAN, CYAN_SOFT),
        ("Style Dictionary", "one transform per\nplatform", GOLD, GOLD_SOFT),
        ("Build outputs", "CSS · SCSS · TS · XML", GOOD, GOOD_SOFT),
    ]
    for i, (t, sub, c, soft) in enumerate(stages):
        x = 48 + i * 250
        s += rect(x, 116, 216, 104, 13, soft, c, 1.5)
        s += text(x + 16, 146, t, 13, TEXT, 800)
        for j, ln in enumerate(sub.split("\n")):
            s += text(x + 16, 168 + j * 15, ln, 10, MUTE, 600)
        if i < 3:
            s += arrow(x + 216, 168, x + 250, 168, MUTE, 2)

    # outputs fan
    outs = [("web/tokens.css", "custom properties", CYAN),
            ("angular/_tokens.scss", "mixins + maps", FIRE),
            ("ts/tokens.ts", "typed constants", GOLD),
            ("android/colors.xml", "resource values", GOOD)]
    rail_x = 806
    s += f'<path d="M958 220 V236 H{rail_x} V{250 + 3*62 + 25} " stroke="{LINE_2}" stroke-width="1.4" fill="none"/>'
    for i, (f, d, c) in enumerate(outs):
        y = 250 + i * 62
        s += f'<line x1="{rail_x}" y1="{y+25}" x2="830" y2="{y+25}" stroke="{LINE_2}" stroke-width="1.4"/>'
        s += f'<circle cx="{rail_x}" cy="{y+25}" r="3" fill="{LINE_2}"/>'
        s += rect(830, y, 322, 50, 10, PAPER, LINE, 1.3)
        s += f'<rect x="830" y="{y}" width="4" height="50" rx="2" fill="{c}"/>'
        s += text(848, y + 22, f, 10.6, TEXT, 700, font=MONO)
        s += text(848, y + 38, d, 9.4, MUTE, 600)

    # CI gate
    s += rect(48, 250, 750, 248, 14, PAPER, LINE, 1.4)
    s += text(70, 280, "The gate that stops drift", 13, TEXT, 800)
    s += text(70, 298, "A pull request cannot merge if any of these fail", 10, MUTE, 600)
    checks = [
        ("no-raw-colour", "eslint rule: a hex literal in a component is an error", GOOD),
        ("token-diff", "posts a table of every changed token on the PR", GOOD),
        ("contrast", "every semantic pair checked against WCAG AA, both modes", GOOD),
        ("visual-diff", "Storybook snapshots, 1% threshold", GOOD),
        ("a11y", "axe on every story, zero criticals", GOOD),
        ("bundle", "the token layer must stay under 6 KB", GOLD),
    ]
    for i, (n, d, c) in enumerate(checks):
        cy = 320 + i * 30
        s += f'<circle cx="84" cy="{cy-4}" r="8" fill="{c}"/>'
        s += f'<path d="M80 {cy-4} l3 3 l5.5 -6.5" stroke="#FFF" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
        s += text(102, cy, n, 10.6, TEXT, 800, font=MONO)
        s += text(240, cy, d, 10.2, MUTE, 600)

    s += rect(48, 518, 1104, 76, 12, GOLD_SOFT, GOLD, 1.4)
    s += text(70, 546, "Before this existed", 12, TEXT, 800)
    s += text(70, 568, "213 hard-coded colours across 4 products, a brand refresh estimated at 6 weeks, and a QA backlog where “wrong shade of grey” was a recurring ticket type.", 11.2, MUTE, 600)
    s += text(70, 586, "After: the same refresh took 2 days, most of which was screenshots for sign-off.", 10.4, MUTE, 600)
    write(P("ds-01-pipeline.svg"), svg(W, H, s, title="Design token pipeline"))


# ══════════════════════════════════════════════════════════════════════════
# MERIDIAN 02 — token layers
# ══════════════════════════════════════════════════════════════════════════
def ds_tokens():
    W, H = 1200, 600
    s = text(48, 52, "Three layers, and a rule about which one you may touch", 23, TEXT, 800)
    s += text(48, 76, "Designers work in semantic. Product teams work in component. Nobody but me edits primitives.", 12, MUTE, 600)

    layers = [
        ("01 · Primitive", "Raw values. No meaning. Never referenced by a component.",
         [("brand.amber.500", "#F0A500"), ("neutral.900", "#0E0E10"), ("neutral.050", "#F5EDD8"), ("red.600", "#E04E14")], PURPLE, PURPLE_SOFT),
        ("02 · Semantic", "What the value is for. Flips with the mode. This is the layer designers use.",
         [("surface.base", "→ neutral.900"), ("text.high", "→ neutral.050"), ("action.primary", "→ brand.amber.500"), ("status.danger", "→ red.600")], CYAN, CYAN_SOFT),
        ("03 · Component", "Scoped to one component. Defaults to a semantic token, overridable per product.",
         [("button.bg.rest", "→ action.primary"), ("button.text.rest", "→ surface.base"), ("card.border", "→ border.subtle"), ("input.ring.focus", "→ action.primary"), ], GOLD, GOLD_SOFT),
    ]
    for i, (t, d, rows, c, soft) in enumerate(layers):
        x = 48 + i * 372
        s += rect(x, 116, 356, 300, 14, PAPER, LINE, 1.4)
        s += rect(x, 116, 356, 40, 14, soft, "none", 0)
        s += f'<rect x="{x}" y="{136}" width="356" height="20" fill="{soft}"/>'
        s += text(x + 18, 141, t.upper(), 10.5, c, 800, ls=0.8)
        body, _ = wrap_text(x + 18, 176, d, 44, 10, MUTE, 600, 13)
        s += body
        for j, (k, v) in enumerate(rows):
            ry = 226 + j * 40
            s += rect(x + 18, ry, 320, 32, 8, CANVAS, LINE_2, 1.1)
            s += text(x + 30, ry + 20, k, 9.6, TEXT, 700, font=MONO)
            if v.startswith("#"):
                s += rect(x + 300, ry + 8, 26, 16, 4, v, LINE, 1)
            else:
                s += text(x + 326, ry + 20, v, 9, c, 700, "end", font=MONO)
        if i < 2:
            s += arrow(x + 356, 266, x + 372, 266, MUTE, 2)

    # resolution example
    s += rect(48, 436, 1104, 142, 14, PAPER, LINE, 1.4)
    s += text(70, 464, "How one value resolves — and why light mode needs no extra work", 13, TEXT, 800)
    chain = [("button.bg.rest", GOLD), ("action.primary", CYAN), ("brand.amber.500", PURPLE), ("#F0A500", TEXT)]
    for i, (n, c) in enumerate(chain):
        cx = 70 + i * 250
        s += rect(cx, 486, 210, 40, 9, CANVAS, c, 1.4)
        s += text(cx + 105, 511, n, 10.4, c, 800, "middle", font=MONO)
        if i < 3:
            s += arrow(cx + 210, 506, cx + 250, 506, MUTE, 1.8)
    s += text(70, 552, "In light mode only the semantic layer changes: action.primary → brand.amber.700. Components are untouched, so nothing can be missed.", 10.6, MUTE, 600)
    s += rect(70, 560, 1060, 1, 0.5, LINE, "none", 0)
    write(P("ds-02-tokens.svg"), svg(W, H, s, title="Token architecture in three layers"))


# ══════════════════════════════════════════════════════════════════════════
# MERIDIAN 03 — component inventory + adoption
# ══════════════════════════════════════════════════════════════════════════
def ds_inventory():
    W, H = 1200, 634
    s = text(48, 52, "80+ components, and proof anyone is using them", 23, TEXT, 800)
    s += text(48, 76, "A library nobody adopts is a hobby. Adoption is measured in CI and posted to the team channel every Monday.", 12, MUTE, 600)

    groups = [("Primitives", ["Button", "Icon button", "Link", "Input", "Textarea", "Select", "Checkbox", "Radio", "Switch", "Slider", "Chip", "Avatar"]),
              ("Layout", ["Stack", "Grid", "Card", "Divider", "Panel", "Sheet", "Modal", "Drawer"]),
              ("Navigation", ["Tabs", "Breadcrumb", "Pagination", "Stepper", "Menu", "Sidebar"]),
              ("Feedback", ["Alert", "Toast", "Skeleton", "Spinner", "Empty", "Progress", "Tooltip"]),
              ("Data", ["Table", "List", "Tree", "Stat", "Badge", "Timeline", "Chart shell"])]
    x = 48
    for gi, (g, items) in enumerate(groups):
        colw = 214
        gx = 48 + gi * (colw + 8)
        ch = 54 + len(items) * 21
        s += rect(gx, 116, colw, ch, 12, PAPER, LINE, 1.4)
        s += text(gx + 14, 140, g.upper(), 9.5, GOLD, 800, ls=1)
        s += text(gx + colw - 14, 140, str(len(items)), 9.5, MUTE, 800, "end")
        for j, it in enumerate(items):
            iy = 154 + j * 21
            s += rect(gx + 12, iy, colw - 24, 17, 4, CANVAS, LINE_2, 1)
            s += text(gx + 20, iy + 12.5, it, 8.8, MUTE, 700)
    s += text(48, 412, "Plus 12 patterns (search, filter bar, form layout, empty-to-first-run, destructive confirm…) documented as compositions, not new components.", 10.4, MUTE, 600)

    # adoption
    s += rect(48, 434, 552, 176, 14, PAPER, LINE, 1.4)
    s += text(70, 462, "Adoption — % of UI built from the library", 12.5, TEXT, 800)
    s += line_chart(90, 482, 480, 84, [12, 31, 48, 63, 74, 81, 88, 91], GOOD,
                    ["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8"])
    s += text(70, 598, "Measured by an AST scan of every product repo on each merge to main.", 9.8, MUTE, 600)

    s += rect(624, 434, 528, 176, 14, PAPER, LINE, 1.4)
    s += text(646, 462, "Design-QA comments per release", 12.5, TEXT, 800)
    s += bar_chart(666, 490, 470, 76, [("r1", 64), ("r2", 51), ("r3", 38), ("r4", 22), ("r5", 14), ("r6", 11)],
                   maxv=82, color=FIRE, gap=26)
    s += text(646, 598, "Same reviewer, same checklist. “Wrong shade of grey” has not appeared since release 3.", 9.8, MUTE, 600)
    write(P("ds-03-inventory.svg"), svg(W, H, s, title="Component inventory and adoption"))


# ══════════════════════════════════════════════════════════════════════════
# PERF 01 — audit before / after
# ══════════════════════════════════════════════════════════════════════════
def perf_audit():
    W, H = 1200, 580
    s = text(48, 52, "I audited my own site and did not like what I found", 23, TEXT, 800)
    s += text(48, 76, "November baseline on a Moto G Power, Fast 3G, cold cache. The numbers below are all from that same rig.", 12, MUTE, 600)

    s += rect(48, 112, 540, 268, 14, PAPER, LINE, 1.4)
    s += text(70, 142, "Lighthouse — before", 12.5, FIRE, 800)
    for i, (v, sub) in enumerate([(41, "Performance"), (78, "Accessibility"), (83, "Best practices"), (72, "SEO")]):
        s += gauge(140 + (i % 2) * 240, 210 + (i // 2) * 118, 38, v, FIRE if v < 60 else GOLD, str(v), sub)

    s += rect(612, 112, 540, 268, 14, PAPER, LINE, 1.4)
    s += text(634, 142, "Lighthouse — after", 12.5, GOOD, 800)
    for i, (v, sub) in enumerate([(99, "Performance"), (100, "Accessibility"), (100, "Best practices"), (100, "SEO")]):
        s += gauge(704 + (i % 2) * 240, 210 + (i // 2) * 118, 38, v, GOOD, str(v), sub)

    rows = [("Largest contentful paint", "6.4s", "1.1s", GOOD),
            ("Total blocking time", "980ms", "20ms", GOOD),
            ("Cumulative layout shift", "0.34", "0.00", GOOD),
            ("Page weight", "5.8 MB", "0.24 MB", GOOD),
            ("Requests", "74", "18", GOOD),
            ("Third-party scripts", "6", "0", GOOD)]
    s += rect(48, 404, 1104, 152, 14, PAPER, LINE, 1.4)
    s += text(70, 432, "The six numbers that moved", 12.5, TEXT, 800)
    for i, (n, a, b, c) in enumerate(rows):
        rx = 70 + (i % 3) * 364
        ry = 456 + (i // 3) * 50
        s += text(rx, ry + 14, n, 10.4, MUTE, 700)
        s += text(rx, ry + 34, a, 13, FIRE, 800)
        s += arrow(rx + 58, ry + 29, rx + 84, ry + 29, LINE_2, 1.6)
        s += text(rx + 92, ry + 34, b, 13, c, 800)
    write(P("perf-01-audit.svg"), svg(W, H, s, title="Performance audit before and after"))


# ══════════════════════════════════════════════════════════════════════════
# PERF 02 — waterfall
# ══════════════════════════════════════════════════════════════════════════
def perf_waterfall():
    W, H = 1200, 650
    s = text(48, 52, "Where the six seconds went", 23, TEXT, 800)
    s += text(48, 76, "Network waterfall, same page, same connection. Left is what I inherited. Right is what ships now.", 12, MUTE, 600)

    def wf(x, y, w, title_txt, items, total, color_map, tone, tti="", h=380):
        g = rect(x, y, w, h, 14, PAPER, LINE, 1.4)
        g += text(x + 20, y + 30, title_txt, 12.5, tone, 800)
        g += text(x + w - 20, y + 30, tti, 10.5, tone, 800, "end")
        track_x = x + 132
        track_w = w - 152
        for i in range(0, int(total) + 1):
            gx = track_x + (i / total) * track_w
            g += f'<line x1="{gx:.0f}" y1="{y+44}" x2="{gx:.0f}" y2="{y+h-32}" stroke="{LINE}" stroke-width="1" stroke-dasharray="2 4"/>'
            g += text(gx, y + h - 16, f"{i}s", 8.6, MUTE, 700, "middle")
        for i, (n, st, dur, kind) in enumerate(items):
            iy = y + 56 + i * 26
            g += text(x + 20, iy + 12, n, 9.2, MUTE, 700, font=MONO)
            bx = track_x + (st / total) * track_w
            bw = max(3, (dur / total) * track_w)
            g += f'<rect x="{bx:.1f}" y="{iy+3}" width="{bw:.1f}" height="13" rx="3" fill="{color_map[kind]}"/>'
        return g

    before = [("document", 0, .5, "doc"), ("style.css", .5, .7, "css"), ("fonts.gstatic", .6, 1.1, "font"),
              ("bootstrap.js", .6, 1.4, "js"), ("jquery.js", .7, .9, "js"), ("analytics-a.js", 1.2, 1.3, "3p"),
              ("analytics-b.js", 1.4, 1.5, "3p"), ("chat-widget.js", 1.6, 1.8, "3p"), ("hero.png 2.1MB", 2.0, 3.4, "img"),
              ("gallery-1.png", 2.4, 2.9, "img"), ("gallery-2.png", 2.6, 2.8, "img"), ("icon-set.png", 3.1, 1.2, "img")]
    after = [("document", 0, .32, "doc"), ("critical css", 0, 0, "css"), ("hero.webp 41KB", .34, .38, "img"),
             ("app.js 24KB", .34, .3, "js"), ("font (subset)", .36, .22, "font"), ("gallery (lazy)", 1.3, .2, "img")]
    cm = {"doc": TEXT, "css": PURPLE, "js": GOLD, "font": CYAN, "img": FIRE, "3p": "#B0A695"}
    s += wf(48, 108, 552, "Before — 74 requests, 5.8 MB", before, 7, cm, FIRE, "6.9s to interactive")
    s += wf(624, 108, 528, "After — 18 requests, 240 KB", after, 7, cm, GOOD, "1.1s to interactive")

    legend = [("Document", TEXT), ("CSS", PURPLE), ("JavaScript", GOLD), ("Font", CYAN), ("Image", FIRE), ("Third party", "#B0A695")]
    lx = 48
    for n, c in legend:
        s += f'<rect x="{lx}" y="{508}" width="12" height="12" rx="3" fill="{c}"/>'
        s += text(lx + 18, 518, n, 9.6, MUTE, 700)
        lx += len(n) * 6.4 + 46

    s += rect(48, 536, 1104, 92, 12, CANVAS, LINE, 1.4)
    s += text(70, 564, "Six changes, in the order that mattered", 12, TEXT, 800)
    changes = ["Deleted 3 third-party scripts nobody had asked for in two years.",
               "Re-encoded 41 images to WebP at the size they are actually displayed (−96% weight).",
               "Inlined the 6 KB of CSS the first screen needs; the rest loads after paint.",
               "Subset the font to the glyphs the site uses, self-hosted, preloaded.",
               "Replaced jQuery + Bootstrap with 24 KB of hand-written JavaScript.",
               "Reserved height on every image, which is where the 0.34 layout shift went."]
    for i, c in enumerate(changes):
        cx = 70 + (i % 2) * 552
        cy = 586 + (i // 2) * 17
        s += text(cx, cy, "· " + c, 9.8, MUTE, 600)
    write(P("perf-02-waterfall.svg"), svg(W, H, s, title="Network waterfall before and after"))


# ══════════════════════════════════════════════════════════════════════════
# PERF 03 — structured data
# ══════════════════════════════════════════════════════════════════════════
def perf_schema():
    W, H = 1200, 560
    s = text(48, 52, "Making the site legible to machines", 23, TEXT, 800)
    s += text(48, 76, "One JSON-LD graph per page, six connected types, validated in CI against the Schema.org vocabulary.", 12, MUTE, 600)

    nodes = [("Person", "Lulamile Mkhungela", 300, 200, PURPLE),
             ("WebSite", "lulasync.app", 120, 320, CYAN),
             ("WebPage", "this page", 300, 380, CYAN),
             ("BreadcrumbList", "Home › Work › …", 500, 330, GOLD),
             ("CreativeWork", "each case study", 500, 190, GOLD),
             ("Organization", "LulaSync", 120, 160, GOOD)]
    edges = [(0, 1, "publisher"), (0, 5, "worksFor"), (1, 2, "isPartOf"),
             (2, 3, "breadcrumb"), (0, 4, "author"), (2, 4, "mainEntity")]
    # keep edge labels clear of the nodes
    for a, b, lbl in edges:
        x1, y1 = nodes[a][2], nodes[a][3]
        x2, y2 = nodes[b][2], nodes[b][3]
        s += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{LINE_2}" stroke-width="1.4"/>'
        s += f'<rect x="{(x1+x2)/2 - (len(lbl)*2.6+7)}" y="{(y1+y2)/2 - 15}" width="{len(lbl)*5.2+14}" height="15" rx="7.5" fill="{CANVAS}"/>'
        s += text((x1 + x2) / 2, (y1 + y2) / 2 - 4, lbl, 8.4, MUTE, 700, "middle")
    for n, sub, x, y, c in nodes:
        w = max(120, len(n) * 8 + 40)
        s += rect(x - w / 2, y - 22, w, 44, 10, PAPER, c, 1.6)
        s += text(x, y - 4, n, 10.6, c, 800, "middle")
        s += text(x, y + 12, sub, 8.8, MUTE, 600, "middle")

    s += rect(660, 112, 492, 300, 14, "#101014", "#26262B", 1.4)
    s += text(682, 140, "index.html — the graph, abbreviated", 10, DMUTE, 800)
    code = [
        '"@context": "https://schema.org",', '"@graph": [', '  { "@type": "Person",',
        '    "@id": "…/#lulamile",', '    "jobTitle": ["UX/UI Designer",',
        '                 "Frontend Developer"],', '    "knowsAbout": ["Design systems", …] },',
        '  { "@type": "WebSite", "publisher":', '    { "@id": "…/#lulamile" } },',
        '  { "@type": "CreativeWork",', '    "name": "Engage — one home screen",',
        '    "author": { "@id": "…/#lulamile" } }', ']',
    ]
    for i, ln in enumerate(code):
        col = "#E8C46A" if '"@type"' in ln else ("#8FCFA8" if ln.strip().startswith('"') else DTEXT)
        s += text(682, 166 + i * 18, ln, 9.4, col, 500, font=MONO)

    tiles = [("6", "schema types"), ("0", "validation warnings"), ("11/11", "pages with canonical + OG"),
             ("100", "Lighthouse SEO"), ("0", "cookies set"), ("1.4 KB", "analytics payload")]
    for i, (b, l) in enumerate(tiles):
        s += kpi_tile(48 + i * 186, 436, 170, 66, b, l, GOLD)

    s += text(48, 534, "Analytics is a 1.4 KB first-party script that records page, referrer and Core Web Vitals. No cookies, no fingerprint, no consent banner needed.", 10.4, MUTE, 600)
    write(P("perf-03-schema.svg"), svg(W, H, s, title="Structured data graph"))


if __name__ == "__main__":
    sw_states(); sw_arch(); sw_perf()
    ds_pipeline(); ds_tokens(); ds_inventory()
    perf_audit(); perf_waterfall(); perf_schema()
