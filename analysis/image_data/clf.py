import pandas as pd,numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, roc_auc_score
f=pd.read_csv('features.csv'); f['y']=(f.cls=='harsh').astype(int)
tr,te=f[f.set=='train'],f[f.set=='test']
def run(cols,name):
    X=pd.get_dummies(f[cols],dtype=float)
    m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000)).fit(X[f.set=='train'],tr.y)
    p=m.predict_proba(X[f.set=='test'])[:,1]
    print(f'{name:28s} test acc {accuracy_score(te.y,p>.5):.2f}  AUC {roc_auc_score(te.y,p):.2f}')
run(['contrast'],'명암 대비 하나')
run(['kb'],'파일 크기 하나')
run(['bright'],'밝기 하나')
run(['sat'],'채도 하나')
run(['light','color','dist','weave'],'촬영 조건(조명·색·거리·조직)')
run(['contrast','sharp','hf','aniso','bright','sat','kb','illum'],'손으로 만든 특징 8개')
# threshold rule
for t in [12,14,16]:
    print('contrast >',t,'→ 거침: train',((tr.contrast>t)==tr.y).mean().round(3),'test',((te.contrast>t)==te.y).mean().round(3))
print(f.groupby(['cls','color']).contrast.median().unstack().round(1))
print(f.groupby('cls').contrast.agg(['min','max']).round(1))
print(f[f.cls=='harsh'].sort_values('contrast').head(5)[['name','type','deg','color','contrast']])
print(f[f.cls=='soft'].sort_values('contrast').tail(5)[['name','color','light','contrast']])
print(f.groupby(['type','deg']).contrast.median().unstack().round(1))
print(f.groupby('regen').size(), f.groupby(['regen','cls']).size())
