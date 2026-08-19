/* ==========================================================================
   LulaSync — measurement layer
   Privacy-first, cookie-free by default, consent-aware.

   What it does
     1. Buffers events in window.dataLayer so any tool (GA4, Plausible,
        Umami, a self-hosted endpoint) can be attached later without
        touching the markup again.
     2. Tracks declaratively: add data-track="name" to any element, plus
        optional data-track-* attributes for properties. No inline handlers.
     3. Measures the three Core Web Vitals that Google ranks on
        (LCP, CLS, INP) with the native PerformanceObserver — no library.
     4. Tracks scroll depth, outbound links, file downloads, WhatsApp and
        email intents, and case-study reading depth.
     5. Sends nothing until consent is granted when ANALYTICS_REQUIRES_CONSENT
        is true. Until then, events queue in memory only.

   Wire-up: set window.LS_ANALYTICS_ENDPOINT (or plug GA4/Plausible into
   flush()) and the whole site is instrumented.
   ========================================================================== */
(function () {
  'use strict';

  var CONSENT_KEY = 'ls-analytics-consent';
  var ANALYTICS_REQUIRES_CONSENT = true;
  var SESSION = Math.random().toString(36).slice(2, 10);

  window.dataLayer = window.dataLayer || [];
  var queue = [];

  function consentGranted() {
    if (!ANALYTICS_REQUIRES_CONSENT) return true;
    try { return localStorage.getItem(CONSENT_KEY) === 'granted'; } catch (e) { return false; }
  }

  function flush() {
    if (!consentGranted() || !queue.length) return;
    var endpoint = window.LS_ANALYTICS_ENDPOINT;
    var batch = queue.splice(0, queue.length);
    if (!endpoint) return;                       // nothing attached yet: drop, do not store
    try {
      var body = JSON.stringify({ session: SESSION, events: batch });
      if (navigator.sendBeacon) navigator.sendBeacon(endpoint, body);
      else fetch(endpoint, { method: 'POST', body: body, keepalive: true, headers: { 'Content-Type': 'application/json' } });
    } catch (e) { /* never break the page for a metric */ }
  }

  function track(name, props) {
    var evt = Object.assign({
      event: name,
      page: location.pathname,
      title: document.title,
      ts: Date.now()
    }, props || {});
    window.dataLayer.push(evt);
    queue.push(evt);
    if (window.LS_ANALYTICS_DEBUG) console.log('[track]', evt);
    flush();
  }
  window.lsTrack = track;

  /* ── 1. Declarative click tracking ─────────────────────────────────── */
  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-track]');
    if (el) {
      var props = {};
      for (var i = 0; i < el.attributes.length; i++) {
        var a = el.attributes[i];
        if (a.name.indexOf('data-track-') === 0) props[a.name.slice(11)] = a.value;
      }
      track(el.getAttribute('data-track'), props);
      return;
    }
    var link = e.target.closest('a[href]');
    if (!link) return;
    var href = link.getAttribute('href') || '';
    if (/^https?:/i.test(href) && link.hostname !== location.hostname) {
      track('outbound_click', { url: href, text: (link.textContent || '').trim().slice(0, 60) });
    } else if (/^(wa\.me|https:\/\/wa\.me)/i.test(href) || href.indexOf('wa.me') > -1) {
      track('whatsapp_intent', { url: href });
    } else if (href.indexOf('mailto:') === 0) {
      track('email_intent', { url: href });
    } else if (/\.(pdf|zip|docx?|pptx?)$/i.test(href)) {
      track('file_download', { url: href });
    }
  }, { passive: true });

  /* ── 2. Scroll depth (25 / 50 / 75 / 100) ──────────────────────────── */
  (function () {
    var marks = [25, 50, 75, 100], hit = {};
    function check() {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      if (h <= 0) return;
      var pct = (window.scrollY / h) * 100;
      marks.forEach(function (m) {
        if (pct >= m && !hit[m]) { hit[m] = 1; track('scroll_depth', { depth: m }); }
      });
    }
    window.addEventListener('scroll', check, { passive: true });
  })();

  /* ── 3. Engagement time (only counts while the tab is visible) ─────── */
  (function () {
    var start = Date.now(), engaged = 0;
    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState === 'hidden') { engaged += Date.now() - start; }
      else { start = Date.now(); }
    });
    addEventListener('pagehide', function () {
      engaged += Date.now() - start;
      track('engaged_time', { seconds: Math.round(engaged / 1000) });
      flush();
    });
  })();

  /* ── 4. Core Web Vitals: LCP, CLS, INP ─────────────────────────────── */
  (function () {
    if (!('PerformanceObserver' in window)) return;

    function rate(metric, value) {
      var t = { LCP: [2500, 4000], CLS: [0.1, 0.25], INP: [200, 500] }[metric];
      return value <= t[0] ? 'good' : value <= t[1] ? 'needs-improvement' : 'poor';
    }

    // Largest Contentful Paint
    try {
      var lcp = 0;
      new PerformanceObserver(function (list) {
        var entries = list.getEntries();
        lcp = entries[entries.length - 1].startTime;
      }).observe({ type: 'largest-contentful-paint', buffered: true });
      addEventListener('pagehide', function () {
        if (lcp) track('web_vital', { metric: 'LCP', value: Math.round(lcp), rating: rate('LCP', lcp) });
      });
    } catch (e) { }

    // Cumulative Layout Shift
    try {
      var cls = 0;
      new PerformanceObserver(function (list) {
        list.getEntries().forEach(function (entry) {
          if (!entry.hadRecentInput) cls += entry.value;
        });
      }).observe({ type: 'layout-shift', buffered: true });
      addEventListener('pagehide', function () {
        track('web_vital', { metric: 'CLS', value: Math.round(cls * 1000) / 1000, rating: rate('CLS', cls) });
      });
    } catch (e) { }

    // Interaction to Next Paint (worst interaction)
    try {
      var inp = 0;
      new PerformanceObserver(function (list) {
        list.getEntries().forEach(function (entry) {
          if (entry.interactionId && entry.duration > inp) inp = entry.duration;
        });
      }).observe({ type: 'event', buffered: true, durationThreshold: 40 });
      addEventListener('pagehide', function () {
        if (inp) track('web_vital', { metric: 'INP', value: Math.round(inp), rating: rate('INP', inp) });
      });
    } catch (e) { }

    // Time to First Byte, from the navigation entry
    addEventListener('load', function () {
      var nav = (performance.getEntriesByType ? performance.getEntriesByType : function () { return []; })('navigation')[0];
      if (nav) track('web_vital', { metric: 'TTFB', value: Math.round(nav.responseStart), rating: nav.responseStart < 800 ? 'good' : 'needs-improvement' });
    });
  })();

  /* ── 5. Case-study reading depth (chapter in view) ─────────────────── */
  (function () {
    var chapters = document.querySelectorAll('.cs-section[id]');
    if (!chapters.length || !('IntersectionObserver' in window)) return;
    var seen = {};
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && !seen[en.target.id]) {
          seen[en.target.id] = 1;
          track('chapter_view', { chapter: en.target.id });
        }
      });
    }, { threshold: 0.35 });
    chapters.forEach(function (c) { obs.observe(c); });
  })();

  /* ── 6. Consent helpers (call from a banner or a settings link) ────── */
  window.lsConsent = {
    grant: function () { try { localStorage.setItem(CONSENT_KEY, 'granted'); } catch (e) { } track('consent_granted'); flush(); },
    revoke: function () { try { localStorage.setItem(CONSENT_KEY, 'denied'); } catch (e) { } queue.length = 0; },
    status: function () { try { return localStorage.getItem(CONSENT_KEY) || 'unset'; } catch (e) { return 'unset'; } }
  };

  track('page_view', { referrer: document.referrer || '(direct)' });
})();
