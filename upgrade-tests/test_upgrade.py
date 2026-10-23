"""Production integration checks. Uses synthetic contact details; exports are temporary."""
import io, json, os, re, tempfile
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/upgrade'
URL=os.environ.get('BACKGROUND_TEST_URL','http://localhost:3004')
artwork_bounds={}
for asset in (ROOT/'public/characters').rglob('*.png'):
 box=Image.open(asset).getbbox()
 if box:artwork_bounds['/'+asset.relative_to(ROOT/'public').as_posix()]=box
report={'frames':[],'calendarDates':[],'counts':[],'responsive':[]}
def step(page,name):
 page.locator('.step-progress').get_by_role('button',name=re.compile(name+'$')).click()
 headings={'Фигури':'Колку фигури сакате?','Стил':'Дајте им свој карактер.','Позадина':'Поставете ја сцената.','Текст':'Деталите се сè.','Преглед':'Вашата MiniBrick рамка.'}
 page.get_by_role('heading',name=headings[name],exact=True).wait_for()
 page.wait_for_function("()=>{const e=document.querySelector('.step-content>div');return e && +getComputedStyle(e).opacity>.999}")
def price(page):return int(page.locator('.preview-pane [data-price-total]').get_attribute('data-price-total'))
def figure_state(page):return page.locator('.preview-pane svg[data-character-id]').evaluate_all('(els)=>els.map(e=>[e.dataset.characterId,e.dataset.characterType,e.dataset.faceId,e.dataset.headId])')
def select_count(page,count):
 if count<=4:page.get_by_role('button',name=str(count)+(' фигура' if count==1 else ' фигури'),exact=True).click()
 else:
  page.get_by_role('button',name='Тимска рамка 4+',exact=True).click()
  page.get_by_label('Број на фигури во тимот',exact=True).fill(str(count))
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 context=browser.new_context(viewport={'width':1440,'height':1100},reduced_motion='reduce',permissions=['clipboard-read','clipboard-write'],accept_downloads=True)
 page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(URL+'/#configurator');page.wait_for_load_state('networkidle')
 frame=page.locator('.preview-pane .frame-assembly')
 expect(frame).to_have_attribute('data-frame-color','white');assert price(page)==1860
 original=figure_state(page)
 for label,color in [('Црна','black'),('Бела','white'),('Црна','black')]:
  page.get_by_role('button',name=label,exact=True).click();expect(frame).to_have_attribute('data-frame-color',color);assert figure_state(page)==original;assert price(page)==1860;report['frames'].append(color)
 # All supported counts have correct totals and stable slots.
 expected=[1460,1860,2260,2660,3010,3360,3710,4060]
 for n in range(1,9):
  select_count(page,n);assert price(page)==expected[n-1];expect(page.locator('.preview-pane svg[data-character-id]')).to_have_count(n);report['counts'].append({'figures':n,'total':price(page)})
 select_count(page,2);step(page,'Стил')
 page.get_by_role('button',name='Срце за фигура 1',exact=True).click();page.get_by_role('button',name='Милениче за фигура 1',exact=True).click();page.get_by_role('button',name='Мачка',exact=True).click();assert price(page)==2080
 expect(page.locator('.character-preview-pane [data-accessory="cat"]')).to_have_count(1)
 pet_labels=['Куче','Куче · бело','Куче · шарено','Мачка','Мачка · црна','Мачка · портокалова','Мачка · бела']
 pet_ids=['dog','dog-white','dog-spotted','cat','cat-black','cat-orange','cat-white']
 for label,id in zip(pet_labels,pet_ids):
  button=page.get_by_role('button',name=label,exact=True);button.click();button.locator('img').evaluate('e=>e.decode()');assert price(page)==2080;expect(page.locator(f'.character-preview-pane [data-accessory="{id}"]')).to_have_count(1)
 page.get_by_role('button',name='Мачка',exact=True).click();report['petVariants']=len(pet_ids)
 page.set_viewport_size({'width':320,'height':844});page.wait_for_timeout(350)
 for label in pet_labels:
  button=page.get_by_role('button',name=label,exact=True);assert button.evaluate('e=>e.scrollWidth<=e.clientWidth'),label
 assert page.locator('.config-controls').evaluate('e=>e.scrollWidth<=e.clientWidth')
 page.locator('.config-shell').screenshot(path=str(OUT/'accessories-mobile.png'))
 page.set_viewport_size({'width':1440,'height':1100})
 page.get_by_role('button',name='Фигура 2',exact=True).click();page.get_by_role('button',name='Пари за фигура 2',exact=True).click();page.get_by_role('button',name='Пиштол за фигура 2',exact=True).click();assert price(page)==2220
 page.get_by_role('button',name='Новороденче',exact=True).click();page.get_by_role('button',name=re.compile('^B04 —')).click()
 step(page,'Фигури');select_count(page,1);assert price(page)==1680
 select_count(page,2);assert price(page)==2220
 step(page,'Стил');page.get_by_role('button',name='Фигура 2',exact=True).click();expect(page.get_by_role('button',name='Пари за фигура 2',exact=True)).to_have_attribute('aria-pressed','true');expect(page.get_by_role('button',name='Пиштол за фигура 2',exact=True)).to_have_attribute('aria-pressed','true')
 step(page,'Позадина');saved=figure_state(page);page.get_by_role('button',name='Календар',exact=True).click()
 calendar=page.locator('.preview-pane .calendar-design')
 for y,m,d,expected_day in [(2024,2,29,29),(2025,2,29,28),(2026,10,26,26),(2026,11,31,30),(2000,2,29,29),(2100,2,29,28)]:
  page.get_by_label('Година',exact=True).select_option(str(y));page.get_by_label('Месец',exact=True).select_option(str(m));page.get_by_label('Ден',exact=True).select_option(str(min(d,expected_day)))
  expect(calendar).to_have_attribute('data-calendar-date',f'{y}-{m}-{expected_day}');expect(calendar.locator('circle')).to_have_count(1);expect(calendar.locator('g[data-selected="true"]')).to_have_attribute('data-calendar-day',str(expected_day));assert figure_state(page)==saved;report['calendarDates'].append(f'{y}-{m}-{expected_day}')
 # Actual automatic clamping when changing month and year.
 page.get_by_label('Година',exact=True).select_option('2024');page.get_by_label('Месец',exact=True).select_option('1');page.get_by_label('Ден',exact=True).select_option('31');page.get_by_label('Месец',exact=True).select_option('2');expect(page.get_by_label('Ден',exact=True)).to_have_value('29');page.get_by_label('Година',exact=True).select_option('2025');expect(page.get_by_label('Ден',exact=True)).to_have_value('28')
 page.get_by_label('Година',exact=True).select_option('2026');page.get_by_label('Месец',exact=True).select_option('10');page.get_by_label('Ден',exact=True).select_option('26')
 page.get_by_role('slider',name='Вертикална положба на фигурите',exact=True).fill('10');page.get_by_role('slider',name='Растојание меѓу фигурите',exact=True).fill('40')
 page.get_by_role('button',name='Од колекцијата',exact=True).click();page.get_by_role('button',name=re.compile('^Позадина BG085 —')).click();assert figure_state(page)==saved
 page.get_by_role('button',name='Календар',exact=True).click();expect(calendar).to_have_attribute('data-calendar-date','2026-10-26');expect(frame).to_have_attribute('data-frame-color','black')
 page.locator('.config-shell').screenshot(path=str(OUT/'calendar-desktop.png'))
 step(page,'Текст');page.get_by_role('textbox',name='Кратка порака').fill('Нашиот датум');page.get_by_role('checkbox',name='Подлога за читливост',exact=True).check();step(page,'Преглед')
 expect(calendar).to_have_attribute('data-calendar-date','2026-10-26');assert price(page)==2220;assert figure_state(page)==saved
 expect(page.locator('.summary-list')).to_contain_text('Календар — 26 октомври 2026');expect(page.locator('.summary-list')).to_contain_text('Црна')
 page.get_by_role('button',name='Подготви барање',exact=True).click();expect(page.locator('#configurator').get_by_role('alert')).to_have_count(4)
 for label,value in [('Име и презиме','Тест Корисник'),('Телефонски број','+389 (70) 123-456'),('Адреса за достава','Тест адреса 12'),('Град','Скопје')]:page.get_by_label(label,exact=True).fill(value)
 page.get_by_role('button',name='Подготви барање',exact=True).click();prepared=page.get_by_role('region',name='Подготвено барање');expect(prepared).to_be_visible()
 page.get_by_role('button',name='Копирај барање',exact=True).click();expect(prepared.get_by_role('status')).to_contain_text('копирано');copied=page.evaluate('navigator.clipboard.readText()');assert 'Нашиот датум' in copied and 'НЕ е испратено' in copied
 with page.expect_download() as info:page.get_by_role('button',name='Преземи податоци',exact=True).click()
 download=info.value
 with tempfile.TemporaryDirectory() as temp:
  target=Path(temp)/'order.json';download.save_as(target);order=json.loads(target.read_text());assert order['pricing']['total']==2220;assert order['background']['calendar']=={'year':2026,'month':10,'day':26};assert order['characters'][1]['type']=='baby';assert 'hairId' not in order['characters'][1];assert len(order['characters'][1]['accessories'])==2
 page.get_by_label('Име и презиме',exact=True).fill('Тест Втор');expect(prepared).to_have_count(0)
 step(page,'Позадина');page.get_by_role('button',name='Своја фотографија',exact=True).click()
 buf=io.BytesIO();Image.new('RGB',(800,400),'#91a2b8').save(buf,format='PNG');page.get_by_label('Прикачи своја фотографија',exact=True).set_input_files({'name':'synthetic-photo.png','mimeType':'image/png','buffer':buf.getvalue()})
 background=page.locator('.preview-pane [data-background-id="custom"]');expect(background).to_have_attribute('aria-busy','false');assert figure_state(page)==saved
 step(page,'Преглед');expect(page.get_by_label('Име и презиме',exact=True)).to_have_value('Тест Втор');page.get_by_role('button',name='Подготви барање',exact=True).click();text=page.get_by_label('Текст на барањето',exact=True).input_value();assert 'blob:' not in text and 'НЕ е приложена' in text
 with page.expect_download() as info:page.get_by_role('button',name='Преземи податоци',exact=True).click()
 with tempfile.TemporaryDirectory() as temp:
  target=Path(temp)/'order.json';info.value.save_as(target);order=json.loads(target.read_text());assert 'blob:' not in json.dumps(order);assert not order['background']['photo']['attached']
 report['order']={'validation':'passed','copy':'passed','export':'passed','photoUrlSanitization':'passed','newbornFields':'passed'}
 # New features at narrow widths and large groups, plus physical asset bounds.
 step(page,'Позадина');page.get_by_role('button',name='Календар',exact=True).click()
 for width in [1440,1024,768,390,320]:
  page.set_viewport_size({'width':width,'height':1000 if width>500 else 844})
  for count in [1,2,4,8]:
   step(page,'Фигури');select_count(page,count);step(page,'Позадина');page.wait_for_timeout(300)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,count,'overflow')
   geometry=calendar.evaluate('(e)=>{const a=e.getBoundingClientRect(),f=e.closest(".frame-art").getBoundingClientRect();return {width:a.width,height:a.height,inside:a.x>=f.x&&a.right<=f.right&&a.y>=f.y&&a.bottom<=f.bottom}}');assert geometry['inside'] and geometry['width']>100
   # Test actual artwork, excluding the SVG viewport's transparent letterboxing.
   bounds=page.locator('.preview-pane svg[data-character-id]').evaluate_all('''(els,boxes)=>els.map(e=>{const f=e.closest('.frame-art').getBoundingClientRect(),parts=[...e.querySelectorAll('image[data-layer]')].filter(p=>p.dataset.layer!=='face').map(p=>{const b=boxes[p.getAttribute('href')],m=p.getScreenCTM();return [new DOMPoint(b[0],b[1]).matrixTransform(m),new DOMPoint(b[2],b[3]).matrixTransform(m)]});const x=Math.min(...parts.map(p=>p[0].x)),y=Math.min(...parts.map(p=>p[0].y)),r=Math.max(...parts.map(p=>p[1].x)),b=Math.max(...parts.map(p=>p[1].y));const viewport=e.getBoundingClientRect();return {w:viewport.width,h:viewport.height,inside:x>=f.x-1&&r<=f.right+1&&y>=f.y-1&&b<=f.bottom+1}})''',artwork_bounds);assert all(b['w']>8 and b['h']>10 and b['inside'] for b in bounds),(width,count,bounds)
   report['responsive'].append({'width':width,'figures':count,'calendar':geometry,'figuresInBounds':True})
  step(page,'Стил');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,'style overflow')
  step(page,'Преглед');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,'review overflow')
  if width in [1440,390,320]:page.locator('.config-shell').screenshot(path=str(OUT/f'review-{width}.png'))
 report['runtimeErrors']=errors;assert not errors,errors
 (OUT/'browser-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));browser.close();print(json.dumps(report,ensure_ascii=False))
