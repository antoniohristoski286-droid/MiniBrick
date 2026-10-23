"""Original-photo resolution and larger team figure bounds across viewports."""
import json
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/photo-quality'
base=json.loads((OUT/'team-before.json').read_text());base={(r['width'],r['count']):r['scale']['x'] for r in base}
bounds={}
for file in (ROOT/'public/characters').rglob('*.png'):
 box=Image.open(file).getbbox()
 if box:bounds['/'+file.relative_to(ROOT/'public').as_posix()]=box
for item in json.loads((OUT/'sources.json').read_text()):
 image=Image.open(ROOT/item['path']);assert image.size==tuple(item['newDimensions']);assert min(image.size)>=1200
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');page=b.new_page(viewport={'width':1440,'height':1100},reduced_motion='reduce',device_scale_factor=2);errors=[];failed=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:failed.append(r.url) if r.status>=400 else None)
 page.goto('http://localhost:3004');page.wait_for_load_state('networkidle');hero=page.locator('.hero-real-project img');hero.evaluate('e=>e.decode()');src=hero.get_attribute('src');assert 'birthday-frame-hq.jpg' in src and 'q=90' in src
 page.locator('.hero').screenshot(path=str(OUT/'hero-retina.png'))
 results=[]
 for width in [1440,390,320]:
  page.set_viewport_size({'width':width,'height':1100});page.wait_for_timeout(250)
  for n in [5,8,12,24]:
   page.get_by_role('button',name='Тимска рамка 4+',exact=True).click();page.get_by_label('Број на фигури во тимот',exact=True).fill(str(n));page.wait_for_timeout(350)
   scale=page.locator('.preview-pane svg[data-character-id]').first.evaluate('e=>e.getScreenCTM().a');increase=scale/base[(width,n)];assert increase>=1.2,(width,n,increase)
   rects=page.locator('.preview-pane svg[data-character-id]').evaluate_all('''(els,boxes)=>els.map(svg=>{const f=svg.closest('.frame-art').getBoundingClientRect(),parts=[...svg.querySelectorAll('image[data-layer]')].filter(e=>e.dataset.layer!=='face').map(e=>{const box=boxes[e.getAttribute('href')],m=e.getScreenCTM();return [new DOMPoint(box[0],box[1]).matrixTransform(m),new DOMPoint(box[2],box[3]).matrixTransform(m)]});const x=Math.min(...parts.map(p=>p[0].x)),y=Math.min(...parts.map(p=>p[0].y)),r=Math.max(...parts.map(p=>p[1].x)),bottom=Math.max(...parts.map(p=>p[1].y));return {x,y,r,bottom,inside:x>=f.x-1&&y>=f.y-1&&r<=f.right+1&&bottom<=f.bottom+1}})''',bounds)
   assert all(r['inside'] for r in rects),(width,n,rects)
   for i,a in enumerate(rects):
    for z in rects[i+1:]:assert min(a['r'],z['r'])-max(a['x'],z['x'])<=2 or min(a['bottom'],z['bottom'])-max(a['y'],z['y'])<=2,(width,n,'figures overlap',a,z)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   results.append({'width':width,'count':n,'scaleIncrease':round(increase,3)})
   if n==12:page.locator('.preview-pane').screenshot(path=str(OUT/f'team-{width}.png'))
 page.goto('http://localhost:3004/gallery');page.wait_for_load_state('networkidle')
 for button in page.locator('.gallery-image-button').all():
  button.scroll_into_view_if_needed();img=button.locator('img');img.evaluate('e=>e.decode()');assert 'q=90' in img.get_attribute('src');button.click();expect(page.get_by_role('dialog')).to_be_visible();page.get_by_role('dialog').locator('img').evaluate('e=>e.decode()');assert 'q=90' in page.get_by_role('dialog').locator('img').get_attribute('src');page.keyboard.press('Escape')
 assert not errors,errors;assert not failed,failed
 report={'originalsReplaced':4,'imageQuality':90,'teamScale':results,'realArtworkBounds':'passed','figureOverlap':'none','galleryAndLightbox':'passed','runtimeErrors':errors,'failedRequests':failed};(OUT/'browser-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True);page.close();b.close()
