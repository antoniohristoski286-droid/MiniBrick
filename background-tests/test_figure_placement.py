"""Verify figure placement, preserved customization, final preview and visible asset bounds."""
import json, os, re
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/backgrounds'
URL=os.environ.get('BACKGROUND_TEST_URL','http://localhost:3004')

def step(page,name):
 page.locator('.step-progress').get_by_role('button',name=re.compile(r'^(?:\d{2} )?'+name+r'$')).click()
 page.wait_for_function("()=>{const e=document.querySelector('.step-content>div');return e&&Number(getComputedStyle(e).opacity)>.999}")

def appearance(page):
 return page.locator('.preview-pane svg[data-character-id]').evaluate_all("els=>els.map(e=>({id:e.dataset.characterId,face:e.dataset.faceId,head:e.dataset.headId,parts:[...e.querySelectorAll('image[data-layer]')].map(i=>i.getAttribute('href'))}))")

def metrics(page):
 page.wait_for_function("()=>[...document.querySelectorAll('.preview-pane .figure-row>div')].every(e=>{const m=new DOMMatrixReadOnly(getComputedStyle(e).transform);return Math.abs(m.a-1)<.0001&&Math.abs(m.f)<.001})")
 page.wait_for_timeout(100)
 return page.locator('.preview-pane .figure-row>div').evaluate_all('els=>els.map(e=>{const r=e.getBoundingClientRect(),f=e.closest(".frame-art").getBoundingClientRect(),m=e.querySelector("svg").getScreenCTM();return {x:r.x+r.width/2-f.x,y:r.y+r.height/2-f.y,scale:m.a}})')

bounds={}
for path in (ROOT/'public/characters').rglob('*.png'):
 box=Image.open(path).getbbox()
 if box:bounds['/'+path.relative_to(ROOT/'public').as_posix()]=box
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 page=browser.new_page(viewport={'width':1440,'height':1100},reduced_motion='reduce');errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(URL+'/#configurator');page.wait_for_load_state('networkidle')
 step(page,'Стил');page.get_by_role('button',name=re.compile('^H04 —')).click();page.get_by_role('button',name=re.compile('^F08 —')).click()
 step(page,'Позадина');row=page.locator('.preview-pane .figure-row');saved=appearance(page);before=metrics(page)
 vertical=page.get_by_role('slider',name='Вертикална положба на фигурите',exact=True);spacing=page.get_by_role('slider',name='Растојание меѓу фигурите',exact=True)
 vertical.fill('-20');up=metrics(page);assert up[0]['y']<before[0]['y'];vertical.fill('20');down=metrics(page);assert down[0]['y']>before[0]['y']
 spacing.fill('100');spread=metrics(page);assert spread[1]['x']-spread[0]['x']>before[1]['x']-before[0]['x']
 assert all(abs(a['scale']-b['scale'])<.001 for a,b in zip(before,spread)),(before,spread);assert appearance(page)==saved,(saved,appearance(page))
 # Controls support keyboard changes and state survives changing the background and steps.
 vertical.focus();page.keyboard.press('ArrowDown');expect(vertical).to_have_value('19')
 page.get_by_role('button',name=re.compile('^Позадина BG025 —')).click();expect(row).to_have_attribute('data-figure-vertical','19');assert appearance(page)==saved
 step(page,'Текст');expect(vertical).to_have_value('19');step(page,'Преглед');expect(spacing).to_have_value('100');expect(row).to_have_attribute('data-figure-spacing','100')
 page.locator('.preview-pane').screenshot(path=str(OUT/'figure-placement-desktop.png'))
 cases=0
 for width in [1440,390,320]:
  page.set_viewport_size({'width':width,'height':1000})
  for count in [1,2,3,4]:
   step(page,'Фигури');page.get_by_role('button',name=f'{count} '+('фигура' if count==1 else 'фигури'),exact=True).click();step(page,'Позадина')
   if count==1:expect(spacing).to_be_disabled()
   else:expect(spacing).to_be_enabled()
   for y in [-30,0,30]:
    vertical.fill(str(y))
    for gap in [0,100]:
     if count>1:spacing.fill(str(gap))
     metrics(page)
     assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
     # Check real nontransparent artwork, not transparent SVG canvas margins.
     result=page.evaluate('''boxes=>{const f=document.querySelector('.preview-pane .frame-art').getBoundingClientRect();return [...document.querySelectorAll('.preview-pane image[data-layer]')].filter(e=>e.dataset.layer!=='face').map(e=>{const b=boxes[e.getAttribute('href')],m=e.getScreenCTM();const a=new DOMPoint(b[0],b[1]).matrixTransform(m),z=new DOMPoint(b[2],b[3]).matrixTransform(m);return {part:e.dataset.layer,inside:a.x>=f.left-1&&a.y>=f.top-1&&z.x<=f.right+1&&z.y<=f.bottom+1,a:[a.x,a.y],z:[z.x,z.y],frame:[f.left,f.top,f.right,f.bottom]}})}''',bounds)
     assert all(part['inside'] for part in result),(width,count,y,gap,result)
     cases+=1
  if width==390:page.locator('.preview-pane').screenshot(path=str(OUT/'figure-placement-mobile.png'))
 # Reset only placement; retain the selected artwork and individually customized figures.
 step(page,'Фигури');page.get_by_role('button',name='2 фигури',exact=True).click();step(page,'Позадина')
 page.get_by_role('button',name='Врати ја почетната положба на фигурите',exact=True).click();expect(vertical).to_have_value('0');expect(spacing).to_have_value('0');expect(page.locator('.preview-pane svg[data-character-id]')).to_have_count(2);assert appearance(page)==saved
 expect(page.locator('.preview-pane [data-background-id]')).to_have_attribute('data-background-id','BG025')
 assert not errors,errors
 report={'placementBoundsCases':cases,'counts':[1,2,3,4],'widths':[1440,390,320],'verticalMovement':'passed','spacing':'passed','uniformScale':'preserved','keyboard':'passed','finalPreview':'synchronized','customization':'preserved','reset':'passed','runtimeErrors':errors}
 (OUT/'figure-placement-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));browser.close()
