from pathlib import Path
import re

SITE = Path('_site')

DIRECT = {
    'r98ko7v0Vas': 'https://images.pexels.com/photos/34276646/pexels-photo-34276646.jpeg?auto=compress&cs=tinysrgb&w=2200',
    'Yxm90BYxq3E': 'https://images.pexels.com/photos/5794152/pexels-photo-5794152.jpeg?auto=compress&cs=tinysrgb&w=1800',
    'F9v4iq0RDZ0': 'https://commons.wikimedia.org/wiki/Special:FilePath/CaptiveAire%20Hood.jpg',
    'KDB8-kQw0Ac': 'https://images.pexels.com/photos/38190070/pexels-photo-38190070.jpeg?auto=compress&cs=tinysrgb&w=1800',
    'Y_tMFA6KCcI': 'https://images.pexels.com/photos/37174868/pexels-photo-37174868.jpeg?auto=compress&cs=tinysrgb&w=1800',
    'KhZSSHoS6Xs': 'https://images.pexels.com/photos/5835331/pexels-photo-5835331.jpeg?auto=compress&cs=tinysrgb&w=1800',
    'GUvMJU5ZZLg': 'https://images.pexels.com/photos/6375553/pexels-photo-6375553.jpeg?auto=compress&cs=tinysrgb&w=1800',
    'TNMene5DvQ8': 'https://images.pexels.com/photos/2544830/pexels-photo-2544830.jpeg?auto=compress&cs=tinysrgb&w=1800',
    'WNGGc1euT_g': 'https://images.pexels.com/photos/6375553/pexels-photo-6375553.jpeg?auto=compress&cs=tinysrgb&w=1800',
    'aCgbkvfkFME': 'https://images.pexels.com/photos/6375553/pexels-photo-6375553.jpeg?auto=compress&cs=tinysrgb&w=1800',
    'BrlIqTYR190': 'https://images.pexels.com/photos/34276646/pexels-photo-34276646.jpeg?auto=compress&cs=tinysrgb&w=1800',
    'yTw1v1SIxUE': 'https://images.pexels.com/photos/38190070/pexels-photo-38190070.jpeg?auto=compress&cs=tinysrgb&w=1800',
    'YFK5dBI6Ftc': 'https://images.pexels.com/photos/5779775/pexels-photo-5779775.jpeg?auto=compress&cs=tinysrgb&w=1800',
}

LOCAL = {
    'assets/hero-kitchen.jpg': DIRECT['r98ko7v0Vas'],
    'assets/hero-kitchen.webp': DIRECT['r98ko7v0Vas'],
    'assets/project-nha-hang.jpg': DIRECT['Yxm90BYxq3E'],
    'assets/project-nha-hang.webp': DIRECT['Yxm90BYxq3E'],
    'assets/project-khach-san.jpg': DIRECT['TNMene5DvQ8'],
    'assets/project-khach-san.webp': DIRECT['TNMene5DvQ8'],
    'assets/project-canteen.jpg': DIRECT['KhZSSHoS6Xs'],
    'assets/project-canteen.webp': DIRECT['KhZSSHoS6Xs'],
    'assets/project-bep-trung-tam.jpg': DIRECT['aCgbkvfkFME'],
    'assets/project-bep-trung-tam.webp': DIRECT['aCgbkvfkFME'],
    'assets/repair-tech.jpg': DIRECT['yTw1v1SIxUE'],
    'assets/repair-tech.webp': DIRECT['yTw1v1SIxUE'],
    'assets/about-team.jpg': DIRECT['YFK5dBI6Ftc'],
    'assets/about-team.webp': DIRECT['YFK5dBI6Ftc'],
    'assets/contact-visual.jpg': DIRECT['WNGGc1euT_g'],
    'assets/contact-visual.webp': DIRECT['WNGGc1euT_g'],
    'assets/industrial-texture.jpg': DIRECT['GUvMJU5ZZLg'],
    'assets/industrial-texture.webp': DIRECT['GUvMJU5ZZLg'],
    'assets/article-thiet-ke-bep.jpg': DIRECT['r98ko7v0Vas'],
    'assets/article-thiet-ke-bep.webp': DIRECT['r98ko7v0Vas'],
    'assets/article-bo-tri-nha-hang.jpg': DIRECT['Yxm90BYxq3E'],
    'assets/article-bo-tri-nha-hang.webp': DIRECT['Yxm90BYxq3E'],
    'assets/article-hut-khoi.jpg': DIRECT['F9v4iq0RDZ0'],
    'assets/article-hut-khoi.webp': DIRECT['F9v4iq0RDZ0'],
    'assets/article-bao-tri.jpg': DIRECT['KDB8-kQw0Ac'],
    'assets/article-bao-tri.webp': DIRECT['KDB8-kQw0Ac'],
    'assets/article-xu-ly-loi.jpg': DIRECT['Y_tMFA6KCcI'],
    'assets/article-xu-ly-loi.webp': DIRECT['Y_tMFA6KCcI'],
    'assets/article-bep-canteen.jpg': DIRECT['KhZSSHoS6Xs'],
    'assets/article-bep-canteen.webp': DIRECT['KhZSSHoS6Xs'],
}

FONT_LINKS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800;900&family=Montserrat:wght@600;700;800;900&display=swap" rel="stylesheet">'
)

DOWNLOAD_RE = re.compile(r'https://unsplash\.com/photos/([^/]+)/download\?[^\"\']+')

for html in SITE.glob('*.html'):
    text = html.read_text(encoding='utf-8')
    text = DOWNLOAD_RE.sub(lambda m: DIRECT.get(m.group(1), DIRECT['r98ko7v0Vas']), text)
    for old, new in LOCAL.items():
        text = text.replace(old, new)
    text = text.replace('Dự án tiêu biểu', 'Mô hình dự án')
    text = text.replace('alt="Dự án bếp nhà hàng"', 'alt="Ảnh chụp thật mô hình bếp nhà hàng công nghiệp"')
    text = text.replace('alt="Dự án bếp khách sạn"', 'alt="Ảnh chụp thật mô hình bếp khách sạn"')
    text = text.replace('alt="Dự án bếp canteen"', 'alt="Ảnh chụp thật mô hình bếp canteen"')
    text = text.replace('alt="Dự án bếp trung tâm"', 'alt="Ảnh chụp thật mô hình bếp trung tâm"')
    text = text.replace('alt="Kỹ thuật sửa chữa bếp công nghiệp"', 'alt="Ảnh chụp thật kỹ thuật viên sửa chữa thiết bị"')
    text = text.replace('alt="Kỹ thuật viên sửa chữa bếp công nghiệp"', 'alt="Ảnh chụp thật kỹ thuật viên sửa chữa thiết bị"')
    if html.name == 'index.html':
        text = text.replace(
            'Tập trung vào các hệ thống bếp cần khảo sát, thiết kế, bố trí công năng, thi công và nghiệm thu đồng bộ. Mỗi dự án được tiếp cận theo mô hình vận hành thực tế.',
            'Tập trung vào các hệ thống bếp cần khảo sát, thiết kế, bố trí công năng, thi công và nghiệm thu đồng bộ. Hình ảnh tại khu vực này là ảnh chụp thật minh họa đúng từng mô hình, không phải ảnh AI và không được gắn nhãn là công trình Bếp Á Âu khi chưa có hồ sơ ảnh gốc.'
        )
    if html.name == 'du-an.html':
        text = text.replace(
            'Mỗi mô hình có tải phục vụ, nhịp chế biến và hạ tầng khác nhau. Bản vẽ phải bắt đầu từ dữ liệu sử dụng thực tế.',
            'Mỗi mô hình có tải phục vụ, nhịp chế biến và hạ tầng khác nhau. Bản vẽ phải bắt đầu từ dữ liệu sử dụng thực tế. Ảnh hiển thị là ảnh chụp thật đúng loại hình để minh họa cấu hình, chưa được tuyên bố là công trình đã thi công của Bếp Á Âu.'
        )
    if 'fonts.googleapis.com' not in text:
        text = text.replace('<link rel="stylesheet" href="styles.css">', FONT_LINKS + '<link rel="stylesheet" href="styles.css?v=7">')
    if '<meta name="robots"' not in text:
        text = text.replace('<meta name="viewport" content="width=device-width,initial-scale=1">', '<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">')
    text = text.replace('<script src="script.js"></script>', '<script src="script.js?v=7"></script>')
    html.write_text(text, encoding='utf-8')

css_path = SITE / 'styles.css'
css = css_path.read_text(encoding='utf-8')
for old, new in LOCAL.items():
    css = css.replace(old, new)
css = css.replace(
    'font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif',
    'font-family:"Be Vietnam Pro",ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif'
)
css += '''

/* Real-photo + typography refresh v7 */
body{font-family:"Be Vietnam Pro",ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-weight:400;letter-spacing:-.008em;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
h1,h2,h3,h4,.hero-sub,.menu,.btn,.eyebrow,.stat b,.project-info strong,.article-hero h1{font-family:"Montserrat","Be Vietnam Pro",ui-sans-serif,system-ui,sans-serif}
.hero h1,.page-hero h1,.article-hero h1{font-weight:900;letter-spacing:-.045em}
.section-head h2,.repair-copy h2,.project-detail h2{font-weight:800}.hero-sub,.menu,.btn,.eyebrow{font-weight:800}p,li{font-weight:400}
.hero-bg{background-image:url("https://images.pexels.com/photos/34276646/pexels-photo-34276646.jpeg?auto=compress&cs=tinysrgb&w=2200")!important;background-size:cover!important;background-position:center!important}
.project-card img,.news-card img,.gallery-item img,.repair-photo img,.project-detail img,.about-split img,.article-figure img{filter:saturate(1.02) contrast(1.02)}
'''
css_path.write_text(css, encoding='utf-8')
(SITE / 'robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf-8')

all_html='\n'.join(p.read_text(encoding='utf-8') for p in SITE.glob('*.html'))
assert all_html.count('images.pexels.com') >= 20
assert all_html.count('commons.wikimedia.org') >= 1
assert 'images.unsplash.com' not in all_html
assert 'unsplash.com/photos/' not in all_html
assert 'Be Vietnam Pro' in css and 'Montserrat' in css
print('Real content-matched photography and typography applied')
