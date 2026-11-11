from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=2048,1152
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',64)
def page(photos, out, t="Иш-чаралардан сүрөттөр"):
    bg=Image.open('slide_2.png').convert('RGB').resize((W,H)).filter(ImageFilter.GaussianBlur(28))
    bg=Image.blend(bg,Image.new('RGB',(W,H),(235,242,252)),0.55)
    d=ImageDraw.Draw(bg)
    tw=d.textlength(t,font=F); bw=tw+160
    d.rounded_rectangle(((W-bw)/2,50,(W+bw)/2,170),60,fill=(16,38,104),outline=(214,175,80),width=5)
    d.text((W/2,110),t,font=F,fill='white',anchor='mm')
    top,bottom,gap=220,H-60,50
    ims=[Image.open(p).convert('RGB') for p in photos]
    ah=bottom-top
    ws=[im.width*ah/im.height for im in ims]
    scale=min(1,(W-120-gap*(len(ims)-1))/sum(ws)); h=int(ah*scale)
    x=(W-(sum(ws)*scale+gap*(len(ims)-1)))/2; y=top+(ah-h)//2
    for im,w in zip(ims,ws):
        w=int(w*scale); im=im.resize((w,h),Image.LANCZOS)
        sh=Image.new('RGBA',(w+60,h+60),(0,0,0,0)); ImageDraw.Draw(sh).rectangle((30,30,w+30,h+30),fill=(0,0,40,90))
        sh=sh.filter(ImageFilter.GaussianBlur(14)); bg.paste(sh,(int(x)-22,y-18),sh)
        d.rectangle((int(x)-8,y-8,int(x)+w+8,y+h+8),fill='white')
        bg.paste(im,(int(x),y)); x+=w+gap
    bg.save(out)
page(['../photos/photo_1_HD.jpg','../photos/photo_4_HD.jpg'],'photos_page_1.png')
page(['../photos/photo_2_HD.jpg','../photos/photo_3_HD.jpg'],'photos_page_2.png')
L='../photos/lineika/lineika_'
T="1-сентябрь – Билим күнү: салтанаттуу линейка"
page([L+'3.jpg',L+'1.jpg',L+'5.jpg'],'lineika_page_1.png',T)
page([L+'2.jpg',L+'4.jpg'],'lineika_page_2.png',T)
