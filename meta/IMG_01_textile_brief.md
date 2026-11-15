# 이미지 제작 명세서 — 01 직물 구조로 성능을 미리 맞히는 AI

| 항목 | 내용 |
|---|---|
| 페이지 | hanyang_textile_ai_brief_01.html |
| 형식 | 브리핑(대담)형 — 인턴 시아·모아가 묻고 조수 하루가 답함 (사용자 지정, 대결 섹션 없음) |
| 주 앵커 | D 일상 (냉장고·라면·시험지 비유) |
| 시즌 | 없음 · 낮의 연구실 |

## 그림 전체 목록

| 키 | 판 | 상태 | 쓰는 곳 | 만드는 법 |
|---|---|---|---|---|
| cover_01_brief | L 16:9 | **새로 그림** | 페이지 맨 위 표지 | `COVER_01_textile_brief.md` 지시문 → Genspark |
| og_01 | 1200×630 | 표지에서 자름 | 공유 미리보기 | 표지를 받은 뒤 잘라 만듦 |
| thumb_01 | 3:2 | 표지에서 자름 | 시리즈 목차 카드 | 표지를 받은 뒤 잘라 만듦 |
| sia_smile·guide·explain·think·proud | B 192px | 캐릭터 팩 재사용 | 말풍선·등장인물 | `packs/character/character_pack/webp/192/sia` |
| moa_smile·tea·think·report·ok·sparkle | B 192px | 캐릭터 팩 재사용 | 말풍선·등장인물 | `.../webp/192/moa` |
| asst_smile·report·spark·firm·proud | B 192px | 캐릭터 팩 재사용 | 말풍선·등장인물 | `.../webp/192/asst` |

## 만드는 순서
1. 표지 `cover_01_brief`를 먼저 받아 그림체를 확인한다.
2. 받은 표지에서 og·thumb를 자른다.
3. 페이지의 대체 표지(직물 격자 + 캐릭터 3명)를 받은 표지로 바꾸고 `cover_manifest.json`의 `status`를 `ok`로 고친다.

## 아웃트로 표정 점검
대결이 없는 브리핑이라 승패 표정이 없다. 아웃트로는 시아 `proud`, 모아 `sparkle`, 조수 `report`·`proud`로 정리·보고 분위기에 맞췄다.
