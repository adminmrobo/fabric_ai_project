"""Lab 4b — 생성 모델의 예측 성적: p(y | x)를 시험 자료로 잰다
Lab 4와 같은 방식(학습 자료의 X8 + Y를 로그·표준화, BIC로 무리 수)으로 가우시안 혼합을 학습하고,
시험 자료·새 조합 시험에서 조건부 평균(예측값)과 ±2σ 범위가 실제 Voc를 얼마나 맞히는지 잰다.
지도 회귀 기준선(Lab 3)과 같은 표에 놓고 비교한다.
결과: outputs/lab4b_generative_test.csv, lab4b_predictions.csv"""
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
from sklearn.mixture import GaussianMixture
from sklearn.metrics import r2_score, mean_squared_error
from common import load, save, X8, Y, LogStd, gmm_conditional

tr, te, nc = load("02_train.csv"), load("02_test.csv"), load("02_test_new_combo.csv")
cols = X8 + [Y]
t = LogStd().fit(tr, cols); Z = t.transform(tr)           # 변환 기준은 학습 자료로만
bics = [GaussianMixture(k, covariance_type="full", random_state=0, n_init=3).fit(Z).bic(Z) for k in range(1, 9)]
K = int(np.argmin(bics)) + 1
gmm = GaussianMixture(K, covariance_type="full", random_state=0, n_init=5).fit(Z)
ix, iy = list(range(len(X8))), len(X8)
mu_y, sd_y = t.mu[iy], t.sd[iy]

def predict(df):
    Zx = (np.log(df[X8].values) - t.mu[ix]) / t.sd[ix]
    m, s, _ = gmm_conditional(gmm, Zx, ix, iy)
    return np.exp(m * sd_y + mu_y), np.exp((m - 2 * s) * sd_y + mu_y), np.exp((m + 2 * s) * sd_y + mu_y)

rows, preds = [], []
for name, df in [("시험", te), ("새 조합", nc)]:
    p, lo, hi = predict(df)
    y = df[Y].values
    cover = float(np.mean((y >= lo) & (y <= hi)))
    rows.append(dict(set=name, components=K, n=len(df), R2=r2_score(y, p), RMSE=mean_squared_error(y, p) ** 0.5,
                     cover95=cover, mean_width_V=float(np.mean(hi - lo))))
    preds.append(pd.DataFrame(dict(set=name, fabric_id=df.fabric_id, material=df.material, structure=df.structure,
                                   Voc_true=y, Voc_pred=p, Voc_lo95=lo, Voc_hi95=hi, inside=(y >= lo) & (y <= hi))))
R = pd.DataFrame(rows)
print(f"가우시안 혼합 (무리 {K}개) p(y | x)")
print(R.round(3).to_string(index=False))
save(R, "lab4b_generative_test.csv"); save(pd.concat(preds), "lab4b_predictions.csv")
print("읽는 법: R²·RMSE는 Lab 3 기준선과 비교, cover95는 ±2σ 범위가 실제 값을 담은 비율(0.95 근처면 범위가 정직함).")
