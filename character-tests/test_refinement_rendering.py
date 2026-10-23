"""Confirm asset-only refinements keep uniform scaling in both existing previews."""
from pathlib import Path
import os,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/characters';URL=os.environ.get('CHARACTER_TEST_URL','http://localhost:3004')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 page=browser.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce');page.goto(URL);page.wait_for_load_state('networkidle')
 page.get_by_role('button',name='02 Стил',exact=True).click();page.get_by_role('heading',name='Дајте им свој карактер.').wait_for()
 results=[]
 for id,name in [('H01','Брановидна кафеава'),('H04','Долга црна'),('H09','Кратка руса')]:
  page.get_by_role('button',name=f'{id} — {name}',exact=True).click()
  scale=page.locator('.character-preview-pane svg[data-character-id]').evaluate('''e=>{const m=e.getScreenCTM();return {x:m.a,y:m.d,box:e.getAttribute('viewBox')}}''')
  assert abs(scale['x']-scale['y'])<.0001 and scale['box']=='0 0 512 768',scale
  results.append({'previewHead':id,'uniformScale':True})
 page.get_by_role('button',name='Фигури',exact=True).click();page.get_by_role('button',name='4 фигури',exact=True).click();page.get_by_role('button',name='03 Позадина',exact=True).click();page.get_by_role('heading',name='Поставете ја сцената.').wait_for()
 page.wait_for_function('''()=>[...document.querySelectorAll('.preview-pane .modular-figure-row>div')].every(e=>Number(getComputedStyle(e).opacity)>.999)''')
 scales=page.locator('.preview-pane svg[data-character-id]').evaluate_all('''els=>els.map(e=>{const m=e.getScreenCTM();return {id:e.dataset.characterId,x:m.a,y:m.d,box:e.getAttribute('viewBox')}})''')
 for value in scales:assert abs(value['x']-value['y'])<.0001 and value['box']=='0 0 512 768',value
 assert max(value['x'] for value in scales)-min(value['x'] for value in scales)<.0001,scales
 results.append({'frameFigures':4,'uniformScale':True,'equalFigureScale':True})
 page.wait_for_load_state('networkidle');page.locator('.preview-pane').screenshot(path=str(OUT/'refined-frame-four-figures.png'))
 (OUT/'refinement-rendering-report.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results));browser.close()
