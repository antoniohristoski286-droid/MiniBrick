"""Frontend readiness checks; backend submission is explicitly out of scope."""
import io, json, re, tempfile
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/frontend-readiness';URL='http://localhost:3004'
def step(page,name):
 page.locator('.step-progress').get_by_role('button',name=re.compile(name+'$')).click()
 headings={'Фигури':'Колку фигури сакате?','Стил':'Дајте им свој карактер.','Позадина':'Поставете ја сцената.','Текст':'Деталите се сè.','Преглед':'Вашата MiniBrick рамка.'}
 page.get_by_role('heading',name=headings[name],exact=True).wait_for()
 page.wait_for_function("()=>{const e=document.querySelector('.step-content>div');return e && +getComputedStyle(e).opacity>.999}")
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 context=browser.new_context(viewport={'width':1440,'height':1100},reduced_motion='reduce',permissions=['clipboard-read','clipboard-write'],accept_downloads=True)
 page=context.new_page();errors=[];failures=[];writes=[]
 page.on('pageerror',lambda err:errors.append(str(err)))
 page.on('response',lambda response:failures.append({'status':response.status,'path':response.url.split('?')[0]}) if response.status>=400 and not response.url.endswith('/does-not-exist') else None)
 page.on('request',lambda request:writes.append(request.method) if request.method not in ['GET','HEAD'] else None)
 response=page.goto(URL);page.wait_for_load_state('networkidle');headers=response.headers
 assert headers['x-content-type-options']=='nosniff' and headers['x-frame-options']=='DENY';assert "frame-ancestors 'none'" in headers['content-security-policy']
 expect(page.locator('html')).to_have_attribute('lang','mk');expect(page.locator('meta[name="robots"]')).to_have_attribute('content',re.compile('noindex'))
 assert page.locator('.testimonials blockquote').count()==0;assert page.locator('a[href="https://www.instagram.com/"]').count()==0
 assert 'Без обработка на лични податоци' not in page.locator('footer').inner_text()
 links=page.locator('a[href^="#"]').evaluate_all('(els)=>els.map(e=>e.getAttribute("href").slice(1)).filter(Boolean)');assert all(page.locator('[id="'+id+'"]').count() for id in links),links
 page.keyboard.press('Tab');expect(page.get_by_role('link',name='Прескокни до содржината',exact=True)).to_be_focused();page.keyboard.press('Enter');expect(page.locator('#main-content')).to_be_focused()
 faq=page.locator('#faq details').first;faq.locator('summary').focus();page.keyboard.press('Enter');expect(faq).to_have_attribute('open','');page.keyboard.press('Enter');assert faq.get_attribute('open') is None
 photo=page.locator('.showcase-photo img');photo.scroll_into_view_if_needed();photo.evaluate('e=>e.decode()');assert '/_next/image?' in photo.get_attribute('src')
 for width in [1440,1024,768,390,320]:
  page.set_viewport_size({'width':width,'height':1000});page.wait_for_timeout(300)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),('page overflow',width)
  if width<=1000:
   page.locator('.menu-toggle').click();expect(page.locator('#mobile-navigation')).to_be_visible();page.keyboard.press('Escape');expect(page.locator('#mobile-navigation')).to_have_count(0);expect(page.locator('.menu-toggle')).to_be_focused()
  if width in [1440,390]:
   page.screenshot(path=str(OUT/f'after-{width}.png'),full_page=True);page.locator('#faq').screenshot(path=str(OUT/f'faq-{width}.png'));page.locator('footer').screenshot(path=str(OUT/f'footer-{width}.png'))
   assert 'јасоздадете' not in page.locator('#faq h2').inner_text()
 page.set_viewport_size({'width':1440,'height':1100});step(page,'Стил')
 page.wait_for_function("()=>document.activeElement?.getAttribute('aria-label')==='Чекор 2: Стил'")
 page.get_by_role('button',name='Срце за фигура 1',exact=True).click();page.get_by_role('button',name='Милениче за фигура 1',exact=True).click();page.get_by_role('button',name='Мачка',exact=True).click()
 for img in page.get_by_role('group',name='Милениче за фигура 1',exact=True).locator('img').all():img.evaluate('e=>e.decode()');assert '/_next/image?' in img.get_attribute('src')
 step(page,'Позадина');page.get_by_role('button',name='Своја фотографија',exact=True).click();buf=io.BytesIO();Image.new('RGB',(600,400),'#839ba5').save(buf,format='PNG');page.get_by_label('Прикачи своја фотографија',exact=True).set_input_files({'name':'test-local.png','mimeType':'image/png','buffer':buf.getvalue()})
 expect(page.locator('.preview-pane [data-background-id="custom"]')).to_have_attribute('aria-busy','false');step(page,'Преглед')
 page.get_by_role('button',name='Подготви барање',exact=True).click();expect(page.get_by_label('Име и презиме',exact=True)).to_be_focused();expect(page.locator('#configurator').get_by_role('alert')).to_have_count(4)
 for label,value in [('Име и презиме','Тест Корисник'),('Телефонски број','070/123-456'),('Адреса за достава','Тест адреса 12'),('Град','Скопје')]:page.get_by_label(label,exact=True).fill(value)
 page.get_by_label('Дополнителна забелешка (по избор)',exact=True).fill('<img src=x onerror="window.__mbXss=true">')
 page.get_by_role('button',name='Подготви барање',exact=True).click();assert page.evaluate('window.__mbXss') is None;heading=page.get_by_role('heading',name='Барањето е подготвено за копирање',exact=True);expect(heading).to_be_focused()
 # Force clipboard denial: a real error path must preserve the request and select its text.
 page.evaluate("Object.defineProperty(navigator.clipboard,'writeText',{value:async()=>{throw new Error('denied')}})")
 page.get_by_role('button',name='Копирај барање',exact=True).click();expect(page.get_by_role('status').filter(has_text='Автоматското копирање')).to_be_visible();output=page.get_by_label('Текст на барањето',exact=True);expect(output).to_be_focused();assert output.evaluate('e=>e.selectionEnd-e.selectionStart')==len(output.input_value())
 with page.expect_download() as download:page.get_by_role('button',name='Преземи податоци',exact=True).click()
 with tempfile.TemporaryDirectory() as folder:
  target=Path(folder)/'request.json';download.value.save_as(target);order=json.loads(target.read_text());assert order['pricing']['total']==2080 and order['status']=='prepared-not-submitted';assert 'blob:' not in json.dumps(order);assert order['background']['photo']['attached'] is False
 # New tab privacy navigation leaves the current personalized configuration in place.
 with context.expect_page() as opened:page.get_by_role('link',name='Вашите податоци (се отвора во нов таб)',exact=True).click()
 privacy=opened.value;privacy.wait_for_load_state('networkidle');assert privacy.url.endswith('/privacy');expect(privacy.get_by_role('heading',level=1)).to_contain_text('Вашите податоци');assert 'не претставува целосна политика' in privacy.locator('main').inner_text();privacy.screenshot(path=str(OUT/'privacy-desktop.png'));privacy.set_viewport_size({'width':320,'height':900});assert privacy.evaluate('document.documentElement.scrollWidth<=innerWidth');privacy.screenshot(path=str(OUT/'privacy-mobile.png'),full_page=True);privacy.close()
 expect(page.locator('.preview-pane [data-background-id="custom"]')).to_be_visible();expect(page.get_by_label('Име и презиме',exact=True)).to_have_value('Тест Корисник')
 page.set_viewport_size({'width':320,'height':900});page.wait_for_timeout(300);assert page.get_by_label('Име и презиме',exact=True).evaluate('e=>getComputedStyle(e).fontSize')=='16px'
 assert not writes, writes;assert not errors,errors;assert not failures,failures
 not_found=context.new_page();res=not_found.goto(URL+'/does-not-exist');assert res.status==404;expect(not_found.get_by_role('heading',level=1)).to_contain_text('Страницата не е');not_found.close()
 report={'viewports':[1440,1024,768,390,320],'navigationAnchors':len(links),'skipLink':'passed','stepFocus':'passed','mobileEscapeFocus':'passed','faqKeyboard':'passed','optimizedImages':'passed','privacyPage':'passed','noFalseTestimonialsOrContactLink':'passed','contactValidation':'passed','preparedRequestFocus':'passed','clipboardFailureRecovery':'passed','download':'passed','photoNotTransmitted':'passed','personalDataNotPosted':not writes,'htmlInputRenderedAsText':'passed','runtimeErrors':errors,'failedRequests':failures,'securityHeaders':'passed','prelaunchNoindex':'passed','localized404':'passed'}
 (OUT/'browser-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));browser.close();print(json.dumps(report,ensure_ascii=False))
