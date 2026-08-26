from pathlib import Path
import json
import re

SITE = Path('_site')

COMPANY = {
    'name': 'CÔNG TY CỔ PHẦN THIẾT BỊ Á ÂU',
    'tax_id': '0106163396',
    'email': 'info@bepaau.com.vn',
    'website': 'https://bepaau.com.vn/',
    'hn_factory': 'Thôn 7, Đình Vĩ, xã Hoài Đức, Hà Nội',
    'hn_office': 'LK24 Khu đô thị Nam La Khê, phường Hà Đông, Hà Nội',
    'hn_hotlines': [('0961048405', '0961 048 405'), ('0962554955', '0962 554 955')],
    'hcm_address': '46B, Đường Số 6, Phường Tân Sơn Nhì, TP.Hồ Chí Minh',
    'hcm_landline': ('02822404999', '028 22 404 999'),
    'primary_hotline': ('0904603688', '0904 603 688'),
}

# Exact contact block based on the contact information supplied from bepaau.com.vn.
CONTACT_BLOCK = f'''\n<div class="verified-company-info" data-company-source="bepaau.com.vn">
  <div class="verified-company-inner">
    <div class="verified-company-brand">
      <strong>{COMPANY['name']}</strong>
      <span>MST: {COMPANY['tax_id']}</span>
    </div>
    <div class="verified-company-grid">
      <div class="verified-company-col">
        <h3>Hà Nội</h3>
        <p><b>Xưởng sản xuất:</b> {COMPANY['hn_factory']}</p>
        <p><b>VPGD:</b> {COMPANY['hn_office']}</p>
        <p><b>Hotline:</b> <a href="tel:{COMPANY['hn_hotlines'][0][0]}">{COMPANY['hn_hotlines'][0][1]}</a> - <a href="tel:{COMPANY['hn_hotlines'][1][0]}">{COMPANY['hn_hotlines'][1][1]}</a></p>
      </div>
      <div class="verified-company-col">
        <h3>TP Hồ Chí Minh</h3>
        <p>{COMPANY['hcm_address']}</p>
        <p><b>ĐT:</b> <a href="tel:{COMPANY['hcm_landline'][0]}">{COMPANY['hcm_landline'][1]}</a> - <b>Hotline:</b> <a href="tel:{COMPANY['primary_hotline'][0]}">{COMPANY['primary_hotline'][1]}</a></p>
        <p><b>Email:</b> <a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a></p>
      </div>
    </div>
  </div>
</div>\n'''

CONTACT_PAGE_BLOCK = f'''\n<section class="verified-contact-page" data-company-source="bepaau.com.vn">
  <div class="verified-company-inner">
    <div class="eyebrow">THÔNG TIN LIÊN HỆ CHÍNH THỨC</div>
    <h2>{COMPANY['name']}</h2>
    <p class="verified-tax">Mã số thuế: <strong>{COMPANY['tax_id']}</strong></p>
    <div class="verified-company-grid">
      <div class="verified-company-col">
        <h3>Hà Nội</h3>
        <p><b>Xưởng sản xuất:</b> {COMPANY['hn_factory']}</p>
        <p><b>Văn phòng giao dịch:</b> {COMPANY['hn_office']}</p>
        <p><b>Hotline:</b> <a href="tel:{COMPANY['hn_hotlines'][0][0]}">{COMPANY['hn_hotlines'][0][1]}</a> - <a href="tel:{COMPANY['hn_hotlines'][1][0]}">{COMPANY['hn_hotlines'][1][1]}</a></p>
      </div>
      <div class="verified-company-col">
        <h3>TP Hồ Chí Minh</h3>
        <p><b>Địa chỉ:</b> {COMPANY['hcm_address']}</p>
        <p><b>Điện thoại:</b> <a href="tel:{COMPANY['hcm_landline'][0]}">{COMPANY['hcm_landline'][1]}</a></p>
        <p><b>Hotline:</b> <a href="tel:{COMPANY['primary_hotline'][0]}">{COMPANY['primary_hotline'][1]}</a></p>
        <p><b>Email:</b> <a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a></p>
      </div>
    </div>
  </div>
</section>\n'''

SCHEMA = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    'name': COMPANY['name'],
    'url': COMPANY['website'],
    'taxID': COMPANY['tax_id'],
    'email': COMPANY['email'],
    'telephone': '+84-904-603-688',
    'contactPoint': [
        {'@type': 'ContactPoint', 'telephone': '+84-961-048-405', 'contactType': 'sales', 'areaServed': 'VN', 'availableLanguage': ['vi']},
        {'@type': 'ContactPoint', 'telephone': '+84-962-554-955', 'contactType': 'sales', 'areaServed': 'VN', 'availableLanguage': ['vi']},
        {'@type': 'ContactPoint', 'telephone': '+84-904-603-688', 'contactType': 'customer service', 'areaServed': 'VN', 'availableLanguage': ['vi']},
    ],
    'location': [
        {'@type': 'Place', 'name': 'Xưởng sản xuất Hà Nội', 'address': {'@type': 'PostalAddress', 'streetAddress': COMPANY['hn_factory'], 'addressCountry': 'VN'}},
        {'@type': 'Place', 'name': 'Văn phòng giao dịch Hà Nội', 'address': {'@type': 'PostalAddress', 'streetAddress': COMPANY['hn_office'], 'addressCountry': 'VN'}},
        {'@type': 'Place', 'name': 'Văn phòng TP Hồ Chí Minh', 'address': {'@type': 'PostalAddress', 'streetAddress': COMPANY['hcm_address'], 'addressCountry': 'VN'}},
    ],
}
SCHEMA_TAG = '<script type="application/ld+json" id="verified-company-schema">' + json.dumps(SCHEMA, ensure_ascii=False, separators=(',', ':')) + '</script>'

# Replace previously used preview numbers/emails without touching unrelated numeric content.
OLD_PHONE_PATTERNS = [
    r'0832\s*122\s*208', r'0902\s*122\s*208', r'0902\s*122\s*208',
    r'0832122208', r'0902122208'
]

for html in SITE.glob('*.html'):
    text = html.read_text(encoding='utf-8')

    # Remove a previous generated canonical block/schema so the build is idempotent.
    text = re.sub(r'<div class="verified-company-info".*?</div>\s*</div>\s*</div>', '', text, flags=re.S)
    text = re.sub(r'<section class="verified-contact-page".*?</section>', '', text, flags=re.S)
    text = re.sub(r'<script type="application/ld\+json" id="verified-company-schema">.*?</script>', '', text, flags=re.S)

    # Normalize legacy preview phone/email links before inserting the verified block.
    text = re.sub(r'href="tel:(?:0832122208|0902122208|0902122208)"', f'href="tel:{COMPANY["primary_hotline"][0]}"', text)
    for pattern in OLD_PHONE_PATTERNS:
        text = re.sub(pattern, COMPANY['primary_hotline'][1], text)
    text = re.sub(r'href="mailto:[^"]+"', f'href="mailto:{COMPANY["email"]}"', text)
    text = re.sub(r'(?i)\b(?:contact|hello|sales|hotro|support)@[a-z0-9.-]+\.[a-z]{2,}\b', COMPANY['email'], text)

    # Add canonical organization schema to every page.
    if '</head>' in text:
        text = text.replace('</head>', SCHEMA_TAG + '\n</head>', 1)

    # Make contact page comprehensive and visible above the footer.
    if html.name in {'lien-he.html', 'contact.html'}:
        if '<footer' in text:
            text = text.replace('<footer', CONTACT_PAGE_BLOCK + '<footer', 1)
        else:
            text = text.replace('</body>', CONTACT_PAGE_BLOCK + '</body>', 1)

    # Add the verified company footer block to every page.
    if '</footer>' in text:
        text = text.replace('</footer>', CONTACT_BLOCK + '</footer>', 1)
    else:
        text = text.replace('</body>', CONTACT_BLOCK + '</body>', 1)

    html.write_text(text, encoding='utf-8')

css_path = SITE / 'styles.css'
css = css_path.read_text(encoding='utf-8')
css += '''

/* Canonical Bep A Au company information */
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

# Hard build assertions. Deployment must stop if canonical data is missing.
all_html = '\n'.join(p.read_text(encoding='utf-8') for p in SITE.glob('*.html'))
for required in [
    COMPANY['name'], COMPANY['tax_id'], COMPANY['email'], COMPANY['hn_factory'],
    COMPANY['hn_office'], COMPANY['hcm_address'], COMPANY['hn_hotlines'][0][1],
    COMPANY['hn_hotlines'][1][1], COMPANY['hcm_landline'][1], COMPANY['primary_hotline'][1]
]:
    assert required in all_html, f'missing verified company data: {required}'

print('Verified Bep A Au company data applied to', len(list(SITE.glob('*.html'))), 'HTML pages')
