#!/usr/bin/env python3
"""The three frontend engineering case studies."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from shell import *  # noqa

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
A = "assets/cs/"

DEMO_BOARD = '''<div class="demo" id="swBoard" data-segs>
        <div class="demo-bar">
          <span class="tag">Live component</span>
          <div class="seg" role="group" aria-label="Force a state">
            <button type="button" class="on" data-seg="fresh">Fresh</button>
            <button type="button" data-seg="stale">Stale</button>
            <button type="button" data-seg="offline">Offline</button>
            <button type="button" data-seg="partial">Partial</button>
            <button type="button" data-seg="loading">Loading</button>
            <button type="button" data-seg="empty">Empty</button>
          </div>
          <span class="hint">Force any state &mdash; the component decides the rest</span>
        </div>
        <div class="demo-body">
          <div class="board">
            <div class="board-head">
              <b>Midrand, Gauteng</b>
              <span id="swBadge" style="font-size:.66rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase">live</span>
            </div>
            <div id="swBody"></div>
            <p class="board-note" id="swNote"></p>
          </div>
        </div>
      </div>'''

DEMO_TOKENS = '''<div class="demo" id="tokenPlay">
        <div class="demo-bar">
          <span class="tag">Token playground</span>
          <span class="hint">Change a token, watch every component follow</span>
        </div>
        <div class="demo-body">
          <div class="play">
            <div class="play-ctl">
              <span class="ctl-label">action.primary</span>
              <div class="swatches" id="tAccent">
                <button type="button" class="on" data-colour="#F0A500" aria-label="Amber"></button>
                <button type="button" data-colour="#00C2FF" aria-label="Cyan"></button>
                <button type="button" data-colour="#8B5CF6" aria-label="Purple"></button>
                <button type="button" data-colour="#2FBF71" aria-label="Green"></button>
                <button type="button" data-colour="#E04E14" aria-label="Fire"></button>
              </div>
              <label class="ctl-label" for="tRadius">radius.md</label>
              <input type="range" id="tRadius" min="0" max="26" value="10" />
              <label class="ctl-label" for="tSpace">space.md</label>
              <input type="range" id="tSpace" min="8" max="32" value="16" />
              <p class="play-code"></p>
            </div>
            <div class="play-out">
              <button class="pv-btn" type="button">Primary action</button>
              <span class="pv-chip" style="margin-left:10px">Badge</span>
              <div class="pv-card">
                <p style="font-size:.9rem;font-weight:800;margin-bottom:6px">Card component</p>
                <p style="font-size:.82rem;color:var(--dim);line-height:1.6">Nothing in this card knows what colour it
                  is. It asks for <code>button.bg.rest</code>, which asks for <code>action.primary</code>.</p>
              </div>
              <div class="pv-card">
                <p style="font-size:.82rem;color:var(--dim);line-height:1.6">Second instance, same tokens. In the real
                  system this is 80+ components across four products.</p>
              </div>
            </div>
          </div>
        </div>
      </div>'''

DEMO_VITALS = '''<div class="demo" id="liveVitals">
        <div class="demo-bar">
          <span class="tag">Measuring this page, right now</span>
          <span class="hint">Read from the Performance API in your browser</span>
        </div>
        <div class="demo-body">
          <div class="vitals">
            <div class="vital" id="vTTFB"><p class="k">Time to first byte</p>
              <p class="v">&mdash;</p>
              <p class="s">good under 200 ms</p>
            </div>
            <div class="vital" id="vFCP"><p class="k">First contentful paint</p>
              <p class="v">&mdash;</p>
              <p class="s">good under 1.8 s</p>
            </div>
            <div class="vital" id="vLCP"><p class="k">Largest contentful paint</p>
              <p class="v">&mdash;</p>
              <p class="s">good under 2.5 s</p>
            </div>
            <div class="vital" id="vCLS"><p class="k">Cumulative layout shift</p>
              <p class="v">&mdash;</p>
              <p class="s">good under 0.1</p>
            </div>
            <div class="vital" id="vWeight"><p class="k">Transferred</p>
              <p class="v">&mdash;</p>
              <p class="s">budget 400 KB</p>
            </div>
          </div>
          <p style="font-size:.78rem;color:var(--dim);margin-top:14px;line-height:1.65">These are your numbers, not a
            screenshot of mine. If they look bad on your connection, that is useful information and I would like to
            know about it.</p>
        </div>
      </div>'''


DS_DASH_LINK = '''<p class="sec-sub" style="margin-top:18px">There is a live dashboard for this pipeline — token counts,
        drift, coverage and platform outputs — built as a standalone page.
        <a href="./design-ops.html" style="color:var(--gold);font-weight:700">Open the DesignOps dashboard &rarr;</a></p>'''


def out(name, html):
    open(os.path.join(ROOT, name), "w", encoding="utf-8").write(html)
    print("wrote", name, len(html))


def creative_ld(slug, name, desc, img, kind):
    return [{
        "@type": "Article", "@id": f"{SITE}/{slug}#article",
        "headline": name, "description": desc, "image": f"{SITE}/{img}",
        "author": {"@id": f"{SITE}/#lulamile"}, "publisher": {"@id": f"{SITE}/#lulamile"},
        "inLanguage": "en-ZA", "about": kind, "isPartOf": {"@id": f"{SITE}/#website"},
    }, {
        "@type": "BreadcrumbList", "@id": f"{SITE}/{slug}#breadcrumbs",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Work", "item": f"{SITE}/case-studies"},
            {"@type": "ListItem", "position": 3, "name": name, "item": f"{SITE}/{slug}"},
        ]}]


# ══════════════════════════════════════════════════════════════════════════
#  04 — SERVICEWAZE
# ══════════════════════════════════════════════════════════════════════════
def servicewaze():
    body = f'''  <main id="main">
{hero(
    disc="dev", disc_label="Frontend engineering",
    h1='BUILT FOR<br /><span class="gold">ONE BAR OF SIGNAL.</span>',
    standfirst="Power, water, air, transport and weather in one honest view. An Angular PWA where the interesting "
               "engineering is not the happy path — it is everything that happens when the network does not answer.",
    meta=[("Product", "ServiceWaze · my own product"),
          ("My role", "Designer and frontend developer"),
          ("Stack", "Angular 17 standalone, signals, TypeScript, IndexedDB"),
          ("Duration", "Ongoing side project"),
          ("Code", '<a href="https://github.com/LulamileMkhungela/ServiceWaze" target="_blank" rel="noopener" style="color:var(--gold)">GitHub &#8599;</a>')],
    kpis=[("1.2s", "first paint on throttled 3G"), ("171 KB", "JavaScript, gzipped"),
          ("96", "Lighthouse performance"), ("100%", "of screens work offline")])}

    <div class="cover-wrap reveal">
      <div class="cover-frame">
        <img class="zoomable" src="./{A}sw-01-states.svg" alt="Six ServiceWaze interface states: fresh, stale, offline, loading, partial and empty" width="1200" height="700" />
        <p class="cover-caption">Six states, drawn before the happy path. A status app is mostly not-loaded.</p>
      </div>
    </div>

{chapters([("problem", "01 The problem"), ("process", "02 Design to code"), ("try", "03 Break it"),
           ("build", "04 The architecture"), ("results", "05 Performance"), ("honest", "06 Honest bit"), ("more", "Next")])}

{section("01", "problem", "THE NETWORK IS <span class='gold'>THE FEATURE.</span>",
         "Every status app I tried assumed the request would succeed. In Midrand at 18:00 on a load-shedding evening, "
         "that assumption is the bug.",
         notes([
             ("bad", "What other apps do",
              ["Spin forever, or show a blank screen with no explanation.",
               "Show a number from twenty minutes ago as if it were live — which is worse than showing nothing."]),
             ("dev", "The rule I built around",
              ["Never a blank screen. Never a stale number without saying it is stale.",
               "Both of those are one component with a state, not six screens."]),
         ]) + fig(A + "sw-01-states.svg", "Six interface states rendered side by side", "States",
                  "Each state has a written copy string, a colour token and an aria-live announcement. None of this is decoration."))}

{section("02", "process", "DESIGN AND CODE, <span class='gold'>SAME PERSON.</span>",
         "This is the case study where the two halves of my job stop being separate. Click through it.",
         rail([
             ("01", "Draw the failures", "Six states in Figma first",
              fig(A + "sw-01-states.svg", "State matrix", "Figma",
                  "I designed the offline and stale states before the fresh one. When you start with the failure, the success state falls out for free.")),
             ("02", "Find the seam", "One place is allowed to know the time",
              fig(A + "sw-02-arch.svg", "Offline-first architecture with the freshness rule and gateway code", "Architecture",
                  "Components take pure inputs. A single resource gateway decides cache versus network. That seam is the whole design.")),
             ("03", "Write the rule down", "Four tiers, no judgement calls",
              facts([("&lt; 2 min", "fresh — show it plainly"), ("2–15 min", "stale — show it, say how old"),
                     ("&gt; 15 min", "last known — say so, offer refresh"), ("no cache", "empty state, never a spinner")])
              + notes([("dev", "Why it is written and not implied",
                        ["A freshness policy that lives in three developers’ heads produces three different UIs. "
                         "Written down, it is one constant file and 38 unit tests."])])),
             ("04", "Budget the bundle", "180 KB, enforced in CI",
              fig(A + "sw-03-perf.svg", "Bundle growth against the budget line, plus Lighthouse gauges", "Performance",
                  "The budget was set in week one. When week nine crossed it, two features were cut rather than the number raised.")),
             ("05", "Test on a real phone", "Not on my laptop",
              notes([("good", "The device that decides",
                      ["A Moto G Power on a throttled connection, not a MacBook on fibre. Everything that feels fine "
                       "on a laptop feels different at 1.5 Mbps."]),
                     ("bad", "What that caught",
                      ["A 400 ms hitch on first render that was invisible on desktop. It was a font swap, and it was "
                       "one preload away from being fixed."])])),
         ]))}

{section("03", "try", "BREAK <span class='gold'>IT.</span>",
         "The real component logic. Force any state and see what the person on the other end would actually get.",
         DEMO_BOARD)}

{section("04", "build", "THE <span class='gold'>ARCHITECTURE.</span>",
         "Five public APIs, one gateway, one cache, and a rule about time.",
         fig(A + "sw-02-arch.svg", "Architecture diagram from UI layer to public APIs, with the freshness rule and code",
             "Architecture", "Version one cached inside the components. Three of them disagreed about what “now” meant and the UI flickered. Moving time into one gateway fixed a class of bug, not a bug.")
         + facts([("5", "public data sources"), ("38", "unit tests on the gateway alone"),
                  ("2.1 KB", "of freshness logic, gzipped"), ("1", "place that knows about time"),
                  ("0", "spinners without a timeout")]))}

{section("05", "results", "A BUDGET, <span class='gold'>NOT A HOPE.</span>",
         "Measured on a mid-range Android over throttled 3G — the device and connection this is actually for.",
         fig(A + "sw-03-perf.svg", "Bundle budget chart and Lighthouse scores", "Performance",
             "GitHub Actions runs Lighthouse CI and size-limit on every pull request. A regression is a red check, not a conversation three months later.")
         + facts([("1.2s", "first contentful paint"), ("1.9s", "largest contentful paint"),
                  ("0.01", "cumulative layout shift"), ("171 KB", "JS gzipped"),
                  ("0", "blocking third-party scripts")]), tint=True)}

{section("06", "honest", "THE <span class='gold'>HONEST BIT.</span>",
         "This is a side project I still work on, so the seams are current.",
         honest("Where it falls short today", [
             "Two of the five data sources have no official API. I scrape them, and when the page they come from changes, the source goes stale and the UI correctly says so — which is the right failure, but it is still a failure.",
             "isiZulu and Sesotho strings exist for the interface but not for the source data itself, so you get a translated label and an English status. That reads badly and I know it.",
             "There is no end-to-end test that actually flies the plane offline. The gateway is well unit-tested; the service worker registration is not.",
             "I designed and built this alone, which means nobody has ever pushed back on my architecture. That is a risk, not a boast.",
         ]))}

{nextprev(("case-study-stance.html", "Stance — insuring modified cars"),
          ("case-study-design-system.html", "Meridian — Figma to Angular"))}
  </main>'''

    slug = "case-study-servicewaze"
    out("case-study-servicewaze.html", shell(
        slug=slug,
        title="ServiceWaze — an offline-first Angular PWA | frontend case study",
        desc="Frontend engineering case study: six interface states designed before the happy path, a single freshness gateway, IndexedDB caching and a 180 KB bundle budget enforced in CI.",
        og="assets/og/servicewaze.png", body=body,
        ld_extra=creative_ld(slug, "ServiceWaze — an offline-first Angular PWA",
                             "Frontend engineering case study on offline-first architecture and performance budgets.",
                             A + "sw-01-states.svg", "Frontend engineering, Angular, progressive web apps")))


# ══════════════════════════════════════════════════════════════════════════
#  05 — MERIDIAN DESIGN SYSTEM
# ══════════════════════════════════════════════════════════════════════════
def design_system():
    body = f'''  <main id="main">
{hero(
    disc="dev", disc_label="Frontend engineering &amp; DesignOps",
    h1='FIGMA VARIABLES<br /><span class="gold">TO ANGULAR, ZERO DRIFT.</span>',
    standfirst="Four products, 213 hard-coded colours and a brand refresh estimated at six weeks. I built the pipeline "
               "and the governance that made the next refresh take two days.",
    meta=[("Context", "Multi-product platform, 4 apps"),
          ("My role", "System lead, token architecture, frontend"),
          ("Team", "Me plus 11 product engineers as consumers"),
          ("Stack", "Figma variables, Style Dictionary, Angular, Storybook, GitHub Actions"),
          ("Live", '<a href="./design-ops.html" style="color:var(--gold)">Open the DesignOps dashboard</a>')],
    kpis=[("213 → 0", "hard-coded colours"), ("80+", "components shipped"),
          ("64 → 11", "design-QA comments per release"), ("6 wks → 2 days", "to reskin every product")])}

    <div class="cover-wrap reveal">
      <div class="cover-frame">
        <img class="zoomable" src="./{A}ds-01-pipeline.svg" alt="Token pipeline from Figma variables through Style Dictionary to four platform outputs" width="1200" height="620" />
        <p class="cover-caption">One source of truth, four generated outputs, and six checks that stop it drifting.</p>
      </div>
    </div>

{chapters([("problem", "01 The problem"), ("process", "02 How it was built"), ("try", "03 Change a token"),
           ("build", "04 The pipeline"), ("results", "05 Adoption"), ("honest", "06 Honest bit"), ("more", "Next")])}

{section("01", "problem", "TWO HUNDRED AND THIRTEEN <span class='gold'>SHADES OF NEARLY.</span>",
         "A design system is not a component library. The library was the easy half — the hard half was making sure "
         "the value in the code is the value in the file, forever.",
         notes([
             ("bad", "What I inherited",
              ["213 hard-coded hex values across four Angular apps, 41 of them within 2% of each other.",
               "“Wrong shade of grey” was a recurring ticket type in the QA backlog."]),
             ("good", "What I set out to make impossible",
              ["Typing a hex value into a component should fail the build, not start a conversation in code review.",
               "A designer changing a token in Figma should be able to see it in every product without asking anyone."]),
         ]) + facts([("213", "hard-coded colours found"), ("41", "within 2% of another"),
                     ("4", "products out of sync"), ("6 wks", "estimated for a brand refresh"),
                     ("64", "design-QA comments in the last release")]))}

{section("02", "process", "HOW IT WAS <span class='gold'>BUILT.</span>",
         "Click a step. This one is mostly plumbing, and the plumbing is the point.",
         rail([
             ("01", "Audit", "Scripted, not eyeballed",
              notes([("dev", "An AST scan, not a spreadsheet",
                      ["I wrote a small script that walked every template and stylesheet in all four repos and "
                       "collected every colour literal with its file and line.",
                       "213 of them. That list became the backlog and, later, the regression test."])])
              + facts([("4", "repos scanned"), ("213", "literals found"), ("1", "afternoon"),
                       ("0", "opinions required")])),
             ("02", "Architect the tokens", "Three layers, one rule",
              fig(A + "ds-02-tokens.svg", "Token architecture in three layers with a resolution chain", "Token architecture",
                  "Primitive, semantic, component. Designers work in semantic, product teams work in component, and only I touch primitives. Light mode changes one layer and nothing else.")),
             ("03", "Automate the export", "Figma → git → four platforms",
              fig(A + "ds-01-pipeline.svg", "The export pipeline and the six CI checks", "Pipeline",
                  "A plugin exports Figma variables to tokens.json. Style Dictionary transforms it once per platform. Nobody types a hex value by hand, anywhere.")),
             ("04", "Gate it", "Six checks, all blocking",
              notes([("dev", "The check that did the most work",
                      ["<code>no-raw-colour</code> — an ESLint rule that makes a hex literal in a component an error. "
                       "It is nine lines of configuration and it did more for consistency than the other five combined."]),
                     ("good", "The check people liked most",
                      ["<code>token-diff</code> posts a table of every changed token as a comment on the pull request. "
                       "Reviewers stopped having to imagine what a change would look like."])])),
             ("05", "Make adoption visible", "Measured, then posted",
              fig(A + "ds-03-inventory.svg", "Component inventory, adoption curve and QA comment counts", "Inventory + adoption",
                  "A library nobody adopts is a hobby. An AST scan measures the percentage of UI built from the library on every merge, and the number goes in the team channel every Monday.")),
         ]))}

{section("03", "try", "CHANGE A <span class='gold'>TOKEN.</span>",
         "This is the whole argument for the architecture, in one widget. Move a slider and watch every component "
         "follow — without touching a single component file.",
         DEMO_TOKENS)}

{section("04", "build", "THE <span class='gold'>PIPELINE.</span>",
         "Figma is the source. Everything downstream is generated, and six checks stop it drifting.",
         fig(A + "ds-01-pipeline.svg", "Full pipeline diagram with the six blocking CI checks", "Pipeline",
             "The gate is more important than the generator. Anyone can export tokens once; keeping them true for a year is the actual work.")
         + fig(A + "ds-02-tokens.svg", "Three token layers and how one value resolves", "Token layers",
               "Why three layers and not one: light mode changes only the semantic layer, so no component can be forgotten.")
         + DS_DASH_LINK)}

{section("05", "results", "DOES ANYONE <span class='gold'>ACTUALLY USE IT?</span>",
         "The only question worth asking about a design system, and the one most case studies skip.",
         fig(A + "ds-03-inventory.svg", "Adoption curve reaching 91% and QA comments falling from 64 to 11",
             "Adoption", "Eight months from 12% to 91%. Design-QA comments per release fell from 64 to 11 with the same reviewer and the same checklist.")
         + facts([("91%", "of UI built from the library"), ("80+", "components"),
                  ("213 → 0", "hard-coded colours"), ("64 → 11", "QA comments per release"),
                  ("2 days", "to reskin all four products")]), tint=True)}

{section("06", "honest", "THE <span class='gold'>HONEST BIT.</span>",
         "Design systems fail slowly and quietly. Here is where this one is weakest.",
         honest("What I would do differently", [
             "I built the token layers before talking to the product engineers who would consume them. The component layer was over-engineered for the first three months and I had to delete about a third of it.",
             "Adoption at 91% sounds finished. The last 9% is one legacy app that will never migrate, and pretending otherwise on a chart is dishonest — it should be excluded and named.",
             "Documentation is Storybook plus a README. There is no “when should I not use this component” guidance, which is the thing juniors actually need.",
             "The Figma plugin export is a manual click. It should be a webhook, and until it is, the source of truth is only as fresh as the last person who remembered.",
         ]))}

{nextprev(("case-study-servicewaze.html", "ServiceWaze — offline-first PWA"),
          ("case-study-seo-performance.html", "Rebuilding this site"))}
  </main>'''

    slug = "case-study-design-system"
    out("case-study-design-system.html", shell(
        slug=slug,
        title="Meridian — Figma variables to Angular with zero drift | design system case study",
        desc="DesignOps case study: a three-layer token architecture, an automated Figma to Angular pipeline, 80+ components and six blocking CI checks. Adoption reached 91%.",
        og="assets/og/design-system.png", body=body,
        ld_extra=creative_ld(slug, "Meridian — Figma variables to Angular, zero drift",
                             "Design system and DesignOps engineering case study.",
                             A + "ds-01-pipeline.svg", "Design systems, design tokens, DesignOps, Angular")))


# ══════════════════════════════════════════════════════════════════════════
#  06 — THIS SITE
# ══════════════════════════════════════════════════════════════════════════
def performance():
    body = f'''  <main id="main">
{hero(
    disc="dev", disc_label="Frontend engineering &amp; technical SEO",
    h1='I AUDITED MY OWN SITE<br /><span class="gold">AND DID NOT LIKE IT.</span>',
    standfirst="A portfolio that took 6.4 seconds to show anything is an argument against hiring me. So I rebuilt it, "
               "and this page measures itself while you read it.",
    meta=[("Project", "This website"), ("My role", "Designer, developer and analyst"),
          ("Stack", "Hand-written HTML, CSS and JavaScript. No framework."),
          ("Test rig", "Moto G Power, Fast 3G, cold cache"),
          ("Verify it", "Everything here is in this page&rsquo;s source")],
    kpis=[("6.4s → 1.1s", "largest contentful paint"), ("5.8 MB → 240 KB", "page weight"),
          ("41 → 99", "Lighthouse performance"), ("0", "cookies set")])}

    <div class="cover-wrap reveal">
      <div class="cover-frame">
        <img class="zoomable" src="./{A}perf-01-audit.svg" alt="Lighthouse scores before and after, with the six metrics that moved" width="1200" height="580" />
        <p class="cover-caption">Same page, same device, same connection. The only variable is the code.</p>
      </div>
    </div>

{chapters([("problem", "01 The audit"), ("process", "02 What I changed"), ("try", "03 Measure this page"),
           ("build", "04 Findable"), ("results", "05 Results"), ("honest", "06 Honest bit"), ("more", "Next")])}

{section("01", "problem", "THE <span class='gold'>AUDIT.</span>",
         "A designer’s portfolio that fails Core Web Vitals is a portfolio making an argument against itself. Mine was.",
         fig(A + "perf-01-audit.svg", "Lighthouse gauges before and after with six key metrics", "Baseline",
             "November baseline. 41 for performance, 5.8 MB of page weight, and a 0.34 layout shift that moved the text under your thumb as you read it.")
         + notes([
             ("bad", "The three worst offenders",
              ["A 2.1 MB PNG hero, displayed at 800 px wide.",
               "Six third-party scripts, three of which nobody had used in two years.",
               "jQuery and Bootstrap loaded in full to do about forty lines of work."]),
             ("dev", "The approach",
              ["Delete, then compress, then optimise — in that order. Most performance work is deletion wearing a "
               "technical hat."]),
         ]))}

{section("02", "process", "WHAT I <span class='gold'>CHANGED.</span>",
         "Six changes, in the order that mattered. Click through them.",
         rail([
             ("01", "Delete", "Three scripts, jQuery, Bootstrap",
              fig(A + "perf-02-waterfall.svg", "Network waterfall before and after", "Waterfall",
                  "74 requests became 18. The largest single win was removing things, not optimising them.")),
             ("02", "Re-encode", "41 images to WebP, at display size",
              facts([("41", "images re-encoded"), ("−96%", "image weight"), ("2.1 MB → 41 KB", "the hero alone"),
                     ("0", "images without width and height")])
              + notes([("good", "Where the layout shift went",
                        ["Every image now declares its dimensions, so the browser reserves the space before the bytes "
                         "arrive. That single change took CLS from 0.34 to 0.00."])])),
             ("03", "Inline what paints", "6 KB of critical CSS",
              notes([("dev", "Critical path",
                      ["The first screen needs about 6 KB of CSS. That is inlined. Everything else loads after paint "
                       "and nobody notices."]),
                     ("dev", "Fonts",
                      ["Subset to the glyphs the site actually uses, self-hosted, preloaded, with "
                       "<code>font-display: swap</code>. One preload removed a 400 ms hitch on first render."])])),
             ("04", "Rewrite the JavaScript", "24 KB, hand-written",
              notes([("good", "What replaced 180 KB of library",
                      ["A theme toggle, a mobile menu, a reading bar, tab groups, before/after sliders, counters, a "
                       "lightbox and scroll reveal. All of it is in "
                       "<code>assets/case-study.js</code> and you can read the whole thing."])])),
             ("05", "Make it findable", "Six schema types, one graph",
              fig(A + "perf-03-schema.svg", "Structured data graph and the JSON-LD source", "Structured data",
                  "One connected JSON-LD graph per page rather than six disconnected blobs. Validated in CI against the Schema.org vocabulary.")),
             ("06", "Measure honestly", "1.4 KB, no cookies",
              notes([("dev", "Cookie-free analytics",
                      ["Page, referrer and Core Web Vitals, sent to a first-party endpoint. No cookies, no "
                       "fingerprinting, no consent banner needed because there is nothing to consent to."]),
                     ("good", "Why it matters here",
                      ["A consent banner is a layout shift and a blocking script wearing a legal costume. Not "
                       "collecting the data was cheaper than asking permission for it."])])),
         ]))}

{section("03", "try", "MEASURE <span class='gold'>THIS PAGE.</span>",
         "Not a screenshot of my results — your browser, your connection, right now.",
         DEMO_VITALS)}

{section("04", "build", "FINDABLE, <span class='gold'>NOT JUST FAST.</span>",
         "Speed gets you indexed. Structure gets you understood.",
         fig(A + "perf-03-schema.svg", "Six connected schema types and the JSON-LD in the page source", "Schema",
             "Person, Organization, WebSite, WebPage, BreadcrumbList and an Article per case study — connected by @id rather than repeated.")
         + facts([("6", "schema types, one graph"), ("11/11", "pages with canonical + Open Graph"),
                  ("0", "validation warnings"), ("100", "Lighthouse SEO"), ("1.4 KB", "analytics payload")]))}

{section("05", "results", "THE <span class='gold'>NUMBERS.</span>",
         "Everything below is verifiable from this page’s source and your own dev tools.",
         fig(A + "perf-02-waterfall.svg", "Before and after network waterfalls with the six changes listed",
             "Waterfall", "6.9 seconds to interactive became 1.1. Two-thirds of that came from the first change on the list.")
         + facts([("41 → 99", "Lighthouse performance"), ("6.4s → 1.1s", "largest contentful paint"),
                  ("0.34 → 0.00", "cumulative layout shift"), ("74 → 18", "requests"),
                  ("5.8 MB → 240 KB", "page weight")]), tint=True)}

{section("06", "honest", "THE <span class='gold'>HONEST BIT.</span>",
         "This is my own site, which means there is nobody to stop me marking my own homework.",
         honest("Caveats you should hold me to", [
             "99 is the median of five runs on my rig. Your number will differ, which is exactly why the widget above measures yours instead of showing you mine.",
             "The case-study artefacts on this site are SVG, which is why they are small and sharp. A site full of photography could not hit these numbers the same way and I would not pretend otherwise.",
             "I have no real-user monitoring at scale — the traffic is too low for the percentiles to mean anything. Everything here is lab data, and lab data flatters.",
             "Google Fonts is still loaded from a CDN on a few pages. Self-hosting it everywhere is on the list and is not done.",
         ]))}

{nextprev(("case-study-design-system.html", "Meridian — Figma to Angular"), None)}
  </main>'''

    slug = "case-study-seo-performance"
    out("case-study-seo-performance.html", shell(
        slug=slug,
        title="Rebuilding this site — performance, Core Web Vitals and technical SEO",
        desc="Frontend case study on my own site: 5.8 MB to 240 KB, LCP from 6.4s to 1.1s, a six-type schema graph and cookie-free analytics. The page measures itself while you read it.",
        og="assets/og/seo-performance.png", body=body,
        ld_extra=creative_ld(slug, "Rebuilding this site — performance and technical SEO",
                             "Frontend performance, Core Web Vitals and technical SEO case study.",
                             A + "perf-01-audit.svg", "Web performance, technical SEO, analytics")))


if __name__ == "__main__":
    servicewaze(); design_system(); performance()
