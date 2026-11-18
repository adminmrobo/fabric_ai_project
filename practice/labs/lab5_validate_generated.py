"""Lab 5 — 생성 데이터 검증: ① 열별 분포 비교(KS) ② 상관 구조 차이 ③ TSTR vs TRTR
TSTR = 생성 데이터로 학습, 실측(시험)으로 평가. TRTR = 실측 학습, 실측 평가.
결과: outputs/lab5_ks.csv, lab5_corr_gap.csv, lab5_tstr.csv"""
import numpy as np, pandas as pd
from scipy.stats import ks_2samp
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from common import load, save, X8, Y, LogStd, OUT
import os

tr, te = load("02_train.csv"), load("02_test.csv")
G = pd.read_csv(os.path.join(OUT, "lab4_generated_candidates.csv")).rename(columns={"Voc_sampled": Y})
cols = X8 + [Y]
ks = [dict(item=c, KS=ks_2samp(np.log(tr[c]), np.log(G[c])).statistic, p=ks_2samp(np.log(tr[c]), np.log(G[c])).pvalue) for c in cols]
K = pd.DataFrame(ks); K["판정"] = np.where(K.KS < 0.1, "닮음", np.where(K.KS < 0.2, "주의", "다름")); save(K, "lab5_ks.csv")
cr, cg = np.log(tr[cols]).corr(), np.log(G[cols]).corr()
gap = (cg - cr).abs(); C = gap.stack().reset_index(); C.columns = ["a", "b", "abs_gap"]; C = C[C.a < C.b].sort_values("abs_gap", ascending=False)
save(C, "lab5_corr_gap.csv"); print("상관 차이 최대:", round(C.abs_gap.max(), 3), "평균:", round(C.abs_gap.mean(), 3))
def score(train, label):
    t = LogStd().fit(train, X8); m = RandomForestRegressor(300, min_samples_leaf=3, random_state=0)
    m.fit(t.transform(train), np.log(train[Y])); p = np.exp(m.predict(t.transform(te)))
    return dict(setting=label, n_train=len(train), test_R2=r2_score(te[Y], p), test_RMSE=mean_squared_error(te[Y], p) ** 0.5)
T = pd.DataFrame([score(tr, "TRTR 실측 학습 → 실측 시험"), score(G, "TSTR 생성 학습 → 실측 시험"),
                  score(pd.concat([tr, G]), "실측+생성 학습 → 실측 시험")])
save(T, "lab5_tstr.csv"); print(T.round(3).to_string(index=False))
print("해석: TSTR이 TRTR에 가까우면 생성 데이터가 패턴을 잘 담은 것. 실측+생성이 TRTR보다 나아지지 않으면 생성은 새 정보를 주지 못한 것.")
