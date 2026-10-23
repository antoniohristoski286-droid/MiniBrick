"""Prepare supplied MiniBrick catalogs. No RGB color key is used.
Heads use an exterior-connected background mask; faces retain their actual source alpha.
Bodies are controlled flat vector tracings, rasterized by render-vectors.mjs.
"""
from pathlib import Path
from PIL import Image, ImageDraw
from collections import deque
import numpy as np
import json
from head_style import flatten_head

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).parent / 'references'
OUT = ROOT / 'public/characters'
REPORT = ROOT / 'artifacts/characters'
REPORT.mkdir(parents=True, exist_ok=True)
CANVAS = (512, 768)

# Source crop, exposed face left/right/bottom, and manually traced exposed-skin polygon.
HEADS = [
 ('H01',(105,22,434,306),(195,367,292),[(222,164),(281,163),(336,150),(347,165),(365,176),(366,257),(360,276),(338,286),(276,290),(219,286),(198,277),(195,265),(197,216),(207,207),(214,178)]),
 ('H02',(592,22,921,305),(680,853,292),[(706,164),(765,163),(822,150),(836,168),(851,177),(852,258),(846,277),(826,286),(765,290),(707,286),(684,277),(680,266),(682,217),(695,209)]),
 ('H03',(1109,22,1418,340),(1195,1338,284),[(1201,163),(1254,161),(1292,148),(1319,128),(1334,173),(1337,251),(1333,269),(1317,279),(1260,283),(1210,278),(1196,268)]),
 ('H04',(122,370,427,678),(211,347,624),[(216,507),(262,508),(302,496),(327,483),(342,521),(347,557),(346,602),(339,617),(310,622),(258,624),(220,617),(212,608)]),
 ('H05',(600,375,922,674),(693,846,629),[(703,517),(737,500),(761,481),(782,498),(813,511),(837,515),(844,548),(846,586),(840,612),(825,624),(772,628),(719,625),(701,618),(693,582),(694,543)]),
 ('H06',(1111,384,1408,643),(1182,1344,633),[(1191,542),(1218,533),(1235,537),(1260,524),(1286,535),(1305,530),(1334,547),(1341,588),(1342,610),(1333,624),(1316,630),(1232,633),(1198,627),(1182,614),(1184,578)]),
 ('H07',(127,715,418,960),(179,366,954),[(184,903),(201,871),(217,834),(245,844),(274,849),(273,835),(302,848),(341,859),(343,851),(360,856),(366,916),(360,937),(345,947),(297,952),(215,951),(190,942),(180,928)]),
 ('H08',(617,715,908,960),(672,857,954),[(676,902),(691,868),(702,835),(729,844),(757,849),(752,834),(783,846),(824,858),(826,850),(849,856),(855,912),(851,934),(835,946),(785,952),(712,950),(686,944),(673,927)]),
 ('H09',(1122,716,1407,960),(1172,1358,954),[(1178,900),(1192,867),(1201,842),(1238,852),(1281,861),(1314,863),(1312,851),(1342,853),(1353,886),(1357,920),(1351,936),(1337,946),(1290,953),(1215,951),(1187,941),(1174,925)])
]

def exterior_mask(rgb):
    """Flood only pale, border-connected pixels; closed white regions are retained."""
    arr=np.asarray(rgb).astype(np.int16)
    candidate=(arr.min(2)>112)&((arr.max(2)-arr.min(2))<110)&(arr[:,:,1]>140)
    h,w=candidate.shape; outside=np.zeros((h,w),dtype=bool); q=deque()
    for x in range(w):
        for y in (0,h-1):
            if candidate[y,x] and not outside[y,x]:outside[y,x]=True;q.append((x,y))
    for y in range(h):
        for x in (0,w-1):
            if candidate[y,x] and not outside[y,x]:outside[y,x]=True;q.append((x,y))
    while q:
        x,y=q.popleft()
        for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0<=nx<w and 0<=ny<h and candidate[ny,nx] and not outside[ny,nx]:
                outside[ny,nx]=True;q.append((nx,ny))
    # Labels below long hair are disconnected ink, not part of the sprite.
    foreground=~outside;visited=np.zeros_like(foreground);largest=[]
    for sy,sx in np.argwhere(foreground):
        if visited[sy,sx]:continue
        component=[];queue=deque([(int(sx),int(sy))]);visited[sy,sx]=True
        while queue:
            x,y=queue.popleft();component.append((x,y))
            for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if 0<=nx<w and 0<=ny<h and foreground[ny,nx] and not visited[ny,nx]:
                    visited[ny,nx]=True;queue.append((nx,ny))
        if len(component)>len(largest):largest=component
    alpha=np.zeros((h,w),dtype='uint8')
    for x,y in largest:alpha[y,x]=255
    return Image.fromarray(alpha)

metadata={}; source=Image.open(SOURCE/'heads.png').convert('RGB')
for id,crop,face,poly in HEADS:
    l,t,r,b=crop; left,right,bottom=face
    part=source.crop(crop).convert('RGBA');part.putalpha(exterior_mask(part.convert('RGB')))
    scale=140/(right-left); center=(left+right)/2
    tx=256+(l-center)*scale;ty=280+(t-bottom)*scale
    resized=part.resize((round(part.width*scale),round(part.height*scale)),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',CANVAS);canvas.alpha_composite(resized,(round(tx),round(ty)))
    # Exposed skin mask follows the reference fringe, never the rectangular crop.
    points=[(256+(x-center)*scale,280+(y-bottom)*scale) for x,y in poly]
    mask=Image.new('RGBA',(1024,1536));d=ImageDraw.Draw(mask);d.polygon([(x*2,y*2) for x,y in points],fill='white')
    face_mask=mask.resize(CANVAS,Image.Resampling.LANCZOS)
    face_mask.save(OUT/f'hair-heads/{id}-face-mask.png')
    flatten_head(canvas,face_mask,id).save(OUT/f'hair-heads/{id}.png')
    short=id in ('H06','H07','H08','H09')
    metadata[id]={'face':{'x':190 if short else 178,'y':194 if short else 177,'width':132 if short else 156,'height':99 if short else 117},'faceCenter':{'x':256,'y':235 if short else 222},'headConnection':{'x':256,'y':280},'sourceCrop':crop,'scale':round(scale,5)}

# Exact facial features retained, including white eyes, mouth details and beard.
# Bounds exclude every catalog label/card. All expressions share an eye-line anchor.
FACES=[
 ('female','F01',(36,99,197,210),(117,145)),('female','F02',(260,95,416,215),(337,145)),('female','F03',(478,103,635,210),(556,145)),('female','F04',(679,107,840,212),(759,151)),('female','F05',(894,112,1057,213),(974,156)),('female','F06',(1118,105,1262,215),(1190,148)),('female','F07',(1338,103,1497,211),(1417,148)),
 ('female','F08',(48,308,208,419),(127,358)),('female','F09',(268,307,436,414),(352,357)),('female','F10',(498,310,663,419),(580,359)),('female','F11',(713,308,898,418),(804,358)),('female','F12',(949,309,1127,415),(1038,359)),('female','F13',(1189,312,1365,418),(1278,357)),
 ('male','M01',(62,595,208,697),(135,637)),('male','M02',(290,594,468,696),(381,637)),('male','M03',(560,588,720,697),(640,637)),('male','M04',(784,581,966,706),(875,637)),('male','M05',(1038,591,1226,697),(1131,637)),('male','M06',(1305,582,1497,706),(1401,637)),
 ('child','C01',(44,838,190,941),(117,888)),('child','C02',(217,839,379,940),(298,888)),('child','C03',(402,839,554,943),(478,888)),('child','C04',(592,837,741,944),(668,888)),
 ('baby','B01',(809,838,956,941),(882,888)),('baby','B02',(1000,839,1147,940),(1074,888)),('baby','B03',(1174,838,1320,940),(1246,888)),('baby','B04',(1350,834,1504,945),(1427,888))
]
face_source=Image.open(SOURCE/'faces.png').convert('RGBA')
for category,id,bounds,eye in FACES:
    part=face_source.crop(bounds);a=np.array(part.getchannel('A'));a[a<16]=0;part.putalpha(Image.fromarray(a))
    scale=1.18; part=part.resize((round(part.width*scale),round(part.height*scale)),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(240,180));canvas.alpha_composite(part,(round(120+(bounds[0]-eye[0])*scale),round(70+(bounds[1]-eye[1])*scale)))
    canvas.save(OUT/f'faces/{category}/{id}.png')

(OUT/'head-alignment.json').write_text(json.dumps(metadata,indent=2)+'\n')
# Review source-alpha and exact work performed; browser never loads the catalog sheets.
report={'sources':{},'heads':9,'faces':27,'torsos':12,'legs':12,'babyBody':'provisional manually drawn SVG; no baby body reference supplied'}
for p in SOURCE.glob('*.png'):
    im=Image.open(p);report['sources'][p.stem]={'mode':im.mode,'size':im.size,'alphaRange':im.getchannel('A').getextrema() if im.mode=='RGBA' else None}
(REPORT/'source-report.json').write_text(json.dumps(report,indent=2)+'\n')
# A single composited inspection sheet makes alpha problems visible on the intended skin color.
sheet=Image.new('RGB',(1080,780),'#f5ece2');d=ImageDraw.Draw(sheet)
for i,(id,*_) in enumerate(HEADS):
    im=Image.open(OUT/f'hair-heads/{id}.png');im.thumbnail((220,330));x=(i%3)*360+70;y=(i//3)*260-8
    # Crop only the head in this inspection output.
    head=Image.open(OUT/f'hair-heads/{id}.png').crop((70,20,442,350));head.thumbnail((240,215));sheet.paste(head,(x,y+20),head);d.text((x+100,y+236),id,fill='#292323')
sheet.save(REPORT/'heads-inspection.jpg')
print('Prepared 9 heads, 9 exposed-face masks, and all 27 facial decals.')
