"""Verify the production build, its live character controls, and shipped PNG assets."""
from pathlib import Path
import json, os
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1];URL=os.environ.get('CHARACTER_TEST_URL','http://localhost:3004');OUT=ROOT/'artifacts/characters'
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 page=browser.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce');errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
 response=page.goto(URL);assert response.status==200;page.wait_for_load_state('networkidle')
 page.get_by_role('button',name='02 Стил',exact=True).click();page.get_by_role('heading',name='Дајте им свој карактер.').wait_for()
 page.get_by_role('button',name='H04 — Долга црна',exact=True).click();page.get_by_role('button',name='F08 — Тиркизни очи',exact=True).click();page.get_by_role('button',name='T11 — Црвена',exact=True).click()
 preview=page.locator('.character-preview-pane .minibrick-character');expect(preview).to_have_attribute('data-head-id','H04');expect(preview).to_have_attribute('data-face-id','F08')
 page.get_by_role('button',name='Фигура 2',exact=True).click();expect(preview).to_have_attribute('data-head-id','H07');page.get_by_role('button',name='Фигура 1',exact=True).click();expect(preview).to_have_attribute('data-head-id','H04')
 page.wait_for_function("()=>Number(getComputedStyle(document.querySelector('.step-content>div')).opacity)>.999")
 page.locator('.config-shell').evaluate('(e)=>e.scrollIntoView({block:"start",behavior:"instant"})');page.screenshot(path=str(OUT/'builder-production-desktop.png'))
 for width in [390,320]:
  page.set_viewport_size({'width':width,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.get_by_role('button',name='Новороденче',exact=True).click();expect(page.get_by_role('group',name='Избери фризура 9 варијанти')).to_have_count(0)
  page.get_by_role('button',name='Женски',exact=True).click();expect(preview).to_have_attribute('data-head-id','H04')
 files=list((ROOT/'public/characters').rglob('*.png'))
 for path in files:
  response=page.request.get(URL+'/'+path.relative_to(ROOT/'public').as_posix());assert response.ok,path
 response=page.goto(URL+'/dev/characters');assert response.status==404,'Development gallery leaked into production'
 expect(page.get_by_role('heading',name='Страницата не е пронајдена.',exact=True)).to_be_visible();assert not errors,errors
 report={'homepage':200,'productionCharacterControls':'passed','independentFigures':'passed','responsiveWidths':[390,320],'assetFilesServed':len(files),'developmentGalleryStatus':404,'runtimeErrors':errors}
 (OUT/'production-test-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));browser.close()
