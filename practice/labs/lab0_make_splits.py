"""Lab 0 — 실습용 자료 나누기 (강사가 한 번 실행, 결과는 data/에 이미 있음)
- 학습 80% / 시험 20%: 원단 단위 무작위
- 새 조합 시험: '울 × 호프색' 칸 전체를 빼 두어, 본 적 없는 조합 예측을 시험"""
import numpy as np, pandas as pd
from common import load, DATA
import os
df = load("01_mock_full.csv")
new = df[(df.material == "wool") & (df.structure == "hopsack22")]
rest = df.drop(new.index)
rng = np.random.default_rng(7)
te = rest.sample(frac=0.2, random_state=7)
tr = rest.drop(te.index)
for d, n in [(tr, "02_train.csv"), (te, "02_test.csv"), (new, "02_test_new_combo.csv")]:
    d.to_csv(os.path.join(DATA, n), index=False, encoding="utf-8-sig", float_format="%.5g")
    print(n, len(d))
