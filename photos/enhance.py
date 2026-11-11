import cv2, sys, numpy as np
def up(img,T=320,P=12):
    H,W=img.shape[:2]; out=np.zeros((H*2,W*2,3),np.uint8)
    for y in range(0,H,T):
        for x in range(0,W,T):
            y0,x0=max(0,y-P),max(0,x-P); y1,x1=min(H,y+T+P),min(W,x+T+P)
            t=sr.upsample(img[y0:y1,x0:x1])
            oy,ox=(y-y0)*2,(x-x0)*2; hh,ww=min(T,H-y)*2,min(T,W-x)*2
            out[y*2:y*2+hh,x*2:x*2+ww]=t[oy:oy+hh,ox:ox+ww]
    return out
sr = cv2.dnn_superres.DnnSuperResImpl_create(); sr.readModel("models/EDSR_x2.pb"); sr.setModel("edsr", 2)
def wb(img):  # gray-world white balance, mild
    f=img.astype(np.float32); m=f.reshape(-1,3).mean(0); g=m.mean()
    f*= (1+0.6*(g/m-1)); return np.clip(f,0,255).astype(np.uint8)
for i in sys.argv[1:]:
    img=cv2.imread(f"orig/photo_{i}.jpg")
    img=cv2.fastNlMeansDenoisingColored(img,None,3,3,7,21)
    img=up(img)
    img=wb(img)
    lab=cv2.cvtColor(img,cv2.COLOR_BGR2LAB); l,a,b=cv2.split(lab)
    l=cv2.createCLAHE(clipLimit=1.6,tileGridSize=(8,8)).apply(l)
    img=cv2.cvtColor(cv2.merge([l,a,b]),cv2.COLOR_LAB2BGR)
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV).astype(np.float32); hsv[...,1]*=1.08
    img=cv2.cvtColor(np.clip(hsv,0,255).astype(np.uint8),cv2.COLOR_HSV2BGR)
    blur=cv2.GaussianBlur(img,(0,0),1.2); img=cv2.addWeighted(img,1.35,blur,-0.35,0)
    cv2.imwrite(f"photo_{i}_HD.jpg",img,[cv2.IMWRITE_JPEG_QUALITY,96]); print(i, img.shape)
