import json, re, base64, os, sys, copy
B = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, B)
import kg as K
import chars as CH
OUT = os.environ.get('LAB_OUT', os.path.join(B, '..'))
os.makedirs(OUT, exist_ok=True)
T = open(f'{B}/template.html', encoding='utf-8').read()
JS0 = open(f'{B}/assets_lab.js', encoding='utf-8').read()
RJ = open(f'{B}/assets_robo.js', encoding='utf-8').read()
i = JS0.index('/* ---------- 그리기 시작')
JS = JS0[:i] + RJ + JS0[i:]
SIMS = open(f'{B}/sims.js', encoding='utf-8').read()
DATA = json.load(open(f'{B}/data.json'))

def js(o): return json.dumps(o, ensure_ascii=False).replace('</', '<\\/')
def sec(id_):
    m = re.search(r'(<section class="level[^"]*" id="%s">.*?</div></section>)' % id_, T, re.S)
    return m.group(1)

HEAD = T[:T.index('</style>')]
FOOT = T[T.index('<footer>'):T.index('<div id="tip"')]
COVER = T[T.index('<div class="cover" id="top">'):T.index('<header class="hero">')]
INTRO = sec('intro')

EXTRA_CSS = r"""
.sm4{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;margin:14px 0}
.sm4 .st4{position:relative;border:1px solid var(--rule);border-radius:12px;padding:10px;background:#fff}
.sm4 .st4:not(:last-child)::after{content:"→";position:absolute;right:-19px;top:42%;font-size:20px;font-weight:800;color:#1e55c8}
.sm4 .st4 h5{margin:0 0 6px;font-size:14px}.sm4 .st4 h5 i{font-style:normal;display:inline-block;width:22px;height:22px;line-height:22px;text-align:center;border-radius:50%;background:#1e55c8;color:#fff;font-size:12px;margin-right:4px}
.sm4 canvas{width:100%;height:auto;display:block;border-radius:8px;background:#f4f6f8}
.sm4 #smA{cursor:crosshair}.sm4 p{font-size:13.5px;line-height:1.6;margin:8px 0 0;color:var(--muted)}
.vtxt{font-family:ui-monospace,Menlo,monospace;font-size:12px;background:#f4f6f8;border-radius:6px;padding:6px 8px;margin:6px 0;word-break:break-all;line-height:1.5}
.nnflow{display:grid;grid-template-columns:1.1fr 1.6fr 1fr 1fr 1.3fr 1fr;gap:16px;align-items:stretch;margin:14px 0}
.nnflow>div{position:relative;border:1px solid var(--rule);border-radius:12px;padding:10px;background:#fff;font-size:13.5px;line-height:1.55}
.nnflow>div:not(:last-child)::after{content:"→";position:absolute;right:-15px;top:40%;font-weight:800;color:#1e55c8}
.nnflow h5{margin:0 0 6px;font-size:13.5px}.nnflow canvas{width:100%;height:auto;display:block;border-radius:6px;border:1px solid var(--rule)}
.nnflow .fm{display:grid;grid-template-columns:1fr 1fr;gap:6px}.nnflow .fm figure{margin:0;font-size:11.5px;text-align:center;color:var(--muted)}
.nnflow .concept{background:#fbfcfd;border-style:dashed}
#smVec{display:grid;grid-template-columns:auto minmax(40px,1fr) auto;gap:5px 8px;align-items:center;font-size:12.5px}#smVec .track{height:10px;min-width:40px;position:relative;background:#eef1f4;border-radius:5px}#smVec .fill{position:absolute;top:0;bottom:0;border-radius:5px}
.nnflow canvas{max-width:240px;margin:0 auto}
@media (max-width:980px){.nnflow{grid-template-columns:1fr 1fr}.nnflow>div::after{display:none}}
@media (max-width:860px){.sm4{grid-template-columns:1fr 1fr}.sm4 .st4::after{display:none}}
@media (max-width:420px){.nnflow{grid-template-columns:1fr}}
.labcard{display:grid;grid-template-columns:1fr auto;gap:4px 16px;align-items:center;border:1.5px solid #1e55c8;border-radius:14px;padding:14px 18px;margin:12px 0 16px;background:#f4f7fd}
.labcard .lk{grid-column:1/-1;font-size:12px;font-weight:700;color:#1e55c8;letter-spacing:.04em}
.labcard .ln{font-size:17px}.labcard .lp{font-size:15px}.labcard .lf{font-size:13.5px;color:var(--muted);grid-column:1}
.labcard a.bt{grid-column:2;grid-row:2/5;white-space:nowrap;text-decoration:none}
@media (max-width:600px){.labcard{grid-template-columns:1fr}.labcard a.bt{grid-column:1;grid-row:auto;justify-self:start}}
.crumb{font-size:13px;color:var(--muted);margin:0 0 6px}.crumb a{color:var(--muted)}
.st{display:inline-block;font-size:12px;font-weight:700;padding:2px 9px;border-radius:999px;border:1.5px solid;vertical-align:middle;white-space:nowrap;line-height:1.5}
.st.run{color:#13733a;border-color:#13733a;background:#e8f5ec}.st.part{color:#1e55c8;border-color:#1e55c8;background:#e6eefb}
.st.draft{color:#a35c00;border-color:#a35c00;background:#fff4e2}.st.plan{color:#5b6874;border-color:#8a96a3;border-style:dashed;background:#fff}
.st.done{color:#fff;border-color:#13733a;background:#13733a}
.shead{border:1px solid var(--rule);border-radius:14px;padding:18px 20px;margin:18px 0;background:#fbfcfd}
.shead dl{display:grid;grid-template-columns:110px 1fr;gap:8px 14px;margin:10px 0 0}.shead dt{font-weight:700;color:var(--muted)}.shead dd{margin:0}
.mapc{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin:16px 0}
.mapc a.card{display:block;border:1px solid var(--rule);border-radius:14px;padding:16px 18px;text-decoration:none;color:var(--text);background:#fff;transition:border-color .15s,transform .15s}
.mapc a.card:hover,.mapc a.card:focus-visible{border-color:#1e55c8;transform:translateY(-2px)}
.mapc a.card b{display:block;font-size:16px;margin:6px 0 4px}.mapc a.card span.d{font-size:14px;color:var(--muted);line-height:1.6}
.mapc a.card.plan{border-style:dashed;background:#fbfcfd}
.yr{border:1px solid var(--rule);border-radius:14px;padding:18px 20px;margin:16px 0;background:#fff}
.yr.plan{border-style:dashed;background:#fbfcfd}
.yr h3{margin:0 0 8px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.yr .cols{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.yr ul{margin:6px 0 0;padding-left:20px}.yr h4{margin:10px 0 2px;font-size:14px;color:var(--muted)}
.chk{width:100%;border-collapse:collapse;font-size:14.5px}.chk td,.chk th{border-bottom:1px solid var(--rule);padding:9px 8px;text-align:left;vertical-align:top}
.chk td:last-child{white-space:nowrap}
.pager{display:flex;justify-content:space-between;gap:12px;margin:30px 0 0;flex-wrap:wrap}
.pager a{border:1px solid var(--rule);border-radius:12px;padding:12px 16px;text-decoration:none;color:var(--text);max-width:48%}
.pager a small{display:block;color:var(--muted)}
.planbox{border:1.5px dashed #8a96a3;border-radius:14px;padding:16px 18px;margin:14px 0;background:#fbfcfd}
.planbox h4{margin:0 0 6px}
nav.top a.l[aria-current="page"]{font-weight:800;text-decoration:underline;text-underline-offset:4px}
nav.top .sep{color:var(--rule);margin:0 2px}
.stgrid{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;margin:14px 0}
.stgrid a{border:1px solid var(--rule);border-radius:10px;padding:10px 8px;text-align:center;text-decoration:none;color:var(--text);font-size:13px;background:#fff}
.stgrid a b{display:block;font-size:15px}.stgrid a.plan{border-style:dashed}
.say[data-who=robo] img.who{border-color:var(--c-robo)} .say[data-who=robo] .name{color:var(--c-robo)}
.rq{border:1.5px solid var(--c-robo);border-radius:16px;padding:18px 20px;background:#f3fafb;margin:14px 0}
.rq .step{display:grid;grid-template-columns:120px 1fr;gap:10px;align-items:start;margin:10px 0}
.rq .step>b{font-size:14px;color:var(--c-robo);padding-top:6px}
.rq .opts{display:flex;flex-wrap:wrap;gap:6px}
.rq .bt.rqc[aria-pressed="true"]{background:var(--c-robo);border-color:var(--c-robo);color:#fff}
.bt.sm{font-size:12.5px;padding:3px 9px;min-height:28px}
.rq textarea{width:100%;min-height:70px;border:1px solid var(--rule);border-radius:10px;padding:10px 12px;font:inherit;font-size:15px;box-sizing:border-box;background:#fff}
.rq blockquote{margin:0 0 6px;padding:8px 12px;border-left:4px solid var(--c-robo);background:#fff;border-radius:6px;font-size:14px}
.rqlist{list-style:none;padding:0;margin:10px 0}.rqlist li{border:1px solid var(--rule);border-radius:10px;padding:10px 12px;margin:6px 0;background:#fff;font-size:14.5px;line-height:1.7}
.rqlist li.done{opacity:.6}.rqlist .rqb{display:flex;gap:6px;margin-top:6px}
.rqpin{display:inline-flex;align-items:center;gap:4px;margin-left:10px;vertical-align:middle;font-size:12px;font-weight:600;color:var(--c-robo);background:#fff;border:1px solid var(--c-robo);border-radius:999px;padding:1px 9px 1px 3px;cursor:pointer;line-height:1.6}
.rqpin img{width:20px;height:20px;border-radius:50%;object-fit:cover}
.rqpin:hover,.rqpin:focus-visible{background:#e3f4f6}
#roboFab{position:fixed;right:16px;bottom:16px;z-index:60;display:flex;align-items:center;gap:8px;background:#fff;border:2px solid var(--c-robo);border-radius:999px;padding:4px 14px 4px 4px;font-weight:700;color:var(--c-robo);box-shadow:0 4px 16px rgba(11,122,134,.25);cursor:pointer;font-size:14px}
#roboFab img{width:40px;height:40px;border-radius:50%;object-fit:cover;background:#f3fafb}
.thumbs{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:8px;margin:10px 0}
.thumbs figure{margin:0;font-size:12px;color:var(--muted);text-align:center}.thumbs img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:8px;border:1px solid var(--rule)}
.thumbs figure.bad img{outline:3px solid #c9302c;outline-offset:-3px}
.prob td:first-child{font-weight:700;white-space:nowrap}
.code{font-family:ui-monospace,Menlo,monospace;font-size:13px;background:#f4f6f8;border:1px solid var(--rule);border-radius:8px;padding:10px 12px;white-space:pre-wrap;word-break:break-all;margin:8px 0}
.refl{list-style:none;padding:0}.refl li{border-bottom:1px solid var(--rule);padding:10px 0;line-height:1.7}.refl .why{display:block;font-size:14px;color:var(--muted)}
@media (max-width:600px){#roboFab span{display:none}#roboFab{padding:4px}.rq .step{grid-template-columns:1fr}}
@media (max-width:860px){.yr .cols{grid-template-columns:1fr}.stgrid{grid-template-columns:repeat(4,1fr)}.shead dl{grid-template-columns:88px 1fr}.pager a{max-width:100%;flex:1 1 100%}}
"""

STAGES = [
 dict(k='s0', n=0, file='stage_0_kickoff.html', name='착수·자료 정리', st='run', stl='진행 중', per='2026-11-16 ~ 2026-11-30', own='AI 분석 쪽 (평직이·능직이·편직이)', gate='G1 — 변수와 정답(Y)의 정의 합의 (2026-11-30)', out='데이터 사전, 변수 역할표(B·C·A·Y), 결정 질문 10개의 답', yr='1차년도 · 실/직물 구조 DB 구축', d='받은 자료 8가지를 정리하고, 무엇이 있고 무엇이 비었는지 진단합니다.'),
 dict(k='s1', n=1, file='stage_1_explore.html', name='파일럿 탐색 분석', st='part', stl='일부 완료', per='2026-12-01 ~ 2027-01-15', own='AI 분석 쪽', gate='— (관문 없음, S3로 넘김)', out='정제한 27개 원단 표, 핵심 후보 변수 10개 안팎', yr='1차년도 · 구조–마찰–압축 관계의 정량 분석', d='기존 원단 27개로 닮음 지도와 장비 간 일치도를 먼저 봅니다.'),
 dict(k='s2', n=2, file='stage_2_data.html', name='샘플 확충·전기 특성 실측', st='draft', stl='설계안', per='2026-12-01 ~ 2027-05-31', own='실험실 (제작·측정) + AI 쪽 (입력 양식, 자동 품질검사)', gate='G2 — 원단 50개 이상 직물 특성(X)·전기 특성(Y) 실측 완료 (2027-05-31)', out='마스터 표 (원단 × 직물 특성 X × 전기 특성 Y), 반복 측정 원자료', yr='1차년도 · 직물 특성 DB + 전기적 특성 실측', d='같은 장비·같은 조건으로 원단을 만들고, 직물 특성(X)과 전기적 특성(Y, 마찰전기 출력)을 함께 잽니다.'),
 dict(k='s3', n=3, file='stage_3_model.html', name='전기 특성 회귀 모델', st='draft', stl='설계안', per='2027-02-01 ~ 2027-06-30', own='AI 분석 쪽', gate='G3 — 기준선보다 나은 회귀 모델과 원단 단위 교차검증 보고서 (2027-06-30)', out='직물 특성 → 전기 특성 회귀 모델, 교차검증 보고서, 변수 영향도', yr='1차년도 · 직물 특성 → 전기 특성 회귀 (실측 정답으로 학습)', d='실측 원단으로 "직물 특성 → 전기 특성" 회귀 모델을 만들고, 원단 단위로 나눠 검증합니다.'),
 dict(k='s4', n=4, file='stage_4_sim2real.html', name='실측 기반 데이터 생성', st='draft', stl='설계안', per='2027-04-01 ~ 2027-09-30', own='AI 분석 쪽 (생성) + 실험실 (만들 수 있는 범위 검토)', gate='G4 — 생성 데이터 품질 검사 통과 (분포·범위·물리 방향)', out='가상 직물 표(X), 품질 검사 보고, 생성 방식 비교', yr='1차년도 · 실측 근거 가상 직물 생성 (시뮬레이션은 보조 경로)', d='실측 직물 특성의 분포를 배워 가상 직물을 만듭니다. 시뮬레이션(TexGen·Abaqus)은 보조 경로입니다.'),
 dict(k='s5', n=5, file='stage_5_tribo.html', name='생성 직물 예측·검증', st='draft', stl='설계안', per='2027-07-01 ~ 2027-12-15', own='AI 분석 쪽 (예측) + 실험실 (검증용 제작·측정)', gate='G5 — 선정한 생성 직물을 실제로 만들어 예측과 맞춰 봄', out='생성 직물별 예측값과 불확실도, 전향 검증 보고', yr='1차년도 · 생성 직물의 전기 특성 예측 → 일부 실측 검증', d='가상 직물의 전기 특성을 예측하고, 그중 일부를 실제로 만들어 예측이 맞는지 확인합니다.'),
 dict(k='s6', n=6, file='stage_6_device.html', name='측정 장치 개선', st='plan', stl='예정', per='2027-07-01 ~ 2027-11-30 (예정)', own='예정 — 미확정', gate='예정', out='개선 장치 설계안, 특허 선행조사 (예정)', yr='킥오프 문서의 장치 개선 과제 (연차 배정 예정)', d='핵심 변수를 정확하고 쉽게 잴 수 있게 장치를 고칩니다.'),
]
SBY = {s['k']: s for s in STAGES}

ANCH = {'#lv1': 'stage_0_kickoff.html#lv1', '#lv2': 'stage_1_explore.html#lv2', '#lv3': 'stage_2_data.html#lv3',
        '#lv4': 'stage_3_model.html#lv4', '#lv5': 'stage_3_model.html#lv5', '#plan': 'stages.html#plan',
        '#ask': 'stage_0_kickoff.html#ask', '#flow': 'stages.html#flow'}
def fixa(a): return ANCH.get(a, a if '.html' in a else 'index.html' + a)
KG = copy.deepcopy(K.KG)
for n in KG['nodes']: n['anchor'] = fixa(n.get('anchor', '#top'))
for e in KG['edges']:
    if 'anchor' in e: e['anchor'] = fixa(e['anchor'])

def chip(s): return f'<span class="st {s["st"]}">{s["stl"]}</span>'

def nav(cur):
    L = [('index.html', '전체 계획'), ('index.html#ai-summary', 'SUMMARY'), ('plan_years.html', '연차별 계획'), ('stages.html', '스테이지·FLOW')]
    h = '<nav class="top" aria-label="문서 바로가기"><div class="wrap"><a class="logo" href="index.html">섬유 AI 연구 브리핑</a>'
    for f, t in L: h += f'<a class="l" href="{f}"' + (' aria-current="page"' if f == cur else '') + f'>{t}</a>'
    h += '<span class="sep">|</span>'
    for s in STAGES:
        h += f'<a class="l" href="{s["file"]}" title="{s["name"]} ({s["stl"]})"' + (' aria-current="page"' if s['file'] == cur else '') + f'>S{s["n"]}{"·예정" if s["st"]=="plan" else ""}</a>'
    h += '<span class="sep">|</span>'
    for f, t in [('method_review.html', '방법 검토'), ('image_data.html', '이미지(2차년도)'), ('data_guide.html', '작성 가이드'), ('references.html', '참고문헌')]:
        h += f'<a class="l" href="{f}"' + (' aria-current="page"' if f == cur else '') + f'>{t}</a>'
    h += '<span class="sep">|</span><a class="l" href="https://fashion.hanyang.ac.kr/-19" target="_blank" rel="noopener" title="한양대 스마트텍스타일연구실 (배지현 교수)">연구실 소개 ↗</a>'
    return h + '</div></nav>'

def crumb(*parts):
    return '<p class="crumb">' + ' › '.join(f'<a href="{f}">{t}</a>' if f else t for f, t in parts) + '</p>'

def say(who, mood, txt):
    nm = {'sia': '능직이', 'moa': '편직이', 'asst': '평직이', 'robo': '부직이'}[who]
    return f'<div class="say" data-who="{who}"><img class="who" data-who="{who}" data-mood="{mood}" alt="" aria-hidden="true"><div class="bub"><b class="name">{nm}</b><p>{txt}</p></div></div>'

def pager(prev, nxt):
    h = '<div class="pager">'
    h += f'<a href="{prev[0]}"><small>← 이전</small>{prev[1]}</a>' if prev else '<span></span>'
    h += f'<a href="{nxt[0]}" style="text-align:right"><small>다음 →</small>{nxt[1]}</a>' if nxt else '<span></span>'
    return h + '</div>'

def stage_head(s, rows):
    h = f'<div class="shead"><div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap"><b style="font-size:17px">S{s["n"]} · {s["name"]}</b>{chip(s)}<span class="small muted">2026-11-17 기준</span></div>'
    h += f'<dl><dt>하는 일</dt><dd>{s["d"]}</dd><dt>기간</dt><dd>{s["per"]}</dd><dt>담당</dt><dd>{s["own"]}</dd><dt>관문</dt><dd>{s["gate"]}</dd><dt>산출물</dt><dd>{s["out"]}</dd><dt>연차 연결</dt><dd>{s["yr"]} · <a href="plan_years.html">연차별 계획 보기</a></dd></dl>'
    h += '<h4 style="margin:16px 0 4px">이 스테이지 항목별 상태</h4><div class="tw"><table class="chk"><tr><th>항목</th><th>상태</th></tr>'
    for t, c in rows:
        cl = {'완료': 'done', '진행 중': 'run', '일부 완료': 'part', '설계안': 'draft', '예정': 'plan'}[c]
        h += f'<tr><td>{t}</td><td><span class="st {cl}">{c}</span></td></tr>'
    return h + '</table></div></div>'

def sprites(html):
    # 섬유 조직 캐릭터(chars.py)를 표정별 SVG로 만들어 넣는다 — 외부 그림 팩 없음
    moods = set(re.findall(r'data-who="(\w+)" data-mood="(\w+)"', html))
    for w in CH.CAST: moods.add((w, 'smile'))
    for m in ['calc','happy','smile','chart','meh','wow']: moods.add(('robo', m))
    return {f'{w}_{m}': CH.uri(w, m) for w, m in sorted(moods) if w in CH.CAST}

def page(fname, title, body, cur=None, kg=False, extra=None):
    head = HEAD.replace('<title>', '<title>', 1)
    head = re.sub(r'<title>.*?</title>', f'<title>{title} — 섬유 AI 연구 브리핑</title>', head, flags=re.S)
    html = head + EXTRA_CSS + '</style>\n</head><body>\n<div id="prog" aria-hidden="true"></div>\n' + nav(cur or fname) + '\n' + body + '\n' + FOOT + '<div id="tip" role="tooltip"></div>\n<button type="button" id="roboFab" aria-label="부직이에게 수정·보완 요청"><img alt=""><span>수정 요청</span></button>\n'
    lab = {'data': DATA, 'refs': K.REFS, 'meta': K.META, 'page': {'file': fname, 'title': title}}
    if extra: lab.update(extra)
    if kg: lab['kg'] = KG
    scr = '<script>\nwindow.LAB=' + js(lab) + ';\n' + SIMS + '\nvar SPRITE=' + js(sprites(html)) + ';\n' + JS + '\n</script>\n'
    if kg: scr = '<script type="application/ld+json" id="kg-ld">' + js(K.jsonld(KG)) + '</script>\n' + scr
    html += scr + '</body></html>'
    open(f'{OUT}/{fname}', 'w', encoding='utf-8').write(html)
    return len(html.encode())

# ---------------- 스테이지 쪽 본문 다듬기 ----------------
def lv(id_, title, rev=None, drop_rev=False):
    s = sec(id_)
    s = re.sub(r'<h2>보고[①②③④⑤] [^<]*</h2>', f'<h2>{title}</h2>', s, count=1)
    if drop_rev: s = re.sub(r'\s*<div class="review" data-rev="r\d"></div>', '', s)
    elif rev: s = re.sub(r'<div class="review" data-rev="r\d"></div>', f'<div class="review" id="review-{rev}" data-rev="{rev}"></div>', s)
    return s

def wrap(inner): return f'<section class="level"><div class="wrap">{inner}</div></section>'
ROBO = ('<section class="level" id="robo"><div class="wrap"><h2>부직이에게 수정·보완 요청</h2>'
  '<div class="say" data-who="robo"><img class="who" id="rqFace" data-who="robo" data-mood="calc" alt="" aria-hidden="true"><div class="bub"><b class="name">부직이</b><p id="rqSay">이 쪽에서 고칠 곳을 알려 주세요. 두 번 누르고 한 줄만 쓰시면 요청서가 됩니다. 제목 옆 "요청" 단추로 바로 오셔도 됩니다.</p></div></div>'
  '<div class="rq" id="roboReq">'
  '<div class="step"><b>① 어디를</b><div class="opts" id="rqSec" role="group" aria-label="고칠 위치"></div></div>'
  '<div class="step"><b>② 무엇을</b><div class="opts" id="rqKind" role="group" aria-label="요청 유형"></div></div>'
  '<div class="step"><b>③ 언제까지</b><div class="opts" id="rqPri" role="group" aria-label="기한"></div></div>'
  '<div class="step"><b>④ 고칠 문장</b><div><div id="rqQuote"></div><button type="button" class="bt sm" id="rqGrab" style="margin-top:6px">선택한 글 가져오기</button></div></div>'
  '<div class="step"><b>⑤ 한 줄 메모</b><div><textarea id="rqMemo" aria-label="요청 메모 (선택)"></textarea><div class="opts" id="rqQuick" style="margin-top:6px"></div></div></div>'
  '<div class="ctrl"><button type="button" class="bt primary" id="rqGo" disabled>요청 접수</button><button type="button" class="bt" id="rqReset">다시 고르기</button><span class="small muted" id="rqHint" aria-live="polite"></span></div>'
  '<p class="small muted" style="margin:6px 0 0">메모는 비워도 됩니다. Ctrl + Enter로도 접수됩니다. 요청은 이 브라우저에만 남고, <a href="index.html#reqs">INDEX의 요청 모음</a>에서 한꺼번에 복사·내려받기 합니다.</p></div>'
  '<h3>이 쪽의 요청 <span class="num" id="rqN">0</span>건</h3><ul class="rqlist" id="rqList"></ul></div></section>')
def tail(t): return ROBO + wrap(pager(*t))

def stage_page(s, top_rows, content, intro_say):
    i = s['n']
    prev = ('stages.html', '전체 스테이지 및 FLOW') if i == 0 else (STAGES[i-1]['file'], f'S{i-1} {STAGES[i-1]["name"]}')
    nxt = (STAGES[i+1]['file'], f'S{i+1} {STAGES[i+1]["name"]}') if i < 6 else ('index.html', 'INDEX — 전체 연구 계획 정리')
    top = wrap(crumb(('index.html', 'INDEX'), ('stages.html', '스테이지·FLOW'), (None, f'S{i}')) +
               f'<h1 style="margin:4px 0 6px">S{i} · {s["name"]} {chip(s)}</h1>' + stage_head(s, top_rows) + intro_say)
    tl = tail((prev, nxt))
    return page(s['file'], f'S{i} {s["name"]}', top + content + tl)

sizes = {}
# S0
s = SBY['s0']
ask = sec('ask').replace('<h2>결정이 필요한 질문 10가지</h2>', '<h2>S0 · 결정이 필요한 질문 10가지</h2>').replace('검토 결과 정리에 함께 모입니다', 'INDEX의 검토 결과 정리에 함께 모입니다')
sizes[s['file']] = stage_page(s, [
    ('받은 자료 8가지 정리 (킥오프·계획서·데이터셋·강의자료 등)', '완료'),
    ('데이터 진단 — 원단 × 측정 묶음 채움 지도', '완료'),
    ('결정 질문 10개 정리', '완료'),
    ('연구책임자 미팅에서 질문 답 듣기', '진행 중'),
    ('데이터 사전, 변수 역할표(B·C·A·Y) 확정', '진행 중'),
    ('정답 Y(마찰전기 출력) 측정 시작일·수량', '예정'),
    ('과제 협약 기간 확정에 따른 일정 맞춤', '예정')],
    lv('lv1', 'S0 · 데이터 현황 — 무엇이 있고 무엇이 비었나', rev='s0') + ask,
    say('asst', 'report', '교수님, S0는 2026-11-16에 시작한 단계입니다. 2026-11-17에 1차년도 방향이 "직물 특성 → 실측 전기 특성 → 생성 → 예측"으로 정해져, 정답 Y는 이제 전기적 특성입니다.'))
# S1
s = SBY['s1']
sizes[s['file']] = stage_page(s, [
    ('공통 19항목으로 주성분 분석(PCA) — 파일럿 계산', '완료'),
    ('FTT와 KES-FB 순위 상관 — 파일럿 계산', '완료'),
    ('튀는 값 2건 원자료 대조', '예정'),
    ('27개 원단 정제본(단위 통일·결측 표시)', '예정'),
    ('상관·군집 분석, 핵심 후보 변수 10개 안팎', '예정')],
    lv('lv2', 'S1 · 탐색 분석 — 원단끼리 얼마나 닮았나 (M0)', rev='s1'),
    say('sia', 'explain', 'S1은 일부를 미리 계산해 두었습니다. 아래 그림은 실측 값이고, 정식 정제와 변수 선정은 12월에 시작합니다.'))
# S2
s = SBY['s2']
sizes[s['file']] = stage_page(s, [
    ('원단마다 기록할 8묶음 항목 (제안)', '설계안'),
    ('실험계획 요인·수준 (실 4 × 조직 3 × 밀도 3 × 계열 2, 제안)', '설계안'),
    ('측정 장비 통일 (FTT 또는 KES-FB)', '예정'),
    ('원단 제작 (디지털 편직·자카드 직기)', '예정'),
    ('전기적 특성(Y) 측정 장치·조건 표준화 — 접촉 모드·상대 물질·힘·주파수·온습도', '예정'),
    ('직물 특성(X) 항목 확정 — 1차년도는 수치 특성만, 이미지는 2차년도 이후', '설계안'),
    ('입력 양식과 자동 품질검사', '예정')],
    lv('lv3', 'S2 · 데이터 준비 — 원단마다 8묶음, 몇 개를 만들까', rev='s2'),
    say('moa', 'think', 'S2는 설계안까지 왔습니다. 바뀐 방향에서 S2가 가장 중요합니다. 전기 특성 실측값이 이후 모든 단계의 유일한 정답이기 때문입니다.'))
# S3
s = SBY['s3']
sizes[s['file']] = stage_page(s, [
    ('목표 변경: 직물 특성(X) → 전기 특성(Y) 회귀 (2026-11-17 방향)', '설계안'),
    ('모델 순서: 기준선 → 트리 앙상블 → 가우시안 과정(불확실도) → 신경망 (제안)', '설계안'),
    ('원단 단위 교차검증 원칙', '설계안'),
    ('평가 기준 13개와 합격선 (제안값)', '설계안'),
    ('실제 모델 학습 (S2 정답 데이터가 필요)', '예정'),
    ('경로 분석(PLS-SEM)과 변수 영향도(SHAP)', '예정'),
    ('새 원단 10개 이상 외부 검증', '예정')],
    lv('lv4', 'S3-1 · 모델링 — 작은 모델부터 단계적으로 (M1~M4)', drop_rev=True) + lv('lv5', 'S3-2 · 평가 기준 — 무엇을, 얼마면 합격인가', rev='s3'),
    say('asst', 'report', 'S3는 1차년도 방향에 따라 "직물 특성 → 전기 특성" 회귀로 목표를 바꿨습니다. 실측 정답으로 배우므로 이 단계는 지도학습입니다. 아래 두 실험은 원리를 보여 드리는 가상 데이터입니다. <a href="method_review.html">방법 검토</a>에 근거를 정리했습니다.'))

# S4~S6 예정 쪽
def plan_body(s, fixed, open_, link, sayx):
    h = f'<section class="level lv"><div class="wrap"><div class="lvhead"><span class="hexno">{s["n"]}</span><h2>S{s["n"]} · {s["name"]} — 정해진 것과 정해야 할 것</h2></div>'
    if s['st'] == 'plan':
        h += '<div class="planbox"><h4>아직 준비 전인 스테이지입니다 <span class="st plan">예정</span></h4><p class="small" style="margin:0">아래 "정해진 것"은 연구계획서·킥오프 문서에 적힌 내용입니다. "예정"은 담당·범위·날짜가 아직 정해지지 않은 항목입니다.</p></div>'
    else:
        h += '<div class="planbox"><h4>설계안 단계입니다 <span class="st draft">설계안</span></h4><p class="small" style="margin:0">2026-11-17에 정해진 1차년도 방향을 따른 설계안입니다. 근거 문헌은 <a href="method_review.html">1차년도 연구 방법 검토</a> 쪽에 있습니다. "정해야 할 것"은 교수님 검토 뒤 확정합니다.</p></div>'
    h += '<div class="yr"><h3>' + ('정해진 것 — 문서 근거' if s['st'] == 'plan' else '방향과 근거') + '</h3><ul>' + ''.join(f'<li>{x}</li>' for x in fixed) + '</ul></div>'
    h += '<div class="yr plan"><h3>정해야 할 것 <span class="st plan">예정</span></h3><ul>' + ''.join(f'<li>{x}</li>' for x in open_) + '</ul></div>'
    h += '<div class="yr"><h3>앞뒤 스테이지와의 연결</h3><ul>' + ''.join(f'<li>{x}</li>' for x in link) + '</ul></div>'
    h += '<div class="talk"><p class="th">질의응답</p>' + sayx + '</div>'
    h += f'<div class="review" id="review-{s["k"]}" data-rev="{s["k"]}"></div></div></section>'
    return h

s = SBY['s4']
sizes[s['file']] = stage_page(s, [('생성 대상: 직물 특성 X (전기 특성 Y는 만들지 않음, 제안)', '설계안'), ('생성 방식 비교: 실험계획 격자 · 가우시안 혼합·코퓰라 · CTGAN/TVAE', '설계안'), ('품질 검사: 분포 비교 · 범위 밖 차단 · 만들 수 있는지 실험실 확인', '설계안'), ('시뮬레이션(TexGen·Abaqus) 보조 경로', '예정'), ('실제 생성·검사', '예정')],
    plan_body(s, ['1차년도 방향(2026-11-17): 실측 데이터를 근거로 데이터를 생성하고, 생성한 직물의 전기 특성을 예측합니다.',
                  '제안: 생성하는 것은 "가상 직물의 특성 X"입니다. 전기 특성 Y까지 만들어 다시 학습에 넣으면 같은 정보가 되풀이됩니다. 생성 데이터를 거듭 학습한 모델이 원래 분포의 꼬리를 잃는 현상(model collapse)도 보고되었습니다 <a href="method_review.html#risk">[방법 검토]</a>.',
                  '소표본 재료 연구에서는 이 작업을 가상 샘플 생성(VSG)이라 부르며, 실험으로 확인하기 전의 가상 샘플은 "미지 샘플"로 취급합니다 <a href="method_review.html#lit">[방법 검토]</a>.',
                  '연구계획서의 TexGen → Abaqus 시뮬레이션은 실측과 독립된 물리 정보를 주므로 보조 경로로 둡니다 [4].'],
              ['생성 범위 — 실측 원단의 범위 안으로 제한할지, 실험실이 만들 수 있는 범위까지 넓힐지', '생성 방식 — 표 데이터 생성 모델을 쓸지, 실험계획 격자처럼 규칙으로 만들지', '시뮬레이션 담당·계산 환경', '생성 직물 수 — 예측·선별용 수천 개, 검증용 소수'],
              ['앞: S2 실측 분포와 S3 회귀 모델의 적용 범위가 생성 범위의 기준입니다.', '뒤: S5가 생성 직물의 전기 특성을 예측하고 일부를 실제로 검증합니다.'],
              say('sia', 'think', '생성한 데이터로 모델을 다시 학습하면 정확도가 오르지 않습니까?') + say('asst', 'report', '실측에 없는 새 정보가 들어오지 않으면 오르지 않습니다. 그래서 생성 데이터를 쓴 모델의 점수는 반드시 실측 원단으로만 재겠습니다(TSTR). 비교 모의실험은 <a href="method_review.html#sim">방법 검토</a>에 있습니다.')),
    say('asst', 'report', 'S4는 2026-11-17 방향에 따라 "실측 기반 데이터 생성"으로 바꿨습니다. 1차년도 안에서 진행합니다.'))
s = SBY['s5']
sizes[s['file']] = stage_page(s, [('예측 대상: 생성 직물의 전기 특성 (정답 없음)', '설계안'), ('불확실도 함께 보고 (앙상블·가우시안 과정)', '설계안'), ('전향 검증: 생성 직물 일부를 실제 제작·측정', '설계안'), ('검증 원단 선택 규칙 (예측 최고 + 불확실도 최고)', '예정'), ('주 정답 지표·측정 조건 (S2와 같게)', '예정')],
    plan_body(s, ['생성 직물에는 정답이 없습니다. 그래서 이 단계의 예측은 실제로 만들어 재기 전까지 "검증되지 않은 예측"입니다 <a href="method_review.html#type">[방법 검토]</a>.',
                  '정답 없는 예측을 믿을 수 있게 하는 장치: ① 실측 원단 교차검증 성적, ② 예측마다 불확실도, ③ 물리 방향 검사(접촉 면적·거칠기가 크면 출력이 큰 경향 등), ④ 일부를 실제 제작해 맞춰 보는 전향 검증.',
                  '전향 검증 원단을 고를 때 불확실도가 큰 후보를 섞으면, 측정 한 번으로 모델이 가장 많이 배우는 능동 학습(active learning)이 됩니다 <a href="method_review.html#lit">[방법 검토]</a>.'],
              ['검증용으로 실제 만들 생성 직물 수 (제안: 10개 이상)', '선정 규칙 — 예측 최고 몇 개, 불확실도 최고 몇 개', '전기 특성 주 지표 — 전압·전류·전하밀도 중 무엇', '검증 측정 뒤 모델을 다시 학습할지(반복 횟수)'],
              ['앞: S4 생성 직물과 S3 회귀 모델을 씁니다.', '뒤: 검증된 결과는 2차년도 센서 구조·이미지 결합 모델의 출발점입니다.'],
              say('moa', 'think', '정답이 없는데 맞았는지 어떻게 압니까?') + say('asst', 'report', '모두는 알 수 없습니다. 그래서 일부를 실제로 만들어 재고, 그 결과로 나머지 예측을 얼마나 믿을지 정하겠습니다.')),
    say('asst', 'report', 'S5는 2026-11-17 방향의 마지막 단계입니다. 1차년도 안에서 진행하는 안을 제안합니다.'))
s = SBY['s6']
sizes[s['file']] = stage_page(s, [('목적: 핵심 변수를 정확하고 쉽게 재는 장치 (킥오프 문서)', '설계안'), ('담당·제작처', '예정'), ('개선 목표 우선순위', '예정'), ('특허 선행조사 범위', '예정')],
    plan_body(s, ['킥오프 문서는 핵심 변수를 정확히 잴 수 있도록 측정 장치를 개선하고 특허로 이어 가는 과제를 적었습니다 [2].',
                  'S1·S3에서 고른 핵심 변수가 장치 개선의 대상이 됩니다.'],
              ['장치 설계·제작을 맡을 사람과 제작처', '측정 정확도와 측정 용이성 중 무엇을 먼저 올릴지', '마찰전기 측정 장치 관련 선행 특허 조사 범위', '연차 배정 — 계획서 연차표에는 별도 항목이 없어 배정이 예정입니다'],
              ['앞: S3 변수 영향도에서 "가장 중요한데 측정이 흔들리는 변수"를 고릅니다.', '뒤: 개선한 장치로 S5 외부 검증 원단을 측정하는 안을 제안합니다.'],
              say('sia', 'think', '장치 개선은 언제 시작합니까?') + say('asst', 'report', '핵심 변수가 정해져야 시작할 수 있어, 날짜는 예정으로 두었습니다.')),
    say('asst', 'report', 'S6은 예정 단계입니다. 정해진 범위만 정리했습니다.'))

# ---------------- 전체 스테이지 및 FLOW ----------------
flow = sec('flow').replace('<h2>전체 흐름 — 한 장으로 보는 흐름도</h2>', '<h2>연구 흐름도 — 한 장으로 보기</h2>')
plan = sec('plan')
plan = re.sub(r'<details><summary>연구계획서의 5년 큰 그림 펼치기</summary>.*?</details>', '<p class="small">점선 막대는 <span class="st plan">예정</span> 스테이지입니다. 5년 전체는 <a href="plan_years.html">연차별 연구계획</a>에 있습니다.</p>', plan, flags=re.S)
plan = plan.replace('세로 점선은 오늘(2026-11-14)입니다.', '세로 점선은 오늘(2026-11-17)입니다.')
cards = '<div class="mapc">' + ''.join(
    f'<a class="card{" plan" if s["st"]=="plan" else ""}" href="{s["file"]}"><span>S{s["n"]} {chip(s)}</span><b>{s["name"]}</b><span class="d">{s["d"]}<br>{s["per"]}<br>관문: {s["gate"]}</span></a>' for s in STAGES) + '</div>'
legend = '<p class="small">상태 표시: <span class="st done">완료</span> <span class="st run">진행 중</span> <span class="st part">일부 완료</span> <span class="st draft">설계안</span> <span class="st plan">예정</span> — 예정은 담당·범위·날짜가 아직 정해지지 않았다는 뜻입니다.</p>'
st_top = wrap(crumb(('index.html', 'INDEX'), (None, '전체 연구 스테이지 및 FLOW')) +
    '<h1 style="margin:4px 0 8px">전체 연구 스테이지 및 FLOW</h1><p class="lead">2026-11부터 2027-12까지 7개 스테이지(S0~S6)로 진행합니다. S0~S5는 1차년도 방향(직물 특성 → 실측 전기 특성 → 생성 → 예측)을 따르고, S6은 아직 <span class="st plan">예정</span>입니다. 카드를 누르면 스테이지 쪽으로 들어갑니다.</p>' + legend + cards +
    say('asst', 'report', '교수님, 스테이지는 흐름도의 단계를 묶은 것입니다. 흐름도 상자나 일정 막대를 누르셔도 해당 스테이지 쪽으로 가실 수 있습니다.'))
sizes['stages.html'] = page('stages.html', '전체 연구 스테이지 및 FLOW', st_top + flow + plan + tail((('plan_years.html', '연차별 연구계획'), (STAGES[0]['file'], 'S0 착수·자료 정리'))))

# ---------------- 연차별 연구계획 ----------------
DIRBOX = ('<div class="brief" id="dir1117"><div class="bh">1차년도 진행 방향 — 2026-11-17 확정</div><dl>'
  '<dt>입력 X</dt><dd>섬유직물의 주요 특성 (실·조직·밀도·두께·평량·표면·압축·굽힘 등 수치)</dd>'
  '<dt>출력 Y</dt><dd>섬유직물의 전기적 특성 — 실제로 계측 (마찰전기 전압·전류·전하밀도)</dd>'
  '<dt>생성</dt><dd>실측 데이터를 근거로 가상 직물 데이터를 만듦</dd>'
  '<dt>예측</dt><dd>회귀 모델로 생성 직물의 전기 특성을 예측 — 생성 직물에는 실제 정답이 없음</dd>'
  '<dt>이미지</dt><dd>섬유 이미지는 2차년도 이후 활용</dd>'
  '<dt class="ask">검토</dt><dd>이 방법이 지도·비지도 중 어디에 가까운지, 문헌으로 본 위험과 검증 방법은 <a href="method_review.html">1차년도 연구 방법 검토</a>에 정리했습니다.</dd></dl></div>')
YEARS = [
 ('1차년도', '2026 (계획서 기재) · 방향 2026-11-17 확정', 'run', '진행 중', '직물 주요 특성 → 실측 전기적 특성 → 실측 근거 데이터 생성 → 생성 직물의 전기 특성 회귀 예측',
  ['직물 주요 특성(X: 실·조직·밀도·두께·평량·표면·압축·굽힘 등) 측정과 DB 구축', '같은 원단의 전기적 특성(Y: 마찰전기 전압·전류·전하밀도) 실측 — 측정 조건 표준화', '실측 원단으로 X → Y 회귀 모델 (기준선 → 트리 앙상블 → 가우시안 과정)', '실측 분포를 근거로 가상 직물 데이터 생성 (시뮬레이션은 보조 경로)', '생성 직물의 전기 특성 예측과 불확실도, 일부를 실제 제작해 전향 검증', '이미지 데이터는 2차년도 이후 활용 — 1차년도는 수치 특성만'],
  ['전기 특성 반복 측정의 재현성 (변동계수)', '실측 원단 단위 교차검증 R²·RMSE, 기준선 대비 개선', '생성 데이터 품질 (분포·범위·물리 방향 검사)', '생성 직물 일부의 실제 제작·측정으로 예측 확인'], 'S0 S1 S2 S3 S4 S5',
  '계획서 원안: 구조·물성 DB와 동적 마찰 예측 기초 모델 (마찰전기 예측은 2차년도). 2026-11-17 방향으로 전기 특성 실측·예측을 1차년도로 당겼습니다.'),
 ('2차년도', '2027 (계획서 기재) · 조정안', 'draft', '계획', '이미지 결합과 마찰전기 센서 성능 예측 고도화 (Structure-to-Performance)',
  ['섬유·직물 이미지 특징을 수치 특성과 결합 (이미지 140장 진단 결과 반영)', '직물 마찰전기 센서 후보 구조 설계·제작, 온도·습도·접촉 조건별 전기 특성 측정', 'Sim-to-Real 보정 — 시뮬레이션 합성 데이터와 실측 정합', '1차년도 회귀 모델을 센서 구조로 넓히고 초기 센서로 보정'],
  ['합성 데이터와 실측 데이터의 정합도', '감도·출력·선형성 예측 정확도 (R², RMSE)', '이미지 추가 전후 예측 성능 비교', '보정 전후 예측 성능 비교'], 'S6',
  '계획서 원안의 2차년도 목표(마찰전기 센서 성능 예측)는 유지하되, 1차년도 결과 위에 이미지와 센서 구조를 더하는 조정안입니다.'),
 ('3차년도', '2028 (예정)', 'plan', '예정', '옷에 넣었을 때의 성능 재예측 (Wearable-aware)',
  ['착용형 플랫폼(상의·하의·장갑 등) 선정, 센서 의복 통합', '동작별 변형 분포(strain map) 수집, 패턴·봉제선별 변형 분석', '착용 환경 변수를 더한 재예측 모델 (시계열 모델 전이학습)'],
  ['착용 환경 요인 분석의 정량성', 'strain map 데이터 완성도', '착용 환경 반영 후 예측 정확도 향상 여부'], '스테이지 설계 예정', ''),
 ('4차년도', '2029 (예정)', 'plan', '예정', '여러 센서로 인체 동작 인식',
  ['멀티센서 의복형 시스템 설계·제작과 착용성 시험', '보행·균형·상지·체간 동작 데이터 수집과 지표 구축', '센서 수·배치·감도 조합 ablation으로 최적 구성 도출'],
  ['동작 분류 정확도 90% 이상', '최소 센서 구성으로 성능 90% 이상 유지', '센서 수·위치 대 성능 변화 곡선 제시'], '스테이지 설계 예정', ''),
 ('5차년도', '2030 (예정)', 'plan', '예정', '개인정보 보호형 온디바이스 플랫폼',
  ['모델 경량화와 스마트 기기 탑재, 비식별화·암호화', '반복 변형·세탁·땀·온습도 내구성 평가', '사용성 평가와 통합 플랫폼, 응용 분야 검토'],
  ['모델 80% 이상 경량화에 성능 95% 유지', '세탁 10~20회 후 출력 80% 이상 유지', '착용자 평가 5점 척도 평균 4점 이상, 유효 데이터 획득률 90% 이상'], '스테이지 설계 예정', ''),
]
yh = ''
for nm, when, cl, lb, goal, cont, crit, stg, note in YEARS:
    links = ' '.join(f'<a href="{SBY["s"+t[1]]["file"]}">{t}</a>' if t.startswith('S') and t[1].isdigit() else t for t in stg.split(' ')) if stg.startswith('S') else f'<span class="st plan">{stg}</span>'
    h1, h2 = ('연구 내용 (2026-11-17 방향)', '평가 착안점 (제안)') if note else ('연구 내용 (계획서 요약)', '평가 착안점 (계획서 기재)')
    yh += f'<div class="yr{" plan" if cl=="plan" else ""}"><h3>{nm} <span class="small muted">{when}</span> <span class="st {cl}">{lb}</span></h3><p style="margin:0"><b>목표</b> — {goal}</p>' + (f'<p class="small muted" style="margin:6px 0 0">{note}</p>' if note else '') + f'<div class="cols"><div><h4>{h1}</h4><ul>' + ''.join(f'<li>{x}</li>' for x in cont) + f'</ul></div><div><h4>{h2}</h4><ul>' + ''.join(f'<li>{x}</li>' for x in crit) + f'</ul></div></div><p class="small" style="margin:10px 0 0"><b>연결 스테이지</b> — {links}</p></div>'
yrs = wrap(crumb(('index.html', 'INDEX'), (None, '연차별 연구계획')) +
    '<h1 style="margin:4px 0 8px">연차별 연구계획 — 5년 로드맵</h1><p class="lead">연구계획서(2026년도 핵심연구 유형B)의 5년 계획을 연차별로 정리했습니다. 1차년도는 2026-11-17에 정한 방향으로 고쳤고, 3~5차년도는 <span class="st plan">예정</span>입니다.</p>' + DIRBOX +
    '<div class="planbox"><h4>날짜에 대한 알림 <span class="st plan">예정</span></h4><p class="small" style="margin:0">계획서는 1차년도를 2026년으로 적었지만, 이 브리핑의 스테이지 일정은 2026-11 ~ 2027-12입니다. 과제 협약 시작일이 정해지면 연차 경계를 다시 맞추겠습니다(결정 질문 1번).</p></div>' +
    say('asst', 'report', '교수님, 연차마다 목표, 연구 내용, 계획서의 평가 착안점, 연결 스테이지 순서로 보고드립니다.') + yh +
    '<h3>연구 가설과 연차 (1차년도 방향 반영)</h3><div class="tw"><table class="tb"><tr><th>가설</th><th>내용 (요약)</th><th>주로 검증하는 연차</th></tr>'
    '<tr><td>1</td><td>직물 주요 특성으로 전기적(마찰전기) 특성을 회귀 예측할 수 있다 <span class="st draft">변경</span></td><td>1차 (S2·S3)</td></tr>'
    '<tr><td>1-2</td><td>실측 근거로 생성한 가상 직물의 전기 특성을 예측할 수 있고, 그 예측은 일부 실제 제작·측정으로 확인된다 <span class="st draft">추가</span></td><td>1차 (S4·S5)</td></tr>'
    '<tr><td>2</td><td>이미지·합성·실측 데이터를 합치면 마찰전기 센서 성능 예측이 온습도 조건에서도 일반화된다</td><td>2차</td></tr>'
    '<tr><td>3</td><td>옷의 패턴·봉제·인체 변형이 센서 성능에 비선형으로 영향을 주며, 이를 모델링해 재예측할 수 있다</td><td>3차 (예정)</td></tr>'
    '<tr><td>4</td><td>센서 수·배치·감도를 최적화하면 적은 센서로 높은 동작 인식 성능을 낸다</td><td>4차 (예정)</td></tr>'
    '<tr><td>5</td><td>온디바이스 처리·비식별화·암호화로 개인정보를 지키며 실사용 신뢰성을 높인다</td><td>5차 (예정)</td></tr></table></div>') + tail((('index.html', 'INDEX — 전체 연구 계획 정리'), ('stages.html', '전체 연구 스테이지 및 FLOW')))
sizes['plan_years.html'] = page('plan_years.html', '연차별 연구계획', yrs)

# ---------------- INDEX ----------------
hero = T[T.index('<header class="hero">'):T.index('<section class="level" id="intro">')]
hero = hero.replace('2026-11-14 기준', '2026-11-17 기준').replace('한양대 섬유 AI 과제 · 연구 계획 브리핑 01', '한양대 스마트텍스타일연구실 · 연구 계획 브리핑 01').replace('</h1>', '</h1>'+'<div class="labcard" role="note" aria-label="PM 연구실"><span class="lk">PM</span><b class="ln">한양대학교 생활과학대학 의류학과 · 스마트텍스타일연구실</b><span class="lp">담당 교수 <b>배지현 교수</b></span><span class="lf">연구 분야: 스마트섬유소재 · 섬유기반소자 · 섬유구조설계 · 지속가능성 소재 및 공정</span><a class="bt primary" href="https://fashion.hanyang.ac.kr/-19" target="_blank" rel="noopener">연구실 소개 페이지 열기 ↗</a></div>', 1).replace('보고마다 결론을 먼저 말씀드리고, 끝에 교수님 검토가 필요한 사항을 정리했습니다. 그림은 직접 눌러 확인하실 수 있습니다.',
    '이 쪽은 전체 계획의 요약입니다. 연차별 계획, 스테이지 흐름, 스테이지별 상세 쪽으로 이어집니다. 아직 정해지지 않은 것은 <span class="st plan">예정</span>으로 표시했습니다.')
hero = hero.replace('보고마다 검토 사항을 정리해 두었습니다. 표시해 주시면 마지막에 모아 드리겠습니다.', '스테이지마다 검토 사항이 있습니다. 표시해 주시면 이 쪽 아래에 모아 드리겠습니다.')
intro = re.sub(r'<h3 style="margin-top:22px">오늘 보고 순서</h3>\s*<ol class="agenda">.*?</ol>', '', INTRO, flags=re.S)
docmap = (DIRBOX + '<h2 id="map" style="margin-top:30px">문서 지도 — 어디부터 보시면 되나</h2><div class="mapc">'
    '<a class="card" href="method_review.html"><span>★</span><b>1차년도 연구 방법 검토 (문헌)</b><span class="d">직물 특성 → 실측 전기 특성 → 생성 → 예측. 지도·비지도 구분, 위험, 검증 방법, 모의실험.</span></a>'
    '<a class="card" href="#ai-summary"><span>0</span><b>SUMMARY — 사진이 벡터가 되기까지</b><span class="d">이미지는 2차년도 이후 활용. 원단 사진 → 확대 → 숫자 → 벡터, 딥러닝이 사진을 나누는 방법.</span></a>'
    '<a class="card" href="plan_years.html"><span>1</span><b>연차별 연구계획</b><span class="d">5년 로드맵. 연차마다 목표·내용·평가 착안점. 3~5차년도는 예정.</span></a>'
    '<a class="card" href="stages.html"><span>2</span><b>전체 연구 스테이지 및 FLOW</b><span class="d">흐름도와 일정 막대, 7개 스테이지 카드.</span></a>'
    '<a class="card" href="stage_0_kickoff.html"><span>3</span><b>스테이지별 상세 (S0~S6)</b><span class="d">S0 데이터 현황·결정 질문부터. 스테이지마다 검토 사항.</span></a>'
    '<a class="card" href="image_data.html"><span>4</span><b>섬유 이미지 데이터 리뷰·분석</b><span class="d">2차년도 이후 활용 예정. 실습용 이미지 140장 진단과 보완사항.</span></a>'
    '<a class="card" href="data_guide.html"><span>5</span><b>가상 섬유 데이터 작성 가이드</b><span class="d">합성 표·시뮬레이션·생성 이미지 기록 양식과 점검표.</span></a>'
    '<a class="card" href="references.html"><span>6</span><b>참고 레퍼런스</b><span class="d">장비·마찰전기·시뮬레이션·데이터 품질 문헌.</span></a></div>'
    '<div class="stgrid" role="list">' + ''.join(f'<a role="listitem" class="{"plan" if s["st"]=="plan" else ""}" href="{s["file"]}"><b>S{s["n"]}</b>{s["name"]}<br>{chip(s)}</a>' for s in STAGES) + '</div>')
stt = '<h2 id="status" style="margin-top:30px">스테이지 현황 — 2026-11-17 기준</h2><div class="tw"><table class="tb"><tr><th>스테이지</th><th>상태</th><th>기간</th><th>관문</th><th>연차</th></tr>' + ''.join(
    f'<tr><td><a href="{s["file"]}">S{s["n"]} {s["name"]}</a></td><td>{chip(s)}</td><td>{s["per"]}</td><td>{s["gate"]}</td><td>{s["yr"].split(" · ")[0]}</td></tr>' for s in STAGES) + '</table></div>'
intro = intro.replace('<h2 id="cast"', docmap + stt + '<h2 id="cast"')
review = sec('review').replace('<h2>검토 결과 정리</h2>', '<h2>검토 결과 정리 — 모든 스테이지</h2>').replace(
    '보고마다 표시해 주신 검토 결과와 의견 메모를 한데 모았습니다. 복사해서 회의록에 붙이실 수 있습니다. 표시는 이 화면에만 남고 저장되지 않습니다.',
    '스테이지 쪽에서 표시해 주신 검토 결과와 의견 메모를 한데 모았습니다. 표시는 이 브라우저에만 남고 서버에는 저장되지 않습니다. 복사해서 회의록에 붙이실 수 있습니다.')
review = review.replace('<div class="ctrl"><button class="bt primary" id="revCopy">검토 결과 복사</button>',
    '<p class="small">답을 들은 결정 질문: <b class="num" id="revQ">0 / 10</b> · <a href="stage_0_kickoff.html#ask">S0에서 표시하기</a></p><div class="ctrl"><button class="bt primary" id="revCopy">검토 결과 복사</button><button class="bt" id="revClear">표시 모두 지우기</button>')
summary = sec('summary')
summary = summary.replace('<h2>보고 요약 — 다섯 보고를 한 표로</h2>', '<h2>보고 요약 — 스테이지별 한 줄</h2>')
for a, b in [('<td>① 데이터 현황</td>', '<td><a href="stage_0_kickoff.html">S0</a> 데이터 현황</td>'), ('<td>② 탐색 분석</td>', '<td><a href="stage_1_explore.html">S1</a> 탐색 분석</td>'),
             ('<td>③ 데이터 준비</td>', '<td><a href="stage_2_data.html">S2</a> 데이터 준비</td>'), ('<td>④ 모델링</td>', '<td><a href="stage_3_model.html">S3</a> 모델링</td>'), ('<td>⑤ 평가 기준</td>', '<td><a href="stage_3_model.html#lv5">S3</a> 평가 기준</td>')]:
    assert a in summary; summary = summary.replace(a, b)
summary = summary.replace('</table></div>', '<tr><td><a href="stage_4_sim2real.html">S4</a>~<a href="stage_6_device.html">S6</a></td><td>Sim-to-Real, 마찰전기 예측, 장치 개선</td><td><span class="st plan">예정</span></td><td>담당·범위 확정 뒤 다시 보고</td></tr></table></div>', 1)
outro = sec('outro').replace('검토 결과는 위 표에 모아 두었습니다.', '검토 결과는 위 표에 스테이지별로 모아 두었습니다.')
REQS = ('<section class="level" id="reqs"><div class="wrap"><h2>부직이 요청 모음 — 모든 쪽</h2>'
  '<p class="lead">각 쪽에서 남기신 수정·보완 요청을 한곳에 모았습니다. 기한 순으로 정렬되며, 반영하면 상태를 눌러 바꿉니다. 요청서는 복사하거나 .md·.csv로 내려받을 수 있습니다.</p>'
  '<div class="say" data-who="robo"><img class="who" id="roboFace2" data-who="robo" data-mood="chart" alt="" aria-hidden="true"><div class="bub"><b class="name">부직이</b><p id="reqSay">아직 접수된 요청이 없습니다.</p></div></div>'
  '<div class="kpis" id="reqK"></div>'
  '<div class="ctrl"><div class="group" role="group" aria-label="요청 거르기"><button type="button" class="bt" data-rf="open" aria-pressed="true">남은 요청</button><button type="button" class="bt" data-rf="done" aria-pressed="false">반영 완료</button><button type="button" class="bt" data-rf="all" aria-pressed="false">전체</button></div></div>'
  '<div class="tw" id="reqT"></div>'
  '<div class="ctrl"><button type="button" class="bt primary" id="reqCopy">요청서 복사</button><button type="button" class="bt" id="reqMd">요청서 .md 내려받기</button><button type="button" class="bt" id="reqCsv">표 .csv 내려받기</button><span class="small muted" id="reqMsg" aria-live="polite"></span></div>'
  '<p class="small muted dlnote" aria-live="polite"></p><pre class="cite" id="reqTxt" hidden></pre></div></section>')
SUMHTML = ('<section class="level" id="ai-summary"><div class="wrap"><h2>SUMMARY — 원단 사진이 AI 안에서 숫자(벡터)가 되기까지</h2>'
 '<div class="planbox"><h4>이미지 활용은 2차년도 이후 <span class="st plan">예정</span></h4><p class="small" style="margin:0">2026-11-17 방향에 따라 1차년도는 수치로 잰 직물 특성으로 전기 특성을 예측합니다. 아래 SUMMARY는 2차년도 이후 이미지를 더할 때의 원리를 미리 정리한 것입니다.</p></div><p class="lead">"AI가 원단을 보고 촉감을 맞힌다"는 말이 처음엔 막연합니다. 원단 사진 한 장이 <b>섬유(직물) → 직물 확대 → 확대 모습 → 벡터</b>로 바뀌는 과정과, 딥러닝 모델이 그 사진을 어떻게 벡터로 나누는지 그림으로 보여 드립니다. 아래 그림은 실습용 원단 사진으로 화면에서 직접 계산합니다.</p>'
 + say('sia', 'think', 'AI는 원단 사진을 어떻게 알아봅니까? 사람처럼 "거칠다"고 느끼는 겁니까?')
 + say('asst', 'report', '느끼지 않습니다. 사진을 숫자로 바꾸고, 그 숫자에서 패턴을 계산합니다. 원단을 고르고 사진에서 확대할 곳을 눌러 보십시오.')
 + '<div class="panel"><h4>1부 · 사진 한 장이 벡터가 되는 4단계 <span class="realnote">실제 사진으로 계산</span></h4>'
 '<div class="ctrl"><div class="group" role="group" aria-label="원단 고르기" id="smPick"></div></div>'
 '<div class="ctrl"><div class="group"><span class="glabel">확대 위치</span><button type="button" class="bt sm" data-smv="l" aria-label="왼쪽으로">←</button><button type="button" class="bt sm" data-smv="u" aria-label="위로">↑</button><button type="button" class="bt sm" data-smv="d" aria-label="아래로">↓</button><button type="button" class="bt sm" data-smv="r" aria-label="오른쪽으로">→</button></div>'
 '<div class="group"><span class="glabel">확대 배율</span><input type="range" id="smZoom" min="10" max="40" step="2" value="20" aria-label="확대 배율"><span class="val" id="smZoomV">5배</span></div></div>'
 '<div class="sm4">'
 '<div class="st4"><h5><i>1</i>섬유(직물) 원단</h5><canvas id="smA" width="240" height="240" aria-label="원단 사진. 누르면 확대할 위치를 고릅니다"></canvas><p>원단 전체를 찍은 사진입니다. 노란 네모를 누른 곳으로 옮길 수 있습니다.</p></div>'
 '<div class="st4"><h5><i>2</i>직물 확대</h5><canvas id="smB" width="240" height="240" aria-label="노란 네모 부분 확대"></canvas><p>노란 네모 안을 크게 본 모습입니다. 실이 지나가는 결과 교차점이 보입니다.</p></div>'
 '<div class="st4"><h5><i>3</i>확대 모습 = 숫자 격자</h5><canvas id="smC" width="240" height="240" aria-label="8 곱하기 8 밝기 격자"></canvas><p>확대한 곳을 8 × 8칸으로 나누고 칸마다 밝기를 0(검정)~1(흰색) 숫자로 적습니다.</p></div>'
 '<div class="st4"><h5><i>4</i>벡터로 분해</h5><div class="vtxt" id="smVecTxt"></div><canvas id="smD" width="240" height="120" aria-label="64개 숫자 막대"></canvas><p>격자를 한 줄로 펼치면 숫자 64개짜리 목록, 곧 <b>벡터</b>가 됩니다. 막대 하나가 숫자 하나입니다.</p></div>'
 '</div>'
 + say('robo', 'calc', '<span id="smSay">계산 중입니다.</span>')
 + '</div>'
 '<div class="panel"><h4>2부 · 딥러닝 모델은 이 사진을 어떻게 벡터로 나누나 <span class="realnote">1층은 실제 계산 · 2~3층은 개념도</span></h4>'
 '<p class="small">딥러닝 이미지 모델(합성곱 신경망, CNN)은 작은 "돋보기 필터"를 사진 위로 밀며 무늬를 찾습니다. 아래 1층 필터 4개는 학습된 필터를 흉내 낸 예시이고, 위 1부에서 고른 곳에 실제로 적용한 결과입니다.</p>'
 '<div class="nnflow">'
 '<div><h5>입력</h5><canvas id="smIn" width="160" height="160" aria-label="입력 밝기 격자 40 곱하기 40"></canvas><p class="small" style="margin:6px 0 0">확대한 곳 40 × 40 = 숫자 1,600개</p></div>'
 '<div><h5>1층 · 결 찾기 필터</h5><div class="fm">'
 + ''.join(f'<figure><canvas id="smF{j}" width="120" height="120" aria-label="{n} 필터 반응"></canvas><figcaption>{n}</figcaption></figure>' for j, n in enumerate(['가로결', '세로결', '사선결 ↗', '사선결 ↘']))
 + '</div><p class="small" style="margin:6px 0 0">색이 진한 곳 = 그 방향의 결이 강한 곳</p></div>'
 '<div class="concept"><h5>2층 · 결의 조합</h5>가로결 + 세로결이 만나는 곳 → <b>실 교차점</b>, 둥근 반응 → <b>편직 고리</b>, 작은 덩어리 → <b>보풀</b></div>'
 '<div class="concept"><h5>3층 · 조직 무늬</h5>교차점이 사선으로 늘어서면 <b>능직</b>, 세로 골이 반복되면 <b>리브</b>처럼 원단 전체의 짜임을 알아봅니다.</div>'
 '<div><h5>요약 → 특징 벡터</h5><div id="smVec"></div><p class="small" style="margin:6px 0 0">필터 반응을 평균 내 숫자 몇 개로 줄입니다. 결 막대 4개는 가장 강한 결을 꽉 차게 그려 방향을 비교합니다. 여기서는 6개, 실제 모델은 수백 개입니다.</p></div>'
 '<div class="concept"><h5>예측 <span class="st plan">예정</span></h5>특징 벡터 + 구조·물성 값 → <b>태 점수</b>, <b>마찰전기 출력</b>. 정답(Y)을 측정한 뒤 학습합니다(2차년도 이후).</div>'
 '</div></div>'
 '<div class="panel"><h4>3부 · 벡터로 원단끼리 비교하기 <span class="realnote">실제 사진으로 계산</span></h4>'
 '<p class="small">원단 5장 각각의 사진 전체를 같은 방법으로 6개 숫자(특징 벡터)로 바꿨습니다. 벡터끼리 거리가 짧을수록 AI 눈에는 비슷한 원단입니다.</p><div class="tw" id="smTab"></div></div>'
 '<div class="talk"><p class="th">질의응답</p>'
 + say('moa', 'think', '그럼 이 벡터만 있으면 촉감을 맞힐 수 있습니까?')
 + say('asst', 'report', '아직은 아닙니다. 벡터는 "사진이 어떻게 생겼나"까지만 담습니다. 이 벡터와 실제로 잰 촉감·마찰전기 값을 짝지어 학습해야 예측이 됩니다. 그래서 S2에서 전기 특성 실측이 먼저이고, 이미지는 2차년도 이후에 더합니다.')
 + say('robo', 'meh', '주의할 점 하나. 벡터가 사진의 흐림·밝기만 담으면 AI가 엉뚱한 지름길을 배웁니다. <a href="image_data.html">이미지 데이터 분석</a>에 계산해 두었습니다.')
 + '</div><p class="small muted">벡터: 숫자를 순서대로 늘어놓은 목록. 합성곱 신경망(CNN): 작은 필터를 사진 위로 밀며 무늬를 찾는 딥러닝 모델. 2·3층 설명은 일반적인 CNN의 동작을 쉽게 풀어 쓴 개념도입니다.</p></div></section>')
kgs, exs = sec('kg'), sec('export')
idx = COVER + hero + SUMHTML + intro + summary + review + REQS + outro + kgs + exs + tail((None, ('plan_years.html', '연차별 연구계획')))
SMI = json.load(open(os.path.join(B, '..', 'analysis', 'summary', 'summary_imgs.json'), encoding='utf-8'))
sizes['index.html'] = page('index.html', 'INDEX — 전체 연구 계획 정리', idx, kg=True, extra={'sm': SMI})
exec(open(f'{B}/pages_method.py', encoding='utf-8').read())
exec(open(f'{B}/pages_extra.py', encoding='utf-8').read())
for k, v in sizes.items(): print(k, round(v / 1024), 'KB')
