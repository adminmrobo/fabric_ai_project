# ---- 섬유 메커니즘 기반 모의 데이터 생성 가이드 (mock_data_guide.html) ----
# build_pages.py 안에서 exec 로 실행된다 (page, wrap, tail, say, crumb 공유)
import importlib.util as _ilu, json as _json
_spec = _ilu.spec_from_file_location('mockgen', os.path.join(B, '..', 'analysis', 'mock_data', 'generate_mock_fabric.py'))
MG = _ilu.module_from_spec(_spec); _spec.loader.exec_module(MG)
_df = MG.generate(20, 20261118)

MK_CSS = """<style>
.mk-eq{font-family:"IBM Plex Mono",monospace;font-size:13.5px;background:#f7f9fb;border:1px solid var(--rule);border-radius:8px;padding:8px 12px;margin:6px 0;line-height:1.75;overflow-x:auto}
.mk-calc{display:grid;grid-template-columns:300px minmax(0,1fr);gap:16px;align-items:start}
.mk-calc label{display:block;font-size:13px;font-weight:600;margin:8px 0 2px}.mk-calc select{width:100%;padding:6px;border:1px solid var(--rule);border-radius:8px;font:inherit}
.mk-calc input[type=range]{width:100%}.mk-calc .v{font-variant-numeric:tabular-nums;color:var(--muted);font-size:12.5px}
.mk-out{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.mk-out .tw{margin:0;overflow:visible}.mk-out .tb{min-width:0!important;width:100%;table-layout:fixed;font-size:13px}.mk-out .tb td,.mk-out .tb th{padding:6px 8px;word-break:keep-all}.mk-out .tb td:first-child{width:58%}
.mk-heat td.h{font-variant-numeric:tabular-nums;text-align:right}
@media (max-width:900px){.mk-calc{grid-template-columns:1fr}.mk-out{grid-template-columns:1fr}}
</style>"""

MREF2 = [
 ('G1', 'Peirce, F. T. (1937). The geometry of cloth structure. <i>Journal of the Textile Institute Transactions</i>, 28, T45–T96.', None, '제직물 기하: 실 지름·간격·굴곡·커버·두께·평량이 서로 묶인 하나의 기하 체계'),
 ('G2', 'Love, L. (1954). Graphical relationships in cloth geometry for plain, twill, and sateen weaves. <i>Textile Research Journal</i>, 24(12), 1073–1083.', 'https://doi.org/10.1177/004051755402401208', '평직·능직·주자직의 커버 팩터와 조직 계수(weave factor) — 능직은 평직보다 밀도를 더 올릴 수 있음'),
 ('G3', 'Munden, D. L. (1959). The geometry and dimensional properties of plain-knit fabrics. <i>Journal of the Textile Institute Transactions</i>.', None, '편직: 코스·웨일 밀도 = 상수 ÷ 루프 길이, 상수는 조임과 무관'),
 ('G4', 'van Wyk, C. M. (1946). A study of the compressibility of wool, with special reference to South African Merino wool. <i>Onderstepoort Journal of Veterinary Science and Animal Industry</i>, 21(1).', 'https://core.ac.uk/download/80918115.pdf', '섬유 집합체의 압축 이론(역세제곱 압력–부피 관계)'),
 ('G5', 'de Jong, S., Snaith, J. W., & Michie, N. A. (1986). A mechanical model for the lateral compression of woven fabrics. <i>Textile Research Journal</i>, 56, 759–767.', None, 'van Wyk 이론을 직물 압축에 적용, KES 압축 시험과 비교'),
 ('G6', 'Howell, H. G., & Mazur, J. (1953). Amontons\' law and fibre friction. <i>Journal of the Textile Institute Transactions</i>, 44, T59–T69.', None, '섬유·직물 마찰은 F = a·Nⁿ (Amontons 법칙이 맞지 않음)'),
 ('G7', 'Kawabata, S. (1980). <i>The Standardization and Analysis of Hand Evaluation</i> (2nd ed.). Hand Evaluation and Standardization Committee, Textile Machinery Society of Japan.', None, 'KES-FB 물성 항목(인장·전단·굽힘·압축·표면)과 태 평가'),
 ('G8', '(Indian Journal of Fibre & Textile Research). 면·폴리에스터·나일론·폴리프로필렌 직물의 접촉·마찰 대전 실험 (Tsuji 등의 대전 서열 인용).', 'https://core.ac.uk/download/276541713.pdf', '직물 대전 서열: 나일론 > 강철 > 면 > 폴리에스터 > 폴리프로필렌 > PTFE (저자 확인 필요)'),
 ('G9', 'Nguyen, V., & Yang, R. (2013). Effect of humidity and pressure on the triboelectric nanogenerator. <i>Nano Energy</i>.', 'https://doi.org/10.1016/j.nanoen.2013.07.012', '상대습도가 90%에서 10%로 내려가면 발생 전하가 20% 넘게 증가'),
 ('G10', 'Kumar, C., Perris, J., Bairagi, S., Min, G., Xu, Y., et al. (2023). Multiscale in-situ quantification of the role of surface roughness and contact area using a novel Mica-PVS triboelectric nanogenerator. <i>Nano Energy</i>, 107, 108122.', 'https://doi.org/10.1016/j.nanoen.2022.108122', '평평한 탄성 표면에서는 거칠기가 커질수록 실접촉 면적과 출력이 감소'),
 ('G11', 'Min, G., et al. (2021). Origin of the contact force-dependent response of triboelectric nanogenerators.', 'https://eld.bl.uk/catalog/100175994510_0x000001', '출력(Voc, Isc)은 실접촉 면적을 따라 증가하고 같은 압력에서 포화'),
 ('G12', 'McKay, M. D., Beckman, R. J., & Conover, W. J. (1979). A comparison of three methods for selecting values of input variables in the analysis of output from a computer code. <i>Technometrics</i>, 21(2), 239–245.', None, '라틴 하이퍼큐브 표본 추출'),
]
MKR = {k: (c, u, w) for k, c, u, w in MREF2}
def gc(*ks): return '<sup>' + ','.join(f'<a href="#{k}">{k}</a>' if k in MKR else f'<a href="method_review.html#{k}">{k}</a>' for k in ks) + '</sup>'

chain_svg = '''<svg viewBox="0 0 980 210" role="img" aria-label="섬유에서 실, 직물 구조, 물성 19항목, 전기 특성 Y로 이어지는 생성 사슬" style="width:100%;height:auto">
<defs><marker id="mka" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#16212b"/></marker></defs>
<g font-family="sans-serif" font-size="13">
<rect x="6" y="40" width="160" height="120" rx="12" fill="#eef3fb" stroke="#2f5d9e" stroke-width="2"/><text x="86" y="64" text-anchor="middle" font-weight="800" font-size="15">① 섬유(소재)</text><text x="86" y="88" text-anchor="middle">밀도 · 탄성률 · 수분율</text><text x="86" y="108" text-anchor="middle">섬유 지름 · 회복성</text><text x="86" y="128" text-anchor="middle">대전 서열</text>
<rect x="206" y="40" width="160" height="120" rx="12" fill="#eef8f2" stroke="#13733a" stroke-width="2"/><text x="286" y="64" text-anchor="middle" font-weight="800" font-size="15">② 실</text><text x="286" y="88" text-anchor="middle">선밀도 tex</text><text x="286" y="108" text-anchor="middle">실 지름 (충전율)</text><text x="286" y="128" text-anchor="middle">→ 굽힘 강성</text>
<rect x="406" y="40" width="180" height="120" rx="12" fill="#fff6e8" stroke="#a35c00" stroke-width="2"/><text x="496" y="64" text-anchor="middle" font-weight="800" font-size="15">③ 직물 구조</text><text x="496" y="88" text-anchor="middle">제직: Peirce · 커버 팩터</text><text x="496" y="108" text-anchor="middle">편직: Munden 루프 상수</text><text x="496" y="128" text-anchor="middle">부직: 평량 · 고형률</text><text x="496" y="148" text-anchor="middle">→ 평량 · 두께 · 충전율</text>
<rect x="626" y="40" width="160" height="120" rx="12" fill="#f3effb" stroke="#6f5aa8" stroke-width="2"/><text x="706" y="64" text-anchor="middle" font-weight="800" font-size="15">④ 물성 X (19)</text><text x="706" y="88" text-anchor="middle">표면: 마찰 · 거칠기</text><text x="706" y="108" text-anchor="middle">역학: 굽힘 · 압축</text><text x="706" y="128" text-anchor="middle">열: 냉온감 Qmax</text>
<rect x="826" y="40" width="148" height="120" rx="12" fill="#fdecec" stroke="#c9302c" stroke-width="2.5"/><text x="900" y="64" text-anchor="middle" font-weight="800" font-size="15">⑤ 전기 특성 Y</text><text x="900" y="88" text-anchor="middle">Voc · Q · I (연속)</text><text x="900" y="108" text-anchor="middle">= 서열 차</text><text x="900" y="128" text-anchor="middle">× 실접촉 × 습도</text>
<path d="M166,100 L204,100" stroke="#16212b" stroke-width="2" marker-end="url(#mka)"/><path d="M366,100 L404,100" stroke="#16212b" stroke-width="2" marker-end="url(#mka)"/><path d="M586,100 L624,100" stroke="#16212b" stroke-width="2" marker-end="url(#mka)"/><path d="M786,100 L824,100" stroke="#16212b" stroke-width="2" marker-end="url(#mka)"/>
<path d="M86,160 C86,200 880,205 900,162" stroke="#c9302c" stroke-width="1.6" stroke-dasharray="5 4" fill="none" marker-end="url(#mka)"/><text x="490" y="200" text-anchor="middle" fill="#c9302c" font-size="12">소재의 대전 서열·수분율은 Y로 직접도 들어간다</text>
<text x="490" y="24" text-anchor="middle" fill="#5b6874" font-size="12.5">각 칸은 앞 칸에서 식으로 계산하고, 칸마다 정해진 크기의 잡음을 더한다</text>
</g></svg>'''

mat_rows = ''.join(f'<tr><td><b>{v["ko"]}</b></td><td>{v["rho"]}</td><td>{v["regain"]}</td><td>{v["E"]}</td><td>{v["dfib"]}</td><td>{v["resil"]}</td><td>{v["mu0"]}</td><td>{v["kth"]}</td><td>{v["tribo"]:+.2f}</td></tr>' for v in MG.MATERIALS.values())
matt = ('<div class="tw"><table class="tb"><tr><th>소재</th><th>밀도 g/cm³</th><th>표준 수분율 %</th><th>섬유 탄성률 GPa</th><th>섬유 지름 μm</th><th>회복 경향</th><th>기준 마찰계수</th><th>열 전달 계수</th><th>대전 서열 점수</th></tr>'
        + mat_rows + f'<tr><td><b>상대 전극</b></td><td colspan="7" class="small">측정 프로토콜에서 고정: {MG.COUNTER["name"]}</td><td>{MG.COUNTER["tribo"]:+.2f}</td></tr></table></div>')
stru_rows = [
 ('평직', '제직', '경·위사가 한 올씩 교차, 교차가 가장 많음', '커버 팩터 합 20~28 (막힘 한계 32)', '실 간격 × 1', '1.00'),
 ('능직 2/2', '제직', '두 올씩 건너뛰며 사선 — 뜬 실이 길다', '22~32 (막힘 한계 36)', '실 간격 × 2', '1.25'),
 ('호프색 2/2', '제직', '두 올을 한 묶음으로 평직처럼', '22~32 (막힘 한계 36)', '실 간격 × 2', '1.30'),
 ('싱글 저지', '편직', '실 고리를 한 방향으로 엮음, 앞뒤가 다름', '조임 계수 TF = √tex ÷ 루프 길이(mm), 1.2~1.7', '웨일 간격', '1.15'),
 ('니들펀치 부직포', '부직', '실 없이 섬유망을 바늘로 얽음', '평량 40~200 g/m², 고형률 0.06~0.20', '섬유망 요철', '0.90'),
]
strt = '<div class="tw"><table class="tb"><tr><th>구조</th><th>방식</th><th>제작 메커니즘</th><th>밀도를 정하는 인자 (생성 범위)</th><th>표면 요철 주기</th><th>실-실 접촉 표면 계수</th></tr>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in stru_rows) + '</table></div>'

items_rows = [
 ('W 평량', '실 질량의 합 (굴곡만큼 실이 더 들어감)', '제직 (EPC·tex·(1+c₁) + PPC·tex·(1+c₂)) / 10<br>편직 S·l·tex / 10, 부직 설계값', 'G1 G3'),
 ('SRA 거칠기 진폭 앞·뒤', '실 지름 × 뜬 길이 효과, 밀도가 막힘에 가까울수록 평평', '0.18·d·(1+0.6(float−1))·(1−0.35·K/K_jam), 능직 앞면 +15% / 편직 뒷면 ×1.3', 'G1 G2'),
 ('SRW 거칠기 파장 앞·뒤', '표면 요철의 반복 주기', '실 간격 × 뜬 길이 (편직: 웨일 간격)', 'G1 G3'),
 ('SFC 마찰계수 앞·뒤', 'Howell형 마찰 F = a·Nⁿ, 요철이 클수록 맞물림 증가', 'μ = μ₀(소재) · (1 + 0.25·ln(SRA/20))', 'G6 G7'),
 ('BAR 굽힘 강성 앞·뒤', '섬유 탄성률 × 섬유 단면 관성 합 × 폭당 실 수, 교차가 적으면 유연', '∝ E · tex · (d_f/15)² · 밀도, 뜬 실 구조 ×0.8, 편직 ×0.45', 'G1 G7'),
 ('BW 굽힘 일 (앞·뒤 × L·C)', '방향별 굽힘 강성 × 굽힘 범위', '경사(L)·위사(C) 밀도 비, 편직 웨일 방향 ×1.5, 부직 MD/CD 1.3', 'G7'),
 ('CW 압축 일 앞·뒤', 'van Wyk 계열: 공극이 많고 섬유가 유연할수록 압축 일 큼', '0.9 · t · (1−φ)² · (10/(E+2))^0.3, φ = 평량 / (두께·밀도·1000)', 'G4 G5'),
 ('CRR 압축 회복률 앞·뒤', '섬유 회복성(울·나일론 큼, 면 작음) × 구조(편직 > 제직 > 부직)', '100 · (0.25 + 0.55·회복 경향) · 구조 계수', 'G4 G7'),
 ('Qmax 접촉 냉온감 앞·뒤', '충전율·열 전달이 클수록, 거칠수록(접촉 면적 작음) 작음, 수분율이 크면 약간 큼', '0.18 · k_th · √φ · (1 − 0.25·log₁₀(SRA/10)) · (1 + 0.02·수분율)', 'G7'),
]
itemst = '<div class="tw"><table class="tb"><tr><th>항목 (공통 19개)</th><th>메커니즘</th><th>생성 식 (요약)</th><th>근거</th></tr>' + ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td class="small">{c}</td><td>{gc(*d.split())}</td></tr>' for a, b, c, d in items_rows) + '</table></div>'

P = MG.PROTOCOL
prott = ('<div class="tw"><table class="tb"><tr><th>측정 조건 (고정)</th><th>값</th><th>왜 고정하나</th></tr>'
 f'<tr><td>접촉 방식 · 상대 전극</td><td>접촉-분리 · {MG.COUNTER["name"]}</td><td>대전량은 상대 물질에 따라 부호와 크기가 바뀜{gc("M1","G8")}</td></tr>'
 f'<tr><td>간격 x · 전극 면적 S</td><td>{P["gap_mm"]} mm · {P["area_cm2"]} cm²</td><td>Voc ∝ x, Q ∝ S{gc("M2")}</td></tr>'
 f'<tr><td>누르는 압력 · 주파수</td><td>{P["pressure_kpa"]} kPa · {P["freq_hz"]} Hz</td><td>출력은 실접촉 면적을 따라 압력에 따라 늘다 포화{gc("G11")}</td></tr>'
 f'<tr><td>상대습도</td><td>{P["rh_mean"]:.0f} ± {P["rh_sd"]:.0f} % (ISO 139 표준 상태)</td><td>습도가 높으면 대전량 감소{gc("G9","M5")}</td></tr>'
 f'<tr><td>반복 측정</td><td>{P["repeats"]}회 평균 + 변동계수</td><td>Y는 엄격한 정답이 아닌 관측값 — 오차 범위를 함께 기록</td></tr></table></div>')

piv = _df.pivot_table(index='material', columns='structure', values='Voc_V', aggfunc='median')
cols = ['plain', 'twill22', 'hopsack22', 'jersey', 'needle']
vmax = float(piv.values.max())
heat = ('<div class="tw"><table class="tb mk-heat"><tr><th>Voc 중앙값 (V, 모의)</th>' + ''.join(f'<th>{MG.STRUCTURES[c]["ko"]}</th>' for c in cols) + '</tr>'
        + ''.join(f'<tr><td><b>{MG.MATERIALS[m]["ko"]}</b></td>' + ''.join(f'<td class="h" style="background:rgba(201,48,44,{0.08 + 0.6 * piv.loc[m, c] / vmax:.2f})">{piv.loc[m, c]:.1f}</td>' for c in cols) + '</tr>' for m in ['nylon', 'wool', 'cotton', 'polyester', 'pp'])
        + '</table></div>')
n_rows = len(_df)
sp = _df[['SRA_F', 'CW_F', 'Qmax_F', 'W', 'Voc_V']].corr(method='spearman')['Voc_V']

calc_consts = _json.dumps(dict(M=MG.MATERIALS, S=MG.STRUCTURES, C=MG.COUNTER, P=MG.PROTOCOL, s0=MG.SIGMA0_UC, sopt=MG.SRA_OPT), ensure_ascii=False)
calc = r"""
<div class="mk-calc" id="mkCalc">
 <div>
  <label>소재</label><select id="mkM"></select>
  <label>구조 (제작 방법)</label><select id="mkS"></select>
  <div id="mkWov"><label>실 선밀도 tex <span class="v" id="mkTexV"></span></label><input type="range" id="mkTex" min="10" max="50" step="1" value="25">
   <label>커버 팩터 합 K <span class="v" id="mkKV"></span></label><input type="range" id="mkK" min="20" max="32" step="0.5" value="25">
   <label>경사 비중 <span class="v" id="mkWsV"></span></label><input type="range" id="mkWs" min="0.45" max="0.6" step="0.01" value="0.52"></div>
  <div id="mkKnit"><label>실 선밀도 tex <span class="v" id="mkKtexV"></span></label><input type="range" id="mkKtex" min="10" max="40" step="1" value="20">
   <label>조임 계수 TF <span class="v" id="mkTfV"></span></label><input type="range" id="mkTf" min="1.2" max="1.7" step="0.01" value="1.45"></div>
  <div id="mkNon"><label>평량 g/m² <span class="v" id="mkGV"></span></label><input type="range" id="mkG" min="40" max="200" step="5" value="100">
   <label>고형률 <span class="v" id="mkSolV"></span></label><input type="range" id="mkSol" min="0.06" max="0.2" step="0.005" value="0.12"></div>
  <label>상대습도 % <span class="v" id="mkRhV"></span></label><input type="range" id="mkRh" min="30" max="90" step="1" value="65">
 </div>
 <div><div class="mk-out" id="mkOut"></div><p class="small muted" id="mkWarn" style="margin:8px 0 0"></p></div>
</div>
<script>
(function(){var C=@@C@@,$=function(i){return document.getElementById(i)};if(!$('mkCalc'))return;
var M=C.M,S=C.S,P=C.P;
Object.keys(M).forEach(function(k){$('mkM').add(new Option(M[k].ko,k))});Object.keys(S).forEach(function(k){$('mkS').add(new Option(S[k].ko,k))});$('mkS').value='twill22';$('mkM').value='nylon';
function yd(tex,rho){var a=tex*1e-5/(rho*0.6);return Math.sqrt(4*a/Math.PI)*10}
function compute(d){var m=M[d.material],s=S[d.structure],o={},dy,gsm,t,srw,sra,dL,dC;
 if(s.kind==='woven'){dy=yd(d.tex,m.rho);var K1=d.cover*d.warp_share,K2=d.cover-K1,epc=K1*10/Math.sqrt(d.tex),ppc=K2*10/Math.sqrt(d.tex),p1=10/epc,p2=10/ppc,c1=0.9*s.interl*Math.pow(dy/p2,2),c2=0.9*s.interl*Math.pow(dy/p1,2);
  gsm=(epc*d.tex*(1+c1)+ppc*d.tex*(1+c2))/10;t=2*dy*(1+0.12*(s.float-1));srw=p1*s.float;sra=dy*1000*0.18*(1+0.6*(s.float-1))*(1-0.35*Math.min(d.cover/s.jam,1));dL=epc;dC=ppc;o.epc=epc;o.ppc=ppc;o.jam=d.cover/s.jam}
 else if(s.kind==='knit'){dy=yd(d.tex,m.rho);var l=Math.sqrt(d.tex)/d.tf,cpc=d.kc/(l/10),wpc=d.kw/(l/10);gsm=cpc*wpc*(l/10)*d.tex/10;t=2.2*dy;srw=10/wpc;sra=dy*1000*0.22;dL=wpc;dC=cpc;o.loop=l;o.cpc=cpc;o.wpc=wpc}
 else{dy=m.dfib/1000;gsm=d.gsm;t=gsm/(m.rho*d.solidity*1000);srw=0.8+3*(1-d.solidity);sra=6+60*(1-d.solidity)*(m.dfib/15);dL=1.3;dC=1.0}
 var phi=gsm/(t*m.rho*1000),k=s.kind,fb={woven:[1+0.15*(s.float-1),1-0.10*(s.float-1)],knit:[0.85,1.3],nonwoven:[1,1.1]}[k],sf=sra*fb[0],sb=sra*fb[1];
 var mu=function(x){return m.mu0*(1+0.25*Math.log(Math.max(x,1)/20))},b0;
 if(k==='nonwoven')b0=m.E*Math.pow(m.dfib/15,2)*gsm/100*(0.6+2*d.solidity);else b0=m.E*d.tex/20*Math.pow(m.dfib/15,2)*(k==='woven'?1:0.45);
 var bL,bC;if(k==='woven'){bL=b0*dL/25*(s.float===1?1:0.8);bC=b0*dC/25*(s.float===1?1:0.8)}else if(k==='knit'){bL=b0*1.5*dL/12;bC=b0*dC/15}else{bL=b0*dL;bC=b0*dC}
 var cw=0.9*t*Math.pow(1-phi,2)*Math.pow(10/(m.E+2),0.3),crr=100*(0.25+0.55*m.resil)*{woven:0.95,knit:1.05,nonwoven:0.85}[k];
 var q=function(x){return 0.18*m.kth*Math.sqrt(phi)*(1-0.25*Math.log(Math.max(x,1)/10)/Math.log(10))*(1+0.02*m.regain)};
 var v={W:gsm,SFC_F:mu(sf),SFC_B:mu(sb),SRA_F:sf,SRA_B:sb,SRW_F:srw,SRW_B:srw*(k==='knit'?1.15:1),BAR_F:(bL+bC)/2,BW_FL:bL*0.9,BW_FC:bC*0.9,CW_F:cw,CRR_F:crr,Qmax_F:q(sf),Qmax_B:q(sb)};
 var dtr=m.tribo-C.C.tribo,gr=Math.exp(-Math.pow(Math.log(sf/C.sopt),2)/(2*0.64)),ps=6/(1+4*cw),ci=s.surf*gr*(1-Math.exp(-P.pressure_kpa/ps)),beta=0.25*(1+m.regain/10),hum=Math.max(0.05,1-beta*(d.rh-40)/100);
 var sig=C.s0*dtr*ci*hum,voc=sig*1e-6*(P.gap_mm/1000)/8.854e-12,qn=sig*1e-6*P.area_cm2*1e-4*1e9;
 return {st:o,dy:dy,gsm:gsm,t:t,phi:phi,v:v,y:{sigma:sig,Voc:voc,Q:qn,I:2*qn*P.freq_hz,ci:ci,hum:hum,dtr:dtr,gr:gr}}}
window.MKcompute=compute;
function f(x,n){return (Math.abs(x)>=100?x.toFixed(0):x.toFixed(n==null?2:n))}
function box(t,rows){return '<div class="tw"><table class="tb"><tr><th colspan="2">'+t+'</th></tr>'+rows.map(function(r){return '<tr><td>'+r[0]+'</td><td style="text-align:right;font-variant-numeric:tabular-nums">'+r[1]+'</td></tr>'}).join('')+'</table></div>'}
function run(){var mk=$('mkM').value,sk=$('mkS').value,k=S[sk].kind;$('mkWov').style.display=k==='woven'?'':'none';$('mkKnit').style.display=k==='knit'?'':'none';$('mkNon').style.display=k==='nonwoven'?'':'none';
 $('mkK').min=S[sk].Kmin||20;$('mkK').max=S[sk].Kmax||32;
 var d={material:mk,structure:sk,rh:+$('mkRh').value,tex:+(k==='knit'?$('mkKtex').value:$('mkTex').value),cover:+$('mkK').value,warp_share:+$('mkWs').value,tf:+$('mkTf').value,kc:5.1,kw:4.05,gsm:+$('mkG').value,solidity:+$('mkSol').value};
 ['Tex','K','Ws','Ktex','Tf','G','Sol','Rh'].forEach(function(n){$('mk'+n+'V').textContent=$('mk'+n).value});
 var r=compute(d),st=[['실(섬유) 지름',f(r.dy*1000,0)+' μm'],['평량',f(r.gsm,1)+' g/m²'],['두께',f(r.t,3)+' mm'],['충전율 φ',f(r.phi,3)]];
 if(k==='woven')st.push(['경·위 밀도',f(r.st.epc,1)+' · '+f(r.st.ppc,1)+' 올/cm'],['막힘 한계 대비',f(r.st.jam*100,0)+'%']);if(k==='knit')st.push(['루프 길이',f(r.st.loop,2)+' mm'],['웨일·코스',f(r.st.wpc,1)+' · '+f(r.st.cpc,1)+' /cm']);
 var v=r.v,ph=[['마찰계수 SFC 앞·뒤',f(v.SFC_F,3)+' · '+f(v.SFC_B,3)],['거칠기 SRA 앞·뒤',f(v.SRA_F,1)+' · '+f(v.SRA_B,1)],['거칠기 파장 SRW',f(v.SRW_F,2)],['굽힘 BAR',f(v.BAR_F,2)],['굽힘 일 BW L·C',f(v.BW_FL,2)+' · '+f(v.BW_FC,2)],['압축 일 CW',f(v.CW_F,3)],['압축 회복 CRR',f(v.CRR_F,1)+'%'],['냉온감 Qmax 앞',f(v.Qmax_F,3)]];
 var y=r.y,yy=[['<b>Voc</b>','<b>'+f(y.Voc,1)+' V</b>'],['전하 Q',f(y.Q,3)+' nC'],['평균 전류',f(y.I,2)+' nA'],['표면 전하 밀도 σ',f(y.sigma,3)+' μC/m²'],['서열 차 (대 PTFE)',f(y.dtr,2)],['거칠기 계수 (역U자)',f(y.gr,2)],['실접촉 지수',f(y.ci,2)],['습도 계수',f(y.hum,2)]];
 $('mkOut').innerHTML=box('③ 구조',st)+box('④ 물성 X (일부)',ph)+box('⑤ 전기 특성 Y',yy);
 $('mkWarn').textContent=(k==='woven'&&r.st.jam>0.98?'⚠ 막힘 한계를 넘어 실제로 짤 수 없는 조합입니다(생성기에서는 버림). ':'')+'잡음 없는 "참값"입니다. 생성기는 여기에 원단 간 변동 6%, 물성 측정 오차 4%, 전기 측정 오차 12%를 더합니다.'}
document.querySelectorAll('#mkCalc select,#mkCalc input').forEach(function(e){e.addEventListener('input',run)});run();
})();
</script>""".replace('@@C@@', calc_consts)

refl2 = '<ol class="refl">' + ''.join(f'<li id="{k}"><b>[{k}]</b> {c}' + (f' <a href="{u}" target="_blank" rel="noopener">링크</a>' if u else '') + f'<span class="why">이 가이드에서: {w}</span></li>' for k, c, u, w in MREF2) + '</ol>'

mk_body = MK_CSS + wrap(crumb(('index.html', 'INDEX'), ('data_guide.html', '가상 섬유 데이터 작성 가이드'), (None, '모의 데이터 생성 가이드')) +
 '<h1 style="margin:4px 0 8px">섬유 메커니즘 기반 모의 데이터 생성 가이드 — 소재·제작 방법에서 전기 특성 Y까지</h1>'
 '<p class="lead">섬유직물의 모의 데이터를 "숫자를 아무렇게나 흩뿌려" 만들지 않고, <b>섬유 → 실 → 직물 구조 → 물성 → 전기 특성</b>으로 이어지는 제작 메커니즘을 식으로 따라가며 만드는 방법입니다. 각 칸의 식은 섬유공학의 고전 이론과 마찰전기 문헌에 근거를 두었고, Y는 섬유직물의 전기 데이터(마찰전기 출력, 연속변수)입니다.</p>'
 '<div class="brief"><div class="bh">핵심 보고</div><dl>'
 '<dt>방법</dt><dd>소재 5종 × 구조 5종 칸마다 라틴 하이퍼큐브로 설계 인자를 뽑고' + gc('G12') + ', 구조 이론으로 평량·두께·충전율을 계산한 뒤' + gc('G1', 'G3') + ', 19개 공통 물성과 전기 특성 Y를 메커니즘 식으로 만들고 세 층의 잡음을 더합니다.</dd>'
 '<dt>Y</dt><dd>접촉-분리형 마찰전기 이론' + gc('M2') + ': Voc = σ·x/ε₀. 표면 전하 밀도 σ = 규모 계수 × 대전 서열 차' + gc('G8') + ' × 실접촉 지수' + gc('G11', 'M3') + ' × 습도 계수' + gc('G9') + '.</dd>'
 '<dt>결과</dt><dd>기본 설정으로 ' + str(n_rows) + '개 원단(막힘 한계를 넘는 조합 제외)을 만들었습니다. 같은 소재에서 능직·호프색이 평직보다 출력이 높고, 소재는 나일론 > 울 > 면 > 폴리에스터 > 폴리프로필렌 순입니다. 문헌이 말하는 방향을 재현하도록 계수를 맞춘 결과입니다.</dd>'
 '<dt class="ask">요청</dt><dd>① 소재 대표값과 구조 범위가 실험실이 만들 수 있는 범위와 맞는지, ② 전기 측정 프로토콜 고정값(상대 전극·간격·압력·습도), ③ 모의 데이터의 쓰임을 "파이프라인 시험·실험계획"으로 한정하는 원칙을 검토해 주십시오.</dd></dl></div>'
 + say('asst', 'report', '교수님, 이 데이터는 실측이 모이기 전에 분석 도구와 생성 모델을 미리 시험하려는 연습용입니다. 식에 넣은 관계를 모델이 되찾는지 확인하는 용도이며, 연구 결과로는 쓰지 않습니다.')
 + '<div class="panel">' + chain_svg + '</div>') + \
 wrap('<h2 id="use">0. 쓰임과 금지 — 먼저 정하는 원칙</h2><div class="pair">'
 '<div><span class="tag nn">쓰는 곳</span><p>① 분석 파이프라인(입력 양식·품질 검사·모델 학습·평가) 시험, ② 생성 모델이 알려진 관계를 되찾는지 점검(정답을 아는 시험), ③ 실험계획 — 어떤 인자 범위에서 Y가 크게 바뀌는지 미리 보고 실측 원단을 고르는 데.</p></div>'
 '<div><span class="tag fly">쓰지 않는 곳</span><p>① 연구 결과·논문 근거, ② 실측과 섞어 학습(섞을 때는 is_mock 열로 반드시 구분), ③ 성능 보고 — 성적은 실측 원단으로만 잽니다' + gc('M11') + '. 모델이 모의 데이터에서 찾은 관계는 우리가 식에 넣은 가정일 뿐입니다.</p></div></div>') + \
 wrap('<h2 id="design">1. 설계 인자 — 소재와 제작 방법</h2>'
 '<h3>소재(섬유) 대표값</h3><p class="small muted">교과서 수준의 대표값입니다. 대전 서열 점수는 직물 대전 서열(나일론 > 면 > 폴리에스터 > 폴리프로필렌 > PTFE)' + gc('G8') + '을 순서 점수로 옮긴 가정값이며, 울은 문헌마다 위치가 달라 불확실성이 큽니다. 실험실에서 쓰는 실의 시험 성적서 값으로 바꿔 넣습니다.</p>' + matt +
 '<h3>구조(제작 방법)</h3>' + strt +
 '<p class="small">능직은 교차가 적어 평직보다 실을 더 촘촘히 넣을 수 있어(조직 계수)' + gc('G2') + ' 막힘 한계를 높게 두었습니다. 평직은 커버 팩터 16+16 근처에서 막혀 아주 강한 직기가 필요하다고 알려져 있습니다.</p>') + \
 wrap('<h2 id="geom">2. 구조 계산 — 실과 직물의 기하</h2>'
 '<p>Peirce는 제직물을 실 지름·간격·굴곡·커버·두께·평량이 서로 묶인 기하 체계로 다뤘습니다' + gc('G1') + '. 생성기는 이 관계를 단순화해 씁니다.</p>'
 '<div class="mk-eq">실 지름 d = √( 4 · tex·10⁻⁵ / (π · ρ_f · 0.6) )  [cm]   ← 단면적 = 선밀도 ÷ (섬유 밀도 × 충전율 0.6)<br>'
 '커버 팩터(SI) K = 올/cm × √tex / 10   →   경사 밀도 EPC = K₁ · 10 / √tex<br>'
 '굴곡률 c ≈ 0.9 · 교차 비율 · (d / 맞은편 실 간격)²   (평직 교차 비율 1, 능직·호프색 0.5)<br>'
 '평량 W = ( EPC · tex · (1+c₁) + PPC · tex · (1+c₂) ) / 10   [g/m²]<br>'
 '두께 t ≈ 2d · (1 + 0.12·(뜬 길이 − 1)),   충전율 φ = W / (t · ρ_f · 1000)</div>'
 '<p>편직은 Munden의 관계를 씁니다. 코스·웨일 밀도는 루프 길이에 반비례하고 그 상수는 조임과 무관합니다' + gc('G3') + '.</p>'
 '<div class="mk-eq">루프 길이 l = √tex / TF  [mm]  (조임 계수 TF 1.2~1.7)<br>코스/cm = K_c / l,  웨일/cm = K_w / l  (l: cm, K_c ≈ 4.8~5.4, K_w ≈ 3.8~4.3)<br>평량 W = 코스 · 웨일 · l · tex / 10</div>'
 '<p>부직포는 평량과 고형률(섬유가 차지하는 부피 비)로 두께를 정합니다.</p><div class="mk-eq">두께 t = W / (ρ_f · 고형률 · 1000)  [mm]</div>'
 '<p><b>제작 가능성 필터</b> — 제직은 막힘 한계의 98%를 넘으면, 편직은 TF가 1.15~1.75 밖이면, 부직은 충전율이 0.03~0.30 밖이면 버립니다. 실험실이 실제로 만들 수 없는 직물이 데이터에 들어가지 않게 하는 장치입니다.</p>') + \
 wrap('<h2 id="items">3. 물성 19항목 — 메커니즘 식</h2>'
 '<p>실측 엑셀의 27개 원단 모두에 있는 19개 항목과 같은 이름으로 만듭니다. 그래서 실측이 들어오면 같은 파이프라인에 그대로 넣을 수 있습니다.</p>' + itemst +
 '<p class="small muted">섬유·직물 마찰은 Amontons 법칙(F/N = 일정)이 맞지 않고 F = a·Nⁿ 꼴을 따릅니다' + gc('G6') + '. 압축은 van Wyk의 섬유 집합체 이론' + gc('G4') + '과 이를 직물에 적용한 모델' + gc('G5') + '의 방향을 따랐습니다. 단위는 FTT 출력 단위에 맞춰 실측으로 보정합니다.</p>') + \
 wrap('<h2 id="y">4. 전기 특성 Y — 마찰전기 출력</h2>'
 '<div class="mk-eq">σ = σ₀ · (대전 서열 점수_소재 − 점수_PTFE) · 실접촉 지수 · 습도 계수   [μC/m²]<br>'
 'Voc = σ · x / ε₀,   Q = σ · S,   평균 전류 = 2 · Q · f<br>'
 '실접촉 지수 = 표면 계수(구조) · g(SRA) · (1 − e^(−P / P*)),   P* = 6 / (1 + 4·CW)<br>'
 'g(SRA) = exp( −(ln(SRA / SRA_opt))² / (2·0.8²) )   ← 역U자,  SRA_opt = ' + f'{MG.SRA_OPT:g}' + ' μm<br>'
 '습도 계수 = 1 − β · (RH − 40)/100,   β = 0.25 · (1 + 수분율/10)</div>'
 '<div class="pair"><div><span class="tag nn">거칠기를 역U자로 둔 이유</span><p>직물 TENG에서는 능직·호프색이 접촉 표면적과 거칠기가 커서 평직보다 출력이 높았습니다' + gc('M3', 'M4') + '. 반면 평평한 탄성 표면에서는 거칠기가 커질수록 실접촉 면적과 출력이 줄었습니다' + gc('G10') + '. 두 결과를 함께 담으려면 "적당한 요철에서 최대"인 모양이 필요합니다.</p></div>'
 '<div><span class="tag fly">압력과 습도</span><p>출력은 실접촉 면적을 따라 압력이 커질수록 늘다가 포화합니다' + gc('G11') + '. 그래서 압축이 쉬운 직물(CW 큼)은 낮은 압력에서 포화하게 했습니다. 상대습도는 90%에서 10%로 내리면 전하가 20% 넘게 늘었다는 보고' + gc('G9') + '에 맞춰 기울기를 정했고, 흡습성 섬유(울·면)가 더 민감하게 했습니다.</p></div></div>'
 '<h3>측정 프로토콜 — Y를 직물의 성질로 만드는 고정값</h3>' + prott +
 '<p class="small muted">규모 계수 σ₀ = ' + f'{MG.SIGMA0_UC:g}' + ' μC/m²와 SRA_opt는 실측 첫 원단 10개 안팎으로 보정합니다. 보정 전의 Voc 크기(수 V~100 V)는 자리표일 뿐입니다.</p>') + \
 wrap('<h2 id="noise">5. 잡음 세 층 — "정답이 아닌 관측값"을 흉내 내기</h2>'
 '<div class="tw"><table class="tb"><tr><th>층</th><th>크기</th><th>뜻</th></tr>'
 '<tr><td>원단 간 변동</td><td>로그정규, CV 6%</td><td>같은 설계라도 실·가공 차이로 생기는, 식이 설명하지 못하는 몫</td></tr>'
 '<tr><td>물성 측정 오차</td><td>CV 4% × 3회 평균</td><td>FTT·KES 반복 측정의 흔들림</td></tr>'
 '<tr><td>전기 측정 오차</td><td>CV 12% × 3회 평균, 변동계수 열 함께 저장</td><td>마찰전기는 표면 상태·잔류 전하에 민감해 더 크게 흔들림</td></tr>'
 '<tr><td>측정 환경</td><td>상대습도 65 ± 2%</td><td>표준 상태 안에서의 흔들림이 습도 계수로 Y에 들어감</td></tr></table></div>'
 '<p class="small">세 층을 나눠 두면 "모델의 오차가 측정 오차 수준까지 내려왔는가"를 판단할 수 있습니다. 측정 오차보다 작은 오차는 과적합 신호입니다.</p>') + \
 wrap('<h2 id="steps">6. 생성 절차 8단계</h2><ol>'
 '<li><b>설계 공간 정하기</b> — 소재·구조 목록과 연속 인자 범위(1절 표). 실험실이 만들 수 있는 범위로.</li>'
 '<li><b>표본 추출</b> — 소재 × 구조 칸마다 라틴 하이퍼큐브' + gc('G12') + '. 칸마다 같은 수(기본 20)로 균형을 맞춥니다.</li>'
 '<li><b>구조 계산</b> — 2절 식으로 실 지름·밀도·평량·두께·충전율.</li>'
 '<li><b>제작 가능성 필터</b> — 막힘 한계·조임 계수·충전율 범위 밖은 버림.</li>'
 '<li><b>물성 19항목</b> — 3절 식 + 원단 간 변동 + 측정 오차.</li>'
 '<li><b>전기 특성 Y</b> — 4절 식 + 습도 + 전기 측정 오차, 반복 3회 평균과 변동계수.</li>'
 '<li><b>품질 검사</b> — 7절 표.</li>'
 '<li><b>기록</b> — 시드, 생성기 버전, 가정 표(변수 사전 JSON)를 데이터와 함께 저장. 모든 행에 is_mock = True.</li></ol>'
 '<p><b>실측이 들어오면</b> — 27개 원단의 19항목 분포에 맞춰 각 항목의 단위·규모를 분위수로 맞추고, 전기 특성을 잰 원단으로 σ₀ → SRA_opt → 습도 기울기 순으로 보정합니다. 보정한 생성기는 S4의 생성 모델과 비교하는 "물리 기반 기준선"이 됩니다.</p>') + \
 wrap('<h2 id="qc">7. 품질 검사 — 메커니즘이 살아 있는지</h2>'
 '<div class="tw"><table class="tb"><tr><th>검사</th><th>기준</th><th>이번 결과 (기본 설정)</th></tr>'
 f'<tr><td>범위</td><td>평량·두께·밀도가 실제 직물 범위 안</td><td>제직 평량 중앙값 {_df[_df.kind=="woven"].W.median():.0f}, 편직 {_df[_df.kind=="knit"].W.median():.0f}, 부직 {_df[_df.kind=="nonwoven"].W.median():.0f} g/m²</td></tr>'
 f'<tr><td>구조 순서</td><td>같은 소재에서 능직·호프색 ≥ 평직{gc("M3","M4")}</td><td>나일론 평직 {piv.loc["nylon","plain"]:.0f} V &lt; 능직 {piv.loc["nylon","twill22"]:.0f} V · 호프색 {piv.loc["nylon","hopsack22"]:.0f} V</td></tr>'
 f'<tr><td>소재 순서</td><td>대 PTFE에서 나일론 > 면 > 폴리에스터 > PP{gc("G8")}</td><td>평직 기준 {piv.loc["nylon","plain"]:.0f} > {piv.loc["cotton","plain"]:.0f} > {piv.loc["polyester","plain"]:.0f} > {piv.loc["pp","plain"]:.0f} V</td></tr>'
 f'<tr><td>측정 흔들림</td><td>Voc 반복 변동계수 중앙값 ≈ 10%</td><td>{_df.Voc_cv.median()*100:.0f}%</td></tr>'
 '<tr><td>실측 분포 비교</td><td>19항목 각각 실측 27개와 분포 비교(분위수 그림, KS 검정)</td><td>실측 엑셀 연결 후 실행</td></tr></table></div>'
 '<h3>미리보기 — 소재 × 구조별 Voc 중앙값</h3>' + heat +
 f'<p class="small muted">순위 상관(Spearman, 모의 {n_rows}개): Voc와 Qmax {sp["Qmax_F"]:+.2f}, 거칠기 SRA {sp["SRA_F"]:+.2f}, 압축 일 CW {sp["CW_F"]:+.2f}, 평량 W {sp["W"]:+.2f}. 이 상관은 식이 만든 것이며, 특히 Qmax와 Y의 상관은 둘 다 거칠기에 기대어 생긴 간접 상관입니다. 실측에서도 같은지 확인할 대상입니다.</p>') + \
 wrap('<h2 id="calc">8. 한 원단 만들어 보기 — 메커니즘 계산기</h2><p>소재와 구조, 인자를 바꾸면 2~4절의 식으로 구조·물성·전기 특성이 바로 계산됩니다(잡음 없는 참값). 생성기 파이썬 코드와 같은 식입니다.</p>' + calc) + \
 wrap('<h2 id="files">9. 파일</h2><ul>'
 '<li><a href="analysis/mock_data/generate_mock_fabric.py">generate_mock_fabric.py</a> — 생성기. <code>python3 generate_mock_fabric.py [칸당 수] [시드] [출력 폴더]</code></li>'
 f'<li><a href="analysis/mock_data/mock_fabric_data.csv">mock_fabric_data.csv</a> — 기본 설정 결과 {n_rows}행. 설계 인자, 구조량, 19항목(실측과 같은 이름), Voc·Q·평균 전류·σ, 습도, is_mock</li>'
 '<li><a href="analysis/mock_data/mock_fabric_dictionary.json">mock_fabric_dictionary.json</a> — 소재·구조 대표값, 측정 프로토콜, 보정 계수, 버전</li></ul>'
 + say('moa', 'think', '모의 데이터로 생성 모델을 먼저 돌려 보면 무엇을 알 수 있습니까?')
 + say('asst', 'report', '정답을 아는 시험이 됩니다. 우리가 넣은 관계, 예를 들어 능직이 평직보다 출력이 높다는 관계를 모델이 되찾지 못하면 실측에서도 찾기 어렵습니다. 그리고 원단 몇 개면 관계가 보이는지를 미리 재 볼 수 있어, S2에서 몇 개를 만들지 정하는 데 씁니다.')) + \
 wrap('<h2 id="gref">근거 문헌</h2><p class="small muted">M로 시작하는 번호는 <a href="method_review.html#mrefs">1차년도 연구 방법 검토</a>의 문헌입니다. 원문 전체가 아니라 초록·서지·검색 결과로 확인한 범위에서 인용했으며, "확인 필요" 표시는 서지 일부를 더 확인해야 하는 항목입니다.</p>' + refl2)

sizes['mock_data_guide.html'] = page('mock_data_guide.html', '모의 데이터 생성 가이드', mk_body + tail((('data_guide.html', '가상 섬유 데이터 작성 가이드'), ('slides/index.html', '웹 슬라이드 — 데이터 생성·검증·실습'))))
