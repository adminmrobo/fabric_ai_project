import pandas as pd, numpy as np, cv2, os, json
import sys
R=sys.argv[1] if len(sys.argv)>1 else 'fabric_dataset'
d=pd.read_csv(f'{R}/creation_log.csv'); pd.set_option('display.width',200)
print(pd.crosstab(d['클래스'],d['조명'])); print(pd.crosstab(d['거침 유형'],d['조직'])); print(pd.crosstab(d['거침 유형'],d['거리']))
rows=[]
def phash(g):
    s=cv2.resize(g,(32,32),interpolation=cv2.INTER_AREA).astype(np.float32); c=cv2.dct(s)[:8,:8]; return (c>np.median(c)).flatten()
H={}
for _,r in d.iterrows():
    cls='soft' if r['클래스']=='부드러움' else 'harsh'
    p=f"{R}/{r['세트']}/{cls}/{r['파일명']}.jpg"
    im=cv2.imread(p); h,w=im.shape[:2]; g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    gs=cv2.resize(g,(512,512),interpolation=cv2.INTER_AREA).astype(np.float32)
    lap=cv2.Laplacian(gs,cv2.CV_32F).var()
    F=np.abs(np.fft.fftshift(np.fft.fft2(gs-gs.mean())))**2; yy,xx=np.indices(F.shape); rr=np.hypot(yy-256,xx-256)
    hf=F[rr>64].sum()/F.sum()
    gx=cv2.Sobel(gs,cv2.CV_32F,1,0);gy=cv2.Sobel(gs,cv2.CV_32F,0,1);ang=np.arctan2(gy,gx);mag=np.hypot(gx,gy)
    hist,_=np.histogram(np.mod(ang,np.pi),bins=18,weights=mag); hist=hist/hist.sum(); aniso=float(hist.max()/hist.mean())
    hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
    # vignetting / illumination gradient: mean of 4x4 blocks std
    blk=cv2.resize(gs,(4,4),interpolation=cv2.INTER_AREA); illum=float(blk.std())
    H[r['파일명']]=phash(g)
    rows.append(dict(name=r['파일명'],set=r['세트'],cls=cls,type=r['거침 유형'],light=r['조명'],color=r['색상'],dist=r['거리'],weave=r['조직'],deg=r['거침 정도'],
      w=w,h=h,kb=os.path.getsize(p)/1024,bright=float(gs.mean()),contrast=float(gs.std()),sharp=float(lap),hf=float(hf),aniso=aniso,sat=float(hsv[...,1].mean()),illum=illum,regen=r['비고'] if isinstance(r['비고'],str) else ''))
f=pd.DataFrame(rows); f.to_csv('features.csv',index=False)
print(f.groupby(['w','h']).size())
print(f.groupby('cls')[['kb','bright','contrast','sharp','hf','aniso','sat','illum']].median().round(3))
print(f.groupby('type')[['kb','contrast','sharp','hf','aniso']].median().round(3))
# near duplicates
names=list(H); M=np.array([H[n] for n in names]); D=(M[:,None,:]!=M[None,:,:]).sum(-1)
sets=dict(zip(f.name,f.set)); pairs=[]
for i in range(len(names)):
    for j in range(i+1,len(names)):
        if D[i,j]<=10: pairs.append((names[i],names[j],int(D[i,j]),sets[names[i]]+'-'+sets[names[j]]))
print('near-dup pairs <=10:',len(pairs),pairs[:15])
print('min train-test dist', min(D[i,j] for i in range(len(names)) for j in range(len(names)) if sets[names[i]]!=sets[names[j]]))
