# Ascovita Healthcare

Static, crawlable corporate website hosted by GitHub Pages at www.ascovita.com.

## Update

Edit `source/home.html`, `source/brands.html`, `source/redesign.css` or the retained interior content in `source/original-site.html`. Interactive behavior is in `assets/site.js`. Then run:

```sh
python scripts/build.py
python scripts/check.py
node --check assets/site.js
```

Commit the generated HTML and assets together. No package installation or runtime backend is needed. Existing `#/...` bookmarks redirect to real static pages. `.html` compatibility pages point to canonical directory URLs. The CNAME and existing Analytics measurement ID are preserved.

## Images

New built-in image generation produced `assets/hero-brand.webp`, `assets/manufacturing-new.webp`, `assets/development-new.webp`, `assets/packaging-new.webp`, and `assets/export-new.webp`. Original logo files and real product pack photos remain intact. The hero uses the original Glutathione and logo references. Generated manufacturing/service scenes are illustrative, not photographs of the actual Ascovita facility.

Image briefs: premium photorealistic sage/ivory wellness product hero with original white/orange Glutathione packaging and white cap; stainless tablet production still life; formulation laboratory still life with glassware and botanicals; white tubes and cartons with packaging swatches; unbranded supplement packaging, shipping cartons and globe for export. No invented certifications, people, or facility claims.

## SEO and enquiry measurement

Eight indexable pages, individual metadata and canonicals, linked Organization/WebSite/WebPage schema, homepage FAQ schema, robots.txt and sitemap.xml. Contact CTA events record only channel and page path. Form details are sent only through the customer's WhatsApp action and never included in analytics. These changes address technical SEO and conversion clarity; enquiry recovery requires comparing Search Console and Analytics data.
