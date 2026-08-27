from pathlib import Path
import re

SITE = Path('_site')
css_path = SITE / 'styles.css'
css = css_path.read_text(encoding='utf-8')

# Remove an older generated desktop patch if Actions is re-run locally.
css = re.sub(r'/\* Desktop hero layout fix v14 \*/.*?(?=\n/\*|\Z)', '', css, flags=re.S)

css += r'''

/* Desktop hero layout fix v14 */
@media (min-width:981px){
  .hero{min-height:860px;align-items:stretch;overflow:hidden}
  .hero-grid{min-height:860px;align-items:start}
  .hero-copy{position:relative;z-index:3;padding:88px 0 220px;max-width:900px}
  .hero h1{font-size:clamp(3.55rem,5.15vw,5.45rem)!important;line-height:.94!important;letter-spacing:-.05em!important;margin:.55rem 0 1rem!important;max-width:900px!important}
  .hero h1 .hero-title-main,.hero h1 .hero-title-accent{line-height:.94!important}
  .hero h1 .hero-title-accent{margin-top:.08em}
  .hero-sub{font-size:clamp(1.15rem,1.75vw,1.62rem)!important;line-height:1.22!important;margin-bottom:22px!important}
  .hero-bullets{gap:10px!important;margin-bottom:28px!important;line-height:1.42!important}
  .actions{position:relative;z-index:4;margin-bottom:0}
  .hero-services{bottom:24px!important;z-index:5}
  .hero-service{min-height:104px!important;padding:20px!important}
}

/* Short desktop/laptop screens were the source of the clipping shown in QA. */
@media (min-width:981px) and (max-height:900px){
  .hero{min-height:790px}
  .hero-grid{min-height:790px}
  .hero-copy{padding:52px 0 190px;max-width:820px}
  .hero h1{font-size:clamp(3.05rem,4.55vw,4.65rem)!important;line-height:.95!important;max-width:820px!important}
  .hero h1 .hero-title-main,.hero h1 .hero-title-accent{line-height:.95!important}
  .hero-sub{font-size:clamp(1rem,1.45vw,1.36rem)!important;margin-bottom:18px!important}
  .hero-bullets{gap:7px!important;margin-bottom:20px!important;font-size:.94rem!important}
  .btn{padding:13px 20px!important;min-height:48px}
  .hero-services{bottom:16px!important}
  .hero-service{min-height:92px!important;padding:16px 18px!important}
}

/* Keep floating contacts away from the service rail on wide screens. */
@media (min-width:1280px){
  .contact-dock{right:16px!important;bottom:18px!important;gap:8px!important}
  .contact-dock__item{min-height:44px!important;padding:5px 9px 5px 5px!important}
  .contact-dock__icon{width:34px!important;height:34px!important}
  .contact-dock__label{font-size:12px!important}
}
'''

css_path.write_text(css, encoding='utf-8')

assert 'Desktop hero layout fix v14' in css
assert 'max-height:900px' in css
assert '.hero-copy{padding:52px 0 190px' in css
print('Desktop hero clipping/CTA overlap fixed')
