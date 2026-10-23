"""Exercise the real configurator, catalog, upload validation and preview in Chrome.
Run: /tmp/minibrick-character-qa/bin/python background-tests/test_backgrounds.py
BACKGROUND_TEST_URL overrides localhost:3004.
"""
import json, os, re, io
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/backgrounds';OUT.mkdir(exist_ok=True,parents=True)
URL=os.environ.get('BACKGROUND_TEST_URL','http://localhost:3004')
manifest=json.loads((ROOT/'data/backgrounds.json').read_text())
entries=[x for x in manifest['backgrounds'] if x['src'] and x['thumbnail'] and x['status']!='excluded']
report={'originalsLoaded':0,'thumbnailsLoaded':0,'catalogSelections':0,'categoryFilters':[],'uploads':[],'responsiveWidths':[]}

def step(page,name):
 page.locator('.step-progress').get_by_role('button',name=re.compile(r'^(?:\d{2} )?'+name+r'$')).click()
 page.wait_for_function("()=>{const e=document.querySelector('.step-content>div');return e&&Number(getComputedStyle(e).opacity)>.999}")

def figures(page):
 return page.locator('.preview-pane svg[data-character-id]').evaluate_all('''els=>els.map(e=>({id:e.dataset.characterId,type:e.dataset.characterType,head:e.dataset.headId,face:e.dataset.faceId,layers:[...e.querySelectorAll('image[data-layer]')].map(i=>[i.dataset.layer,i.getAttribute('href')])}))''')

def background(page):
 return page.locator('.preview-pane [data-background-id]')

def ready(page):
 page.wait_for_function("()=>{const e=document.querySelector('.preview-pane [data-background-id]');const i=e?.querySelector('img');return e?.getAttribute('aria-busy')==='false'&&i?.complete&&i.naturalWidth>0}")

def upload_bytes(fmt,size=(800,400)):
 im=Image.new('RGB',size,'#90b8c4');d=ImageDraw.Draw(im)
 d.rectangle((0,0,190,400),fill='#c34d55');d.rectangle((600,0,800,400),fill='#e2ae48');d.ellipse((300,100,500,300),fill='#f9ead8')
 buf=io.BytesIO();im.save(buf,format=fmt);return buf.getvalue()

with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 page=browser.new_page(viewport={'width':1440,'height':1100},reduced_motion='reduce')
 errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
 page.add_init_script('''window.__revoked=[];const revoke=URL.revokeObjectURL.bind(URL);URL.revokeObjectURL=url=>{window.__revoked.push(url);revoke(url)};''')
 page.goto(URL+'/#configurator');page.wait_for_load_state('networkidle')
 # Preserve independently edited characters, counts, text and dates through every background operation.
 step(page,'Фигури');page.get_by_role('button',name='4 фигури',exact=True).click();step(page,'Стил')
 page.get_by_role('button',name=re.compile('^H04 —')).click();page.get_by_role('button',name=re.compile('^F08 —')).click();page.get_by_role('button',name=re.compile('^T11 —')).click()
 page.get_by_role('button',name='Фигура 2',exact=True).click();page.get_by_role('button',name=re.compile('^M06 —')).click()
 step(page,'Текст');page.get_by_role('textbox',name='Име 1',exact=True).fill('Ана');page.get_by_role('textbox',name='Кратка порака').fill('Нашиот момент');page.get_by_role('textbox',name='Посебен датум').fill('22.10.2026')
 step(page,'Позадина');ready(page);saved=figures(page)
 assert len(saved)==4 and saved[0]['head']=='H04' and saved[0]['face']=='F08' and saved[1]['face']=='M06'
 # Memoization: changing backgrounds must preserve the existing SVG nodes and mask IDs.
 page.locator('.preview-pane svg[data-character-id="figure-1"]').evaluate('e=>window.__originalFigure=e')
 gallery=page.get_by_role('group',name='Колекција на позадини',exact=True)
 expect(gallery.get_by_role('button')).to_have_count(110)
 assert gallery.get_by_role('button',name=re.compile('^Позадина BG014 ')).count()==0
 for cat in manifest['categories']:
  page.get_by_role('button',name=cat['name'],exact=True).click()
  expect(gallery.get_by_role('button')).to_have_count(cat['count'])
  assert all(cat['name'] in label for label in gallery.get_by_role('button').evaluate_all('els=>els.map(e=>e.getAttribute("aria-label"))'))
  report['categoryFilters'].append({'name':cat['name'],'count':cat['count']})
 page.get_by_role('button',name='Сите',exact=True).click()
 for entry in entries:
  choice=gallery.get_by_role('button',name=f"Позадина {entry['id']} — {entry['category']}",exact=True)
  choice.click();expect(choice).to_have_attribute('aria-pressed','true');expect(background(page)).to_have_attribute('data-background-id',entry['id']);ready(page)
  # Both real thumbnail and full source decode in the actual browser.
  choice.locator('img').last.evaluate('(e)=>e.decode()');report['thumbnailsLoaded']+=1
  assert background(page).locator('img').last.get_attribute('src')==entry['src'];report['originalsLoaded']+=1;report['catalogSelections']+=1
  assert background(page).locator('img').last.evaluate('e=>getComputedStyle(e).objectFit')=='cover'
 assert figures(page)==saved
 assert page.evaluate('window.__originalFigure===document.querySelector(".preview-pane svg[data-character-id=figure-1]")')
 # Native keyboard controls activate both categories and thumbnail selection.
 cat=page.get_by_role('button',name=manifest['categories'][0]['name'],exact=True);cat.focus();page.keyboard.press('Space');expect(cat).to_have_attribute('aria-pressed','true')
 option=gallery.get_by_role('button',name=re.compile('^Позадина BG002 '));option.focus();page.keyboard.press('Enter');expect(option).to_have_attribute('aria-pressed','true');ready(page)
 frame=page.locator('.preview-pane .frame-art')
 assert frame.evaluate('e=>getComputedStyle(e).overflow')=='hidden'
 assert frame.locator('.figure-row').evaluate('e=>Number(getComputedStyle(e).zIndex)')>background(page).evaluate('e=>Number(getComputedStyle(e).zIndex)')
 # Background covers frame bounds without distorting its aspect ratio.
 assert background(page).evaluate('e=>{const p=e.parentElement.getBoundingClientRect(),b=e.getBoundingClientRect();return b.x>=p.x-.1&&b.y>=p.y-.1&&b.right<=p.right+.1&&b.bottom<=p.bottom+.1}')
 page.locator('#configurator').screenshot(path=str(OUT/'desktop-catalog.png'))
 step(page,'Преглед');ready(page);expect(background(page)).to_have_attribute('data-background-id','BG002');expect(frame.locator('.art-message')).to_have_text('Нашиот момент');expect(frame.locator('.art-date')).to_have_text('22.10.2026');assert figures(page)==saved
 step(page,'Позадина');page.get_by_role('button',name='Своја фотографија',exact=True).click()
 file=page.get_by_label('Прикачи своја фотографија',exact=True)
 file.set_input_files({'name':'bad.txt','mimeType':'text/plain','buffer':b'hello'});expect(page.locator('#configurator').get_by_role('alert')).to_have_text('Изберете JPG, PNG или WebP фотографија.')
 file.set_input_files({'name':'huge.jpg','mimeType':'image/jpeg','buffer':b'0'*(10*1024*1024+1)});expect(page.locator('#configurator').get_by_role('alert')).to_have_text('Фотографијата мора да биде помала од 10 MB.')
 file.set_input_files({'name':'broken.png','mimeType':'image/png','buffer':b'not an image'});expect(page.locator('#configurator').get_by_role('alert')).to_contain_text('не може да се отвори')
 file.set_input_files({'name':'empty.png','mimeType':'image/png','buffer':b''});expect(page.locator('#configurator').get_by_role('alert')).to_contain_text('празна')
 previous=None
 for ext,mime,fmt in [('jpg','image/jpeg','JPEG'),('png','image/png','PNG'),('webp','image/webp','WEBP')]:
  file.set_input_files({'name':f'photo.{ext}','mimeType':mime,'buffer':upload_bytes(fmt)});expect(background(page)).to_have_attribute('data-background-id','custom');ready(page)
  source=background(page).locator('img').last.get_attribute('src');assert source.startswith('blob:')
  if previous:page.wait_for_function('url=>window.__revoked.includes(url)',arg=previous)
  previous=source;report['uploads'].append(ext);assert figures(page)==saved
 # Portrait and square sources keep their intrinsic proportions as well.
 for name,size in [('portrait',(400,800)),('square',(600,600))]:
  file.set_input_files({'name':name+'.png','mimeType':'image/png','buffer':upload_bytes('PNG',size)});ready(page)
  page.wait_for_function('url=>window.__revoked.includes(url)',arg=previous)
  previous=background(page).locator('img').last.get_attribute('src')
  assert background(page).locator('img').last.evaluate('e=>[e.naturalWidth,e.naturalHeight]')==list(size)
  assert background(page).locator('img').last.evaluate('e=>getComputedStyle(e).objectFit')=='cover'
 report['photoAspectRatios']=['landscape','portrait','square']
 # Invalid replacement keeps the existing valid photo and its object URL.
 file.set_input_files({'name':'invalid.svg','mimeType':'image/svg+xml','buffer':b'<svg/>'});expect(page.locator('#configurator').get_by_role('alert')).to_contain_text('JPG, PNG или WebP');assert background(page).locator('img').last.get_attribute('src')==previous
 page.get_by_role('button',name='Пополни ја рамката',exact=True).click()
 for label,val in [('Хоризонтална положба','23'),('Вертикална положба','77'),('Зголемување','1.6')]:page.get_by_role('group',name='Намести ја фотографијата',exact=True).get_by_role('slider',name=re.compile('^'+label)).fill(val)
 style=background(page).locator('img').last.get_attribute('style');assert 'object-fit: cover' in style and '23% 77%' in style and 'scale(1.6)' in style
 # Changing position materially changes the rendered crop, not just control values.
 first=background(page).screenshot();page.get_by_role('slider',name='Хоризонтална положба',exact=True).fill('88');assert background(page).screenshot()!=first
 page.get_by_role('slider',name='Хоризонтална положба',exact=True).fill('23')
 page.locator('#configurator').screenshot(path=str(OUT/'desktop-upload.png'))
 page.get_by_role('button',name='Од колекцијата',exact=True).click();expect(background(page)).to_have_attribute('data-background-id','BG002');ready(page)
 page.get_by_role('button',name='Своја фотографија',exact=True).click();ready(page);assert background(page).locator('img').last.get_attribute('src')==previous;assert background(page).locator('img').last.get_attribute('style')==style
 assert not page.evaluate('url=>window.__revoked.includes(url)',previous)
 step(page,'Преглед');ready(page);assert background(page).locator('img').last.get_attribute('style')==style;assert figures(page)==saved
 step(page,'Позадина')
 for width in [1440,1024,768,390,320]:
  page.set_viewport_size({'width':width,'height':900});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  for mode in ['Од колекцијата','Своја фотографија']:
   page.get_by_role('button',name=mode,exact=True).click();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,mode)
   assert page.locator('.config-controls').evaluate('e=>e.scrollWidth<=e.clientWidth'),(width,mode,'control overflow')
  report['responsiveWidths'].append(width)
  if width in [390,320]:page.locator('#configurator').screenshot(path=str(OUT/f'mobile-upload-{width}.png'))
 page.get_by_role('button',name='Врати ја почетната положба',exact=True).click();assert 'object-fit: cover' in background(page).locator('img').last.get_attribute('style')
 page.get_by_role('button',name='Отстрани',exact=True).click();page.wait_for_function('url=>window.__revoked.includes(url)',arg=previous);expect(background(page)).to_have_attribute('data-background-id','BG002')
 assert figures(page)==saved
 # A reset must also release its selected upload without leaking a live object URL.
 page.get_by_role('button',name='Своја фотографија',exact=True).click()
 file.set_input_files({'name':'reset-photo.png','mimeType':'image/png','buffer':upload_bytes('PNG')});ready(page)
 reset_url=background(page).locator('img').last.get_attribute('src')
 step(page,'Фигури');page.get_by_role('button',name='Почни одново',exact=True).click()
 page.wait_for_function('url=>window.__revoked.includes(url)',arg=reset_url);expect(background(page)).to_have_attribute('data-background-id','BG018');ready(page)
 # Inject missing thumbnail and full-resolution errors in a separate page.
 other=browser.new_page();other.route('**/backgrounds/thumbnails/BG018.jpg',lambda route:route.abort());other.route('**/backgrounds/BG018.jpg',lambda route:route.abort());other.goto(URL);other.wait_for_load_state('networkidle');step(other,'Позадина')
 expect(other.get_by_text('Прегледот не е достапен',exact=True)).to_be_visible();expect(other.locator('#configurator').get_by_role('alert')).to_contain_text('Позадината не може да се вчита.')
 other.unroute('**/backgrounds/BG018.jpg');other.get_by_role('button',name='Обиди се повторно',exact=True).click();ready(other);other.close()
 assert not errors,errors
 report.update({'BG014':'excluded','reviewEntriesRetained':sum(x['status']=='review' for x in entries),'independentFiguresPreserved':4,'textAndDate':'preserved','keyboard':'passed','layeringAndClipping':'passed','sameFigureDOMNodes':'passed','validation':['invalid type','oversize','corrupt image','empty file','invalid replacement preserves photo'],'cropAndFinalPreview':'passed','objectURLCleanup':'passed','imageErrorAndRetry':'passed','runtimeErrors':errors})
 (OUT/'test-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps(report,indent=2,ensure_ascii=False));browser.close()
