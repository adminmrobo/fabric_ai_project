# 실습 키트 — 모의 직물 데이터로 생성·검증·전향 검증까지

섬유직물 1차년도 방법 정의를 실습합니다.

> 실측 직물 데이터의 패턴(결합분포)을 학습하는 생성 모델로 새 직물을 만들고, 그 직물의 전기적 특성을 연속값(회귀형 출력)으로 예측한다.

실측 전기 특성이 모이기 전이므로 **모의 데이터**(`is_mock = True`)로 연습합니다. 여기서 얻는 숫자는 생성기에 넣은 가정을 되찾는 것일 뿐 연구 결과가 아닙니다. 실측이 들어오면 같은 스크립트에 실측 CSV만 바꿔 넣습니다.

## 0. 준비 (10분)

```bash
cd practice
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd labs
```

Python 3.10 이상. 각 Lab은 `practice/outputs/`에 결과 CSV를 씁니다. `practice/data/`에는 같은 결과의 **예시 파일**이 미리 들어 있어, 실행하지 않고도 결과 모양을 볼 수 있습니다.

## 1. 자료 (`data/`)

| 파일 | 내용 | 쓰는 Lab |
|---|---|---|
| `00_measurement_template.csv` | 실측 기록 양식(52열) + 예시 3행 — 실험실이 이 양식으로 기록 | 실측 |
| `00_column_dictionary.csv` | 열 이름·뜻·단위·필수 여부 | 실측 |
| `01_mock_full.csv` | 모의 원단 500개 (소재 5 × 구조 5 × 20, 막힘 한계 넘는 조합 제외) | 6, 7 |
| `02_train.csv` | 학습용 384개 (원단 단위 무작위 80%) | 1~5, 7 |
| `02_test.csv` | 시험용 96개 (20%) — 성적은 여기서만 | 3, 5 |
| `02_test_new_combo.csv` | 새 조합 시험 20개 — 울 × 호프색 칸 전체를 학습에서 뺌 | 3 |
| `03_qc_report_example.csv` | Lab 1 결과 예시 | — |
| `04_generated_candidates_example.csv` | Lab 4 결과 예시 — 새 직물 1000개, 예측 Voc와 95% 범위, 적용 범위 표시 | — |
| `05_*_example.csv` | Lab 3·5 결과 예시 — 기준선 성적, 분포 비교(KS), TSTR | — |
| `06_verification_plan_example.csv` | Lab 6 — 실제로 만들 후보와 측정 칸 | — |
| `07_verification_result_example.csv` | Lab 6 — 측정 후 예상 범위 안/밖 판정 | — |
| `08_inverse_candidates_example.csv` | Lab 7 — 목표 Voc에서 거꾸로 예상한 직물 후보 | — |
| `09_learning_curve_example.csv` | Lab 8 — 원단 수별 시험 R² | — |

모의 데이터를 다시 만들려면: `python ../../analysis/mock_data/generate_mock_fabric.py 20 20261118 ../data` 뒤 `python lab0_make_splits.py`.

## 2. 실습 순서

| Lab | 명령 | 배우는 것 | 확인할 숫자 (기본 설정) |
|---|---|---|---|
| 1 자료 점검 | `python lab1_check_data.py` | 열·결측·양수·튀는 값·범위·반복 흔들림·중복 | 통과 66 · 경고 1 (CW_B 튀는 값 2개), 재측정 목록 78개(Voc CV > 0.15) → `lab1_remeasure.csv` |
| 2 탐색 PCA | `python lab2_explore_pca.py` | 로그·표준화 → PC = Z·W, 가중치(적재값)와 점수 | PC1·PC2 설명 비율, W 열 길이 1·내적 0 |
| 3 비교 기준 | `python lab3_baseline_regression.py` | 지도 회귀(평균·릿지·랜덤포레스트·가우시안 과정), 5겹 교차검증, 새 조합 시험 | 가우시안 과정 시험 R² ≈ 0.94, 새 조합 RMSE ≈ 10 V |
| 4 생성 모델 | `python lab4_generative_model.py` | 가우시안 혼합으로 p(X, Y) 학습, BIC로 무리 수, 새 직물 1000개, 조건부 평균·범위, 적용 범위 | 무리 4개, 적용 범위 안 837/1000 |
| 5 생성 검증 | `python lab5_validate_generated.py` | 열별 KS, 상관 차이, TSTR vs TRTR | KS 모두 < 0.1, TSTR R² 0.82 < TRTR 0.91 |
| 6 전향 검증 | `python lab6_select_and_verify.py` | 후보 고르기(기대값 최고 + 범위 최대), 측정 후 판정, 외삽 함정 | 적용 범위 안 후보 6개 중 4개 ✓ (0.67), 함정 3개 모두 ✗ |
| 7 역방향 | `python lab7_inverse_design.py 90` | 목표 Voc*에서 p(X | Y=Voc*)로 직물 후보, 닮은 원단 | 90 V → 나일론·울의 호프색·능직·저지 쪽 |
| 8 원단 수 | `python lab8_how_many_fabrics.py` | 학습 원단 수를 늘리며 시험 R² (학습 곡선) — 실측 원단 수 결정 | GP: 40개 0.64±0.21, 100개 0.82±0.11, 250개 0.93 |

## 3. Lab마다 꼭 지킬 규칙

1. **변환 기준은 학습 자료로만 정한다.** `LogStd().fit(train)` 뒤 시험 자료는 `transform`만. 시험 자료가 평균·표준편차 계산에 들어가면 누수입니다.
2. **성적은 실측(여기서는 시험 자료)으로만 잰다.** 생성 데이터를 섞은 모델도 마찬가지(TSTR).
3. **생성 결과를 다시 학습 자료로 넣지 않는다.** Lab 5의 "실측+생성" 줄이 TRTR보다 나아지지 않는 것을 확인하십시오.
4. **적용 범위 밖 예측은 믿지 않는다.** Lab 6의 함정 후보는 예측 240 V였지만 측정은 50~77 V였습니다. X가 범위 안이어도 조합이 새로우면 Y가 외삽될 수 있어, 예측값이 학습 자료 Y 범위 안인지도 검사합니다.
5. **측정 오차보다 작은 오차는 과적합 신호.** Voc 반복 변동계수 중앙값(≈ 10%)을 기준으로 봅니다.

## 4. 데이터 생성 프롬프트

LLM으로 생성기 코드·문헌값 표·검증 리뷰를 받을 때는 `prompts/data_generation_prompts.md`의 P1~P6을 씁니다. 원칙: LLM은 숫자가 아니라 코드와 근거를 만들고, 숫자는 시드를 고정한 코드가 만듭니다.

## 5. 실측이 들어오면

1. 실험실은 `00_measurement_template.csv` 양식으로 기록 (장비·상대 전극·간격·압력·주파수·온습도 고정, 반복 3회).
2. `lab1_check_data.py 실측파일.csv`로 점검 → 변동계수 0.15 초과 원단 재측정.
3. 원단이 50개 미만이면 Lab 4의 무리 수를 1~3으로 제한하고, 8항목(`X8`)으로 시작.
4. 생성기(`analysis/mock_data/generate_mock_fabric.py`)를 실측으로 보정: 19항목 분위수 맞춤 → σ₀ → SRA_opt → 습도 기울기.
5. Lab 6의 측정 칸(`measured_Voc`)을 실제 측정값으로 채우고 판정.
