// ---- 슬라이드 넘기기 ----
(function(){
var S=[].slice.call(document.querySelectorAll('.slide')),cur=0,done={};
function fit(){var k=Math.min(innerWidth/1300,innerHeight/740);S.forEach(function(s){s.style.transform='scale('+k+')'})}
function run(f){if(f&&!done[f]&&window[f]){done[f]=1;try{window[f]()}catch(e){console.error(f,e)}}}
function go(i){i=Math.max(0,Math.min(S.length-1,i));S[cur].classList.remove('on');cur=i;S[i].classList.add('on');
 document.getElementById('bar').style.width=((i+1)/S.length*100)+'%';try{history.replaceState(null,'','#'+(i+1))}catch(e){}run(S[i].dataset.init)}
window.goSlide=go;
addEventListener('keydown',function(e){if(e.target.tagName==='INPUT'||e.target.tagName==='SELECT')return;
 if(['ArrowRight','PageDown',' '].indexOf(e.key)>=0){e.preventDefault();go(cur+1)}else if(['ArrowLeft','PageUp'].indexOf(e.key)>=0){e.preventDefault();go(cur-1)}
 else if(e.key==='Home')go(0);else if(e.key==='End')go(S.length-1);else if(e.key==='o'||e.key==='O')ov();else if(e.key==='f'||e.key==='F'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen()}else if(e.key==='Escape')document.getElementById('ov').classList.remove('on')});
document.getElementById('pv').onclick=function(){go(cur-1)};document.getElementById('nx').onclick=function(){go(cur+1)};document.getElementById('ob').onclick=ov;
function ov(){var o=document.getElementById('ov');if(o.classList.contains('on')){o.classList.remove('on');return}
 o.innerHTML=S.map(function(s,i){var h=s.querySelector('h2,h1');return '<div data-i="'+i+'"><b>'+(i+1)+' · '+s.dataset.part+'</b>'+(h?h.textContent:'')+'</div>'}).join('');o.classList.add('on');
 o.querySelectorAll('div').forEach(function(d){d.onclick=function(){o.classList.remove('on');go(+d.dataset.i)}})}
addEventListener('resize',fit);fit();
var h=parseInt(location.hash.slice(1));go(isNaN(h)?0:h-1);
addEventListener('beforeprint',function(){S.forEach(function(s){run(s.dataset.init)})});
document.querySelectorAll('.cp').forEach(function(b){b.onclick=function(){var t=CP[b.dataset.cp];(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){b.textContent='복사됨'},function(){b.textContent='복사 실패'});setTimeout(function(){b.textContent='복사'},1500)}});
})();

// ---- 공통 도구 ----
var COL=['#22398f','#c4561a','#7f9c62','#5b63a8','#e0a84a','#3f8f8f'],INK='#1d2433',GRID='#ebe7de',MUTE='#8a8f99';
var MK=Object.keys(D.M),SK=Object.keys(D.S);
function $(i){return document.getElementById(i)}
function ctx(id){var c=$(id),x=c.getContext('2d');x.clearRect(0,0,c.width,c.height);x.font='13px "Noto Sans KR",sans-serif';x.lineWidth=1;x.globalAlpha=1;return [c,x]}
function ticks(a,b,log){var t=[];if(log){for(var e=Math.floor(Math.log10(a));e<=Math.ceil(Math.log10(b));e++)[1,2,5].forEach(function(m){var v=m*Math.pow(10,e);if(v>=a*0.999&&v<=b*1.001)t.push(v)});return t}
 var st=Math.pow(10,Math.floor(Math.log10((b-a)/5))),r=(b-a)/st;st*=r>25?5:r>10?2:1;for(var v=Math.ceil(a/st)*st;v<=b+1e-9;v+=st)t.push(+v.toPrecision(10));return t}
function fmt(v){var a=Math.abs(v);return a>=1000?v.toFixed(0):a>=10?(+v.toFixed(1)).toString():a>=1?(+v.toFixed(2)).toString():(+v.toPrecision(2)).toString()}
// o: {L,T,W,H,x0,x1,y0,y1,xlog,ylog,xl,yl}
function frame(x,o){var fx=function(v){return o.L+(o.xlog?(Math.log(v)-Math.log(o.x0))/(Math.log(o.x1)-Math.log(o.x0)):(v-o.x0)/(o.x1-o.x0))*o.W},
 fy=function(v){return o.T+o.H-(o.ylog?(Math.log(v)-Math.log(o.y0))/(Math.log(o.y1)-Math.log(o.y0)):(v-o.y0)/(o.y1-o.y0))*o.H};
 x.save();x.font='12px "Noto Sans KR",sans-serif';x.strokeStyle=GRID;x.fillStyle=MUTE;
 ticks(o.x0,o.x1,o.xlog).forEach(function(v){var p=fx(v);x.beginPath();x.moveTo(p,o.T);x.lineTo(p,o.T+o.H);x.stroke();x.textAlign='center';x.fillText(fmt(v),p,o.T+o.H+16)});
 (o.noy?[]:ticks(o.y0,o.y1,o.ylog)).forEach(function(v){var p=fy(v);x.beginPath();x.moveTo(o.L,p);x.lineTo(o.L+o.W,p);x.stroke();x.textAlign='right';x.fillText(fmt(v),o.L-6,p+4)});
 x.strokeStyle='#9aa0aa';x.beginPath();x.moveTo(o.L,o.T);x.lineTo(o.L,o.T+o.H);x.lineTo(o.L+o.W,o.T+o.H);x.stroke();
 x.fillStyle='#3a4152';x.font='13px "Noto Sans KR",sans-serif';x.textAlign='right';if(o.xl)x.fillText(o.xl,o.L+o.W,o.T+o.H+34);
 if(o.yl){x.save();x.translate(o.L-44,o.T);x.rotate(-Math.PI/2);x.textAlign='right';x.fillText(o.yl,0,0);x.restore()}x.restore();return [fx,fy]}
function legend(x,items,L,T){x.save();x.font='13px "Noto Sans KR",sans-serif';var cx=L;items.forEach(function(it){x.fillStyle=it[1];x.fillRect(cx,T-9,12,12);x.fillStyle=INK;x.textAlign='left';x.fillText(it[0],cx+16,T+1);cx+=x.measureText(it[0]).width+34});x.restore()}
function line(x,pts,col,w,dash){x.save();x.strokeStyle=col;x.lineWidth=w||2.5;if(dash)x.setLineDash(dash);x.beginPath();pts.forEach(function(p,i){i?x.lineTo(p[0],p[1]):x.moveTo(p[0],p[1])});x.stroke();x.restore()}
function dot(x,a,b,r,col,al){x.globalAlpha=al==null?1:al;x.fillStyle=col;x.beginPath();x.arc(a,b,r,0,7);x.fill();x.globalAlpha=1}
function rng(seed){var s=seed>>>0||1;return function(){s=(s*1664525+1013904223)>>>0;return s/4294967296}}
function gauss(r){var u=r()||1e-9,v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(6.283185*v)}
function rank(a){var i=a.map(function(v,k){return [v,k]}).sort(function(p,q){return p[0]-q[0]}),r=new Array(a.length);i.forEach(function(p,k){r[p[1]]=k});return r}
function corr(a,b){var n=a.length,ma=0,mb=0;for(var i=0;i<n;i++){ma+=a[i]/n;mb+=b[i]/n}var s=0,sa=0,sb=0;for(i=0;i<n;i++){s+=(a[i]-ma)*(b[i]-mb);sa+=(a[i]-ma)*(a[i]-ma);sb+=(b[i]-mb)*(b[i]-mb)}return s/Math.sqrt(sa*sb)}
function rho(a,b){return corr(rank(a),rank(b))}
function sel(id,keys,names,val){var s=$(id);keys.forEach(function(k){s.add(new Option(names[k],k))});if(val)s.value=val;return s}
function design(m,s,o){var st=D.S[s],d={material:m,structure:s,rh:65,tex:st.kind==='knit'?20:25,cover:st.Kmin?(st.Kmin+st.Kmax)/2:24,warp_share:.52,tf:1.45,kc:5.1,kw:4.05,gsm:150,solidity:.12};for(var k in (o||{}))d[k]=o[k];return d}
function comp(d){return window.MKcompute(d)}
var MCOL={};MK.forEach(function(k,i){MCOL[k]=COL[i%6]});var SCOL={};SK.forEach(function(k,i){SCOL[k]=COL[i%6]});

// ---- 1. 채움 지도 ----
function initCov(){var r=ctx('covCv'),x=r[1],L=110,T=40,cw=60,rh=15,G=D.grp.concat(['전기 Y']);
 x.save();x.font='12px "Noto Sans KR",sans-serif';G.forEach(function(g,j){x.save();x.translate(L+j*cw+cw/2,T-8);x.rotate(-0.5);x.fillStyle=j===8?'#c4561a':INK;x.fillText(g,-14,0);x.restore()});
 D.cov.forEach(function(row,i){x.fillStyle=MUTE;x.textAlign='right';x.fillText(row[0],L-8,T+i*rh+11);x.textAlign='left';
  for(var j=0;j<9;j++){var v=j<8?row[2+j]:0;x.fillStyle=j===8?'#fbeee6':'rgba(34,57,143,'+(0.08+0.85*v)+')';x.fillRect(L+j*cw+1,T+i*rh+1,cw-2,rh-2);if(j===8){x.strokeStyle='#c4561a';x.strokeRect(L+j*cw+1.5,T+i*rh+1.5,cw-3,rh-3)}}});
 x.fillStyle='#c4561a';x.font='bold 13px "Noto Sans KR",sans-serif';x.fillText('비어 있음',L+8*cw+4,T+27*rh+18);x.restore()}

// ---- 2. 범주로 자르기 ----
function initBin(){var v=D.tr.map(function(r){return r[10]}),t=$('binT');
 function dr(){var th=+t.value;$('binV').textContent=th;var r=ctx('binCv'),x=r[1],o={L:60,T:20,W:620,H:320,x0:0,x1:140,y0:0,y1:40,xl:'Voc (V) →',yl:'원단 수'},bins=new Array(28).fill(0);
  v.forEach(function(a){bins[Math.min(27,Math.floor(a/5))]++});o.y1=Math.max.apply(0,bins)+4;var f=frame(x,o);
  bins.forEach(function(b,i){x.fillStyle=(i*5+2.5)>=th?'#c4561a':'#5b63a8';x.globalAlpha=.85;x.fillRect(f[0](i*5)+1,f[1](b),f[0](5)-f[0](0)-2,f[1](0)-f[1](b))});x.globalAlpha=1;
  line(x,[[f[0](th),o.T],[f[0](th),o.T+o.H]],INK,1.5,[5,4]);x.fillStyle=INK;x.fillText('"낮음"',f[0](th)-50,o.T+14);x.fillText('"높음"',f[0](th)+10,o.T+14);
  var hi=v.filter(function(a){return a>=th}),lo=v.filter(function(a){return a<th});
  function rg(a){if(!a.length)return '–';var mn=Math.min.apply(0,a),mx=Math.max.apply(0,a);return mn.toFixed(0)+'~'+mx.toFixed(0)+' V ('+(mx/mn).toFixed(1)+'배)'}
  $('binA').textContent=rg(hi);$('binB').textContent=rg(lo)}
 t.oninput=dr;dr()}

// ---- 2. 반복 측정 ----
function initRep(){var c=$('repC'),n=$('repN');
 function dr(){var cv=+c.value,k=+n.value;$('repCV').textContent=cv.toFixed(2);$('repNV').textContent=k;var R=rng(7),m=[];
  for(var i=0;i<300;i++){var s=0;for(var j=0;j<k;j++)s+=60*Math.exp(0.06*0+cv*gauss(R)-cv*cv/2);m.push(s/k)}
  var r=ctx('repCv'),x=r[1],o={L:60,T:20,W:620,H:320,x0:20,x1:100,y0:0,y1:80,xl:'측정 평균 (V) →',yl:'횟수'},bins=new Array(40).fill(0);
  m.forEach(function(a){var b=Math.floor((a-20)/2);if(b>=0&&b<40)bins[b]++});o.y1=Math.max(20,Math.max.apply(0,bins)+5);var f=frame(x,o);
  bins.forEach(function(b,i){x.fillStyle='#5b63a8';x.globalAlpha=.8;x.fillRect(f[0](20+i*2)+1,f[1](b),f[0](22)-f[0](20)-2,f[1](0)-f[1](b))});x.globalAlpha=1;
  line(x,[[f[0](60),o.T],[f[0](60),o.T+o.H]],'#c4561a',2.5);x.fillStyle='#c4561a';x.font='bold 13px sans-serif';x.fillText('참값 60 V',f[0](60)+6,o.T+14);
  var sd=cv/Math.sqrt(k);$('repR').textContent=(60*Math.exp(-1.96*sd)).toFixed(0)+' ~ '+(60*Math.exp(1.96*sd)).toFixed(0)+' V'}
 c.oninput=dr;n.oninput=dr;dr()}

// ---- 4. TENG ----
function initTeng(){var s=$('tgS');function dr(){var sg=+s.value;$('tgSV').textContent=sg.toFixed(2);var r=ctx('tgCv'),x=r[1],o={L:60,T:20,W:470,H:260,x0:0,x1:3,y0:0,y1:400,xl:'간격 x (mm) →',yl:'Voc (V)'},f=frame(x,o);
 [0.1,0.3,0.6,1.0].forEach(function(v,i){var p=[];for(var g=0;g<=3;g+=0.05)p.push([f[0](g),f[1](Math.min(400,v*1e-6*g*1e-3/8.854e-12))]);line(x,p,'#c9c3b4',1.5);x.fillStyle=MUTE;x.fillText('σ='+v,f[0](Math.min(2.9,400*8.854e-12/(v*1e-9)))-34,f[1](Math.min(400,v*112.9*3))+(v<0.5?-6:14))});
 var p=[];for(var g=0;g<=3;g+=0.05)p.push([f[0](g),f[1](Math.min(400,sg*112.94*g))]);line(x,p,'#c4561a',3.5);
 line(x,[[f[0](1),o.T],[f[0](1),o.T+o.H]],INK,1,[4,4]);dot(x,f[0](1),f[1](Math.min(400,sg*112.94)),6,'#c4561a');x.fillStyle=INK;x.fillText('프로토콜 1 mm',f[0](1)+6,o.T+12);
 var v=sg*112.94,q=sg*1e-6*25e-4*1e9;$('tgV').textContent=v.toFixed(0)+' V';$('tgQ').textContent=q.toFixed(2)+' nC';$('tgI').textContent=(2*q*2).toFixed(1)+' nA'}
 s.oninput=dr;dr()}

// ---- 4. 대전 서열 ----
function initTribo(){var s=$('trRef');s.add(new Option('PTFE 필름 (프로토콜)','PTFE'));MK.forEach(function(k){s.add(new Option(D.M[k].ko,k))});
 function dr(){var ref=s.value==='PTFE'?D.C.tribo:D.M[s.value].tribo,r=ctx('trCv'),x=r[1],L=60,W=600,y0=80,f=function(v){return L+(v+1.1)/2.2*W};
  x.strokeStyle='#9aa0aa';x.lineWidth=2;x.beginPath();x.moveTo(L,y0);x.lineTo(L+W,y0);x.stroke();x.fillStyle=MUTE;x.font='12px sans-serif';
  [-1,-0.5,0,0.5,1].forEach(function(v){x.fillText(v,f(v)-8,y0+18)});x.fillStyle='#22398f';x.font='bold 13px "Noto Sans KR",sans-serif';x.fillText('← 전자를 받음 (−)',L,y0-44);x.textAlign='right';x.fillText('전자를 내줌 (+) →',L+W,y0-44);x.textAlign='left';
  var pts=[['PTFE',D.C.tribo,'#22398f']].concat(MK.map(function(k){return [D.M[k].ko,D.M[k].tribo,MCOL[k]]}));
  pts.forEach(function(p,i){dot(x,f(p[1]),y0,8,p[2]);x.fillStyle=INK;x.font='13px "Noto Sans KR",sans-serif';x.fillText(p[0],f(p[1])-14,y0-(i%2?14:26))});
  dot(x,f(ref),y0,13,'rgba(196,86,26,.25)');
  var bx=L,by=150,bw=W;x.fillStyle=INK;x.font='bold 14px "Noto Sans KR",sans-serif';x.fillText('Δ = 소재 − 상대 전극   (σ에 곱해지는 값)',bx,by);
  MK.forEach(function(k,i){var d=D.M[k].tribo-ref,yy=by+22+i*40,c=L+bw/2;x.fillStyle=INK;x.font='13px "Noto Sans KR",sans-serif';x.fillText(D.M[k].ko,bx,yy+16);
   x.fillStyle=d>=0?'#c4561a':'#5b63a8';x.fillRect(d>=0?c:c+d*bw/4.4,yy+2,Math.abs(d)*bw/4.4,22);x.fillStyle=INK;x.fillText((d>=0?'+':'')+d.toFixed(2),d>=0?c+d*bw/4.4+6:c+d*bw/4.4-44,yy+18)});
  line(x,[[L+bw/2,by+16],[L+bw/2,by+226]],'#9aa0aa',1)}
 s.onchange=dr;dr()}

// ---- 4. 거칠기 역U ----
function initRough(){var o2=$('ruOpt'),sm=D.sra_med;function dr(){var op=+o2.value;$('ruV').textContent=op;var r=ctx('ruCv'),x=r[1],o={L:60,T:20,W:470,H:320,x0:5,x1:200,y0:0,y1:1.05,xlog:1,xl:'거칠기 SRA (μm, 로그) →',yl:'g(SRA)'},f=frame(x,o),p=[];
 for(var i=0;i<=200;i++){var v=5*Math.pow(40,i/200);p.push([f[0](v),f[1](Math.exp(-Math.pow(Math.log(v/op),2)/1.28))])}line(x,p,'#c4561a',3);
 Object.keys(sm).forEach(function(k,i){var v=sm[k],g=Math.exp(-Math.pow(Math.log(v/op),2)/1.28);dot(x,f[0](v),f[1](g),7,COL[i]);x.fillStyle=COL[i];x.fillText('●',o.L+12,o.T+o.H-112+i*20);x.fillStyle=INK;x.fillText(k+'  '+v+' μm',o.L+28,o.T+o.H-112+i*20)})}
 o2.oninput=dr;dr()}

// ---- 4. 압력 ----
function initPress(){var s=sel('prM',MK,D.mats,'nylon');function dr(){var m=s.value,r=ctx('prCv'),x=r[1],o={L:60,T:30,W:620,H:320,x0:0,x1:20,y0:0,y1:1.6,xl:'누르는 압력 P (kPa) →',yl:'실접촉 지수 ci'},f=frame(x,o),it=[];
 SK.forEach(function(k,i){var c=comp(design(m,k)),ps=6/(1+4*c.v.CW_F),a=D.S[k].surf*c.y.gr,p=[];for(var P=0;P<=20;P+=0.25)p.push([f[0](P),f[1](a*(1-Math.exp(-P/ps)))]);line(x,p,SCOL[k],2.8);it.push([D.S[k].ko,SCOL[k]])});
 line(x,[[f[0](5),o.T],[f[0](5),o.T+o.H]],INK,1.2,[5,4]);x.fillStyle=INK;x.fillText('프로토콜 5 kPa',f[0](5)+6,o.T+o.H-8);legend(x,it,o.L,14)}
 s.onchange=dr;dr()}

// ---- 4. 습도 ----
function initHum(){var s=sel('huS',SK,D.strs,'twill22');function dr(){var k=s.value,r=ctx('huCv'),x=r[1],o={L:60,T:30,W:620,H:320,x0:30,x1:90,y0:0,y1:140,xl:'상대습도 RH (%) →',yl:'Voc (V)'},it=[];
 var mx=0;MK.forEach(function(m){mx=Math.max(mx,comp(design(m,k,{rh:30})).y.Voc)});o.y1=Math.ceil(mx/20)*20+10;var f=frame(x,o);
 x.fillStyle='rgba(196,86,26,.12)';x.fillRect(f[0](63),o.T,f[0](67)-f[0](63),o.H);
 MK.forEach(function(m){var p=[];for(var h=30;h<=90;h+=1)p.push([f[0](h),f[1](comp(design(m,k,{rh:h})).y.Voc)]);line(x,p,MCOL[m],2.8);it.push([D.M[m].ko+' '+D.M[m].regain+'%',MCOL[m]])});legend(x,it,o.L,12);x.fillStyle=MUTE;x.textAlign='right';x.fillText('(소재 · 표준 수분율)',o.L+o.W,12);x.textAlign='left'}
 s.onchange=dr;dr()}

// ---- 4. 커버 팩터 ----
function initCover(){var s=sel('cfM',MK,D.mats,'nylon');function dr(){var m=s.value,r=ctx('cfCv'),x=r[1],W=['plain','twill22','hopsack22'],it=[];
 var A={L:70,T:28,W:610,H:150,x0:16,x1:36,y0:0,y1:80,yl:'SRA (μm)'},Bo={L:70,T:220,W:610,H:170,x0:16,x1:36,y0:0,y1:140,xl:'커버 팩터 K (경사+위사) →',yl:'Voc (V)'},curves={};
 W.forEach(function(k){var st=D.S[k],a=[],b=[];for(var K=16;K<=st.jam*0.98;K+=0.25){var c=comp(design(m,k,{cover:K}));a.push([K,c.v.SRA_F]);b.push([K,c.y.Voc])}curves[k]=[a,b]});
 var sv=[].concat.apply([],W.map(function(k){return curves[k][0].map(function(p){return p[1]})}));A.y0=Math.max(0,Math.floor(Math.min.apply(0,sv)/5)*5-5);A.y1=Math.max(Math.ceil(Math.max.apply(0,sv)/5)*5+5,D.sopt+5);
 Bo.y1=Math.ceil(Math.max.apply(0,W.map(function(k){return Math.max.apply(0,curves[k][1].map(function(p){return p[1]}))}))/20)*20+10;
 var fa=frame(x,A),fb=frame(x,Bo);W.forEach(function(k){line(x,curves[k][0].map(function(p){return [fa[0](p[0]),fa[1](p[1])]}),SCOL[k],2.8);line(x,curves[k][1].map(function(p){return [fb[0](p[0]),fb[1](p[1])]}),SCOL[k],2.8);
  var e=curves[k][1][curves[k][1].length-1];dot(x,fb[0](e[0]),fb[1](e[1]),5,SCOL[k]);it.push([D.S[k].ko+' (막힘 '+D.S[k].jam+')',SCOL[k]])});
 line(x,[[fa[0](16),fa[1](D.sopt)],[fa[0](36),fa[1](D.sopt)]],'#c4561a',1.2,[5,4]);x.fillStyle='#c4561a';x.fillText('SRA_opt '+D.sopt,A.L+A.W-90,fa[1](D.sopt)-5);legend(x,it,A.L,14)}
 s.onchange=dr;dr()}

// ---- 4. 두 인자 지도 ----
function initMap(){var r=ctx('mpCv'),x=r[1],o={L:70,T:20,W:600,H:380,x0:5,x1:200,y0:0,y1:2,xlog:1,xl:'거칠기 SRA (μm, 로그) →',yl:'대전 서열 차 Δ (대 PTFE)'},f;
 var lx=function(v){return 5*Math.pow(40,v)},Z=function(s,d){return D.s0*d*Math.exp(-Math.pow(Math.log(s/D.sopt),2)/1.28)*112.94};
 for(var i=0;i<120;i++)for(var j=0;j<76;j++){var s=lx((i+.5)/120),d=2*(j+.5)/76,v=Z(s,d)/130;x.fillStyle='rgba(34,57,143,'+Math.min(.9,v*0.9+0.03)+')';x.fillRect(o.L+i*o.W/120,o.T+o.H-(j+1)*o.H/76,o.W/120+0.6,o.H/76+0.6)}
 f=frame(x,o);
 [20,40,60,80,100].forEach(function(lv){x.fillStyle='#fff';for(var i=0;i<400;i++){var s=lx(i/400);for(var j=0;j<300;j++){var d=2*j/300;if(Math.abs(Z(s,d)-lv)<0.35){x.fillRect(f[0](s),f[1](d),1.6,1.6)}}}
  var s0=D.sopt,d0=lv/(D.s0*112.94);if(d0<2){x.font='bold 12px sans-serif';x.fillText(lv+' V',f[0](s0)+4,f[1](d0)-4)}});
 var R=rng(3);D.tr.forEach(function(t){var d=D.M[t[0]].tribo-D.C.tribo+(R()-.5)*0.06;dot(x,f[0](t[4]),f[1](d),3,'#e0a84a',.9)});
 MK.forEach(function(k){var d=D.M[k].tribo-D.C.tribo;x.fillStyle='#fff';x.font='bold 13px "Noto Sans KR",sans-serif';x.fillText(D.M[k].ko,o.L+o.W-80,f[1](d)-6)})}

// ---- 4. 토네이도 ----
function initTor(){var sm=sel('toM',MK,D.mats,'nylon'),ss=sel('toS',SK,D.strs,'twill22');
 function dr(){var m=sm.value,k=ss.value,kind=D.S[k].kind,base=design(m,k),b0=comp(base).y.Voc,P={woven:[['tex','실 선밀도 tex'],['cover','커버 팩터'],['warp_share','경사 비중'],['rh','상대습도']],knit:[['tex','실 선밀도 tex'],['tf','조임 계수 TF'],['kc','코스 상수 Kc'],['rh','상대습도']],nonwoven:[['gsm','평량 설계값'],['solidity','고형률'],['rh','상대습도']]}[kind];
  var rows=P.map(function(p){var lo={},hi={};lo[p[0]]=base[p[0]]*0.85;hi[p[0]]=base[p[0]]*1.15;return [p[1],comp(design(m,k,lo)).y.Voc-b0,comp(design(m,k,hi)).y.Voc-b0]}).sort(function(a,b){return Math.max(Math.abs(b[1]),Math.abs(b[2]))-Math.max(Math.abs(a[1]),Math.abs(a[2]))});
  var r=ctx('toCv'),x=r[1],mx=Math.max(1,Math.max.apply(0,rows.map(function(q){return Math.max(Math.abs(q[1]),Math.abs(q[2]))}))),cx=450,sc=165/mx;
  x.fillStyle=INK;x.font='bold 14px "Noto Sans KR",sans-serif';x.fillText('기준 Voc '+b0.toFixed(1)+' V  ('+D.M[m].ko+' · '+D.S[k].ko+')',20,24);
  rows.forEach(function(q,i){var y=60+i*72;x.fillStyle=INK;x.font='14px "Noto Sans KR",sans-serif';x.textAlign='left';x.fillText(q[0],10,y+26);
   [[q[1],'#5b63a8','−15%'],[q[2],'#c4561a','+15%']].forEach(function(z,j){var v=z[0],w=v*sc;x.fillStyle=z[1];x.fillRect(Math.min(cx,cx+w),y+j*24,Math.abs(w),20);x.fillStyle=INK;x.font='12px sans-serif';x.fillText(z[2]+' '+(v>=0?'+':'')+v.toFixed(1)+' V',v>=0?cx+w+6:cx+w-92,y+j*24+15)})});
  line(x,[[cx,40],[cx,60+rows.length*72]],INK,1.5)}
 sm.onchange=dr;ss.onchange=dr;dr()}

// ---- 4. 분해 ----
function initWf(){var sm=sel('wfM',MK,D.mats,'nylon'),ss=sel('wfS',SK,D.strs,'twill22');
 function dr(){var m=sm.value,k=ss.value,c=comp(design(m,k)),y=c.y,surf=D.S[k].surf,sat=y.ci/(surf*y.gr),st=[['σ₀ 규모',D.s0,'보정 상수 (μC/m²)'],['× 대전 서열 차 Δ',y.dtr,D.M[m].ko+' − PTFE'],['× 구조 접촉 표면',surf,D.S[k].ko],['× 거칠기 g(SRA)',y.gr,'SRA '+c.v.SRA_F.toFixed(1)+' μm'],['× 압력 포화',sat,'5 kPa, CW '+c.v.CW_F.toFixed(3)],['× 습도 계수',y.hum,'RH 65%']];
  var run=1,h='',mx=D.s0*2.2;st.forEach(function(s,i){run=i?run*s[1]:s[1];h+='<div class="wf"><span><b>'+s[0]+'</b> '+s[1].toFixed(3)+'</span><i style="width:'+Math.min(100,run/mx*100)+'%"></i><em>'+s[2]+'</em></div>'});
  h+='<div class="wf"><span><b>= σ</b> '+y.sigma.toFixed(3)+' μC/m²</span><i class="o" style="width:'+Math.min(100,y.sigma/mx*100)+'%"></i><em></em></div>';
  h+='<div class="wf"><span><b>Voc = σ·x/ε₀</b></span><i class="o" style="width:'+Math.min(100,y.Voc/150*100)+'%"></i><em><b style="font-size:20px;color:#c4561a">'+y.Voc.toFixed(1)+' V</b></em></div>';$('wfOut').innerHTML=h}
 sm.onchange=dr;ss.onchange=dr;dr()}

// ---- 4. 산점도 ----
function initScat(){var s=$('scX');D.x8.forEach(function(n,i){s.add(new Option(n,i))});s.value=1;
 function dr(){var j=+s.value,xs=D.tr.map(function(r){return r[2+j]}),ys=D.tr.map(function(r){return r[10]}),r=ctx('scCv'),x=r[1];
  var o={L:70,T:30,W:610,H:330,x0:Math.min.apply(0,xs)*0.9,x1:Math.max.apply(0,xs)*1.1,y0:3,y1:200,xlog:1,ylog:1,xl:D.x8[j]+' (로그) →',yl:'Voc (V, 로그)'},f=frame(x,o);
  D.tr.forEach(function(t,i){dot(x,f[0](xs[i]),f[1](ys[i]),3.4,MCOL[t[0]],.75)});legend(x,MK.map(function(k){return [D.M[k].ko,MCOL[k]]}),o.L,14);
  $('scR').textContent=rho(xs,ys).toFixed(2);var w=MK.map(function(k){var a=[],b=[];D.tr.forEach(function(t,i){if(t[0]===k){a.push(xs[i]);b.push(ys[i])}});return rho(a,b)});$('scR2').textContent=(w.reduce(function(p,q){return p+q})/w.length).toFixed(2)}
 s.onchange=dr;dr()}

// ---- 5. 열마다 섞기 ----
function initShuf(){var s=$('shP'),R=rng(11),cols=[];for(var j=0;j<9;j++){var c=D.tr.map(function(r){return r[2+j]}),p=c.slice();for(var i=p.length-1;i>0;i--){var k=Math.floor(R()*(i+1)),t=p[i];p[i]=p[k];p[k]=t}cols.push([c,p])}
 function sc(id,xs,ys,title,col){var r=ctx(id),x=r[1],o={L:60,T:30,W:470,H:200,x0:Math.min.apply(0,xs)*0.9,x1:Math.max.apply(0,xs)*1.1,y0:3,y1:200,xlog:1,ylog:1,yl:'Voc'},f=frame(x,o);
  xs.forEach(function(v,i){dot(x,f[0](v),f[1](ys[i]),3,col,.6)});x.fillStyle=INK;x.font='bold 14px "Noto Sans KR",sans-serif';x.fillText(title+'   ρ = '+rho(xs,ys).toFixed(2),o.L,18)}
 function mat(id,k,title){var r=ctx(id),x=r[1],n=9,cs=16,L=70,T=12,names=D.x8.concat(['Voc']);var tx=L+n*(cs+2)+16;x.fillStyle=INK;x.font='bold 13px "Noto Sans KR",sans-serif';x.fillText(title,tx,40);x.font='12px sans-serif';x.fillStyle=MUTE;x.fillText('순위 상관 행렬 (주황 +, 남색 −)',tx,60);x.font='11px sans-serif';
  for(var a=0;a<n;a++)for(var b=0;b<n;b++){var v=a===b?1:rho(cols[a][k],cols[b][k]);x.fillStyle=v>=0?'rgba(196,86,26,'+Math.abs(v)+')':'rgba(34,57,143,'+Math.abs(v)+')';x.fillRect(L+b*(cs+2),T+a*(cs+2),cs,cs)}
  x.fillStyle=MUTE;names.forEach(function(nm,a){x.textAlign='right';x.fillText(nm,L-4,T+a*(cs+2)+11)});x.textAlign='left'}
 function dr(){var j=+s.value;sc('shA',cols[j][0],cols[8][0],'메커니즘 순서','#22398f');sc('shB',cols[j][1],cols[8][1],'열마다 독립','#c4561a')}
 s.onchange=dr;dr();mat('shM1',0,'메커니즘: 색 있는 칸 = 관계');mat('shM2',1,'열마다 독립: 대각선 밖이 빔')}

// ---- 5. 잡음 천장 ----
function initNoise(){var c=$('nzC'),n=$('nzN'),lv=D.tr.map(function(r){return Math.log(r[10])}),m=lv.reduce(function(a,b){return a+b})/lv.length,vt=lv.reduce(function(a,b){return a+(b-m)*(b-m)},0)/(lv.length-1);
 function dr(){var cv=+c.value,k=+n.value;$('nzCV').textContent=cv.toFixed(2);$('nzNV').textContent=k;var sd=cv/Math.sqrt(k),R=rng(5),r=ctx('nzCv'),x=r[1],o={L:70,T:20,W:610,H:330,x0:3,x1:200,y0:3,y1:200,xlog:1,ylog:1,xl:'참값 Voc (V) →',yl:'관측 Voc (V)'},f=frame(x,o);
  line(x,[[f[0](3),f[1](3)],[f[0](200),f[1](200)]],'#9aa0aa',1.2,[4,4]);D.tr.forEach(function(t){var v=t[10],ob=v*Math.exp(sd*gauss(R));dot(x,f[0](v),f[1](Math.max(3,Math.min(200,ob))),3,'#5b63a8',.6)});
  $('nzR').textContent=(vt/(vt+sd*sd)).toFixed(3)}
 c.oninput=dr;n.oninput=dr;dr()}

// ---- 5. 학습 곡선 ----
function initLC(){var r=ctx('lcCv'),x=r[1],o={L:70,T:30,W:610,H:330,x0:10,x1:500,y0:-0.2,y1:1,xlog:1,xl:'학습 원단 수 (로그) →',yl:'시험 R²'},f=frame(x,o),it=[];
 Object.keys(D.lc).forEach(function(k,i){var a=D.lc[k],col=['#22398f','#c4561a','#7f9c62'][i%3];x.fillStyle=['rgba(34,57,143,.13)','rgba(196,86,26,.13)','rgba(127,156,98,.18)'][i%3];x.beginPath();
  a.forEach(function(p,j){var X=f[0](p[0]),Y=f[1](Math.min(1,p[1]+p[2]));j?x.lineTo(X,Y):x.moveTo(X,Y)});a.slice().reverse().forEach(function(p){x.lineTo(f[0](p[0]),f[1](Math.max(-0.2,p[1]-p[2])))});x.fill();
  line(x,a.map(function(p){return [f[0](p[0]),f[1](p[1])]}),col,3);a.forEach(function(p){dot(x,f[0](p[0]),f[1](p[1]),4,col)});it.push([k,col])});
 x.fillStyle='rgba(127,156,98,.18)';x.fillRect(f[0](50),o.T,f[0](120)-f[0](50),o.H);x.fillStyle='#3f7a3a';x.font='bold 13px "Noto Sans KR",sans-serif';x.fillText('S2 목표 구간',f[0](52),o.T+o.H-10);legend(x,it,o.L,14)}

// ---- 6. LHS ----
function initLHS(){var n=$('lhN'),seed=1;function dr(){var N=+n.value,R=rng(seed);$('lhV').textContent=N;var r=ctx('lhCv'),x=r[1];
 [[0,'무작위'],[1,'라틴 하이퍼큐브']].forEach(function(p){var L=20+p[0]*295,T=28,S=260;x.fillStyle=INK;x.font='bold 14px "Noto Sans KR",sans-serif';x.fillText(p[1],L,18);x.strokeStyle=GRID;
  for(var i=0;i<=N;i++){x.beginPath();x.moveTo(L+S*i/N,T);x.lineTo(L+S*i/N,T+S);x.moveTo(L,T+S*i/N);x.lineTo(L+S,T+S*i/N);x.stroke()}
  var pts=[];if(p[0]===0){for(var i=0;i<N;i++)pts.push([R(),R()])}else{var b=[];for(var i=0;i<N;i++)b.push(i);for(var i=N-1;i>0;i--){var j=Math.floor(R()*(i+1)),t=b[i];b[i]=b[j];b[j]=t}for(var i=0;i<N;i++)pts.push([(i+R())/N,(b[i]+R())/N])}
  pts.forEach(function(q){dot(x,L+q[0]*S,T+(1-q[1])*S,5,p[0]?'#22398f':'#c4561a')});x.strokeStyle='#9aa0aa';x.strokeRect(L,T,S,S)})}
 n.oninput=dr;$('lhR').onclick=function(){seed=Math.floor(Math.random()*1e6)+2;dr()};dr()}

// ---- 6. 분포 ----
function initDist(){var si=$('dsItem'),sb=$('dsBy'),names=D.x8.concat(['Voc_V']);names.forEach(function(n,i){si.add(new Option(n,i))});si.value=names.length-1;
 function dr(){var k=+si.value,by=+sb.value,r=ctx('dsCv'),x=r[1],L=170,T=20,W=930,H=410,g={},keys;
  D.tr.forEach(function(row){var key=by?D.strs[row[1]]:D.mats[row[0]];(g[key]=g[key]||[]).push(row[2+k])});keys=Object.keys(g);
  var all=[].concat.apply([],keys.map(function(q){return g[q]})),lo=Math.min.apply(0,all)*0.9,hi=Math.max.apply(0,all)*1.1,o={L:L,T:T,W:W,H:H,x0:lo,x1:hi,y0:0,y1:1,xlog:1,noy:1,xl:names[k]+' (로그 눈금) →'};
  var f=frame(x,o),rh=H/keys.length;
  keys.forEach(function(q,i){var a=g[q].slice().sort(function(u,v){return u-v}),y0=T+i*rh+rh/2,qq=function(p){return a[Math.floor(p*(a.length-1))]};
   x.fillStyle=INK;x.font='14px "Noto Sans KR",sans-serif';x.textAlign='right';x.fillText(q+' ('+a.length+')',L-10,y0+5);x.textAlign='left';
   x.fillStyle='rgba(34,57,143,.12)';x.fillRect(f[0](qq(.25)),y0-rh*.3,f[0](qq(.75))-f[0](qq(.25)),rh*.6);x.fillStyle='#22398f';x.fillRect(f[0](qq(.5))-1.5,y0-rh*.34,3,rh*.68);
   var R=rng(7+i);a.forEach(function(v){dot(x,f[0](v),y0+(R()-.5)*rh*.5,2.6,COL[(i+1)%6],.55)})})}
 si.onchange=dr;sb.onchange=dr;dr()}

// ---- 7. KS ----
function initKS(){var s=$('ksI'),map=[[2,0],[7,1],[4,2],[9,3],[10,8]];
 function dr(){var m=map[+s.value],a=D.tr.map(function(r){return r[m[0]]}).sort(function(p,q){return p-q}),b=D.gen.map(function(r){return r[m[1]]}).sort(function(p,q){return p-q}),r=ctx('ksCv'),x=r[1];
  var o={L:60,T:16,W:470,H:160,x0:Math.min(a[0],b[0])*0.9,x1:Math.max(a[a.length-1],b[b.length-1])*1.1,y0:0,y1:1,xlog:1,yl:'누적 비율'},f=frame(x,o);
  function cdf(arr,v){var lo=0,hi=arr.length;while(lo<hi){var md=(lo+hi)>>1;if(arr[md]<=v)lo=md+1;else hi=md}return lo/arr.length}
  [[a,'#5b63a8','학습(실측 역할)'],[b,'#c4561a','생성']].forEach(function(z){line(x,z[0].map(function(v,i){return [f[0](v),f[1]((i+1)/z[0].length)]}),z[1],2.5)});
  var ks=0,at=0;a.concat(b).forEach(function(v){var d=Math.abs(cdf(a,v)-cdf(b,v));if(d>ks){ks=d;at=v}});line(x,[[f[0](at),f[1](cdf(a,at))],[f[0](at),f[1](cdf(b,at))]],INK,2,[3,3]);
  legend(x,[['학습','#5b63a8'],['생성','#c4561a']],o.L+10,o.T+12);$('ksV').textContent=ks.toFixed(3)}
 s.onchange=dr;dr()}

// ---- 7. CV ----
function initCV(){var t=$('cvT'),cv=D.tr.map(function(r){return r[11]}).sort(function(a,b){return a-b});$('cvM').textContent=cv[Math.floor(cv.length/2)].toFixed(3);
 function dr(){var th=+t.value;$('cvV').textContent=th.toFixed(2);var r=ctx('cvCv'),x=r[1],bins=new Array(30).fill(0);cv.forEach(function(v){bins[Math.min(29,Math.floor(v/0.01))]++});
  var o={L:60,T:20,W:620,H:320,x0:0,x1:0.3,y0:0,y1:Math.max.apply(0,bins)+4,xl:'Voc 반복 변동계수 CV →',yl:'원단 수'},f=frame(x,o);
  bins.forEach(function(b,i){x.fillStyle=(i+.5)*0.01>th?'#c4561a':'#5b63a8';x.globalAlpha=.85;x.fillRect(f[0](i*0.01)+1,f[1](b),f[0](0.01)-f[0](0)-2,f[1](0)-f[1](b))});x.globalAlpha=1;
  line(x,[[f[0](th),o.T],[f[0](th),o.T+o.H]],INK,1.5,[5,4]);$('cvN').textContent=cv.filter(function(v){return v>th}).length+' / '+cv.length}
 t.oninput=dr;dr()}

// ---- 7. 간접 상관 ----
function initConf(){var mode=0,bs=document.querySelectorAll('[data-cf]');
 function med(a){var b=a.slice().sort(function(p,q){return p-q});return b[Math.floor(b.length/2)]}
 var mq={},mv={};MK.forEach(function(k){var a=D.tr.filter(function(t){return t[0]===k});mq[k]=med(a.map(function(t){return Math.log(t[9])}));mv[k]=med(a.map(function(t){return Math.log(t[10])}))});
 function dr(){var xs=D.tr.map(function(t){return mode?Math.log(t[9])-mq[t[0]]:t[9]}),ys=D.tr.map(function(t){return mode?Math.log(t[10])-mv[t[0]]:t[10]}),r=ctx('cfdCv'),x=r[1];
  var o=mode?{L:70,T:30,W:610,H:320,x0:-0.6,x1:0.6,y0:-1.6,y1:1.6,xl:'log Qmax − 소재 중앙값 →',yl:'log Voc − 소재 중앙값'}:{L:70,T:30,W:610,H:320,x0:Math.min.apply(0,xs)*0.9,x1:Math.max.apply(0,xs)*1.1,y0:3,y1:200,xlog:1,ylog:1,xl:'냉온감 Qmax_F (로그) →',yl:'Voc (V, 로그)'},f=frame(x,o);
  D.tr.forEach(function(t,i){dot(x,f[0](Math.max(o.x0,Math.min(o.x1,xs[i]))),f[1](Math.max(o.y0,Math.min(o.y1,ys[i]))),3.4,MCOL[t[0]],.75)});legend(x,MK.map(function(k){return [D.M[k].ko,MCOL[k]]}),o.L,14);
  $('cfR').textContent=rho(xs,ys).toFixed(2)}
 bs.forEach(function(b){b.onclick=function(){mode=+b.dataset.cf;bs.forEach(function(q){q.classList.toggle('on',q===b)});dr()}});dr()}

// ---- 8. PCA ----
function initPCA(){var by=$('pcBy'),wsel=$('pcW'),c=$('pcCv'),hov=-1,pts=[];
 function dr(){var r=ctx('pcCv'),x=r[1],P=D.pc,xs=P.map(function(p){return p[0]}),ys=P.map(function(p){return p[1]}),k=+by.value;
  var o={L:60,T:34,W:520,H:360,x0:Math.min.apply(0,xs)-0.5,x1:Math.max.apply(0,xs)+0.5,y0:Math.min.apply(0,ys)-0.5,y1:Math.max.apply(0,ys)+0.5,xl:'PC1 ('+Math.round(D.ev[0]*100)+'%) →',yl:'PC2 ('+Math.round(D.ev[1]*100)+'%)'},f=frame(x,o);pts=[];
  D.tr.forEach(function(row,i){var key=k?row[1]:row[0],col=k?SCOL[key]:MCOL[key],px=f[0](P[i][0]),py=f[1](P[i][1]);pts.push([px,py,i]);dot(x,px,py,i===hov?6:3.5,col,.75)});
  legend(x,(k?SK:MK).map(function(q){return [k?D.S[q].ko:D.M[q].ko,k?SCOL[q]:MCOL[q]]}),o.L,14);
  if(hov>=0){var row=D.tr[hov],s=D.mats[row[0]]+' · '+D.strs[row[1]]+' · Voc '+row[10].toFixed(1)+' V';x.fillStyle='rgba(29,36,51,.92)';x.fillRect(o.L+10,o.T+o.H-34,x.measureText(s).width+16,24);x.fillStyle='#fff';x.fillText(s,o.L+18,o.T+o.H-17)}
  var r2=ctx('pcL'),y=r2[1],j=+wsel.value,ld=D.load.slice().sort(function(a,b){return Math.abs(b[1+j])-Math.abs(a[1+j])}),cx=300;y.fillStyle=INK;y.font='bold 14px "Noto Sans KR",sans-serif';y.fillText('PC'+(j+1)+' 가중치 (W의 '+(j+1)+'열, 길이 1)',20,18);
  ld.forEach(function(l,i){var v=l[1+j],yy=32+i*21;y.fillStyle=INK;y.font='12.5px sans-serif';y.fillText(l[0],20,yy+13);y.fillStyle=v>=0?'#c4561a':'#22398f';y.fillRect(v>=0?cx:cx+v*400,yy+2,Math.abs(v)*400,15);y.fillStyle=MUTE;y.fillText(v.toFixed(2),v>=0?cx+v*400+4:cx+v*400-36,yy+14)});
  y.strokeStyle='#9aa0aa';y.beginPath();y.moveTo(cx,28);y.lineTo(cx,32+19*21);y.stroke()}
 c.onmousemove=function(e){var b=c.getBoundingClientRect(),mx=(e.clientX-b.left)*c.width/b.width,my=(e.clientY-b.top)*c.height/b.height,best=-1,bd=100;pts.forEach(function(p){var d=(p[0]-mx)*(p[0]-mx)+(p[1]-my)*(p[1]-my);if(d<bd){bd=d;best=p[2]}});if(best!==hov){hov=best;dr()}};
 by.onchange=dr;wsel.onchange=dr;dr()}

// ---- 8. EM ----
function initEM(){var k=$('emK'),X=D.tr.map(function(r,i){return [D.pc[i][0],Math.log(r[10])]}),n=X.length,samp=[],G=null;
 var m=[0,0];X.forEach(function(p){m[0]+=p[0]/n;m[1]+=p[1]/n});var s=[0,0];X.forEach(function(p){s[0]+=Math.pow(p[0]-m[0],2)/n;s[1]+=Math.pow(p[1]-m[1],2)/n});X=X.map(function(p){return [(p[0]-m[0])/Math.sqrt(s[0]),(p[1]-m[1])/Math.sqrt(s[1])]});
 function pdf(p,mu,S){var a=S[0],b=S[1],d=S[3],det=a*d-b*b,dx=p[0]-mu[0],dy=p[1]-mu[1],q=(d*dx*dx-2*b*dx*dy+a*dy*dy)/det;return Math.exp(-q/2)/(2*Math.PI*Math.sqrt(det))}
 function fitK(K){var R=rng(5),mu=[X[Math.floor(R()*n)].slice()];
  while(mu.length<K){var d=X.map(function(p){return Math.min.apply(0,mu.map(function(c){return Math.pow(p[0]-c[0],2)+Math.pow(p[1]-c[1],2)}))}),t=d.reduce(function(a,b){return a+b})*R(),acc=0;for(var i=0;i<n;i++){acc+=d[i];if(acc>=t){mu.push(X[i].slice());break}}}
  var S=mu.map(function(){return [.3,0,0,.3]}),pi=mu.map(function(){return 1/K}),ll=0;
  for(var it=0;it<150;it++){var Rs=X.map(function(p){var r=mu.map(function(c,j){return pi[j]*pdf(p,c,S[j])}),z=r.reduce(function(a,b){return a+b})||1e-300;return r.map(function(v){return v/z})});
   ll=X.reduce(function(a,p){return a+Math.log(mu.reduce(function(s2,c,j){return s2+pi[j]*pdf(p,c,S[j])},0)||1e-300)},0);
   for(var j=0;j<K;j++){var Nj=1e-9,mx=0,my=0;for(var i=0;i<n;i++){Nj+=Rs[i][j];mx+=Rs[i][j]*X[i][0];my+=Rs[i][j]*X[i][1]}mx/=Nj;my/=Nj;var a=0,b=0,d=0;
    for(var i=0;i<n;i++){var dx=X[i][0]-mx,dy=X[i][1]-my;a+=Rs[i][j]*dx*dx;b+=Rs[i][j]*dx*dy;d+=Rs[i][j]*dy*dy}mu[j]=[mx,my];S[j]=[a/Nj+1e-3,b/Nj,b/Nj,d/Nj+1e-3];pi[j]=Nj/n}}
  return {mu:mu,S:S,pi:pi,ll:ll,bic:-2*ll+(K*6-1)*Math.log(n)}}
 function sample(g,N){var out=[],R=rng(11);for(var i=0;i<N;i++){var t=R(),j=0,acc=0;for(;j<g.pi.length;j++){acc+=g.pi[j];if(t<=acc)break}j=Math.min(j,g.pi.length-1);
  var S=g.S[j],l11=Math.sqrt(S[0]),l21=S[1]/l11,l22=Math.sqrt(Math.max(S[3]-l21*l21,1e-9)),e1=gauss(R),e2=gauss(R);out.push([g.mu[j][0]+l11*e1,g.mu[j][1]+l21*e1+l22*e2])}return out}
 function dr(){var r=ctx('emCv'),x=r[1],o={L:60,T:20,W:610,H:370,x0:-3,x1:3,y0:-3,y1:3,xl:'PC1 점수 (표준화) →',yl:'log Voc (표준화)'},f=frame(x,o);
  X.forEach(function(p){dot(x,f[0](p[0]),f[1](p[1]),3,'#5b63a8',.45)});
  if(G){G.mu.forEach(function(c,j){var S=G.S[j],a=S[0],b=S[1],d=S[3],tr=(a+d)/2,dd=Math.sqrt(Math.max(tr*tr-(a*d-b*b),0)),l1=tr+dd,l2=tr-dd,ang=Math.atan2(l1-a,b||1e-9),p=[];
    for(var t=0;t<=60;t++){var u=t/60*6.2832,ex=2*Math.sqrt(l1)*Math.cos(u),ey=2*Math.sqrt(Math.max(l2,1e-9))*Math.sin(u);p.push([f[0](c[0]+ex*Math.cos(ang)-ey*Math.sin(ang)),f[1](c[1]+ex*Math.sin(ang)+ey*Math.cos(ang))])}line(x,p,COL[(j+1)%6],2.5)})}
  samp.forEach(function(p){dot(x,f[0](p[0]),f[1](p[1]),3.4,'#8a5fbf',.85)})}
 function run(){var K=+k.value;$('emV').textContent=K;G=fitK(K);samp=[];$('emLL').textContent=G.ll.toFixed(0);$('emB').textContent=G.bic.toFixed(0);dr()}
 k.oninput=run;$('emS').onclick=function(){samp=sample(G,200);dr()};run()}

// ---- 8. 적용 범위 ----
function initDom(){var mode=0,bs=document.querySelectorAll('[data-dm]');
 function dr(){var r=ctx('dmCv'),x=r[1],o={L:70,T:30,W:610,H:330,x0:40,x1:600,y0:3,y1:200,xlog:1,ylog:1,xl:'평량 W (g/m², 로그) →',yl:'거칠기 SRA_F (μm, 로그)'},f=frame(x,o),ymax=Math.max.apply(0,D.tr.map(function(t){return t[10]}));
  D.tr.forEach(function(t){dot(x,f[0](t[2]),f[1](t[4]),3,'#b9b3a6',.8)});
  D.gen.forEach(function(g){var col=mode?(g[4]>ymax?'#c4561a':'rgba(34,57,143,'+(0.25+0.7*Math.min(1,g[4]/ymax))+')'):(g[7]?'#22398f':'#c4561a');dot(x,f[0](Math.max(40,Math.min(600,g[0]))),f[1](Math.max(3,Math.min(200,g[2]))),mode?3.6:3.4,col,mode?1:.8)});
  legend(x,mode?[['진할수록 예측 Voc 큼','#22398f'],['학습 Y 범위 밖 (>'+ymax.toFixed(0)+' V)','#c4561a'],['학습 원단','#b9b3a6']]:[['적용 범위 안','#22398f'],['밖 (외삽)','#c4561a'],['학습 원단','#b9b3a6']],o.L,14);
  var nin=D.gen.filter(function(g){return g[7]}).length;x.fillStyle=INK;x.font='13px "Noto Sans KR",sans-serif';x.fillText('표본 400개 중 적용 범위 안 '+nin+'개',o.L+o.W-210,o.T+o.H-10)}
 bs.forEach(function(b){b.onclick=function(){mode=+b.dataset.dm;bs.forEach(function(q){q.classList.toggle('on',q===b)});dr()}});dr()}

// ---- 8. 모델 붕괴 ----
function initCol(){var g=$('clG'),nn=$('clN'),lv=D.tr.map(function(r){return Math.log(r[10])}),m0=lv.reduce(function(a,b){return a+b})/lv.length,s0=Math.sqrt(lv.reduce(function(a,b){return a+(b-m0)*(b-m0)},0)/(lv.length-1));
 function chains(N){var out=[];for(var c=0;c<20;c++){var R=rng(100+c),m=m0,s=s0,h=[[m,s]];for(var t=1;t<=200;t++){var a=[],sm=0;for(var i=0;i<N;i++){var v=m+s*gauss(R);a.push(v);sm+=v}m=sm/N;var q=0;a.forEach(function(v){q+=(v-m)*(v-m)});s=Math.sqrt(q/(N-1));h.push([m,s])}out.push(h)}return out}
 var cache={};function dr(){var G=+g.value,N=+nn.value;$('clGV').textContent=G;$('clNV').textContent=N;var C=cache[N]||(cache[N]=chains(N)),r=ctx('clCv'),x=r[1];
  var A={L:70,T:28,W:280,H:330,x0:0,x1:200,y0:0,y1:s0*1.6,xl:'세대 →',yl:'퍼짐 (log Voc 표준편차)'},fa=frame(x,A);
  C.forEach(function(h){line(x,h.map(function(p,t){return [fa[0](t),fa[1](Math.min(A.y1,p[1]))]}),'rgba(34,57,143,.22)',1.2)});var mean=[];for(var t=0;t<=200;t++){var a=0;C.forEach(function(h){a+=h[t][1]/C.length});mean.push([fa[0](t),fa[1](Math.min(A.y1,a))])}line(x,mean,'#22398f',3.5);line(x,[[fa[0](G),A.T],[fa[0](G),A.T+A.H]],'#c4561a',2,[4,4]);
  var ymx=1.05;C.slice(0,6).forEach(function(h){ymx=Math.max(ymx,s0/Math.max(h[G][1],0.02)*1.05)});ymx=Math.min(ymx,8);var Bo={L:420,T:28,W:280,H:330,x0:1,x1:250,y0:0,y1:ymx,xlog:1,xl:'Voc (V, 로그) →'},fb=frame(x,Bo);
  function curve(m,s,col,w){var p=[];for(var i=0;i<=200;i++){var v=Math.exp(Math.log(1)+i/200*Math.log(250)),z=(Math.log(v)-m)/s;p.push([fb[0](v),fb[1](Math.min(ymx,Math.exp(-z*z/2)*s0/s))])}line(x,p,col,w)}
  curve(m0,s0,'#9aa0aa',3);C.slice(0,6).forEach(function(h){curve(h[G][0],Math.max(h[G][1],0.02),'rgba(196,86,26,.75)',1.8)});
  legend(x,[['실측 분포','#9aa0aa'],[G+'세대 뒤','#c4561a']],Bo.L,14);var av=C.reduce(function(a,h){return a+h[G][1]},0)/C.length;x.font='bold 13px "Noto Sans KR",sans-serif';var tt='평균 퍼짐 '+(av/s0*100).toFixed(0)+'% 남음';x.fillStyle='rgba(255,255,255,.9)';x.fillRect(A.L+6,A.T+2,x.measureText(tt).width+10,20);x.fillStyle='#c4561a';x.fillText(tt,A.L+11,A.T+17)}
 g.oninput=dr;nn.oninput=dr;dr()}

// ---- 9. 역방향 ----
function initInv(){var o=$('ivOut');function show(t){document.querySelectorAll('[data-iv]').forEach(function(b){b.classList.toggle('on',+b.dataset.iv===t)});var rows=D.inv[t],m=Math.max.apply(0,rows.map(function(r){return r[2]}));
 o.innerHTML='<div class="bars">'+rows.map(function(r){return '<div class="bar"><span>'+r[0]+' · '+r[1]+'</span><i style="width:'+(r[2]/m*100)+'%"></i><b>'+r[2]+' / 200</b></div>'}).join('')+'</div>'}
 document.querySelectorAll('[data-iv]').forEach(function(b){b.onclick=function(){show(+b.dataset.iv)}});show(90)}
