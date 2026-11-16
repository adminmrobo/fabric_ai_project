# ---- 1차년도 연구 방법 검토 (2026-11-17 방향) ----
# build_pages.py 안에서 exec 로 실행된다 (page, wrap, tail, say, crumb, SBY, DIRBOX 등 공유)

MREFS = [
 # (키, 서지, 링크, 이 검토에서 쓰는 곳)
 ('M1', 'Zou, H., Zhang, Y., Guo, L., et al. (2019). Quantifying the triboelectric series. <i>Nature Communications</i>, 10, 1427.', 'https://doi.org/10.1038/s41467-019-09461-x', '마찰전기 전하 밀도를 정해진 조건(액체 금속 상대 전극, 통제된 환경)에서 재는 표준 방법 → 출력 Y를 "직물의 성질"로 만들려면 측정 조건을 고정해야 함.'),
 ('M2', 'Niu, S., Wang, S., Lin, L., et al. (2013). Theoretical study of contact-mode triboelectric nanogenerators as an effective power source. <i>Energy & Environmental Science</i>, 6, 3576–3583.', 'https://doi.org/10.1039/C3EE42571A', '접촉-분리형 TENG의 이론 모델(V–Q–x 관계) → 물리 방향 검사와 물리 기반 보조 데이터의 근거.'),
 ('M3', 'Bakhtiyari, S., Bagherzadeh, R., Ezazshahabi, N., Jahanshahi, A., Van Langenhove, L., & Malengier, B. (2024). Yarn-to-yarn surface area and roughness as structural engineering tools for optimizing the electrical output of triboelectric nanogenerators. <i>Advanced Materials Technologies</i>.', 'https://doi.org/10.1002/admt.202401346', '평직·능직·호프색 직물 TENG 비교. 능직 2/2와 호프색 2/2의 출력이 높았고 접촉 면적·거칠기로 설명 → 조직·표면 특성을 입력 X에 넣는 근거.'),
 ('M4', 'Jeong, J., Kwon, J.-H., Lim, K., Biswas, S., Tibaldi, A., et al. (2019). Comparative study of triboelectric nanogenerators with differently woven cotton textiles for wearable electronics. <i>Polymers</i>, 11(9), 1443.', 'https://www.mdpi.com/2073-4360/11/9/1443', '같은 면이라도 2/1 능직이 평직보다 출력 전압이 높음 → 소재가 같아도 조직이 Y를 바꿈.'),
 ('M5', '(2023). The effect of ambient humidity on the performance of a wearable textile triboelectric generator. <i>Energy Technology</i>, 11(7).', None, '싱글 저지 편직물 6종으로 습도 영향을 잰 연구 → 측정 환경(습도)을 Y와 함께 기록해야 함. (저자·DOI 확인 필요)'),
 ('M6', 'Jiang, M., Li, B., Jia, W., & Zhu, Z. (2022). Predicting output performance of triboelectric nanogenerators using deep learning model. <i>Nano Energy</i>, 106830.', 'https://doi.org/10.1016/j.nanoen.2021.106830', '실험하지 않은 파라미터 범위의 TENG 출력을 신경망으로 예측 → 이 연구와 같은 "설계 변수 → 출력" 회귀의 선례. 다만 소자 구조 변수이고 직물 특성은 아님.'),
 ('M7', 'Uddin, M. A., Lim, M., Kim, R., Burgess, B. L., et al. (2025). Machine learning-driven surrogate modeling for optimization of triboelectric nanogenerator design parameters. <i>Advanced Electronic Materials</i>.', 'https://doaj.org/article/e2c2d215853748efa5afa81c2825dac9', '두께·기공률·힘·주파수 4변수를 실험계획법으로 잡고 회귀 대리모델 구축 → 실험계획 + 회귀 대리모델 구성의 선례.'),
 ('M8', '(2025). Interpretable machine learning for evaluating nanogenerators\' structural design. <i>ACS Nano</i>. (저자 확인 필요)', 'https://doi.org/10.1021/acsnano.5c02525', '신경망 대리모델과 해석 기법으로 TENG 구조 변수의 영향을 평가 → 변수 영향도(SHAP) 단계의 선례.'),
 ('M9', 'Xu, P., Ji, X., Li, M., & Lu, W. (2023). Virtual sample generation in machine learning assisted materials design and discovery. <i>Journal of Materials Informatics</i>, 3(3), 16.', 'https://doi.org/10.20517/jmi.2023.18', '소표본 재료 연구의 가상 샘플 생성(VSG) 리뷰. 실험으로 확인되지 않은 가상 샘플은 "미지 샘플"이며, 분포를 넓혀 학습하거나 설계·예측 대상으로 쓰인다 → 이번 방향의 정확한 이름.'),
 ('M10', 'Xu, L., Skoularidou, M., Cuesta-Infante, A., & Veeramachaneni, K. (2019). Modeling tabular data using conditional GAN. <i>NeurIPS 2019</i>.', 'https://arxiv.org/abs/1907.00503', '표 데이터 생성 모델 CTGAN·TVAE → 생성 방식 후보. 논문 스스로 표 데이터 생성이 기본 방법보다 못한 지표가 있다고 밝힘.'),
 ('M11', 'Esteban, C., Hyland, S. L., & Rätsch, G. (2017). Real-valued (medical) time series generation with recurrent conditional GANs. arXiv:1706.02633.', 'https://arxiv.org/abs/1706.02633', '"생성 데이터로 학습, 실측으로 시험(TSTR)" 평가 → 생성 데이터를 쓴 모델도 점수는 실측으로만.'),
 ('M12', 'Shumailov, I., Shumaylov, Z., Zhao, Y., Papernot, N., Anderson, R., & Gal, Y. (2024). AI models collapse when trained on recursively generated data. <i>Nature</i>, 631, 755–759.', 'https://doi.org/10.1038/s41586-024-07566-y', '생성 데이터를 무분별하게 다시 학습하면 원래 분포의 꼬리가 사라지는 "모델 붕괴" — 가우시안 혼합·VAE에서도 발생 → 생성 Y로 재학습하지 않는 원칙의 근거.'),
 ('M13', 'Zhou, Z.-H., & Li, M. (2005). Semi-supervised regression with co-training. <i>IJCAI 2005</i>, 908–916. / (2007). Semisupervised regression with cotraining-style algorithms. <i>IEEE TKDE</i>, 19(11), 1479–1493.', 'https://mlanthology.org/ijcai/2005/zhou2005ijcai-semi', '정답 없는 예제에 예측값을 붙여 회귀를 돕는 준지도 회귀(COREG). 저자들도 정답 없는 데이터 활용이 늘 이롭지는 않다고 지적 → "비지도"가 아니라 "준지도"의 영역.'),
 ('M14', 'Lookman, T., Balachandran, P. V., Xue, D., & Yuan, R. (2019). Active learning in materials science with emphasis on adaptive sampling using uncertainties for targeted design. <i>npj Computational Materials</i>, 5, 21.', 'https://doi.org/10.1038/s41524-019-0153-8', '불확실도로 다음 실험을 고르는 능동 학습 → 생성 직물 중 실제로 만들 후보 고르기(S5).'),
 ('M15', 'Dong, K., Peng, X., & Wang, Z. L. (2020). Fiber/fabric-based piezoelectric and triboelectric nanogenerators for flexible/stretchable and wearable electronics and artificial intelligence. <i>Advanced Materials</i>, 32(5), e1902549.', None, '섬유·직물 기반 나노발전기 종합 리뷰 → 직물 TENG의 구조·소재 변수 목록의 배경.'),
]
MR = {k: (c, u, w) for k, c, u, w in MREFS}
def mc(*ks): return '<sup>' + ','.join(f'<a href="#{k}">{k}</a>' for k in ks) + '</sup>'

flow_svg = '''<svg viewBox="0 -6 960 276" role="img" aria-label="1차년도 흐름: 직물 특성과 전기 특성 실측, 지도 회귀, 분포 학습으로 가상 직물 생성, 예측, 일부 실측 검증" style="width:100%;height:auto">
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#16212b"/></marker></defs>
<g font-family="sans-serif" font-size="14">
<rect x="10" y="20" width="180" height="62" rx="10" fill="#eaf1fb" stroke="#2f5d9e" stroke-width="2"/><text x="100" y="46" text-anchor="middle" font-weight="700">① 직물 특성 X 측정</text><text x="100" y="66" text-anchor="middle" font-size="12">실·조직·밀도·두께·표면…</text>
<rect x="10" y="120" width="180" height="62" rx="10" fill="#fff4e5" stroke="#a35c00" stroke-width="2"/><text x="100" y="146" text-anchor="middle" font-weight="700">② 전기 특성 Y 실측</text><text x="100" y="166" text-anchor="middle" font-size="12">전압·전류·전하밀도</text>
<rect x="260" y="70" width="190" height="62" rx="10" fill="#e8f5ee" stroke="#13733a" stroke-width="2"/><text x="355" y="96" text-anchor="middle" font-weight="700">③ 회귀 모델 f(X)→Y</text><text x="355" y="116" text-anchor="middle" font-size="12" fill="#13733a">지도학습 (실측 정답)</text>
<rect x="260" y="200" width="190" height="62" rx="10" fill="#f1ecfb" stroke="#6f5aa8" stroke-width="2"/><text x="355" y="226" text-anchor="middle" font-weight="700">④ 가상 직물 X′ 생성</text><text x="355" y="246" text-anchor="middle" font-size="12" fill="#6f5aa8">분포 학습 = 비지도</text>
<rect x="520" y="130" width="200" height="62" rx="10" fill="#fff" stroke="#16212b" stroke-width="2"/><text x="620" y="156" text-anchor="middle" font-weight="700">⑤ 예측 Ŷ′ = f(X′)</text><text x="620" y="176" text-anchor="middle" font-size="12" fill="#c9302c">정답 없음 · 불확실도 함께</text>
<rect x="770" y="130" width="180" height="62" rx="10" fill="#fdecec" stroke="#c9302c" stroke-width="2"/><text x="860" y="156" text-anchor="middle" font-weight="700">⑥ 일부 제작·측정</text><text x="860" y="176" text-anchor="middle" font-size="12">전향 검증 (능동 학습)</text>
<path d="M190,51 L258,92" stroke="#16212b" stroke-width="2" marker-end="url(#ah)" fill="none"/><path d="M190,151 L258,112" stroke="#16212b" stroke-width="2" marker-end="url(#ah)" fill="none"/>
<path d="M100,182 C100,232 200,231 258,231" stroke="#6f5aa8" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#ah)" fill="none"/><text x="120" y="250" font-size="12" fill="#6f5aa8">실측 원단의 X 분포</text>
<path d="M450,101 L518,150" stroke="#16212b" stroke-width="2" marker-end="url(#ah)" fill="none"/><path d="M450,231 L518,172" stroke="#16212b" stroke-width="2" marker-end="url(#ah)" fill="none"/>
<path d="M720,161 L768,161" stroke="#16212b" stroke-width="2" marker-end="url(#ah)" fill="none"/>
<path d="M860,130 C860,-6 130,-10 110,18" stroke="#c9302c" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#ah)" fill="none"/>
<text x="560" y="58" text-anchor="middle" font-size="12" fill="#c9302c">측정한 원단은 실측 데이터(①②)로 들어가 모델을 다시 학습</text>
</g></svg>'''

type_rows = [
 ('③ 실측 원단으로 X → Y 회귀', '<b>지도학습</b>', '실측 Y가 정답으로 붙어 있음', '원단 단위 교차검증으로 성적을 잼'),
 ('④ 가상 직물 X′ 생성', '<b>비지도</b> (분포 학습)', 'X의 분포만 배우고 정답은 쓰지 않음', '실측 분포와 비교, 범위 밖 차단, 제작 가능성 확인'),
 ('⑤ 생성 직물의 Ŷ′ 예측', '학습이 아니라 <b>추론</b>', '정답이 없음 — 실험 전에는 "미지 샘플"' + mc('M9'), '불확실도, 물리 방향 검사, ⑥ 실측 확인'),
 ('(하지 말 것) Ŷ′을 정답처럼 다시 학습', '<b>준지도</b> (자기 학습)' + mc('M13'), '모델이 붙인 예측값을 정답으로 씀', '새 정보가 없고, 거듭하면 분포의 꼬리가 사라짐' + mc('M12')),
 ('⑥ 일부 제작·측정 후 재학습', '<b>능동 학습</b>' + mc('M14'), '불확실도로 고른 원단에 진짜 정답이 붙음', '측정 한 번으로 모델이 가장 많이 배우는 원단을 고름'),
]
typet = '<div class="tw"><table class="tb"><tr><th>단계</th><th>학습 유형</th><th>정답(Y)의 출처</th><th>어떻게 믿나</th></tr>' + ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in type_rows) + '</table></div>'

lit_rows = [
 ('직물 구조가 전기 출력을 바꾸나', '같은 소재라도 조직(평직·능직·호프색)과 접촉 면적·거칠기에 따라 출력이 달라짐이 실험으로 보고됨.', '입력 X에 조직·밀도·표면 거칠기·압축 특성을 넣는 근거가 있음.', 'M3 M4 M15'),
 ('전기 특성 Y는 무엇에 좌우되나', '마찰전기 전하 밀도는 상대 물질·측정 조건에 따라 달라져, 표준화된 조건(액체 금속 상대 전극 등)에서 재는 방법이 제안됨. 습도도 출력에 영향.', 'Y를 "직물의 성질"로 쓰려면 접촉 모드·상대 물질·힘·주파수·온습도를 고정해야 함.', 'M1 M5'),
 ('물리 이론이 있나', '접촉-분리형 TENG의 V–Q–x 이론 모델이 있음.', '예측이 물리 방향(접촉 면적·전하 밀도 ↑ → 출력 ↑)과 맞는지 검사하는 기준. 물리 기반 보조 데이터의 바탕.', 'M2'),
 ('ML로 TENG 출력을 예측한 선례', '신경망·회귀 대리모델로 TENG 출력을 예측하고 설계를 최적화한 연구들이 있음. 대부분 소자 구조·공정 변수(두께·기공률·힘·주파수 등)이고, 직물 특성 수치를 입력으로 한 사례는 드묾.', '"설계 변수 → 출력" 회귀 구성은 선례가 있음. "직물 특성 → 전기 특성"은 이 과제의 새로운 부분.', 'M6 M7 M8'),
 ('적은 실측으로 데이터를 생성하는 방법', '재료 분야에서 가상 샘플 생성(VSG)이 소표본 문제의 대표 전략으로 정리됨. 표 데이터 생성 모델(CTGAN·TVAE)도 있음. 보고된 큰 성능 향상은 실측 시험 세트를 따로 두었는지 확인하고 읽어야 함.', '생성은 가능하고 흔한 방법. 다만 생성 데이터의 효과는 실측으로 재야 함.', 'M9 M10 M11'),
 ('생성 데이터를 다시 학습하면', '모델이 만든 데이터를 거듭 학습하면 원래 분포의 꼬리가 사라지는 "모델 붕괴"가 가우시안 혼합·VAE에서도 보고됨. 준지도 회귀 연구도 정답 없는 데이터 활용이 늘 이롭지는 않다고 지적.', '생성 Y를 정답처럼 재학습하지 않음. 생성은 X에만, 정답은 실측에서만.', 'M12 M13'),
 ('정답 없는 예측을 어떻게 믿나', '불확실도로 다음 실험을 고르는 능동 학습이 재료 탐색에서 정리됨.', '생성 직물 중 예측 최고·불확실도 최고 후보를 실제로 만들어 재는 전향 검증.', 'M14'),
]
litt = '<div class="tw"><table class="tb"><tr><th>질문</th><th>문헌이 보여 주는 것</th><th>이 과제에 주는 뜻</th><th>문헌</th></tr>' + ''.join(
    f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>' + ' '.join(f'<a href="#{k}">{k}</a>' for k in d.split()) + '</td></tr>' for a, b, c, d in lit_rows) + '</table></div>'

risk_rows = [
 ('높음', '생성 Y를 정답처럼 재학습', '실측에 없는 정보가 생기지 않는데 성적·불확실도만 좋아 보임. 거듭하면 분포 꼬리 소실' + mc('M12'), '생성은 X에만. 생성 데이터를 쓴 모델도 점수는 실측 원단으로만(TSTR)' + mc('M11')),
 ('높음', 'Y 측정 조건이 흔들림', '같은 원단도 상대 물질·힘·습도에 따라 출력이 달라져, 모델이 직물이 아니라 측정 조건을 배움' + mc('M1', 'M5'), '측정 프로토콜 고정, 반복 측정 변동계수 기록, 온습도를 열로 남김'),
 ('중간', '생성 직물이 실측 범위를 벗어남', '회귀 모델은 본 적 없는 영역에서 근거 없이 외삽', '적용 범위 검사(실측 최근접 거리), 범위 밖은 "탐색 후보"로만 표시, 불확실도 함께 보고'),
 ('중간', '만들 수 없는 직물을 생성', '특성 조합이 물리적으로 불가능(예: 얇은데 매우 무거움)', '실험실이 정한 제약 규칙으로 거르고, 생성 직물 일부를 실제로 제작'),
 ('중간', '원단 수에 비해 특성이 많음', '27개 원단 × 19항목이면 교차검증 R²가 음수로 나올 수 있음(S3 모의실험)', '핵심 특성 10개 안팎으로 줄이고, 실험계획으로 원단 50~100개'),
]
riskt = '<div class="tw"><table class="tb"><tr><th>위험도</th><th>위험</th><th>왜 문제인가</th><th>대응</th></tr>' + ''.join(
    f'<tr><td><span class="st {"draft" if a=="높음" else "part"}">{a}</span></td><td><b>{b}</b></td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in risk_rows) + '</table></div>'

proto = '''<ol class="steps1">
<li><b>Y 측정 표준 정하기 (S0·S2)</b> — 접촉 모드, 상대 물질, 누르는 힘·주파수, 온습도. 원단마다 3회 이상 반복하고 변동계수를 남깁니다.</li>
<li><b>X·Y 실측 (S2)</b> — 실험계획으로 원단 50~100개. 한 요인만 다른 짝을 남겨 조직·밀도의 효과를 따로 볼 수 있게 합니다.</li>
<li><b>회귀 모델 (S3)</b> — 기준선 → 트리 앙상블 → 가우시안 과정. 원단 단위 교차검증. 불확실도를 내는 모델을 하나 이상 둡니다.</li>
<li><b>가상 직물 생성 (S4)</b> — X만 생성. 실측 분포 비교, 범위 밖 차단, 실험실 제약 규칙으로 거르기.</li>
<li><b>예측과 후보 선정 (S5)</b> — 생성 직물마다 Ŷ′ ± 불확실도. 예측 최고 후보와 불확실도 최고 후보를 섞어 10개 이상 고릅니다.</li>
<li><b>전향 검증과 반복 (S5)</b> — 고른 원단을 실제로 만들어 재고, 예측을 먼저 적어 둔 값과 비교한 뒤 실측 데이터에 넣어 다시 학습합니다.</li>
</ol>'''

sim = '''<div class="panel" id="mrsim"><h4>모의실험 — 생성 데이터를 다시 학습하면 무엇이 달라지나 <span class="stampnote">설명용 모형 · 가상 데이터</span></h4>
<p class="small">가로축은 직물 특성 하나(예: 표면 거칠기 지표), 세로축은 전기 특성(예: 출력 전압)이라고 보십시오. 진짜 관계(회색 점선)는 모의실험이라서 알 뿐, 실제 연구에서는 모릅니다. 남색 점이 실측 원단 20개, 회귀 모델은 가우시안 과정입니다.</p>
<div class="ctrl"><div class="group" role="group" aria-label="방식"><button type="button" class="bt" data-mrm="real" aria-pressed="true">① 실측만</button><button type="button" class="bt" data-mrm="pred" aria-pressed="false">② 생성 X → 예측만</button><button type="button" class="bt" data-mrm="self" aria-pressed="false">③ 생성 Y로 재학습</button></div></div>
<div class="ctrl"><div class="group"><span class="glabel">생성 직물 수</span><input type="range" id="mrN" min="0" max="200" step="10" value="80" aria-label="생성 직물 수"><span class="val" id="mrNv">80</span></div>
<div class="group" role="group" aria-label="생성 범위"><button type="button" class="bt sm" data-mrr="in" aria-pressed="true">실측 범위 안</button><button type="button" class="bt sm" data-mrr="out" aria-pressed="false">범위 밖까지</button></div></div>
<canvas id="mrCv" style="width:100%;height:340px;display:block" aria-label="모의실험 그림"></canvas>
<div class="kpis" style="margin-top:10px"><div class="kpi g"><b id="mrR">–</b><span>실측 시험 원단 RMSE (낮을수록 좋음)</span></div><div class="kpi i"><b id="mrSi">–</b><span>범위 안 평균 불확실도 ±2σ</span></div><div class="kpi a"><b id="mrSo">–</b><span>범위 밖 평균 불확실도 ±2σ</span></div></div>
<p class="small" id="mrMsg" aria-live="polite"></p></div>
<script>
(function(){
var cv=document.getElementById('mrCv');if(!cv)return;
function rng(s){return function(){s=(s*1664525+1013904223)%4294967296;return s/4294967296}}
function gauss(r){var u=r()||1e-9,v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v)}
function truth(x){return 2+3*x+1.2*Math.sin(7*x)}
var r=rng(11),SN=0.35,L=0.14,SF=1.6,LO=0.08,HI=0.68;
var XR=[],YR=[],XT=[],YT=[];
for(var i=0;i<20;i++){var x=LO+(HI-LO)*(i+r())/20;XR.push(x);YR.push(truth(x)+SN*gauss(r))}
for(var i=0;i<40;i++){var x=LO+(HI-LO)*(i+.5)/40;XT.push(x);YT.push(truth(x)+SN*gauss(r))}
function k(a,b){var d=a-b;return SF*SF*Math.exp(-d*d/(2*L*L))}
function gp(X,Y,noise){var n=X.length,K=[],i,j;var m=Y.reduce(function(a,b){return a+b},0)/n;
 for(i=0;i<n;i++){K.push([]);for(j=0;j<n;j++)K[i].push(k(X[i],X[j])+(i===j?noise[i]*noise[i]:0))}
 var Lc=[];for(i=0;i<n;i++){Lc.push(new Array(n).fill(0));for(j=0;j<=i;j++){var s=K[i][j];for(var q=0;q<j;q++)s-=Lc[i][q]*Lc[j][q];Lc[i][j]=i===j?Math.sqrt(Math.max(s,1e-12)):s/Lc[j][j]}}
 function solve(b){var z=new Array(n),x=new Array(n),i,q;for(i=0;i<n;i++){var s=b[i];for(q=0;q<i;q++)s-=Lc[i][q]*z[q];z[i]=s/Lc[i][i]}for(i=n-1;i>=0;i--){var s=z[i];for(q=i+1;q<n;q++)s-=Lc[q][i]*x[q];x[i]=s/Lc[i][i]}return x}
 function fsub(b){var z=new Array(n);for(var i=0;i<n;i++){var s=b[i];for(var q=0;q<i;q++)s-=Lc[i][q]*z[q];z[i]=s/Lc[i][i]}return z}
 var al=solve(Y.map(function(y){return y-m}));
 return function(x){var ks=X.map(function(xi){return k(x,xi)});var mu=m;for(var i=0;i<n;i++)mu+=ks[i]*al[i];var v=fsub(ks),vv=SF*SF;for(var i=0;i<n;i++)vv-=v[i]*v[i];return [mu,Math.sqrt(Math.max(vv,1e-9))]}}
var mode='real',N=80,rg='in';
function gen(){var g=rng(29),X=[];for(var i=0;i<N;i++){if(rg==='in'){var b=XR[Math.floor(g()*XR.length)];X.push(Math.min(HI,Math.max(LO,b+0.04*gauss(g))))}else X.push(g()*1.0)}return X}
function draw(){
 var W=cv.clientWidth||700,H=340,d=window.devicePixelRatio||1;cv.width=W*d;cv.height=H*d;var c=cv.getContext('2d');c.setTransform(d,0,0,d,0,0);c.clearRect(0,0,W,H);
 var pl=46,pr=12,pt=12,pb=34,y0=0.5,y1=6.5;function px(x){return pl+x*(W-pl-pr)}function py(y){return pt+(1-(y-y0)/(y1-y0))*(H-pt-pb)}
 c.fillStyle='#fff7e8';c.fillRect(px(HI),pt,px(1)-px(HI),H-pt-pb);c.fillRect(px(0),pt,px(LO)-px(0),H-pt-pb);
 c.fillStyle='#a35c00';c.font='12px sans-serif';c.fillText('실측 범위 밖',px(HI)+6,pt+14);
 c.strokeStyle='#d5dbe2';c.beginPath();c.moveTo(pl,pt);c.lineTo(pl,H-pb);c.lineTo(W-pr,H-pb);c.stroke();
 c.fillStyle='#5b6874';c.fillText('직물 특성 X →',W-pr-90,H-10);c.save();c.translate(14,pt+120);c.rotate(-Math.PI/2);c.fillText('전기 특성 Y →',0,0);c.restore();
 var XG=gen(),Xtr=XR.slice(),Ytr=YR.slice(),nz=XR.map(function(){return SN});
 var f0=gp(XR,YR,nz),f=f0,GY=XG.map(function(x){return f0(x)[0]});
 if(mode==='self'&&N>0){Xtr=Xtr.concat(XG);Ytr=Ytr.concat(GY);nz=nz.concat(XG.map(function(){return SN}));f=gp(Xtr,Ytr,nz)}
 c.fillStyle='rgba(19,115,58,.13)';c.beginPath();var i,x;for(i=0;i<=200;i++){x=i/200;var p=f(x);c.lineTo(px(x),py(p[0]+2*p[1]))}for(i=200;i>=0;i--){x=i/200;var p=f(x);c.lineTo(px(x),py(p[0]-2*p[1]))}c.fill();
 c.setLineDash([5,4]);c.strokeStyle='#8a96a3';c.lineWidth=1.5;c.beginPath();for(i=0;i<=200;i++){x=i/200;c.lineTo(px(x),py(truth(x)))}c.stroke();c.setLineDash([]);
 c.strokeStyle='#13733a';c.lineWidth=2.5;c.beginPath();for(i=0;i<=200;i++){x=i/200;c.lineTo(px(x),py(f(x)[0]))}c.stroke();c.lineWidth=1;
 if(mode!=='real'){XG.forEach(function(x,j){var p=f(x),yy=mode==='self'?GY[j]:p[0];c.fillStyle='rgba(111,90,168,.75)';c.beginPath();c.arc(px(x),py(yy),3,0,7);c.fill();
   if(mode==='pred'&&j%4===0){c.strokeStyle='rgba(111,90,168,.5)';c.beginPath();c.moveTo(px(x),py(p[0]-2*p[1]));c.lineTo(px(x),py(p[0]+2*p[1]));c.stroke()}})}
 c.fillStyle='#2f5d9e';XR.forEach(function(x,j){c.beginPath();c.arc(px(x),py(YR[j]),4.5,0,7);c.fill()});
 var se=0;XT.forEach(function(x,j){var e=f(x)[0]-YT[j];se+=e*e});var rm=Math.sqrt(se/XT.length);
 var si=0,so=0,ni=0,no=0;for(i=0;i<=100;i++){x=i/100;var s=2*f(x)[1];if(x>=LO&&x<=HI){si+=s;ni++}else{so+=s;no++}}
 document.getElementById('mrR').textContent=rm.toFixed(2);document.getElementById('mrSi').textContent=(si/ni).toFixed(2);document.getElementById('mrSo').textContent=(so/no).toFixed(2);
 var base=(function(){var s=0;XT.forEach(function(x,j){var e=f0(x)[0]-YT[j];s+=e*e});return Math.sqrt(s/XT.length)})();
 var msg={real:'실측 원단 20개만으로 배운 상태입니다. 초록 띠(±2σ)가 범위 밖에서 넓어집니다. 모델이 "여기는 모른다"고 말하는 것입니다.',
  pred:'생성 직물(보라)은 예측만 받았습니다. 모델은 그대로라서 실측 시험 RMSE가 ① 실측만과 같습니다('+base.toFixed(2)+'). 범위 밖 생성 직물은 세로 막대(불확실도)가 길어, 실제로 만들어 확인할 후보가 됩니다.',
  self:'생성 직물에 모델의 예측값을 정답처럼 붙여 다시 배웠습니다. 실측 시험 RMSE는 '+base.toFixed(2)+' → '+rm.toFixed(2)+'로 거의 그대로이거나 나빠지는데, 불확실도 띠는 좁아집니다. 새 정보 없이 자신감만 커진 상태입니다.'}[mode];
 document.getElementById('mrMsg').textContent=msg}
function press(sel,attr,val){document.querySelectorAll(sel).forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute(attr)===val?'true':'false')})}
document.querySelectorAll('[data-mrm]').forEach(function(b){b.addEventListener('click',function(){mode=b.getAttribute('data-mrm');press('[data-mrm]','data-mrm',mode);draw()})});
document.querySelectorAll('[data-mrr]').forEach(function(b){b.addEventListener('click',function(){rg=b.getAttribute('data-mrr');press('[data-mrr]','data-mrr',rg);draw()})});
var sl=document.getElementById('mrN');sl.addEventListener('input',function(){N=+sl.value;document.getElementById('mrNv').textContent=N;draw()});
window.addEventListener('resize',draw);draw();
})();
</script>'''

refl = '<ol class="refl">' + ''.join(f'<li id="{k}"><b>[{k}]</b> {c}' + (f' <a href="{u}" target="_blank" rel="noopener">링크</a>' if u else '') + f'<span class="why">이 검토에서: {w}</span></li>' for k, c, u, w in MREFS) + '</ol>'

mr_body = wrap(crumb(('index.html', 'INDEX'), (None, '1차년도 연구 방법 검토')) +
 '<h1 style="margin:4px 0 8px">1차년도 연구 방법 검토 — 직물 특성 → 실측 전기 특성 → 생성 → 예측</h1>'
 '<p class="lead">2026-11-17에 정한 1차년도 진행 방향을 논문·문헌으로 검토했습니다. 이 방법이 지도학습과 비지도학습 중 어디에 가까운지, 문헌이 말하는 위험은 무엇인지, 정답이 없는 예측을 어떻게 믿을 수 있게 만들지를 차례로 보고드립니다. 문헌 서지는 2026-11-17에 웹 검색으로 확인했습니다.</p>'
 '<div class="brief"><div class="bh">핵심 보고</div><dl>'
 '<dt>결론</dt><dd>방향은 문헌으로 뒷받침되는 실행 가능한 방법입니다. 다만 정확히는 "비지도 학습"이 아니라 <b>실측 정답으로 배우는 지도 회귀 + 실측 근거 가상 샘플 생성(VSG) + 일부 실측 검증</b>입니다. 생성 단계만 비지도(분포 학습)이고, 생성 직물의 예측은 실험 전까지 검증되지 않은 예측입니다.</dd>'
 '<dt>근거</dt><dd>직물 조직·표면이 마찰전기 출력을 바꾼다는 실험 보고' + mc('M3', 'M4') + ', TENG 출력 회귀 선례' + mc('M6', 'M7', 'M8') + ', 재료 분야 가상 샘플 생성 리뷰' + mc('M9') + ', 생성 데이터 재학습의 위험' + mc('M12') + '.</dd>'
 '<dt class="ask">요청</dt><dd>① 생성은 직물 특성 X에만 하고 생성 Y로 재학습하지 않는 원칙, ② 전기 특성 측정 조건 고정, ③ 생성 직물 10개 이상 실제 제작·측정을 승인해 주십시오.</dd></dl></div>'
 + DIRBOX +
 say('asst', 'report', '교수님, 바뀐 방향을 한 장 그림으로 먼저 보고드립니다. 색은 학습 유형입니다. 초록은 지도, 보라는 비지도, 빨강은 정답 없는 예측과 그 검증입니다.') +
 '<div class="panel">' + flow_svg + '</div>') + \
 wrap('<h2 id="type">1. 지도학습인가, 비지도학습인가</h2>'
 '<p>"실제 정답이 있는 것이 아니라 비지도 학습에 가깝다"는 판단에는 맞는 부분과 다른 부분이 함께 있습니다. 단계별로 나누면 분명해집니다.</p>' + typet +
 '<div class="talk"><p class="th">질의응답</p>' +
 say('sia', 'think', '생성 직물에는 정답이 없으니 전체가 비지도 학습 아닙니까?') +
 say('asst', 'report', '모델이 배우는 재료는 실측 원단의 X와 Y입니다. 정답이 붙은 데이터로 배우므로 회귀 단계는 지도학습입니다. 정답이 없는 것은 "생성 직물에 대한 예측"이고, 이것은 학습이 아니라 추론입니다. 재료 분야 리뷰는 실험으로 확인하기 전의 가상 샘플을 "미지 샘플"이라고 부릅니다.' + mc('M9')) +
 say('moa', 'report', '그래서 이름은 "실측 지도 회귀 + 가상 샘플 생성 + 전향 검증"으로 정리하는 안을 올립니다. 생성 단계(분포 학습)만 비지도입니다.') + '</div>') + \
 wrap('<h2 id="lit">2. 문헌 검토 — 질문별로</h2>' + litt +
 say('asst', 'report', '직물 특성 → 전기 특성을 머신러닝으로 예측한 연구는 아직 드뭅니다. 선례 대부분은 소자 구조·공정 변수입니다. 이 점이 과제의 새로운 부분이자, 측정 표준이 더 중요한 이유입니다.')) + \
 wrap('<h2 id="risk">3. 위험과 대응</h2>' + riskt) + \
 wrap('<h2 id="sim">4. 모의실험으로 보는 핵심 위험</h2>' + sim +
 '<div class="talk"><p class="th">질의응답</p>' +
 say('sia', 'think', '③에서 띠가 좁아지면 모델이 더 정확해진 것 아닙니까?') +
 say('asst', 'firm', '아닙니다. 실측 시험 원단으로 잰 오차는 그대로입니다. 모델이 자기 예측을 정답으로 다시 배워 자신감만 커졌습니다. 그래서 생성 데이터를 쓴 모델도 점수는 실측으로만 재겠습니다.' + mc('M11')) + '</div>') + \
 wrap('<h2 id="proto">5. 제안 절차 — 6단계</h2>' + proto +
 '<p class="small">S2~S5 스테이지 쪽에 같은 내용이 단계별로 들어가 있습니다: ' + ' · '.join(f'<a href="{SBY[k]["file"]}">S{SBY[k]["n"]} {SBY[k]["name"]}</a>' for k in ['s2', 's3', 's4', 's5']) + '</p>'
 '<div class="review" id="review-mr" data-rev="mr"></div>') + \
 wrap('<h2 id="mrefs">검토 문헌</h2><p class="small muted">논문 원문을 모두 읽은 것은 아니며, 초록·서지 정보와 검색 결과로 확인한 범위에서 인용했습니다. "확인 필요" 표시는 서지 일부를 더 확인해야 하는 항목입니다.</p>' + refl)

sizes['method_review.html'] = page('method_review.html', '1차년도 연구 방법 검토', mr_body + tail((('references.html', '참고 레퍼런스'), ('index.html', 'INDEX — 전체 연구 계획 정리'))))
