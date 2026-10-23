"""Check owner-requested New Year labels, reference baby, child size and notices."""
import json
import re
from pathlib import Path

from PIL import Image, ImageChops
from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/new-year-models'
OUT.mkdir(parents=True, exist_ok=True)
manifest = json.loads((ROOT / 'data/backgrounds.json').read_text())
seasonal = [item for item in manifest['backgrounds'] if item['category'] == 'Новогодишни']
assert len(seasonal) == 12
assert not any('Божиќ' in item['name'] or 'зима' in item['name'] for item in manifest['categories'])
silhouette = None
for number in range(1, 13):
    image = Image.open(ROOT / f'public/characters/baby-reference/BC{number:02}.png')
    assert image.mode == 'RGBA' and image.size == (512, 768)
    alpha = image.getchannel('A')
    assert alpha.getpixel((0, 0)) == 0 and alpha.getbbox()
    if silhouette is not None:
        assert ImageChops.difference(silhouette, alpha).getbbox() is None
    silhouette = alpha

def step(page, label):
    page.locator('.step-progress').get_by_role('button', name=re.compile(label + '$')).click()
    page.wait_for_function("()=>{const e=document.querySelector('.step-content>div');return e&&+getComputedStyle(e).opacity>.999}")

def choice(page, prefix):
    return page.get_by_role('button', name=re.compile('^' + prefix + ' — '))

errors = []
failed = []
cases = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    page = browser.new_page(viewport={'width': 1440, 'height': 1100}, reduced_motion='reduce')
    page.set_default_timeout(10000)
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('response', lambda response: failed.append(response.url) if response.status >= 400 else None)
    page.goto('http://localhost:3004')
    page.wait_for_load_state('networkidle')
    preview = page.locator('#configurator [data-background-id]')
    expect(preview).to_have_attribute('data-background-id', 'BG018')
    occasion = page.locator('#ideas').get_by_role('button', name=re.compile('Нова година'))
    expect(occasion).to_have_count(1)
    occasion.click()
    expect(preview).to_have_attribute('data-background-id', seasonal[0]['id'])
    step(page, 'Позадина')
    expect(page.get_by_role('button', name='Божиќ и зима', exact=True)).to_have_count(0)
    page.get_by_role('button', name='Новогодишни', exact=True).click()
    cards = page.get_by_role('group', name='Колекција на позадини').get_by_role('button')
    expect(cards).to_have_count(12)
    for item in seasonal:
        page.get_by_role('button', name=re.compile('^Позадина ' + item['id'] + ' — ')).click()
        expect(preview).to_have_attribute('data-background-id', item['id'])
        preview.locator('img').evaluate('e=>e.decode()')
    step(page, 'Стил')
    expect(page.locator('.model-availability-note')).to_contain_text('ќе се одбере модел што е најблизок')
    page.get_by_role('button', name='Дете', exact=True).click()
    assembly = page.locator('.character-preview-pane [data-character-assembly]')
    expect(assembly).to_have_attribute('transform', 'translate(256 714) scale(0.88) translate(-256 -714)')
    anchor = assembly.evaluate('e=>{const p=new DOMPoint(256,714).matrixTransform(e.transform.baseVal.consolidate().matrix);return {x:p.x,y:p.y}}')
    assert abs(anchor['x'] - 256) < .001 and abs(anchor['y'] - 714) < .001
    page.get_by_role('button', name='Срце за фигура 1', exact=True).click()
    page.wait_for_function("""()=>{
      const e=document.querySelector('.accessorized-live-preview');
      const svg=e.querySelector('svg[data-character-id]'), overlay=e.querySelector('.figure-accessories');
      return Math.abs(512*svg.getScreenCTM().a*.88-overlay.getBoundingClientRect().width)<1;
    }""")
    geometry = page.locator('.accessorized-live-preview').evaluate("""e=>{
      const svg=e.querySelector('svg[data-character-id]'), overlay=e.querySelector('.figure-accessories');
      return {expected:512*svg.getScreenCTM().a*.88, actual:overlay.getBoundingClientRect().width};
    }""")
    assert abs(geometry['expected'] - geometry['actual']) < 1, geometry
    for width in [1440, 768, 390, 320]:
        page.set_viewport_size({'width': width, 'height': 1100})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        page.locator('.preview-pane').screenshot(path=str(OUT / f'child-{width}.png'))
        cases.append({'width': width, 'type': 'child'})
    step(page, 'Преглед')
    expect(page.locator('.preview-stage [data-character-assembly]').first).to_have_attribute('transform', 'translate(256 714) scale(0.88) translate(-256 -714)')
    expect(page.locator('.step-content')).to_contain_text('Напомена:')
    expect(page.locator('.step-content')).to_contain_text('ќе се одбере модел што е најблизок')
    step(page, 'Стил')
    page.get_by_role('button', name='Новороденче', exact=True).click()
    for number in range(1, 13):
        choice(page, f'BC{number:02}').click()
        image = page.locator('.character-preview-pane image[data-layer="baby-body"]')
        expect(image).to_have_attribute('href', f'/characters/baby-reference/BC{number:02}.png')
    for number in range(1, 5):
        choice(page, f'B{number:02}').click()
        expect(page.locator('.character-preview-pane svg[data-character-id]')).to_have_attribute('data-face-id', f'B{number:02}')
    choice(page, 'BC10').click()
    choice(page, 'B03').click()
    expect(page.get_by_role('group', name=re.compile('^Избери фризура'))).to_have_count(0)
    for width in [1440, 768, 390, 320]:
        page.set_viewport_size({'width': width, 'height': 1100})
        page.wait_for_load_state('networkidle')
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        page.locator('.preview-pane').screenshot(path=str(OUT / f'baby-{width}.png'))
        cases.append({'width': width, 'type': 'baby'})
    expect(page.locator('.footer-product-notice strong')).to_have_text('Напомена:')
    assert not errors and not failed, {'runtimeErrors': errors, 'httpErrors': failed}
    report = {'newYearCategory': 12, 'newYearOccasion': 'selects first New Year background', 'allSeasonalOriginalsDecode': True, 'referenceBabyColors': 12, 'babyFaces': 4, 'childScale': .88, 'childFeetAnchor': anchor, 'childAccessoryAlignment': geometry, 'availabilityAndDisclaimer': 'passed', 'responsiveCases': cases, 'runtimeErrors': errors, 'httpErrors': failed}
    (OUT / 'report.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report), flush=True)
    browser.close()

