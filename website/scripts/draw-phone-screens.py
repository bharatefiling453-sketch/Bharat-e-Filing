from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from collections import deque
D='/tmp/claude-0/-home-user-Bharat-e-Filing/6ad0d519-9932-5f4b-8c2b-13c968900758/images/'
S='/tmp/claude-0/-home-user-Bharat-e-Filing/6ad0d519-9932-5f4b-8c2b-13c968900758/scratchpad/'
F=S+'Inter.ttf'; FX=S+'InterExt.ttf'
def font(sz, wght=700, ext=False):
    f=ImageFont.truetype(FX if ext else F, sz)
    try: f.set_variation_by_axes([14 if sz<20 else 32, wght])
    except Exception:
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f
def screen_mask(img, seed, thr=215):
    a=np.asarray(img.convert('RGB')).astype(int); h,w,_=a.shape
    ok=a.min(axis=2)>thr; m=np.zeros((h,w),bool); q=deque([seed]); m[seed[1],seed[0]]=True
    while q:
        x,y=q.popleft()
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+dx,y+dy
            if 0<=nx<w and 0<=ny<h and not m[ny,nx] and ok[ny,nx]: m[ny,nx]=True; q.append((nx,ny))
    ys,xs=np.where(m); return m,(xs.min(),ys.min(),xs.max()+1,ys.max()+1)
NAVY=(16,33,97); SAFF=(255,136,19); LEAF=(60,140,49); WA=(7,94,84); INK=(29,29,31)
def ui_filed(W,H,k):
    im=Image.new('RGB',(W*k,H*k),(255,255,255)); d=ImageDraw.Draw(im); s=lambda v:int(v*k)
    d.rectangle([0,0,W*k,s(H*0.17)],fill=NAVY)
    d.text((s(W/2),s(H*0.095)),'Bharat e-Filing',font=font(s(W*0.105)),fill=(255,255,255),anchor='mm')
    cx,cy,r=W/2,H*0.36,W*0.2
    d.ellipse([s(cx-r),s(cy-r),s(cx+r),s(cy+r)],fill=LEAF)
    d.line([s(cx-r*0.45),s(cy+r*0.02),s(cx-r*0.1),s(cy+r*0.38),s(cx+r*0.5),s(cy-r*0.35)],fill=(255,255,255),width=s(W*0.045),joint='curve')
    d.text((s(W/2),s(H*0.56)),'GSTR-3B',font=font(s(W*0.12),600),fill=(110,110,115),anchor='mm')
    d.text((s(W/2),s(H*0.645)),'Filed!',font=font(s(W*0.2),800),fill=NAVY,anchor='mm')
    d.rounded_rectangle([s(W*0.12),s(H*0.74),s(W*0.88),s(H*0.84)],radius=s(W*0.06),fill=(236,247,234))
    d.text((s(W/2),s(H*0.79)),'No late fee',font=font(s(W*0.105),700),fill=(47,111,39),anchor='mm')
    d.rounded_rectangle([s(W*0.12),s(H*0.87),s(W*0.88),s(H*0.95)],radius=s(W*0.06),fill=SAFF)
    d.text((s(W/2),s(H*0.91)),'View ARN',font=font(s(W*0.095),700),fill=(11,20,51),anchor='mm')
    return im.resize((W,H),Image.LANCZOS)
def ui_reminder(W,H,k):
    im=Image.new('RGB',(W*k,H*k),(239,234,226)); d=ImageDraw.Draw(im); s=lambda v:int(v*k)
    d.rectangle([0,0,W*k,s(H*0.15)],fill=WA)
    d.ellipse([s(W*0.07),s(H*0.04),s(W*0.07+W*0.15),s(H*0.04+W*0.15)],fill=SAFF)
    d.text((s(W*0.28),s(H*0.075)),'Bharat e-Filing',font=font(s(W*0.085)),fill=(255,255,255),anchor='lm')
    def bubble(y0,y1,x0,x1,col,lines):
        d.rounded_rectangle([s(x0),s(y0),s(x1),s(y1)],radius=s(W*0.05),fill=col)
        yy=y0+(y1-y0)/2-(len(lines)-1)*W*0.06
        for t,f,c in lines: d.text((s(x0+W*0.05),s(yy)),t,font=f,fill=c,anchor='lm'); yy+=W*0.12
    bubble(H*0.2,H*0.43,W*0.06,W*0.86,(255,255,255),[('GSTR-3B due',font(s(W*0.085),700),INK),('in 3 days ⏰'.replace(' ⏰',''),font(s(W*0.085),700),(196,22,28)),('Send your bills',font(s(W*0.072),500),(66,66,69))])
    bubble(H*0.47,H*0.58,W*0.3,W*0.94,(217,253,211),[('Bills sent ✓'.replace(' ✓',''),font(s(W*0.08),700),INK)])
    bubble(H*0.62,H*0.79,W*0.06,W*0.86,(255,255,255),[('Filed today!',font(s(W*0.085),800),(47,111,39)),('ARN on WhatsApp',font(s(W*0.068),500),(66,66,69))])
    d.rounded_rectangle([s(W*0.06),s(H*0.84),s(W*0.94),s(H*0.93)],radius=s(W*0.08),fill=SAFF)
    d.text((s(W/2),s(H*0.885)),'File my GST',font=font(s(W*0.09),800),fill=(11,20,51),anchor='mm')
    return im.resize((W,H),Image.LANCZOS)
def apply(n,seed,ui,out):
    img=Image.open(D+f'{n}.webp').convert('RGB')
    m,(x0,y0,x1,y1)=screen_mask(img,seed)
    W,H=x1-x0,y1-y0; print(n,'screen',x0,y0,W,H)
    panel=ui(W,H,4)
    mask=Image.fromarray((m[y0:y1,x0:x1]*255).astype('uint8')).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.6))
    img.paste(panel,(x0,y0),mask); img.save(S+'img/'+out+'.png'); return img
apply(13,(1172,410),ui_filed,'s1')
apply(15,(420,495),ui_reminder,'cafe')
