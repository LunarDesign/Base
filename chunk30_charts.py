#!/usr/bin/env python3
"""
Chunk 30 — Ph2 Respiratory: 5 charts × 3 levels = 15 cards
Charts: P-V Compliance, Flow-Volume Loop, V/Q Shunt, PE Severity, Auto-PEEP
Run: python chunk30_charts.py
"""
import sys, os, json, re, time, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card, SHARED_JS, CHART_CSS_ADDON, DID)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_29.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_30.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c30')
CHUNK_NUM   = 30
MID_BASE    = 1_800_004_000
CHART_ORDER = ['pvcompliancecurve', 'flowvolumeloop', 'vqshunt', 'peseverity', 'autopeep']

RF = {}

# ── Chart 1: P-V Compliance Curve ─────────────────────────────────────────────
RF['pvcompliancecurve'] = r"""
function _render(cv,ctrl,P){
  var W=cv.width,H=cv.height,ctx=cv.getContext('2d');if(!ctx)return;
  var mx=60,my=18,pw=W-mx-14,ph=H-my-50,xD=40,yD=900;
  var CURVES=[
    {label:'Normal',color:_TE,on:true,
     fn:function(P){var Vm=850,P50=12,k=5;return Vm/(1+Math.exp(-(P-P50)/k));}},
    {label:'Mild ARDS',color:_AM,on:false,
     fn:function(P){var Vm=500,P50=18,k=4;return Vm/(1+Math.exp(-(P-P50)/k));}},
    {label:'Severe ARDS',color:_RE,on:true,
     fn:function(P){var Vm=300,P50=24,k=3;return Vm/(1+Math.exp(-(P-P50)/k));}},
    {label:'Post-Recruitment',color:_GN,on:false,
     fn:function(P){var Vm=420,P50=20,k=3.5;return Vm/(1+Math.exp(-(P-P50)/k));}},
  ];
  var showVt=P.vt||420;
  function draw(){
    _cl(ctx,W,H);_gd(ctx,mx,my,pw,ph,5,40,100,900);_ax(ctx,mx,my,pw,ph);
    ctx.textAlign='center';
    [0,5,10,15,20,25,30,35,40].forEach(function(v){_lb(ctx,v,mx+(v/40)*pw,my+ph+15,_LB,10);});
    ctx.textAlign='right';
    [0,100,200,300,400,500,600,700,800,900].forEach(function(v){_lb(ctx,v,mx-6,my+ph-(v/900)*ph+4,_LB,10,'right');});
    _lb(ctx,'Airway Pressure (cmH₂O)',mx+pw/2,H-5,_LB,11);
    _rl(ctx,'Volume above FRC (mL)',14,my+ph/2);
    CURVES.forEach(function(c){
      if(!c.on)return;
      _crv(ctx,c.fn,0,40,mx,my,pw,ph,xD,yD,c.color,2.5);
      var endV=Math.min(yD,c.fn(38));
      _lb(ctx,c.label,mx+pw-4,my+ph-(endV/yD)*ph-6,c.color,10,'right');
      if(c.label.includes('ARDS')||c.label==='Post-Recruitment'){
        var lip=c.label.includes('Severe')?8:12;
        var uip=c.label.includes('Severe')?30:34;
        var lipY=c.fn(lip),uipY=c.fn(uip);
        ctx.setLineDash([3,3]);ctx.strokeStyle=c.color+'66';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(mx+(lip/40)*pw,my+ph-(lipY/yD)*ph);ctx.lineTo(mx+(lip/40)*pw,my+ph);ctx.stroke();
        ctx.beginPath();ctx.moveTo(mx+(uip/40)*pw,my+ph-(uipY/yD)*ph);ctx.lineTo(mx+(uip/40)*pw,my+ph);ctx.stroke();
        ctx.setLineDash([]);
        _lb(ctx,'LIP',mx+(lip/40)*pw,my+ph-4,c.color+'99',8);
        _lb(ctx,'UIP',mx+(uip/40)*pw,my+ph-4,c.color+'99',8);}});
    if(CURVES[0].on){
      var vtH=(showVt/yD)*ph;
      ctx.fillStyle=_TE+'11';
      ctx.fillRect(mx,my+ph/2-vtH/2,pw,vtH);
      _lb(ctx,'Vt '+showVt+' mL',mx+10,my+ph/2,_TE+'88',9,'left');}
  }
  draw();
  if(ctrl){ctrl.innerHTML='';var row=document.createElement('div');
    row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;align-items:center;';
    var sp=document.createElement('span');sp.textContent='CURVES: ';
    sp.style.cssText='font-size:10px;font-weight:800;color:#444;';row.appendChild(sp);
    CURVES.forEach(function(c){var b=_mkB(c.label,c.color,c.on,function(on){c.on=on;
      b.style.background=on?c.color+'22':'transparent';b.style.color=on?c.color:'#555';b._on=on;draw();});
      row.appendChild(b);});ctrl.appendChild(row);}}
"""

# ── Chart 2: Flow-Volume Loop ──────────────────────────────────────────────────
RF['flowvolumeloop'] = r"""
function _render(cv,ctrl,P){
  var W=cv.width,H=cv.height,ctx=cv.getContext('2d');if(!ctx)return;
  var mx=52,my=18,pw=W-mx-14,ph=H-my-50;
  var baseline=my+ph/2;
  var LOOPS=[
    {label:'Normal',color:_TE,on:true,
     VC:5.0,PEF:9.0,FEV1:4.0,
     expFn:function(v,VC,PEF){
       var f=v/VC;if(f<=0)return 0;
       if(f<0.12)return PEF*(f/0.12);
       return PEF*Math.pow(1-f,0.7)/(Math.pow(0.88,0.7));},
     inspFn:function(v,VC,PIF){return -(PIF||6)*Math.sin(Math.PI*(v/VC));}},
    {label:'Obstruction',color:_OR,on:false,
     VC:4.2,PEF:6.5,FEV1:2.0,
     expFn:function(v,VC,PEF){
       var f=v/VC;if(f<=0)return 0;
       if(f<0.18)return PEF*(f/0.18)*0.85;
       return PEF*0.85*Math.pow(1-f,1.8)/(Math.pow(0.82,1.8));},
     inspFn:function(v,VC,PIF){return -(PIF||5.5)*Math.sin(Math.PI*(v/VC));}},
    {label:'Restriction',color:_AM,on:false,
     VC:2.8,PEF:5.5,FEV1:2.4,
     expFn:function(v,VC,PEF){
       var f=v/VC;if(f<=0)return 0;
       if(f<0.12)return PEF*(f/0.12);
       return PEF*Math.pow(1-f,0.65)/(Math.pow(0.88,0.65));},
     inspFn:function(v,VC,PIF){return -(PIF||4.5)*Math.sin(Math.PI*(v/VC));}},
    {label:'Upper Airway Obstruction',color:_PU,on:false,
     VC:4.8,PEF:5.0,FEV1:3.5,
     expFn:function(v,VC,PEF){
       var f=v/VC;if(f<=0)return 0;
       if(f<0.12)return PEF*(f/0.12);
       return PEF*Math.pow(1-f,0.7)/(Math.pow(0.88,0.7));},
     inspFn:function(v,VC,PIF){return -(PIF||3.0);}}
  ];
  var maxVC=5.5,maxF=12;
  function toX(v){return mx+(v/maxVC)*pw;}
  function toY(f){return baseline-(f/maxF)*(ph/2);}
  function draw(){
    _cl(ctx,W,H);
    ctx.strokeStyle=_GR;ctx.lineWidth=1;
    [-6,-3,0,3,6,9].forEach(function(f){var y=baseline-(f/maxF)*(ph/2);
      ctx.beginPath();ctx.moveTo(mx,y);ctx.lineTo(mx+pw,y);ctx.stroke();});
    [0,1,2,3,4,5].forEach(function(v){var x=toX(v);
      ctx.beginPath();ctx.moveTo(x,my);ctx.lineTo(x,my+ph);ctx.stroke();});
    ctx.strokeStyle=_AX;ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(mx,my);ctx.lineTo(mx,my+ph);ctx.stroke();
    ctx.beginPath();ctx.moveTo(mx,baseline);ctx.lineTo(mx+pw,baseline);ctx.stroke();
    ctx.textAlign='center';
    [0,1,2,3,4,5].forEach(function(v){_lb(ctx,v,toX(v),my+ph+15,_LB,10);});
    ctx.textAlign='right';
    [-6,-3,3,6,9].forEach(function(f){if(f!==0)_lb(ctx,f,mx-6,toY(f)+4,_LB,10,'right');});
    _lb(ctx,'Volume Exhaled (L)',mx+pw/2,H-5,_LB,11);
    _rl(ctx,'Flow (L/s)  ↑ Expiration  ↓ Inspiration',14,my+ph/2);
    _lb(ctx,'Expiration →',mx+pw*0.75,my+10,'#333',9);
    _lb(ctx,'← Inspiration',mx+pw*0.75,my+ph-8,'#333',9);
    LOOPS.forEach(function(lp){
      if(!lp.on)return;
      ctx.strokeStyle=lp.color;ctx.lineWidth=2.5;
      ctx.beginPath();ctx.moveTo(toX(0),toY(0));
      for(var v=0;v<=lp.VC;v+=lp.VC/200){
        var f=lp.expFn(v,lp.VC,lp.PEF);
        ctx.lineTo(toX(v),toY(f));}
      ctx.stroke();
      ctx.beginPath();ctx.moveTo(toX(lp.VC),toY(0));
      for(var v2=0;v2<=lp.VC;v2+=lp.VC/100){
        var rv=lp.VC-v2;
        var f2=lp.inspFn(v2,lp.VC,lp.PEF*0.7);
        ctx.lineTo(toX(rv),toY(f2));}
      ctx.lineTo(toX(0),toY(0));ctx.stroke();
      _lb(ctx,lp.label+' VC='+lp.VC+'L',toX(lp.VC*0.5),toY(lp.PEF)+14,lp.color,10);});}
  draw();
  if(ctrl){ctrl.innerHTML='';var row=document.createElement('div');
    row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;align-items:center;';
    var sp=document.createElement('span');sp.textContent='PATTERN: ';
    sp.style.cssText='font-size:10px;font-weight:800;color:#444;';row.appendChild(sp);
    LOOPS.forEach(function(lp){var b=_mkB(lp.label,lp.color,lp.on,function(on){lp.on=on;
      b.style.background=on?lp.color+'22':'transparent';b.style.color=on?lp.color:'#555';b._on=on;draw();});
      row.appendChild(b);});ctrl.appendChild(row);}}
"""

# ── Chart 3: V/Q Shunt Effect on PaO2 ─────────────────────────────────────────
RF['vqshunt'] = r"""
function _render(cv,ctrl,P){
  var W=cv.width,H=cv.height,ctx=cv.getContext('2d');if(!ctx)return;
  var mx=58,my=18,pw=W-mx-14,ph=H-my-54,xD=60,yD=500;
  function calcPaO2(fio2,shuntPct){
    var Qs=shuntPct/100;
    var PAO2=fio2*713;
    var PaO2_vent=Math.min(PAO2*0.96,650);
    return Math.max(40,PaO2_vent*(1-Qs)+40*Qs);}
  var FIOS=[{fio2:0.21,color:'#555',label:'RA (21%)'},{fio2:0.40,color:_LB,label:'40%'},
    {fio2:0.60,color:_TE,label:'60%'},{fio2:1.00,color:_GN,label:'100% O₂'}];
  var state={shunt:P.shunt||30};
  function draw(){
    _cl(ctx,W,H);_gd(ctx,mx,my,pw,ph,10,60,100,500);_ax(ctx,mx,my,pw,ph);
    ctx.textAlign='center';
    [0,10,20,30,40,50,60].forEach(function(v){_lb(ctx,v+'%',mx+(v/60)*pw,my+ph+15,_LB,10);});
    ctx.textAlign='right';
    [0,100,200,300,400,500].forEach(function(v){_lb(ctx,v,mx-6,my+ph-(v/yD)*ph+4,_LB,10,'right');});
    _lb(ctx,'Intrapulmonary Shunt Fraction (%)',mx+pw/2,H-5,_LB,11);
    _rl(ctx,'PaO₂ (mmHg)',14,my+ph/2);
    [{'p':60,'l':'SpO₂ 90% threshold'},{'p':80,'l':'SpO₂ 95%'}].forEach(function(ref){
      var y=my+ph-(ref.p/yD)*ph;
      ctx.strokeStyle='#2a2a2a';ctx.lineWidth=1;ctx.setLineDash([4,3]);
      ctx.beginPath();ctx.moveTo(mx,y);ctx.lineTo(mx+pw,y);ctx.stroke();ctx.setLineDash([]);
      _lb(ctx,ref.l,mx+8,y-5,'#333',8,'left');});
    FIOS.forEach(function(fi){
      _crv(ctx,function(s){return calcPaO2(fi.fio2,s);},0,60,mx,my,pw,ph,xD,yD,fi.color,2);
      var endV=calcPaO2(fi.fio2,60);
      _lb(ctx,'FiO₂ '+fi.label,mx+pw-2,my+ph-(endV/yD)*ph,fi.color,9,'right');});
    var sx=mx+(state.shunt/60)*pw;
    ctx.strokeStyle=_RE+'88';ctx.lineWidth=1.5;ctx.setLineDash([5,3]);
    ctx.beginPath();ctx.moveTo(sx,my);ctx.lineTo(sx,my+ph);ctx.stroke();ctx.setLineDash([]);
    _lb(ctx,'Shunt '+state.shunt+'%',sx,my+10,_RE,10);
    FIOS.forEach(function(fi){
      var pao2=calcPaO2(fi.fio2,state.shunt);
      _dot(ctx,sx,my+ph-(pao2/yD)*ph,5,fi.color);
      _lb(ctx,Math.round(pao2),sx+18,my+ph-(pao2/yD)*ph+4,fi.color,9,'left');;});}
  draw();
  if(ctrl){ctrl.innerHTML='';var row=document.createElement('div');
    row.style.cssText='display:flex;flex-wrap:wrap;gap:12px;margin-top:8px;';
    row.appendChild(_mkS('Shunt %','0','55','1',state.shunt,
      function(v){return v+'%';},function(v){state.shunt=v;draw();}));
    ctrl.appendChild(row);}}
"""

# ── Chart 4: PE Severity Classification ───────────────────────────────────────
RF['peseverity'] = r"""
function _render(cv,ctrl,P){
  var W=cv.width,H=cv.height,ctx=cv.getContext('2d');if(!ctx)return;
  _cl(ctx,W,H);
  var rows=[
    {attr:'Hemodynamics',lr:'Stable\n(SBP ≥90 mmHg)',sm:'Stable\n(SBP ≥90 mmHg)',mas:'UNSTABLE\nSBP <90 or vasopressors'},
    {attr:'RV dysfunction\n(echo/CT)',lr:'None',sm:'Present\n(RV:LV >0.9, septal shift)',mas:'Severe\n(RV:LV >1.2, McConnell sign)'},
    {attr:'Biomarkers\n(Troponin/BNP)',lr:'Normal',sm:'↑ Troponin OR\n↑ BNP/NT-proBNP',mas:'↑↑ Both\n(massive myocardial strain)'},
    {attr:'30-day mortality',lr:'1–2%',sm:'3–15%',mas:'>25–50%'},
    {attr:'Primary treatment',lr:'Anticoagulation\n(LMWH/DOAC)',sm:'Anticoagulation\n± CDT/CDUA if high risk',mas:'SYSTEMIC THROMBOLYSIS\nor thrombectomy/ECMO'},
    {attr:'Thrombolysis',lr:'NOT indicated',sm:'Consider if deteriorating\nor high-risk features',mas:'STRONGLY INDICATED\nif no absolute contraindication'},
  ];
  var n=rows.length;
  var colW=(W-12)/4,rowH=(H-30)/n;
  var cols=[6,6+colW,6+colW*2,6+colW*3];
  [{label:'Parameter',c:'#1a1a1a'},{label:'Low-Risk PE',c:'#1a2a1a'},{label:'Submassive PE',c:'#2a2a1a'},{label:'Massive PE',c:'#2a1a1a'}].forEach(function(h,i){
    ctx.fillStyle=h.c;ctx.fillRect(cols[i],10,colW,rowH*0.85);
    ctx.fillStyle=i===0?_LB:i===1?_GN:i===2?_AM:_RE;
    ctx.font='bold '+(i===0?10:11)+'px -apple-system,sans-serif';ctx.textAlign='center';
    ctx.fillText(h.label,cols[i]+colW/2,10+rowH*0.58);});
  rows.forEach(function(r,i){
    var y=10+rowH*(i+0.9);
    ctx.fillStyle=i%2===0?'#0d0d0d':'#111';ctx.fillRect(6,y,colW*4,rowH);
    var attrLines=r.attr.split('\n');
    ctx.fillStyle=_LB;ctx.font='bold 9px -apple-system,sans-serif';ctx.textAlign='center';
    attrLines.forEach(function(l,li){ctx.fillText(l,cols[0]+colW/2,y+rowH*(0.28+li*0.38));});
    [[r.lr,_GN,'#1a2a1a'],[r.sm,_AM,'#2a2a1a'],[r.mas,_RE,'#2a1a1a']].forEach(function(v,vi){
      if(i===3||i===5){ctx.fillStyle=v[2]+'88';ctx.fillRect(cols[vi+1],y,colW,rowH);}
      var lines=v[0].split('\n');ctx.fillStyle=v[1];ctx.font='9px -apple-system,sans-serif';ctx.textAlign='center';
      lines.forEach(function(l,li){ctx.fillText(l,cols[vi+1]+colW/2,y+rowH*(0.28+li*0.38));});});
    ctx.strokeStyle='#1e1e1e';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(6,y+rowH);ctx.lineTo(6+colW*4,y+rowH);ctx.stroke();
    [1,2,3].forEach(function(ci){ctx.beginPath();ctx.moveTo(cols[ci],y);ctx.lineTo(cols[ci],y+rowH);ctx.stroke();});});
  if(P.highlight!==undefined){
    var hy=10+rowH*(P.highlight+0.9);
    ctx.strokeStyle=_TE;ctx.lineWidth=2;ctx.strokeRect(7,hy+1,colW*4-2,rowH-2);}
  if(ctrl){ctrl.innerHTML='';var row2=document.createElement('div');
    row2.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:8px;align-items:center;';
    var sp=document.createElement('span');sp.textContent='FOCUS: ';
    sp.style.cssText='font-size:10px;font-weight:800;color:#444;';row2.appendChild(sp);
    rows.forEach(function(r,i){var b=document.createElement('button');
      b.textContent=r.attr.split('\n')[0];
      b.style.cssText='font-size:10px;padding:2px 7px;border-radius:4px;cursor:pointer;border:1px solid #333;background:transparent;color:#555;';
      b.addEventListener('click',function(){P.highlight=P.highlight===i?undefined:i;
        _cl(ctx,W,H);_render(cv,ctrl,P);});row2.appendChild(b);});ctrl.appendChild(row2);}}
"""

# ── Chart 5: Auto-PEEP Flow-Time Waveform ─────────────────────────────────────
RF['autopeep'] = r"""
function _render(cv,ctrl,P){
  var W=cv.width,H=cv.height,ctx=cv.getContext('2d');if(!ctx)return;
  var mx=56,my=18,pw=W-mx-14,ph=H-my-50,tMax=6,yMin=-10,yMax=18,yRange=yMax-yMin;
  function toX(t){return mx+(t/tMax)*pw;}
  function toY(f){return my+ph-((f-yMin)/yRange)*ph;}
  var mode=P.mode||'normal';
  function gen(hasAutoPEEP){
    var pts=[],T=4,Ti=1.33;
    var Vt=0.5,TeConst=hasAutoPEEP?6:3;
    for(var t=0;t<=tMax;t+=0.02){
      var tMod=t%T,f;
      if(tMod<Ti){f=Vt/Ti;}
      else{
        var te=tMod-Ti;
        f=-Vt/Ti*Math.exp(-TeConst*te/(T-Ti));}
      pts.push({t:t,f:f});}
    return pts;}
  function draw(){
    _cl(ctx,W,H);
    ctx.strokeStyle=_GR;ctx.lineWidth=1;
    [-8,-4,0,4,8,12,16].forEach(function(f){var y=toY(f);ctx.beginPath();ctx.moveTo(mx,y);ctx.lineTo(mx+pw,y);ctx.stroke();});
    [0,1,2,3,4,5,6].forEach(function(t){var x=toX(t);ctx.beginPath();ctx.moveTo(x,my);ctx.lineTo(x,my+ph);ctx.stroke();});
    ctx.strokeStyle=_AX;ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(mx,toY(0));ctx.lineTo(mx+pw,toY(0));ctx.stroke();
    ctx.beginPath();ctx.moveTo(mx,my);ctx.lineTo(mx,my+ph);ctx.stroke();
    ctx.textAlign='center';
    [0,1,2,3,4,5,6].forEach(function(v){_lb(ctx,v,toX(v),my+ph+15,_LB,10);});
    ctx.textAlign='right';
    [-8,-4,4,8,12,16].forEach(function(v){if(v!==0)_lb(ctx,v,mx-6,toY(v)+4,_LB,10,'right');});
    _lb(ctx,'Time (seconds)',mx+pw/2,H-5,_LB,11);
    _rl(ctx,'Flow (L/s)  ↑Insp ↓Exp',14,my+ph/2);
    var isAutoPEEP=mode==='autoPEEP';
    var pts=gen(isAutoPEEP);
    var color=isAutoPEEP?_RE:_TE;
    ctx.strokeStyle=color;ctx.lineWidth=2.5;ctx.beginPath();
    pts.forEach(function(p,i){var x=toX(p.t),y=toY(Math.max(yMin,Math.min(yMax,p.f)));
      if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);});
    ctx.stroke();
    if(isAutoPEEP){
      [1.33,5.33].forEach(function(breathEnd){
        var markerX=toX(breathEnd);
        var residualF=gen(true).find(function(p){return Math.abs(p.t-breathEnd)<0.02;});
        if(residualF){
          _dot(ctx,markerX,toY(residualF.f),6,_RE);
          _lb(ctx,'Flow ≠0',markerX+10,toY(residualF.f)-10,_RE,9,'left');}});
      _lb(ctx,'⚠ Expiratory flow never reaches zero → air trapping → intrinsic PEEP',mx+pw/2,my+ph+28,_RE,10);}
    else{
      _lb(ctx,'✓ Flow returns to zero before next breath — no air trapping',mx+pw/2,my+ph+28,_TE,10);}
    _lb(ctx,isAutoPEEP?'Auto-PEEP (Air Trapping)':'Normal',mx+pw*0.88,my+14,color,12);}
  draw();
  if(ctrl){ctrl.innerHTML='';var row=document.createElement('div');
    row.style.cssText='display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;align-items:center;';
    var sp=document.createElement('span');sp.textContent='MODE: ';
    sp.style.cssText='font-size:10px;font-weight:800;color:#444;';row.appendChild(sp);
    [{key:'normal',label:'Normal',color:_TE},{key:'autoPEEP',label:'Auto-PEEP',color:_RE}].forEach(function(m){
      var b=_mkB(m.label,m.color,mode===m.key,function(on){if(!on)return;mode=m.key;
        row.querySelectorAll('button').forEach(function(btn){btn.style.background='transparent';btn.style.color='#555';btn._on=false;});
        b.style.background=m.color+'22';b.style.color=m.color;b._on=true;draw();});
      row.appendChild(b);});ctrl.appendChild(row);}}
"""

# ── CARDS ──────────────────────────────────────────────────────────────────────
CARDS = [

# ══ P-V Compliance Curve ══════════════════════════════════════════════════════
("On the P-V compliance curve, the STEEPER the slope, the _______ the compliance. Compare Normal vs. Severe ARDS curves. The same 20 cmH₂O pressure in Normal lung generates approximately _______ mL; in Severe ARDS it generates approximately _______ mL.",
 """HIGHER compliance — a steep slope means large volume change per unit pressure change. Compliance = ΔV/ΔP (mL/cmH₂O).
| At 20 cmH₂O: NORMAL lung ≈ 600–700 mL above FRC (compliance ~200 mL/cmH₂O — the lung inflates easily). SEVERE ARDS ≈ 150–200 mL (compliance ~15–25 mL/cmH₂O — the stiff, consolidated lung barely inflates despite high pressure).
| Clinical implication: delivering the same tidal volume (e.g., 500 mL) requires 3–5× higher pressure in ARDS than in a normal lung. This is why the same ventilator settings that are safe in a normal lung cause VILI in ARDS — the stiff lung concentrates pressure in the remaining open alveoli.
→ CCRN KEY: Compliance monitoring: calculate DYNAMIC compliance = Vt / (PIP − PEEP); STATIC compliance = Vt / (Pplat − PEEP). A declining static compliance over hours = worsening ARDS, new pneumothorax, progressive consolidation, or increasing abdominal pressure. Trending compliance is more informative than a single value.
→ MASTERY NOTE: The '20% rule' for PEEP in ARDS: optimal PEEP is often near the Lower Inflection Point (LIP) of the P-V curve — the pressure at which compliance improves because alveoli begin recruiting. Setting PEEP just above the LIP prevents alveolar collapse on expiration (atelectotrauma) while the Upper Inflection Point (UIP) marks where overdistension begins.""",
 'tier-review', 'Ph2 · 🔴 T1 · Respiratory — ARDS & Lung Protection',
 DID['ards'], 'pvcompliancecurve', '{}', 'chart-l1'),

("Toggle Normal and Severe ARDS curves. The LIP (Lower Inflection Point) on the ARDS curve represents _______. Setting PEEP ABOVE the LIP aims to _______. The UIP (Upper Inflection Point) represents _______ — tidal volume should remain _______ this pressure.",
 """LIP (Lower Inflection Point): the pressure at which the compliance curve suddenly steepens — representing ALVEOLAR RECRUITMENT. Below this pressure, most recruiteable alveoli are collapsed. At this pressure, they begin to open and the lung becomes more compliant. On the curve: the 'knee' at the bottom where the line changes slope.
| Setting PEEP ABOVE the LIP aims to: PREVENT CYCLIC ATELECTASIS (atelectotrauma) — by keeping end-expiratory pressure above the closing pressure of recruiteable alveoli, they stay open throughout the respiratory cycle rather than collapsing on expiration and being forcibly re-recruited on inspiration. This cyclic opening/closing generates shear stress injury.
| UIP (Upper Inflection Point): the pressure at which overdistension begins — compliance flattens again (upper knee). Above this pressure, additional volume creates more pressure than volume → overdistension of already-open alveoli → VOLUTRAUMA.
| Tidal volume should remain BELOW the UIP pressure — the breathing cycle should stay within the steep (compliant) portion of the curve: PEEP above LIP, Pplat below UIP. This is the target region for lung-protective ventilation.
→ CCRN KEY: The 'baby lung' concept in ARDS: the recruitable portion of the ARDS lung is much smaller than the normal lung. Vt set for 6 mL/kg IBW of TOTAL lung is actually delivered to only the open portion — effectively delivering a much larger Vt per functional alveolus. This is why driving pressure (not just Vt per IBW) matters.
→ MASTERY NOTE: P-V curve measurement (quasi-static or dynamic supersyringe method) is not routine bedside practice. However, understanding the LIP/UIP concept explains WHY PEEP trials work: a PEEP increase from 8 → 14 cmH₂O may recruit 200 mL of previously collapsed alveoli → ↑compliance → ↓Pplat → ↓driving pressure. Monitor Pplat response to PEEP changes as a surrogate for compliance change.""",
 'tier-high', 'Ph2 · 🔴 T1 · Respiratory — ARDS & Lung Protection',
 DID['ards'], 'pvcompliancecurve', '{}', 'chart-l2'),

("ARDS patient on VCV: Vt 420 mL, PEEP 8, Pplat 34, PIP 42. Static compliance = _______ mL/cmH₂O. Compare to Normal curve. If PEEP is increased from 8 to 14 and Pplat falls to 28 (same Vt), the new compliance = _______, indicating _______, and driving pressure changes from _______ to _______.",
 """Static compliance = Vt / (Pplat − PEEP) = 420 / (34 − 8) = 420 / 26 = 16.2 mL/cmH₂O — severely reduced (normal ~100 mL/cmH₂O). This patient's lung is very stiff — the remaining open alveoli are bearing the full ventilation burden.
| After PEEP 8 → 14 with Pplat falling to 28: New static compliance = 420 / (28 − 14) = 420 / 14 = 30 mL/cmH₂O — improved (nearly doubled). The compliance improvement indicates ALVEOLAR RECRUITMENT — more alveoli opened by the higher PEEP → the same Vt is now distributed over a larger functional lung surface → each individual alveolus receives less pressure.
| Driving pressure changes: Before = Pplat − PEEP = 34 − 8 = 26 cmH₂O. After = 28 − 14 = 14 cmH₂O. Below the ≤15 target. The PEEP increase REDUCED driving pressure despite the same Vt — confirmation that recruitment improved compliance.
→ CCRN KEY: When PEEP is increased and BOTH Pplat AND driving pressure DECREASE → the PEEP increase was beneficial (recruiting lung). When PEEP is increased and Pplat INCREASES → PEEP is overdistending already-open alveoli, not recruiting new ones → reduce PEEP. The P-V curve behavior determines which is happening.
→ MASTERY NOTE: This is the practical PEEP titration protocol: increase PEEP in increments (typically 2 cmH₂O), check Pplat after each increase (wait 2-3 breath cycles for equilibration), calculate new driving pressure. If ΔP decreases → continue. If ΔP increases → stop (overdistension). Target: PEEP that minimizes ΔP without causing overdistension. Document the response.""",
 'tier-critical', 'Ph2 · 🔴 T1 · Respiratory — ARDS & Lung Protection',
 DID['ards'], 'pvcompliancecurve', '{}', 'chart-l3'),

# ══ Flow-Volume Loop ══════════════════════════════════════════════════════════
("On the flow-volume loop, the EXPIRATORY limb is the _______ half of the loop. Toggle Obstruction. The expiratory limb shows a _______ (scooped/linear) shape because _______. This pattern is called _______.",
 """UPPER half of the loop — expiration is shown as POSITIVE flow (above the zero line), moving from TLC (left) to RV (right). Inspiration is the lower half (negative flow, returning from RV back to TLC).
| Obstruction: SCOOPED (concave) expiratory limb — flows are disproportionately reduced at LOW lung volumes. The expiratory flow at high volumes (near TLC) is relatively preserved, but at low volumes (near RV), the airways collapse and trap air (dynamic airway collapse). This creates the characteristic scoop or 'frown' shape.
| This pattern is called FLOW LIMITATION at low lung volumes — the airways are so narrowed and floppy that increasing expiratory effort doesn't increase flow (effort-independence). The flow is determined by airway elastic recoil, not effort.
→ CCRN KEY: The spirometry values correlate with the loop: FEV1 = volume exhaled in first second of expiration (the first portion of the expiratory limb). FEV1/FVC ratio < 0.70 = obstructive pattern. In obstruction, FVC may be normal but FEV1 is severely reduced → low ratio.
→ MASTERY NOTE: Peak expiratory flow (PEF) is the first peak of the expiratory limb. In asthma attacks, PEF is reduced (the peak is lower). PEF monitoring at home correlates with airway inflammation and PEFR <50% predicted = severe exacerbation. The flow-volume loop makes this visible: the entire upper limb shifts downward.""",
 'tier-review', 'Ph2 · 🔴 T1 · Respiratory — Obstructive Disease',
 DID['obstructive'], 'flowvolumeloop', '{}', 'chart-l1'),

("Toggle Normal vs. Restriction. In restriction, TLC and VC are _______ (increased/decreased) but the FEV1/FVC ratio is _______ because _______. The key spirometry difference from obstruction: FEV1/FVC in obstruction = _______, in restriction = _______.",
 """TLC and VC are DECREASED — the defining feature of restriction is reduced lung volumes (stiff lungs can't expand fully). The loop is SMALLER but retains its normal shape (not scooped).
| FEV1/FVC ratio is NORMAL or INCREASED (>0.70, often >0.80) because both FEV1 and FVC are proportionally reduced. The lungs blow out the same fraction of their (smaller) capacity in one second.
| Key spirometry difference: Obstruction = ↓FEV1/FVC (<0.70) — the denominator (FVC) is relatively preserved but FEV1 is selectively reduced. | Restriction = FEV1/FVC NORMAL (>0.70) — both numerator and denominator are reduced proportionally. The diagnosis of restriction requires reduced TLC on full pulmonary function testing.
→ CCRN KEY: Causes of restriction in ICU: pulmonary fibrosis, chest wall restriction (morbid obesity, kyphoscoliosis, neuromuscular weakness — diaphragm can't generate full excursion), pleural effusion (compresses and restricts lung expansion). All → small, stiff lungs → require higher pressures per volume delivered → compliance ↓.
→ MASTERY NOTE: The 'mixed pattern' (both obstruction and restriction): FEV1/FVC <0.70 AND TLC reduced. Seen in: combined COPD + pulmonary fibrosis (combined pulmonary fibrosis and emphysema — CPFE), severe COPD with respiratory muscle weakness, obesity hypoventilation syndrome with air trapping. The flow-volume loop will show both scooped expiratory limb AND reduced overall loop size.""",
 'tier-high', 'Ph2 · 🔴 T1 · Respiratory — Obstructive Disease',
 DID['obstructive'], 'flowvolumeloop', '{}', 'chart-l2'),

("Toggle Upper Airway Obstruction on the loop. The INSPIRATORY limb is _______ while the expiratory limb is _______ — this pattern of variable extrathoracic obstruction indicates _______. Bedside clinical assessment to confirm: _______.",
 """INSPIRATORY LIMB is FLAT (truncated) — the fixed inspiratory flow cannot increase above a plateau despite increased inspiratory effort. EXPIRATORY limb is NORMAL (or near-normal) shape — expiration is preserved because extrathoracic airway obstruction (above the thoracic inlet) is RELIEVED by positive intrathoracic pressure during expiration.
| Variable extrathoracic obstruction: the obstruction is ABOVE the thoracic inlet (larynx, subglottis, trachea above the sternum). During INSPIRATION, atmospheric pressure compresses the floppy extrathoracic airway → obstruction worsens → inspiratory flow limited. During EXPIRATION, positive intraluminal pressure distends the extrathoracic airway → obstruction relieved → expiratory flow preserved. Examples: tracheomalacia, subglottic stenosis, vocal cord paralysis (unilateral or bilateral), large goiter compressing the trachea.
| Fixed obstruction (tracheal stenosis from ETT trauma): BOTH limbs are flattened — a box-shaped loop.
| Bedside clinical assessment: INSPIRATORY STRIDOR (high-pitched noise on inspiration) — the hallmark of upper airway obstruction. Auscultate over the larynx/trachea. Positional change (stridor worsens supine = posterior tracheal wall collapsing). Direct laryngoscopy or flexible bronchoscopy for visualization.
→ CCRN KEY: Post-extubation stridor (within 30-60 minutes) = glottic or subglottic edema — the most common cause of post-extubation airway obstruction. Prevention: cuff leak test before extubation (absence of leak suggests tight fit → edema risk). Treatment: racemic epinephrine nebulizer (vasoconstriction → ↓ mucosal edema), IV dexamethasone, heliox (lower density gas → ↓ turbulent flow → ↓ work of breathing).
→ MASTERY NOTE: The cuff leak test: deflate the ETT cuff and occlude the tube momentarily. The patient should generate an audible air leak around the tube. Absence of leak (tight fit) = significant airway edema risk → consider dexamethasone 8 mg IV 12-24h before extubation, recheck leak before proceeding.""",
 'tier-critical', 'Ph2 · 🔴 T1 · Respiratory — Obstructive Disease',
 DID['obstructive'], 'flowvolumeloop', '{}', 'chart-l3'),

# ══ V/Q Shunt ═════════════════════════════════════════════════════════════════
("On the V/Q shunt chart, move the Shunt slider to 30%. PaO₂ on 100% O₂ (FiO₂ 1.0) = approximately _______ mmHg. PaO₂ on room air (FiO₂ 0.21) = approximately _______ mmHg. A region with V/Q = 0 is called _______ and blood passing through it remains at _______ mmHg PO₂.",
 """At 30% shunt: PaO₂ on 100% O₂ ≈ 200–250 mmHg (severely reduced despite 100% O₂). PaO₂ on room air ≈ 55–65 mmHg (critically low — SpO₂ ~88–92%).
| V/Q = 0 region = TRUE INTRAPULMONARY SHUNT — the alveolus is perfused (blood flows through) but NOT ventilated (no gas exchange occurs). Blood passes through and exits with the same PO₂ it entered with: MIXED VENOUS PO₂ ≈ 40 mmHg, SaO₂ ≈ 75%. This deoxygenated blood mixes with oxygenated blood from normal V/Q units → lowers the overall PaO₂.
| Causes of shunt (V/Q = 0): consolidation (pneumonia — alveoli filled with fluid/pus), atelectasis (alveoli collapsed — no air), ARDS (alveolar flooding), pulmonary edema (alveoli filled with transudate/exudate). All share: alveolus present and perfused, but no air reaching it.
→ CCRN KEY: Shunt vs. V/Q mismatch vs. diffusion limitation: TRUE SHUNT (V/Q=0) is the only oxygenation failure that does NOT respond to increased FiO₂. This is because no amount of O₂ added to the breathing mixture can oxygenate blood that bypasses the gas exchange surface entirely.
→ MASTERY NOTE: The 100% O₂ test: if PaO₂ fails to rise above 300–350 mmHg on FiO₂ 1.0, true intrapulmonary shunt is present. The calculated shunt fraction: Qs/Qt = (CcO₂ − CaO₂)/(CcO₂ − CvO₂) where CcO₂ is the end-capillary O₂ content (assumed fully saturated at FiO₂ 1.0), CaO₂ is arterial content, CvO₂ is mixed venous content from PA catheter.""",
 'tier-review', 'Ph2 · 🔴 T1 · Respiratory — ARDS & Lung Protection',
 DID['ards'], 'vqshunt', '{"shunt":30}', 'chart-l1'),

("Move the shunt slider to 40% and compare PaO₂ at FiO₂ 0.60 vs. FiO₂ 1.0. The difference is approximately _______ mmHg. This demonstrates that in high shunt, increasing FiO₂ above _______ has diminishing returns because _______. The correct intervention to improve oxygenation in shunt is _______.",
 """At 40% shunt: FiO₂ 0.60 → PaO₂ ≈ 120 mmHg. FiO₂ 1.0 → PaO₂ ≈ 160 mmHg. Difference ≈ 40 mmHg (small relative to the FiO₂ change from 0.60 to 1.0 — a 40% increase in O₂ fraction for only 40 mmHg PaO₂ gain). On the chart: the FiO₂ 0.6 and FiO₂ 1.0 curves converge as shunt increases.
| Above approximately 30% shunt, FiO₂ increases have diminishing returns because: the oxygenated blood (from ventilated alveoli) is ALREADY near fully saturated (PaO₂ is high). Further increasing FiO₂ raises the venous-arterial O₂ content difference minimally. The shunted blood (PaO₂ 40 mmHg, SaO₂ 75%) dilutes the oxygenated blood regardless of how much O₂ you add to the ventilated units — those units can't take up more O₂ than Hgb can carry.
| Correct intervention: PEEP (recruit collapsed alveoli → convert V/Q=0 to V/Q>0) and/or PRONE POSITIONING (recruit dorsal atelectatic areas → ↓ shunt fraction). These address the CAUSE of shunt — not the oxygen concentration breathing in.
→ CCRN KEY: Oxygen toxicity threshold: FiO₂ >0.60 for >24-48h → absorptive atelectasis (N₂ washout → alveoli collapse) + direct O₂ radical injury to alveolar epithelium. Reducing FiO₂ after PEEP optimization is a care bundle priority — not a secondary concern.
→ MASTERY NOTE: The clinical algorithm: FiO₂ >0.60 to maintain SpO₂ ≥88% → MUST optimize PEEP and lung recruitment before accepting high FiO₂ long-term. PEEP trials, prone positioning, and neuromuscular blockade (if severe dyssynchrony) should all be considered before accepting FiO₂ >0.60 as a 'stable' ventilator setting.""",
 'tier-high', 'Ph2 · 🔴 T1 · Respiratory — ARDS & Lung Protection',
 DID['ards'], 'vqshunt', '{"shunt":40}', 'chart-l2'),

("ARDS patient: FiO₂ 1.0, PaO₂ 68 mmHg, PEEP 14. Using the V/Q shunt chart, estimated shunt fraction ≈ _______%. The primary intervention at this point is _______, not _______ (higher FiO₂), because _______. If PaO₂ improves to 120 mmHg after prone positioning, the new estimated shunt fraction is approximately _______.",
 """Estimated shunt fraction ≈ 40–45% — at FiO₂ 1.0 and PaO₂ 68 mmHg, the shunt curve shows ~40–45% shunt is required to produce this degree of hypoxemia on pure O₂.
| Primary intervention: PRONE POSITIONING — addresses the shunt directly by recruiting the posterior (dorsal) lung zones that are most atelectatic due to gravitational compressive forces in the supine position. Prone redistributes ventilation more evenly → ↓ shunt fraction → ↑ PaO₂. This is indicated for PaO₂/FiO₂ <150 (this patient: 68/1.0 = 68 — severely impaired).
| Not FiO₂ higher — FiO₂ is already at 1.0 (maximum). No further increase is possible. But even if FiO₂ could be increased further, the shunt chart shows that at 40%+ shunt, additional FiO₂ provides minimal PaO₂ improvement.
| After prone positioning, PaO₂ 120 mmHg on FiO₂ 1.0: shunt fraction ≈ 25–30% — a meaningful improvement. Now FiO₂ can be reduced (to ↓ O₂ toxicity) while maintaining SpO₂ ≥88%.
→ CCRN KEY: Prone positioning recommendation (PROSEVA trial, 2013): moderate-severe ARDS (PaO₂/FiO₂ <150, PEEP ≥5) → prone ≥16h/day → mortality reduction from 33% to 16% (NNT ≈6). This is one of the highest-impact interventions in critical care nursing. Positioning requires ≥4 staff, careful securing of lines/ETT, face pressure relief, and eye protection.
→ MASTERY NOTE: Proning complications the nurse monitors: pressure injuries (face, chest, pelvis, knees — q2h repositioning within prone), ETT displacement (pre-prone: verify and secure position, check bilateral breath sounds immediately after prone), unplanned extubation, facial edema (may affect airway management on return to supine), hemodynamic changes (prone can improve RV function by ↓ pulmonary vascular resistance).""",
 'tier-critical', 'Ph2 · 🔴 T1 · Respiratory — ARDS & Lung Protection',
 DID['ards'], 'vqshunt', '{"shunt":45}', 'chart-l3'),

# ══ PE Severity Classification ════════════════════════════════════════════════
("From the PE classification chart: MASSIVE PE is defined by _______, NOT by the size of the clot. This represents approximately _______ of all PE and carries 30-day mortality of _______. The immediate first-line treatment is _______.",
 """MASSIVE PE is defined by: HEMODYNAMIC INSTABILITY — specifically persistent hypotension (SBP <90 mmHg for ≥15 minutes), need for vasopressors, cardiac arrest, or severe bradycardia with shock signs. The definition is based on hemodynamic impact, NOT on clot burden, imaging findings, or biomarkers alone.
| Represents approximately 5% of all PE — the minority of cases but the most immediately life-threatening.
| 30-day mortality: >25–50% with current therapy (this is the highest-risk subgroup by far). Untreated, mortality may approach 90%.
| Immediate first-line treatment: SYSTEMIC THROMBOLYSIS — alteplase 100 mg IV over 2 hours (or reduced dose for smaller patients). This rapidly dissolves the clot burden, reduces RV afterload, restores hemodynamics. OR: surgical or catheter-directed thrombectomy if thrombolysis contraindicated or fails.
→ CCRN KEY: Thrombolysis absolute contraindications for massive PE: prior intracranial hemorrhage, known structural CNS lesion, ischemic stroke within 3 months, active internal bleeding, significant closed-head trauma within 3 months. RELATIVE contraindications (weigh against death risk from massive PE): recent major surgery, recent major bleeding, uncontrolled severe hypertension. In a dying patient, there are very few absolute contraindications.
→ MASTERY NOTE: The hemodynamic definition of massive PE means clinical recognition at the bedside: a PE patient who was previously stable becomes hypotensive (SBP <90) — MASSIVE PE until proven otherwise. This triggers immediate escalation: call the physician, prepare for thrombolysis/thrombectomy, activate PERT (PE Response Team) if available, place a second IV, prepare for deterioration.""",
 'tier-review', 'Ph2 · 🔴 T1 · Respiratory — Pulmonary Embolism',
 DID['pulmonary_embolism'], 'peseverity', '{"highlight":0}', 'chart-l1'),

("A patient has PE with: BP 104/72 (stable), Troponin 0.18 ng/mL (elevated), echo showing RV:LV ratio 1.1 and septal flattening. Click the RV dysfunction row on the chart. This classifies the PE as _______. The current treatment standard is _______, and the reason systemic thrombolysis is NOT automatically given: _______.",
 """SUBMASSIVE PE — hemodynamically STABLE (BP 104/72, no vasopressors needed) BUT has BOTH RV dysfunction on imaging (RV:LV 1.1 >0.9, septal flattening = D-sign indicating RV pressure overload) AND elevated troponin (myocardial injury from RV strain).
| Current treatment standard: ANTICOAGULATION (heparin or LMWH) as the foundation. For high-risk submassive PE with multiple adverse features: CONSIDER catheter-directed thrombolysis (CDT) or ultrasound-accelerated CDT — a lower-dose, targeted approach with lower bleeding risk than systemic thrombolysis.
| Systemic thrombolysis is NOT automatically given because: the risk of major bleeding (including intracranial hemorrhage, 0.5-1%) must be weighed against the benefit in a patient who is HEMODYNAMICALLY STABLE. Studies (PEITHO trial) showed systemic thrombolysis in submassive PE reduced hemodynamic decompensation but significantly increased major bleeding without clear mortality benefit in the overall group.
→ CCRN KEY: The submassive PE monitoring priority: ANTICIPATE DECOMPENSATION. These patients have limited RV reserve. Anything that increases O₂ demand (fever, pain, tachycardia) or reduces O₂ delivery (fluid restriction, vasodilation) can tip them into massive PE. Monitor: HR, BP, SpO₂, mental status. Have a RAPID ESCALATION PLAN ready.
→ MASTERY NOTE: Fluid management in RV failure from PE: the RV is dilated and pressure-overloaded. Aggressive fluid resuscitation is counterproductive — it further dilates the RV, worsens septal shift into the LV (D-sign), and reduces LV filling (interventricular interdependence). Give small, judicious fluid boluses (250-500 mL) only for clear hypovolemia. Vasopressors (norepinephrine or vasopressin) and inotropes (dobutamine) are preferred over fluids for hemodynamic support.""",
 'tier-high', 'Ph2 · 🔴 T1 · Respiratory — Pulmonary Embolism',
 DID['pulmonary_embolism'], 'peseverity', '{"highlight":1}', 'chart-l2'),

("PE patient: BP 82/52, HR 138, RR 30, SpO₂ 84% on 15L NRB, troponin 2.8, echo: RV:LV 1.4, RV hypokinesis, McConnell sign. Classification: _______ PE. Before systemic thrombolysis: nursing confirms _______ contraindications (none found). Dose of alteplase: _______ over _______ hours. For the first 2 hours of infusion, the nurse holds _______.",
 """MASSIVE PE — hemodynamically UNSTABLE (BP 82/52, requiring vasopressors, SpO₂ 84% despite 15L O₂). RV:LV 1.4, McConnell sign (RV free wall akinesis with preserved RV apex motion — specific for acute PE) confirms severe acute RV failure.
| Before systemic thrombolysis: confirm NO ABSOLUTE CONTRAINDICATIONS — recent intracranial surgery or trauma (<3 months), prior intracerebral hemorrhage, known intracranial neoplasm or AVM, active internal bleeding, ischemic stroke <3 months. Ask about recent surgeries, bleeding history. In cardiac arrest from massive PE: thrombolysis is appropriate even if recent minor surgery (dying patient: relative contraindications become much less important).
| Dose: ALTEPLASE 100 mg IV over 2 HOURS (standard dose). Reduced dose 0.6 mg/kg (max 50 mg) for smaller patients or those with higher bleeding risk. Note: 10 mg given as IV bolus over 1-2 minutes, then 90 mg over 2 hours.
| During infusion: HOLD ALL ANTICOAGULATION (heparin infusion must be stopped during alteplase infusion — concurrent use dramatically increases bleeding risk). Restart heparin WITHOUT bolus 1 hour after alteplase completion if aPTT <80 seconds. No arterial sticks, no IV insertions if possible during and 24h after thrombolysis.
→ CCRN KEY: Thrombolysis nursing: check neurochecks q30min during infusion (first sign of intracranial hemorrhage = altered mental status, new headache, pupils). Stop alteplase IMMEDIATELY if neurological change occurs. Have reversal plan: protamine (if heparin was on), cryoprecipitate/FFP (fibrinogen replacement). The physician orders — the nurse executes and MONITORS.
→ MASTERY NOTE: McConnell sign specificity: basal/mid RV wall hypo/akinesis with preserved RV apical motion on echo — specific for ACUTE PE (not chronic PH). In chronic RV pressure overload (chronic PE, PAH), the entire RV wall is hypokinetic including the apex. McConnell's specificity for acute RV pressure overload is ~94% in the right clinical context.""",
 'tier-critical', 'Ph2 · 🔴 T1 · Respiratory — Pulmonary Embolism',
 DID['pulmonary_embolism'], 'peseverity', '{"highlight":0}', 'chart-l3'),

# ══ Auto-PEEP Flow-Time Waveform ══════════════════════════════════════════════
("Toggle to Auto-PEEP mode on the flow-time waveform. Auto-PEEP is identified when the expiratory flow _______ before the next breath begins. This indicates _______. The clinical consequences of undetected auto-PEEP: _______ and _______.",
 """DOES NOT RETURN TO ZERO — the expiratory flow curve is still negative (patient still exhaling) when the ventilator triggers the next breath. This is the definitive waveform sign of auto-PEEP (intrinsic PEEP, inadvertent PEEP, dynamic hyperinflation).
| Indicates: INCOMPLETE EXHALATION — the patient cannot fully exhale within the available expiratory time. Air is trapped in the lungs above the set PEEP level, creating an additional positive end-expiratory pressure that is NOT reflected in the set PEEP on the ventilator display.
| Clinical consequences of undetected auto-PEEP: (1) TRUE PEEP = set PEEP + auto-PEEP → Pplat and driving pressure calculations are INCORRECT (falsely low) — you think ΔP = 14 cmH₂O but actual ΔP = 22 cmH₂O → VILI risk is higher than calculated. (2) HEMODYNAMIC COMPROMISE — elevated intrathoracic pressure from air trapping → ↓ venous return → ↓ preload → ↓ CO → hypotension. (3) TRIGGERING FAILURE — the patient must generate enough effort to overcome auto-PEEP before they can trigger the ventilator → increased work of breathing → respiratory distress.
→ CCRN KEY: How to measure auto-PEEP: perform an EXPIRATORY HOLD (pause at end-expiration, 0.5–1 second). The pressure equilibrates during the pause and the display shows the TRUE total PEEP (set PEEP + auto-PEEP). Auto-PEEP = measured total PEEP − set PEEP. This should be checked routinely in COPD and asthma patients on mechanical ventilation.
→ MASTERY NOTE: The clinical scenario: COPD patient on ventilator, hemodynamically stable, then develops unexplained hypotension (BP 90/60). The flow-time waveform shows auto-PEEP. Mechanism: progressive air trapping → ↑ intrathoracic pressure → ↓ venous return → ↓ CO → hypotension. Treatment: temporarily disconnect from the ventilator (allowing passive exhalation of trapped air) → BP immediately improves. This is the diagnostic AND therapeutic maneuver for auto-PEEP-induced hemodynamic compromise.""",
 'tier-review', 'Ph2 · 🔴 T1 · Respiratory — Mechanical Ventilation',
 DID['mechanical_vent'], 'autopeep', '{"mode":"autoPEEP"}', 'chart-l1'),

("A ventilated COPD patient has auto-PEEP of 8 cmH₂O measured on expiratory hold. Set PEEP is 5. Total PEEP = _______. The patient is struggling to trigger the ventilator because _______. Two ventilator adjustments that reduce auto-PEEP: _______ and _______.",
 """Total PEEP = SET PEEP + AUTO-PEEP = 5 + 8 = 13 cmH₂O — the true end-expiratory pressure in the lungs, significantly higher than the monitored set PEEP.
| Patient struggles to trigger because: the ventilator triggers when airway pressure drops below the set sensitivity threshold (e.g., −2 cmH₂O below set PEEP). But the actual pressure at the carina is +13 cmH₂O (not +5). To trigger the ventilator, the patient must generate enough inspiratory effort to drop pressure from +13 cmH₂O to the trigger threshold — requiring far more work than if PEEP were actually 5. This is auto-PEEP-related triggering failure, a major cause of dyssynchrony in COPD patients.
| Adjustments to reduce auto-PEEP: (1) ↓ RESPIRATORY RATE — increases expiratory time (Te) per cycle → more time to exhale. (2) ↓ I:E RATIO (shorten inspiratory time) — increases Te further. Also: ↑ INSPIRATORY FLOW RATE (deliver the same Vt faster → starts expiration sooner → longer Te); TREAT BRONCHOSPASM (reduce airway resistance → faster exhalation → less air trapping); REDUCE TIDAL VOLUME.
→ CCRN KEY: The 'applied PEEP to counter auto-PEEP' strategy: setting external PEEP to 70–80% of the measured auto-PEEP reduces the trigger work without worsening dynamic hyperinflation. The logic: since auto-PEEP creates positive alveolar pressure at end-expiration, adding external PEEP to match it means the patient only needs to generate a small pressure DROP to trigger (rather than a large drop from atmospheric). This is counterintuitive but reduces patient effort significantly.
→ MASTERY NOTE: Auto-PEEP in ARDS: less common than in COPD but occurs with high respiratory rates (RR >25) in small-lunged patients. In ARDS, the primary concern is lung-protective Vt and ΔP — a high RR to compensate for small Vt can inadvertently cause auto-PEEP. The flow-time waveform should be checked routinely in all mechanically ventilated patients, not just COPD.""",
 'tier-high', 'Ph2 · 🔴 T1 · Respiratory — Mechanical Ventilation',
 DID['mechanical_vent'], 'autopeep', '{"mode":"autoPEEP"}', 'chart-l2'),

("Mechanically ventilated ARDS patient: set PEEP 10, Pplat 28. Expiratory hold reveals total PEEP 16 cmH₂O → auto-PEEP = _______ cmH₂O. The TRUE driving pressure (ΔP) = _______ cmH₂O, NOT the calculated 18 (Pplat − set PEEP). This matters because _______. Two interventions to address this: _______ and _______.",
 """Auto-PEEP = Total PEEP − Set PEEP = 16 − 10 = 6 cmH₂O
| TRUE driving pressure = Pplat − TOTAL PEEP = 28 − 16 = 12 cmH₂O (NOT 28 − 10 = 18 as would be calculated using set PEEP). The driving pressure using set PEEP OVERESTIMATES the alveolar distending pressure in the presence of auto-PEEP.
| Wait — actually this is important to clarify: when auto-PEEP is present, the true driving pressure = Pplat − total PEEP = 28 − 16 = 12 cmH₂O. This is actually LOWER than the set PEEP-based calculation (18 cmH₂O). In this case, auto-PEEP is actually masking that the lung is better protected than the set PEEP-based calculation suggests. HOWEVER, the total PEEP of 16 (not the set 10) is the true end-expiratory alveolar pressure — all monitoring, compliance calculations, and driving pressure assessments must use TOTAL PEEP.
| This matters because: compliance = Vt / (Pplat − total PEEP) — using set PEEP gives falsely low compliance (overestimates stiffness). Clinical decisions about PEEP titration, recruitment maneuvers, and hemodynamic assessments must account for total PEEP.
| Interventions: (1) REDUCE RESPIRATORY RATE from current setting → longer Te → less auto-PEEP; (2) SHORTEN INSPIRATORY TIME (↑ inspiratory flow) → more Te. If auto-PEEP cannot be reduced: SET EXTERNAL PEEP closer to auto-PEEP level (70-80% of auto-PEEP) to reduce trigger work.
→ CCRN KEY: The routine for detecting auto-PEEP: (1) observe flow-time waveform — if expiratory flow ≠ 0 at end of expiration → auto-PEEP present. (2) Quantify: expiratory hold → compare displayed PEEP to set PEEP. (3) Calculate TRUE driving pressure using total PEEP. (4) Assess hemodynamics (↑ total PEEP → ↓ venous return → ↓ CO). Do this at shift start and with any ventilator setting changes.
→ MASTERY NOTE: Expiratory hold technique: timing matters. The hold must be done at END-EXPIRATION just before the next scheduled breath. On volume-control modes, most modern ventilators have an 'expiratory pause' button. Hold for 0.5 seconds minimum (allow pressure equilibration). The plateau that appears = true total PEEP. In a spontaneously breathing patient, muscle activity interferes — the most accurate measurement is in a fully paralyzed (NMB) patient or a completely passive patient.""",
 'tier-critical', 'Ph2 · 🔴 T1 · Respiratory — Mechanical Ventilation',
 DID['mechanical_vent'], 'autopeep', '{"mode":"autoPEEP"}', 'chart-l3'),
]


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
    print(f"  Output: {OUT_PATH}")
    print(f"{'='*65}")


if __name__ == '__main__':
    main()
