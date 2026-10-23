"""Exact four-figure portrait and numeric 4+ landscape team flow."""
import json,re,tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
def step(page,name):
 page.locator('.step-progress').get_by_role('button',name=re.compile(name+'$')).click()
 page.wait_for_function("()=>{const e=document.querySelector('.step-content>div');return e && +getComputedStyle(e).opacity>.999}")
def select_count(page,count):
 if count<=4:page.get_by_role('button',name=str(count)+(' фигура' if count==1 else ' фигури'),exact=True).click()
 else:
  page.get_by_role('button',name='Тимска рамка 4+',exact=True).click()
  page.get_by_label('Број на фигури во тимот',exact=True).fill(str(count))
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 page=browser.new_page(viewport={'width':1440,'height':1100},reduced_motion='reduce',accept_downloads=True);errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
 page.goto('http://localhost:3004/#configurator');page.wait_for_load_state('networkidle')
 for count in [1,2,3,4,5,8,12,24]:
  select_count(page,count);expected='15 × 20 cm' if count<=3 else '20 × 25 cm' if count==4 else 'A4'
  expect(page.locator('#configurator .hint').last).to_contain_text(expected)
  expect(page.locator('.preview-pane .frame-assembly')).to_have_attribute('data-frame-orientation','landscape' if count>4 else 'portrait')
  expect(page.locator('.preview-pane svg[data-character-id]')).to_have_count(count)
  ratio=page.locator('.preview-pane .frame-assembly').evaluate('e=>e.getBoundingClientRect().width/e.getBoundingClientRect().height')
  assert ratio>1.4 if count>4 else ratio<1,(count,ratio)
 select_count(page,12);price=page.locator('.preview-pane [data-price-total]').get_attribute('data-price-total');assert int(price)==5460
 for invalid in ['', '4','25','5.5']:
  page.get_by_label('Број на фигури во тимот',exact=True).fill(invalid);expect(page.get_by_label('Број на фигури во тимот',exact=True)).to_have_attribute('aria-invalid','true');expect(page.get_by_role('button',name='Продолжи',exact=True)).to_be_disabled();expect(page.locator('.preview-pane svg[data-character-id]')).to_have_count(12)
 page.get_by_label('Број на фигури во тимот',exact=True).fill('12');step(page,'Преглед');expect(page.locator('.summary-list')).to_contain_text('Хоризонтална');expect(page.locator('.summary-list')).to_contain_text('A4')
 for label,value in [('Име и презиме','Тест Корисник'),('Телефонски број','070123456'),('Адреса за достава','Тест адреса 12'),('Град','Скопје')]:page.get_by_label(label,exact=True).fill(value)
 page.get_by_role('button',name='Подготви барање',exact=True).click();expect(page.get_by_label('Текст на барањето',exact=True)).to_contain_text('Ориентација: Хоризонтална')
 with page.expect_download() as downloaded:page.get_by_role('button',name='Преземи податоци',exact=True).click()
 with tempfile.TemporaryDirectory() as folder:
  file=Path(folder)/'request.json';downloaded.value.save_as(file);order=json.loads(file.read_text());assert order['product']['figureCount']==12 and order['product']['orientation']=='landscape' and order['product']['frameSize']=='A4';assert len(order['characters'])==12 and order['pricing']['total']==int(price)
 step(page,'Фигури');select_count(page,4);step(page,'Преглед');expect(page.locator('.summary-list')).to_contain_text('20 × 25 cm');expect(page.locator('.summary-list')).to_contain_text('Вертикална')
 step(page,'Фигури');page.get_by_role('button',name='Почни одново',exact=True).click();expect(page.locator('.preview-pane svg[data-character-id]')).to_have_count(2)
 assert not errors,errors
 report={'fourFigures':'20 × 25 cm portrait','teamCounts':[5,8,12,24],'A4Orientation':'landscape','invalidTeamInput':'blocked','reviewAndExport':'passed','pricingAndReset':'passed','runtimeErrors':errors};(ROOT/'artifacts/authentic-content/frame-test.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True);page.close();browser.close()
