# ---- 웹 슬라이드: 섬유직물 데이터 생성·검증·실습 가이드 (slides/index.html) ----
# build_pages.py 안에서 pages_method.py, pages_mock.py 다음에 exec 로 실행된다.
import json as _sj, numpy as _np, pandas as _pd, html as _html
from sklearn.mixture import GaussianMixture as _GMM

_PR = os.path.join(B, '..', 'practice')
_tr = _pd.read_csv(os.path.join(_PR, 'data', '02_train.csv'))
_gen = _pd.read_csv(os.path.join(_PR, 'data', '04_generated_candidates_example.csv'))
_ks = _pd.read_csv(os.path.join(_PR, 'data', '05_ks_example.csv'), encoding='utf-8-sig')
_tstr = _pd.read_csv(os.path.join(_PR, 'data', '05_tstr_result_example.csv'))
_base = _pd.read_csv(os.path.join(_PR, 'data', '05_baseline_scores_example.csv'))
_ver = _pd.read_csv(os.path.join(_PR, 'data', '07_verification_result_example.csv'))
_qc = _pd.read_csv(os.path.join(_PR, 'data', '03_qc_report_example.csv'), encoding='utf-8-sig')
_tmpl = _pd.read_csv(os.path.join(_PR, 'data', '00_measurement_template.csv'))
_X19 = ["W", "SFC_F", "SFC_B", "SRA_F", "SRA_B", "SRW_F", "SRW_B", "BAR_F", "BAR_B", "BW_FL", "BW_FC", "BW_BL", "BW_BC", "CW_F", "CW_B", "CRR_F", "CRR_B", "Qmax_F", "Qmax_B"]
_X8 = ["W", "SFC_F", "SRA_F", "SRW_F", "BAR_F", "CW_F", "CRR_F", "Qmax_F"]

# PCA (학습 자료, 로그·표준화)
_Z = _np.log(_tr[_X19].values); _Z = (_Z - _Z.mean(0)) / _Z.std(0, ddof=1)
_U, _s, _Vt = _np.linalg.svd(_Z, full_matrices=False)
_ev = (_s ** 2 / (_s ** 2).sum())[:3]
_W = _Vt[:2].T
if _W[:, 0].sum() < 0: _W[:, 0] *= -1
if _W[:, 1].sum() < 0: _W[:, 1] *= -1
_P = _Z @ _W

# 역방향 (Lab 7과 같은 방식) — 목표 30/60/90 V
_cols = _X8 + ["Voc_V"]; _L = _np.log(_tr[_cols].values); _mu, _sd = _L.mean(0), _L.std(0, ddof=1); _ZZ = (_L - _mu) / _sd
_g = _GMM(4, covariance_type='full', random_state=0, n_init=5).fit(_ZZ)
_full = _pd.read_csv(os.path.join(_PR, 'data', '01_mock_full.csv'))
_Lf = _np.log(_full[_X8].values); _Zf = (_Lf - _Lf.mean(0)) / _Lf.std(0, ddof=1)
_inv = {}
for _t in (30, 60, 90):
    yz = (_np.log(_t) - _mu[-1]) / _sd[-1]
    w = _np.array([_g.weights_[k] * _np.exp(-0.5 * (yz - _g.means_[k][-1]) ** 2 / _g.covariances_[k][-1, -1]) / _np.sqrt(_g.covariances_[k][-1, -1]) for k in range(4)]); w /= w.sum()
    rng = _np.random.default_rng(3); cnt = {}
    for i in range(200):
        k = rng.choice(4, p=w); m, S = _g.means_[k], _g.covariances_[k]
        Sxy, Syy = S[:-1, -1], S[-1, -1]
        x = rng.multivariate_normal(m[:-1] + Sxy / Syy * (yz - m[-1]), S[:-1, :-1] - _np.outer(Sxy, Sxy) / Syy)
        xr = _np.exp(x * _sd[:-1] + _mu[:-1]); zf = (_np.log(xr) - _Lf.mean(0)) / _Lf.std(0, ddof=1)
        j = int(_np.argmin(((_Zf - zf) ** 2).sum(1))); key = (_full.material.iloc[j], _full.structure.iloc[j]); cnt[key] = cnt.get(key, 0) + 1
    _inv[_t] = sorted([[MG.MATERIALS[a]['ko'], MG.STRUCTURES[b]['ko'], c] for (a, b), c in cnt.items()], key=lambda r: -r[2])[:6]

_gs = _gen.sample(400, random_state=1)
SD = dict(
    tr=[[r.material, r.structure] + [round(float(getattr(r, c)), 4) for c in _X8] + [round(float(r.Voc_V), 2), round(float(r.Voc_cv), 4)] for r in _tr.itertuples()],
    x8=_X8, pc=[[round(float(a), 3), round(float(b), 3)] for a, b in _P], ev=[round(float(e), 3) for e in _ev],
    load=[[c, round(float(_W[i, 0]), 3), round(float(_W[i, 1]), 3)] for i, c in enumerate(_X19)],
    gen=[[round(float(r.W), 2), round(float(r.CW_F), 4), round(float(r.SRA_F), 2), round(float(r.Qmax_F), 4), round(float(r.Voc_pred), 2), round(float(r.Voc_lo95), 2), round(float(r.Voc_hi95), 2), bool(r.in_domain), round(float(r.Voc_sampled), 2)] for r in _gs.itertuples()],
    mats={k: v['ko'] for k, v in MG.MATERIALS.items()}, strs={k: v['ko'] for k, v in MG.STRUCTURES.items()},
    sopt=MG.SRA_OPT, sra_med={MG.STRUCTURES[k]['ko']: round(float(v), 1) for k, v in _df.groupby('structure').SRA_F.median().items()},
)
_SDJ = _sj.dumps(SD, ensure_ascii=False, separators=(',', ':'))

def _img(name, cap, h=330):
    src = _sj.load(open(os.path.join(B, '..', 'slides', 'img', 'gh', 'sources.json')))[name]
    return f'<figure class="gh"><img src="img/gh/{name}.webp" alt="{cap}" style="max-height:{h}px"><figcaption>{cap} <span>그림: adminmrobo/{src}</span></figcaption></figure>'

def _tbl(head, rows, cls='t'):
    return f'<table class="{cls}"><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</table>'

def _ref(*ks):
    return '<sup class="rf">' + ','.join(ks) + '</sup>'

def _f(v, n=2):
    return f'{v:.{n}f}'

SL = []   # (part, title, body, init)
def S(part, title, body, init=''):
    SL.append((part, title, body, init))

P0, P1, P2, P3, P4, P5, P6, P7, P8 = '표지', '1. 왜 데이터를 만드나', '2. 데이터 기초', '3. 섬유 메커니즘', '4. 생성 절차', '5. 데이터 검증', '6. 방법론 (머신러닝·딥러닝)', '7. 실습', '8. 향후 연구'

# ---------------- 표지·목차 ----------------
S(P0, '', '<div class="cover"><div class="kicker">한양대 스마트텍스타일연구실 · 직물 마찰전기 AI 과제 · 1차년도</div>'
  '<h1>섬유직물 데이터 생성 가이드<br><span>메커니즘 · 검증 · 생성 모델 실습</span></h1>'
  '<p class="lead">실측 직물 데이터의 패턴(결합분포)을 학습하는 생성 모델로 새 직물을 만들고,<br>그 직물의 전기적 특성을 연속값(회귀형 출력)으로 예측한다.</p>'
  '<div class="who">2026-11-18 · 연구진 공유용 · 글 안상선</div>'
  '<div class="keys">← → 이동 · O 전체 보기 · F 전체 화면 · 인쇄하면 쪽마다 PDF</div></div>')
S(P0, '이 자료의 목표 — 연구진이 바로 쓸 세 가지', '<div class="g3">'
  '<div class="card"><b>① 데이터 생성 가이드</b><p>섬유 → 실 → 직물 구조 → 물성 19항목 → 전기 특성 Y. 소재와 제작 방법(제직·편직·부직)의 메커니즘을 식으로 따라가 모의 데이터를 만드는 방법과 근거 이론.</p></div>'
  '<div class="card"><b>② 데이터 검증</b><p>측정값을 정답이 아닌 관측값으로 다루는 법. 품질 검사, 반복 측정 흔들림, 분포·상관 비교, 누수 방지, TSTR, 적용 범위.</p></div>'
  '<div class="card"><b>③ 향후 연구 방법·실습</b><p>생성된 데이터로 생성 모델을 학습하고 검증하는 7개 Lab. 실행 명령, 확인할 숫자, CSV 예시 파일 14개를 함께 드립니다.</p></div></div>'
  '<p class="note">섬유공학 전문가가 아닌 데이터·AI 쪽에서 쓴 자료입니다. 섬유 메커니즘 부분은 고전 이론과 문헌 방향을 따른 가정이며, 실험실의 검토와 보정을 전제로 합니다.</p>')
S(P0, '목차', '<ol class="toc">' + ''.join(f'<li><b>{p}</b><span>{d}</span></li>' for p, d in [
  (P1, '실측 27개, 전기 특성 0개 — 모의 데이터가 필요한 이유와 한계'), (P2, '원단 한 줄 = 직물 특성 X 19 + 전기 특성 Y, 측정 기록 양식'),
  (P3, '소재·실·구조 이론(Peirce·Munden·van Wyk·Howell)과 마찰전기 이론'), (P4, '라틴 하이퍼큐브, 제작 가능성 필터, 잡음 세 층, 실측 보정'),
  (P5, '품질 검사, 반복 흔들림, 분포·상관 비교, 누수, TSTR'), (P6, '지도·비지도, PCA, 가우시안 혼합, 조건부 생성, VAE·CTGAN, 비교 기준 회귀, 불확실도'),
  (P7, '실습 키트와 Lab 1~7 상세 지침, CSV 예시'), (P8, '실측 이후 일정·역할·체크리스트, 참고문헌')]) + '</ol>')

# ---------------- 1. 왜 ----------------
S(P1, '출발점 — 실측 27개, 전기 특성 0개', '<div class="cols"><div>'
  '<div class="kpis"><div class="kpi"><b>27</b><span>받은 원단 수</span></div><div class="kpi"><b>19</b><span>27개 모두에 있는 항목</span></div><div class="kpi"><b>68%</b><span>평균 채움률</span></div><div class="kpi r"><b>0</b><span>전기 특성 Y 측정 수</span></div></div>'
  '<ul class="b"><li>출처 세 곳(Huvis 11 · 연구실 2 · 산업 14), 장비가 섞여 FTT와 KES 값이 함께 있음</li><li>두 장비 값은 압축 일만 뚜렷이 일치 — 새 원단은 장비 하나로 통일</li><li>예측할 전기 특성(마찰전기 출력)은 아직 한 개도 없음</li></ul></div><div>'
  + _img('lab_tests', '실측이 먼저 — 실험실 측정이 모든 단계의 출발점') + '</div></div>'
  '<p class="note">그래서 실측이 모이는 동안 <b>메커니즘으로 만든 모의 데이터</b>로 도구·모델·검증 절차를 먼저 시험해 둡니다.</p>')
S(P1, '1차년도 방법 정의', '<div class="def">실측 직물 데이터의 패턴(결합분포)을 학습하는 생성 모델로 새 직물을 만들고,<br>그 직물의 전기적 특성을 연속값(회귀형 출력)으로 예측한다.</div>'
  '<div class="g4"><div class="card"><b>실측</b><p>직물 특성 19항목 + 전기 특성(전압·전류·전하밀도)을 함께 계측. 전기 특성은 엄격한 정답이 아니라 직물 특성 중 하나</p></div>'
  '<div class="card"><b>학습</b><p>비지도 — 생성 모델이 "어떤 직물 특성이 어떤 전기 특성과 함께 나타나는가"를 배움</p></div>'
  '<div class="card"><b>출력</b><p>새 직물 + 전기 특성의 연속값과 범위. 지도 회귀는 비교 기준</p></div>'
  '<div class="card"><b>검증</b><p>생성 직물 일부를 실제로 만들어 측정 오차 범위 안에서 맞는지 확인</p></div></div>'
  '<p class="note">학습 방식(지도·비지도)과 출력 종류(연속·이산)는 서로 다른 구분입니다. 이 과제는 <b>학습은 비지도, 출력은 연속값</b>입니다.</p>')
S(P1, '모의 데이터의 쓰임과 금지', '<div class="cols"><div>'
  '<h3 class="ok">쓰는 곳</h3><ul class="b"><li>분석 파이프라인 시험 — 입력 양식, 품질 검사, 학습, 평가</li><li>정답을 아는 시험 — 생성 모델이 우리가 넣은 관계를 되찾는가</li><li>실험계획 — 어느 인자 범위에서 Y가 크게 바뀌는지 미리 보고 실측 원단을 고름</li><li>원단 몇 개면 관계가 보이는지 미리 재기 (S2 원단 수 결정)</li></ul>'
  '<h3 class="ng">쓰지 않는 곳</h3><ul class="b"><li>연구 결과·논문 근거 — 모의 데이터의 관계는 우리가 넣은 가정</li><li>표시 없이 실측과 섞기 — 모든 행에 <code>is_mock</code></li><li>성능 보고 — 성적은 실측 원단으로만' + _ref('M11') + '</li></ul></div><div>'
  + _img('mirror', '모의 데이터는 거울 — 넣은 것만 비춘다') + '</div></div>')

# ---------------- 2. 데이터 기초 ----------------
_ex = _tr.iloc[:4]
S(P2, '원단 한 줄 = 직물 특성 X 19개 + 전기 특성 Y', '<p>표의 한 줄이 원단 하나입니다. 열은 실측 엑셀의 공통 19항목과 같은 이름을 씁니다.</p>'
  + _tbl(['fabric_id', '소재', '구조', 'W', 'SFC_F', 'SRA_F', 'BAR_F', 'CW_F', 'Qmax_F', '…', '<span class="y">Voc_V</span>', 'Voc_cv'],
         [[r.fabric_id, MG.MATERIALS[r.material]['ko'], MG.STRUCTURES[r.structure]['ko'], _f(r.W, 0), _f(r.SFC_F, 3), _f(r.SRA_F, 1), _f(r.BAR_F, 2), _f(r.CW_F, 3), _f(r.Qmax_F, 3), '…', f'<b>{_f(r.Voc_V, 1)}</b>', _f(r.Voc_cv, 3)] for r in _ex.itertuples()])
  + '<div class="g3" style="margin-top:18px"><div class="card"><b>설계 인자</b><p>소재, 구조, 실 선밀도, 밀도(커버 팩터·루프 길이·고형률) — 실험실이 정하는 값</p></div>'
  '<div class="card"><b>직물 특성 X (19)</b><p>평량, 마찰, 거칠기 진폭·파장, 굽힘 강성·일, 압축 일·회복, 냉온감 — FTT로 재는 값</p></div>'
  '<div class="card"><b>전기 특성 Y</b><p>개방 전압 Voc, 전하 Q, 평균 전류 — 반복 3회 평균과 변동계수</p></div></div>')
S(P2, 'Y는 연속변수 — 범주가 아니라 크기', '<div class="cols"><div><ul class="b">'
  '<li><b>범주(이산)</b>: "출력 높음 / 낮음" 같은 칸 → 분류</li><li><b>연속</b>: 41.3 V, 0.92 nC 처럼 크기 그 자체 → 회귀형 출력</li>'
  '<li>전기 특성을 범주로 자르면 정보를 버림. 연속값과 <b>범위</b>를 함께 냄</li><li>단위가 다른 Y(전압·전하·전류)는 각각 따로 다룸. 주 지표는 Voc로 시작</li>'
  '<li>Voc·Q처럼 양수이고 오른쪽으로 치우친 값은 <b>로그</b>를 씌워 다룸</li></ul></div><div>' + _img('scale', '연속값은 저울 눈금처럼 크기를 그대로 잰다') + '</div></div>')
S(P2, '측정값은 정답이 아니다 — 관측값 = 참값 + 오차', '<div class="cols"><div>'
  '<div class="fbox">관측값 = 직물의 참값 × (원단 간 변동) × (측정 오차)</div><ul class="b">'
  '<li>같은 원단도 상대 물질·힘·습도·잔류 전하에 따라 전기 출력이 흔들림</li><li>그래서 Y를 "정답 라벨"로 고정하지 않고 직물 특성 중 하나로 다룸</li>'
  '<li>반복 측정 3회 → 평균과 <b>변동계수(CV)</b>를 함께 기록</li><li>모델 오차가 측정 오차(CV)보다 작아지면 <b>과적합 신호</b></li></ul></div><div>'
  + _img('archery', '같은 과녁에 쏴도 화살은 흩어진다 — 측정의 흔들림') + '</div></div>')
_tc = list(_tmpl.columns)
S(P2, '측정 기록 양식 — 52열', '<p>실험실은 이 양식(<a href="../practice/data/00_measurement_template.csv">00_measurement_template.csv</a>)으로 기록합니다. 열 뜻과 단위는 <a href="../practice/data/00_column_dictionary.csv">00_column_dictionary.csv</a>.</p>'
  '<div class="chips">' + ''.join(f'<span class="chip{" y" if c.startswith(("Voc", "Qsc")) else (" p" if c in ("counter_material", "contact_mode", "gap_mm", "area_cm2", "pressure_kPa", "freq_Hz", "temp_C", "rh_pct", "x_instrument") else "")}">{c}</span>' for c in _tc) + '</div>'
  '<div class="lg"><span class="chip">식별·설계·물성</span> <span class="chip p">측정 조건 (고정·기록)</span> <span class="chip y">전기 특성 (반복 3회)</span></div>'
  + _tbl(['fabric_id', 'material', 'structure', 'W', 'SRA_F', 'counter', 'rh_pct', 'Voc_rep1~3', 'Voc_V', 'Voc_cv'], [[r.fabric_id, r.material, r.structure, r.W, r.SRA_F, r.counter_material, r.rh_pct, f'{r.Voc_rep1} · {r.Voc_rep2} · {r.Voc_rep3}', r.Voc_V, r.Voc_cv] for r in _tmpl.itertuples()]))
S(P2, '측정 프로토콜 — Y를 "직물의 성질"로 만드는 고정값', prott.replace('class="tw"', 'class="tw t2"').replace('class="tb"', 'class="t"')
  + '<p class="note">조건이 흔들리면 모델은 직물이 아니라 측정 조건을 배웁니다. 고정할 수 없는 온습도는 반드시 열로 남깁니다.</p>')

# ---------------- 3. 섬유 메커니즘 ----------------
S(P3, '생성 사슬 — 섬유에서 전기 특성까지', '<div class="wide">' + chain_svg + '</div>'
  '<div class="g3"><div class="card"><b>앞 칸 → 뒤 칸은 식</b><p>각 칸은 앞 칸의 값으로 계산합니다. 무작위로 흩뿌린 숫자가 아니라 제작 메커니즘을 따라간 숫자입니다.</p></div>'
  '<div class="card"><b>칸마다 잡음</b><p>식이 다 설명하지 못하는 몫(원단 간 변동)과 측정 오차를 칸마다 정한 크기로 더합니다.</p></div>'
  '<div class="card"><b>소재는 Y로 직접도</b><p>대전 서열과 수분율은 구조를 거치지 않고 전기 특성에 바로 영향을 줍니다.</p></div></div>')
S(P3, '① 소재 — 섬유의 대표값', '<div class="t2">' + matt.replace('class="tb"', 'class="t"') + '</div>'
  '<p class="note">교과서 수준의 대표값입니다. 대전 서열 점수는 직물 대전 서열(나일론 > 면 > 폴리에스터 > 폴리프로필렌 > PTFE)' + _ref('G8') + '을 순서 점수로 옮긴 가정값이며, 울은 문헌마다 위치가 달라 불확실성이 큽니다. 실험실 실의 시험 성적서 값으로 바꿔 넣습니다.</p>')
S(P3, '② 실 — 지름과 커버 팩터', '<div class="cols"><div>'
  '<div class="fbox">실 지름 d = √( 4 · tex·10⁻⁵ / (π · ρ<sub>f</sub> · 0.6) )  [cm]</div><ul class="b"><li>단면적 = 선밀도 ÷ (섬유 밀도 × 충전율 0.6)</li><li>같은 tex라도 가벼운 섬유(PP 0.91)는 굵고, 무거운 섬유(면 1.52)는 가늘다</li></ul>'
  '<div class="fbox">커버 팩터(SI) K = 올/cm × √tex / 10</div><ul class="b"><li>K가 클수록 실이 빽빽 — 경사 K₁ + 위사 K₂</li><li>평직은 K₁+K₂ ≈ 32에서 막힘(jam), 능직·호프색은 36까지</li><li>생성기는 막힘 한계의 98%를 넘으면 버림 — 짤 수 없는 직물</li></ul></div><div>'
  '<div class="mini"><b>예: 나일론 25 tex, K = 26, 경사 비중 0.52</b><br>d = 0.216 mm<br>EPC = 13.5·10/√25 = 27.0 올/cm<br>PPC = 12.5·10/√25 = 25.0 올/cm<br>막힘 한계 대비 26/36 = 72%</div></div></div>')
S(P3, '③ 구조 — 제작 방법 5종', '<div class="t2">' + strt.replace('class="tb"', 'class="t"') + '</div>'
  '<p class="note">능직·호프색은 교차가 적어 평직보다 실을 더 촘촘히 넣을 수 있어(조직 계수)' + _ref('G2') + ' 막힘 한계를 높게 둡니다. 실-실 접촉 표면 계수는 직물 TENG 비교 연구' + _ref('M3', 'M4') + '의 순서를 따른 가정입니다.</p>')
S(P3, '③-1 제직 — Peirce의 직물 기하', '<p>Peirce(1937)는 제직물을 실 지름·간격·굴곡·커버·두께·평량이 서로 묶인 하나의 기하 체계로 다뤘습니다' + _ref('G1') + '. 생성기는 이를 단순화해 씁니다.</p>'
  '<div class="fbox">굴곡률 c ≈ 0.9 · 교차 비율 · (d / 맞은편 실 간격)²   (평직 1, 능직·호프색 0.5)</div>'
  '<div class="fbox">평량 W = ( EPC · tex · (1+c₁) + PPC · tex · (1+c₂) ) / 10   [g/m²]</div>'
  '<div class="fbox">두께 t ≈ 2d · (1 + 0.12·(뜬 길이 − 1)),   충전율 φ = W / (t · ρ<sub>f</sub> · 1000)</div>'
  '<ul class="b"><li>실이 위아래로 굽은 만큼(굴곡) 실이 더 들어가 평량이 늘어남</li><li>충전율 φ = 직물 부피 중 섬유가 차지하는 비율 — 압축·냉온감·실접촉의 핵심 중간 변수</li></ul>')
S(P3, '③-2 편직 Munden · ③-3 부직포 고형률', '<div class="cols"><div><h3>편직 (싱글 저지)</h3>'
  '<div class="fbox">루프 길이 l = √tex / TF  [mm]   (조임 계수 TF 1.2~1.7)</div><div class="fbox">코스/cm = K<sub>c</sub> / l,   웨일/cm = K<sub>w</sub> / l   (l: cm)</div><div class="fbox">평량 W = 코스 · 웨일 · l · tex / 10</div>'
  '<p class="note">코스·웨일 밀도는 루프 길이에 반비례하고, 상수는 조임과 무관합니다' + _ref('G3') + '. K<sub>c</sub> ≈ 4.8~5.4, K<sub>w</sub> ≈ 3.8~4.3 (건조 이완 대표값).</p></div>'
  '<div><h3>부직포 (니들펀치)</h3><div class="fbox">두께 t = W / (ρ<sub>f</sub> · 고형률 · 1000)  [mm]</div>'
  '<ul class="b"><li>실을 만들지 않고 섬유망을 바늘로 얽음 — 평량과 고형률(0.06~0.20)이 설계 인자</li><li>공극이 많아 압축 일이 크고 냉온감은 작음</li><li>섬유 배향 MD/CD ≈ 1.3 — 방향별 굽힘 차이</li></ul></div></div>')
_ir = items_rows
S(P3, '④ 물성 19항목 — 생성 규칙 (1/2)', _tbl(['항목', '메커니즘', '생성 식 (요약)', '근거'], [[f'<b>{a}</b>', b, f'<span class="s">{c}</span>', _ref(*d.split())] for a, b, c, d in _ir[:5]]))
S(P3, '④ 물성 19항목 — 생성 규칙 (2/2)', _tbl(['항목', '메커니즘', '생성 식 (요약)', '근거'], [[f'<b>{a}</b>', b, f'<span class="s">{c}</span>', _ref(*d.split())] for a, b, c, d in _ir[5:]])
  + '<p class="note">섬유·직물 마찰은 Amontons 법칙(F/N = 일정)이 맞지 않고 F = a·Nⁿ을 따릅니다' + _ref('G6') + '. 압축은 van Wyk 섬유 집합체 이론' + _ref('G4', 'G5') + '의 방향을 따랐습니다. 단위는 FTT 출력 단위로 보정합니다.</p>')
S(P3, '⑤ 전기 특성 — 접촉-분리형 마찰전기 이론', '<div class="cols"><div>'
  '<div class="fbox">Voc = σ · x / ε₀      Q = σ · S      평균 전류 = 2 · Q · f</div>'
  '<ul class="b"><li>σ: 표면 전하 밀도 (μC/m²) — 직물이 정하는 부분</li><li>x: 최대 간격, S: 전극 면적, f: 주파수 — 프로토콜로 고정</li><li>반주기마다 전하 Q가 한 번 이동 → 평균 |I| = 2Qf</li></ul>'
  '<div class="fbox">σ = σ₀ · (대전 서열 차) · (실접촉 지수) · (습도 계수)</div>'
  '<p class="note">접촉-분리형 TENG의 V–Q–x 이론' + _ref('M2') + '. σ₀(규모)는 실측 첫 원단 10개 안팎으로 보정합니다.</p></div><div>'
  '<div class="mini"><b>세 계수가 담는 메커니즘</b><br><br><b>대전 서열 차</b> — 소재가 상대 전극(PTFE)과 얼마나 먼가' + _ref('G8', 'M1') + '<br><br><b>실접촉 지수</b> — 구조의 접촉 표면 × 거칠기(역U자) × 압력 포화' + _ref('G11', 'M3') + '<br><br><b>습도 계수</b> — 습할수록 감소, 흡습성 섬유가 더 민감' + _ref('G9', 'M5') + '</div></div></div>')
S(P3, '거칠기를 역U자로 둔 이유 — 두 문헌을 함께 담기', '<div class="cols"><div><ul class="b">'
  '<li>직물 TENG: 능직 2/2·호프색 2/2가 접촉 표면적과 거칠기가 커서 평직보다 출력이 높음' + _ref('M3') + '</li>'
  '<li>평평한 탄성 표면: 거칠기가 커질수록 실접촉 면적과 출력이 감소' + _ref('G10') + '</li>'
  '<li>둘을 함께 담으려면 "적당한 요철에서 최대"인 모양</li></ul>'
  '<div class="fbox">g(SRA) = exp( −(ln(SRA / SRA<sub>opt</sub>))² / (2·0.8²) )</div>'
  '<div class="ctl">SRA<sub>opt</sub> <input type="range" id="ruOpt" min="15" max="90" step="1" value="45"> <b id="ruV">45</b> μm</div>'
  '<p class="note">꼭짓점 SRA<sub>opt</sub>를 움직여 보십시오. 점은 구조별 거칠기 중앙값(모의)입니다. 실측 원단으로 꼭짓점을 정합니다.</p></div>'
  '<div><canvas id="ruCv" width="560" height="380"></canvas></div></div>', 'initRough')
S(P3, '메커니즘 계산기 — 한 원단을 직접 만들어 보기', '<p class="small">소재·구조·인자를 바꾸면 구조 → 물성 → 전기 특성이 같은 식으로 계산됩니다(잡음 없는 참값). 생성기 파이썬 코드와 값이 일치합니다.</p><div class="calcwrap">' + calc + '</div>')

# ---------------- 4. 생성 절차 ----------------
S(P4, '생성 절차 8단계', '<ol class="steps">'
  '<li><b>설계 공간</b> — 소재·구조 목록과 연속 인자 범위. 실험실이 만들 수 있는 범위로</li><li><b>표본 추출</b> — 소재 × 구조 칸마다 라틴 하이퍼큐브, 칸마다 같은 수(기본 20)</li>'
  '<li><b>구조 계산</b> — 실 지름·밀도·평량·두께·충전율</li><li><b>제작 가능성 필터</b> — 막힘 한계·조임 계수·충전율 범위 밖은 버림</li>'
  '<li><b>물성 19항목</b> — 메커니즘 식 + 원단 간 변동 + 측정 오차</li><li><b>전기 특성 Y</b> — 마찰전기 식 + 습도 + 전기 측정 오차, 반복 3회</li>'
  '<li><b>품질 검사</b> — 범위·순서·흔들림·분포 비교</li><li><b>기록</b> — 시드, 생성기 버전, 가정 표(변수 사전 JSON), 모든 행 is_mock</li></ol>'
  + _img('factory', '공정처럼 칸을 차례로 지나며 값이 만들어진다', 190))
S(P4, '라틴 하이퍼큐브 — 설계 공간을 고르게 채우기', '<div class="cols"><div><ul class="b">'
  '<li>무작위 추출은 운에 따라 한쪽에 몰리고 빈 곳이 생김</li><li>라틴 하이퍼큐브는 각 인자 범위를 n칸으로 나눠 <b>칸마다 정확히 하나</b>씩 뽑음' + _ref('G12') + '</li>'
  '<li>적은 원단 수로 인자 범위 전체를 덮음 — 실측 실험계획에도 그대로 씀</li><li>소재 × 구조는 범주라 칸(층)으로 나누고, 칸 안에서 연속 인자를 뽑음</li></ul>'
  '<div class="ctl">원단 수 <input type="range" id="lhN" min="5" max="40" value="12"> <b id="lhV">12</b> <button class="bt" id="lhR">다시 뽑기</button></div></div>'
  '<div><canvas id="lhCv" width="580" height="320"></canvas><p class="small">가로: 실 선밀도, 세로: 커버 팩터. 왼쪽 무작위, 오른쪽 라틴 하이퍼큐브(각 행·열에 점 하나).</p></div></div>', 'initLHS')
S(P4, '제작 가능성 필터와 잡음 세 층', '<div class="cols"><div><h3>제작 가능성 필터</h3>' + _tbl(['구조', '버리는 조건'], [['제직', '커버 팩터 합 > 막힘 한계 × 0.98'], ['편직', '조임 계수 TF < 1.15 또는 > 1.75'], ['부직', '충전율 φ < 0.03 또는 > 0.30']])
  + '<p class="note">실험실이 실제로 만들 수 없는 직물이 데이터에 들어가지 않게 합니다.</p></div><div><h3>잡음 세 층</h3>'
  + _tbl(['층', '크기', '뜻'], [['원단 간 변동', 'CV 6%', '같은 설계라도 실·가공 차이'], ['물성 측정', 'CV 4% × 3회 평균', 'FTT 반복의 흔들림'], ['전기 측정', 'CV 12% × 3회 평균', '표면 상태·잔류 전하에 민감'], ['측정 환경', 'RH 65 ± 2%', '습도 계수로 Y에 들어감']])
  + '<p class="note">층을 나눠 두면 "모델 오차가 측정 오차 수준까지 내려왔는가"를 판단할 수 있습니다.</p></div></div>')
S(P4, '생성기 실행과 출력 열', '<div class="cols"><div><pre class="code">cd analysis/mock_data\npython generate_mock_fabric.py 20 20261118 .\n# 칸당 20개 × 소재 5 × 구조 5\n# → mock_fabric_data.csv (500행)\n# → mock_fabric_dictionary.json</pre>'
  '<ul class="b"><li>같은 시드 → 같은 데이터 (재현성)</li><li>소재·구조 대표값, 프로토콜, 보정 계수는 파일 맨 위 표에서 바꿈</li><li>버전·시드는 JSON에 기록</li></ul></div><div>'
  + _tbl(['열 묶음', '열'], [['식별', 'fabric_id, material, structure, kind, is_mock'], ['설계 인자', 'tex, cover, warp_share, tf, gsm_design, solidity'], ['구조량', 'yarn_d_mm, thick_mm, phi, epc, ppc, cpc, wpc, loop_mm'], ['환경', 'rh'], ['물성 19', 'W, SFC_F … Qmax_B'], ['전기 특성', 'Voc_V, Voc_cv, Qsc_nC, Iavg_nA, sigma_uCm2'], ['진단', 'contact_index, hum_factor']]) + '</div></div>')
S(P4, '결과 둘러보기 — 항목별 분포 대시보드', '<div class="ctl">항목 <select id="dsItem"></select> 묶음 <select id="dsBy"><option value="1">구조</option><option value="0">소재</option></select> <span class="small">점 하나 = 학습 자료의 원단 하나 (모의 384개), 막대 = 사분위 범위, 굵은 선 = 중앙값</span></div>'
  '<canvas id="dsCv" width="1150" height="470"></canvas>', 'initDist')
S(P4, '결과 미리보기 — 소재 × 구조별 Voc', '<div class="t2">' + heat.replace('class="tb mk-heat"', 'class="t heat"') + '</div><ul class="b">'
  '<li>같은 소재에서 능직·호프색 > 평직 — 직물 TENG 실험의 방향' + _ref('M3', 'M4') + '</li><li>소재는 나일론 > 울 > 면 > 폴리에스터 > 폴리프로필렌 — 대 PTFE 대전 서열의 방향' + _ref('G8') + '</li>'
  '<li>크기(수 V~100 V)는 σ₀ 보정 전의 자리표 — 순서와 비율만 의미가 있음</li></ul>')
S(P4, '실측이 들어오면 — 생성기 보정 순서', '<ol class="steps">'
  '<li><b>단위·규모 맞추기</b> — 19항목 각각 실측 27개의 분위수에 맞춰 모의 분포를 옮김(분위수 맞춤). CRR처럼 단위가 다른 항목 먼저</li>'
  '<li><b>σ₀ 보정</b> — 전기 특성을 처음 잰 원단 10개 안팎의 Voc 중앙값에 규모를 맞춤</li>'
  '<li><b>SRA<sub>opt</sub> 보정</b> — 거칠기가 다른 원단들의 Voc로 역U자 꼭짓점 추정</li>'
  '<li><b>습도 기울기</b> — 같은 원단을 RH 40/65/80%에서 재어 β 추정</li>'
  '<li><b>대전 서열 점수</b> — 소재별 평직 원단으로 순서·간격 확인 (특히 울)</li></ol>'
  '<p class="note">보정한 생성기는 버리지 않습니다. 생성 모델(S4)과 비교하는 <b>물리 기반 기준선</b>이 됩니다.</p>')

# ---------------- 5. 데이터 검증 ----------------
S(P5, '검증의 세 질문', '<div class="g3"><div class="card"><b>① 값이 말이 되나</b><p>결측·음수·튀는 값·범위·중복·반복 흔들림 — Lab 1</p></div>'
  '<div class="card"><b>② 관계가 살아 있나</b><p>구조·소재 순서, 분포·상관 비교, 간접 상관 함정 — Lab 2, 5</p></div>'
  '<div class="card"><b>③ 쓸 수 있나</b><p>누수 없는 분할, TSTR, 적용 범위, 전향 검증 — Lab 3, 5, 6</p></div></div>'
  + _img('overlay', '모의와 실측을 겹쳐 보며 다른 곳을 찾는다', 300))
_qcs = _qc.groupby(['check', 'result']).size().unstack(fill_value=0)
S(P5, 'Lab 1 품질 검사 — 무엇을 보나', '<div class="cols"><div>' + _tbl(['검사', '기준'], [['필수 열', '19항목 + Voc_V 모두'], ['결측 · 양수', '결측 0, 0 이하 0 (로그 변환 전제)'], ['튀는 값', '로그 z 점수 |z| > 4 인 원단 0개'], ['범위', '평량 30~400 g/m² 등 실제 직물 범위'], ['반복 흔들림', 'Voc CV 중앙값 ≤ 0.15, 초과 원단은 재측정'], ['중복', 'fabric_id 중복 0']])
  + '</div><div>' + _tbl(['검사', '통과', '경고'], [[i, int(r.get('통과', 0)), int(r.get('경고', 0))] for i, r in _qcs.iterrows()])
  + '<p class="note">학습 자료(모의 384개) 결과: 통과 66 · 경고 1 — 압축 일 CW_B에서 |z| &gt; 4 원단 2개. 반복 흔들림은 CV 중앙값 0.10으로 통과했지만, CV 0.15를 넘는 원단 78개가 재측정 목록 <code>lab1_remeasure.csv</code>로 나옵니다. 예시: <a href="../practice/data/03_qc_report_example.csv">03_qc_report_example.csv</a></p></div></div>')
S(P5, '반복 측정 흔들림 — 재측정 기준 정하기', '<div class="cols"><div><canvas id="cvCv" width="620" height="380"></canvas></div><div>'
  '<div class="ctl">재측정 기준 CV <input type="range" id="cvT" min="0.05" max="0.3" step="0.01" value="0.15"> <b id="cvV">0.15</b></div>'
  '<div class="kpis"><div class="kpi r"><b id="cvN">–</b><span>재측정 원단 수</span></div><div class="kpi"><b id="cvM">–</b><span>CV 중앙값</span></div></div>'
  '<ul class="b"><li>3회 반복의 CV는 그 자체도 흔들림 — 기준을 너무 낮추면 재측정이 폭증</li><li>재측정해도 흔들리면 원단 자체(표면 불균일)를 기록</li><li>실측 첫 20개로 기준을 다시 정함</li></ul></div></div>', 'initCV')
S(P5, '분포 비교 — 열마다 KS 거리', '<div class="cols"><div>' + _tbl(['항목', 'KS 거리', 'p', '판정'], [[r.item, _f(r.KS, 3), _f(r.p, 2), r['판정']] for _, r in _ks.iterrows()])
  + '</div><div><ul class="b"><li>KS 거리 = 두 누적분포의 최대 차이 (0이면 같음)</li><li>&lt; 0.1 닮음, 0.1~0.2 주의, &gt; 0.2 다름 (실습 기준)</li><li>위 표: Lab 4 생성 직물 1000개 vs 학습 자료 — 모두 닮음</li>'
  '<li>실측이 오면 같은 표를 <b>모의 vs 실측</b>으로 만들어 생성기 보정 대상을 고름</li><li>한 열씩만 보면 관계를 놓침 → 다음 장의 상관 비교</li></ul></div></div>')
S(P5, '상관 비교와 간접 상관 함정', '<div class="cols"><div><ul class="b">'
  '<li>열마다 분포가 닮아도 <b>관계</b>가 다를 수 있음 → 상관 행렬 차이(생성 vs 학습: 최대 0.06, 평균 0.02)</li>'
  '<li>모의 데이터에서 Voc와 냉온감 Qmax의 순위 상관이 높게 나옴 — 둘 다 <b>거칠기</b>에 기대어 생긴 간접 상관</li>'
  '<li>Qmax를 바꾼다고 출력이 바뀌지 않음. 상관 ≠ 원인</li><li>실측에서도 같은지 확인하고, 원인 해석은 설계 실험(한 요인만 다른 원단 짝)으로</li></ul></div><div>'
  + _img('confounder', '아이스크림과 해수욕 사고 — 둘 다 더위 때문', 330) + '</div></div>')
S(P5, '누수와 지름길 — 성적이 너무 좋을 때', '<div class="cols"><div><ul class="b">'
  '<li><b>변환 누수</b>: 평균·표준편차를 전체 자료로 계산 → 시험 정보가 학습에 샘. 기준은 학습 자료로만</li>'
  '<li><b>원단 누수</b>: 같은 원단의 반복 측정이 학습·시험에 나뉨 → 원단 단위로 나눔</li>'
  '<li><b>조합 누수</b>: 새 조합 예측을 보려면 그 조합 칸 전체를 빼 둠 (실습: 울 × 호프색)</li>'
  '<li><b>지름길</b>: 출처·장비 열로 Y를 맞히는 경우 — 출처를 섞어 나누고 출처 열은 입력에서 뺌</li></ul></div><div>'
  + _img('leak', '시험 정보가 새면 성적이 부풀려진다', 210) + _img('split', '나누는 단위가 곧 검증의 질', 210) + '</div></div>')
_tb = _tstr
S(P5, 'TSTR — 생성 데이터가 패턴을 담았는가', '<div class="cols"><div><ul class="b">'
  '<li><b>TRTR</b>: 실측으로 학습 → 실측으로 시험 (기준)</li><li><b>TSTR</b>: 생성으로 학습 → 실측으로 시험' + _ref('M11') + '</li>'
  '<li>TSTR이 TRTR에 가까우면 생성 데이터가 패턴을 잘 담은 것</li><li>실측+생성이 TRTR보다 나아지지 않으면 생성은 <b>새 정보를 주지 않은 것</b></li></ul>'
  '<div class="mini">실습 결과 (랜덤포레스트, 8항목)</div></div><div class="bars">'
  + ''.join(f'<div class="bar"><span>{r.setting}</span><i style="width:{max(r.test_R2, 0) * 100:.0f}%"></i><b>R² {r.test_R2:.3f} · RMSE {r.test_RMSE:.1f} V</b></div>' for r in _tb.itertuples())
  + '<p class="note">생성 1000개로 학습해도 실측 384개 학습을 넘지 못합니다. 생성은 실측을 대신하지 못하고, 패턴을 확인·탐색하는 데 씁니다.</p></div></div>')

# ---------------- 6. 방법론 ----------------
S(P6, '지도 · 비지도 — 학습 방식과 출력은 다른 구분', '<div class="cols"><div>'
  + _tbl(['', '지도학습', '비지도학습'], [['배우는 것', '목표 열 Y를 따로 두고 X → Y', '자료 전체의 패턴(분포)'], ['출력이 연속', '회귀', '연속값을 내는 생성 모델'], ['출력이 이산', '분류', '군집'], ['이 과제', '<b>비교 기준</b> (릿지·RF·GP)', '<b>주 방법</b> (결합분포 생성 모델)']])
  + '<ul class="b"><li>측정된 전기 특성은 엄격한 정답이 아니라 직물 특성 중 하나 → 함께 배움</li><li>출력은 연속값이므로 "회귀형 출력"</li></ul></div><div>' + _img('board', '머신러닝 지도 — 지도·비지도·생성', 320) + '</div></div>')
S(P6, 'PCA — 19개 변수를 섞은 종합 점수 (행렬과 내적)', '<div class="fbox">PC = Z · W     (원단 n × 19) · (19 × 2) = (n × 2)       PC1ᵢ = zᵢ · w₁ = Σₖ zᵢₖ w₁ₖ</div>'
  '<ul class="b"><li>Z: 로그 변환 후 표준화한 19항목 (평균 0, 표준편차 1)</li><li>W의 열: 원단이 가장 넓게 퍼지는 방향, 길이 1이고 서로 직교(내적 0)</li>'
  '<li>원단 하나의 PC1 점수 = 그 원단의 줄과 W 첫 열의 내적 — 경기종합지수처럼 여러 지표의 가중합</li>'
  f'<li>모의 학습 자료: PC1 {SD["ev"][0]:.0%}, PC2 {SD["ev"][1]:.0%} (실측 27개는 39%·29%)</li><li>PCA는 보는 도구 — 생성 모델 학습은 19개(또는 핵심 8개) 전체로</li></ul>')
S(P6, 'PCA 탐색기 — 점수와 가중치', '<div class="ctl">색 <select id="pcBy"><option value="1">구조</option><option value="0">소재</option></select> 가중치 <select id="pcW"><option value="0">PC1</option><option value="1">PC2</option></select> <span class="small">점에 올리면 원단 정보</span></div>'
  '<div class="cols"><canvas id="pcCv" width="600" height="440"></canvas><canvas id="pcL" width="520" height="440"></canvas></div>', 'initPCA')
S(P6, '군집 — k-평균과 가우시안 혼합', '<div class="cols"><div><ul class="b">'
  '<li><b>k-평균</b>: 점마다 가장 가까운 중심 하나에 배정 (딱 잘라 나눔), 무리 모양은 둥근 공</li>'
  '<li><b>가우시안 혼합(GMM)</b>: 무리마다 평균과 공분산(타원), 점마다 소속 확률 — 경계가 부드러움</li>'
  '<li>GMM은 "자료가 어떻게 생겼나"를 확률분포로 배우므로 <b>새 점을 뽑을 수 있음</b> → 생성 모델</li>'
  '<li>무리 수는 BIC로 고름 (다음 장)</li><li>직물에서 무리는 대체로 조직·소재 계열 — 실측 S1 PCA에서도 종류별로 모임</li></ul></div><div>' + _img('moons', '두 개의 고리 — 모양이 다른 무리', 320) + '</div></div>')
S(P6, '결합분포와 조건부 생성 — 핵심 식', '<div class="fbox">p(x, y) = Σₖ πₖ · N( [x, y] ; μₖ, Σₖ )          ← 직물 특성 x와 전기 특성 y를 함께</div>'
  '<div class="fbox">p(y | x) = Σₖ wₖ(x) · N( y ; μ<sub>y|x,k</sub> , σ²<sub>y|x,k</sub> )</div>'
  '<div class="fbox">μ<sub>y|x,k</sub> = μ<sub>y,k</sub> + Σ<sub>yx,k</sub> Σ<sub>xx,k</sub>⁻¹ (x − μ<sub>x,k</sub>)        σ²<sub>y|x,k</sub> = Σ<sub>yy,k</sub> − Σ<sub>yx,k</sub> Σ<sub>xx,k</sub>⁻¹ Σ<sub>xy,k</sub></div>'
  '<ul class="b"><li>학습: x와 y를 구분하지 않고 패턴 p(x, y)를 배움 — 비지도</li><li>새 직물: p(x, y)에서 뽑음 → x와 y가 함께 나옴</li>'
  '<li>예측: 새 x를 정하면 p(y | x)의 평균(연속값)과 표준편차(범위) — 회귀형 출력</li><li>역방향: 목표 y*를 정하면 p(x | y*) → 그 출력을 낼 직물 후보 (Lab 7)</li></ul>')
S(P6, '생성 모델 시연 — 무리 수를 바꿔 보기', '<div class="ctl">무리 수 K <input type="range" id="emK" min="1" max="6" value="3"> <b id="emV">3</b> <button class="bt" id="emS">새 직물 200개 뽑기</button> <span class="small">가로: PC1 점수, 세로: log Voc (표준화). EM 알고리즘을 브라우저에서 바로 돌립니다.</span></div>'
  '<div class="cols"><canvas id="emCv" width="700" height="440"></canvas><div><div class="kpis"><div class="kpi"><b id="emLL">–</b><span>로그 가능도</span></div><div class="kpi"><b id="emB">–</b><span>BIC (작을수록 좋음)</span></div></div>'
  '<ul class="b"><li>타원 = 무리마다 배운 패턴 (2σ)</li><li>보라 점 = 배운 패턴에서 새로 뽑은 직물</li><li>K가 너무 작으면 패턴을 뭉갬, 너무 크면 원단 하나하나를 외움 → BIC로 균형</li></ul></div></div>', 'initEM')
S(P6, '딥러닝 생성 모델 — 언제 쓰나', '<div class="cols"><div>' + _tbl(['방법', '배우는 법', '원단 수', '이 과제에서'], [
  ['가우시안 혼합', '무리별 평균·공분산', '수십 개부터', '<b>1차 시작점</b> — 조건부 식이 정확, 해석 쉬움'],
  ['가우시안 코퓰라', '열별 분포 + 상관 구조', '수십 개부터', '분포가 치우친 항목이 많을 때'],
  ['VAE (TVAE)', '인코더로 잠재 공간 → 디코더로 복원', '수백 개 이상', '원단이 늘고 관계가 비선형일 때'],
  ['CTGAN', '생성기 vs 판별기 경쟁, 범주 조건', '수백 개 이상', '소재·구조 같은 범주를 조건으로 줄 때' + _ref('M10')]])
  + '<p class="note">표 데이터 생성 모델 논문도 일부 지표에서 단순한 방법보다 못하다고 밝힙니다' + _ref('M10') + '. 원단이 적을 때 딥러닝 생성 모델은 원단을 외웁니다.</p></div><div>' + _img('magic', '딥러닝 생성 모델 — 강력하지만 자료를 많이 먹는다', 300) + '</div></div>')
_bb = _base
S(P6, '비교 기준 — 지도 회귀 (Lab 3)', '<div class="cols"><div class="bars">'
  + ''.join(f'<div class="bar"><span>{r.model}</span><i style="width:{max(r.test_R2, 0) * 100:.0f}%"></i><b>시험 R² {r.test_R2:.3f} · 새 조합 RMSE {r.newcombo_RMSE:.1f} V</b></div>' for r in _bb.itertuples())
  + '<ul class="b"><li>평균 → 릿지 → 랜덤포레스트 → 가우시안 과정 순으로 복잡도를 올림</li><li>5겹 교차검증 + 시험 자료 + 새 조합(울 × 호프색)</li><li>생성 모델의 p(y|x)는 이 기준선을 넘어야 의미</li></ul></div><div class="imgs3">'
  + _img('tree', '결정 트리 — 스무고개', 190) + _img('forest', '랜덤포레스트 — 나무들의 투표', 190) + '</div></div>')
S(P6, '불확실도와 적용 범위 — 외삽을 믿지 않기', '<div class="cols"><div><ul class="b">'
  '<li>예측마다 범위(±2σ)를 함께 냄. 범위가 넓다 = 모델이 모름</li><li><b>적용 범위</b>: ① 각 항목이 학습 자료 1~99% 안 ② 마할라노비스 거리가 학습 자료 99% 이내 ③ 예측 Y가 학습 Y 범위 안</li>'
  '<li>Lab 4: 생성 1000개 중 837개가 적용 범위 안</li><li>Lab 6 함정: 범위 검사 없이 기대값 최고를 고르면 예측 240 V → 실제 50~77 V. 예상 범위조차 틀림</li>'
  '<li>X가 각각 범위 안이어도 <b>조합</b>이 새로우면 Y가 외삽됨 → ③이 필요</li></ul></div><div>' + _img('maze', '자료가 없는 곳은 미로 — 지도를 벗어나면 길을 모른다', 300) + '</div></div>')
S(P6, '모델 붕괴와 능동 학습 — 생성 결과를 어떻게 다루나', '<div class="cols"><div><h3 class="ng">모델 붕괴</h3><ul class="b"><li>모델이 만든 데이터를 다시 학습하면 원래 분포의 꼬리가 사라짐' + _ref('M12') + '</li><li>가우시안 혼합·VAE에서도 보고됨</li><li>규칙: 생성 결과는 선별·예상에만, 학습 재료는 실측에서만</li></ul></div>'
  '<div><h3 class="ok">능동 학습</h3><ul class="b"><li>불확실도가 큰 곳을 골라 실제로 재면 측정 한 번으로 모델이 가장 많이 배움' + _ref('M14') + '</li><li>후보 = 기대값 최고(쓸모) + 범위 최대(배움)</li><li>잰 원단은 실측에 더하고 다시 학습 — 몇 바퀴 반복</li></ul></div></div>'
  + _img('night', '같은 자료만 거듭 보면 꼬리가 사라진다', 220))

# ---------------- 7. 실습 ----------------
_files = [('00_measurement_template.csv', '실측 기록 양식 52열 + 예시 3행'), ('00_column_dictionary.csv', '열 뜻·단위·필수 여부'), ('01_mock_full.csv', '모의 원단 500개'),
          ('02_train.csv', '학습 384개'), ('02_test.csv', '시험 96개'), ('02_test_new_combo.csv', '새 조합 시험 20개 (울 × 호프색)'),
          ('03_qc_report_example.csv', 'Lab 1 결과'), ('04_generated_candidates_example.csv', 'Lab 4 — 새 직물 1000개, 예측·범위·적용 범위'),
          ('05_baseline_scores_example.csv', 'Lab 3 — 비교 기준 성적'), ('05_ks_example.csv', 'Lab 5 — 분포 비교'), ('05_tstr_result_example.csv', 'Lab 5 — TSTR'),
          ('06_verification_plan_example.csv', 'Lab 6 — 만들 후보와 측정 칸'), ('07_verification_result_example.csv', 'Lab 6 — 측정 후 판정'), ('08_inverse_candidates_example.csv', 'Lab 7 — 역방향 후보')]
S(P7, '실습 키트 — practice/ 폴더', '<div class="cols"><div><pre class="code">practice/\n├─ README.md          상세 지침\n├─ requirements.txt   numpy pandas scikit-learn scipy matplotlib\n├─ data/              CSV 14개\n├─ labs/\n│   common.py         경로·열 목록·변환·조건부 계산\n│   lab0_make_splits.py   (강사용) 자료 나누기\n│   lab1_check_data.py    품질 검사\n│   lab2_explore_pca.py   PCA\n│   lab3_baseline_regression.py\n│   lab4_generative_model.py\n│   lab5_validate_generated.py\n│   lab6_select_and_verify.py\n│   lab7_inverse_design.py\n└─ outputs/           실행 결과</pre></div><div>'
  + _tbl(['파일 (클릭하면 내려받기)', '내용'], [[f'<a href="../practice/data/{a}">{a}</a>', b] for a, b in _files], 't s') + '</div></div>')
S(P7, '준비와 공통 규칙', '<div class="cols"><div><pre class="code">cd practice\npython -m venv .venv\nsource .venv/bin/activate   # Windows: .venv\\Scripts\\activate\npip install -r requirements.txt\ncd labs\npython lab1_check_data.py</pre>'
  '<p class="note">Python 3.10 이상. 결과는 practice/outputs/ 에, 같은 결과의 예시는 practice/data/ 에 미리 있음.</p></div><div><h3>다섯 가지 규칙</h3><ol class="steps">'
  '<li>변환 기준(평균·표준편차)은 학습 자료로만</li><li>성적은 실측(시험) 자료로만 — 생성 데이터를 섞어도</li><li>생성 결과를 다시 학습 자료로 넣지 않음</li><li>적용 범위 밖 예측은 믿지 않음</li><li>측정 오차보다 작은 오차는 과적합 신호</li></ol></div></div>')
S(P7, 'Lab 1 · 2 — 자료 점검과 탐색', '<div class="cols"><div><h3>Lab 1 자료 점검</h3><pre class="code">$ python lab1_check_data.py          # 기본 02_train.csv\n$ python lab1_check_data.py 실측.csv # 실측이 오면\n  저장: outputs/lab1_remeasure.csv (78행)\n  저장: outputs/lab1_qc_report.csv (67행)\n통과 66\n경고  1</pre>'
  '<ul class="b"><li>경고 1: CW_B 튀는 값 2개 → 입력 실수인지 실제 값인지 실험실과 확인</li><li>재측정 78개: Voc 3회 CV &gt; 0.15 → 실측이면 실험실에 목록 전달</li><li>실측 파일은 <code>00_measurement_template.csv</code> 열 이름 그대로</li></ul></div>'
  '<div><h3>Lab 2 PCA</h3><pre class="code">$ python lab2_explore_pca.py\n설명 비율 PC1 0.355  PC2 0.322  PC3 0.111\nW 열 길이 [1. 1. 1.]  PC1·PC2 내적 0.0\n  저장: lab2_pca_loadings.csv (19×3)\n  저장: lab2_pca_scores.csv, lab2_pca.png</pre><ul class="b">'
  '<li>할 일 ① 구조·소재별로 점이 갈리는지 그림에서 보기</li><li>② 가중치 표에서 PC1을 끄는 항목(굽힘 강성·굽힘 일) 적기</li><li>③ 실측 27개 결과(39%·29%)와 비교</li></ul></div></div>')
S(P7, 'Lab 3 · 4 — 비교 기준과 생성 모델', '<div class="cols"><div><h3>Lab 3 비교 기준 (지도 회귀)</h3><pre class="code">$ python lab3_baseline_regression.py\n평균(기준선)  CV R² -0.151 시험 R² -0.028 새 조합 41.8 V\n릿지          CV R²  0.757 시험 R²  0.829 새 조합 18.8 V\n랜덤포레스트  CV R²  0.820 시험 R²  0.920 새 조합 10.1 V\n가우시안 과정 CV R²  0.916 시험 R²  0.944 새 조합 10.3 V\n측정 오차 수준: Voc 반복 CV 중앙값 0.1</pre>'
  '<ul class="b"><li>새 조합(울 × 호프색) 오차가 시험 오차보다 큼 — 본 적 없는 조합은 어렵다</li><li>릿지(선형)가 크게 뒤짐 — 관계가 비선형</li></ul></div>'
  '<div><h3>Lab 4 생성 모델 (비지도)</h3><pre class="code">$ python lab4_generative_model.py\nBIC로 고른 무리 수: 4\n적용 범위 안 생성 직물: 837 / 1000\n  (Y 학습 범위 4.6~126.8 V)\n  저장: lab4_bic.csv, lab4_generated_candidates.csv\n        Voc_sampled  Voc_pred\nmedian       46.7      45.9\nmax         257.7     240.0   ← 외삽</pre><ul class="b">'
  '<li>Voc_sampled: 결합분포에서 X와 함께 뽑은 값 · Voc_pred·lo95·hi95: 조건부 평균과 범위</li><li>max 240 V는 학습 범위 밖 → in_domain = False</li><li>원단이 50개 미만이면 무리 수 1~3, 8항목으로</li></ul></div></div>')
S(P7, 'Lab 5 · 6 · 7 — 검증, 전향 검증, 역방향', '<div class="g3"><div class="card"><b>Lab 5 생성 검증</b><pre class="code">$ python lab5_validate_generated.py\nKS 9항목 모두 &lt; 0.1 (닮음)\n상관 차이 최대 0.058 평균 0.021\nTRTR      R² 0.913 RMSE  9.5\nTSTR      R² 0.818 RMSE 13.7\n실측+생성 R² 0.897 RMSE 10.3</pre><p>분포·상관은 닮았지만 TSTR &lt; TRTR, 실측+생성도 나아지지 않음 → 생성은 새 정보를 주지 않음</p></div>'
  '<div class="card"><b>Lab 6 전향 검증</b><pre class="code">$ python lab6_select_and_verify.py\n기대값 최고 3  → ✓✓✓\n예상 범위 최대 3 → ✓✗✗\n(함정) 범위 검사 없음 3 → ✗✗✗\n적용 범위 안 비율 0.67\n함정 0.0</pre><p>측정값은 예시. 06_verification_plan의 measured_Voc 칸을 실험실 값으로 채우고 다시 실행</p></div>'
  '<div class="card"><b>Lab 7 역방향</b><pre class="code">$ python lab7_inverse_design.py 90\n목표 Voc* = 90 V\n무리 가중치 [0.81 0.10 0 0.09]\n후보 40개 → 닮은 원단:\n 나일론 호프색·저지\n 울 저지·능직</pre><p>p(x | y*)에서 뽑은 직물을 실험실이 만들 수 있는지 검토 → 만들 후보 목록</p></div></div>'
  '<p class="note">각 Lab 결과 CSV는 practice/outputs/ 에 쓰이고, 같은 내용의 예시가 practice/data/ 에 있어 실행 전에도 열어 볼 수 있습니다.</p>')
S(P7, '결과판 — 전향 검증과 역방향', '<div class="cols"><div><h3>전향 검증 (Lab 6, 측정값은 예시)</h3>'
  + _tbl(['후보', '고른 이유', '예측', '95% 범위', '측정', '판정'], [[r.gen_id, r.reason.replace(' (적용 범위 안)', '').replace(' (모델이 가장 모름)', ''), _f(r.Voc_pred, 0), f'{r.Voc_lo95:.0f}~{r.Voc_hi95:.0f}', _f(r.measured_Voc, 0), '<b class="ok">✓</b>' if r.inside_95 else '<b class="ng">✗</b>'] for r in _ver.itertuples()], 't s')
  + '</div><div><h3>역방향 (Lab 7 방식)</h3><div class="ctl">목표 Voc* <button class="bt" data-iv="30">30 V</button><button class="bt" data-iv="60">60 V</button><button class="bt" data-iv="90">90 V</button></div><div id="ivOut"></div>'
  '<p class="note">후보 200개가 가장 닮은 원단의 소재·구조 빈도입니다. 출력을 높이려면 어느 쪽 직물을 만들어야 하는지가 보입니다.</p></div></div>', 'initInv')

# ---------------- 8. 향후 ----------------
S(P8, '실측 이후 — 일정과 할 일', _tbl(['단계', '기간 (안)', '할 일', '산출물'], [
  ['S2 실측', '2026-12 ~ 2027-05', '양식대로 X·Y 측정, 장비 통일, 반복 3회, 재측정', '실측 CSV (50개 이상), Lab 1 보고'],
  ['생성기 보정', '실측 10개 시점', '분위수 맞춤 → σ₀ → SRA_opt → 습도', '보정된 생성기 v1.1'],
  ['S3 패턴 학습', '2027-02 ~ 06', 'Lab 2~5를 실측으로, 비교 기준과 비교', '생성 모델, TSTR 보고'],
  ['S4 생성·예측', '2027-04 ~ 09', '새 직물 생성, 적용 범위, 역방향 후보', '후보 목록'],
  ['S5 전향 검증', '2027-07 ~ 12', '후보 10개 이상 제작·측정, 판정, 다시 학습', '검증 보고, 2차년도 출발점']])
  + '<p class="note">2차년도에 섬유 이미지를 더할 때도 같은 원칙(실측 시험, 적용 범위, 생성 결과 재학습 금지)을 씁니다.</p>')
S(P8, '역할과 체크리스트', '<div class="cols"><div>' + _tbl(['역할', '맡는 일'], [['실험실', '설계 범위 확정, 원단 제작, FTT·전기 측정, 양식 기록, 재측정'], ['데이터·AI', '품질 검사, 생성기 보정, 생성 모델·비교 기준, 후보 선정, 보고'], ['함께', '측정 프로토콜 고정, 후보 검토(만들 수 있나), 판정 기준'], ['교수님', '방향·우선순위, 검토 항목 승인']])
  + '</div><div><h3>매번 확인</h3><ul class="check"><li>is_mock 표시가 있는가</li><li>측정 조건 열이 모두 채워졌는가</li><li>반복 CV 0.15 초과 원단을 재측정했는가</li><li>변환 기준을 학습 자료로만 정했는가</li><li>성적을 실측 시험 자료로만 쟀는가</li><li>생성 결과를 학습에 넣지 않았는가</li><li>후보가 적용 범위 안인가</li><li>예상값을 측정 전에 기록했는가</li></ul></div></div>')
_rs = [(k, c, u) for k, c, u, w in MREF2] + [(k, c, u) for k, c, u, w in MREFS if k in ('M1', 'M2', 'M3', 'M4', 'M5', 'M10', 'M11', 'M12', 'M14')]
_half = (len(_rs) + 1) // 2
for i, part in enumerate((_rs[:_half], _rs[_half:])):
    S(P8, f'참고문헌 ({i + 1}/2)', '<ol class="refs">' + ''.join(f'<li><b>[{k}]</b> {c}' + (f' <a href="{u}">링크</a>' if u else '') + '</li>' for k, c, u in part) + '</ol>')
S(P8, '', '<div class="cover end"><h1>정리</h1><ul class="b big"><li>모의 데이터는 메커니즘을 따라 만들되, 넣은 가정만 비춘다</li><li>측정값은 정답이 아닌 관측값 — 범위와 흔들림을 함께</li><li>학습은 비지도 생성 모델, 출력은 연속값, 지도 회귀는 비교 기준</li><li>성적은 실측으로, 적용 범위 밖은 믿지 않고, 일부를 실제로 만들어 확인</li></ul>'
  '<p class="lead">실습 키트: <a href="../practice/README.md">practice/README.md</a> · 가이드: <a href="../mock_data_guide.html">모의 데이터 생성 가이드</a> · <a href="../method_review.html">방법 검토</a></p></div>')

# ---------------- 조립 ----------------
_N = len(SL)
_secs = []
for i, (part, title, body, init) in enumerate(SL):
    head = f'<h2>{title}</h2>' if title else ''
    foot = f'<footer><span>{part}</span><span>섬유직물 데이터 생성 가이드</span><span>{i + 1} / {_N}</span></footer>' if i else ''
    _secs.append(f'<section class="slide" data-init="{init}" data-part="{_html.escape(part)}">{head}<div class="body">{body}</div>{foot}</section>')

SLIDE_CSS = r"""
*{box-sizing:border-box}html,body{margin:0;height:100%;background:#e9edf2;font-family:"Pretendard","Noto Sans KR","Noto Sans CJK KR",sans-serif;color:#16212b}
a{color:#1e55c8}code{font-family:"IBM Plex Mono",monospace;font-size:.9em;background:#f1f4f7;padding:1px 4px;border-radius:4px}
#deck{position:fixed;inset:0;display:flex;align-items:center;justify-content:center}
.slide{position:absolute;width:1280px;height:720px;background:#fff;padding:40px 60px 52px;display:none;transform-origin:center center;box-shadow:0 10px 40px rgba(0,0,0,.18);border-radius:6px;overflow:hidden}
.slide.on{display:block}
.slide h2{margin:0 0 16px;font-size:31px;letter-spacing:-.5px;border-left:8px solid #2f5d9e;padding-left:14px;line-height:1.25}
.slide .body{font-size:19px;line-height:1.55;height:calc(100% - 70px);overflow:hidden}
.slide footer{position:absolute;left:60px;right:60px;bottom:16px;display:flex;justify-content:space-between;font-size:13px;color:#7a8794;border-top:1px solid #e4e8ec;padding-top:6px}
.cover{height:100%;display:flex;flex-direction:column;justify-content:center}.cover .kicker{color:#2f5d9e;font-weight:700;font-size:18px}
.cover h1{font-size:56px;line-height:1.15;margin:14px 0 18px;letter-spacing:-1px}.cover h1 span{font-size:34px;color:#5b6874;font-weight:600}
.cover .lead{font-size:22px;color:#334;border-left:5px solid #c9302c;padding:6px 16px;background:#fdf3f2}.cover .who{margin-top:26px;color:#5b6874}.cover .keys{margin-top:8px;font-size:14px;color:#8a96a3}
.cover.end h1{font-size:44px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:start}.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.card{border:1px solid #dfe4ea;border-radius:12px;padding:14px 16px;background:#f9fbfd}.card b{font-size:20px;color:#2f5d9e}.card p{margin:8px 0 0;font-size:16.5px;line-height:1.55}
.def{font-size:25px;font-weight:700;line-height:1.5;background:#eef3fb;border-left:8px solid #2f5d9e;padding:16px 22px;margin:4px 0 20px;border-radius:6px}
ul.b{margin:6px 0;padding-left:22px}ul.b li{margin:5px 0}ul.big li{font-size:23px;margin:10px 0}
.note{font-size:15.5px;color:#4b5864;background:#f6f7f9;border-radius:8px;padding:8px 12px;margin:12px 0 0}.small{font-size:14px;color:#5b6874}
.fbox{font-family:"IBM Plex Mono",monospace;font-size:17px;background:#fff8ec;border:1px solid #f0d9ae;border-radius:8px;padding:9px 14px;margin:8px 0;overflow-x:auto;white-space:nowrap}
.mini{background:#f4f7fb;border:1px solid #dbe3ee;border-radius:10px;padding:14px 16px;font-size:16.5px;line-height:1.6}
table.t{border-collapse:collapse;width:100%;font-size:15.5px;background:#fff}table.t th{background:#eef2f6;text-align:left;padding:7px 9px;border-bottom:2px solid #cfd7e0}table.t td{padding:6px 9px;border-bottom:1px solid #e5e9ee;vertical-align:top}
table.t.s{font-size:13.5px}table.t td .s,table.t .s{font-size:13.5px;color:#334}.t2 table{font-size:14.5px}.t2 .t th,.t2 .t td{padding:6px 8px}
table.heat td{text-align:right;font-variant-numeric:tabular-nums}
.kpis{display:flex;gap:12px;margin:6px 0 12px}.kpi{flex:1;border:1px solid #dfe4ea;border-radius:10px;padding:10px 12px;background:#fff}.kpi b{display:block;font-size:30px;color:#2f5d9e}.kpi.r b{color:#c9302c}.kpi span{font-size:14px;color:#5b6874}
figure.gh{margin:0;text-align:center}figure.gh img{max-width:100%;border-radius:10px;border:1px solid #e1e5ea}figure.gh figcaption{font-size:14px;color:#4b5864;margin-top:4px}figure.gh figcaption span{display:block;font-size:11.5px;color:#9aa5b1}
.imgs3{display:grid;grid-template-columns:1fr;gap:6px}.imgs3 figure img{max-height:190px}
sup.rf{font-size:11px;color:#1e55c8;font-weight:700;margin-left:1px}
h3{margin:4px 0 8px;font-size:21px}h3.ok,.ok{color:#13733a}h3.ng,.ng{color:#c9302c}
ol.toc{columns:2;column-gap:40px;font-size:19px;padding-left:0;list-style:none}ol.toc li{margin:0 0 14px;break-inside:avoid}ol.toc span{display:block;font-size:15px;color:#5b6874}
ol.steps{padding-left:24px;margin:4px 0}ol.steps li{margin:6px 0}
ol.refs{font-size:13.5px;line-height:1.5;padding-left:0;list-style:none;columns:1}ol.refs li{margin:0 0 7px}
pre.code{background:#0f1720;color:#d7e3ee;font-family:"IBM Plex Mono",monospace;font-size:14.5px;line-height:1.55;border-radius:10px;padding:12px 14px;margin:6px 0;white-space:pre;overflow:hidden}
.card pre.code{font-size:13px}
.chips{display:flex;flex-wrap:wrap;gap:5px;margin:6px 0 8px}.chip{font-family:"IBM Plex Mono",monospace;font-size:12.5px;background:#eef2f6;border:1px solid #d7dee6;border-radius:5px;padding:2px 6px}.chip.p{background:#eaf5ee;border-color:#b9dcc6}.chip.y{background:#fdecec;border-color:#f1c2bf}.lg{margin:0 0 10px}
.y{color:#c9302c}
.ctl{display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-size:16px;margin:4px 0 8px}.ctl select,.ctl input[type=range]{font:inherit;font-size:15px}.ctl input[type=range]{width:200px}
.bt{font:inherit;font-size:14.5px;border:1px solid #c7d0da;background:#fff;border-radius:7px;padding:4px 10px;cursor:pointer}.bt:hover{background:#eef3fb}.bt.on{background:#2f5d9e;color:#fff;border-color:#2f5d9e}
.bars .bar{display:grid;grid-template-columns:260px 1fr;align-items:center;gap:6px 10px;margin:10px 0}.bars .bar span{font-size:15px}.bars .bar i{display:block;height:20px;background:linear-gradient(90deg,#2f5d9e,#5b8fd6);border-radius:4px}.bars .bar b{grid-column:2;font-size:14px;color:#334;font-weight:500}
.wide svg{max-height:250px}
ul.check{list-style:none;padding:0;margin:0}ul.check li{padding:5px 0 5px 30px;position:relative;font-size:17px}ul.check li:before{content:"☐";position:absolute;left:0;font-size:20px;color:#2f5d9e}
.calcwrap{transform:scale(.86);transform-origin:top left;width:116%}
.calcwrap .mk-calc{grid-template-columns:280px minmax(0,1fr)}
#bar{position:fixed;left:0;top:0;height:4px;background:#2f5d9e;z-index:5;transition:width .2s}
#nav{position:fixed;right:14px;top:10px;opacity:.75;z-index:5;display:flex;gap:6px}#nav button{font:inherit;border:1px solid #c7d0da;background:#fff;border-radius:8px;padding:6px 12px;cursor:pointer}
#ov{position:fixed;inset:0;background:rgba(15,23,32,.92);z-index:10;display:none;overflow:auto;padding:24px}#ov.on{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
#ov div{background:#fff;border-radius:6px;padding:10px 12px;cursor:pointer;font-size:13.5px;min-height:70px}#ov div b{color:#2f5d9e;display:block;font-size:12px}#ov div:hover{outline:3px solid #5b8fd6}
@media print{@page{size:1280px 720px;margin:0}html,body{background:#fff;height:auto}#deck{position:static;display:block}.slide{display:block!important;position:relative;transform:none!important;box-shadow:none;border-radius:0;page-break-after:always;margin:0}#bar,#nav,#ov{display:none!important}}
"""

SLIDE_JS = r"""
var D=@@D@@;
(function(){
var S=[].slice.call(document.querySelectorAll('.slide')),cur=0,done={};
function fit(){var k=Math.min(innerWidth/1300,innerHeight/740);S.forEach(function(s){s.style.transform='scale('+k+')'})}
function go(i){i=Math.max(0,Math.min(S.length-1,i));S[cur].classList.remove('on');cur=i;S[i].classList.add('on');
 document.getElementById('bar').style.width=((i+1)/S.length*100)+'%';history.replaceState(null,'','#'+(i+1));
 var f=S[i].dataset.init;if(f&&!done[f]&&window[f]){done[f]=1;try{window[f]()}catch(e){console.log(e)}}}
addEventListener('keydown',function(e){if(e.target.tagName==='INPUT'||e.target.tagName==='SELECT')return;
 if(['ArrowRight','PageDown',' '].indexOf(e.key)>=0){e.preventDefault();go(cur+1)}else if(['ArrowLeft','PageUp'].indexOf(e.key)>=0){e.preventDefault();go(cur-1)}
 else if(e.key==='Home')go(0);else if(e.key==='End')go(S.length-1);else if(e.key==='o'||e.key==='O')ov();else if(e.key==='f'||e.key==='F'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen()}else if(e.key==='Escape')document.getElementById('ov').classList.remove('on')});
document.getElementById('pv').onclick=function(){go(cur-1)};document.getElementById('nx').onclick=function(){go(cur+1)};document.getElementById('ob').onclick=ov;
function ov(){var o=document.getElementById('ov');if(o.classList.contains('on')){o.classList.remove('on');return}
 o.innerHTML=S.map(function(s,i){var h=s.querySelector('h2,h1');return '<div data-i="'+i+'"><b>'+(i+1)+' · '+s.dataset.part+'</b>'+(h?h.textContent:'')+'</div>'}).join('');o.classList.add('on');
 o.querySelectorAll('div').forEach(function(d){d.onclick=function(){o.classList.remove('on');go(+d.dataset.i)}})}
addEventListener('resize',fit);fit();
var h=parseInt(location.hash.slice(1));go(isNaN(h)?0:h-1);
window.addEventListener('beforeprint',function(){S.forEach(function(s){var f=s.dataset.init;if(f&&!done[f]&&window[f]){done[f]=1;try{window[f]()}catch(e){}}})});
})();
function ctx(id){var c=document.getElementById(id),x=c.getContext('2d');x.clearRect(0,0,c.width,c.height);x.font='14px sans-serif';return [c,x]}
var COL=['#2f5d9e','#13733a','#a35c00','#c9302c','#6f5aa8','#0b7a86'];
function axes(x,L,T,W,H,xl,yl){x.strokeStyle='#9aa5b1';x.beginPath();x.moveTo(L,T);x.lineTo(L,T+H);x.lineTo(L+W,T+H);x.stroke();x.fillStyle='#4b5864';x.font='13px sans-serif';x.fillText(xl,L+W-x.measureText(xl).width,T+H+30);x.save();x.translate(L-44,T+H/2+40);x.rotate(-Math.PI/2);x.fillText(yl,0,0);x.restore()}
function initRough(){var o=document.getElementById('ruOpt'),sm=D.sra_med;function dr(){var r=ctx('ruCv'),c=r[0],x=r[1],L=60,T=20,W=470,H=300,op=+o.value;document.getElementById('ruV').textContent=op;
 axes(x,L,T,W,H,'거칠기 SRA (μm, 로그 눈금) →','g(SRA)');var lx=function(v){return L+(Math.log(v)-Math.log(5))/(Math.log(200)-Math.log(5))*W},ly=function(g){return T+H-g*H*0.95};
 [5,10,20,50,100,200].forEach(function(v){x.fillStyle='#8a96a3';x.fillText(v,lx(v)-6,T+H+16)});
 x.strokeStyle='#c9302c';x.lineWidth=3;x.beginPath();for(var i=0;i<=200;i++){var v=5*Math.pow(40,i/200),g=Math.exp(-Math.pow(Math.log(v/op),2)/(2*.64));i?x.lineTo(lx(v),ly(g)):x.moveTo(lx(v),ly(g))}x.stroke();x.lineWidth=1;
 Object.keys(sm).forEach(function(k,i){var v=sm[k],g=Math.exp(-Math.pow(Math.log(v/op),2)/(2*.64));x.fillStyle=COL[i];x.beginPath();x.arc(lx(v),ly(g),7,0,7);x.fill();x.fillText('● ',L+W-175,T+14+i*20);x.fillStyle='#16212b';x.fillText(k+'  '+v+' μm',L+W-160,T+14+i*20)})}
 o.oninput=dr;dr()}
function initLHS(){var n=document.getElementById('lhN'),seed=1;function rnd(){seed=(seed*69069+1)%4294967296;return seed/4294967296}
 function dr(){var N=+n.value;document.getElementById('lhV').textContent=N;var r=ctx('lhCv'),x=r[1];
  [[0,'무작위'],[1,'라틴 하이퍼큐브']].forEach(function(p){var L=20+p[0]*295,T=28,S=260;x.fillStyle='#16212b';x.font='15px sans-serif';x.fillText(p[1],L,18);x.strokeStyle='#e1e5ea';
   for(var i=0;i<=N;i++){x.beginPath();x.moveTo(L+S*i/N,T);x.lineTo(L+S*i/N,T+S);x.moveTo(L,T+S*i/N);x.lineTo(L+S,T+S*i/N);x.stroke()}
   var pts=[];if(p[0]===0){for(var i=0;i<N;i++)pts.push([rnd(),rnd()])}else{var a=[],b=[];for(var i=0;i<N;i++){a.push(i);b.push(i)}
    for(var i=N-1;i>0;i--){var j=Math.floor(rnd()*(i+1)),t=b[i];b[i]=b[j];b[j]=t}for(var i=0;i<N;i++)pts.push([(a[i]+rnd())/N,(b[i]+rnd())/N])}
   x.fillStyle=p[0]?'#13733a':'#c9302c';pts.forEach(function(q){x.beginPath();x.arc(L+q[0]*S,T+(1-q[1])*S,5,0,7);x.fill()});x.strokeStyle='#9aa5b1';x.strokeRect(L,T,S,S)})}
 n.oninput=dr;document.getElementById('lhR').onclick=function(){seed=Math.floor(Math.random()*1e6);dr()};dr()}
function initDist(){var si=document.getElementById('dsItem'),sb=document.getElementById('dsBy'),names=D.x8.concat(['Voc_V']);names.forEach(function(n,i){si.add(new Option(n,i))});si.value=names.length-1;
 function dr(){var k=+si.value,by=+sb.value,r=ctx('dsCv'),c=r[0],x=r[1],L=170,T=20,W=930,H=420,g={},keys;
  D.tr.forEach(function(row){var key=by?D.strs[row[1]]:D.mats[row[0]];(g[key]=g[key]||[]).push(row[2+k])});keys=Object.keys(g);
  var all=[].concat.apply([],keys.map(function(q){return g[q]})),lo=Math.min.apply(0,all),hi=Math.max.apply(0,all),lg=lo>0,
   f=function(v){return lg?(Math.log(v)-Math.log(lo))/(Math.log(hi)-Math.log(lo)):(v-lo)/(hi-lo)},rh=H/keys.length;
  x.fillStyle='#4b5864';x.font='13px sans-serif';for(var t=0;t<=4;t++){var v=lg?Math.exp(Math.log(lo)+(Math.log(hi)-Math.log(lo))*t/4):lo+(hi-lo)*t/4;x.fillText(v.toPrecision(3),L+W*t/4-12,T+H+18)}
  x.fillText(names[k]+(lg?' (로그 눈금)':''),L+W-120,T+H+36);
  keys.forEach(function(q,i){var a=g[q].slice().sort(function(u,v){return u-v}),y0=T+i*rh+rh/2,qq=function(p){return a[Math.floor(p*(a.length-1))]};
   x.fillStyle='#16212b';x.font='15px sans-serif';x.fillText(q+' ('+a.length+')',10,y0+5);
   x.fillStyle='rgba(47,93,158,.18)';x.fillRect(L+f(qq(.25))*W,y0-rh*.3,(f(qq(.75))-f(qq(.25)))*W,rh*.6);x.fillStyle='#2f5d9e';x.fillRect(L+f(qq(.5))*W-1.5,y0-rh*.34,3,rh*.68);
   x.fillStyle=COL[i%6];var s=7;a.forEach(function(v){s=(s*69069+1)%4294967296;x.globalAlpha=.55;x.beginPath();x.arc(L+f(v)*W,y0+(s/4294967296-.5)*rh*.5,2.6,0,7);x.fill()});x.globalAlpha=1})}
 si.onchange=dr;sb.onchange=dr;dr()}
function initCV(){var t=document.getElementById('cvT'),cv=D.tr.map(function(r){return r[11]}).sort(function(a,b){return a-b});document.getElementById('cvM').textContent=cv[Math.floor(cv.length/2)].toFixed(3);
 function dr(){var th=+t.value;document.getElementById('cvV').textContent=th.toFixed(2);var r=ctx('cvCv'),x=r[1],L=60,T=20,W=530,H=300,bins=new Array(30).fill(0),mx=0.3;
  cv.forEach(function(v){bins[Math.min(29,Math.floor(v/mx*30))]++});var m=Math.max.apply(0,bins);axes(x,L,T,W,H,'Voc 반복 변동계수 CV →','원단 수');
  bins.forEach(function(b,i){var x0=L+i*W/30;x.fillStyle=(i+.5)*mx/30>th?'#c9302c':'#5b8fd6';x.fillRect(x0+1,T+H-b/m*H,W/30-2,b/m*H)});
  x.strokeStyle='#16212b';x.setLineDash([5,4]);x.beginPath();x.moveTo(L+th/mx*W,T);x.lineTo(L+th/mx*W,T+H);x.stroke();x.setLineDash([]);
  [0,.1,.2,.3].forEach(function(v){x.fillStyle='#8a96a3';x.fillText(v.toFixed(1),L+v/mx*W-8,T+H+16)});
  document.getElementById('cvN').textContent=cv.filter(function(v){return v>th}).length+' / '+cv.length}
 t.oninput=dr;dr()}
function initPCA(){var by=document.getElementById('pcBy'),wsel=document.getElementById('pcW'),c=document.getElementById('pcCv'),hov=-1,pts=[];
 function dr(){var r=ctx('pcCv'),x=r[1],L=50,T=20,W=530,H=380,P=D.pc,xs=P.map(function(p){return p[0]}),ys=P.map(function(p){return p[1]}),
  x0=Math.min.apply(0,xs),x1=Math.max.apply(0,xs),y0=Math.min.apply(0,ys),y1=Math.max.apply(0,ys),k=+by.value,keys=[];
  axes(x,L,T,W,H,'PC1 ('+Math.round(D.ev[0]*100)+'%) →','PC2 ('+Math.round(D.ev[1]*100)+'%)');pts=[];
  D.tr.forEach(function(row,i){var key=row[1-k===0?0:1];key=k?row[1]:row[0];if(keys.indexOf(key)<0)keys.push(key);var px=L+(P[i][0]-x0)/(x1-x0)*W,py=T+H-(P[i][1]-y0)/(y1-y0)*H;pts.push([px,py,i]);
   x.fillStyle=COL[keys.indexOf(key)%6];x.globalAlpha=.7;x.beginPath();x.arc(px,py,i===hov?6:3.5,0,7);x.fill()});x.globalAlpha=1;
  var lx0=L+10;keys.forEach(function(q,i){var nm=k?D.strs[q]:D.mats[q];x.fillStyle=COL[i%6];x.fillRect(lx0,T-4,10,10);x.fillStyle='#16212b';x.fillText(nm,lx0+14,T+6);lx0+=x.measureText(nm).width+30});
  if(hov>=0){var row=D.tr[hov];x.fillStyle='rgba(22,33,43,.9)';var s=D.mats[row[0]]+' · '+D.strs[row[1]]+' · Voc '+row[10].toFixed(1)+' V';x.fillRect(L+10,T+H-34,x.measureText(s).width+16,24);x.fillStyle='#fff';x.fillText(s,L+18,T+H-17)}
  var r2=ctx('pcL'),y=r2[1],j=+wsel.value,ld=D.load.slice().sort(function(a,b){return Math.abs(b[1+j])-Math.abs(a[1+j])}),cx=300,bh=20;y.fillStyle='#16212b';y.font='15px sans-serif';y.fillText('PC'+(j+1)+' 가중치 (W의 '+(j+1)+'열, 길이 1)',20,18);
  ld.forEach(function(l,i){var v=l[1+j],yy=32+i*21;y.fillStyle='#16212b';y.font='13px sans-serif';y.fillText(l[0],20,yy+13);y.fillStyle=v>=0?'#d6782a':'#2f5d9e';y.fillRect(v>=0?cx:cx+v*400,yy+2,Math.abs(v)*400,15);y.fillStyle='#4b5864';y.fillText(v.toFixed(2),v>=0?cx+v*400+4:cx+v*400-36,yy+14)});
  y.strokeStyle='#9aa5b1';y.beginPath();y.moveTo(cx,28);y.lineTo(cx,32+19*21);y.stroke()}
 c.onmousemove=function(e){var b=c.getBoundingClientRect(),mx=(e.clientX-b.left)*c.width/b.width,my=(e.clientY-b.top)*c.height/b.height,best=-1,bd=100;pts.forEach(function(p){var d=(p[0]-mx)*(p[0]-mx)+(p[1]-my)*(p[1]-my);if(d<bd){bd=d;best=p[2]}});if(best!==hov){hov=best;dr()}};
 by.onchange=dr;wsel.onchange=dr;dr()}
function initEM(){var k=document.getElementById('emK'),X=D.tr.map(function(r,i){return [D.pc[i][0],Math.log(r[10])]}),n=X.length,samp=[],G=null;
 var m=[0,0];X.forEach(function(p){m[0]+=p[0]/n;m[1]+=p[1]/n});var s=[0,0];X.forEach(function(p){s[0]+=Math.pow(p[0]-m[0],2)/n;s[1]+=Math.pow(p[1]-m[1],2)/n});X=X.map(function(p){return [(p[0]-m[0])/Math.sqrt(s[0]),(p[1]-m[1])/Math.sqrt(s[1])]});
 function pdf(p,mu,S){var a=S[0],b=S[1],d=S[3],det=a*d-b*b,dx=p[0]-mu[0],dy=p[1]-mu[1],q=(d*dx*dx-2*b*dx*dy+a*dy*dy)/det;return Math.exp(-q/2)/(2*Math.PI*Math.sqrt(det))}
 function fitK(K){var seed=5;function rnd(){seed=(seed*69069+1)%4294967296;return seed/4294967296}
  var mu=[X[Math.floor(rnd()*n)]];while(mu.length<K){var d=X.map(function(p){return Math.min.apply(0,mu.map(function(c){return Math.pow(p[0]-c[0],2)+Math.pow(p[1]-c[1],2)}))}),t=d.reduce(function(a,b){return a+b})*rnd(),acc=0;for(var i=0;i<n;i++){acc+=d[i];if(acc>=t){mu.push(X[i].slice());break}}}
  var S=mu.map(function(){return [.3,0,0,.3]}),pi=mu.map(function(){return 1/K}),ll=0;
  for(var it=0;it<150;it++){var R=X.map(function(p){var r=mu.map(function(c,j){return pi[j]*pdf(p,c,S[j])}),z=r.reduce(function(a,b){return a+b})||1e-300;return r.map(function(v){return v/z})});
   ll=X.reduce(function(a,p){return a+Math.log(mu.reduce(function(s2,c,j){return s2+pi[j]*pdf(p,c,S[j])},0)||1e-300)},0);
   for(var j=0;j<K;j++){var Nj=0,mx=0,my=0;for(var i=0;i<n;i++){Nj+=R[i][j];mx+=R[i][j]*X[i][0];my+=R[i][j]*X[i][1]}mx/=Nj;my/=Nj;var a=0,b=0,d=0;
    for(var i=0;i<n;i++){var dx=X[i][0]-mx,dy=X[i][1]-my;a+=R[i][j]*dx*dx;b+=R[i][j]*dx*dy;d+=R[i][j]*dy*dy}mu[j]=[mx,my];S[j]=[a/Nj+1e-3,b/Nj,b/Nj,d/Nj+1e-3];pi[j]=Nj/n}}
  return {mu:mu,S:S,pi:pi,ll:ll,bic:-2*ll+(K*6-1)*Math.log(n)}}
 function sample(g,N){var out=[],seed=11;function rnd(){seed=(seed*69069+1)%4294967296;return seed/4294967296}function gn(){var u=rnd()||1e-9,v=rnd();return Math.sqrt(-2*Math.log(u))*Math.cos(6.2832*v)}
  for(var i=0;i<N;i++){var t=rnd(),j=0,acc=0;for(;j<g.pi.length;j++){acc+=g.pi[j];if(t<=acc)break}j=Math.min(j,g.pi.length-1);var S=g.S[j],l11=Math.sqrt(S[0]),l21=S[1]/l11,l22=Math.sqrt(Math.max(S[3]-l21*l21,1e-9)),e1=gn(),e2=gn();out.push([g.mu[j][0]+l11*e1,g.mu[j][1]+l21*e1+l22*e2])}return out}
 function dr(){var r=ctx('emCv'),x=r[1],L=50,T=20,W=620,H=380,f=function(p){return [L+(p[0]+3)/6*W,T+H-(p[1]+3)/6*H]};axes(x,L,T,W,H,'PC1 점수 (표준화) →','log Voc (표준화)');
  x.fillStyle='rgba(47,93,158,.45)';X.forEach(function(p){var q=f(p);x.beginPath();x.arc(q[0],q[1],3,0,7);x.fill()});
  if(G){G.mu.forEach(function(c,j){var S=G.S[j],a=S[0],b=S[1],d=S[3],tr=(a+d)/2,dd=Math.sqrt(Math.max(tr*tr-(a*d-b*b),0)),l1=tr+dd,l2=tr-dd,ang=Math.atan2(l1-a,b||1e-9);
    x.strokeStyle=COL[(j+3)%6];x.lineWidth=2.5;x.beginPath();for(var t=0;t<=60;t++){var u=t/60*6.2832,ex=2*Math.sqrt(l1)*Math.cos(u),ey=2*Math.sqrt(Math.max(l2,1e-9))*Math.sin(u),px=c[0]+ex*Math.cos(ang)-ey*Math.sin(ang),py=c[1]+ex*Math.sin(ang)+ey*Math.cos(ang),q=f([px,py]);t?x.lineTo(q[0],q[1]):x.moveTo(q[0],q[1])}x.stroke();x.lineWidth=1})}
  x.fillStyle='rgba(111,90,168,.85)';samp.forEach(function(p){var q=f(p);x.beginPath();x.arc(q[0],q[1],3.4,0,7);x.fill()})}
 function run(){var K=+k.value;document.getElementById('emV').textContent=K;G=fitK(K);samp=[];document.getElementById('emLL').textContent=G.ll.toFixed(0);document.getElementById('emB').textContent=G.bic.toFixed(0);dr()}
 k.oninput=run;document.getElementById('emS').onclick=function(){samp=sample(G,200);dr()};run()}
function initInv(){var o=document.getElementById('ivOut'),IV=@@IV@@;function show(t){document.querySelectorAll('[data-iv]').forEach(function(b){b.classList.toggle('on',+b.dataset.iv===t)});var rows=IV[t],m=Math.max.apply(0,rows.map(function(r){return r[2]}));
 o.innerHTML='<div class="bars">'+rows.map(function(r){return '<div class="bar"><span>'+r[0]+' · '+r[1]+'</span><i style="width:'+(r[2]/m*100)+'%"></i><b>'+r[2]+' / 200</b></div>'}).join('')+'</div>'}
 document.querySelectorAll('[data-iv]').forEach(function(b){b.onclick=function(){show(+b.dataset.iv)}});show(90)}
"""

_slides_html = ('<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
  '<title>섬유직물 데이터 생성 가이드 — 웹 슬라이드</title><style>' + SLIDE_CSS + '</style>' + MK_CSS + '</head><body>'
  '<div id="bar"></div><div id="deck">' + ''.join(_secs) + '</div>'
  '<div id="nav"><button id="pv" aria-label="이전">←</button><button id="ob">전체 보기 (O)</button><button id="nx" aria-label="다음">→</button></div><div id="ov"></div>'
  '<script>' + SLIDE_JS.replace('@@D@@', _SDJ).replace('@@IV@@', _sj.dumps({str(k): v for k, v in _inv.items()}, ensure_ascii=False)) + '</script></body></html>')
open(os.path.join(B, '..', 'slides', 'index.html'), 'w', encoding='utf-8').write(_slides_html)
print('slides/index.html', _N, 'slides', len(_slides_html) // 1024, 'KB')
