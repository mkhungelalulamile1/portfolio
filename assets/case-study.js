/* ==========================================================================
   LulaSync — shared case study behaviour
   Theme toggle · mobile nav · reading bar · chapter spy · tabs ·
   before/after sliders · counters · lightbox · scroll reveal
   ========================================================================== */
(function () {
  'use strict';

  var doc = document, root = doc.documentElement;

  /* ── Theme ───────────────────────────────────────────────────────────── */
  function applyTheme(t) {
    root.setAttribute('data-theme', t);
    root.style.colorScheme = t;
    try { localStorage.setItem('ls-theme', t); } catch (e) { }
    doc.querySelectorAll('.theme-toggle').forEach(function (b) {
      b.textContent = t === 'dark' ? '🌙' : '☀️';
      b.setAttribute('aria-label', t === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
    });
  }
  var saved = 'dark';
  try { saved = localStorage.getItem('ls-theme') || 'dark'; } catch (e) { }
  applyTheme(saved);
  doc.addEventListener('click', function (e) {
    var t = e.target.closest('.theme-toggle');
    if (t) applyTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
  });

  /* ── Mobile navigation ───────────────────────────────────────────────── */
  var overlay = doc.getElementById('mobileOverlay');
  function closeMenu() { if (overlay) { overlay.classList.remove('open'); doc.body.style.overflow = ''; } }
  doc.addEventListener('click', function (e) {
    if (e.target.closest('#menuBtn')) { overlay.classList.add('open'); doc.body.style.overflow = 'hidden'; }
    if (e.target.closest('#closeBtn') || (overlay && overlay.classList.contains('open') && e.target.closest('.mobile-nav-link'))) closeMenu();
  });
  doc.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });

  /* ── Reading progress ────────────────────────────────────────────────── */
  var bar = doc.querySelector('.read-bar');
  if (bar) {
    var tick = function () {
      var h = doc.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? Math.min(100, (window.scrollY / h) * 100) : 0) + '%';
    };
    window.addEventListener('scroll', tick, { passive: true });
    window.addEventListener('resize', tick);
    tick();
  }

  /* ── Chapter scroll-spy ──────────────────────────────────────────────── */
  var chapterLinks = Array.prototype.slice.call(doc.querySelectorAll('.chapter-link'));
  if (chapterLinks.length) {
    var targets = chapterLinks
      .map(function (l) { return doc.querySelector(l.getAttribute('href')); })
      .filter(Boolean);
    var spy = function () {
      var y = window.scrollY + 160, current = 0;
      targets.forEach(function (t, i) { if (t.offsetTop <= y) current = i; });
      chapterLinks.forEach(function (l, i) { l.classList.toggle('active', i === current); });
    };
    window.addEventListener('scroll', spy, { passive: true });
    spy();
  }

  /* ── Tab groups: [data-tabs] wrapper > .tab-btn[data-pane] + .tab-pane[data-pane] ── */
  doc.querySelectorAll('[data-tabs]').forEach(function (group) {
    var btns = group.querySelectorAll('.tab-btn');
    var panes = group.querySelectorAll('.tab-pane');
    btns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var id = btn.getAttribute('data-pane');
        btns.forEach(function (b) { b.classList.toggle('active', b === btn); b.setAttribute('aria-selected', b === btn); });
        panes.forEach(function (p) { p.classList.toggle('active', p.getAttribute('data-pane') === id); });
      });
    });
  });

  /* ── Before / after sliders ──────────────────────────────────────────── */
  doc.querySelectorAll('.ba').forEach(function (ba) {
    var layer = ba.querySelector('.after-layer');
    var handle = ba.querySelector('.ba-handle');
    if (!layer || !handle) return;
    var img = layer.querySelector('img');
    function size() { if (img) img.style.width = ba.clientWidth + 'px'; }
    function set(pct) {
      pct = Math.max(2, Math.min(98, pct));
      layer.style.width = pct + '%';
      handle.style.left = pct + '%';
    }
    function fromEvent(e) {
      var rect = ba.getBoundingClientRect();
      var x = (e.touches ? e.touches[0].clientX : e.clientX) - rect.left;
      set((x / rect.width) * 100);
    }
    var dragging = false;
    handle.addEventListener('pointerdown', function (e) { dragging = true; handle.setPointerCapture(e.pointerId); });
    handle.addEventListener('pointerup', function () { dragging = false; });
    ba.addEventListener('pointermove', function (e) { if (dragging) fromEvent(e); });
    ba.addEventListener('click', function (e) { if (!e.target.closest('.ba-handle')) fromEvent(e); });
    handle.setAttribute('tabindex', '0');
    handle.setAttribute('role', 'slider');
    handle.setAttribute('aria-label', 'Compare before and after');
    handle.addEventListener('keydown', function (e) {
      var cur = parseFloat(layer.style.width) || 50;
      if (e.key === 'ArrowLeft') { set(cur - 4); e.preventDefault(); }
      if (e.key === 'ArrowRight') { set(cur + 4); e.preventDefault(); }
    });
    window.addEventListener('resize', size);
    size(); set(50);
    if (img && !img.complete) img.addEventListener('load', size);
  });

  /* ── Animated counters: <b data-count="25000" data-suffix="+"> ───────── */
  var counters = doc.querySelectorAll('[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    var cObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, end = parseFloat(el.getAttribute('data-count'));
        var suffix = el.getAttribute('data-suffix') || '', dec = (end % 1 !== 0) ? 1 : 0;
        var start = performance.now(), dur = 1100;
        function step(now) {
          var p = Math.min(1, (now - start) / dur), eased = 1 - Math.pow(1 - p, 3);
          var val = end * eased;
          el.textContent = (end >= 1000 ? Math.round(val).toLocaleString('en-ZA') : val.toFixed(dec)) + suffix;
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
        cObs.unobserve(el);
      });
    }, { threshold: .4 });
    counters.forEach(function (c) { cObs.observe(c); });
  }

  /* ── Lightbox for .zoomable images ───────────────────────────────────── */
  var zoomables = doc.querySelectorAll('img.zoomable');
  if (zoomables.length) {
    var lb = doc.createElement('div');
    lb.className = 'lightbox';
    lb.innerHTML = '<button type="button" aria-label="Close">✕</button><img alt="" /><p class="lb-cap"></p>';
    doc.body.appendChild(lb);
    var lbImg = lb.querySelector('img'), lbCap = lb.querySelector('.lb-cap');
    function closeLb() { lb.classList.remove('open'); doc.body.style.overflow = ''; }
    zoomables.forEach(function (i) {
      i.addEventListener('click', function () {
        lbImg.src = i.currentSrc || i.src;
        lbImg.alt = i.alt;
        var figEl = i.closest('figure');
        var cap = figEl ? (figEl.querySelector('figcaption span:not(.zoom-hint)') || figEl.querySelector('figcaption')) : null;
        lbCap.textContent = cap ? cap.textContent.trim() : i.alt;
        lb.classList.add('open');
        doc.body.style.overflow = 'hidden';
      });
    });
    lb.querySelector('button').addEventListener('click', closeLb);
    lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeLb(); });
  }

  /* ── Scroll reveal ───────────────────────────────────────────────────── */
  var reveals = doc.querySelectorAll('.reveal');
  if (reveals.length && 'IntersectionObserver' in window) {
    var rObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); rObs.unobserve(en.target); } });
    }, { threshold: .12, rootMargin: '0px 0px -40px' });
    reveals.forEach(function (r) { rObs.observe(r); });
  } else {
    reveals.forEach(function (r) { r.classList.add('in'); });
  }

  /* ── Current year ────────────────────────────────────────────────────── */
  doc.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();

/* ==========================================================================
   v2 — story layer behaviour
   Step rails · segmented switches · hub tabs · chat · calculator ·
   status board · token playground · IA path visualiser · live vitals
   ========================================================================== */
(function () {
  'use strict';
  var doc = document;
  var $ = function (s, r) { return (r || doc).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); };

  /* ── Step rails ──────────────────────────────────────────────────────── */
  $$('[data-rail]').forEach(function (rail) {
    var steps = $$('.rail-step', rail), panes = $$('.rail-pane', rail);
    function show(id) {
      steps.forEach(function (s) { var on = s.dataset.step === id; s.classList.toggle('on', on); s.setAttribute('aria-selected', on); });
      panes.forEach(function (p) { p.classList.toggle('on', p.dataset.step === id); });
    }
    steps.forEach(function (s) {
      s.addEventListener('click', function () { show(s.dataset.step); });
      s.addEventListener('keydown', function (e) {
        var i = steps.indexOf(s);
        if (e.key === 'ArrowDown' || e.key === 'ArrowRight') { e.preventDefault(); steps[(i + 1) % steps.length].focus(); steps[(i + 1) % steps.length].click(); }
        if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { e.preventDefault(); steps[(i - 1 + steps.length) % steps.length].focus(); steps[(i - 1 + steps.length) % steps.length].click(); }
      });
    });
    if (steps.length) show(steps[0].dataset.step);
  });

  /* ── Segmented switches: .seg button[data-seg] toggles [data-segview] ─── */
  $$('[data-segs]').forEach(function (group) {
    var btns = $$('.seg button', group);
    var views = $$('[data-segview]', group);
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        btns.forEach(function (x) { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b); });
        views.forEach(function (v) { v.hidden = v.dataset.segview !== b.dataset.seg; });
        group.dispatchEvent(new CustomEvent('segchange', { detail: b.dataset.seg }));
      });
    });
  });

  /* ── Work-hub tabs (also reflected in the URL hash) ──────────────────── */
  (function () {
    var tabs = $$('.hub-tab'); if (!tabs.length) return;
    var panels = $$('.hub-panel');
    function open(id, push) {
      tabs.forEach(function (t) { var on = t.dataset.panel === id; t.classList.toggle('on', on); t.setAttribute('aria-selected', on); });
      panels.forEach(function (p) { p.classList.toggle('on', p.id === 'panel-' + id); });
      if (push && history.replaceState) history.replaceState(null, '', '#' + id);
    }
    tabs.forEach(function (t) { t.addEventListener('click', function () { open(t.dataset.panel, true); }); });
    var start = (location.hash || '').replace('#', '');
    open(tabs.some(function (t) { return t.dataset.panel === start; }) ? start : tabs[0].dataset.panel, false);
    window.addEventListener('hashchange', function () {
      var h = location.hash.replace('#', '');
      if (tabs.some(function (t) { return t.dataset.panel === h; })) open(h, false);
    });
  })();

  /* ── Filter chips inside the hub ─────────────────────────────────────── */
  $$('[data-filters]').forEach(function (wrap) {
    var target = doc.getElementById(wrap.dataset.filters);
    if (!target) return;
    var btns = $$('button', wrap);
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        btns.forEach(function (x) { x.classList.toggle('on', x === b); });
        var f = b.dataset.filter;
        $$('[data-tags]', target).forEach(function (c) {
          c.hidden = !(f === 'all' || (c.dataset.tags || '').split(' ').indexOf(f) > -1);
        });
      });
    });
  });

  /* ── TOBi chat demo ──────────────────────────────────────────────────── */
  (function () {
    var host = $('#tobiChat'); if (!host) return;
    var log = $('.chat', host), asks = $('.chat-asks', host);
    var mode = 'after';
    var script = {
      before: {
        greet: ['Hi! I\u2019m TOBi. How can I help you today?'],
        bursary: ['Sorry, I didn\u2019t get that. You can ask me about airtime, data or billing.'],
        eligible: ['Sorry, I didn\u2019t get that. Type \u201Cagent\u201D to speak to someone.'],
        status: ['Sorry, I didn\u2019t get that. Type \u201Cagent\u201D to speak to someone.'],
        docs: ['Sorry, I didn\u2019t get that. You can ask me about airtime, data or billing.']
      },
      after: {
        greet: ['Sawubona. I can check bursary eligibility, track an application, or explain what documents you need. Which one?'],
        bursary: ['I can help with that. Quick question first \u2014 are you a current employee, or applying from outside?', 'Employee \u00B7 Outside applicant'],
        eligible: ['You qualify if you have worked here 12 months and passed your last review. Shall I check your record?'],
        status: ['REQ-24817 is with the panel. It moved on Tuesday. Decisions for this round go out on 30 September \u2014 I\u2019ll push you a notification.'],
        docs: ['Three things: your ID, your latest academic record, and a quote from the institution. Photos from your phone are fine, 8 MB each.']
      }
    };
    var qs = [
      ['bursary', 'I need help with my bursary'],
      ['eligible', 'Am I eligible?'],
      ['status', 'Where is my application?'],
      ['docs', 'What documents do I need?']
    ];
    function bubble(cls, txt, meta) {
      var d = doc.createElement('div');
      d.className = 'bub ' + cls;
      d.textContent = txt;
      if (meta) { var m = doc.createElement('span'); m.className = 'meta'; m.textContent = meta; d.appendChild(m); }
      log.appendChild(d);
      log.scrollTop = log.scrollHeight;
      return d;
    }
    function typing() {
      var d = doc.createElement('div');
      d.className = 'bub bot';
      d.innerHTML = '<span class="typing"><i></i><i></i><i></i></span>';
      log.appendChild(d); log.scrollTop = log.scrollHeight;
      return d;
    }
    function reset() {
      log.innerHTML = '';
      bubble('bot', script[mode].greet[0], mode === 'before' ? 'The bot as I found it' : 'The rewritten opening');
    }
    function ask(key, label) {
      bubble('me', label);
      var t = typing();
      setTimeout(function () {
        t.remove();
        bubble('bot', script[mode][key][0], mode === 'before' ? 'Dead end \u2014 no next move offered' : 'Answers, then offers the next move');
      }, 620);
    }
    qs.forEach(function (q) {
      var b = doc.createElement('button');
      b.type = 'button'; b.textContent = q[1];
      b.addEventListener('click', function () { ask(q[0], q[1]); });
      asks.appendChild(b);
    });
    host.addEventListener('segchange', function (e) { mode = e.detail; reset(); });
    reset();
  })();

  /* ── Stance quote calculator ─────────────────────────────────────────── */
  (function () {
    var host = $('#stanceCalc'); if (!host) return;
    var base = 942;
    function render() {
      var mods = $$('input[type=checkbox]:checked', host);
      var modCost = 0, modValue = 0;
      mods.forEach(function (m) { modCost += +m.dataset.cost; modValue += +m.dataset.value; });
      var track = $('#trackDay', host) && $('#trackDay', host).checked ? 56 : 0;
      var total = base + modCost + track;
      // What the same car costs elsewhere, where declared mods are loaded hard
      var elsewhere = Math.round(base * 1.10 + modCost * 1.8 + track);
      $('#qTotal', host).textContent = 'R' + total.toLocaleString('en-ZA');
      $('#qBase', host).textContent = 'R' + base;
      $('#qMods', host).textContent = 'R' + modCost;
      $('#qTrack', host).textContent = track ? 'R' + track : 'not added';
      $('#qValue', host).textContent = 'R' + (385000 + modValue).toLocaleString('en-ZA');
      $('#qCount', host).textContent = mods.length + (mods.length === 1 ? ' modification' : ' modifications');
      var saving = elsewhere - total;
      $('#qSaving', host).textContent = mods.length
        ? 'R' + saving.toLocaleString('en-ZA') + ' a month less than the same cover priced the way the market loads modifications \u2014 and every part above is named on the schedule.'
        : 'Nothing declared yet. Tick what is fitted \u2014 declaring it is what makes it covered.';
    }
    $$('input', host).forEach(function (i) { i.addEventListener('change', render); });
    render();
  })();

  /* ── ServiceWaze status board ────────────────────────────────────────── */
  (function () {
    var host = $('#swBoard'); if (!host) return;
    var body = $('#swBody', host), note = $('#swNote', host), badge = $('#swBadge', host);
    var rows = [
      ['Electricity', 'Stage 2 from 18:00', 'warn'],
      ['Water', 'No interruptions', 'good'],
      ['Air quality', 'Moderate \u00B7 62 AQI', 'warn'],
      ['Transport', 'Gautrain on time', 'good'],
      ['Weather', '21\u00B0C, clearing', 'good']
    ];
    var colour = { good: 'var(--good)', warn: 'var(--gold)', bad: 'var(--fire)', off: 'var(--border)' };
    function paint(state) {
      body.innerHTML = '';
      badge.textContent = { fresh: 'live', stale: '4 min old', offline: 'no network', loading: 'fetching', partial: '3 of 5 sources', empty: 'no suburb yet' }[state];
      badge.style.color = state === 'offline' ? 'var(--fire)' : state === 'fresh' ? 'var(--good)' : 'var(--gold)';
      if (state === 'loading') {
        for (var i = 0; i < 5; i++) {
          var r = doc.createElement('div'); r.className = 'board-row';
          r.innerHTML = '<div class="skel" style="width:' + (34 + i * 6) + '%"></div>';
          body.appendChild(r);
        }
        note.textContent = 'Skeletons match the height of the real rows, so nothing jumps when data lands.';
        note.style.color = 'var(--dim)';
        return;
      }
      if (state === 'empty') {
        body.innerHTML = '<div style="padding:34px 16px;text-align:center"><p style="font-size:.86rem;color:var(--dim);margin-bottom:14px">Pick a suburb to start.</p><button class="btn btn-primary" type="button">Use my location</button></div>';
        note.textContent = 'An empty state with one obvious action beats a spinner that never resolves.';
        note.style.color = 'var(--dim)';
        return;
      }
      rows.forEach(function (r, i) {
        var off = (state === 'offline' && i > 0) || (state === 'partial' && i > 2);
        var el = doc.createElement('div');
        el.className = 'board-row' + (off ? ' off' : '');
        var st = off ? 'off' : r[2];
        var val = off ? (state === 'offline' ? 'Not available offline' : 'Source timed out') : r[1];
        if (state === 'offline' && i === 0) val = 'Last seen 22 min ago';
        el.innerHTML = '<span class="dot" style="background:' + colour[st] + '"></span><span class="nm">' + r[0] + '</span><span class="vl">' + val + '</span>';
        body.appendChild(el);
      });
      var notes = {
        fresh: ['Fetched 40 seconds ago. Shown plainly, no qualifier needed.', 'var(--good)'],
        stale: ['Shown from cache and labelled. Tap to refresh \u2014 never a silent old number.', 'var(--gold)'],
        offline: ['You are offline. This is what we last knew, and when.', 'var(--fire)'],
        partial: ['2 sources timed out. The other 3 still render \u2014 partial beats blank.', 'var(--gold)']
      };
      note.textContent = notes[state][0];
      note.style.color = notes[state][1];
    }
    host.addEventListener('segchange', function (e) { paint(e.detail); });
    paint('fresh');
  })();

  /* ── Token playground ────────────────────────────────────────────────── */
  (function () {
    var host = $('#tokenPlay'); if (!host) return;
    var out = $('.play-out', host);
    var state = { accent: '#F0A500', radius: 10, space: 16 };
    function apply() {
      out.style.setProperty('--t-accent', state.accent);
      out.style.setProperty('--t-radius', state.radius + 'px');
      out.style.setProperty('--t-space', state.space + 'px');
      $$('.pv-btn, .pv-chip', out).forEach(function (el) {
        el.style.background = state.accent; el.style.borderRadius = state.radius + 'px'; el.style.color = '#0A0705';
      });
      $$('.pv-card', out).forEach(function (el) {
        el.style.borderRadius = state.radius + 'px'; el.style.padding = state.space + 'px';
      });
      $('.play-code', host).innerHTML =
        'action.primary: <b>' + state.accent + '</b>\nradius.md:      <b>' + state.radius + 'px</b>\nspace.md:       <b>' + state.space + 'px</b>\n\n/* 3 tokens changed \u2192 ' + $$('.pv-btn, .pv-chip, .pv-card', out).length + ' component instances restyled, 0 files edited */';
    }
    $$('.swatches button', host).forEach(function (b) {
      b.style.background = b.dataset.colour;
      b.addEventListener('click', function () {
        $$('.swatches button', host).forEach(function (x) { x.classList.toggle('on', x === b); });
        state.accent = b.dataset.colour; apply();
      });
    });
    var r = $('#tRadius', host), s = $('#tSpace', host);
    if (r) r.addEventListener('input', function () { state.radius = +r.value; apply(); });
    if (s) s.addEventListener('input', function () { state.space = +s.value; apply(); });
    apply();
  })();

  /* ── IA path visualiser ──────────────────────────────────────────────── */
  (function () {
    var host = $('#iaPaths'); if (!host) return;
    var tasks = {
      payslip: {
        old: [['Home \u2014 scan 11 tiles', ''], ['Tap \u201CSelf Help\u201D', 'wrong'], ['Back', 'wrong'], ['Tap \u201CHR Zone\u201D', ''], ['Scroll past 9 links', ''], ['Documents \u2192 Payslip', 'done']],
        neu: [['Today \u2014 quick tiles', ''], ['Tap \u201CPayslip\u201D', 'done']],
        oldT: '52 seconds \u00B7 2 wrong turns', newT: '11 seconds \u00B7 0 wrong turns'
      },
      leave: {
        old: [['Home \u2014 scan 11 tiles', ''], ['Tap \u201CServices\u201D', 'wrong'], ['Back', 'wrong'], ['Tap \u201CTools\u201D', 'wrong'], ['Search \u201Cleave\u201D', ''], ['Apply for leave', 'done']],
        neu: [['Do', ''], ['Apply for leave', 'done']],
        oldT: '61 seconds \u00B7 3 wrong turns', newT: '14 seconds \u00B7 0 wrong turns'
      },
      claim: {
        old: [['Home \u2014 scan 11 tiles', ''], ['Tap \u201CCorporate\u201D', 'wrong'], ['Back', 'wrong'], ['Tap \u201CMore\u201D', ''], ['Finance \u2192 Forms', ''], ['Travel claim', 'done']],
        neu: [['Do', ''], ['Claim travel', 'done']],
        oldT: '48 seconds \u00B7 2 wrong turns', newT: '13 seconds \u00B7 0 wrong turns'
      },
      status: {
        old: [['Home \u2014 scan 11 tiles', ''], ['No status anywhere', 'wrong'], ['Phone the service desk', 'wrong']],
        neu: [['Today \u2014 \u201CIn progress\u201D', ''], ['Open the claim timeline', 'done']],
        oldT: 'Not possible in the app', newT: '6 seconds \u00B7 0 wrong turns'
      }
    };
    function draw(key) {
      var t = tasks[key];
      function list(items) {
        return items.map(function (i, n) {
          return '<li class="' + i[1] + '" style="animation-delay:' + (n * 90) + 'ms">' + i[0] + '</li>';
        }).join('');
      }
      $('#pathOld ol', host).innerHTML = list(t.old);
      $('#pathNew ol', host).innerHTML = list(t.neu);
      $('#pathOld .path-foot', host).textContent = t.oldT;
      $('#pathNew .path-foot', host).textContent = t.newT;
    }
    var btns = $$('.seg button', host);
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        btns.forEach(function (x) { x.classList.toggle('on', x === b); });
        draw(b.dataset.task);
      });
    });
    draw('payslip');
  })();

  /* ── Live Core Web Vitals of the page you are reading ────────────────── */
  (function () {
    var host = $('#liveVitals'); if (!host) return;
    function set(id, val, unit, good, poor) {
      var el = doc.getElementById(id); if (!el) return;
      var v = el.querySelector('.v');
      v.textContent = (unit === 'ms' ? Math.round(val) : val.toFixed(unit === '' ? 3 : 2)) + unit;
      v.className = 'v' + (val <= good ? '' : val <= poor ? ' warn' : ' bad');
    }
    try {
      var nav = performance.getEntriesByType('navigation')[0];
      if (nav) set('vTTFB', nav.responseStart - nav.requestStart, 'ms', 200, 500);
      new PerformanceObserver(function (l) {
        var e = l.getEntries();
        set('vLCP', e[e.length - 1].startTime, 'ms', 2500, 4000);
      }).observe({ type: 'largest-contentful-paint', buffered: true });
      new PerformanceObserver(function (l) {
        l.getEntries().forEach(function (e) {
          if (e.name === 'first-contentful-paint') set('vFCP', e.startTime, 'ms', 1800, 3000);
        });
      }).observe({ type: 'paint', buffered: true });
      var cls = 0;
      new PerformanceObserver(function (l) {
        l.getEntries().forEach(function (e) { if (!e.hadRecentInput) cls += e.value; });
        set('vCLS', cls, '', 0.1, 0.25);
      }).observe({ type: 'layout-shift', buffered: true });
      var w = performance.getEntriesByType('resource').reduce(function (a, r) { return a + (r.transferSize || 0); }, 0);
      set('vWeight', (w + (nav ? nav.transferSize || 0 : 0)) / 1024, ' KB', 400, 1000);
    } catch (err) {
      host.querySelectorAll('.v').forEach(function (v) { v.textContent = 'n/a'; });
    }
  })();

  /* ── Copy-to-clipboard ───────────────────────────────────────────────── */
  $$('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      navigator.clipboard && navigator.clipboard.writeText(b.dataset.copy).then(function () {
        var t = b.textContent; b.textContent = 'Copied'; setTimeout(function () { b.textContent = t; }, 1400);
      });
    });
  });
})();
