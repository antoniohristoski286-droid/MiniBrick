import hashlib,json,zipfile
from pathlib import Path
from urllib.parse import urlparse,parse_qs
from playwright.sync_api import sync_playwright,expect
ROOT=Path('/Users/antoniohristoski/programiranje/MiniBrick'); OUT=ROOT/'artifacts/client-gallery'
manifest=json.loads((OUT/'manifest.json').read_text())
with zipfile.ZipFile('/Users/antoniohristoski/Downloads/Archive 2.zip') as archive:
 entries={Path(n).name:n for n in archive.namelist() if not n.startswith('__MACOSX/') and n.lower().endswith('.jpg')}
 assert len(entries)==len(manifest)==50
 for m in manifest:
  data=(ROOT/'public/projects/client'/m['file']).read_bytes()
  assert data==archive.read(entries[m['file']])
  assert hashlib.sha256(data).hexdigest()==m['sha256']
errors=[];bad=[];cases=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 context=browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce')
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:bad.append({'url':r.url,'status':r.status}) if r.status>=400 else None)
 page.goto('http://localhost:3004/gallery');page.wait_for_load_state('networkidle')
 expect(page.locator('.project-gallery figure')).to_have_count(50)
 assert page.locator('.project-gallery figcaption a').count()==0
 actual=[]
 for i,button in enumerate(page.locator('.gallery-image-button').all()):
  button.scroll_into_view_if_needed();img=button.locator('img');img.evaluate('(e)=>e.decode()')
  assert img.evaluate('e=>e.naturalWidth>0&&e.naturalHeight>0')
  assert img.evaluate('e=>getComputedStyle(e).objectFit')=='contain'
  src=parse_qs(urlparse(img.get_attribute('src')).query)['url'][0];actual.append(src)
  button.click();dialog=page.get_by_role('dialog');expect(dialog).to_be_visible()
  full=dialog.locator('img');full.evaluate('e=>e.decode()');assert parse_qs(urlparse(full.get_attribute('src')).query)['url'][0]==src
  page.keyboard.press('Escape');expect(dialog).not_to_be_visible();expect(button).to_be_focused()
 assert set(actual)=={'/projects/client/'+m['file'] for m in manifest}
 for width in [1440,768,390,320]:
  page.set_viewport_size({'width':width,'height':1000});page.evaluate('document.activeElement.blur();window.scrollTo(0,0)')
  page.wait_for_timeout(150)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  cases.append({'width':width,'overflow':False})
  if width in [1440,390]:page.screenshot(path=str(OUT/f'gallery-{width}.png'))
 page.set_viewport_size({'width':1440,'height':1000});page.goto('http://localhost:3004');page.wait_for_load_state('networkidle')
 hero=page.locator('.hero-real-project img');hero.evaluate('e=>e.decode()');assert 'birthday-frame-hq.jpg' in hero.get_attribute('src')
 for selector in ['.showcase-photo img','.showcase-detail img']:
  img=page.locator(selector);img.scroll_into_view_if_needed();img.evaluate('e=>e.decode()');assert '%2Fprojects%2Fclient%2F' in img.get_attribute('src');assert img.evaluate('e=>getComputedStyle(e).objectFit')=='contain'
 assert page.locator('.showcase-photo img').evaluate('e=>getComputedStyle(e).transform')=='none'
 page.locator('#gallery').screenshot(path=str(OUT/'homepage-gallery.png'))
 expect(page.locator('#configurator')).to_be_visible();expect(page.locator('.step-progress button')).to_have_count(5)
 assert not errors and not bad,{'errors':errors,'httpErrors':bad}
 report={'clientPhotos':50,'zipBytesUnchanged':True,'allThumbnailsDecoded':True,'allLightboxesDecoded':True,'escapeAndFocusRestore':True,'uncroppedPhotos':True,'responsiveCases':cases,'homepageGallery':'two client photos','hero':'preserved','configurator':'present, five steps','runtimeErrors':errors,'httpErrors':bad}
 (OUT/'browser-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
 context.close();browser.close()
