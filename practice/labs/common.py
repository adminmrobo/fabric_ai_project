"""실습 공통 도구 — 경로, 열 목록, 표준화, 가우시안 혼합 조건부 계산."""
import os, numpy as np, pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "outputs")
os.makedirs(OUT, exist_ok=True)

# 실측 엑셀의 27개 원단 모두에 있는 공통 19항목과 같은 이름
X19 = ["W", "SFC_F", "SFC_B", "SRA_F", "SRA_B", "SRW_F", "SRW_B", "BAR_F", "BAR_B",
       "BW_FL", "BW_FC", "BW_BL", "BW_BC", "CW_F", "CW_B", "CRR_F", "CRR_B", "Qmax_F", "Qmax_B"]
Y = "Voc_V"                      # 주 전기 특성 (연속변수)
# 생성 모델에 넣는 핵심 8항목 (원단 수가 적을 때 차원을 줄이는 기본안)
X8 = ["W", "SFC_F", "SRA_F", "SRW_F", "BAR_F", "CW_F", "CRR_F", "Qmax_F"]
POSITIVE = X19 + [Y]             # 모두 양수 → 로그 변환해 치우침을 줄인다


def load(name):
    return pd.read_csv(os.path.join(DATA, name))


def save(df, name):
    p = os.path.join(OUT, name)
    df.to_csv(p, index=False, encoding="utf-8-sig", float_format="%.5g")
    print("  저장:", os.path.relpath(p, ROOT), f"({len(df)}행)")
    return p


class LogStd:
    """양수 열 로그 변환 + 표준화. fit은 학습 자료로만 한다(누수 방지)."""
    def fit(self, df, cols):
        self.cols = cols
        z = np.log(df[cols].values)
        self.mu, self.sd = z.mean(0), z.std(0, ddof=1)
        return self
    def transform(self, df):
        return (np.log(df[self.cols].values) - self.mu) / self.sd
    def inverse(self, Z):
        return pd.DataFrame(np.exp(Z * self.sd + self.mu), columns=self.cols)


def gmm_conditional(gmm, Zx, ix, iy):
    """가우시안 혼합 p(x, y)에서 p(y | x)의 평균과 표준편차 (y는 1차원).
    ix: 조건 열 위치 목록, iy: 목표 열 위치"""
    n = Zx.shape[0]
    K = gmm.n_components
    logw = np.zeros((n, K)); mu = np.zeros((n, K)); var = np.zeros(K)
    for k in range(K):
        m, S = gmm.means_[k], gmm.covariances_[k]
        Sxx = S[np.ix_(ix, ix)]; Syx = S[iy, ix]; Syy = S[iy, iy]
        inv = np.linalg.inv(Sxx)
        d = Zx - m[ix]
        logw[:, k] = np.log(gmm.weights_[k]) - 0.5 * np.einsum("ij,jk,ik->i", d, inv, d) - 0.5 * np.linalg.slogdet(Sxx)[1]
        mu[:, k] = m[iy] + d @ (inv @ Syx)
        var[k] = Syy - Syx @ inv @ Syx
    w = np.exp(logw - logw.max(1, keepdims=True)); w /= w.sum(1, keepdims=True)
    mean = (w * mu).sum(1)
    v = (w * (var + mu ** 2)).sum(1) - mean ** 2
    return mean, np.sqrt(np.maximum(v, 1e-12)), w
