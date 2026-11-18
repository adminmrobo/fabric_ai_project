# ---- 웹 슬라이드: 섬유직물 데이터 생성 가이드 (slides/index.html) ----
# build_pages.py 안에서 pages_method.py, pages_mock.py 다음에 exec 로 실행된다.
# 글 자료는 slides_content.py, 스타일은 slides.css, 대시보드 스크립트는 slides.js
import json as _sj, numpy as _np, pandas as _pd, html as _html, sys as _sys
from sklearn.mixture import GaussianMixture as _GMM
_sys.path.insert(0, B)
import slides_content as SC

_PR = os.path.join(B, '..', 'practice')
def _rd(n): return _pd.read_csv(os.path.join(_PR, 'data', n), encoding='utf-8-sig')
_tr, _gen, _ks, _tstr, _base, _ver, _qc, _tmpl, _lc = [_rd(n) for n in (
    '02_train.csv', '04_generated_candidates_example.csv', '05_ks_example.csv', '05_tstr_result_example.csv',
    '05_baseline_scores_example.csv', '07_verification_result_example.csv', '03_qc_report_example.csv',
    '00_measurement_template.csv', '09_learning_curve_example.csv')]
_X19 = ["W", "SFC_F", "SFC_B", "SRA_F", "SRA_B", "SRW_F", "SRW_B", "BAR_F", "BAR_B", "BW_FL", "BW_FC", "BW_BL", "BW_BC", "CW_F", "CW_B", "CRR_F", "CRR_B", "Qmax_F", "Qmax_B"]
_X8 = ["W", "SFC_F", "SRA_F", "SRW_F", "BAR_F", "CW_F", "CRR_F", "Qmax_F"]
_DJ = _sj.load(open(os.path.join(B, 'data.json'), encoding='utf-8'))

# PCA (학습 자료, 로그·표준화)
_Z = _np.log(_tr[_X19].values); _Z = (_Z - _Z.mean(0)) / _Z.std(0, ddof=1)
_U, _s, _Vt = _np.linalg.svd(_Z, full_matrices=False)
_ev = (_s ** 2 / (_s ** 2).sum())[:3]
_W = _Vt[:2].T
for _j in range(2):
    if _W[:, _j].sum() < 0: _W[:, _j] *= -1
_P = _Z @ _W

# 역방향 (Lab 7과 같은 방식)
_cols = _X8 + ["Voc_V"]; _L = _np.log(_tr[_cols].values); _mu, _sd = _L.mean(0), _L.std(0, ddof=1); _ZZ = (_L - _mu) / _sd
_g = _GMM(4, covariance_type='full', random_state=0, n_init=5).fit(_ZZ)
_full = _rd('01_mock_full.csv')
_Lf = _np.log(_full[_X8].values); _Zf = (_Lf - _Lf.mean(0)) / _Lf.std(0, ddof=1)
_inv = {}
for _t in (30, 60, 90):
    yz = (_np.log(_t) - _mu[-1]) / _sd[-1]
    w = _np.array([_g.weights_[k] * _np.exp(-0.5 * (yz - _g.means_[k][-1]) ** 2 / _g.covariances_[k][-1, -1]) / _np.sqrt(_g.covariances_[k][-1, -1]) for k in range(4)]); w /= w.sum()
    rng = _np.random.default_rng(3); cnt = {}
    for i in range(200):
        k = rng.choice(4, p=w); m, S_ = _g.means_[k], _g.covariances_[k]
        Sxy, Syy = S_[:-1, -1], S_[-1, -1]
        x = rng.multivariate_normal(m[:-1] + Sxy / Syy * (yz - m[-1]), S_[:-1, :-1] - _np.outer(Sxy, Sxy) / Syy)
        xr = _np.exp(x * _sd[:-1] + _mu[:-1]); zf = (_np.log(xr) - _Lf.mean(0)) / _Lf.std(0, ddof=1)
        j = int(_np.argmin(((_Zf - zf) ** 2).sum(1))); key = (_full.material.iloc[j], _full.structure.iloc[j]); cnt[key] = cnt.get(key, 0) + 1
    _inv[str(_t)] = sorted([[MG.MATERIALS[a]['ko'], MG.STRUCTURES[b]['ko'], c] for (a, b), c in cnt.items()], key=lambda r: -r[2])[:6]

_gs_ = _gen.sample(400, random_state=1)
_GRP = ['기본', '표면 FTT', '역학 FTT', '열 FTT', '표면 KES', '역학 KES', '인장', '기타 열']
SD = dict(
    tr=[[r.material, r.structure] + [round(float(getattr(r, c)), 4) for c in _X8] + [round(float(r.Voc_V), 2), round(float(r.Voc_cv), 4)] for r in _tr.itertuples()],
    x8=_X8, pc=[[round(float(a), 3), round(float(b), 3)] for a, b in _P], ev=[round(float(e), 3) for e in _ev],
    load=[[c, round(float(_W[i, 0]), 3), round(float(_W[i, 1]), 3)] for i, c in enumerate(_X19)],
    gen=[[round(float(r.W), 2), round(float(r.CW_F), 4), round(float(r.SRA_F), 2), round(float(r.Qmax_F), 4), round(float(r.Voc_pred), 2), round(float(r.Voc_lo95), 2), round(float(r.Voc_hi95), 2), bool(r.in_domain), round(float(r.Voc_sampled), 2)] for r in _gs_.itertuples()],
    mats={k: v['ko'] for k, v in MG.MATERIALS.items()}, strs={k: v['ko'] for k, v in MG.STRUCTURES.items()},
    M=MG.MATERIALS, S=MG.STRUCTURES, C=MG.COUNTER, PR=MG.PROTOCOL, s0=MG.SIGMA0_UC, sopt=MG.SRA_OPT,
    sra_med={MG.STRUCTURES[k]['ko']: round(float(v), 1) for k, v in _df.groupby('structure').SRA_F.median().items()},
    cov=[[s_['id'], s_['src']] + [round(c / g, 2) for c, g in zip(s_['cov'], _DJ['gsize'])] for s_ in _DJ['samples']], grp=_GRP,
    lc={m: [[int(r.n), round(float(r['mean']), 3), round(float(r['std']), 3)] for _, r in g.iterrows()] for m, g in _lc.groupby('model')},
    inv=_inv,
)
_SDJ = _sj.dumps(SD, ensure_ascii=False, separators=(',', ':'))

# ---------------- 도우미 ----------------
def _tbl(head, rows, cls='t'):
    return f'<table class="{cls}"><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</table>'
def _ref(*ks): return '<sup class="rf">' + ','.join(ks) + '</sup>'
def _f(v, n=2): return f'{v:.{n}f}'
def _side(title, body): return f'<aside class="side"><h4>{title}</h4>{body}</aside>'
def _cv(id_, w=620, h=380): return f'<canvas id="{id_}" width="{w}" height="{h}"></canvas>'

# 팔레트 (참고 교안 스타일)
NV, OR, SG, IN, AM = '#22398f', '#c4561a', '#7f9c62', '#5b63a8', '#e0a84a'

def _weave(kind, n=10, cell=14, x0=0, y0=0):
    o = []
    if kind in ('plain', 'twill22', 'hopsack22'):
        for i in range(n):
            for j in range(n):
                up = {'plain': (i + j) % 2 == 0, 'twill22': (i - j) % 4 < 2, 'hopsack22': ((i // 2) + (j // 2)) % 2 == 0}[kind]
                o.append(f'<rect x="{x0 + j * cell}" y="{y0 + i * cell}" width="{cell - 1}" height="{cell - 1}" rx="3" fill="{IN if up else AM}" opacity="{0.85 if up else 0.75}"/>')
    elif kind == 'jersey':
        for i in range(n):
            for j in range(n // 2):
                cx, cy = x0 + j * cell * 2 + cell, y0 + i * cell + cell / 2
                o.append(f'<path d="M{cx - cell * .9:.1f},{cy - cell * .4:.1f} Q{cx:.1f},{cy + cell * .9:.1f} {cx + cell * .9:.1f},{cy - cell * .4:.1f}" fill="none" stroke="{SG}" stroke-width="3" stroke-linecap="round"/>')
    else:
        r = _np.random.default_rng(4)
        for q in range(60):
            a, b = r.uniform(0, n * cell, 2); t = r.uniform(0, 3.14); L = r.uniform(20, 60)
            o.append(f'<line x1="{x0 + a:.0f}" y1="{y0 + b:.0f}" x2="{x0 + min(n * cell, max(0, a + L * _np.cos(t))):.0f}" y2="{y0 + min(n * cell, max(0, b + L * _np.sin(t))):.0f}" stroke="{[IN, AM, SG][q % 3]}" stroke-width="2" opacity=".7"/>')
    return ''.join(o)

def _svg(w, h, inner): return _uniq(f'<svg viewBox="0 0 {w} {h}" style="width:100%;height:auto" xmlns="http://www.w3.org/2000/svg"><rect width="{w}" height="{h}" rx="16" fill="#fbf6ee"/>{inner}</svg>')
def _t(x, y, s, size=14, fill='#33415c', anchor='middle', wt=500): return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{wt}">{s}</text>'
def _box(x, y, w, h, fill, label, sub='', fs=15):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" opacity=".92"/>' + _t(x + w / 2, y + h / 2 - (6 if sub else -5), label, fs, '#fff', wt=700)
            + (_t(x + w / 2, y + h / 2 + 14, sub, 12, '#fff') if sub else ''))
_ARW = '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" fill="#7a8394"/></marker></defs>'
_MK = [0]
def _uniq(svg):
    _MK[0] += 1; return svg.replace('id="ah"', f'id="ah{_MK[0]}"').replace('url(#ah)', f'url(#ah{_MK[0]})')
def _ar(x1, y1, x2, y2, dash=False):
    d = ' stroke-dasharray="5 5"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#7a8394" stroke-width="2"{d} marker-end="url(#ah)"/>'
def _pts(rng, centers, sds, r=3.5, fill='#33415c', op=.55, dx=0):
    o = []
    for (cx, cy), (sx, sy), n in zip(centers, sds, [25, 30, 20, 25, 25]):
        for x, y in rng.normal([cx, cy], [sx, sy], (n, 2)): o.append(f'<circle cx="{x + dx:.0f}" cy="{y:.0f}" r="{r}" fill="{fill}" opacity="{op}"/>')
    return ''.join(o)

FB = {}
FB['GS01'] = _svg(680, 384, _ARW + _weave('plain', 12, 16, 40, 96) + _ar(250, 192, 330, 192)
    + ''.join(f'<circle cx="{360 + (i % 8) * 18}" cy="{120 + (i // 8) * 16}" r="4" fill="{IN if (i + i // 8) % 2 else AM}"/>' for i in range(80))
    + _ar(510, 192, 560, 192) + '<rect x="570" y="120" width="90" height="150" rx="10" fill="#fff" stroke="#dcd6c8"/>'
    + ''.join(f'<rect x="{582 + i * 15}" y="{255 - h}" width="11" height="{h}" rx="2" fill="{[IN, SG, AM, OR, IN][i]}"/>' for i, h in enumerate([40, 70, 55, 95, 80]))
    + _t(136, 330, '실·직물', 15) + _t(425, 330, '데이터 격자', 15) + _t(615, 330, '예측', 15))
FB['GS02'] = _svg(680, 384, _ARW + _box(30, 70, 150, 90, IN, 'FTT', '표면·굽힘·압축·열') + _box(30, 220, 150, 90, OR, 'TENG 시험기', '접촉-분리 Voc·Q·I')
    + _box(220, 150, 130, 80, SG, '온습도계', 'RH 65 ± 2%') + _ar(180, 115, 425, 165) + _ar(180, 265, 425, 205) + _ar(350, 190, 425, 188)
    + '<rect x="430" y="90" width="220" height="190" rx="12" fill="#fff" stroke="#dcd6c8"/>'
    + ''.join(f'<line x1="440" y1="{120 + i * 26}" x2="640" y2="{120 + i * 26}" stroke="#e4ddcd"/>' for i in range(6))
    + ''.join(f'<line x1="{480 + i * 40}" y1="100" x2="{480 + i * 40}" y2="270" stroke="#e4ddcd"/>' for i in range(4)) + _t(540, 315, '측정 기록 양식 (52열)', 15))
FB['GS03'] = _svg(700, 210, ''.join(_weave(k, 8, 14, 23 + i * 136, 22) + _t(79 + i * 136, 168 + 22, n, 15) for i, (k, n) in enumerate([('plain', '평직'), ('twill22', '능직 2/2'), ('hopsack22', '호프색 2/2'), ('jersey', '싱글 저지'), ('needle', '니들펀치')])))
def _teng(x0, sep):
    gap = 70 if sep else 0; o = []
    o.append(f'<rect x="{x0}" y="60" width="220" height="16" rx="4" fill="#9aa3b5"/>' + _t(x0 + 110, 52, '전극', 12))
    o.append(f'<rect x="{x0}" y="76" width="220" height="34" rx="6" fill="{AM}"/>' + _t(x0 + 110, 98, '직물', 13, '#5a3a00', wt=700))
    o.append(f'<rect x="{x0}" y="{110 + gap}" width="220" height="22" rx="6" fill="{IN}"/>' + _t(x0 + 110, 126 + gap, 'PTFE 필름', 12, '#fff', wt=700))
    o.append(f'<rect x="{x0}" y="{132 + gap}" width="220" height="16" rx="4" fill="#9aa3b5"/>')
    o += [f'<text x="{x0 + 8 + i * 22}" y="108" font-size="14" fill="{OR}" font-weight="700">+</text>' for i in range(10) if i not in (4, 5)]
    o += [f'<text x="{x0 + 10 + i * 22}" y="{125 + gap}" font-size="16" fill="#fff" font-weight="700">−</text>' for i in range(10) if i not in (4, 5)]
    if sep:
        o.append(f'<line x1="{x0 + 238}" y1="112" x2="{x0 + 238}" y2="178" stroke="{OR}" stroke-width="2" marker-end="url(#ah)"/>' + _t(x0 + 254, 150, 'x', 15, OR, wt=700))
        o.append(f'<path d="M{x0 - 4},68 H{x0 - 30} V{140 + gap} H{x0 - 4}" fill="none" stroke="{OR}" stroke-width="2.5"/><circle cx="{x0 - 30}" cy="{(68 + 140 + gap) / 2}" r="10" fill="#ffe08a" stroke="{OR}"/>')
    return ''.join(o)
FB['GS04'] = _svg(680, 300, _ARW + _teng(60, False) + _teng(390, True) + _t(170, 250, '① 접촉 — 전하가 옮겨 감', 15) + _t(500, 280, '② 분리 — 전압 Voc = σx/ε₀', 15))
def _rough(x0, amp, per, pw):
    ys = [150 - amp * (0.5 + 0.5 * _np.cos(2 * 3.14159 * i / per)) ** pw for i in range(101)]
    pts = ' '.join(f'{x0 + i * 2},{y:.1f}' for i, y in enumerate(ys))
    hits = ''.join(f'<circle cx="{x0 + i * 2}" cy="112" r="3.5" fill="{OR}"/>' for i, y in enumerate(ys) if y <= 113.5 and i % 3 == 0)
    return f'<rect x="{x0}" y="96" width="200" height="14" rx="4" fill="{IN}"/><polyline points="{pts} {x0 + 200},190 {x0},190" fill="{AM}" opacity=".85"/>{hits}'
FB['GS05'] = _svg(680, 240, _rough(20, 40, 100, 0.08) + _rough(240, 38, 20, 1.2) + _rough(460, 40, 25, 8) + _t(120, 220, '매끈 — 얕게 닿음', 13) + _t(340, 220, '적당한 요철 — 접촉 최대', 13, OR, wt=700) + _t(560, 220, '아주 거침 — 꼭짓점만', 13))
FB['GS06'] = _svg(680, 240, '<rect x="40" y="110" width="600" height="40" rx="18" fill="#e0a84a"/>'
    + ''.join(f'<text x="{60 + i * 26}" y="106" font-size="18" fill="{OR}" font-weight="700" opacity="{max(0.1, 1 - max(0, i - 11) / 11):.2f}">+</text>' for i in range(23))
    + ''.join(f'<ellipse cx="{360 + i * 24}" cy="{92 - (i % 2) * 10}" rx="8" ry="10" fill="#9ec5e8" opacity=".85"/>' for i in range(11))
    + _t(180, 190, '건조 — 전하가 남음', 15) + _t(500, 190, '습함 — 물 분자로 새어 나감', 15))
FB['GS07'] = _svg(700, 200, _ARW + ''.join(_box(14 + i * 114, 60, 96, 70, c, a, b, 14) + (_ar(110 + i * 114, 95, 126 + i * 114, 95) if i < 5 else '')
    for i, (a, b, c) in enumerate([('섬유', '소재 대표값', IN), ('실', 'tex·지름', SG), ('직물', '구조·밀도', AM), ('물성 19', '+ 잡음', IN), ('전기 Y', '+ 습도·잡음', OR), ('품질 검사', '기록·is_mock', SG)])))
_ell = lambda L: ''.join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({a} {cx} {cy})" fill="{c}" opacity=".22" stroke="{c}" stroke-width="2"/>' for cx, cy, rx, ry, a, c in L)
FB['GS08'] = _svg(680, 300, '<line x1="60" y1="260" x2="640" y2="260" stroke="#7a8394"/><line x1="60" y1="260" x2="60" y2="30" stroke="#7a8394"/>'
    + _ell([(170, 190, 90, 40, -20, IN), (340, 130, 110, 36, -35, SG), (520, 80, 80, 30, -10, AM)])
    + _pts(_np.random.default_rng(2), [(170, 190), (340, 130), (520, 80)], [(45, 18), (55, 18), (40, 15)])
    + _pts(_np.random.default_rng(9), [(170, 190), (340, 130), (520, 80)], [(45, 18), (55, 18), (40, 15)], 3, '#8a5fbf', .8)
    + _t(350, 290, '직물 특성 x', 13) + _t(40, 150, 'y', 15, wt=700))
FB['GS09'] = _svg(680, 260, '<path d="M60,220 C160,220 180,60 260,60 C340,60 360,220 460,220" fill="#5b63a8" opacity=".25" stroke="#5b63a8" stroke-width="2"/>'
    '<path d="M100,220 C200,220 210,80 290,80 C370,80 390,220 500,220" fill="#f2c27a" opacity=".35" stroke="#d9772b" stroke-width="2"/>'
    + '<rect x="530" y="60" width="120" height="150" rx="12" fill="#fff" stroke="#dcd6c8"/>' + ''.join(f'<text x="548" y="{100 + i * 38}" font-size="20" fill="{SG}">✓</text><rect x="574" y="{88 + i * 38}" width="60" height="10" rx="5" fill="#e4ddcd"/>' for i in range(3))
    + _t(160, 248, '모의', 14, IN, wt=700) + _t(380, 248, '실측', 14, OR, wt=700))
FB['GS10'] = _svg(680, 260, _ARW + '<rect x="40" y="50" width="240" height="150" rx="12" fill="#2b3550"/>' + ''.join(f'<rect x="60" y="{72 + i * 18}" width="{[150, 110, 170, 90, 130, 100][i]}" height="8" rx="4" fill="{[AM, IN, SG, OR, IN, AM][i]}" opacity=".9"/>' for i in range(6))
    + _ar(290, 125, 350, 125) + f'<rect x="360" y="80" width="130" height="90" rx="40" fill="#fff" stroke="{IN}" stroke-width="2"/>' + ''.join(f'<circle cx="{400 + i * 25}" cy="125" r="7" fill="{IN}"/>' for i in range(3))
    + _ar(500, 125, 540, 125) + '<rect x="550" y="70" width="100" height="110" rx="10" fill="#fff" stroke="#dcd6c8"/>' + ''.join(f'<line x1="560" y1="{95 + i * 20}" x2="640" y2="{95 + i * 20}" stroke="#e4ddcd"/>' for i in range(4))
    + _t(160, 230, '프롬프트', 14) + _t(425, 230, 'LLM', 14) + _t(600, 230, '코드·표', 14))

GSMAP = {g[0]: g for g in SC.GS_REQ}
def _gs(id_, h=300):
    g = GSMAP[id_]
    return (f'<figure class="gs"><div class="gsi" style="max-height:{h}px"><img src="img/gs/{id_}.png" alt="{g[2]}" onerror="this.remove()"><div class="fb">{FB[id_]}</div></div>'
            f'<figcaption>{g[2]} <span>{id_}</span></figcaption></figure>')

SL = []
def S(part, title, body, init=''): SL.append((part, title, body, init))
PARTS = [('0', '표지'), ('1', '왜 데이터를 만드나'), ('2', '데이터 기초'), ('3', '섬유 메커니즘'), ('4', '섬유 특성 → 전기 특성'), ('5', '데이터 생성 원칙'),
         ('6', '생성 절차'), ('7', '데이터 검증'), ('8', '방법론'), ('9', '실습'), ('10', '향후 연구'), ('A', '부록 A · 프롬프트 가이드'), ('B', '부록 B · 이미지 요청서'), ('R', '참고문헌')]
P = {k: (k, v) for k, v in PARTS}

# ================= 0 표지 =================
S(P['0'], '', '<div class="cover"><div><div class="eyeb">한양대 스마트텍스타일연구실 · 직물 마찰전기 AI 과제 · 1차년도</div>'
  '<h1>섬유직물 데이터<br>생성 가이드</h1><p class="sub">섬유 메커니즘 · 전기 특성 · 생성 원칙 · 검증 · 실습</p>'
  '<p class="lead">실측 직물 데이터의 패턴(결합분포)을 학습하는 생성 모델로 새 직물을 만들고,<br>그 직물의 전기적 특성을 연속값(회귀형 출력)으로 예측한다.</p>'
  '<div class="who">2026-11-18 · 연구진 공유용 · 글 안상선</div><div class="keys">← → 이동 · O 전체 보기 · F 전체 화면 · 인쇄하면 쪽마다 PDF</div></div>'
  '<div>' + _gs('GS01', 380) + '</div></div>')
S(P['0'], '이 자료로 연구진이 바로 할 수 있는 것', '<p class="lead2">섬유공학 전공자가 아닌 데이터·AI 쪽에서 썼습니다. 메커니즘과 방법론을 깊게 다루고, 섬유 메커니즘의 숫자는 고전 이론과 문헌 방향을 따른 <b>가정</b>입니다.</p><div class="g4">'
  '<div class="card"><i>01</i><b>섬유 → 전기, 좌표축으로</b><p>소재·구조·표면·환경이 전기 출력이 되는 길을 그래프로 직접 움직여 봄</p></div>'
  '<div class="card"><i>02</i><b>데이터 생성 원칙</b><p>10조 지침, 하지 말 것 5가지, 범위·잡음·원단 수 기준</p></div>'
  '<div class="card"><i>03</i><b>데이터 검증</b><p>품질 검사, 분포·상관, 누수, TSTR, 적용 범위, 전향 검증</p></div>'
  '<div class="card"><i>04</i><b>실습과 프롬프트</b><p>Lab 1~8 지침, CSV 예시 15개, 데이터 생성 프롬프트 6종</p></div></div>')
_tocd = ['실측 27개, 전기 특성 0개 — 모의 데이터가 필요한 이유와 한계', '원단 한 줄의 구성, Y는 연속값, 측정은 관측값', '소재·실·구조·물성 — Peirce·Munden·van Wyk·Howell',
  '좌표축으로 보기: 대전 서열, σx/ε₀, 거칠기, 압력, 습도, 제작 인자, 민감도', '10조 지침과 금지 5가지, 잡음·원단 수 기준', '라틴 하이퍼큐브, 필터, 잡음 세 층, 보정 순서',
  '품질 검사, 분포·상관, 누수, TSTR', 'PCA, 가우시안 혼합, 조건부 생성, VAE·GAN, 적용 범위, 모델 붕괴', 'Lab 1~8 명령·출력·CSV', '일정·역할·체크리스트',
  '데이터 생성용 프롬프트 6종, 나쁜 예·좋은 예', 'Genspark 삽화 10장 요청서', '']
S(P['0'], '목차', '<ol class="toc">' + ''.join(f'<li><em>{k}</em><b>{v}</b><span>{d}</span></li>' for (k, v), d in zip(PARTS[1:-1], _tocd)) + '</ol>')

# ================= 1 왜 =================
S(P['1'], '출발점 — 실측 27개, 전기 특성 0개', '<div class="cols c64"><div><div class="small">원단 27개 × 측정 묶음 8개 + 전기 특성 Y — 칸 색 = 채운 비율 (실측 엑셀 집계, S0)</div>' + _cv('covCv', 720, 470) + '</div>'
  + _side('읽는 법', '<div class="kpis v"><div class="kpi"><b>27</b><span>받은 원단</span></div><div class="kpi"><b>19</b><span>27개 모두에 있는 항목</span></div><div class="kpi r"><b>0</b><span>전기 특성 Y</span></div></div>'
  '<p>출처 세 곳(Huvis·연구실·산업)마다 잰 묶음이 다르고, 맨 오른쪽 Y 열은 비어 있습니다. 실측이 모이는 동안 <b>메커니즘으로 만든 모의 데이터</b>로 도구와 절차를 먼저 시험합니다.</p>') + '</div>', 'initCov')
S(P['1'], '1차년도 방법 정의', '<div class="def">실측 직물 데이터의 패턴(결합분포)을 학습하는 생성 모델로 새 직물을 만들고,<br>그 직물의 전기적 특성을 연속값(회귀형 출력)으로 예측한다.</div>'
  '<div class="g4"><div class="card"><i>실측</i><b>X와 Y를 함께</b><p>직물 특성 19항목 + 전기 특성. 전기 특성은 엄격한 정답이 아니라 직물 특성 중 하나</p></div>'
  '<div class="card"><i>학습</i><b>비지도</b><p>생성 모델이 "어떤 직물 특성이 어떤 전기 특성과 함께 나타나는가"를 배움</p></div>'
  '<div class="card"><i>출력</i><b>연속값 + 범위</b><p>새 직물과 전기 특성의 예측값·범위. 지도 회귀는 비교 기준</p></div>'
  '<div class="card"><i>검증</i><b>실제로 만들어 잼</b><p>생성 직물 일부를 만들어 측정 오차 범위 안에서 맞는지 확인</p></div></div>'
  '<p class="note">학습 방식(지도·비지도)과 출력 종류(연속·이산)는 서로 다른 구분입니다. 이 과제는 <b>학습은 비지도, 출력은 연속값</b>입니다.</p>')
S(P['1'], '모의 데이터의 쓰임과 금지', '<div class="cols"><div><h3 class="ok">쓰는 곳</h3><ul class="b"><li>분석 파이프라인 시험 — 입력 양식, 품질 검사, 학습, 평가</li><li>정답을 아는 시험 — 생성 모델이 우리가 넣은 관계를 되찾는가</li><li>실험계획 — 어느 인자 범위에서 Y가 크게 바뀌는지 미리 보고 실측 원단을 고름</li><li>원단 몇 개면 관계가 보이는지 미리 재기 (Lab 8)</li></ul></div>'
  '<div><h3 class="ng">쓰지 않는 곳</h3><ul class="b"><li>연구 결과·논문 근거 — 모의 데이터의 관계는 우리가 넣은 가정</li><li>표시 없이 실측과 섞기 — 모든 행에 <code>is_mock</code></li><li>성능 보고 — 성적은 실측 원단으로만' + _ref('M11') + '</li><li>실측 결측 채우기 — 결측은 결측으로</li></ul></div></div>'
  '<div class="quote">모의 데이터는 거울입니다 — 넣은 가정만 비춥니다.</div>')

# ================= 2 데이터 기초 =================
_ex = _tr.iloc[:4]
S(P['2'], '원단 한 줄 = 직물 특성 X 19개 + 전기 특성 Y', '<p>표의 한 줄이 원단 하나입니다. 열은 실측 엑셀의 공통 19항목과 같은 이름을 씁니다.</p>'
  + _tbl(['fabric_id', '소재', '구조', 'W', 'SFC_F', 'SRA_F', 'BAR_F', 'CW_F', 'Qmax_F', '…', '<span class="y">Voc_V</span>', 'Voc_cv'],
         [[r.fabric_id, MG.MATERIALS[r.material]['ko'], MG.STRUCTURES[r.structure]['ko'], _f(r.W, 0), _f(r.SFC_F, 3), _f(r.SRA_F, 1), _f(r.BAR_F, 2), _f(r.CW_F, 3), _f(r.Qmax_F, 3), '…', f'<b>{_f(r.Voc_V, 1)}</b>', _f(r.Voc_cv, 3)] for r in _ex.itertuples()])
  + '<div class="g3" style="margin-top:18px"><div class="card"><b>설계 인자</b><p>소재, 구조, 실 선밀도, 밀도(커버 팩터·루프 길이·고형률) — 실험실이 정하는 값</p></div>'
  '<div class="card"><b>직물 특성 X (19)</b><p>평량, 마찰, 거칠기 진폭·파장, 굽힘 강성·일, 압축 일·회복, 냉온감 — FTT로 재는 값</p></div>'
  '<div class="card"><b>전기 특성 Y</b><p>개방 전압 Voc, 전하 Q, 평균 전류 — 반복 3회 평균과 변동계수</p></div></div>')
S(P['2'], 'Y는 연속변수 — 범주로 자르면 무엇을 잃나', '<div class="cols c64"><div><div class="ctl">기준 <input type="range" id="binT" min="10" max="110" value="50"> <b id="binV">50</b> V 이상을 "높음"</div>' + _cv('binCv', 720, 400) + '</div>'
  + _side('범주 vs 연속', '<div class="kpis v"><div class="kpi"><b id="binA">–</b><span>"높음" 안의 Voc 범위</span></div><div class="kpi"><b id="binB">–</b><span>"낮음" 안의 Voc 범위</span></div></div>'
  '<p>같은 "높음"이라도 몇 배 차이가 납니다. 연속값과 <b>범위</b>를 함께 내는 회귀형 출력을 씁니다. Voc처럼 양수이고 오른쪽으로 치우친 값은 로그로 다룹니다.</p>') + '</div>', 'initBin')
S(P['2'], '측정값은 정답이 아니다 — 관측값 = 참값 × 오차', '<div class="cols c64"><div><div class="ctl">전기 측정 CV <input type="range" id="repC" min="0.02" max="0.3" step="0.01" value="0.12"> <b id="repCV">0.12</b> · 반복 <input type="range" id="repN" min="1" max="10" value="3"> <b id="repNV">3</b>회</div>' + _cv('repCv', 720, 400) + '</div>'
  + _side('같은 원단을 300번 잰다면', '<div class="fbox s">관측 = 참값 × (원단 간 변동) × (측정 오차)</div><p>참값 60 V인 원단을 n회 재서 평균을 낸 값의 흩어짐입니다. 반복 평균의 흔들림은 CV/√n로 줄어듭니다.</p>'
  '<div class="kpis v"><div class="kpi"><b id="repR">–</b><span>95%가 들어오는 범위</span></div></div><p>모델 오차가 이 범위보다 작아지면 <b>과적합 신호</b>입니다.</p>') + '</div>', 'initRep')
_tc = list(_tmpl.columns)
S(P['2'], '측정 기록 양식 — 52열', '<p>실험실은 이 양식(<a href="../practice/data/00_measurement_template.csv">00_measurement_template.csv</a>)으로 기록합니다. 열 뜻과 단위는 <a href="../practice/data/00_column_dictionary.csv">00_column_dictionary.csv</a>.</p>'
  '<div class="chips">' + ''.join(f'<span class="chip{" y" if c.startswith(("Voc", "Qsc")) else (" p" if c in ("counter_material", "contact_mode", "gap_mm", "area_cm2", "pressure_kPa", "freq_Hz", "temp_C", "rh_pct", "x_instrument") else "")}">{c}</span>' for c in _tc) + '</div>'
  '<div class="lg"><span class="chip">식별·설계·물성</span> <span class="chip p">측정 조건 (고정·기록)</span> <span class="chip y">전기 특성 (반복 3회)</span></div>'
  + _tbl(['fabric_id', 'material', 'structure', 'W', 'SRA_F', 'counter', 'rh_pct', 'Voc_rep1~3', 'Voc_V', 'Voc_cv'], [[r.fabric_id, r.material, r.structure, r.W, r.SRA_F, r.counter_material, r.rh_pct, f'{r.Voc_rep1} · {r.Voc_rep2} · {r.Voc_rep3}', r.Voc_V, r.Voc_cv] for r in _tmpl.itertuples()]))
S(P['2'], '측정 프로토콜 — Y를 "직물의 성질"로 만드는 고정값', '<div class="cols c64"><div class="t2">' + prott.replace('class="tb"', 'class="t"') + '</div><div>' + _gs('GS02', 250)
  + '<p class="note">조건이 흔들리면 모델은 직물이 아니라 측정 조건을 배웁니다. 고정할 수 없는 온습도는 반드시 열로 남깁니다.</p></div></div>')

# ================= 3 섬유 메커니즘 =================
S(P['3'], '생성 사슬 — 섬유에서 전기 특성까지', '<div class="wide">' + chain_svg + '</div>'
  '<div class="g3"><div class="card"><b>앞 칸 → 뒤 칸은 식</b><p>각 칸은 앞 칸의 값으로 계산합니다. 흩뿌린 숫자가 아니라 제작 메커니즘을 따라간 숫자입니다.</p></div>'
  '<div class="card"><b>칸마다 잡음</b><p>식이 다 설명하지 못하는 몫(원단 간 변동)과 측정 오차를 칸마다 정한 크기로 더합니다.</p></div>'
  '<div class="card"><b>소재는 Y로 직접도</b><p>대전 서열과 수분율은 구조를 거치지 않고 전기 특성에 바로 영향을 줍니다.</p></div></div>')
S(P['3'], '① 소재 — 섬유의 대표값', '<div class="t2">' + matt.replace('class="tb"', 'class="t"') + '</div>'
  '<p class="note">교과서 수준의 대표값입니다. 대전 서열 점수는 직물 대전 서열(나일론 > 면 > 폴리에스터 > 폴리프로필렌 > PTFE)' + _ref('G8') + '을 순서 점수로 옮긴 가정값이며, 울은 문헌마다 위치가 달라 불확실성이 큽니다. 실험실 실의 시험 성적서 값으로 바꿔 넣습니다.</p>')
S(P['3'], '② 실 — 지름과 커버 팩터', '<div class="cols c64"><div>'
  '<div class="fbox">실 지름 d = √( 4 · tex·10⁻⁵ / (π · ρ<sub>f</sub> · 0.6) )  [cm]</div><ul class="b"><li>단면적 = 선밀도 ÷ (섬유 밀도 × 충전율 0.6)</li><li>같은 tex라도 가벼운 섬유(PP 0.91)는 굵고, 무거운 섬유(면 1.52)는 가늘다</li></ul>'
  '<div class="fbox">커버 팩터(SI) K = 올/cm × √tex / 10</div><ul class="b"><li>K가 클수록 실이 빽빽 — 경사 K₁ + 위사 K₂</li><li>평직은 K₁+K₂ ≈ 32에서 막힘(jam), 능직·호프색은 36까지</li><li>생성기는 막힘 한계의 98%를 넘으면 버림 — 짤 수 없는 직물</li></ul></div>'
  + _side('예: 나일론 25 tex, K = 26, 경사 비중 0.52', '<p class="mono">d = 0.216 mm<br>EPC = 13.5·10/√25 = 27.0 올/cm<br>PPC = 12.5·10/√25 = 25.0 올/cm<br>막힘 한계 대비 26/36 = 72%</p>') + '</div>')
S(P['3'], '③ 구조 — 제작 방법 5종', _gs('GS03', 175) + '<div class="t2">' + strt.replace('class="tb"', 'class="t"') + '</div>'
  '<p class="note">능직·호프색은 교차가 적어 실을 더 촘촘히 넣을 수 있어(조직 계수)' + _ref('G2') + ' 막힘 한계를 높게 둡니다. 실-실 접촉 표면 계수는 직물 TENG 비교 연구' + _ref('M3', 'M4') + '의 순서를 따른 가정입니다.</p>')
S(P['3'], '③-1 제직 — Peirce의 직물 기하', '<p>Peirce(1937)는 제직물을 실 지름·간격·굴곡·커버·두께·평량이 서로 묶인 하나의 기하 체계로 다뤘습니다' + _ref('G1') + '. 생성기는 이를 단순화해 씁니다.</p>'
  '<div class="fbox">굴곡률 c ≈ 0.9 · 교차 비율 · (d / 맞은편 실 간격)²   (평직 1, 능직·호프색 0.5)</div>'
  '<div class="fbox">평량 W = ( EPC · tex · (1+c₁) + PPC · tex · (1+c₂) ) / 10   [g/m²]</div>'
  '<div class="fbox">두께 t ≈ 2d · (1 + 0.12·(뜬 길이 − 1)),   충전율 φ = W / (t · ρ<sub>f</sub> · 1000)</div>'
  '<ul class="b"><li>실이 위아래로 굽은 만큼(굴곡) 실이 더 들어가 평량이 늘어남</li><li>충전율 φ = 직물 부피 중 섬유가 차지하는 비율 — 압축·냉온감·실접촉의 핵심 중간 변수</li></ul>')
S(P['3'], '③-2 편직 Munden · ③-3 부직포 고형률', '<div class="cols"><div><h3>편직 (싱글 저지)</h3>'
  '<div class="fbox">루프 길이 l = √tex / TF  [mm]   (조임 계수 TF 1.2~1.7)</div><div class="fbox">코스/cm = K<sub>c</sub> / l,   웨일/cm = K<sub>w</sub> / l   (l: cm)</div><div class="fbox">평량 W = 코스 · 웨일 · l · tex / 10</div>'
  '<p class="note">코스·웨일 밀도는 루프 길이에 반비례하고, 상수는 조임과 무관합니다' + _ref('G3') + '. K<sub>c</sub> ≈ 4.8~5.4, K<sub>w</sub> ≈ 3.8~4.3 (건조 이완 대표값).</p></div>'
  '<div><h3>부직포 (니들펀치)</h3><div class="fbox">두께 t = W / (ρ<sub>f</sub> · 고형률 · 1000)  [mm]</div>'
  '<ul class="b"><li>실을 만들지 않고 섬유망을 바늘로 얽음 — 평량과 고형률(0.06~0.20)이 설계 인자</li><li>공극이 많아 압축 일이 크고 냉온감은 작음</li><li>섬유 배향 MD/CD ≈ 1.3 — 방향별 굽힘 차이</li></ul></div></div>')
_ir = items_rows
S(P['3'], '④ 물성 19항목 — 생성 규칙 (1/2)', _tbl(['항목', '메커니즘', '생성 식 (요약)', '근거'], [[f'<b>{a}</b>', b, f'<span class="s">{c}</span>', _ref(*d.split())] for a, b, c, d in _ir[:5]]))
S(P['3'], '④ 물성 19항목 — 생성 규칙 (2/2)', _tbl(['항목', '메커니즘', '생성 식 (요약)', '근거'], [[f'<b>{a}</b>', b, f'<span class="s">{c}</span>', _ref(*d.split())] for a, b, c, d in _ir[5:]])
  + '<p class="note">섬유·직물 마찰은 Amontons 법칙(F/N = 일정)이 맞지 않고 F = a·Nⁿ을 따릅니다' + _ref('G6') + '. 압축은 van Wyk 섬유 집합체 이론' + _ref('G4', 'G5') + '의 방향을 따랐습니다. 단위는 FTT 출력 단위로 보정합니다.</p>')
S(P['3'], '메커니즘 계산기 — 한 원단을 직접 만들어 보기', '<p class="small">소재·구조·인자를 바꾸면 구조 → 물성 → 전기 특성이 같은 식으로 계산됩니다(잡음 없는 참값). 생성기 파이썬 코드와 값이 일치합니다.</p><div class="calcwrap">' + calc + '</div>')

# ================= 4 섬유 특성 → 전기 특성 =================
_dag = _svg(1100, 400, _ARW
  + _box(20, 30, 170, 64, IN, '소재 ①', '대전 서열 · 수분율') + _box(20, 168, 170, 64, IN, '소재 ②', '탄성률 · 섬유 지름 · 밀도') + _box(20, 300, 170, 64, SG, '제작 인자', '구조 · tex · 커버/루프/고형률')
  + _box(250, 230, 170, 64, SG, '직물 기하', '실 지름 · 밀도 · 두께 · φ')
  + _box(480, 110, 170, 60, AM, '표면', 'SRA · SRW · SFC') + _box(480, 220, 170, 60, AM, '역학', 'CW · BAR · CRR') + _box(480, 320, 170, 60, '#b8b2a4', '열', 'Qmax (냉온감)')
  + _box(710, 160, 170, 64, OR, '실접촉 지수', '구조 × g(SRA) × 압력 포화') + _box(710, 30, 170, 64, '#8a6f9e', '환경', 'RH · 압력 · 간격')
  + _box(930, 100, 150, 64, NV, 'σ 표면 전하', 'σ₀·Δ서열·접촉·습도') + _box(930, 250, 150, 64, NV, 'Voc · Q · I', 'σx/ε₀ · σS · 2Qf')
  + _ar(190, 55, 928, 112) + _ar(190, 200, 248, 250) + _ar(190, 332, 248, 280) + _ar(420, 250, 478, 145) + _ar(420, 262, 478, 250) + _ar(420, 274, 478, 345)
  + _ar(650, 140, 708, 182) + _ar(650, 250, 708, 205) + _ar(880, 192, 928, 145) + _ar(880, 62, 928, 112) + _ar(1005, 164, 1005, 248)
  + '<line x1="650" y1="350" x2="930" y2="290" stroke="#c4561a" stroke-width="2" stroke-dasharray="4 6"/>' + _t(800, 352, '간접 상관 (원인 아님)', 13, OR, wt=700))
S(P['4'], '인과 지도 — 무엇이 무엇을 거쳐 전기 출력이 되나', _dag + '<div class="g3"><div class="card"><b>얼마나 주고받나</b><p>소재의 대전 서열 차이 — 상대 전극(PTFE)과 멀수록 전하가 많이 옮겨감</p></div>'
  '<div class="card"><b>얼마나 닿나</b><p>구조·표면 요철·압축성이 실제 접촉 면적을 정함 — 실접촉 지수</p></div><div class="card"><b>얼마나 남나</b><p>습도가 높으면 표면 전하가 새어 나감 — 흡습성 섬유가 더 민감</p></div></div>')
S(P['4'], '접촉-분리형 마찰전기 — 기본 식', '<div class="cols c55"><div>' + _gs('GS04', 230)
  + '<div class="fbox">Voc = σ · x / ε₀      Q = σ · S      평균 전류 = 2 · Q · f</div><ul class="b"><li>σ: 표면 전하 밀도 — <b>직물이 정하는 부분</b></li><li>x 간격, S 면적, f 주파수 — 프로토콜로 고정' + _ref('M2') + '</li></ul></div>'
  '<div><div class="ctl">σ <input type="range" id="tgS" min="0.05" max="1.2" step="0.01" value="0.4"> <b id="tgSV">0.40</b> μC/m²</div>' + _cv('tgCv', 560, 330)
  + '<div class="kpis"><div class="kpi"><b id="tgV">–</b><span>Voc (x = 1 mm)</span></div><div class="kpi"><b id="tgQ">–</b><span>Q (25 cm²)</span></div><div class="kpi"><b id="tgI">–</b><span>평균 전류 (2 Hz)</span></div></div></div></div>', 'initTeng')
S(P['4'], '좌표축 ① 대전 서열 — 누가 전자를 내주나', '<div class="cols c64"><div><div class="ctl">상대 전극 <select id="trRef"></select></div>' + _cv('trCv', 720, 400) + '</div>'
  + _side('읽는 법', '<p>오른쪽(+)일수록 접촉 때 전자를 내주고 양전하를 띱니다. 상대 전극과의 <b>거리 Δ</b>가 클수록 σ가 큽니다' + _ref('G8', 'M1') + '.</p><p>상대 전극을 나일론으로 바꾸면 Δ의 부호가 뒤집히는 소재가 생깁니다 — 그래서 상대 전극은 프로토콜로 <b>고정</b>합니다.</p><p class="small">점수는 문헌 순서를 옮긴 가정값. 울은 문헌마다 위치가 다름.</p>') + '</div>', 'initTribo')
S(P['4'], '좌표축 ② 거칠기 — 역U자로 둔 이유', '<div class="cols c55"><div><ul class="b">'
  '<li>직물 TENG: 능직 2/2·호프색 2/2가 접촉 표면적과 거칠기가 커서 평직보다 출력이 높음' + _ref('M3') + '</li><li>평평한 탄성 표면: 거칠기가 커질수록 실접촉 면적과 출력이 감소' + _ref('G10') + '</li><li>둘을 함께 담으려면 "적당한 요철에서 최대"</li></ul>'
  '<div class="fbox">g(SRA) = exp( −(ln(SRA / SRA<sub>opt</sub>))² / (2·0.8²) )</div><div class="ctl">SRA<sub>opt</sub> <input type="range" id="ruOpt" min="15" max="90" step="1" value="45"> <b id="ruV">45</b> μm</div>' + _gs('GS05', 150) + '</div>'
  '<div>' + _cv('ruCv', 560, 400) + '<p class="small">점은 구조별 거칠기 중앙값(모의). 실측 원단으로 꼭짓점을 정합니다.</p></div></div>', 'initRough')
S(P['4'], '좌표축 ③ 누르는 힘 — 접촉은 포화한다', '<div class="cols c64"><div><div class="ctl">소재 <select id="prM"></select></div>' + _cv('prCv', 720, 400) + '</div>'
  + _side('실접촉 지수 ci(P)', '<div class="fbox s">ci = surf · g(SRA) · (1 − e<sup>−P/P<sub>s</sub></sup>)<br>P<sub>s</sub> = 6 / (1 + 4·CW)</div><p>부드러운(압축 일 CW가 큰) 직물은 작은 힘에도 빨리 붙습니다. 힘을 키워도 접촉이 무한히 늘지 않아 출력이 포화합니다' + _ref('G11') + '.</p><p>점선 = 프로토콜 5 kPa. 포화 구간에서 재야 힘의 작은 흔들림이 Y를 흔들지 않습니다.</p>') + '</div>', 'initPress')
S(P['4'], '좌표축 ④ 습도 — 흡습성 섬유가 더 민감', '<div class="cols c64"><div><div class="ctl">구조 <select id="huS"></select></div>' + _cv('huCv', 720, 400) + '</div>'
  + _side('습도 계수', '<div class="fbox s">hum = 1 − β·(RH − 40)/100<br>β = 0.25 · (1 + 수분율/10)</div><p>습할수록 표면 물 분자로 전하가 새어 나갑니다' + _ref('G9', 'M5') + '. 수분율이 큰 울·면의 기울기가 가파릅니다. 띠 = 프로토콜 RH 65 ± 2%.</p>' + _gs('GS06', 130)) + '</div>', 'initHum')
S(P['4'], '좌표축 ⑤ 제작 인자 — 커버 팩터를 올리면', '<div class="cols c64"><div><div class="ctl">소재 <select id="cfM"></select> <span class="small">실 25 tex · 경사 비중 0.52 · RH 65%</span></div>' + _cv('cfCv', 720, 440) + '</div>'
  + _side('같은 x축, 두 단계', '<p><b>위</b>: 커버 팩터가 오르면 실이 빽빽해져 표면 요철(SRA)이 줄어듭니다.</p><p><b>아래</b>: SRA가 역U자 꼭짓점에서 멀어지는 쪽이면 Voc도 줄어듭니다.</p><p>능직·호프색은 뜬 길이가 길어 요철이 크고 막힘 한계도 높습니다(선 끝 = 막힘 98%). 제작 인자 → 물성 → 전기 특성이 한 축에서 이어집니다.</p>') + '</div>', 'initCover')
S(P['4'], '좌표축 ⑥ 두 인자 지도 — 거칠기 × 대전 서열 차', '<div class="cols c64"><div>' + _cv('mpCv', 720, 460) + '</div>'
  + _side('등고선 = Voc (V)', '<p>가로 거칠기 SRA, 세로 PTFE와의 대전 서열 차 Δ. 색이 진할수록 Voc가 큽니다(구조·압력·습도 계수는 1로 둔 상한).</p><p>점 = 모의 학습 원단(소재마다 같은 Δ라 가로 줄로 섬). 같은 소재라도 거칠기에 따라 등고선을 여러 칸 건넙니다 — <b>소재가 규모를, 구조·표면이 그 안의 위치를</b> 정합니다.</p>') + '</div>', 'initMap')
S(P['4'], '좌표축 ⑦ 민감도 — 무엇을 바꾸면 Voc가 가장 움직이나', '<div class="cols c64"><div><div class="ctl">소재 <select id="toM"></select> 구조 <select id="toS"></select> 변화 ±15%</div>' + _cv('toCv', 720, 400) + '</div>'
  + _side('토네이도 그림', '<p>기준 원단에서 인자 하나만 ±15% 바꿨을 때 Voc 변화입니다(나머지 고정, 메커니즘 계산기와 같은 식).</p><p>막대가 긴 인자는 <b>실험계획에서 넓게 바꿔 볼 인자</b>, 짧은 인자는 고정해도 되는 인자입니다. 소재·구조를 바꾸면 순위가 달라집니다.</p>') + '</div>', 'initTor')
S(P['4'], '좌표축 ⑧ 분해 — 한 원단의 Voc는 이렇게 곱해진다', '<div class="ctl">소재 <select id="wfM"></select> 구조 <select id="wfS"></select></div><div id="wfOut"></div>'
  '<p class="note">σ = σ₀ × Δ서열 × 접촉 표면 × g(SRA) × 압력 포화 × 습도 → Voc = σ · x / ε₀. 곱셈 구조라 하나가 0에 가까우면 나머지가 커도 출력이 작습니다(예: 폴리프로필렌은 Δ가 작음).</p>', 'initWf')
S(P['4'], '데이터로 보기 — 직물 특성 하나와 Voc', '<div class="cols c64"><div><div class="ctl">x축 <select id="scX"></select> <span class="small">점 = 모의 학습 원단 384개, 로그 눈금</span></div>' + _cv('scCv', 720, 420) + '</div>'
  + _side('순위 상관 ρ', '<div class="kpis v"><div class="kpi"><b id="scR">–</b><span>전체 ρ</span></div><div class="kpi"><b id="scR2">–</b><span>소재 안 평균 ρ</span></div></div><p>한 항목만으로는 관계가 흐립니다 — Voc는 여러 인자가 <b>곱해진</b> 값이기 때문입니다. 전체 ρ와 소재 안 ρ가 크게 다르면 소재가 끼어든 간접 관계입니다.</p>') + '</div>', 'initScat')
S(P['4'], '정리 — 섬유 특성이 전기 특성이 되는 세 갈래', '<div class="g3"><div class="card big"><i>얼마나 주고받나</i><b>소재</b><p>대전 서열 차 Δ가 출력의 <b>규모</b>를 정함. 상대 전극 고정이 전제</p><p class="small">좌표축 ①⑥</p></div>'
  '<div class="card big"><i>얼마나 닿나</i><b>구조 · 표면 · 압축</b><p>구조의 접촉 표면, 거칠기 역U자, 압력 포화가 실접촉을 정함 — 제작 인자가 여기로 들어옴</p><p class="small">좌표축 ②③⑤⑦</p></div>'
  '<div class="card big"><i>얼마나 남나</i><b>환경</b><p>습도가 전하를 흘려보냄. 흡습성 섬유일수록 민감 — 측정 조건 기록이 필수</p><p class="small">좌표축 ④</p></div></div>'
  '<div class="quote">데이터 생성은 이 세 갈래를 곱셈 순서대로 따라가는 일입니다. 다음 장이 그 원칙입니다.</div>')

# ================= 5 데이터 생성 원칙 =================
S(P['5'], '데이터 생성 원칙 10조', _tbl(['', '원칙', '어떻게', '어기면'], [[f'<b class="num">{i + 1:02d}</b>', f'<b>{a}</b>', b, f'<span class="s">{c}</span>'] for i, (a, b, c) in enumerate(SC.PRINCIPLES)], 't s'))
S(P['5'], '하지 말 것 다섯 가지', '<div class="g5">' + ''.join(f'<div class="card ng"><i>✕</i><b>{a}</b><p>{b}</p></div>' for a, b in SC.DONTS) + '</div>'
  '<p class="note">다섯 가지 모두 "숫자는 그럴듯하지만 관계가 틀린" 데이터를 만듭니다. 다음 장에서 첫 번째(열마다 독립 난수)를 직접 봅니다.</p>')
S(P['5'], '원칙 01 시연 — 열마다 따로 뽑으면 관계가 사라진다', '<div class="ctl">짝 <select id="shP"><option value="1">마찰계수 SFC_F × Voc</option><option value="4">굽힘 강성 BAR_F × Voc</option><option value="7">냉온감 Qmax_F × Voc</option><option value="0">평량 W × Voc</option></select> <span class="small">왼쪽: 메커니즘 순서로 만든 모의 데이터 · 오른쪽: 같은 값을 열마다 섞음(열별 분포는 그대로)</span></div>'
  '<div class="cols">' + _cv('shA', 560, 290) + _cv('shB', 560, 290) + '</div><div class="cols">' + _cv('shM1', 560, 180) + _cv('shM2', 560, 180) + '</div>', 'initShuf')
S(P['5'], '원칙 04 — 잡음 크기가 예측의 천장을 정한다', '<div class="cols c64"><div><div class="ctl">전기 측정 CV <input type="range" id="nzC" min="0.02" max="0.4" step="0.01" value="0.12"> <b id="nzCV">0.12</b> · 반복 <input type="range" id="nzN" min="1" max="6" value="3"> <b id="nzNV">3</b>회</div>' + _cv('nzCv', 720, 420) + '</div>'
  + _side('R² 천장', '<div class="kpis v"><div class="kpi"><b id="nzR">–</b><span>완벽한 모델도 넘을 수 없는 R²</span></div></div><div class="fbox s">천장 = Var(참값) / (Var(참값) + (CV/√n)²)  (로그 척도)</div>'
  '<p>잡음을 너무 작게 넣으면 모델이 비현실적으로 좋아 보이고, 실측이 오면 실망합니다. 잡음 크기는 <b>실측 반복 CV</b>에서 가져옵니다. 반복을 늘리면 천장이 올라갑니다.</p>') + '</div>', 'initNoise')
S(P['5'], '원칙 06 — 원단이 몇 개면 관계가 보이나 (Lab 8)', '<div class="cols c64"><div>' + _cv('lcCv', 720, 420) + '</div>'
  + _side('학습 곡선', '<p>모의 학습 자료에서 원단 수를 15개부터 384개까지 늘리며 시험 R²를 쟀습니다(무작위 5회 평균 ± 표준편차).</p>'
  '<ul class="b"><li>~60개: 들쭉날쭉 — 뽑힌 원단에 따라 결과가 크게 다름</li><li>100개 안팎: R² 0.8대로 안정</li><li>그 이상: 천천히 오름</li></ul><p><b>S2 실측 목표 50개 이상</b>은 하한입니다. 실측은 잡음이 더 클 수 있어 여유를 둡니다.</p>') + '</div>', 'initLC')
_rng19 = _df[_X19].quantile([0.01, 0.5, 0.99]).T
_units = {'W': 'g/m²', 'SFC': 'Gf/Gf', 'SRA': 'μm', 'SRW': 'mm', 'BAR': 'Gf·mm/rad', 'BW': 'Gf·mm·rad', 'CW': 'Gf·mm', 'CRR': '% (보정 필요)', 'Qmax': 'W/cm²'}
_rr = [[c, _units[c.split('_')[0]], f'{r[0.01]:.3g}', f'{r[0.5]:.3g}', f'{r[0.99]:.3g}'] for c, r in _rng19.iterrows()]
S(P['5'], '원칙 03·07·08 — 범위표와 기록 규칙', '<div class="cols"><div class="t2">' + _tbl(['항목', '단위', '1%', '중앙', '99%'], _rr[:10], 't s') + '</div><div class="t2">' + _tbl(['항목', '단위', '1%', '중앙', '99%'], _rr[10:], 't s')
  + '<pre class="code s">{ "generator": "generate_mock_fabric.py v1.0",\n  "seed": 20261118, "is_mock": true,\n  "assumptions": [{"name": "SRA_OPT", "value": 45,\n     "basis": "M3·G10 방향 절충", "uncertainty": "높음"}] }</pre></div></div>'
  '<p class="note">모의 데이터 500개의 1·50·99% 값. 실측 27개가 오면 같은 표를 만들어 나란히 두고, 범위가 어긋난 항목부터 분위수 맞춤으로 보정합니다. 가정마다 근거와 불확실성을 JSON에 남깁니다.</p>')

# ================= 6 생성 절차 =================
S(P['6'], '생성 절차 8단계', _gs('GS07', 190) + '<ol class="steps two">'
  '<li><b>설계 공간</b> — 소재·구조 목록과 연속 인자 범위. 실험실이 만들 수 있는 범위로</li><li><b>표본 추출</b> — 소재 × 구조 칸마다 라틴 하이퍼큐브, 칸마다 같은 수(기본 20)</li>'
  '<li><b>구조 계산</b> — 실 지름·밀도·평량·두께·충전율</li><li><b>제작 가능성 필터</b> — 막힘 한계·조임 계수·충전율 범위 밖은 버림</li>'
  '<li><b>물성 19항목</b> — 메커니즘 식 + 원단 간 변동 + 측정 오차</li><li><b>전기 특성 Y</b> — 마찰전기 식 + 습도 + 전기 측정 오차, 반복 3회</li>'
  '<li><b>품질 검사</b> — 범위·순서·흔들림·분포 비교</li><li><b>기록</b> — 시드, 생성기 버전, 가정 표(변수 사전 JSON), 모든 행 is_mock</li></ol>')
S(P['6'], '라틴 하이퍼큐브 — 설계 공간을 고르게 채우기', '<div class="cols"><div><ul class="b">'
  '<li>무작위 추출은 운에 따라 한쪽에 몰리고 빈 곳이 생김</li><li>라틴 하이퍼큐브는 각 인자 범위를 n칸으로 나눠 <b>칸마다 정확히 하나</b>씩 뽑음' + _ref('G12') + '</li>'
  '<li>적은 원단 수로 인자 범위 전체를 덮음 — 실측 실험계획에도 그대로 씀</li><li>소재 × 구조는 범주라 칸(층)으로 나누고, 칸 안에서 연속 인자를 뽑음</li></ul>'
  '<div class="ctl">원단 수 <input type="range" id="lhN" min="5" max="40" value="12"> <b id="lhV">12</b> <button class="bt" id="lhR">다시 뽑기</button></div></div>'
  '<div>' + _cv('lhCv', 580, 320) + '<p class="small">가로: 실 선밀도, 세로: 커버 팩터. 왼쪽 무작위, 오른쪽 라틴 하이퍼큐브(각 행·열에 점 하나).</p></div></div>', 'initLHS')
S(P['6'], '제작 가능성 필터와 잡음 세 층', '<div class="cols"><div><h3>제작 가능성 필터</h3>' + _tbl(['구조', '버리는 조건'], [['제직', '커버 팩터 합 > 막힘 한계 × 0.98'], ['편직', '조임 계수 TF < 1.15 또는 > 1.75'], ['부직', '충전율 φ < 0.03 또는 > 0.30']])
  + '<p class="note">실험실이 실제로 만들 수 없는 직물이 데이터에 들어가지 않게 합니다.</p></div><div><h3>잡음 세 층</h3>'
  + _tbl(['층', '크기', '뜻'], [['원단 간 변동', 'CV 6%', '같은 설계라도 실·가공 차이'], ['물성 측정', 'CV 4% × 3회 평균', 'FTT 반복의 흔들림'], ['전기 측정', 'CV 12% × 3회 평균', '표면 상태·잔류 전하에 민감'], ['측정 환경', 'RH 65 ± 2%', '습도 계수로 Y에 들어감']])
  + '<p class="note">층을 나눠 두면 "모델 오차가 측정 오차 수준까지 내려왔는가"를 판단할 수 있습니다.</p></div></div>')
S(P['6'], '생성기 실행과 출력 열', '<div class="cols"><div><pre class="code">cd analysis/mock_data\npython generate_mock_fabric.py 20 20261118 .\n# 칸당 20개 × 소재 5 × 구조 5\n# → mock_fabric_data.csv (500행)\n# → mock_fabric_dictionary.json</pre>'
  '<ul class="b"><li>같은 시드 → 같은 데이터 (재현성)</li><li>소재·구조 대표값, 프로토콜, 보정 계수는 파일 맨 위 표에서 바꿈</li><li>버전·시드는 JSON에 기록</li></ul></div><div>'
  + _tbl(['열 묶음', '열'], [['식별', 'fabric_id, material, structure, kind, is_mock'], ['설계 인자', 'tex, cover, warp_share, tf, gsm_design, solidity'], ['구조량', 'yarn_d_mm, thick_mm, phi, epc, ppc, cpc, wpc, loop_mm'], ['환경', 'rh'], ['물성 19', 'W, SFC_F … Qmax_B'], ['전기 특성', 'Voc_V, Voc_cv, Qsc_nC, Iavg_nA, sigma_uCm2'], ['진단', 'contact_index, hum_factor']]) + '</div></div>')
S(P['6'], '결과 둘러보기 — 항목별 분포 대시보드', '<div class="ctl">항목 <select id="dsItem"></select> 묶음 <select id="dsBy"><option value="1">구조</option><option value="0">소재</option></select> <span class="small">점 하나 = 학습 자료의 원단 하나 (모의 384개), 막대 = 사분위 범위, 굵은 선 = 중앙값</span></div>'
  + _cv('dsCv', 1150, 470), 'initDist')
S(P['6'], '결과 미리보기 — 소재 × 구조별 Voc', '<div class="t2">' + heat.replace('class="tb mk-heat"', 'class="t heat"') + '</div><ul class="b">'
  '<li>같은 소재에서 능직·호프색 > 평직 — 직물 TENG 실험의 방향' + _ref('M3', 'M4') + '</li><li>소재는 나일론 > 울 > 면 > 폴리에스터 > 폴리프로필렌 — 대 PTFE 대전 서열의 방향' + _ref('G8') + '</li>'
  '<li>크기(수 V~100 V)는 σ₀ 보정 전의 자리표 — 순서와 비율만 의미가 있음</li></ul>')
S(P['6'], '실측이 들어오면 — 생성기 보정 순서', '<ol class="steps">'
  '<li><b>단위·규모 맞추기</b> — 19항목 각각 실측 27개의 분위수에 맞춰 모의 분포를 옮김(분위수 맞춤). CRR처럼 단위가 다른 항목 먼저</li>'
  '<li><b>σ₀ 보정</b> — 전기 특성을 처음 잰 원단 10개 안팎의 Voc 중앙값에 규모를 맞춤</li><li><b>SRA<sub>opt</sub> 보정</b> — 거칠기가 다른 원단들의 Voc로 역U자 꼭짓점 추정</li>'
  '<li><b>습도 기울기</b> — 같은 원단을 RH 40/65/80%에서 재어 β 추정</li><li><b>대전 서열 점수</b> — 소재별 평직 원단으로 순서·간격 확인 (특히 울)</li></ol>'
  '<p class="note">보정한 생성기는 버리지 않습니다. 생성 모델과 비교하는 <b>물리 기반 기준선</b>이 됩니다. 보정 계획은 부록 A의 프롬프트 P5로 함께 세울 수 있습니다.</p>')

# ================= 7 검증 =================
S(P['7'], '검증의 세 질문', '<div class="cols c55"><div class="g1"><div class="card"><i>①</i><b>값이 말이 되나</b><p>결측·음수·튀는 값·범위·중복·반복 흔들림 — Lab 1</p></div>'
  '<div class="card"><i>②</i><b>관계가 살아 있나</b><p>구조·소재 순서, 분포·상관 비교, 간접 상관 — Lab 2, 5</p></div><div class="card"><i>③</i><b>쓸 수 있나</b><p>누수 없는 분할, TSTR, 적용 범위, 전향 검증 — Lab 3, 5, 6</p></div></div>'
  '<div>' + _gs('GS09', 200) + '<div class="ctl">누적분포 비교 <select id="ksI"><option value="0">평량 W</option><option value="1">압축 일 CW_F</option><option value="2">거칠기 SRA_F</option><option value="3">냉온감 Qmax_F</option><option value="4">Voc</option></select> KS = <b id="ksV">–</b></div>' + _cv('ksCv', 560, 220) + '</div></div>', 'initKS')
_qcs = _qc.groupby(['check', 'result']).size().unstack(fill_value=0)
S(P['7'], 'Lab 1 품질 검사 — 무엇을 보나', '<div class="cols"><div>' + _tbl(['검사', '기준'], [['필수 열', '19항목 + Voc_V 모두'], ['결측 · 양수', '결측 0, 0 이하 0 (로그 변환 전제)'], ['튀는 값', '로그 z 점수 |z| > 4 인 원단 0개'], ['범위', '평량 30~400 g/m² 등 실제 직물 범위'], ['반복 흔들림', 'Voc CV 중앙값 ≤ 0.15, 초과 원단은 재측정'], ['중복', 'fabric_id 중복 0']])
  + '</div><div>' + _tbl(['검사', '통과', '경고'], [[i, int(r.get('통과', 0)), int(r.get('경고', 0))] for i, r in _qcs.iterrows()])
  + '<p class="note">학습 자료(모의 384개): 통과 66 · 경고 1 — 압축 일 CW_B에서 |z| &gt; 4 원단 2개. 반복 흔들림은 CV 중앙값 0.10으로 통과했지만, CV 0.15를 넘는 원단 78개가 재측정 목록 <code>lab1_remeasure.csv</code>로 나옵니다.</p></div></div>')
S(P['7'], '반복 측정 흔들림 — 재측정 기준 정하기', '<div class="cols c64"><div>' + _cv('cvCv', 720, 400) + '</div>'
  + _side('재측정 기준', '<div class="ctl">기준 CV <input type="range" id="cvT" min="0.05" max="0.3" step="0.01" value="0.15"> <b id="cvV">0.15</b></div>'
  '<div class="kpis v"><div class="kpi r"><b id="cvN">–</b><span>재측정 원단 수</span></div><div class="kpi"><b id="cvM">–</b><span>CV 중앙값</span></div></div>'
  '<p>3회 반복의 CV는 그 자체도 흔들립니다 — 기준을 너무 낮추면 재측정이 폭증합니다. 실측 첫 20개로 기준을 다시 정합니다.</p>') + '</div>', 'initCV')
S(P['7'], '분포 비교 — 열마다 KS 거리', '<div class="cols"><div>' + _tbl(['항목', 'KS 거리', 'p', '판정'], [[r['item'], _f(r.KS, 3), _f(r.p, 2), r['판정']] for _, r in _ks.iterrows()])
  + '</div><div><ul class="b"><li>KS 거리 = 두 누적분포의 최대 차이 (0이면 같음)</li><li>&lt; 0.1 닮음, 0.1~0.2 주의, &gt; 0.2 다름 (실습 기준)</li><li>위 표: Lab 4 생성 직물 1000개 vs 학습 자료 — 모두 닮음</li>'
  '<li>실측이 오면 같은 표를 <b>모의 vs 실측</b>으로 만들어 생성기 보정 대상을 고름</li><li>한 열씩만 보면 관계를 놓침 → 상관 비교(최대 차이 0.06, 평균 0.02)</li></ul></div></div>')
S(P['7'], '간접 상관 함정 — 냉온감과 Voc', '<div class="cols c64"><div><div class="ctl"><button class="bt on" data-cf="0">원래 값</button><button class="bt" data-cf="1">소재 효과를 뺀 값</button></div>' + _cv('cfdCv', 720, 400) + '</div>'
  + _side('상관 ≠ 원인', '<div class="kpis v"><div class="kpi"><b id="cfR">–</b><span>순위 상관 ρ</span></div></div><p>모의 데이터에서 냉온감 Qmax와 Voc가 같이 움직이는 것처럼 보입니다. 그러나 둘 다 <b>소재</b>(열전달·수분율과 대전 서열)에 기대어 생긴 관계입니다 — 소재마다 중앙값을 빼면 상관이 거의 사라집니다.</p><p>Qmax를 바꿔도 출력은 바뀌지 않습니다. 원인 해석은 한 요인만 다른 원단 짝(설계 실험)으로.</p>') + '</div>', 'initConf')
_split = _svg(1100, 250, _t(250, 32, '✕ 반복 측정 단위로 나누기', 17, OR, wt=700) + _t(820, 32, '✓ 원단 단위로 나누기', 17, SG, wt=700)
  + ''.join(f'<rect x="{40 + i * 84}" y="54" width="76" height="40" rx="8" fill="{[IN, AM, SG, IN, AM][i]}" opacity=".85"/>' + _t(78 + i * 84, 80, f'원단 {i + 1}', 13, '#fff', wt=700) for i in range(5))
  + ''.join(f'<rect x="{44 + (k % 5) * 84 + (k // 5) * 24}" y="120" width="20" height="20" rx="4" fill="{[IN, AM, SG, IN, AM][k % 5]}" stroke="{OR if (k * 7) % 3 == 0 else "#fbf6ee"}" stroke-width="3"/>' for k in range(15))
  + _t(250, 180, '같은 원단의 반복이 학습·시험에 갈림 (주황 테두리 = 시험)', 13) + _t(250, 204, '→ 시험 성적이 부풀려짐', 13, OR, wt=700)
  + ''.join(f'<rect x="{620 + i * 84}" y="54" width="76" height="40" rx="8" fill="{[IN, AM, SG, IN, AM][i]}" opacity=".85" stroke="{OR if i == 4 else "#fbf6ee"}" stroke-width="3"/>' + _t(658 + i * 84, 80, f'원단 {i + 1}', 13, '#fff', wt=700) for i in range(5))
  + ''.join(f'<rect x="{624 + (k % 5) * 84 + (k // 5) * 24}" y="120" width="20" height="20" rx="4" fill="{[IN, AM, SG, IN, AM][k % 5]}" stroke="{OR if k % 5 == 4 else "#fbf6ee"}" stroke-width="3"/>' for k in range(15))
  + _t(820, 180, '원단 5의 반복은 모두 시험으로', 13) + _t(820, 204, '→ 본 적 없는 원단에 대한 성적', 13, SG, wt=700))
S(P['7'], '누수와 지름길 — 성적이 너무 좋을 때', _split + '<div class="g4"><div class="card"><b>변환 누수</b><p>평균·표준편차를 전체로 계산 → 기준은 학습 자료로만</p></div><div class="card"><b>원단 누수</b><p>같은 원단의 반복이 학습·시험에 갈림 → 원단 단위로</p></div>'
  '<div class="card"><b>조합 누수</b><p>새 조합 예측을 보려면 그 칸 전체를 빼 둠 (울 × 호프색)</p></div><div class="card"><b>지름길</b><p>출처·장비 열로 Y를 맞힘 → 출처를 섞어 나누고 입력에서 뺌</p></div></div>')
S(P['7'], 'TSTR — 생성 데이터가 패턴을 담았는가', '<div class="cols"><div><ul class="b">'
  '<li><b>TRTR</b>: 실측으로 학습 → 실측으로 시험 (기준)</li><li><b>TSTR</b>: 생성으로 학습 → 실측으로 시험' + _ref('M11') + '</li>'
  '<li>TSTR이 TRTR에 가까우면 생성 데이터가 패턴을 잘 담은 것</li><li>실측+생성이 TRTR보다 나아지지 않으면 생성은 <b>새 정보를 주지 않은 것</b></li></ul></div><div class="bars">'
  + ''.join(f'<div class="bar"><span>{r.setting}</span><i style="width:{max(r.test_R2, 0) * 100:.0f}%"></i><b>R² {r.test_R2:.3f} · RMSE {r.test_RMSE:.1f} V</b></div>' for r in _tstr.itertuples())
  + '<p class="note">생성 1000개로 학습해도 실측 384개 학습을 넘지 못합니다. 생성은 실측을 대신하지 못하고, 패턴을 확인·탐색하는 데 씁니다.</p></div></div>')

# ================= 8 방법론 =================
_sup = _svg(1100, 290, _ARW + _t(270, 34, '지도학습 — X로 Y를 맞힘', 17, NV, wt=700) + _t(820, 34, '비지도 생성 — (X, Y)를 함께 배움', 17, OR, wt=700)
  + _box(60, 110, 150, 70, IN, 'X', '직물 특성 19') + _ar(215, 145, 325, 145) + _box(330, 110, 150, 70, OR, 'Y', '정답 라벨로 고정') + _t(270, 230, '오차 = Y − ŷ 를 줄임 → 이 과제에서는 비교 기준', 14)
  + '<line x1="620" y1="250" x2="1060" y2="250" stroke="#7a8394"/><line x1="620" y1="250" x2="620" y2="60" stroke="#7a8394"/>'
  + _ell([(720, 200, 80, 30, -20, IN), (860, 150, 95, 30, -30, SG), (990, 100, 60, 24, -15, AM)])
  + _pts(_np.random.default_rng(5), [(720, 200), (860, 150), (990, 100)], [(40, 13), (48, 14), (28, 10)], 3, '#33415c', .5)
  + _t(840, 278, 'X (직물 특성)', 13) + _t(604, 150, 'Y', 15, wt=700))
S(P['8'], '지도 · 비지도 — 학습 방식과 출력은 다른 구분', _sup + _tbl(['', '지도학습', '비지도학습'], [['출력이 연속', '회귀', '연속값을 내는 생성 모델'], ['출력이 이산', '분류', '군집'], ['이 과제', '<b>비교 기준</b> (릿지·RF·GP)', '<b>주 방법</b> (결합분포 생성 모델) — 출력은 연속값']]))
S(P['8'], 'PCA — 19개 변수를 섞은 종합 점수 (행렬과 내적)', '<div class="fbox">PC = Z · W     (원단 n × 19) · (19 × 2) = (n × 2)       PC1ᵢ = zᵢ · w₁ = Σₖ zᵢₖ w₁ₖ</div>'
  '<ul class="b"><li>Z: 로그 변환 후 표준화한 19항목 (평균 0, 표준편차 1)</li><li>W의 열: 원단이 가장 넓게 퍼지는 방향, 길이 1이고 서로 직교(내적 0)</li>'
  '<li>원단 하나의 PC1 점수 = 그 원단의 줄과 W 첫 열의 내적 — 경기종합지수처럼 여러 지표의 가중합</li>'
  f'<li>모의 학습 자료: PC1 {SD["ev"][0]:.0%}, PC2 {SD["ev"][1]:.0%} (실측 27개는 39%·29%)</li><li>PCA는 보는 도구 — 생성 모델 학습은 19개(또는 핵심 8개) 전체로</li></ul>')
S(P['8'], 'PCA 탐색기 — 점수와 가중치', '<div class="ctl">색 <select id="pcBy"><option value="1">구조</option><option value="0">소재</option></select> 가중치 <select id="pcW"><option value="0">PC1</option><option value="1">PC2</option></select> <span class="small">점에 올리면 원단 정보</span></div>'
  '<div class="cols">' + _cv('pcCv', 600, 440) + _cv('pcL', 520, 440) + '</div>', 'initPCA')
_r1 = _np.random.default_rng(1).normal([[200, 140]] * 25 + [[340, 140]] * 25, 38)
_mix = lambda x: min(1, max(0, (x - 220) / 100))
_clu = _svg(1100, 250, _t(270, 30, 'k-평균 — 딱 잘라 나눔', 16, NV, wt=700) + _t(820, 30, '가우시안 혼합 — 소속 확률', 16, OR, wt=700)
  + ''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="{IN if x < 270 else AM}"/>' for x, y in _r1)
  + '<line x1="270" y1="50" x2="270" y2="230" stroke="#7a8394" stroke-dasharray="4 4"/>'
  + ''.join(f'<circle cx="{x + 550:.0f}" cy="{y:.0f}" r="5" fill="rgb({int(91 + 151 * _mix(x))},{int(99 + 95 * _mix(x))},{int(168 - 46 * _mix(x))})"/>' for x, y in _r1)
  + '<ellipse cx="750" cy="140" rx="70" ry="55" fill="none" stroke="#5b63a8" stroke-width="2"/><ellipse cx="890" cy="140" rx="70" ry="55" fill="none" stroke="#d9772b" stroke-width="2"/>')
S(P['8'], '군집 — k-평균과 가우시안 혼합', _clu + '<ul class="b"><li><b>k-평균</b>: 점마다 가장 가까운 중심 하나에 배정, 무리 모양은 둥근 공</li><li><b>가우시안 혼합(GMM)</b>: 무리마다 평균과 공분산(타원), 점마다 소속 확률 — 가운데 점은 두 색이 섞임</li>'
  '<li>GMM은 자료의 모양을 확률분포로 배우므로 <b>새 점을 뽑을 수 있음</b> → 생성 모델. 무리 수는 BIC로 고름</li></ul>')
S(P['8'], '결합분포와 조건부 생성 — 핵심 식', '<div class="cols c64"><div><div class="fbox">p(x, y) = Σₖ πₖ · N( [x, y] ; μₖ, Σₖ )      ← x와 y를 함께</div>'
  '<div class="fbox">p(y | x) = Σₖ wₖ(x) · N( y ; μ<sub>y|x,k</sub> , σ²<sub>y|x,k</sub> )</div>'
  '<div class="fbox">μ<sub>y|x,k</sub> = μ<sub>y,k</sub> + Σ<sub>yx,k</sub> Σ<sub>xx,k</sub>⁻¹ (x − μ<sub>x,k</sub>)<br>σ²<sub>y|x,k</sub> = Σ<sub>yy,k</sub> − Σ<sub>yx,k</sub> Σ<sub>xx,k</sub>⁻¹ Σ<sub>xy,k</sub></div>'
  '<ul class="b"><li>학습: x와 y를 구분하지 않고 패턴 p(x, y)를 배움 — 비지도</li><li>새 직물: p(x, y)에서 뽑음 → x와 y가 함께 나옴</li>'
  '<li>예측: 새 x를 정하면 p(y | x)의 평균(연속값)과 표준편차(범위)</li><li>역방향: 목표 y*를 정하면 p(x | y*) → 그 출력을 낼 직물 후보 (Lab 7)</li></ul></div><div>' + _gs('GS08', 300) + '</div></div>')
S(P['8'], '생성 모델 시연 — 무리 수를 바꿔 보기', '<div class="ctl">무리 수 K <input type="range" id="emK" min="1" max="6" value="3"> <b id="emV">3</b> <button class="bt" id="emS">새 직물 200개 뽑기</button> <span class="small">가로: PC1 점수, 세로: log Voc (표준화). EM 알고리즘을 브라우저에서 바로 돌립니다.</span></div>'
  '<div class="cols c64">' + _cv('emCv', 700, 440) + '<div><div class="kpis"><div class="kpi"><b id="emLL">–</b><span>로그 가능도</span></div><div class="kpi"><b id="emB">–</b><span>BIC (작을수록 좋음)</span></div></div>'
  '<ul class="b"><li>타원 = 무리마다 배운 패턴 (2σ)</li><li>보라 점 = 배운 패턴에서 새로 뽑은 직물</li><li>K가 너무 작으면 패턴을 뭉갬, 너무 크면 원단 하나하나를 외움 → BIC로 균형</li></ul></div></div>', 'initEM')
_dl = _svg(1100, 220, _ARW + _t(270, 28, 'VAE — 압축했다 복원', 16, NV, wt=700) + _t(820, 28, 'GAN — 만들기 vs 가려내기', 16, OR, wt=700)
  + _box(30, 80, 110, 70, IN, '직물 x') + '<polygon points="160,70 250,95 250,135 160,160" fill="#a9bf8e"/>' + _t(205, 120, '인코더', 13, '#fff', wt=700) + _box(260, 95, 60, 40, OR, 'z', '', 15)
  + '<polygon points="330,95 420,70 420,160 330,135" fill="#a9bf8e"/>' + _t(375, 120, '디코더', 13, '#fff', wt=700) + _box(430, 80, 110, 70, IN, "x'", '복원') + _t(285, 195, '잠재 공간 z에서 새 점을 뽑으면 새 직물', 13)
  + _box(600, 55, 120, 60, OR, '잡음 z') + _ar(720, 85, 770, 85) + _box(775, 55, 130, 60, SG, '생성기') + _ar(905, 85, 950, 105) + _box(955, 80, 120, 70, NV, '판별기', '진짜? 가짜?') + _box(775, 140, 130, 50, IN, '실측 직물') + _ar(905, 165, 950, 135))
S(P['8'], '딥러닝 생성 모델 — 언제 쓰나', _dl + _tbl(['방법', '배우는 법', '원단 수', '이 과제에서'], [
  ['가우시안 혼합', '무리별 평균·공분산', '수십 개부터', '<b>1차 시작점</b> — 조건부 식이 정확, 해석 쉬움'], ['가우시안 코퓰라', '열별 분포 + 상관 구조', '수십 개부터', '분포가 치우친 항목이 많을 때'],
  ['VAE (TVAE)', '인코더로 잠재 공간 → 디코더로 복원', '수백 개 이상', '원단이 늘고 관계가 비선형일 때'], ['CTGAN', '생성기 vs 판별기, 범주 조건', '수백 개 이상', '소재·구조를 조건으로 줄 때' + _ref('M10')]], 't s'))
S(P['8'], '비교 기준 — 지도 회귀 (Lab 3)', '<div class="cols"><div class="bars">'
  + ''.join(f'<div class="bar"><span>{r.model}</span><i style="width:{max(r.test_R2, 0) * 100:.0f}%"></i><b>시험 R² {r.test_R2:.3f} · 새 조합 RMSE {r.newcombo_RMSE:.1f} V</b></div>' for r in _base.itertuples())
  + '</div><div><ul class="b"><li>평균 → 릿지 → 랜덤포레스트 → 가우시안 과정 순으로 복잡도를 올림</li><li>5겹 교차검증 + 시험 자료 + 새 조합(울 × 호프색)</li><li>릿지(선형)가 크게 뒤짐 — Voc는 곱셈 구조라 비선형</li>'
  '<li>새 조합 오차가 시험 오차보다 큼 — 본 적 없는 조합은 어렵다</li><li>생성 모델의 p(y|x)는 이 기준선을 넘어야 의미</li></ul></div></div>')
S(P['8'], '불확실도와 적용 범위 — 외삽을 믿지 않기', '<div class="cols c64"><div><div class="ctl"><button class="bt on" data-dm="0">적용 범위 안/밖</button><button class="bt" data-dm="1">예측 Voc</button> <span class="small">점 = Lab 4 생성 직물 400개, 회색 = 학습 원단</span></div>' + _cv('dmCv', 720, 420) + '</div>'
  + _side('적용 범위 세 조건', '<ol class="steps s"><li>각 항목이 학습 자료 1~99% 안</li><li>마할라노비스 거리가 학습 자료 99% 이내</li><li>예측 Y가 학습 Y 범위(4.6~126.8 V) 안</li></ol><p>Lab 6 함정: 범위 검사 없이 기대값 최고를 고르면 예측 240 V → 측정 50~77 V. X가 각각 범위 안이어도 <b>조합</b>이 새로우면 Y가 외삽됩니다.</p>') + '</div>', 'initDom')
S(P['8'], '모델 붕괴 — 생성 결과를 다시 학습하면', '<div class="cols c64"><div><div class="ctl">세대 <input type="range" id="clG" min="0" max="200" value="60"> <b id="clGV">60</b> · 세대당 표본 <input type="range" id="clN" min="10" max="200" step="10" value="30"> <b id="clNV">30</b></div>' + _cv('clCv', 720, 420) + '</div>'
  + _side('분포의 꼬리가 사라진다', '<p>log Voc 분포에 정규분포를 맞추고 → 거기서 뽑고 → 다시 맞추기를 반복한 20개 사슬입니다. 세대가 지날수록 퍼짐(표준편차)이 줄어 <b>극단 직물이 사라집니다</b>' + _ref('M12') + '.</p>'
  '<p>규칙: 생성 결과는 선별·예상에만 쓰고, 학습 재료는 실측에서만. 불확실도가 큰 곳을 골라 실제로 재는 <b>능동 학습</b>' + _ref('M14') + '이 반대 방향의 처방입니다.</p>') + '</div>', 'initCol')

# ================= 9 실습 =================
_files = [('00_measurement_template.csv', '실측 기록 양식 52열 + 예시 3행'), ('00_column_dictionary.csv', '열 뜻·단위·필수 여부'), ('01_mock_full.csv', '모의 원단 500개'),
          ('02_train.csv', '학습 384개'), ('02_test.csv', '시험 96개'), ('02_test_new_combo.csv', '새 조합 시험 20개 (울 × 호프색)'),
          ('03_qc_report_example.csv', 'Lab 1 결과'), ('04_generated_candidates_example.csv', 'Lab 4 — 새 직물 1000개, 예측·범위·적용 범위'),
          ('05_baseline_scores_example.csv', 'Lab 3 — 비교 기준 성적'), ('05_ks_example.csv', 'Lab 5 — 분포 비교'), ('05_tstr_result_example.csv', 'Lab 5 — TSTR'),
          ('06_verification_plan_example.csv', 'Lab 6 — 만들 후보와 측정 칸'), ('07_verification_result_example.csv', 'Lab 6 — 측정 후 판정'), ('08_inverse_candidates_example.csv', 'Lab 7 — 역방향 후보'),
          ('09_learning_curve_example.csv', 'Lab 8 — 원단 수별 R²')]
S(P['9'], '실습 키트 — practice/ 폴더', '<div class="cols"><div><pre class="code">practice/\n├─ README.md          상세 지침\n├─ requirements.txt   numpy pandas scikit-learn scipy matplotlib\n├─ data/              CSV 15개\n├─ prompts/           데이터 생성 프롬프트 (부록 A)\n├─ labs/\n│   common.py         경로·열 목록·변환·조건부 계산\n│   lab0_make_splits.py   (강사용) 자료 나누기\n│   lab1_check_data.py    품질 검사\n│   lab2_explore_pca.py   PCA\n│   lab3_baseline_regression.py\n│   lab4_generative_model.py\n│   lab5_validate_generated.py\n│   lab6_select_and_verify.py\n│   lab7_inverse_design.py\n│   lab8_how_many_fabrics.py\n└─ outputs/           실행 결과</pre></div><div>'
  + _tbl(['파일 (클릭하면 내려받기)', '내용'], [[f'<a href="../practice/data/{a}">{a}</a>', b] for a, b in _files], 't s') + '</div></div>')
_GH = 'https://github.com/adminmrobo/fabric_ai_project/blob/main/'
def _kb(path):
    try: return f'{max(1, round(os.path.getsize(os.path.join(B, "..", path)) / 1024))} KB'
    except OSError: return ''
_labs = ['common.py'] + sorted(f for f in os.listdir(os.path.join(_PR, 'labs')) if f.startswith('lab') and f.endswith('.py'))
def _dl(path, label=None):
    return f'<a href="../{path}" download>{label or os.path.basename(path)}</a> <span class="kb">{_kb(path)}</span>'
S(P['9'], '자료 내려받기 — 슬라이드의 모든 첨부물', '<div class="dlall"><a class="bt big" href="downloads/fabric_practice_kit.zip" download>⬇ 실습 키트 전체 (zip)</a>'
  '<span>CSV 15 · 실습 코드 10 · 지침 · 프롬프트 · 이미지 요청서 · 모의 데이터 생성기 — 압축을 풀고 <code>practice/README.md</code>부터</span></div><div class="cols c3">'
  '<div><h3>데이터 (CSV)</h3><ul class="dl">' + ''.join(f'<li>{_dl("practice/data/" + a)}</li>' for a, b in _files) + '</ul></div>'
  '<div><h3>실습 코드 (Python)</h3><ul class="dl">' + ''.join(f'<li>{_dl("practice/labs/" + f)}</li>' for f in _labs) + f'<li>{_dl("practice/requirements.txt")}</li></ul>'
  '<h3>모의 데이터 생성기</h3><ul class="dl">' + f'<li>{_dl("analysis/mock_data/generate_mock_fabric.py")}</li><li>{_dl("analysis/mock_data/mock_fabric_dictionary.json")}</li></ul></div>'
  '<div><h3>지침 · 부록</h3><ul class="dl">'
  f'<li>{_dl("practice/README.md", "README.md — 실습 지침")} <a href="{_GH}practice/README.md" target="_blank">보기</a></li>'
  f'<li>{_dl("practice/prompts/data_generation_prompts.md", "data_generation_prompts.md — 부록 A")} <a href="{_GH}practice/prompts/data_generation_prompts.md" target="_blank">보기</a></li>'
  f'<li>{_dl("slides/img/gs/GENSPARK_REQUESTS.md", "GENSPARK_REQUESTS.md — 부록 B")} <a href="{_GH}slides/img/gs/GENSPARK_REQUESTS.md" target="_blank">보기</a></li></ul>'
  '<p class="note">파일 이름을 누르면 바로 내려받고, "보기"는 GitHub에서 서식대로 엽니다. zip은 저장소와 같은 폴더 구조라 README의 명령이 그대로 동작합니다.</p></div></div>')
S(P['9'], '준비와 공통 규칙', '<div class="cols"><div><pre class="code">cd practice\npython -m venv .venv\nsource .venv/bin/activate   # Windows: .venv\\Scripts\\activate\npip install -r requirements.txt\ncd labs\npython lab1_check_data.py</pre>'
  '<p class="note">Python 3.10 이상. 결과는 practice/outputs/ 에, 같은 결과의 예시는 practice/data/ 에 미리 있음.</p></div><div><h3>다섯 가지 규칙</h3><ol class="steps">'
  '<li>변환 기준(평균·표준편차)은 학습 자료로만</li><li>성적은 실측(시험) 자료로만 — 생성 데이터를 섞어도</li><li>생성 결과를 다시 학습 자료로 넣지 않음</li><li>적용 범위 밖 예측은 믿지 않음</li><li>측정 오차보다 작은 오차는 과적합 신호</li></ol></div></div>')
S(P['9'], 'Lab 1 · 2 — 자료 점검과 탐색', '<div class="cols"><div><h3>Lab 1 자료 점검</h3><pre class="code">$ python lab1_check_data.py          # 기본 02_train.csv\n$ python lab1_check_data.py 실측.csv # 실측이 오면\n  저장: outputs/lab1_remeasure.csv (78행)\n  저장: outputs/lab1_qc_report.csv (67행)\n통과 66\n경고  1</pre>'
  '<ul class="b"><li>경고 1: CW_B 튀는 값 2개 → 입력 실수인지 실제 값인지 실험실과 확인</li><li>재측정 78개: Voc 3회 CV &gt; 0.15 → 실측이면 실험실에 목록 전달</li><li>실측 파일은 <code>00_measurement_template.csv</code> 열 이름 그대로</li></ul></div>'
  '<div><h3>Lab 2 PCA</h3><pre class="code">$ python lab2_explore_pca.py\n설명 비율 PC1 0.355  PC2 0.322  PC3 0.111\nW 열 길이 [1. 1. 1.]  PC1·PC2 내적 0.0\n  저장: lab2_pca_loadings.csv (19×3)\n  저장: lab2_pca_scores.csv, lab2_pca.png</pre><ul class="b">'
  '<li>할 일 ① 구조·소재별로 점이 갈리는지 그림에서 보기</li><li>② 가중치 표에서 PC1을 끄는 항목(굽힘 강성·굽힘 일) 적기</li><li>③ 실측 27개 결과(39%·29%)와 비교</li></ul></div></div>')
S(P['9'], 'Lab 3 · 4 — 비교 기준과 생성 모델', '<div class="cols"><div><h3>Lab 3 비교 기준 (지도 회귀)</h3><pre class="code">$ python lab3_baseline_regression.py\n평균(기준선)  CV R² -0.151 시험 R² -0.028 새 조합 41.8 V\n릿지          CV R²  0.757 시험 R²  0.829 새 조합 18.8 V\n랜덤포레스트  CV R²  0.820 시험 R²  0.920 새 조합 10.1 V\n가우시안 과정 CV R²  0.916 시험 R²  0.944 새 조합 10.3 V\n측정 오차 수준: Voc 반복 CV 중앙값 0.1</pre>'
  '<ul class="b"><li>새 조합(울 × 호프색) 오차가 시험 오차보다 큼</li><li>릿지(선형)가 크게 뒤짐 — 관계가 비선형</li></ul></div>'
  '<div><h3>Lab 4 생성 모델 (비지도)</h3><pre class="code">$ python lab4_generative_model.py\nBIC로 고른 무리 수: 4\n적용 범위 안 생성 직물: 837 / 1000\n  (Y 학습 범위 4.6~126.8 V)\n  저장: lab4_bic.csv, lab4_generated_candidates.csv\n        Voc_sampled  Voc_pred\nmedian       46.7      45.9\nmax         257.7     240.0   ← 외삽</pre><ul class="b">'
  '<li>Voc_sampled: 결합분포에서 X와 함께 뽑은 값 · Voc_pred·lo95·hi95: 조건부 평균과 범위</li><li>max 240 V는 학습 범위 밖 → in_domain = False</li><li>원단이 50개 미만이면 무리 수 1~3, 8항목으로</li></ul></div></div>')
S(P['9'], 'Lab 5 · 6 · 7 · 8 — 검증, 전향 검증, 역방향, 원단 수', '<div class="g2"><div class="card"><b>Lab 5 생성 검증</b><pre class="code">$ python lab5_validate_generated.py\nKS 9항목 모두 &lt; 0.1\n상관 차이 최대 0.058\nTRTR      R² 0.913\nTSTR      R² 0.818\n실측+생성 R² 0.897</pre><p>분포·상관은 닮았지만 생성은 새 정보를 주지 않음</p></div>'
  '<div class="card"><b>Lab 6 전향 검증</b><pre class="code">$ python lab6_select_and_verify.py\n기대값 최고 3   ✓✓✓\n범위 최대 3     ✓✗✗\n(함정) 3        ✗✗✗\n적용 범위 안 0.67</pre><p>measured_Voc 칸을 실험실 값으로 채우고 다시 실행</p></div>'
  '<div class="card"><b>Lab 7 역방향</b><pre class="code">$ python lab7_inverse_design.py 90\n목표 Voc* = 90 V\n무리 가중치 [0.81 0.10 0 0.09]\n→ 나일론 호프색·저지\n→ 울 저지·능직</pre><p>p(x | y*)에서 뽑은 직물을 만들 수 있는지 검토</p></div>'
  '<div class="card"><b>Lab 8 원단 수</b><pre class="code">$ python lab8_how_many_fabrics.py\n GP  n=40  R² 0.64 ± 0.21\n GP  n=100 R² 0.82 ± 0.11\n GP  n=250 R² 0.93 ± 0.01</pre><p>곡선이 평평해지는 원단 수 = S2 목표의 근거</p></div></div>'
  '<p class="note">각 Lab 결과 CSV는 practice/outputs/ 에 쓰이고, 같은 내용의 예시가 practice/data/ 에 있어 실행 전에도 열어 볼 수 있습니다. 자세한 지침은 practice/README.md.</p>')
S(P['9'], '결과판 — 전향 검증과 역방향', '<div class="cols"><div><h3>전향 검증 (Lab 6, 측정값은 예시)</h3>'
  + _tbl(['후보', '고른 이유', '예측', '95% 범위', '측정', '판정'], [[r.gen_id, r.reason.replace(' (적용 범위 안)', '').replace(' (모델이 가장 모름)', ''), _f(r.Voc_pred, 0), f'{r.Voc_lo95:.0f}~{r.Voc_hi95:.0f}', _f(r.measured_Voc, 0), '<b class="ok">✓</b>' if r.inside_95 else '<b class="ng">✗</b>'] for r in _ver.itertuples()], 't s')
  + '</div><div><h3>역방향 (Lab 7 방식)</h3><div class="ctl">목표 Voc* <button class="bt" data-iv="30">30 V</button><button class="bt" data-iv="60">60 V</button><button class="bt" data-iv="90">90 V</button></div><div id="ivOut"></div>'
  '<p class="note">후보 200개가 가장 닮은 원단의 소재·구조 빈도입니다.</p></div></div>', 'initInv')

# ================= 10 향후 =================
S(P['10'], '실측 이후 — 일정과 할 일', _tbl(['단계', '기간 (안)', '할 일', '산출물'], [
  ['S2 실측', '2026-12 ~ 2027-05', '양식대로 X·Y 측정, 장비 통일, 반복 3회, 재측정', '실측 CSV (50개 이상), Lab 1 보고'], ['생성기 보정', '실측 10개 시점', '분위수 맞춤 → σ₀ → SRA_opt → 습도', '보정된 생성기 v1.1'],
  ['S3 패턴 학습', '2027-02 ~ 06', 'Lab 2~5를 실측으로, 비교 기준과 비교', '생성 모델, TSTR 보고'], ['S4 생성·예측', '2027-04 ~ 09', '새 직물 생성, 적용 범위, 역방향 후보', '후보 목록'],
  ['S5 전향 검증', '2027-07 ~ 12', '후보 10개 이상 제작·측정, 판정, 다시 학습', '검증 보고, 2차년도 출발점']])
  + '<p class="note">2차년도에 섬유 이미지를 더할 때도 같은 원칙(실측 시험, 적용 범위, 생성 결과 재학습 금지)을 씁니다.</p>')
S(P['10'], '역할과 체크리스트', '<div class="cols"><div>' + _tbl(['역할', '맡는 일'], [['실험실', '설계 범위 확정, 원단 제작, FTT·전기 측정, 양식 기록, 재측정'], ['데이터·AI', '품질 검사, 생성기 보정, 생성 모델·비교 기준, 후보 선정, 보고'], ['함께', '측정 프로토콜 고정, 후보 검토(만들 수 있나), 판정 기준'], ['교수님', '방향·우선순위, 검토 항목 승인']])
  + '</div><div><h3>매번 확인</h3><ul class="check"><li>is_mock 표시가 있는가</li><li>측정 조건 열이 모두 채워졌는가</li><li>반복 CV 0.15 초과 원단을 재측정했는가</li><li>변환 기준을 학습 자료로만 정했는가</li><li>성적을 실측 시험 자료로만 쟀는가</li><li>생성 결과를 학습에 넣지 않았는가</li><li>후보가 적용 범위 안인가</li><li>예상값을 측정 전에 기록했는가</li></ul></div></div>')

# ================= 부록 A 프롬프트 가이드 =================
S(P['A'], '원칙 — LLM은 숫자가 아니라 코드와 근거를 만든다', '<div class="cols c55"><div class="g1">'
  '<div class="card"><i>1</i><b>숫자는 코드가 만든다</b><p>LLM에게 데이터 행을 직접 쓰게 하지 않습니다. 생성 규칙을 담은 코드를 받고, 숫자는 시드를 고정한 코드로 만듭니다.</p></div>'
  '<div class="card"><i>2</i><b>문헌값은 출처와 범위로</b><p>대표값마다 출처·범위를 요구하고, 모르면 "확인되지 않음"이라고 쓰게 합니다.</p></div>'
  '<div class="card"><i>3</i><b>결과는 다시 검증</b><p>LLM이 낸 표·코드는 Lab 1·5로 다시 점검합니다. LLM의 판단은 "확인 필요" 목록일 뿐입니다.</p></div></div><div>' + _gs('GS10', 250) + '</div></div>')
S(P['A'], '프롬프트의 여섯 칸', _tbl(['칸', '쓰는 것', '이 과제의 예'], [
  ['<b>역할</b>', '누구로서 답하나', '섬유공학 문헌 정리 보조 / 과학 시뮬레이션 개발자 / 데이터 품질 검토자'], ['<b>맥락</b>', '과제 정의, 자료 양식, 붙이는 파일', '1차년도 방법 정의, 52열 양식, generate_mock_fabric.py'],
  ['<b>요청</b>', '한 번에 하나', '"새틴 구조의 float·jam·surf를 제안하라"'], ['<b>제약</b>', '하지 말 것, 지킬 것', '숫자를 지어내지 않음, 열마다 독립 난수 금지, 기존 결과 불변'],
  ['<b>출력</b>', '형식을 정함', '마크다운 표 1개 / diff / STRUCTURES 한 줄 / CSV 열 이름'], ['<b>자체 점검</b>', '끝에 스스로 확인할 것', '단위, 출처 없는 숫자, 기존 결과와 같음 테스트']]))
for _i in range(0, len(SC.PROMPTS), 2):
    _pp = SC.PROMPTS[_i:_i + 2]
    S(P['A'], '프롬프트 ' + ' · '.join(f'{p[0]} {p[1]}' for p in _pp), '<div class="cols">' + ''.join(
        f'<div><div class="ph"><b>{p[0]}</b> {p[1]} <span>— {p[2]}</span><button class="bt cp" data-cp="{p[0]}">복사</button></div><pre class="code pr">{_html.escape(p[3])}</pre></div>' for p in _pp) + '</div>')
S(P['A'], '나쁜 프롬프트 → 좋은 프롬프트', _tbl(['나쁜 예', '좋은 예'], [[f'<span class="ng">{a}</span>', b] for a, b in SC.BAD_GOOD])
  + '<p class="note">전체 프롬프트는 <a href="../practice/prompts/data_generation_prompts.md">practice/prompts/data_generation_prompts.md</a>에 있습니다. 붙일 파일과 [ ] 칸만 바꿔 씁니다.</p>')

# ================= 부록 B 이미지 요청서 =================
S(P['B'], 'Genspark 이미지 요청서 — 공통 스타일', '<div class="cols c55"><div><div class="ph"><b>공통 스타일 블록</b> <span>— 모든 요청 앞에 붙임</span><button class="bt cp" data-cp="STYLE">복사</button></div><pre class="code pr">' + _html.escape(SC.GS_STYLE) + '</pre>'
  '<ul class="b"><li>참고: 시멘트 공정 교안(2장)의 삽화 — 크림 배경, 파스텔 인디고·피치·세이지, 둥근 아이콘, 점선 연결</li><li>만든 그림을 <code>slides/img/gs/GS01.png</code>처럼 번호 이름으로 넣으면 슬라이드가 바로 바꿔 보여 줌</li><li>그림이 없으면 같은 자리에 도식(지금 보이는 그림)이 대신 나옴</li></ul></div>'
  '<div>' + _tbl(['번호', '쓰는 곳', '제목'], [[g[0], g[1], g[2]] for g in SC.GS_REQ], 't s') + '</div></div>')
for _i in range(0, len(SC.GS_REQ), 5):
    S(P['B'], f'이미지 요청 {SC.GS_REQ[_i][0]}~{SC.GS_REQ[min(_i + 4, len(SC.GS_REQ) - 1)][0]}', _tbl(['번호', '제목', '장면 (공통 스타일 블록 뒤에 붙임)', ''], [[f'<b>{g[0]}</b>', g[2], f'<span class="s">{g[3]}</span>', f'<button class="bt cp" data-cp="{g[0]}">복사</button>'] for g in SC.GS_REQ[_i:_i + 5]], 't s'))

# ================= 참고문헌·끝 =================
_rs = [(k, c, u) for k, c, u, w in MREF2] + [(k, c, u) for k, c, u, w in MREFS if k in ('M1', 'M2', 'M3', 'M4', 'M5', 'M10', 'M11', 'M12', 'M14')]
_half = (len(_rs) + 1) // 2
for i, part in enumerate((_rs[:_half], _rs[_half:])):
    S(P['R'], f'참고문헌 ({i + 1}/2)', '<ol class="refs">' + ''.join(f'<li><b>[{k}]</b> {c}' + (f' <a href="{u}">링크</a>' if u else '') + '</li>' for k, c, u in part) + '</ol>')
S(P['R'], '', '<div class="cover end"><div><div class="eyeb">정리</div><h1>네 문장</h1><ul class="b big"><li>섬유 특성은 <b>주고받는 양(소재) × 닿는 면적(구조·표면) × 남는 양(환경)</b>으로 전기 특성이 된다</li><li>데이터는 그 곱셈 순서대로, 만들 수 있는 직물만, 실측에서 가져온 잡음으로 만든다</li><li>학습은 비지도 생성 모델, 출력은 연속값과 범위, 지도 회귀는 비교 기준</li><li>성적은 실측으로, 적용 범위 밖은 믿지 않고, 일부를 실제로 만들어 확인한다</li></ul>'
  '<p class="lead">실습: <a href="../practice/README.md">practice/README.md</a> · 프롬프트: <a href="../practice/prompts/data_generation_prompts.md">부록 A 원문</a> · <a href="../mock_data_guide.html">모의 데이터 생성 가이드</a> · <a href="../method_review.html">방법 검토</a></p></div></div>')

# ---------------- 조립 ----------------
_N = len(SL); _secs = []; _cnt = {}
for i, ((pk, pn), title, body, init) in enumerate(SL):
    _cnt[pk] = _cnt.get(pk, 0) + 1
    head = (f'<div class="eyeb">{pk}.{_cnt[pk]} · {pn}</div><h2>{title}</h2><div class="rule"></div>') if title else ''
    foot = f'<footer><span>{pn}</span><span>섬유직물 데이터 생성 가이드</span><span>{i + 1} / {_N}</span></footer>' if i else ''
    _secs.append(f'<section class="slide" data-init="{init}" data-part="{_html.escape(pk + " " + pn)}">{head}<div class="body">{body}</div>{foot}</section>')

SLIDE_CSS = open(os.path.join(B, 'slides.css'), encoding='utf-8').read()
SLIDE_JS = open(os.path.join(B, 'slides.js'), encoding='utf-8').read()
_cp = {p[0]: p[3] for p in SC.PROMPTS}; _cp.update({g[0]: SC.GS_STYLE + '\n\n' + g[3] for g in SC.GS_REQ}); _cp['STYLE'] = SC.GS_STYLE
_slides_html = ('<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
  '<title>섬유직물 데이터 생성 가이드 — 웹 슬라이드</title><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@600;700;900&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">'
  '<style>' + SLIDE_CSS + '</style>' + MK_CSS + '</head><body>'
  '<div id="bar"></div><div id="deck">' + ''.join(_secs) + '</div>'
  '<div id="nav"><button id="pv" aria-label="이전">←</button><button id="ob">전체 보기 (O)</button><button id="nx" aria-label="다음">→</button></div><div id="ov"></div>'
  '<script>var D=' + _SDJ + ';var CP=' + _sj.dumps(_cp, ensure_ascii=False) + ';\n' + SLIDE_JS + '</script></body></html>')
import re as _re
_slides_html = _re.sub(r'href="(\.\./practice/[^"]+)"(?! download)', r'href="\1" download', _slides_html)
open(os.path.join(B, '..', 'slides', 'index.html'), 'w', encoding='utf-8').write(_slides_html)

# 부록 원문 파일
os.makedirs(os.path.join(_PR, 'prompts'), exist_ok=True)
open(os.path.join(_PR, 'prompts', 'data_generation_prompts.md'), 'w', encoding='utf-8').write(
    '# 데이터 생성 프롬프트 가이드 (부록 A)\n\n원칙: LLM은 숫자가 아니라 **생성 코드와 근거**를 만든다. 숫자는 시드를 고정한 코드가 만들고, 결과는 Lab 1·5로 다시 검증한다.\n\n'
    '프롬프트의 여섯 칸: 역할 · 맥락 · 요청 · 제약 · 출력 · 자체 점검\n\n'
    + ''.join(f'## {p[0]} {p[1]}\n\n언제: {p[2]}\n\n```text\n{p[3]}\n```\n\n' for p in SC.PROMPTS)
    + '## 나쁜 예 → 좋은 예\n\n| 나쁜 예 | 좋은 예 |\n|---|---|\n' + ''.join(f'| {a} | {b} |\n' for a, b in SC.BAD_GOOD)
    + '\n## 데이터 생성 원칙 10조\n\n' + ''.join(f'{i + 1}. **{a}** — {b} (어기면: {c})\n' for i, (a, b, c) in enumerate(SC.PRINCIPLES))
    + '\n## 하지 말 것\n\n' + ''.join(f'- **{a}** — {b}\n' for a, b in SC.DONTS))
os.makedirs(os.path.join(B, '..', 'slides', 'img', 'gs'), exist_ok=True)
open(os.path.join(B, '..', 'slides', 'img', 'gs', 'GENSPARK_REQUESTS.md'), 'w', encoding='utf-8').write(
    '# Genspark 이미지 요청서 (부록 B)\n\n만든 그림은 이 폴더에 `GS01.png` … `GS10.png` 이름으로 넣는다. 그림이 없으면 슬라이드는 같은 자리에 도식을 보여 준다.\n\n'
    '## 공통 스타일 블록 (모든 요청 앞에 붙임)\n\n```text\n' + SC.GS_STYLE + '\n```\n\n'
    + ''.join(f'## {g[0]} — {g[2]}\n\n쓰는 곳: {g[1]}\n\n```text\n{SC.GS_STYLE}\n\n{g[3]}\n```\n\n' for g in SC.GS_REQ))
print('slides/index.html', _N, 'slides', len(_slides_html) // 1024, 'KB')

# 실습 키트 zip (저장소와 같은 폴더 구조, 시각 고정 — 빌드마다 바뀌지 않게)
import zipfile as _zf
_root = os.path.normpath(os.path.join(B, '..'))
_items = ['practice/README.md', 'practice/requirements.txt'] + [f'practice/data/{a}' for a, b in _files] + [f'practice/labs/{f}' for f in _labs] + [
    'practice/prompts/data_generation_prompts.md', 'analysis/mock_data/generate_mock_fabric.py', 'analysis/mock_data/mock_fabric_dictionary.json', 'slides/img/gs/GENSPARK_REQUESTS.md']
os.makedirs(os.path.join(_root, 'slides', 'downloads'), exist_ok=True)
with _zf.ZipFile(os.path.join(_root, 'slides', 'downloads', 'fabric_practice_kit.zip'), 'w', _zf.ZIP_DEFLATED) as z:
    for it in _items:
        zi = _zf.ZipInfo('fabric_practice_kit/' + it, date_time=(2026, 11, 18, 0, 0, 0)); zi.compress_type = _zf.ZIP_DEFLATED; zi.external_attr = 0o644 << 16
        z.writestr(zi, open(os.path.join(_root, it), 'rb').read())
    zi = _zf.ZipInfo('fabric_practice_kit/practice/outputs/', date_time=(2026, 11, 18, 0, 0, 0)); z.writestr(zi, b'')
print('zip', len(_items), 'files')
