from pathlib import Path
from urllib.request import Request, urlopen
import re

SITE = Path('_site')
ASSET_DIR = SITE / 'assets' / 'vietnam'
ASSET_DIR.mkdir(parents=True, exist_ok=True)

# Real photography/projects from Vietnam-based sources only.
# Deliberately choose frames without visible people so foreign people cannot appear.
SOURCES = {
    'hero.jpg': 'https://bizweb.dktcdn.net/100/485/868/files/z4371519257642-1f85de24cc43f14c8a276b7534e1665b.jpg?v=1684988197479',
    'project-restaurant.jpg': 'https://daithuanphat.com.vn/upload/filemanager/D%E1%BB%B0%20%C3%81N%20H%E1%BA%A6M%20R%C6%AF%E1%BB%A2U%20S%C3%94NG%20C%E1%BA%A6U%20T%C3%82Y%20NINH/z4434539035761_2a6b569091b663dda40e717ee0e2bbdc.jpg',
    'project-hotel.jpg': 'https://hayen.com.vn/data/images/thiet-ke-bep-khach-san-toi-uu-hieu-suat_1761193395.jpg',
    'project-canteen.jpg': 'https://hayen.com.vn/data/images/bep-an-truong-hoc-anh2_1761195946.jpg',
    'project-central.png': 'https://www.obayashivn.com/Data/Sites/1/News/266/bv1-detail3.png',
    'repair.jpg': 'https://inoxquyenphat.com.vn/thumbs/1276x956x2/upload/product/chup-hut-10-7753.jpg',
    'about.jpg': 'https://haihunggroup.com/admin/public/images/tour_imgs/talica-36013522778197258eeecfafa4423627.jpg',
    'contact.jpg': 'https://file.hstatic.net/1000381568/file/chu-y-bo-tri-lap-dat-trang-thiet-bi-phu-hop-trong-bep-an-tap-the_ea4bbb13f5b6454b84a10daaee3acdb2_grande.jpg',
    'article-design.jpg': 'https://hayen.com.vn/data/Services/thuvien/1_1614667067.jpg',
    'article-layout.jpg': 'https://cdn.shopify.com/s/files/1/0878/1270/files/Tam-Quan-Trong-Cua-Bep-Inox-Trong-Nha-Hang_1_480x480.jpg?v=1727689517',
    'article-exhaust.jpg': 'https://binhhiepphu.com.vn/upload/filemanager/files/Thi%E1%BA%BFt%20b%E1%BB%8B/gia-cong-lap-dat-chup-hut-khoi-gia-re-tai-TPHCM.jpg',
    'article-maintenance.jpg': 'https://product.hstatic.net/200000574527/product/bep-tu-cong-nghiep-doi-lom-lien-chao-viet-han-vh15kl800x2-ih52-1_03607ce23ac6426bbe11eeae1137e016.jpg',
    'article-fault.jpg': 'https://meta.vn/Data/image/2022/01/28/bep-tu-cong-nghiep-don-viet-han-vh15kl800-ih52.jpg',
    'article-canteen.jpg': 'https://file.hstatic.net/1000381568/file/chu-y-bo-tri-lap-dat-trang-thiet-bi-phu-hop-trong-bep-an-tap-the_ea4bbb13f5b6454b84a10daaee3acdb2_grande.jpg',
}

for filename, url in SOURCES.items():
    target = ASSET_DIR / filename
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (GitHub Pages build; Bep A Au preview)'})
    with urlopen(req, timeout=30) as r:
        data = r.read()
    if len(data) < 20_000:
        raise RuntimeError(f'image download too small/failed: {filename} ({len(data)} bytes)')
    target.write_bytes(data)

LOCAL = {
    'assets/hero-kitchen.jpg': 'assets/vietnam/hero.jpg',
    'assets/hero-kitchen.webp': 'assets/vietnam/hero.jpg',
    'assets/project-nha-hang.jpg': 'assets/vietnam/project-restaurant.jpg',
    'assets/project-nha-hang.webp': 'assets/vietnam/project-restaurant.jpg',
    'assets/project-khach-san.jpg': 'assets/vietnam/project-hotel.jpg',
    'assets/project-khach-san.webp': 'assets/vietnam/project-hotel.jpg',
    'assets/project-canteen.jpg': 'assets/vietnam/project-canteen.jpg',
    'assets/project-canteen.webp': 'assets/vietnam/project-canteen.jpg',
    'assets/project-bep-trung-tam.jpg': 'assets/vietnam/project-central.png',
    'assets/project-bep-trung-tam.webp': 'assets/vietnam/project-central.png',
    'assets/repair-tech.jpg': 'assets/vietnam/repair.jpg',
    'assets/repair-tech.webp': 'assets/vietnam/repair.jpg',
    'assets/about-team.jpg': 'assets/vietnam/about.jpg',
    'assets/about-team.webp': 'assets/vietnam/about.jpg',
    'assets/contact-visual.jpg': 'assets/vietnam/contact.jpg',
    'assets/contact-visual.webp': 'assets/vietnam/contact.jpg',
    'assets/industrial-texture.jpg': 'assets/vietnam/hero.jpg',
    'assets/industrial-texture.webp': 'assets/vietnam/hero.jpg',
    'assets/article-thiet-ke-bep.jpg': 'assets/vietnam/article-design.jpg',
    'assets/article-thiet-ke-bep.webp': 'assets/vietnam/article-design.jpg',
    'assets/article-bo-tri-nha-hang.jpg': 'assets/vietnam/article-layout.jpg',
    'assets/article-bo-tri-nha-hang.webp': 'assets/vietnam/article-layout.jpg',
    'assets/article-hut-khoi.jpg': 'assets/vietnam/article-exhaust.jpg',
    'assets/article-hut-khoi.webp': 'assets/vietnam/article-exhaust.jpg',
    'assets/article-bao-tri.jpg': 'assets/vietnam/article-maintenance.jpg',
    'assets/article-bao-tri.webp': 'assets/vietnam/article-maintenance.jpg',
    'assets/article-xu-ly-loi.jpg': 'assets/vietnam/article-fault.jpg',
    'assets/article-xu-ly-loi.webp': 'assets/vietnam/article-fault.jpg',
    'assets/article-bep-canteen.jpg': 'assets/vietnam/article-canteen.jpg',
    'assets/article-bep-canteen.webp': 'assets/vietnam/article-canteen.jpg',
}

FONT_LINKS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800;900&family=Montserrat:wght@600;700;800;900&display=swap" rel="stylesheet">'
)

# Clean every previously injected external visual URL, including Pexels/Unsplash/Commons.
EXTERNAL_IMAGE_RE = re.compile(r'https://(?:images\.pexels\.com|images\.unsplash\.com|unsplash\.com|commons\.wikimedia\.org)[^\"\']*')

for html in SITE.glob('*.html'):
    text = html.read_text(encoding='utf-8')
    for old, new in LOCAL.items():
        text = text.replace(old, new)
    # Previous builds may already contain direct external URLs. Map them by context-sensitive known names below.
    text = re.sub(r'https://images\.pexels\.com/photos/[^\"\']+', 'assets/vietnam/hero.jpg', text)
    text = re.sub(r'https://commons\.wikimedia\.org/[^\"\']+', 'assets/vietnam/article-exhaust.jpg', text)
    text = re.sub(r'https://images\.unsplash\.com/[^\"\']+', 'assets/vietnam/hero.jpg', text)
    text = re.sub(r'https://unsplash\.com/photos/[^\"\']+', 'assets/vietnam/hero.jpg', text)
    text = text.replace('Dự án tiêu biểu', 'Mô hình dự án')
    text = text.replace('alt="Dự án bếp nhà hàng"', 'alt="Bếp nhà hàng thực tế tại Việt Nam"')
    text = text.replace('alt="Dự án bếp khách sạn"', 'alt="Bếp khách sạn thực tế tại Việt Nam"')
    text = text.replace('alt="Dự án bếp canteen"', 'alt="Bếp canteen thực tế tại Việt Nam"')
    text = text.replace('alt="Dự án bếp trung tâm"', 'alt="Bếp công nghiệp quy mô lớn tại Việt Nam"')
    if 'fonts.googleapis.com' not in text:
        text = text.replace('<link rel="stylesheet" href="styles.css">', FONT_LINKS + '<link rel="stylesheet" href="styles.css?v=9">')
    text = text.replace('<script src="script.js"></script>', '<script src="script.js?v=9"></script>')
    html.write_text(text, encoding='utf-8')

css_path = SITE / 'styles.css'
css = css_path.read_text(encoding='utf-8')
for old, new in LOCAL.items():
    css = css.replace(old, new)
css = re.sub(r'https://images\.pexels\.com/photos/[^\"\')]+', 'assets/vietnam/hero.jpg', css)
css = re.sub(r'https://images\.unsplash\.com/[^\"\')]+', 'assets/vietnam/hero.jpg', css)
css = css.replace(
    'font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif',
    'font-family:"Be Vietnam Pro",ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif'
)
css += '''

/* Vietnam-only real-photo refresh v9 */
body{font-family:"Be Vietnam Pro",ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-weight:400;letter-spacing:-.008em;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
h1,h2,h3,h4,.hero-sub,.menu,.btn,.eyebrow,.stat b,.project-info strong,.article-hero h1{font-family:"Montserrat","Be Vietnam Pro",ui-sans-serif,system-ui,sans-serif}
.hero h1,.page-hero h1,.article-hero h1{font-weight:900;letter-spacing:-.045em}
.hero-bg{background-image:url("assets/vietnam/hero.jpg")!important;background-size:cover!important;background-position:center!important}
.project-card img,.news-card img,.gallery-item img,.repair-photo img,.project-detail img,.about-split img,.article-figure img{filter:saturate(1.04) contrast(1.03);object-fit:cover}
'''
css_path.write_text(css, encoding='utf-8')

all_html='\n'.join(p.read_text(encoding='utf-8') for p in SITE.glob('*.html'))
for forbidden in ['images.pexels.com', 'images.unsplash.com', 'unsplash.com/photos/', 'commons.wikimedia.org']:
    assert forbidden not in all_html, f'forbidden non-Vietnam image source remains: {forbidden}'
for required in [
    'project-restaurant.jpg', 'project-hotel.jpg', 'project-canteen.jpg', 'project-central.png',
    'article-design.jpg', 'article-layout.jpg', 'article-exhaust.jpg'
]:
    assert required in all_html, f'missing Vietnam visual: {required}'
assert len({LOCAL['assets/project-nha-hang.jpg'], LOCAL['assets/project-khach-san.jpg'], LOCAL['assets/project-canteen.jpg'], LOCAL['assets/project-bep-trung-tam.jpg']}) == 4
print('Vietnam-only real photography downloaded locally and wired; project cards are unique')
