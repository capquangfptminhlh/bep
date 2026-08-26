from pathlib import Path
import re

SITE = Path('_site')

SWITCH = r'''
<div class="language-switcher" id="languageSwitcher" aria-label="Language selector">
  <button type="button" class="lang-btn is-active" data-lang="vi" aria-label="Tiếng Việt">VI</button>
  <span class="lang-sep">/</span>
  <button type="button" class="lang-btn" data-lang="en" aria-label="English">EN</button>
</div>
<script id="language-switcher-script">
(function(){
  const box=document.getElementById('languageSwitcher');
  if(!box) return;
  const vi=box.querySelector('[data-lang="vi"]');
  const en=box.querySelector('[data-lang="en"]');
  const cleanUrl=window.location.href.split('#')[0].split('?')[0];
  vi.addEventListener('click',function(){ window.location.href=cleanUrl; });
  en.addEventListener('click',function(){
    const translated='https://translate.google.com/translate?sl=vi&tl=en&_x_tr_hl=en&_x_tr_pto=wapp&u='+encodeURIComponent(cleanUrl);
    window.location.href=translated;
  });
})();
</script>
'''

CSS = r'''

/* VI / EN language selector */
.language-switcher{position:fixed;z-index:1200;top:18px;right:22px;display:flex;align-items:center;gap:7px;padding:7px 10px;border:1px solid rgba(255,255,255,.18);border-radius:999px;background:rgba(5,5,5,.78);backdrop-filter:blur(14px);box-shadow:0 10px 35px rgba(0,0,0,.28)}
.lang-btn{appearance:none;border:0;background:transparent;color:#9f9f9f;font-family:"Montserrat","Be Vietnam Pro",sans-serif;font-weight:800;font-size:12px;letter-spacing:.08em;padding:3px 2px;cursor:pointer;transition:.2s ease}
.lang-btn:hover,.lang-btn.is-active{color:#fff}.lang-btn.is-active{color:#ff3b3b}.lang-sep{color:#5b5b5b;font-size:11px;user-select:none}
@media(max-width:900px){.language-switcher{top:13px;right:64px;padding:6px 9px}.lang-btn{font-size:11px}}
'''

for html in SITE.glob('*.html'):
    text = html.read_text(encoding='utf-8')
    text = re.sub(r'<div class="language-switcher".*?<script id="language-switcher-script">.*?</script>\s*', '', text, flags=re.S)
    text = text.replace('</body>', SWITCH + '\n</body>', 1)
    html.write_text(text, encoding='utf-8')

css_path = SITE / 'styles.css'
css = css_path.read_text(encoding='utf-8')
css = re.sub(r'/\* VI / EN language selector \*/.*?(?=\n/\*|\Z)', '', css, flags=re.S)
css += CSS
css_path.write_text(css, encoding='utf-8')

all_html='\n'.join(p.read_text(encoding='utf-8') for p in SITE.glob('*.html'))
assert all_html.count('class="language-switcher"') == len(list(SITE.glob('*.html')))
assert 'translate.google.com/translate?sl=vi&tl=en' in all_html
print('VI/EN selector added to', len(list(SITE.glob('*.html'))), 'pages')
