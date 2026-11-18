"""Lab 2 — 탐색: 로그·표준화 → 주성분 분석(PCA) → 적재값(가중치)과 점수
PC = Z · W   (원단 n × 19) · (19 × k)
결과: outputs/lab2_pca_loadings.csv, lab2_pca_scores.csv, lab2_pca.png"""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from common import load, save, X19, LogStd, OUT
from matplotlib import font_manager as _fm
_have = {f.name for f in _fm.fontManager.ttflist}
for _f in ["Malgun Gothic", "AppleGothic", "Apple SD Gothic Neo", "NanumGothic", "Noto Sans KR", "Noto Sans CJK KR", "Noto Sans CJK JP"]:
    if _f in _have:
        plt.rcParams["font.family"] = _f; break
else:
    print("주의: 한글 글꼴을 찾지 못해 그림의 한글이 네모로 보일 수 있습니다 (Windows: 맑은 고딕, macOS: AppleGothic)")
plt.rcParams["axes.unicode_minus"] = False
df = load("02_train.csv")
t = LogStd().fit(df, X19); Z = t.transform(df)
U, s, Vt = np.linalg.svd(Z, full_matrices=False)
ev = s ** 2 / (s ** 2).sum()
W = Vt[:3].T                                   # 19 × 3 가중치 행렬 (열 길이 1, 서로 직교)
P = Z @ W                                      # 점수 = 내적
print("설명 비율 PC1~3:", np.round(ev[:3], 3))
print("W 열 길이:", np.round((W ** 2).sum(0), 3), " PC1·PC2 내적:", round(float(W[:, 0] @ W[:, 1]), 6))
L = pd.DataFrame(W, columns=["PC1", "PC2", "PC3"]); L.insert(0, "item", X19)
save(L, "lab2_pca_loadings.csv")
S = df[["fabric_id", "material", "structure"]].copy(); S[["PC1", "PC2", "PC3"]] = P[:, :3]
save(S, "lab2_pca_scores.csv")
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
for k, g in S.groupby("structure"):
    ax[0].scatter(g.PC1, g.PC2, s=12, label=k)
ax[0].set_xlabel(f"PC1 ({ev[0]:.0%})"); ax[0].set_ylabel(f"PC2 ({ev[1]:.0%})"); ax[0].legend(); ax[0].set_title("원단 점수 (구조별 색)")
o = np.argsort(-np.abs(W[:, 0]))
ax[1].barh([X19[i] for i in o][::-1], W[o, 0][::-1]); ax[1].set_title("PC1 가중치 (적재값)")
plt.tight_layout(); plt.savefig(f"{OUT}/lab2_pca.png", dpi=110); print("  그림: outputs/lab2_pca.png")
