"""Validate prepared sprites and render a deterministic alignment contact sheet."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import json
ROOT=Path(__file__).resolve().parents[2];ASSETS=ROOT/'public/characters';ART=ROOT/'artifacts/characters'
metadata=json.loads((ASSETS/'head-alignment.json').read_text())
display_scales=json.loads((ASSETS/'head-display.json').read_text())
faces=list((ASSETS/'faces').glob('*/*.png'))
assert len(faces)==27
assert len(list((ASSETS/'hair-heads').glob('H??.png')))==9
assert len(list((ASSETS/'torsos').glob('T??.png')))==12
assert len(list((ASSETS/'legs').glob('L??.png')))==12
assert len(list((ASSETS/'baby').glob('BC??.png')))==12
for path in ASSETS.rglob('*.png'):
 im=Image.open(path)
 assert im.mode=='RGBA',(path,'missing RGBA')
 alpha=im.getchannel('A');assert alpha.getextrema()[0]==0,(path,'no transparency')
 assert alpha.getbbox() is not None,(path,'empty asset')
 assert all(alpha.getpixel(xy)==0 for xy in [(0,0),(im.width-1,0),(0,im.height-1),(im.width-1,im.height-1)]),(path,'opaque corner')
 assert im.size==((240,180) if path in faces else (512,768)),(path,'incorrect coordinate space')
for folder,prefix,top in [('torsos','T',276),('legs','L',462)]:
 base=None
 for index in range(1,13):
  alpha=Image.open(ASSETS/f'{folder}/{prefix}{index:02}.png').getchannel('A')
  assert alpha.crop((0,0,512,top)).getbbox() is None, 'Unexpected connector/stud'
  if base is None:base=alpha
  else:assert ImageChops.difference(base,alpha).getbbox() is None,'Color changed silhouette'
# White body regions must remain opaque, not color keyed away.
assert Image.open(ASSETS/'torsos/T12.png').getpixel((256,350))[3]==255
assert Image.open(ASSETS/'legs/L12.png').getpixel((200,620))[3]==255

def compose(head='H03',face='F02',torso='T12',legs='L02',baby=False,color='BC10'):
 canvas=Image.new('RGBA',(512,768))
 category={'F':'female','M':'male','C':'child','B':'baby'}[face[0]]
 if baby:
  canvas.alpha_composite(Image.open(ASSETS/f'baby/{color}.png'));place={'x':190,'y':231,'width':132,'height':99}
  mask=Image.new('L',(512,768));ImageDraw.Draw(mask).rounded_rectangle((193,202,319,338),radius=45,fill=255)
 else:
  for path in [f'legs/{legs}.png',f'torsos/{torso}.png']:canvas.alpha_composite(Image.open(ASSETS/path))
  place=metadata[head]['face'];mask=Image.open(ASSETS/f'hair-heads/{head}-face-mask.png').getchannel('A')
 decal=Image.open(ASSETS/f'faces/{category}/{face}.png').resize((place['width'],place['height']),Image.Resampling.LANCZOS)
 layer=Image.new('RGBA',(512,768));layer.alpha_composite(decal,(place['x'],place['y']));layer.putalpha(ImageChops.multiply(layer.getchannel('A'),mask))
 if not baby:
  head_layer=Image.open(ASSETS/f'hair-heads/{head}.png').copy();head_layer.alpha_composite(layer)
  scale=display_scales[head]
  layer=head_layer.transform((512,768),Image.Transform.AFFINE,(1/scale,0,256-256/scale,0,1/scale,280-280/scale),Image.Resampling.BICUBIC)
 canvas.alpha_composite(layer)
 return canvas
sheet=Image.new('RGB',(1620,810),'#f5efe7');d=ImageDraw.Draw(sheet)
for i in range(9):
 h=f'H{i+1:02}';im=compose(head=h,face='F02' if i<5 else 'M04',torso='T12',legs='L02');im.thumbnail((175,265));x=i*180+3;sheet.paste(im,(x,30),im);d.text((x+65,300),h,fill='#272322')
for i,path in enumerate(faces):
 im=compose(head='H03' if path.stem[0]=='F' else 'H07',face=path.stem,baby=path.stem[0]=='B');im.thumbnail((112,169));x=(i%14)*115+3;y=340+(i//14)*226;sheet.paste(im,(x,y),im);d.text((x+40,y+176),path.stem,fill='#272322')
sheet.save(ART/'assembled-contact-sheet.png')
# Color consistency and full body connections at the common centerline.
for i in range(12):
 im=compose(torso=f'T{i+1:02}',legs=f'L{12-i:02}')
 alpha=im.getchannel('A')
 assert all(alpha.getpixel((256,y))>0 for y in range(275,580)),f'Body connection gap {i}'
print('PASS: 81 RGBA PNG layers/masks; all 27 faces, 9 heads, 12 torsos, 12 legs, 12 provisional newborn bodies.')
print('PASS: uniform canvas, genuine transparent exteriors, identical body silhouettes, white interiors preserved, no top studs, continuous body connections.')
