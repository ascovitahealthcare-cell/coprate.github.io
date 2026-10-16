"""Build crawlable static pages for GitHub Pages; no client router required."""
from pathlib import Path
import re,json,html
root=Path(__file__).resolve().parents[1]
s=(root/'source/original-site.html').read_text()
main=re.search(r'<main id="app">(.*?)</main>',s,re.S)[1]
starts=list(re.finditer(r'^<div class="page"[^>]+>',main,re.M))
pages={}
for i,m in enumerate(starts):
 tag=m[0]; route=re.search(r'data-route="([^"]+)"',tag)[1]
 body=main[m.end():starts[i+1].start() if i+1<len(starts) else len(main)].strip()
 body=re.sub(r'</div>\s*$','',body)
 body=re.sub(r'<script\b[^>]*>.*?</script>','',body,flags=re.S)
 pages[route]={'title':html.unescape(re.search(r'data-title="([^"]+)"',tag)[1]),'desc':html.unescape(re.search(r'data-desc="([^"]+)"',tag)[1]),'body':body}
pages['/']['body']=(root/'source/home.html').read_text()
pages['/']['desc']='Nutraceutical and effervescent tablet manufacturer in Anand, Gujarat. Private label, contract manufacturing, formulation and packaging. Discuss your product and request a quote from Ascovita Healthcare.'
pages['/brands']={'title':'Our Brands — Ozylix & Ascofizz | Ascovita Healthcare','desc':'Explore Ozylix, Ascovita Healthcare’s consumer wellness brand, and Ascofizz, our demonstration storefront for brand launch and e-commerce services.','body':(root/'source/brands.html').read_text()}
css=re.search(r'<style>(.*?)</style>',s,re.S)[1]
(root/'assets/site.css').write_text(css+'\n'+(root/'source/redesign.css').read_text())
nav='''<header class="nav"><div class="wrap"><div class="nav-in"><a class="brand" href="/" aria-label="Ascovita Healthcare home"><img src="/assets/ascovita_logo.png" alt="Ascovita Healthcare" width="200" height="88"></a><nav class="nav-links" id="navlinks" aria-label="Main navigation">'''
for route,label in [('/','Home'),('/about','About'),('/services','Manufacturing'),('/b2b','Products & B2B'),('/studio','Brand Launch'),('/brands','Our Brands'),('/contact','Contact')]:
 nav+=f'<a href="{route if route=="/" else route+"/"}" data-nav="{route}"'+(' class="nav-studio"' if route=='/studio' else '')+f'>{label}</a>'
nav+='''</nav><button class="nav-toggle" type="button" aria-label="Open navigation" aria-expanded="false" aria-controls="navlinks"><span></span></button></div></div></header>'''
footer='''<footer class="site-footer"><div class="wrap"><div class="footer-layout"><div><a href="/"><img src="/assets/ascovita_logo.png" alt="Ascovita Healthcare" width="200" height="88"></a><p>From a product idea to a brand of your own.</p><p class="sm">Nutraceutical manufacturing, formulation<br>and brand development in Anand, Gujarat.</p></div><div><h2>Explore</h2><a href="/services/">Manufacturing services</a><a href="/b2b/">Products & B2B catalogue</a><a href="/studio/">Launch your brand</a><a href="/global-export/">International buyers</a><a href="/brands/">Our brands</a></div><div><h2>Let’s talk</h2><a href="tel:+919898582650">+91 98985 82650</a><a href="mailto:ascovitahealthcare@gmail.com">ascovitahealthcare@gmail.com</a><a href="/contact/">Near Rajshivalay Cinema<br>Anand, Gujarat 388001, India</a><a href="https://www.instagram.com/ascovita_healthcare">Instagram ↗</a></div></div><p class="footer-fine">© 2026 Ascovita Healthcare. Food supplements are not intended to diagnose, treat, cure or prevent disease.</p></div></footer><a class="contact-float btn" href="https://wa.me/919898582650?text=Hello%20Ascovita%2C%20I%20would%20like%20to%20discuss%20nutraceutical%20manufacturing." aria-label="Enquire with Ascovita on WhatsApp">WhatsApp <span aria-hidden="true">↗</span></a>'''
def urls(t):
 def cv(m):
  v=m[1]; ps=v.split('/'); route=ps[0]; frag='/'.join(ps[1:]);return 'href="/'+(route+'/' if route else '')+('#'+frag if frag else '')+'"'
 t=re.sub(r'href="#/([^"\s]*)"',cv,t)
 return t.replace('./assets/','/assets/')
org={'@context':'https://schema.org','@graph':[{'@type':'Organization','@id':'https://www.ascovita.com/#organization','name':'Ascovita Healthcare','url':'https://www.ascovita.com/','logo':'https://www.ascovita.com/assets/ascovita_logo.png','telephone':'+91-98985-82650','email':'ascovitahealthcare@gmail.com','address':{'@type':'PostalAddress','streetAddress':'Near Rajshivalay Cinema','addressLocality':'Anand','addressRegion':'Gujarat','postalCode':'388001','addressCountry':'IN'},'brand':[{'@type':'Brand','name':'Ozylix','url':'https://www.ozylix.com/'}],'sameAs':['https://www.instagram.com/ascovita_healthcare','https://www.linkedin.com/company/ascovita-healthcare']}]}
# Only claim brand ownership for Ozylix. Ascofizz is a demo, not a live consumer brand.
for route,p in pages.items():
 url='https://www.ascovita.com'+(route+'/' if route!='/' else '/')
 body=p['body']
 replacements={'b2b_category_effervescent.webp':'hero-brand.webp','svc_private_label.webp':'packaging-new.webp','svc_white_label.webp':'packaging-new.webp','b2b_category_softgels.webp':'packaging-new.webp','svc_contract.webp':'manufacturing-new.webp','about_facility.webp':'manufacturing-new.webp','svc_development.webp':'development-new.webp','svc_packaging.webp':'packaging-new.webp','svc_brandlaunch.webp':'hero-brand.webp','hero-vertical.webp':'hero-brand.webp','global_export.webp':'export-new.webp','svc_distribution.webp':'export-new.webp','svc_franchise.webp':'packaging-new.webp','instagram_stay_sharp_brand_launch.webp':'development-new.webp','instagram_fuel_every_adventure.webp':'hero-brand.webp'}
 for before,after in replacements.items():body=body.replace(before,after)
 # Generated service artwork describes capabilities; it is not documentary facility photography.
 body=re.sub(r'(<img[^>]*src="[^"]*(?:manufacturing|development|packaging|export)-new.webp"[^>]*alt=")[^"]*(")',r'\1Illustrative nutraceutical service visual\2',body)

 if route=='/b2b':
  gallery='<section class="product-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">Real products from Ascovita</p><h2 class="t-1">Discover our <span class="grad">product range.</span></h2></div><p class="lede">Select a product to discuss availability,<br>private label and manufacturing.</p></div><div class="product-grid">'
  products=[('Glutathione','prod_glutathione.webp','orange'),('Vitamin C + Amla','prod_vitc.webp','amber'),('ACV + Moringa','prod_acv.webp','lime'),('Multidiata','prod_multidata.webp','blue'),('B12 + Biotin','prod_b12_biotin.webp','orange'),('L-Carnitine','prod_lcarnitine.webp','lime'),('Magnesium','prod_b12_magnesium.webp','blue'),('Iron + Calcium','prod_iron_calcium.webp','amber')]
  from urllib.parse import quote
  for name,asset,color in products:
   gallery+=f'<article class="product-tile"><a href="/contact/?product={quote(name)}"><div class="product-stage {color}"><img src="/assets/{asset}" alt="Real Ascovita {html.escape(name)} packaging" loading="lazy" width="600" height="600"></div><div class="product-label"><h3>{html.escape(name)}</h3><span aria-hidden="true">↗</span></div></a></article>'
  gallery+='</div><p class="range-note">Product specifications, pack size, formulation, MOQ and availability are confirmed by our team.</p></div></section>'
  body=body.replace('</section>','</section>'+gallery,1)
 if route=='/services':body=body.replace('</section>','</section><div class="wrap section-links" aria-label="Manufacturing services"><a href="#svc-privatelabel">Private label</a><a href="#svc-contract">Contract manufacturing</a><a href="#svc-development">Formulation</a><a href="#svc-design">Packaging</a></div>',1)
 if route!='/':body='<div class="wrap breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span>'+html.escape({'/studio':'Brand Launch','/b2b':'Products & B2B','/global-export':'International buyers'}.get(route,route.strip('/').title()))+'</span></div>'+body
 if route=='/contact':
  body=body.replace('<div style="margin-top:26px">','<form id="enquiry-form" style="margin-top:26px">',1)
  body=body.replace('<button class="btn" id="f-send" type="button"','<button class="btn" id="f-send" type="submit"')
  body=body.replace('Please add your name and what you need.</p>\n        </div>','Please add your name and what you need.</p>\n        </form>')
 body=re.sub(r'<canvas\b[^>]*>.*?</canvas>','',body,flags=re.S)
 body=re.sub(r'<div class="art-cap"[^>]*>.*?</div>','',body,flags=re.S)
 schema=json.loads(json.dumps(org));schema['@graph'].append({'@type':'WebPage','@id':url+'#webpage','url':url,'name':p['title'],'description':p['desc'],'isPartOf':{'@id':'https://www.ascovita.com/#website'},'about':{'@id':'https://www.ascovita.com/#organization'}})
 if route=='/':
  faqs=re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>',body,re.S)
  schema['@graph'].append({'@type':'FAQPage','mainEntity':[{'@type':'Question','name':html.unescape(q),'acceptedAnswer':{'@type':'Answer','text':html.unescape(a)}} for q,a in faqs]})
 schema['@graph'].append({'@type':'WebSite' ,'@id':'https://www.ascovita.com/#website','url':'https://www.ascovita.com/','name':'Ascovita Healthcare','publisher':{'@id':'https://www.ascovita.com/#organization'}})
 head=f'''<!doctype html><html lang="en-IN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(p['title'])}</title><meta name="description" content="{html.escape(p['desc'],quote=True)}"><link rel="canonical" href="{url}"><meta name="theme-color" content="#E8EDE6"><link rel="icon" href="/assets/ascovita_logo_192.png"><meta property="og:type" content="website"><meta property="og:site_name" content="Ascovita Healthcare"><meta property="og:title" content="{html.escape(p['title'],quote=True)}"><meta property="og:description" content="{html.escape(p['desc'],quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="https://www.ascovita.com/assets/hero-brand.webp"><meta name="twitter:card" content="summary_large_image"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet"><link rel="stylesheet" href="/assets/site.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script><script async src="https://www.googletagmanager.com/gtag/js?id=G-47ESBFEQ76"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-47ESBFEQ76');</script>'''
 if route=='/':head+='<link rel="preload" as="image" href="/assets/hero-brand.webp" fetchpriority="high">'
 if route=='/404':head+='<meta name="robots" content="noindex">'
 document=head+'</head><body><a class="skip" href="#app">Skip to content</a>'+nav+'<main id="app" tabindex="-1" data-page="'+route+'">'+urls(body)+'</main>'+footer+'<script src="/assets/site.js" defer></script></body></html>'
 document=document.replace('data-nav="'+route+'"','data-nav="'+route+'" aria-current="page"')
 path=root/('index.html' if route=='/' else '404.html' if route=='/404' else route.strip('/')+'/index.html');path.parent.mkdir(parents=True,exist_ok=True);path.write_text(document)
 if route not in ['/','/404']:
  (root/(route.strip('/')+'.html')).write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Ascovita Healthcare</title><link rel="canonical" href="{url}"><meta http-equiv="refresh" content="0;url={url}"></head><body><a href="{url}">Continue to Ascovita Healthcare</a></body></html>')
valid=[r for r in pages if r!='/404']
(root/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>https://www.ascovita.com'+(r+'/' if r!='/' else '/')+'</loc></url>' for r in valid)+'</urlset>')
(root/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /source/\nDisallow: /scripts/\nSitemap: https://www.ascovita.com/sitemap.xml\n')
(root/'.nojekyll').touch()
print('Built',len(pages),'pages')
