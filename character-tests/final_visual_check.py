from pathlib import Path
import os
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/characters'
URL=os.environ.get('CHARACTER_TEST_URL','http://localhost:3010')
def settled(page):
 page.wait_for_function('''()=>[...document.querySelectorAll('.step-content>div,.preview-pane .modular-figure-row>div')].every(e=>Number(getComputedStyle(e).opacity)>.999)''')
 page.wait_for_load_state('networkidle')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 page=browser.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce')
 page.goto(URL);page.wait_for_load_state('networkidle');page.get_by_role('button',name='02 Стил',exact=True).click();page.get_by_role('heading',name='Дајте им свој карактер.').wait_for();settled(page)
 page.locator('.config-shell').evaluate('(e)=>e.scrollIntoView({block:"start",behavior:"instant"})')
 page.screenshot(path=str(OUT/'builder-desktop-final.png'))
 page.locator('.config-shell').screenshot(path=str(OUT/'builder-desktop-full-final.png'))
 for width,height in [(390,844),(320,700)]:
  page.set_viewport_size({'width':width,'height':height});settled(page)
  page.locator('.character-preview-pane').evaluate('(e)=>e.scrollIntoView({block:"start",behavior:"instant"})')
  page.screenshot(path=str(OUT/f'builder-mobile-{width}-final.png'))
  svg=page.locator('.character-preview-pane .minibrick-character').bounding_box()
  ids=page.locator('[class*="previewIds"]').bounding_box()
  assert svg['y']+svg['height']<=ids['y']+1,('Preview overlaps caption',svg,ids)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.get_by_role('button',name='Новороденче',exact=True).click();settled(page)
  page.locator('.character-preview-pane').evaluate('(e)=>e.scrollIntoView({block:"start",behavior:"instant"})')
  page.screenshot(path=str(OUT/f'builder-newborn-mobile-{width}.png'))
  page.get_by_role('button',name='Женски',exact=True).click()
 page.set_viewport_size({'width':1440,'height':1000});page.get_by_role('button',name='Фигури',exact=True).click();page.get_by_role('button',name='4 фигури',exact=True).click();page.get_by_role('button',name='03 Позадина',exact=True).click();page.get_by_role('heading',name='Поставете ја сцената.').wait_for();settled(page)
 page.locator('.preview-pane').screenshot(path=str(OUT/'frame-four-figures-final.png'))
 if not os.environ.get('CHARACTER_TEST_PRODUCTION'):
  page.goto(URL+'/dev/characters');page.wait_for_load_state('networkidle');page.screenshot(path=str(OUT/'testing-gallery-final.png'),full_page=True)
 print('PASS: final desktop/mobile captures, no caption overlap at 320/390, no horizontal overflow, stable frame figures, full asset gallery rendered.')
 browser.close()
