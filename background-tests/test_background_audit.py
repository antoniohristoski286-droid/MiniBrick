"""Focused composition audit: long copy, readable overlays, loading and preview continuity."""
import io,json,os,re
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/backgrounds/audit';OUT.mkdir(parents=True,exist_ok=True);URL=os.environ.get('BACKGROUND_TEST_URL','http://localhost:3004')
def step(page,n):
 page.locator('.step-progress button').nth(n).click();page.wait_for_function("()=>{const e=document.querySelector('.step-content>div');return e&&Number(getComputedStyle(e).opacity)>.999}")
def geometry(page):
 page.wait_for_function("()=>[...document.querySelectorAll('.preview-pane .figure-row>div')].every(e=>{const m=new DOMMatrixReadOnly(getComputedStyle(e).transform);return Math.abs(m.a-1)<.0001&&Math.abs(m.f)<.001})")
 page.wait_for_timeout(100)
 return page.locator('.preview-pane .frame-art').evaluate('''f=>{const b=f.getBoundingClientRect();const r=e=>{const p=e.getBoundingClientRect();return [p.x-b.x,p.y-b.y,p.width,p.height].map(n=>Math.round(n*100)/100)};return {frame:[b.width,b.height],figures:[...f.querySelectorAll('svg[data-character-id]')].map(r)}}''')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');page=browser.new_page(viewport={'width':1440,'height':1200},reduced_motion='reduce');errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(URL);page.wait_for_load_state('networkidle')
 step(page,0);page.get_by_role('button',name='4 фигури',exact=True).click();step(page,3);initial=geometry(page)
 names=['Александра-Марија','Константин-Андреј']*2
 for i,name in enumerate(names,1):page.get_by_role('textbox',name=f'Име {i}',exact=True).fill(name)
 page.get_by_role('textbox',name='Кратка порака').fill('W'*42);page.get_by_role('textbox',name='Посебен датум').fill('23.10.2026 · Спомени')
 expect(page.locator('.preview-pane .art-names')).to_have_text(' & '.join(names));assert geometry(page)==initial,('Long text shifted or resized the figures',initial,geometry(page))
 plate=page.get_by_role('checkbox',name='Подлога за читливост',exact=True);plate.check()
 page.get_by_role('slider',name='Вертикална положба на фигурите',exact=True).fill('-15');page.get_by_role('slider',name='Растојание меѓу фигурите',exact=True).fill('40');page.get_by_role('slider',name='Вертикална положба на текстот',exact=True).fill('-20');expected=geometry(page)
 assert page.locator('.preview-pane .frame-text-backplate').evaluate('e=>Number(getComputedStyle(e).zIndex)')<page.locator('.preview-pane .figure-row').evaluate('e=>Number(getComputedStyle(e).zIndex)')
 page.locator('.preview-pane').screenshot(path=str(OUT/'after-long-text.png'))
 # Keep full source and figures mounted while a new background is loading.
 step(page,2);pending=[];page.route('**/backgrounds/BG003.jpg',lambda route:pending.append(route));page.get_by_role('button',name=re.compile('^Позадина BG003 —')).click()
 expect(page.locator('.preview-pane [data-background-id]')).to_have_attribute('aria-busy','true');assert geometry(page)==expected
 assert pending;pending.pop().fulfill(path=str(ROOT/'public/backgrounds/BG003.jpg'),content_type='image/jpeg');page.wait_for_function("()=>document.querySelector('.preview-pane [data-background-id]').getAttribute('aria-busy')==='false'")
 # Filters are view-only and cannot replace the selected background.
 page.get_by_role('button',name='Божиќ и зима',exact=True).click();expect(page.locator('.preview-pane [data-background-id]')).to_have_attribute('data-background-id','BG003')
 page.get_by_role('button',name='Сите',exact=True).click();expect(page.get_by_role('group',name='Колекција на позадини',exact=True).get_by_role('button')).to_have_count(110)
 for index in [3,4,2,4]:
  step(page,index);assert geometry(page)==expected,(index,expected,geometry(page));expect(plate).to_be_checked()
  expect(page.locator('.preview-pane [data-background-id]')).to_have_attribute('data-background-id','BG003')
 # Dark upload reproduces the observed contrast problem; the opt-in plate restores contrast.
 step(page,2);page.get_by_role('button',name='Своја фотографија',exact=True).click();buf=io.BytesIO();Image.new('RGB',(800,1000),'#1a1a1a').save(buf,format='PNG');page.get_by_label('Прикачи своја фотографија',exact=True).set_input_files({'name':'dark.png','mimeType':'image/png','buffer':buf.getvalue()});expect(page.locator('.preview-pane [data-background-id]')).to_have_attribute('data-background-id','custom')
 page.wait_for_function("()=>document.querySelector('.preview-pane [data-background-id]').getAttribute('aria-busy')==='false'");expect(page.locator('.preview-pane .art-copy-readable')).to_have_count(1);page.locator('.preview-pane').screenshot(path=str(OUT/'after-dark-photo.png'))
 image_source=page.locator('.preview-pane [data-background-id] img').get_attribute('src');step(page,4);assert page.locator('.preview-pane [data-background-id] img').get_attribute('src')==image_source;assert geometry(page)==expected
 cases=0
 for width in [1440,1024,768,390,320]:
  page.set_viewport_size({'width':width,'height':1100})
  for offset in [-70,0,5]:
   slider=page.get_by_role('slider',name='Вертикална положба на текстот',exact=True);slider.fill(str(offset));expect(page.locator('.preview-pane .art-copy')).to_have_attribute('data-text-vertical',str(offset));page.wait_for_timeout(100)
   for enabled in [False,True]:
    plate.set_checked(enabled);page.wait_for_timeout(100)
    rows=page.locator('.preview-pane .art-copy-content').evaluate('''e=>{const f=e.closest('.frame-art').getBoundingClientRect(),r=e.getBoundingClientRect();return {inside:r.top>=f.top-1&&r.left>=f.left-1&&r.bottom<=f.bottom+1&&r.right<=f.right+1,rows:[...e.children].map(c=>({scroll:c.scrollWidth,width:c.clientWidth,ellipsis:getComputedStyle(c).textOverflow,text:c.textContent}))}}''')
    assert rows['inside'],(width,offset,rows)
    assert all(r['scroll']<=r['width']+1 and r['ellipsis']!='ellipsis' for r in rows['rows']),(width,rows)
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
    cases+=1
  if width in [390,320]:page.locator('.preview-pane').screenshot(path=str(OUT/f'after-mobile-{width}.png'))
 # No visible backing plate is left behind when optional fields are empty.
 step(page,3)
 for name in ['Име 1','Име 2','Име 3','Име 4','Кратка порака','Посебен датум']:page.get_by_role('textbox',name=name,exact=name.startswith('Име')).fill('')
 expect(page.locator('.preview-pane .art-copy')).to_have_text('');expect(page.locator('.preview-pane .art-copy-readable')).to_have_count(0)
 assert not errors,errors
 report={'confirmedBefore':['long names truncated with ellipsis (548px content in 210px row)','dark text unreadable over dark uploaded photo','long unbroken review values changed frame width from 238.56px to 243.13px'],'longTextAndReadabilityCases':cases,'fullNamesAndMessage':'preserved without ellipsis','textInsideFrame':'passed','emptyFields':'preserved, no backing plate','figureGeometry':'unchanged by text edits','loadingGeometry':'stable','categorySelection':'preserved','catalogAndCustomFinalReview':'synchronized','runtimeErrors':errors,'frameColor':'This legacy audit checks the default white frame; upgrade-tests/test_upgrade.py verifies both frame colors.'}
 (OUT/'audit-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2));browser.close()
