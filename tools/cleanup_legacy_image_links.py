from pathlib import Path
import re

SITE = Path('_site')
DOMAINS = [
    'unsplash.com', 'pexels.com', 'commons.wikimedia.org',
    'hayen.com.vn', 'daithuanphat.com.vn', 'obayashivn.com', 'haihunggroup.com',
    'inoxquyenphat.com.vn', 'hstatic.net', 'shopify.com', 'meta.vn',
]

for html in SITE.glob('*.html'):
    text = html.read_text(encoding='utf-8')
    for domain in DOMAINS:
        # Remove old attribution/hotlink URLs without touching normal site content.
        text = re.sub(
            rf'https?://(?:www\.)?[^"\'\s<>]*{re.escape(domain)}[^"\'\s<>]*',
            '#',
            text,
            flags=re.I,
        )
    html.write_text(text, encoding='utf-8')

all_html = '\n'.join(p.read_text(encoding='utf-8') for p in SITE.glob('*.html')).lower()
for domain in DOMAINS:
    assert domain.lower() not in all_html, f'legacy image-source domain remains: {domain}'

print('Legacy image-source links removed from', len(list(SITE.glob('*.html'))), 'pages')
