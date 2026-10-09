"""Rebuild every profile SVG in assets/ (light + dark).

    python3 scripts/build_assets.py

header   name, role and thesis, with a play-once reveal
link-*   LinkedIn / email / ORCID buttons under the header
card-*   featured work, a 2x2 table in the README; each card has a small looping drawing
repo-*   public repositories, linked from the README
stack    one scrolling strip of chips per layer

All motion sits inside `prefers-reduced-motion: no-preference`, and the base styles are the
finished frame, so viewers who asked for less motion get a complete, still picture.
Icons: Simple Icons (CC0), fetched from jsDelivr at a pinned version.
"""
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
ICONS_URL = "https://cdn.jsdelivr.net/npm/simple-icons@16.30.0/icons/{}.svg"
PATH_OK = re.compile(r"^[MmLlHhVvCcSsQqTtAaZzEe0-9.,\s+-]+$")
SANS = '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif'
MONO = 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace'
EASE = "cubic-bezier(.16, 1, .3, 1)"
W = 820

THEMES = {
    "light": dict(fg="#1f2328", text="#1f2328", muted="#59636e", line="#d1d9e0", surface="#f6f8fa",
                  accent="#5b47e0", bg="#ffffff"),
    "dark": dict(fg="#f0f6fc", text="#d1d7e0", muted="#9198a1", line="#3d444d", surface="#151b23",
                 accent="#a594ff", bg="#0d1117"),
}


def svg(w, h, label, t, css, anim, body):
    """Shared shell: theme colors as CSS variables, plus .fade/.rise entrances."""
    tokens = " ".join(f"--{k}: {v};" for k, v in t.items())
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(label, {'"': '&quot;'})}">
<title>{escape(label)}</title>
<style>
  svg {{ {tokens} }}
  .sans {{ font-family: {SANS}; }}
  .mono {{ font-family: {MONO}; }}
  .fg {{ fill: var(--fg); }} .tx {{ fill: var(--text); }} .mu {{ fill: var(--muted); }} .ac {{ fill: var(--accent); }}
  .frame {{ fill: none; stroke: var(--line); }}
{css}
  @media (prefers-reduced-motion: no-preference) {{
    @keyframes fade {{ from {{ opacity: 0; }} }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} }}
    .fade {{ animation: fade .8s ease-out both; }}
    .rise {{ animation: rise .9s {EASE} both; }}
{anim}
  }}
</style>
{body}
</svg>
'''


# ---------------------------------------------------------------- header

def header(t):
    l1, l2, rule, s1, s2, H = 106, 214, 254, 304, 344, 362  # baselines, height
    css = f'''  .name {{ font-size: 112px; font-weight: 700; letter-spacing: -4px; fill: var(--fg); }}
  .meta {{ font-size: 17px; letter-spacing: 1.5px; fill: var(--muted); }}
  .thesis {{ font-size: 31px; font-weight: 500; letter-spacing: -.4px; fill: var(--fg); }}
  .thesis.soft {{ fill: var(--muted); font-weight: 400; }}
  .hair {{ fill: none; stroke: var(--line); stroke-width: 1.25; }}
  .lead {{ fill: none; stroke: var(--accent); stroke-width: 3; }}
  @media (max-width: 560px) {{ .meta {{ font-size: 25px; letter-spacing: 0; }} .thesis {{ font-size: 36px; }} }}'''
    anim = '''    .up { animation: up 1.2s cubic-bezier(.16, 1, .3, 1) both; }
    .up.small { animation-name: up-small; animation-duration: 1s; }
    .slide { animation: slide .9s ease-out both; }
    .draw { animation: draw 1.4s cubic-bezier(.65, 0, .35, 1) both; }
    .lead { animation-duration: .8s; }
    .a1 { animation-delay: .05s; } .a2 { animation-delay: .19s; } .a3 { animation-delay: .55s; }
    .a4 { animation-delay: .8s; } .a5 { animation-delay: .92s; } .a6 { animation-delay: .95s; } .a7 { animation-delay: 1.07s; }
    @keyframes up { from { transform: translateY(124px); } }
    @keyframes up-small { from { transform: translateY(44px); } }
    @keyframes slide { from { opacity: 0; transform: translateX(-8px); } }
    @keyframes draw { from { stroke-dashoffset: 1; } }'''
    body = f'''<defs>
  <clipPath id="c1"><rect x="0" y="0" width="{W}" height="{l1 + 22}"/></clipPath>
  <clipPath id="c2"><rect x="0" y="{l2 - 104}" width="{W}" height="126"/></clipPath>
  <clipPath id="c3"><rect x="0" y="{s1 - 32}" width="{W}" height="42"/></clipPath>
  <clipPath id="c4"><rect x="0" y="{s2 - 32}" width="{W}" height="42"/></clipPath>
</defs>
<g class="sans" clip-path="url(#c1)"><text class="name up a1" x="-4" y="{l1}">Péricles</text></g>
<g class="sans" clip-path="url(#c2)"><text class="name up a2" x="-4" y="{l2}">Feitoza<tspan class="ac">.</tspan></text></g>
<g class="mono meta" text-anchor="end">
  <text class="slide a4" x="{W - 1}" y="{l2 - 30}">FULL-STACK DEVELOPER</text>
  <text class="slide a5" x="{W - 1}" y="{l2}">MACEIÓ, BRAZIL</text>
</g>
<path class="hair draw a3" pathLength="1" stroke-dasharray="1" d="M0 {rule}H{W}"/>
<path class="lead draw a3" pathLength="1" stroke-dasharray="1" d="M0 {rule}H96"/>
<g class="sans" clip-path="url(#c3)"><text class="thesis up small a6" x="1" y="{s1}">Software built end to end, in production,</text></g>
<g class="sans" clip-path="url(#c4)"><text class="thesis soft up small a7" x="1" y="{s2}">from the interface to the infrastructure.</text></g>'''
    label = ("Péricles Feitoza, full-stack developer in Maceió, Brazil. "
             "Software built end to end, in production, from the interface to the infrastructure.")
    return svg(W, H, label, t, css, anim, body)


# ---------------------------------------------------------------- link buttons (under the header)

LINKS = [  # (name, glyph source pinned on jsDelivr, attribution kept in the SVG)
    ("linkedin", "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.7.2/svgs/brands/linkedin-in.svg",
     "LinkedIn glyph: Font Awesome Free 6.7.2, CC BY 4.0, https://fontawesome.com/license/free"),
    ("email", "https://cdn.jsdelivr.net/npm/@primer/octicons@19.36.0/build/svg/mail-24.svg",
     "Mail glyph: GitHub Octicons 19.36.0, MIT"),
    ("orcid", "https://cdn.jsdelivr.net/npm/simple-icons@16.30.0/icons/orcid.svg",
     "ORCID glyph: Simple Icons 16.30.0, CC0"),
]


def glyph(url):
    """(viewBox width, height, path data) of a single-path icon."""
    with urllib.request.urlopen(url, timeout=20) as r:
        s = r.read().decode()
    _, _, w, h = map(float, re.search(r'viewBox="([^"]+)"', s).group(1).split())
    d = re.search(r'\bd="([^"]+)"', s).group(1)
    if not PATH_OK.match(d):
        raise ValueError(f"unexpected path data in {url}")
    return w, h, d


def link_button(t, i, name, w, h, d, credit):
    S, G = 40, 20  # button size, glyph box
    k = G / max(w, h)
    body = (f'<!-- {credit} -->\n<g class="in">'
            f'<rect class="btn" x=".5" y=".5" width="{S - 1}" height="{S - 1}" rx="10"/>'
            f'<path class="ac" transform="translate({(S - w * k) / 2:.2f} {(S - h * k) / 2:.2f}) scale({k:.4f})" d="{d}"/></g>')
    css = "  .btn { fill: var(--surface); stroke: var(--line); stroke-width: 1; }"
    anim = f"    .in {{ animation: rise .9s {EASE} {1.1 + i * .12:.2f}s both; }}"  # lands right after the header reveal
    return svg(S, S, name, t, css, anim, body)


# ---------------------------------------------------------------- featured-work cards

CW, CH = 360, 258
CARDS = [
    dict(id="meuhub", tag="OWN PRODUCT", meta="LIVE", title="MeuHub", link=True, art="order",
         lines=["Link-in-bio storefront for Instagram", "and WhatsApp sellers. Customers pick",
                "size or flavor; the order lands in", "WhatsApp, ready-made."],
         chips=["React", "Express", "PostgreSQL", "Docker"]),
    dict(id="games", tag="ASSISTIVE TECH", meta="3 GAMES", title="Assistive games", link=True, art="tangram",
         lines=["TEAGRAM (math), MEMOAUT (memory) and", "AUTMoney (money skills), tested with",
                "autistic users and therapists; in-game", "telemetry feeds a KPI dashboard."],
         chips=["React Native", "Expo", "Lua", "Defold"]),
    dict(id="delivery", tag="DELIVERY", meta="END TO END", title="Delivery platform", link=False, art="receipt",
         lines=["Web app, API, Electron print terminal,", "WhatsApp AI agent, payment and iFood",
                "integrations. I built nearly all of it", "in ~8 months, left tested and sellable."],
         chips=["Next.js", "Electron", "RabbitMQ", "Oracle"]),
    dict(id="escavador", tag="PERSONAL", meta="PWA", title="Escavador de Preços", link=False, art="price",
         lines=["Price tracker that scrapes dozens of", "Brazilian stores, matches the same",
                "product across retailers and alerts", "only on genuine price drops."],
         chips=["Django", "Playwright", "React", "Web Push"]),
]


def tangram():
    """Classic 7-piece tangram in a 44x44 square; one small triangle slides into place."""
    s = 44
    pieces = [[(0, 0), (1, 0), (.5, .5)], [(0, 0), (.5, .5), (0, 1)], [(1, 1), (.5, 1), (1, .5)],
              [(.5, .5), (.75, .25), (.75, .75)], [(.5, .5), (.75, .75), (.5, 1), (.25, .75)],
              [(1, 0), (1, .5), (.75, .75), (.75, .25)], [(0, 1), (.25, .75), (.5, 1)]]
    pts = lambda p: " ".join(f"{x * s:.1f},{y * s:.1f}" for x, y in p)
    out = "".join(f'<polygon class="tg" points="{pts(p)}"/>' for p in pieces[:-1])
    return out + f'<polygon class="tg-on piece" points="{pts(pieces[-1])}"/>'


def art(kind):
    """~100x44 drawing for the card's header band (origin top-left) and its looping motion."""
    if kind == "order":  # pick an option, the order pops up as a chat message
        opts = "".join(f'<rect class="opt" x="{i * 26}" y="0" width="22" height="16" rx="5"/>' for i in range(3))
        return (opts + '<rect class="opt-on pick" x="26" y="0" width="22" height="16" rx="5"/>'
                '<path class="aline" d="M37 20 V27"/>'
                '<g class="bubble"><path class="bub" d="M30 28 H94 a6 6 0 0 1 6 6 V40 a6 6 0 0 1 -6 6 H40 l-6 4 v-4 h-4 '
                'a6 6 0 0 1 -6 -6 V34 a6 6 0 0 1 6 -6 Z"/>'
                '<rect class="aline-f" x="32" y="34.5" width="40" height="3" rx="1.5"/>'
                '<rect class="aline-f" x="32" y="40" width="26" height="3" rx="1.5"/>'
                '<path class="chk" d="M80 37.5 l2.6 2.6 l5 -5.4"/></g>',
                "@keyframes pick { 0%, 10% { transform: translateX(-26px); } 22%, 100% { transform: translateX(0); } }"
                "@keyframes bubble { 0%, 28% { opacity: 0; transform: translateY(5px); } 36%, 90% { opacity: 1; transform: translateY(0); } 97%, 100% { opacity: 0; } }"
                ".pick { animation: pick 8s cubic-bezier(.5, 0, .2, 1) infinite; }"
                ".bubble { animation: bubble 8s ease-out infinite; }")
    if kind == "tangram":
        return (f'<g transform="translate(56 0)">{tangram()}</g>',
                "@keyframes place { 0%, 12% { transform: translate(-30px, -6px) rotate(-90deg); opacity: .4; }"
                " 40%, 100% { transform: none; opacity: 1; } }"
                ".piece { transform-box: fill-box; transform-origin: center; animation: place 8s cubic-bezier(.4, 0, .2, 1) infinite alternate; }")
    if kind == "receipt":  # a ticket prints out of the terminal
        lines = "".join(f'<rect class="aline-f" x="60" y="{14 + i * 7}" width="{[26, 18, 22][i]}" height="2.5" rx="1.25"/>'
                        for i in range(3))
        return ('<clipPath id="slot"><rect x="40" y="6" width="60" height="40"/></clipPath>'
                '<rect class="opt" x="44" y="0" width="56" height="8" rx="3"/>'
                f'<g clip-path="url(#slot)"><g class="paper"><path class="bub" d="M54 6 H92 V40 l-4.75 3 l-4.75 -3 l-4.75 3 l-4.75 -3 '
                f'l-4.75 3 l-4.75 -3 l-4.75 3 l-4.75 -3 Z"/>{lines}<path class="chk" d="M80 31 l2.3 2.3 l4.2 -4.6"/></g></g>'
                '<circle class="adot led" cx="94" cy="4" r="1.6"/>',
                "@keyframes paper { 0%, 8% { transform: translateY(-36px); } 45%, 88% { transform: translateY(0); } 96%, 100% { transform: translateY(-36px); } }"
                "@keyframes led { 0%, 8%, 45%, 100% { opacity: 1; } 20%, 32% { opacity: .2; } }"
                ".paper { animation: paper 8s cubic-bezier(.4, 0, .3, 1) infinite; } .led { animation: led 8s linear infinite; }")
    if kind == "price":  # price steps along, then a real drop gets flagged
        return ('<path class="aline" d="M0 14 H16 V10 H36 V15 H56 V11 H72"/><path class="aacc drop" pathLength="100" d="M72 11 V34 H100"/>'
                '<circle class="halo2" cx="100" cy="34" r="3"/><circle class="adot" cx="100" cy="34" r="3"/>'
                '<path class="aline" d="M0 44 H100" stroke-dasharray="2 4"/>',
                "@keyframes drop { 0%, 30% { stroke-dashoffset: 100; } 55%, 100% { stroke-dashoffset: 0; } }"
                "@keyframes ping { 0%, 55% { opacity: 0; transform: scale(1); } 60% { opacity: .8; } 85%, 100% { opacity: 0; transform: scale(3); } }"
                ".drop { stroke-dasharray: 100 100; animation: drop 8s ease-in-out infinite; }"
                ".halo2 { transform-box: fill-box; transform-origin: center; animation: ping 8s ease-out infinite; }")
    raise ValueError(kind)


def card(t, c):
    drawing, motion = art(c["art"])
    css = '''  text { dominant-baseline: central; }
  .card { fill: var(--surface); stroke: var(--line); stroke-width: 1; }
  .tag { font-size: 12px; letter-spacing: .6px; fill: var(--accent); font-weight: 600; }
  .meta { font-size: 12px; letter-spacing: .6px; fill: var(--muted); }
  .title { font-size: 25px; font-weight: 650; letter-spacing: -.4px; fill: var(--fg); }
  .desc { font-size: 16px; fill: var(--muted); }
  .chip { fill: var(--bg); stroke: var(--line); stroke-width: 1; }
  .chipt { font-size: 12.5px; fill: var(--text); }
  .go { fill: none; stroke: var(--accent); stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
  .aline { fill: none; stroke: var(--line); stroke-width: 1.5; stroke-linejoin: round; stroke-linecap: round; }
  .aline-f { fill: var(--line); }
  .aacc { fill: none; stroke: var(--accent); stroke-width: 2; stroke-linejoin: round; stroke-linecap: round; }
  .adot { fill: var(--accent); }
  .halo2 { fill: none; stroke: var(--accent); stroke-width: 1.2; opacity: 0; }
  .opt { fill: var(--bg); stroke: var(--line); stroke-width: 1; }
  .opt-on { fill: var(--accent); fill-opacity: .14; stroke: var(--accent); stroke-width: 1.25; }
  .bub { fill: var(--bg); stroke: var(--line); stroke-width: 1; }
  .chk { fill: none; stroke: var(--accent); stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
  .tg { fill: var(--bg); stroke: var(--line); stroke-width: 1.25; stroke-linejoin: round; }
  .tg-on { fill: var(--accent); fill-opacity: .18; stroke: var(--accent); stroke-width: 1.4; stroke-linejoin: round; }'''
    assert 20 + len(f'{c["tag"]} · {c["meta"]}') * 7.8 < CW - 120 - (20 if c["link"] else 0), f"tag line hits the art on {c['id']}"
    body = [f'<rect class="card" x=".5" y=".5" width="{CW - 1}" height="{CH - 1}" rx="12"/>',
            f'<text class="mono tag" x="20" y="30">{c["tag"]}</text>',
            f'<text class="mono meta" x="{20 + len(c["tag"]) * 7.8 + 4:.1f}" y="30">· {c["meta"]}</text>',
            f'<text class="sans title" x="20" y="88">{escape(c["title"])}</text>']
    if c["link"]:
        body.append(f'<path class="go" d="M{CW - 30} 28 l9 -9 M{CW - 28} 19 H{CW - 21} V26"/>')
    for i, ln in enumerate(c["lines"]):
        assert len(ln) <= 39, f"desc line too long on {c['id']}: {ln!r}"
        body.append(f'<text class="sans desc" x="20" y="{122 + i * 23}">{escape(ln)}</text>')
    x = 20
    for chip in c["chips"]:
        w = len(chip) * 7.5 + 18
        body.append(f'<rect class="chip" x="{x:.1f}" y="{CH - 46}" width="{w:.1f}" height="28" rx="6"/>'
                    f'<text class="mono chipt" x="{x + w / 2:.1f}" y="{CH - 32}" text-anchor="middle">{escape(chip)}</text>')
        x += w + 6
    assert x < CW - 14, f"chips overflow on {c['id']}"
    body.append(f'<g transform="translate({CW - 120 - (22 if c["link"] else 0)} 14)">{drawing}</g>')
    label = f'{c["title"]}: {" ".join(c["lines"])} Stack: {", ".join(c["chips"])}.'
    return svg(CW, CH, label, t, css, motion, "\n".join(body))


# ---------------------------------------------------------------- public repositories

REPOS = [  # (name, description lines, meta)
    ("material_estudos_ifal", ("Study platform for IFAL's Information", "Systems degree, with AI-generated quizzes."),
     ("TypeScript", "★ 29", "live site")),
    ("Pulmoseg", ("Lung-nodule segmentation on CT scans:", "classical vision vs. the U-Net family."), ("Python", "PyTorch")),
    ("AUTMONEY", ("Serious game on money skills: 10 shops,", "40 levels, in-game telemetry."), ("Lua", "Defold")),
    ("test_scan_xlsx", ("Builds printable exams and reads scanned", "answer sheets with OpenCV."), ("Python", "Flask · OpenCV")),
]
REPO_ICON = ("M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8"
             "a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1"
             " 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.25.25 0 0 0-.3 0"
             "L5.4 15.7a.25.25 0 0 1-.4-.2Z")  # Octicons repo-16 (MIT)


def repo_card(t, name, desc, meta):
    H = 148
    body = [f'<rect class="frame" x=".5" y=".5" width="399" height="{H - 1}" rx="12"/>',
            f'<path class="mu" transform="translate(24 24)" d="{REPO_ICON}"/>',
            f'<text class="mono ac" x="50" y="37" font-size="17" font-weight="600">{escape(name)}</text>',
            f'<text class="mono mu" x="376" y="37" font-size="17" text-anchor="end">↗</text>']
    body += [f'<text class="sans mu" x="24" y="{72 + 22 * i}" font-size="16">{escape(s)}</text>' for i, s in enumerate(desc)]
    body += [f'<circle class="ac" cx="29" cy="{H - 27}" r="5"/>',
             f'<text class="mono tx" x="42" y="{H - 27}" font-size="13" dominant-baseline="central">{escape("  ·  ".join(meta))}</text>']
    return svg(400, H, f"{name}: {' '.join(desc)} ({', '.join(meta)})", t, "", "", "\n".join(body))


# ---------------------------------------------------------------- stack strip

ROWS = [  # (row label, [(chip, simple-icons slug or None)])
    ("app", [("React", "react"), ("Next.js", "nextdotjs"), ("TypeScript", "typescript"), ("Vite", "vite"),
             ("TanStack", "tanstack"), ("Tailwind CSS", "tailwindcss"), ("shadcn/ui", "shadcnui"), ("Recharts", None),
             ("Leaflet", "leaflet"), ("React Native", "react"), ("Expo", "expo"), ("Electron", "electron"),
             ("Defold", None)]),
    ("api", [("Node.js", "nodedotjs"), ("NestJS", "nestjs"), ("Express", "express"), ("Python", "python"),
             ("Django", "django"), ("FastAPI", "fastapi"), ("Flask", "flask"), ("Laravel", "laravel"), ("Zod", "zod"),
             ("Keycloak", "keycloak"), ("LLM APIs", None), ("MCP", "modelcontextprotocol"), ("PyTorch", "pytorch"),
             ("OpenCV", "opencv")]),
    ("data", [("PostgreSQL", "postgresql"), ("Oracle", None), ("PL/SQL", None), ("MongoDB", "mongodb"),
              ("Redis", "redis"), ("SQLite", "sqlite"), ("Prisma", "prisma"), ("Drizzle", "drizzle"),
              ("RabbitMQ", "rabbitmq")]),
    ("ops", [("Docker", "docker"), ("Kubernetes", "kubernetes"), ("Helm", "helm"), ("GitHub Actions", "githubactions"),
             ("Nginx", "nginx"), ("Cloudflare", "cloudflare"), ("Oracle Cloud", None), ("Prometheus", "prometheus"),
             ("Grafana", "grafana"), ("Loki", None), ("Vitest", "vitest"), ("Jest", "jest"), ("Playwright", None),
             ("pytest", "pytest")]),
]


def stack(t, paths):
    ROW_H, PITCH, X0 = 30, 42, 64
    FONT, PAD, ICON, GAP, SPACE, SPEED = 11.5, 10, 14, 7, 8, 26
    h = PITCH * (len(ROWS) - 1) + ROW_H + 2
    anim, labels, rows, names = [], [], [], []
    for i, (name, items) in enumerate(ROWS):
        names += [label for label, _ in items]
        chips, x = [], 0.0
        for label, slug in items:
            w = PAD + (ICON + GAP if slug else 0) + len(label) * FONT * .6 + PAD
            chips.append((x, w, label, slug))
            x += w + SPACE
        frm, to = (0, -x) if i % 2 == 0 else (-x, 0)  # odd rows run the other way
        anim.append(f"    @keyframes m{i} {{ from {{ transform: translateX({frm:.1f}px); }} to {{ transform: translateX({to:.1f}px); }} }}"
                    f" .r{i} {{ animation: m{i} {x / SPEED:.1f}s linear infinite; }}")
        parts = []
        for offset in (0, x):  # two copies so the loop is seamless
            for cx, w, label, slug in chips:
                cx += offset
                parts.append(f'<rect x="{cx:.1f}" y="0" width="{w:.1f}" height="{ROW_H}" rx="7"/>')
                tx = cx + PAD
                if slug:
                    parts.append(f'<use href="#{slug}" transform="translate({tx:.1f} 8) scale({ICON / 24:.4f})"/>')
                    tx += ICON + GAP
                parts.append(f'<text x="{tx:.1f}" y="{ROW_H / 2:.0f}">{escape(label)}</text>')
        y = 1 + i * PITCH
        labels.append(f'<text class="lbl" x="2" y="{y + ROW_H / 2:.0f}">{name}</text>')
        rows.append(f'<g transform="translate({X0} {y})"><g class="r{i}">{"".join(parts)}</g></g>')
    defs = "".join(f'<path id="{k}" d="{v}"/>' for k, v in paths.items())
    css = f'''  .strip text {{ font-family: {MONO}; font-size: {FONT}px; fill: var(--text); dominant-baseline: central; }}
  .lbl {{ font-family: {MONO}; font-size: 11px; fill: var(--muted); dominant-baseline: central; }}
  .strip rect {{ fill: var(--surface); stroke: var(--line); stroke-width: 1; }}
  use {{ fill: var(--accent); }}'''
    body = f'''<defs>
  <linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#000"/><stop offset=".06" stop-color="#fff"/><stop offset=".94" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>
  <mask id="edges"><rect x="{X0}" y="0" width="{W - X0}" height="{h}" fill="url(#fade)"/></mask>
  {defs}
</defs>
{"".join(labels)}
<g class="strip" mask="url(#edges)">{"".join(rows)}</g>'''
    return svg(W, h, "Stack: " + ", ".join(dict.fromkeys(names)), t, css, "\n".join(anim), body)


# ---------------------------------------------------------------- main

def icon_path(slug):
    with urllib.request.urlopen(ICONS_URL.format(slug), timeout=20) as r:
        d = re.search(r'\bd="([^"]+)"', r.read().decode()).group(1)
    if not PATH_OK.match(d):  # only plain path data goes into the SVG
        raise ValueError(f"unexpected path data for {slug}")
    # one decimal is plenty for 14px icons and halves the file; arcs are left alone because
    # their packed flags ("0 00.186") would be read as numbers
    if not re.search(r"[aA]", d):
        d = re.sub(r"-?\d*\.\d+", lambda m: re.sub(r"^(-?)0\.", r"\1.", f"{float(m.group()):.1f}"), d)
    return slug, d


def main():
    slugs = list(dict.fromkeys(s for _, items in ROWS for _, s in items if s))
    with ThreadPoolExecutor(8) as ex:
        paths = dict(ex.map(icon_path, slugs))
        glyphs = list(ex.map(glyph, [url for _, url, _ in LINKS]))
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    for theme, t in THEMES.items():
        files = {"header": header(t), "stack": stack(t, paths)}
        files.update({f"card-{c['id']}": card(t, c) for c in CARDS})
        files.update({f"repo-{name.lower()}": repo_card(t, name, *rest) for name, *rest in REPOS})
        files.update({f"link-{name}": link_button(t, i, name, *g, credit)
                      for i, ((name, _, credit), g) in enumerate(zip(LINKS, glyphs))})
        for name, text in files.items():
            (OUT / f"{name}-{theme}.svg").write_text(text)
    for f in sorted(OUT.glob("*.svg")):
        print(f"{f.stat().st_size / 1024:6.1f} KB  {f.name}")


if __name__ == "__main__":
    main()
