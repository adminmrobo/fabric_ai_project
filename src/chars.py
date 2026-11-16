# 섬유 조직 캐릭터 4종 — 평직이·능직이·편직이·부직이 (SVG 직접 생성, 외부 그림 팩 없음)
# 몸통 = 해당 조직의 실 배치를 그대로 그린 둥근 덩어리, 얼굴·발은 공통.
import random, base64

CAST = {
    'asst': dict(name='평직이', kind='plain', role='보고 담당', desc='평직(Plain) — 날실과 씨실이 한 올씩 번갈아 오르내리는 가장 기본 조직',
                 base='#5b8fd6', a='#4f84cf', b='#9cc0ee', gap='#2f5d9e', foot='#4a7cc2', cheek='#ff9db0'),
    'sia':  dict(name='능직이', kind='twill', role='질문 담당', desc='능직(Twill) — 교차점이 한 칸씩 밀려 사선 무늬가 생기는 조직 (데님)',
                 base='#2f9e8f', a='#1f8574', b='#a6e3d8', gap='#125a50', foot='#278a7c', cheek='#ffa3a3'),
    'moa':  dict(name='편직이', kind='knit', role='기록 담당', desc='편직(Knit) — 실로 고리를 만들어 엮은 조직 (티셔츠·스웨터)',
                 base='#e0786a', a='#d8685a', b='#f6b2a6', gap='#b24c40', foot='#cc6255', cheek='#ffd0d6'),
    'robo': dict(name='부직이', kind='nonwoven', role='수정 요청 접수', desc='부직포(Nonwoven) — 실을 만들지 않고 섬유를 바로 얽어 붙인 천 (마스크)',
                 base='#a996d6', a='#8e78c9', b='#e7defa', gap='#6f5aa8', foot='#8f7bc8', cheek='#ffb3cf'),
}
CX, CY, RX, RY = 96, 98, 74, 70

def _cells(c, n, over):
    s, out = 16, []
    for i in range(n):
        for j in range(n):
            x, y = j * s, i * s
            if over(i, j):
                out.append(f'<rect x="{x+2.5}" y="{y+0.5}" width="{s-5}" height="{s-1}" rx="5" fill="{c["a"]}"/>'
                           f'<rect x="{x+5}" y="{y+2}" width="3" height="{s-5}" rx="1.5" fill="#fff" opacity=".22"/>')
            else:
                out.append(f'<rect x="{x+0.5}" y="{y+2.5}" width="{s-1}" height="{s-5}" rx="5" fill="{c["b"]}"/>'
                           f'<rect x="{x+2}" y="{y+4}" width="{s-5}" height="3" rx="1.5" fill="#fff" opacity=".35"/>')
    return ''.join(out)

def _tile(pid, w, h, c, body):
    return (f'<pattern id="{pid}" width="{w}" height="{h}" patternUnits="userSpaceOnUse" x="-8" y="-6">'
            f'<rect width="{w}" height="{h}" fill="{c["gap"]}"/>{body}</pattern>')

def _weave(c, twill, pid):
    if twill:
        return _tile(pid, 64, 64, c, _cells(c, 4, lambda i, j: (j - i) % 4 < 2))
    return _tile(pid, 32, 32, c, _cells(c, 2, lambda i, j: (i + j) % 2 == 0))

def _knit(c, pid):
    w, h, out = 18, 14, []
    for i in range(2):
        for j in range(3):
            x, y = j * w, i * h - h
            col = c['a'] if (i + j) % 3 else c['b']
            for yy in (y, y + 2 * h):
                out.append(f'<path d="M{x+2},{yy} Q{x+4},{yy+h} {x+w/2},{yy+h+3}" stroke="{c["b"]}" stroke-width="7" fill="none" stroke-linecap="round"/>'
                           f'<path d="M{x+w-2},{yy} Q{x+w-4},{yy+h} {x+w/2},{yy+h+3}" stroke="{col}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    return _tile(pid, 3 * w, 2 * h, c, ''.join(out))

def _nonwoven(c):
    r = random.Random(7)
    out = [f'<rect x="0" y="0" width="192" height="192" fill="{c["base"]}"/>']
    cols = [c['a'], c['b'], c['gap'], '#ffffff']
    for k in range(60):
        x0, y0 = r.uniform(0, 192), r.uniform(0, 192)
        x1, y1 = x0 + r.uniform(-60, 60), y0 + r.uniform(-60, 60)
        qx, qy = (x0 + x1) / 2 + r.uniform(-30, 30), (y0 + y1) / 2 + r.uniform(-30, 30)
        out.append(f'<path d="M{x0:.0f},{y0:.0f} Q{qx:.0f},{qy:.0f} {x1:.0f},{y1:.0f}" stroke="{r.choice(cols)}" stroke-width="{r.uniform(1.4,3.2):.1f}" fill="none" stroke-linecap="round" opacity="{r.uniform(.45,.9):.2f}"/>')
    for k in range(14):  # 섬유가 얽힌 접점(본딩점)
        out.append(f'<circle cx="{r.uniform(20,172):.0f}" cy="{r.uniform(20,172):.0f}" r="{r.uniform(2,4):.1f}" fill="#fff" opacity=".55"/>')
    return ''.join(out)

def _top(kind, c):
    if kind == 'plain':   # 실 고리 한 올
        return f'<path d="M96,30 C86,8 112,6 104,24" stroke="{c["b"]}" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M96,30 C86,8 112,6 104,24" stroke="{c["a"]}" stroke-width="2" fill="none" stroke-linecap="round" opacity=".6"/>'
    if kind == 'twill':   # 사선 실 끝 두 가닥
        return f'<path d="M84,30 L74,10" stroke="{c["b"]}" stroke-width="6" stroke-linecap="round"/><path d="M98,29 L92,8" stroke="{c["a"]}" stroke-width="6" stroke-linecap="round"/>'
    if kind == 'knit':    # 털실 방울
        dots = ''.join(f'<circle cx="{96+dx}" cy="{22+dy}" r="5" fill="{c["b"] if (dx+dy)%2 else c["a"]}"/>' for dx, dy in [(-7,-3),(0,-8),(7,-3),(-4,4),(4,4),(0,-1)])
        return f'<circle cx="96" cy="22" r="13" fill="{c["gap"]}"/>' + dots
    out = ''          # 부직포: 삐죽 나온 섬유털
    r = random.Random(3)
    for k in range(16):
        import math
        a = -math.pi * (0.15 + 0.7 * k / 15)
        x0, y0 = CX + RX * 0.96 * math.cos(a), CY + RY * 0.96 * math.sin(a)
        L = r.uniform(7, 14)
        x1, y1 = x0 + L * math.cos(a + r.uniform(-.5, .5)), y0 + L * math.sin(a + r.uniform(-.5, .5))
        out += f'<path d="M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}" stroke="{c["a"]}" stroke-width="2.4" stroke-linecap="round"/>'
    return out

HAPPY = {'smile', 'happy', 'proud', 'sparkle', 'ok', 'calc', 'chart'}
WOW = {'spark', 'wow'}
THINK = {'think', 'meh'}

def _face(mood, c):
    ex, ey = 26, 96
    eyes = ''
    if mood in {'proud', 'happy'}:
        for sx in (-1, 1):
            eyes += f'<path d="M{CX+sx*ex-10},{ey+3} Q{CX+sx*ex},{ey-9} {CX+sx*ex+10},{ey+3}" stroke="#14161a" stroke-width="5" fill="none" stroke-linecap="round"/>'
    else:
        dx, dy = (4, -4) if mood == 'think' else (0, 0)
        for sx in (-1, 1):
            x = CX + sx * ex
            eyes += f'<ellipse cx="{x}" cy="{ey}" rx="12" ry="13" fill="#14161a"/>'
            eyes += f'<circle cx="{x-3+dx}" cy="{ey-4+dy}" r="4.2" fill="#fff"/><circle cx="{x+4+dx}" cy="{ey+4+dy}" r="1.8" fill="#fff" opacity=".8"/>'
            if mood == 'meh':
                eyes += f'<rect x="{x-14}" y="{ey-15}" width="28" height="12" fill="#fbf7f2"/>'
            if mood == 'firm':
                eyes += f'<path d="M{x-12},{ey-19+sx*-2} L{x+12},{ey-19+sx*2}" stroke="#14161a" stroke-width="3.5" stroke-linecap="round" transform="scale(1,1)"/>'
    my = 122
    if mood in HAPPY:
        mouth = (f'<path d="M{CX-17},{my-2} Q{CX},{my+26} {CX+17},{my-2} Z" fill="#14161a"/>'
                 f'<path d="M{CX-11},{my+1} Q{CX},{my+6} {CX+11},{my+1} L{CX+9},{my-1} L{CX-9},{my-1} Z" fill="#fff"/>')
    elif mood in WOW:
        mouth = f'<ellipse cx="{CX}" cy="{my+6}" rx="9" ry="11" fill="#14161a"/><ellipse cx="{CX}" cy="{my+12}" rx="5" ry="3" fill="#e46a7a"/>'
    elif mood == 'think':
        mouth = f'<path d="M{CX-4},{my+6} Q{CX+6},{my+2} {CX+12},{my+7}" stroke="#14161a" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
    elif mood == 'meh':
        mouth = f'<path d="M{CX-12},{my+6} Q{CX-6},{my+2} {CX},{my+6} T{CX+12},{my+6}" stroke="#14161a" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
    elif mood == 'firm':
        mouth = f'<path d="M{CX-11},{my+6} L{CX+11},{my+6}" stroke="#14161a" stroke-width="5" stroke-linecap="round"/>'
    else:  # report, explain 등 — 다문 미소
        mouth = f'<path d="M{CX-14},{my+1} Q{CX},{my+15} {CX+14},{my+1}" stroke="#14161a" stroke-width="5" fill="none" stroke-linecap="round"/>'
    cheeks = ''.join(f'<ellipse cx="{CX+sx*40}" cy="{ey+20}" rx="9" ry="5.5" fill="{c["cheek"]}" opacity=".75"/>' for sx in (-1, 1))
    return eyes + cheeks + mouth

def _deco(mood):
    star = lambda x, y, s: f'<path d="M{x},{y-s} L{x+s*.3},{y-s*.3} L{x+s},{y} L{x+s*.3},{y+s*.3} L{x},{y+s} L{x-s*.3},{y+s*.3} L{x-s},{y} L{x-s*.3},{y-s*.3} Z" fill="#ffc531" stroke="#c98a00" stroke-width="1.2"/>'
    if mood in {'spark', 'sparkle', 'wow'}:
        return star(166, 34, 13) + star(150, 14, 7) + star(24, 46, 8)
    if mood == 'think':
        return '<circle cx="160" cy="44" r="4" fill="#5b6874"/><circle cx="170" cy="30" r="6" fill="#5b6874"/><text x="174" y="20" font-size="26" font-weight="800" fill="#1e55c8" font-family="sans-serif" text-anchor="middle">?</text>'
    if mood in {'calc', 'chart'}:
        return ('<rect x="138" y="130" width="44" height="40" rx="7" fill="#fff" stroke="#16212b" stroke-width="2.5"/>'
                '<rect x="146" y="152" width="7" height="12" fill="#1e55c8"/><rect x="157" y="144" width="7" height="20" fill="#13733a"/><rect x="168" y="138" width="7" height="26" fill="#a35c00"/>')
    if mood == 'report':
        return '<path d="M156,150 L182,124" stroke="#7a5230" stroke-width="5" stroke-linecap="round"/><circle cx="183" cy="123" r="4" fill="#c9302c"/>'
    if mood == 'explain':
        return '<rect x="146" y="22" width="36" height="24" rx="8" fill="#fff" stroke="#16212b" stroke-width="2"/><path d="M152,46 L148,56 L160,46 Z" fill="#fff" stroke="#16212b" stroke-width="2" stroke-linejoin="round"/><text x="164" y="40" font-size="15" font-weight="800" fill="#16212b" font-family="sans-serif" text-anchor="middle">!</text>'
    return ''

def svg(who, mood='smile'):
    c = CAST[who]; k = c['kind']
    pid = f'p_{who}'
    defs, pat = '', ''
    if k in ('plain', 'twill', 'knit'):
        defs = _weave(c, k == 'twill', pid) if k != 'knit' else _knit(c, pid)
        pat = f'<rect width="192" height="192" fill="url(#{pid})"/>'
    else:
        pat = _nonwoven(c)
    g = f'g_{who}'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192" width="192" height="192">'
            f'<defs>{defs}<clipPath id="cp_{who}"><ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}"/></clipPath>'
            f'<radialGradient id="{g}" cx="35%" cy="28%" r="80%"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".32"/></radialGradient>'
            f'<radialGradient id="f_{who}" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fbf7f2" stop-opacity=".95"/><stop offset=".72" stop-color="#fbf7f2" stop-opacity=".82"/><stop offset="1" stop-color="#fbf7f2" stop-opacity="0"/></radialGradient></defs>'
            f'<ellipse cx="96" cy="178" rx="58" ry="7" fill="#000" opacity=".12"/>'
            + _top(k, c) +
            f'<g clip-path="url(#cp_{who})">{pat}<ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="url(#{g})"/></g>'
            f'<ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="none" stroke="{c["gap"]}" stroke-width="2" opacity=".6"/>'
            f'<ellipse cx="{CX}" cy="109" rx="46" ry="33" fill="url(#f_{who})"/>'
            + _face(mood, c) +
            ''.join(f'<ellipse cx="{CX+sx*32}" cy="166" rx="16" ry="11" fill="{c["foot"]}"/><ellipse cx="{CX+sx*32-4}" cy="162" rx="6" ry="3" fill="#fff" opacity=".35"/>' for sx in (-1, 1))
            + _deco(mood) + '</svg>')

def uri(who, mood='smile'):
    from urllib.parse import quote
    return 'data:image/svg+xml;charset=utf-8,' + quote(svg(who, mood), safe=' =:/,;.-_')

MOODS = ['smile', 'report', 'explain', 'think', 'spark', 'firm', 'ok', 'proud', 'sparkle', 'calc', 'happy', 'chart', 'meh', 'wow']

if __name__ == '__main__':
    import sys, os
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(out, exist_ok=True)
    for w in CAST:
        for m in MOODS:
            open(f'{out}/{w}_{m}.svg', 'w').write(svg(w, m))
