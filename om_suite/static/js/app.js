(function () {
  var sidebar = document.getElementById('sidebar'), scrim = document.getElementById('scrim'),
      menuBtn = document.getElementById('menuBtn');
  function toggle(open) {
    if (!sidebar) return;
    sidebar.classList.toggle('open', open);
    scrim.classList.toggle('show', open);
  }
  if (menuBtn) menuBtn.addEventListener('click', function () { toggle(!sidebar.classList.contains('open')); });
  if (scrim) scrim.addEventListener('click', function () { toggle(false); });
  if (sidebar) sidebar.addEventListener('click', function (e) {
    if (e.target.closest('a')) toggle(false);
  });

  // user menu: close on outside click / Esc
  var um = document.getElementById('userMenu');
  document.addEventListener('click', function (e) { if (um && um.open && !um.contains(e.target)) um.open = false; });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && um) um.open = false; });

  // confirm dialogs: <button data-confirm="...">
  document.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('[data-confirm]') : null;
    if (b && !window.confirm(b.getAttribute('data-confirm'))) e.preventDefault();
  });

  // auto-hide plain success flashes
  setTimeout(function () {
    document.querySelectorAll('.flash.ok').forEach(function (f) { f.style.display = 'none'; });
  }, 6000);

  if ('serviceWorker' in navigator) navigator.serviceWorker.register('/sw.js').catch(function () {});
})();
