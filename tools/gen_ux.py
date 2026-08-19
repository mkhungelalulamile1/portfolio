#!/usr/bin/env python3
"""Artefacts for the three UX/UI + product design case studies."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from artifacts_lib import *  # noqa

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "cs")
os.makedirs(OUT, exist_ok=True)
P = lambda n: os.path.join(OUT, n)


# ══════════════════════════════════════════════════════════════════════════
# ENGAGE 01 — Research wall (affinity clustering)
# ══════════════════════════════════════════════════════════════════════════
def engage_research():
    W, H = 1200, 716
    s = ""
    s += text(48, 54, "Discovery — affinity wall", 24, TEXT, 800)
    s += text(48, 78, "14 interviews · 6 shadowing sessions · 2 041 support tickets tagged · 31 days", 12.5, MUTE, 600)
    c, _ = chip(48, 96, "Vodacom Engage · week 1–4", CANVAS, LINE_2, MUTE)
    s += c

    themes = [
        ("Cannot find it", FIRE, FIRE_SOFT, [
            "I know the leave form exists. I just never know where.",
            "I use the search box because the menu lies to me.",
            "Eleven tiles and none of them say payslip.",
        ]),
        ("Two apps, one job", STICKY_2, CYAN_SOFT, [
            "Half of HR is in the app, half is on the intranet.",
            "I screenshot the canteen menu because it loads once a day.",
            "Manager approvals only work on desktop.",
        ]),
        ("The 4-bar problem", STICKY, GOLD_SOFT, [
            "In the basement it just spins forever.",
            "If it fails I stop trying. I phone the service desk.",
            "Data is expensive. I only open it on Wi-Fi.",
        ]),
        ("Nobody trusts it", STICKY_4, GOOD_SOFT, [
            "It said submitted. HR never got it.",
            "There is no way to see where my request is.",
            "I ask my colleague instead of the app.",
        ]),
    ]

    x0, y0, colw = 48, 140, 272
    stick_colors = [STICKY_3, STICKY_2, STICKY, STICKY_4]
    for i, (name, accent, soft, quotes) in enumerate(themes):
        cx = x0 + i * (colw + 16)
        s += rect(cx, y0, colw, 448, 14, PAPER, LINE, 1.4)
        s += rect(cx, y0, colw, 40, 14, soft, "none", 0)
        s += f'<rect x="{cx}" y="{y0+26}" width="{colw}" height="14" fill="{soft}"/>'
        s += text(cx + 16, y0 + 25, name.upper(), 11, TEXT, 800, ls=0.8)
        s += text(cx + colw - 16, y0 + 25, ["31 notes", "22 notes", "26 notes", "18 notes"][i], 10, MUTE, 800, "end")
        yy = y0 + 56
        for j, q in enumerate(quotes):
            s += sticky(cx + 14, yy, colw - 28, 104, "“" + q + "”", stick_colors[i], rot=(-1.4 if j % 2 else 1.2), size=10.5, chars=27)
            yy += 116
        s += f'<line x1="{cx+14}" y1="{y0+408}" x2="{cx+colw-14}" y2="{y0+408}" stroke="{LINE}" stroke-width="1"/>'
        s += text(cx + 16, y0 + 430, "→ design principle 0" + str(i + 1), 10, GOLD, 800)

    # method strip
    s += rect(48, 616, 1104, 76, 14, PAPER, LINE, 1.4)
    facts = [("14", "employee interviews"), ("6", "site shadowing"), ("2 041", "tickets tagged"),
             ("48s", "median time to task"), ("11", "top-level destinations"), ("31%", "gave up, phoned")]
    for i, (b, l) in enumerate(facts):
        fx = 48 + 20 + i * 182
        s += text(fx, 652, b, 22, GOLD, 800)
        s += text(fx, 672, l, 10, MUTE, 700)
        if i:
            s += f'<line x1="{fx-24}" y1="634" x2="{fx-24}" y2="674" stroke="{LINE}" stroke-width="1"/>'
    write(P("engage-01-research.svg"), svg(W, H, s, title="Engage affinity wall",
          desc="Four clusters of interview quotes: findability, split systems, connectivity and trust."))


# ══════════════════════════════════════════════════════════════════════════
# ENGAGE 02 — Current-state journey map
# ══════════════════════════════════════════════════════════════════════════
def engage_journey():
    W, H = 1200, 700
    s = text(48, 52, "Current-state journey — “claim a travel expense”", 23, TEXT, 800)
    s += text(48, 76, "Shadowed with 6 employees on their own devices. Median 48 seconds to reach the form, 3 of 6 gave up.", 12, MUTE, 600)

    stages = ["Opens app", "Scans home", "Guesses menu", "Finds form", "Submits", "Waits"]
    emo = [3, 2, 1, 2, 2, 1]  # 0 bad .. 4 good
    x0, y0, w = 48, 118, 1104
    cw = w / len(stages)

    s += rect(x0, y0, w, 44, 12, CANVAS, LINE, 1.4)
    for i, st in enumerate(stages):
        s += text(x0 + i * cw + cw / 2, y0 + 28, f"{i+1}. {st}", 12, TEXT, 800, "middle")
        if i:
            s += f'<line x1="{x0+i*cw}" y1="{y0}" x2="{x0+i*cw}" y2="{y0+400}" stroke="{LINE}" stroke-width="1" stroke-dasharray="3 4"/>'

    # emotion band
    band_y, band_h = y0 + 60, 150
    s += rect(x0, band_y, w, band_h, 12, PAPER, LINE, 1.4)
    s += label(x0 + 14, band_y + 20, "Emotion", MUTE)
    pts = [(x0 + i * cw + cw / 2, band_y + 34 + (4 - v) / 4 * (band_h - 58)) for i, v in enumerate(emo)]
    s += f'<path d="M{pts[0][0]} {band_y+band_h-14} ' + " ".join(f"L{px:.0f} {py:.0f}" for px, py in pts) + f' L{pts[-1][0]} {band_y+band_h-14} Z" fill="{FIRE}" opacity=".08"/>'
    s += curve(pts, FIRE, 2.6)
    for i, (px, py) in enumerate(pts):
        s += face(round(px), round(py), emo[i], FIRE)

    # rows
    rows = [
        ("Doing", [
            "Cold start, splash 2.4s", "Reads 11 tiles twice", "Taps “Services” — wrong",
            "Uses search as a menu", "Uploads photo of slip", "No status anywhere",
        ], PAPER),
        ("Pain", [
            "Login times out on 3G", "No labels they use", "Menu names are org-chart names",
            "Search is the real IA", "Upload fails silently", "Phones the service desk",
        ], FIRE_SOFT),
        ("Opportunity", [
            "Session that survives", "Show today, not everything", "Rename around tasks",
            "Promote search + recents", "Optimistic save + retry", "One status timeline",
        ], GOOD_SOFT),
    ]
    ry = band_y + band_h + 14
    for name, cells, fill in rows:
        s += rect(x0, ry, w, 74, 12, fill, LINE, 1.4)
        s += label(x0 + 14, ry + 18, name, MUTE)
        for i, cell in enumerate(cells):
            body, _ = wrap_text(x0 + i * cw + 14, ry + 38, cell, 20, 10.2, TEXT if fill == PAPER else MUTE, 600, 13)
            s += body
        ry += 82

    s += rect(x0, ry + 4, w, 62, 12, GOLD_SOFT, GOLD, 1.4)
    s += text(x0 + 18, ry + 30, "The finding that changed the brief", 12.5, TEXT, 800)
    s += text(x0 + 18, ry + 50, "Nobody was lost inside a task — they were lost before it started. The problem was the home screen, not the forms.", 11.5, MUTE, 600)
    write(P("engage-02-journey.svg"), svg(W, H, s, title="Engage current-state journey map"))


# ══════════════════════════════════════════════════════════════════════════
# ENGAGE 03 — IA before / after
# ══════════════════════════════════════════════════════════════════════════
def engage_ia():
    W, H = 1200, 700
    s = text(48, 52, "Information architecture — before and after", 23, TEXT, 800)
    s += text(48, 76, "Open card sort with 24 employees, then a tree test on both structures with 31 more.", 12, MUTE, 600)

    # BEFORE
    s += rect(48, 106, 540, 470, 16, PAPER, LINE, 1.4)
    s += rect(48, 106, 540, 42, 16, FIRE_SOFT, "none", 0)
    s += f'<rect x="48" y="132" width="540" height="16" fill="{FIRE_SOFT}"/>'
    s += text(70, 133, "BEFORE — 11 top-level destinations", 11.5, FIRE, 800, ls=0.6)
    old = ["My Vodacom", "Services", "Corporate", "Self Help", "HR Zone", "Comms",
           "Facilities", "Tools", "Links", "Directory", "More"]
    for i, o in enumerate(old):
        bx, by = 70 + (i % 3) * 168, 172 + (i // 3) * 62
        s += rect(bx, by, 152, 48, 9, CANVAS, LINE_2, 1.2)
        s += text(bx + 76, by + 29, o, 11, MUTE, 700, "middle")
    s += rect(70, 420, 488, 66, 10, FIRE_SOFT, FIRE, 1.2)
    s += text(86, 444, "Tree test: 38% success · 48s median · 4.1 wrong turns", 11.5, FIRE, 800)
    s += text(86, 464, "Named after departments. Two labels meant the same thing.", 10.5, MUTE, 600)
    s += text(70, 520, "Card sort agreement on “where does a payslip live?” — 21%", 10.5, MUTE, 700)
    s += rect(70, 532, 488, 10, 5, CANVAS, LINE, 1)
    s += rect(70, 532, 488 * 0.21, 10, 5, FIRE, "none", 0)

    s += arrow(600, 340, 640, 340, GOLD, 3)

    # AFTER
    s += rect(652, 106, 500, 470, 16, PAPER, LINE, 1.4)
    s += rect(652, 106, 500, 42, 16, GOOD_SOFT, "none", 0)
    s += f'<rect x="652" y="132" width="500" height="16" fill="{GOOD_SOFT}"/>'
    s += text(674, 133, "AFTER — 4 task hubs", 11.5, GOOD, 800, ls=0.6)
    new = [
        ("Today", "Shift, payslip, canteen, alerts", GOLD),
        ("Ask", "TOBi, service desk, directory", CYAN),
        ("Do", "Leave, claims, IT requests", PURPLE),
        ("Me", "Profile, documents, learning", GOOD),
    ]
    for i, (n, sub, col) in enumerate(new):
        bx, by = 674, 170 + i * 76
        s += rect(bx, by, 456, 62, 11, CANVAS, LINE_2, 1.2)
        s += f'<rect x="{bx}" y="{by}" width="5" height="62" rx="2.5" fill="{col}"/>'
        s += text(bx + 20, by + 27, n, 14, TEXT, 800)
        s += text(bx + 20, by + 46, sub, 10.5, MUTE, 600)
        s += text(bx + 436, by + 36, "›", 20, MUTE, 700, "end")
    s += rect(674, 482, 456, 66, 10, GOOD_SOFT, GOOD, 1.2)
    s += text(690, 506, "Tree test: 86% success · 19s median · 0.7 wrong turns", 11.5, GOOD, 800)
    s += text(690, 526, "Named after the thing you came to do, in the words people used.", 10.5, MUTE, 600)

    s += rect(48, 600, 1104, 62, 12, CANVAS, LINE, 1.4)
    s += text(68, 626, "Rule I held to", 12, TEXT, 800)
    s += text(196, 626, "If a label needs explaining during a tree test it is the wrong label. I change it, I do not defend it.", 11.5, MUTE, 600)
    s += text(68, 648, "Tested twice: 31 employees round one, 27 round two, same tasks, same script.", 10.5, MUTE, 600)
    write(P("engage-03-ia.svg"), svg(W, H, s, title="Engage information architecture before and after"))


# ══════════════════════════════════════════════════════════════════════════
# ENGAGE 04 — Wireframes with annotations
# ══════════════════════════════════════════════════════════════════════════
def engage_wireframes():
    W, H = 1200, 700
    s = text(48, 52, "Lo-fi wireframes — tested flat before any pixels", 23, TEXT, 800)
    s += text(48, 76, "Greyscale on purpose. Five employees, printed screens, one task each. Round 1 of 3.", 12, MUTE, 600)

    frames = [
        ("01 · Today", [("line", 0.55), ("card", 0.30), ("row3", 0), ("list", 0)]),
        ("02 · Do", [("line", 0.4), ("search", 0), ("list", 0), ("list", 0)]),
        ("03 · Request", [("line", 0.5), ("field", 0), ("field", 0), ("cta", 0)]),
        ("04 · Status", [("line", 0.45), ("timeline", 0), ("card", 0.22), ("cta", 0)]),
    ]
    x0 = 48
    for i, (name, blocks) in enumerate(frames):
        fx = x0 + i * 282
        s += frame_header(fx, 118, 250, name)
        s += rect(fx, 128, 250, 420, 14, PAPER, LINE_2, 1.4)
        s += wire_block(fx + 16, 146, 218, 26, "line")
        yy = 186
        for kind, ratio in blocks:
            if kind == "line":
                s += wire_block(fx + 16, yy, 218 * ratio + 60, 12, "line"); yy += 28
            elif kind == "card":
                s += wire_block(fx + 16, yy, 218, 84, "box"); s += wire_block(fx + 28, yy + 16, 120, 10, "line"); s += wire_block(fx + 28, yy + 34, 170, 10, "line"); s += wire_block(fx + 28, yy + 56, 68, 16, "btn"); yy += 100
            elif kind == "row3":
                for k in range(3):
                    s += wire_block(fx + 16 + k * 74, yy, 66, 60, "box")
                yy += 76
            elif kind == "list":
                for k in range(3):
                    s += wire_block(fx + 16, yy + k * 40, 218, 32, "box")
                yy += 132
            elif kind == "search":
                s += wire_block(fx + 16, yy, 218, 34, "box"); yy += 50
            elif kind == "field":
                s += wire_block(fx + 16, yy, 80, 9, "line"); s += wire_block(fx + 16, yy + 16, 218, 32, "box"); yy += 62
            elif kind == "cta":
                s += wire_block(fx + 16, yy, 218, 38, "btn"); yy += 54
            elif kind == "timeline":
                for k in range(4):
                    s += f'<circle cx="{fx+30}" cy="{yy+16+k*38}" r="7" fill="{GOLD if k<2 else LINE_2}"/>'
                    if k < 3:
                        s += f'<line x1="{fx+30}" y1="{yy+23+k*38}" x2="{fx+30}" y2="{yy+47+k*38}" stroke="{LINE_2}" stroke-width="2"/>'
                    s += wire_block(fx + 48, yy + 11 + k * 38, 150, 10, "line")
                yy += 160
        # bottom bar
        s += f'<line x1="{fx}" y1="492" x2="{fx+250}" y2="492" stroke="{LINE}" stroke-width="1.2"/>'
        for k in range(4):
            s += f'<circle cx="{fx+40+k*58}" cy="518" r="9" fill="{GOLD if k==i else LINE_2}" opacity="{1 if k==i else .6}"/>'

    notes = [
        (48, 588, 1, "Round 1: “Today” was called “Home”. Nobody expected their shift on it. Renamed and moved the shift card to the top."),
        (620, 588, 2, "Round 2: the request form lost 3 fields we could infer from the staff number. Completion went from 4 of 5 to 5 of 5."),
        (48, 640, 3, "Round 3: status timeline added after every participant asked “did it go through?” unprompted."),
        (620, 640, 4, "Only what survived three rounds got drawn in colour. Two ideas died here — a chat tab and a news feed."),
    ]
    for nx, ny, n, t in notes:
        s += annot(nx + 9, ny, t, n, FIRE, chars=62, size=10.5)
    write(P("engage-04-wireframes.svg"), svg(W, H, s, title="Engage lo-fi wireframes with test annotations"))


# ══════════════════════════════════════════════════════════════════════════
# ENGAGE 05 — Hi-fi UI
# ══════════════════════════════════════════════════════════════════════════
def engage_ui():
    W, H = 1200, 668
    s = text(48, 52, "Shipped interface — Android, iOS and web", 23, TEXT, 800)
    s += text(48, 76, "Built on the same tokens as the design system. Every screen works at 200% text size and on a 360 px phone.", 12, MUTE, 600)

    RED = "#E60000"

    def screen_today(ox, oy, iw, ih):
        g = f'<rect x="{ox}" y="{oy}" width="{iw}" height="{ih}" rx="18" fill="#FFFFFF"/>'
        g += f'<path d="M{ox} {oy+18} h{iw} v82 a18 18 0 0 1 -18 18 h-{iw-36} a18 18 0 0 1 -18 -18 Z" fill="{RED}"/>'
        g += f'<rect x="{ox}" y="{oy+18}" width="{iw}" height="18" fill="{RED}"/>'
        g += text(ox + 16, oy + 46, "Molo, Thandi", 15, "#FFF", 800)
        g += text(ox + 16, oy + 64, "Tuesday · Midrand campus", 9.5, "#FFD9D9", 600)
        g += rect(ox + 16, oy + 76, iw - 32, 34, 9, "#FFFFFF", "none", 0)
        g += text(ox + 28, oy + 97, "Search or ask TOBi", 10, MUTE, 600)
        g += f'<circle cx="{ox+iw-32}" cy="{oy+93}" r="8" fill="{GOLD}"/>'
        # shift card
        g += rect(ox + 16, oy + 124, iw - 32, 66, 11, "#FFF6F6", "#FFD2D2", 1.2)
        g += label(ox + 28, oy + 142, "Your shift today", RED, 8.5)
        g += text(ox + 28, oy + 164, "08:00 – 16:30", 16, TEXT, 800)
        g += text(ox + 28, oy + 180, "Clock-in open · Gate 2", 9.5, MUTE, 600)
        # quick tiles
        tiles = [("Payslip", GOLD), ("Leave", PURPLE), ("IT help", CYAN), ("Canteen", GOOD)]
        for i, (t, c) in enumerate(tiles):
            tx = ox + 16 + (i % 2) * ((iw - 32) / 2 + 4)
            ty = oy + 200 + (i // 2) * 62
            g += rect(tx, ty, (iw - 40) / 2, 54, 10, "#FAF8F5", "#EDE7DE", 1.2)
            g += f'<rect x="{tx+10}" y="{ty+10}" width="18" height="18" rx="5" fill="{c}"/>'
            g += text(tx + 10, ty + 44, t, 10.5, TEXT, 700)
        g += label(ox + 16, oy + 340, "In progress", MUTE)
        for i, (t, st, c) in enumerate([("Travel claim R1 240", "With finance", GOLD), ("New laptop dock", "Approved", GOOD)]):
            iy = oy + 350 + i * 42
            g += rect(ox + 16, iy, iw - 32, 36, 9, "#FFFFFF", "#EDE7DE", 1.2)
            g += f'<circle cx="{ox+30}" cy="{iy+18}" r="5" fill="{c}"/>'
            g += text(ox + 44, iy + 15, t, 10, TEXT, 700)
            g += text(ox + 44, iy + 28, st, 8.8, MUTE, 600)
        return g

    def screen_do(ox, oy, iw, ih):
        g = f'<rect x="{ox}" y="{oy}" width="{iw}" height="{ih}" rx="18" fill="#FFFFFF"/>'
        g += f'<rect x="{ox}" y="{oy+18}" width="{iw}" height="52" fill="#FFFFFF"/>'
        g += text(ox + 16, oy + 52, "Do", 18, TEXT, 800)
        g += rect(ox + 16, oy + 74, iw - 32, 32, 9, "#F4F1EB", "#E7E1D6", 1.2)
        g += text(ox + 28, oy + 94, "Find a request…", 10, MUTE, 600)
        g += label(ox + 16, oy + 126, "Most used", MUTE)
        rows = [("Apply for leave", "2 min · manager approves", PURPLE),
                ("Claim travel", "3 min · finance approves", GOLD),
                ("Log an IT fault", "1 min · auto-routed", CYAN),
                ("Book a meeting room", "instant", GOOD),
                ("Request a letter", "1 day", "#8A8070")]
        for i, (t, sub, c) in enumerate(rows):
            ry = oy + 138 + i * 50
            g += rect(ox + 16, ry, iw - 32, 44, 10, "#FFFFFF", "#EDE7DE", 1.2)
            g += f'<rect x="{ox+26}" y="{ry+12}" width="20" height="20" rx="6" fill="{c}" opacity=".16"/>'
            g += f'<rect x="{ox+32}" y="{ry+18}" width="8" height="8" rx="2" fill="{c}"/>'
            g += text(ox + 56, ry + 20, t, 10.6, TEXT, 700)
            g += text(ox + 56, ry + 34, sub, 8.0, MUTE, 600)
            g += text(ox + iw - 16, ry + 27, "›", 13, MUTE, 700, "end")
        return g

    def screen_status(ox, oy, iw, ih):
        g = f'<rect x="{ox}" y="{oy}" width="{iw}" height="{ih}" rx="18" fill="#FFFFFF"/>'
        g += text(ox + 16, oy + 52, "Travel claim", 17, TEXT, 800)
        g += text(ox + 16, oy + 70, "REQ-24817 · R1 240.00", 10, MUTE, 600)
        steps = [("Submitted", "Tue 09:14", GOOD), ("Manager approved", "Tue 11:02", GOOD),
                 ("With finance", "since Wed 08:00", GOLD), ("Paid", "expected Fri", "#C9C2B6")]
        for i, (t, when, c) in enumerate(steps):
            sy = oy + 104 + i * 62
            g += f'<circle cx="{ox+32}" cy="{sy+14}" r="9" fill="{c}"/>'
            if c != "#C9C2B6":
                g += f'<path d="M{ox+28} {sy+14} l3 3 l6 -7" stroke="#FFF" stroke-width="2" fill="none" stroke-linecap="round"/>'
            if i < 3:
                g += f'<line x1="{ox+32}" y1="{sy+25}" x2="{ox+32}" y2="{sy+53}" stroke="{"#DDD6C9" if i>1 else GOOD}" stroke-width="2.4"/>'
            g += text(ox + 52, sy + 12, t, 11, TEXT, 800)
            g += text(ox + 52, sy + 27, when, 9, MUTE, 600)
        g += rect(ox + 16, oy + 356, iw - 32, 52, 10, "#FFF9E8", "#F0DDA8", 1.2)
        g += text(ox + 28, oy + 376, "Finance pays on Fridays.", 9.2, TEXT, 700)
        g += text(ox + 28, oy + 392, "Push when it moves.", 8.8, MUTE, 600)
        g += rect(ox + 16, oy + 418, iw - 32, 34, 9, RED, "none", 0)
        g += text(ox + iw / 2, oy + 440, "Ask about this claim", 10.5, "#FFF", 800, "middle")
        return g

    labels = ["Today — one screen that answers “what now?”",
              "Do — tasks named the way people say them",
              "Status — the question the service desk kept getting"]
    for i, fn in enumerate([screen_today, screen_do, screen_status]):
        px = 60 + i * 240
        pre, (ox, oy), (iw, ih) = phone(px, 118, 200, 470)
        s += pre + fn(ox, oy, iw, ih)
        body, _ = wrap_text(px, 610, labels[i], 26, 10.2, MUTE, 600, 14)
        s += body

    # spec panel
    s += rect(800, 118, 352, 470, 14, PAPER, LINE, 1.4)
    s += text(822, 148, "Handover, not hand-off", 15, TEXT, 800)
    s += text(822, 168, "What went to the sprint with each screen", 10.5, MUTE, 600)
    items = [
        ("Tokens", "Colour, type, spacing referenced by name — no hex in the specs."),
        ("States", "Default, loading, empty, error, offline, 200% text. Six per screen."),
        ("Motion", "120 ms in / 90 ms out; reduced-motion turns it off."),
        ("A11y", "Touch 48 px, contrast ≥ 4.5:1, labelled landmarks, focus order written down."),
        ("Copy", "Every string in the file, reviewed with the service desk lead."),
        ("Code", "I opened the pull request for the Today screen myself."),
    ]
    yy = 196
    for t, d in items:
        s += f'<rect x="822" y="{yy}" width="4" height="{18 if len(d)<64 else 30}" rx="2" fill="{GOLD}"/>'
        s += text(836, yy + 12, t, 11.5, TEXT, 800)
        body, yy2 = wrap_text(836, yy + 28, d, 44, 10, MUTE, 600, 13)
        s += body
        yy = yy2 + 12
    write(P("engage-05-ui.svg"), svg(W, H, s, title="Engage shipped interface screens"))


# ══════════════════════════════════════════════════════════════════════════
# ENGAGE 06 — Results
# ══════════════════════════════════════════════════════════════════════════
def engage_results():
    W, H = 1200, 520
    s = text(48, 52, "Measured the same way, twice", 23, TEXT, 800)
    s += text(48, 76, "Same five tasks, same script, unmoderated, 8 weeks before launch and 8 weeks after. n = 31 then n = 27.", 12, MUTE, 600)

    s += rect(48, 110, 640, 300, 14, PAPER, LINE, 1.4)
    s += text(70, 140, "Task success rate", 13, TEXT, 800)
    s += text(70, 158, "% of people who finished without help", 10, MUTE, 600)
    c1, w1 = chip(468, 128, "Before", FIRE_SOFT, FIRE)
    c2, _ = chip(468 + w1 + 8, 128, "After", GOOD_SOFT, GOOD)
    s += c1 + c2
    series = [("Payslip", 41, 92), ("Leave", 52, 88), ("Travel claim", 38, 81),
              ("IT fault", 47, 90), ("Shift", 29, 94)]
    s += bar_chart(78, 190, 580, 168, series, maxv=112, color=FIRE, color2=GOOD, gap=22, val_fmt="{:.0f}%")

    s += rect(704, 110, 448, 300, 14, PAPER, LINE, 1.4)
    s += text(726, 140, "Median time to first task", 13, TEXT, 800)
    s += text(726, 158, "seconds, cold start on a mid-range Android", 10, MUTE, 600)
    s += line_chart(750, 186, 380, 140, [48, 44, 37, 28, 22, 19], GOLD,
                    ["wk 0", "wk 2", "wk 4", "wk 6", "wk 8", "wk 10"])
    s += text(750, 360, "48s", 19, FIRE, 800)
    s += text(750, 376, "before", 9.5, MUTE, 700)
    s += arrow(800, 354, 838, 354, MUTE, 2)
    s += text(852, 360, "19s", 19, GOOD, 800)
    s += text(852, 376, "after", 9.5, MUTE, 700)
    s += text(960, 360, "−60%", 19, GOLD, 800)
    s += text(960, 376, "improvement", 9.5, MUTE, 700)

    tiles = [("+34%", "self-service chats"), ("−28%", "service-desk calls"),
             ("4.6/5", "in-app rating (was 2.9)"), ("11 → 4", "top-level destinations"),
             ("0", "P1 accessibility defects")]
    for i, (b, l) in enumerate(tiles):
        s += kpi_tile(48 + i * 224, 430, 208, 62, b, l, GOLD)
    write(P("engage-06-results.svg"), svg(W, H, s, title="Engage before and after results"))


# ══════════════════════════════════════════════════════════════════════════
# TOBi 01 — Conversation audit
# ══════════════════════════════════════════════════════════════════════════
def tobi_audit():
    W, H = 1200, 700
    s = text(48, 52, "Conversation audit — what the bot actually did", 23, TEXT, 800)
    s += text(48, 76, "3 400 transcripts read in a spreadsheet, tagged by intent and by outcome. Two weeks, no assumptions.", 12, MUTE, 600)

    # left: transcript
    s += rect(48, 112, 470, 460, 14, PAPER, LINE, 1.4)
    s += text(70, 142, "A real transcript, lightly redacted", 12.5, TEXT, 800)
    msgs = [("u", "hi i need help with my bursary"),
            ("b", "Hi! I'm TOBi. How can I help you today?"),
            ("u", "bursary"),
            ("b", "Sorry, I didn't get that. You can ask me about airtime, data or billing."),
            ("u", "BURSARY APPLICATION"),
            ("b", "Sorry, I didn't get that. Type 'agent' to speak to someone."),
            ("u", "agent")]
    yy = 166
    for who, m in msgs:
        wdt = min(330, 60 + len(m) * 5.2)
        lines = (len(m) // 44) + 1
        hgt = 20 + lines * 14
        if who == "u":
            s += rect(518 - 26 - wdt, yy, wdt, hgt, 12, "#E8F3FF", "#C9E0F5", 1.2)
            body, _ = wrap_text(518 - 26 - wdt + 12, yy + 18, m, 44, 10.4, TEXT, 600, 14)
        else:
            s += rect(70, yy, wdt, hgt, 12, CANVAS, LINE_2, 1.2)
            body, _ = wrap_text(82, yy + 18, m, 44, 10.4, MUTE, 600, 14)
        s += body
        yy += hgt + 10
    s += rect(70, yy + 4, 426, 52, 10, FIRE_SOFT, FIRE, 1.2)
    s += text(84, yy + 26, "Six turns. Zero answers. One angry human.", 11.5, FIRE, 800)
    s += text(84, yy + 44, "This shape appeared in 41% of the transcripts I read.", 10.2, MUTE, 600)

    # right: intent coverage
    s += rect(542, 112, 610, 460, 14, PAPER, LINE, 1.4)
    s += text(564, 142, "Top intents vs. what the bot could answer", 12.5, TEXT, 800)
    s += text(564, 160, "Volume over 30 days · green = handled, red = dead end", 10, MUTE, 600)
    intents = [("Bursary / application status", 812, 0.0),
               ("Password + VPN reset", 640, 0.35),
               ("Payslip and tax certificate", 505, 0.0),
               ("Leave balance", 402, 0.55),
               ("Laptop / hardware fault", 361, 0.20),
               ("Canteen + shuttle times", 288, 1.0),
               ("Data and airtime", 244, 1.0),
               ("Everything else", 148, 0.10)]
    mx = 812
    for i, (n, v, cov) in enumerate(intents):
        iy = 186 + i * 46
        s += text(564, iy + 12, n, 10.6, TEXT, 700)
        s += text(1130, iy + 12, str(v), 10.6, MUTE, 800, "end")
        bw = (v / mx) * 566
        s += rect(564, iy + 20, 566, 12, 6, CANVAS, LINE, 1)
        s += rect(564, iy + 20, bw, 12, 6, FIRE, "none", 0)
        if cov > 0:
            s += rect(564, iy + 20, bw * cov, 12, 6, GOOD, "none", 0)
    lg1, w1 = chip(564, 546, "Handled end-to-end", GOOD_SOFT, GOOD)
    lg2, _ = chip(564 + w1 + 8, 546, "Dead end → human", FIRE_SOFT, FIRE)
    s += lg1 + lg2

    s += rect(48, 596, 1104, 68, 12, GOLD_SOFT, GOLD, 1.4)
    s += text(68, 622, "What the numbers said", 12.5, TEXT, 800)
    s += text(68, 644, "The two highest-volume intents had no coverage at all. Nobody had ever mapped intent volume against bot capability — so the roadmap was being written from opinion.", 11.5, MUTE, 600)
    write(P("tobi-01-audit.svg"), svg(W, H, s, title="TOBi conversation audit"))


# ══════════════════════════════════════════════════════════════════════════
# TOBi 02 — Service blueprint
# ══════════════════════════════════════════════════════════════════════════
def tobi_blueprint():
    W, H = 1200, 660
    s = text(48, 52, "Service blueprint — bursary application", 23, TEXT, 800)
    s += text(48, 76, "Drawn with the bursary office, the service desk and one student who had failed the process twice.", 12, MUTE, 600)
    cols = ["Hears about it", "Checks if eligible", "Applies", "Uploads documents", "Waits", "Outcome"]
    rows = [
        ("Student", ["Sees a poster, no link", "Reads a 6-page PDF", "42 fields, one page", "Scans at an internet café", "No status, phones", "Email, no reason given"]),
        ("Frontstage", ["Poster + WhatsApp forward", "PDF on the intranet", "Web form", "Email attachment", "Service desk queue", "Bulk mail merge"]),
        ("Backstage", ["Comms schedules print", "Policy owner updates PDF yearly", "Form writes to a shared inbox", "Admin renames files by hand", "Admin answers by phone", "Panel scores in a spreadsheet"]),
        ("Systems", ["—", "SharePoint", "Legacy form engine", "Outlook + network drive", "No ticket type exists", "Excel + mail merge"]),
        ("Fails", ["No single link to share", "Eligibility buried on p.4", "60% abandon here", "Filenames lost", "31% call twice", "No feedback loop"]),
    ]
    s += swimlane(48, 116, 1104, rows, cols, row_h=76, head_h=36)

    vis_y = 116 + 36 + 76 * 2
    s += f'<line x1="48" y1="{vis_y}" x2="1152" y2="{vis_y}" stroke="{CYAN}" stroke-width="1.6" stroke-dasharray="6 5"/>'
    s += text(1146, vis_y - 7, "line of visibility", 8.8, CYAN, 800, "end", ls=0.6)
    fails_y = 116 + 36 + 76 * 4
    s += f'<rect x="48" y="{fails_y}" width="1104" height="76" fill="{FIRE}" opacity=".05"/>'

    s += rect(48, 528, 542, 100, 12, PAPER, LINE, 1.4)
    s += text(68, 556, "Five failure points, one root cause", 12.5, TEXT, 800)
    s += text(68, 578, "The service assumed a laptop, a printer, uncapped data and patience.", 11, MUTE, 600)
    s += text(68, 598, "None of those were true for the students it was written for.", 11, MUTE, 600)
    s += rect(610, 528, 542, 100, 12, GOOD_SOFT, GOOD, 1.4)
    s += text(630, 556, "What I changed first", 12.5, TEXT, 800)
    s += text(630, 578, "Not the form. The two moments around it: an assistant that can answer", 11, MUTE, 600)
    s += text(630, 598, "“am I eligible?”, and a status the student can check without phoning.", 11, MUTE, 600)
    write(P("tobi-02-blueprint.svg"), svg(W, H, s, title="Bursary service blueprint"))


# ══════════════════════════════════════════════════════════════════════════
# TOBi 03 — Conversation design flow
# ══════════════════════════════════════════════════════════════════════════
def tobi_flow():
    W, H = 1200, 614
    s = text(48, 52, "Conversation design — the happy path and the three ways out", 23, TEXT, 800)
    s += text(48, 76, "Written as a script first, read aloud with the bursary office before a single node was built.", 12, MUTE, 600)

    def node(x, y, w, h, t, sub="", fill=PAPER, stroke=LINE, tc=TEXT, r=12):
        g = rect(x, y, w, h, r, fill, stroke, 1.5)
        g += text(x + w / 2, y + (h / 2 + 4 if not sub else h / 2 - 3), t, 11.5, tc, 800, "middle")
        if sub:
            g += text(x + w / 2, y + h / 2 + 14, sub, 9.5, MUTE, 600, "middle")
        return g

    s += node(48, 118, 190, 58, "“bursary”", "any of 61 phrasings", CYAN_SOFT, CYAN)
    s += arrow(238, 147, 282, 147, MUTE)
    s += node(282, 118, 200, 58, "Recognise intent", "confidence ≥ 0.72", PAPER)
    s += arrow(482, 147, 526, 147, MUTE)
    s += node(526, 106, 210, 82, "Ask ONE question", "employee, or applying from outside?", GOLD_SOFT, GOLD)
    s += arrow(736, 147, 782, 147, MUTE)
    s += node(782, 118, 190, 58, "Branch on answer", "2 paths, not 7", PAPER)
    s += arrow(972, 147, 1014, 147, MUTE)
    s += node(1014, 118, 138, 58, "Answer + link", "deep link to step 1", GOOD_SOFT, GOOD)

    # low confidence branch
    s += arrow(382, 176, 382, 232, FIRE, 1.8, dash="5 5")
    s += node(282, 232, 200, 62, "Low confidence", "< 0.72", FIRE_SOFT, FIRE)
    s += arrow(482, 263, 526, 263, FIRE, 1.8)
    s += node(526, 226, 300, 74, "Offer the 3 nearest intents", "never “I didn't get that” — always a next move", PAPER)
    s += arrow(826, 263, 874, 263, MUTE)
    s += node(874, 232, 278, 62, "Still stuck after 2 turns?", "hand to a human, with the transcript", GOLD_SOFT, GOLD)

    # rules
    s += rect(48, 336, 552, 250, 14, PAPER, LINE, 1.4)
    s += text(70, 366, "Five rules the script had to obey", 13, TEXT, 800)
    rules = [
        "One question per turn. Never two.",
        "No dead ends: every reply offers a next move.",
        "Two failed turns hands over to a human — with the transcript attached.",
        "Answer in the language the person opened in (EN, isiZulu, Sesotho, Afrikaans).",
        "Never say “I didn't understand” without naming what it can do.",
    ]
    yy = 396
    for i, r in enumerate(rules):
        s += f'<circle cx="84" cy="{yy-4}" r="10" fill="{GOLD_SOFT}" stroke="{GOLD}" stroke-width="1.2"/>'
        s += text(84, yy, str(i + 1), 10, GOLD, 800, "middle")
        body, yy2 = wrap_text(104, yy, r, 54, 11, MUTE, 600, 15)
        s += body
        yy = yy2 + 14

    s += rect(620, 336, 532, 250, 14, PAPER, LINE, 1.4)
    s += text(642, 366, "Content design: same answer, half the words", 13, TEXT, 800)
    s += rect(642, 382, 488, 84, 10, FIRE_SOFT, FIRE, 1.2)
    s += label(656, 402, "Before — 61 words", FIRE)
    body, _ = wrap_text(656, 420, "Thank you for contacting us. In order to determine your eligibility for the bursary programme, kindly refer to the eligibility criteria document available on the intranet portal under Human Resources / Learning and Development / Bursaries.", 74, 9.8, MUTE, 600, 13)
    s += body
    s += rect(642, 480, 488, 84, 10, GOOD_SOFT, GOOD, 1.2)
    s += label(656, 500, "After — 24 words", GOOD)
    body, _ = wrap_text(656, 518, "You qualify if you have worked here 12 months and passed your last review. Two questions and I'll check for you — ready?", 74, 9.8, TEXT, 600, 13)
    s += body
    write(P("tobi-03-flow.svg"), svg(W, H, s, title="TOBi conversation flow and content design"))


# ══════════════════════════════════════════════════════════════════════════
# TOBi 04 — Form redesign
# ══════════════════════════════════════════════════════════════════════════
def tobi_form():
    W, H = 1200, 660
    s = text(48, 52, "42 fields on one page → 4 steps that save themselves", 23, TEXT, 800)
    s += text(48, 76, "Field-by-field audit: what is it for, who reads it, can we already know it? 17 fields could not answer.", 12, MUTE, 600)

    # before
    s += rect(48, 112, 400, 452, 14, PAPER, LINE, 1.4)
    s += rect(48, 112, 400, 38, 14, FIRE_SOFT, "none", 0)
    s += f'<rect x="48" y="136" width="400" height="14" fill="{FIRE_SOFT}"/>'
    s += text(68, 137, "BEFORE — one page, 42 fields", 11, FIRE, 800, ls=0.6)
    for i in range(14):
        fy = 166 + i * 27
        s += wire_block(68, fy, 60 + (i % 3) * 24, 8, "line")
        s += wire_block(68, fy + 11, 360, 14, "box", "#F2EEE6")
    s += f'<rect x="48" y="{166+14*27}" width="400" height="70" fill="{PAPER}"/>'
    s += text(68, 456, "…28 more fields below the fold", 10.5, MUTE, 700)
    s += rect(68, 466, 360, 30, 7, CANVAS, FIRE, 1.2)
    s += text(84, 486, "No progress bar. No save. No way back.", 10, FIRE, 800)
    s += rect(68, 508, 360, 34, 8, FIRE_SOFT, FIRE, 1.2)
    s += text(84, 530, "60% abandonment · 38% completion", 11, FIRE, 800)

    s += arrow(464, 340, 508, 340, GOLD, 3)

    # after
    s += rect(524, 112, 628, 452, 14, PAPER, LINE, 1.4)
    s += rect(524, 112, 628, 38, 14, GOOD_SOFT, "none", 0)
    s += f'<rect x="524" y="136" width="628" height="14" fill="{GOOD_SOFT}"/>'
    s += text(544, 137, "AFTER — 4 steps, 25 fields, autosaves every answer", 11, GOOD, 800, ls=0.6)

    steps = [("1", "You", "4 fields — 3 pre-filled from your staff record", GOOD),
             ("2", "Your studies", "6 fields — institution list, not free text", GOOD),
             ("3", "Documents", "3 uploads — camera-first, 8 MB limit stated up front", GOLD),
             ("4", "Check & send", "read-only summary, one edit link per section", "#C9C2B6")]
    for i, (n, t, d, c) in enumerate(steps):
        sy = 168 + i * 74
        s += rect(544, sy, 588, 62, 11, CANVAS if i < 3 else PAPER, LINE_2, 1.2)
        s += f'<circle cx="574" cy="{sy+31}" r="15" fill="{c}"/>'
        s += text(574, sy + 36, n, 13, "#FFF", 800, "middle")
        s += text(602, sy + 26, t, 12.5, TEXT, 800)
        s += text(602, sy + 44, d, 10.2, MUTE, 600)
        if i < 3:
            s += text(1112, sy + 36, "✓", 15, GOOD, 800, "end")
    # progress
    s += text(544, 486, "Progress saved · you can close this and come back", 10.5, MUTE, 700)
    s += rect(544, 496, 588, 10, 5, CANVAS, LINE, 1)
    s += rect(544, 496, 588 * 0.75, 10, 5, GOOD, "none", 0)
    s += rect(544, 518, 588, 34, 8, GOOD_SOFT, GOOD, 1.2)
    s += text(560, 540, "22% abandonment · 61% completion · median 9 min (was 40)", 11, GOOD, 800)

    tiles = [("42 → 25", "fields"), ("17", "fields removed or inferred"),
             ("+61%", "completion"), ("−78%", "“where is my application?” calls"),
             ("4", "languages supported")]
    for i, (b, l) in enumerate(tiles):
        s += kpi_tile(48 + i * 224, 584, 208, 58, b, l, GOLD)
    write(P("tobi-04-form.svg"), svg(W, H, s, title="Bursary form redesign"))


# ══════════════════════════════════════════════════════════════════════════
# STANCE 01 — Discovery
# ══════════════════════════════════════════════════════════════════════════
def stance_discovery():
    W, H = 1200, 700
    s = text(48, 52, "Discovery — a market that kept being told “no”", 23, TEXT, 800)
    s += text(48, 76, "South Africa's modified-car community. 9 broker interviews, 214 forum posts coded, 3 ride-alongs.", 12, MUTE, 600)

    # problem framing
    s += rect(48, 112, 560, 268, 14, PAPER, LINE, 1.4)
    s += text(70, 142, "What actually happens today", 13, TEXT, 800)
    flow = [("Owner fits an exhaust", MUTE), ("Declares it", MUTE), ("Insurer loads or refuses", FIRE),
            ("Owner stops declaring", FIRE), ("Claim rejected later", FIRE)]
    for i, (t, c) in enumerate(flow):
        fy = 168 + i * 36
        s += f'<circle cx="88" cy="{fy+10}" r="7" fill="{c}"/>'
        if i < 4:
            s += f'<line x1="88" y1="{fy+18}" x2="88" y2="{fy+38}" stroke="{LINE_2}" stroke-width="2"/>'
        s += text(106, fy + 14, t, 11.5, c if c == FIRE else TEXT, 700)
    s += rect(70, 332, 516, 32, 8, FIRE_SOFT, FIRE, 1.2)
    s += text(86, 353, "7 of 9 brokers said they simply decline the segment.", 11, FIRE, 800)

    # evidence
    s += rect(628, 112, 524, 268, 14, PAPER, LINE, 1.4)
    s += text(650, 142, "Evidence from 214 forum posts", 13, TEXT, 800)
    ev = [("Refused cover outright", 96), ("Premium loaded 40%+", 61),
          ("Claim rejected for a mod", 38), ("Stopped declaring mods", 71),
          ("Wanted agreed value", 118)]
    for i, (t, v) in enumerate(ev):
        ey = 170 + i * 36
        s += text(650, ey + 11, t, 10.6, TEXT, 700)
        s += text(1130, ey + 11, str(v), 10.6, MUTE, 800, "end")
        s += rect(650, ey + 18, 460, 9, 4.5, CANVAS, LINE, 1)
        s += rect(650, ey + 18, 460 * v / 130, 9, 4.5, GOLD, "none", 0)

    # personas
    personas = [
        ("Sipho, 29", "Golf 7 GTI · Soweto", "If I tell them about the mods the price doubles. If I don't, I'm not covered. So I just drive carefully.", PURPLE),
        ("Rethabile, 34", "Ranger build · Polokwane", "It works Monday to Friday and climbs on Saturday. I need the canopy and winch named on the schedule.", CYAN),
        ("Dean, 41", "E30 restoration · Cape Town", "Market value is meaningless on a car like this. Give me an agreed value, photos on file, my own repairer.", GOLD),
    ]
    for i, (n, sub, q, c) in enumerate(personas):
        px = 48 + i * 372
        s += rect(px, 398, 356, 196, 14, PAPER, LINE, 1.4)
        s += f'<rect x="{px}" y="398" width="356" height="5" rx="2.5" fill="{c}"/>'
        s += f'<circle cx="{px+38}" cy="438" r="20" fill="{c}" opacity=".16"/>'
        s += text(px + 38, 444, n[0], 17, c, 800, "middle")
        s += text(px + 70, 432, n, 13.5, TEXT, 800)
        s += text(px + 70, 449, sub, 10, MUTE, 600)
        body, _ = wrap_text(px + 20, 484, "“" + q + "”", 46, 10.4, MUTE, 600, 14.5)
        s += body
        need = ["Price certainty before declaring", "Named parts on the schedule", "Agreed value, not market value"][i]
        s += rect(px + 20, 556, 316, 26, 7, CANVAS, LINE_2, 1)
        s += text(px + 32, 573, "Job to be done: " + need, 9.6, TEXT, 700)

    s += rect(48, 612, 1104, 62, 12, GOLD_SOFT, GOLD, 1.4)
    s += text(68, 638, "The bet", 12.5, TEXT, 800)
    s += text(68, 660, "If declaring mods made the price go DOWN in some cases — because the car is better maintained — the whole funnel changes. That became the product.", 11.5, MUTE, 600)
    write(P("stance-01-discovery.svg"), svg(W, H, s, title="Stance discovery research"))


# ══════════════════════════════════════════════════════════════════════════
# STANCE 02 — Quote flow + UI
# ══════════════════════════════════════════════════════════════════════════
def stance_flow():
    W, H = 1200, 726
    s = text(48, 52, "From a 27-question form to a 4-minute quote", 23, TEXT, 800)
    s += text(48, 76, "Prototyped in Figma, tested with 11 owners at two car meets on their own phones, outdoors, in daylight.", 12, MUTE, 600)

    # flow rail
    steps = [("Your car", "reg lookup fills 9 fields"), ("Your mods", "visual picker, not free text"),
             ("Your cover", "agreed vs market, side by side"), ("Your price", "monthly, with the mods priced separately")]
    for i, (t, d) in enumerate(steps):
        fx = 48 + i * 282
        s += rect(fx, 112, 258, 78, 12, PAPER, LINE, 1.4)
        s += f'<circle cx="{fx+30}" cy="151" r="16" fill="{GOLD_SOFT}" stroke="{GOLD}" stroke-width="1.4"/>'
        s += text(fx + 30, 156, str(i + 1), 13, GOLD, 800, "middle")
        s += text(fx + 58, 145, t, 12.5, TEXT, 800)
        body, _ = wrap_text(fx + 58, 163, d, 26, 9.8, MUTE, 600, 12)
        s += body
        if i < 3:
            s += arrow(fx + 258, 151, fx + 282, 151, LINE_2, 2)

    # phone: mod picker
    pre, (ox, oy), (iw, ih) = phone(70, 216, 210, 440)
    s += pre
    s += f'<rect x="{ox}" y="{oy}" width="{iw}" height="{ih}" rx="18" fill="#0E0E10"/>'
    s += text(ox + 16, oy + 40, "What's on the car?", 14, "#F2F0EC", 800)
    s += text(ox + 16, oy + 58, "Tap what applies.", 9, "#8E8B85", 600)
    mods = [("Exhaust system", True), ("Suspension / coilovers", True), ("ECU remap", False),
            ("Wheels & tyres", True), ("Body kit", False), ("Roll cage", False), ("Turbo upgrade", False)]
    for i, (m, on) in enumerate(mods):
        my = oy + 78 + i * 40
        s += rect(ox + 14, my, iw - 28, 32, 9, "#17171A" if not on else "#231C08", "#2A2A2E" if not on else GOLD, 1.2)
        s += f'<rect x="{ox+24}" y="{my+9}" width="14" height="14" rx="4" fill="{GOLD if on else "none"}" stroke="{GOLD if on else "#45454A"}" stroke-width="1.6"/>'
        if on:
            s += f'<path d="M{ox+27} {my+16} l3 3 l5 -6" stroke="#17140F" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
        s += text(ox + 46, my + 21, m, 9.6, "#EDEBE6" if on else "#A8A5A0", 700)
    s += rect(ox + 14, oy + 366, iw - 28, 36, 9, GOLD, "none", 0)
    s += text(ox + iw / 2, oy + 389, "3 selected · continue", 10, "#17140F", 800, "middle")
    body, _ = wrap_text(70, 680, "Step 2 — a picker, because owners could not spell what they had fitted.", 30, 10.2, MUTE, 600, 14)
    s += body

    # phone: quote
    pre, (ox, oy), (iw, ih) = phone(330, 216, 210, 440)
    s += pre
    s += f'<rect x="{ox}" y="{oy}" width="{iw}" height="{ih}" rx="18" fill="#0E0E10"/>'
    s += text(ox + 16, oy + 40, "Your quote", 14, "#F2F0EC", 800)
    s += rect(ox + 14, oy + 54, iw - 28, 78, 12, "#231C08", GOLD, 1.4)
    s += text(ox + 28, oy + 84, "R1 184", 26, GOLD, 800)
    s += text(ox + 28, oy + 102, "per month · agreed value R385 000", 7.8, "#C9C2B0", 600)
    s += text(ox + 28, oy + 120, "Mods covered: R48 000", 8.6, "#8FCFA8", 700)
    lines2 = [("Vehicle cover", "R 942"), ("Declared mods", "R 186"), ("Track-day add-on", "R 56"), ("Excess R6 500", "included")]
    for i, (a, b) in enumerate(lines2):
        ly = oy + 148 + i * 30
        s += text(ox + 20, ly + 14, a, 9.6, "#B7B3AC", 600)
        s += text(ox + iw - 20, ly + 14, b, 9.6, "#EDEBE6", 800, "end")
        s += f'<line x1="{ox+20}" y1="{ly+22}" x2="{ox+iw-20}" y2="{ly+22}" stroke="#232326" stroke-width="1"/>'
    s += rect(ox + 14, oy + 282, iw - 28, 54, 10, "#12211A", "#2C5A44", 1.2)
    s += text(ox + 26, oy + 300, "Declaring your mods saved you", 8.2, "#8FCFA8", 700)
    s += text(ox + 26, oy + 317, "R214 a month against an", 8.6, "#DCEFE4", 800)
    s += text(ox + 26, oy + 330, "undeclared policy.", 8.6, "#DCEFE4", 800)
    s += rect(ox + 14, oy + 348, iw - 28, 36, 9, GOLD, "none", 0)
    s += text(ox + iw / 2, oy + 371, "Accept and upload photos", 9.4, "#17140F", 800, "middle")
    body, _ = wrap_text(330, 680, "Step 4 — the number that made the strategy true, on screen.", 30, 10.2, MUTE, 600, 14)
    s += body

    # decisions panel
    s += rect(600, 216, 552, 440, 14, PAPER, LINE, 1.4)
    s += text(622, 246, "Four decisions and why", 14, TEXT, 800)
    dec = [
        ("Reg lookup first", "Nine fields disappear. Owners could not remember their engine code and would not go outside to check.", GOOD),
        ("Mods as a picker", "Free text produced 340 spellings of “coilovers”. A picker made the data usable for underwriting too."),
        ("Agreed value shown next to market value", "The single biggest trust lever in testing. 9 of 11 chose agreed value once they could compare."),
        ("Price the mods separately", "It proves the promise. Hiding it in one number made people assume they were being penalised."),
    ]
    yy = 272
    for i, item in enumerate(dec):
        t, d = item[0], item[1]
        s += rect(622, yy, 508, 88, 11, CANVAS, LINE_2, 1.2)
        s += f'<rect x="622" y="{yy}" width="4" height="88" rx="2" fill="{[GOOD, CYAN, PURPLE, GOLD][i]}"/>'
        s += text(640, yy + 24, t, 11.8, TEXT, 800)
        body, _ = wrap_text(640, yy + 44, d, 62, 10, MUTE, 600, 13)
        s += body
        yy += 96
    write(P("stance-02-flow.svg"), svg(W, H, s, title="Stance quote flow and interface decisions"))


# ══════════════════════════════════════════════════════════════════════════
# STANCE 03 — Design system / brand kit
# ══════════════════════════════════════════════════════════════════════════
def stance_kit():
    W, H = 1200, 656
    s = text(48, 52, "The kit that made it shippable", 23, TEXT, 800)
    s += text(48, 76, "A small system, on purpose: 9 colours, 6 type sizes, 14 components. Everything else is a combination.", 12, MUTE, 600)

    # colour
    s += rect(48, 112, 350, 268, 14, PAPER, LINE, 1.4)
    s += text(70, 140, "Colour — 9 roles, not 40 swatches", 12, TEXT, 800)
    swatches = [("#0E0E10", "surface/base"), ("#17171A", "surface/raised"), ("#F0A500", "accent/primary"),
                ("#8FCFA8", "status/positive"), ("#E0644F", "status/negative"), ("#F2F0EC", "text/high"),
                ("#A8A5A0", "text/low"), ("#2A2A2E", "border/default"), ("#231C08", "accent/wash")]
    for i, (hexv, name) in enumerate(swatches):
        sx, sy = 70 + (i % 3) * 112, 160 + (i // 3) * 62
        s += rect(sx, sy, 98, 34, 8, hexv, LINE, 1)
        s += text(sx, sy + 46, name, 8.4, MUTE, 700)
        s += text(sx, sy + 56, hexv, 8, MUTE, 500, font=MONO)

    # type
    s += rect(418, 112, 350, 268, 14, PAPER, LINE, 1.4)
    s += text(440, 140, "Type — one family, 6 steps", 12, TEXT, 800)
    ramp = [("Display", 26, 800), ("H1", 20, 800), ("H2", 16, 800), ("Body", 12.5, 500), ("Small", 10.5, 500), ("Micro", 9, 700)]
    yy = 172
    for n, sz, wt in ramp:
        s += text(440, yy + sz * 0.34, "Aa", sz, TEXT, wt)
        s += text(500, yy + sz * 0.34, n, 10, MUTE, 700)
        s += text(740, yy + sz * 0.34, f"{sz*1.6:.0f}/{sz*1.6*1.4:.0f}", 9, MUTE, 600, "end", font=MONO)
        yy += sz * 0.9 + 16

    # components
    s += rect(788, 112, 364, 268, 14, PAPER, LINE, 1.4)
    s += text(810, 140, "14 components, every state drawn", 12, TEXT, 800)
    comps = ["Button", "Input", "Select", "Checkbox", "Card", "Chip", "Stepper", "Price row",
             "Alert", "Sheet", "Tabs", "Empty", "Skeleton", "Toast"]
    for i, c in enumerate(comps):
        cx, cy = 810 + (i % 3) * 112, 158 + (i // 3) * 38
        s += rect(cx, cy, 100, 28, 7, CANVAS, LINE_2, 1)
        s += text(cx + 50, cy + 18, c, 9.4, MUTE, 700, "middle")
    s += text(810, 362, "Each with default / hover / focus / disabled / error", 9.4, MUTE, 600)

    # states row
    s += rect(48, 400, 1104, 148, 14, PAPER, LINE, 1.4)
    s += text(70, 428, "The states nobody asks for, drawn anyway", 12.5, TEXT, 800)
    states = [("Default", "#17171A", GOLD), ("Loading", "#17171A", LINE_2), ("Empty", "#17171A", MUTE),
              ("Error", "#2A1512", FIRE), ("Offline", "#1A1A12", GOLD), ("200% text", "#17171A", CYAN)]
    for i, (n, bg, ac) in enumerate(states):
        bx = 70 + i * 178
        s += rect(bx, 446, 162, 78, 10, bg, "#2A2A2E", 1.2)
        if n == "Loading":
            for k in range(3):
                s += rect(bx + 14, 462 + k * 18, 134 - k * 30, 9, 4.5, "#26262A", "none", 0)
        elif n == "Empty":
            s += f'<circle cx="{bx+81}" cy="478" r="14" fill="none" stroke="#3A3A3E" stroke-width="2"/>'
            s += text(bx + 81, 508, "Nothing here yet", 8.6, "#8E8B85", 600, "middle")
        elif n == "Error":
            s += text(bx + 14, 470, "Could not price this", 9.4, "#F0A18C", 800)
            s += text(bx + 14, 486, "Retry, or call us", 8.6, "#C08E80", 600)
            s += rect(bx + 14, 494, 52, 20, 5, FIRE, "none", 0)
            s += text(bx + 40, 508, "Retry", 8.4, "#FFF", 800, "middle")
        elif n == "Offline":
            s += rect(bx + 14, 458, 134, 20, 5, "#3A2F0C", "none", 0)
            s += text(bx + 22, 472, "Saved. Sends when online.", 8, GOLD, 700)
            s += rect(bx + 14, 486, 100, 26, 6, "#26262A", "none", 0)
        elif n == "200% text":
            s += text(bx + 14, 474, "Your quote", 15, "#F2F0EC", 800)
            s += text(bx + 14, 498, "R1 184 pm", 15, GOLD, 800)
        else:
            s += rect(bx + 14, 458, 134, 22, 6, "#231C08", "none", 0)
            s += text(bx + 22, 473, "Get my quote", 9, GOLD, 800)
            s += rect(bx + 14, 488, 134, 24, 6, "#26262A", "none", 0)
            s += text(bx + 22, 504, "Registration", 8.6, "#8E8B85", 600)
        s += text(bx, 440, n.upper(), 9, ac, 800, ls=0.8)

    s += rect(48, 568, 1104, 62, 12, CANVAS, LINE, 1.4)
    s += text(68, 594, "Why so small?", 12, TEXT, 800)
    s += text(178, 594, "Two developers, ten weeks, one designer. A system you cannot maintain is a system that drifts by month three.", 11.5, MUTE, 600)
    s += text(68, 616, "Handed over as a Figma library plus a one-page README in the repo — the part people actually read.", 10.5, MUTE, 600)
    write(P("stance-03-kit.svg"), svg(W, H, s, title="Stance interface kit"))


if __name__ == "__main__":
    engage_research(); engage_journey(); engage_ia(); engage_wireframes(); engage_ui(); engage_results()
    tobi_audit(); tobi_blueprint(); tobi_flow(); tobi_form()
    stance_discovery(); stance_flow(); stance_kit()
