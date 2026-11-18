"""Lab 3 — 비교 기준 (지도 회귀): 직물 특성 19항목 → Voc
원단 단위 5겹 교차검증 + 시험 자료 + 새 조합 시험. 생성 모델이 넘어야 할 기준선.
결과: outputs/lab3_baseline_scores.csv"""
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
from sklearn.linear_model import RidgeCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score, mean_squared_error
from common import load, save, X19, Y, LogStd

tr, te, nc = load("02_train.csv"), load("02_test.csv"), load("02_test_new_combo.csv")
models = {
    "평균(기준선)": None,
    "릿지": lambda: RidgeCV(alphas=np.logspace(-3, 3, 13)),
    "랜덤포레스트": lambda: RandomForestRegressor(n_estimators=300, min_samples_leaf=3, random_state=0),
    "가우시안 과정": lambda: GaussianProcessRegressor(ConstantKernel() * RBF(np.ones(len(X19))) + WhiteKernel(), normalize_y=True, random_state=0),
}
def fit_pred(name, a, b):
    t = LogStd().fit(a, X19); Xa, Xb = t.transform(a), t.transform(b)
    ya = np.log(a[Y].values)
    if models[name] is None:
        return np.full(len(b), np.exp(ya.mean()))
    m = models[name](); m.fit(Xa, ya); return np.exp(m.predict(Xb))
rows = []
for name in models:
    cv = []
    for i, (a, b) in enumerate(KFold(5, shuffle=True, random_state=0).split(tr)):
        p = fit_pred(name, tr.iloc[a], tr.iloc[b]); cv.append(r2_score(tr.iloc[b][Y], p))
    pt, pn = fit_pred(name, tr, te), fit_pred(name, tr, nc)
    rows.append(dict(model=name, cv_R2=np.mean(cv), cv_R2_sd=np.std(cv), test_R2=r2_score(te[Y], pt),
                     test_RMSE=mean_squared_error(te[Y], pt) ** 0.5, newcombo_RMSE=mean_squared_error(nc[Y], pn) ** 0.5))
    print(f"{name:8s} CV R² {np.mean(cv):.3f}  시험 R² {rows[-1]['test_R2']:.3f}  새 조합 RMSE {rows[-1]['newcombo_RMSE']:.1f} V")
save(pd.DataFrame(rows), "lab3_baseline_scores.csv")
print("측정 오차 수준(참고): Voc 반복 CV 중앙값", round(tr.Voc_cv.median(), 3), "→ 이보다 작은 오차는 과적합 의심")
