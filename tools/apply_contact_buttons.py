from pathlib import Path
import re

SITE = Path('_site')
PHONE_RAW = '0933078500'
PHONE_DISPLAY = '093.307.8500'
ZALO_URL = 'https://zalo.me/0933078500'
# Official fanpage URL has not been verified from bepaau.com.vn yet.
# Keep Facebook functionality explicit and non-deceptive: this opens a Facebook search for the exact brand.
FACEBOOK_URL = 'https://www.facebook.com/search/top?q=B%E1%BA%BFp%20%C3%81%20%C3%82u'

BUTTONS = f'''
<div class="contact-dock" aria-label="Liên hệ nhanh">
  <a class="contact-dock__item contact-dock__call" href="tel:{PHONE_RAW}" aria-label="Gọi {PHONE_DISPLAY}">
    <span class="contact-dock__icon">☎</span><span class="contact-dock__label">Gọi ngay</span>
  </a>
  <a class="contact-dock__item contact-dock__zalo" href="{ZALO_URL}" target="_blank" rel="noopener" aria-label="Chat Zalo {PHONE_DISPLAY}">
    <span class="contact-dock__icon">Z</span><span class="contact-dock__label">Zalo</span>
  </a>
  <a class="contact-dock__item contact-dock__facebook" href="{FACEBOOK_URL}" target="_blank" rel="noopener" aria-label="Tìm Bếp Á Âu trên Facebook">
    <span class="contact-dock__icon">f</span><span class="contact-dock__label">Facebook</span>
  </a>
</div>
'''

CSS = r'''

/* Floating call / Zalo / Facebook contact dock */
.contact-dock{position:fixed;right:18px;bottom:20px;z-index:1400;display:flex;flex-direction:column;gap:10px;align-items:flex-end}
.contact-dock__item{display:flex;align-items:center;gap:10px;min-height:48px;padding:7px 10px 7px 7px;border-radius:999px;text-decoration:none;color:#fff;box-shadow:0 12px 34px rgba(0,0,0,.32);transition:transform .2s ease,filter .2s ease;background:#161616;border:1px solid rgba(255,255,255,.12)}
.contact-dock__item:hover{transform:translateY(-2px);filter:brightness(1.08)}
.contact-dock__icon{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;font-family:"Montserrat","Be Vietnam Pro",sans-serif;font-weight:900;font-size:16px;background:rgba(255,255,255,.13)}
.contact-dock__label{font-family:"Be Vietnam Pro",sans-serif;font-size:13px;font-weight:800;white-space:nowrap}
.contact-dock__call{background:#d61f26}.contact-dock__zalo{background:#0068ff}.contact-dock__facebook{background:#1877f2}
@media(max-width:760px){.contact-dock{right:12px;bottom:14px;gap:8px}.contact-dock__item{min-height:46px;padding:6px}.contact-dock__label{display:none}.contact-dock__icon{width:34px;height:34px}}
'''

pages = list(SITE.glob('*.html'))
for html in pages:
    text = html.read_text(encoding='utf-8')
    # Remove previous generated dock on repeated builds.
    text = re.sub(r'<div class="contact-dock".*?</div>\s*</div>\s*</div>\s*</div>', '', text, flags=re.S)
    # Normalize every click-to-call link to the canonical hotline.
    text = re.sub(r'href="tel:[^"]+"', f'href="tel:{PHONE_RAW}"', text)
    # Normalize known legacy visible hotline variants only.
    for pattern in [
        r'0822\s*122\s*248', r'0822122248',
        r'0832\s*122\s*208', r'0832122208',
        r'0902\s*122\s*208', r'0902122208',
        r'0904\s*603\s*688', r'0904603688',
        r'0961\s*048\s*405', r'0961048405',
        r'0962\s*554\s*955', r'0962554955',
    ]:
        text = re.sub(pattern, PHONE_DISPLAY, text)
    text = text.replace('</body>', BUTTONS + '\n</body>', 1)
    html.write_text(text, encoding='utf-8')

css_path = SITE / 'styles.css'
css = css_path.read_text(encoding='utf-8')
css = re.sub(r'/\* Floating call / Zalo / Facebook contact dock \*/.*?(?=\n/\*|\Z)', '', css, flags=re.S)
css += CSS
css_path.write_text(css, encoding='utf-8')

all_html = '\n'.join(p.read_text(encoding='utf-8') for p in pages)
assert all_html.count('class="contact-dock"') == len(pages)
assert f'tel:{PHONE_RAW}' in all_html
assert ZALO_URL in all_html
assert FACEBOOK_URL in all_html
assert '0822 122 248' not in all_html
assert '0904 603 688' not in all_html
print('Canonical hotline + Call/Zalo/Facebook dock applied to', len(pages), 'pages')
