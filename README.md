# 직물 구조로 성능을 미리 맞히는 AI — 연구 계획 브리핑

한양대 섬유 연구과제(직물 태·마찰전기 AI 예측)의 연구 계획을 연구실 인턴 시아·모아, 조수 하루, 주판봇이 브리핑하는 정적 웹 문서입니다. 기준일 2026-11-16.

## 문서 구성

| 쪽 | 파일 | 내용 |
|---|---|---|
| INDEX | `index.html` | 전체 연구 계획 정리, 스테이지 현황, 검토 결과·주판봇 요청 모음, 지식 색인·내려받기 |
| 연차별 연구계획 | `plan_years.html` | 5년 로드맵 (3~5차년도는 예정) |
| 전체 스테이지 및 FLOW | `stages.html` | 흐름도, 일정, S0~S6 카드 |
| S0 착수·자료 정리 | `stage_0_kickoff.html` | 데이터 현황, 결정 질문 10개 |
| S1 파일럿 탐색 분석 | `stage_1_explore.html` | PCA, 장비 간 일치도 |
| S2 샘플 확충·정답 측정 | `stage_2_data.html` | 8묶음 기록 항목, 실험계획 |
| S3 기초 예측 모델 | `stage_3_model.html` | 모델 순서, 과적합·누수 실험, 평가 기준 |
| S4~S6 (예정) | `stage_4_sim2real.html`, `stage_5_tribo.html`, `stage_6_device.html` | 정해진 것과 예정인 것 |
| 이미지 데이터 분석 | `image_data.html` | 실습용 이미지 140장 진단과 보완사항 |
| 작성 가이드 | `data_guide.html` | 가상 섬유 데이터 작성 규칙, 양식, 점검표 |
| 참고문헌 | `references.html` | 장비·마찰전기·시뮬레이션·모델·데이터 품질 문헌 |

각 쪽은 자체 완결 HTML입니다(스크립트·그림 내장). 검토 표시와 주판봇 요청은 보는 사람의 브라우저(localStorage)에만 저장됩니다.

## 폴더

```
*.html                 게시용 페이지 13개
src/                   빌드 소스 (build_pages.py가 진입점)
analysis/image_data/   이미지 데이터 분석 스크립트와 결과 (features.csv 등)
meta/                  표지·이미지 프롬프트, 지식 색인 등록부
```

## 다시 빌드하기

```bash
# 캐릭터 그림 팩(ahnboat_lab_explainer 저장소)의 위치를 지정
export LAB_CHAR_PACK=../ahnboat_lab_explainer/packs/character/character_pack
python3 src/build_pages.py        # 저장소 루트에 html 13개를 다시 씀
```

이미지 특징 재계산: `python3 analysis/image_data/feat.py <fabric_dataset 폴더>` → `clf.py`

원자료(연구계획서, 데이터셋 엑셀, 이미지 데이터셋 원본)는 이 저장소에 넣지 않았습니다.

글 · 안상선
