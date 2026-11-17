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
<p class="lead">받은 엑셀의 원단 27개를 3D로 그대로 세웠습니다. ①~④는 <b>실측 · 엑셀 직접 집계</b>이고, ⑤⑥은 전기 특성을 잰 뒤에 할 일을 같은 원단 위에 <b>가상 값</b>으로 미리 그려 본 것입니다. 그림을 끌면 돌아가고, 막대나 점에 마우스를 올리면 값이 나옵니다.</p>
@@SAY1@@
<div class="s3d">
 <div class="cv"><canvas id="s3dCv" aria-label="3D 그림: 원단 27개와 측정 묶음 9개의 채움 막대, 공통 19항목, 직물 특성 공간, 전기 특성 연속변수 축, 측정 후 계획"></canvas><span class="hint">끌어서 회전 · 휠로 확대 · 올리면 값 표시</span></div>
 <div class="side">
  <h5>단계</h5>
  <div class="steps3" role="group" aria-label="단계">
   <button type="button" class="bt" data-s3="1" aria-pressed="true"><b>①</b>실측 현황 — 원단 27 × 묶음 9</button>
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
 3:'<b>③ 직물 특성 공간.</b> 19항목을 주성분 분석(PCA)으로 두 축(PC1 열 전달·압축 일·거칠기, PC2 굽힘 일·압축 회복)에 요약해, 원단 27개를 바닥에 놓았습니다(실측, S1과 같은 값). 같은 종류끼리 모이고 부직포는 넓게 흩어집니다. 이 무리 모양이 생성 모델이 배울 "패턴"의 바닥 절반입니다.',
 4:'<b>④ 전기 특성 Y — 연속변수.</b> 세로축이 전기 특성입니다. Y는 "있다/없다" 같은 범주가 아니라 전압·전류·전하밀도처럼 <b>연속변수</b>입니다. 하지만 아직 <b>0개</b> 측정되어 모든 원단의 높이가 "?"입니다. 그래서 S2의 전기 특성 실측이 첫 관문입니다.',
 5:'<b>⑤ 측정 후 — 패턴 학습과 새 직물 (가상).</b> Y를 쟀다고 가정하고 원단들을 높이에 올렸습니다. 생성 모델이 직물 특성과 Y가 함께 나타나는 패턴(보라 타원체, 종류별 무리)을 배우고, 그 패턴에서 새 직물(연보라)을 만듭니다.',
 6:'<b>⑥ 연속값 예측과 일부 검증 (가상).</b> 새 직물마다 Y를 연속값과 범위(초록 막대, ±2σ)로 냅니다. 무리에서 먼 직물일수록 막대가 깁니다. 기대값 최고 3개와 범위가 가장 넓은 3개를 실제로 만들어 잰다고 가정했습니다(빨강, ✓ 범위 안 / ✗ 밖).'};
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
window.addEventListener('resize',draw);setStep(1);
})();
</script>
"""
HTML = HTML_T.replace('@@DATA@@', _data())
