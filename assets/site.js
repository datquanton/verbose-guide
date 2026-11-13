/* theme switch shared by every page; the choice is remembered on this device when storage is available */
(function () {
  var r = document.documentElement, b = document.querySelector('button.theme');
  if (!b) return;
  b.addEventListener('click', function () {
    var d = r.getAttribute('data-theme');
    var dark = d ? d === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    r.setAttribute('data-theme', dark ? 'light' : 'dark');
    try { localStorage.setItem('theme', dark ? 'light' : 'dark'); } catch (e) {}
  });
})();
