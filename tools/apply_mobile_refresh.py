from pathlib import Path
import re

SITE = Path('_site')
HERO_ASSET = 'assets/generated/hero.jpg'

for html in SITE.glob('*.html'):
    text = html.read_text(encoding='utf-8')
    if html.name == 'index.html':
        text = text.replace(
            '<h1>THIẾT KẾ - THI CÔNG <span>BẾP CÔNG NGHIỆP</span></h1>',
            '<h1><span class="hero-title-main">THIẾT KẾ -<br class="mobile-title-break"> THI CÔNG</span><span class="hero-title-accent">BẾP CÔNG NGHIỆP</span></h1>'
        )
    html.write_text(text, encoding='utf-8')

css_path = SITE / 'styles.css'
css = css_path.read_text(encoding='utf-8')
css = re.sub(r'/\* Mobile hero refresh v1[123] \*/.*?(?=\n/\*|\Z)', '', css, flags=re.S)
css += f'''
/* Mobile hero refresh v13 */
.hero-bg{{background-image:url("{HERO_ASSET}")!important;background-position:64% center!important;background-size:cover!important}}
.hero h1 .hero-title-main{{display:block;color:#fff}}.hero h1 .hero-title-accent{{display:block;color:var(--red2)}}.mobile-title-break{{display:none}}
@media(max-width:640px){{
.nav{{height:70px;gap:10px}}.brand img{{width:146px;max-width:44vw}}.language-switcher{{top:15px!important;right:68px!important;padding:6px 9px!important}}
.hero,.hero-grid{{min-height:820px}}.hero-copy{{padding:46px 0 244px}}.hero-bg{{background-position:68% center!important;transform:scale(1.02)!important;animation:none!important}}.hero:before{{background:linear-gradient(180deg,rgba(0,0,0,.34) 0%,rgba(0,0,0,.72) 42%,rgba(5,5,6,.97) 84%)!important}}
.hero h1{{font-size:clamp(2.35rem,11.2vw,2.95rem)!important;line-height:1.02!important;letter-spacing:-.032em!important;margin:.7rem 0 1rem!important;max-width:100%!important}}.hero h1 .hero-title-main,.hero h1 .hero-title-accent{{line-height:1.02!important}}.hero h1 .hero-title-accent{{font-size:.95em;margin-top:.1em}}.mobile-title-break{{display:block}}
.hero-sub{{font-size:clamp(.9rem,4vw,1.06rem)!important;line-height:1.42!important;letter-spacing:.012em!important;margin-bottom:22px!important}}.hero-bullets{{gap:10px!important;font-size:.89rem!important;line-height:1.45!important;margin-bottom:28px!important}}.hero-bullets li{{align-items:flex-start!important;gap:10px!important}}.check{{margin-top:1px}}
.actions{{gap:10px!important}}.btn{{min-height:48px;padding:13px 15px!important;font-size:.72rem!important}}.hero-services{{bottom:14px!important;width:calc(100% - 20px)!important}}.hero-service{{min-height:88px!important;padding:12px 7px!important}}
.contact-dock{{right:10px!important;bottom:84px!important;gap:7px!important}}.contact-dock__item{{min-height:42px!important;padding:4px!important}}.contact-dock__icon{{width:34px!important;height:34px!important;font-size:14px!important}}.page-hero h1,.article-hero h1{{line-height:1.06!important;letter-spacing:-.035em!important}}
}}
@media(max-width:390px){{.brand img{{width:136px}}.hero h1{{font-size:2.28rem!important}}.hero-sub{{font-size:.88rem!important}}.hero-bullets{{font-size:.84rem!important}}.btn{{padding:12px 13px!important}}}}
'''
css_path.write_text(css, encoding='utf-8')

index = (SITE / 'index.html').read_text(encoding='utf-8')
hero = SITE / HERO_ASSET
assert hero.exists() and hero.stat().st_size > 25000
assert 'hero-title-main' in index and 'mobile-title-break' in index
assert HERO_ASSET in css and 'Mobile hero refresh v13' in css
print('Mobile typography fixed and newly generated kitchen hero applied')
