"""Supporting content, full-frame layers and shared all-mode figure geometry."""
import io, json, re
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/visual-refinement'
DISCLAIMER='Производите претставуваат самостојни, небрандирани коцки за составување и не се поврзани со ниту еден официјален бренд или производител.'
def step(page,name):
 page.locator('.step-progress').get_by_role('button',name=re.compile(name+'$')).click()
 page.wait_for_function("()=>{const e=document.querySelector('.step-content>div');return e && +getComputedStyle(e).opacity>.999}")
def geometry(page):
 page.wait_for_function("()=>[...document.querySelectorAll('.preview-pane .figure-row>div')].every(e=>Math.abs(new DOMMatrixReadOnly(getComputedStyle(e).transform).a-1)<.0001)")
 return page.locator('.preview-pane').evaluate('''pane=>{const f=pane.querySelector('.frame-art').getBoundingClientRect();return {frame:[f.width,f.height],figures:[...pane.querySelectorAll('svg[data-character-id]')].map(e=>{const m=e.getScreenCTM(),b=e.viewBox.baseVal;return [m.a/f.width,m.d/f.height,(m.e-f.x)/f.width,(m.f-f.y)/f.height,b.width*m.a,b.height*m.d]})}}''')
def coverage(page,calendar=False):
 selector='.calendar-background' if calendar else '[data-background-id]'
 layer=page.locator('.preview-pane '+selector)
 if not calendar:expect(layer).to_have_attribute('aria-busy','false')
 assert layer.evaluate("e=>{const a=e.getBoundingClientRect(),b=e.closest('.frame-art').getBoundingClientRect();return Math.abs(a.x-b.x)<1&&Math.abs(a.y-b.y)<1&&Math.abs(a.width-b.width)<1&&Math.abs(a.height-b.height)<1}")
 if not calendar:
  image=layer.locator('img').last;image.evaluate('e=>e.decode()')
  assert image.evaluate("e=>getComputedStyle(e).objectFit==='cover'") or layer.locator('img').count()==2
def select_count(page,count):
 if count<=4:page.get_by_role('button',name=str(count)+(' фигура' if count==1 else ' фигури'),exact=True).click()
 else:
  page.get_by_role('button',name='Тимска рамка 4+',exact=True).click()
  page.get_by_label('Број на фигури во тимот',exact=True).fill(str(count))
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 context=browser.new_context(viewport={'width':1440,'height':1100},reduced_motion='reduce')
 page=context.new_page();errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
 page.goto('http://localhost:3004/#configurator');page.wait_for_load_state('networkidle')
 expect(page.locator('#about')).to_contain_text('Во големиот избор на подароци')
 expect(page.locator('footer')).to_contain_text(DISCLAIMER)
 step(page,'Стил')
 for name in ['Срце','Пари','Пиштол']:page.get_by_role('button',name=name+' за фигура 1',exact=True).click()
 step(page,'Позадина');data=io.BytesIO();Image.new('RGB',(1000,300),'#526a84').save(data,format='PNG')
 page.get_by_role('button',name='Своја фотографија',exact=True).click();page.get_by_label('Прикачи своја фотографија',exact=True).set_input_files({'name':'wide.png','mimeType':'image/png','buffer':data.getvalue()});coverage(page)
 cases=0
 for width in [1440,768,390,320]:
  page.set_viewport_size({'width':width,'height':1100 if width>760 else 900});page.wait_for_timeout(300)
  print('Checking viewport',width,flush=True)
  for count in range(1,9):
   step(page,'Фигури');select_count(page,count);step(page,'Позадина')
   page.get_by_role('button',name='Од колекцијата',exact=True).click();coverage(page);reference=geometry(page)
   assert page.locator('.preview-pane .figure-row').evaluate("e=>e.getBoundingClientRect().bottom<=e.closest('.frame-art').querySelector('.art-names').getBoundingClientRect().top+1"), (width,count,'default text overlap')
   for mode in ['Календар','Своја фотографија']:
    page.get_by_role('button',name=mode,exact=True).click();coverage(page,mode=='Календар');actual=geometry(page)
    assert all(abs(x-y)<.002 for a,b in zip(reference['figures'],actual['figures']) for x,y in zip(a,b)),(width,count,mode,reference,actual)
    assert reference['frame']==actual['frame'],(width,count,mode)
    for svg in page.locator('.preview-pane svg[data-character-id]').all():
     assert svg.evaluate('''e=>{const m=e.getScreenCTM(),b=e.viewBox.baseVal,f=e.closest('.frame-art').getBoundingClientRect();return m.e>=f.x-1&&m.f>=f.y-1&&m.e+b.width*m.a<=f.right+1&&m.f+b.height*m.d<=f.bottom+1}'''),(width,count,mode)
    cases+=1
   page.get_by_role('button',name='Цела фотографија',exact=True).click();coverage(page)
   assert page.locator('.preview-pane [data-background-id="custom"] img').count()==2
   step(page,'Текст');text=geometry(page);step(page,'Преглед');assert geometry(page)==text
   step(page,'Позадина');page.get_by_role('button',name='Пополни ја рамката',exact=True).click()
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,count)
  if width in [1440,390]:
   step(page,'Фигури');select_count(page,2);step(page,'Позадина');page.get_by_role('button',name='Календар',exact=True).click();page.locator('.preview-pane').screenshot(path=str(OUT/f'calendar-{width}.png'))
   step(page,'Стил');page.locator('.preview-pane').screenshot(path=str(OUT/f'character-{width}.png'))
   page.locator('.story-editorial img').scroll_into_view_if_needed();page.locator('.story-editorial img').evaluate('e=>e.decode()');page.locator('#about').screenshot(path=str(OUT/f'story-{width}.png'))
 # The dedicated gallery uses all 50 original client photos, never invented projects.
 gallery=context.new_page();gallery.on('pageerror',lambda error:errors.append(str(error)));gallery.goto('http://localhost:3004/gallery');gallery.wait_for_load_state('networkidle')
 expect(gallery.get_by_role('heading',level=1)).to_contain_text('Наши');expect(gallery.locator('footer')).to_contain_text(DISCLAIMER)
 expect(gallery.locator('.project-gallery figure')).to_have_count(50)
 button=gallery.get_by_role('button',name=re.compile('^Зголеми:')).first
 button.scroll_into_view_if_needed();button.locator('img').evaluate('e=>e.decode()');button.click();dialog=gallery.get_by_role('dialog');expect(dialog).to_be_visible();expect(gallery.get_by_role('button',name='Затвори фотографија',exact=True)).to_be_focused()
 gallery.keyboard.press('Escape');expect(dialog).not_to_be_visible();expect(button).to_be_focused()
 button.click();gallery.get_by_role('button',name='Затвори фотографија',exact=True).click();expect(button).to_be_focused()
 for width in [1440,768,390,320]:
  gallery.set_viewport_size({'width':width,'height':900});gallery.wait_for_timeout(200);assert gallery.evaluate('document.documentElement.scrollWidth<=innerWidth')
  gallery.evaluate('document.activeElement.blur();window.scrollTo(0,0)');gallery.screenshot(path=str(OUT/f'gallery-{width}.png'),full_page=True)
 assert not errors,errors
 report={'geometryComparisons':cases,'counts':list(range(1,9)),'widths':[1440,768,390,320],'catalogPhotoCalendarScale':'identical','backgroundCoverage':'full interior','wholePhotoBackdrop':'passed','textFinalConsistency':'passed','galleryPhotos':50,'galleryLightboxKeyboard':'passed','honestStory':'passed','disclaimer':'exact','runtimeErrors':errors}
 (OUT/'browser-report.json').write_text(json.dumps(report,indent=2));page.close();gallery.close();context.close();browser.close();print(json.dumps(report),flush=True)
