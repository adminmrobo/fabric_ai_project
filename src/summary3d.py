# INDEX의 SUMMARY — 1차년도 방법을 3D로: 실측 → 패턴 학습 → 새 직물 생성 → 전기 특성 예측 → 일부 검증
# 외부 라이브러리 없이 canvas에 직접 원근 투영으로 그린다. 데이터는 설명용 모형(가상).

CSS = r"""
.s3d{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:16px;align-items:start}
.s3d .cv{position:relative;border:1px solid var(--rule);border-radius:12px;background:#fff;overflow:hidden}
.s3d canvas{display:block;width:100%;height:470px;cursor:grab;touch-action:none}
.s3d canvas:active{cursor:grabbing}
.s3d .hint{position:absolute;left:10px;bottom:8px;font-size:12px;color:var(--muted);background:rgba(255,255,255,.85);padding:1px 6px;border-radius:4px}
.s3d .side h5{margin:0 0 6px;font-size:15px}
.s3d .steps3 button{display:block;width:100%;text-align:left;margin:0 0 6px}
.s3d .steps3 button b{display:inline-block;width:22px}
.s3d .exp{font-size:14px;line-height:1.7;background:#f7f9fb;border:1px solid var(--rule);border-radius:10px;padding:10px 12px;min-height:120px}
.s3d .lg{font-size:12.5px;line-height:1.9;margin-top:8px}
.s3d .lg i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:-1px}
@media (max-width:900px){.s3d{grid-template-columns:1fr}.s3d canvas{height:380px}}
"""

import json, os

def _data():
    d = json.load(open(os.path.join(os.path.dirname(__file__), 'data.json'), encoding='utf-8'))
    S = [{'id': s['id'], 'src': s['src'], 'type': s['type'], 'cov': s['cov'], 'pc': s['pc']} for s in d['samples']]
    return json.dumps({'S': S, 'gsize': d['gsize'], 'ev': d['ev']}, ensure_ascii=False, separators=(',', ':'))

HTML_T = r"""
<section class="level" id="ai-summary"><div class="wrap">
<h2>SUMMARY — 실측 직물 데이터로 보는 1차년도 방법: 패턴을 배운 생성 모델로 새 직물을 만들고, 전기 특성(연속변수)을 예측하기</h2>
<p class="lead">처음 화면은 마지막 단계 ⑥(가상 예측값)입니다. 받은 엑셀의 원단 27개를 3D로 그대로 세웠습니다. ①~④는 <b>실측 · 엑셀 직접 집계</b>이고, ⑤⑥은 전기 특성을 잰 뒤에 할 일을 같은 원단 위에 <b>가상 값</b>으로 미리 그려 본 것입니다. 그림을 끌면 돌아가고, 막대나 점에 마우스를 올리면 값이 나옵니다.</p>
@@SAY1@@
<div class="s3d">
 <div class="cv"><canvas id="s3dCv" aria-label="3D 그림: 원단 27개와 측정 묶음 9개의 채움 막대, 공통 19항목, 직물 특성 공간, 전기 특성 연속변수 축, 측정 후 계획"></canvas><span class="hint">끌어서 회전 · 휠로 확대 · 올리면 값 표시</span></div>
 <div class="side">
  <h5>단계</h5>
  <div class="steps3" role="group" aria-label="단계">
   <button type="button" class="bt" data-s3="1" aria-pressed="false"><b>①</b>실측 현황 — 원단 27 × 묶음 9</button>
   <button type="button" class="bt" data-s3="2" aria-pressed="false"><b>②</b>27개 모두에 있는 19항목</button>
   <button type="button" class="bt" data-s3="3" aria-pressed="false"><b>③</b>직물 특성 공간 (19항목 PCA)</button>
   <button type="button" class="bt" data-s3="4" aria-pressed="false"><b>④</b>전기 특성 Y — 연속변수, 0개</button>
   <button type="button" class="bt" data-s3="5" aria-pressed="false"><b>⑤</b>측정 후: 패턴 학습·새 직물 <span class="small">(가상)</span></button>
   <button type="button" class="bt" data-s3="6" aria-pressed="false"><b>⑥</b>연속값 예측·일부 검증 <span class="small">(가상)</span></button>
  </div>
  <div class="ctrl" style="margin:4px 0 8px"><button type="button" class="bt sm" id="s3dRot" aria-pressed="true">자동 회전</button> <span class="stampnote" id="s3dTag">실측 · 엑셀 직접 집계</span></div>
  <div class="exp" id="s3dExp" aria-live="polite"></div>
  <div class="lg" id="s3dLg"></div>
 </div>
</div>
@@SAY2@@
<h3 id="inv3" style="margin-top:34px">역방향 보기 — 원하는 전기 특성 Y에서 직물을 예상하기 <span class="stampnote">측정 전 · 가상 값</span></h3>
<p>위 ⑥은 "이 직물이면 Y가 얼마인가"를 봤습니다. 생성 모델은 직물 특성과 Y의 패턴을 함께 배우므로 <b>방향을 뒤집을 수도 있습니다</b>. 원하는 Y 값을 정하면, 그 Y와 함께 나타나는 직물 특성의 분포 p(직물 특성 | Y)에서 후보 직물을 뽑고, 가장 닮은 실측 원단을 찾아 줍니다. 센서용으로 출력이 높은 직물을 설계할 때 쓰는 방향입니다.</p>
<div class="s3d">
 <div class="cv"><canvas id="invCv" aria-label="3D 그림: 목표 전기 특성 높이의 평면, 그 높이에서 예상되는 직물 후보와 바닥의 분포"></canvas><span class="hint">끌어서 회전 · 올리면 값 표시</span></div>
 <div class="side">
  <h5>목표 전기 특성 Y</h5>
  <div class="ctrl" style="margin:0 0 8px"><div class="group"><span class="glabel">Y*</span><input type="range" id="invY" min="0" max="100" step="1" value="80" aria-label="목표 전기 특성"><span class="val" id="invYv"></span></div></div>
  <div class="ctrl" style="margin:0 0 8px"><button type="button" class="bt sm" data-inv="hi">출력 높게</button> <button type="button" class="bt sm" data-inv="mid">중간</button> <button type="button" class="bt sm" data-inv="lo">출력 낮게</button></div>
  <div class="exp" id="invExp" aria-live="polite"></div>
  <div class="lg"><span><i style="background:rgba(214,160,40,.5);border-radius:2px"></i>목표 Y 높이의 평면</span><br><span><i style="background:#d6a028"></i>예상 직물 후보 (p(X | Y*)에서 뽑음)</span><br><span><i style="background:rgba(214,160,40,.25);border-radius:2px"></i>바닥: 후보가 나올 곳 (2σ)</span><br><span><i style="background:#8e78c9"></i>부직포</span> <span><i style="background:#2f5d9e"></i>제직물</span> <span><i style="background:#d8685a"></i>편직물</span> (실측 원단)</div>
 </div>
</div>
<p class="small muted">①②는 <a href="stage_0_kickoff.html#lv1">S0 채움 지도</a>, ③은 <a href="stage_1_explore.html">S1 PCA</a>와 같은 실측 값입니다. ④의 전기 특성 Y는 전압·전류·전하밀도 같은 연속변수이며, 아직 한 개도 측정되지 않았습니다. ⑤⑥의 높이·타원체·새 직물·검증 결과는 측정 전이라 가상 값입니다. 사진을 벡터로 바꾸는 이전 SUMMARY는 2차년도 이미지 쪽(<a href="image_data.html#img-summary">이미지 데이터 분석</a>)으로 옮겼습니다.</p>
</div></section>
<script>
(function(){
var cv=document.getElementById('s3dCv');if(!cv)return;
var D=@@DATA@@,S=D.S,GS=D.gsize.concat([0]);
var GN=['기본 물성','표면 · FTT','역학 · FTT','열 · FTT','표면 · KES','역학 · KES','인장강도','통기·보온','전기 특성 Y'];
var COMMON=[1,6,10,2,0,0,0,0,0];
var TC={Nonwoven:['부직포','#8e78c9'],Woven:['제직물','#2f5d9e'],Knit:['편직물','#d8685a']};
var SRCN={Huvis:'Huvis',Lab:'연구실',Industrial:'산업'};
function rng(s){return function(){s=(s*69069+1)%4294967296;return s/4294967296}}
function gnF(r){return function(){var u=r()||1e-9,v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(6.2832*v)}}
/* ③ 실측 PCA 좌표 → [-1,1] */
var px=S.map(function(s){return s.pc[0]}),pz=S.map(function(s){return s.pc[1]});
var ax=Math.max.apply(0,px.map(Math.abs)),az=Math.max.apply(0,pz.map(Math.abs));
S.forEach(function(s,i){s.x=s.pc[0]/ax*0.95;s.z=s.pc[1]/az*0.95;s.bx=-1.25+2.5*i/(S.length-1)});
/* ⑤⑥ 가상 Y: 측정 전이므로 설명용 */
var g1=gnF(rng(17)),OFF={Woven:0.12,Knit:0.02,Nonwoven:-0.18};
function hypo(x,z,t){return 0.2+0.3*x+0.18*z+(OFF[t]||0)}
S.forEach(function(s){s.y=hypo(s.x,s.z,s.type)+0.05*g1()});
function stats(P,w){var n=P.length,m=[0,0,0];P.forEach(function(p){m[0]+=p.x/n;m[1]+=p.z/n;m[2]+=p.y/n});
 var C=[[0,0,0],[0,0,0],[0,0,0]];P.forEach(function(p){var d=[p.x-m[0],p.z-m[1],p.y-m[2]];for(var i=0;i<3;i++)for(var j=0;j<3;j++)C[i][j]+=d[i]*d[j]/(n-1)});
 for(var i=0;i<3;i++)C[i][i]+=2e-3;return {m:m,S:C,w:n/S.length}}
var TY=['Nonwoven','Woven','Knit'],G=TY.map(function(t){var g=stats(S.filter(function(s){return s.type===t}));g.t=t;return g});
function chol(A){var L=[[0,0,0],[0,0,0],[0,0,0]];for(var i=0;i<3;i++)for(var j=0;j<=i;j++){var s=A[i][j];for(var q=0;q<j;q++)s-=L[i][q]*L[j][q];L[i][j]=i===j?Math.sqrt(Math.max(s,1e-9)):s/L[j][j]}return L}
G.forEach(function(g){g.L=chol(g.S)});
function cond(x,z){var ws=[],mu=[],vv=[];G.forEach(function(g){var a=g.S[0][0],b=g.S[0][1],d=g.S[1][1],det=a*d-b*b,ia=[[d/det,-b/det],[-b/det,a/det]];
  var dx=x-g.m[0],dz=z-g.m[1],q=dx*(ia[0][0]*dx+ia[0][1]*dz)+dz*(ia[1][0]*dx+ia[1][1]*dz);ws.push(g.w*Math.exp(-q/2)/Math.sqrt(det));
  var c=[g.S[2][0],g.S[2][1]],k0=c[0]*ia[0][0]+c[1]*ia[1][0],k1=c[0]*ia[0][1]+c[1]*ia[1][1];mu.push(g.m[2]+k0*dx+k1*dz);vv.push(Math.max(g.S[2][2]-(k0*c[0]+k1*c[1]),1e-4))});
 var W=ws.reduce(function(a,b){return a+b},0)||1e-12,m=0,v=0,i;for(i=0;i<3;i++)m+=ws[i]/W*mu[i];for(i=0;i<3;i++)v+=ws[i]/W*(vv[i]+(mu[i]-m)*(mu[i]-m));return {m:m,s:Math.sqrt(v)}}
var GEN=[],VER=[];(function(){var r=rng(91),g=gnF(r);for(var i=0;i<60;i++){var t=r(),k=0,acc=0;for(var j=0;j<3;j++){acc+=G[j].w;if(t<=acc){k=j;break}}var c=G[k],e=[g()*1.2,g()*1.2,g()],p=[0,0,0];
  for(var a=0;a<3;a++){p[a]=c.m[a];for(var b=0;b<=a;b++)p[a]+=c.L[a][b]*e[b]}var cc=cond(p[0],p[1]);GEN.push({x:p[0],z:p[1],y:cc.m,s:cc.s,t:c.t})}
 var byM=GEN.slice().sort(function(a,b){return b.y-a.y}).slice(0,3),byS=GEN.slice().sort(function(a,b){return b.s-a.s}).filter(function(p){return byM.indexOf(p)<0}).slice(0,3),g2=gnF(rng(5));
 VER=byM.concat(byS).map(function(p){var y=hypo(p.x,p.z,p.t)+0.05*g2();return {p:p,y:y,ok:Math.abs(y-p.y)<=2*Math.sqrt(p.s*p.s+0.0025)}})})();
var step=1,yaw=0.3,pitch=0.55,base=0.3,zoom=1,auto=true,ctx,W,H,hov=null,HOT=[];
function prj(x,y,z){var cy=Math.cos(yaw),sy=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch);var X=x*cy-z*sy,Z=x*sy+z*cy,Y=y*cp-Z*sp,Dp=y*sp+Z*cp;
 var f=4.8/(4.8+Dp),s=Math.min(W*0.75,H)*(step<=2?0.24:0.27)*zoom;return [W/2+X*s*f,H*(step<=2?0.42:0.58)-Y*s*f,Dp]}
function Y3(y){return F+0.2+(y+0.4)*1.2}
function ln(a,b,col,w,dash){var p=prj(a[0],a[1],a[2]),q=prj(b[0],b[1],b[2]);ctx.strokeStyle=col;ctx.lineWidth=w||1;ctx.setLineDash(dash||[]);ctx.beginPath();ctx.moveTo(p[0],p[1]);ctx.lineTo(q[0],q[1]);ctx.stroke();ctx.setLineDash([])}
function tx(t,a,col,al){var p=prj(a[0],a[1],a[2]);ctx.fillStyle=col||'#5b6874';ctx.textAlign=al||'left';ctx.fillText(t,p[0],p[1]);ctx.textAlign='left'}
function poly(P,fill,stroke){ctx.beginPath();P.forEach(function(q,i){i?ctx.lineTo(q[0],q[1]):ctx.moveTo(q[0],q[1])});ctx.closePath();if(fill){ctx.fillStyle=fill;ctx.fill()}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=.6;ctx.stroke()}}
var F=-0.9;
function bars(){var faces=[],dx=0.034,dz=0.075;
 S.forEach(function(s,i){for(var j=0;j<9;j++){var z=-1+2*j/8,x=s.bx,full=GS[j]?s.cov[j]/GS[j]:0,v=s.cov[j];
  if(j===8){var c=[[x-dx,F,z-dz],[x+dx,F,z-dz],[x+dx,F,z+dz],[x-dx,F,z+dz]].map(function(p){return prj(p[0],p[1],p[2])});faces.push({d:prj(x,F,z)[2]+0.01,P:c,f:'rgba(201,48,44,.10)',k:'rgba(201,48,44,.8)'});
    HOT.push({q:prj(x,F+0.05,z),t:s.id+' · 전기 특성 Y (연속변수) · 측정 0'});continue}
  var h,col;if(step===2){h=COMMON[j]?COMMON[j]/GS[j]:0;if(!v)h=0;col=COMMON[j]?'19,115,58':'170,180,191'}else{h=full;col='19,115,58'}
  var ghost=step===2&&!COMMON[j]&&v;if(ghost)h=full;
  if(h<=0){continue}var top=F+h*0.85,al=ghost?0.12:(0.25+0.65*h);
  var c=[[x-dx,F,z-dz],[x+dx,F,z-dz],[x+dx,F,z+dz],[x-dx,F,z+dz],[x-dx,top,z-dz],[x+dx,top,z-dz],[x+dx,top,z+dz],[x-dx,top,z+dz]].map(function(p){return prj(p[0],p[1],p[2])});
  var F5=[[4,5,6,7,1],[0,1,5,4,.78],[1,2,6,5,.62],[2,3,7,6,.78],[3,0,4,7,.62]];
  F5.forEach(function(fc){var P=[c[fc[0]],c[fc[1]],c[fc[2]],c[fc[3]]],dd=(P[0][2]+P[1][2]+P[2][2]+P[3][2])/4,sh=fc[4];
   faces.push({d:dd,P:P,f:'rgba('+col.split(',').map(function(u){return Math.round(+u*sh+255*(1-sh)*(1-al)*0)}).join(',')+','+(al*(fc[4]===1?1:.9)).toFixed(2)+')',k:ghost?'rgba(150,160,170,.3)':'rgba(255,255,255,.5)'})});
  HOT.push({q:prj(x,top,z),t:s.id+' ('+SRCN[s.src]+' · '+TC[s.type][0]+') · '+GN[j]+' '+(step===2&&COMMON[j]?Math.min(v,COMMON[j])+'/'+COMMON[j]+' 공통':v+'/'+GS[j])})}});
 faces.sort(function(a,b){return b.d-a.d});faces.forEach(function(f){poly(f.P,f.f,f.k)});
 ctx.font='11px sans-serif';for(var j=0;j<9;j++)tx(GN[j],[1.32,F,-1+2*j/8],j===8?'#c9302c':'#16212b');
 [['Huvis 11',0,10],['연구실 2',11,12],['산업 14',13,26]].forEach(function(g){var a=S[g[1]].bx,b=S[g[2]].bx;ln([a,F,1.2],[b,F,1.2],'#16212b',2);tx(g[0],[(a+b)/2,F,1.45],'#16212b','center')});
 ctx.font='12px sans-serif'}
function floor(){for(var i=-4;i<=4;i++){var t=i/4;ln([t*1.3,F,-1.1],[t*1.3,F,1.1],'#eef1f4');ln([-1.3,F,t*1.1],[1.3,F,t*1.1],'#eef1f4')}}
function space(){ln([-1.1,F,-1.1],[1.25,F,-1.1],'#16212b',1.5);ln([-1.1,F,-1.1],[-1.1,F,1.25],'#16212b',1.5);
 tx('PC1 ('+Math.round(D.ev[0]*100)+'%) →',[1.3,F,-1.18],'#16212b');tx('PC2 ('+Math.round(D.ev[1]*100)+'%) →',[-1.0,F,1.35],'#16212b','center');
 if(step>=4){ln([-1.1,F,-1.1],[-1.1,1.05,-1.1],'#c9302c',1.6);tx('전기 특성 Y ↑ (연속변수: 전압·전류·전하밀도)',[-1.1,1.12,-1.1],'#c9302c')}
 var it=[];
 if(step>=5){G.forEach(function(g){[[0,1],[0,2],[1,2]].forEach(function(pl){var P=[];for(var a=0;a<=36;a++){var t=a/36*6.2832,e=[0,0,0];e[pl[0]]=2*Math.cos(t);e[pl[1]]=2*Math.sin(t);var p=[0,0,0];for(var r=0;r<3;r++){p[r]=g.m[r];for(var c=0;c<=r;c++)p[r]+=g.L[r][c]*e[c]}P.push(prj(p[0],Y3(p[2]),p[1]))}
   ctx.strokeStyle='rgba(111,90,168,.5)';ctx.lineWidth=1.3;ctx.beginPath();P.forEach(function(q,i){i?ctx.lineTo(q[0],q[1]):ctx.moveTo(q[0],q[1])});ctx.stroke()})})}
 S.forEach(function(s){var y=step>=5?Y3(s.y):F;it.push({k:'r',s:s,q:prj(s.x,y,s.z)})});
 if(step>=5)GEN.forEach(function(p){it.push({k:'g',p:p,q:prj(p.x,Y3(p.y),p.z)})});
 if(step>=6)VER.forEach(function(v){it.push({k:'v',v:v,q:prj(v.p.x,Y3(v.y),v.p.z)})});
 it.sort(function(a,b){return b.q[2]-a.q[2]});
 it.forEach(function(o){var q=o.q;if(o.k==='r'){var s=o.s;
   if(step===4){ln([s.x,F,s.z],[s.x,0.85,s.z],'rgba(201,48,44,.35)',1,[3,4]);tx('?',[s.x,0.9,s.z],'#c9302c','center')}
   if(step>=5)ln([s.x,F,s.z],[s.x,Y3(s.y),s.z],'rgba(47,93,158,.25)',1);
   ctx.fillStyle=TC[s.type][1];ctx.beginPath();ctx.arc(q[0],q[1],5.2,0,7);ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=1.2;ctx.stroke();
   HOT.push({q:q,t:s.id+' ('+SRCN[s.src]+' · '+TC[s.type][0]+') · PC1 '+s.pc[0].toFixed(2)+', PC2 '+s.pc[1].toFixed(2)+(step>=5?' · Y(가상) '+s.y.toFixed(2):step===4?' · Y 미측정':'')})}
  else if(o.k==='g'){var p=o.p;if(step>=6)ln([p.x,Y3(p.y-2*p.s),p.z],[p.x,Y3(p.y+2*p.s),p.z],'rgba(19,115,58,.5)',1.2);ctx.fillStyle='rgba(185,167,232,.95)';ctx.beginPath();ctx.arc(q[0],q[1],3.2,0,7);ctx.fill();
   HOT.push({q:q,t:'새 직물(가상) · '+TC[p.t][0]+' 무리 · Y 예상 '+p.y.toFixed(2)+(step>=6?' ± '+(2*p.s).toFixed(2):'')})}
  else{var v=o.v;ln([v.p.x,Y3(v.p.y),v.p.z],[v.p.x,Y3(v.y),v.p.z],'#c9302c',1.5,[3,3]);ctx.fillStyle='#c9302c';ctx.beginPath();ctx.arc(q[0],q[1],5.6,0,7);ctx.fill();
   ctx.fillStyle='#fff';ctx.font='bold 10px sans-serif';ctx.fillText(v.ok?'✓':'✗',q[0]-3.5,q[1]+3.5);ctx.font='12px sans-serif';HOT.push({q:q,t:'검증(가상) · 측정 '+v.y.toFixed(2)+' / 예상 '+v.p.y.toFixed(2)+(v.ok?' · 범위 안':' · 범위 밖')})}});
 if(step===5)G.forEach(function(g){tx(TC[g.t][0]+' 무리',[g.m[0],Y3(g.m[2])+0.3,g.m[1]],'#6f5aa8','center')})}
function draw(){var d=window.devicePixelRatio||1;W=cv.clientWidth||700;H=cv.clientHeight||470;if(cv.width!==Math.round(W*d)){cv.width=Math.round(W*d);cv.height=Math.round(H*d)}
 ctx=cv.getContext('2d');ctx.setTransform(d,0,0,d,0,0);ctx.clearRect(0,0,W,H);ctx.font='12px sans-serif';HOT=[];floor();
 if(step<=2)bars();else space();
 if(hov){var b=null,bd=196;HOT.forEach(function(h){var e=(h.q[0]-hov[0])*(h.q[0]-hov[0])+(h.q[1]-hov[1])*(h.q[1]-hov[1]);if(e<bd){bd=e;b=h}});
  if(b){ctx.font='12px sans-serif';var w=ctx.measureText(b.t).width+14,x0=Math.min(Math.max(4,b.q[0]+10),W-w-4),y0=Math.max(4,b.q[1]-30);ctx.fillStyle='rgba(22,33,43,.9)';ctx.fillRect(x0,y0,w,22);ctx.fillStyle='#fff';ctx.fillText(b.t,x0+7,y0+15);
   ctx.strokeStyle='#16212b';ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(b.q[0],b.q[1],6,0,7);ctx.stroke()}}}
var EXP={1:'<b>① 실측 현황.</b> 가로로 원단 27개(Huvis 11 · 연구실 2 · 산업 14), 앞뒤로 측정 묶음 9개가 놓입니다. 막대 높이는 그 묶음의 채움 비율입니다. 산업 원단은 KES 묶음까지 차 있고, Huvis·연구실은 FTT 위주입니다. 평균 채움률 68%. 맨 앞 빨간 칸 줄이 <b>전기 특성 Y</b>로, 27개 모두 비어 있습니다.',
 2:'<b>② 27개 모두에 있는 19항목.</b> 출처마다 장비와 항목이 달라, 27개를 함께 쓸 수 있는 항목은 기본 물성 1 + 표면 6 + 역학 10 + 열 2 = <b>19개</b>입니다(초록). 회색은 일부 원단에만 있는 항목입니다. 지금 생성 모델이 배울 수 있는 직물 특성 X는 이 19개입니다.',
 3:'<b>③ 직물 특성 공간.</b> 19항목을 주성분 분석(PCA)으로 두 축에 요약해(PC1·PC2는 19개 변수를 섞은 종합 점수 — 아래 <a href="#pcexp">PC1·PC2는 무엇인가</a>), 원단 27개를 바닥에 놓았습니다(실측, S1과 같은 값). 같은 종류끼리 모이고 부직포는 넓게 흩어집니다. 이 무리 모양이 생성 모델이 배울 "패턴"의 바닥 절반입니다.',
 4:'<b>④ 전기 특성 Y — 연속변수.</b> 세로축이 전기 특성입니다. Y는 "있다/없다" 같은 범주가 아니라 전압·전류·전하밀도처럼 <b>연속변수</b>입니다. 하지만 아직 <b>0개</b> 측정되어 모든 원단의 높이가 "?"입니다. 그래서 S2의 전기 특성 실측이 첫 관문입니다.',
 5:'<b>⑤ 측정 후 — 패턴 학습과 새 직물 (가상).</b> Y를 쟀다고 가정하고 원단들을 높이에 올렸습니다. 생성 모델이 직물 특성과 Y가 함께 나타나는 패턴(보라 타원체, 종류별 무리)을 배우고, 그 패턴에서 새 직물(연보라)을 만듭니다.',
 6:'<b>⑥ 연속값 예측과 일부 검증 (가상).</b> 새 직물마다 Y를 연속값과 범위(초록 막대, ±2σ)로 냅니다. 무리에서 먼 직물일수록 막대가 깁니다. 기대값 최고 3개와 범위가 가장 넓은 3개를 실제로 만들어 잰다고 가정했습니다(빨강, ✓ 범위 안 / ✗ 밖). 어떤 직물 특성이 Y를 얼마나 바꾸는지는 아래 <a href="#rel3">관계 보기</a>에서 변수 2개씩 골라 봅니다.'};
var LG={bar:'<span><i style="background:rgba(19,115,58,.8);border-radius:2px"></i>채움 비율이 높은 묶음</span><br><span><i style="background:rgba(19,115,58,.25);border-radius:2px"></i>채움 비율이 낮은 묶음</span><br><span><i style="background:#fcebea;border:1px solid #c9302c;border-radius:2px"></i>전기 특성 Y — 비어 있음</span>',
 pts:'<span><i style="background:#8e78c9"></i>부직포</span> <span><i style="background:#2f5d9e"></i>제직물</span> <span><i style="background:#d8685a"></i>편직물</span>',
 more:'<br><span><i style="background:#6f5aa8;border-radius:2px"></i>학습한 패턴</span><br><span><i style="background:#b9a7e8"></i>새 직물 (가상)</span><br><span><i style="background:#13733a"></i>예측 범위 ±2σ</span><br><span><i style="background:#c9302c"></i>검증 (가상)</span>'};
function setStep(s){step=s;document.querySelectorAll('[data-s3]').forEach(function(b){b.setAttribute('aria-pressed',+b.getAttribute('data-s3')<=s?'true':'false')});
 var t=EXP[s];if(s===6){var ok=VER.filter(function(v){return v.ok}).length;t+=' 이번 가상 결과: 6개 중 '+ok+'개가 범위 안.'}document.getElementById('s3dExp').innerHTML=t;
 var tag=document.getElementById('s3dTag');tag.textContent=s<=4?'실측 · 엑셀 직접 집계':'측정 전 · 가상 값';tag.className=s<=4?'realnote':'stampnote';
 document.getElementById('s3dLg').innerHTML=s<=2?LG.bar:LG.pts+(s>=5?LG.more:'');pitch=s<=3?0.85:0.5;draw()}
document.querySelectorAll('[data-s3]').forEach(function(b){b.addEventListener('click',function(){setStep(+b.getAttribute('data-s3'))})});
var rb=document.getElementById('s3dRot');rb.addEventListener('click',function(){auto=!auto;rb.setAttribute('aria-pressed',auto?'true':'false')});
var drag=null;cv.addEventListener('pointerdown',function(e){drag=[e.clientX,e.clientY,yaw,pitch];auto=false;rb.setAttribute('aria-pressed','false');cv.setPointerCapture(e.pointerId)});
cv.addEventListener('pointermove',function(e){var r=cv.getBoundingClientRect();hov=[e.clientX-r.left,e.clientY-r.top];if(drag){yaw=drag[2]+(e.clientX-drag[0])*0.01;pitch=Math.max(-0.05,Math.min(1.3,drag[3]+(e.clientY-drag[1])*0.008))}draw()});
cv.addEventListener('pointerleave',function(){hov=null;draw()});cv.addEventListener('pointerup',function(){drag=null;base=yaw});
cv.addEventListener('wheel',function(e){e.preventDefault();zoom=Math.max(0.6,Math.min(2,zoom*(e.deltaY<0?1.08:0.93)));draw()},{passive:false});
if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches){auto=false;rb.setAttribute('aria-pressed','false')}
var last=0;function tick(t){if(auto&&!hov&&t-last>33){yaw=base+0.4*Math.sin(t/2600);draw();last=t}requestAnimationFrame(tick)}requestAnimationFrame(tick);
window.addEventListener('resize',draw);setStep(6);

/* ---- 역방향: p(X | Y*) ---- */
(function(){var ic=document.getElementById('invCv');if(!ic)return;
 var ys=S.map(function(s){return s.y}),ylo=Math.min.apply(0,ys),yhi=Math.max.apply(0,ys),yv=ylo+(yhi-ylo)*0.8,iy=0.7,ip=0.45,ictx,IW,IH,ih=null,IHOT=[],idrag=null;
 function ipr(x,y,z){var cy=Math.cos(iy),sy=Math.sin(iy),cp=Math.cos(ip),sp=Math.sin(ip),X=x*cy-z*sy,Z=x*sy+z*cy,Y=y*cp-Z*sp,Dp=y*sp+Z*cp,f=4.8/(4.8+Dp),sc=Math.min(IW*.75,IH)*0.27;return [IW/2+X*sc*f,IH*0.64-Y*sc*f,Dp]}
 function iln(a,b,c,w,d){var p=ipr(a[0],a[1],a[2]),q=ipr(b[0],b[1],b[2]);ictx.strokeStyle=c;ictx.lineWidth=w||1;ictx.setLineDash(d||[]);ictx.beginPath();ictx.moveTo(p[0],p[1]);ictx.lineTo(q[0],q[1]);ictx.stroke();ictx.setLineDash([])}
 function itx(t,a,c,al){var p=ipr(a[0],a[1],a[2]);ictx.fillStyle=c||'#16212b';ictx.textAlign=al||'left';ictx.fillText(t,p[0],p[1]);ictx.textAlign='left'}
 function condX(y){/* 성분별 p(x,z | y) */var C=G.map(function(g){var syy=g.S[2][2],sx=[g.S[0][2],g.S[1][2]],d=y-g.m[2];
   var w=g.w*Math.exp(-d*d/(2*syy))/Math.sqrt(syy),m=[g.m[0]+sx[0]/syy*d,g.m[1]+sx[1]/syy*d],
   c=[[g.S[0][0]-sx[0]*sx[0]/syy,g.S[0][1]-sx[0]*sx[1]/syy],[g.S[1][0]-sx[1]*sx[0]/syy,g.S[1][1]-sx[1]*sx[1]/syy]];return {w:w,m:m,c:c,t:g.t}});
   var W=C.reduce(function(a,b){return a+b.w},0)||1e-12;C.forEach(function(c){c.w/=W});return C}
 function cands(C){var r=rng(77),g=gnF(r),out=[];for(var i=0;i<40;i++){var t=r(),k=0,acc=0;for(var j=0;j<C.length;j++){acc+=C[j].w;if(t<=acc){k=j;break}}var c=C[k],a=c.c[0][0],b=c.c[0][1],d=c.c[1][1],l11=Math.sqrt(Math.max(a,1e-6)),l21=b/l11,l22=Math.sqrt(Math.max(d-l21*l21,1e-6)),e1=g(),e2=g();
   out.push({x:c.m[0]+l11*e1,z:c.m[1]+l21*e1+l22*e2,t:c.t})}return out}
 function idraw(){var d=window.devicePixelRatio||1;IW=ic.clientWidth||700;IH=ic.clientHeight||470;if(ic.width!==Math.round(IW*d)){ic.width=Math.round(IW*d);ic.height=Math.round(IH*d)}
  ictx=ic.getContext('2d');ictx.setTransform(d,0,0,d,0,0);ictx.clearRect(0,0,IW,IH);ictx.font='12px sans-serif';IHOT=[];
  for(var i=-4;i<=4;i++){var t=i/4;iln([t*1.1,F,-1.1],[t*1.1,F,1.1],'#eef1f4');iln([-1.1,F,t*1.1],[1.1,F,t*1.1],'#eef1f4')}
  iln([-1.1,F,-1.1],[1.25,F,-1.1],'#16212b',1.5);iln([-1.1,F,-1.1],[-1.1,F,1.25],'#16212b',1.5);iln([-1.1,F,-1.1],[-1.1,1.05,-1.1],'#c9302c',1.5);
  itx('PC1 →',[1.3,F,-1.15]);itx('PC2 →',[-1.0,F,1.35],'#16212b','center');itx('전기 특성 Y ↑ (가상)',[-1.1,1.12,-1.1],'#c9302c');
  var C=condX(yv),cd=cands(C),Yp=Y3(yv);
  C.forEach(function(c){if(c.w<0.03)return;var a=c.c[0][0],b=c.c[0][1],dd=c.c[1][1],l11=Math.sqrt(Math.max(a,1e-6)),l21=b/l11,l22=Math.sqrt(Math.max(dd-l21*l21,1e-6)),P=[],Q=[];
   for(var k=0;k<=36;k++){var t=k/36*6.2832,e1=2*Math.cos(t),e2=2*Math.sin(t),x=c.m[0]+l11*e1,z=c.m[1]+l21*e1+l22*e2;P.push(ipr(x,F,z));Q.push(ipr(x,Yp,z))}
   [[P,'rgba(214,160,40,'+(0.12+0.3*c.w).toFixed(2)+')'],[Q,'rgba(214,160,40,'+(0.1+0.25*c.w).toFixed(2)+')']].forEach(function(o){ictx.beginPath();o[0].forEach(function(q,k){k?ictx.lineTo(q[0],q[1]):ictx.moveTo(q[0],q[1])});ictx.closePath();ictx.fillStyle=o[1];ictx.fill();ictx.strokeStyle='rgba(176,120,0,.6)';ictx.lineWidth=1;ictx.stroke()})});
  var pl=[[-1.1,Yp,-1.1],[1.1,Yp,-1.1],[1.1,Yp,1.1],[-1.1,Yp,1.1]].map(function(p){return ipr(p[0],p[1],p[2])});ictx.beginPath();pl.forEach(function(q,k){k?ictx.lineTo(q[0],q[1]):ictx.moveTo(q[0],q[1])});ictx.closePath();ictx.fillStyle='rgba(214,160,40,.10)';ictx.fill();ictx.strokeStyle='rgba(176,120,0,.7)';ictx.stroke();
  itx('Y* = '+yv.toFixed(2),[1.15,Yp,1.1],'#a35c00');
  var it=[];S.forEach(function(s){it.push({k:'r',s:s,q:ipr(s.x,Y3(s.y),s.z)})});cd.forEach(function(c){it.push({k:'c',c:c,q:ipr(c.x,Yp,c.z)})});it.sort(function(a,b){return b.q[2]-a.q[2]});
  it.forEach(function(o){var q=o.q;if(o.k==='r'){ictx.fillStyle=TC[o.s.type][1];ictx.globalAlpha=.55;ictx.beginPath();ictx.arc(q[0],q[1],4.2,0,7);ictx.fill();ictx.globalAlpha=1;IHOT.push({q:q,t:o.s.id+' ('+TC[o.s.type][0]+') · Y(가상) '+o.s.y.toFixed(2)})}
   else{iln([o.c.x,Yp,o.c.z],[o.c.x,F,o.c.z],'rgba(176,120,0,.25)',1,[2,3]);ictx.fillStyle='#d6a028';ictx.beginPath();ictx.arc(q[0],q[1],3.6,0,7);ictx.fill();ictx.strokeStyle='#fff';ictx.lineWidth=.8;ictx.stroke();IHOT.push({q:q,t:'예상 직물 후보 · '+TC[o.c.t][0]+' 쪽 · PC1 '+(o.c.x*ax).toFixed(2)+', PC2 '+(o.c.z*az).toFixed(2)})}});
  if(ih){var bb=null,bd=196;IHOT.forEach(function(h){var e=(h.q[0]-ih[0])*(h.q[0]-ih[0])+(h.q[1]-ih[1])*(h.q[1]-ih[1]);if(e<bd){bd=e;bb=h}});if(bb){var w=ictx.measureText(bb.t).width+14,x0=Math.min(Math.max(4,bb.q[0]+10),IW-w-4),y0=Math.max(4,bb.q[1]-30);ictx.fillStyle='rgba(22,33,43,.9)';ictx.fillRect(x0,y0,w,22);ictx.fillStyle='#fff';ictx.fillText(bb.t,x0+7,y0+15)}}
  /* 설명: 성분 비중, 후보 중심과 가장 닮은 실측 원단 */
  var vote={};cd.forEach(function(c){var best=null,bd=1e9;S.forEach(function(s){var e=Math.hypot(s.x-c.x,s.z-c.z);if(e<bd){bd=e;best=s}});vote[best.id]=(vote[best.id]||0)+1});
  var near=S.filter(function(s){return vote[s.id]}).map(function(s){return {s:s,v:vote[s.id]}}).sort(function(a,b){return b.v-a.v}).slice(0,3);
  var mix=C.slice().sort(function(a,b){return b.w-a.w}).filter(function(c){return c.w>=0.05}).map(function(c){return TC[c.t][0]+' '+Math.round(c.w*100)+'%'}).join(' · ');
  document.getElementById('invYv').textContent=yv.toFixed(2);
  document.getElementById('invExp').innerHTML='<b>목표 Y* = '+yv.toFixed(2)+'</b> (가상 단위)일 때 예상되는 직물 쪽: <b>'+mix+'</b>.<br>후보 40개(주황)가 가장 많이 닮은 실측 원단: '+near.map(function(n){return '<b>'+n.s.id+'</b>('+TC[n.s.type][0]+', '+n.v+'개)'}).join(', ')+'.<br><span class="small muted">실측 원단의 Y가 측정되면 같은 계산이 실제 값으로 바뀝니다. 후보는 실제로 만들어 Y를 재어 확인합니다.</span>'}
 var sl=document.getElementById('invY');function setY(p){yv=ylo+(yhi-ylo)*p/100;sl.value=p;idraw()}
 sl.addEventListener('input',function(){setY(+sl.value)});
 document.querySelectorAll('[data-inv]').forEach(function(b){b.addEventListener('click',function(){setY({hi:90,mid:50,lo:10}[b.dataset.inv])})});
 ic.addEventListener('pointerdown',function(e){idrag=[e.clientX,e.clientY,iy,ip];ic.setPointerCapture(e.pointerId)});
 ic.addEventListener('pointermove',function(e){var r=ic.getBoundingClientRect();ih=[e.clientX-r.left,e.clientY-r.top];if(idrag){iy=idrag[2]+(e.clientX-idrag[0])*.01;ip=Math.max(-.05,Math.min(1.3,idrag[3]+(e.clientY-idrag[1])*.008))}idraw()});
 ic.addEventListener('pointerup',function(){idrag=null});ic.addEventListener('pointerleave',function(){ih=null;idraw()});window.addEventListener('resize',idraw);setY(80);
})();

})();
</script>
"""
HTML = HTML_T.replace('@@DATA@@', _data())

# ---- 관계 보기: 변수 2개 × Y, 나머지 17개 고정 (다항 모델의 3D 단면) ----
VARS = [
 ('W', '평량', 'g/m²'), ('SFC_F', '마찰계수 · 앞면', ''), ('SFC_B', '마찰계수 · 뒷면', ''),
 ('SRA_F', '표면 거칠기 진폭 · 앞면', 'μm'), ('SRA_B', '표면 거칠기 진폭 · 뒷면', 'μm'),
 ('SRW_F', '거칠기 파장 · 앞면', 'mm'), ('SRW_B', '거칠기 파장 · 뒷면', 'mm'),
 ('BAR_F', '굽힘 강성 · 앞면', ''), ('BAR_B', '굽힘 강성 · 뒷면', ''),
 ('BW_FL', '굽힘 일 · 앞면 L', ''), ('BW_FC', '굽힘 일 · 앞면 C', ''), ('BW_BL', '굽힘 일 · 뒷면 L', ''), ('BW_BC', '굽힘 일 · 뒷면 C', ''),
 ('CW_F', '압축 일 · 앞면', ''), ('CW_B', '압축 일 · 뒷면', ''),
 ('CRR_F', '압축 회복률 · 앞면', ''), ('CRR_B', '압축 회복률 · 뒷면', ''),
 ('Qmax_F', '접촉 냉온감 Qmax · 앞면', 'W/cm²'), ('Qmax_B', '접촉 냉온감 Qmax · 뒷면', 'W/cm²'),
]

REL_CSS = r"""
.rel3{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:16px;align-items:start;margin-top:14px}
.rel3 canvas{display:block;width:100%;height:440px;border:1px solid var(--rule);border-radius:12px;background:#fff;cursor:grab;touch-action:none}
.rel3 select{width:100%;padding:6px;border:1px solid var(--rule);border-radius:8px;font:inherit;margin:2px 0 8px}
.rel3 .eqbox{font-family:"IBM Plex Mono",monospace;font-size:12.5px;line-height:1.7;background:#f7f9fb;border:1px solid var(--rule);border-radius:10px;padding:8px 10px;word-break:break-word}
.rel3 details{margin-top:8px;font-size:13px}.rel3 details .fx{display:grid;grid-template-columns:1fr 90px 34px;gap:4px;align-items:center;margin:3px 0}
.rel3 details .fx.off{opacity:.35}.rel3 details input{width:100%}
@media (max-width:900px){.rel3{grid-template-columns:1fr}}
"""

def rel_html():
    names = json.dumps([[k, n, u] for k, n, u in VARS], ensure_ascii=False)
    return r"""
<h3 id="rel3" style="margin-top:34px">관계 보기 — 변수 2개를 고르고, 나머지 17개는 고정 <span class="stampnote">계수는 가상 · 측정 후 실제 계수로 교체</span></h3>
<p>위 ③④처럼 주성분 축에 놓으면 원단 배치는 보이지만, <b>어떤 직물 특성이 Y를 얼마나 바꾸는지</b>는 보이지 않습니다. 그래서 실제 계산은 19개 공통 항목 전체로 하고, 3D에는 그중 <b>2개만 움직이고 나머지 17개는 고정한 단면</b>을 그립니다. 축으로 쓸 2개는 언제든 바꿀 수 있습니다.</p>
<div class="rel3">
 <div><canvas id="relCv" aria-label="선택한 두 직물 특성과 전기 특성 Y의 3D 곡면"></canvas><p class="small muted" style="margin:6px 0 0">값은 표준화 단위(평균 0, 표준편차 1)입니다. 끌어서 회전. 바닥의 등고선은 같은 Y 높이를 이은 선입니다.</p></div>
 <div>
  <label class="small"><b>가로축 변수</b></label><select id="relA"></select>
  <label class="small"><b>깊이축 변수</b></label><select id="relB"></select>
  <div class="ctrl" style="margin:0 0 8px"><button type="button" class="bt sm" id="relMean">나머지 모두 평균(0)에 고정</button> <button type="button" class="bt sm" id="relRand">나머지를 다른 원단처럼</button></div>
  <div class="small" style="margin-bottom:4px"><b>이 단면의 식</b> — 2차 다항 모델을 고정값으로 줄인 결과</div>
  <div class="eqbox" id="relEq"></div>
  <details><summary>고정한 17개 변수 값 바꾸기</summary><div id="relFx"></div></details>
 </div>
</div>
<div class="brief" style="margin-top:14px"><div class="bh">실제 계산 — 다항 행렬</div><dl>
<dt>모델</dt><dd>2차 다항: ŷ = β₀ + Σ βᵢ xᵢ + Σ βᵢᵢ xᵢ² + Σ βᵢⱼ xᵢ xⱼ. 행렬로 쓰면 <b>ŷ = Φ(X) β</b>. Φ(X)는 원단 n개 × 항 210개(상수 1 + 1차 19 + 제곱 19 + 교호작용 171)의 다항 특징 행렬입니다.</dd>
<dt>3D와의 관계</dt><dd>계산은 210개 항을 모두 씁니다. 3D 곡면은 그 결과를 두 변수 방향으로 자른 단면이라, 단면도 다시 2차 곡면(오른쪽 식)이 됩니다. 축 변수를 바꾸면 같은 모델을 다른 방향으로 자른 단면이 나옵니다.</dd>
<dt>생성 모델과의 관계</dt><dd>1차년도 생성 모델에서는 "이 직물 특성일 때 Y의 기대값" E[Y | X]가 같은 자리에 들어갑니다. 비교 기준인 회귀 모델도 같은 방식으로 단면을 그릴 수 있어, 두 모델의 곡면을 나란히 비교할 수 있습니다.</dd>
<dt class="ask">주의</dt><dd>항이 210개인데 원단이 27개면 계수를 정할 수 없습니다. 원단 수를 늘리거나(S2 50~100개), 릿지·라쏘 같은 규제를 쓰거나, 영향이 큰 변수 몇 개로 줄여야 합니다. 지금 곡면의 계수는 측정 전이라 가상 값이며, 거칠기·압축 일이 클수록 출력이 커진다는 문헌 방향만 반영했습니다.</dd></dl></div>
<script>
(function(){
var cv=document.getElementById('relCv');if(!cv)return;
var V=@@VARS@@,n=V.length;
function rng(s){return function(){s=(s*69069+1)%4294967296;return s/4294967296}}var r=rng(23);
var b0=0.3,b=V.map(function(){return (r()-.5)*0.06}),Bq=[];for(var i=0;i<n;i++){Bq.push(new Array(n).fill(0))}
for(var i=0;i<n;i++)for(var j=i;j<n;j++){var v=(r()-.5)*0.012;Bq[i][j]=v;Bq[j][i]=v}
function idx(k){for(var i=0;i<n;i++)if(V[i][0]===k)return i}
/* 문헌 방향(가상 크기): 거칠기·압축 일·마찰 ↑ → 출력 ↑, 거칠기는 포화(제곱 음수), 거칠기×압축 일 교호작용 + */
[['SRA_F',.12],['SRA_B',.05],['CW_F',.10],['CW_B',.04],['SFC_F',.06],['CRR_F',.04],['W',.03],['BW_FL',-.04],['BAR_F',-.03],['Qmax_F',.02]].forEach(function(p){b[idx(p[0])]=p[1]});
Bq[idx('SRA_F')][idx('SRA_F')]=-0.035;Bq[idx('CW_F')][idx('CW_F')]=-0.02;var a=idx('SRA_F'),c=idx('CW_F');Bq[a][c]=Bq[c][a]=0.025;
var fx=new Array(n).fill(0),A=idx('SRA_F'),Bv=idx('CW_F');
function yv(z){var y=b0,i,j;for(i=0;i<n;i++)y+=b[i]*z[i];for(i=0;i<n;i++)for(j=0;j<n;j++)y+=Bq[i][j]*z[i]*z[j];return y}
function sliceCoef(){var c0=b0,a1=b[A],a2=b[Bv],i,j;for(i=0;i<n;i++){if(i===A||i===Bv)continue;c0+=b[i]*fx[i];a1+=2*Bq[A][i]*fx[i];a2+=2*Bq[Bv][i]*fx[i];
  for(j=0;j<n;j++){if(j===A||j===Bv)continue;c0+=Bq[i][j]*fx[i]*fx[j]}}return {c:c0,a1:a1,a2:a2,q1:Bq[A][A],q2:Bq[Bv][Bv],r:2*Bq[A][Bv]}}
var sa=document.getElementById('relA'),sb=document.getElementById('relB');
V.forEach(function(v,i){sa.add(new Option(v[1]+' ('+v[0]+')',i));sb.add(new Option(v[1]+' ('+v[0]+')',i))});sa.value=A;sb.value=Bv;
function buildFx(){var h='';V.forEach(function(v,i){var off=(i===A||i===Bv);h+='<div class="fx'+(off?' off':'')+'"><span>'+v[1]+'</span><input type="range" min="-2" max="2" step="0.1" value="'+fx[i]+'" data-fx="'+i+'"'+(off?' disabled':'')+' aria-label="'+v[1]+' 고정값"><span>'+(off?'축':fx[i].toFixed(1))+'</span></div>'});
 var el=document.getElementById('relFx');el.innerHTML=h;el.querySelectorAll('[data-fx]').forEach(function(s){s.addEventListener('input',function(){fx[+s.dataset.fx]=+s.value;s.nextElementSibling.textContent=(+s.value).toFixed(1);draw()})})}
function sgn(v,t){return (v<0?' − ':' + ')+Math.abs(v).toFixed(3)+t}
var yaw=0.7,pitch=0.5,ctx,W,H;
function prj(x,y,z){var cy=Math.cos(yaw),sy=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch),X=x*cy-z*sy,Z=x*sy+z*cy,Y=y*cp-Z*sp,D=y*sp+Z*cp,f=4.6/(4.6+D),s=Math.min(W*.8,H)*0.3;return [W/2+X*s*f,H*0.6-Y*s*f,D]}
function col(t){t=Math.max(0,Math.min(1,t));var c=[[47,93,158],[19,115,58],[214,160,40],[201,48,44]],k=Math.min(2,Math.floor(t*3)),u=t*3-k,p=c[k],q=c[k+1];return 'rgb('+[0,1,2].map(function(i){return Math.round(p[i]+(q[i]-p[i])*u)}).join(',')+')'}
function draw(){var d=window.devicePixelRatio||1;W=cv.clientWidth||640;H=cv.clientHeight||440;if(cv.width!==Math.round(W*d)){cv.width=Math.round(W*d);cv.height=Math.round(H*d)}
 ctx=cv.getContext('2d');ctx.setTransform(d,0,0,d,0,0);ctx.clearRect(0,0,W,H);ctx.font='12px sans-serif';
 var N=22,G=[],ymin=1e9,ymax=-1e9,z=fx.slice(),i,j;
 for(i=0;i<=N;i++){G.push([]);for(j=0;j<=N;j++){z[A]=-2+4*i/N;z[Bv]=-2+4*j/N;var y=yv(z);G[i].push(y);ymin=Math.min(ymin,y);ymax=Math.max(ymax,y)}}
 var lo=-0.4,hi=1.0,F=-0.95;function Y3(y){return F+(y-lo)/(hi-lo)*1.9}
 function L(a,b,c,w){var p=prj(a[0],a[1],a[2]),q=prj(b[0],b[1],b[2]);ctx.strokeStyle=c;ctx.lineWidth=w||1;ctx.beginPath();ctx.moveTo(p[0],p[1]);ctx.lineTo(q[0],q[1]);ctx.stroke()}
 function T(t,a,c,al){var p=prj(a[0],a[1],a[2]);ctx.fillStyle=c||'#16212b';ctx.textAlign=al||'left';ctx.fillText(t,p[0],p[1]);ctx.textAlign='left'}
 for(i=0;i<=4;i++){var t=-1+i/2;L([t,F,-1],[t,F,1],'#eef1f4');L([-1,F,t],[1,F,t],'#eef1f4')}
 L([-1,F,-1],[1.15,F,-1],'#16212b',1.5);L([-1,F,-1],[-1,F,1.15],'#16212b',1.5);L([-1,F,-1],[-1,0.98,-1],'#c9302c',1.5);
 T(V[A][1]+' →',[1.18,F,-1.05]);T(V[Bv][1]+' →',[-1.0,F,1.3],'#16212b','center');T('전기 특성 Y ↑ (가상)',[-1,1.05,-1],'#c9302c');
 /* 바닥 등고선 */
 [0,.25,.5,.75,1].forEach(function(lv){var yl=ymin+(ymax-ymin)*lv;ctx.strokeStyle=col((yl-lo)/(hi-lo));ctx.globalAlpha=.45;
  for(i=0;i<N;i++)for(j=0;j<N;j++){var P=[[i,j],[i+1,j],[i+1,j+1],[i,j+1]],pts=[];for(var e=0;e<4;e++){var p=P[e],q=P[(e+1)%4],u=G[p[0]][p[1]],w=G[q[0]][q[1]];
    if((u-yl)*(w-yl)<0){var tt=(yl-u)/(w-u),ii=p[0]+(q[0]-p[0])*tt,jj=p[1]+(q[1]-p[1])*tt;pts.push(prj(-1+2*ii/N,F,-1+2*jj/N))}}
   if(pts.length===2){ctx.beginPath();ctx.moveTo(pts[0][0],pts[0][1]);ctx.lineTo(pts[1][0],pts[1][1]);ctx.stroke()}}ctx.globalAlpha=1});
 /* 곡면: 먼 면부터 */
 var Q=[];for(i=0;i<N;i++)for(j=0;j<N;j++){var cs=[[i,j],[i+1,j],[i+1,j+1],[i,j+1]].map(function(p){return prj(-1+2*p[0]/N,Y3(G[p[0]][p[1]]),-1+2*p[1]/N)}),m=(G[i][j]+G[i+1][j+1])/2;
  Q.push({d:(cs[0][2]+cs[2][2])/2,c:cs,m:m})}
 Q.sort(function(a,b){return b.d-a.d});Q.forEach(function(q){ctx.beginPath();q.c.forEach(function(p,k){k?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1])});ctx.closePath();ctx.fillStyle=col((q.m-lo)/(hi-lo));ctx.globalAlpha=.88;ctx.fill();ctx.globalAlpha=1;ctx.strokeStyle='rgba(255,255,255,.35)';ctx.lineWidth=.5;ctx.stroke()});
 var k=sliceCoef();document.getElementById('relEq').innerHTML='ŷ = '+k.c.toFixed(3)+sgn(k.a1,'·u')+sgn(k.a2,'·v')+sgn(k.q1,'·u²')+sgn(k.q2,'·v²')+sgn(k.r,'·uv')+'<br><span class="small">u = '+V[A][1]+', v = '+V[Bv][1]+'<br>Y 범위(이 단면): '+ymin.toFixed(2)+' ~ '+ymax.toFixed(2)+'</span>'}
function setAxes(){var a=+sa.value,b2=+sb.value;if(a===b2){b2=(a+1)%n;sb.value=b2}A=a;Bv=b2;buildFx();draw()}
sa.addEventListener('change',setAxes);sb.addEventListener('change',function(){if(+sb.value===A){sa.value=(A+1)%n}setAxes()});
document.getElementById('relMean').addEventListener('click',function(){fx=new Array(n).fill(0);buildFx();draw()});
document.getElementById('relRand').addEventListener('click',function(){var g=rng(Math.floor(Math.random()*1e6));fx=fx.map(function(){return Math.round(((g()+g()+g())/1.5-1)*1.5*10)/10});buildFx();draw()});
var drag=null;cv.addEventListener('pointerdown',function(e){drag=[e.clientX,e.clientY,yaw,pitch];cv.setPointerCapture(e.pointerId)});
cv.addEventListener('pointermove',function(e){if(!drag)return;yaw=drag[2]+(e.clientX-drag[0])*.01;pitch=Math.max(.05,Math.min(1.3,drag[3]+(e.clientY-drag[1])*.008));draw()});
cv.addEventListener('pointerup',function(){drag=null});window.addEventListener('resize',draw);buildFx();draw();
})();
</script>
""".replace('@@VARS@@', names)

HTML = HTML_T.replace('@@DATA@@', _data()).replace('@@SAY2@@\n<p class="small muted">①②', '@@SAY2@@\n@@REL@@\n<p class="small muted">①②').replace('@@REL@@', rel_html())
CSS = CSS + REL_CSS

# ---- PC1·PC2 구성 설명: 19개 변수의 가중합 ----
def pc_html():
    # (표시명, 묶음, PC1 강조, PC2 강조) — 강조는 S1 분석 기록(PC1: 열 전달·압축 일·거칠기 / PC2: 굽힘 일·압축 회복)에 따른 정성 표시
    rows = [('평량', '기본', 0, 0),
            ('마찰계수 앞', '표면', 0, 0), ('마찰계수 뒤', '표면', 0, 0), ('거칠기 진폭 앞', '표면', 1, 0), ('거칠기 진폭 뒤', '표면', 1, 0), ('거칠기 파장 앞', '표면', 0, 0), ('거칠기 파장 뒤', '표면', 0, 0),
            ('굽힘 강성 앞', '역학', 0, 0), ('굽힘 강성 뒤', '역학', 0, 0), ('굽힘 일 앞 L', '역학', 0, 1), ('굽힘 일 앞 C', '역학', 0, 1), ('굽힘 일 뒤 L', '역학', 0, 1), ('굽힘 일 뒤 C', '역학', 0, 1),
            ('압축 일 앞', '역학', 1, 0), ('압축 일 뒤', '역학', 1, 0), ('압축 회복률 앞', '역학', 0, 1), ('압축 회복률 뒤', '역학', 0, 1),
            ('접촉 냉온감 Qmax 앞', '열', 1, 0), ('접촉 냉온감 Qmax 뒤', '열', 1, 0)]
    BC = {'기본': '#5b6874', '표면': '#2f5d9e', '역학': '#13733a', '열': '#c9302c'}
    W, rh, top = 760, 22, 30
    H = top + rh * len(rows) + 20
    p1 = (600, top + rh * 5); p2 = (600, top + rh * 13)
    s = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="19개 변수가 PC1과 PC2로 섞여 들어가는 그림" style="width:100%;height:auto">',
         '<g font-family="sans-serif" font-size="12.5">',
         f'<text x="10" y="18" font-weight="700" fill="#16212b">27개 원단 모두에 있는 19개 변수</text><text x="600" y="18" font-weight="700" fill="#16212b" text-anchor="middle">종합 점수 2개</text>']
    for i, (nm, g, a, b) in enumerate(rows):
        y = top + rh * i + 14
        s.append(f'<rect x="10" y="{y-12}" width="200" height="18" rx="4" fill="{BC[g]}" opacity=".10"/><text x="18" y="{y+1}" fill="{BC[g]}">{g}</text><text x="58" y="{y+1}" fill="#16212b">{nm}</text>')
        for (tx, ty), on, cls, col in [(p1, a, 'pc1', '#a35c00'), (p2, b, 'pc2', '#6f5aa8')]:
            w = 3.2 if on else 0.8
            op = .9 if on else .28
            s.append(f'<path class="pcl {cls}" d="M212,{y-3} C400,{y-3} 420,{ty} {tx-62},{ty}" stroke="{col if on else "#9aa5b1"}" stroke-width="{w}" fill="none" opacity="{op}"/>')
    for (x, y), nm, pct, col, desc in [(p1, 'PC1', '39%', '#a35c00', '열 전달 · 압축 일 · 거칠기'), (p2, 'PC2', '29%', '#6f5aa8', '굽힘 일 · 압축 회복')]:
        s.append(f'<rect x="{x-62}" y="{y-34}" width="150" height="68" rx="12" fill="#fff" stroke="{col}" stroke-width="2.5"/><text x="{x+13}" y="{y-10}" text-anchor="middle" font-size="17" font-weight="800" fill="{col}">{nm} · 정보 {pct}</text><text x="{x+13}" y="{y+10}" text-anchor="middle" font-size="11.5" fill="#16212b">크게 실린 변수:</text><text x="{x+13}" y="{y+25}" text-anchor="middle" font-size="11.5" fill="#16212b">{desc}</text>')
    s.append('</g></svg>')
    svg = ''.join(s)
    return r"""
<h3 id="pcexp" style="margin-top:34px">PC1·PC2는 무엇인가 — 19개 변수를 섞어 만든 종합 점수 <span class="realnote">실측 분석(S1) 기반 · 굵기는 정성 표시</span></h3>
<p>3D 그림의 바닥 두 축 PC1·PC2는 새로 잰 값이 아닙니다. <b>19개 변수에 가중치를 곱해 더한 종합 점수</b>입니다. 경기종합지수가 여러 경제지표를 가중합해 경기를 숫자 하나로 보여 주는 것과 같은 방식입니다.</p>
<div class="eqline">PC1 = w₁×평량 + w₂×마찰계수(앞) + w₃×마찰계수(뒤) + … + w₁₉×접촉 냉온감(뒤)</div>
<div class="eqline">PC2 = v₁×평량 + v₂×마찰계수(앞) + … + v₁₉×접촉 냉온감(뒤) &nbsp;<span class="small muted">(가중치가 다른 두 번째 조합)</span></div>
<div class="ctrl" style="margin:10px 0 4px"><div class="group" role="group" aria-label="보기"><button type="button" class="bt sm" data-pcv="both" aria-pressed="true">둘 다</button><button type="button" class="bt sm" data-pcv="pc1" aria-pressed="false">PC1만</button><button type="button" class="bt sm" data-pcv="pc2" aria-pressed="false">PC2만</button></div></div>
<div class="panel" id="pcSvg">""" + svg + r"""</div>
<div class="pair">
 <div><span class="tag fly">어떻게 정하나</span><p>① 19개 변수를 로그 변환하고 표준화(평균 0, 표준편차 1)해 단위를 맞춥니다. ② 원단 27개가 가장 넓게 퍼지는 방향을 찾아 그 방향의 가중치 조합을 PC1로 삼습니다. ③ PC1과 겹치지 않으면서 다음으로 넓게 퍼지는 방향이 PC2입니다.</p></div>
 <div><span class="tag nn">읽는 법</span><p>PC1이 큰 원단은 열 전달·압축 일·표면 거칠기 쪽 값이 함께 큰 원단이고, PC2가 큰 원단은 굽힘 일·압축 회복 쪽 값이 큰 원단입니다. 두 축이 19개 변수 정보의 68%를 담고, 나머지 32%는 PC3 이하에 남습니다.</p></div>
</div>
<p class="small muted">굵은 선은 S1 분석에서 "크게 실린" 변수로 기록된 묶음을 표시한 것이고, 선 굵기는 정확한 가중치 크기가 아닙니다. 엑셀 원본을 넣으면 19개 가중치 값을 그대로 막대로 보여 드릴 수 있습니다. 생성 모델과 관계 보기의 실제 계산은 PC 두 개가 아니라 19개 변수 전체로 합니다.</p>
<script>
(function(){var box=document.getElementById('pcSvg');if(!box)return;
document.querySelectorAll('[data-pcv]').forEach(function(b){b.addEventListener('click',function(){var v=b.dataset.pcv;document.querySelectorAll('[data-pcv]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});
 box.querySelectorAll('.pcl').forEach(function(l){l.style.display=(v==='both'||l.classList.contains(v))?'':'none'})})})})();
</script>
"""

HTML = HTML.replace('@@SAY2@@\n', '@@SAY2@@\n' + pc_html(), 1)
