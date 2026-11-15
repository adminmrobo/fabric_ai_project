/* 설명용 모형 두 개: 과적합(원단 수 vs 변수 수), 데이터 누수(반복 측정 나누기) */
function rng(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);
  t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function gauss(r){var u=0;while(!u)u=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*r())}
function solve(A,b){var n=b.length,M=A.map(function(r,i){return r.concat([b[i]])});
  for(var c=0;c<n;c++){var p=c;for(var r=c+1;r<n;r++)if(Math.abs(M[r][c])>Math.abs(M[p][c]))p=r;
    var t=M[c];M[c]=M[p];M[p]=t;var d=M[c][c]||1e-12;
    for(var r2=c+1;r2<n;r2++){var f=M[r2][c]/d;if(!f)continue;for(var k=c;k<=n;k++)M[r2][k]-=f*M[c][k];}}
  var x=new Array(n).fill(0);for(var i=n-1;i>=0;i--){var s=M[i][n];for(var j=i+1;j<n;j++)s-=M[i][j]*x[j];x[i]=s/(M[i][i]||1e-12);}return x;}
function ridgeFit(X,y,lam){var n=X.length,p=X[0].length,mx=new Array(p).fill(0),my=0;
  X.forEach(function(r){r.forEach(function(v,j){mx[j]+=v/n})});y.forEach(function(v){my+=v/n});
  var A=[],b=new Array(p).fill(0);for(var i=0;i<p;i++){A.push(new Array(p).fill(0));A[i][i]=lam;}
  for(var r=0;r<n;r++){var xr=X[r].map(function(v,j){return v-mx[j]}),yr=y[r]-my;
    for(var i2=0;i2<p;i2++){b[i2]+=xr[i2]*yr;for(var j2=0;j2<p;j2++)A[i2][j2]+=xr[i2]*xr[j2];}}
  var w=solve(A,b);return function(x){var s=my;for(var j=0;j<p;j++)s+=w[j]*(x[j]-mx[j]);return s;};}
function r2(y,yh){var m=0;y.forEach(function(v){m+=v/y.length});var sse=0,sst=0;
  y.forEach(function(v,i){sse+=(v-yh[i])*(v-yh[i]);sst+=(v-m)*(v-m)});return 1-sse/sst;}
/* ① 과적합: 진짜로 중요한 변수는 5개, 진짜 설명력 R² = 0.70 */
var BETA=[1,0.8,0.6,0.4,0.3];
function overfit(n,p,seed){var reps=4,tr=0,cv=0;
  for(var rep=0;rep<reps;rep++){var r=rng((seed||11)+rep*101),X=[],y=[];
    for(var i=0;i<n;i++){var row=[];for(var j=0;j<p;j++)row.push(gauss(r));X.push(row);
      var s=0;for(var k=0;k<5&&k<p;k++)s+=BETA[k]*row[k];
      /* p<5이면 빠진 중요 변수의 몫은 잡음이 된다 */
      for(var k2=p;k2<5;k2++)s+=BETA[k2]*gauss(r);
      y.push(s+0.982*gauss(r));}
    var f=ridgeFit(X,y,1e-3);tr+=r2(y,X.map(f))/reps;
    var idx=X.map(function(_,i){return i}),r3=rng(seed+7+rep);
    for(var i2=idx.length-1;i2>0;i2--){var j2=Math.floor(r3()*(i2+1)),t=idx[i2];idx[i2]=idx[j2];idx[j2]=t;}
    var pred=new Array(n);for(var fo=0;fo<5;fo++){var te=idx.filter(function(_,q){return q%5===fo}),
      trn=idx.filter(function(_,q){return q%5!==fo});
      var g=ridgeFit(trn.map(function(q){return X[q]}),trn.map(function(q){return y[q]}),1e-3);
      te.forEach(function(q){pred[q]=g(X[q])});}
    cv+=Math.max(-1,r2(y,pred))/reps;}
  return {train:tr,cv:cv,truth:0.70};}
/* ② 데이터 누수: 원단 30개 × 반복 측정 3번, 이웃 2개로 예측 */
function leak(seed){var r=rng(seed||5),F=[],rows=[];
  for(var f=0;f<30;f++){var a=[gauss(r),gauss(r),gauss(r)],yt=0.8*a[0]+0.6*gauss(r);F.push({a:a,y:yt});
    for(var k=0;k<3;k++)rows.push({fab:f,x:a.map(function(v){return v+0.15*gauss(r)}),y:yt+0.15*gauss(r)});}
  function knn(train,x){var d=train.map(function(t){var s=0;for(var j=0;j<3;j++)s+=(t.x[j]-x[j])*(t.x[j]-x[j]);return {d:s,y:t.y}});
    d.sort(function(a,b){return a.d-b.d});return (d[0].y+d[1].y)/2;}
  function cvBy(key){var pred=[],r4=rng(99),ord=[];
    var groups=key==='row'?rows.map(function(_,i){return i}):F.map(function(_,i){return i});
    for(var i=groups.length-1;i>0;i--){var j=Math.floor(r4()*(i+1)),t=groups[i];groups[i]=groups[j];groups[j]=t;}
    var fold={};groups.forEach(function(g,q){fold[g]=q%5});
    rows.forEach(function(row,i){var fo=key==='row'?fold[i]:fold[row.fab];
      var train=rows.filter(function(rr,i2){return (key==='row'?fold[i2]:fold[rr.fab])!==fo});pred[i]=knn(train,row.x);});
    return r2(rows.map(function(x){return x.y}),pred);}
  var out={random:cvBy('row'),byFabric:cvBy('fab')};
  out.folds=function(key){var r4=rng(99),groups=key==='row'?rows.map(function(_,i){return i}):F.map(function(_,i){return i});
    for(var i=groups.length-1;i>0;i--){var j=Math.floor(r4()*(i+1)),t=groups[i];groups[i]=groups[j];groups[j]=t;}
    var fold={};groups.forEach(function(g,q){fold[g]=q%5});return rows.map(function(row,i){return key==='row'?fold[i]:fold[row.fab]});};
  out.rows=rows;return out;}
if(typeof module!=='undefined')module.exports={overfit:overfit,leak:leak,rng:rng};
