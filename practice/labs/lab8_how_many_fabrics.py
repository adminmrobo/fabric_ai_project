"""Lab 8 — 원단이 몇 개면 관계가 보이나 (학습 곡선)
학습 원단 수를 늘려 가며 시험 자료 R²를 잰다. 실측(S2) 원단 수를 정할 때 쓴다.
결과: outputs/lab8_learning_curve.csv"""
import numpy as np, pandas as pd, warnings, sys
warnings.filterwarnings("ignore")
from sklearn.ensemble import RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel
from sklearn.metrics import r2_score
from common import load, save, X8, Y, LogStd

tr, te = load("02_train.csv"), load("02_test.csv")
sizes = [15, 25, 40, 60, 100, 160, 250, len(tr)]
seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 5
models = {
    "랜덤포레스트": lambda: RandomForestRegressor(n_estimators=200, min_samples_leaf=2, random_state=0),
    "가우시안 과정": lambda: GaussianProcessRegressor(ConstantKernel() * RBF(np.ones(len(X8))) + WhiteKernel(), normalize_y=True, random_state=0),
}
rows = []
for n in sizes:
    for s in range(seeds if n < len(tr) else 1):
        sub = tr.sample(n, random_state=s)
        t = LogStd().fit(sub, X8)
        for name, mk in models.items():
            m = mk().fit(t.transform(sub), np.log(sub[Y].values))
            rows.append(dict(n=n, seed=s, model=name, test_R2=r2_score(te[Y], np.exp(m.predict(t.transform(te))))))
df = pd.DataFrame(rows)
out = df.groupby(["model", "n"]).test_R2.agg(["mean", "std"]).reset_index().fillna(0)
print(out.round(3).to_string(index=False))
save(out, "lab8_learning_curve.csv")
print("읽는 법: 곡선이 평평해지기 시작하는 원단 수가 '관계가 보이는' 최소 규모. 실측은 측정 오차가 더 클 수 있어 여유를 둔다.")
