/* LulaSync Interactive Animations & Enhancements */
(function() {
  'use strict';

  function initInteractiveAnimations() {
    // 1. 3D Card Tilt & Mouse Radial Glow Effect (all portfolio cards)
    const interactiveCardSelector = [
      '.ls-hover-card',
      '.cs-card',
      '.dailyui-card',
      '.product-card',
      '.service-card',
      '.service',
      '.live-build-card',
      '.who-card',
      '.innov-card',
      '.craft-group-card',
      '.case-study-proof-card',
      '.showcase-card',
      '.creative-card',
      '.tool-card',
      '.auto-card',
      '.agent-card',
      '.cta-card',
      '.bundle-card',
      '.scan-card'
    ].join(', ');

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const interactiveCards = document.querySelectorAll(interactiveCardSelector);
    interactiveCards.forEach(card => {
      // Create glow overlay if not present
      if (!card.querySelector('.card-glow-overlay')) {
        const glow = document.createElement('div');
        glow.className = 'card-glow-overlay';
        card.insertBefore(glow, card.firstChild);
      }

      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
        card.classList.add('is-card-hover');

        if (reduceMotion) return;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = ((y - centerY) / centerY) * -3.5;
        const rotateY = ((x - centerX) / centerX) * 3.5;
        card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-6px)`;
      });

      card.addEventListener('mouseleave', () => {
        card.classList.remove('is-card-hover');
        card.style.transform = '';
      });
    });

    // 2. Button & CTA Click Ripple Effect
    const rippleButtons = document.querySelectorAll('.btn-fire, .btn-outline, .btn-gold-outline, .btn-wa, .show-tab, .filter-tag');
    rippleButtons.forEach(btn => {
      btn.addEventListener('click', function(e) {
        const rect = btn.getBoundingClientRect();
        const circle = document.createElement('span');
        const diameter = Math.max(rect.width, rect.height);
        const radius = diameter / 2;
        circle.style.width = circle.style.height = `${diameter}px`;
        circle.style.left = `${e.clientX - rect.left - radius}px`;
        circle.style.top = `${e.clientY - rect.top - radius}px`;
        circle.classList.add('ls-ripple');
        const ripple = btn.querySelector('.ls-ripple');
        if (ripple) {
          ripple.remove();
        }
        btn.appendChild(circle);
      });
    });

    // 3. Staggered Scroll Reveal
    if ('IntersectionObserver' in window) {
      const revealItems = document.querySelectorAll(
        '.reveal-up, .cs-card, .dailyui-card, .craft-group-card, .live-build-card, .innov-card, .who-card, .case-study-proof-card'
      );
      const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach((entry, idx) => {
          if (entry.isIntersecting) {
            setTimeout(() => {
              entry.target.classList.add('is-visible');
            }, (idx % 4) * 60);
            obs.unobserve(entry.target);
          }
        });
      }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

      revealItems.forEach(el => observer.observe(el));
    }

    // 4. Smooth tab and filter counter updates
    const uiFilters = document.querySelectorAll('[data-uifilter]');
    const uiCards = document.querySelectorAll('#uiGrid .dailyui-card');
    if (uiFilters.length && uiCards.length) {
      uiFilters.forEach(btn => {
        btn.addEventListener('click', () => {
          uiFilters.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          const filter = btn.getAttribute('data-uifilter');
          uiCards.forEach((card, i) => {
            const types = (card.getAttribute('data-uitype') || '').split(' ');
            const match = filter === 'all' || types.includes(filter);
            card.style.display = match ? '' : 'none';
            if (match) {
              card.style.animation = 'none';
              void card.offsetWidth; // trigger reflow
              card.style.animation = `cardIn 0.4s cubic-bezier(0.22,0.61,0.36,1) ${(i % 5) * 0.05}s both`;
            }
          });
        });
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initInteractiveAnimations);
  } else {
    initInteractiveAnimations();
  }
})();
