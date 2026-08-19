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
        var cap = i.closest('figure') ? i.closest('figure').querySelector('figcaption') : null;
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
