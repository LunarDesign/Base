#!/usr/bin/env python3
"""
chunk34_charts.py — Ph3 Multisystem: Lactate Clearance, DO2/VO2 Curve,
                     Hemorrhagic Shock, Damage Control, Parkland Formula
                     5 charts x 3 cards = 15 cards
"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_33_vari.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_34.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c34')
CHUNK_NUM   = 34
MID_BASE    = 1_800_005_015
CHART_ORDER = ['lactate_clearance', 'do2_vo2_curve', 'hemorrhagic_shock',
               'damage_control', 'parkland_formula']

# Badge strings — verified from live Anki deck 2026-05-14
_SS = 'Ph3 · \U0001f534 T1 · Multisystem — Sepsis & Septic Shock'
_MT = 'Ph3 · \U0001f534 T1 · Multisystem — MODS & Trauma'
_BT = 'Ph3 · \U0001f7e0 T2 · Multisystem — Burns & Toxicology'

RF = {}

# ── Chart 1: Lactate Clearance ────────────────────────────────────────────────
RF['lactate_clearance'] = r"""
function _render(cv, ctrl, P) {
  var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
  _cl(ctx, W, H);
  var mx=52, my=18, pw=W-mx-16, ph=H-my-38;
  var xD=12, yD=8;
  _gd(ctx, mx, my, pw, ph, 2, xD, 1, yD);
  _ax(ctx, mx, my, pw, ph);
  function hline(yv, col, lbl) {
    var py=my+ph-(yv/yD)*ph;
    ctx.strokeStyle=col; ctx.lineWidth=1; ctx.setLineDash([5,3]);
    ctx.beginPath(); ctx.moveTo(mx,py); ctx.lineTo(mx+pw,py); ctx.stroke();
    ctx.setLineDash([]);
    _lb(ctx, lbl, mx+pw-4, py-5, col, 9, 'right');
  }
  hline(4, _RE, '≥4 = Shock');
  hline(2, _GN, '<2 Normal');
  var init=6.2;
  _crv(ctx, function(x){return (init-1.6)*Math.exp(-0.29*x)+1.6;}, 0,12, mx,my,pw,ph,xD,yD, _GN, 2.5);
  _crv(ctx, function(x){return (init-4.9)*Math.exp(-0.07*x)+4.9;}, 0,12, mx,my,pw,ph,xD,yD, _RE, 2.5);
  var g2=(init-1.6)*Math.exp(-0.58)+1.6, g6=(init-1.6)*Math.exp(-1.74)+1.6;
  var px2=mx+(2/xD)*pw, px6=mx+(6/xD)*pw;
  _dot(ctx, px2, my+ph-(g2/yD)*ph, 4, _GN);
  _dot(ctx, px6, my+ph-(g6/yD)*ph, 4, _GN);
  _lb(ctx, '-'+Math.round((1-g2/init)*100)+'% @2h', px2+4, my+ph-(g2/yD)*ph-9, _GN, 9, 'left');
  _lb(ctx, '-'+Math.round((1-g6/init)*100)+'% @6h', px6+4, my+ph-(g6/yD)*ph-9, _GN, 9, 'left');
  _lb(ctx, 'Time (hours)', mx+pw/2, H-4, _LB, 10);
  _rl(ctx, 'Lactate (mmol/L)', mx-34, my+ph/2);
  for (var i=0; i<=12; i+=2) _lb(ctx, i, mx+(i/xD)*pw, my+ph+13, _LB, 10);
  for (var j=0; j<=8; j+=2) _lb(ctx, j, mx-8, my+ph-(j/yD)*ph+4, _LB, 10, 'right');
  ctx.strokeStyle=_GN; ctx.lineWidth=2.5;
  ctx.beginPath(); ctx.moveTo(mx+8,my+6); ctx.lineTo(mx+24,my+6); ctx.stroke();
  _lb(ctx, 'Adequate clearance', mx+66, my+10, _GN, 9, 'center');
  ctx.strokeStyle=_RE; ctx.lineWidth=2.5;
  ctx.beginPath(); ctx.moveTo(mx+8,my+19); ctx.lineTo(mx+24,my+19); ctx.stroke();
  _lb(ctx, 'Poor clearance', mx+60, my+23, _RE, 9, 'center');
}
"""

# ── Chart 2: DO2/VO2 Curve ────────────────────────────────────────────────────
RF['do2_vo2_curve'] = r"""
function _render(cv, ctrl, P) {
  var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
  _cl(ctx, W, H);
  var mx=56, my=18, pw=W-mx-16, ph=H-my-38;
  var xD=800, yD=280;
  _gd(ctx, mx, my, pw, ph, 100, xD, 50, yD);
  _ax(ctx, mx, my, pw, ph);
  var critX=330, plateau=215;
  var critPx=mx+(critX/xD)*pw;
  ctx.strokeStyle=_AM; ctx.lineWidth=1; ctx.setLineDash([4,4]);
  ctx.beginPath(); ctx.moveTo(critPx,my); ctx.lineTo(critPx,my+ph); ctx.stroke();
  ctx.setLineDash([]);
  _lb(ctx, 'Critical DO₂', critPx, my+9, _AM, 9);
  _lb(ctx, '~330', critPx, my+20, _AM, 9);
  _crv(ctx, function(x){return x<critX?(plateau/critX)*x:plateau;}, 0,800, mx,my,pw,ph,xD,yD, _TE, 2.5);
  _crv(ctx, function(x){return Math.min(168, x*0.21);}, 0,800, mx,my,pw,ph,xD,yD, _RE, 2.5);
  var platY=my+ph-(plateau/yD)*ph;
  ctx.strokeStyle=_TE; ctx.lineWidth=1; ctx.setLineDash([3,3]);
  ctx.beginPath(); ctx.moveTo(mx,platY); ctx.lineTo(mx+pw,platY); ctx.stroke();
  ctx.setLineDash([]);
  _lb(ctx, 'VO₂ plateau ~215', mx+pw-4, platY-5, _TE, 9, 'right');
  var midSD=mx+(critX*0.45/xD)*pw;
  _lb(ctx, 'Supply-dependent', midSD, my+ph-18, _LB, 9);
  var midSI=mx+((critX+(xD-critX)*0.5)/xD)*pw;
  _lb(ctx, 'Supply-independent', midSI, my+ph-18, _TE, 9);
  _lb(ctx, 'DO₂ (mL/min/m²)', mx+pw/2, H-4, _LB, 10);
  _rl(ctx, 'VO₂ (mL/min/m²)', mx-37, my+ph/2);
  for (var xi=0; xi<=800; xi+=200) _lb(ctx, xi, mx+(xi/xD)*pw, my+ph+13, _LB, 10);
  for (var yi=0; yi<=280; yi+=50) _lb(ctx, yi, mx-8, my+ph-(yi/yD)*ph+4, _LB, 10, 'right');
  ctx.strokeStyle=_TE; ctx.lineWidth=2.5;
  ctx.beginPath(); ctx.moveTo(mx+8,my+6); ctx.lineTo(mx+24,my+6); ctx.stroke();
  _lb(ctx, 'Normal', mx+44, my+10, _TE, 9, 'center');
  ctx.strokeStyle=_RE; ctx.lineWidth=2.5;
  ctx.beginPath(); ctx.moveTo(mx+8,my+19); ctx.lineTo(mx+24,my+19); ctx.stroke();
  _lb(ctx, 'Sepsis (supply-dependent)', mx+90, my+23, _RE, 9, 'center');
}
"""

# ── Chart 3: Hemorrhagic Shock Classification (canvas table) ─────────────────
RF['hemorrhagic_shock'] = r"""
function _render(cv, ctrl, P) {
  var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
  _cl(ctx, W, H);
  var cols=[
    {name:'Class I',  pct:'<15%',  hr:'<100',   sbp:'Normal', pp:'Normal', rr:'14-20', ms:'Normal',   col:'#4caf50'},
    {name:'Class II', pct:'15-30%',hr:'100-120', sbp:'Normal', pp:'↓ PP', rr:'20-30', ms:'Anxious',  col:'#ffca28'},
    {name:'Class III',pct:'30-40%',hr:'120-140', sbp:'↓↓',     pp:'↓ PP', rr:'30-40', ms:'Confused', col:'#ff7043'},
    {name:'Class IV', pct:'>40%',  hr:'>140',    sbp:'↓↓↓',pp:'↓↓',  rr:'>35',   ms:'Lethargic',col:'#ef5350'}
  ];
  var rows=['HR (bpm)','SBP','Pulse Pres','RR (/min)','Neuro'];
  var keys=['hr','sbp','pp','rr','ms'];
  var sX=96, sY=16, cw=(W-sX)/4, hdrH=32, rh=(H-sY-hdrH)/5;
  for (var c=0; c<4; c++) {
    var cx=sX+c*cw, cl=cols[c];
    ctx.fillStyle=cl.col+'33'; ctx.fillRect(cx,sY,cw,hdrH);
    ctx.strokeStyle=cl.col+'88'; ctx.lineWidth=1; ctx.strokeRect(cx,sY,cw,hdrH);
    _lb(ctx, cl.name, cx+cw/2, sY+13, cl.col, 11);
    _lb(ctx, cl.pct+' vol', cx+cw/2, sY+25, cl.col, 9);
    for (var r=0; r<5; r++) {
      var ry=sY+hdrH+r*rh;
      ctx.fillStyle=(r%2===0)?cl.col+'0d':cl.col+'18';
      ctx.fillRect(cx,ry,cw,rh);
      ctx.strokeStyle='#222'; ctx.lineWidth=0.5; ctx.strokeRect(cx,ry,cw,rh);
      _lb(ctx, cl[keys[r]], cx+cw/2, ry+rh/2+4, '#e8e8e8', 10);
    }
  }
  for (var r=0; r<5; r++) {
    var ry=sY+hdrH+r*rh;
    ctx.fillStyle='#111'; ctx.fillRect(0,ry,sX,rh);
    ctx.strokeStyle='#333'; ctx.lineWidth=0.5; ctx.strokeRect(0,ry,sX,rh);
    _lb(ctx, rows[r], sX-6, ry+rh/2+4, '#888', 9, 'right');
  }
  _lb(ctx, 'Vol Loss', sX-6, sY+hdrH/2+4, '#555', 8, 'right');
}
"""

# ── Chart 4: Damage Control Resuscitation — Lethal Triad ─────────────────────
RF['damage_control'] = r"""
function _render(cv, ctrl, P) {
  var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
  _cl(ctx, W, H);
  var mx=50, my=20, pw=W-mx-16, ph=H-my-48;
  var groups=[
    {name:'Temperature',unit:'°C',trad:34.2,dcr:36.5,lo:32,hi:38,target:36.0,hib:true},
    {name:'pH',         unit:'',       trad:7.18, dcr:7.38,lo:7.0,hi:7.5,target:7.35,hib:true},
    {name:'INR',        unit:'',       trad:2.4,  dcr:1.3, lo:1.0,hi:3.0,target:1.5, hib:false}
  ];
  var gw=pw/3, bw=gw*0.27, gap=gw*0.07;
  for (var g=0; g<3; g++) {
    var gr=groups[g], gx=mx+g*gw, rng=gr.hi-gr.lo;
    var tN=(gr.trad-gr.lo)/rng, dN=(gr.dcr-gr.lo)/rng, tgN=(gr.target-gr.lo)/rng;
    if (!gr.hib) { tN=1-tN; dN=1-dN; tgN=1-tgN; }
    var tradH=Math.max(4,tN*ph*0.84), dcrH=Math.max(4,dN*ph*0.84);
    var targetY=my+ph-tgN*ph*0.84;
    var bx1=gx+gw/2-bw-gap/2, bx2=gx+gw/2+gap/2;
    var tMet=gr.hib?(gr.trad>=gr.target):(gr.trad<=gr.target);
    var dMet=gr.hib?(gr.dcr>=gr.target):(gr.dcr<=gr.target);
    ctx.fillStyle=(tMet?_GN:_RE)+'33'; ctx.fillRect(bx1,my+ph-tradH,bw,tradH);
    ctx.strokeStyle=tMet?_GN:_RE; ctx.lineWidth=1.5; ctx.strokeRect(bx1,my+ph-tradH,bw,tradH);
    _lb(ctx, gr.trad+gr.unit, bx1+bw/2, my+ph-tradH+14, tMet?_GN:_RE, 9);
    _lb(ctx, 'Trad', bx1+bw/2, my+ph-tradH+25, tMet?_GN:_RE, 8);
    ctx.fillStyle=(dMet?_GN:_RE)+'33'; ctx.fillRect(bx2,my+ph-dcrH,bw,dcrH);
    ctx.strokeStyle=dMet?_GN:_RE; ctx.lineWidth=1.5; ctx.strokeRect(bx2,my+ph-dcrH,bw,dcrH);
    _lb(ctx, gr.dcr+gr.unit, bx2+bw/2, my+ph-dcrH+14, dMet?_GN:_RE, 9);
    _lb(ctx, 'DCR', bx2+bw/2, my+ph-dcrH+25, dMet?_GN:_RE, 8);
    ctx.strokeStyle=_AM; ctx.lineWidth=1.5; ctx.setLineDash([4,3]);
    ctx.beginPath(); ctx.moveTo(gx+4,targetY); ctx.lineTo(gx+gw-4,targetY); ctx.stroke();
    ctx.setLineDash([]);
    _lb(ctx, 'target '+(gr.hib?'≥':'≤')+gr.target+gr.unit, gx+gw/2, targetY-5, _AM, 8);
    _lb(ctx, gr.name, gx+gw/2, my+ph+14, '#888', 10);
  }
  var lx=mx+pw-108, ly=my+4;
  ctx.fillStyle=_RE+'33'; ctx.fillRect(lx,ly,10,10);
  ctx.strokeStyle=_RE; ctx.lineWidth=1; ctx.strokeRect(lx,ly,10,10);
  _lb(ctx, 'Traditional', lx+40, ly+9, _RE, 9, 'center');
  ctx.fillStyle=_GN+'33'; ctx.fillRect(lx,ly+14,10,10);
  ctx.strokeStyle=_GN; ctx.lineWidth=1; ctx.strokeRect(lx,ly+14,10,10);
  _lb(ctx, 'DCR 1:1:1', lx+36, ly+23, _GN, 9, 'center');
  ctx.strokeStyle=_AM; ctx.lineWidth=1.5; ctx.setLineDash([4,3]);
  ctx.beginPath(); ctx.moveTo(lx,ly+30); ctx.lineTo(lx+10,ly+30); ctx.stroke();
  ctx.setLineDash([]);
  _lb(ctx, 'Target', lx+26, ly+34, _AM, 9, 'center');
}
"""

# ── Chart 5: Parkland Formula (interactive) ───────────────────────────────────
RF['parkland_formula'] = r"""
function _render(cv, ctrl, P) {
  var curWt=P.wt||70, curTbsa=P.tbsa||30;
  function draw() {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var total=4*curWt*curTbsa;
    var rate1=total/16, rate2=total/32;
    var maxRate=Math.max(200, Math.ceil(rate1/200+0.5)*200);
    _cl(ctx, W, H);
    var mx=68, my=18, pw=W-mx-16, ph=H-my-46;
    _ax(ctx, mx, my, pw, ph);
    var bw=pw*0.22, b1x=mx+pw*0.08, b2x=mx+pw*0.08+bw+pw*0.18;
    var h1=(rate1/maxRate)*ph, h2=(rate2/maxRate)*ph;
    ctx.fillStyle=_TE+'33'; ctx.fillRect(b1x,my+ph-h1,bw,h1);
    ctx.strokeStyle=_TE; ctx.lineWidth=2; ctx.strokeRect(b1x,my+ph-h1,bw,h1);
    _lb(ctx, rate1.toFixed(0)+' mL/hr', b1x+bw/2, my+ph-h1+14, _TE, 12);
    _lb(ctx, (total/2000).toFixed(1)+'L in 8h', b1x+bw/2, my+ph-h1+27, _TE, 9);
    _lb(ctx, 'First 8h', b1x+bw/2, my+ph+13, _TE, 10);
    ctx.fillStyle=_GN+'33'; ctx.fillRect(b2x,my+ph-h2,bw,h2);
    ctx.strokeStyle=_GN; ctx.lineWidth=2; ctx.strokeRect(b2x,my+ph-h2,bw,h2);
    _lb(ctx, rate2.toFixed(0)+' mL/hr', b2x+bw/2, my+ph-h2+14, _GN, 12);
    _lb(ctx, (total/2000).toFixed(1)+'L in 16h', b2x+bw/2, my+ph-h2+27, _GN, 9);
    _lb(ctx, 'Next 16h', b2x+bw/2, my+ph+13, _GN, 10);
    var step=Math.max(100,Math.ceil(maxRate/4/100)*100);
    for (var r=0; r<=maxRate; r+=step)
      _lb(ctx, r, mx-8, my+ph-(r/maxRate)*ph+4, _LB, 10, 'right');
    _rl(ctx, 'Infusion Rate (mL/hr)', mx-46, my+ph/2);
    var rx=b2x+bw+18;
    _lb(ctx, '4 × '+curWt+' × '+curTbsa+'%', rx+(W-mx-rx)/2, my+ph/2-12, _AM, 11);
    _lb(ctx, '= '+(total/1000).toFixed(1)+'L LR total', rx+(W-mx-rx)/2, my+ph/2+4, _AM, 12);
    _lb(ctx, 'UO goal: 0.5-1 mL/kg/hr', rx+(W-mx-rx)/2, my+ph/2+22, _LB, 9);
    _lb(ctx, '('+Math.round(curWt*0.5)+'-'+curWt+' mL/hr)', rx+(W-mx-rx)/2, my+ph/2+34, _LB, 9);
  }
  draw();
  if (ctrl) {
    ctrl.innerHTML='';
    var row=document.createElement('div');
    row.style.cssText='display:flex;flex-wrap:wrap;gap:6px;align-items:center;';
    row.appendChild(_mkS('Weight',40,120,5,curWt,function(v){return v+' kg';},function(v){curWt=v;draw();}));
    row.appendChild(_mkS('%TBSA', 5, 95, 5,curTbsa,function(v){return v+'%';},function(v){curTbsa=v;draw();}));
    ctrl.appendChild(row);
  }
}
"""

# ── Card definitions ──────────────────────────────────────────────────────────
# (front, back, tier, badge, did, chart_type, params_json, level_tag)

CARDS = [
    # ═══ lactate_clearance ═══════════════════════════════════════════════════
    (
        "The Surviving Sepsis Campaign 2021 targets lactate clearance of _______ "
        "at 2 hours and _______ at 6 hours as resuscitation endpoints.",

        ">=10% reduction at 2h | >=20% reduction at 6h | "
        "The green curve on the chart shows adequate clearance crossing below 4 mmol/L "
        "(shock threshold) by ~4 hours; the red curve fails to clear, remaining in the "
        "shock range despite adequate MAP.\n"
        "→ CCRN KEY: Lactate clearance is superior to MAP alone as a resuscitation "
        "endpoint -- patients can have occult hypoperfusion with MAP >65. Clearance "
        "<10% at 2h warrants reassessment of fluid responsiveness and source control.\n"
        "→ MASTERY NOTE: Type B lactic acidosis (liver failure, metformin toxicity, "
        "thiamine deficiency) impairs clearance without tissue hypoperfusion -- correlate "
        "with ScvO2 >70% and clinical exam before escalating vasopressors.",

        'tier-high',
        _SS,
        DID['sepsis'],
        'lactate_clearance',
        '{}',
        'chart-l1'
    ),
    (
        "A septic shock patient has initial lactate 7.4 mmol/L. At 6 hours with MAP 68 "
        "and UO 0.6 mL/kg/hr, repeat lactate is 6.9 mmol/L. Lactate clearance is "
        "_______, indicating _______.",

        "~6.8% at 6h (target >=20%) | Persistent occult hypoperfusion -- inadequate "
        "resuscitation despite acceptable hemodynamic endpoints | Next: reassess fluid "
        "responsiveness (PLR or POCUS), check ScvO2 (target >70%), confirm source "
        "control, optimize vasopressors.\n"
        "→ CCRN KEY: MAP >=65 + UO >=0.5 mL/kg/hr do NOT guarantee adequate perfusion. "
        "Lactate non-clearance at 6h doubles 28-day mortality independent of other "
        "endpoints in septic shock.\n"
        "→ MASTERY NOTE: ScvO2 >80% + non-clearing lactate = suspect cytopathic hypoxia "
        "(mitochondrial dysfunction). Cells cannot extract delivered O2 -- rising lactate "
        "reflects cellular hypoxia, not low-flow state. More fluid or vasopressors will "
        "not correct this.",

        'tier-critical',
        _SS,
        DID['sepsis'],
        'lactate_clearance',
        '{}',
        'chart-l2'
    ),
    (
        "A post-arrest patient has MAP 72, ScvO2 78%, and adequate UO, but lactate "
        "remains 8.1 mmol/L with no clearance at 8 hours. Before escalating "
        "resuscitation, the nurse considers _______ as an alternative explanation.",

        "Type B lactic acidosis -- most likely hepatic clearance failure (shock liver / "
        "ischemic hepatopathy) in the post-arrest state | Check LFTs, INR, bilirubin; "
        "shock liver peaks at 24-72h post-arrest. Also: thiamine (B1) deficiency "
        "(impairs pyruvate dehydrogenase), epinephrine infusion (drives glycolysis), "
        "metformin (if not held).\n"
        "→ CCRN KEY: Elevated lactate + improving hemodynamics + adequate ScvO2 = "
        "suspect impaired hepatic clearance, not ongoing tissue hypoperfusion. The liver "
        "clears ~70% of circulating lactate.\n"
        "→ MASTERY NOTE: Thiamine 200 mg IV should be given empirically in any "
        "post-arrest or septic patient with non-clearing lactate -- it is the essential "
        "cofactor for pyruvate dehydrogenase (pyruvate -> acetyl-CoA instead of lactate). "
        "Safe, inexpensive, and effects are seen within minutes.",

        'tier-critical',
        _SS,
        DID['sepsis'],
        'lactate_clearance',
        '{}',
        'chart-l3'
    ),

    # ═══ do2_vo2_curve ═══════════════════════════════════════════════════════
    (
        "On the DO2/VO2 curve, oxygen consumption becomes supply-dependent below the "
        "critical DO2 threshold of approximately _______. Above this threshold, VO2 "
        "_______.",

        "~300-330 mL/min/m2 | VO2 plateaus at ~200-220 mL/min/m2 regardless of further "
        "DO2 increases (supply-independent region) | Below critical DO2: anaerobic "
        "metabolism begins, lactate rises, organ dysfunction develops.\n"
        "→ CCRN KEY: DO2 = CI x CaO2 x 10. Optimize all three components: Hgb/SaO2 "
        "(CaO2), cardiac output (CI), and arterial oxygen content. Targeting ScvO2 >70% "
        "is a surrogate for adequate supply-demand balance above critical DO2.\n"
        "→ MASTERY NOTE: The inflection point (critical DO2) varies by patient and "
        "metabolic state -- fever, shivering, and pain increase VO2 demand and shift "
        "the critical threshold higher. Temperature management and analgesia reduce "
        "VO2 demand in critically ill patients.",

        'tier-high',
        _SS,
        DID['sepsis'],
        'do2_vo2_curve',
        '{}',
        'chart-l1'
    ),
    (
        "In sepsis, the DO2/VO2 curve shows _______, meaning VO2 continues rising "
        "proportionally with DO2 even above normal delivery. This is caused by _______, "
        "and results in ScvO2 that may be _______.",

        "Pathological supply dependency | Microvascular shunting + mitochondrial "
        "dysfunction (cytopathic hypoxia) -- cells cannot extract or utilize delivered "
        "O2 | ScvO2 may be falsely elevated (>75-80%) -- venous blood returns "
        "O2-rich because cells cannot use it, NOT because delivery is excessive.\n"
        "→ CCRN KEY: High ScvO2 in septic shock does NOT reliably indicate adequate "
        "resuscitation. Use lactate trajectory, base deficit, and clinical perfusion "
        "markers alongside ScvO2. O2 extraction ratio (OER = VO2/DO2) is normally "
        "25-30%; in cytopathic hypoxia OER may be <20% despite cellular hypoxia.\n"
        "→ MASTERY NOTE: The sepsis curve in the chart stays supply-dependent across "
        "the entire DO2 range -- no plateau forms. This is pathognomonic of distributive "
        "shock with extraction failure, not simple low-output states where increasing "
        "CO or Hgb would restore the plateau.",

        'tier-critical',
        _SS,
        DID['sepsis'],
        'do2_vo2_curve',
        '{}',
        'chart-l2'
    ),
    (
        "A septic patient has CI 4.8 L/min/m2, Hgb 10 g/dL, SaO2 98%, ScvO2 84%, and "
        "lactate 6.2 mmol/L rising. DO2 is adequate. The nurse interprets this pattern "
        "as _______ and identifies the priority intervention as _______.",

        "Pathological O2 supply dependency with cytopathic hypoxia -- adequate delivery, "
        "impaired cellular utilization | Priority: rule out and drain undrained infectious "
        "source (definitive source control), optimize antibiotic timing and spectrum, "
        "thiamine IV empirically, avoid vasopressor escalation as the sole response to "
        "rising lactate when CI is already adequate.\n"
        "→ CCRN KEY: Do NOT interpret ScvO2 >80% as 'all is well' when lactate is "
        "rising. Dysregulated O2 extraction is a defining feature of late septic shock "
        "and does not respond to more fluid or vasopressors -- treat the underlying "
        "cause (antibiotics + source control).\n"
        "→ MASTERY NOTE: Lactate >4 mmol/L + ScvO2 >80% + CI >4 L/min/m2 = "
        "cytopathic hypoxia triad until proven otherwise. This pattern carries higher "
        "mortality than low-DO2 shock. Organ support (renal replacement, ventilator "
        "optimization) and metabolic resuscitation (thiamine, ascorbic acid) are the "
        "relevant levers -- not further DO2 augmentation.",

        'tier-critical',
        _SS,
        DID['sepsis'],
        'do2_vo2_curve',
        '{}',
        'chart-l3'
    ),

    # ═══ hemorrhagic_shock ═══════════════════════════════════════════════════
    (
        "In ATLS hemorrhagic shock classification, systolic blood pressure first falls "
        "in Class _______. Heart rate and _______ are earlier and more sensitive "
        "indicators of hemorrhage.",

        "Class III (30-40% blood volume loss, ~1,500-2,000 mL) | Classes I and II "
        "compensate via tachycardia + increased SVR (catecholamine surge raises diastolic "
        "before systolic falls) | Pulse pressure narrowing (PP = SBP - DBP) is the "
        "earliest vital sign -- PP <25 mmHg indicates Class II even with 'normal' SBP.\n"
        "→ CCRN KEY: BP is a late indicator of hemorrhagic shock. A healthy adult can "
        "lose up to 30% of blood volume (1,500 mL in 70 kg) before SBP drops. Narrow "
        "pulse pressure + tachycardia = early hemorrhagic shock.\n"
        "→ MASTERY NOTE: Athletes and beta-blocker users may not mount tachycardia -- "
        "HR alone is unreliable. Use level of consciousness, capillary refill, and pulse "
        "pressure together. Elderly patients (reduced cardiac reserve) may decompensate "
        "sooner at lower volume losses.",

        'tier-high',
        _MT,
        DID['mods_trauma'],
        'hemorrhagic_shock',
        '{}',
        'chart-l1'
    ),
    (
        "A 70 kg trauma patient has HR 136, SBP 74, RR 38, and GCS 13. ATLS class is "
        "_______, estimated blood loss is _______, and the nurse immediately activates "
        "_______ targeting a product ratio of _______.",

        "Class III-IV | >1,500 mL (>30% of estimated 4.9L blood volume) | Massive "
        "Transfusion Protocol (MTP) | 1:1:1 (pRBC:FFP:platelets) | Also: TXA 1g IV "
        "if within 3 hours of injury; CaCl2 10 mL of 10% per 4 units pRBC; permissive "
        "hypotension (SBP 80-90 penetrating, MAP 50-65 blunt) until surgical control.\n"
        "→ CCRN KEY: PROPPR trial (2015): 1:1:1 MTP reduced 24h mortality and "
        "exsanguination death vs. historical ratios. Activate on clinical grounds -- "
        "do NOT wait for lab confirmation of coagulopathy.\n"
        "→ MASTERY NOTE: Avoid large-volume crystalloid (>1-2L): causes dilutional "
        "coagulopathy, hypothermia (room-temp fluid), and hyperchloremic acidosis (NS). "
        "In Class III-IV, blood products ARE the resuscitation fluid. TXA efficacy "
        "drops to zero >3h from injury (CRASH-2 trial) -- time matters.",

        'tier-critical',
        _MT,
        DID['mods_trauma'],
        'hemorrhagic_shock',
        '{}',
        'chart-l2'
    ),
    (
        "Pulse pressure narrows in early hemorrhagic shock before SBP falls because "
        "_______. In a 70 kg patient with Class II hemorrhage, an expected pulse "
        "pressure would be _______.",

        "Hemorrhage reduces preload -> decreased stroke volume -> baroreceptor reflex "
        "-> catecholamine surge -> increased HR + SVR -> diastolic BP rises (vasoconstriction) "
        "before systolic falls -> PP narrows | PP <25 mmHg (e.g., 110/88 = PP 22) in "
        "Class II with 15-30% volume loss (750-1,500 mL).\n"
        "→ CCRN KEY: Pulse pressure is the earliest vital sign change in hemorrhagic "
        "shock. Normal PP = 40 mmHg. PP <25 mmHg despite normal SBP = Class II hemorrhage "
        "-- do not be falsely reassured by a systolic of 110-115 mmHg.\n"
        "→ MASTERY NOTE: PP narrowing reflects the sum of two concurrent changes: "
        "diastolic rises (vasoconstriction) and systolic stays same or falls slightly "
        "(reduced SV). This hemodynamic signature is also seen in pericardial tamponade "
        "(Beck's triad) and tension pneumothorax -- distinguish by JVD, tracheal "
        "deviation, and breath sounds.",

        'tier-critical',
        _MT,
        DID['mods_trauma'],
        'hemorrhagic_shock',
        '{}',
        'chart-l3'
    ),

    # ═══ damage_control ═══════════════════════════════════════════════════════
    (
        "Damage control resuscitation uses a blood product ratio of _______, "
        "replacing the historical crystalloid-heavy approach. Each 4 units pRBC "
        "should be accompanied by _______ to prevent a common MTP complication.",

        "1:1:1 (pRBC:FFP:platelets) -- mimics whole blood composition | CaCl2 10 mL "
        "of 10% solution (or Ca-gluconate 30 mL of 10%) per 4 units pRBC -- stored "
        "blood citrate chelates ionized Ca2+, causing impaired clotting AND cardiac "
        "dysfunction.\n"
        "→ CCRN KEY: The chart shows Temperature, pH, and INR for Traditional vs DCR "
        "at 6h post-injury. Traditional bars (red) fall short of all targets; DCR bars "
        "(green) meet all three. PROPPR trial: 1:1:1 reduced 24h mortality by 20% vs "
        "historical ratios.\n"
        "→ MASTERY NOTE: Hypocalcemia is often called the 'fourth component' of the "
        "lethal triad. Ionized Ca2+ (target >1.1 mmol/L) is essential for both clot "
        "formation (factor cofactor, thrombin activation) and myocardial contractility. "
        "Monitor iCa2+ every 30-60 min during active MTP and replace aggressively.",

        'tier-high',
        _MT,
        DID['mods_trauma'],
        'damage_control',
        '{}',
        'chart-l1'
    ),
    (
        "The lethal triad of trauma coagulopathy consists of _______, _______, and "
        "_______. DCR corrects each component by _______.",

        "Hypothermia + Acidosis + Coagulopathy (each worsens the other two in a "
        "self-amplifying cycle) | Hypothermia: warm fluids to 39C, forced-air "
        "warming, raise OR temp -- clotting enzymes lose 50% activity at 33C. "
        "Acidosis: 1:1:1 blood products instead of NS/crystalloid, rapid hemorrhage "
        "control -- pH <7.2 = near-complete coagulation failure. Coagulopathy: 1:1:1 "
        "MTP + TXA within 3h + calcium replacement.\n"
        "→ CCRN KEY: No coagulopathy treatment is effective in the presence of "
        "hypothermia and acidosis -- all three must be corrected simultaneously. "
        "A pH of 7.1 renders nearly all clotting factors functionally inactive "
        "regardless of how many products are given.\n"
        "→ MASTERY NOTE: Clotting factor activity decreases exponentially with falling "
        "temperature and pH. This is why traditional labs (PT/INR) drawn at 37C in the "
        "lab may look 'normal' while the patient at 33C is actually coagulopathic. "
        "TEG/ROTEM is performed at the patient's actual temperature -- use it to guide "
        "product choice during massive transfusion.",

        'tier-critical',
        _MT,
        DID['mods_trauma'],
        'damage_control',
        '{}',
        'chart-l2'
    ),
    (
        "In damage control resuscitation, permissive hypotension targets MAP _______ "
        "for penetrating trauma and MAP _______ for traumatic brain injury. This "
        "strategy is contraindicated when _______.",

        "MAP 50 mmHg (SBP 80-90 mmHg) for penetrating trauma without TBI | "
        "MAP >=80 mmHg when TBI is confirmed or suspected (CPP = MAP - ICP; "
        "adequate CPP requires higher MAP) | Contraindicated: confirmed/suspected TBI, "
        "known severe CAD or cerebrovascular disease, elderly with chronic hypertension "
        "(impaired autoregulation), hypotension lasting >60 minutes.\n"
        "→ CCRN KEY: Permissive hypotension prevents dislodging the clot and diluting "
        "clotting factors during active hemorrhage. Once surgical hemostasis is achieved, "
        "resuscitate to normal MAP immediately. Base excess worse than -6 mEq/L predicts "
        "ongoing coagulopathy and need for continued MTP.\n"
        "→ MASTERY NOTE: Duration of permissive hypotension matters -- each additional "
        "15 minutes of MAP <60 increases end-organ ischemia risk (kidney, gut, liver). "
        "The goal is the MINIMUM acceptable pressure for the MINIMUM time to definitive "
        "hemorrhage control. Avoid comfort with sustained low BP -- it is a strategy "
        "with a deadline, not a goal.",

        'tier-critical',
        _MT,
        DID['mods_trauma'],
        'damage_control',
        '{}',
        'chart-l3'
    ),

    # ═══ parkland_formula ════════════════════════════════════════════════════
    (
        "Using the Parkland formula, a 70 kg patient with 40% TBSA burns requires "
        "_______ mL total LR. The first-8-hour infusion rate (from time of injury) "
        "is _______ mL/hr.",

        "4 x 70 x 40 = 11,200 mL total LR | First 8h: 5,600 mL / 8h = 700 mL/hr | "
        "Next 16h: 5,600 mL / 16h = 350 mL/hr | Clock starts from TIME OF INJURY, "
        "not hospital arrival. Use the slider to see how volume scales with weight "
        "and TBSA.\n"
        "→ CCRN KEY: Titrate all Parkland rates to UO 0.5-1 mL/kg/hr (35-70 mL/hr "
        "for 70 kg). The formula provides a starting point, not a fixed rate -- adjust "
        "hourly based on UO. Use LR, not NS (NS causes hyperchloremic acidosis).\n"
        "→ MASTERY NOTE: Only count 2nd and 3rd degree burns in %TBSA for Parkland -- "
        "superficial (1st degree) burns do NOT contribute to fluid shift. The Rule of "
        "Nines estimates TBSA: each arm 9%, each leg 18%, anterior trunk 18%, posterior "
        "trunk 18%, head 9%, perineum 1%.",

        'tier-high',
        _BT,
        DID['burns_tox'],
        'parkland_formula',
        '{"wt":70,"tbsa":40}',
        'chart-l1'
    ),
    (
        "An 80 kg patient with 55% TBSA burns arrives 2.5 hours post-injury. "
        "The Parkland first-8h volume is _______ mL. The corrected infusion rate "
        "for the remaining time window is _______.",

        "4 x 80 x 55 / 2 = 8,800 mL for first 8h | 8,800 mL / 5.5h remaining = "
        "1,600 mL/hr (rounded) | Clock started at injury -- 2.5h have elapsed, "
        "leaving only 5.5h to deliver the full first-half volume. Adjust the slider "
        "to 80 kg / 55% to verify.\n"
        "→ CCRN KEY: Never restart the 8-hour clock at hospital arrival -- this is a "
        "CCRN examination trap. Formula: (first-half volume) / (8h - elapsed hours) = "
        "corrected rate. Always confirm elapsed time from the emergency report.\n"
        "→ MASTERY NOTE: If arrival is >6h post-burn with no prior resuscitation, "
        "aggressive catch-up is necessary but risk of over-resuscitation increases "
        "exponentially. Monitor bladder pressure q4h in burns >20% TBSA. If IAP >12 "
        "mmHg, reduce rate toward strict 0.5 mL/kg/hr UO target despite the volume "
        "deficit.",

        'tier-critical',
        _BT,
        DID['burns_tox'],
        'parkland_formula',
        '{"wt":80,"tbsa":55}',
        'chart-l2'
    ),
    (
        "A burn patient receiving Parkland resuscitation develops bladder pressure "
        "28 mmHg, progressive abdominal distension, and worsening PaO2/FiO2 ratio. "
        "The nurse recognizes _______ caused by _______, and anticipates _______.",

        "Abdominal compartment syndrome (ACS) | Fluid creep -- resuscitation volumes "
        "exceeding Parkland formula targets ('over-resuscitation'), often from over-"
        "titration when UO >1 mL/kg/hr is mistakenly accepted as acceptable | "
        "Anticipate: decompressive laparotomy if IAP >20 mmHg + new organ dysfunction; "
        "reduce rate to strict UO 0.5 mL/kg/hr; consider albumin 5% after hour 8 "
        "to reduce crystalloid volume (0.5 mL/kg/%TBSA over 8h).\n"
        "→ CCRN KEY: IAP >12 mmHg = intra-abdominal hypertension; >20 mmHg + new organ "
        "dysfunction = ACS requiring surgical decompression. Monitor q4-6h in all burns "
        ">20% TBSA. Fluid creep also causes extremity compartment syndrome, orbital "
        "compartment syndrome, and ARDS.\n"
        "→ MASTERY NOTE: Risk factors for fluid creep: inhalation injury (adds ~2 "
        "mL/kg/%TBSA per some protocols), opioid-induced urinary retention masking true "
        "UO (causing over-titration), delayed presentations, and pre-existing renal "
        "disease. Colloid supplementation at 8-24h reduces total crystalloid requirement "
        "by 30-40% in major burns -- consult burn surgery before initiation.",

        'tier-critical',
        _BT,
        DID['burns_tox'],
        'parkland_formula',
        '{"wt":80,"tbsa":60}',
        'chart-l3'
    ),
]

# ── Build pipeline ────────────────────────────────────────────────────────────
def main():
    db, models, existing_guids = load_deck(DECK_PATH, WORK_DIR)
    main_css  = get_main_css(models)
    CHART_CSS = main_css + CHART_CSS_ADDON

    validator = CardValidator()
    now       = int(time.time())
    nid_base  = now * 1000
    added     = 0

    print(f"{'='*65}")
    print(f"CHUNK {CHUNK_NUM} — Validating {len(CARDS)} cards")
    print(f"{'='*65}")

    for i, card in enumerate(CARDS):
        front, back, tier, badge, did, ctype, pj, ltag = card
        issues = validator.validate(f'c{CHUNK_NUM}_{i}', front, back, badge)
        warns  = validator.results[-1].get('warnings', [])
        ok     = not issues
        w_str  = ' W8' if warns else ''
        print(f"  {'OK' if ok else 'FAIL'} [{ctype}|{ltag}]{w_str}  {front[:65]}")
        if not ok:
            for iss in issues: print(f"      x {iss}")

    print(validator.report())
    print()

    for i, card in enumerate(CARDS):
        front, back, tier, badge, did, ctype, pj, ltag = card

        issues = validator.validate(f'c{CHUNK_NUM}_{i}_ins', front, back, badge)
        if issues:
            print(f"  SKIP (invalid): {front[:55]}")
            continue

        chart_idx = CHART_ORDER.index(ctype) if ctype in CHART_ORDER else i
        mid_int   = MID_BASE + chart_idx
        mkey      = str(mid_int)

        if mkey not in models:
            qfmt, afmt = make_chart_template(
                ctype, pj, RF[ctype], SHARED_JS, CHART_CSS)
            register_chart_model(models, mid_int, ctype, did, qfmt, afmt, CHART_CSS)

        guid = make_guid(front, back)
        if guid in existing_guids:
            print(f"  SKIP (dup): {front[:50]}")
            continue
        existing_guids.add(guid)

        flds = '\x1f'.join([safe_html(front), safe_html(back), tier, badge])
        sfld = re.sub(r'<[^>]+>', '', front)[:100]
        nid  = nid_base + i * 3
        tags = f' ccrn-pccn-v6 chunk-{CHUNK_NUM} {ltag} '

        insert_card(db, nid, nid+1, guid, mkey, flds, sfld, did, tags, now)
        added += 1
        print(f"  + [{ctype}|{ltag}]  {front[:65]}")

    save_deck(db, models, WORK_DIR, OUT_PATH)

    db2 = sqlite3.connect(os.path.join(WORK_DIR, 'collection.anki2'))
    total = db2.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    db2.close()

    print(f"\n{'='*65}")
    print(f"  Chunk {CHUNK_NUM}: {added} cards added | Total deck: {total} cards")
    print(f"{'='*65}")


if __name__ == '__main__':
    main()
