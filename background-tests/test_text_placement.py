"""Verify optional text, independent placement, final preview and responsive bounds."""
import json,os,re
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/backgrounds';URL=os.environ.get('BACKGROUND_TEST_URL','http://localhost:3004')
def step(page,name):
 page.locator('.step-progress').get_by_role('button',name=re.compile(r'^(?:\d{2} )?'+name+r'$')).click()
 page.wait_for_function("()=>{const e=document.querySelector('.step-content>div');return e&&Number(getComputedStyle(e).opacity)>.999}")
def relative_rect(page,selector):
 page.wait_for_timeout(100)
 return page.locator('.preview-pane '+selector).evaluate('e=>{const r=e.getBoundingClientRect(),f=e.closest(".frame-art").getBoundingClientRect();return {x:r.x-f.x,y:r.y-f.y,w:r.width,h:r.height}}')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');page=browser.new_page(viewport={'width':1440,'height':1100},reduced_motion='reduce');errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(URL+'/#configurator');page.wait_for_load_state('networkidle');step(page,'Текст')
 slider=page.get_by_role('slider',name='Вертикална положба на текстот',exact=True);copy=page.locator('.preview-pane .art-copy')
 base=relative_rect(page,'.art-copy');figure=relative_rect(page,'.figure-row')
 slider.fill('-40');expect(copy).to_have_attribute('data-text-vertical','-40');up=relative_rect(page,'.art-copy');assert up['y']<base['y']
 slider.fill('5');expect(copy).to_have_attribute('data-text-vertical','5');down=relative_rect(page,'.art-copy');assert down['y']>base['y'];assert relative_rect(page,'.figure-row')==figure
 slider.focus();page.keyboard.press('ArrowLeft');expect(slider).to_have_value('4')
 page.get_by_role('button',name='Врати ја почетната положба на текстот',exact=True).click();expect(slider).to_have_value('0')
 # Empty fields render no replacement names, message or date, and do not move figures.
 for name in ['Име 1','Име 2','Кратка порака','Посебен датум']:
  page.get_by_role('textbox',name=name,exact=(name.startswith('Име'))).fill('')
 for selector in ['.art-names','.art-message','.art-date']:
  expect(copy.locator(selector)).to_have_text('')
  assert copy.locator(selector).evaluate('e=>e.clientHeight')>0
 assert relative_rect(page,'.figure-row')==figure
 expect(page.locator('.preview-pane').get_by_text('Вашите имиња',exact=True)).to_have_count(0)
 step(page,'Преглед');expect(copy).to_have_text('');step(page,'Текст')
 # Only the nonempty fields are displayed, with no separator for an omitted name.
 page.get_by_role('textbox',name='Име 2',exact=True).fill('Ана');expect(copy.locator('.art-names')).to_have_text('Ана')
 page.get_by_role('textbox',name='Кратка порака').fill('Нашиот момент');page.get_by_role('textbox',name='Посебен датум').fill('22.10.2026')
 slider.fill('-30');page.get_by_role('slider',name='Вертикална положба на фигурите',exact=True).fill('-10');page.get_by_role('slider',name='Растојание меѓу фигурите',exact=True).fill('65')
 step(page,'Позадина');page.get_by_role('button',name=re.compile('^Позадина BG025 —')).click();expect(slider).to_have_value('-30')
 step(page,'Преглед');expect(copy).to_have_attribute('data-text-vertical','-30');expect(copy.locator('.art-names')).to_have_text('Ана');expect(copy.locator('.art-message')).to_have_text('Нашиот момент');expect(page.get_by_role('slider',name='Растојание меѓу фигурите',exact=True)).to_have_value('65')
 page.locator('.preview-pane').screenshot(path=str(OUT/'text-placement-desktop.png'))
 cases=0
 for width in [1440,768,390,320]:
  page.set_viewport_size({'width':width,'height':1000})
  for value in [-70,0,5]:
   slider.fill(str(value));expect(copy).to_have_attribute('data-text-vertical',str(value))
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   for selector in ['.art-names','.art-message','.art-date']:
    assert page.locator('.preview-pane '+selector).evaluate('e=>{const r=e.getBoundingClientRect(),f=e.closest(".frame-art").getBoundingClientRect();return r.top>=f.top-1&&r.bottom<=f.bottom+1}'),(width,value,selector,relative_rect(page,selector))
   cases+=1
  if width==390:page.locator('.preview-pane').screenshot(path=str(OUT/'text-placement-mobile.png'))
 assert not errors,errors
 report={'movement':'passed','emptyFields':'no fallback text','textRowsReserveSpace':True,'figuresUnchangedByText':'passed','partialNames':'passed','stateAcrossStepsAndBackgrounds':'preserved','keyboard':'passed','responsiveBoundsCases':cases,'widths':[1440,768,390,320],'runtimeErrors':errors}
 (OUT/'text-placement-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));browser.close()
