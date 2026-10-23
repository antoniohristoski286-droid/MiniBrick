"""Mobile preview stays visible while real controls remain clickable."""
import json
import re
from pathlib import Path
from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/mobile-sticky-preview'
OUT.mkdir(parents=True, exist_ok=True)

def ready(page):
    page.wait_for_function("()=>{const e=document.querySelector('.step-content>div');return e&&+getComputedStyle(e).opacity>.999}")

def choice(page, identifier):
    return page.get_by_role('button', name=re.compile('^' + identifier + ' — '))

errors = []
cases = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    page = browser.new_page(reduced_motion='reduce')
    page.set_default_timeout(8000)
    page.on('pageerror', lambda error: errors.append(str(error)))
    for width, height in [(320, 568), (360, 640), (390, 844), (430, 932), (667, 375)]:
        page.set_viewport_size({'width': width, 'height': height})
        page.goto('http://localhost:3004')
        page.wait_for_load_state('networkidle')
        page.locator('.step-progress button').nth(1).click()
        ready(page)
        compact = page.locator('[data-mobile-character-preview]')
        svg = compact.locator('svg[data-character-id]')
        for identifier, attribute in [('F13', 'data-face-id'), ('H09', 'data-head-id'), ('T02', None), ('L12', None)]:
            button = choice(page, identifier)
            button.click()
            expect(button).to_have_attribute('aria-pressed', 'true')
            if attribute:
                expect(svg).to_have_attribute(attribute, identifier)
            bounds = compact.bounding_box()
            assert abs(bounds['y']) < 1 and 139 <= bounds['height'] <= 181, bounds
            assert button.evaluate("e=>{const r=e.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return !!hit&&e.contains(hit)}"), identifier
        assert '/T02.png' in svg.locator('image[data-layer="torso"]').get_attribute('href')
        assert '/L12.png' in svg.locator('image[data-layer="legs"]').get_attribute('href')
        page.get_by_role('button', name='Срце за фигура 1', exact=True).click()
        expect(compact.locator('[data-accessory="heart"]')).to_be_visible()
        tabs = page.get_by_role('group', name='Избери фигура за уредување')
        tabs.get_by_role('button', name='Фигура 2', exact=True).click()
        expect(svg).to_have_attribute('data-character-id', 'figure-2')
        page.get_by_role('button', name='Новороденче', exact=True).click()
        choice(page, 'BC12').click()
        choice(page, 'B04').click()
        expect(svg).to_have_attribute('data-character-type', 'baby')
        expect(svg).to_have_attribute('data-face-id', 'B04')
        expect(svg.locator('image[data-layer="baby-body"]')).to_have_attribute('href', '/characters/baby-reference/BC12.png')
        tabs.get_by_role('button', name='Фигура 1', exact=True).click()
        expect(svg).to_have_attribute('data-face-id', 'F13')
        expect(svg).to_have_attribute('data-head-id', 'H09')
        choice(page, 'L12').click()
        opener = compact.get_by_role('button')
        before = page.evaluate('scrollY')
        opener.click()
        dialog = page.get_by_role('dialog', name='Зголемен преглед на фигура 1', exact=True)
        expect(dialog).to_be_visible()
        expect(dialog.get_by_role('button', name='Затвори зголемен преглед')).to_be_focused()
        expect(dialog.locator('svg[data-character-id]')).to_have_attribute('data-face-id', 'F13')
        assert dialog.locator('svg[data-character-id]').bounding_box()['height'] > svg.bounding_box()['height']
        page.keyboard.press('Tab')
        expect(dialog.get_by_role('button', name='Затвори зголемен преглед')).to_be_focused()
        page.keyboard.press('Escape')
        expect(dialog).not_to_be_visible()
        expect(opener).to_be_focused()
        page.wait_for_function("document.body.style.overflow!=='hidden'")
        assert abs(page.evaluate('scrollY') - before) < 3
        opener.click()
        dialog.get_by_role('button', name='Затвори зголемен преглед').click()
        expect(opener).to_be_focused()
        assert compact.locator('.preview-disclaimer,.preview-gallery-link').count() == 0
        assert page.locator('.character-preview-pane').evaluate('e=>getComputedStyle(e).position') == 'static'
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        choice(page, 'T02').click()
        page.screenshot(path=str(OUT / f'editing-{width}.png'))
        cases.append({'width': width, 'height': height, 'stickyHeight': compact.bounding_box()['height'], 'controls': 'clicked normally', 'independentFigures': 'preserved', 'dialog': 'Escape, close, focus and scroll restoration passed'})
        page.evaluate('window.scrollTo(0,document.body.scrollHeight)')
        assert compact.bounding_box()['y'] + compact.bounding_box()['height'] < 0
        choice(page, 'L12').click()
        opener.click()
        page.set_viewport_size({'width': 1440, 'height': 1000})
        expect(dialog).not_to_be_visible()
        page.wait_for_function("document.body.style.overflow!=='hidden'")
        expect(compact).not_to_be_visible()
        expect(page.locator('.character-preview-pane svg[data-character-id]')).to_be_visible()
        page.locator('.step-progress button').nth(2).click()
        ready(page)
        expect(compact).to_have_count(0)
    assert not errors, errors
    report = {'cases': cases, 'desktopPreview': 'preserved', 'otherSteps': 'compact preview removed', 'stickyEndsAtEditor': True, 'runtimeErrors': errors}
    (OUT / 'report.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report), flush=True)
    browser.close()
