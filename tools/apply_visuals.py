from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
import re
import time

SITE = Path('_site')
ASSET_DIR = SITE / 'assets' / 'generated'
ASSET_DIR.mkdir(parents=True, exist_ok=True)

# Source-of-truth visual policy:
# - Never fetch project photography from another kitchen/equipment company.
# - Generate new visuals specifically for this website.
# - No people, logos, signs, brand marks, watermarks or readable text.
# - Fixed seeds keep each build visually stable.
# The deployed website serves the downloaded files locally; it does not hotlink them.
GENERATED = {
    'hero.jpg': {
        'seed': 12041,
        'size': (1536, 864),
        'prompt': 'photorealistic premium industrial commercial kitchen in Vietnam, expansive stainless steel 304 cooking line, professional exhaust hoods, spotless dark charcoal architecture, cinematic architectural photography, dramatic but realistic lighting, large clean negative space on the left for website headline, no people, no human, no text, no letters, no logo, no brand, no watermark, no signage',
    },
    'project-restaurant.jpg': {
        'seed': 32117,
        'size': (1200, 900),
        'prompt': 'photorealistic high end restaurant commercial kitchen in Vietnam, stainless steel 304 cooking range, wok and stove line, professional ventilation hood, warm premium restaurant lighting, clean organized workspace, architectural interior photography, no people, no human, no text, no letters, no logo, no brand, no watermark, no signage',
    },
    'project-hotel.jpg': {
        'seed': 46021,
        'size': (1200, 900),
        'prompt': 'photorealistic luxury hotel industrial kitchen in Vietnam, very large stainless steel 304 prep islands, combi ovens, cooking line, extraction hoods, elegant modern hotel back of house, bright professional lighting, architectural photography, no people, no human, no text, no letters, no logo, no brand, no watermark, no signage',
    },
    'project-canteen.jpg': {
        'seed': 58103,
        'size': (1200, 900),
        'prompt': 'photorealistic modern factory and school canteen industrial kitchen in Vietnam, large stainless steel serving line, food trays, bulk cooking equipment, clean bright hygienic interior, professional commercial kitchen architecture, no people, no human, no text, no letters, no logo, no brand, no watermark, no signage',
    },
    'project-central.jpg': {
        'seed': 73019,
        'size': (1200, 900),
        'prompt': 'photorealistic massive central production kitchen in Vietnam, industrial stainless steel 304 equipment, multiple preparation islands, large extraction hood system, high capacity professional food production facility, dark premium industrial architecture, no people, no human, no text, no letters, no logo, no brand, no watermark, no signage',
    },
}


def generation_url(prompt: str, width: int, height: int, seed: int) -> str:
    encoded = quote(prompt, safe='')
    return (
        f'https://image.pollinations.ai/prompt/{encoded}'
        f'?width={width}&height={height}&seed={seed}&model=flux&nologo=true&private=true&safe=true&enhance=true'
    )


def generate_to_file(filename: str, spec: dict) -> None:
    target = ASSET_DIR / filename
    width, height = spec['size']
    url = generation_url(spec['prompt'], width, height, spec['seed'])
    last_error = None
    for attempt in range(1, 6):
        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0 BepAAu-GitHub-Pages/1.0'})
            with urlopen(req, timeout=240) as response:
                data = response.read()
                content_type = (response.headers.get('Content-Type') or '').lower()
            if len(data) < 25_000:
                raise RuntimeError(f'generated image too small: {len(data)} bytes')
            if 'image' not in content_type:
                raise RuntimeError(f'unexpected content type: {content_type}')
            target.write_bytes(data)
            return
        except Exception as exc:
            last_error = exc
            if attempt == 5:
                break
            time.sleep(8 * attempt)
    raise RuntimeError(f'failed to generate {filename}: {last_error}')


for filename, spec in GENERATED.items():
    generate_to_file(filename, spec)
    # Old endpoint is rate-limited; spacing requests also makes CI more reliable.
    time.sleep(6)

# Every original site image is now mapped to one of the five newly generated visuals.
LOCAL = {
    'assets/hero-kitchen.jpg': 'assets/generated/hero.jpg',
    'assets/hero-kitchen.webp': 'assets/generated/hero.jpg',
    'assets/project-nha-hang.jpg': 'assets/generated/project-restaurant.jpg',
    'assets/project-nha-hang.webp': 'assets/generated/project-restaurant.jpg',
    'assets/project-khach-san.jpg': 'assets/generated/project-hotel.jpg',
    'assets/project-khach-san.webp': 'assets/generated/project-hotel.jpg',
    'assets/project-canteen.jpg': 'assets/generated/project-canteen.jpg',
    'assets/project-canteen.webp': 'assets/generated/project-canteen.jpg',
    'assets/project-bep-trung-tam.jpg': 'assets/generated/project-central.jpg',
    'assets/project-bep-trung-tam.webp': 'assets/generated/project-central.jpg',
    'assets/repair-tech.jpg': 'assets/generated/project-central.jpg',
    'assets/repair-tech.webp': 'assets/generated/project-central.jpg',
    'assets/about-team.jpg': 'assets/generated/hero.jpg',
    'assets/about-team.webp': 'assets/generated/hero.jpg',
    'assets/contact-visual.jpg': 'assets/generated/project-canteen.jpg',
    'assets/contact-visual.webp': 'assets/generated/project-canteen.jpg',
    'assets/industrial-texture.jpg': 'assets/generated/hero.jpg',
    'assets/industrial-texture.webp': 'assets/generated/hero.jpg',
    'assets/article-thiet-ke-bep.jpg': 'assets/generated/hero.jpg',
    'assets/article-thiet-ke-bep.webp': 'assets/generated/hero.jpg',
    'assets/article-bo-tri-nha-hang.jpg': 'assets/generated/project-restaurant.jpg',
    'assets/article-bo-tri-nha-hang.webp': 'assets/generated/project-restaurant.jpg',
    'assets/article-hut-khoi.jpg': 'assets/generated/project-central.jpg',
    'assets/article-hut-khoi.webp': 'assets/generated/project-central.jpg',
    'assets/article-bao-tri.jpg': 'assets/generated/project-hotel.jpg',
    'assets/article-bao-tri.webp': 'assets/generated/project-hotel.jpg',
    'assets/article-xu-ly-loi.jpg': 'assets/generated/project-central.jpg',
    'assets/article-xu-ly-loi.webp': 'assets/generated/project-central.jpg',
    'assets/article-bep-canteen.jpg': 'assets/generated/project-canteen.jpg',
    'assets/article-bep-canteen.webp': 'assets/generated/project-canteen.jpg',
}

PROJECT_BY_ALT = {
    'nhà hàng': 'assets/generated/project-restaurant.jpg',
    'khách sạn': 'assets/generated/project-hotel.jpg',
    'canteen': 'assets/generated/project-canteen.jpg',
    'bếp trung tâm': 'assets/generated/project-central.jpg',
    'trung tâm': 'assets/generated/project-central.jpg',
}
ARTICLE_BY_ALT = {
    'hút khói': 'assets/generated/project-central.jpg',
    'bảo trì': 'assets/generated/project-hotel.jpg',
    'sửa chữa': 'assets/generated/project-central.jpg',
    'xử lý lỗi': 'assets/generated/project-central.jpg',
    'thiết kế bếp': 'assets/generated/hero.jpg',
}

FONT_LINKS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800;900&family=Montserrat:wght@600;700;800;900&display=swap" rel="stylesheet">'
)


def set_src(tag: str, src: str) -> str:
    if re.search(r'\bsrc=["\'][^"\']*["\']', tag, flags=re.I):
        return re.sub(r'\bsrc=["\'][^"\']*["\']', f'src="{src}"', tag, count=1, flags=re.I)
    return tag[:-1] + f' src="{src}">'


def contextualize_images(text: str) -> str:
    def repl(match):
        tag = match.group(0)
        alt_match = re.search(r'\balt=["\']([^"\']*)["\']', tag, flags=re.I)
        if not alt_match:
            return tag
        alt = alt_match.group(1).lower()
        for needle, src in PROJECT_BY_ALT.items():
            if needle in alt:
                return set_src(tag, src)
        for needle, src in ARTICLE_BY_ALT.items():
            if needle in alt:
                return set_src(tag, src)
        return tag
    return re.sub(r'<img\b[^>]*>', repl, text, flags=re.I)


for html in SITE.glob('*.html'):
    text = html.read_text(encoding='utf-8')
    for old, new in LOCAL.items():
        text = text.replace(old, new)

    # Purge every previous external image source, including the old borrowed Vietnam-company photos.
    text = re.sub(r'https?://[^"\']+\.(?:jpg|jpeg|png|webp)(?:\?[^"\']*)?', 'assets/generated/hero.jpg', text, flags=re.I)
    text = contextualize_images(text)

    text = text.replace('Dự án tiêu biểu', 'Mô hình dự án')
    text = text.replace('alt="Dự án bếp nhà hàng"', 'alt="Mô hình bếp nhà hàng"')
    text = text.replace('alt="Dự án bếp khách sạn"', 'alt="Mô hình bếp khách sạn"')
    text = text.replace('alt="Dự án bếp canteen"', 'alt="Mô hình bếp canteen"')
    text = text.replace('alt="Dự án bếp trung tâm"', 'alt="Mô hình bếp trung tâm"')
    text = text.replace('alt="Bếp nhà hàng thực tế tại Việt Nam"', 'alt="Mô hình bếp nhà hàng"')
    text = text.replace('alt="Bếp khách sạn thực tế tại Việt Nam"', 'alt="Mô hình bếp khách sạn"')
    text = text.replace('alt="Bếp canteen thực tế tại Việt Nam"', 'alt="Mô hình bếp canteen"')
    text = text.replace('alt="Bếp trung tâm thực tế tại Việt Nam"', 'alt="Mô hình bếp trung tâm"')

    if 'fonts.googleapis.com' not in text:
        text = text.replace('<link rel="stylesheet" href="styles.css">', FONT_LINKS + '<link rel="stylesheet" href="styles.css?v=13">')
    text = text.replace('<script src="script.js"></script>', '<script src="script.js?v=13"></script>')
    html.write_text(text, encoding='utf-8')

css_path = SITE / 'styles.css'
css = css_path.read_text(encoding='utf-8')
for old, new in LOCAL.items():
    css = css.replace(old, new)
css = re.sub(r'https?://[^"\')]+\.(?:jpg|jpeg|png|webp)(?:\?[^"\')]+)?', 'assets/generated/hero.jpg', css, flags=re.I)
css += '''

/* Generated visual system v13 — no borrowed project photography */
body{font-family:"Be Vietnam Pro",ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-weight:400;letter-spacing:-.008em;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
h1,h2,h3,h4,.hero-sub,.menu,.btn,.eyebrow,.stat b,.project-info strong,.article-hero h1{font-family:"Montserrat","Be Vietnam Pro",ui-sans-serif,system-ui,sans-serif}
.hero h1,.page-hero h1,.article-hero h1{font-weight:900;letter-spacing:-.045em}
.hero-bg{background-image:url("assets/generated/hero.jpg")!important;background-size:cover!important;background-position:center!important}
.project-card img,.news-card img,.gallery-item img,.repair-photo img,.project-detail img,.about-split img,.article-figure img{filter:saturate(1.02) contrast(1.03);object-fit:cover}
'''
css_path.write_text(css, encoding='utf-8')

all_html = '\n'.join(p.read_text(encoding='utf-8') for p in SITE.glob('*.html'))
for forbidden in [
    'hayen.com.vn', 'daithuanphat.com.vn', 'obayashivn.com', 'haihunggroup.com',
    'inoxquyenphat.com.vn', 'hstatic.net', 'shopify.com', 'meta.vn',
    'images.pexels.com', 'images.unsplash.com', 'commons.wikimedia.org'
]:
    assert forbidden not in all_html, f'borrowed/external image source remains: {forbidden}'

required = [
    'assets/generated/project-restaurant.jpg',
    'assets/generated/project-hotel.jpg',
    'assets/generated/project-canteen.jpg',
    'assets/generated/project-central.jpg',
]
for item in required:
    assert item in all_html, f'missing generated visual: {item}'

for filename in GENERATED:
    target = ASSET_DIR / filename
    assert target.exists() and target.stat().st_size >= 25_000, f'invalid generated asset: {filename}'

print('Five new generated kitchen visuals wired successfully; zero borrowed project photography')
