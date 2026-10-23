"""Authentic story/photos/hero, landscape teams, responsive coverage and lightbox."""
import json,re
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/authentic-content'
def step(page,name):
 page.locator('.step-progress').get_by_role('button',name=re.compile(name+'$')).click()
 page.wait_for_function("()=>{const e=document.querySelector('.step-content>div');return e && +getComputedStyle(e).opacity>.999}")
def count(page,n):
 step(page,'Фигури')
 if n<=4:page.get_by_role('button',name=str(n)+(' фигура' if n==1 else ' фигури'),exact=True).click()
 else:
  page.get_by_role('button',name='Тимска рамка 4+',exact=True).click();page.get_by_label('Број на фигури во тимот',exact=True).fill(str(n))
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');context=b.new_context(viewport={'width':1440,'height':1100},reduced_motion='reduce');page=context.new_page();errors=[];failed=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:failed.append(r.url) if r.status>=400 else None)
 page.goto('http://localhost:3004');page.wait_for_load_state('networkidle');hero=page.locator('.hero-real-project img');hero.evaluate('e=>e.decode()');assert '%2Fprojects%2Fbirthday-frame-hq.jpg' in hero.get_attribute('src');assert hero.evaluate("e=>getComputedStyle(e).clipPath.startsWith('polygon(')");expect(page.locator('.hero .frame-assembly')).to_have_count(0)
 story=page.locator('#about');expect(story).to_contain_text('Во големиот избор на подароци');expect(story).to_contain_text('Така се роди идејата');expect(story).to_contain_text('Не веруваме во подароци');expect(story).to_contain_text('Без разлика дали станува збор');assert 'Наскоро' not in story.inner_text()
 cases=0
 for width in [1440,768,390,320]:
  page.set_viewport_size({'width':width,'height':1100 if width>760 else 900});page.wait_for_timeout(300)
  for n in [4,5,8,12,24]:
   count(page,n);step(page,'Позадина');base=None
   for mode in ['Од колекцијата','Календар']:
    page.get_by_role('button',name=mode,exact=True).click();page.wait_for_timeout(200)
    geometry=page.locator('.preview-pane').evaluate('''e=>{const a=e.querySelector('.frame-art').getBoundingClientRect();return {ratio:e.querySelector('.frame-assembly').getBoundingClientRect().width/e.querySelector('.frame-assembly').getBoundingClientRect().height,figures:[...e.querySelectorAll('svg[data-character-id]')].map(s=>{const m=s.getScreenCTM(),v=s.viewBox.baseVal;return {x:(m.e-a.x)/a.width,y:(m.f-a.y)/a.height,w:v.width*m.a/a.width,h:v.height*m.d/a.height,inside:m.e>=a.x-1&&m.f>=a.y-1&&m.e+v.width*m.a<=a.right+1&&m.f+v.height*m.d<=a.bottom+1}})}}''')
    assert all(s['inside'] for s in geometry['figures']),(width,n,mode,geometry)
    if base:
     assert abs(geometry['ratio']-base['ratio'])<.001,(width,n,mode)
     assert all(abs(a[k]-z[k])<.002 for a,z in zip(geometry['figures'],base['figures']) for k in ['x','y','w','h']),(width,n,mode)
    base=geometry;assert geometry['ratio']>1.4 if n>4 else geometry['ratio']<1
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,n,mode)
    cases+=1
   if n==12:page.locator('.preview-pane').screenshot(path=str(OUT/f'team-calendar-{width}.png'))
  count(page,12);step(page,'Стил');expect(page.get_by_role('group',name='Избери фигура за уредување',exact=True).get_by_role('button')).to_have_count(12)
  page.get_by_role('button',name='Фигура 12',exact=True).click();page.get_by_role('button',name='Срце за фигура 12',exact=True).click();page.get_by_role('button',name='Срце за фигура 12',exact=True).click()
  page.locator('.hero').scroll_into_view_if_needed();page.locator('.hero').screenshot(path=str(OUT/f'hero-{width}.png'));story.scroll_into_view_if_needed();story.screenshot(path=str(OUT/f'story-{width}.png'))
 gallery=context.new_page();gallery.on('pageerror',lambda e:errors.append(str(e)));gallery.goto('http://localhost:3004/gallery');gallery.wait_for_load_state('networkidle');expect(gallery.locator('.project-gallery figure')).to_have_count(50);expect(gallery.locator('.project-gallery figcaption a')).to_have_count(0)
 for item in gallery.locator('.gallery-image-button').all():
  item.scroll_into_view_if_needed();item.locator('img').evaluate('e=>e.decode()');source=item.locator('img').get_attribute('src');item.click();dialog=gallery.get_by_role('dialog');expect(dialog).to_be_visible();expect(dialog.locator('img')).to_have_attribute('src',re.compile('projects|minibrick-products'));gallery.keyboard.press('Escape');expect(dialog).not_to_be_visible();expect(item).to_be_focused()
 for width in [1440,768,390,320]:
  gallery.set_viewport_size({'width':width,'height':900});gallery.evaluate('document.activeElement.blur();window.scrollTo(0,0)');gallery.wait_for_timeout(200);assert gallery.evaluate('document.documentElement.scrollWidth<=innerWidth');gallery.screenshot(path=str(OUT/f'gallery-{width}.png'),full_page=True)
 assert not errors,errors;assert not failed,failed
 report={'story':'four supplied paragraphs','hero':'original photo with exterior-only CSS mask','galleryPhotos':50,'instagramPhotos':0,'lightboxEachPhoto':'passed','responsiveCases':cases,'teamCounts':[5,8,12,24],'widths':[1440,768,390,320],'scaleAcrossCatalogAndCalendar':'identical','figureBounds':'passed','builderFigure12':'passed','runtimeErrors':errors,'failedRequests':failed};(OUT/'browser-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True);page.close();gallery.close();context.close();b.close()
