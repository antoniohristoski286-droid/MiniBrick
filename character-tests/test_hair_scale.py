"""Targeted regression for fuller hairstyle display sizes and neck registration."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];scales=json.loads((ROOT/'public/characters/head-display.json').read_text())
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');page=browser.new_page(viewport={'width':1440,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://localhost:3004');page.wait_for_load_state('networkidle');page.get_by_role('button',name='02 Стил',exact=True).click();page.get_by_role('heading',name='Дајте им свој карактер.').wait_for()
 for id,scale in scales.items():
  page.locator(f'button[aria-label^="{id} — "]').click()
  actual=page.locator('.character-preview-pane svg[data-character-id]').evaluate('''e=>{let h=e.querySelector('[data-layer="head"]').getScreenCTM(),f=e.querySelector('[data-layer="face"]').getScreenCTM(),b=e.querySelector('[data-layer="torso"]').getScreenCTM();let hp=new DOMPoint(256,280).matrixTransform(h),bp=new DOMPoint(256,280).matrixTransform(b);return {scale:h.a/b.a,faceScale:f.a/b.a,neckError:Math.hypot(hp.x-bp.x,hp.y-bp.y)}}''')
  assert abs(actual['scale']-scale)<.0001 and abs(actual['faceScale']-scale)<.0001 and actual['neckError']<.001,(id,actual)
 page.locator('button[aria-label^="H03 — "]').click();page.get_by_role('button',name='03 Позадина',exact=True).click();page.get_by_role('heading',name='Поставете ја сцената.').wait_for();page.wait_for_function('''()=>[...document.querySelectorAll('.preview-pane .modular-figure-row>div')].every(e=>Number(getComputedStyle(e).opacity)>.999)''');page.wait_for_load_state('networkidle')
 page.locator('.preview-pane').screenshot(path=str(ROOT/'artifacts/characters/hair-size-frame-comparison.png'))
 for width in [390,320]:
  page.set_viewport_size({'width':width,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 assert not errors,errors;browser.close();print('PASS: all nine head/face scales, fixed neck anchors, frame preview, and 320/390px overflow checks.')
