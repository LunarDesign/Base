#!/usr/bin/env python3
"""
Chunk 31 — Ph1 Cardiovascular remaining (5 charts × 3 levels = 15 cards)
Charts: PA catheter waveform, MAP isolines, cardiac cycle, aortic dissection, shock progression
Run: python chunk31_charts.py
"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card, SHARED_JS, CHART_CSS_ADDON, DID)
from card_validator import CardValidator

DECK_PATH  = 'CCRN_PCCN_Mastery_v7_final_30.apkg'
OUT_PATH   = 'CCRN_PCCN_Mastery_v7_final_31.apkg'
WORK_DIR   = os.path.join(tempfile.gettempdir(), 'c31')
CHUNK_NUM  = 31
MID_BASE   = 1_800_005_000
CHART_ORDER = ['pacatheter','mapisoline','cardiaccycle','aorticdissect','shockprogress']

RF = {}

# ── 1. PA Catheter Waveform ──────────────────────────────────────────────────
RF['pacatheter'] = r"""
function _render(cv,ctrl,P){
  var W=cv.width,H=cv.height,ctx=cv.getContext('2d');if(!ctx)return;
  var mx=54,my=16,pw=W-mx-14,ph=H-my-52,yMin=0,yMax=40,yRange=yMax-yMin;
  function toX(t){return mx+(t/1)*pw;}
  function toY(p){return my+ph-((p-yMin)/yRange)*ph;}
  var mode=P.mode||'normal';
  var PHASES={
    ra:{label:'RA',color:'#29b6f6',range:[0,0.22],
      pts:[[0,6],[0.04,10],[0.07,6],[0.10,4],[0.14,8],[0.17,5],[0.20,4],[0.22,5]]},
    rv:{label:'RV',color:'#ff7043',range:[0.22,0.45],
      pts:[[0.22,5],[0.24,5],[0.26,30],[0.30,32],[0.34,28],[0.38,8],[0.41,4],[0.45,5]]},
    pa:{label:'PA',color:'#4caf50',range:[0.45,0.70],
      pts:[[0.45,5],[0.47,5],[0.50,28],[0.54,30],[0.57,22],[0.61,14],[0.65,12],[0.70,14]]},
    pawp:{label:'PAWP',color:'#ffca28',range:[0.70,1.00],
      pts:[[0.70,14],[0.72,16],[0.75,12],[0.78,10],[0.82,14],[0.86,12],[0.90,10],[0.95,11],[1.00,11]]},
  };
  var active=P.phase||'all';
  function draw(){
    _cl(ctx,W,H);_gd(ctx,mx,my,pw,ph,0.1,1,5,40);
    ctx.strokeStyle='#666';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(mx,my);ctx.lineTo(mx,my+ph);ctx.lineTo(mx+pw,my+ph);ctx.stroke();
    ctx.textAlign='right';
    [0,5,10,15,20,25,30,35,40].forEach(function(v){_lb(ctx,v,mx-6,toY(v)+4,null,10,'right');});
    _lb(ctx,'Pressure (mmHg)',mx+pw/2,H-5,null,11);
    // Phase dividers
    Object.entries(PHASES).forEach(function(e){
      var key=e[0],ph2=e[1];
      if(active!=='all'&&active!==key)return;
      // Background shade
      ctx.fillStyle=ph2.color+'11';
      ctx.fillRect(toX(ph2.range[0]),my,toX(ph2.range[1])-toX(ph2.range[0]),H-my-52);
      // Waveform
      ctx.strokeStyle=ph2.color;ctx.lineWidth=2.5;ctx.beginPath();
      ph2.pts.forEach(function(p,i){var x=toX(p[0]),y=toY(p[1]);
        if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);});
      ctx.stroke();
      // Label
      var midT=(ph2.range[0]+ph2.range[1])/2;
      _lb(ctx,ph2.label,toX(midT),my+10,ph2.color,12);
      // Normal range label
      var pressureRange=key==='ra'?'2-8':key==='rv'?'15-30/0-8':key==='pa'?'15-30/6-12':'6-12';
      _lb(ctx,pressureRange+' mmHg',toX(midT),my+22,ph2.color+'aa',9);});}
  draw();
  if(ctrl){ctrl.innerHTML='';var row=document.createElement('div');
    row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;align-items:center;';
    var sp=document.createElement('span');sp.textContent='CHAMBER: ';
    sp.style.cssText='font-size:10px;font-weight:800;color:#444;';row.appendChild(sp);
    [['all','Full Pass','#888']].concat(Object.entries(PHASES).map(function(e){return [e[0],e[1].label,e[1].color];}))
    .forEach(function(item){
      var b=_mkB(item[1],item[2],active===item[0],function(on){if(!on)return;active=item[0];
        row.querySelectorAll('button').forEach(function(btn){btn.style.background='transparent';btn.style.color='#555';btn._on=false;});
        b.style.background=item[2]+'22';b.style.color=item[2];b._on=true;draw();});
      row.appendChild(b);});ctrl.appendChild(row);}}
"""

# ── 2. MAP Isoline Chart ─────────────────────────────────────────────────────
RF['mapisoline'] = r"""
function _render(cv,ctrl,P){
  var W=cv.width,H=cv.height,ctx=cv.getContext('2d');if(!ctx)return;
  var mx=58,my=16,pw=W-mx-14,ph=H-my-52,xD=12,yD=3000;
  function toX(co){return mx+(co/xD)*pw;}
  function toY(svr){return my+ph-(svr/yD)*ph;}
  var targetMAP=P.map||65;
  var MAPS=[45,55,65,75,90,110];
  var mapColors={45:'#ef535088',55:'#ef535055',65:'#4caf5088',75:'#29b6f655',90:'#ff704333',110:'#ff704311'};
  function draw(){
    _cl(ctx,W,H);_gd(ctx,mx,my,pw,ph,2,12,500,3000);
    ctx.strokeStyle='#666';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(mx,my);ctx.lineTo(mx,my+ph);ctx.lineTo(mx+pw,my+ph);ctx.stroke();
    ctx.textAlign='center';
    [0,2,4,6,8,10,12].forEach(function(v){_lb(ctx,v,toX(v),my+ph+15,null,10);});
    ctx.textAlign='right';
    [0,500,1000,1500,2000,2500,3000].forEach(function(v){_lb(ctx,v,mx-6,toY(v)+4,null,10,'right');});
    _lb(ctx,'Cardiac Output (L/min)',mx+pw/2,H-5,null,11);
    _rl(ctx,'SVR (dynes·s/cm⁵)',14,my+ph/2);
    // MAP isolines: MAP = CO × SVR / 80
    MAPS.forEach(function(map){
      ctx.strokeStyle=mapColors[map]||'#33333388';
      ctx.lineWidth=map===targetMAP?3:1.5;
      ctx.setLineDash(map===targetMAP?[]:[4,3]);
      ctx.beginPath();var first=true;
      for(var co=0.5;co<=12;co+=0.1){
        var svr=map*80/co;if(svr<100||svr>3000){first=true;continue;}
        if(first){ctx.moveTo(toX(co),toY(svr));first=false;}else ctx.lineTo(toX(co),toY(svr));}
      ctx.stroke();ctx.setLineDash([]);
      var labelCO=6,labelSVR=map*80/6;
      if(labelSVR>200&&labelSVR<2800)
        _lb(ctx,'MAP '+map,toX(labelCO)+8,toY(labelSVR)-5,map===targetMAP?'#4caf50':'#444',9,'left');});
    // Normal zone
    ctx.fillStyle='rgba(41,182,246,0.06)';ctx.fillRect(toX(3.5),toY(1700),(toX(7.5)-toX(3.5)),(toY(600)-toY(1700)));
    _lb(ctx,'Normal zone',toX(5.5),toY(1150),'rgba(41,182,246,0.3)',9);}
  draw();
  if(ctrl){ctrl.innerHTML='';var row=document.createElement('div');
    row.style.cssText='display:flex;flex-wrap:wrap;gap:12px;margin-top:8px;';
    row.appendChild(_mkS('Target MAP','40','120','5',targetMAP,function(v){return v+' mmHg';},function(v){targetMAP=v;P.map=v;draw();}));
    ctrl.appendChild(row);}}
"""

# ── 3. Cardiac Cycle (Wiggers-style) ────────────────────────────────────────
RF['cardiaccycle'] = r"""
function _render(cv,ctrl,P){
  var W=cv.width,H=cv.height,ctx=cv.getContext('2d');if(!ctx)return;
  var mx=56,my=16,pw=W-mx-14,ph=H-my-52;
  var showAo=P.aortic!==false,showLV=P.lv!==false,showLA=P.la!==false;
  // Time: 0 to 1 (one cardiac cycle, ~800ms)
  function toX(t){return mx+(t/1)*pw;}
  function toYp(p,pMin,pMax){return my+ph*0.55-((p-pMin)/(pMax-pMin))*ph*0.5;}
  // LV pressure: 0→8(end diastole) → 80(isovolumetric contraction) → 120(peak systole) → 80→12→8
  function lvP(t){
    if(t<0.08)return 8+t/0.08*4;// late diastole fill
    if(t<0.14)return 12+(t-0.08)/0.06*68;// isovolumetric contraction
    if(t<0.18)return 80+(t-0.14)/0.04*42;// rapid ejection
    if(t<0.36)return 122-(t-0.18)/0.18*30;// reduced ejection
    if(t<0.40)return 92-(t-0.36)/0.04*82;// isovolumetric relaxation
    if(t<0.50)return 10-(t-0.40)/0.10*2;// rapid filling
    if(t<0.72)return 8;// diastasis
    if(t<0.80)return 8+(t-0.72)/0.08*4;// atrial contraction
    return 8+(1.0-t)/0.20*4;}
  // Aortic pressure
  function aoP(t){
    if(t<0.18)return 80;// diastolic
    if(t<0.22)return 80+(t-0.18)/0.04*42;// systolic rise
    if(t<0.36)return 122-(t-0.22)/0.14*20;// systolic fall
    if(t<0.38)return 102-(t-0.36)/0.02*16;// dicrotic notch
    if(t<0.40)return 86+(t-0.38)/0.02*4;// post-notch hump
    return 90-(t-0.40)/0.60*10;}// slow diastolic fall
  // LA pressure
  function laP(t){
    if(t<0.12)return 10+(t/0.12)*4;// a wave
    if(t<0.16)return 14-(t-0.12)/0.04*4;// x descent
    if(t<0.30)return 10+(t-0.16)/0.14*8;// c→v wave
    if(t<0.36)return 18-(t-0.30)/0.06*8;// y descent
    return 10;}
  function draw(){
    _cl(ctx,W,H);_gd(ctx,mx,my,pw,ph,0.1,1,20,140);
    ctx.strokeStyle='#666';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(mx,my);ctx.lineTo(mx,my+ph);ctx.lineTo(mx+pw,my+ph);ctx.stroke();
    // Key events (vertical lines)
    [{t:0.14,l:'MV\ncloses'},{t:0.18,l:'AV\nopens'},{t:0.40,l:'AV\ncloses'},{t:0.50,l:'MV\nopens'}].forEach(function(ev){
      ctx.strokeStyle='#2a2a2a';ctx.lineWidth=1;ctx.setLineDash([3,3]);
      ctx.beginPath();ctx.moveTo(toX(ev.t),my);ctx.lineTo(toX(ev.t),my+ph);ctx.stroke();ctx.setLineDash([]);
      ev.l.split('\n').forEach(function(l,li){_lb(ctx,l,toX(ev.t),my+ph+15+li*11,'#444',8);});});
    // Pressure curves
    if(showLV){ctx.strokeStyle=_RE;ctx.lineWidth=2.5;ctx.beginPath();
      for(var t=0;t<=1;t+=0.005){var x=toX(t),y=toYp(lvP(t),-10,140);
        if(t===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}ctx.stroke();
      _lb(ctx,'LV',toX(0.28),toYp(118,-10,140)-10,_RE,10);}
    if(showAo){ctx.strokeStyle=_GN;ctx.lineWidth=2.5;ctx.beginPath();
      for(var t2=0;t2<=1;t2+=0.005){var x2=toX(t2),y2=toYp(aoP(t2),-10,140);
        if(t2===0)ctx.moveTo(x2,y2);else ctx.lineTo(x2,y2);}ctx.stroke();
      _lb(ctx,'Aorta',toX(0.28),toYp(122,-10,140)+12,_GN,10);}
    if(showLA){ctx.strokeStyle=_AM;ctx.lineWidth=2;ctx.setLineDash([4,3]);ctx.beginPath();
      for(var t3=0;t3<=1;t3+=0.005){var x3=toX(t3),y3=toYp(laP(t3),-10,140);
        if(t3===0)ctx.moveTo(x3,y3);else ctx.lineTo(x3,y3);}ctx.stroke();ctx.setLineDash([]);
      _lb(ctx,'LA',toX(0.18),toYp(19,-10,140)-8,_AM,10);}
    ctx.textAlign='right';
    [0,40,80,120].forEach(function(v){_lb(ctx,v,mx-6,toYp(v,-10,140)+4,null,10,'right');});
    _lb(ctx,'Pressure (mmHg)',mx+pw/2,H-5,null,11);}
  draw();
  if(ctrl){ctrl.innerHTML='';var row=document.createElement('div');
    row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;align-items:center;';
    var sp=document.createElement('span');sp.textContent='SHOW: ';
    sp.style.cssText='font-size:10px;font-weight:800;color:#444;';row.appendChild(sp);
    [{key:'lv',l:'LV Pressure',c:_RE,ref:function(){return showLV;},set:function(v){showLV=v;}},
     {key:'ao',l:'Aortic Pressure',c:_GN,ref:function(){return showAo;},set:function(v){showAo=v;}},
     {key:'la',l:'LA Pressure',c:_AM,ref:function(){return showLA;},set:function(v){showLA=v;}}].forEach(function(item){
      var b=_mkB(item.l,item.c,item.ref(),function(on){item.set(on);b.style.background=on?item.c+'22':'transparent';b.style.color=on?item.c:'#555';b._on=on;draw();});
      row.appendChild(b);});ctrl.appendChild(row);}}
"""

# ── 4. Aortic Dissection Type A vs B ─────────────────────────────────────────
RF['aorticdissect'] = r"""
function _render(cv,ctrl,P){
  var W=cv.width,H=cv.height,ctx=cv.getContext('2d');if(!ctx)return;
  _cl(ctx,W,H);
  var mode=P.type||'both';
  function drawAorta(ox,oy,scale,type,highlight){
    // Simplified aortic arch diagram
    var r=18*scale;
    ctx.strokeStyle=highlight?'#ef5350':'#444';ctx.lineWidth=highlight?3:1.5;
    // Ascending aorta (right side)
    ctx.beginPath();ctx.arc(ox+40*scale,oy+20*scale,r,Math.PI,0);ctx.stroke();
    // Arch
    ctx.beginPath();ctx.arc(ox+40*scale,oy-10*scale,20*scale,0,Math.PI,true);ctx.stroke();
    // Descending aorta
    ctx.beginPath();ctx.moveTo(ox+20*scale,oy-10*scale);ctx.lineTo(ox+20*scale,oy+60*scale);ctx.stroke();
    // Labels
    _lb(ctx,'Ascending',ox+58*scale,oy+28*scale,'#888',8,'left');
    _lb(ctx,'Arch',ox+40*scale,oy-28*scale,'#888',8);
    _lb(ctx,'Descending',ox+6*scale,oy+40*scale,'#888',8,'right');
    // Type A tear (ascending)
    if(type==='A'||type==='both'){
      ctx.strokeStyle='#ef5350';ctx.lineWidth=2;ctx.setLineDash([3,2]);
      ctx.beginPath();
      ctx.moveTo(ox+52*scale,oy+32*scale);ctx.lineTo(ox+44*scale,oy+14*scale);ctx.stroke();
      ctx.setLineDash([]);
      _lb(ctx,'Type A\n(ascending)',ox+66*scale,oy+22*scale,'#ef5350',9,'left');}
    // Type B tear (descending)
    if(type==='B'||type==='both'){
      ctx.strokeStyle='#ff7043';ctx.lineWidth=2;ctx.setLineDash([3,2]);
      ctx.beginPath();
      ctx.moveTo(ox+16*scale,oy+8*scale);ctx.lineTo(ox+16*scale,oy+28*scale);ctx.stroke();
      ctx.setLineDash([]);
      _lb(ctx,'Type B\n(descending)',ox+6*scale,oy+18*scale,'#ff7043',9,'right');}}
  // Left panel: Type A
  if(mode==='A'||mode==='both'){
    _lb(ctx,'TYPE A',W/4,30,'#ef5350',13);
    _lb(ctx,'Involves ascending aorta',W/4,44,'#ef5350',9);
    drawAorta(W/4-40,70,1.6,'A',true);
    var rows_a=[['Involves','Ascending ± arch ± descending'],['Mortality untreated','1-2% per hour early'],['Treatment','EMERGENCY SURGERY'],['Complications','Tamponade · AR · MI · Stroke']];
    rows_a.forEach(function(r,i){
      _lb(ctx,r[0]+':',W/4-30,185+i*16,'#888',9,'right');
      _lb(ctx,r[1],W/4-25,185+i*16,'#ef5350',9,'left');});}
  // Right panel: Type B
  if(mode==='B'||mode==='both'){
    _lb(ctx,'TYPE B',3*W/4,30,'#ff7043',13);
    _lb(ctx,'Descending only (distal to LSA)',3*W/4,44,'#ff7043',9);
    drawAorta(3*W/4-40,70,1.6,'B',true);
    var rows_b=[['Involves','Descending aorta only'],['Mortality','Lower (5-10% early)'],['Treatment','Medical (BP control) ± TEVAR'],['Complications','Malperfusion · Rupture']];
    rows_b.forEach(function(r,i){
      _lb(ctx,r[0]+':',3*W/4-30,185+i*16,'#888',9,'right');
      _lb(ctx,r[1],3*W/4-25,185+i*16,'#ff7043',9,'left');});}
  // Stanford Classification label
  _lb(ctx,'Stanford Classification',W/2,H-8,'#444',9);
  if(ctrl){ctrl.innerHTML='';var row=document.createElement('div');
    row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;align-items:center;';
    [{key:'both',l:'Both Types',c:'#888'},{key:'A',l:'Type A Only',c:'#ef5350'},{key:'B',l:'Type B Only',c:'#ff7043'}].forEach(function(m){
      var b=_mkB(m.l,m.c,mode===m.key,function(on){if(!on)return;mode=m.key;
        row.querySelectorAll('button').forEach(function(btn){btn.style.background='transparent';btn.style.color='#555';btn._on=false;});
        b.style.background=m.c+'22';b.style.color=m.c;b._on=true;_cl(ctx,W,H);_render(cv,ctrl,P);});
      row.appendChild(b);});ctrl.appendChild(row);}}
"""

# ── 5. Shock Hemodynamic Progression ─────────────────────────────────────────
RF['shockprogress'] = r"""
function _render(cv,ctrl,P){
  var W=cv.width,H=cv.height,ctx=cv.getContext('2d');if(!ctx)return;
  var mx=56,my=20,pw=W-mx-14,ph=H-my-60,tMax=12,yD=100;
  function toX(t){return mx+(t/tMax)*pw;}
  function toY(v){return my+ph-(v/yD)*ph;}
  var type=P.type||'septic';
  var TYPES={
    septic:{label:'Septic Shock',color:_OR,
      co:  function(t){if(t<2)return 50+t*5;if(t<5)return 60-t*4;return Math.max(20,40-t*3);},
      svr: function(t){if(t<2)return 30+t*5;if(t<5)return 25+t;return Math.min(80,30+t*4);},
      map: function(t){if(t<1)return 75;if(t<4)return 75-t*5;return Math.max(25,55-t*2);},
      lac: function(t){if(t<2)return 15+t*10;if(t<6)return 35-t*2;return Math.max(10,23-t);}},
    cardio:{label:'Cardiogenic Shock',color:_RE,
      co:  function(t){return Math.max(15,50-t*4);},
      svr: function(t){return Math.min(90,40+t*6);},
      map: function(t){if(t<2)return 72-t*3;return Math.max(30,66-t*4);},
      lac: function(t){return Math.min(80,10+t*7);}},
  };
  var show={co:true,svr:true,map:true,lac:false};
  var PARAMS=[
    {key:'co',label:'CO (% normal)',color:_TE},
    {key:'svr',label:'SVR (% normal)',color:_OR},
    {key:'map',label:'MAP (% normal)',color:_GN},
    {key:'lac',label:'Lactate (% critical)',color:_RE},
  ];
  function draw(){
    _cl(ctx,W,H);_gd(ctx,mx,my,pw,ph,2,tMax,10,yD);
    ctx.strokeStyle='#666';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(mx,my);ctx.lineTo(mx,my+ph);ctx.lineTo(mx+pw,my+ph);ctx.stroke();
    // Critical threshold line at 50%
    ctx.strokeStyle='#2a2a2a';ctx.lineWidth=1;ctx.setLineDash([4,3]);
    ctx.beginPath();ctx.moveTo(mx,toY(50));ctx.lineTo(mx+pw,toY(50));ctx.stroke();ctx.setLineDash([]);
    _lb(ctx,'Critical',mx-4,toY(50)+4,'#333',8,'right');
    // Normal line at 100%
    ctx.strokeStyle='#1e3a1e';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(mx,toY(100));ctx.lineTo(mx+pw,toY(100));ctx.stroke();
    _lb(ctx,'Normal',mx-4,toY(100)+4,'#2a4a2a',8,'right');
    ctx.textAlign='center';
    [0,2,4,6,8,10,12].forEach(function(v){_lb(ctx,v+'h',toX(v),my+ph+15,null,10);});
    _lb(ctx,'Hours since onset',mx+pw/2,H-5,null,11);
    var tobj=TYPES[type];
    _lb(ctx,tobj.label,mx+pw/2,my+12,tobj.color,12);
    PARAMS.forEach(function(pa){
      if(!show[pa.key])return;
      _crv(ctx,tobj[pa.key],0,tMax,mx,my,pw,ph,tMax,yD,pa.color,2.5);
      var endV=tobj[pa.key](tMax);
      _lb(ctx,pa.label,mx+pw-4,toY(endV)-6,pa.color,9,'right');});}
  draw();
  if(ctrl){ctrl.innerHTML='';var row=document.createElement('div');
    row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;align-items:center;';
    var sp=document.createElement('span');sp.textContent='TYPE: ';
    sp.style.cssText='font-size:10px;font-weight:800;color:#444;';row.appendChild(sp);
    Object.entries(TYPES).forEach(function(e){
      var key=e[0],st=e[1];
      var b=_mkB(st.label,st.color,type===key,function(on){if(!on)return;type=key;
        row.querySelectorAll('button').forEach(function(btn){btn.style.background='transparent';btn.style.color='#555';btn._on=false;});
        b.style.background=st.color+'22';b.style.color=st.color;b._on=true;draw();});
      row.appendChild(b);});
    sp=document.createElement('span');sp.textContent='  PARAMS: ';
    sp.style.cssText='font-size:10px;font-weight:800;color:#444;';row.appendChild(sp);
    PARAMS.forEach(function(pa){
      var b=_mkB(pa.label.split(' ')[0],pa.color,show[pa.key],function(on){show[pa.key]=on;
        b.style.background=on?pa.color+'22':'transparent';b.style.color=on?pa.color:'#555';b._on=on;draw();});
      row.appendChild(b);});ctrl.appendChild(row);}}
"""

# ── CARDS ─────────────────────────────────────────────────────────────────────
CARDS = [

# ══ PA Catheter Waveform ══════════════════════════════════════════════════════
("During PA catheter insertion, the waveform transitions from RA → RV → PA → PAWP. The change from RV to PA waveform is identified by _______. Normal PA diastolic pressure (PADP) is _______ mmHg and approximates _______ in the absence of pulmonary hypertension.",
 """RV → PA transition identified by: DIASTOLIC PRESSURE RISE — the RV waveform has a LOW diastolic (0–8 mmHg, returns to near zero) while the PA waveform has a HIGHER diastolic (6–12 mmHg) that does NOT return to zero. The systolic pressure remains similar (15–30 mmHg in both). The dicrotic notch (pulmonic valve closure) also appears on the PA waveform.
| Normal PADP: 6–12 mmHg
| PADP approximates PAWP/PAOP (pulmonary artery occlusion pressure) in the absence of pulmonary hypertension — because in diastole, with the pulmonic valve closed and mitral valve open, the pressure in the PA → pulmonary veins → LA is one continuous column. PADP = PAWP when pulmonary vascular resistance is normal.
→ CCRN KEY: When PADP ≠ PAWP (PADP > PAWP by >5 mmHg): pulmonary hypertension is present — the elevated PVR creates a pressure gradient between the PA and the pulmonary veins. In this case, PADP overestimates LV filling pressure and PAWP must be measured directly by balloon occlusion.
→ MASTERY NOTE: PA catheter waveform troubleshooting: if the PA waveform suddenly looks like a PAWP waveform (no pulsatility, low pressure) — the balloon is inflated when it shouldn't be OR the catheter has migrated distally into a wedged position. Immediately call physician — prolonged inadvertent wedge → pulmonary infarction from ischemia of the occluded segment.""",
 'tier-review','Ph1 · 🔴 T1 · Cardiovascular — Hemodynamics & Shock',
 DID['hemodynamics'],'pacatheter','{"phase":"all"}','chart-l1'),

("Select the RA waveform. The 'a' wave represents _______ and the 'v' wave represents _______. A LARGE 'v' wave in the PAWP tracing indicates _______. Normal CVP (RA pressure) is _______ mmHg.",
 """'a' wave (first positive deflection after P wave on ECG): ATRIAL CONTRACTION — the atrium squeezes and pushes blood into the ventricle. The 'a' wave follows the P wave by a short delay (AV conduction time).
| 'v' wave (second positive deflection, during ventricular systole): VENOUS FILLING of the atrium against a closed tricuspid/mitral valve — blood continues to return from the pulmonary veins/SVC into the atrium while the AV valve is shut.
| LARGE 'v' wave in PAWP tracing: ACUTE MITRAL REGURGITATION (or severe chronic MR) — during ventricular systole, regurgitant blood jets back into the LA → dramatically elevated LA pressure during systole → giant 'v' wave. The LA is not stiff enough to absorb the sudden volume surge → v wave height reflects the severity of regurgitation. Also seen in: VSD, acute papillary muscle rupture.
| Normal CVP: 2–8 mmHg
→ CCRN KEY: Giant 'v' waves in PAWP + new murmur + hemodynamic deterioration post-MI = acute papillary muscle rupture until proven otherwise — a surgical emergency. Echo confirms. This is one of the highest-stakes waveform interpretations in critical care nursing.
→ MASTERY NOTE: 'x' descent = atrial relaxation after 'a' wave. 'y' descent = AV valve opening (ventricular filling begins). Blunted or absent 'y' descent suggests tricuspid stenosis (slow right ventricular filling) or constrictive pericarditis.""",
 'tier-high','Ph1 · 🔴 T1 · Cardiovascular — Hemodynamics & Shock',
 DID['hemodynamics'],'pacatheter','{"phase":"pawp"}','chart-l2'),

("PA catheter readings: CVP 18, PA 52/26 mmHg, PAWP 24 mmHg, CO 1.8 L/min, SVR 2600. PADP − PAWP = _______ mmHg. This gap indicates _______ is present. The hemodynamic profile (low CO, high SVR, high PAWP) confirms _______ shock. PAWP 24 tells you that the _______ is the problem, not volume depletion.",
 """PADP − PAWP = 26 − 24 = 2 mmHg — WITHIN NORMAL (&lt;5 mmHg). No elevated PVR — PADP is a reliable surrogate for PAWP here. Primary pulmonary hypertension is NOT the culprit; the elevated PA pressures (52/26) reflect PASSIVE BACK-PRESSURE from the elevated LV filling pressure (PAWP 24), not primary pulmonary vascular disease.
| CARDIOGENIC SHOCK — the complete profile: Low CO (1.8) + High SVR (2600, reflex vasoconstriction) + High PAWP (24, LV cannot eject → backs up) + High CVP (18, backs up further to right heart).
| PAWP 24 tells you: LEFT VENTRICLE is the problem — the LV is so impaired that it cannot empty adequately. Blood backs up into the pulmonary circuit (PAWP ↑) and then the right heart (CVP ↑). This is NOT volume depletion (which would show low CVP and PAWP). Do NOT give fluids.
→ CCRN KEY: Reading the complete PA catheter profile: (1) CVP = right-sided preload; (2) PA systolic = RV systolic pressure; (3) PA diastolic ≈ PAWP (if no PH); (4) PAWP = left-sided preload/LV filling; (5) CO = pump function; (6) SVR = afterload. All five together identify the shock type and the correct intervention.
→ MASTERY NOTE: PA catheter derived calculations: CI = CO/BSA (normal >2.2 L/min/m²); SVR = (MAP − CVP)/CO × 80 (normal 800–1400); PVR = (mean PA − PAWP)/CO × 80 (normal <250). These calculations determine the hemodynamic profile — the chart shows each pressure visually, but the mathematics drive clinical decisions.""",
 'tier-critical','Ph1 · 🔴 T1 · Cardiovascular — Hemodynamics & Shock',
 DID['hemodynamics'],'pacatheter','{"phase":"all"}','chart-l3'),

# ══ MAP Isolines ══════════════════════════════════════════════════════════════
("MAP = CO × SVR / 80. On the isoline chart, adjust the Target MAP slider to 65 mmHg. A patient with CO 2.0 and SVR 2600 has MAP = _______ mmHg. A patient with CO 7.0 and SVR 350 has MAP = _______ mmHg. Both of these are examples of _______ shock with different mechanisms.",
 """CO 2.0 × SVR 2600 / 80 = MAP 65 mmHg — achieved through HIGH SVR compensating for LOW CO (cardiogenic/hypovolemic/obstructive shock: vasoconstriction maintains MAP despite pump failure).
| CO 7.0 × SVR 350 / 80 = MAP 31 mmHg — LOW MAP despite HIGH CO because SVR is critically low (distributive shock: normal or high flow, vasodilated vasculature).
| Both: DISTRIBUTIVE (low SVR example) and CARDIOGENIC (low CO example) represent different paths to hemodynamic failure — one through vascular failure, one through pump failure. The MAP isoline chart makes visible that the same MAP can be achieved through vastly different CO/SVR combinations.
→ CCRN KEY: MAP = CO × SVR / 80 is the governing equation for all vasopressor and inotrope decisions. Before choosing a drug: identify which component is failing. Low SVR → vasopressor (norepinephrine). Low CO → inotrope (dobutamine). Both failing → combination. The isoline shows which axis the patient is on.
→ MASTERY NOTE: The MAP target (≥65 mmHg in most shock) is a surrogate for organ perfusion pressure. CPP = MAP − ICP (brain). Coronary perfusion ∝ diastolic MAP − LVEDP (heart). Renal perfusion ∝ MAP − renal vein pressure (kidney). All of these require MAP ≥65 mmHg as a minimum floor — but optimal MAP may be higher for patients with chronic hypertension (whose autoregulation is reset to higher baselines).""",
 'tier-review','Ph1 · 🔴 T1 · Cardiovascular — Hemodynamics & Shock',
 DID['hemodynamics'],'mapisoline','{"map":65}','chart-l1'),

("A septic shock patient is started on norepinephrine. MAP rises from 52 to 67 mmHg. On the MAP isoline chart, this represents moving FROM the _______ mmHg isoline TO the _______ mmHg isoline. If CO simultaneously drops from 6.2 to 5.4 L/min, the likely explanation is _______.",
 """Moving FROM the 52 mmHg isoline TO the 67 mmHg isoline — achieved by norepinephrine increasing SVR.
| The patient moves RIGHT-UPWARD on the chart (same or slightly lower CO, higher SVR → higher MAP isoline). The treatment has successfully improved MAP by increasing the vascular resistance component.
| CO drop from 6.2 → 5.4 L/min: ↑SVR (from norepinephrine) → ↑LV afterload → mildly reduced stroke volume. This is the expected tradeoff of vasopressor therapy — the afterload increase slightly reduces CO. In a normal heart, the β1 effects of norepinephrine compensate; in a compromised heart, afterload sensitivity may cause a larger CO drop.
→ CCRN KEY: When norepinephrine raises MAP but CO falls significantly (>15–20% drop): CONSIDER ADDING DOBUTAMINE. The increased afterload is compromising a vulnerable LV. The ScvO₂ will confirm — if it drops alongside CO, tissue delivery has been compromised. MAP was 'fixed' but DO₂ was not.
→ MASTERY NOTE: The isoline chart reinforces the principle: MAP can be achieved through multiple CO/SVR combinations. Two patients both with MAP 70 — one has CO 7 and SVR 800 (septic, well-compensated on norepinephrine), another has CO 2 and SVR 2800 (cardiogenic, barely maintaining pressure through extreme vasoconstriction). Same MAP, opposite hemodynamic profiles, opposite treatments.""",
 'tier-high','Ph1 · 🔴 T1 · Cardiovascular — Hemodynamics & Shock',
 DID['hemodynamics'],'mapisoline','{"map":65}','chart-l2'),

("A patient has MAP 58 mmHg, CO 1.9 L/min, SVR 2440 dynes·s/cm⁵. Calculate their current MAP isoline using the formula. Norepinephrine is started, raising SVR to 2800 but CO drops to 1.6. New MAP = _______. This demonstrates why _______ should be added and why MAP alone _______ guide resuscitation adequacy.",
 """Current MAP: CO × SVR / 80 = 1.9 × 2440 / 80 = 57.9 mmHg ≈ 58 mmHg ✓ (confirms consistent with values).
| After norepinephrine: CO 1.6 × SVR 2800 / 80 = 56 mmHg — MAP barely changed despite the vasopressor (and CO dropped). The patient moved right-upward on the chart very slightly — they hit a wall because the CO drop offset the SVR gain.
| DOBUTAMINE should be added — the failing LV cannot compensate for the afterload increase from norepinephrine. Adding an inotrope (dobutamine) would ↑CO → combined with the SVR support from norepinephrine, MAP would rise meaningfully: e.g., CO 2.4 × SVR 2600 / 80 = 78 mmHg.
| MAP alone CANNOT guide resuscitation adequacy — it is maintained by extreme vasoconstriction even as CO falls. A patient with MAP 65 and CO 1.6 is in worse hemodynamic failure than a patient with MAP 58 and CO 3.0. Track CO, ScvO₂, and lactate clearance alongside MAP.
→ CCRN KEY: The combination of dobutamine + norepinephrine for cardiogenic shock: norepinephrine maintains perfusion pressure (MAP), dobutamine improves pump function (CO). Neither alone is optimal: norepi alone worsens CO; dobutamine alone drops SVR further.
→ MASTERY NOTE: Milrinone as an alternative inotrope: phosphodiesterase III inhibitor → ↑cAMP → ↑contractility + ↑vasodilation (both cardiac and systemic). Advantage: additive effect with β-agonists (different mechanism). Disadvantage: hypotension more common (vasodilation), long half-life, renally cleared (caution in AKI). Used when dobutamine tolerance develops or in post-cardiac surgery low-output states.""",
 'tier-critical','Ph1 · 🔴 T1 · Cardiovascular — Hemodynamics & Shock',
 DID['hemodynamics'],'mapisoline','{"map":65}','chart-l3'),

# ══ Cardiac Cycle ═════════════════════════════════════════════════════════════
("On the cardiac cycle chart (Wiggers diagram), toggle LV and Aortic pressure curves. The DICROTIC NOTCH on the aortic waveform represents _______. It occurs at _______ of the cardiac cycle. On the arterial line waveform, this notch is clinically important for _______ timing.",
 """DICROTIC NOTCH: CLOSURE OF THE AORTIC VALVE — at the end of ventricular ejection, the LV pressure falls below the aortic pressure → the pressure gradient reverses → the aortic valve closes. This creates a brief pressure reflection wave that appears as the characteristic notch on the descending aortic pressure waveform.
| Occurs at the END OF SYSTOLE / BEGINNING OF ISOVOLUMETRIC RELAXATION — approximately 350–400 ms into the cardiac cycle (at normal heart rate).
| Clinically important for IABP TIMING — the IABP balloon should INFLATE at the dicrotic notch (aortic valve closure), which is the optimal timing to begin diastolic augmentation. Inflation before the notch (early inflation) = premature aortic valve closure → ↓ SV. Inflation after = reduced diastolic augmentation time.
→ CCRN KEY: On arterial line monitoring, the dicrotic notch confirms the transition from systole to diastole on every beat. Loss of the dicrotic notch (smooth descending slope without a notch): suggests AORTIC REGURGITATION (blood flows back through an incompetent aortic valve, preventing the normal pressure reflection) or very low SVR states.
→ MASTERY NOTE: The area under the systolic portion of the arterial pressure waveform (from upstroke to dicrotic notch) is proportional to STROKE VOLUME. This is the basis for pulse contour cardiac output monitoring (PiCCO, LiDCO, FloTrac) — these devices estimate CO by analyzing the arterial waveform shape rather than requiring a PA catheter.""",
 'tier-review','Ph1 · 🔴 T1 · Cardiovascular — Hemodynamics & Shock',
 DID['hemodynamics'],'cardiaccycle','{}','chart-l1'),

("Toggle LV Pressure and LA Pressure on the cardiac cycle chart. The mitral valve OPENS when _______. The period between mitral valve closure and aortic valve opening is called _______. During this phase, LV volume _______ and LV pressure _______.",
 """Mitral valve OPENS when: LV pressure falls BELOW LA pressure during isovolumetric relaxation — the LV has relaxed after ejection, its pressure falls rapidly, and once it drops below the (still slightly elevated) LA pressure, the mitral valve is pushed open by the pressure gradient. This begins the rapid ventricular filling phase.
| The period between MITRAL VALVE CLOSURE and AORTIC VALVE OPENING = ISOVOLUMETRIC CONTRACTION — both valves are closed, the LV is a sealed chamber. This is the time from when the LV starts contracting (generating pressure) until the pressure exceeds the diastolic aortic pressure and the aortic valve opens.
| During isovolumetric contraction: LV VOLUME IS CONSTANT (both valves closed — no blood in or out). LV PRESSURE RISES RAPIDLY (from ~8–12 mmHg at end-diastole to ~80 mmHg — the diastolic aortic pressure — in about 60 ms). This represents the pure pressure-generating capacity of the myocardium.
→ CCRN KEY: Isovolumetric contraction time (IVCT) on Doppler echo: prolonged IVCT = impaired LV pressure generation (systolic dysfunction) or elevated afterload. Normal IVCT ≈ 40–80 ms. IVCT + IVRT + ejection time = total cardiac cycle. Their ratios reflect ventricular function.
→ MASTERY NOTE: 'Atrial kick' occurs during the 'a' wave: atrial contraction at the end of diastole generates the terminal LA pressure wave → fills the LV with the final 10–30% of its end-diastolic volume. In atrial fibrillation, the atrial kick is LOST → CO drops 10–30%, more in stiff/non-compliant ventricles (HFpEF, LVH, aortic stenosis). This is why rate control in AF matters — not just the rate, but the LOSS OF ATRIAL SYNCHRONY.""",
 'tier-high','Ph1 · 🔴 T1 · Cardiovascular — Hemodynamics & Shock',
 DID['hemodynamics'],'cardiaccycle','{}','chart-l2'),

("A patient in AF with rapid ventricular response (HR 142) has MAP 64 and CO 3.1 (down from 4.8 at sinus rhythm). On the cardiac cycle chart, the two mechanisms causing the CO drop are: (1) _______ because diastolic filling time _______, and (2) _______ because atrial kick is _______. Target HR for CO optimization: _______.",
 """(1) REDUCED DIASTOLIC FILLING TIME — at HR 142, the cardiac cycle duration is 60/142 = 422 ms. Most of this is consumed by systole (~300 ms, relatively fixed). Diastole shrinks to ~120 ms — barely enough for passive ventricular filling. EDV decreases → stroke volume decreases (Frank-Starling principle: less preload → less SV). CO = HR × SV: HR is high but SV is so reduced that the product (CO) falls.
| (2) LOSS OF ATRIAL KICK — AF means disorganized atrial electrical activity with no coordinated atrial contraction. The terminal active filling phase (contributing 10–30% of EDV) is absent. In this patient with presumably some diastolic dysfunction (stiff ventricle), the atrial kick contribution was likely higher (>20%), explaining the large CO drop.
| Target HR: 60–100 bpm (optimally 70–90 bpm) — sufficient rate to maintain cardiac output while allowing adequate diastolic filling time. Rate control agents: beta-blockers (metoprolol), calcium channel blockers (diltiazem), digoxin. Target the LOWEST heart rate that maintains adequate MAP — not the lowest possible rate.
→ CCRN KEY: Rate control vs. rhythm control in hemodynamically unstable AF: if MAP <90 or signs of end-organ hypoperfusion → SYNCHRONIZED CARDIOVERSION (rate control drugs work too slowly). If hemodynamically stable → trial of rate control drugs while investigating cause (infection, pain, fluid shift).
→ MASTERY NOTE: The Fick equation connects the cardiac cycle to oxygen delivery: CO = VO₂ / (CaO₂ − CvO₂). In tachycardia with ↓CO, VO₂ may be unchanged while CaO₂ − CvO₂ widens (↑extraction) → ScvO₂ falls. Monitoring ScvO₂ in tachycardic AF reveals the hemodynamic impact: ScvO₂ <60% confirms that the tachycardia is causing significant DO₂ compromise.""",
 'tier-critical','Ph1 · 🔴 T1 · Cardiovascular — Hemodynamics & Shock',
 DID['hemodynamics'],'cardiaccycle','{}','chart-l3'),

# ══ Aortic Dissection ═════════════════════════════════════════════════════════
("From the aortic dissection comparison chart: Type A involves _______ and Type B involves _______ only. The immediate life-threatening difference that makes Type A a surgical emergency: _______.",
 """Type A: ASCENDING AORTA (and may extend to arch or descending aorta). The Stanford classification defines Type A by ascending aorta involvement regardless of where the tear originates.
| Type B: DESCENDING AORTA ONLY (distal to the left subclavian artery origin). The ascending aorta is spared.
| Type A is a surgical emergency because: proximity to the pericardium → PERICARDIAL TAMPONADE (blood leaks into the pericardial sac → cardiac compression → cardiac arrest). Also: proximity to the coronary ostia → acute MI (RCA most commonly, from dissection flap extending into right coronary ostium). Proximity to the aortic valve → acute severe aortic regurgitation (dissection disrupts the aortic root → valve prolapse). These three complications — tamponade, MI, and severe AR — can develop within hours and require emergency surgical repair.
→ CCRN KEY: Type A presentation: sudden severe tearing chest pain radiating to the back + NEW murmur of AR + pulse differentials between arms + hypotension + elevated troponin (RCA MI). Any one of these in combination → activate aortic surgery pathway immediately.
→ MASTERY NOTE: Differentiating Type A dissection MI from primary ACS: in dissection MI, PCI may propagate the dissection flap or introduce contrast into the false lumen catastrophically. The key question BEFORE taking a chest pain patient to the cath lab: could this be aortic dissection? Red flags: tearing/ripping character, maximal at onset, radiation to back, pulse differentials, widened mediastinum on CXR. If dissection is a possibility → CT angiography FIRST, not coronary angiogram.""",
 'tier-review','Ph1 · 🔴 T1 · Cardiovascular — Aortic & Vascular',
 DID['aortic_vascular'],'aorticdissect','{"type":"both"}','chart-l1'),

("Type B aortic dissection: treatment is _______ management unless complications develop. Target SBP: _______ mmHg. Target HR: _______ bpm. The antihypertensive drug CLASS preferred in aortic dissection because it reduces both _______ and _______ is _______.",
 """MEDICAL management — pain control + aggressive blood pressure and heart rate control. Unlike Type A, surgery (open or TEVAR) is reserved for complications: malperfusion (ischemia to spinal cord, mesenteric vessels, renal arteries), rupture, refractory hypertension, or rapid expansion.
| Target SBP: 100–120 mmHg (some sources say <120 mmHg) — lower BP reduces the hydraulic stress on the aortic wall and slows propagation of the dissection flap. However, too low → spinal cord ischemia (spinal arteries arise from the descending aorta in many patients).
| Target HR: <60–65 bpm — reducing heart rate decreases dP/dt (rate of pressure rise), which is a key driver of dissection propagation even more than the absolute pressure.
| Preferred class: BETA-BLOCKERS (IV esmolol first-line for acute management, then oral metoprolol/labetalol) — they reduce BOTH blood pressure AND heart rate. No other single drug class achieves both simultaneously. Nitroprusside lowers BP but reflexively increases HR (not ideal). Calcium channel blockers (diltiazem) reduce both but are less first-line than beta-blockers for acute management.
→ CCRN KEY: IV esmolol protocol for aortic dissection: 500 mcg/kg loading dose, then 50–200 mcg/kg/min infusion, titrate to HR <65 and SBP 100–120. Short half-life (9 min) allows rapid dose adjustment. If SBP remains elevated after adequate HR control → add IV nitroprusside (to reduce afterload).
→ MASTERY NOTE: Pain control is critical in aortic dissection — undertreated pain → catecholamine surge → ↑HR and BP → worsens dissection. IV morphine or fentanyl titrated to pain control (typically NRS <4) is part of the acute management package alongside antihypertensives. The patient who reports 10/10 tearing pain on IV esmolol alone is not adequately treated.""",
 'tier-high','Ph1 · 🔴 T1 · Cardiovascular — Aortic & Vascular',
 DID['aortic_vascular'],'aorticdissect','{"type":"B"}','chart-l2'),

("A patient has sudden tearing chest pain radiating to the back, BP 186/94 right arm and 148/82 left arm, new soft diastolic murmur, and ST elevation in lead II. CT angiography confirms Type A aortic dissection. The ST elevation is caused by _______, NOT primary ACS. This distinction changes management because _______. Immediate nursing priorities: _______, _______, and _______.",
 """ST elevation caused by: DISSECTION FLAP OCCLUDING THE RIGHT CORONARY ARTERY OSTIUM — the dissection extending into the aortic root can compress or extend into the RCA origin, causing inferior MI (leads II, III, aVF pattern) from RCA territory ischemia.
| NOT primary ACS — the distinction changes management critically: in primary ACS → PCI with anticoagulation and possible thrombolytics. In Type A dissection with RCA involvement → PCI would introduce the catheter into or near the dissection flap, could extend the dissection, would give anticoagulation that promotes aortic hemorrhage, and delays definitive surgical repair. ANTICOAGULATION IS CONTRAINDICATED in aortic dissection. Taking this patient to PCI would likely cause death.
| Immediate nursing priorities:
  (1) NOTIFY CARDIAC SURGERY AND OR TEAM IMMEDIATELY — this is a surgical emergency, mortality 1-2% per hour untreated
  (2) ARTERIAL LINE in the right radial (better pressure) + large-bore IV access × 2 — for continuous BP monitoring and rapid infusion
  (3) IV ESMOLOL infusion to target HR &lt;65 and SBP 100–120 mmHg while awaiting OR — reduce dP/dt to slow dissection propagation
→ CCRN KEY: The nurse's role in suspected Type A dissection: do NOT give aspirin, heparin, or thrombolytics for the concurrent ST elevation (until dissection is definitively ruled out). Activate the surgical pathway simultaneously with the diagnostic workup. Time to OR is the mortality-determining variable — not time to PCI.
→ MASTERY NOTE: Pulse differentials in aortic dissection: BP difference >20 mmHg between arms suggests the dissection flap is compromising flow to one subclavian artery. Check bilateral BPs at initial assessment. Similarly, check lower extremity pulses (dissection can extend into iliac arteries → limb ischemia). Malperfusion to any major vessel territory (brain, coronary, mesenteric, renal, spinal) represents a Type A or complicated Type B that needs urgent surgical or endovascular intervention.""",
 'tier-critical','Ph1 · 🔴 T1 · Cardiovascular — Aortic & Vascular',
 DID['aortic_vascular'],'aorticdissect','{"type":"A"}','chart-l3'),

# ══ Shock Progression ═════════════════════════════════════════════════════════
("On the shock progression chart, select Septic Shock. In EARLY septic shock (first 2-4 hours), CO is _______ and SVR is _______ (the 'warm shock' phase). This distinguishes early sepsis from cardiogenic shock where CO is _______ and SVR is _______.",
 """EARLY SEPTIC SHOCK: CO is HIGH (or normal to elevated) — the heart compensates for low SVR by ↑HR and ↑contractility driven by catecholamine surge. SVR is LOW — inflammatory mediators (nitric oxide, prostaglandins) cause systemic vasodilation.
| 'WARM SHOCK' phase: the patient is warm (vasodilated, ↑skin perfusion), flushed, with bounding pulses, tachycardic, and hypotensive. High CO pumps blood rapidly but the vasodilated vasculature cannot maintain MAP.
| CARDIOGENIC SHOCK: CO is LOW (pump failure), SVR is HIGH (reflex vasoconstriction — the body compensates for ↓CO by constricting to maintain MAP). The patient is cool, clammy, pale, with weak pulses ('cold shock').
→ CCRN KEY: The distinction matters for initial treatment: warm shock (distributive) → vasopressors (norepinephrine) to ↑SVR. Cold shock (cardiogenic) → inotropes (dobutamine) to ↑CO. Starting norepinephrine in a patient in cold/cardiogenic shock worsens CO by ↑afterload on the failing LV.
→ MASTERY NOTE: 'Late septic shock' can look like cardiogenic shock on the progression chart — after several hours, sepsis-induced myocardial depression develops (cytokine-mediated ↓contractility) → CO begins falling. At this point, the hemodynamic profile shifts from warm/high CO to cold/low CO. This is why ScvO₂ monitoring matters throughout septic shock — it detects the transition from distributive to mixed distributive-cardiogenic physiology.""",
 'tier-review','Ph1 · 🔴 T1 · Cardiovascular — Hemodynamics & Shock',
 DID['hemodynamics'],'shockprogress','{"type":"septic"}','chart-l1'),

("On the shock progression chart, the lactate parameter tracks the DO₂/VO₂ mismatch over time. Lactate rising past the critical threshold despite adequate MAP indicates _______. Select Cardiogenic Shock — compare the CO trajectory to Septic Shock. The reason cardiogenic shock has worse early lactate elevation: _______.",
 """Lactate rising past the critical threshold despite adequate MAP indicates: COVERT HEMODYNAMIC FAILURE — the macrovascular parameters (MAP, CVP) appear adequate, but tissue oxygen delivery has fallen below the critical threshold. The cells are switching to anaerobic metabolism. This pattern (acceptable MAP + rising lactate) is 'cryptic shock' and requires IMMEDIATE reassessment of CO and ScvO₂.
| Cardiogenic shock has worse early lactate elevation than septic shock because: in cardiogenic shock, CO fails IMMEDIATELY from pump dysfunction — the DO₂ deficit begins at onset. In early septic shock, CO is actually ELEVATED (high-output distributive), and the lactate elevation initially reflects microcirculatory dysfunction and altered metabolism rather than global DO₂ deficit. The absolute DO₂ in early sepsis may be normal or high — the problem is distribution, not total delivery. In cardiogenic shock, total DO₂ is critically reduced from the first moment.
→ CCRN KEY: Lactate targets in shock management: initial lactate >4 mmol/L = high-risk, 6h mortality 40%+. Target: ≥10% clearance per 2 hours. Failure to clear = resuscitation incomplete regardless of normal vital signs. The resuscitation endpoint is not blood pressure — it is metabolic normalization.
→ MASTERY NOTE: Causes of elevated lactate WITHOUT hemodynamic shock: hepatic failure (can't clear lactate), metformin toxicity (inhibits hepatic gluconeogenesis and lactate clearance), thiamine deficiency (impairs pyruvate dehydrogenase → lactate accumulates), vigorous seizure activity (muscle lactate production), beta-agonist toxicity (albuterol → glycolysis → lactate). These 'type B' lactic acidoses must be distinguished from 'type A' (tissue hypoperfusion) before attributing lactate to inadequate resuscitation.""",
 'tier-high','Ph1 · 🔴 T1 · Cardiovascular — Hemodynamics & Shock',
 DID['hemodynamics'],'shockprogress','{"type":"cardio"}','chart-l2'),

("At hour 6 on the Cardiogenic Shock progression chart, CO has fallen to 25% of normal and MAP is at 45% of normal despite vasopressors. Lactate is 8.2 mmol/L (critically elevated). The next escalation beyond dobutamine + norepinephrine is _______ (mechanical circulatory support). Two options and the distinction between them: _______.",
 """MECHANICAL CIRCULATORY SUPPORT (MCS) — when pharmacological support (dobutamine + norepinephrine) is insufficient to maintain perfusion and prevent progressive end-organ failure, hardware assistance is required.
| Two options and distinction:
  (1) IABP (Intra-Aortic Balloon Pump): counter-pulsation → ↑diastolic augmentation (↑coronary perfusion) + ↓LV afterload (↓LVEDP). Augments native CO by 10–20%. Easiest to place, least hemodynamic support, requires some native LV function to benefit. Limited by: tachycardia (less diastolic time), aortic regurgitation (contraindicated), severe PVD.
  (2) IMPELLA (microaxial LV-to-aorta pump): direct LV unloading — pulls blood from LV and ejects into ascending aorta. Provides 2.5–5.5 L/min additional CO (model-dependent). Does NOT require native LV function. Indicated for severe cardiogenic shock (SCAI Stage C–E). Requires anticoagulation, larger sheath (14–22F). Reduces LV wall stress, ↓myocardial O₂ demand, potentially allows myocardial recovery.
→ CCRN KEY: SCAI Shock Classification (CCRN exam topic): Stage A (At risk), B (Beginning shock — tachycardia, early hypoperfusion), C (Classic cardiogenic — hypotension + inotropes + early organ damage), D (Deteriorating — worsening despite support), E (Extremis — cardiac arrest or near-arrest). Stage D–E typically requires MCS and/or ECMO.
→ MASTERY NOTE: IMPELLA nursing: anticoagulation monitoring (heparin infusion via device controller), positioning verification (device tip should be 3.5 cm above aortic valve on chest X-ray), suction alarms (device pulled into LV — reposition), outlet alarms (device advanced too far — reposition). Verify correct positioning with echo or fluoroscopy after every position change or patient movement.""",
 'tier-critical','Ph1 · 🔴 T1 · Cardiovascular — Hemodynamics & Shock',
 DID['hemodynamics'],'shockprogress','{"type":"cardio"}','chart-l3'),
]

# ── Build ────────────────────────────────────────────────────────────────────
def main():
    db, models, existing_guids = load_deck(DECK_PATH, WORK_DIR)
    main_css  = get_main_css(models)
    CHART_CSS = main_css + CHART_CSS_ADDON
    validator = CardValidator()
    now       = int(time.time())
    nid_base  = now * 1000
    added     = 0

    print(f"{'='*65}\nCHUNK {CHUNK_NUM} — Validating {len(CARDS)} cards\n{'='*65}")

    for i, card in enumerate(CARDS):
        front, back, tier, badge, did, ctype, pj, ltag = card
        issues = validator.validate(f'c{CHUNK_NUM}_{i}', front, back, badge)
        ok = not issues
        print(f"  {'✅' if ok else '❌'} [{ctype}·{ltag}] {front[:65]}")
        if not ok:
            for iss in issues: print(f"      ✗ {iss}")

    print(validator.report())

    for i, card in enumerate(CARDS):
        front, back, tier, badge, did, ctype, pj, ltag = card
        issues = validator.validate(f'c{CHUNK_NUM}_{i}_ins', front, back, badge)
        if issues: continue

        chart_idx = CHART_ORDER.index(ctype)
        mid_int   = MID_BASE + chart_idx
        mkey      = str(mid_int)

        if mkey not in models:
            qfmt, afmt = make_chart_template(ctype, pj, RF[ctype], SHARED_JS, CHART_CSS)
            register_chart_model(models, mid_int, ctype, did, qfmt, afmt, CHART_CSS)

        guid = make_guid(front, back)
        if guid in existing_guids: continue
        existing_guids.add(guid)

        flds = '\x1f'.join([safe_html(front), safe_html(back), tier, badge])
        sfld = re.sub(r'<[^>]+>', '', front)[:100]
        nid  = nid_base + i * 3
        tags = f' ccrn-pccn-v6 chunk-{CHUNK_NUM} {ltag} '

        insert_card(db, nid, nid+1, guid, mkey, flds, sfld, did, tags, now)
        added += 1
        print(f"  ✓ [{ctype}·{ltag}]")

    save_deck(db, models, WORK_DIR, OUT_PATH)

    import sqlite3 as _sq
    db2 = _sq.connect(os.path.join(WORK_DIR, 'collection.anki2'))
    total = db2.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    db2.close()

    print(f"\n{'='*65}")
    print(f"  Chunk {CHUNK_NUM}: {added} cards added | Total: {total}")
    print(f"{'='*65}")

if __name__ == '__main__':
    main()
