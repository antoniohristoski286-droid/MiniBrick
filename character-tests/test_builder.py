"""Behavior tests against the real existing configurator. Requires Python Playwright.
Usage: CHARACTER_TEST_URL=http://localhost:3010 python character-tests/test_builder.py
"""
import json, os, re
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/characters';OUT.mkdir(exist_ok=True,parents=True)
URL=os.environ.get('CHARACTER_TEST_URL','http://localhost:3010')
report={'faceHairCombinations':0,'torsoColors':0,'legColors':0,'newbornFaces':0,'newbornBodyColors':0,'viewports':[]}

def choice(page,id):
 return page.get_by_role('button',name=re.compile(r'^'+re.escape(id)+r' — '))
def step(page,name):
 page.locator('.step-progress').get_by_role('button',name=re.compile(r'^(?:\d{2} )?'+name+r'$')).click()
 if name=='Стил':page.get_by_role('heading',name='Дајте им свој карактер.').wait_for()
def layers(page):
 return page.locator('.character-preview-pane .minibrick-character image[data-layer]').evaluate_all('(els)=>Object.fromEntries(els.map(e=>[e.dataset.layer,e.getAttribute("href")]))')
def same_except(before,after,key):
 assert {k:v for k,v in before.items() if k!=key}=={k:v for k,v in after.items() if k!=key},(before,after,key)
def ready_motion(page):
 page.wait_for_function('''()=>{const e=document.querySelector('.step-content>div');return e && Number(getComputedStyle(e).opacity)>.999}''')
def capture(page,name):
 ready_motion(page);page.wait_for_load_state('networkidle');page.screenshot(path=str(OUT/name))

with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1,reduced_motion='reduce')
 errors=[];missing=[]
 page.on('pageerror',lambda error:errors.append(str(error)))
 page.on('response',lambda response:missing.append(response.url) if response.status>=400 and not (os.environ.get('CHARACTER_TEST_PRODUCTION') and response.status==404 and response.url.endswith('/dev/characters')) else None)
 page.goto(URL);page.wait_for_load_state('networkidle');step(page,'Стил')
 # Exercise all 23 non-baby faces on each of the 9 heads. Other layers must stay fixed.
 for label,prefix,count in [('Женски','F',13),('Машки','M',6),('Дете','C',4)]:
  page.get_by_role('button',name=label,exact=True).click()
  for hair in range(1,10):
   id=f'H{hair:02}';before=layers(page);choice(page,id).click();after=layers(page);same_except(before,after,'head')
   expect(page.locator('.character-preview-pane svg[data-character-id]')).to_have_attribute('data-head-id',id)
   for face in range(1,count+1):
    fid=f'{prefix}{face:02}';before=layers(page);choice(page,fid).click();after=layers(page);same_except(before,after,'face')
    expect(page.locator('.character-preview-pane svg[data-character-id]')).to_have_attribute('data-face-id',fid)
    report['faceHairCombinations']+=1
 # All body variants: source changes only in its own layer; head and face never move/reset.
 for prefix,key,counter in [('T','torso','torsoColors'),('L','legs','legColors')]:
  for color in range(1,13):
   id=f'{prefix}{color:02}';before=layers(page);choice(page,id).click();after=layers(page);same_except(before,after,key)
   assert after[key].endswith(f'/{id}.png');report[counter]+=1
 adult=layers(page)
 page.get_by_role('button',name='Новороденче',exact=True).click()
 assert set(layers(page))=={'baby-body','face'}
 for group in ['Избери фризура','Боја на горен дел','Боја на долен дел']:
  expect(page.get_by_role('group',name=re.compile('^'+group))).to_have_count(0)
 for i in range(1,5):
  choice(page,f'B{i:02}').click();assert layers(page)['face'].endswith(f'/B{i:02}.png');report['newbornFaces']+=1
 for i in range(1,13):
  before=layers(page);choice(page,f'BC{i:02}').click();after=layers(page);same_except(before,after,'baby-body');report['newbornBodyColors']+=1
 page.locator('.config-shell').scroll_into_view_if_needed();capture(page,'builder-newborn-desktop.png')
 page.get_by_role('button',name='Дете',exact=True).click();assert layers(page)==adult,'Adult selections lost after newborn'
 page.get_by_role('button',name='Новороденче',exact=True).click();assert layers(page)['face'].endswith('/B04.png') and layers(page)['baby-body'].endswith('/BC12.png')
 page.get_by_role('button',name='Женски',exact=True).click();expect(choice(page,'F13')).to_have_attribute('aria-pressed','true')
 # Keyboard activation uses native buttons and shows the same selected state.
 choice(page,'F02').focus();page.keyboard.press('Space');expect(choice(page,'F02')).to_have_attribute('aria-pressed','true')
 # Four independently configured stable characters, including a newborn.
 step(page,'Фигури');page.get_by_role('button',name='4 фигури',exact=True).click();step(page,'Стил')
 selections=[('Женски','F02','H03','T11','L12'),('Машки','M06','H07','T02','L04'),('Дете','C02','H02','T05','L09'),('Новороденче','B01',None,'BC03',None)]
 saved={}
 for index,(kind,face,hair,torso,lower) in enumerate(selections,1):
  page.get_by_role('button',name=f'Фигура {index}',exact=True).click();page.get_by_role('button',name=kind,exact=True).click()
  for id in [face,hair,torso,lower]:
   if id:choice(page,id).click()
  saved[f'figure-{index}']=layers(page)
 for index in [2,1,4,3,1]:
  page.get_by_role('button',name=f'Фигура {index}',exact=True).click();assert layers(page)==saved[f'figure-{index}'],'Character state leaked'
 # Count reduction and readdition must retain removed figures instead of recreating them.
 step(page,'Фигури');page.get_by_role('button',name='1 фигура',exact=True).click();step(page,'Стил');assert layers(page)==saved['figure-1']
 step(page,'Фигури');page.get_by_role('button',name='4 фигури',exact=True).click();step(page,'Стил')
 for index in range(1,5):
  page.get_by_role('button',name=f'Фигура {index}',exact=True).click();assert layers(page)==saved[f'figure-{index}']
 page.get_by_role('button',name='Фигура 1',exact=True).click()
 page.locator('.config-shell').scroll_into_view_if_needed();capture(page,'builder-desktop-final.png')
 # Existing frame preview stays synchronized and all unrelated defaults survive.
 step(page,'Позадина');frame=page.locator('.preview-pane .frame-art')
 expect(frame.locator('[data-background-id]')).to_have_attribute('data-background-id','BG018');expect(frame.locator('.art-names')).to_have_text('Бојана & Петар')
 expect(frame.locator('.art-message')).to_have_text('Against all odds');expect(frame.locator('.art-date')).to_have_text('14.02.2026')
 for index in range(1,5):
  actual=frame.locator(f'svg[data-character-id="figure-{index}"] image[data-layer]').evaluate_all('(els)=>Object.fromEntries(els.map(e=>[e.dataset.layer,e.getAttribute("href")]))')
  assert actual==saved[f'figure-{index}'],'Frame preview is not synchronized'
 page.locator('.preview-pane').screenshot(path=str(OUT/'frame-four-figures-final.png'))
 # Narrow layouts and active choices remain within their actual control containers.
 step(page,'Стил')
 for width,height in [(1024,900),(768,1024),(390,844),(320,700)]:
  page.set_viewport_size({'width':width,'height':height});page.wait_for_load_state('networkidle')
  layout=page.evaluate('''()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,oversized:[...document.querySelectorAll('.config-controls button')].filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>e.textContent.trim())})''')
  assert layout['scroll']<=width,layout
  assert not layout['oversized'],layout
  report['viewports'].append(layout)
  if width in [390,320]:
   choice(page,'F08').click();expect(choice(page,'F08')).to_have_attribute('aria-pressed','true')
   page.locator('.character-preview-pane').scroll_into_view_if_needed();capture(page,f'builder-mobile-{width}-final.png')
 # Development-only gallery covers every asset in the actual renderer.
 page.set_viewport_size({'width':1440,'height':1000});page.goto(URL+'/dev/characters');page.wait_for_load_state('networkidle')
 if os.environ.get('CHARACTER_TEST_PRODUCTION'):
  expect(page.get_by_role('heading',name='Страницата не е пронајдена.',exact=True)).to_be_visible()
 else:
  expect(page.locator('figure')).to_have_count(72)
  page.get_by_role('checkbox',name='Прикажи водилки за порамнување').check()
  assert page.locator('svg circle').count()==144
  page.get_by_role('checkbox',name='Прикажи водилки за порамнување').uncheck()
  page.screenshot(path=str(OUT/'testing-gallery-final.png'),full_page=True)
  # Every referenced layer/mask is available; no whole catalog is used by the page.
  paths=page.locator('svg image').evaluate_all('(els)=>[...new Set(els.map(e=>e.getAttribute("href")))]')
  for path in paths:
   assert path.startswith('/characters/'),path
   response=page.request.get(URL+path);assert response.ok,path
 report['runtimeErrors']=errors;report['failedRequests']=missing
 assert not errors,errors
 assert not missing,missing
 report['independentFigures']=4;report['countRetention']='passed';report['unrelatedFrameSettings']='preserved';report['keyboard']='passed'
 (OUT/'browser-test-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(report,indent=2,ensure_ascii=False))
 browser.close()
