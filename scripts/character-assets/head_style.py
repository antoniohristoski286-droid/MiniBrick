"""Flatten the existing head artwork without moving its silhouette or face anchors."""
from collections import deque
from PIL import Image, ImageFilter
import numpy as np

SKIN = (255, 199, 142)
INK = (24, 25, 25)
PALETTES = {
 'brown': [(143,75,41),(111,56,31),(65,37,25)],
 'blonde': [(237,199,126),(207,165,94),(153,116,67)],
 'black': [(49,49,51),(37,37,39),(25,25,27)],
}

def flatten_head(image, face_mask, head_id):
    original=np.asarray(image).copy();rgb=original[:,:,:3].astype(np.int16);alpha=original[:,:,3]
    # A connected skin region seeded inside the exposed head. The hue predicate
    # distinguishes peach from blonde; the skin/hair outline remains the barrier.
    r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    allowed=np.asarray(face_mask.getchannel('A').filter(ImageFilter.MaxFilter(21)))>0
    candidate=(r>195)&(r-g>20)&(g-b>25)&((r-g)>(g-b)*.65)&(b>95)&(alpha>128)&allowed
    h,w=alpha.shape;skin=np.zeros((h,w),dtype=bool)
    y,x=(235 if head_id in ('H06','H07','H08','H09') else 222),256
    assert candidate[y,x],f'{head_id}: skin anchor not inside the face'
    q=deque([(x,y)]);skin[y,x]=True
    while q:
        x,y=q.popleft()
        for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0<=nx<w and 0<=ny<h and candidate[ny,nx] and not skin[ny,nx]:
                skin[ny,nx]=True;q.append((nx,ny))
    family='blonde' if head_id in ('H02','H09') else 'black' if head_id in ('H04','H05','H06','H07') else 'brown'
    palette=np.array(PALETTES[family],dtype=np.int16)
    if head_id=='H03':palette=np.array([(143,75,41),(85,41,23),(50,30,20)],dtype=np.int16)
    if head_id=='H09':palette=np.array([(242,203,132),(218,178,110),(153,116,67)],dtype=np.int16)
    if head_id=='H08':palette=np.array([(127,68,39),(98,49,28),(58,34,23)],dtype=np.int16)
    smooth=np.asarray(image.convert('RGB').filter(ImageFilter.GaussianBlur(2))).astype(np.int16)
    distances=((smooth[:,:,None,:].astype(np.float32)-palette[None,None,:,:])**2).sum(3)
    labels=Image.fromarray(np.argmin(distances,axis=2).astype('uint8')).filter(ImageFilter.ModeFilter(5))
    skin=np.asarray(Image.fromarray((skin*255).astype('uint8')).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MedianFilter(5)))>128
    flat=palette[np.asarray(labels)].astype('uint8');flat[skin]=SKIN
    inner_skin=np.asarray(Image.fromarray((skin*255).astype('uint8')).filter(ImageFilter.MinFilter(7)))>128
    flat[skin&~inner_skin]=INK
    # Draw inside the original silhouette, so the transparent geometry is exact.
    eroded=np.asarray(image.getchannel('A').filter(ImageFilter.MinFilter(7)))
    rim=np.divide(alpha.astype(float)-eroded,alpha,out=np.zeros_like(alpha,dtype=float),where=alpha>0)
    flat=np.round(flat*(1-rim[:,:,None])+np.array(INK)*rim[:,:,None]).astype('uint8')
    result=np.dstack((flat,alpha));result[alpha==0,:3]=0
    return Image.fromarray(result,'RGBA')
