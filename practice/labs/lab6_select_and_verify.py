"""Lab 6 — 전향 검증: 생성 직물 중 실제로 만들 후보 고르기 → (측정 후) 예상과 비교
① 적용 범위 안에서 기대값 최고 3개 + 예상 범위가 가장 넓은 3개 (능동 학습), 비교용 함정 3개
② 예시 측정값: 실험실 측정 대신, 가장 닮은 모의 원단의 값에 측정 오차를 더해 채움
결과: outputs/lab6_verification_plan.csv, lab6_verification_result.csv"""
import numpy as np, pandas as pd, os
from common import load, save, X8, LogStd, OUT

G = pd.read_csv(os.path.join(OUT, "lab4_generated_candidates.csv"))
full = load("01_mock_full.csv")
# 함정 예시: 적용 범위 검사 없이 기대값만 보면 분포 꼬리(외삽)의 직물이 뽑힌다
trap = G.sort_values("Voc_pred", ascending=False).head(3).assign(reason="(함정) 범위 검사 없이 기대값 최고")
D = G[G.in_domain]
top = D.sort_values("Voc_pred", ascending=False).head(3).assign(reason="기대값 최고 (적용 범위 안)")
wide = D.drop(top.index).sort_values("pred_sd_z", ascending=False).head(3).assign(reason="예상 범위 최대 (모델이 가장 모름)")
plan = pd.concat([top, wide, trap])
t = LogStd().fit(full, X8); Zf, Zp = t.transform(full), t.transform(plan)
near = [int(np.argmin(((Zf - z) ** 2).sum(1))) for z in Zp]
plan["nearest_mock_fabric"] = full.iloc[near].fabric_id.values
plan["nearest_material"] = full.iloc[near].material.values; plan["nearest_structure"] = full.iloc[near].structure.values
plan["measured_Voc"] = ""                       # 실험실이 채울 칸
save(plan[["gen_id", "reason", "Voc_pred", "Voc_lo95", "Voc_hi95", "nearest_mock_fabric", "nearest_material", "nearest_structure", "measured_Voc"] + X8], "lab6_verification_plan.csv")
rng = np.random.default_rng(11)
res = plan.copy()
res["measured_Voc"] = full.iloc[near].Voc_V.values * np.exp(rng.normal(0, 0.12, len(res)))
res["inside_95"] = (res.measured_Voc >= res.Voc_lo95) & (res.measured_Voc <= res.Voc_hi95)
res["abs_err"] = (res.measured_Voc - res.Voc_pred).abs()
save(res[["gen_id", "reason", "Voc_pred", "Voc_lo95", "Voc_hi95", "measured_Voc", "inside_95", "abs_err"]], "lab6_verification_result.csv")
print(res[["gen_id", "reason", "Voc_pred", "measured_Voc", "inside_95"]].round(1).to_string(index=False))
ok = res[~res.reason.str.startswith("(함정)")]
print("적용 범위 안 후보의 범위 안 비율:", round(ok.inside_95.mean(), 2), " / 함정 후보:", round(res[res.reason.str.startswith("(함정)")].inside_95.mean(), 2))
print("→ 적용 범위 밖(외삽) 후보는 예상 범위조차 믿을 수 없다. 범위 안 비율이 낮으면 범위를 넓히거나 다시 학습")
