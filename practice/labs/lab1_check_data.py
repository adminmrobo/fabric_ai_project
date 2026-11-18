"""Lab 1 — 자료 점검 (품질 검사): 열·결측·범위·반복 측정 흔들림·모의 표시
실행: python lab1_check_data.py [파일명=02_train.csv]
결과: outputs/lab1_qc_report.csv  (검사 항목별 통과/경고)"""
import sys, numpy as np, pandas as pd
from common import load, save, X19, Y

f = sys.argv[1] if len(sys.argv) > 1 else "02_train.csv"
df = load(f)
rep = []
def add(check, target, value, rule, ok):
    rep.append(dict(check=check, target=target, value=value, rule=rule, result="통과" if ok else "경고"))

miss = [c for c in X19 + [Y] if c not in df.columns]
add("필수 열", "19항목+Voc_V", len(miss), "빠진 열 0개", len(miss) == 0)
for c in X19 + [Y]:
    n = int(df[c].isna().sum()); add("결측", c, n, "결측 0개", n == 0)
    nonpos = int((df[c] <= 0).sum()); add("양수", c, nonpos, "0 이하 값 0개 (로그 변환 전제)", nonpos == 0)
    z = (np.log(df[c]) - np.log(df[c]).mean()) / np.log(df[c]).std()
    out = int((z.abs() > 4).sum()); add("튀는 값", c, out, "로그 z 점수 |z|>4 인 원단 0개", out == 0)
# 범위 (실제 직물 범위, 실측 연결 후 조정)
add("범위", "W", f"{df.W.min():.0f}~{df.W.max():.0f}", "30~400 g/m²", df.W.between(30, 400).all())
add("범위", "CRR_F", f"{df.CRR_F.min():.0f}~{df.CRR_F.max():.0f}", "0~100 %", df.CRR_F.between(0, 100).all())
if "Voc_cv" in df:
    m = df.Voc_cv.median(); add("반복 흔들림", "Voc_cv", round(m, 3), "중앙값 0.15 이하, 0.15 초과 원단은 재측정", m <= 0.15)
    add("재측정 대상", "Voc_cv>0.15", int((df.Voc_cv > 0.15).sum()), "목록을 outputs/lab1_remeasure.csv로", True)
    save(df[df.Voc_cv > 0.15][["fabric_id", "material", "structure", "Voc_V", "Voc_cv"]], "lab1_remeasure.csv")
if "is_mock" in df:
    add("모의 표시", "is_mock", int(df.is_mock.sum()), "모의 행은 실측 성적 계산에서 제외", True)
dup = int(df.fabric_id.duplicated().sum()); add("중복", "fabric_id", dup, "중복 0개", dup == 0)
r = pd.DataFrame(rep)
save(r, "lab1_qc_report.csv")
print(r.result.value_counts().to_string())
