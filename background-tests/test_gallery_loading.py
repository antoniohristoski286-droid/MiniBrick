import json,re
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');page=b.new_page(viewport={'width':1440,'height':1100});requests=[];page.on('request',lambda request:requests.append(request.url));page.goto('http://localhost:3004/#configurator');page.wait_for_load_state('networkidle');page.locator('.step-progress button').nth(2).click();expect(page.get_by_role('group',name='Колекција на позадини',exact=True).get_by_role('button')).to_have_count(110);page.wait_for_load_state('networkidle')
 full=[u for u in requests if re.search(r'/backgrounds/BG\d+\.jpg$',u)];thumb=[u for u in requests if '/backgrounds/thumbnails/' in u]
 assert len(set(full))==1,(full,thumb)
 assert len(set(thumb))<110,len(thumb)
 report={'firstGalleryFullResolutionImagesRequested':len(set(full)),'firstGalleryThumbnailsRequested':len(set(thumb)),'totalCatalogOptions':110,'lazyLoading':'passed'};Path('artifacts/backgrounds/audit/loading-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));b.close()
