"""Shared SVG drawing primitives for LulaSync case-study artefacts.

Everything is hand-authored vector: wireframes, journey maps, IA trees,
service blueprints, token graphs and measurement charts. These are the
same artefacts that come out of a real design/engineering process.
"""

from html import escape

# ── Palette (matches assets/case-study.css) ────────────────────────────────
INK = "#0F0D0B"
PAPER = "#FBF7EF"
CANVAS = "#F3EEE4"
LINE = "#D9D1C2"
LINE_2 = "#C3B9A6"
TEXT = "#1A1208"
MUTE = "#7C7060"
GOLD = "#C98A00"
GOLD_SOFT = "#FCEFCB"
FIRE = "#D2461A"
FIRE_SOFT = "#FBE1D6"
GOOD = "#1F8A57"
GOOD_SOFT = "#DAF0E5"
CYAN = "#0C7FA8"
CYAN_SOFT = "#D8EEF6"
PURPLE = "#6A45C4"
PURPLE_SOFT = "#E7DFFA"
STICKY = "#FFE49A"
STICKY_2 = "#CFE9FF"
STICKY_3 = "#FFD3C2"
STICKY_4 = "#D9F5DE"

FONT = "Inter, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'SFMono-Regular', Menlo, monospace"


def esc(t):
    return escape(str(t), quote=True)


def svg(w, h, body, bg=CANVAS, title="", desc=""):
    head = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img" font-family="{FONT}">'
    )
    meta = ""
    if title:
        meta += f"<title>{esc(title)}</title>"
    if desc:
        meta += f"<desc>{esc(desc)}</desc>"
    grid = (
        '<defs><pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
        f'<circle cx="1" cy="1" r="1" fill="{LINE}" opacity=".55"/></pattern>'
        '<filter id="sh" x="-20%" y="-20%" width="140%" height="140%">'
        '<feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#1A1208" flood-opacity=".10"/></filter>'
        '<filter id="sh2" x="-20%" y="-20%" width="140%" height="140%">'
        '<feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#1A1208" flood-opacity=".14"/></filter>'
        "</defs>"
    )
    return (
        head + meta + grid
        + f'<rect width="{w}" height="{h}" fill="{bg}"/>'
        + f'<rect width="{w}" height="{h}" fill="url(#dots)"/>'
        + body
        + "</svg>"
    )


def rect(x, y, w, h, r=10, fill=PAPER, stroke=LINE, sw=1.4, extra=""):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}" {extra}/>'
    )


def text(x, y, t, size=13, fill=TEXT, weight=600, anchor="start", font=FONT, ls=0, op=1):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
        f'text-anchor="{anchor}" font-family="{font}" letter-spacing="{ls}" opacity="{op}">{esc(t)}</text>'
    )


def wrap_text(x, y, t, width_chars, size=12, fill=MUTE, weight=500, lh=16, anchor="start", weight_first=None):
    words, lines, cur = str(t).split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= width_chars:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    out = ""
    for i, ln in enumerate(lines):
        out += text(x, y + i * lh, ln, size, fill, weight_first if (i == 0 and weight_first) else weight, anchor)
    return out, y + len(lines) * lh


def label(x, y, t, fill=MUTE, size=9.5):
    return text(x, y, str(t).upper(), size, fill, 800, ls=1.1)


def chip(x, y, t, fill=GOLD_SOFT, stroke=GOLD, tc=None, size=10, pad=9, h=20):
    w = len(str(t)) * (size * 0.58) + pad * 2
    return (
        rect(x, y, w, h, h / 2, fill, stroke, 1)
        + text(x + w / 2, y + h / 2 + 3.4, t, size, tc or stroke, 800, "middle")
    ), w


def arrow(x1, y1, x2, y2, color=MUTE, sw=1.6, dash=None, head=True):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    s = f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="{sw}" fill="none"{d} stroke-linecap="round"/>'
    if head:
        import math
        a = math.atan2(y2 - y1, x2 - x1)
        L = 7
        p1 = (x2 - L * math.cos(a - 0.42), y2 - L * math.sin(a - 0.42))
        p2 = (x2 - L * math.cos(a + 0.42), y2 - L * math.sin(a + 0.42))
        s += f'<path d="M{x2} {y2} L{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} Z" fill="{color}"/>'
    return s


def curve(pts, color=GOLD, sw=2.6, dash=None, fill="none"):
    if not pts:
        return ""
    d = f"M{pts[0][0]} {pts[0][1]}"
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]
        x1, y1 = pts[i]
        cx = (x0 + x1) / 2
        d += f" C{cx} {y0} {cx} {y1} {x1} {y1}"
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" stroke="{color}" stroke-width="{sw}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round"{da}/>'


def frame_header(x, y, w, name, tag=None, tag_fill=GOLD_SOFT, tag_stroke=GOLD):
    """A Figma-ish frame label above an artboard."""
    s = text(x, y, name, 10.5, MUTE, 800, ls=1)
    if tag:
        c, cw = chip(x + w - 4 - (len(tag) * 5.8 + 18), y - 14, tag, tag_fill, tag_stroke)
        s += c
    return s


def sticky(x, y, w, h, t, fill=STICKY, rot=0, size=11, tc=TEXT, chars=22):
    g = f'<g transform="rotate({rot} {x + w/2} {y + h/2})">'
    g += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}" filter="url(#sh)"/>'
    body, _ = wrap_text(x + 10, y + 20, t, chars, size, tc, 600, size + 4)
    g += body + "</g>"
    return g


def phone(x, y, w=196, h=400, screen_fill="#FFFFFF"):
    """Returns (open_group_prefix, close, inner_origin, inner_size)."""
    bez = 9
    pre = (
        f'<g filter="url(#sh2)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="#17140F"/></g>'
        f'<rect x="{x + bez}" y="{y + bez}" width="{w - 2*bez}" height="{h - 2*bez}" rx="18" fill="{screen_fill}"/>'
        f'<rect x="{x + w/2 - 22}" y="{y + bez + 6}" width="44" height="5" rx="2.5" fill="#E7E2D8"/>'
    )
    return pre, (x + bez, y + bez), (w - 2 * bez, h - 2 * bez)


def browser(x, y, w, h, url="", fill="#FFFFFF"):
    s = f'<g filter="url(#sh2)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#17140F"/></g>'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="12" fill="#221E18"/>'
    s += f'<rect x="{x}" y="{y + 18}" width="{w}" height="14" fill="#221E18"/>'
    for i, c in enumerate(["#E0644F", "#E8B23D", "#5FBE7D"]):
        s += f'<circle cx="{x + 16 + i*14}" cy="{y + 15}" r="4.2" fill="{c}"/>'
    if url:
        s += rect(x + 66, y + 7, min(w - 90, 300), 17, 8.5, "#100E0B", "#332C22", 1)
        s += text(x + 76, y + 19.5, url, 9, "#B9AE9A", 600, font=MONO)
    s += f'<rect x="{x}" y="{y + 30}" width="{w}" height="{h - 30}" fill="{fill}"/>'
    return s, (x, y + 30), (w, h - 30)


def bar_chart(x, y, w, h, series, maxv=None, color=GOLD, color2=None, gap=14, show_val=True, val_fmt="{:.0f}"):
    """series: list of (label, value) or (label, v1, v2) for before/after."""
    maxv = maxv or max(max(s[1:]) for s in series) * 1.18
    n = len(series)
    bw = (w - gap * (n - 1)) / n
    s = f'<line x1="{x}" y1="{y+h}" x2="{x+w}" y2="{y+h}" stroke="{LINE_2}" stroke-width="1.4"/>'
    for i, item in enumerate(series):
        bx = x + i * (bw + gap)
        vals = item[1:]
        sub = bw / len(vals) - (3 if len(vals) > 1 else 0)
        for j, v in enumerate(vals):
            bh = max(3, (v / maxv) * h)
            c = color if j == 0 else (color2 or GOOD)
            s += f'<rect x="{bx + j*(sub+3)}" y="{y + h - bh}" width="{sub}" height="{bh}" rx="4" fill="{c}"/>'
            if show_val:
                s += text(bx + j * (sub + 3) + sub / 2, y + h - bh - 7, val_fmt.format(v), 10.5, c, 800, "middle")
        s += text(bx + bw / 2, y + h + 16, item[0], 10, MUTE, 700, "middle")
    return s


def line_chart(x, y, w, h, pts, color=GOLD, labels=None, fill_area=True, dot=True):
    n = len(pts)
    mx = max(pts) * 1.15 or 1
    coords = [(x + i * (w / (n - 1)), y + h - (v / mx) * h) for i, v in enumerate(pts)]
    s = ""
    if fill_area:
        d = f"M{coords[0][0]} {y+h} " + " ".join(f"L{cx:.1f} {cy:.1f}" for cx, cy in coords) + f" L{coords[-1][0]} {y+h} Z"
        s += f'<path d="{d}" fill="{color}" opacity=".10"/>'
    s += curve(coords, color, 2.4)
    if dot:
        for cx, cy in coords:
            s += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.6" fill="{PAPER}" stroke="{color}" stroke-width="2.2"/>'
    if labels:
        for i, l in enumerate(labels):
            s += text(coords[i][0], y + h + 16, l, 9.5, MUTE, 700, "middle")
    return s


def gauge(cx, cy, r, value, color=GOOD, cap="", sub=""):
    import math
    circ = 2 * math.pi * r
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="8"/>'
    s += (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="8" '
        f'stroke-linecap="round" stroke-dasharray="{circ*value/100:.1f} {circ:.1f}" '
        f'transform="rotate(-90 {cx} {cy})"/>'
    )
    s += text(cx, cy + 7, cap or str(value), 22, TEXT, 800, "middle")
    if sub:
        s += text(cx, cy + r + 20, sub, 10, MUTE, 700, "middle")
    return s


def wire_block(x, y, w, h, kind="box", fill="#EFEAE0", stroke=LINE_2):
    """Low-fidelity wireframe primitives."""
    if kind == "img":
        s = rect(x, y, w, h, 6, fill, stroke, 1.2)
        s += f'<path d="M{x} {y+h} L{x+w*0.36} {y+h*0.42} L{x+w*0.62} {y+h*0.72} L{x+w*0.8} {y+h*0.55} L{x+w} {y+h} Z" fill="{LINE_2}" opacity=".55"/>'
        s += f'<circle cx="{x+w*0.76}" cy="{y+h*0.26}" r="{min(w,h)*0.09}" fill="{LINE_2}" opacity=".7"/>'
        return s
    if kind == "line":
        return rect(x, y, w, h, h / 2, LINE_2, "none", 0, 'opacity=".45"')
    if kind == "btn":
        return rect(x, y, w, h, 7, LINE_2, "none", 0, 'opacity=".85"')
    return rect(x, y, w, h, 8, fill, stroke, 1.2)


def annot(x, y, t, n=None, color=FIRE, side="left", chars=30, size=10.5):
    """Red-pen annotation used on wireframes and audits."""
    s = ""
    if n is not None:
        s += f'<circle cx="{x}" cy="{y}" r="9" fill="{color}"/>'
        s += text(x, y + 3.6, n, 10, "#FFF", 800, "middle")
        tx = x + 15 if side == "left" else x - 15
    else:
        tx = x
    body, _ = wrap_text(tx, y + 4, t, chars, size, color, 700, size + 3, "start" if side == "left" else "end")
    return s + body


def swimlane(x, y, w, rows, col_labels, row_h=54, head_h=30, lane_fill=PAPER):
    """rows: list of (lane_name, [cell_text_per_col]) ; returns svg string."""
    ncol = len(col_labels)
    lw = 132
    cw = (w - lw) / ncol
    s = rect(x, y, w, head_h + row_h * len(rows), 12, PAPER, LINE, 1.4)
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{head_h}" rx="12" fill="{CANVAS}"/>'
    s += f'<rect x="{x}" y="{y+head_h-12}" width="{w}" height="12" fill="{CANVAS}"/>'
    for i, c in enumerate(col_labels):
        s += text(x + lw + i * cw + cw / 2, y + head_h / 2 + 4, c.upper(), 9.5, MUTE, 800, "middle", ls=1)
        if i:
            s += f'<line x1="{x+lw+i*cw}" y1="{y}" x2="{x+lw+i*cw}" y2="{y+head_h+row_h*len(rows)}" stroke="{LINE}" stroke-width="1"/>'
    s += f'<line x1="{x+lw}" y1="{y}" x2="{x+lw}" y2="{y+head_h+row_h*len(rows)}" stroke="{LINE}" stroke-width="1.2"/>'
    for r, (name, cells) in enumerate(rows):
        ry = y + head_h + r * row_h
        if r:
            s += f'<line x1="{x}" y1="{ry}" x2="{x+w}" y2="{ry}" stroke="{LINE}" stroke-width="1"/>'
        s += text(x + 14, ry + row_h / 2 + 4, name, 10.5, TEXT, 800)
        for i, cell in enumerate(cells):
            if not cell:
                continue
            cx0 = x + lw + i * cw + 8
            body, _ = wrap_text(cx0, ry + 20, cell, max(12, int(cw / 6.3)), 9.4, MUTE, 600, 12.5)
            s += body
    return s


def kpi_tile(x, y, w, h, big, small, color=GOLD, fill=PAPER):
    s = rect(x, y, w, h, 12, fill, LINE, 1.4)
    s += text(x + w / 2, y + h / 2 + 2, big, min(26, w / (len(str(big)) * 0.62)), color, 800, "middle")
    s += text(x + w / 2, y + h - 12, small, 9.5, MUTE, 700, "middle")
    return s


def face(cx, cy, mood, color=FIRE, r=13, bg=PAPER):
    """Drawn emotion face (0 = miserable .. 4 = happy). No emoji fonts needed."""
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}" stroke="{color}" stroke-width="2.2"/>'
    ex = r * 0.34
    s += f'<circle cx="{cx-ex}" cy="{cy-r*0.18}" r="1.7" fill="{color}"/>'
    s += f'<circle cx="{cx+ex}" cy="{cy-r*0.18}" r="1.7" fill="{color}"/>'
    curveness = (mood - 2) / 2.0          # -1 sad .. +1 happy
    mw = r * 0.52
    my = cy + r * 0.30
    cy2 = my + curveness * r * 0.42
    s += (f'<path d="M{cx-mw} {my} Q{cx} {cy2} {cx+mw} {my}" stroke="{color}" '
          f'stroke-width="2" fill="none" stroke-linecap="round"/>')
    return s


def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path, len(content))
