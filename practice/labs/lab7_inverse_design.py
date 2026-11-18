"""Lab 7 — 역방향: 원하는 Voc*에서 직물 특성 분포 p(X | Y = Voc*) → 후보와 닮은 실측(모의) 원단
결과: outputs/lab7_inverse_candidates.csv"""
import numpy as np, pandas as pd, sys
from sklearn.mixture import GaussianMixture
from common import load, save, X8, Y, LogStd

target = float(sys.argv[1]) if len(sys.argv) > 1 else 90.0   # 목표 Voc (V)
tr, full = load("02_train.csv"), load("01_mock_full.csv")
cols = X8 + [Y]; t = LogStd().fit(tr, cols); Z = t.transform(tr)
g = GaussianMixture(4, covariance_type="full", random_state=0, n_init=5).fit(Z)
yz = (np.log(target) - t.mu[-1]) / t.sd[-1]
rng = np.random.default_rng(3); out = []
w = np.array([g.weights_[k] * np.exp(-0.5 * (yz - g.means_[k][-1]) ** 2 / g.covariances_[k][-1, -1]) / np.sqrt(g.covariances_[k][-1, -1]) for k in range(g.n_components)]); w /= w.sum()
for i in range(40):
    k = rng.choice(len(w), p=w); m, S = g.means_[k], g.covariances_[k]
    Sxy, Syy = S[:-1, -1], S[-1, -1]
    mu = m[:-1] + Sxy / Syy * (yz - m[-1]); C = S[:-1, :-1] - np.outer(Sxy, Sxy) / Syy
    out.append(np.append(rng.multivariate_normal(mu, C), yz))
X = t.inverse(np.array(out)); X.insert(0, "cand_id", [f"I{i+1:03d}" for i in range(len(X))])
Zf = LogStd().fit(full, X8); zf, zc = Zf.transform(full), Zf.transform(X)
nn = [int(np.argmin(((zf - z) ** 2).sum(1))) for z in zc]
X["nearest_fabric"] = full.iloc[nn].fabric_id.values; X["nearest_material"] = full.iloc[nn].material.values
X["nearest_structure"] = full.iloc[nn].structure.values; X["nearest_Voc"] = full.iloc[nn].Voc_V.values
save(X, "lab7_inverse_candidates.csv")
print(f"목표 Voc* = {target} V 일 때 예상 무리 비중:", np.round(w, 2))
print(X.groupby(["nearest_material", "nearest_structure"]).size().sort_values(ascending=False).head(5).to_string())
