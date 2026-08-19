#!/usr/bin/env python3
"""The three UX/UI + product design case studies."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from shell import *  # noqa

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
A = "assets/cs/"


DEMO_IA = '''<div class="demo" id="iaPaths">
        <div class="demo-bar">
          <span class="tag">Interactive</span>
          <div class="seg" role="group" aria-label="Pick a task">
            <button type="button" class="on" data-task="payslip">Find my payslip</button>
            <button type="button" data-task="leave">Apply for leave</button>
            <button type="button" data-task="claim">Claim travel</button>
            <button type="button" data-task="status">Check a request</button>
          </div>
          <span class="hint">Tree-test data, n = 31</span>
        </div>
        <div class="demo-body">
          <div class="paths">
            <div class="path old" id="pathOld">
              <h5>Before — 11 destinations</h5>
              <ol></ol>
              <p class="path-foot"></p>
            </div>
            <div class="path new" id="pathNew">
              <h5>After — 4 task hubs</h5>
              <ol></ol>
              <p class="path-foot"></p>
            </div>
          </div>
        </div>
      </div>'''

DEMO_CHAT = '''<div class="demo" id="tobiChat" data-segs>
        <div class="demo-bar">
          <span class="tag">Interactive</span>
          <div class="seg" role="group" aria-label="Which version">
            <button type="button" data-seg="before">The bot I found</button>
            <button type="button" class="on" data-seg="after">The bot I wrote</button>
          </div>
          <span class="hint">Responses are the actual scripted copy</span>
        </div>
        <div class="demo-body">
          <div class="chat" aria-live="polite"></div>
          <div class="chat-asks"></div>
        </div>
      </div>'''

DEMO_CALC = '''<div class="demo" id="stanceCalc">
        <div class="demo-bar">
          <span class="tag">Interactive</span>
          <span class="hint">Illustrative rates, real structure</span>
        </div>
        <div class="demo-body">
          <div class="duo" style="grid-template-columns:1.05fr .95fr">
            <div>
              <p style="font-size:.72rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--dim);margin-bottom:10px">
                What&rsquo;s on the car?</p>
              <div class="picker">
                <label><input type="checkbox" data-cost="52" data-value="18000" checked /><span>Exhaust system</span></label>
                <label><input type="checkbox" data-cost="61" data-value="22000" checked /><span>Suspension / coilovers</span></label>
                <label><input type="checkbox" data-cost="44" data-value="14000" /><span>ECU remap</span></label>
                <label><input type="checkbox" data-cost="73" data-value="26000" checked /><span>Wheels &amp; tyres</span></label>
                <label><input type="checkbox" data-cost="38" data-value="12000" /><span>Body kit</span></label>
                <label><input type="checkbox" data-cost="86" data-value="31000" /><span>Turbo upgrade</span></label>
                <label><input type="checkbox" data-cost="29" data-value="9000" /><span>Roll cage</span></label>
                <label><input type="checkbox" id="trackDay" /><span>Track-day cover</span></label>
              </div>
            </div>
            <div class="readout">
              <p style="font-size:.68rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--dim)">
                Monthly premium</p>
              <p class="big" id="qTotal">R1 128</p>
              <p style="font-size:.74rem;color:var(--dim);margin:2px 0 14px" id="qCount">3 modifications</p>
              <div class="row"><span>Vehicle cover</span><b id="qBase">R942</b></div>
              <div class="row"><span>Declared modifications</span><b id="qMods">R186</b></div>
              <div class="row"><span>Track-day add-on</span><b id="qTrack">not added</b></div>
              <div class="row"><span>Agreed value</span><b id="qValue">R451 000</b></div>
              <p style="margin-top:14px;padding:12px 14px;border-radius:10px;background:color-mix(in srgb,var(--good) 12%,transparent);border:1px solid color-mix(in srgb,var(--good) 34%,transparent);font-size:.8rem;font-weight:700;color:var(--good);line-height:1.5"
                id="qSaving"></p>
            </div>
          </div>
        </div>
      </div>'''


def out(name, html):
    p = os.path.join(ROOT, name)
    open(p, "w", encoding="utf-8").write(html)
    print("wrote", name, len(html))


def creative_ld(slug, name, desc, img, kind):
    return [{
        "@type": "Article", "@id": f"{SITE}/{slug}#article",
        "headline": name, "description": desc,
        "image": f"{SITE}/{img}",
        "author": {"@id": f"{SITE}/#lulamile"},
        "publisher": {"@id": f"{SITE}/#lulamile"},
        "inLanguage": "en-ZA",
        "about": kind,
        "isPartOf": {"@id": f"{SITE}/#website"},
    }, {
        "@type": "BreadcrumbList", "@id": f"{SITE}/{slug}#breadcrumbs",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Work", "item": f"{SITE}/case-studies"},
            {"@type": "ListItem", "position": 3, "name": name, "item": f"{SITE}/{slug}"},
        ]}]


# ══════════════════════════════════════════════════════════════════════════
#  01 — ENGAGE
# ══════════════════════════════════════════════════════════════════════════
def engage():
    body = f'''  <main id="main">
{hero(
    disc="design", disc_label="UX / UI &amp; product design",
    h1='TWENTY-FIVE THOUSAND PEOPLE.<br /><span class="gold">ONE HOME SCREEN.</span>',
    standfirst="An employee app everybody had installed and nobody used for real work. I rebuilt what it was made of, "
               "not what it looked like — and measured the same five tasks before and after.",
    meta=[("Client", "Vodacom · internal product"), ("My role", "UX research, IA, UI, prototype"),
          ("Team", "1 designer (me), 4 engineers, 1 PO"), ("Duration", "14 weeks"),
          ("Platforms", "Android, iOS, web")],
    kpis=[("48s → 19s", "median time to first task"), ("38 → 86%", "task success in a tree test"),
          ("11 → 4", "top-level destinations"), ("+34%", "self-service, no service desk")])}

    <div class="cover-wrap reveal">
      <div class="cover-frame">
        <img class="zoomable" src="./{A}engage-05-ui.svg" alt="Three shipped Engage screens: Today, Do and request status" width="1200" height="668" />
        <p class="cover-caption">The three screens that carry the whole app. Everything else is a detail page.</p>
      </div>
    </div>

{chapters([("problem", "01 The problem"), ("process", "02 How I got there"), ("try", "03 Try the rebuild"),
           ("shipped", "04 What shipped"), ("results", "05 Results"), ("honest", "06 Honest bit"), ("more", "Next")])}

{section("01", "problem", "IT WAS NOT A <span class='gold'>DESIGN PROBLEM</span> YET.",
         "Adoption was 91%. Weekly active use was 12%. The brief I was handed said “refresh the UI”. Four weeks of "
         "research said something else.",
         notes([
             ("bad", "What the brief assumed",
              ["The app looked dated, so people avoided it.",
               "A visual refresh and a new icon set would fix engagement."]),
             ("good", "What the evidence said",
              ["People could not find anything. Search was doing the job the menu should have done.",
               "31% of employees who opened the app gave up and phoned the service desk instead."]),
         ]) + fig(A + "engage-01-research.svg",
                  "Affinity wall of employee interview quotes clustered into four themes",
                  "Discovery", "14 interviews, 6 shadowing sessions and 2 041 tagged support tickets, clustered into four themes. Each cluster became a design principle.")
         + fig(A + "engage-02-journey.svg",
               "Current-state journey map for claiming a travel expense with an emotion curve",
               "Journey map", "Shadowing one task end to end. The dip happens before the form — people were lost on the home screen, not inside the task."))}

{section("02", "process", "HOW I GOT <span class='gold'>THERE.</span>",
         "Click a step. Each one shows the actual artefact it produced, not a description of it.",
         rail([
             ("01", "Discover", "14 interviews, 2 041 tickets",
              fig(A + "engage-01-research.svg", "Affinity wall", "Week 1–4",
                  "Quotes on a wall, clustered until the clusters stopped moving. Ticket data confirmed what the interviews suggested: navigation, not features.")),
             ("02", "Frame", "One problem, four principles",
              notes([("bad", "Problem statement",
                      ["“An employee needs to complete one small admin task in the gap between meetings — and today "
                       "the app makes them hunt for it.”"]),
                     ("good", "The four principles",
                      ["01 Name things the way people say them.",
                       "02 Show today, not everything.",
                       "03 Every action must have a visible status.",
                       "04 Assume a bad signal and an old phone."])])
              + facts([("4", "principles, agreed in writing"), ("5", "tasks chosen as the benchmark"),
                       ("48s", "the number we had to beat"), ("0", "features added to the scope")])),
             ("03", "Restructure", "Card sort, then two tree tests",
              fig(A + "engage-03-ia.svg", "Information architecture before and after", "Card sort + tree test",
                  "24 employees sorted the content, 31 more tested both structures on the same five tasks. Eleven department-shaped destinations became four task-shaped hubs.")),
             ("04", "Test flat", "Three rounds, greyscale",
              fig(A + "engage-04-wireframes.svg", "Lo-fi wireframes with test annotations", "Wireframes",
                  "Printed, greyscale, deliberately ugly. Two ideas died here — a chat tab and a news feed — which is exactly what this stage is for.")),
             ("05", "Design & hand over", "Tokens, six states, and the PR",
              fig(A + "engage-05-ui.svg", "Shipped interface screens with the handover checklist", "UI + handover",
                  "Only what survived three rounds got colour. Each screen shipped with six states, its copy, and its accessibility notes — and I opened the pull request for the Today screen myself.")),
         ]))}

{section("03", "try", "TRY THE <span class='gold'>REBUILD.</span>",
         "Pick a task and watch the route people actually took, next to the route they take now. Real paths from the tree tests.",
         DEMO_IA)}

{section("04", "shipped", "WHAT ACTUALLY <span class='gold'>SHIPPED.</span>",
         "Three screens carry the app. The rest are detail pages that inherit from them.",
         fig(A + "engage-05-ui.svg", "Today, Do and status screens with handover notes", "Shipped UI",
             "Built on the same tokens as the design system, so a brand change does not become a redesign.")
         + facts([("6", "states drawn per screen"), ("48px", "minimum touch target"),
                  ("4.5:1", "minimum contrast, both themes"), ("200%", "text size supported"),
                  ("0", "P1 accessibility defects at launch")]))}

{section("05", "results", "MEASURED THE <span class='gold'>SAME WAY, TWICE.</span>",
         "Same five tasks, same script, unmoderated. Eight weeks before launch and eight weeks after.",
         fig(A + "engage-06-results.svg", "Before and after task success and time-to-task charts", "Benchmark",
             "n = 31 before, n = 27 after. The one that mattered internally was the 28% drop in service-desk calls about “where is…”.")
         + facts([("+48pp", "average task success"), ("−60%", "median time to first task"),
                  ("−28%", "service-desk “where is…” calls"), ("2.9 → 4.6", "in-app rating"),
                  ("+34%", "self-service completions")]), tint=True)}

{section("06", "honest", "THE <span class='gold'>HONEST BIT.</span>",
         "Things that did not go to plan, because a case study without them is a brochure.",
         honest("What I would do differently", [
             "I ran the first card sort with head-office staff only. The retail and call-centre vocabulary was different enough that I had to redo it in week six. Recruit for the edges first.",
             "“Ask” was the weakest of the four hubs — it is really two things (search a person, ask a question) wearing one label. It works, but I would split it.",
             "I did not instrument the empty states, so I still cannot tell you how often people hit them. That is a measurement gap I created.",
             "The web build lagged mobile by five weeks. Designing three platforms at once with one designer meant web got the leftovers.",
         ]) + notes([
             ("dev", "Where the frontend part mattered",
              ["I wrote the Today screen in the Angular codebase rather than specifying it. It removed a week of "
               "back-and-forth about scroll behaviour and let me feel how slow the shift card really was on a cheap phone.",
               "That is the part of my role that is hard to put in a Figma file."]),
             ("good", "What I would keep",
              ["Agreeing the benchmark before designing anything. It is the only reason there is an “after” number "
               "at all, and it ended arguments about taste very quickly."]),
         ]))}

{nextprev(None, ("case-study-tobi-bursary.html", "TOBi &amp; the bursary journey"))}
  </main>'''

    slug = "case-study-engage"
    out("case-study-engage.html", shell(
        slug=slug,
        title="Engage — 25 000 people, one home screen | UX case study",
        desc="Enterprise UX case study: research, a rebuilt information architecture, three rounds of flat testing and a shipped interface. Time to first task fell from 48 to 19 seconds.",
        og="assets/og/engage.png",
        body=body,
        ld_extra=creative_ld(slug, "Engage — 25 000 people, one home screen",
                             "Enterprise UX and product design case study for an employee app.",
                             A + "engage-05-ui.svg", "UX research, information architecture, product design")))


# ══════════════════════════════════════════════════════════════════════════
#  02 — TOBi + bursary
# ══════════════════════════════════════════════════════════════════════════
def tobi():
    body = f'''  <main id="main">
{hero(
    disc="design", disc_label="UX / UI &amp; product design",
    h1='A BOT THAT SAID SORRY,<br /><span class="gold">AND A FORM NOBODY FINISHED.</span>',
    standfirst="Two broken halves of one service. I read 3 400 transcripts, mapped the service around them, and "
               "rewrote both the conversation and the 42-field form it kept sending people to.",
    meta=[("Context", "Internal support assistant + bursary programme"),
          ("My role", "UX lead, conversation &amp; content design"),
          ("Team", "1 designer (me), 2 engineers, bursary office, service desk"),
          ("Duration", "11 weeks"), ("Languages", "English, isiZulu, Sesotho, Afrikaans")],
    kpis=[("41 → 68%", "conversations contained"), ("38 → 61%", "applications completed"),
          ("40 → 9 min", "median time to apply"), ("−78%", "“where is my application?” calls")])}

    <div class="cover-wrap reveal">
      <div class="cover-frame">
        <img class="zoomable" src="./{A}tobi-03-flow.svg" alt="Conversation flow with the happy path and three exits" width="1200" height="614" />
        <p class="cover-caption">The script, drawn before a single node was built. Two failed turns hands over to a human.</p>
      </div>
    </div>

{chapters([("problem", "01 The problem"), ("process", "02 How I got there"), ("try", "03 Talk to it"),
           ("shipped", "04 The form"), ("results", "05 Results"), ("honest", "06 Honest bit"), ("more", "Next")])}

{section("01", "problem", "SIX TURNS. <span class='gold'>ZERO ANSWERS.</span>",
         "The assistant had a 94% “resolution” rate on the dashboard. It was counting anything that ended, including "
         "the people who gave up.",
         fig(A + "tobi-01-audit.svg", "Conversation audit: a real transcript and intent volume against bot coverage",
             "Audit", "3 400 transcripts read and tagged by hand. The two highest-volume intents had no coverage at all — nobody had ever compared demand against capability.")
         + notes([
             ("bad", "Measuring the wrong thing",
              ["“Resolved” meant the chat window closed. A person swearing and closing the tab counted as a success.",
               "I replaced it with containment: did this person get what they came for without a human?"]),
             ("good", "Where the real cost sat",
              ["Every dead end became a phone call. The bursary intent alone generated 812 conversations a month and "
               "answered none of them.",
               "The form on the other end abandoned six people in ten."]),
         ]))}

{section("02", "process", "HOW I GOT <span class='gold'>THERE.</span>",
         "Click a step to see the artefact.",
         rail([
             ("01", "Read everything", "3 400 transcripts, tagged",
              fig(A + "tobi-01-audit.svg", "Conversation audit", "Audit",
                  "Two weeks in a spreadsheet. Unglamorous, and the only reason the rest of the project pointed the right way.")),
             ("02", "Map the service", "Blueprint with the people who run it",
              fig(A + "tobi-02-blueprint.svg", "Service blueprint of the bursary application", "Blueprint",
                  "Drawn in one room with the bursary office, the service desk and a student who had failed the process twice. Five failure points, one root cause: the service assumed a laptop, a printer and patience.")),
             ("03", "Write the script", "Read aloud before it was built",
              fig(A + "tobi-03-flow.svg", "Conversation flow and content design comparison", "Conversation design",
                  "One question per turn, no dead ends, hand over after two failures. The rewrite cut the eligibility answer from 61 words to 24.")),
             ("04", "Rebuild the form", "42 fields audited one by one",
              fig(A + "tobi-04-form.svg", "Form redesign from 42 fields on one page to four saved steps", "Form",
                  "For each field: what is it for, who reads it, can we already know it? Seventeen could not answer and were removed or inferred.")),
             ("05", "Ship and watch", "Weekly transcript review",
              facts([("68%", "contained after 8 weeks"), ("61%", "applications completed"),
                     ("4", "languages live"), ("2", "turns before a human"), ("weekly", "transcript review, still running")])
              + notes([("good", "The habit that kept it working",
                        ["Every Friday I read 40 fresh transcripts and tag the misses. Three intents were added in the "
                         "first two months purely because people kept asking for them."])])),
         ]))}

{section("03", "try", "TALK TO <span class='gold'>IT.</span>",
         "The real scripts, side by side. Switch between the bot I found and the bot I wrote, then ask it something.",
         DEMO_CHAT)}

{section("04", "shipped", "THE FORM ON <span class='gold'>THE OTHER END.</span>",
         "Fixing the conversation only moves the problem if it hands people to a form they cannot finish.",
         fig(A + "tobi-04-form.svg", "Before and after of the bursary application form", "Form redesign",
             "Four steps that autosave, an institution picker instead of free text, camera-first uploads with the size limit stated before you try.")
         + facts([("42 → 25", "fields"), ("17", "removed or inferred"), ("4", "steps, each one saved"),
                  ("8 MB", "upload limit, stated up front"), ("9 min", "median completion")]))}

{section("05", "results", "WHAT <span class='gold'>CHANGED.</span>",
         "Eight weeks after launch, measured on the same definitions I set at the start.",
         facts([("41 → 68%", "conversations contained"), ("38 → 61%", "applications completed"),
                ("−33%", "repeat contacts"), ("−78%", "status phone calls"), ("40 → 9 min", "median time to apply")])
         + notes([
             ("good", "The number I care about most",
              ["Repeat contacts. A single resolved chat is easy to fake; someone not coming back the next day is not."]),
             ("bad", "The number that did not move",
              ["Applications from outside the organisation stayed flat. That funnel starts on a printed poster with no "
               "link on it, which is not a problem a chatbot can solve."]),
         ]), tint=True)}

{section("06", "honest", "THE <span class='gold'>HONEST BIT.</span>",
         "What I got wrong, and what I still cannot prove.",
         honest("What I would do differently", [
             "I wrote the isiZulu and Sesotho copy with a translator, not with a content designer who speaks them daily. It is correct but it is stiff, and two participants said so politely.",
             "I built 61 phrasings for the bursary intent by hand. That should have been mined from the transcripts programmatically — it would have caught the SMS-style spellings I missed.",
             "Containment is not satisfaction. I have no CSAT on the new flow because we never shipped the survey, so “68% contained” is the best claim I can honestly make.",
             "The panel scoring at the end is still a spreadsheet. The applicant experience is fixed; the staff experience behind it is not, and that is where the next round of work should go.",
         ]))}

{nextprev(("case-study-engage.html", "Engage — one home screen"),
          ("case-study-stance.html", "Stance — insuring modified cars"))}
  </main>'''

    slug = "case-study-tobi-bursary"
    out("case-study-tobi-bursary.html", shell(
        slug=slug,
        title="TOBi &amp; the bursary journey — conversation design case study",
        desc="Conversational UX and service design: 3 400 transcripts audited, a service blueprint, a rewritten script and a 42-field form rebuilt as four saved steps. Completion rose from 38% to 61%.",
        og="assets/og/tobi.png",
        body=body,
        ld_extra=creative_ld(slug, "TOBi & the bursary journey",
                             "Conversational UX, service design and content design case study.",
                             A + "tobi-03-flow.svg", "Conversation design, service design, content design")))


# ══════════════════════════════════════════════════════════════════════════
#  03 — STANCE
# ══════════════════════════════════════════════════════════════════════════
def stance():
    body = f'''  <main id="main">
{hero(
    disc="design", disc_label="UX / UI &amp; product design",
    h1='INSURANCE FOR THE CARS<br /><span class="gold">EVERYONE ELSE REFUSED.</span>',
    standfirst="South Africa’s modified-car owners were being loaded, declined, or quietly under-insuring themselves. "
               "I took it from a market question to a live product with a four-minute quote.",
    meta=[("Client", "Stance Insurance"), ("My role", "Product strategy, UX research, UI, design system"),
          ("Team", "2 developers, 1 underwriter, me"), ("Duration", "10 weeks to first release"),
          ("Status", '<a href="https://www.stanceinsurance.co.za/" target="_blank" rel="noopener" style="color:var(--gold)">Live in production &#8599;</a>')],
    kpis=[("27 → 9", "questions to a quote"), ("4 min", "median time to a price"),
          ("9 of 11", "testers chose agreed value"), ("0 → 1", "product, built from research")])}

    <div class="cover-wrap reveal">
      <div class="cover-frame">
        <img class="zoomable" src="./{A}stance-02-flow.svg" alt="Quote flow, modification picker and price breakdown screens" width="1200" height="726" />
        <p class="cover-caption">The two screens the whole product turns on: what is fitted, and what that costs.</p>
      </div>
    </div>

{chapters([("problem", "01 The problem"), ("process", "02 How I got there"), ("try", "03 Price a car"),
           ("shipped", "04 The kit"), ("results", "05 Results"), ("honest", "06 Honest bit"), ("more", "Next")])}

{section("01", "problem", "A MARKET THAT KEPT BEING <span class='gold'>TOLD NO.</span>",
         "Fit an exhaust, declare it, get loaded or declined. So people stopped declaring — and then found out at "
         "claim stage that they were not covered.",
         fig(A + "stance-01-discovery.svg", "Discovery research: the current journey, forum evidence and three personas",
             "Discovery", "Nine broker interviews, 214 coded forum posts and three ride-alongs. Seven of nine brokers said they simply decline the segment.")
         + notes([
             ("bad", "The trap",
              ["Declaring a modification raised the premium. Not declaring it voided the claim.",
               "Both options were bad, so people chose the one that hurt later."]),
             ("good", "The bet that became the product",
              ["A modified car is often a better-maintained car. If declaring can make the price go <em>down</em> in "
               "some cases, the whole funnel changes — and the insurer gets accurate risk data for the first time."]),
         ]))}

{section("02", "process", "HOW I GOT <span class='gold'>THERE.</span>",
         "Ten weeks, four artefacts, one very opinionated underwriter.",
         rail([
             ("01", "Find the pain", "9 brokers, 214 posts, 3 ride-alongs",
              fig(A + "stance-01-discovery.svg", "Discovery research board", "Research",
                  "Forum posts were the honest data source — people say things to each other that they will not say to an insurer. Three personas came out of it, each with a different job to be done.")),
             ("02", "Price the bet", "Sat with the underwriter for two days",
              notes([("dev", "Design working on the maths",
                      ["I could not design the pricing screen until I understood the model, so I spent two days with "
                       "the underwriter building the loading table in a spreadsheet.",
                       "That is where the “declared can be cheaper” rule actually got written."]),
                     ("good", "What it unlocked",
                      ["Because I knew which inputs moved the number, I could cut 18 questions that did not — and "
                       "defend the cut with the underwriter’s own model."])])
              + facts([("27 → 9", "questions asked"), ("18", "questions with no pricing effect"),
                       ("2 days", "with the underwriter"), ("1", "spreadsheet nobody else wanted to open")])),
             ("03", "Design the quote", "Reg lookup, picker, comparison",
              fig(A + "stance-02-flow.svg", "Four-step quote flow and the interface decisions behind it", "Flow + UI",
                  "Four steps. Registration lookup fills nine fields. Modifications are a picker, because free text produced 340 spellings of “coilovers”.")),
             ("04", "Test outdoors", "11 owners, two car meets, real phones",
              notes([("good", "Testing where the users are",
                      ["Two Saturday car meets, 11 owners, their own phones, in direct sunlight.",
                       "Three contrast problems and one unreadable disclaimer only showed up because we were outside."]),
                     ("bad", "What failed the test",
                      ["My first pricing screen showed one number. People assumed they were being penalised for the "
                       "mods and half of them abandoned. Splitting the price into lines fixed it."])])),
             ("05", "Ship a small system", "9 colours, 6 sizes, 14 components",
              fig(A + "stance-03-kit.svg", "Interface kit: colour roles, type ramp, components and states", "Design system",
                  "Deliberately small. Two developers and ten weeks means a system you can hold in your head — anything bigger drifts by month three.")),
         ]))}

{section("03", "try", "PRICE A <span class='gold'>CAR.</span>",
         "The real logic from the quote step. Tick what is fitted and watch both numbers move — including the one that "
         "makes the whole strategy true.",
         DEMO_CALC)}

{section("04", "shipped", "A SMALL KIT, <span class='gold'>SHIPPED FAST.</span>",
         "Nine colour roles, six type sizes, fourteen components — and every awkward state drawn before launch.",
         fig(A + "stance-03-kit.svg", "The Stance interface kit and its component states", "Design system",
             "Handed over as a Figma library plus a one-page README in the repo, which is the part developers actually read.")
         + facts([("14", "components"), ("5", "states each"), ("9", "colour roles"),
                  ("10 wks", "research to production"), ("Live", "stanceinsurance.co.za")]))}

{section("05", "results", "WHERE IT <span class='gold'>LANDED.</span>",
         "A 0→1 product, so the honest framing is “what we can show”, not a before-and-after.",
         facts([("27 → 9", "questions to a quote"), ("4 min", "median time to a price"),
                ("9 of 11", "chose agreed value once they could compare"),
                ("100%", "of testers completed the flow unaided"), ("Live", "in production since launch")])
         + notes([
             ("good", "What testing proved",
              ["Showing agreed value next to market value was the single biggest trust lever. Nine of eleven switched "
               "once they could see both, and every one of them said the comparison was the reason."]),
             ("bad", "What I cannot claim",
              ["I do not have conversion or retention data — I designed and handed over, and the business does not "
                "publish it. Anything I said about revenue here would be invented, so I have left it out."]),
         ]), tint=True)}

{section("06", "honest", "THE <span class='gold'>HONEST BIT.</span>",
         "A 0→1 product with a small team leaves visible seams.",
         honest("What I would do differently", [
             "The modification picker has seven options. Real builds have dozens, and “other” is doing far too much work. It needs a searchable catalogue with underwriter-approved categories behind it.",
             "I tested with owners at car meets, which selects for enthusiasts who are already engaged. The person who fitted one exhaust and does not consider themselves a “car person” is under-represented in my sample.",
             "The claims journey is not designed. The quote is lovely and the moment you actually need the product is a phone number, which is the wrong way round.",
             "Ten weeks meant no dark-mode variant and no proper motion spec. Both are on the list, neither shipped.",
         ]))}

{nextprev(("case-study-tobi-bursary.html", "TOBi &amp; the bursary journey"),
          ("case-study-servicewaze.html", "ServiceWaze — offline-first PWA"))}
  </main>'''

    slug = "case-study-stance"
    out("case-study-stance.html", shell(
        slug=slug,
        title="Stance — insuring South Africa&rsquo;s modified cars | product design case study",
        desc="0→1 product design case study: broker and community research, a pricing model I helped write, a four-step quote flow and a 14-component design system, shipped in ten weeks.",
        og="assets/og/stance.png",
        body=body,
        ld_extra=creative_ld(slug, "Stance — insuring South Africa's modified cars",
                             "Product strategy, UX research and interface design for a niche insurance product.",
                             A + "stance-02-flow.svg", "Product strategy, UX research, interface design")))


if __name__ == "__main__":
    engage(); tobi(); stance()
