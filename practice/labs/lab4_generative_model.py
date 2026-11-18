"""Lab 4 — 생성 모델 (비지도): 실측 직물의 패턴 p(X, Y)를 가우시안 혼합으로 학습
→ 새 직물 생성 → 각 새 직물의 Voc를 연속값(조건부 평균)과 범위(조건부 표준편차)로
결과: outputs/lab4_bic.csv, lab4_generated_candidates.csv"""
import numpy as np, pandas as pd
from sklearn.mixture import GaussianMixture
from common import load, save, X8, Y, LogStd, gmm_conditional

tr = load("02_train.csv")
cols = X8 + [Y]                                  # 원단 수가 적으면 핵심 8항목 + Y로 시작
t = LogStd().fit(tr, cols); Z = t.transform(tr)
bic = []
for k in range(1, 9):
    g = GaussianMixture(k, covariance_type="full", random_state=0, n_init=3).fit(Z); bic.append(dict(components=k, BIC=g.bic(Z)))
B = pd.DataFrame(bic); save(B, "lab4_bic.csv")
K = int(B.loc[B.BIC.idxmin(), "components"]); print("BIC로 고른 무리 수:", K)
gmm = GaussianMixture(K, covariance_type="full", random_state=0, n_init=5).fit(Z)
Zg, comp = gmm.sample(1000)                    # 결합분포에서 새 직물 (X와 Y 함께)
ix, iy = list(range(len(X8))), len(X8)
mean, sd, _ = gmm_conditional(gmm, Zg[:, ix], ix, iy)
G = t.inverse(Zg)                              # 원래 단위로
G.insert(0, "gen_id", [f"G{i+1:04d}" for i in range(len(G))]); G.insert(1, "component", comp)
lo, hi = mean - 2 * sd, mean + 2 * sd           # 로그·표준화 공간의 Y → 원래 단위
mu_y, sd_y = t.mu[iy], t.sd[iy]
G["Voc_pred"] = np.exp(mean * sd_y + mu_y)
G["Voc_lo95"] = np.exp(lo * sd_y + mu_y); G["Voc_hi95"] = np.exp(hi * sd_y + mu_y)
G["pred_sd_z"] = sd                            # 표준화 단위 불확실도 (클수록 모델이 모름)
# 적용 범위 검사: 학습 자료의 1~99% 범위 안 + 마할라노비스 거리(X 부분)가 학습 자료 99% 이내
Zx_tr = Z[:, ix]; mu_x = Zx_tr.mean(0); inv = np.linalg.inv(np.cov(Zx_tr.T))
md = lambda A: np.sqrt(np.einsum("ij,jk,ik->i", A - mu_x, inv, A - mu_x))
lim = np.quantile(md(Zx_tr), 0.99)
q1, q99 = np.quantile(Zx_tr, 0.01, axis=0), np.quantile(Zx_tr, 0.99, axis=0)
G["domain_dist"] = md(Zg[:, ix])
G["in_domain"] = (G.domain_dist <= lim) & ((Zg[:, ix] >= q1) & (Zg[:, ix] <= q99)).all(1)
# 예측값도 학습 자료의 Y 범위 안이어야 한다 (X가 범위 안이어도 조합이 새로우면 Y가 외삽될 수 있음)
ymin, ymax = tr[Y].min(), tr[Y].max()
G["y_in_range"] = (G["Voc_pred"] >= ymin) & (G["Voc_pred"] <= ymax)
G["in_domain"] = G["in_domain"] & G["y_in_range"]
print("적용 범위 안 생성 직물:", int(G.in_domain.sum()), "/", len(G), f"(Y 학습 범위 {ymin:.1f}~{ymax:.1f} V)")
G = G.rename(columns={Y: "Voc_sampled"})
G["is_mock"] = True; G["is_generated"] = True
save(G, "lab4_generated_candidates.csv")
print(G[["Voc_sampled", "Voc_pred", "pred_sd_z"]].describe().round(3).to_string())
