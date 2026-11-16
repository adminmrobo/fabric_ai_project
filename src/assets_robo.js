/* ---------- 부직이 수정·보완 요청 ---------- */
var PG=LAB.page||{file:'',title:''};
var RK=[['fix','내용 수정','어느 부분을 어떻게 바꿀지 적어 주세요. 예: "27개 → 29개로"'],
 ['add','내용 추가','무엇을 더 넣을지 적어 주세요. 예: "부직포 사례 하나 더"'],
 ['cut','줄이기·삭제','빼거나 줄일 부분을 적어 주세요.'],
 ['num','숫자·근거 확인','확인할 숫자나 출처를 적어 주세요.'],
 ['easy','더 쉽게','어려운 말이나 문장을 적어 주세요.'],
 ['fig','그림·표 추가','어떤 그림·표가 있으면 좋을지 적어 주세요.'],
 ['term','용어·표기 통일','바꿀 용어와 바꿀 말을 적어 주세요. 예: "태 → 촉감(태)"'],
 ['ask','질문','궁금한 점을 적어 주세요. 다음 보고에서 답하겠습니다.']];
var RKM={};RK.forEach(function(k){RKM[k[0]]=k});
var RP=[['now','다음 보고 전'],['week','이번 주 안'],['later','나중에']];var RPM={};RP.forEach(function(k){RPM[k[0]]=k[1]});
var QUICK={fix:['○○을 △△로 바꿔 주세요.','이 결론이 근거와 맞지 않습니다.','날짜를 고쳐 주세요.'],
 add:['예시를 하나 더 넣어 주세요.','실제 측정 사진을 넣어 주세요.','관련 문헌을 붙여 주세요.'],
 cut:['이 단락은 빼도 됩니다.','반으로 줄여 주세요.','부록으로 옮겨 주세요.'],
 num:['이 숫자의 출처를 밝혀 주세요.','계산을 다시 확인해 주세요.','단위를 확인해 주세요.'],
 easy:['비전공자도 알게 풀어 주세요.','비유를 바꿔 주세요.','약어를 풀어 써 주세요.'],
 fig:['흐름을 그림 한 장으로 보여 주세요.','표로 정리해 주세요.','전후 비교 그림이 필요합니다.'],
 term:['연구실에서 쓰는 말로 바꿔 주세요.','영어 원어를 함께 적어 주세요.'],
 ask:['이 방법을 고른 이유는?','다른 방법과 비교하면?','언제까지 가능한가?']};
function rqAll(){var m=ST.get();if(!m.req)m.req=[];if(!m.rqn)m.rqn=0;return m.req;}
function rqSave(){ST.save();if(HOOK.reqSum)HOOK.reqSum();}
function robo(mood){return SPRITE['robo_'+mood]||SPRITE.robo_smile||''}
var RQ={sec:'',kind:'',pri:'now',quote:''};
if($('#roboReq')){
  var secs=[];$$('section.level h2, section.level h1').forEach(function(h){if(h.closest('#robo,#reqs,#kg,#export'))return;var t=h.textContent.replace(/\s+/g,' ').trim();if(t&&secs.indexOf(t)<0)secs.push(t)});
  secs.unshift('이 쪽 전체');
  function chips(id,list,cur,cls){return list.map(function(x){var v=x[0],l=x[1];return '<button type="button" class="bt rqc '+(cls||'')+'" data-g="'+id+'" data-v="'+esc(v)+'" aria-pressed="'+(cur===v)+'">'+esc(l)+'</button>'}).join('')}
  function paintRQ(){
    $('#rqSec').innerHTML=chips('sec',secs.map(function(s){return [s,s.length>26?s.slice(0,25)+'…':s]}),RQ.sec);
    $('#rqKind').innerHTML=chips('kind',RK,RQ.kind);
    $('#rqPri').innerHTML=chips('pri',RP,RQ.pri);
    var k=RQ.kind||'fix';$('#rqMemo').placeholder=RKM[k][2];
    $('#rqQuick').innerHTML=(QUICK[k]||[]).map(function(q){return '<button type="button" class="bt sm" data-q="'+esc(q)+'">+ '+esc(q)+'</button>'}).join('');
    $('#rqQuote').innerHTML=RQ.quote?'<blockquote>“'+esc(RQ.quote)+'”</blockquote><button type="button" class="bt sm" id="rqQx">인용 지우기</button>':'<span class="small muted">본문에서 글을 드래그해 고른 뒤 아래 단추를 누르면, 고칠 문장이 그대로 들어갑니다.</span>';
    var ok=RQ.sec&&RQ.kind;$('#rqGo').disabled=!ok;$('#rqHint').textContent=ok?'준비 완료 — 메모는 비워 두셔도 됩니다.':'①어디를 ②무엇을 고르시면 접수할 수 있습니다.';
    pageList();}
  $('#roboReq').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;
    if(b.dataset.g){RQ[b.dataset.g]=RQ[b.dataset.g]===b.dataset.v&&b.dataset.g!=='pri'?'':b.dataset.v;paintRQ();if(b.dataset.g==='kind')$('#rqMemo').focus();return;}
    if(b.dataset.q){var m=$('#rqMemo');m.value=(m.value?m.value.replace(/\s*$/,' '):'')+b.dataset.q;m.focus();return;}
    if(b.id==='rqQx'){RQ.quote='';paintRQ();return;}
    if(b.dataset.del){var L=rqAll(),i=L.findIndex(function(r){return r.id===b.dataset.del});if(i>=0)L.splice(i,1);rqSave();pageList();return;}
    if(b.dataset.done){var r=rqAll().find(function(r){return r.id===b.dataset.done});if(r){r.st=r.st==='done'?'open':'done';rqSave();pageList();}return;}});
  var lastSel='';document.addEventListener('selectionchange',function(){var s=String(window.getSelection()||'').trim();if(s&&!(document.activeElement&&document.activeElement.id==='rqMemo'))lastSel=s.slice(0,300);});
  $('#rqGrab').addEventListener('mousedown',function(e){e.preventDefault()});
  $('#rqGrab').addEventListener('click',function(){var s=String(window.getSelection()||'').trim()||lastSel;
    if(!s){roboSay('meh','먼저 본문에서 고칠 문장을 드래그해 골라 주세요.');return;}
    RQ.quote=s.slice(0,300);var n=window.getSelection().anchorNode;var sec=n&&(n.nodeType===1?n:n.parentElement);sec=sec&&sec.closest('section.level');
    if(sec&&!RQ.sec){var h=sec.querySelector('h2,h1');if(h){var t=h.textContent.replace(/\s+/g,' ').trim();if(secs.indexOf(t)>=0)RQ.sec=t;}}
    paintRQ();roboSay('calc','인용을 넣었습니다. 무엇을 할지만 골라 주세요.');});
  $('#rqGo').addEventListener('click',function(){var m=ST.get();rqAll();m.rqn=(m.rqn||0)+1;var id='R-'+String(m.rqn).padStart(3,'0');
    m.req.push({id:id,page:PG.file,ptitle:PG.title,sec:RQ.sec,kind:RQ.kind,pri:RQ.pri,quote:RQ.quote,memo:$('#rqMemo').value.trim(),ts:new Date().toLocaleString('sv-SE').slice(0,16),st:'open'});
    rqSave();var here=m.req.filter(function(r){return r.page===PG.file}).length,open=m.req.filter(function(r){return r.st!=='done'}).length;
    roboSay('happy','요청 '+id+' 접수! 이 쪽 '+here+'건, 전체 남은 요청 '+open+'건입니다. 계산 끝.');
    RQ.kind='';RQ.quote='';$('#rqMemo').value='';paintRQ();});
  $('#rqReset').addEventListener('click',function(){RQ={sec:'',kind:'',pri:'now',quote:''};$('#rqMemo').value='';paintRQ();});
  $('#rqMemo').addEventListener('keydown',function(e){if((e.ctrlKey||e.metaKey)&&e.key==='Enter'&&!$('#rqGo').disabled)$('#rqGo').click();});
  function roboSay(mood,t){$('#rqSay').textContent=t;var i=$('#rqFace');if(i)i.src=robo(mood);}
  function pageList(){var L=rqAll().filter(function(r){return r.page===PG.file});$('#rqN').textContent=L.length;
    $('#rqList').innerHTML=L.length?L.map(function(r){return '<li class="'+(r.st==='done'?'done':'')+'"><b>'+r.id+'</b> <span class="st '+(r.st==='done'?'done':'draft')+'">'+(r.st==='done'?'반영 완료':RPM[r.pri])+'</span> '+esc(RKM[r.kind][1])+' · <span class="muted">'+esc(r.sec)+'</span>'+(r.quote?'<br><span class="small muted">“'+esc(r.quote.slice(0,80))+(r.quote.length>80?'…':'')+'”</span>':'')+(r.memo?'<br>'+esc(r.memo):'')+
      '<span class="rqb"><button type="button" class="bt sm" data-done="'+r.id+'">'+(r.st==='done'?'되돌리기':'반영 완료')+'</button><button type="button" class="bt sm" data-del="'+r.id+'">삭제</button></span></li>'}).join(''):'<li class="muted">이 쪽에는 아직 요청이 없습니다.</li>';}
  /* 섹션마다 작은 요청 단추 */
  $$('section.level h2').forEach(function(h){if(h.closest('#robo,#reqs'))return;var t=h.textContent.replace(/\s+/g,' ').trim();
    var b=document.createElement('button');b.type='button';b.className='rqpin';b.title='이 부분 수정·보완 요청';b.setAttribute('aria-label',t+' — 부직이에게 수정 요청');b.innerHTML='<img alt="" src="'+robo('calc')+'">요청';
    b.addEventListener('click',function(){RQ.sec=t;paintRQ();$('#robo').scrollIntoView({behavior:reduce?'auto':'smooth'});setTimeout(function(){var f=$('#rqKind button');if(f)f.focus({preventScroll:true})},400);roboSay('calc','"'+(t.length>30?t.slice(0,29)+'…':t)+'" 부분이군요. 무엇을 할지 골라 주세요.');});
    h.appendChild(b);});
  var fab=$('#roboFab');if(fab){fab.querySelector('img').src=robo('smile');fab.addEventListener('click',function(){$('#robo').scrollIntoView({behavior:reduce?'auto':'smooth'})});}
  var fi=$('#rqFace');if(fi)fi.src=robo('calc');
  paintRQ();
}
/* INDEX: 요청 모음 */
if($('#reqT')){
  var RF='open';
  HOOK.reqSum=function(){var L=rqAll(),open=L.filter(function(r){return r.st!=='done'}),now=open.filter(function(r){return r.pri==='now'});
    $('#reqK').innerHTML='<div class="kpi i"><b>'+L.length+'</b><span>전체 요청</span></div><div class="kpi a"><b>'+open.length+'</b><span>남은 요청</span></div><div class="kpi r"><b>'+now.length+'</b><span>다음 보고 전</span></div><div class="kpi g"><b>'+(L.length-open.length)+'</b><span>반영 완료</span></div>';
    var S=RF==='all'?L:RF==='done'?L.filter(function(r){return r.st==='done'}):open;
    S=S.slice().sort(function(a,b){var o={now:0,week:1,later:2};return (o[a.pri]-o[b.pri])||a.id.localeCompare(b.id)});
    $('#reqT').innerHTML=S.length?'<table class="tb"><tr><th>번호</th><th>쪽 · 위치</th><th>유형</th><th>기한</th><th>내용</th><th>상태</th></tr>'+S.map(function(r){return '<tr><td style="white-space:nowrap">'+r.id+'</td><td><a href="'+r.page+'#robo">'+esc(r.ptitle)+'</a><br><span class="small muted">'+esc(r.sec)+'</span></td><td>'+esc(RKM[r.kind][1])+'</td><td>'+RPM[r.pri]+'</td><td>'+(r.quote?'<span class="small muted">“'+esc(r.quote)+'”</span><br>':'')+esc(r.memo||'—')+'</td><td><button type="button" class="bt sm" data-rdone="'+r.id+'">'+(r.st==='done'?'반영 완료 ✓':'미처리')+'</button></td></tr>'}).join('')+'</table>':'<p class="muted">표시할 요청이 없습니다. 각 쪽 아래 부직이 칸이나 제목 옆 "요청" 단추로 남기실 수 있습니다.</p>';
    $('#reqSay').textContent=L.length?'남은 요청 '+open.length+'건 중 다음 보고 전까지 '+now.length+'건입니다. 반영하면 상태를 눌러 바꿔 주세요.':'아직 접수된 요청이 없습니다. 제목 옆 "요청" 단추를 누르면 바로 시작됩니다.';
    var f=$('#roboFace2');if(f)f.src=robo(open.length?'chart':'smile');};
  $('#reqs').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;
    if(b.dataset.rf){RF=b.dataset.rf;$$('#reqs [data-rf]').forEach(function(x){x.setAttribute('aria-pressed',x===b)});HOOK.reqSum();}
    if(b.dataset.rdone){var r=rqAll().find(function(r){return r.id===b.dataset.rdone});if(r){r.st=r.st==='done'?'open':'done';rqSave();}}});
  function reqMd(){var L=rqAll(),by={};L.forEach(function(r){(by[r.ptitle]=by[r.ptitle]||[]).push(r)});
    var o=['# 부직이 수정·보완 요청서','','- 문서: 직물 구조로 성능을 미리 맞히는 AI — 연구 계획 브리핑','- 작성: '+new Date().toLocaleDateString('sv-SE')+' · 전체 '+L.length+'건, 남은 '+L.filter(function(r){return r.st!=='done'}).length+'건',''];
    Object.keys(by).forEach(function(k){o.push('## '+k,'');by[k].forEach(function(r){o.push('- ['+(r.st==='done'?'x':' ')+'] **'+r.id+'** ('+RKM[r.kind][1]+' · '+RPM[r.pri]+') — '+r.sec);if(r.quote)o.push('  > '+r.quote.replace(/\n/g,' '));if(r.memo)o.push('  '+r.memo);});o.push('');});return o.join('\n');}
  function reqCsv(){return '﻿'+[['번호','쪽','위치','유형','기한','인용','메모','상태','작성']].concat(rqAll().map(function(r){return [r.id,r.ptitle,r.sec,RKM[r.kind][1],RPM[r.pri],r.quote,r.memo,r.st==='done'?'반영 완료':'미처리',r.ts]})).map(function(row){return row.map(function(c){c=String(c==null?'':c);return /[",\n]/.test(c)?'"'+c.replace(/"/g,'""')+'"':c}).join(',')}).join('\n');}
  $('#reqCopy').addEventListener('click',function(){var t=reqMd(),pre=$('#reqTxt');pre.textContent=t;pre.hidden=false;
    if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(function(){$('#reqMsg').textContent='요청서를 복사했습니다.'},function(){$('#reqMsg').textContent='아래 글을 복사해 주십시오.'});else $('#reqMsg').textContent='아래 글을 복사해 주십시오.';});
  $('#reqMd').addEventListener('click',function(){dlText(reqMd(),'robo_requests.md','text/markdown;charset=utf-8')});
  $('#reqCsv').addEventListener('click',function(){dlText(reqCsv(),'robo_requests.csv','text/csv;charset=utf-8')});
  HOOK.reqSum();
}
/* ---------- 이미지 데이터: 지름길 산점도 ---------- */
if($('#imgSc')&&LAB.img){
  var IM=LAB.img,isc=$('#imgSc'),imode='cls',ithr=14;
  var ICOL={cls:function(d){return d.cls==='soft'?'#13733a':'#c9302c'},color:function(d){return {'navy blue':'#1e3a8a','light gray':'#8a96a3','white':'#c8ccd2','ivory beige':'#c9a76b'}[d.color]||'#555'},
    set:function(d){return d.set==='test'?'#1e55c8':'#c9cfd6'}};
  function drawImg(){var w=fit(isc,340),x=isc.getContext('2d');x.clearRect(0,0,w,340);
    var L=54,R=w-14,T=14,B=300,xm=function(v){return L+(Math.log10(v)-1.4)/(4-1.4)*(R-L)},ym=function(v){return B-(v/52)*(B-T)};
    x.strokeStyle='#d5dbe2';x.fillStyle='#5b6874';x.font='12px sans-serif';x.lineWidth=1;
    [0,10,20,30,40,50].forEach(function(v){x.beginPath();x.moveTo(L,ym(v));x.lineTo(R,ym(v));x.stroke();x.fillText(v,L-24,ym(v)+4)});
    [[30,'30'],[100,'100'],[300,'300'],[1000,'1천'],[3000,'3천'],[10000,'1만']].forEach(function(v){var xx=xm(v[0]);x.beginPath();x.moveTo(xx,T);x.lineTo(xx,B);x.stroke();x.textAlign=v[0]===10000?'right':'center';x.fillText(v[1],xx,B+16);x.textAlign='left'});
    x.fillText('선명도 (라플라시안 분산, 로그 눈금) →',L,B+34);x.save();x.translate(14,B-40);x.rotate(-Math.PI/2);x.fillText('명암 대비 (밝기 표준편차) →',0,0);x.restore();
    x.strokeStyle='#a35c00';x.setLineDash([6,4]);x.lineWidth=2;x.beginPath();x.moveTo(L,ym(ithr));x.lineTo(R,ym(ithr));x.stroke();x.setLineDash([]);
    x.fillStyle='#a35c00';x.fillText('이 선 위 = "거침"으로 찍기 ('+ithr+')',R-190,ym(ithr)-6);
    IM.forEach(function(d){var cx=xm(Math.max(26,d.sharp)),cy=ym(Math.min(51,d.contrast));x.beginPath();
      if(d.set==='test'){x.rect(cx-5,cy-5,10,10)}else x.arc(cx,cy,4.5,0,7);
      x.fillStyle=ICOL[imode](d);x.globalAlpha=.85;x.fill();x.globalAlpha=1;
      var wrong=(d.contrast>ithr)!==(d.cls==='harsh');if(wrong){x.strokeStyle='#16212b';x.lineWidth=1.6;x.stroke();}});
    var tr=IM.filter(function(d){return d.set==='train'}),te=IM.filter(function(d){return d.set==='test'});
    function acc(S){return S.filter(function(d){return (d.contrast>ithr)===(d.cls==='harsh')}).length/S.length}
    $('#imgAcc').innerHTML='<div class="kpi a"><b>'+Math.round(acc(tr)*100)+'%</b><span>학습 120장 정답률</span></div><div class="kpi r"><b>'+Math.round(acc(te)*100)+'%</b><span>시험 20장 정답률</span></div><div class="kpi i"><b>1개</b><span>쓴 정보: 명암 대비</span></div>';
    $('#imgLeg').innerHTML=imode==='cls'?'<span style="color:#13733a">●</span> 부드러움 <span style="color:#c9302c">●</span> 거침 · ■ 시험 세트 · 테두리 = 이 규칙이 틀린 사진':imode==='color'?'<span style="color:#1e3a8a">●</span> 남색 <span style="color:#8a96a3">●</span> 연회색 <span style="color:#b8bcc2">●</span> 흰색 <span style="color:#c9a76b">●</span> 아이보리':'<span style="color:#1e55c8">■</span> 시험 20장 <span style="color:#c9cfd6">●</span> 학습 120장';}
  $$('[data-im]').forEach(function(b){b.addEventListener('click',function(){imode=b.dataset.im;$$('[data-im]').forEach(function(x){x.setAttribute('aria-pressed',x===b)});drawImg()})});
  $('#imgThr').addEventListener('input',function(){ithr=+this.value;$('#imgThrV').textContent=ithr;drawImg()});
  RD.push(drawImg);
}
/* ---------- 작성 가이드: 점검표와 양식 내려받기 ---------- */
if($('#ckList')){
  function ckPaint(){var C=ST.get().ck||{};var bs=$$('#ckList button');bs.forEach(function(b){var on=!!C[b.dataset.ck];b.setAttribute('aria-pressed',on);b.querySelector('.bx').textContent=on?'✓':''});
    $('#ckN').textContent=bs.filter(function(b){return C[b.dataset.ck]}).length+' / '+bs.length;}
  $$('#ckList button').forEach(function(b){b.addEventListener('click',function(){var m=ST.get();m.ck=m.ck||{};m.ck[b.dataset.ck]=!m.ck[b.dataset.ck];ST.save();ckPaint()})});ckPaint();
}
if(LAB.guide){
  function csvRow(a){return a.map(function(c){c=String(c==null?'':c);return /[",\n]/.test(c)?'"'+c.replace(/"/g,'""')+'"':c}).join(',')}
  $$('[data-tpl]').forEach(function(b){b.addEventListener('click',function(){var k=b.dataset.tpl,G=LAB.guide[k];if(!G)return;
    if(G.kind==='header')dlText('﻿'+csvRow(G.cols)+'\n'+(G.example?csvRow(G.example)+'\n':''),G.file,'text/csv;charset=utf-8');
    else if(G.kind==='dict')dlText('﻿'+[csvRow(G.head)].concat(G.rows.map(csvRow)).join('\n'),G.file,'text/csv;charset=utf-8');
    else dlText(G.text,G.file,'text/markdown;charset=utf-8');});});
}
/* ---------- SUMMARY: 직물 사진 → 확대 → 숫자 격자 → 벡터, 1층 필터 ---------- */
if($('#smA')&&LAB.sm){
  var SM=LAB.sm,si=0,zx=.5,zy=.5,ZR=.2,imgs=[],nready=0,smV=[];
  var KN=[['가로결',[-1,-2,-1,0,0,0,1,2,1],'#1e55c8'],['세로결',[-1,0,1,-2,0,2,-1,0,1],'#13733a'],['사선결 ↗',[0,1,2,-1,0,1,-2,-1,0],'#a35c00'],['사선결 ↘',[-2,-1,0,-1,0,1,0,1,2],'#8e3fb0']];
  var VN=KN.map(function(k){return k[0]+' 세기'}).concat(['밝기','명암 대비']);
  function grid(i,cx,cy,r,n){var c=document.createElement('canvas');c.width=c.height=n;var x=c.getContext('2d',{willReadFrequently:true});x.imageSmoothingEnabled=true;x.imageSmoothingQuality='high';
    var W=imgs[i].naturalWidth,s=r*W;x.drawImage(imgs[i],(cx-r/2)*W,(cy-r/2)*W,s,s,0,0,n,n);var d=x.getImageData(0,0,n,n).data,g=new Array(n*n);
    for(var k=0;k<n*n;k++)g[k]=(0.299*d[4*k]+0.587*d[4*k+1]+0.114*d[4*k+2])/255;return g;}
  function conv(g,n,K){var m=n-2,o=new Float32Array(m*m);for(var y=1;y<n-1;y++)for(var x=1;x<n-1;x++){var s=0,t=0;for(var dy=-1;dy<=1;dy++)for(var dx=-1;dx<=1;dx++){s+=K[t++]*g[(y+dy)*n+x+dx]}o[(y-1)*m+x-1]=Math.abs(s)}return o;}
  function feat(g,n){var v=KN.map(function(k){var o=conv(g,n,k[1]),s=0;for(var i=0;i<o.length;i++)s+=o[i];return s/o.length});
    var mu=0;g.forEach(function(a){mu+=a});mu/=g.length;var sd=0;g.forEach(function(a){sd+=(a-mu)*(a-mu)});sd=Math.sqrt(sd/g.length);return v.concat([mu,sd]);}
  function cv(id){var c=$(id);return [c,c.getContext('2d')]}
  function smDraw(){if(!imgs[si]||!imgs[si].complete)return;
    var A=cv('#smA'),W=A[0].width;A[1].drawImage(imgs[si],0,0,W,W);A[1].strokeStyle='#ffd400';A[1].lineWidth=3;A[1].strokeRect((zx-ZR/2)*W,(zy-ZR/2)*W,ZR*W,ZR*W);A[1].strokeStyle='#16212b';A[1].lineWidth=1;A[1].strokeRect((zx-ZR/2)*W-2,(zy-ZR/2)*W-2,ZR*W+4,ZR*W+4);
    var B=cv('#smB'),N=imgs[si].naturalWidth;B[1].imageSmoothingEnabled=true;B[1].drawImage(imgs[si],(zx-ZR/2)*N,(zy-ZR/2)*N,ZR*N,ZR*N,0,0,B[0].width,B[0].width);
    var g=grid(si,zx,zy,ZR,8),C=cv('#smC'),cw=C[0].width/8;C[1].font='600 '+Math.round(cw*.3)+'px sans-serif';C[1].textAlign='center';C[1].textBaseline='middle';
    for(var k=0;k<64;k++){var v=g[k],x=(k%8)*cw,y=Math.floor(k/8)*cw,L=Math.round(v*255);C[1].fillStyle='rgb('+L+','+L+','+L+')';C[1].fillRect(x,y,cw,cw);C[1].strokeStyle='rgba(30,85,200,.35)';C[1].strokeRect(x+.5,y+.5,cw-1,cw-1);C[1].fillStyle=v>.55?'#16212b':'#ffffff';C[1].fillText(v.toFixed(2).slice(1),x+cw/2,y+cw/2);}
    $('#smVecTxt').textContent='[ '+g.slice(0,10).map(function(a){return a.toFixed(2)}).join(', ')+', … ]  ← 숫자 64개';
    var D=cv('#smD'),dw=D[0].width,dh=D[0].height,bw=dw/64;D[1].clearRect(0,0,dw,dh);for(k=0;k<64;k++){var h=g[k]*(dh-14);D[1].fillStyle=Math.floor(k/8)%2?'#1e55c8':'#6f97e6';D[1].fillRect(k*bw+.5,dh-12-h,bw-1,h)}
    D[1].fillStyle='#5b6874';D[1].font='11px sans-serif';D[1].textAlign='left';D[1].fillText('1번 줄',0,dh-1);D[1].textAlign='right';D[1].fillText('8번 줄',dw,dh-1);
    /* 2부: 1층 필터 */
    var n=40,gg=grid(si,zx,zy,ZR,n),I=cv('#smIn'),iw=I[0].width,p=iw/n;for(k=0;k<n*n;k++){L=Math.round(gg[k]*255);I[1].fillStyle='rgb('+L+','+L+','+L+')';I[1].fillRect((k%n)*p,Math.floor(k/n)*p,p+.5,p+.5)}
    KN.forEach(function(K,j){var o=conv(gg,n,K[1]),m=n-2,mx=0;for(var i=0;i<o.length;i++)if(o[i]>mx)mx=o[i];var F=cv('#smF'+j),fw=F[0].width,q=fw/m,rgb=K[2].match(/\w\w/g).map(function(h){return parseInt(h,16)});
      F[1].fillStyle='#fff';F[1].fillRect(0,0,fw,fw);for(i=0;i<o.length;i++){var a=mx?o[i]/mx:0;F[1].fillStyle='rgba('+rgb.join(',')+','+a.toFixed(3)+')';F[1].fillRect((i%m)*q,Math.floor(i/m)*q,q+.5,q+.5)}});
    var v6=feat(gg,n);smBars(v6);
    $('#smSay').textContent='고른 곳 숫자 64개 중 가장 밝은 칸 '+Math.max.apply(null,g).toFixed(2)+', 가장 어두운 칸 '+Math.min.apply(null,g).toFixed(2)+'. 사진 원본(1254 × 1254 화소 × 3색)은 숫자 4,717,548개입니다.';}
  function smBars(v){var m4=Math.max(v[0],v[1],v[2],v[3])||1,mx=[m4,m4,m4,m4,1,0.25];
    $('#smVec').innerHTML=v.map(function(a,i){var c=i<4?KN[i][2]:'#5b6874';return '<span>'+VN[i]+'</span><div class="track"><div class="fill" style="left:0;width:'+(mx[i]?a/mx[i]*100:0).toFixed(1)+'%;background:'+c+'"></div></div><b class="num">'+a.toFixed(3)+'</b>'}).join('');}
  function smAll(){smV=SM.map(function(o,i){return feat(grid(i,.5,.5,1,96),96)});
    var mu=[],sd=[];for(var j=0;j<6;j++){var c=smV.map(function(r){return r[j]}),m=c.reduce(function(a,b){return a+b})/c.length;mu[j]=m;sd[j]=Math.sqrt(c.reduce(function(a,b){return a+(b-m)*(b-m)},0)/c.length)||1}
    var Z=smV.map(function(r){return r.map(function(a,j){return (a-mu[j])/sd[j]})});
    function dist(a,b){var s=0;for(var j=0;j<6;j++)s+=(Z[a][j]-Z[b][j])*(Z[a][j]-Z[b][j]);return Math.sqrt(s)}
    var h='<table class="tb"><tr><th>원단 (사진 전체)</th>'+VN.map(function(n){return '<th>'+n+'</th>'}).join('')+'<th>가장 가까운 원단</th></tr>';
    SM.forEach(function(o,i){var best=-1,bd=1e9;SM.forEach(function(_,k){if(k!==i){var d=dist(i,k);if(d<bd){bd=d;best=k}}});
      h+='<tr><td><b>'+esc(o.label)+'</b></td>'+smV[i].map(function(a){return '<td class="num">'+a.toFixed(3)+'</td>'}).join('')+'<td>'+esc(SM[best].label)+' <span class="small muted">(거리 '+bd.toFixed(2)+')</span></td></tr>'});
    $('#smTab').innerHTML=h+'</table>';smDraw();}
  SM.forEach(function(o,i){var im=new Image();im.onload=function(){nready++;if(nready===SM.length)smAll();else if(i===si)smDraw();};im.src=o.src;imgs[i]=im;});
  $('#smPick').innerHTML=SM.map(function(o,i){return '<button type="button" class="bt" data-sm="'+i+'" aria-pressed="'+(i===si)+'">'+esc(o.label)+'</button>'}).join('');
  $('#smPick').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;si=+b.dataset.sm;zx=zy=.5;$$('#smPick button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});smDraw();});
  function clampZ(){zx=Math.max(ZR/2,Math.min(1-ZR/2,zx));zy=Math.max(ZR/2,Math.min(1-ZR/2,zy));}
  $('#smA').addEventListener('click',function(e){var r=this.getBoundingClientRect();zx=(e.clientX-r.left)/r.width;zy=(e.clientY-r.top)/r.height;clampZ();smDraw();});
  $$('[data-smv]').forEach(function(b){b.addEventListener('click',function(){var d=b.dataset.smv;if(d==='l')zx-=.08;if(d==='r')zx+=.08;if(d==='u')zy-=.08;if(d==='d')zy+=.08;clampZ();smDraw();})});
  $('#smZoom').addEventListener('input',function(){ZR=+this.value/100;$('#smZoomV').textContent=Math.round(1/ZR*10)/10+'배';clampZ();smDraw();});
}
