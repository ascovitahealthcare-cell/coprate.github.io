"""Check generated pages, metadata, structured data, assets and internal links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.tags=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
pages=[root/'index.html',*root.glob('*/index.html'),root/'404.html']
errors=[]
for path in pages:
 s=path.read_text();p=Page(s);tags=p.tags
 ids=[a['id'] for t,a in tags if 'id' in a]
 if len(ids)!=len(set(ids)):errors.append(f'{path}: duplicate ids')
 if sum(t=='h1' for t,a in tags)!=1:errors.append(f'{path}: expected one H1')
 if sum(t=='link' and a.get('rel')=='canonical' for t,a in tags)!=1:errors.append(f'{path}: canonical')
 if '<form' in s and '</form>' not in s:errors.append(f'{path}: unclosed form')
 for script in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):json.loads(script)
 for tag,a in tags:
  target=a.get('src') if tag in ['img','script'] else a.get('href') if tag in ['a','link'] else None
  if not target:continue
  if target.startswith('#/') :errors.append(f'{path}: legacy hash link {target}')
  u=urlsplit(target)
  if u.scheme or u.netloc:continue
  dest=(root/u.path.lstrip('/')) if u.path.startswith('/') else path.parent/u.path if u.path else path
  if dest.is_dir():dest=dest/'index.html'
  if not dest.exists():errors.append(f'{path.relative_to(root)}: missing {target}')
  elif tag=='a' and u.fragment:
   if not re.search(r'id=[\"\']'+re.escape(unquote(u.fragment))+r'[\"\']',dest.read_text()):errors.append(f'{path.relative_to(root)}: missing anchor {target}')
ET.parse(root/'sitemap.xml')
print('\n'.join(errors) if errors else f'PASS: {len(pages)} pages; H1, canonical, JSON-LD, local assets, links and anchors; sitemap XML')
raise SystemExit(bool(errors))
