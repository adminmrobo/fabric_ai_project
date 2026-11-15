# 지식 그래프·참고문헌·페이지 서지 (페이지에 넣을 데이터 블록)
import json

PAGE = "hanyang_textile_ai_brief_01"
N = []
def node(id, type, ko, en, d=None, anchor="#top", level=None, family=None, conf="high", ev=None, src=None, status="known", alt=None):
    n = {"id": id, "type": type, "label": {"ko": ko, "en": en}, "page": PAGE, "anchor": anchor,
         "domain": ["ai", "stats"], "status": status, "confidence": conf}
    if d: n["definition"] = {"ko": d}
    if level: n["level"] = level
    if family: n["family"] = family
    if ev: n["evidence"] = ev
    if src: n["source"] = src
    if alt: n["altLabel"] = {"ko": alt}
    N.append(n)

# 개념·용어
node("lab:concept/fabric-hand", "Concept", "태 (Hand)", "fabric hand", "천을 손으로 만졌을 때의 느낌. 부드러움·뻣뻣함·매끄러움·따뜻함 등을 통틀어 이른다.", "#top", 1, "basics", alt=["촉감"])
node("lab:concept/triboelectricity", "Concept", "마찰전기", "triboelectricity", "두 물질이 닿았다 떨어질 때 전하가 한쪽으로 옮겨 가며 생기는 전기.", "#top", 1, "basics")
node("lab:concept/teng", "Concept", "TENG (마찰전기 나노발전기)", "triboelectric nanogenerator", "마찰전기를 모아 전기 신호로 쓰는 소자. 누르거나 문지르면 신호가 나와 배터리 없이 움직임을 감지한다.", "#why", 2, "systems")
node("lab:concept/structure-variables", "Concept", "구조 변수 (B·C)", "structure variables", "실 특성(B)과 제작 조건(C). 원인 쪽 변수.", "#lv3", 2, "basics")
node("lab:concept/fabric-properties", "Concept", "직물 물성 (A)", "fabric properties", "인장·굽힘·압축·표면·열 물성. 구조와 성능 사이의 중간 단계.", "#lv1", 2, "basics")
node("lab:concept/performance-target", "Concept", "성능 정답 (Y)", "performance target", "모델이 맞혀야 할 값. 마찰전기 출력(전압·전류·전하밀도) 또는 태 점수.", "#lv1", 2, "evaluation")
node("lab:term/mediator", "Term", "매개변수", "mediator", "원인이 결과에 닿기 전에 거치는 중간 변수. 이 연구에서는 직물 물성.", "#lv4", 3, "evaluation")
node("lab:method/kes-fb", "Method", "KES-FB (가와바타 평가 시스템)", "Kawabata Evaluation System for Fabrics", "인장·전단·굽힘·압축·표면 시험으로 직물의 태를 숫자로 재는 장비 체계.", "#lv2", 2, "evaluation", ev=["F07"], src=[{"cite": "Kawabata 1980"}])
node("lab:method/ftt", "Method", "FTT (촉감 측정기)", "Fabric Touch Tester", "한 번의 측정으로 굽힘·압축·표면·열을 재는 장비. 엑셀 열 이름으로 추정했다.", "#lv2", 2, "evaluation", conf="mid")
# 칸(사다리)
node("lab:method/data-audit", "Method", "데이터 진단", "data audit", "원단 × 측정 항목 지도를 그려 빈칸의 모양을 확인하는 일.", "#lv1", 1, "evaluation")
node("lab:method/pca", "Method", "주성분 분석 (PCA)", "principal component analysis", "서로 겹치는 정보를 묶어 많은 변수를 몇 개의 대표 축으로 줄이는 방법.", "#lv2", 2, "unsupervised")
node("lab:method/doe", "Method", "실험계획법 (DOE)", "design of experiments", "원인 후보의 수준을 미리 정해 고르게 조합해 실험하는 방법.", "#lv3", 2, "evaluation")
node("lab:method/baseline", "Method", "기준선 모델", "baseline model", "평균값으로 찍기나 선형 회귀처럼 단순한 모델. 복잡한 모델은 이것을 이겨야 의미가 있다.", "#lv4", 2, "evaluation")
node("lab:method/tree-ensemble", "Method", "랜덤포레스트·XGBoost", "tree ensembles", "작은 결정트리를 여러 개 모아 예측하는 모델. 표 데이터에 강하다.", "#lv4", 3, "ensemble")
node("lab:method/mlp", "Method", "신경망 (MLP)", "multilayer perceptron", "층을 쌓은 신경망. 데이터가 많거나 합성 데이터가 있을 때 쓴다.", "#lv4", 3, "basics")
node("lab:method/pls-sem", "Method", "PLS-SEM (경로 분석)", "partial least squares structural equation modeling", "구조 → 물성 → 성능 경로의 직접·간접 효과를 작은 표본에서 추정하는 방법.", "#lv4", 4, "evaluation")
node("lab:method/sim-to-real", "Method", "Sim-to-Real", "sim-to-real", "시뮬레이션 가상 데이터로 먼저 배우고 적은 실측 데이터로 보정하는 방법.", "#flow", 4, "systems")
node("lab:method/shap", "Method", "SHAP", "SHAP", "예측값 하나를 변수별 기여도로 나눠 보여 주는 해석 방법.", "#lv4", 3, "evaluation")
node("lab:method/group-cv", "Method", "원단 단위 교차검증", "grouped cross-validation", "같은 원단의 반복 측정을 한 묶음에 넣어 나누는 교차검증.", "#lv5", 3, "evaluation")
# 한계·문제
node("lab:limitation/no-target", "Limitation", "정답 데이터가 없음", "no target values", "마찰전기 출력·태 점수가 없어 예측 모델을 만들 수 없다.", "#lv1", 1)
node("lab:limitation/source-confound", "Limitation", "출처와 직물 종류가 겹침", "source-type confounding", "Huvis 원단이 대부분 부직포라 차이가 장비 때문인지 원단 때문인지 가를 수 없다.", "#lv2", 2)
node("lab:limitation/small-sample", "Limitation", "원단 수가 적음", "small sample", "원단을 다 모아도 100개 안팎이라 항목이 많으면 외우기 쉽다.", "#lv3", 2)
node("lab:problem/overfitting", "Problem", "과적합", "overfitting", "학습 데이터를 외워 학습 점수는 높지만 새 데이터에서는 틀리는 상태.", "#lv4", 2, "evaluation")
node("lab:problem/data-leakage", "Problem", "데이터 누수", "data leakage", "시험에 쓸 정보가 학습에 섞여 점수가 부풀려지는 일.", "#lv5", 3, "evaluation")
# 지표
node("lab:metric/r2", "Metric", "결정계수 (R²)", "coefficient of determination", "원단 사이 차이 중 모델이 설명한 몫. 1이 완벽.", "#lv4", 2, "evaluation")
node("lab:metric/rmse", "Metric", "RMSE", "root mean squared error", "평균적으로 빗나간 크기(원래 단위).", "#lv5", 2, "evaluation")
node("lab:metric/cv-repeat", "Metric", "변동계수 (CV)", "coefficient of variation", "반복 측정의 흔들림. 표준편차 ÷ 평균.", "#lv5", 2, "evaluation")
node("lab:metric/icc", "Metric", "급내상관계수 (ICC)", "intraclass correlation", "원단 사이 차이가 측정 오차보다 큰 정도.", "#lv5", 3, "evaluation")
# 주장 (출처 있음)
node("lab:claim/27-fabrics", "Claim", "원단 27개 × 측정 항목 73개", "27 fabrics × 73 measured items", "엑셀에는 원단 27개와 측정 항목 73개가 있다.", "#lv1", ev=["F01"], src=[{"cite": "AI 데이터셋 엑셀", "loc": "시트 Physical_Structural 외 3"}])
node("lab:claim/19-common", "Claim", "공통 항목 19개", "19 items common to all fabrics", "27개 원단 모두에 값이 있는 항목은 19개다.", "#lv1", ev=["F02"], src=[{"cite": "AI 데이터셋 엑셀", "loc": "직접 집계"}])
node("lab:claim/pca-68", "Claim", "두 축이 정보의 68%", "two PCs explain 68%", "공통 19항목 PCA에서 PC1 39%, PC2 29%.", "#lv2", ev=["F03"], src=[{"cite": "AI 데이터셋 엑셀", "loc": "로그·표준화 후 PCA"}])
node("lab:claim/ftt-kes-cw", "Claim", "두 장비는 압축 일만 뚜렷이 일치", "FTT and KES agree only on compression work", "산업 원단 14개에서 CW↔WC 순위 상관 0.72(p = 0.003), 나머지 네 쌍은 0.09~0.34.", "#lv2", conf="mid", ev=["F04"], src=[{"cite": "AI 데이터셋 엑셀", "loc": "산업 원단 14개, 스피어만"}])
node("lab:claim/iso139", "Claim", "표준 상태 20 ± 2 °C, 65 ± 4 %", "ISO 139 standard atmosphere", "섬유 시험의 표준 상태는 온도 20 °C, 상대습도 65 %, 허용 범위 ±2 °C, ±4 %.", "#lv3", ev=["F05"], src=[{"cite": "ISO 139:2005/Amd 1:2011", "loc": "3.1, 3.3"}])
node("lab:claim/kickoff-sample", "Claim", "목표 원단 50~100개", "target 50–100 fabrics", "킥오프 문서는 최소 50~100 샘플, 변수당 5~10개 규칙을 제시했다.", "#lv3", ev=["F06"], src=[{"cite": "Kick off 2025-12-11", "loc": "2-2-2, 3"}])
node("lab:claim/grant-plan", "Claim", "5년 과제 연차 목표", "five-year plan", "1차년도 구조·물성 DB와 기초 모델, 2차년도 마찰전기 성능 예측.", "#plan", ev=["F08"], src=[{"cite": "연구계획서 2026", "loc": "2-2) 연구과제의 내용"}])
node("lab:claim/kes-hand", "Claim", "KES-FB는 태를 기계로 잰다", "KES-FB measures hand objectively", "가와바타 위원회가 기계 측정으로 태를 평가하는 체계를 정리했다.", "#lv2", ev=["F07"], src=[{"cite": "Kawabata 1980"}])
# 질문
node("lab:question/core", "Question", "구조만으로 성능을 맞힐 수 있을까", "can structure predict performance", "실을 고르고 조직을 정하는 순간 마찰전기와 촉감을 미리 알 수 있을까?", "#top", status="known", conf="mid")
node("lab:question/target-plan", "Question", "정답 측정 계획", "target measurement plan", "마찰전기를 어떤 장치·모드·상대 물질로 언제부터 측정하나?", "#ask", conf="mid")
node("lab:question/column-suffix", "Question", "열 이름 _1·_2·_3의 뜻", "column suffix meaning", "_1이 FTT, _2가 KES-FB, _3이 일반 시험인지 확인 필요.", "#ask", conf="low")
node("lab:question/instrument", "Question", "어느 장비로 통일할까", "which instrument", "새 원단을 FTT와 KES-FB 중 어느 장비로 통일해 측정할까?", "#ask", conf="mid")
# 비유
node("lab:analogy/fridge", "Analogy", "냉장고 재료 확인", "checking the fridge", "요리 전에 재료부터 확인하는 일.", "#lv1")
node("lab:analogy/three-classes", "Analogy", "세 반의 다른 시험 과목", "three classes, different exams", "함께 본 과목으로만 성적을 비교할 수 있다.", "#lv1")
node("lab:analogy/shadow", "Analogy", "손전등 그림자", "flashlight shadow", "입체를 그림자로 짐작한다.", "#lv2")
node("lab:analogy/ramen", "Analogy", "라면 비결 실험", "ramen experiment", "재료를 하나씩만 바꿔 본다.", "#lv3")
node("lab:analogy/memorize", "Analogy", "기출문제 외우기", "memorizing past exams", "외운 학생은 새 문제에서 떨어진다.", "#lv4")
node("lab:analogy/same-exam", "Analogy", "같은 시험지 두 번", "same exam twice", "두 번째 점수는 기억이다.", "#lv5")
# 시뮬레이션
for sid, ko, en, a in [("coverage-map", "채움 지도", "coverage map", "#lv1"), ("pca-map", "PCA 닮음 지도", "PCA map", "#lv2"),
                       ("doe-calc", "원단 수 계산기", "DOE calculator", "#lv3"), ("overfit-lab", "과적합 실험실", "overfitting lab", "#lv4"),
                       ("leak-lab", "나누는 방식 실험", "split experiment", "#lv5"), ("gauge", "합격선 계기판", "pass gauge", "#lv5"),
                       ("flowchart", "연구 흐름도", "research flowchart", "#flow")]:
    node("lab:simulation/" + sid, "Simulation", ko, en, None, a)
# 문헌
for wid, ko, en in [("kickoff2025", "Kick off 문서 (2025-12-11)", "Kick-off document"), ("grant2026", "연구계획서 (2026 핵심연구 유형B)", "2026 research proposal"),
                    ("aidataset2026", "AI 데이터셋 엑셀", "AI dataset workbook"), ("iso1392005", "ISO 139:2005/Amd 1:2011", "ISO 139"),
                    ("kawabata1980standardization", "Kawabata (1980)", "Kawabata 1980"), ("handcourse2026", "강의 「직물 태 판정 AI 만들기」", "fabric hand AI course")]:
    node("lab:work/" + wid, "Work", ko, en, None, "#export")

E = []
def edge(s, p, o, anchor, ev=None, conf="high"):
    e = {"s": s, "p": p, "o": o, "anchor": anchor, "confidence": conf}
    if ev: e["evidence"] = ev
    E.append(e)

L = ["lab:method/data-audit", "lab:method/pca", "lab:method/doe", "lab:method/baseline", "lab:method/group-cv"]
for a, b in zip(L, L[1:]): edge(a, "lab:prerequisiteOf", b, "#flow")
lim = [("lab:method/data-audit", "lab:limitation/no-target", "lab:method/pca", "#lv1"),
       ("lab:method/pca", "lab:limitation/source-confound", "lab:method/doe", "#lv2"),
       ("lab:method/doe", "lab:limitation/small-sample", "lab:method/baseline", "#lv3"),
       ("lab:method/baseline", "lab:problem/overfitting", "lab:method/group-cv", "#lv4")]
for m, l, nx, a in lim:
    edge(m, "lab:hasLimitation", l, a); edge(l, "lab:addressedBy", nx, a)
edge("lab:method/group-cv", "lab:hasLimitation", "lab:problem/data-leakage", "#lv5")
edge("lab:problem/data-leakage", "lab:addressedBy", "lab:method/group-cv", "#lv5")
edge("lab:limitation/no-target", "lab:raises", "lab:question/target-plan", "#lv1")
edge("lab:limitation/source-confound", "lab:raises", "lab:question/instrument", "#lv2")
edge("lab:method/ftt", "lab:raises", "lab:question/column-suffix", "#lv1", conf="mid")
edge("lab:concept/performance-target", "lab:raises", "lab:question/core", "#top")
edge("lab:concept/structure-variables", "lab:prerequisiteOf", "lab:concept/fabric-properties", "#lv3")
edge("lab:concept/fabric-properties", "lab:prerequisiteOf", "lab:concept/performance-target", "#lv1")
edge("lab:term/mediator", "lab:broader", "lab:concept/fabric-properties", "#lv4")
edge("lab:concept/teng", "lab:partOf", "lab:concept/triboelectricity", "#why")
edge("lab:concept/triboelectricity", "lab:measuredBy", "lab:concept/performance-target", "#lv1")
edge("lab:concept/fabric-hand", "lab:measuredBy", "lab:method/kes-fb", "#lv2")
edge("lab:method/kes-fb", "lab:contrastsWith", "lab:method/ftt", "#lv2")
edge("lab:method/ftt", "lab:solves", "lab:concept/fabric-properties", "#lv1", conf="mid")
edge("lab:method/kes-fb", "lab:solves", "lab:concept/fabric-properties", "#lv1")
edge("lab:method/baseline", "lab:prerequisiteOf", "lab:method/tree-ensemble", "#lv4")
edge("lab:method/tree-ensemble", "lab:prerequisiteOf", "lab:method/mlp", "#lv4")
edge("lab:limitation/small-sample", "lab:addressedBy", "lab:method/sim-to-real", "#flow")
edge("lab:method/pls-sem", "lab:solves", "lab:term/mediator", "#lv4")
edge("lab:method/shap", "lab:solves", "lab:method/tree-ensemble", "#lv4", conf="mid")
for m in ["lab:method/baseline", "lab:method/tree-ensemble", "lab:method/mlp"]:
    edge(m, "lab:evaluatedBy", "lab:metric/r2", "#lv5")
edge("lab:method/group-cv", "lab:evaluatedBy", "lab:metric/rmse", "#lv5")
edge("lab:method/doe", "lab:evaluatedBy", "lab:metric/cv-repeat", "#lv3")
edge("lab:method/doe", "lab:evaluatedBy", "lab:metric/icc", "#lv5")
edge("lab:metric/rmse", "lab:derivedFrom", "lab:metric/r2", "#lv5")
edge("lab:problem/overfitting", "lab:evaluatedBy", "lab:metric/r2", "#lv4")
# 주장
for c, t, w, a, f in [("lab:claim/27-fabrics", "lab:method/data-audit", "aidataset2026", "#lv1", "F01"),
                      ("lab:claim/19-common", "lab:method/data-audit", "aidataset2026", "#lv1", "F02"),
                      ("lab:claim/pca-68", "lab:method/pca", "aidataset2026", "#lv2", "F03"),
                      ("lab:claim/ftt-kes-cw", "lab:question/instrument", "aidataset2026", "#lv2", "F04"),
                      ("lab:claim/iso139", "lab:method/doe", "iso1392005", "#lv3", "F05"),
                      ("lab:claim/kickoff-sample", "lab:method/doe", "kickoff2025", "#lv3", "F06"),
                      ("lab:claim/kes-hand", "lab:method/kes-fb", "kawabata1980standardization", "#lv2", "F07"),
                      ("lab:claim/grant-plan", "lab:method/sim-to-real", "grant2026", "#plan", "F08")]:
    edge(c, "lab:supports", t, a, [f]); edge(c, "lab:assertedIn", "lab:work/" + w, a, [f])
edge("lab:work/handcourse2026", "lab:explainedIn", "lab:concept/fabric-hand", "#top", conf="mid")
edge("lab:method/data-audit", "lab:assertedIn", "lab:work/aidataset2026", "#lv1")
# 비유
for an, t in [("fridge", "lab:method/data-audit"), ("three-classes", "lab:limitation/source-confound"), ("shadow", "lab:method/pca"),
              ("ramen", "lab:method/doe"), ("memorize", "lab:problem/overfitting"), ("same-exam", "lab:problem/data-leakage")]:
    edge("lab:analogy/" + an, "lab:analogyOf", t, next(n["anchor"] for n in N if n["id"] == "lab:analogy/" + an))
# 시뮬레이션
for t, sm in [("lab:method/data-audit", "coverage-map"), ("lab:method/pca", "pca-map"), ("lab:method/doe", "doe-calc"),
              ("lab:problem/overfitting", "overfit-lab"), ("lab:problem/data-leakage", "leak-lab"), ("lab:metric/r2", "gauge"),
              ("lab:method/sim-to-real", "flowchart")]:
    edge(t, "lab:demonstratedBy", "lab:simulation/" + sm, next(n["anchor"] for n in N if n["id"] == "lab:simulation/" + sm))

# 점검
ids = {n["id"] for n in N}
for e in E:
    assert e["s"] in ids and e["o"] in ids, e
deg = {i: 0 for i in ids}
for e in E: deg[e["s"]] += 1; deg[e["o"]] += 1
iso = [i for i, d in deg.items() if d == 0]
assert not iso, iso
KG = {"version": "1.0", "page": PAGE, "nodes": N, "edges": E}

REFS = [
 {"id": "kickoff2025", "type": "report", "title": "Kick off : 2025.12.11 — 섬유-직물-마찰전기 통합 예측 모델 연구 목적과 방법", "issued": {"date-parts": [[2025, 12, 11]]},
  "lab": {"work": "lab:work/kickoff2025", "role": "primary", "supports": ["lab:claim/kickoff-sample"], "locs": [{"claim": "lab:claim/kickoff-sample", "loc": "2-2-2, 3장"}],
          "verified": {"title": True, "authors": False, "year": True, "venue": False, "doi": False, "pages": False}, "checkedBy": "제공 자료 2026-11-14", "note": "내부 문서, 작성자 표기 없음"}},
 {"id": "grant2026", "type": "report", "title": "직물 구조–물성의 Sim-to-Real AI 학습을 통한 의복형 웨어러블 직물센서 온디바이스 플랫폼 (2026년도 핵심연구(유형B) 신규과제 연구계획서)", "issued": {"date-parts": [[2026]]},
  "lab": {"work": "lab:work/grant2026", "role": "primary", "supports": ["lab:claim/grant-plan"], "locs": [{"claim": "lab:claim/grant-plan", "loc": "2-2) 연구과제의 내용"}],
          "verified": {"title": True, "authors": False, "year": True, "venue": False, "doi": False, "pages": False}, "checkedBy": "제공 자료 2026-11-14", "note": "연구책임자 이름은 자료에 없음"}},
 {"id": "aidataset2026", "type": "dataset", "title": "AI 데이터셋 (Yarn_Descriptors · Physical_Structural · Surface_Friction · Mechanical · Thermal_Transport)",
  "lab": {"work": "lab:work/aidataset2026", "role": "data", "supports": ["lab:claim/27-fabrics", "lab:claim/19-common", "lab:claim/pca-68", "lab:claim/ftt-kes-cw"],
          "locs": [{"claim": "lab:claim/19-common", "loc": "직접 집계"}, {"claim": "lab:claim/ftt-kes-cw", "loc": "산업 원단 14개"}],
          "verified": {"title": True, "authors": False, "year": False, "venue": False, "doi": False, "pages": False}, "checkedBy": "직접 계산 2026-11-14", "note": "만든 날짜·작성자 확인 필요"}},
 {"id": "iso1392005", "type": "report", "title": "Textiles — Standard atmospheres for conditioning and testing (ISO 139:2005, Amendment 1:2011)", "author": [{"literal": "ISO"}],
  "issued": {"date-parts": [[2005]]}, "URL": "https://standards.iteh.ai/catalog/standards/iso/f70fad6d-df27-498d-9fee-e548484a50e4/iso-139-2005-amd-1-2011", "accessed": {"date-parts": [[2026, 11, 14]]},
  "lab": {"work": "lab:work/iso1392005", "role": "background", "supports": ["lab:claim/iso139"], "locs": [{"claim": "lab:claim/iso139", "loc": "3.1, 3.3"}],
          "verified": {"title": True, "authors": True, "year": True, "venue": True, "doi": False, "pages": False}, "checkedBy": "웹 검색 2026-11-14", "note": "개정판 미리보기로 확인"}},
 {"id": "kawabata1980standardization", "type": "book", "title": "The Standardization and Analysis of Hand Evaluation", "edition": "2", "author": [{"family": "Kawabata", "given": "Sueo"}],
  "issued": {"date-parts": [[1980]]}, "publisher": "The Hand Evaluation and Standardization Committee, The Textile Machinery Society of Japan",
  "lab": {"work": "lab:work/kawabata1980standardization", "role": "background", "supports": ["lab:claim/kes-hand"], "locs": [],
          "verified": {"title": True, "authors": True, "year": True, "venue": True, "doi": False, "pages": False}, "checkedBy": "웹 검색 2026-11-14", "note": ""}},
 {"id": "handcourse2026", "type": "report", "title": "직물 태(Hand) 판정 AI 만들기 — Teachable Machine으로 배우는 이미지 → 숫자 → 학습 → 판단", "issued": {"date-parts": [[2026]]},
  "lab": {"work": "lab:work/handcourse2026", "role": "background", "supports": ["lab:concept/fabric-hand"], "locs": [],
          "verified": {"title": True, "authors": False, "year": True, "venue": False, "doi": False, "pages": False}, "checkedBy": "제공 자료 2026-11-14", "note": "강의 슬라이드 60쪽"}},
]
META = {"title": "직물 구조로 성능을 미리 맞히는 AI — 배 교수님 연구 계획 브리핑", "series": "한양대 섬유 AI 과제 브리핑", "number": "01",
        "creator": [{"name": "안상선", "role": "author", "affiliation": "(주)M-Robo 대표"}], "contributor": [{"name": "AI 보조 제작", "role": "assistant"}],
        "date": "2026-11-14", "version": "1.0", "language": ["ko"], "license": "", "url": "",
        "about": ["lab:method/data-audit", "lab:method/pca", "lab:method/doe", "lab:method/baseline", "lab:method/group-cv", "lab:concept/triboelectricity"],
        "educationalLevel": "입문~중급", "learningResourceType": "interactive explainer", "basedOn": ["kickoff2025", "grant2026", "aidataset2026"],
        "suggestedCitation": "안상선 (2026). 직물 구조로 성능을 미리 맞히는 AI — 배 교수님 연구 계획 브리핑. 한양대 섬유 AI 과제 브리핑 01, v1.0."}

CTX = {"skos": "http://www.w3.org/2004/02/skos/core#", "schema": "https://schema.org/", "dct": "http://purl.org/dc/terms/",
       "prov": "http://www.w3.org/ns/prov#", "lab": "urn:lab:"}
TMAP = {"Concept": "skos:Concept", "Term": "skos:Concept", "Method": "schema:DefinedTerm", "Problem": "skos:Concept", "Limitation": "skos:Concept",
        "Metric": "schema:DefinedTerm", "Claim": "schema:Claim", "Question": "schema:Question", "Analogy": "skos:Concept", "Simulation": "schema:SoftwareSourceCode", "Work": "schema:CreativeWork"}
def jsonld(kg):
    g = []
    for n in kg["nodes"]:
        o = {"@id": n["id"], "@type": [TMAP.get(n["type"], "skos:Concept"), "lab:" + n["type"]],
             "skos:prefLabel": [{"@value": n["label"]["ko"], "@language": "ko"}, {"@value": n["label"]["en"], "@language": "en"}]}
        if n.get("definition"): o["skos:definition"] = {"@value": n["definition"]["ko"], "@language": "ko"}
        g.append(o)
    for e in kg["edges"]:
        g.append({"@id": "lab:edge/" + e["s"].split("/")[-1] + "--" + e["p"].split(":")[-1] + "--" + e["o"].split("/")[-1],
                  "@type": "rdf:Statement", "rdf:subject": {"@id": e["s"]}, "rdf:predicate": {"@id": e["p"]}, "rdf:object": {"@id": e["o"]}})
    c = dict(CTX); c["rdf"] = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    return {"@context": c, "@graph": g}

if __name__ == "__main__":
    print(len(N), "nodes", len(E), "edges", sum(1 for e in E if e["p"] == "lab:relatedTo"), "relatedTo")
