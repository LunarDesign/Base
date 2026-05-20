#!/usr/bin/env python3
"""
Chunk 32 — Ph4 Neurology (5 charts: 4+4+3+3+3 = 17 cards)
Charts: Cerebral autoregulation, ICP waveforms, Monro-Kellie, CPP interactive, RASS scale
Run: python chunk32_charts.py
"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card, SHARED_JS, CHART_CSS_ADDON, DID)
from card_validator import CardValidator

DECK_PATH  = 'CCRN_PCCN_Mastery_v7_final_31.apkg'
OUT_PATH   = 'CCRN_PCCN_Mastery_v7_final_32.apkg'
WORK_DIR   = os.path.join(tempfile.gettempdir(), 'c32')
CHUNK_NUM  = 32
MID_BASE   = 1_800_005_005
CHART_ORDER = ['cerebralautoregulation','icpwaveforms','monrokellie','cppinteractive','rassscale']

RF = {}

# ── 1. Cerebral Autoregulation ────────────────────────────────────────────────
RF['cerebralautoregulation'] = r"""
function _render(cv,ctrl,P){
  var W=cv.width,H=cv.height,ctx=cv.getContext('2d');if(!ctx)return;
  var mx=54,my=16,pw=W-mx-14,ph=H-my-52,xD=160,yD=100;
  function toX(cpp){return mx+(cpp/xD)*pw;}
  function toY(cbf){return my+ph-(cbf/yD)*ph;}
  function cbfFn(cpp){
    if(cpp<=0)return 0;
    if(cpp<50)return(cpp/50)*75;
    if(cpp<=150)return 75+((cpp-50)/100)*5;
    return 80+(cpp-150)*0.8;}
  var patCPP=P.cpp!==undefined?P.cpp:70;
  function draw(){
    _cl(ctx,W,H);
    ctx.fillStyle='rgba(239,83,80,0.09)';ctx.fillRect(toX(0),my,toX(50)-toX(0),ph);
    ctx.fillStyle='rgba(76,175,80,0.06)';ctx.fillRect(toX(50),my,toX(150)-toX(50),ph);
    ctx.fillStyle='rgba(255,112,67,0.09)';ctx.fillRect(toX(150),my,pw-(toX(150)-mx),ph);
    _gd(ctx,mx,my,pw,ph,20,xD,10,yD);
    ctx.strokeStyle='#555';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(mx,my);ctx.lineTo(mx,my+ph);ctx.lineTo(mx+pw,my+ph);ctx.stroke();
    _lb(ctx,'Ischemia',toX(25),my+18,_RE+'aa',9);
    _lb(ctx,'Autoregulated Plateau',toX(100),my+18,_GN+'bb',9);
    _lb(ctx,'Breakthrough',toX(157),my+18,_OR+'aa',8);
    [0,20,40,60,80,100,120,140,160].forEach(function(v){_lb(ctx,v,toX(v),my+ph+15,null,9);});
    [0,20,40,60,80,100].forEach(function(v){_lb(ctx,v+'%',mx-5,toY(v)+4,null,9,'right');});
    _lb(ctx,'CPP (mmHg)',mx+pw/2,H-5,null,11);
    _rl(ctx,'CBF (% normal)',14,my+ph/2);
    ctx.strokeStyle=_TE;ctx.lineWidth=3;ctx.beginPath();
    for(var c=0;c<=160;c+=1){var x=toX(c),y=toY(cbfFn(c));if(c===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}
    ctx.stroke();
    var px=toX(patCPP),py=toY(cbfFn(patCPP));
    ctx.strokeStyle=_AM;ctx.lineWidth=1;ctx.setLineDash([3,3]);
    ctx.beginPath();ctx.moveTo(px,my);ctx.lineTo(px,my+ph);ctx.stroke();ctx.setLineDash([]);
    _dot(ctx,px,py,7,_AM);
    var zone=patCPP<50?'ISCHEMIA RISK':patCPP<=150?'AUTOREGULATED':'BREAKTHROUGH';
    var zcol=patCPP<50?_RE:patCPP<=150?_GN:_OR;
    _lb(ctx,'CPP '+patCPP+' mmHg → '+zone,mx+pw/2,my+ph-10,zcol,10);}
  draw();
  if(ctrl){ctrl.innerHTML='';var row=document.createElement('div');
    row.style.cssText='display:flex;flex-wrap:wrap;gap:12px;margin-top:8px;';
    row.appendChild(_mkS('Patient CPP','0','160','5',patCPP,function(v){return v+' mmHg';},
      function(v){patCPP=v;P.cpp=v;draw();}));
    ctrl.appendChild(row);}}
"""

# ── 2. ICP Waveforms ─────────────────────────────────────────────────────────
RF['icpwaveforms'] = r"""
function _render(cv,ctrl,P){
  var W=cv.width,H=cv.height,ctx=cv.getContext('2d');if(!ctx)return;
  var mx=54,my=16,pw=W-mx-14,ph=H-my-52,yMin=0,yMax=100;
  function toX(t){return mx+(t/1)*pw;}
  function toY(p){return my+ph-((p-yMin)/(yMax-yMin))*ph;}
  var mode=P.mode||'A';
  var WAVES={
    'A':{label:'A Waves (Plateau Waves)',color:_RE,desc:'50-100 mmHg · 5-20 min · CRITICAL — IMMINENT HERNIATION RISK',
      fn:function(t){var ph2=t%0.4/0.4;
        if(ph2<0.06)return 15+(ph2/0.06)*65;
        if(ph2<0.55)return 80-(ph2-0.06)/0.49*6;
        if(ph2<0.68)return 74-(ph2-0.55)/0.13*59;
        return 15;}},
    'B':{label:'B Waves',color:_AM,desc:'10-30 mmHg · 0.5-2/min · WARNING — Reduced compliance',
      fn:function(t){return 14+Math.abs(Math.sin(t*Math.PI*4))*22;}},
    'C':{label:'C Waves',color:_TE,desc:'Up to 20 mmHg · 4-8/min · MONITOR — Least significant',
      fn:function(t){return 11+Math.sin(t*Math.PI*9)*5+Math.sin(t*Math.PI*6)*3;}}};
  function draw(){
    _cl(ctx,W,H);_gd(ctx,mx,my,pw,ph,0.1,1,10,yMax);
    ctx.strokeStyle='#555';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(mx,my);ctx.lineTo(mx,my+ph);ctx.lineTo(mx+pw,my+ph);ctx.stroke();
    ctx.fillStyle='rgba(239,83,80,0.07)';ctx.fillRect(mx,toY(20),pw,toY(0)-toY(20));
    ctx.strokeStyle=_RE;ctx.lineWidth=1;ctx.setLineDash([4,3]);
    ctx.beginPath();ctx.moveTo(mx,toY(20));ctx.lineTo(mx+pw,toY(20));ctx.stroke();ctx.setLineDash([]);
    _lb(ctx,'ICP >20 mmHg — TREAT',mx+pw-4,toY(22),_RE,9,'right');
    ctx.fillStyle='rgba(76,175,80,0.05)';ctx.fillRect(mx,toY(15),pw,toY(0)-toY(15));
    [0,20,40,60,80,100].forEach(function(v){_lb(ctx,v,mx-5,toY(v)+4,null,9,'right');});
    _lb(ctx,'ICP (mmHg)',mx+pw/2,H-5,null,11);
    var wv=WAVES[mode];
    ctx.strokeStyle=wv.color;ctx.lineWidth=2.5;ctx.beginPath();
    for(var i=0;i<=400;i++){var t=i/400;var p=wv.fn(t);
      var x=toX(t),y=toY(Math.max(0,Math.min(100,p)));
      if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}
    ctx.stroke();
    _lb(ctx,wv.label,mx+pw/2,my+10,wv.color,11);
    _lb(ctx,wv.desc,mx+pw/2,my+24,wv.color+'cc',8);}
  draw();
  if(ctrl){ctrl.innerHTML='';var row=document.createElement('div');
    row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;align-items:center;';
    var sp=document.createElement('span');sp.textContent='WAVE TYPE: ';
    sp.style.cssText='font-size:10px;font-weight:800;color:#444;';row.appendChild(sp);
    ['A','B','C'].forEach(function(k){
      var wv=WAVES[k];
      var b=_mkB(k+' Waves',wv.color,mode===k,function(on){if(!on)return;mode=k;
        row.querySelectorAll('button').forEach(function(btn){btn.style.background='transparent';btn.style.color='#555';});
        b.style.background=wv.color+'22';b.style.color=wv.color;draw();});
      row.appendChild(b);});ctrl.appendChild(row);}}
"""

# ── 3. Monro-Kellie Volume-Pressure Curve ────────────────────────────────────
RF['monrokellie'] = r"""
function _render(cv,ctrl,P){
  var W=cv.width,H=cv.height,ctx=cv.getContext('2d');if(!ctx)return;
  var mx=56,my=16,pw=W-mx-14,ph=H-my-52,xD=40,yD=80;
  function toX(v){return mx+(v/xD)*pw;}
  function toY(p){return my+ph-(p/yD)*ph;}
  function icpFn(v){return Math.min(80,5+0.15*Math.exp(0.155*v));}
  var patVol=P.vol!==undefined?P.vol:0;
  function draw(){
    _cl(ctx,W,H);
    ctx.fillStyle='rgba(76,175,80,0.07)';ctx.fillRect(toX(0),my,toX(22)-toX(0),ph);
    ctx.fillStyle='rgba(239,83,80,0.07)';ctx.fillRect(toX(22),my,toX(40)-toX(22),ph);
    _gd(ctx,mx,my,pw,ph,5,xD,10,yD);
    ctx.strokeStyle='#555';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(mx,my);ctx.lineTo(mx,my+ph);ctx.lineTo(mx+pw,my+ph);ctx.stroke();
    ctx.strokeStyle=_RE;ctx.lineWidth=1;ctx.setLineDash([4,3]);
    ctx.beginPath();ctx.moveTo(mx,toY(20));ctx.lineTo(mx+pw,toY(20));ctx.stroke();ctx.setLineDash([]);
    _lb(ctx,'ICP 20 mmHg threshold',mx+pw-4,toY(22),_RE,8,'right');
    _lb(ctx,'Compensated',toX(11),my+16,_GN+'aa',9);
    _lb(ctx,'(CSF + venous shift)',toX(11),my+28,_GN+'88',8);
    _lb(ctx,'Decompensated',toX(31),my+16,_RE+'aa',9);
    _lb(ctx,'(rapid ICP rise)',toX(31),my+28,_RE+'88',8);
    [0,10,20,30,40].forEach(function(v){_lb(ctx,v,toX(v),my+ph+15,null,9);});
    [0,20,40,60,80].forEach(function(v){_lb(ctx,v,mx-5,toY(v)+4,null,9,'right');});
    _lb(ctx,'Volume added (mL)',mx+pw/2,H-5,null,11);
    _rl(ctx,'ICP (mmHg)',14,my+ph/2);
    ctx.strokeStyle=_TE;ctx.lineWidth=3;ctx.beginPath();
    for(var v=0;v<=40;v+=0.2){var x=toX(v),y=toY(icpFn(v));
      if(v===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}
    ctx.stroke();
    if(patVol>0){
      var pv=toX(patVol),picp=icpFn(patVol),py2=toY(picp);
      ctx.strokeStyle=_AM;ctx.lineWidth=1;ctx.setLineDash([3,3]);
      ctx.beginPath();ctx.moveTo(pv,my);ctx.lineTo(pv,my+ph);ctx.stroke();ctx.setLineDash([]);
      _dot(ctx,pv,py2,7,_AM);
      var zone2=patVol<22?'COMPENSATED':'DECOMPENSATED';
      var zcol2=patVol<22?_GN:_RE;
      _lb(ctx,'+'+patVol+' mL → ICP '+Math.round(icpFn(patVol))+' mmHg ('+zone2+')',mx+pw/2,my+ph-10,zcol2,10);}}
  draw();
  if(ctrl){ctrl.innerHTML='';var row=document.createElement('div');
    row.style.cssText='display:flex;flex-wrap:wrap;gap:12px;margin-top:8px;';
    row.appendChild(_mkS('Added volume','0','40','1',patVol,function(v){return v+' mL';},
      function(v){patVol=v;P.vol=v;draw();}));
    ctrl.appendChild(row);}}
"""

# ── 4. CPP Interactive ───────────────────────────────────────────────────────
RF['cppinteractive'] = r"""
function _render(cv,ctrl,P){
  var W=cv.width,H=cv.height,ctx=cv.getContext('2d');if(!ctx)return;
  var mapVal=P.map!==undefined?P.map:80,icpVal=P.icp!==undefined?P.icp:15;
  function draw(){
    _cl(ctx,W,H);
    var cpp=mapVal-icpVal;
    var cppCol=cpp<50?_RE:cpp<70?_AM:_GN;
    ctx.textAlign='center';
    ctx.font='bold 11px monospace';ctx.fillStyle='#666';ctx.fillText('CPP = MAP − ICP',W/2,38);
    ctx.font='13px monospace';ctx.fillStyle='#555';ctx.fillText(mapVal+' − '+icpVal+' =',W/2,62);
    ctx.font='bold 54px monospace';ctx.fillStyle=cppCol;ctx.fillText(cpp+' mmHg',W/2,122);
    var zl=cpp<50?'CRITICAL — Cerebral ischemia risk':cpp<70?'BELOW TARGET (50–70 borderline)':'ADEQUATE — Target ≥70 mmHg met';
    ctx.font='bold 10px monospace';ctx.fillStyle=cppCol;ctx.fillText(zl,W/2,146);
    var bx=55,bw=W-110,by=160,bh=22;
    var zones=[{mn:0,mx2:50,col:_RE+'66',lbl:'Critical <50'},
               {mn:50,mx2:70,col:_AM+'66',lbl:'Borderline 50–70'},
               {mn:70,mx2:140,col:_GN+'66',lbl:'Target ≥70'}];
    zones.forEach(function(z){
      var x1=bx+z.mn/140*bw,x2=bx+Math.min(z.mx2,140)/140*bw;
      ctx.fillStyle=z.col;ctx.fillRect(x1,by,x2-x1,bh);
      ctx.font='8px monospace';ctx.fillStyle='#ddd';ctx.textAlign='center';
      ctx.fillText(z.lbl,(x1+x2)/2,by+bh/2+3);});
    var mpos=bx+Math.max(0,Math.min(cpp,140))/140*bw;
    ctx.fillStyle=cppCol;ctx.fillRect(mpos-2,by-4,4,bh+8);
    ctx.font='10px monospace';ctx.fillStyle=cppCol;ctx.textAlign='center';ctx.fillText('▲',mpos,by+bh+14);
    _lb(ctx,'Formula: CPP = MAP − ICP · Target CPP: 60–70 mmHg (TBI) · Raise CPP via ↑MAP or ↓ICP',W/2,H-8,'#555',8);}
  draw();
  if(ctrl){ctrl.innerHTML='';var row=document.createElement('div');
    row.style.cssText='display:flex;flex-wrap:wrap;gap:12px;margin-top:8px;';
    row.appendChild(_mkS('MAP','40','140','5',mapVal,function(v){return v+' mmHg';},
      function(v){mapVal=v;P.map=v;draw();}));
    row.appendChild(_mkS('ICP','0','60','1',icpVal,function(v){return v+' mmHg';},
      function(v){icpVal=v;P.icp=v;draw();}));
    ctrl.appendChild(row);}}
"""

# ── 5. RASS Scale ─────────────────────────────────────────────────────────────
RF['rassscale'] = r"""
function _render(cv,ctrl,P){
  var W=cv.width,H=cv.height,ctx=cv.getContext('2d');if(!ctx)return;
  var target=P.target!==undefined?parseInt(P.target):0;
  var LEVELS=[
    {v:4,label:'+4 Combative',desc:'Overtly combative, violent, danger to staff',col:'#b71c1c'},
    {v:3,label:'+3 Very Agitated',desc:'Pulls/removes tubes, aggressive',col:'#c62828'},
    {v:2,label:'+2 Agitated',desc:'Frequent non-purposeful movement',col:'#ef5350'},
    {v:1,label:'+1 Restless',desc:'Anxious, apprehensive, movements not aggressive',col:'#ff7043'},
    {v:0,label:'0 Alert & Calm',desc:'Spontaneously awake, calm, attentive',col:'#4caf50'},
    {v:-1,label:'−1 Drowsy',desc:'Briefly awakens to voice, eye contact >10 sec',col:'#29b6f6'},
    {v:-2,label:'−2 Light Sedation',desc:'Eye opening/contact to voice <10 sec',col:'#039be5'},
    {v:-3,label:'−3 Moderate Sedation',desc:'Movement or eye opening to voice, no contact',col:'#0288d1'},
    {v:-4,label:'−4 Deep Sedation',desc:'Movement to physical stimulus only',col:'#0277bd'},
    {v:-5,label:'−5 Unarousable',desc:'No response to voice or physical stimulus',col:'#01579b'}];
  var bx=166,bw=W-bx-8,barH=19,gap=3;
  var totalH=LEVELS.length*(barH+gap),startY=Math.max(10,(H-52-totalH)/2+10);
  function draw(){
    _cl(ctx,W,H);
    LEVELS.forEach(function(lv,i){
      var y=startY+i*(barH+gap),isTgt=lv.v===target;
      ctx.fillStyle=lv.col+(isTgt?'ff':'44');ctx.fillRect(bx,y,bw,barH);
      if(isTgt){ctx.strokeStyle=lv.col;ctx.lineWidth=2;ctx.strokeRect(bx-1,y-1,bw+2,barH+2);}
      ctx.textAlign='right';ctx.font=(isTgt?'bold ':'')+'9px monospace';
      ctx.fillStyle=isTgt?lv.col:'#888';ctx.fillText(lv.label,bx-4,y+barH/2+3);
      ctx.textAlign='left';ctx.font='8px monospace';ctx.fillStyle=isTgt?'#fff':'#aaa';
      ctx.fillText(lv.desc,bx+6,y+barH/2+3);});
    _lb(ctx,'RASS: Richmond Agitation-Sedation Scale · PADIS target: 0 to −1 (light sedation)',W/2,H-8,'#555',8);}
  draw();
  if(ctrl){ctrl.innerHTML='';var row=document.createElement('div');
    row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;align-items:center;';
    var sp=document.createElement('span');sp.textContent='HIGHLIGHT: ';
    sp.style.cssText='font-size:10px;font-weight:800;color:#444;';row.appendChild(sp);
    [{v:-2,l:'−2 (Vent)'},{v:-1,l:'−1 (Light)'},{v:0,l:'0 (Alert)'},{v:1,l:'+1 (Restless)'}].forEach(function(t){
      var b=_mkB(t.l,'#29b6f6',target===t.v,function(on){if(!on)return;target=t.v;P.target=t.v;
        row.querySelectorAll('button').forEach(function(btn){btn.style.background='transparent';btn.style.color='#555';});
        b.style.background='#29b6f622';b.style.color='#29b6f6';draw();});
      row.appendChild(b);});ctrl.appendChild(row);}}
"""

# ── CARDS ─────────────────────────────────────────────────────────────────────
CARDS = [

# ══ Cerebral Autoregulation (4 cards) ═════════════════════════════════════════
("On the cerebral autoregulation curve, CBF stays constant (the plateau) between CPP _______ and _______ mmHg in healthy adults. Below the lower limit, CBF _______ with falling CPP (pressure-passive zone).",
 """Plateau: CPP 50–150 mmHg — cerebral arterioles dilate as CPP falls and constrict as CPP rises, maintaining CBF at ~50 mL/100g/min. This is cerebral autoregulation: intrinsic vascular tone adjustment that decouples blood flow from perfusion pressure across a wide CPP range.
| Below CPP 50 mmHg: CBF FALLS proportionally with CPP — arterioles are maximally dilated and cannot compensate further. This pressure-passive (ischemic) zone is where every drop in MAP or rise in ICP directly reduces cerebral perfusion.
→ CCRN KEY: Normal CPP = 60–100 mmHg (MAP − ICP). Within the plateau zone, modest MAP changes do not alter CBF — autoregulation buffers the brain. Outside the plateau (CPP &lt;50 or &gt;150), CBF becomes perfusion-pressure dependent. In critical illness — TBI, SAH, severe hypertension — autoregulation can fail, shifting the entire curve or eliminating the plateau.
→ MASTERY NOTE: The upper limit (~150 mmHg) marks hypertensive breakthrough: arterioles can no longer prevent high-pressure flow into brain tissue → forced hyperemia → cerebral edema → hypertensive encephalopathy, PRES (posterior reversible encephalopathy syndrome). PRES presents with headache, seizures, visual changes, and cortical/subcortical T2 hyperintensity on MRI — treated with aggressive BP reduction.""",
 'tier-review','Ph4 · \U0001f7e0 T2 · Neurology — Stroke & TBI',
 DID['stroke_tbi'],'cerebralautoregulation','{"cpp":70}','chart-l1'),

("Move the CPP slider to 40 mmHg (ischemia zone). In severe TBI, cerebral autoregulation is often IMPAIRED — CBF becomes _______ at CPP values that would normally be well-compensated. The primary cellular mechanism causing autoregulatory failure after TBI is _______.",
 """CBF becomes PRESSURE-PASSIVE at CPP values well above 50 mmHg — in TBI, autoregulatory failure means even a CPP of 60-70 may produce inadequate or unpredictable CBF, depending on regional injury patterns.
| Mechanism of autoregulatory failure: DISRUPTED VASCULAR REACTIVITY from TBI — direct injury to cerebrovascular endothelium and smooth muscle cells impairs myogenic tone. Concurrent inflammatory mediators (IL-1β, TNF-α), mitochondrial dysfunction, blood-brain barrier breakdown, and local acidosis abolish the ability of arterioles to constrict or dilate in response to CPP changes. The vessels become 'stiff' and non-reactive.
| Consequence: the entire Monro-Kellie curve also shifts — any CPP drop triggers reflex cerebral vasodilation (attempting to restore flow) → ↑cerebral blood volume → ↑ICP → further ↓CPP — a vicious cycle that accelerates toward herniation.
→ CCRN KEY: Pressure reactivity index (PRx): correlates MAP waves with ICP waves over time. If autoregulation is intact, ICP and MAP are UNCORRELATED (brain resists pressure fluctuations). If impaired, ICP tracks MAP directly (pressure-passive). PRx &gt;0.25 consistently = impaired autoregulation = need tighter CPP control. Emerging TBI management tool.
→ MASTERY NOTE: Autoregulatory failure is not all-or-nothing — it varies by brain region and injury severity. A TBI patient may have intact autoregulation globally but focal pressure-passive zones in the pericontusional area. This is why 'safe' CPP targets from population studies may not protect every patient individually. PRx-guided individualized CPP targets (the 'optimal CPP' concept) are an active research area in neurocritical care.""",
 'tier-high','Ph4 · \U0001f7e0 T2 · Neurology — Stroke & TBI',
 DID['stroke_tbi'],'cerebralautoregulation','{"cpp":40}','chart-l2'),

("A severe TBI patient: MAP 68 mmHg, ICP 32 mmHg. CPP = _______. BTF guideline CPP target for severe TBI: _______ mmHg. To reach target CPP 60 mmHg, you must raise MAP to at least _______ mmHg (assuming ICP unchanged), OR lower ICP to _______ mmHg (assuming MAP unchanged).",
 """CPP = MAP − ICP = 68 − 32 = 36 mmHg — critically below target, severe ischemia zone.
| BTF (Brain Trauma Foundation, 4th edition) CPP target: 60–70 mmHg. Floor = 60 mmHg minimum. Targets above 70 mmHg are NOT recommended — pursuing CPP &gt;70 with fluids/vasopressors without ICP reduction is associated with ↑ARDS risk without proven neurological benefit.
| To reach CPP 60 via MAP: MAP must be ≥ 60 + 32 = 92 mmHg. Vasopressors (norepinephrine first-line) titrated to MAP 92.
| To reach CPP 60 via ICP: ICP must fall to ≤ 68 − 60 = 8 mmHg. Osmotherapy (mannitol or HTS) + CSF drainage target.
| Most efficient approach: TREAT BOTH simultaneously — even partial success on each axis (e.g., MAP 80 + ICP 18 = CPP 62) achieves the target with lower vasopressor and osmotherapy doses.
→ CCRN KEY: Bedside CPP calculation is mandatory after every ICP reading. If ICP 25 and MAP 80 → CPP 55 → below target → notify team. Don't report ICP in isolation. HOB 30° neutral-position reduces ICP 5-10 mmHg in most patients and should be verified before any drug intervention.
→ MASTERY NOTE: The BTF guideline CPP 60-70 range is a population-derived target. Individual patients may have their 'optimal CPP' (PRx-guided) as high as 80 mmHg if their autoregulation is intact at that range. Targeting MAP aggressively in a patient with intact autoregulation may not improve CBF (autoregulation compensates), but in a patient with impaired autoregulation, every MAP increase directly raises CBF — reinforcing the importance of bedside autoregulation assessment.""",
 'tier-critical','Ph4 · \U0001f7e0 T2 · Neurology — Stroke & TBI',
 DID['stroke_tbi'],'cerebralautoregulation','{"cpp":36}','chart-l3'),

("TBI patient: MAP 80, ICP 25, CPP 55 mmHg. Mannitol 0.5 g/kg IV is given. ICP drops to 18 mmHg, MAP stays at 80. New CPP = _______. Two mechanisms by which mannitol reduces ICP: _______ and _______. Mannitol is contraindicated when serum osmolality exceeds _______ mOsm/kg.",
 """New CPP = 80 − 18 = 62 mmHg — now within target (60-70 mmHg). A 7 mmHg ICP reduction yields a 7 mmHg CPP gain without any vasopressor use.
| Mannitol mechanism 1 — OSMOTIC: creates an osmotic gradient between blood (↑osmolality) and brain interstitium → draws free water from edematous brain into vascular space → reduces cerebral edema and ICP. Onset: 15–30 min. Duration: 2–6 hours.
| Mannitol mechanism 2 — RHEOLOGICAL: reduces blood viscosity → ↑cerebral microvascular flow → cerebral arteriolar autoregulatory vasoconstriction (response to ↑flow) → ↓cerebral blood volume → ↓ICP. Onset: immediate (minutes). Effect transient.
| Contraindication: serum osmolality &gt;320 mOsm/kg — additional mannitol cannot establish an adequate osmotic gradient and risks hyperosmolar renal tubular injury and electrolyte crisis.
→ CCRN KEY: Mannitol monitoring: check serum osmolality + osmol gap (measured minus calculated; normal &lt;10 mOsm/kg) every 4-6 hours. Hold mannitol if osmolality &gt;320 OR osmol gap &gt;20. Also: monitor serum Na (hypernatremia risk), urine output (osmotic diuresis → hypovolemia → ↓MAP → ↓CPP — the very thing you're trying to fix), and ICP response within 30 min.
→ MASTERY NOTE: HTS (hypertonic saline) vs mannitol: HTS (3% NaCl infusion or 23.4% NaCl bolus) reduces ICP via the same osmotic mechanism but WITHOUT osmotic diuresis. Advantage in hypotensive TBI: HTS expands intravascular volume (raises MAP) while reducing ICP — a double benefit. HTS sodium target: 145–155 mEq/L. HTS is the preferred osmotherapy in hemodynamically unstable TBI patients or when mannitol-related diuresis would compromise MAP.""",
 'tier-critical','Ph4 · \U0001f7e0 T2 · Neurology — Stroke & TBI',
 DID['stroke_tbi'],'cerebralautoregulation','{"cpp":55}','chart-l3'),

# ══ ICP Waveforms (4 cards) ════════════════════════════════════════════════════
("Select 'A Waves' on the ICP waveform chart. A waves (plateau waves) are characterized by amplitude _______ mmHg, duration _______ minutes, and represent _______. They are clinically significant because _______.",
 """A waves: AMPLITUDE 50–100 mmHg (dramatic spike from ICP baseline), DURATION 5–20 minutes (sustained plateau, not brief). Each A wave represents a VASODILATORY CASCADE: rising ICP → ↓CPP → reflex cerebral vasodilation (attempting to maintain CBF) → ↑cerebral blood volume → ↑ICP further → positive feedback → sustained plateau elevation.
| Clinically significant because: A waves indicate CRITICAL LOSS OF COMPENSATORY RESERVE and IMMINENT HERNIATION RISK. During each plateau wave, CPP may fall to near zero — the brain is in severe ischemia for 5-20 minutes per episode. Without immediate intervention, repeated A waves precede transtentorial herniation.
| The A wave precursor: sustained B waves (warning phase) → A waves (critical phase). The transition signals the patient has crossed the inflection point of the Monro-Kellie volume-pressure curve — exhausted compensation.
→ CCRN KEY: When A waves appear: (1) NOTIFY neurosurgery/attending IMMEDIATELY, (2) If EVD in place → drain CSF per protocol (5-10 mL), (3) Osmotherapy if not recently given, (4) Confirm HOB 30° neutral head position, (5) Verify adequate sedation (agitation drives ICP), (6) Check EVD for obstruction or migration. Do all of these simultaneously — A waves are not 'wait and see.'
→ MASTERY NOTE: Distinguishing true A waves from artifact: true A waves are SUSTAINED (5-20 min), have a characteristic 'plateau' shape with a sharp rise and fall, correlate with ↓CPP and possible clinical changes (pupil dilation, posturing, Cushing response). Artifacts from line flushing, patient movement, or coughing are BRIEF (&lt;1-2 min), don't have the plateau morphology, and don't correlate with sustained hemodynamic changes.""",
 'tier-review','Ph4 · \U0001f7e0 T2 · Neurology — ICP & Neuro Crisis',
 DID['icp_neuro'],'icpwaveforms','{"mode":"A"}','chart-l1'),

("Select 'B Waves.' B waves occur at _______ cycles/minute and amplitude _______. Clinically, sustained B waves indicate _______ and often PRECEDE _______. C waves occur at _______ cycles/minute and have _______ clinical significance compared to A or B waves.",
 """B waves: FREQUENCY 0.5–2 cycles/minute (one wave every 30 seconds to 2 minutes), AMPLITUDE 10–30 mmHg above baseline — less dramatic than A waves but rhythmically recurring.
| Clinically, sustained B waves indicate REDUCED INTRACRANIAL COMPLIANCE (the brain is on the ascending slope of the volume-pressure curve — compensation is diminishing). B waves often PRECEDE A WAVES — they are the warning phase. A patient showing persistent B wave activity is at risk of acute ICP decompensation with any additional volume insult (fever, agitation, ETT suctioning).
| C waves: FREQUENCY 4–8 cycles/minute, amplitude up to 20 mmHg. C waves reflect normal cardiorespiratory interactions (Traube-Hering-Mayer vasomotor rhythms). LEAST CLINICAL SIGNIFICANCE — they represent physiological variability rather than pathological ICP dynamics and do not require escalated intervention.
→ CCRN KEY: ICP wave severity hierarchy: A waves (emergency) &gt; B waves (warning/monitor closely) &gt; C waves (monitor). Document waveform character in nursing notes — 'ICP 18-22 mmHg with B-wave morphology' communicates the trajectory and compliance state to the team. A flat, non-pulsatile ICP waveform may also indicate CATHETER OBSTRUCTION — requires troubleshooting (flush, reposition).
→ MASTERY NOTE: The pulsatile ICP waveform has three components on each cardiac beat: P1 (percussion wave — arterial pulse transmission), P2 (tidal wave — brain compliance indicator), P3 (dicrotic wave — venous). Normal: P1 &gt; P2 &gt; P3. When intracranial compliance decreases: P2 rises and may exceed P1 (the waveform appears 'rounded' with a dominant second peak). A P2 &gt; P1 ratio signals early compliance loss — often visible before B or A waves develop — and should prompt reassessment of all ICP-reducing interventions.""",
 'tier-high','Ph4 · \U0001f7e0 T2 · Neurology — ICP & Neuro Crisis',
 DID['icp_neuro'],'icpwaveforms','{"mode":"B"}','chart-l2'),

("ICP monitor: baseline 22 mmHg, recurring A waves to 78 mmHg lasting 8 minutes. MAP is 85 mmHg. During a plateau wave, CPP = _______. The fastest bedside ICP-reducing intervention if EVD is in place: _______. The clinical triad of HYPERTENSION + BRADYCARDIA + IRREGULAR RESPIRATIONS is called _______ and indicates _______.",
 """During A wave: CPP = MAP − ICP = 85 − 78 = 7 mmHg — essentially zero cerebral perfusion during each 8-minute episode. Profound ischemia. Multiple A waves = cumulative ischemic injury.
| Fastest bedside intervention with EVD: DRAIN CSF — open the EVD at the prescribed drainage level, allow 5-10 mL to drain, reassess ICP immediately. Removing even a small CSF volume descends the volume-pressure curve back into the compensated zone, breaking the vasodilatory cascade. Effect is immediate (within seconds to minutes of drainage). Document: volume drained, ICP before/after, patient response.
| HYPERTENSION + BRADYCARDIA + IRREGULAR RESPIRATIONS = CUSHING'S TRIAD — indicates BRAINSTEM COMPRESSION from impending or active transtentorial herniation. The brainstem becomes ischemic from ICP-mediated compression → autonomic storm: massive sympathetic discharge (hypertension), then vagal reflex (bradycardia), and loss of respiratory centers (Biot's or ataxic breathing). Cushing's triad is a PRE-TERMINAL finding.
→ CCRN KEY: Response to Cushing's triad: call rapid response/code team immediately. Simultaneously: (1) Drain EVD if in place, (2) Hyperventilate to PaCO₂ 30-35 mmHg (bag-valve mask if not intubated, or manually ↑RR on vent), (3) Mannitol or 23.4% NaCl bolus, (4) Notify neurosurgery for emergent surgical decompression. Every minute of herniation increases irreversible brainstem damage.
→ MASTERY NOTE: Unilateral pupil dilation in herniation: the uncus (medial temporal lobe) herniates through the tentorial notch → compresses CN III (oculomotor nerve) on the IPSILATERAL side → dilated, non-reactive pupil on the SAME SIDE as the herniation/expanding lesion. Contralateral hemiparesis (corticospinal tract compression). BILATERAL fixed dilated pupils = bilateral herniation = very poor prognosis.""",
 'tier-critical','Ph4 · \U0001f7e0 T2 · Neurology — ICP & Neuro Crisis',
 DID['icp_neuro'],'icpwaveforms','{"mode":"A"}','chart-l3'),

("Refractory ICP (&gt;25 mmHg despite tier-1 measures). Select A Waves. Tier-2 escalation options include _______ (reduces cough/Valsalva-driven ICP spikes) and SHORT-TERM hyperventilation to PaCO₂ _______. Hyperventilation is limited to short-term use because _______. The third-line 'rescue' sedation strategy targeting metabolic suppression: _______.",
 """Tier-2 escalation (refractory ICP despite HOB/positioning/sedation/EVD/osmotherapy):
| NEUROMUSCULAR BLOCKADE (NMBAs) — cisatracurium or vecuronium — eliminates spontaneous movement, coughing, and Valsalva responses that cause ICP spikes. Continuous EEG monitoring recommended during NMBA use (can no longer assess neurological exam). Requires PRN analgesic coverage (paralyzed ≠ sedated or pain-free).
| SHORT-TERM HYPERVENTILATION to PaCO₂ 30–35 mmHg — lowers CO₂ → cerebral arteriolar vasoconstriction → ↓cerebral blood volume → ↓ICP within 30–60 seconds. Bridge therapy during acute crisis.
| Hyperventilation limited to short-term (&lt;4 hours) because: VASOCONSTRICTION → CEREBRAL ISCHEMIA in areas already hypoperfused. Additionally, CSF bicarbonate equilibrates to the new PaCO₂ within hours → vasoconstrictive effect wanes → ICP rebounds. Prophylactic hyperventilation is CONTRAINDICATED in TBI.
| Third-line rescue: HIGH-DOSE BARBITURATE COMA (pentobarbital) — metabolic suppression → ↓CMRO₂ (cerebral metabolic rate for oxygen) → autoregulatory ↓CBF → ↓ICP. Requires continuous EEG monitoring for burst suppression. Major risk: profound hypotension requiring vasopressors. Reserved for refractory ICP with salvageable injury.
→ CCRN KEY: Decompressive craniectomy — surgical removal of a bone flap — directly reduces ICP by allowing outward brain expansion. Evidence supports it for malignant MCA infarction (DESTINY-I/II trials: mortality benefit in selected patients &lt;60 years) and severe TBI. The DECRA trial in diffuse TBI showed reduced ICP but no functional outcome benefit. Neurosurgery decision.
→ MASTERY NOTE: Targeted temperature management (TTM) as ICP therapy: cooling to 32-35°C reduces CMRO₂ by ~5-7% per 1°C → ↓CBF demand → ↓ICP. Practical use: TTM 35-36°C (moderate hypothermia) is often used as tier-2 ICP therapy. More aggressive cooling (&lt;34°C) has not shown outcome benefit in TBI RCTs and has higher complication rates (coagulopathy, pneumonia, arrhythmias).""",
 'tier-critical','Ph4 · \U0001f7e0 T2 · Neurology — ICP & Neuro Crisis',
 DID['icp_neuro'],'icpwaveforms','{"mode":"A"}','chart-l3'),

# ══ Monro-Kellie (3 cards) ════════════════════════════════════════════════════
("The Monro-Kellie doctrine states the total intracranial volume is _______. When a mass lesion (hematoma, edema) enlarges, the two compensatory mechanisms that maintain ICP are _______ displacement and _______ displacement.",
 """CONSTANT — the rigid skull creates a fixed total volume. Any new mass or volume increase in one compartment MUST be offset by a decrease in another, or ICP rises.
| Compensatory mechanism 1: CSF DISPLACEMENT — CSF is shunted from the cranial vault into the lumbar spinal subarachnoid space. This is the primary and largest early buffer. Approximately 20-30 mL of new volume can be accommodated before this mechanism is exhausted.
| Compensatory mechanism 2: CEREBRAL VENOUS BLOOD DISPLACEMENT — venous blood is pushed from the intracranial dural sinuses and cortical veins into the systemic jugular system. Smaller buffer than CSF (~10-15 mL).
| Together these two mechanisms maintain ICP in the normal range (5-15 mmHg) until capacity is exceeded — then ICP rises exponentially. Brain tissue is the LEAST compressible compartment and cannot be displaced without fatal herniation.
→ CCRN KEY: Interventions map directly onto the doctrine: EVD CSF drainage (removes CSF volume), osmotherapy (reduces brain tissue water), head elevation to promote venous drainage (facilitates venous blood displacement), hyperventilation (causes vasoconstriction → ↓cerebral blood volume → frees venous reserve). Every ICP intervention targets one of the three compartments.
→ MASTERY NOTE: Normal adult intracranial volumes: brain tissue ~1400 mL (80%), CSF ~150 mL (10%), cerebral blood ~150 mL (10%). Of the CSF and blood compartments, only ~20-30 mL total can be displaced before decompensation. This small reserve explains why even modest hematoma expansion or cerebral edema can cause catastrophic ICP rises.""",
 'tier-review','Ph4 · \U0001f7e0 T2 · Neurology — ICP & Neuro Crisis',
 DID['icp_neuro'],'monrokellie','{}','chart-l1'),

("Advance the volume slider to 30 mL. ICP is now approximately _______ mmHg. Compare to ICP at 10 mL (approximately _______ mmHg). The 10-mL increase from 20 mL to 30 mL raises ICP far more than from 0 to 10 mL. This disproportionate rise reflects _______, the inverse of intracranial compliance.",
 """At 30 mL added volume: ICP ≈ 18-22 mmHg (entering the steep decompensated zone). At 10 mL: ICP ≈ 6-8 mmHg (still in the flat compensated zone). A 20 mL increase (10→30 mL) nearly triples ICP — while the same volume from 0→20 mL barely raises it above baseline.
| ELASTANCE (dP/dV) — the pressure rise per unit volume added. In the compensated zone: LOW elastance (high compliance — large ΔV causes minimal ΔP). At and beyond the inflection point: HIGH elastance (low compliance — tiny ΔV causes massive ΔP). The curve's exponential shape reflects rapidly rising elastance as reserves are exhausted.
| Clinical implication: a patient on the steep portion of the curve has NO RESERVE. Any additional volume insult — ETT suctioning, coughing, position change without sedation, fever — can trigger a plateau A wave. The absolute ICP value alone is insufficient; TREND and COMPLIANCE STATE determine actual risk.
→ CCRN KEY: Intracranial elastance test (clinical): inject 1 mL sterile saline into the ICP monitor and observe the pressure response. Normal (compliant): &lt;2 mmHg rise per mL. Concerning: 2-5 mmHg/mL. High elastance (decompensated): &gt;5 mmHg/mL — patient cannot tolerate any further volume. Requires physician order. Used to guide the urgency of ICP-reducing interventions.
→ MASTERY NOTE: The inflection point on the Monro-Kellie curve (~20-25 mL in this model) corresponds clinically to the moment CSF and venous displacement are exhausted. Recognition: ICP waveform changes from P1-dominant to P2-dominant (rounded morphology), baseline ICP creeps upward into the 15-20 range, and B waves appear. These are the pre-decompensation signals — act before the curve goes vertical.""",
 'tier-high','Ph4 · \U0001f7e0 T2 · Neurology — ICP & Neuro Crisis',
 DID['icp_neuro'],'monrokellie','{"vol":30}','chart-l2'),

("SAH patient: ICP 28 mmHg, EVD minimal drainage (compressed ventricles). Per Monro-Kellie, lowering ICP requires reducing _______ or _______ volume. Preferred osmotherapy for SAH (over mannitol): _______, because mannitol causes _______ which is dangerous in SAH due to _______.",
 """Per Monro-Kellie, to lower ICP: reduce CEREBRAL BLOOD VOLUME (vasoconstriction, reduce venous engorgement) or reduce BRAIN TISSUE WATER (osmotherapy to draw out edema). CSF drainage is unavailable (ventricles compressed). Brain tissue itself cannot be reduced without surgery.
| Preferred osmotherapy for SAH: HYPERTONIC SALINE (3% NaCl infusion or 23.4% NaCl bolus) rather than mannitol.
| Why not mannitol in SAH: mannitol causes OSMOTIC DIURESIS → hypovolemia → ↓MAP → ↓CPP. In SAH, HYPOVOLEMIA IS ESPECIALLY DANGEROUS because: (1) reduced circulating volume worsens cerebral vasospasm (vasospasm risk peaks days 4-14 post-SAH), and (2) hypovolemia drops MAP needed for CPP in a patient who may already have impaired autoregulation from the bleed.
| HTS raises serum Na → osmotic gradient → draws water from brain → ↓ICP without volume depletion. Sodium target: 145-155 mEq/L. HTS also provides mild volume expansion (beneficial in SAH).
→ CCRN KEY: SAH vasospasm monitoring window: days 4-14 after ictus. ALL SAH patients receive nimodipine 60 mg q4h (PO or NG) — reduces vasospasm morbidity even if it doesn't reduce angiographic spasm. Nursing: report ANY new neurological deficit immediately during this window (new focal weakness, ↓LOC, speech change). TCD velocities (MCA &gt;120 cm/s = mild, &gt;200 = severe) monitored daily.
→ MASTERY NOTE: The 'triple H' therapy (hypertension-hypervolemia-hemodilution) for SAH vasospasm has largely been replaced by EUVOLEMIA + INDUCED HYPERTENSION in current practice. Why: hypervolemia risks pulmonary edema and cardiac stress with no proven CBF benefit over euvolemia alone. Current approach: maintain euvolemia, allow permissive or induced hypertension (MAP 80-120+ mmHg per protocol) for symptomatic vasospasm, and proceed to endovascular treatment (intra-arterial nimodipine, balloon angioplasty) for refractory vasospasm.""",
 'tier-critical','Ph4 · \U0001f7e0 T2 · Neurology — ICP & Neuro Crisis',
 DID['icp_neuro'],'monrokellie','{"vol":25}','chart-l3'),

# ══ CPP Interactive (3 cards) ═════════════════════════════════════════════════
("Set MAP 85, ICP 22 on the CPP chart: CPP = _______. Now set MAP 65, ICP 18: CPP = _______. BTF target for severe TBI is CPP _______ mmHg. CPP can be raised by either _______ MAP or _______ ICP — and treating ICP is preferred because _______.",
 """CPP = MAP − ICP = 85 − 22 = 63 mmHg (target range, acceptable). CPP = 65 − 18 = 47 mmHg — BELOW TARGET, ischemia zone, requires immediate intervention.
| BTF target: CPP 60–70 mmHg for severe TBI. Minimum floor: 60 mmHg. Avoid &gt;70 mmHg via aggressive fluid/vasopressor use (ARDS risk without proven neurological benefit).
| Raising CPP: INCREASING MAP (vasopressors — norepinephrine first-line) OR DECREASING ICP (osmotherapy, EVD drainage, HOB 30°, sedation/analgesia).
| Treating ICP is preferred because: (1) It directly addresses the PATHOLOGY (brain swelling, hydrocephalus, hematoma) rather than compensating around it. (2) Lowering ICP also improves cerebrovascular compliance, reducing further ICP spikes. (3) Raising MAP via vasopressors increases cardiac afterload and systemic pressure — with normal autoregulation, this just causes cerebral vasoconstriction without improving CBF. (4) Every 1 mmHg ICP reduction = 1 mmHg CPP gain with no vascular side effects.
→ CCRN KEY: Bedside CPP reflex: after every ICP reading, calculate CPP = MAP − ICP. If CPP &lt;60 → notify provider immediately. Do not report ICP alone to the team — always include both values: 'ICP is 28, MAP is 80, CPP is 52 — below our target of 60.'
→ MASTERY NOTE: 'MAP-first' vs 'ICP-first' debate: in a patient with MAP 60 and ICP 25 (CPP 35), increasing MAP via norepinephrine to 90 achieves CPP 65 — but if autoregulation is intact, cerebral vessels vasoconstrict in response to the higher MAP and CBF may not actually improve. Confirming autoregulation status (PRx, TCD reactivity) guides the optimal strategy.""",
 'tier-review','Ph4 · \U0001f7e0 T2 · Neurology — ICP & Neuro Crisis',
 DID['icp_neuro'],'cppinteractive','{"map":85,"icp":22}','chart-l1'),

("Set MAP 70, ICP 35. CPP = _______. This CPP is CRITICAL. The diagnosis producing ICP 35 despite MAP 70 in a post-cardiac arrest patient is _______. Two physiologic drivers of ICP elevation after global ischemia-reperfusion: _______ and _______.",
 """CPP = 70 − 35 = 35 mmHg — severe ischemia zone, emergency.
| Post-cardiac arrest with ICP 35: CYTOTOXIC CEREBRAL EDEMA from global ischemia-reperfusion injury — after cardiac arrest, global cerebral ischemia → ATP depletion → Na/K-ATPase failure → intracellular Na and water accumulation → neuronal swelling (cytotoxic edema). Unlike vasogenic edema (BBB breakdown), cytotoxic edema does NOT respond well to steroids or mannitol because the problem is intracellular, not interstitial.
| Driver 1: CYTOTOXIC EDEMA — neuronal swelling from ischemia-reperfusion, free radical injury, glutamate excitotoxicity. Peaks at 24-72 hours post-arrest.
| Driver 2: POST-ISCHEMIC HYPEREMIA — following ROSC, loss of cerebrovascular autoregulation → pressure-passive CBF → hyperemia → ↑cerebral blood volume → ↑ICP. Avoiding MAP &gt;100 mmHg (prevents forced hyperemia) and normocapnia (PaCO₂ 35-45 mmHg, avoids vasodilation from hypercapnia) reduces this driver.
→ CCRN KEY: Post-ROSC hemodynamic targets: MAP ≥65-70 mmHg (some centers target ≥70-80 for neuroprotection), avoid MAP &gt;100 (hyperemia risk), SpO₂ 94-98% (avoid hyperoxia — oxidative injury), PaCO₂ 35-45 mmHg (avoid hyper- and hypoventilation), temperature 33-36°C per TTM protocol for comatose survivors.
→ MASTERY NOTE: TTM (targeted temperature management) at 33-36°C for 24 hours after cardiac arrest: reduces CMRO₂ (5-7% per °C) → limits ischemia-reperfusion injury → reduces post-arrest cerebral edema and ICP. TTM 36°C vs 33°C (TTM trial, NEJM 2013): no significant difference in mortality or neurological outcome — most centers now use 36°C with strict fever avoidance (&lt;37.5°C for 72 hours) to avoid the complications of deeper cooling (coagulopathy, bradycardia, pneumonia risk).""",
 'tier-high','Ph4 · \U0001f7e0 T2 · Neurology — ICP & Neuro Crisis',
 DID['icp_neuro'],'cppinteractive','{"map":70,"icp":35}','chart-l2'),

("Set MAP 90, ICP 40. CPP = _______. This patient has a blown right pupil and posturing. Herniation pattern: _______ (side). Three simultaneous nursing interventions: _______, _______, and _______. If ICP does not respond to EVD drainage + osmotherapy, the emergent surgical option is _______.",
 """CPP = 90 − 40 = 50 mmHg — below target. With herniation signs, the clinical situation is a neurological emergency.
| Blown right pupil + right-sided herniation signs: UNCAL HERNIATION — right temporal lobe uncus herniates through the tentorium → compresses RIGHT CN III → right pupil dilates and becomes non-reactive. LEFT-sided motor deficit expected (right cerebral hemisphere → left corticospinal tract). Exception: Kernohan's notch (contralateral peduncle compression against tentorium → ipsilateral motor signs, a false localizing sign).
| Three simultaneous nursing interventions:
  (1) NOTIFY NEUROSURGERY AND ATTENDING EMERGENTLY — herniation is a surgical/medical emergency, every minute matters
  (2) DRAIN CSF VIA EVD if in place (open at prescribed level, drain 5-10 mL) — fastest ICP reduction available at the bedside
  (3) EMERGENT HYPERVENTILATION to PaCO₂ 30-35 mmHg — adjust ventilator RR or manually bag — immediate cerebral vasoconstriction ↓ICP in 30-60 seconds. Bridge therapy only.
| Emergent surgical option: DECOMPRESSIVE CRANIECTOMY — removal of a bone flap to allow outward brain expansion, directly breaking the fixed-volume constraint of the Monro-Kellie doctrine. Indicated for malignant MCA infarction, refractory TBI ICP, and some large intracerebral hemorrhages.
→ CCRN KEY: The ICP management 'toolkit' in order: (1) HOB/positioning, (2) Sedation/analgesia optimization, (3) EVD drainage, (4) Osmotherapy, (5) NMBA, (6) Short-term hyperventilation, (7) Barbiturate coma / TTM, (8) Craniectomy. Herniation signs jump you to simultaneous items 3+6 with immediate surgical consultation.
→ MASTERY NOTE: Mannitol vs 23.4% NaCl for acute herniation: 23.4% NaCl 30 mL IV bolus (via central line ONLY) achieves an osmotic effect within 10-15 minutes — often used as the fastest osmotherapy for acute herniation. Mannitol 1 g/kg IV also works but requires larger volume. Central access required for 23.4% NaCl due to extreme tonicity (the peripheral vein risks thrombophlebitis and tissue necrosis if extravasation occurs).""",
 'tier-critical','Ph4 · \U0001f7e0 T2 · Neurology — ICP & Neuro Crisis',
 DID['icp_neuro'],'cppinteractive','{"map":90,"icp":40}','chart-l3'),

# ══ RASS Scale (3 cards) ══════════════════════════════════════════════════════
("On the RASS chart, RASS 0 means _______. A mechanically ventilated patient with RASS −3 responds to _______. SCCM PADIS 2018 recommends targeting RASS _______ for most ICU patients on mechanical ventilation, because lighter sedation reduces _______.",
 """RASS 0: ALERT AND CALM — spontaneously awake, attentive, cooperative. Not agitated, not drowsy.
| RASS −3 (Moderate Sedation): patient has MOVEMENT OR EYE OPENING TO VOICE but WITHOUT sustained eye contact. They respond to verbal stimulation but do not follow commands or maintain focus. The key distinction from −2 (eye contact &lt;10 sec) and −4 (requires physical stimulus).
| PADIS 2018 recommended target: RASS −1 TO 0 (LIGHT SEDATION) for most mechanically ventilated ICU patients. Deep sedation (RASS −3 to −5) should be avoided unless specific indications exist (severe ARDS requiring prone/paralysis, refractory ICP crisis, status epilepticus, extreme agitation with safety risk).
| Lighter sedation reduces: DURATION OF MECHANICAL VENTILATION (↓ventilator days by ~1-2 days in RCTs), ICU LENGTH OF STAY, DELIRIUM INCIDENCE (deep sedation is an independent risk factor for delirium), and 90-DAY MORTALITY (multiple meta-analyses show benefit of light sedation protocols).
→ CCRN KEY: RASS assessment steps: (1) Observe patient for 30 seconds → if agitated → assign +1 to +4. (2) Call patient's name loudly → alert/calm = 0; drowsy opens eyes = −1; opens eyes briefly &lt;10 sec = −2; movement/no eye contact = −3. (3) Physical stimulus (shoulder shake or sternal rub) → movement = −4; no response = −5. Document RASS each nursing assessment.
→ MASTERY NOTE: RASS vs SAS (Sedation-Agitation Scale): SAS scores 1 (unarousable) to 7 (dangerous agitation), with 4 = calm/cooperative. Both are validated per PADIS. RASS is more widely used and research-validated. SAS 3 ≈ RASS −2; SAS 4 ≈ RASS 0. When transferring from another institution or interpreting prior documentation, clarify which scale was used — a 'sedation score of 3' means very different things in SAS vs GCS.""",
 'tier-review','Ph4 · \U0001f7e0 T2 · Neurology — Delirium & Behavioral',
 DID['delirium'],'rassscale','{"target":0}','chart-l1'),

("Highlight RASS −2 (ventilated target). A patient is RASS +2, pulling at the ETT. Per PADIS 'analgesia-first' approach, before escalating sedation you first assess and treat _______. Delirium screening tool for this patient: _______. Minimum RASS required to administer it: _______.",
 """Before escalating sedation: ASSESS AND TREAT PAIN — the PADIS 'A1C' framework (Analgesia → Sedation → Comfort/delirium management). Pain is the most common, most undertreated driver of ICU agitation. A patient receiving propofol escalation without analgesia remains painful but harder to assess — catecholamine surge, tachycardia, and hypertension persist despite apparent 'sedation.'
| Validated pain tools: NRS (0-10 numeric) if communicative; CPOT (Critical-care Pain Observation Tool: 0-8, score ≥3 = significant pain) or BPS (Behavioral Pain Scale: 3-12, score ≥6 = pain) if non-communicative/intubated. Treat pain FIRST, THEN reassess RASS.
| Delirium screening: CAM-ICU (Confusion Assessment Method for ICU). Requires RASS ≥ −3 — patient must be arousable enough to participate in the inattention test (squeeze my hand when you hear letter 'A' in a sequence). RASS −4 or −5 → delirium cannot be assessed → document 'UNABLE TO ASSESS.'
| CAM-ICU positive = Features 1 (acute/fluctuating) + 2 (inattention) BOTH present, PLUS Feature 3 (altered LOC, RASS ≠ 0) OR Feature 4 (disorganized thinking).
→ CCRN KEY: Treating the RASS +2 patient: (1) Assess pain — give analgesic, reassess in 30 min. (2) If still agitated → investigate cause: hypoxia, urinary retention, ETT migration, full bladder, ICU psychosis, reorientation. (3) THEN consider sedation escalation. Skipping to propofol bolus may mask a critical problem (ETT obstruction, acute respiratory distress) that requires immediate clinical intervention, not sedation.
→ MASTERY NOTE: PADIS ABCDEF bundle evidence: Barnes (ICM 2019) meta-analysis — bundle implementation reduces delirium by 25%, coma duration by 30%, ICU mortality by 32%, and 90-day rehospitalization. The bundle works as a PACKAGE: awakening (A) + breathing coordination (B) + delirium monitoring (C) + early mobility (E) + family engagement (F) are interdependent. A patient liberated from the ventilator earlier (AB) has less sedation exposure, less delirium (C), and more opportunity for mobility (E).""",
 'tier-high','Ph4 · \U0001f7e0 T2 · Neurology — Delirium & Behavioral',
 DID['delirium'],'rassscale','{"target":-2}','chart-l2'),

("A post-op day 2 patient is intubated, RASS −4, on propofol 40 mcg/kg/min + fentanyl 50 mcg/hr. CAM-ICU is _______. The ABCDEF 'A' bundle intervention is the SAT. During a SAT, _______ is held while _______ is continued. SAT PASS criterion for RASS: _______ or better for ≥5 minutes. Daily SAT + SBT reduces mechanical ventilation by _______ days.",
 """CAM-ICU: UNABLE TO ASSESS — the patient is at RASS −4 (deep sedation), cannot participate in the inattention test. Delirium cannot be ruled in or out. This is clinically significant: deep sedation itself is a major delirium risk factor, and the patient cannot demonstrate delirium while deeply sedated.
| SAT (Spontaneous Awakening Trial): HOLD SEDATION (propofol, benzodiazepines, dexmedetomidine — all sedative agents) while CONTINUING ANALGESIA (fentanyl continued at reduced dose or maintenance rate). Analgesics are NOT held during SAT — abrupt analgesia withdrawal causes acute pain → agitation → failed SAT with unclear cause.
| SAT PASS for RASS: patient achieves RASS −1 OR BETTER (opens eyes, light sedation or alert) for ≥5 minutes without: RASS ≥+2 agitation, respiratory distress (RR &gt;35, SpO₂ &lt;88%), acute arrhythmia, or device removal.
| If SAT passes → immediately coordinate SBT → combined daily SAT + SBT reduces mechanical ventilation by ~3 DAYS (Girard MENDS trial / SLEAP trial, NEJM 2008).
→ CCRN KEY: SAT FAIL: restart sedation at HALF prior dose (not full dose — avoid re-sedation overshoot). Document which criterion caused failure. Common causes: pain (increase analgesia before next SAT), agitation from hypoxia (check ventilator, SpO₂, ABG), delirium/hyperactive (address non-pharmacologically first — reorient, family presence, day/night lighting cycle).
→ MASTERY NOTE: Propofol infusion syndrome (PRIS): propofol &gt;4 mg/kg/hr (67 mcg/kg/min) for &gt;48 hours → metabolic acidosis (high anion gap), rhabdomyolysis, hepatomegaly, cardiac dysrhythmias (RBBB, ST changes), renal failure. Monitoring: triglycerides q24h (hold if &gt;400 mg/dL), CPK, urine color (myoglobinuria), lactate. At 40 mcg/kg/min (2.4 mg/kg/hr), this patient is below the threshold — but risk increases with prolonged duration, concurrent catecholamines/steroids, or carbohydrate restriction.""",
 'tier-critical','Ph4 · \U0001f7e0 T2 · Neurology — Delirium & Behavioral',
 DID['delirium'],'rassscale','{"target":-2}','chart-l3'),

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
