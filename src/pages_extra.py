# ---- 부록 쪽 3개: 이미지 데이터 분석 · 가상 데이터 작성 가이드 · 참고 레퍼런스 ----
# build_pages.py 안에서 exec 로 실행된다 (page, wrap, tail, say, crumb, SBY 등 공유)
IMGD = os.path.join(B, '..', 'analysis', 'image_data')
IMF = json.load(open(f'{IMGD}/feat_small.json', encoding='utf-8'))
THB = json.load(open(f'{IMGD}/thumbs.json'))

def sl(k, mood): return f'<a href="{SBY[k]["file"]}">S{SBY[k]["n"]}</a>'
def fig(n, cap, bad=False): return f'<figure class="{"bad" if bad else ""}"><img src="{THB[n]}" alt="{n} 원단 사진 축소본" loading="lazy"><figcaption>{cap}</figcaption></figure>'

# ================= 이미지 데이터 리뷰·분석 =================
gal = ''
for key, lab in [('soft', '부드러움'), ('rib', '거침 · 리브 골'), ('twill', '거침 · 사선 능직'), ('stiff', '거침 · 뻣뻣한 고밀도'), ('flat', '거침 · 얇고 납작함'), ('pill', '거침 · 필링')]:
    names = [n for n in THB if n.startswith(key + '_')]
    gal += f'<h4 style="margin:14px 0 4px">{lab}</h4><div class="thumbs">' + ''.join(fig(n, n) for n in names) + '</div>'

prob = [
 ('①', '"흐리고 밋밋하면 부드러움" 지름길', '명암 대비 중앙값 부드러움 9.5 · 거침 25.2, 선명도 중앙값 489 · 1,582. 명암 대비 하나로 시험 20장 중 18장을 맞힙니다.', '모델이 태가 아니라 사진의 흐림·대비를 배웁니다. 실제 원단 사진에서는 무너질 가능성이 큽니다.', '높음'),
 ('②', '색에 따라 틀리는 쏠림', '남색 거침 사진은 대비가 낮고(중앙값 19.5), 연회색 부드러움 사진은 높습니다(14.2). 지름길 규칙이 틀린 시험 사진 2장은 모두 연회색 부드러움입니다.', '색이 진하거나 밝으면 판정이 흔들립니다.', '높음'),
 ('③', '부드러움 사진의 다양성이 낮음', '생성 지시문의 본문(조건 문구를 뺀 부분)이 부드러움은 3가지, 거침은 10가지입니다.', '부드러움 사진이 서로 비슷해, 모델이 "부드러움의 한 가지 모습"만 외웁니다.', '중간'),
 ('④', '거침 정도 라벨이 사진과 맞지 않음', 'mild → moderate → strong 순으로 명암 대비가 꾸준히 커지는 유형은 사선 능직뿐입니다. 필링은 26.5 → 20.2 → 32.1로 오르내립니다.', '거침 정도를 학습 목표로 쓰면 잡음이 됩니다.', '중간'),
 ('⑤', '배율 정보가 없음', '"5cm 접사", "15cm 근접"을 지시했지만 사진마다 실 굵기가 달라 보입니다(저희 눈으로 본 판단). 사진 안에 자나 눈금이 없습니다.', '실 굵기·밀도 같은 구조 변수를 사진에서 읽을 수 없습니다.', '중간'),
 ('⑥', '유형과 조직이 묶여 있음', '리브 골 14장은 모두 편직, 사선 능직 14장은 모두 제직입니다. 정의상 자연스럽지만, 모델이 "조직 종류"를 거침 단서로 쓸 수 있습니다.', '조직 분류와 거침 분류가 섞입니다.', '낮음'),
 ('⑦', '라벨이 측정값이 아님', '라벨은 생성 지시문에서 왔습니다. README도 KES-FB 같은 실제 태 측정값이 아니라고 밝힙니다. 엑셀의 원단 27개와 이어 주는 원단 번호가 없습니다.', '연구 본선(구조 → 물성 → 성능)에는 바로 쓸 수 없습니다.', '높음'),
 ('⑧', '시험 세트가 작음', '시험 20장으로 잰 정답률 90%의 95% 신뢰구간은 약 70~97%입니다.', '모델끼리 차이를 가리기 어렵습니다.', '중간'),
 ('⑨', '일부 사진의 라벨이 애매함', 'stiff_002는 굵은 편직이라 푹신해 보이고, stiff_010은 매끈한 저지처럼 보입니다(저희 눈으로 본 판단, 확인 필요).', '사람이 봐도 갈리는 사진은 학습을 흐립니다.', '낮음'),
]
probt = '<div class="tw"><table class="tb prob"><tr><th>번호</th><th>문제</th><th>근거 (직접 계산)</th><th>영향</th><th>우선순위</th></tr>' + ''.join(
    f'<tr><td>{a}</td><td><b>{b}</b></td><td>{c}</td><td>{d}</td><td><span class="st {"draft" if e=="높음" else "part" if e=="중간" else "plan"}">{e}</span></td></tr>' for a, b, c, d, e in prob) + '</table></div>'
fixes = [
 ('부드러움 사진을 선명하게 다시 만들기', '①③', '생성 지시문에 "sharp focus, crisp fiber detail"을 두 클래스 모두 넣고, 부드러움 본문을 기모·저지·벨벳·플리스 등 8가지 이상으로 늘립니다.', '두 클래스의 선명도·대비 중앙값 차이 20% 이내 (제안값)'),
 ('지름길 검사를 품질검사에 넣기', '①②', '명암·선명도·밝기·채도 하나씩으로 분류해 봅니다. 하나로 잘 맞히면 그 특징의 분포를 맞춰 다시 만듭니다.', '단일 특징 AUC 0.65 이하 (제안값)'),
 ('학습할 때 흐림·대비를 무작위로 바꾸기', '①②', '데이터 증강으로 흐림, 대비, 밝기, 색조를 섞어 지름길을 쓸모없게 만듭니다.', '증강 전후 시험 정답률과 오답 사진 비교'),
 ('색 × 클래스 칸마다 사진 수 맞추기', '②', '4색 × 2클래스 × 4조명 칸마다 최소 2장씩 둡니다. 남색·연회색 칸을 먼저 채웁니다.', '칸마다 2장 이상'),
 ('자·색표를 넣고 배율 기록하기', '⑤', '실제 촬영은 같은 조명 상자에서 자와 색 기준표를 함께 찍고, 1 mm가 몇 화소인지 기록합니다.', '모든 사진에 화소/mm 값'),
 ('거침 정도 라벨은 빼거나 다시 정의하기', '④', '정도 라벨은 학습 목표에서 빼고, 필요하면 사람 3명이 매긴 점수의 평균으로 바꿉니다.', '평가자 간 일치도(ICC) 0.7 이상 (제안값)'),
 ('실제 원단 27개를 직접 찍어 엑셀과 잇기', '⑦', '원단 번호(H_ND3 등)를 파일 이름에 넣어 사진과 측정값을 한 줄로 묶습니다. 생성 사진은 학습 보조로만 씁니다.', '사진 → 엑셀 연결률 100%'),
 ('시험 세트 늘리고 원단 단위로 나누기', '⑧', '시험은 실제 촬영 사진으로, 원단마다 3장 이상, 원단 단위로 학습·시험을 나눕니다.', '시험 원단 10개 이상'),
]
fixt = '<div class="tw"><table class="tb"><tr><th>보완 방법</th><th>해결하는 문제</th><th>어떻게</th><th>확인 기준</th></tr>' + ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in fixes) + '</table></div>'

img_body = wrap(crumb(('index.html', 'INDEX'), (None, '섬유 이미지 데이터 리뷰·분석')) +
 '<h1 style="margin:4px 0 8px">섬유 이미지 데이터 리뷰·분석 <span class="st plan">2차년도 이후</span></h1>'
 '<div class="planbox"><h4>이 데이터는 2차년도 이후에 활용합니다 <span class="st plan">예정</span></h4><p class="small" style="margin:0">2026-11-17에 정한 1차년도 방향은 "수치로 잰 직물 특성 → 실측 전기 특성 → 생성 → 예측"입니다. 이미지 진단 결과는 2차년도에 이미지를 더할 때 쓰도록 보관합니다. <a href="method_review.html">1차년도 연구 방법 검토</a> 참고.</p></div>'
 '<p class="lead">받은 실습용 이미지 데이터셋(fabric_dataset, 2026-09-22 생성) 140장을 전부 열어 보고 숫자로 진단했습니다. 강의 「직물 태(Hand) 판정 AI 만들기」의 Teachable Machine 실습용 최소판입니다.</p>'
 '<div class="brief"><div class="bh">핵심 보고</div><dl><dt>결론</dt><dd>정리와 균형은 잘 되어 있습니다. 다만 사진의 <b>명암 대비 하나만으로 시험 20장 중 18장</b>을 맞힐 수 있어, 모델이 태가 아니라 "흐림·대비"를 배울 위험이 큽니다.</dd>'
 '<dt>근거</dt><dd>140장 전체에서 명암 대비·선명도·밝기·채도·주파수 특징을 직접 계산하고, 특징 하나씩으로 분류해 봤습니다.</dd>'
 '<dt>요청</dt><dd>부드러움 사진 재생성(선명하게), 지름길 검사 추가, 실제 원단 촬영 계획 여부를 정해 주십시오.</dd></dl></div>'
 + say('asst', 'report', '교수님, 이 데이터는 실습용으로는 충분히 정돈되어 있습니다. 연구 본선에 쓰려면 아래 보완이 필요해 보고드립니다.') +
 '<h2 style="margin-top:28px">데이터 개요</h2><div class="kpis">'
 '<div class="kpi g"><b>140</b><span>사진 수 (학습 120 · 시험 20)</span></div><div class="kpi i"><b>1:1</b><span>부드러움 70 · 거침 70</span></div>'
 '<div class="kpi m"><b>5유형</b><span>거침 유형 × 14장씩</span></div><div class="kpi a"><b>1254²</b><span>모두 같은 크기 JPEG</span></div><div class="kpi r"><b>22</b><span>재생성한 사진 (1~2회)</span></div></div>'
 '<p class="small muted">생성: Genspark 이미지 생성(GPT Image 2). 기록표 creation_log.csv에 사진마다 라벨·조명·색·거리·조직·지시문이 있습니다. <span class="realnote">실측</span> 아래 숫자는 모두 사진 파일에서 직접 계산했습니다.</p>'
 '<h2 style="margin-top:28px">잘 된 점</h2><ul>'
 '<li><b>촬영 조건 균형</b> — 조명·색·거리·조직만으로 분류하면 시험 정답률 45%로 찍기 수준입니다. 조건이 라벨을 흘리지 않습니다.</li>'
 '<li><b>중복 없음</b> — 사진 지문(64비트 지각 해시)으로 비교하니 학습↔시험 사이 가장 가까운 쌍도 16비트가 달랐고, 10비트 이하 쌍은 0건입니다.</li>'
 '<li><b>규격 통일과 기록</b> — 크기·형식이 같고, 사진마다 생성 지시문과 재생성 횟수가 남아 있습니다. 재현과 점검이 쉽습니다.</li></ul>'
 '<h2 style="margin-top:28px">사진 둘러보기</h2><p class="small muted">유형마다 4장씩 줄여서 보여 드립니다. 부드러움 사진이 전체적으로 흐리고 결이 덜 보이는 것이 눈으로도 보입니다.</p>' + gal) + \
 wrap('<h2>지름길 실험 — 명암 대비 하나로 얼마나 맞힐까</h2>'
 '<p class="lead">가로는 선명도, 세로는 명암 대비입니다. 노란 점선 위는 "거침", 아래는 "부드러움"으로 찍는 규칙입니다. 점선을 움직여 보세요.</p>'
 '<div class="panel"><h4>140장 산점도 <span class="realnote">실측 · 사진에서 직접 계산</span></h4>'
 '<div class="ctrl"><div class="group" role="group" aria-label="색칠 기준"><span class="glabel">색칠</span><button class="bt" data-im="cls" aria-pressed="true">정답 라벨</button><button class="bt" data-im="color" aria-pressed="false">원단 색</button><button class="bt" data-im="set" aria-pressed="false">학습/시험</button></div>'
 '<div class="group"><span class="glabel">점선 높이</span><input type="range" id="imgThr" min="6" max="34" step="1" value="14" aria-label="명암 대비 기준값"><span class="val" id="imgThrV">14</span></div></div>'
 '<div class="cwrap"><canvas id="imgSc" height="340" aria-label="사진 140장의 선명도와 명암 대비 산점도"></canvas></div><div class="small" id="imgLeg" style="margin-top:6px"></div>'
 '<div class="kpis" id="imgAcc" style="margin-top:10px"></div></div>'
 '<div class="tw"><table class="tb"><tr><th>쓴 정보</th><th>시험 20장 정답률</th><th>뜻</th></tr>'
 '<tr><td>명암 대비 하나 (기준 14)</td><td><b>90%</b> (18/20)</td><td>지름길이 강함</td></tr>'
 '<tr><td>명암 대비 하나 (로지스틱 회귀)</td><td>75% · AUC 0.84</td><td>140장 전체 AUC는 0.93</td></tr>'
 '<tr><td>선명도 하나</td><td>70%</td><td>흐림도 단서가 됨</td></tr>'
 '<tr><td>단순 특징 8개 (대비·선명도·밝기·채도 등)</td><td>90% · AUC 0.96</td><td>딥러닝 없이도 거의 다 맞힘</td></tr>'
 '<tr><td>촬영 조건만 (조명·색·거리·조직)</td><td>45%</td><td>조건 균형은 잘 됨</td></tr></table></div>'
 '<h4>지름길 규칙이 틀린 시험 사진 2장</h4><div class="thumbs" style="max-width:320px">' + fig('t_soft_03', 't_soft_03 · 부드러움인데 대비 29.5', True) + fig('t_soft_05', 't_soft_05 · 부드러움인데 대비 23.5', True) + '</div>'
 '<div class="talk"><p class="th">질의응답</p>' + say('sia', 'think', '시험에서 90%면 잘 된 것 아닙니까?') +
 say('asst', 'report', '점수만 보면 그렇습니다. 그런데 사진의 흐림·대비만 봐도 같은 점수가 나옵니다. 실제 원단을 찍은 사진에서는 이 단서가 통하지 않을 수 있습니다.') +
 say('robo', 'calc', '제가 계산해 보니, 대비 기준 하나로 학습 약 93%, 시험 90%입니다. 딥러닝이 이 숫자를 넘지 못하면 지름길만 배운 것입니다.') + '</div>') + \
 wrap('<h2>보완사항 — 문제 9가지</h2>' + probt +
 '<h2 style="margin-top:28px">보완 방법과 확인 기준</h2>' + fixt +
 '<h2 style="margin-top:28px">이 데이터의 자리</h2><ul>'
 '<li><b>지금</b> — 강의·실습용(Teachable Machine)으로 그대로 씁니다. 다만 "지름길" 실습 사례로 함께 보여 주면 교육 효과가 큽니다.</li>'
 f'<li><b>연구 본선</b> — 실제 원단 촬영 사진을 원단 번호로 엑셀과 이으면, {sl("s2","")}의 8묶음에 "표면 이미지" 묶음을 더하는 안을 <span class="st plan">예정</span>으로 둡니다.</li>'
 f'<li><b>생성 이미지</b> — 실측 사진이 모인 뒤 학습 보조로만 쓰고, 시험은 실측 사진으로만 합니다. 작성 규칙은 <a href="data_guide.html">가상 섬유 데이터 작성 가이드</a>에 있습니다.</li></ul>'
 '<details><summary>계산 방법 펼치기</summary><ul class="small">'
 '<li>모든 사진을 흑백 512×512로 줄인 뒤 계산했습니다.</li><li>명암 대비 = 밝기의 표준편차, 선명도 = 라플라시안(경계 강조) 결과의 분산, 고주파 비율 = 2차원 푸리에 변환에서 반지름 64 바깥 에너지 비율.</li>'
 '<li>사진 지문 = 32×32 이산 코사인 변환 왼쪽 위 8×8의 중앙값 비교(64비트).</li><li>신뢰구간 = 윌슨 방법.</li></ul></details>')
sizes['image_data.html'] = page('image_data.html', '섬유 이미지 데이터 리뷰·분석', img_body + tail((('references.html', '참고 레퍼런스'), ('data_guide.html', '가상 섬유 데이터 작성 가이드'))), extra={'img': IMF})

# ================= 가상 섬유 데이터 작성 가이드 =================
COLS = [
 ('식별', 'fabric_id', '원단 고유 번호', '—', '실측 H_ND3 / 가상 SIM-T03-000123 / 생성 GEN-IMG-000045', '필수'),
 ('식별', 'source', '출처 구분', '—', 'real · sim · gen 중 하나', '필수'),
 ('식별', 'parent_id', '바탕이 된 실측 원단', '—', 'H_ND3 (없으면 빈칸)', '권장'),
 ('식별', 'generator', '만든 도구와 버전', '—', 'TexGen 3.13 + Abaqus 2024', '가상 필수'),
 ('식별', 'seed', '난수 시드', '—', '20270301', '가상 필수'),
 ('식별', 'rep', '반복 측정 번호', '—', '1, 2, 3', '실측 필수'),
 ('식별', 'created_at', '만든 날짜', '—', '2027-03-15', '필수'),
 ('실 특성 (B)', 'fiber', '섬유 조성', '%', 'PET100 / PET65-CO35', '필수'),
 ('실 특성 (B)', 'yarn_count', '실 굵기(섬도)', 'dtex', '167', '필수'),
 ('실 특성 (B)', 'filaments', '필라멘트 수', '가닥', '48', '권장'),
 ('실 특성 (B)', 'twist', '꼬임 수', '회/m', '600', '권장'),
 ('실 특성 (B)', 'yarn_shape', '단면 형상', '—', 'round · trilobal · hollow', '권장'),
 ('제작 조건 (C)', 'structure', '조직', '—', 'plain · twill · satin · jersey · rib · nonwoven', '필수'),
 ('제작 조건 (C)', 'dens_1', '경사 밀도 (편직은 웨일)', '가닥/cm', '40', '필수'),
 ('제작 조건 (C)', 'dens_2', '위사 밀도 (편직은 코스)', '가닥/cm', '32', '필수'),
 ('제작 조건 (C)', 'tension', '제직·편직 장력', 'cN', '15', '권장'),
 ('제작 조건 (C)', 'finish', '후가공', '—', 'none · brushed · calendered', '권장'),
 ('기본 물성', 'thickness', '두께', 'mm', '0.42', '필수'),
 ('기본 물성', 'weight', '단위 면적당 중량', 'g/m²', '180', '필수'),
 ('기본 물성', 'air_perm', '통기도', 'cm³/cm²/s', '45', '권장'),
 ('역학 (KES-FB)', 'LT_1, LT_2', '인장 선형성 (_1 경사, _2 위사)', '—', '0.65', '필수'),
 ('역학 (KES-FB)', 'WT_1, WT_2', '인장 에너지', 'gf·cm/cm²', '8.2', '필수'),
 ('역학 (KES-FB)', 'RT_1, RT_2', '인장 회복률', '%', '62', '필수'),
 ('역학 (KES-FB)', 'B_1, B_2', '굽힘 강성', 'gf·cm²/cm', '0.085', '필수'),
 ('역학 (KES-FB)', '2HB_1, 2HB_2', '굽힘 이력', 'gf·cm/cm', '0.031', '권장'),
 ('역학 (KES-FB)', 'G_1, G_2', '전단 강성', 'gf/(cm·deg)', '0.62', '필수'),
 ('역학 (KES-FB)', '2HG_1, 2HG_2', '전단 이력 (0.5°)', 'gf/cm', '0.55', '권장'),
 ('역학 (KES-FB)', 'LC', '압축 선형성', '—', '0.31', '필수'),
 ('역학 (KES-FB)', 'WC', '압축 일', 'gf·cm/cm²', '0.25', '필수'),
 ('역학 (KES-FB)', 'RC', '압축 회복률', '%', '48', '필수'),
 ('역학 (KES-FB)', 'MIU_1, MIU_2', '평균 마찰 계수', '—', '0.21', '필수'),
 ('역학 (KES-FB)', 'MMD_1, MMD_2', '마찰 계수 변동', '—', '0.012', '필수'),
 ('역학 (KES-FB)', 'SMD_1, SMD_2', '표면 거칠기', 'μm', '3.4', '필수'),
 ('동적 마찰', 'mu_s', '정지 마찰 계수', '—', '0.34', '필수'),
 ('동적 마찰', 'mu_k', '운동 마찰 계수', '—', '0.27', '필수'),
 ('동적 마찰', 'slide_speed', '미끄럼 속도', 'mm/s', '1.0', '필수'),
 ('동적 마찰', 'normal_load', '누르는 힘', 'N', '0.5', '필수'),
 ('동적 마찰', 'fric_ts', '마찰력 시계열 파일과 표본 주기', '—', 'ts/H_ND3_r1.csv @ 1 kHz', '필수'),
 ('마찰전기 (Y)', 'te_mode', '접촉 모드', '—', 'contact-separation · sliding · single-electrode', '필수'),
 ('마찰전기 (Y)', 'counter', '상대 물질', '—', 'PTFE · nylon 등', '필수'),
 ('마찰전기 (Y)', 'te_force', '누르는 힘', 'N', '10', '필수'),
 ('마찰전기 (Y)', 'te_freq', '주파수', 'Hz', '2', '필수'),
 ('마찰전기 (Y)', 'Voc', '개방 전압', 'V', '35', '필수'),
 ('마찰전기 (Y)', 'Isc', '단락 전류', 'μA', '0.8', '필수'),
 ('마찰전기 (Y)', 'sigma', '전하 밀도', 'μC/m²', '25', '권장'),
 ('측정 환경', 'temp', '온도', '°C', '20', '필수'),
 ('측정 환경', 'rh', '상대 습도', '%', '65', '필수'),
 ('측정 환경', 'cond_h', '컨디셔닝 시간', 'h', '24', '필수'),
 ('측정 환경', 'instrument', '측정 장비', '—', 'KES-FB · FTT', '필수'),
 ('측정 환경', 'operator', '측정자', '—', '이니셜', '권장'),
]
def col_names():
    out = []
    for c in COLS:
        for n in c[1].split(', '): out.append(n)
    return out
MASTER_EX = {'fabric_id': 'SIM-T03-000123', 'source': 'sim', 'parent_id': 'H_ND3', 'generator': 'TexGen 3.13 + Abaqus 2024', 'seed': '20270301', 'rep': '', 'created_at': '2027-03-15',
             'fiber': 'PET100', 'yarn_count': '167', 'structure': 'plain', 'dens_1': '40', 'dens_2': '32', 'thickness': '0.42', 'weight': '180', 'temp': '20', 'rh': '65'}
SIMC = ['run_id', 'fabric_id', 'parent_id', 'tool_versions', 'seed', 'unitcell_x_mm', 'unitcell_y_mm', 'yarn_width_mm', 'yarn_height_mm', 'yarn_spacing_mm', 'yarn_E_MPa', 'yarn_poisson', 'contact_friction', 'element_type', 'mesh_size_mm', 'n_elements', 'load_case', 'max_strain_or_load', 'output_file', 'run_time_min', 'converged', 'mesh_check_pass', 'note']
IMGC = ['file', 'set', 'label', 'label_source', 'fabric_id', 'structure', 'color', 'light', 'distance_cm', 'px_per_mm', 'scale_bar', 'generator', 'model', 'prompt', 'seed', 'regen_count', 'created_at', 'qc_contrast', 'qc_sharpness', 'qc_pass', 'note']
DATASHEET = """# 데이터 설명서 — (데이터 이름)

## 1. 왜 만들었나
- 목적:
- 쓰일 스테이지: (S2·S3·S4·S5)

## 2. 무엇이 들어 있나
- 행 하나의 뜻: (원단 1개 × 반복 1회 등)
- 행 수 / 원단 수:
- 출처 구분: real ○건 · sim ○건 · gen ○건
- 열 사전: data_dictionary.csv 참고

## 3. 어떻게 만들었나
- 도구와 버전:
- 시드와 설정 파일 위치:
- 실측 원단과의 연결(parent_id) 규칙:

## 4. 품질검사 결과
- 범위 위반: ○건
- 실측 대비 분포 비교:
- 지름길 검사(이미지): 단일 특징 AUC 최댓값 ○
- 판별기 AUC(합성 vs 실측):

## 5. 쓰는 규칙
- 시험·검증에는 실측(real)만 씁니다.
- 원단 단위로 나눌 때 같은 parent_id는 같은 묶음에 넣습니다.

## 6. 알려진 한계
-

## 7. 관리
- 작성자 / 작성일 / 버전:
- 바뀐 점:
"""
GUIDE = {
 'master': {'kind': 'header', 'file': 'master_template.csv', 'cols': col_names(), 'example': [MASTER_EX.get(c, '') for c in col_names()]},
 'dict': {'kind': 'dict', 'file': 'data_dictionary.csv', 'head': ['묶음', '열 이름', '뜻', '단위', '형식·예', '필수 여부'], 'rows': [list(c) for c in COLS]},
 'sim': {'kind': 'header', 'file': 'sim_runs_template.csv', 'cols': SIMC},
 'img': {'kind': 'header', 'file': 'image_log_template.csv', 'cols': IMGC},
 'sheet': {'kind': 'md', 'file': 'datasheet_template.md', 'text': DATASHEET},
}
colt = '<div class="tw"><table class="tb"><tr><th>묶음</th><th>열 이름</th><th>뜻</th><th>단위</th><th>형식·예</th><th>필수</th></tr>' + ''.join(
    f'<tr><td>{a}</td><td><code>{b}</code></td><td>{c}</td><td>{d}</td><td>{e}</td><td>{f}</td></tr>' for a, b, c, d, e, f in COLS) + '</table></div>'
principles = [
 ('가상이라고 표시한다', '모든 행에 source(real·sim·gen)를 적습니다. 섞인 뒤에도 언제든 걸러낼 수 있어야 합니다.'),
 ('실측과 같은 열 이름', '가상 데이터도 실측 마스터 표와 같은 열 이름·단위를 씁니다. 따로 놀면 합칠 때 실수가 납니다.'),
 ('다시 만들 수 있게', '도구 버전, 시드, 설정 파일을 남깁니다. 같은 설정이면 같은 데이터가 나와야 합니다.'),
 ('실측 원단에 묶는다', '어느 실측 원단을 바탕으로 만들었는지 parent_id로 남깁니다. 원단 단위로 나눌 때 함께 움직입니다.'),
 ('시험은 실측으로만', '가상 데이터는 학습에만 씁니다. 성능은 실측 시험 세트로만 보고합니다.'),
 ('지름길을 먼저 잡는다', '라벨과 상관없는 단서(밝기·흐림·색·파일 크기)로 맞힐 수 있으면 다시 만듭니다.'),
 ('분포를 비교하고 남긴다', '실측과 범위·분포·상관을 비교한 결과를 데이터 설명서에 적습니다.'),
]
pcards = '<div class="mapc">' + ''.join(f'<div class="card" style="border:1px solid var(--rule);border-radius:14px;padding:14px 16px;background:#fff"><span class="small muted">원칙 {i+1}</span><b style="display:block;margin:4px 0">{a}</b><span class="small">{b}</span></div>' for i, (a, b) in enumerate(principles)) + '</div>'
checks = [
 '모든 행에 source(real·sim·gen)를 적었다', '열 이름·단위를 열 사전과 맞췄다', '가상 행에 generator·seed·created_at을 적었다', '가상 행에 parent_id를 적었다(바탕 원단이 있을 때)',
 '실측 범위를 벗어난 값이 없는지 확인했다', '실측과 분포(평균·범위)를 비교했다', '실측과 상관 구조를 비교했다', '판별기 검사(가상 vs 실측)를 했다',
 '이미지: 단일 특징(대비·선명도·밝기·색) 지름길 검사를 했다', '이미지: 사진 지문으로 학습·시험 중복을 검사했다', '이미지: 배율(화소/mm)을 기록했다',
 '시험·검증 세트에 가상 데이터가 없다', '데이터 설명서(datasheet)를 채웠다']
ckh = '<div class="qlist" id="ckList">' + ''.join(f'<button type="button" aria-pressed="false" data-ck="c{i}"><span class="bx" aria-hidden="true"></span><span>{t}</span></button>' for i, t in enumerate(checks)) + '</div>'
cmp_t = ('<div class="tw"><table class="tb"><tr><th>검사</th><th>어떻게</th><th>합격 기준 (제안값)</th></tr>'
 '<tr><td>범위</td><td>열마다 실측 최솟값~최댓값 밖으로 나간 값 세기</td><td>0건, 넘으면 이유 기록</td></tr>'
 '<tr><td>분포</td><td>열마다 실측과 가상의 분포 차이(KS 통계량) 계산</td><td>핵심 열 KS 0.2 이하</td></tr>'
 '<tr><td>상관 구조</td><td>열끼리 순위 상관 행렬을 실측·가상 각각 계산해 차이 평균</td><td>평균 차이 0.15 이하</td></tr>'
 '<tr><td>판별기</td><td>"실측이냐 가상이냐"를 맞히는 분류기를 학습</td><td>AUC 0.7 이하 (가릴 수 없어야 좋음)</td></tr>'
 '<tr><td>쓸모 (TSTR)</td><td>가상으로 학습하고 실측으로 시험한 성능을 실측끼리 학습·시험한 성능과 비교</td><td>실측 성능의 80% 이상</td></tr>'
 '<tr><td>지름길 (이미지)</td><td>대비·선명도·밝기·채도 하나씩으로 라벨 분류</td><td>각 AUC 0.65 이하</td></tr>'
 '<tr><td>중복 (이미지)</td><td>64비트 사진 지문 거리</td><td>학습↔시험 10비트 이하 쌍 0건</td></tr></table></div>')
prompt_tpl = ('[고정부] close-up top-down macro photo of a flat fabric swatch, fabric texture fills the entire frame, sharp focus, crisp fiber detail, '
 'a small millimeter ruler at the bottom edge, neutral gray color card at the corner, no folds, no text, no people, square 1:1, photorealistic\n'
 '[조건부] {light}, {color}, {distance} — 배치표에서 칸마다 고르게\n'
 '[구조부] {structure}, {yarn description}, {density description} — 라벨과 연결되는 부분\n'
 '[금지] 라벨 쪽에만 "blurry, soft focus, low contrast" 같은 촬영 품질 말 쓰지 않기')
guide_body = wrap(crumb(('index.html', 'INDEX'), (None, '가상 섬유 데이터 작성 가이드')) +
 '<h1 style="margin:4px 0 8px">가상 섬유 데이터 작성 가이드</h1>'
 '<p class="lead">앞으로 만들 가상 데이터 세 종류 — ① 시뮬레이션·합성 표 데이터, ② 시뮬레이션 실행 기록, ③ 생성 이미지 — 를 같은 규칙으로 쓰기 위한 안내입니다. 양식은 바로 내려받아 쓰실 수 있습니다.</p>'
 '<div class="brief"><div class="bh">핵심 보고</div><dl><dt>결론</dt><dd>가상 데이터는 실측과 같은 열 이름으로, 출처·시드·바탕 원단을 꼭 남기고, 학습에만 씁니다.</dd>'
 '<dt>근거</dt><dd>받은 이미지 데이터에서 지름길 문제가 확인됐고(<a href="image_data.html">이미지 분석</a>), 엑셀 27개 원단은 장비·열 이름이 섞여 있었습니다(S0).</dd>'
 f'<dt>요청</dt><dd>열 사전의 필수 항목과 합격 기준(제안값)을 검토해 주십시오. 시뮬레이션 담당이 정해지면 {sl("s4","")} 일정에 맞춰 적용합니다.</dd></dl></div>'
 + say('moa', 'ok', '양식은 아래 단추로 내려받으실 수 있습니다. 엑셀에서 바로 열립니다.') +
 '<div class="ctrl" style="flex-wrap:wrap"><button class="bt primary" data-tpl="master">마스터 표 양식 .csv</button><button class="bt" data-tpl="dict">열 사전 .csv</button><button class="bt" data-tpl="sim">시뮬레이션 실행 기록 .csv</button><button class="bt" data-tpl="img">이미지 기록표 .csv</button><button class="bt" data-tpl="sheet">데이터 설명서 .md</button></div><p class="small muted dlnote" aria-live="polite"></p>'
 '<h2 style="margin-top:28px">일곱 가지 원칙</h2>' + pcards +
 '<h2 style="margin-top:28px">번호와 파일 이름 규칙</h2><div class="tw"><table class="tb"><tr><th>구분</th><th>원단 번호</th><th>파일 이름 예</th></tr>'
 '<tr><td>실측</td><td>기존 번호 그대로 (H_ND3, L_KS1 …)</td><td><code>real_H_ND3_r1_kes.csv</code>, <code>real_H_ND3_r1_face.jpg</code></td></tr>'
 '<tr><td>시뮬레이션</td><td>SIM-조직코드-일련번호 (SIM-T03-000123)</td><td><code>sim_SIM-T03-000123_compress.csv</code></td></tr>'
 '<tr><td>생성 이미지</td><td>GEN-IMG-일련번호</td><td><code>gen_GEN-IMG-000045_soft.jpg</code></td></tr></table></div>'
 '<p class="small muted">조직코드 예: T01 평직, T02 능직, T03 주자직, K01 저지, K02 리브, N01 부직포 (제안).</p>') + \
 wrap('<h2>① 표 데이터 — 열 사전</h2><p class="lead">S2의 8묶음을 열로 풀었습니다. 실측과 가상이 같은 표를 씁니다. 단위는 KES-FB 관례를 따랐습니다.</p>' + colt +
 '<div class="talk"><p class="th">질의응답</p>' + say('sia', 'think', '가상 데이터에도 측정 환경(온도·습도)을 적어야 합니까?') +
 say('asst', 'report', '네. 시뮬레이션이 가정한 조건을 적습니다. 나중에 실측과 같은 조건끼리만 비교할 수 있게 하려는 것입니다.') + '</div>') + \
 wrap('<h2>② 시뮬레이션 실행 기록</h2><p class="lead">TexGen으로 단위 구조를 만들고 Abaqus로 변형을 계산할 때, 실행 한 번마다 한 줄씩 남깁니다.</p>'
 '<div class="code">' + ' · '.join(SIMC) + '</div><ul>'
 '<li><b>격자 점검</b> — 요소 크기를 반으로 줄였을 때 결과가 5% 안에서 같으면 통과(제안값). mesh_check_pass에 적습니다.</li>'
 '<li><b>재료값 출처</b> — 실의 탄성계수·마찰계수는 측정값인지 문헌값인지 note에 적습니다.</li>'
 '<li><b>실측 보정</b> — 같은 원단(parent_id)의 실측 압축·굽힘 곡선과 겹쳐 그려 차이를 기록합니다.</li></ul>'
 '<span class="st plan">예정</span> <span class="small muted">시뮬레이션 담당과 계산 환경이 정해지면 항목을 확정합니다.</span>') + \
 wrap('<h2>③ 생성 이미지</h2><p class="lead">받은 이미지 데이터의 좋은 점(조건 균형·기록표)은 살리고, 지름길 문제를 막는 규칙을 더했습니다.</p>'
 '<h3>지시문 틀</h3><div class="code">' + prompt_tpl + '</div>'
 '<h3>만드는 순서</h3><ol><li>배치표 먼저 — 색 × 조명 × 거리 × 조직 × 라벨 칸마다 몇 장을 만들지 정합니다(칸마다 2장 이상).</li>'
 '<li>라벨 쪽 본문은 8가지 이상으로 — 같은 문장 반복을 피합니다.</li><li>생성 직후 품질검사 — 크기, 사진 지문 중복, 대비·선명도 분포를 봅니다.</li>'
 '<li>지름길 검사 — 단일 특징 AUC가 0.65를 넘으면 그 칸을 다시 만듭니다.</li><li>기록표 채우기 — 이미지 기록표 양식의 열을 모두 채웁니다.</li></ol>'
 '<h3>기록표 열</h3><div class="code">' + ' · '.join(IMGC) + '</div>'
 '<p class="small">label_source에는 prompt(지시문), measured(측정값), panel(사람 평가) 중 하나를 적습니다. 연구 본선에는 measured·panel 라벨을 씁니다.</p>') + \
 wrap('<h2>가상 vs 실측 비교 검사</h2>' + cmp_t +
 '<p class="small muted">합격 기준은 모두 저희 제안값입니다. 실측 원단 50개가 모이면(G2) 실제 분포를 보고 다시 정합니다.</p>'
 '<h2 style="margin-top:28px">섞어 쓰는 규칙</h2><ol><li>시험·검증 세트에는 실측만 둡니다.</li><li>원단 단위로 나눌 때 같은 parent_id의 가상 행은 바탕 원단과 같은 묶음에 넣습니다.</li>'
 '<li>가상 비율은 0% → 25% → 50%처럼 단계적으로 올리고, 단계마다 실측 시험 성능을 기록합니다.</li><li>보고할 때는 "실측만"과 "실측 + 가상" 결과를 나란히 냅니다.</li></ol>'
 '<h2 style="margin-top:28px">제출 전 점검표</h2><p class="small">눌러서 표시하면 이 브라우저에 남습니다. <span class="num" id="ckN">0 / 13</span></p>' + ckh)
sizes['data_guide.html'] = page('data_guide.html', '가상 섬유 데이터 작성 가이드', guide_body + tail((('image_data.html', '섬유 이미지 데이터 리뷰·분석'), ('references.html', '참고 레퍼런스'))), extra={'guide': GUIDE})

# ================= 참고 레퍼런스 =================
REFG = [
 ('직물 촉감(태)과 측정 장비', [
  ('Kawabata, S. (1980). <i>The Standardization and Analysis of Hand Evaluation</i> (2nd ed.). Textile Machinery Society of Japan.', None, 'KES-FB 측정 항목·단위의 기준. 열 사전의 역학 묶음.', ['s0', 's2']),
  ('Hu, J. Y., Hes, L., Li, Y., Yeung, K. W., & Yao, B. G. (2006). Fabric Touch Tester: Integrated evaluation of thermal–mechanical sensory properties of polymeric materials. <i>Polymer Testing</i>, 25(8), 1081–1090.', 'https://doi.org/10.1016/j.polymertesting.2006.07.008', 'FTT 장비 원 논문. 엑셀 FTT 계열 열 해석과 장비 통일 논의(S1-2).', ['s1']),
  ('Minazio, P. G. (1995). FAST – Fabric Assurance by Simple Testing. <i>International Journal of Clothing Science and Technology</i>, 7(2/3), 43–48.', 'https://doi.org/10.1108/09556229510087146', '계획서가 KES-FB와 함께 쓰는 FAST 장비 소개.', ['s2']),
  ('ISO 139:2005/Amd 1:2011. Textiles — Standard atmospheres for conditioning and testing.', 'https://standards.iteh.ai/catalog/standards/iso/f70fad6d-df27-498d-9fee-e548484a50e4/iso-139-2005-amd-1-2011', '측정 환경 20 ± 2 °C, 65 ± 4 % RH 기준.', ['s2'])]),
 ('마찰전기와 직물 센서', [
  ('Fan, F.-R., Tian, Z.-Q., & Wang, Z. L. (2012). Flexible triboelectric generator. <i>Nano Energy</i>, 1(2), 328–334.', 'https://doi.org/10.1016/j.nanoen.2012.01.004', '마찰전기 발전기(TENG)의 출발점. 정답 Y의 물리 배경.', ['s5']),
  ('Zou, H., Zhang, Y., Guo, L., et al. (2019). Quantifying the triboelectric series. <i>Nature Communications</i>, 10, 1427.', 'https://doi.org/10.1038/s41467-019-09461-x', '마찰전기 전하 밀도를 정해진 조건에서 재는 표준 방법. 측정 조건 정하기(S5-2).', ['s5']),
  ('Xiong, J., & Lee, P. S. (2019). Progress on wearable triboelectric nanogenerators in shapes of fiber, yarn, and textile. <i>Science and Technology of Advanced Materials</i>.', 'https://doi.org/10.1080/14686996.2019.1650396', '섬유·실·직물 형태 TENG 개관. 후보 구조 설계.', ['s5', 's6'])]),
 ('시뮬레이션과 Sim-to-Real', [
  ('Brown, L. P., Zeng, X., Long, A. C., & Jones, I. A. (2013). Recent developments in the realistic geometric modelling of textile structures using TexGen. 1st Int. Conf. on Digital Technologies for the Textile Industries, Manchester.', 'https://eprints.nottingham.ac.uk/3267/', 'TexGen 단위 구조 모델링. 시뮬레이션 실행 기록 양식.', ['s4']),
  ('Tobin, J., Fong, R., Ray, A., Schneider, J., Zaremba, W., & Abbeel, P. (2017). Domain randomization for transferring deep neural networks from simulation to the real world. <i>IROS 2017</i>, 23–30.', 'https://doi.org/10.1109/IROS.2017.8202133', '시뮬레이션 조건을 넓게 흔들어 실제로 옮기는 방법(계획서의 domain randomization).', ['s4', 's5']),
  ('Esteban, C., Hyland, S. L., & Rätsch, G. (2017). Real-valued (medical) time series generation with recurrent conditional GANs. arXiv:1706.02633.', 'https://arxiv.org/abs/1706.02633', '"가상으로 학습, 실측으로 시험(TSTR)" 평가 방법. 비교 검사표의 쓸모 항목.', ['s4'])]),
 ('모델과 해석', [
  ('Breiman, L. (2001). Random forests. <i>Machine Learning</i>, 45(1), 5–32.', 'https://doi.org/10.1023/A:1010933404324', '계획서의 예비 모델(랜덤포레스트).', ['s3']),
  ('Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. <i>KDD 2016</i>, 785–794.', 'https://doi.org/10.1145/2939672.2939785', '계획서의 예비 모델(XGBoost).', ['s3']),
  ('Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. <i>NeurIPS 2017</i>.', 'https://arxiv.org/abs/1705.07874', '변수 영향도(SHAP). 장치 개선 대상 변수 고르기.', ['s3', 's6']),
  ('Hair, J. F., Hult, G. T. M., Ringle, C. M., & Sarstedt, M. (2022). <i>A Primer on Partial Least Squares Structural Equation Modeling (PLS-SEM)</i> (3rd ed.). Sage.', None, '구조 → 물성 → 성능 경로 분석(S3-3).', ['s3']),
  ('Montgomery, D. C. <i>Design and Analysis of Experiments</i>. Wiley.', None, '실험계획법(요인·수준 배치).', ['s2'])]),
 ('1차년도 방법 검토 — 전기 특성·데이터 생성·전향 검증 (2026-11-17 추가)', [(c + f' <a href="method_review.html#{k}">[{k}]</a>', u, w, ['s3', 's4', 's5']) for k, c, u, w in MREFS if k not in ('M1', 'M11')]),
 ('데이터 품질과 검증', [
  ('Kapoor, S., & Narayanan, A. (2023). Leakage and the reproducibility crisis in machine-learning-based science. <i>Patterns</i>, 4(9), 100804.', 'https://doi.org/10.1016/j.patter.2023.100804', '데이터 누수 유형과 점검법. 원단 단위 교차검증 원칙의 근거.', ['s3']),
  ('Geirhos, R., Jacobsen, J.-H., Michaelis, C., et al. (2020). Shortcut learning in deep neural networks. <i>Nature Machine Intelligence</i>, 2, 665–673.', 'https://doi.org/10.1038/s42256-020-00257-z', '지름길 학습. 이미지 데이터 분석의 핵심 개념.', ['s1']),
  ('Gebru, T., Morgenstern, J., Vecchione, B., et al. (2021). Datasheets for datasets. <i>Communications of the ACM</i>, 64(12), 86–92.', 'https://doi.org/10.1145/3458723', '데이터 설명서 양식의 바탕.', ['s2', 's4']),
  ('Carney, M., Webster, B., Alvarado, I., et al. (2020). Teachable Machine: Approachable web-based tool for exploring machine learning classification. <i>CHI 2020 Extended Abstracts</i>.', 'https://doi.org/10.1145/3334480.3382839', '실습용 이미지 데이터셋이 쓰는 도구.', ['s1'])]),
]
INTERNAL = ['Kick off 문서 (2025-12-11)', '2026년도 핵심연구(유형B) 신규과제 연구계획서', 'AI 데이터셋 엑셀 (실 13종, 원단 27개, 측정 항목 73개)', '강의 「직물 태(Hand) 판정 AI 만들기」', '실습용 이미지 데이터셋 fabric_dataset (2026-09-22 생성, 140장)', 'Notion 「한양대 섬유 \'태\'」']
rh = ''; mdl = ['# 참고 레퍼런스 — 섬유 AI 연구 브리핑', '']; n = 0
for g, L in REFG:
    rh += f'<h2 style="margin-top:26px">{g}</h2><ol class="refl">'; mdl.append(f'## {g}')
    for cite, url, why, st in L:
        n += 1
        chips_ = ' '.join(f'<a class="st {SBY[s]["st"]}" href="{SBY[s]["file"]}" style="text-decoration:none">S{SBY[s]["n"]}</a>' for s in st)
        rh += f'<li><b>[R{n}]</b> {cite}' + (f' <a href="{url}" target="_blank" rel="noopener">링크</a>' if url else '') + f'<span class="why">이 연구에서: {why} {chips_}</span></li>'
        plain = re.sub(r'<[^>]+>', '', cite); mdl.append(f'- [R{n}] {plain}' + (f' {url}' if url else '') + f'  \n  이 연구에서: {why}')
    rh += '</ol>'; mdl.append('')
mdl += ['## 내부 자료'] + [f'- {x}' for x in INTERNAL]
ref_body = wrap(crumb(('index.html', 'INDEX'), (None, '참고 레퍼런스')) +
 '<h1 style="margin:4px 0 8px">참고 레퍼런스</h1><p class="lead">장비, 마찰전기, 시뮬레이션, 모델, 1차년도 방법 검토, 데이터 품질 여섯 갈래로 정리했습니다. 문헌마다 "이 연구에서 어디에 쓰는지"와 관련 스테이지를 달았습니다. 서지 정보는 2026-11-16에 검색으로 확인했습니다.</p>'
 + say('moa', 'report', '문헌 목록은 아래 단추로 .md 파일로 받으실 수 있습니다. 더 넣을 문헌은 부직이에게 요청해 주세요.') +
 '<div class="ctrl"><button class="bt primary" data-tpl="refs">참고문헌 목록 .md 내려받기</button><span class="small muted dlnote" aria-live="polite"></span></div>' + rh +
 '<h2 style="margin-top:26px">내부 자료</h2><ul>' + ''.join(f'<li>{x}</li>' for x in INTERNAL) + '</ul>'
 '<h2 style="margin-top:26px">더 찾아볼 문헌 <span class="st plan">예정</span></h2><ul>'
 '<li>직물 특성 수치(KES-FB·FTT 항목)를 입력으로 마찰전기 출력을 예측한 머신러닝 논문 — 이번 검토에서 찾지 못함, 계속 찾음</li>'
 '<li>KES-FB 값으로 태 점수를 예측한 머신러닝 논문 — S3 기준선 비교용</li>'
 '<li>직물 표면 이미지로 촉감을 예측한 연구 — 이미지 묶음을 더할지 정할 때</li></ul>')
sizes['references.html'] = page('references.html', '참고 레퍼런스', ref_body + tail((('data_guide.html', '가상 섬유 데이터 작성 가이드'), ('index.html', 'INDEX — 전체 연구 계획 정리'))), extra={'guide': {'refs': {'kind': 'md', 'file': 'references.md', 'text': '\n'.join(mdl)}}})
