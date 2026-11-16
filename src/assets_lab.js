(function(){
"use strict";
var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function $(s,r){return (r||document).querySelector(s)}
function $$(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))}
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function fit(c,h){var d=window.devicePixelRatio||1,w=c.clientWidth||c.parentElement.clientWidth||600;
  if(c.width!==Math.round(w*d)||c.height!==Math.round(h*d)){c.width=Math.round(w*d);c.height=Math.round(h*d);c.style.height=h+'px';}
  var x=c.getContext('2d');x.setTransform(d,0,0,d,0,0);return w;}
function f2(v){return (Math.round(v*100)/100).toFixed(2)}
var LAB=window.LAB||{};var DATA=LAB.data;var RD=[];var HOOK={revSum:function(){}};
var NS='http://www.w3.org/2000/svg';function sv(t,a,txt){var e=document.createElementNS(NS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;return e;}
function rBar(lbl,v,c,note){var p=Math.max(-1,Math.min(1,v)),L=50,w=Math.abs(p)*50,left=p>=0?L:L-w;
  return '<span>'+lbl+'</span><div class="track"><div class="fill" style="left:'+left+'%;width:'+w+'%;background:'+c+'"></div><div class="zero" style="left:50%"></div></div><b class="num">'+(v<-1?'−1 아래':(v<0?'−':'')+Math.abs(v).toFixed(2))+(note||'')+'</b>';}
var ST=(function(){var K='tex_brief01_state',m={rv:{},q:{}};try{var s=localStorage.getItem(K);if(s)m=JSON.parse(s);}catch(e){}
  /* 1번 질문 문구가 바뀌어(M-Robo 삭제) 예전 표시를 한 번만 지움 */
  if(m&&m.q&&!m.mig_q1){delete m.q['0'];m.mig_q1=1;try{localStorage.setItem(K,JSON.stringify(m))}catch(e){}}
  return {get:function(){return m},save:function(){try{localStorage.setItem(K,JSON.stringify(m))}catch(e){}}};})();
var DL=null;try{if(window.claude&&typeof window.claude.use==='function')window.claude.use('downloads').then(function(d){DL=d}).catch(function(){});}catch(e){}
function dlNote(t){$$('#dlNote,.dlnote').forEach(function(n){n.textContent=t})}
function download(blob,name){var fn=/\.(json|txt|csv|zip|md)$/i.test(name)?name:name+'.txt';
  if(DL){DL.save({filename:fn,data:blob}).then(function(){dlNote(fn+' 내려받기를 넘겼습니다.')},function(e){dlNote(e&&e.code==='declined'?'내려받기를 취소했습니다.':'이 화면에서는 내려받기를 쓸 수 없습니다. 페이지 파일을 직접 열면 됩니다.')});return;}
  try{var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=fn;document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove();},500);dlNote(fn+' 내려받기를 시작했습니다.');}catch(e){dlNote('내려받기를 시작하지 못했습니다.');}}
function dlText(t,name,type){download(new Blob([t],{type:type||'text/plain;charset=utf-8'}),name)}
var COL={text:'#16212b',muted:'#5b6874',rule:'#d5dbe2',gfp:'#13733a',eye:'#c9302c',amber:'#a35c00',info:'#1e55c8',stain:'#9b3fb5',accent:'#8f5a2e'};
var TYPE={Nonwoven:['부직포','#9b3fb5'],Woven:['제직물','#1e55c8'],Knit:['편직물','#13733a']};
var SRC={Industrial:['산업 원단','#1e55c8'],Huvis:['Huvis','#a35c00'],Lab:['연구실','#c9302c']};

/* ---------- 캐릭터 ---------- */
var Cast={src:function(who,mood){return SPRITE[who+'_'+mood]||SPRITE[who+'_smile']||''},
  fill:function(){$$('img[data-who]').forEach(function(i){var s=Cast.src(i.dataset.who,i.dataset.mood||'smile');if(s)i.src=s;})}};
Cast.fill();

/* ---------- 용어 말풍선 ---------- */
var GL={
 '태':['태 (Hand)','섬유','천을 손으로 만졌을 때의 느낌. 부드러움·뻣뻣함·매끄러움·따뜻함 등을 통틀어 이릅니다.'],
 '마찰전기':['마찰전기','물리','두 물질이 닿았다 떨어질 때 전하가 한쪽으로 옮겨 가며 생기는 전기. 풍선을 머리에 문지를 때의 정전기와 같습니다.'],
 'TENG':['TENG (마찰전기 나노발전기)','소자','마찰전기를 모아 전기 신호로 쓰는 소자. 누르거나 문지르면 신호가 나와 배터리 없이 움직임을 감지합니다.'],
 'Sim-to-Real':['Sim-to-Real','방법','컴퓨터 시뮬레이션으로 만든 가상 데이터로 먼저 배우고, 적은 실측 데이터로 보정하는 방법입니다.'],
 '주성분 분석':['주성분 분석 (PCA)','방법','서로 겹치는 정보를 묶어 많은 변수를 몇 개의 대표 축으로 줄이는 방법입니다.'],
 '실험계획법':['실험계획법 (DOE)','방법','원인 후보의 수준을 미리 정해 고르게 조합해 실험하는 방법. 무엇이 원인인지 가리기 쉽습니다.'],
 '기준선':['기준선 (baseline)','평가','평균값으로 찍기나 선형 회귀처럼 단순한 모델의 성능. 복잡한 모델은 이것을 이겨야 의미가 있습니다.'],
 '교차검증':['교차검증','평가','데이터를 몇 묶음으로 나눠, 돌아가며 한 묶음은 시험에 쓰고 나머지로 배우는 검증 방법입니다.'],
 '과적합':['과적합','평가','모델이 학습 데이터를 외워, 학습 점수는 높지만 새 데이터에서는 틀리는 상태입니다.'],
 '데이터 누수':['데이터 누수','평가','시험에 쓸 정보가 학습에 섞여 들어가 점수가 부풀려지는 일. 같은 원단의 반복 측정을 나눠 넣을 때 생깁니다.'],
 'KES-FB':['KES-FB (가와바타 평가 시스템)','장비','인장·전단·굽힘·압축·표면 시험으로 직물의 태를 숫자로 재는 장비 체계입니다.'],
 'FTT':['FTT (Fabric Touch Tester)','장비','한 번의 측정으로 굽힘·압축·표면·열을 재는 촉감 측정기. 엑셀 열 이름으로 추정했습니다.']
};
var tip=$('#tip'),tipFor=null;
function showTip(el){var g=GL[el.dataset.k];if(!g)return;tip.innerHTML='<span class="k">'+esc(g[1])+'</span><b>'+esc(g[0])+'</b>'+esc(g[2]);
  tip.style.display='block';var r=el.getBoundingClientRect(),tw=Math.min(320,window.innerWidth-24);tip.style.maxWidth=tw+'px';
  var x=Math.max(12,Math.min(r.left,window.innerWidth-tw-12)),y=r.bottom+8;if(y+tip.offsetHeight>window.innerHeight-8)y=r.top-tip.offsetHeight-8;
  tip.style.left=x+'px';tip.style.top=y+'px';tipFor=el;}
function hideTip(){tip.style.display='none';tipFor=null;}
$$('.jt').forEach(function(el){el.tabIndex=0;el.setAttribute('role','button');el.setAttribute('aria-label',el.textContent+' 뜻 보기');
  el.addEventListener('mouseenter',function(){showTip(el)});el.addEventListener('mouseleave',hideTip);
  el.addEventListener('focus',function(){showTip(el)});el.addEventListener('blur',hideTip);
  el.addEventListener('click',function(e){e.stopPropagation();tipFor===el?hideTip():showTip(el)});});
document.addEventListener('click',hideTip);document.addEventListener('keydown',function(e){if(e.key==='Escape')hideTip()});
window.addEventListener('scroll',function(){if(tipFor)hideTip();var h=document.documentElement;
  $('#prog').style.width=(100*h.scrollTop/Math.max(1,h.scrollHeight-h.clientHeight))+'%';},{passive:true});

/* ---------- 박자 (보이는 것만) ---------- */
var mods=[],vis=new Set(),io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?vis.add(e.target):vis.delete(e.target)})},{rootMargin:'100px'}):null;
function addMod(el,fn){mods.push({el:el,fn:fn});if(io)io.observe(el);else vis.add(el);}
var last=0;function loop(ts){var dt=last?Math.min(0.05,(ts-last)/1000):0.016;last=ts;mods.forEach(function(m){if(vis.has(m.el))m.fn(dt)});requestAnimationFrame(loop);}

/* ---------- 표지: 평직 픽셀 격자 ---------- */
if($('#coverCv')){
var cov=$('#coverCv');
function drawCover(t){var w=cov.clientWidth,h=cov.clientHeight;if(!w)return;var d=window.devicePixelRatio||1;
  if(cov.width!==Math.round(w*d)){cov.width=Math.round(w*d);cov.height=Math.round(h*d);}
  var x=cov.getContext('2d');x.setTransform(d,0,0,d,0,0);x.imageSmoothingEnabled=false;x.fillStyle='#fbfaf7';x.fillRect(0,0,w,h);
  var s=Math.max(10,Math.round(w/64)),warp=['#d9c7b0','#cdb699'],weft=['#b9cbe6','#a8bde0'];
  var shift=reduce?0:Math.floor((t||0)*2)%2;
  for(var j=0;j*s<h;j++)for(var i=0;i*s<w;i++){var up=((i+j+shift)%2===0);x.fillStyle=up?warp[i%2]:weft[j%2];x.globalAlpha=.55;x.fillRect(i*s,j*s,s-1,s-1);}
  x.globalAlpha=1;var g=x.createLinearGradient(0,0,w*0.7,0);g.addColorStop(0,'rgba(251,250,247,.95)');g.addColorStop(1,'rgba(251,250,247,0)');x.fillStyle=g;x.fillRect(0,0,w,h);}
var covT=0;drawCover(0);addMod(cov,function(dt){covT+=dt*0.25;if(!reduce&&Math.floor(covT*2)!==Math.floor((covT-dt*0.25)*2))drawCover(covT)});

RD.push(function(){drawCover(covT)});
}
/* ---------- 흐름도 ---------- */
if($('#flowSvg')){
var FN=[
 {id:'n1',x:20,y:52,t:'① 원단 설계·제작',s:'실험계획법으로 조합',k:'lab',d:{할일:'실 종류·조직·밀도의 수준을 정해 원단 50~100개를 계획해서 만든다.',산출물:'원단 목록, 제작 기록지',담당:'연구실',관련:'S2 샘플 확충·정답 측정'},st:'s2'},
 {id:'n2',x:220,y:52,t:'② 측정',s:'물성·마찰·마찰전기',k:'lab',d:{할일:'8묶음을 같은 장비·같은 조건으로 측정한다. 반복 3회, 원자료 보관.',산출물:'반복 측정 표, 원자료 폴더',담당:'연구실',관련:'S2 샘플 확충·정답 측정'},st:'s2'},
 {id:'n3',x:420,y:52,t:'③ 데이터 정리',s:'마스터 표 작성',k:'ai',d:{할일:'단위 통일, 원단 ID 대조, 반복 측정 평균·흔들림 계산.',산출물:'마스터 표, 데이터 사전',담당:'AI',관련:'S0 착수·자료 정리'},st:'s0'},
 {id:'d1',cx:700,cy:80,t:'품질검사',s:'통과?',k:'gate',d:{할일:'반복 측정 변동계수 15% 이하, 표준 상태(20 ± 2 °C, 65 ± 4 %) 기록 확인.',통과하면:'④ 탐색 분석으로',못하면:'② 측정으로 돌아가 재측정',관련:'S2 · 재측정 기준'},st:'s2'},
 {id:'n4',x:620,y:202,t:'④ 탐색 분석',s:'상관·PCA·군집',k:'ai',d:{할일:'물성끼리 겹치는 정보를 찾고 원단의 닮음을 지도로 본다.',산출물:'탐색 분석 보고서',담당:'AI',관련:'S1 파일럿 탐색 분석'},st:'s1'},
 {id:'n5',x:420,y:202,t:'⑤ 핵심 변수 선정',s:'10개 안팎으로',k:'ai',d:{할일:'서로 겹치지 않는 핵심 물성을 고른다. 변수당 원단 5~10개 규칙에 맞춘다.',산출물:'핵심 변수 목록',담당:'AI + 연구책임자 검토',관련:'S1 → S3'},st:'s1'},
 {id:'n6',x:220,y:202,t:'⑥ 모델링',s:'M1·M2·M3 단계별',k:'ai',d:{할일:'기준선 → 랜덤포레스트·XGBoost → 신경망. 기준선을 이길 때만 채택.',산출물:'모델과 교차검증 보고서',담당:'AI',관련:'S3 기초 예측 모델'},st:'s3'},
 {id:'sim',x:20,y:202,t:'Sim-to-Real',s:'합성 데이터',k:'lab2',d:{할일:'TexGen으로 직물 단위 구조를 만들고 Abaqus로 변형을 계산해 가상 데이터를 만든다.',산출물:'합성 데이터 세트',담당:'연구실·시뮬레이션 담당',관련:'S4 Sim-to-Real (예정)'},st:'s4'},
 {id:'d2',cx:300,cy:380,t:'평가 기준',s:'충족?',k:'gate',d:{할일:'원단 단위 교차검증 R², 기준선 대비 개선, 그룹 제외 검증을 확인.',통과하면:'⑦ 해석·외부 검증으로',못하면:'① 원단 추가·변수 재선정',관련:'S3 · 평가 기준'},st:'s3'},
 {id:'n7',x:420,y:352,t:'⑦ 해석·외부 검증',s:'SHAP·새 원단 실측',k:'ai',d:{할일:'변수 영향도를 해석하고, 새 원단 10개 이상의 예측을 먼저 적어 둔 뒤 측정해 맞춰 본다.',산출물:'해석 보고서, 외부 검증 결과',담당:'AI + 연구실',관련:'S3 → S5 (예정)'},st:'s3'},
 {id:'n8',x:620,y:352,t:'⑧ 설계 제안',s:'최적 구조·논문·특허',k:'ai',d:{할일:'원하는 성능을 내는 구조 후보를 제안한다.',산출물:'설계 가이드, 논문·특허 초안',담당:'공동',관련:'S5 이후 (예정)'},st:'s5'}
];
var FLINK={s0:'stage_0_kickoff.html',s1:'stage_1_explore.html',s2:'stage_2_data.html',s3:'stage_3_model.html',s4:'stage_4_sim2real.html',s5:'stage_5_tribo.html',s6:'stage_6_device.html'};
var FORD=['n1','n2','n3','d1','n4','n5','sim','n6','d2','n7','n8'];
var svg=$('#flowSvg');
var KC={lab:['#fcebea','#c9302c'],lab2:['#fcebea','#c9302c'],ai:['#e6eefb','#1e55c8'],gate:['#fff','#5b6874']};
function buildFlow(){svg.innerHTML='';var defs=sv('defs',{});var m=sv('marker',{id:'fa',viewBox:'0 0 10 10',refX:9,refY:5,markerWidth:7,markerHeight:7,orient:'auto-start-reverse'});
  m.appendChild(sv('path',{d:'M0 0L10 5L0 10z',fill:'#5b6874'}));defs.appendChild(m);svg.appendChild(defs);
  var P=[['M180 80H220'],['M380 80H420'],['M580 80H630'],['M700 40V18H300V52','아니오 · 재측정',500,12],['M700 120V202','예',712,165],
    ['M620 230H580'],['M420 230H380'],['M180 230H220',null,0,0,1],['M300 258V340'],['M370 380H420','예',395,370],['M580 380H620'],
    ['M230 380H8V80H20','아니오: 원단 추가·변수 재선정',120,402]];
  P.forEach(function(p){svg.appendChild(sv('path',{d:p[0],fill:'none',stroke:'#8a96a3','stroke-width':1.6,'marker-end':'url(#fa)','stroke-dasharray':p[4]?'5 4':''}));
    if(p[1])svg.appendChild(sv('text',{x:p[2],y:p[3],'font-size':13,fill:'#5b6874','text-anchor':'middle'},p[1]));});
  FN.forEach(function(n){var g=sv('g',{class:'fnode',tabindex:0,role:'button','aria-label':n.t+' — '+n.s,'data-id':n.id}),c=KC[n.k];
    if(n.k==='gate'){g.appendChild(sv('polygon',{points:(n.cx-70)+','+n.cy+' '+n.cx+','+(n.cy-40)+' '+(n.cx+70)+','+n.cy+' '+n.cx+','+(n.cy+40),fill:c[0],stroke:c[1],'stroke-width':1.6}));
      g.appendChild(sv('text',{x:n.cx,y:n.cy-3,'text-anchor':'middle','font-size':14,'font-weight':700,fill:'#16212b'},n.t));
      g.appendChild(sv('text',{x:n.cx,y:n.cy+15,'text-anchor':'middle','font-size':13,fill:'#16212b'},n.s));}
    else{g.appendChild(sv('rect',{x:n.x,y:n.y,width:160,height:56,rx:9,fill:c[0],stroke:c[1],'stroke-width':1.6,'stroke-dasharray':n.k==='lab2'?'5 4':''}));
      g.appendChild(sv('text',{x:n.x+80,y:n.y+24,'text-anchor':'middle','font-size':14.5,'font-weight':700,fill:'#16212b'},n.t));
      g.appendChild(sv('text',{x:n.x+80,y:n.y+43,'text-anchor':'middle','font-size':12.5,fill:'#5b6874'},n.s));}
    g.addEventListener('click',function(){flowSel(n.id,true)});g.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();flowSel(n.id,true)}});
    svg.appendChild(g);});
  [['#fcebea','#c9302c','연구실 (제작·측정)',560],['#e6eefb','#1e55c8','AI (분석·모델)',700]].forEach(function(l){
    svg.appendChild(sv('rect',{x:l[3],y:446,width:14,height:12,rx:3,fill:l[0],stroke:l[1]}));svg.appendChild(sv('text',{x:l[3]+20,y:457,'font-size':12.5,fill:'#5b6874'},l[2]));});}
var flowCur=null,flowTimer=null;
function flowSel(id,stop){if(stop)flowStop();flowCur=id;var n=FN.filter(function(f){return f.id===id})[0];
  $$('.fnode',svg).forEach(function(g){var on=g.dataset.id===id,sh=g.querySelector('rect,polygon');sh.setAttribute('stroke-width',on?3.4:1.6);g.style.opacity=on||!id?1:.55;});
  var dl='';for(var k in n.d)dl+='<dt>'+esc(k)+'</dt><dd>'+esc(n.d[k])+'</dd>';
  $('#flowDetail').innerHTML='<h4>'+esc(n.t)+' <span class="small muted">'+esc(n.s)+'</span></h4><dl>'+dl+'</dl>'+(n.st?'<p style="margin:8px 0 0"><a href="'+FLINK[n.st]+'">이 단계의 스테이지 쪽 보기 →</a></p>':'');
  $('#flowStep').textContent=(FORD.indexOf(id)+1)+' / '+FORD.length;}
function flowStop(){if(flowTimer){clearInterval(flowTimer);flowTimer=null;}var b=$('#flowPlay');b.textContent='▶ 흐름 따라가기';b.setAttribute('aria-pressed','false');}
$('#flowPlay').addEventListener('click',function(){if(flowTimer){flowStop();return;}var i=Math.max(0,FORD.indexOf(flowCur)+1)%FORD.length;
  this.textContent='❚❚ 멈추기';this.setAttribute('aria-pressed','true');flowSel(FORD[i]);if(reduce){flowStop();return;}
  flowTimer=setInterval(function(){i++;if(i>=FORD.length){flowStop();return;}flowSel(FORD[i]);},1600);});
$('#flowReset').addEventListener('click',function(){flowStop();flowSel('n1')});
buildFlow();flowSel('n1');

}
/* ---------- ① 채움 지도 ---------- */
if($('#heat')){
var GH=[['기본 물성',5],['표면 · FTT',12],['역학 · FTT',16],['열 · FTT',8],['표면 · KES',6],['역학 · KES',21],['인장강도',2],['통기·보온',3],['정답 Y',0]];
var heat=$('#heat');heat.style.gridTemplateColumns='minmax(150px,1.3fr) repeat(9,minmax(52px,1fr))';
function buildHeat(src){var h='<div class="h" role="columnheader">원단</div>';GH.forEach(function(g){h+='<div class="h" role="columnheader">'+g[0]+'<br>('+g[1]+')</div>'});
  DATA.samples.forEach(function(s){var dim=(src!=='all'&&s.src!==src)?' dim':'';
    h+='<div class="rid'+dim+'" role="rowheader"><span class="dot" style="background:'+SRC[s.src][1]+'"></span>'+esc(s.id)+' <span class="muted">'+TYPE[s.type][0]+'</span></div>';
    s.cov.forEach(function(v,i){var f=v/GH[i][1],bg='rgba(19,115,58,'+(0.08+0.8*f).toFixed(2)+')';
      h+='<div class="c'+dim+'" role="cell" style="background:'+(v?bg:'#f1f3f5')+';color:'+(f>.6?'#fff':'#16212b')+'" title="'+esc(s.id)+' · '+GH[i][0]+' '+v+'/'+GH[i][1]+'">'+(v?v:'–')+'</div>';});
    h+='<div class="c'+dim+'" role="cell" style="background:#fcebea;color:#c9302c">없음</div>';});
  heat.innerHTML=h;
  var sel=DATA.samples.filter(function(s){return src==='all'||s.src===src}),tot=0;sel.forEach(function(s){tot+=s.cov.reduce(function(a,b){return a+b},0)});
  $('#covK').innerHTML='<div class="kpi g"><b>'+sel.length+'</b><span>원단 수</span></div><div class="kpi a"><b>'+Math.round(100*tot/(73*sel.length))+'%</b><span>평균 채움률</span></div>'+
   '<div class="kpi m"><b>'+DATA.commonBySrc[src]+'</b><span>이 묶음 모두에 있는 항목</span></div><div class="kpi r"><b>0</b><span>정답 Y</span></div>';
  var I={all:['a','27개 전체로 함께 분석할 수 있는 항목은 19개뿐입니다. 정답 Y 열은 모두 비어 있습니다.'],
   Industrial:['g','산업 원단 14개는 FTT 계열과 KES-FB 계열이 함께 있어 가장 꽉 차 있습니다. 14개 모두에 있는 항목 59개.'],
   Huvis:['a','Huvis 11개는 대부분 부직포이고 KES-FB 값이 없습니다. 11개 모두에 있는 항목 39개.'],
   Lab:['r','연구실 원단 2개는 기본 물성은 모두 있지만 KES-FB·인장강도·통기 항목이 없습니다. 둘 모두에 있는 항목 31개.']}[src];
  $('#covI').innerHTML='<p class="'+I[0]+'">'+I[1]+'</p>';}
$$('[data-src]').forEach(function(b){b.addEventListener('click',function(){$$('[data-src]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});buildHeat(b.dataset.src)})});
buildHeat('all');

}
/* ---------- ② PCA ---------- */
if($('#pcaCv')){
var pca=$('#pcaCv'),pcaMode='type',pcaSel=null,pcaPts=[];
function drawPca(){var W=fit(pca,380),H=380,x=pca.getContext('2d');x.clearRect(0,0,W,H);
  var P=DATA.samples.map(function(s){return s.pc}),xs=P.map(function(p){return p[0]}),ys=P.map(function(p){return p[1]});
  var x0=Math.min.apply(0,xs)-1,x1=Math.max.apply(0,xs)+1,y0=Math.min.apply(0,ys)-1,y1=Math.max.apply(0,ys)+1;
  var L=46,R=16,T=16,B=40,sx=function(v){return L+(v-x0)/(x1-x0)*(W-L-R)},sy=function(v){return H-B-(v-y0)/(y1-y0)*(H-T-B)};
  x.strokeStyle='rgba(22,33,43,.05)';for(var g=0;g<W;g+=24){x.beginPath();x.moveTo(g,0);x.lineTo(g,H);x.stroke()}for(var g2=0;g2<H;g2+=24){x.beginPath();x.moveTo(0,g2);x.lineTo(W,g2);x.stroke()}
  x.strokeStyle='#aab4bf';x.setLineDash([4,4]);x.beginPath();x.moveTo(sx(0),T);x.lineTo(sx(0),H-B);x.moveTo(L,sy(0));x.lineTo(W-R,sy(0));x.stroke();x.setLineDash([]);
  x.fillStyle=COL.muted;x.font='12.5px "IBM Plex Sans KR",sans-serif';x.textAlign='center';x.fillText('PC1 (39%) — 열 전달·압축 일·거칠기',(L+W-R)/2,H-12);
  x.save();x.translate(14,(T+H-B)/2);x.rotate(-Math.PI/2);x.fillText('PC2 (29%) — 굽힘 일·압축 회복',0,0);x.restore();
  pcaPts=[];DATA.samples.forEach(function(s){var px=sx(s.pc[0]),py=sy(s.pc[1]),c=(pcaMode==='type'?TYPE[s.type]:SRC[s.src])[1];pcaPts.push([px,py,s]);
    x.beginPath();x.arc(px,py,pcaSel===s.id?9:6.5,0,7);x.fillStyle=c;x.globalAlpha=.85;x.fill();x.globalAlpha=1;
    if(pcaSel===s.id){x.lineWidth=2.5;x.strokeStyle=COL.text;x.stroke();x.lineWidth=1;}});
  x.font='11px "IBM Plex Sans KR",sans-serif';x.fillStyle=COL.amber;x.textAlign='right';
  var lab=pcaSel?'':'';x.fillText('실측 · 로그 변환 후 표준화',W-R-2,T+12);
  var m=pcaMode==='type'?TYPE:SRC,h='';for(var k in m)h+='<span style="margin-right:14px"><span class="dot" style="background:'+m[k][1]+'"></span> '+m[k][0]+'</span>';$('#pcaLegend').innerHTML=h;}
pca.addEventListener('pointerdown',function(e){var r=pca.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top,best=null,bd=900;
  pcaPts.forEach(function(p){var d=(p[0]-mx)*(p[0]-mx)+(p[1]-my)*(p[1]-my);if(d<bd){bd=d;best=p[2]}});
  if(best){pcaSel=best.id;drawPca();$('#pcaI').innerHTML='<p class="m"><b>'+esc(best.id)+'</b> · '+esc(best.name)+' · '+TYPE[best.type][0]+' · '+SRC[best.src][0]+(best.st&&best.st!=='nan'?' · 조직 '+esc(best.st):'')+' — PC1 '+f2(best.pc[0])+', PC2 '+f2(best.pc[1])+'</p>';}});
$$('[data-color]').forEach(function(b){b.addEventListener('click',function(){$$('[data-color]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});pcaMode=b.dataset.color;drawPca();
  $('#pcaI').innerHTML=pcaMode==='type'?'<p class="m">같은 종류끼리 모입니다. 산업 편직물은 오른쪽 아래, 산업 제직물은 왼쪽, 부직포는 넓게 흩어집니다.</p>':'<p class="a">출처로 칠해도 거의 같은 무리가 나옵니다. Huvis 원단이 대부분 부직포라, 출처와 종류의 효과를 이 데이터로는 가를 수 없습니다.</p>';})});
var ab='';DATA.cor.forEach(function(c){var sig=c.p<0.05;ab+='<span>'+esc(c.name)+' <span class="muted small">('+c.ftt+' ↔ '+c.kes+')</span></span><div class="track"><div class="fill" style="width:'+Math.max(2,c.rho*100)+'%;background:'+(sig?COL.gfp:'#aab4bf')+'"></div></div><b class="num">ρ '+c.rho.toFixed(2)+' · p '+c.p.toFixed(3)+'</b>'});
$('#agreeBars').innerHTML=ab;

RD.push(drawPca);
}
/* ---------- ③ 8묶음 + 계산기 ---------- */
if($('#bund')){
var BUN=[
 ['1. 식별 정보','part','원단 ID, 출처, 제작일, 로트 번호, 측정 일시, 측정자','기록','1회','ID·출처만 있음'],
 ['2. 실 특성 (B)','no','소재 조성(%), 섬도(데니어·dtex), 필라멘트 수, 꼬임 수(회/m), 단면 형상, 중공율(%), 실 강도·신도','실 규격서, 섬유 단면 SEM 사진, 실 인장 시험','실 종류별 1회 (강도 5회)','대부분 빈칸'],
 ['3. 제작 조건 (C)','part','직물 종류, 조직, 경·위사 밀도(올/cm) 또는 웨일·코스 밀도, 게이지, 제작 장력(cN), 후가공 여부','제작 기록지','1회','조직·게이지·밀도만'],
 ['4. 기본 물성 (A1)','ok','두께(mm), 평량(g/m²)','두께계, 저울','5회','있음 (두께 일부 빈칸)'],
 ['5. 역학·표면·열 (A2)','part','FTT 전 항목 또는 KES-FB 전 항목 중 하나로 통일','FTT 또는 KES-FB','시편 3장 × 앞·뒷면 × 세로·가로','출처별로 다름'],
 ['6. 동적 마찰 (A3)','no','마찰력 시계열 원자료, 정지·운동 마찰계수, 마찰 감소 기간, 하중(N)·속도(mm/s)·샘플링 주파수(Hz)','마찰 시험기','조건별 3회','없음'],
 ['7. 마찰전기 출력 (Y)','no','개방 전압 Voc(V), 단락 전류 Isc(μA), 전하량 Qsc(nC) → 전하밀도(μC/m²), 원시 파형','기존 마찰전기 측정 장치, 오실로스코프·전위계','시편 3장, 안정 구간 평균','없음'],
 ['8. 측정 환경','no','온도(°C), 상대습도(%), 접촉 모드, 상대 물질, 접촉 면적(cm²), 누르는 힘(N), 접촉 주파수(Hz)','온습도계, 장치 설정 기록','측정마다','없음']];
var CH={ok:['ok','있음'],part:['part','일부'],no:['no','없음']};
var bh='';BUN.forEach(function(b,i){bh+='<button aria-pressed="'+(i===6)+'" data-b="'+i+'"><b>'+b[0]+'</b><span class="chip '+CH[b[1]][0]+'">지금: '+CH[b[1]][1]+'</span></button>'});
$('#bund').innerHTML=bh;
function bundSel(i){var b=BUN[i];$$('#bund button').forEach(function(x){x.setAttribute('aria-pressed',x.dataset.b==String(i)?'true':'false')});
  $('#bundD').innerHTML='<b>'+b[0]+'</b><dl class="small" style="display:grid;grid-template-columns:max-content 1fr;gap:4px 14px;margin:6px 0 0"><dt class="muted">필수 항목</dt><dd style="margin:0">'+b[2]+'</dd><dt class="muted">측정 방법·장비</dt><dd style="margin:0">'+b[3]+'</dd><dt class="muted">원단당 횟수 (제안)</dt><dd style="margin:0">'+b[4]+'</dd><dt class="muted">현재 엑셀</dt><dd style="margin:0">'+b[5]+'</dd></dl>';}
$$('#bund button').forEach(function(b){b.addEventListener('click',function(){bundSel(+b.dataset.b)})});bundSel(6);
var DOE={yarn:[4,1,6,'실 종류'],str:[3,1,4,'조직 수'],den:[3,1,4,'밀도 수준'],fam:[2,1,2,'계열 (제직·편직)'],vars:[10,3,20,'핵심 변수 수'],rep:[3,1,5,'반복 측정']};
var dc='';Object.keys(DOE).forEach(function(k){dc+='<div class="stepper"><span class="lb">'+DOE[k][3]+'</span><button aria-label="'+DOE[k][3]+' 줄이기" data-k="'+k+'" data-d="-1">−</button><span class="val" id="dv_'+k+'">'+DOE[k][0]+'</span><button aria-label="'+DOE[k][3]+' 늘리기" data-k="'+k+'" data-d="1">+</button></div>'});
$('#doeCtrl').innerHTML=dc;
function doeCalc(){var v={};for(var k in DOE){v[k]=DOE[k][0];$('#dv_'+k).textContent=v[k];}
  var nw=v.yarn*v.str*v.den*v.fam,tot=nw+27,lo=v.vars*5,hi=v.vars*10,meas=tot*v.rep*4;
  $('#doeK').innerHTML='<div class="kpi i"><b>'+nw+'</b><span>새로 만들 원단</span></div><div class="kpi g"><b>'+tot+'</b><span>기존 27개 포함 합계</span></div><div class="kpi a"><b>'+lo+'~'+hi+'</b><span>필요 원단 (변수 × 5~10)</span></div><div class="kpi m"><b>'+meas.toLocaleString()+'</b><span>측정 횟수 (× 반복 × 4개 시험)</span></div>';
  var mx=Math.max(tot,hi)*1.1;
  $('#doeBars').innerHTML='<span>합계 원단</span><div class="track"><div class="fill" style="width:'+(100*tot/mx)+'%;background:'+(tot>=hi?COL.gfp:tot>=lo?COL.amber:COL.eye)+'"></div><div class="thr" style="left:'+(100*lo/mx)+'%"></div><div class="thr" style="left:'+(100*hi/mx)+'%"></div></div><b class="num">'+tot+'개</b>'+
    '<span class="small muted" style="grid-column:1/-1">점선 = 최소선('+lo+'개)과 넉넉한 선('+hi+'개)</span>';
  var I=tot<lo?['r','원단이 '+(lo-tot)+'개 모자랍니다. 수준을 늘리거나 핵심 변수를 줄여야 합니다.']:tot<hi?['a','최소선은 넘었습니다. 다만 넉넉한 선까지 '+(hi-tot)+'개 남았습니다.']:['g','넉넉한 선을 넘었습니다. 측정 횟수가 '+meas.toLocaleString()+'번이라 일정과 비용을 함께 봐야 합니다.'];
  $('#doeI').innerHTML='<p class="'+I[0]+'">'+I[1]+' 기존 27개도 같은 장비로 다시 측정한다는 가정입니다.</p>';}
$$('#doeCtrl button').forEach(function(b){b.addEventListener('click',function(){var d=DOE[b.dataset.k];d[0]=Math.max(d[1],Math.min(d[2],d[0]+(+b.dataset.d)));doeCalc()})});doeCalc();

}
/* ---------- ④ 과적합 실험실 ---------- */
if($('#ofBars')){
var ofT=null;
function ofRun(){var n=+$('#ofN').value,p=+$('#ofP').value;$('#ofNv').textContent=n;$('#ofPv').textContent=p;
  var r=overfit(n,p,11);
  $('#ofBars').innerHTML=rBar('학습 R²',r.train,COL.stain)+rBar('교차검증 R²',r.cv,r.cv<0?COL.eye:COL.gfp)+rBar('진짜 설명력',0.70,'#aab4bf')+'<span class="small muted" style="grid-column:1/-1">가운데 세로선 = 0. 왼쪽으로 가면 평균값으로 찍는 것보다 못하다는 뜻입니다.</span>';
  var I=r.cv<0?['r','교차검증 R²가 '+f2(r.cv)+'로 0보다 낮습니다. 처음 보는 원단에서는 평균값으로 찍는 것보다도 못합니다. 원단 '+n+'개에 변수 '+p+'개는 외우기 좋은 조건입니다.']:
    (r.train-r.cv>0.2?['a','학습 '+f2(r.train)+'와 교차검증 '+f2(r.cv)+'의 차이가 '+f2(r.train-r.cv)+'입니다. 아직 외우는 몫이 큽니다.']:['g','교차검증 R² '+f2(r.cv)+'로 진짜 값 0.70에 가깝습니다. 원단 수와 변수 수의 균형이 맞습니다.']);
  $('#ofI').innerHTML='<p class="'+I[0]+'">'+I[1]+'</p>';}
function ofLater(){clearTimeout(ofT);ofT=setTimeout(ofRun,60);}
$('#ofN').addEventListener('input',ofLater);$('#ofP').addEventListener('input',ofLater);
$$('[data-of]').forEach(function(b){b.addEventListener('click',function(){var v=b.dataset.of.split(',');$('#ofN').value=v[0];$('#ofP').value=v[1];ofRun()})});ofRun();
var MOD=[['M0 탐색','어떤 변수끼리 정보가 겹치나?','모든 물성','없음 (비지도)','상관 분석 → PCA → 군집','1단계 · 이미 시작 (② 칸)'],
 ['M1 구조 → 물성','이 실·조직이면 어떤 물성이 나오나?','실 특성 B, 제작 조건 C','핵심 물성 A (마찰·거칠기·굽힘·압축 회복)','라쏘·릿지 회귀 → 랜덤포레스트·XGBoost','3단계'],
 ['M2 직물 특성 → 전기 특성','이 직물이면 마찰전기 출력이 얼마인가?','직물 주요 특성 X (B·C·A 수치)','실측 전기 특성 Y (전압·전류·전하밀도)','라쏘·릿지 → 랜덤포레스트·XGBoost → 가우시안 과정(불확실도)','3단계 · 1차년도 핵심 (2026-11-17 방향)'],
 ['M3 생성 직물 예측','실측에 없던 가상 직물의 출력은 얼마인가?','실측 근거로 생성한 X','예측 Y + 불확실도 (정답 없음)','M2 모델 + 앙상블·가우시안 과정, 일부를 실제 제작해 검증','4·5단계 · 1차년도'],
 ['M4 경로 분석','구조의 효과가 물성을 거쳐 얼마나 전달되나?','B·C → A → Y 경로','경로계수 (직접·간접 효과)','PLS-SEM — 일반 구조방정식은 흔히 표본 200개 이상이 필요해, 작은 표본용을 씀','3·5단계']];
var mh='';MOD.forEach(function(m,i){mh+=(i?'<span class="arrow">→</span>':'')+'<button class="bt" aria-pressed="'+(i===1)+'" data-m="'+i+'">'+m[0]+'</button>'});$('#mlad').innerHTML=mh;
function modSel(i){var m=MOD[i];$$('#mlad button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.m==String(i)?'true':'false')});
  $('#mladD').innerHTML='<b>'+m[0]+'</b> — '+m[1]+'<dl class="small" style="display:grid;grid-template-columns:max-content 1fr;gap:4px 14px;margin:6px 0 0"><dt class="muted">입력 X</dt><dd style="margin:0">'+m[2]+'</dd><dt class="muted">출력 Y</dt><dd style="margin:0">'+m[3]+'</dd><dt class="muted">기법 (시도 순서)</dt><dd style="margin:0">'+m[4]+'</dd><dt class="muted">시점</dt><dd style="margin:0">'+m[5]+'</dd></dl>';}
$$('#mlad button').forEach(function(b){b.addEventListener('click',function(){modSel(+b.dataset.m)})});modSel(1);

}
/* ---------- ⑤ 누수 실험 ---------- */
if($('#leakCv')){
var LK=leak(7),leakMode=null,leakShown={},FC=['#1e55c8','#c9302c','#13733a','#a35c00','#9b3fb5'],leakCv=$('#leakCv'),leakT=0;
function drawLeak(){var W=fit(leakCv,200),H=200,x=leakCv.getContext('2d');x.clearRect(0,0,W,H);
  var fo=leakMode?LK.folds(leakMode==='random'?'row':'fab'):null,step=(W-40)/30;
  var hl=Math.floor(leakT)%5;
  LK.rows.forEach(function(r,i){var k=i%3,cx=20+step*(r.fab+.5),cy=60+k*30,c=fo?FC[fo[i]]:'#aab4bf';
    x.beginPath();x.arc(cx,cy,Math.min(8,step*.32),0,7);x.fillStyle=c;x.globalAlpha=fo&&!reduce&&fo[i]!==hl?.35:.9;x.fill();x.globalAlpha=1;});
  x.fillStyle=COL.muted;x.font='12px "IBM Plex Sans KR",sans-serif';x.textAlign='left';
  x.fillText(fo?'지금 시험에 쓰는 묶음: '+(hl+1)+'번째 (진한 점)':'버튼을 누르면 나누는 모양이 보입니다',20,24);
  x.textAlign='right';x.fillStyle=COL.amber;x.fillText('설명용 모형 · 실제 데이터 아님',W-10,H-12);}
addMod(leakCv,function(dt){if(leakMode&&!reduce){var o=Math.floor(leakT);leakT+=dt*0.7;if(Math.floor(leakT)!==o)drawLeak();}});
function leakBars(){var h='';if(leakShown.random!=null)h+=rBar('무작위로 나누기',leakShown.random,COL.stain);if(leakShown.fabric!=null)h+=rBar('원단 단위로 나누기',leakShown.fabric,COL.gfp);
  $('#leakBars').innerHTML=h;}
$$('[data-split]').forEach(function(b){b.addEventListener('click',function(){$$('[data-split]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});
  leakMode=b.dataset.split;leakShown[leakMode]=leakMode==='random'?LK.random:LK.byFabric;leakT=0;drawLeak();leakBars();
  $('#leakI').innerHTML=leakMode==='random'?'<p class="r">R² '+f2(LK.random)+'. 같은 원단의 다른 측정이 학습 쪽에 남아 있어, 모델은 "이웃한 같은 원단"을 찾아 맞힙니다. 점수가 부풀려졌습니다.</p>':
    '<p class="g">R² '+f2(LK.byFabric)+'. 같은 원단의 세 측정이 늘 같은 묶음에 있습니다. 처음 보는 원단에 대한 진짜 실력입니다.</p>';})});

RD.push(drawLeak);
}
/* ---------- ⑤ 계기판 ---------- */
if($('#gauges')){
var GA=[{k:'cv',l:'반복 측정 변동계수',u:'%',min:0,max:40,st:1,v:8,ok:function(v){return v<=15},r:'15% 이하'},
 {k:'icc',l:'급내상관계수 (ICC)',u:'',min:0,max:1,st:.01,v:.86,ok:function(v){return v>=.75},r:'0.75 이상'},
 {k:'r2',l:'교차검증 R² (마찰전기)',u:'',min:-.5,max:1,st:.01,v:.72,ok:function(v){return v>=.6},r:'0.6 이상 (물성은 0.7)'},
 {k:'rs',l:'RMSE ÷ 표준편차',u:'',ro:1,ok:function(v){return v<=.6},r:'0.6 이하 · R²에서 계산'},
 {k:'imp',l:'기준선 대비 RMSE 감소',u:'%',min:-20,max:60,st:1,v:35,ok:function(v){return v>=20},r:'20% 이상'},
 {k:'drop',l:'그룹 제외 검증 R² 하락',u:'',min:0,max:.6,st:.01,v:.08,ok:function(v){return v<=.15},r:'0.15 이내'},
 {k:'cov',l:'90% 예측 구간 적중률',u:'%',min:50,max:100,st:1,v:89,ok:function(v){return v>=85},r:'85% 이상'}];
var gh='';GA.forEach(function(g){gh+='<div class="gauge" id="g_'+g.k+'"><div class="top"><span>'+g.l+'</span><span class="pass" id="gp_'+g.k+'"></span></div>'+
  (g.ro?'<div class="bars" style="grid-template-columns:1fr max-content;margin:8px 0 4px"><div class="track"><div class="fill" id="gf_rs" style="width:0"></div><div class="thr" style="left:60%"></div></div><b class="num" id="gv_rs"></b></div>':
  '<input type="range" min="'+g.min+'" max="'+g.max+'" step="'+g.st+'" value="'+g.v+'" id="gi_'+g.k+'" aria-label="'+g.l+'"><b class="num" id="gv_'+g.k+'"></b>')+
  '<div class="rule">합격선: '+g.r+'</div></div>'});$('#gauges').innerHTML=gh;
function gaUpd(){var n=0;GA.forEach(function(g){var v;
  if(g.ro){var r2=+$('#gi_r2').value;v=r2>=0?Math.sqrt(1-r2):Math.sqrt(1-r2);$('#gv_rs').textContent=v.toFixed(2);var f=$('#gf_rs');f.style.width=Math.min(100,v*100)+'%';f.style.background=g.ok(v)?COL.gfp:COL.eye;}
  else{v=+$('#gi_'+g.k).value;$('#gv_'+g.k).textContent=(g.st<1?v.toFixed(2):v)+g.u;}
  var ok=g.ok(v);if(ok)n++;$('#g_'+g.k).className='gauge '+(ok?'ok':'no');$('#gp_'+g.k).textContent=ok?'통과':'미달';});
  $('#gScore').textContent='통과 '+n+' / '+GA.length;}
$$('#gauges input').forEach(function(i){i.addEventListener('input',gaUpd)});
var GP={good:{cv:8,icc:.86,r2:.72,imp:35,drop:.08,cov:89},over:{cv:8,icc:.86,r2:-.4,imp:-10,drop:.45,cov:58},noisy:{cv:24,icc:.55,r2:.41,imp:12,drop:.12,cov:80}};
$$('[data-gp]').forEach(function(b){b.addEventListener('click',function(){var p=GP[b.dataset.gp];for(var k in p)$('#gi_'+k).value=p[k];gaUpd()})});gaUpd();
var CRIT=[['측정 재현성','반복 측정 변동계수(CV)','같은 원단을 여러 번 측정했을 때의 흔들림','15% 이하'],['측정 재현성','급내상관계수(ICC)','원단 사이 차이가 측정 오차보다 충분히 큰가','0.75 이상'],
 ['예측 정확도','교차검증 R²','원단 사이 차이 중 모델이 설명한 몫','물성(M1·M2) 0.7 이상, 마찰전기(M3) 0.6 이상'],['예측 오차','RMSE·MAE (원래 단위)','평균적으로 빗나간 크기','RMSE가 Y 표준편차의 60% 이하'],
 ['기준선 대비','RMSE 감소율','단순 모델보다 나아졌나','선형 기준선 대비 20% 이상 감소'],['안정성','교차검증 R²의 표준편차','나누는 방식에 따라 흔들리나','0.1 이하'],
 ['일반화','그룹 제외 검증','처음 보는 종류의 원단에서도 맞나','R² 하락 폭 0.15 이내'],['해석 타당성','SHAP 상위 변수','모델이 고른 원인이 상식과 맞나','상위 5개 중 3개 이상을 연구책임자가 타당하다고 판단'],
 ['불확실성','예측 구간 적중률','90% 구간 안에 실측이 들어오나','85% 이상'],['Sim-to-Real','보정 전후 RMSE, 분포 차이(KS 검정)','합성 데이터가 도움이 되나','실측만 쓴 모델보다 RMSE 감소'],
 ['외부 검증','새 원단의 R², 순위 상관','실제 설계에 쓸 수 있나','새 원단 10개 이상에서 R² 0.5 이상, 순위 상관 0.7 이상'],['경로 분석','Q², 경로계수 부트스트랩 유의성, HTMT','인과 사슬이 통계적으로 성립하나','Q² > 0, 주요 경로 p < 0.05, HTMT < 0.85'],
 ['태 분류 (선택)','재현율, F1','거친 원단을 놓치지 않나','재현율 0.85 이상']];
var ct='<table class="tb"><tr><th>평가 대상</th><th>지표</th><th>쉽게 말하면</th><th>합격선 (제안)</th></tr>';CRIT.forEach(function(c){ct+='<tr><td>'+c.map(esc).join('</td><td>')+'</td></tr>'});$('#critT').innerHTML=ct+'</table>';

}
/* ---------- 일정 ---------- */
if($('#ganttSvg')){
var GT=[['p0','0 착수·자료 정리','2026-11-16','2026-11-30','ai','연구책임자 미팅에서 질문 해소, 데이터 사전 작성, 변수 역할표(B·C·A·Y) 확정.','G1 — 변수와 정답의 정의 합의','2026-11-30'],
 ['p1','1 파일럿 탐색 분석','2026-12-01','2027-01-15','ai','27개 원단 정제, 튀는 값 확인, 상관·PCA·군집, FTT와 KES-FB 비교, 핵심 후보 변수 10개 안팎.',null],
 ['p2','2 샘플 확충·전기 특성 실측','2026-12-01','2027-05-31','lab','실험계획법으로 원단 50~100개 제작, 직물 특성 X와 전기 특성 Y(마찰전기) 측정, 반복 측정 원자료 보관. AI 쪽은 입력 양식과 자동 품질검사.','G2 — 원단 50개 이상 X·Y 실측 완료','2027-05-31'],
 ['p3','3 전기 특성 회귀 모델','2027-02-01','2027-06-30','ai','직물 특성 X → 실측 전기 특성 Y 회귀(1차년도 방향). 기준선 → 트리 앙상블 → 가우시안 과정, 원단 단위 교차검증, SHAP.','G3 — 기준선보다 나은 회귀 모델과 교차검증 보고서','2027-06-30'],
 ['p4','4 실측 기반 데이터 생성','2027-04-01','2027-09-30','ai','실측 X 분포를 배워 가상 직물 생성. 분포 비교·범위 밖 차단·제작 가능성 확인. 시뮬레이션(TexGen·Abaqus)은 보조.',null],
 ['p5','5 생성 직물 예측·검증','2027-07-01','2027-12-15','ai','생성 직물의 전기 특성을 불확실도와 함께 예측. 예측 최고·불확실도 최고 후보를 실제 제작해 전향 검증.',null],
 ['p6','6 측정 장치 개선','2027-07-01','2027-11-30','lab','핵심 변수를 정확히 잴 수 있도록 장치 설계, 특허 선행조사.',null]];
var gs=$('#ganttSvg');
function day(d){return Date.parse(d+'T00:00:00Z')/864e5}
function buildGantt(){gs.innerHTML='';var lo=day('2026-11-01'),hi=day('2027-12-31'),X=function(d){return 230+(day(d)-lo)/(hi-lo)*650},Y=function(i){return 64+i*38};
  for(var m=0;m<14;m++){var mm=10+m,ds=(2026+Math.floor(mm/12))+'-'+String(mm%12+1).padStart(2,'0')+'-01',xx=X(ds);
    gs.appendChild(sv('line',{x1:xx,x2:xx,y1:44,y2:330,stroke:'#e6eaee'}));
    gs.appendChild(sv('text',{x:xx+3,y:38,'font-size':11.5,fill:'#5b6874'},(mm%12+1)+'월'));
    if(mm%12===0||m===0)gs.appendChild(sv('text',{x:xx+3,y:20,'font-size':12.5,'font-weight':700,fill:'#16212b'},ds.slice(0,4)));}
  var tx=X('2026-11-17');gs.appendChild(sv('line',{x1:tx,x2:tx,y1:44,y2:330,stroke:'#c9302c','stroke-dasharray':'4 4','stroke-width':1.5}));
  gs.appendChild(sv('text',{x:tx+4,y:343,'font-size':11.5,fill:'#c9302c'},'오늘 11-16'));
  GT.forEach(function(g,i){var y=Y(i),c=g[4]==='ai'?['#e6eefb','#1e55c8']:['#fcebea','#c9302c'],grp=sv('g',{class:'fnode',tabindex:0,role:'button','aria-label':g[1]+' '+g[2]+'부터 '+g[3]+'까지','data-i':i});
    grp.appendChild(sv('text',{x:10,y:y+5,'font-size':13.5,fill:'#16212b'},g[1]));
    var ra={x:X(g[2]),y:y-9,width:Math.max(6,X(g[3])-X(g[2])),height:18,rx:6,fill:i>=4?'#ffffff':c[0],stroke:i>=4?'#8a96a3':c[1],'stroke-width':1.4};if(i>=4)ra['stroke-dasharray']='5 4';grp.appendChild(sv('rect',ra));if(i>=4)grp.appendChild(sv('text',{x:X(g[2])+6,y:y+4.5,'font-size':11.5,fill:'#5b6874'},'예정'));
    if(g[7]){var gx=X(g[7]);grp.appendChild(sv('path',{d:'M'+gx+' '+(y-10)+'l9 10l-9 10l-9 -10z',fill:'#c9302c'}));
      grp.appendChild(sv('text',{x:gx+12,y:y-10,'font-size':11.5,'font-weight':700,fill:'#c9302c'},g[6].slice(0,2)));}
    grp.addEventListener('click',function(){ganttSel(i)});grp.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();ganttSel(i)}});
    gs.appendChild(grp);});
  [['#e6eefb','#1e55c8','AI 담당',360],['#fcebea','#c9302c','연구실 주도',460]].forEach(function(l){gs.appendChild(sv('rect',{x:l[3],y:356,width:14,height:12,rx:3,fill:l[0],stroke:l[1]}));
    gs.appendChild(sv('text',{x:l[3]+20,y:367,'font-size':12,fill:'#5b6874'},l[2]))});
  gs.appendChild(sv('path',{d:'M580 356l6 6l-6 6l-6 -6z',fill:'#c9302c'}));gs.appendChild(sv('text',{x:592,y:367,'font-size':12,fill:'#5b6874'},'관문'));}
function ganttSel(i){var g=GT[i];$$('.fnode',gs).forEach(function(x){x.style.opacity=x.dataset.i==String(i)?1:.55});
  $('#ganttD').innerHTML='<h4>'+esc(g[1])+' <span class="small muted">'+g[2]+' ~ '+g[3]+' · '+(g[4]==='ai'?'AI 담당':'연구실 주도')+'</span></h4><p style="margin:0">'+esc(g[5])+'</p>'+(g[6]?'<p style="margin:6px 0 0;color:#c9302c"><b>관문</b> '+esc(g[6])+'</p>':'')+'<p style="margin:8px 0 0"><a href="stage_'+i+'_'+['kickoff','explore','data','model','sim2real','tribo','device'][i]+'.html">S'+i+' 스테이지 쪽 보기 →</a>'+(i>=4?' <span class="st plan">예정</span>':'')+'</p>';}
buildGantt();ganttSel(2);

}
/* ---------- 질문 ---------- */
if($('#qlist')){
var QS=[['역할과 기간','AI 분석 쪽의 역할 범위와 과제 협약 기간·연차 시작일은 어떻게 되나요?'],
 ['정답 Y','마찰전기를 어떤 장치·모드(접촉-분리 등)·상대 물질로, 언제부터 측정하나요? 지표는 전압·전류·전하밀도 중 무엇인가요?'],
 ['태의 위치','태(Hand)도 연구 목표인가요, 교육용인가요? 목표라면 관능평가 계획이 있나요?'],
 ['열 이름','엑셀 열 이름의 _1·_2·_3과 끝의 i는 무엇인가요? _1이 FTT가 맞나요?'],
 ['튀는 값','H_ND3의 뒷면 SRA 1,159 μm, L_KS1의 가로 방향 BW 9.7은 입력 오류인가요, 실제 값인가요?'],
 ['원자료','반복 측정 원자료와 시계열 마찰 원자료가 있나요? 파일 형식은 무엇인가요?'],
 ['실 특성','실 13종의 빈칸(섬도·꼬임 수·강도 등)을 채울 수 있나요? 중공율·단면 형상은 측정 계획이 있나요?'],
 ['장비 통일','새 원단은 FTT와 KES-FB 중 어느 장비로 통일해 측정할까요? 두 장비 값은 압축 일만 뚜렷이 맞았습니다.'],
 ['데이터 범위','Huvis 데이터의 출처와 공개 범위(논문·강의에 써도 되는지)는 어떻게 되나요?'],
 ['시뮬레이션','Sim-to-Real 시뮬레이션(TexGen·Abaqus)은 누가 맡나요?']];
var qh='';QS.forEach(function(q,i){qh+='<button aria-pressed="false" data-q="'+i+'"><span class="bx" aria-hidden="true"></span><span><span class="who">'+(i+1)+'. '+q[0]+'</span>'+q[1]+'</span></button>'});$('#qlist').innerHTML=qh;
function qPaint(){var S=ST.get().q;$$('#qlist button').forEach(function(b){var on=!!S[b.dataset.q];b.setAttribute('aria-pressed',on);b.querySelector('.bx').textContent=on?'✓':''});$('#askN').textContent=Object.keys(S).filter(function(k){return S[k]}).length+' / 10';}
$$('#qlist button').forEach(function(b){b.addEventListener('click',function(){var S=ST.get().q;S[b.dataset.q]=!S[b.dataset.q];ST.save();qPaint();HOOK.revSum();})});qPaint();

}
/* ---------- 검토 사항 (스테이지별, 이 브라우저에 보관) ---------- */
var REV={s0:[['S0-1','엑셀 열 이름 해석','_1 = FTT 계열, _2 = KES-FB 계열, _3 = 일반 시험, 끝의 i는 미확인으로 보았습니다.'],
  ['S0-2','튀는 값 2건 처리','H_ND3 뒷면 SRA 1,159 μm, L_KS1 가로 BW 9.7 — 입력 오류면 고치고, 실제 값이면 그대로 둡니다.'],
  ['S0-3','정답 Y 측정 시작','마찰전기 출력(전압·전류·전하밀도)을 기존 장치로 언제부터, 몇 개 원단에 측정할지.']],
 s1:[['S1-1','탐색 분석 해석','같은 종류끼리 모이고 부직포는 넓게 흩어진다는 해석이 섬유공학적으로 타당한지.'],
  ['S1-2','측정 장비 통일','새 원단은 FTT와 KES-FB 중 하나로 통일해 측정. 두 장비 값은 압축 일만 뚜렷이 일치했습니다.'],
  ['S1-3','부직포 포함 여부','Huvis 부직포 9개를 계속 분석에 넣을지, 제직·편직 중심으로 좁힐지.']],
 s2:[['S2-1','기록 항목','직물 특성 X(식별·실 특성·제작 조건·기본 물성·역학·표면)와 전기 특성 Y(마찰전기), 측정 환경과 원단당 횟수(제안).'],
  ['S2-2','실험계획 요인·수준','실 4종 × 조직 3 × 밀도 3 × 계열 2 = 72개 + 기존 27개. 한 요인만 다른 짝을 남깁니다.'],
  ['S2-3','재측정 기준과 측정 환경','반복 측정 변동계수 15% 초과 시 재측정, 표준 상태 ISO 139(20 ± 2 °C, 65 ± 4 %) 기록.']],
 s3:[['S3-1','1차년도 목표 (2026-11-17)','직물 주요 특성 X → 실측 전기 특성 Y 회귀. 실측 정답으로 배우는 지도학습 단계입니다.'],
  ['S3-2','모델 순서','기준선 → 랜덤포레스트·XGBoost → 신경망. 신경망은 원단 100개 이상이거나 합성 데이터가 있을 때.'],
  ['S3-3','경로 분석 방법','구조 → 물성 → 성능 경로를 작은 표본에서 추정하는 PLS-SEM 사용.'],
  ['S3-4','성능 보고 원칙','원단 단위로 나눈 검증 결과만 성능으로 보고하고, 예측값 대 실측값 산점도를 함께 냅니다.'],
  ['S3-5','합격선','교차검증 R² 물성 0.7·마찰전기 0.6 이상, 기준선 대비 RMSE 20% 감소 등 13개 기준(제안값).'],
  ['S3-6','외부 검증','새 원단 10개 이상으로 예측을 먼저 적어 두고 측정해 맞춰 봅니다.']],
 s4:[['S4-1','생성 대상','가상 직물의 특성 X만 생성하고, 전기 특성 Y는 만들지 않는 안 (생성 Y를 다시 학습에 넣지 않음).'],
  ['S4-2','생성 범위','실측 범위 안으로 제한할지, 실험실이 만들 수 있는 범위까지 넓힐지.'],
  ['S4-3','시뮬레이션 보조 경로','TexGen·Abaqus를 1차년도에 함께 할지, 2차년도로 미룰지.']],
 s5:[['S5-1','정답 지표','전압·전류·전하밀도 중 무엇을 주 지표로 할지 (S2와 같은 조건).'],
  ['S5-2','전향 검증 원단 수','생성 직물 중 실제로 만들어 잴 원단 수 (제안 10개 이상).'],
  ['S5-3','선정 규칙','예측 최고 후보와 불확실도 최고 후보를 몇 개씩 섞을지.']],
 mr:[['MR-1','방법의 이름','"비지도 학습" 대신 "실측 지도 회귀 + 가상 샘플 생성(VSG) + 전향 검증"으로 부르는 안.'],
  ['MR-2','생성 데이터의 쓰임','생성 직물은 예측·선별에만 쓰고, 생성 Y로 모델을 다시 학습하지 않는 원칙.'],
  ['MR-3','전기 특성 측정 표준','접촉 모드·상대 물질·힘·주파수·온습도를 고정하고 반복 측정 변동계수를 함께 기록.'],
  ['MR-4','성능 보고 원칙','생성 데이터를 쓴 모델도 점수는 실측 원단으로만 잼 (TSTR).']],
 s6:[['S6-1','담당 확정 (예정)','장치 설계·제작을 맡을 사람과 제작처.'],
  ['S6-2','개선 목표 우선순위 (예정)','측정 정확도와 측정 용이성 중 무엇을 먼저 올릴지.'],
  ['S6-3','특허 선행조사 범위 (예정)','마찰전기 측정 장치 관련 선행 특허를 어디까지 볼지.']]};
var SNAME={s0:'S0 착수·자료 정리',s1:'S1 파일럿 탐색 분석',s2:'S2 샘플 확충·전기 특성 실측',s3:'S3 전기 특성 회귀 모델',s4:'S4 실측 기반 데이터 생성',s5:'S5 생성 직물 예측·검증',s6:'S6 측정 장치 개선',mr:'1차년도 연구 방법 검토'};
var SFILE={mr:'method_review.html',s0:'stage_0_kickoff.html',s1:'stage_1_explore.html',s2:'stage_2_data.html',s3:'stage_3_model.html',s4:'stage_4_sim2real.html',s5:'stage_5_tribo.html',s6:'stage_6_device.html'};
var VL={agree:'동의',fix:'수정 필요',talk:'논의 필요'};
function rvGet(id){var r=ST.get().rv;return r[id]||{v:'',m:''}}
function rvSet(id,o){ST.get().rv[id]=o;ST.save();}
$$('.review[data-rev]').forEach(function(box){var k=box.dataset.rev,h='<h4>검토 사항 — 교수님 검토 요청</h4><p class="small muted" style="margin:0 0 4px">항목마다 하나를 고르시고, 필요하면 의견을 적어 주십시오. 표시는 이 브라우저에만 남고, INDEX의 검토 결과 정리에 모입니다.</p>';
  REV[k].forEach(function(r){var s=rvGet(r[0]);h+='<div class="ri"><div class="rq">'+r[0]+'. '+esc(r[1])+'<small>'+esc(r[2])+'</small></div><div class="ro" role="group" aria-label="'+r[0]+' 검토">'+
    ['agree','fix','talk'].map(function(v){return '<button data-id="'+r[0]+'" data-v="'+v+'" aria-pressed="'+(s.v===v)+'">'+VL[v]+'</button>'}).join('')+
    '<input type="text" data-id="'+r[0]+'" value="'+esc(s.m)+'" placeholder="의견 메모 (선택)" aria-label="'+r[0]+' 의견 메모"></div></div>';});
  box.innerHTML=h;});
$$('.review .ro button').forEach(function(b){b.addEventListener('click',function(){var id=b.dataset.id,on=b.getAttribute('aria-pressed')!=='true',s=rvGet(id);
  $$('.review .ro button[data-id="'+id+'"]').forEach(function(x){x.setAttribute('aria-pressed','false')});if(on)b.setAttribute('aria-pressed','true');s.v=on?b.dataset.v:'';rvSet(id,s);HOOK.revSum();})});
$$('.review .ro input').forEach(function(i){i.addEventListener('input',function(){var s=rvGet(i.dataset.id);s.m=i.value;rvSet(i.dataset.id,s);HOOK.revSum();})});
function revAll(){var L=[];Object.keys(REV).forEach(function(k){REV[k].forEach(function(r){var s=rvGet(r[0]);L.push([r[0],r[1],s.v,s.m,k])})});return L;}
var QS_T=['역할과 기간','정답 Y','태의 위치','열 이름','튀는 값','원자료','실 특성','장비 통일','데이터 범위','시뮬레이션'];
if($('#revT')){
HOOK.revSum=function(){var L=revAll(),c={agree:0,fix:0,talk:0,'':0};L.forEach(function(r){c[r[2]]++});
  $('#revK').innerHTML='<div class="kpi g"><b>'+c.agree+'</b><span>동의</span></div><div class="kpi a"><b>'+c.fix+'</b><span>수정 필요</span></div><div class="kpi i"><b>'+c.talk+'</b><span>논의 필요</span></div><div class="kpi r"><b>'+c['']+'</b><span>아직 검토 전</span></div>';
  var h='<table class="tb"><tr><th>번호</th><th>스테이지</th><th>검토 사항</th><th>결과</th><th>의견 메모</th></tr>';
  L.forEach(function(r){var col=r[2]==='agree'?COL.gfp:r[2]==='fix'?COL.amber:r[2]==='talk'?COL.info:COL.muted;
    h+='<tr><td>'+r[0]+'</td><td><a href="'+SFILE[r[4]]+'#review-'+r[4]+'">'+SNAME[r[4]]+'</a></td><td>'+esc(r[1])+'</td><td style="color:'+col+';font-weight:700">'+(r[2]?VL[r[2]]:'—')+'</td><td>'+esc(r[3])+'</td></tr>'});
  $('#revT').innerHTML=h+'</table>';
  var q=ST.get().q,qn=Object.keys(q).filter(function(k){return q[k]}).length;$('#revQ').textContent=qn+' / 10';
  var n=L.length-c[''];$('#revSay').textContent=n?'검토 사항 '+L.length+'개 중 '+n+'개를 표시해 주셨습니다. 수정 '+c.fix+'건, 논의 '+c.talk+'건은 다음 보고에 반영하겠습니다.':'아직 표시된 검토 사항이 없습니다. 스테이지 쪽에서 표시해 주시면 여기에 모입니다.';};
function revText(){var L=revAll(),q=ST.get().q,ql=Object.keys(q).filter(function(k){return q[k]}).map(function(k){return '  - '+(+k+1)+'. '+QS_T[+k]});
  return ['[검토 결과] 직물 구조로 성능을 미리 맞히는 AI — 연구 계획 브리핑 (작성 '+new Date().toLocaleDateString('sv-SE')+')',''].concat(L.map(function(r){return r[0]+' ['+SNAME[r[4]]+'] '+r[1]+': '+(r[2]?VL[r[2]]:'검토 전')+(r[3]?' — '+r[3]:'')}))
   .concat(['','답을 들은 결정 질문 '+ql.length+' / 10'].concat(ql)).join('\n');}
$('#revCopy').addEventListener('click',function(){var t=revText(),pre=$('#revTxt');pre.textContent=t;pre.hidden=false;
  function ok(){$('#revMsg').textContent='복사했습니다.'}function sel(){var r=document.createRange();r.selectNodeContents(pre);var s=window.getSelection();s.removeAllRanges();s.addRange(r);$('#revMsg').textContent='아래 글을 선택해 두었습니다. 복사해 주십시오.'}
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(ok,sel);else sel();});
$('#revClear').addEventListener('click',function(){if(!$('#revClear').dataset.arm){$('#revClear').dataset.arm='1';$('#revClear').textContent='한 번 더 누르면 지웁니다';return;}
  var m=ST.get();m.rv={};m.q={};ST.save();$('#revClear').dataset.arm='';$('#revClear').textContent='표시 모두 지우기';HOOK.revSum();});
HOOK.revSum();}
if($('#kgList')){
var KG=LAB.kg,REF=LAB.refs,META=LAB.meta;
var TK={Concept:['개념','#1e55c8'],Term:['용어','#5b6874'],Method:['방법','#13733a'],Problem:['문제','#c9302c'],Limitation:['한계','#c9302c'],Metric:['지표','#a35c00'],
  Claim:['주장','#9b3fb5'],Question:['질문','#8f5a2e'],Analogy:['비유','#93651a'],Simulation:['시뮬레이션','#0b7a86'],Work:['문헌','#5a5a6e']};
var NB={};KG.nodes.forEach(function(n){NB[n.id]=n});
var kgOn={};Object.keys(TK).forEach(function(k){kgOn[k]=k!=='Simulation'&&k!=='Work'});
var kc='';Object.keys(TK).forEach(function(k){var c=KG.nodes.filter(function(n){return n.type===k}).length;kc+='<button class="bt" data-t="'+k+'" aria-pressed="'+kgOn[k]+'">'+TK[k][0]+' '+c+'</button>'});
$('#kgChips').innerHTML=kc;var kgOpen=null;
function kgList(){var q=$('#kgQ').value.trim().toLowerCase(),h='',cnt=0;
  KG.nodes.forEach(function(n){if(!kgOn[n.type])return;var hay=[n.label.ko,n.label.en,(n.altLabel&&n.altLabel.ko||[]).join(' '),n.definition?n.definition.ko:''].join(' ').toLowerCase();
    if(q&&hay.indexOf(q)<0)return;cnt++;var ev=KG.edges.filter(function(e){return e.s===n.id||e.o===n.id}).length;
    h+='<div class="kgitem'+(kgOpen===n.id?' open':'')+'" id="ki_'+n.id.replace(/[^a-z0-9]/gi,'_')+'"><div class="t"><b>'+esc(n.label.ko)+'</b><span class="ty" style="color:'+TK[n.type][1]+'">'+TK[n.type][0]+'</span><span class="small muted">'+esc(n.label.en)+'</span></div>'+
      (n.definition?'<p>'+esc(n.definition.ko)+'</p>':'')+'<p class="small"><a href="'+n.anchor+'">설명 보러 가기 →</a> <span class="muted">관계 '+ev+'개'+(n.evidence?' · 근거 '+n.evidence.length+'개':'')+'</span></p></div>';});
  $('#kgList').innerHTML=h||'<p class="muted">찾는 항목이 없습니다.</p>';
  $('#kgStat').textContent='노드 '+KG.nodes.length+'개 · 관계 '+KG.edges.length+'개 · 보이는 항목 '+cnt+'개';}
$('#kgQ').addEventListener('input',kgList);
$$('#kgChips button').forEach(function(b){b.addEventListener('click',function(){kgOn[b.dataset.t]=!kgOn[b.dataset.t];b.setAttribute('aria-pressed',kgOn[b.dataset.t]);kgList();kgLayout();})});
var kgCv=$('#kgCv'),KP={};
function kgLayout(){var vis=KG.nodes.filter(function(n){return kgOn[n.type]}).slice(0,80),r=rng(3),W=kgCv.clientWidth||400,H=380;KP={};
  vis.forEach(function(n){KP[n.id]={x:40+r()*(W-80),y:30+r()*(H-60),vx:0,vy:0}});
  var E=KG.edges.filter(function(e){return KP[e.s]&&KP[e.o]});
  for(var it=0;it<200;it++){var ids=Object.keys(KP);
    ids.forEach(function(a,i){for(var j=i+1;j<ids.length;j++){var A=KP[a],B=KP[ids[j]],dx=A.x-B.x,dy=A.y-B.y,d2=dx*dx+dy*dy+.01,f=900/d2;A.vx+=dx*f/Math.sqrt(d2);A.vy+=dy*f/Math.sqrt(d2);B.vx-=dx*f/Math.sqrt(d2);B.vy-=dy*f/Math.sqrt(d2);}});
    E.forEach(function(e){var A=KP[e.s],B=KP[e.o],dx=B.x-A.x,dy=B.y-A.y,d=Math.sqrt(dx*dx+dy*dy)+.01,f=(d-60)*.02;A.vx+=dx/d*f;A.vy+=dy/d*f;B.vx-=dx/d*f;B.vy-=dy/d*f;});
    ids.forEach(function(k){var p=KP[k];p.vx+=(W/2-p.x)*.003;p.vy+=(H/2-p.y)*.003;p.x+=Math.max(-8,Math.min(8,p.vx));p.y+=Math.max(-8,Math.min(8,p.vy));p.vx*=.5;p.vy*=.5;
      p.x=Math.max(14,Math.min(W-14,p.x));p.y=Math.max(14,Math.min(H-14,p.y));});}
  drawKg();}
function drawKg(){var W=fit(kgCv,380),x=kgCv.getContext('2d');x.clearRect(0,0,W,380);
  KG.edges.forEach(function(e){var A=KP[e.s],B=KP[e.o];if(!A||!B)return;x.strokeStyle=e.p==='lab:hasLimitation'||e.p==='lab:addressedBy'?'rgba(201,48,44,.45)':e.p==='lab:prerequisiteOf'?'rgba(19,115,58,.55)':'rgba(91,104,116,.25)';
    x.beginPath();x.moveTo(A.x,A.y);x.lineTo(B.x,B.y);x.stroke();});
  for(var id in KP){var p=KP[id],n=NB[id];x.beginPath();x.arc(p.x,p.y,kgOpen===id?8:5.5,0,7);x.fillStyle=TK[n.type][1];x.fill();
    if(kgOpen===id){x.fillStyle=COL.text;x.font='12px "IBM Plex Sans KR",sans-serif';x.textAlign='center';x.fillText(n.label.ko,p.x,p.y-12);}}}
kgCv.addEventListener('pointerdown',function(e){var r=kgCv.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top,best=null,bd=300;
  for(var id in KP){var p=KP[id],d=(p.x-mx)*(p.x-mx)+(p.y-my)*(p.y-my);if(d<bd){bd=d;best=id}}
  if(best){kgOpen=best;kgList();drawKg();var el=document.getElementById('ki_'+best.replace(/[^a-z0-9]/gi,'_'));if(el)el.scrollIntoView({block:'nearest',behavior:reduce?'auto':'smooth'});}});
$('#kgLeg').innerHTML='<span style="color:#13733a">━</span> 먼저 알아야 함 · <span style="color:#c9302c">━</span> 한계와 해결 · <span style="color:#8a96a3">━</span> 그 밖의 관계 · 점을 누르면 목록에서 펼칩니다';
var pth=['lab:method/data-audit','lab:limitation/no-target','lab:method/pca','lab:limitation/source-confound','lab:method/doe','lab:limitation/small-sample','lab:method/baseline','lab:problem/overfitting','lab:method/group-cv'];
$('#kgPath').innerHTML=pth.map(function(id,i){var n=NB[id];return (i?'<span class="muted">→</span>':'')+'<span class="'+(n.type==='Method'?'c':'l')+'">'+esc(n.label.ko)+'</span>'}).join('');
$('#kgOpen').innerHTML=KG.nodes.filter(function(n){return n.type==='Question'}).map(function(n){return '<li><b>'+esc(n.label.ko)+'</b> — '+esc(n.definition.ko)+'</li>'}).join('');
kgList();kgLayout();

var CRC=(function(){var t=[],c;for(var n=0;n<256;n++){c=n;for(var k=0;k<8;k++)c=c&1?0xEDB88320^(c>>>1):c>>>1;t[n]=c>>>0;}
  return function(u8){var x=0xFFFFFFFF;for(var i=0;i<u8.length;i++)x=t[(x^u8[i])&255]^(x>>>8);return (x^0xFFFFFFFF)>>>0;};})();
function makeZip(files){var enc=new TextEncoder(),parts=[],central=[],off=0;function u16(v){return [v&255,(v>>8)&255]}function u32(v){return [v&255,(v>>8)&255,(v>>16)&255,(v>>>24)&255]}
  files.forEach(function(f){var name=enc.encode(f.name),data=enc.encode(f.text),crc=CRC(data);
    var head=[].concat(u32(0x04034b50),u16(20),u16(0x0800),u16(0),u16(0),u16(0),u32(crc),u32(data.length),u32(data.length),u16(name.length),u16(0));
    parts.push(new Uint8Array(head),name,data);
    central.push([].concat(u32(0x02014b50),u16(20),u16(20),u16(0x0800),u16(0),u16(0),u16(0),u32(crc),u32(data.length),u32(data.length),u16(name.length),u16(0),u16(0),u16(0),u16(0),u32(0),u32(off)),name);
    off+=head.length+name.length+data.length;});
  var cdStart=off,cdLen=0;central.forEach(function(c){if(Array.isArray(c)){parts.push(new Uint8Array(c));cdLen+=c.length;}else{parts.push(c);cdLen+=c.length;}});
  parts.push(new Uint8Array([].concat(u32(0x06054b50),u16(0),u16(0),u16(files.length),u16(files.length),u32(cdLen),u32(cdStart),u16(0))));
  return new Blob(parts,{type:'application/zip'});}
var BIBT={'article-journal':'article','paper-conference':'inproceedings','book':'book','chapter':'incollection','webpage':'misc','dataset':'misc','report':'techreport','thesis':'phdthesis','software':'misc'};
var RIST={'article-journal':'JOUR','paper-conference':'CPAPER','book':'BOOK','chapter':'CHAP','webpage':'ELEC','dataset':'DATA','report':'RPRT','thesis':'THES','software':'COMP'};
function names(a){return (a||[]).map(function(p){return p.literal||(p.family+(p.given?', '+p.given:''))})}
function yr(r){return r.issued&&r.issued['date-parts'][0][0]}
function toBib(r){var f=[],add=function(k,v){if(v!==undefined&&v!==null&&v!=='')f.push('  '+k+' = {'+v+'}')};
  add('title',r.title);add('author',names(r.author).join(' and '));add('year',yr(r));add(r.type==='article-journal'?'journal':'booktitle',r['container-title']);
  add('edition',r.edition);add('publisher',r.publisher);add('doi',r.DOI);add('url',r.URL);if(r.lab&&r.lab.note)add('note',r.lab.note);
  return '@'+(BIBT[r.type]||'misc')+'{'+r.id+',\n'+f.join(',\n')+'\n}';}
function toRis(r){var L=['TY  - '+(RIST[r.type]||'GEN')],add=function(t,v){if(v)L.push(t+'  - '+v)};add('TI',r.title);names(r.author).forEach(function(n){add('AU',n)});
  add('PY',yr(r));add('PB',r.publisher);add('ET',r.edition);add('UR',r.URL);add('DO',r.DOI);if(r.lab&&r.lab.note)add('N1',r.lab.note);L.push('ER  - ');return L.join('\r\n');}
function plain(r){var a=names(r.author).join(', ');return (a?a+' ':'')+(yr(r)?'('+yr(r)+'). ':'')+r.title+(r.edition?' ('+r.edition+'nd ed.)':'')+(r.publisher?'. '+r.publisher:'')+'.'+(r.URL?' '+r.URL:'');}
function filterScope(g,sc){if(sc==='all')return g;var keep;
  if(sc==='concepts')keep=function(n){return ['Concept','Method','Term','Metric','Problem','Limitation'].indexOf(n.type)>=0};
  else if(sc==='claims')keep=function(n){return n.type==='Claim'||n.type==='Work'||KG.edges.some(function(e){return e.p==='lab:supports'&&e.o===n.id})};
  else keep=function(n){return KG.edges.some(function(e){return e.p==='lab:prerequisiteOf'&&(e.s===n.id||e.o===n.id)})};
  var ns=g.nodes.filter(keep),ids={};ns.forEach(function(n){ids[n.id]=1});
  var es=g.edges.filter(function(e){return ids[e.s]&&ids[e.o]&&(sc!=='prereq'||e.p==='lab:prerequisiteOf')});return {version:g.version,page:g.page,scope:sc,nodes:ns,edges:es};}
var CTX={skos:'http://www.w3.org/2004/02/skos/core#',schema:'https://schema.org/',dct:'http://purl.org/dc/terms/',prov:'http://www.w3.org/ns/prov#',lab:'urn:lab:',rdf:'http://www.w3.org/1999/02/22-rdf-syntax-ns#'};
function toJsonLd(g){var gr=g.nodes.map(function(n){var o={'@id':n.id,'@type':['lab:'+n.type],'skos:prefLabel':[{'@value':n.label.ko,'@language':'ko'},{'@value':n.label.en,'@language':'en'}]};
  if(n.definition)o['skos:definition']={'@value':n.definition.ko,'@language':'ko'};return o;});
  g.edges.forEach(function(e){var s=gr.filter(function(o){return o['@id']===e.s})[0];if(s){(s[e.p]=s[e.p]||[]).push({'@id':e.o});}});
  return {'@context':CTX,'@graph':gr,'dct:source':META.title};}
function lit(s){return '"'+String(s).replace(/\\/g,'\\\\').replace(/"/g,'\\"')+'"'}
function toTurtle(g){var L=[];for(var k in CTX)L.push('@prefix '+k+': <'+CTX[k]+'> .');L.push('');
  g.nodes.forEach(function(n){var p=['<'+n.id+'> a lab:'+n.type,'  skos:prefLabel '+lit(n.label.ko)+'@ko, '+lit(n.label.en)+'@en'];if(n.definition)p.push('  skos:definition '+lit(n.definition.ko)+'@ko');L.push(p.join(' ;\n')+' .');});
  g.edges.forEach(function(e){L.push('<'+e.s+'> '+e.p+' <'+e.o+'> .')});return L.join('\n');}
function csv(rows){return rows.map(function(r){return r.map(function(v){v=v==null?'':String(v);return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v}).join(',')}).join('\r\n')}
function nodesCsv(g){return csv([['id','type','label_ko','label_en','status','level','family','page','anchor']].concat(g.nodes.map(function(n){return [n.id,n.type,n.label.ko,n.label.en,n.status,n.level||'',n.family||'',n.page,n.anchor]})))}
function edgesCsv(g){return csv([['source','predicate','target','anchor','confidence']].concat(g.edges.map(function(e){return [e.s,e.p,e.o,e.anchor,e.confidence]})))}
function provCsv(g){var rows=[['item','kind','work','loc','factCard','confidence','verified','pageAnchor']];
  g.edges.filter(function(e){return e.p==='lab:assertedIn'}).forEach(function(e){var w=e.o.split('/').pop(),r=REF.filter(function(x){return x.id===w})[0],n=NB[e.s],loc='';
    if(r&&r.lab.locs)r.lab.locs.forEach(function(l){if(l.claim===e.s)loc=l.loc});if(!loc&&n.source&&n.source[0].loc)loc=n.source[0].loc;
    rows.push([e.s,'node',w,loc,(e.evidence||[]).join(' '),n.confidence,r&&r.lab.verified.title?'title':'no',n.anchor]);});return csv(rows);}
function mermaid(g){var L=['graph LR'],ids={},i=0;g.nodes.slice(0,40).forEach(function(n){ids[n.id]='N'+(i++);L.push('  '+ids[n.id]+'["'+n.label.ko.replace(/"/g,"'")+'"]')});
  g.edges.forEach(function(e){if(ids[e.s]&&ids[e.o])L.push('  '+ids[e.s]+' -->|'+e.p.replace('lab:','')+'| '+ids[e.o])});return L.join('\n');}
function readme(g){return [META.title,'','꾸러미 버전 '+META.version+' · 만든 날 '+META.date,'노드 '+g.nodes.length+'개, 관계 '+g.edges.length+'개, 문헌 '+REF.length+'개','',
  '인용: '+META.suggestedCitation,'','확인 필요:'].concat(needs().map(function(s){return ' - '+s})).concat(['','채워 넣을 것: 라이선스, 공개 주소','','실측 값(채움 지도, PCA, 장비 간 순위 상관)은 엑셀 직접 계산. 과적합·누수 실험과 합격선은 설명용 모형·제안값.']).join('\r\n');}
function needs(){var L=[];REF.forEach(function(r){var v=r.lab.verified,miss=Object.keys(v).filter(function(k){return !v[k]});if(miss.length)L.push(r.id+': '+miss.join(', ')+(r.lab.note?' ('+r.lab.note+')':''))});
  L.push('열 이름 _1·_2·_3이 FTT·KES-FB·일반 시험인지 (장비 추정)');L.push('라이선스·공개 주소 (페이지 서지)');return L;}
function buildPackage(sc){var g=filterScope(KG,sc);var files=[
  {name:'page_meta.json',text:JSON.stringify(META,null,2)},{name:'kg.json',text:JSON.stringify(g,null,2)},{name:'kg.jsonld',text:JSON.stringify(toJsonLd(g),null,2)},
  {name:'kg.ttl',text:toTurtle(g)},{name:'nodes.csv',text:'﻿'+nodesCsv(g)},{name:'edges.csv',text:'﻿'+edgesCsv(g)},
  {name:'references.csl.json',text:JSON.stringify(REF,null,2)},{name:'references.bib',text:REF.map(toBib).join('\n\n')},{name:'references.ris',text:REF.map(toRis).join('\r\n')},
  {name:'provenance.csv',text:'﻿'+provCsv(g)},{name:'README.txt',text:readme(g)}];
  files.unshift({name:'manifest.json',text:JSON.stringify({package:'lab-kg',version:META.version,page:META.number,created:META.date,scope:sc,counts:{nodes:g.nodes.length,edges:g.edges.length,refs:REF.length},files:files.map(function(f){return f.name})},null,2)});
  return files;}
window.__buildPackage=buildPackage;window.__makeZip=makeZip;
$('#kgJson').addEventListener('click',function(){dlText(JSON.stringify(KG,null,2),'kg_01.json','application/json')});
$('#kgMer').addEventListener('click',function(){dlText(mermaid(KG),'kg_01.mmd')});

var claims=KG.nodes.filter(function(n){return n.type==='Claim'}),withSrc=claims.filter(function(n){return KG.edges.some(function(e){return e.s===n.id&&e.p==='lab:assertedIn'})});
var verOk=REF.filter(function(r){return r.lab.verified.title&&r.lab.verified.year}).length;
$('#exK').innerHTML='<div class="kpi g"><b>'+KG.nodes.length+'</b><span>노드</span></div><div class="kpi m"><b>'+KG.edges.length+'</b><span>관계</span></div><div class="kpi i"><b>'+REF.length+'</b><span>문헌</span></div>'+
 '<div class="kpi a"><b>'+Math.round(100*verOk/REF.length)+'%</b><span>제목·연도 확인된 문헌</span></div><div class="kpi g"><b>'+Math.round(100*withSrc.length/claims.length)+'%</b><span>출처 있는 주장</span></div>';
$('#exSay').textContent='출처 없는 주장은 꾸러미에 넣지 않았어요. 확인할 항목 '+needs().length+'개는 아래에 있어요.';
var pageRef={id:'ahn2026textile',type:'webpage',title:META.title,author:[{family:'안',given:'상선'}],issued:{'date-parts':[[2026,11,14]]},lab:{verified:{}}};
var cf='plain';function cite(){$('#citeBox').textContent=cf==='plain'?META.suggestedCitation:cf==='bib'?toBib(pageRef):toRis(pageRef)}
$$('[data-cf]').forEach(function(b){b.addEventListener('click',function(){$$('[data-cf]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});cf=b.dataset.cf;cite()})});cite();
$('#citeCopy').addEventListener('click',function(){var t=$('#citeBox').textContent,b=this;function done(){b.textContent='복사됨';setTimeout(function(){b.textContent='복사'},1200)}
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(done,sel);else sel();
  function sel(){var r=document.createRange();r.selectNodeContents($('#citeBox'));var s=window.getSelection();s.removeAllRanges();s.addRange(r);}});
var RL={primary:'주 자료',background:'배경',data:'수치',figure:'그림'};
$('#refList').innerHTML=REF.map(function(r){var v=r.lab.verified,ok=v.title&&v.year;
  return '<li>'+esc(plain(r))+' <span class="badge role">'+(RL[r.lab.role]||r.lab.role)+'</span><span class="badge '+(ok?'ok':'no')+'">'+(ok?'확인됨':'확인 필요')+'</span>'+
   (r.lab.supports.length?'<details><summary class="small">뒷받침하는 개념 '+r.lab.supports.length+'개</summary><span class="small">'+r.lab.supports.map(function(s){return NB[s]?'<a href="#kg" data-kgo="'+s+'">'+esc(NB[s].label.ko)+'</a>':''}).join(' · ')+'</span></details>':'')+'</li>'}).join('');
$$('[data-kgo]').forEach(function(a){a.addEventListener('click',function(){var id=a.dataset.kgo,t=NB[id].type;if(!kgOn[t]){kgOn[t]=true;$('#kgChips [data-t="'+t+'"]').setAttribute('aria-pressed','true');kgLayout();}kgOpen=id;kgList();drawKg();})});
var sc='all';$$('[data-sc]').forEach(function(b){b.addEventListener('click',function(){$$('[data-sc]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});sc=b.dataset.sc;})});
$('#zipBtn').addEventListener('click',function(){download(makeZip(buildPackage(sc)),'kg_01_'+sc+'.zip')});
var FN2=['manifest.json','page_meta.json','kg.json','kg.jsonld','kg.ttl','nodes.csv','edges.csv','references.csl.json','references.bib','references.ris','provenance.csv','README.txt'];
$('#fileBtns').innerHTML=FN2.map(function(f){return '<button class="bt" data-f="'+f+'">'+f+'</button>'}).join('');
$$('[data-f]').forEach(function(b){b.addEventListener('click',function(){var f=buildPackage(sc).filter(function(x){return x.name===b.dataset.f})[0];dlText(f.text,f.name)})});
$('#needList').innerHTML=needs().map(function(s){return '<li>'+esc(s)+'</li>'}).join('');
$('#verInfo').textContent='꾸러미 버전 '+META.version+' · 만든 날 '+META.date+' · 페이지 '+META.number+' · 등록부: 이 시리즈 첫 페이지라 새로 만듦';

RD.push(kgLayout);
}
/* ---------- 그리기 시작 ---------- */
function redraw(){RD.forEach(function(f){try{f()}catch(e){if(window.console)console.error(e)}})}
var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(redraw,120)});
redraw();requestAnimationFrame(loop);
})();
