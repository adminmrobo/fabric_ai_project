import json, re, base64, os, sys, copy
B = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, B)
import kg as K
PACK = os.environ.get('LAB_CHAR_PACK', os.path.join(B, '..', '..', 'ahnboat_lab_explainer', 'packs', 'character', 'character_pack'))
OUT = os.environ.get('LAB_OUT', os.path.join(B, '..'))
os.makedirs(OUT, exist_ok=True)
T = open(f'{B}/template.html', encoding='utf-8').read()
JS0 = open(f'{B}/assets_lab.js', encoding='utf-8').read()
RJ = open(f'{B}/assets_robo.js', encoding='utf-8').read()
i = JS0.index('/* ---------- 그리기 시작')
JS = JS0[:i] + RJ + JS0[i:]
SIMS = open(f'{B}/sims.js', encoding='utf-8').read()
DATA = json.load(open(f'{B}/data.json'))
emap = json.load(open(f'{PACK}/expression_map.json'))

def js(o): return json.dumps(o, ensure_ascii=False).replace('</', '<\\/')
def sec(id_):
    m = re.search(r'(<section class="level[^"]*" id="%s">.*?</div></section>)' % id_, T, re.S)
    return m.group(1)

HEAD = T[:T.index('</style>')]
FOOT = T[T.index('<footer>'):T.index('<div id="tip"')]
COVER = T[T.index('<div class="cover" id="top">'):T.index('<header class="hero">')]
INTRO = sec('intro')

EXTRA_CSS = r"""
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
 dict(k='s0', n=0, file='stage_0_kickoff.html', name='착수·자료 정리', st='run', stl='진행 중', per='2026-11-16 ~ 2026-11-30', own='AI 분석 쪽 (조수 하루, 인턴 시아·모아)', gate='G1 — 변수와 정답(Y)의 정의 합의 (2026-11-30)', out='데이터 사전, 변수 역할표(B·C·A·Y), 결정 질문 10개의 답', yr='1차년도 · 실/직물 구조 DB 구축', d='받은 자료 8가지를 정리하고, 무엇이 있고 무엇이 비었는지 진단합니다.'),
 dict(k='s1', n=1, file='stage_1_explore.html', name='파일럿 탐색 분석', st='part', stl='일부 완료', per='2026-12-01 ~ 2027-01-15', own='AI 분석 쪽', gate='— (관문 없음, S3로 넘김)', out='정제한 27개 원단 표, 핵심 후보 변수 10개 안팎', yr='1차년도 · 구조–마찰–압축 관계의 정량 분석', d='기존 원단 27개로 닮음 지도와 장비 간 일치도를 먼저 봅니다.'),
 dict(k='s2', n=2, file='stage_2_data.html', name='샘플 확충·정답 측정', st='draft', stl='설계안', per='2026-12-01 ~ 2027-05-31', own='실험실 (제작·측정) + AI 쪽 (입력 양식, 자동 품질검사)', gate='G2 — 원단 50개 이상 정답 측정 완료 (2027-05-31)', out='마스터 표 (원단 × 8묶음), 반복 측정 원자료', yr='1차년도 · 물리·기계·표면 특성 DB, 시계열 마찰·압축 측정', d='같은 장비·같은 조건으로 원단 50~100개를 만들고 잽니다.'),
 dict(k='s3', n=3, file='stage_3_model.html', name='기초 예측 모델', st='draft', stl='설계안', per='2027-02-01 ~ 2027-06-30', own='AI 분석 쪽', gate='G3 — 기준선보다 나은 모델과 교차검증 보고서 (2027-06-30)', out='기초 예측 모델, 교차검증 보고서, 변수 영향도', yr='1차년도 · 구조와 시계열 마찰 특성 예측 기초 AI 모델', d='작은 모델부터 올리고, 원단 단위 검증과 합격선으로 평가합니다.'),
 dict(k='s4', n=4, file='stage_4_sim2real.html', name='Sim-to-Real 데이터', st='plan', stl='예정', per='2027-03-01 ~ 2027-08-31 (예정)', own='예정 — 미확정 (실험실 쪽 제안)', gate='예정', out='시뮬레이션 합성 데이터, 실측 분포 비교 보고 (예정)', yr='1차년도 Sim-to-Real 구조 데이터 생성 → 2차년도 합성·실측 융합', d='시뮬레이션으로 가상 원단 데이터를 만들어 부족한 데이터를 채웁니다.'),
 dict(k='s5', n=5, file='stage_5_tribo.html', name='마찰전기 예측 모델', st='plan', stl='예정', per='2027-06-01 ~ 2027-12-15 (예정)', own='예정 — AI 분석 쪽 제안', gate='예정', out='Structure-to-Performance 모델, 외부 검증 보고 (예정)', yr='2차년도 · 마찰전기 센서 성능 예측 모델', d='직물 구조와 동적 특성으로 마찰전기 센서 출력을 미리 맞힙니다.'),
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
    L = [('index.html', '전체 계획'), ('plan_years.html', '연차별 계획'), ('stages.html', '스테이지·FLOW')]
    h = '<nav class="top" aria-label="문서 바로가기"><div class="wrap"><a class="logo" href="index.html">섬유 AI 연구 브리핑</a>'
    for f, t in L: h += f'<a class="l" href="{f}"' + (' aria-current="page"' if f == cur else '') + f'>{t}</a>'
    h += '<span class="sep">|</span>'
    for s in STAGES:
        h += f'<a class="l" href="{s["file"]}" title="{s["name"]} ({s["stl"]})"' + (' aria-current="page"' if s['file'] == cur else '') + f'>S{s["n"]}{"·예정" if s["st"]=="plan" else ""}</a>'
    h += '<span class="sep">|</span>'
    for f, t in [('image_data.html', '이미지 분석'), ('data_guide.html', '작성 가이드'), ('references.html', '참고문헌')]:
        h += f'<a class="l" href="{f}"' + (' aria-current="page"' if f == cur else '') + f'>{t}</a>'
    return h + '</div></nav>'

def crumb(*parts):
    return '<p class="crumb">' + ' › '.join(f'<a href="{f}">{t}</a>' if f else t for f, t in parts) + '</p>'

def say(who, mood, txt):
    nm = {'sia': '인턴 시아', 'moa': '인턴 모아', 'asst': '조수 하루', 'robo': '주판봇'}[who]
    return f'<div class="say" data-who="{who}"><img class="who" data-who="{who}" data-mood="{mood}" alt="" aria-hidden="true"><div class="bub"><b class="name">{nm}</b><p>{txt}</p></div></div>'

def pager(prev, nxt):
    h = '<div class="pager">'
    h += f'<a href="{prev[0]}"><small>← 이전</small>{prev[1]}</a>' if prev else '<span></span>'
    h += f'<a href="{nxt[0]}" style="text-align:right"><small>다음 →</small>{nxt[1]}</a>' if nxt else '<span></span>'
    return h + '</div>'

def stage_head(s, rows):
    h = f'<div class="shead"><div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap"><b style="font-size:17px">S{s["n"]} · {s["name"]}</b>{chip(s)}<span class="small muted">2026-11-16 기준</span></div>'
    h += f'<dl><dt>하는 일</dt><dd>{s["d"]}</dd><dt>기간</dt><dd>{s["per"]}</dd><dt>담당</dt><dd>{s["own"]}</dd><dt>관문</dt><dd>{s["gate"]}</dd><dt>산출물</dt><dd>{s["out"]}</dd><dt>연차 연결</dt><dd>{s["yr"]} · <a href="plan_years.html">연차별 계획 보기</a></dd></dl>'
    h += '<h4 style="margin:16px 0 4px">이 스테이지 항목별 상태</h4><div class="tw"><table class="chk"><tr><th>항목</th><th>상태</th></tr>'
    for t, c in rows:
        cl = {'완료': 'done', '진행 중': 'run', '일부 완료': 'part', '설계안': 'draft', '예정': 'plan'}[c]
        h += f'<tr><td>{t}</td><td><span class="st {cl}">{c}</span></td></tr>'
    return h + '</table></div></div>'

def sprites(html):
    moods = set(re.findall(r'data-who="(\w+)" data-mood="(\w+)"', html))
    for w in ['sia', 'moa', 'asst']: moods.add((w, 'smile'))
    for m in ['calc','happy','smile','chart','meh','wow']: moods.add(('robo', m))
    spr = {}
    for who, mood in sorted(moods):
        key = f'{who}_{mood}'
        if key not in emap: continue
        p = f'{PACK}/webp/192/{who}/{emap[key]["key"]}.webp'
        spr[key] = 'data:image/webp;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
    return spr

def page(fname, title, body, cur=None, kg=False, extra=None):
    head = HEAD.replace('<title>', '<title>', 1)
    head = re.sub(r'<title>.*?</title>', f'<title>{title} — 섬유 AI 연구 브리핑</title>', head, flags=re.S)
    html = head + EXTRA_CSS + '</style>\n</head><body>\n<div id="prog" aria-hidden="true"></div>\n' + nav(cur or fname) + '\n' + body + '\n' + FOOT + '<div id="tip" role="tooltip"></div>\n<button type="button" id="roboFab" aria-label="주판봇에게 수정·보완 요청"><img alt=""><span>수정 요청</span></button>\n'
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
ROBO = ('<section class="level" id="robo"><div class="wrap"><h2>주판봇에게 수정·보완 요청</h2>'
  '<div class="say" data-who="robo"><img class="who" id="rqFace" data-who="robo" data-mood="calc" alt="" aria-hidden="true"><div class="bub"><b class="name">주판봇</b><p id="rqSay">이 쪽에서 고칠 곳을 알려 주세요. 두 번 누르고 한 줄만 쓰시면 요청서가 됩니다. 제목 옆 "요청" 단추로 바로 오셔도 됩니다.</p></div></div>'
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
    say('asst', 'report', '교수님, S0는 오늘 시작한 단계입니다. 데이터 진단은 끝났고, 결정 질문의 답을 들으면 G1 관문을 넘습니다.'))
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
    ('마찰전기 출력 측정 장치·조건', '예정'),
    ('입력 양식과 자동 품질검사', '예정')],
    lv('lv3', 'S2 · 데이터 준비 — 원단마다 8묶음, 몇 개를 만들까', rev='s2'),
    say('moa', 'think', 'S2는 설계안까지 왔습니다. 항목과 원단 수는 제안값이라, 교수님 검토 뒤 확정하겠습니다.'))
# S3
s = SBY['s3']
sizes[s['file']] = stage_page(s, [
    ('모델 순서: 기준선 → 트리 앙상블 → 신경망 (제안)', '설계안'),
    ('원단 단위 교차검증 원칙', '설계안'),
    ('평가 기준 13개와 합격선 (제안값)', '설계안'),
    ('실제 모델 학습 (S2 정답 데이터가 필요)', '예정'),
    ('경로 분석(PLS-SEM)과 변수 영향도(SHAP)', '예정'),
    ('새 원단 10개 이상 외부 검증', '예정')],
    lv('lv4', 'S3-1 · 모델링 — 작은 모델부터 단계적으로 (M1~M4)', drop_rev=True) + lv('lv5', 'S3-2 · 평가 기준 — 무엇을, 얼마면 합격인가', rev='s3'),
    say('asst', 'report', 'S3는 설계만 끝났습니다. 아래 두 실험은 원리를 보여 드리는 가상 데이터이고, 실제 학습은 S2 정답 데이터가 모인 뒤 시작합니다.'))

# S4~S6 예정 쪽
def plan_body(s, fixed, open_, link, sayx):
    h = f'<section class="level lv"><div class="wrap"><div class="lvhead"><span class="hexno">{s["n"]}</span><h2>S{s["n"]} · {s["name"]} — 지금 정해진 것과 예정인 것</h2></div>'
    h += '<div class="planbox"><h4>아직 준비 전인 스테이지입니다 <span class="st plan">예정</span></h4><p class="small" style="margin:0">아래 "정해진 것"은 연구계획서·킥오프 문서에 적힌 내용입니다. "예정"은 담당·범위·날짜가 아직 정해지지 않은 항목입니다.</p></div>'
    h += '<div class="yr"><h3>정해진 것 — 문서 근거</h3><ul>' + ''.join(f'<li>{x}</li>' for x in fixed) + '</ul></div>'
    h += '<div class="yr plan"><h3>예정 — 정해야 할 것 <span class="st plan">예정</span></h3><ul>' + ''.join(f'<li>{x}</li>' for x in open_) + '</ul></div>'
    h += '<div class="yr"><h3>앞뒤 스테이지와의 연결</h3><ul>' + ''.join(f'<li>{x}</li>' for x in link) + '</ul></div>'
    h += '<div class="talk"><p class="th">질의응답</p>' + sayx + '</div>'
    h += f'<div class="review" id="review-{s["k"]}" data-rev="{s["k"]}"></div></div></section>'
    return h

s = SBY['s4']
sizes[s['file']] = stage_page(s, [('시뮬레이션 도구: TexGen(또는 Rhino/Grasshopper) → Abaqus (계획서 기재)', '설계안'), ('담당·계산 환경', '예정'), ('가상 원단 범위와 개수', '예정'), ('합성 데이터 형식 합의', '예정'), ('실측 분포와 비교·보정', '예정')],
    plan_body(s, ['TexGen(혹은 Rhino/Grasshopper)으로 제직·편직 조직의 단위 셀(unit-cell)을 만들고, Abaqus로 변형 거동을 계산해 데이터를 만듭니다 [4].',
                  '2차년도에는 합성 출력과 실측 출력의 분포·통계·주파수를 비교해 보정합니다(파라미터 조정, 도메인 랜덤화, 정규화) [4].',
                  '목적은 원단 100개 안팎이라는 실측 데이터의 한계를 가상 데이터로 보완하는 것입니다.'],
              ['시뮬레이션을 맡을 사람과 계산 환경(라이선스·서버)', '어떤 조직·밀도의 가상 원단을 몇 개 만들지', '합성 데이터를 실측 마스터 표와 같은 열 이름으로 맞추는 방법', '시작 시점 — 제안 일정은 2027-03이지만 담당이 정해져야 확정됩니다'],
              ['앞: S2 실측 데이터의 분포가 시뮬레이션 보정의 기준이 됩니다.', '뒤: S5 마찰전기 예측 모델이 합성 + 실측 데이터를 함께 씁니다.'],
              say('sia', 'think', '시뮬레이션 데이터만으로 모델을 만들 수도 있습니까?') + say('asst', 'report', '그렇게 하지 않습니다. 가상 데이터는 실측과 분포를 맞춰 본 뒤에만 보조로 섞겠습니다. 담당이 정해지면 계획을 다시 보고드리겠습니다.')),
    say('asst', 'report', 'S4는 예정 단계입니다. 정해진 것과 정해야 할 것을 나눠 보고드립니다.'))
s = SBY['s5']
sizes[s['file']] = stage_page(s, [('목표: 구조 + 동적 특성 → 마찰전기 센서 성능 (계획서 기재)', '설계안'), ('주 정답 지표 (전압·전류·전하밀도 등)', '예정'), ('측정 조건 (접촉 모드·상대 물질·힘·주파수·온습도)', '예정'), ('모델 구조 선택', '예정'), ('외부 검증용 새 원단', '예정')],
    plan_body(s, ['2차년도 목표: 합성 + 실측 데이터를 결합해 실제 온도·습도 조건에서 마찰전기 센서 성능을 예측하는 Structure-to-Performance 모델 [4].',
                  '입력: 구조 변수, 물리·기계·표면 특성, 동적 마찰·압축 특징, 합성 데이터. 출력: 감도, 선형성, 전하밀도, 주파수 응답 등 [4].',
                  '평가 착안점: R²·RMSE 같은 예측 정확도, 구조 변화에 대한 일반화, 초기 제작 센서로 보정 전후 비교 [4].'],
              ['출력 지표 중 무엇을 주 정답으로 할지', '측정 조건 — 접촉 모드, 상대 물질, 누르는 힘·주파수, 온도·습도 범위', '모델 구조 — 계획서는 CNN·GCN·비전 트랜스포머 임베딩을 적었으나, 데이터 수에 맞춰 S3 결과를 보고 고르는 안을 제안합니다', '외부 검증용 새 원단의 제작 시기와 개수'],
              ['앞: S3 기초 모델의 변수와 검증 방식을 그대로 이어받습니다.', '앞: S4 합성 데이터를 보조 학습 자료로 씁니다.', '뒤: 3차년도 착용 환경 재예측 모델의 출발점이 됩니다.'],
              say('moa', 'think', '합격선은 S3와 같습니까?') + say('asst', 'report', 'S3 계기판에 마찰전기 R² 0.6 이상을 제안해 두었습니다. 정답 지표가 정해지면 합격선도 함께 확정하겠습니다.')),
    say('asst', 'report', 'S5는 2차년도의 중심 과제이며, 아직 예정 단계입니다.'))
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
plan = plan.replace('세로 점선은 오늘(2026-11-14)입니다.', '세로 점선은 오늘(2026-11-16)입니다.')
cards = '<div class="mapc">' + ''.join(
    f'<a class="card{" plan" if s["st"]=="plan" else ""}" href="{s["file"]}"><span>S{s["n"]} {chip(s)}</span><b>{s["name"]}</b><span class="d">{s["d"]}<br>{s["per"]}<br>관문: {s["gate"]}</span></a>' for s in STAGES) + '</div>'
legend = '<p class="small">상태 표시: <span class="st done">완료</span> <span class="st run">진행 중</span> <span class="st part">일부 완료</span> <span class="st draft">설계안</span> <span class="st plan">예정</span> — 예정은 담당·범위·날짜가 아직 정해지지 않았다는 뜻입니다.</p>'
st_top = wrap(crumb(('index.html', 'INDEX'), (None, '전체 연구 스테이지 및 FLOW')) +
    '<h1 style="margin:4px 0 8px">전체 연구 스테이지 및 FLOW</h1><p class="lead">2026-11부터 2027-12까지 7개 스테이지(S0~S6)로 진행합니다. S0~S3은 1차년도 핵심이고, S4~S6은 아직 <span class="st plan">예정</span>입니다. 카드를 누르면 스테이지 쪽으로 들어갑니다.</p>' + legend + cards +
    say('asst', 'report', '교수님, 스테이지는 흐름도의 단계를 묶은 것입니다. 흐름도 상자나 일정 막대를 누르셔도 해당 스테이지 쪽으로 가실 수 있습니다.'))
sizes['stages.html'] = page('stages.html', '전체 연구 스테이지 및 FLOW', st_top + flow + plan + tail((('plan_years.html', '연차별 연구계획'), (STAGES[0]['file'], 'S0 착수·자료 정리'))))

# ---------------- 연차별 연구계획 ----------------
YEARS = [
 ('1차년도', '2026 (계획서 기재)', 'run', '진행 중', '구조·물성 DB와 동적 마찰 예측 기초 모델',
  ['실 구조 설계와 특성 측정, 제직·편직물 조직 설계·제작 (디지털 편직·자카드 직기)', '물리·기계·표면 특성 DB 구축 (KES-FB, FAST, 표면형상측정기)', '시계열 마찰·압축 측정, 마찰력 변화를 스펙트로그램 촉각 이미지로', '랜덤포레스트·XGBoost·MLP로 예비 예측 모델', 'TexGen → Abaqus 시뮬레이션 데이터 생성'],
  ['마찰·압축 데이터의 정량성·재현성', '동적 마찰·압축 응답의 충분한 수집·분석', '구조–마찰–압축 관계의 정량 분석과 학술적 타당성', '데이터 구조화와 기초 모델 검증 완료'], 'S0 S1 S2 S3 S4(일부)'),
 ('2차년도', '2027 (계획서 기재)', 'draft', '계획', '마찰전기 센서 성능 예측 (Structure-to-Performance)',
  ['직물 마찰전기 센서 후보 구조 설계·제작, 출력 특성 측정', '온도·습도·접촉 조건별 전기 특성 측정', '합성 전기 출력 데이터 생성과 Sim-to-Real 보정', '합성 + 실측 통합 데이터로 성능 예측 모델, 초기 센서로 보정'],
  ['합성 데이터와 실측 데이터의 정합도', '감도·출력·선형성 예측 정확도 (R², RMSE)', '구조 변화에 대한 일반화 성능', '보정 전후 예측 성능 비교'], 'S4 S5 S6'),
 ('3차년도', '2028 (예정)', 'plan', '예정', '옷에 넣었을 때의 성능 재예측 (Wearable-aware)',
  ['착용형 플랫폼(상의·하의·장갑 등) 선정, 센서 의복 통합', '동작별 변형 분포(strain map) 수집, 패턴·봉제선별 변형 분석', '착용 환경 변수를 더한 재예측 모델 (시계열 모델 전이학습)'],
  ['착용 환경 요인 분석의 정량성', 'strain map 데이터 완성도', '착용 환경 반영 후 예측 정확도 향상 여부'], '스테이지 설계 예정'),
 ('4차년도', '2029 (예정)', 'plan', '예정', '여러 센서로 인체 동작 인식',
  ['멀티센서 의복형 시스템 설계·제작과 착용성 시험', '보행·균형·상지·체간 동작 데이터 수집과 지표 구축', '센서 수·배치·감도 조합 ablation으로 최적 구성 도출'],
  ['동작 분류 정확도 90% 이상', '최소 센서 구성으로 성능 90% 이상 유지', '센서 수·위치 대 성능 변화 곡선 제시'], '스테이지 설계 예정'),
 ('5차년도', '2030 (예정)', 'plan', '예정', '개인정보 보호형 온디바이스 플랫폼',
  ['모델 경량화와 스마트 기기 탑재, 비식별화·암호화', '반복 변형·세탁·땀·온습도 내구성 평가', '사용성 평가와 통합 플랫폼, 응용 분야 검토'],
  ['모델 80% 이상 경량화에 성능 95% 유지', '세탁 10~20회 후 출력 80% 이상 유지', '착용자 평가 5점 척도 평균 4점 이상, 유효 데이터 획득률 90% 이상'], '스테이지 설계 예정'),
]
yh = ''
for nm, when, cl, lb, goal, cont, crit, stg in YEARS:
    links = ' '.join(f'<a href="{SBY["s"+t[1]]["file"]}">{t}</a>' if t.startswith('S') and t[1].isdigit() else t for t in stg.split(' ')) if stg.startswith('S') else f'<span class="st plan">{stg}</span>'
    yh += f'<div class="yr{" plan" if cl=="plan" else ""}"><h3>{nm} <span class="small muted">{when}</span> <span class="st {cl}">{lb}</span></h3><p style="margin:0"><b>목표</b> — {goal}</p><div class="cols"><div><h4>연구 내용 (계획서 요약)</h4><ul>' + ''.join(f'<li>{x}</li>' for x in cont) + '</ul></div><div><h4>평가 착안점 (계획서 기재)</h4><ul>' + ''.join(f'<li>{x}</li>' for x in crit) + f'</ul></div></div><p class="small" style="margin:10px 0 0"><b>연결 스테이지</b> — {links}</p></div>'
yrs = wrap(crumb(('index.html', 'INDEX'), (None, '연차별 연구계획')) +
    '<h1 style="margin:4px 0 8px">연차별 연구계획 — 5년 로드맵</h1><p class="lead">연구계획서(2026년도 핵심연구 유형B)의 5년 계획을 연차별로 정리했습니다. 1·2차년도는 스테이지로 쪼개 두었고, 3~5차년도는 <span class="st plan">예정</span>입니다.</p>' +
    '<div class="planbox"><h4>날짜에 대한 알림 <span class="st plan">예정</span></h4><p class="small" style="margin:0">계획서는 1차년도를 2026년으로 적었지만, 이 브리핑의 스테이지 일정은 2026-11 ~ 2027-12입니다. 과제 협약 시작일이 정해지면 연차 경계를 다시 맞추겠습니다(결정 질문 1번).</p></div>' +
    say('asst', 'report', '교수님, 연차마다 목표, 연구 내용, 계획서의 평가 착안점, 연결 스테이지 순서로 보고드립니다.') + yh +
    '<h3>연구 가설 다섯 개와 연차</h3><div class="tw"><table class="tb"><tr><th>가설</th><th>내용 (요약)</th><th>주로 검증하는 연차</th></tr>'
    '<tr><td>1</td><td>구조 변수 데이터로 직물의 동적 마찰·압축 특성을 예측할 수 있다</td><td>1차 (S1~S3)</td></tr>'
    '<tr><td>2</td><td>합성 + 실측 데이터로 마찰전기 센서 성능을 예측하고, 온습도 조건에서도 일반화된다</td><td>2차 (S4·S5)</td></tr>'
    '<tr><td>3</td><td>옷의 패턴·봉제·인체 변형이 센서 성능에 비선형으로 영향을 주며, 이를 모델링해 재예측할 수 있다</td><td>3차 (예정)</td></tr>'
    '<tr><td>4</td><td>센서 수·배치·감도를 최적화하면 적은 센서로 높은 동작 인식 성능을 낸다</td><td>4차 (예정)</td></tr>'
    '<tr><td>5</td><td>온디바이스 처리·비식별화·암호화로 개인정보를 지키며 실사용 신뢰성을 높인다</td><td>5차 (예정)</td></tr></table></div>') + tail((('index.html', 'INDEX — 전체 연구 계획 정리'), ('stages.html', '전체 연구 스테이지 및 FLOW')))
sizes['plan_years.html'] = page('plan_years.html', '연차별 연구계획', yrs)

# ---------------- INDEX ----------------
hero = T[T.index('<header class="hero">'):T.index('<section class="level" id="intro">')]
hero = hero.replace('2026-11-14 기준', '2026-11-16 기준').replace('보고마다 결론을 먼저 말씀드리고, 끝에 교수님 검토가 필요한 사항을 정리했습니다. 그림은 직접 눌러 확인하실 수 있습니다.',
    '이 쪽은 전체 계획의 요약입니다. 연차별 계획, 스테이지 흐름, 스테이지별 상세 쪽으로 이어집니다. 아직 정해지지 않은 것은 <span class="st plan">예정</span>으로 표시했습니다.')
hero = hero.replace('보고마다 검토 사항을 정리해 두었습니다. 표시해 주시면 마지막에 모아 드리겠습니다.', '스테이지마다 검토 사항이 있습니다. 표시해 주시면 이 쪽 아래에 모아 드리겠습니다.')
intro = re.sub(r'<h3 style="margin-top:22px">오늘 보고 순서</h3>\s*<ol class="agenda">.*?</ol>', '', INTRO, flags=re.S)
docmap = ('<h2 id="map" style="margin-top:30px">문서 지도 — 어디부터 보시면 되나</h2><div class="mapc">'
    '<a class="card" href="plan_years.html"><span>1</span><b>연차별 연구계획</b><span class="d">5년 로드맵. 연차마다 목표·내용·평가 착안점. 3~5차년도는 예정.</span></a>'
    '<a class="card" href="stages.html"><span>2</span><b>전체 연구 스테이지 및 FLOW</b><span class="d">흐름도와 일정 막대, 7개 스테이지 카드.</span></a>'
    '<a class="card" href="stage_0_kickoff.html"><span>3</span><b>스테이지별 상세 (S0~S6)</b><span class="d">S0 데이터 현황·결정 질문부터. 스테이지마다 검토 사항.</span></a>'
    '<a class="card" href="image_data.html"><span>4</span><b>섬유 이미지 데이터 리뷰·분석</b><span class="d">받은 실습용 이미지 140장 진단과 보완사항.</span></a>'
    '<a class="card" href="data_guide.html"><span>5</span><b>가상 섬유 데이터 작성 가이드</b><span class="d">합성 표·시뮬레이션·생성 이미지 기록 양식과 점검표.</span></a>'
    '<a class="card" href="references.html"><span>6</span><b>참고 레퍼런스</b><span class="d">장비·마찰전기·시뮬레이션·데이터 품질 문헌.</span></a></div>'
    '<div class="stgrid" role="list">' + ''.join(f'<a role="listitem" class="{"plan" if s["st"]=="plan" else ""}" href="{s["file"]}"><b>S{s["n"]}</b>{s["name"]}<br>{chip(s)}</a>' for s in STAGES) + '</div>')
stt = '<h2 id="status" style="margin-top:30px">스테이지 현황 — 2026-11-16 기준</h2><div class="tw"><table class="tb"><tr><th>스테이지</th><th>상태</th><th>기간</th><th>관문</th><th>연차</th></tr>' + ''.join(
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
REQS = ('<section class="level" id="reqs"><div class="wrap"><h2>주판봇 요청 모음 — 모든 쪽</h2>'
  '<p class="lead">각 쪽에서 남기신 수정·보완 요청을 한곳에 모았습니다. 기한 순으로 정렬되며, 반영하면 상태를 눌러 바꿉니다. 요청서는 복사하거나 .md·.csv로 내려받을 수 있습니다.</p>'
  '<div class="say" data-who="robo"><img class="who" id="roboFace2" data-who="robo" data-mood="chart" alt="" aria-hidden="true"><div class="bub"><b class="name">주판봇</b><p id="reqSay">아직 접수된 요청이 없습니다.</p></div></div>'
  '<div class="kpis" id="reqK"></div>'
  '<div class="ctrl"><div class="group" role="group" aria-label="요청 거르기"><button type="button" class="bt" data-rf="open" aria-pressed="true">남은 요청</button><button type="button" class="bt" data-rf="done" aria-pressed="false">반영 완료</button><button type="button" class="bt" data-rf="all" aria-pressed="false">전체</button></div></div>'
  '<div class="tw" id="reqT"></div>'
  '<div class="ctrl"><button type="button" class="bt primary" id="reqCopy">요청서 복사</button><button type="button" class="bt" id="reqMd">요청서 .md 내려받기</button><button type="button" class="bt" id="reqCsv">표 .csv 내려받기</button><span class="small muted" id="reqMsg" aria-live="polite"></span></div>'
  '<p class="small muted dlnote" aria-live="polite"></p><pre class="cite" id="reqTxt" hidden></pre></div></section>')
kgs, exs = sec('kg'), sec('export')
idx = COVER + hero + intro + summary + review + REQS + outro + kgs + exs + tail((None, ('plan_years.html', '연차별 연구계획')))
sizes['index.html'] = page('index.html', 'INDEX — 전체 연구 계획 정리', idx, kg=True)
exec(open(f'{B}/pages_extra.py', encoding='utf-8').read())
for k, v in sizes.items(): print(k, round(v / 1024), 'KB')
