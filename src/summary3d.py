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

HTML = r"""
<section class="level" id="ai-summary"><div class="wrap">
<h2>SUMMARY — 실측 직물 패턴을 배운 생성 모델로 새 직물을 만들고, 전기 특성을 연속값으로 예측하기</h2>
<p class="lead">1차년도 방법을 3D 공간 하나로 보여 드립니다. 바닥의 두 축은 직물 특성, 세로축은 전기 특성입니다. 단계를 차례로 누르면 <b>실측 → 패턴 학습 → 새 직물 생성 → 전기 특성 예측 → 일부 검증</b>이 쌓입니다. 그림을 끌면 돌아갑니다.</p>
@@SAY1@@
<div class="s3d">
 <div class="cv"><canvas id="s3dCv" aria-label="3D 그림: 직물 특성 두 축과 전기 특성 축 위의 실측 직물, 학습한 패턴, 생성 직물, 예측 범위, 검증 직물"></canvas><span class="hint">끌어서 회전 · 휠로 확대</span></div>
 <div class="side">
  <h5>단계 <span class="stampnote">설명용 모형 · 가상 데이터</span></h5>
  <div class="steps3" role="group" aria-label="단계">
   <button type="button" class="bt" data-s3="1" aria-pressed="true"><b>①</b>실측 직물 27개</button>
   <button type="button" class="bt" data-s3="2" aria-pressed="false"><b>②</b>패턴(결합분포) 학습</button>
   <button type="button" class="bt" data-s3="3" aria-pressed="false"><b>③</b>새 직물 생성</button>
   <button type="button" class="bt" data-s3="4" aria-pressed="false"><b>④</b>전기 특성 예측 (연속값 + 범위)</button>
   <button type="button" class="bt" data-s3="5" aria-pressed="false"><b>⑤</b>일부 제작·측정 검증</button>
  </div>
  <div class="ctrl" style="margin:4px 0 8px"><div class="group"><span class="glabel">생성 수</span><input type="range" id="s3dN" min="20" max="200" step="10" value="80" aria-label="생성 직물 수"><span class="val" id="s3dNv">80</span></div>
  <button type="button" class="bt sm" id="s3dRot" aria-pressed="true">자동 회전</button></div>
  <div class="exp" id="s3dExp" aria-live="polite"></div>
  <div class="lg"><span><i style="background:#2f5d9e"></i>실측 직물</span><br><span><i style="background:#6f5aa8;border-radius:2px"></i>학습한 패턴 (무리별 타원체)</span><br><span><i style="background:#b9a7e8"></i>생성한 새 직물</span><br><span><i style="background:#13733a"></i>예측 곡면과 범위 (±2σ)</span><br><span><i style="background:#c9302c"></i>검증용으로 실제 잰 직물</span></div>
 </div>
</div>
@@SAY2@@
<p class="small muted">축 이름(표면 거칠기, 압축 탄성, 출력 전압)과 점들은 원리를 보여 드리기 위한 가상 값입니다. 실제 직물 특성은 10개 안팎이라 3D로 다 그릴 수 없어, 두 개만 골라 보인 것으로 생각해 주십시오. 실측 데이터가 모이면 같은 그림을 실제 값으로 다시 그립니다. 사진을 벡터로 바꾸는 이전 SUMMARY는 2차년도 이미지 쪽(<a href="image_data.html#img-summary">이미지 데이터 분석</a>)으로 옮겼습니다.</p>
</div></section>
<script>
(function(){
var cv=document.getElementById('s3dCv');if(!cv)return;
function rng(s){return function(){s=(s*69069+1)%4294967296;return s/4294967296}}
var R=rng(7);function gn(){var u=R()||1e-9,v=R();return Math.sqrt(-2*Math.log(u))*Math.cos(6.2832*v)}
function truth(x,z){return 0.15+0.45*x+0.25*z+0.22*Math.sin(2.6*x)}
var CL=[{c:[-0.55,-0.35],s:[0.16,0.14],n:10,nm:'평직 무리'},{c:[0.25,0.45],s:[0.15,0.13],n:9,nm:'능직 무리'},{c:[0.55,-0.4],s:[0.13,0.15],n:8,nm:'편직 무리'}];
var NOISE=0.06,REAL=[];
CL.forEach(function(k,ki){for(var i=0;i<k.n;i++){var x=k.c[0]+k.s[0]*gn(),z=k.c[1]+k.s[1]*gn();REAL.push({x:x,z:z,y:truth(x,z)+NOISE*gn(),k:ki})}});
/* GMM: 무리별 평균·공분산 (3차원: x,z,y) */
function stats(P){var n=P.length,m=[0,0,0];P.forEach(function(p){m[0]+=p.x/n;m[1]+=p.z/n;m[2]+=p.y/n});
 var S=[[0,0,0],[0,0,0],[0,0,0]];P.forEach(function(p){var d=[p.x-m[0],p.z-m[1],p.y-m[2]];for(var i=0;i<3;i++)for(var j=0;j<3;j++)S[i][j]+=d[i]*d[j]/(n-1)});
 for(var i=0;i<3;i++)S[i][i]+=1e-4;return {m:m,S:S,w:n/REAL.length}}
var G=CL.map(function(k,ki){return stats(REAL.filter(function(p){return p.k===ki}))});
function chol(S){var L=[[0,0,0],[0,0,0],[0,0,0]];for(var i=0;i<3;i++)for(var j=0;j<=i;j++){var s=S[i][j];for(var q=0;q<j;q++)s-=L[i][q]*L[j][q];L[i][j]=i===j?Math.sqrt(Math.max(s,1e-9)):s/L[j][j]}return L}
G.forEach(function(g){g.L=chol(g.S)});
function cond(x,z){/* 혼합 조건부 분포 y|x,z: 평균과 표준편차 */
 var ws=[],mu=[],vv=[];G.forEach(function(g){var a=g.S[0][0],b=g.S[0][1],d=g.S[1][1],det=a*d-b*b,ia=[[d/det,-b/det],[-b/det,a/det]];
  var dx=x-g.m[0],dz=z-g.m[1],q=dx*(ia[0][0]*dx+ia[0][1]*dz)+dz*(ia[1][0]*dx+ia[1][1]*dz);
  ws.push(g.w*Math.exp(-q/2)/Math.sqrt(det));var c=[g.S[2][0],g.S[2][1]],k0=c[0]*ia[0][0]+c[1]*ia[1][0],k1=c[0]*ia[0][1]+c[1]*ia[1][1];
  mu.push(g.m[2]+k0*dx+k1*dz);vv.push(Math.max(g.S[2][2]-(k0*c[0]+k1*c[1]),1e-4))});
 var W=ws.reduce(function(a,b){return a+b},0)||1e-12,m=0,v=0;for(var i=0;i<G.length;i++)m+=ws[i]/W*mu[i];for(var i=0;i<G.length;i++)v+=ws[i]/W*(vv[i]+(mu[i]-m)*(mu[i]-m));
 var dens=W;return {m:m,s:Math.sqrt(v),d:dens}}
var GEN=[],VER=[];
function regen(N){var r=rng(91);function g2(){var u=r()||1e-9,v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(6.2832*v)}GEN=[];
 for(var i=0;i<N;i++){var t=r(),k=0,acc=0;for(var j=0;j<G.length;j++){acc+=G[j].w;if(t<=acc){k=j;break}}var g=G[k],e=[g2()*1.25,g2()*1.25,g2()];
  var p=[0,0,0];for(var a=0;a<3;a++){p[a]=g.m[a];for(var b=0;b<=a;b++)p[a]+=g.L[a][b]*e[b]}
  var c=cond(p[0],p[1]);GEN.push({x:p[0],z:p[1],y:c.m,s:c.s})}
 /* 검증 후보: 기대값 최고 3 + 범위 가장 넓은 3 */
 var byM=GEN.slice().sort(function(a,b){return b.y-a.y}).slice(0,3),byS=GEN.slice().sort(function(a,b){return b.s-a.s}).filter(function(p){return byM.indexOf(p)<0}).slice(0,3);
 var r2=rng(5);VER=byM.concat(byS).map(function(p){var u=r2()||1e-9,v=r2();var meas=truth(p.x,p.z)+NOISE*Math.sqrt(-2*Math.log(u))*Math.cos(6.2832*v);return {p:p,y:meas,ok:Math.abs(meas-p.y)<=2*Math.sqrt(p.s*p.s+NOISE*NOISE)}})}
var step=1,yaw=0.75,pitch=0.42,zoom=1,auto=true,N=80;regen(N);
var ctx,W,H;
function prj(x,y,z){/* 월드: x 오른쪽, y 위, z 앞 */var cy=Math.cos(yaw),sy=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch);
 var X=x*cy-z*sy,Z=x*sy+z*cy,Y=y*cp-Z*sp,D=y*sp+Z*cp;var f=4.6/(4.6+D),s=Math.min(W,H)*0.27*zoom;return [W/2+X*s*f,H*0.64-Y*s*f,D]}
function Y3(y){return (y-0.15)*1.3}/* 전기 특성 → 세로 좌표 */
function line(a,b,col,w,dash){var p=prj(a[0],a[1],a[2]),q=prj(b[0],b[1],b[2]);ctx.strokeStyle=col;ctx.lineWidth=w||1;ctx.setLineDash(dash||[]);ctx.beginPath();ctx.moveTo(p[0],p[1]);ctx.lineTo(q[0],q[1]);ctx.stroke();ctx.setLineDash([])}
function txt(t,a,col){var p=prj(a[0],a[1],a[2]);ctx.fillStyle=col||'#5b6874';ctx.fillText(t,p[0],p[1])}
function draw(){var d=window.devicePixelRatio||1;W=cv.clientWidth||700;H=cv.clientHeight||470;if(cv.width!==Math.round(W*d)){cv.width=Math.round(W*d);cv.height=Math.round(H*d)}
 ctx=cv.getContext('2d');ctx.setTransform(d,0,0,d,0,0);ctx.clearRect(0,0,W,H);ctx.font='12px sans-serif';
 var F=-1.05;/* 바닥 높이 */
 for(var i=-4;i<=4;i++){var t=i/4;line([t,F,-1],[t,F,1],'#e6eaef');line([-1,F,t],[1,F,t],'#e6eaef')}
 line([-1,F,-1],[1.15,F,-1],'#16212b',1.5);line([-1,F,-1],[-1,F,1.15],'#16212b',1.5);line([-1,F,-1],[-1,1.0,-1],'#16212b',1.5);
 txt('표면 거칠기 →',[1.2,F,-1.08],'#16212b');txt('압축 탄성 →',[-1.05,F,1.25],'#16212b');txt('출력 전압 ↑',[-1.05,1.08,-1],'#c9302c');
 var items=[];
 /* ② 패턴: 무리별 타원체 테두리 3개 + 바닥 그림자 */
 if(step>=2){G.forEach(function(g){var L=g.L;[[0,1],[0,2],[1,2]].forEach(function(pl){var pts=[];for(var a=0;a<=36;a++){var t=a/36*6.2832,e=[0,0,0];e[pl[0]]=2*Math.cos(t);e[pl[1]]=2*Math.sin(t);
   var p=[0,0,0];for(var r=0;r<3;r++){p[r]=g.m[r];for(var c=0;c<=r;c++)p[r]+=L[r][c]*e[c]}pts.push(prj(p[0],Y3(p[2]),p[1]))}
   ctx.strokeStyle='rgba(111,90,168,.55)';ctx.lineWidth=1.4;ctx.beginPath();pts.forEach(function(q,i){i?ctx.lineTo(q[0],q[1]):ctx.moveTo(q[0],q[1])});ctx.stroke()});
   var sh=[];for(var a=0;a<=36;a++){var t=a/36*6.2832,e=[2*Math.cos(t),2*Math.sin(t),0],x=g.m[0]+L[0][0]*e[0],z=g.m[1]+L[1][0]*e[0]+L[1][1]*e[1];sh.push(prj(x,F,z))}
   ctx.fillStyle='rgba(111,90,168,.10)';ctx.beginPath();sh.forEach(function(q,i){i?ctx.lineTo(q[0],q[1]):ctx.moveTo(q[0],q[1])});ctx.fill()})}
 /* ④ 예측 곡면: 패턴이 있는 곳만 */
 if(step>=4){var n=12;for(var i=0;i<=n;i++)for(var j=0;j<n;j++){var a=-1+2*i/n,b1=-1+2*j/n,b2=-1+2*(j+1)/n,c1=cond(a,b1),c2=cond(a,b2);
   var al=Math.min(1,Math.max(c1.d,c2.d)*1.6);if(al<0.06)continue;
   line([a,Y3(c1.m),b1],[a,Y3(c2.m),b2],'rgba(19,115,58,'+(0.35*al).toFixed(2)+')',1);line([b1,Y3(cond(b1,a).m),a],[b2,Y3(cond(b2,a).m),a],'rgba(19,115,58,'+(0.35*al).toFixed(2)+')',1)}}
 REAL.forEach(function(p){items.push({t:'r',p:p,q:prj(p.x,Y3(p.y),p.z)})});
 if(step>=3)GEN.forEach(function(p){items.push({t:'g',p:p,q:prj(p.x,Y3(step>=4?p.y:F+0.02),p.z)})});
 if(step>=5)VER.forEach(function(v){items.push({t:'v',p:v,q:prj(v.p.x,Y3(v.y),v.p.z)})});
 items.sort(function(a,b){return b.q[2]-a.q[2]});
 items.forEach(function(it){var p=it.p,q=it.q;
  if(it.t==='r'){if(step===1){line([p.x,F,p.z],[p.x,Y3(p.y),p.z],'rgba(47,93,158,.25)',1)}ctx.fillStyle='#2f5d9e';ctx.beginPath();ctx.arc(q[0],q[1],4.6,0,7);ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=1;ctx.stroke()}
  else if(it.t==='g'){if(step>=4){line([p.x,Y3(p.y-2*p.s),p.z],[p.x,Y3(p.y+2*p.s),p.z],'rgba(19,115,58,.5)',1.2)}
   ctx.fillStyle=step>=4?'#8f78d6':'#b9a7e8';ctx.beginPath();ctx.arc(q[0],q[1],3.2,0,7);ctx.fill()}
  else{var e=prj(p.p.x,Y3(p.p.y),p.p.z);line([p.p.x,Y3(p.p.y),p.p.z],[p.p.x,Y3(p.y),p.p.z],'#c9302c',1.5,[3,3]);
   ctx.fillStyle='#c9302c';ctx.beginPath();ctx.arc(q[0],q[1],5.5,0,7);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 10px sans-serif';ctx.fillText(p.ok?'✓':'✗',q[0]-3.5,q[1]+3.5);ctx.font='12px sans-serif'}});
 if(step>=2&&step<4){G.forEach(function(g,i){txt(CL[i].nm,[g.m[0],Y3(g.m[2])+0.32,g.m[1]],'#6f5aa8')})}
}
var EXP={1:'<b>① 실측 직물 27개.</b> 직물마다 직물 특성(바닥 두 축)과 전기 특성(높이)을 함께 쟀습니다. 전기 특성은 엄격한 정답이 아니라 이 직물이 가진 특성 중 하나입니다. 점들이 조직별로 무리 지어 있습니다.',
 2:'<b>② 패턴 학습 (비지도).</b> 생성 모델이 "어떤 직물 특성이 어떤 전기 특성과 함께 나타나는가"를 배웁니다. 보라 타원체가 배운 패턴(결합분포)입니다. 여기서는 가장 단순한 생성 모델인 가우시안 혼합으로 그렸습니다.',
 3:'<b>③ 새 직물 생성.</b> 배운 패턴에서 새 직물을 뽑았습니다(연보라, 바닥). 실측에 없던 직물이지만 패턴 안에서 나왔으므로 그럴듯한 조합입니다. 생성 수를 바꿔 보십시오.',
 4:'<b>④ 전기 특성 예측.</b> 새 직물마다 전기 특성을 연속값(회귀형 출력)으로 냈습니다. 초록 막대가 범위(±2σ)이고 초록 그물이 직물 특성별 예상값의 곡면입니다. 무리에서 먼 직물일수록 막대가 깁니다 — 모델이 덜 확실하다는 뜻입니다.',
 5:'<b>⑤ 일부 제작·측정 검증.</b> 기대값이 가장 높은 3개와 범위가 가장 넓은 3개를 실제로 만들어 쟀다고 가정했습니다(빨강). ✓는 측정값이 예상 범위 안, ✗는 밖입니다. 잰 직물은 실측 데이터에 더해 ②부터 다시 학습합니다.'};
function setStep(s){step=s;document.querySelectorAll('[data-s3]').forEach(function(b){b.setAttribute('aria-pressed',+b.getAttribute('data-s3')<=s?'true':'false')});
 var t=EXP[s];if(s===5){var ok=VER.filter(function(v){return v.ok}).length;t+=' 이번 결과: '+VER.length+'개 중 '+ok+'개가 범위 안.'}document.getElementById('s3dExp').innerHTML=t;draw()}
document.querySelectorAll('[data-s3]').forEach(function(b){b.addEventListener('click',function(){setStep(+b.getAttribute('data-s3'))})});
var sl=document.getElementById('s3dN');sl.addEventListener('input',function(){N=+sl.value;document.getElementById('s3dNv').textContent=N;regen(N);setStep(step)});
var rb=document.getElementById('s3dRot');rb.addEventListener('click',function(){auto=!auto;rb.setAttribute('aria-pressed',auto?'true':'false')});
var drag=null;cv.addEventListener('pointerdown',function(e){drag=[e.clientX,e.clientY,yaw,pitch];auto=false;rb.setAttribute('aria-pressed','false');cv.setPointerCapture(e.pointerId)});
cv.addEventListener('pointermove',function(e){if(!drag)return;yaw=drag[2]+(e.clientX-drag[0])*0.01;pitch=Math.max(-0.1,Math.min(1.3,drag[3]+(e.clientY-drag[1])*0.008));draw()});
cv.addEventListener('pointerup',function(){drag=null});
cv.addEventListener('wheel',function(e){e.preventDefault();zoom=Math.max(0.6,Math.min(1.8,zoom*(e.deltaY<0?1.08:0.93)));draw()},{passive:false});
var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;if(reduce){auto=false;rb.setAttribute('aria-pressed','false')}
var last=0;function tick(t){if(auto&&t-last>33){yaw+=0.006;draw();last=t}requestAnimationFrame(tick)}requestAnimationFrame(tick);
window.addEventListener('resize',draw);setStep(1);
})();
</script>
"""
