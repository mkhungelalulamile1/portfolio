(function () {
  'use strict';
  function mount() {
    if (document.getElementById('ls-chat-fab')) return;

    var style = document.createElement('style');
    style.textContent = `
      #ls-chat-fab{position:fixed;right:max(18px,env(safe-area-inset-right));bottom:max(18px,env(safe-area-inset-bottom));z-index:550;width:48px;height:48px;border:1px solid rgba(240,165,0,.45);border-radius:50%;background:linear-gradient(135deg,var(--gold,#F0A500),var(--fire,#E04E14));color:#080604;display:grid;place-items:center;cursor:pointer;box-shadow:0 10px 30px rgba(0,0,0,.28);font-size:20px;transition:transform .2s,box-shadow .2s}
      #ls-chat-fab:hover{transform:translateY(-2px);box-shadow:0 14px 34px rgba(0,0,0,.36)}
      #ls-chat-fab:focus-visible{outline:2px solid var(--gold,#F0A500);outline-offset:3px}
      #ls-chat-panel{position:fixed;right:max(18px,env(safe-area-inset-right));bottom:78px;z-index:550;width:min(330px,calc(100vw - 36px));padding:16px;border:1px solid var(--border,#1a1a1a);border-radius:16px;background:var(--card,#0f0f0f);color:var(--paper,#F5EDD8);box-shadow:0 22px 60px rgba(0,0,0,.35);opacity:0;pointer-events:none;transform:translateY(8px) scale(.98);transition:opacity .2s,transform .2s}
      #ls-chat-panel.open{opacity:1;pointer-events:auto;transform:none}
      [data-theme="light"] #ls-chat-panel{background:#fff;border-color:#E0D8C8;color:#1a1208}
      .ls-chat-title{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:6px;font-weight:800;font-size:.92rem}
      .ls-chat-close{border:0;background:none;color:var(--dim,#777);font-size:1rem;cursor:pointer;padding:2px 4px}
      .ls-chat-copy{color:var(--dim,#777);font-size:.78rem;line-height:1.55;margin-bottom:12px}
      .ls-chat-links{display:grid;gap:8px}.ls-chat-links a{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:10px 12px;border-radius:10px;border:1px solid var(--border,#1a1a1a);color:var(--paper,#F5EDD8);text-decoration:none;font-size:.78rem;font-weight:700}.ls-chat-links a:hover{border-color:var(--gold,#F0A500);color:var(--gold,#F0A500)}
      [data-theme="light"] .ls-chat-links a{color:#1a1208;border-color:#E0D8C8}.ls-chat-links a.primary{background:var(--gold,#F0A500);border-color:var(--gold,#F0A500);color:#080604}.ls-chat-links a.primary:hover{color:#080604;opacity:.9}
      @media (prefers-reduced-motion:reduce){#ls-chat-fab,#ls-chat-panel{transition:none}}
    `;
    document.head.appendChild(style);

    var fab = document.createElement('button');
    fab.id = 'ls-chat-fab';
    fab.type = 'button';
    fab.setAttribute('aria-label', 'Open LulaSync contact options');
    fab.setAttribute('aria-expanded', 'false');
    fab.textContent = '💬';

    var panel = document.createElement('div');
    panel.id = 'ls-chat-panel';
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', 'Contact LulaSync');
    panel.innerHTML = '<div class="ls-chat-title"><span>Talk to Lulamile</span><button class="ls-chat-close" type="button" aria-label="Close contact options">✕</button></div>' +
      '<p class="ls-chat-copy">Tell me what you are trying to improve. I will point you to the right next step.</p>' +
      '<div class="ls-chat-links"><a class="primary" href="./contact.html">Start an enquiry <span>→</span></a>' +
      '<a href="mailto:mkhungela.l@gmail.com?subject=Enquiry%20about%20your%20services">Email me <span>↗</span></a>' +
      '<a href="https://www.linkedin.com/in/lulamile-mkhungela/" target="_blank" rel="noopener noreferrer">LinkedIn <span>↗</span></a></div>';

    document.body.appendChild(fab);
    document.body.appendChild(panel);

    function setOpen(open) {
      panel.classList.toggle('open', open);
      fab.setAttribute('aria-expanded', open ? 'true' : 'false');
      fab.textContent = open ? '✕' : '💬';
    }
    fab.addEventListener('click', function () { setOpen(!panel.classList.contains('open')); });
    panel.querySelector('.ls-chat-close').addEventListener('click', function () { setOpen(false); });
    document.addEventListener('keydown', function (event) { if (event.key === 'Escape') setOpen(false); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})();
