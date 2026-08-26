from pathlib import Path
import json
import re

SITE = Path('_site')

# Source of truth: contact footer currently displayed on https://bepaau.com.vn/
# Do not add any address, phone, company name or email that is not present there.
COMPANY = {
    'brand': 'Bếp Á - Âu',
    'tax_id': '0340890521',
    'email': 'cylamthuanphat@gmail.com',
    'website': 'https://bepaau.com.vn/',
    'address': '43 đường số 6, cư xá Chu Văn An, Bình Thạnh, TP HCM',
    'branch': '393/2G Nguyễn Xí, P13, Quận Bình Thạnh, TP HCM',
    'hotline_raw': '0933078500',
    'hotline_display': '093.307.8500',
    'hours': '8:00 - 20:30, thứ 2 đến thứ 7',
    'closed': 'Chủ nhật nghỉ',
}

CONTACT_BLOCK = f'''\n<div class="verified-company-info" data-company-source="bepaau.com.vn">
  <div class="verified-company-inner">
    <div class="verified-company-brand">
      <strong>{COMPANY['brand']}</strong>
      <span>MST: {COMPANY['tax_id']}</span>
    </div>
    <div class="verified-company-grid">
      <div class="verified-company-col">
        <h3>Thông tin liên hệ</h3>
        <p><b>Địa chỉ:</b> {COMPANY['address']}</p>
        <p><b>Chi nhánh:</b> {COMPANY['branch']}</p>
      </div>
      <div class="verified-company-col">
        <h3>Kết nối</h3>
        <p><b>Hotline:</b> <a href="tel:{COMPANY['hotline_raw']}">{COMPANY['hotline_display']}</a></p>
        <p><b>Email:</b> <a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a></p>
        <p><b>Thời gian mở cửa:</b> {COMPANY['hours']} · {COMPANY['closed']}</p>
      </div>
    </div>
  </div>
</div>\n'''

CONTACT_PAGE_BLOCK = f'''\n<section class="verified-contact-page" data-company-source="bepaau.com.vn">
  <div class="verified-company-inner">
    <div class="eyebrow">THÔNG TIN LIÊN HỆ</div>
    <h2>{COMPANY['brand']}</h2>
    <p class="verified-tax">MST: <strong>{COMPANY['tax_id']}</strong></p>
    <div class="verified-company-grid">
      <div class="verified-company-col">
        <h3>Địa chỉ</h3>
        <p><b>Địa chỉ:</b> {COMPANY['address']}</p>
        <p><b>Chi nhánh:</b> {COMPANY['branch']}</p>
      </div>
      <div class="verified-company-col">
        <h3>Liên hệ</h3>
        <p><b>Hotline:</b> <a href="tel:{COMPANY['hotline_raw']}">{COMPANY['hotline_display']}</a></p>
        <p><b>Email:</b> <a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a></p>
        <p><b>Mở cửa:</b> {COMPANY['hours']}</p>
        <p><b>{COMPANY['closed']}</b></p>
      </div>
    </div>
  </div>
</section>\n'''

SCHEMA = {
    '@context': 'https://schema.org',
    '@type': 'LocalBusiness',
    'name': COMPANY['brand'],
    'url': COMPANY['website'],
    'taxID': COMPANY['tax_id'],
    'email': COMPANY['email'],
    'telephone': '+84-933-078-500',
    'address': {
        '@type': 'PostalAddress',
        'streetAddress': COMPANY['address'],
        'addressLocality': 'Bình Thạnh',
        'addressRegion': 'TP Hồ Chí Minh',
        'addressCountry': 'VN',
    },
    'contactPoint': [{
        '@type': 'ContactPoint',
        'telephone': '+84-933-078-500',
        'contactType': 'customer service',
        'areaServed': 'VN',
        'availableLanguage': ['vi'],
    }],
    'openingHoursSpecification': [{
        '@type': 'OpeningHoursSpecification',
        'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        'opens': '08:00',
        'closes': '20:30',
    }],
}
SCHEMA_TAG = '<script type="application/ld+json" id="verified-company-schema">' + json.dumps(SCHEMA, ensure_ascii=False, separators=(',', ':')) + '</script>'

# Values from the previously incorrect data set. These must not survive the build.
WRONG_VALUES = [
    'CÔNG TY CỔ PHẦN THIẾT BỊ Á ÂU',
    '0106163396',
    'info@bepaau.com.vn',
    'Thôn 7, Đình Vĩ, xã Hoài Đức, Hà Nội',
    'LK24 Khu đô thị Nam La Khê, phường Hà Đông, Hà Nội',
    '0961 048 405', '0962 554 955', '028 22 404 999', '0904 603 688',
    '46B, Đường Số 6, Phường Tân Sơn Nhì, TP.Hồ Chí Minh',
]

LEGACY_PHONES = [
    r'0832\s*122\s*208', r'0902\s*122\s*208', r'0832122208', r'0902122208',
    r'0961\s*048\s*405', r'0962\s*554\s*955', r'028\s*22\s*404\s*999', r'0904\s*603\s*688',
]

for html in SITE.glob('*.html'):
    text = html.read_text(encoding='utf-8')

    # Remove prior generated blocks/schema first so repeated builds are clean.
    text = re.sub(r'<div class="verified-company-info".*?</div>\s*</div>\s*</div>', '', text, flags=re.S)
    text = re.sub(r'<section class="verified-contact-page".*?</section>', '', text, flags=re.S)
    text = re.sub(r'<script type="application/ld\+json" id="verified-company-schema">.*?</script>', '', text, flags=re.S)

    # Normalize every legacy preview/incorrect phone and mailto to the source-of-truth values.
    text = re.sub(r'href="tel:[^"]+"', f'href="tel:{COMPANY["hotline_raw"]}"', text)
    for pattern in LEGACY_PHONES:
        text = re.sub(pattern, COMPANY['hotline_display'], text)
    text = re.sub(r'href="mailto:[^"]+"', f'href="mailto:{COMPANY["email"]}"', text)
    text = re.sub(r'(?i)\b(?:contact|hello|sales|hotro|support|info)@[a-z0-9.-]+\.[a-z]{2,}\b', COMPANY['email'], text)

    # Remove any visible leftover incorrect generated facts.
    for wrong in WRONG_VALUES:
        text = text.replace(wrong, '')

    # Add exact source-of-truth schema.
    if '</head>' in text:
        text = text.replace('</head>', SCHEMA_TAG + '\n</head>', 1)

    # Add full contact details on the contact page.
    if html.name in {'lien-he.html', 'contact.html'}:
        if '<footer' in text:
            text = text.replace('<footer', CONTACT_PAGE_BLOCK + '<footer', 1)
        else:
            text = text.replace('</body>', CONTACT_PAGE_BLOCK + '</body>', 1)

    # Add the exact footer contact block to every page.
    if '</footer>' in text:
        text = text.replace('</footer>', CONTACT_BLOCK + '</footer>', 1)
    else:
        text = text.replace('</body>', CONTACT_BLOCK + '</body>', 1)

    html.write_text(text, encoding='utf-8')

css_path = SITE / 'styles.css'
css = css_path.read_text(encoding='utf-8')
css += '''

/* Contact information sourced from bepaau.com.vn */
.verified-company-info{border-top:1px solid rgba(255,255,255,.12);margin-top:42px;padding:34px 0 10px;color:#ddd}
.verified-company-inner{width:min(1180px,calc(100% - 36px));margin:0 auto}
.verified-company-brand{display:flex;flex-wrap:wrap;gap:12px 24px;align-items:baseline;margin-bottom:22px}
.verified-company-brand strong{font-size:clamp(18px,2vw,26px);color:#fff}.verified-company-brand span{color:#aaa}
.verified-company-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px}
.verified-company-col h3{margin:0 0 10px;color:#fff;font-size:18px}.verified-company-col p{margin:7px 0;line-height:1.65;color:#bbb}
.verified-company-col a{color:#fff;text-decoration:none;font-weight:700}.verified-company-col a:hover{color:#ff4040}
.verified-contact-page{padding:72px 0;background:#0b0b0b;border-top:1px solid rgba(255,255,255,.08)}
.verified-contact-page h2{margin:10px 0 6px;font-size:clamp(30px,4vw,56px)}.verified-contact-page .verified-tax{margin:0 0 30px;color:#bbb}
@media(max-width:760px){.verified-company-grid{grid-template-columns:1fr}.verified-company-info{padding-top:26px}.verified-contact-page{padding:52px 0}}
'''
css_path.write_text(css, encoding='utf-8')

all_html = '\n'.join(p.read_text(encoding='utf-8') for p in SITE.glob('*.html'))
required = [
    COMPANY['brand'], COMPANY['tax_id'], COMPANY['email'], COMPANY['address'],
    COMPANY['branch'], COMPANY['hotline_display'], COMPANY['hours'], COMPANY['closed'],
    'verified-company-schema',
]
for value in required:
    assert value in all_html, f'missing bepaau.com.vn contact data: {value}'
for wrong in WRONG_VALUES:
    assert wrong not in all_html, f'incorrect old company data still present: {wrong}'

print('bepaau.com.vn contact data applied to', len(list(SITE.glob('*.html'))), 'HTML pages')
