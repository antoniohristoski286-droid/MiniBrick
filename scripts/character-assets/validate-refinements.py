"""Assert the targeted hand/style correction preserves geometry and working UI/state."""
from pathlib import Path
from PIL import Image,ImageChops
import hashlib,json
ROOT=Path(__file__).resolve().parents[2];ASSETS=ROOT/'public/characters';BEFORE=ROOT/'artifacts/characters/refinement-before'
skin=(255,199,142)
for i in range(1,13):
 id=f'T{i:02}';after=Image.open(ASSETS/f'torsos/{id}.png');before=Image.open(BEFORE/f'torsos/{id}.png')
 assert ImageChops.difference(after.getchannel('A'),before.getchannel('A')).getbbox() is None,f'{id}: silhouette changed'
 for point in [(101,482),(411,482)]:assert after.getpixel(point)==(*skin,255),(id,point,after.getpixel(point))
 for point in [(256,350),(137,380),(375,380)]:assert after.getpixel(point)==before.getpixel(point),(id,'shirt/arm color changed')
 # All altered pixels are confined to the existing hands; sleeve cuffs stay colored.
 difference=ImageChops.difference(after,before).convert('RGB').getbbox()
 assert difference and difference[1]>=448 and difference[3]<=508,(id,'unexpected torso edit',difference)
for i in range(1,10):
 id=f'H{i:02}';after=Image.open(ASSETS/f'hair-heads/{id}.png');before=Image.open(BEFORE/f'hair-heads/{id}.png')
 assert ImageChops.difference(after.getchannel('A'),before.getchannel('A')).getbbox() is None,f'{id}: hair silhouette moved'
 assert after.getpixel((256,250))[:3]==skin,(id,'inconsistent skin')
 assert len(after.getcolors(512*768))<1000,(id,'continuous shading remains')
# The size correction intentionally changes only renderer display metadata and its head group.
size_correction_files={'components/characters/catalog.ts','components/characters/MiniBrickCharacter.tsx'}
for filename,expected in json.loads((BEFORE/'unchanged-files.json').read_text()).items():
 if filename in size_correction_files:continue
 assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==expected,filename+' unexpectedly modified'
print('PASS: 12 peach hand pairs; unchanged C-shaped hand silhouettes, shirt/arm colors, leg assets, 9 hair silhouettes, source face anchors, UI, state and newborn behavior.')
# Validate every head at the same head/body and waist seam with all 12 mixed colors.
for h in range(1,10):
 head=Image.open(ASSETS/f'hair-heads/H{h:02}.png').getchannel('A')
 for color in range(1,13):
  upper=Image.open(ASSETS/f'torsos/T{color:02}.png').getchannel('A')
  lower=Image.open(ASSETS/f'legs/L{13-color:02}.png').getchannel('A')
  assembled=ImageChops.lighter(ImageChops.lighter(head,upper),lower)
  assert all(assembled.getpixel((256,y))>128 for y in range(260,580)),f'H{h:02}/T{color:02}: body connection gap'
  assert all(assembled.getpixel((x,466))>128 for x in range(180,333)),f'T{color:02}: waist connection gap'
print('PASS: gapless head/torso/waist connections for all 108 head-and-body combinations.')
