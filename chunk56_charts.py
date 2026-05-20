#!/usr/bin/env python3
"""chunk56_charts.py — Ph7 Pharmacology: Monitoring Thresholds (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_55.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_56.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c56')
CHUNK_NUM   = 56
MID_BASE    = 1_800_005_125
CHART_ORDER = ['tdm_targets', 'nephrotox_monitor', 'pressor_endpoints',
               'sedation_endpoints', 'anticoag_monitoring']

_NM = 'Ph7 \U0001f7e1 T3 · Pharmacology — Monitoring Thresholds'

RF = {}

# ── Chart 1: TDM Targets ──────────────────────────────────────────────────────
RF['tdm_targets'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var rows=[
        {n:'Vancomycin', tgt:'AUC/MIC:\n400–600 mg·h/L\n(NOT trough alone)',
         whn:'All patients on\nIV vanco >48h\nor renal impairment',
         tim:'Draw 2 levels\n(peak+trough)\nfor Bayesian PK',
         note:'2020 ASHP/SIDP/IDSA: trough-only monitoring REPLACED by AUC-guided dosing\nAUC >600: ↑ nephrotoxicity; AUC <400: ↑ treatment failure for serious MRSA infections\nVanco+PIPC-TAZO synergistic AKI: switch to meropenem if MRSA coverage needed',
         c:'#4488cc'},
        {n:'Digoxin', tgt:'0.5–2.0 ng/mL\n(HF target:\n0.5–0.9 ng/mL)',
         whn:'Day 5+ (steady\nstate) or suspected\ntoxicity/AKI',
         tim:'≥6–8h post-dose\n(distribution\nphase complete)',
         note:'HF: lower target 0.5–0.9 ng/mL — DIG trial: mortality neutral; only ↓ hospitalizations\nTOXICITY (>2 ng/mL): N/V, xanthopsia, bradycardia, blocks, PVCs/VT — treat with Digibind\nHypokalemia and hypomagnesemia INCREASE toxicity at ANY level — always correct lytes',
         c:'#3a9a5c'},
        {n:'Phenytoin\n(Free)', tgt:'Free: 1–2 mg/L\nTotal: 10–20 mg/L\n(if albumin normal)',
         whn:'Low albumin (<2)\nrenal failure\nDrug interactions',
         tim:'Trough (just\nbefore next dose)\nor 2h post-IV load',
         note:'ALWAYS use FREE phenytoin level when albumin <2 g/dL or uremia — total is falsely low\nWinter-Tozer correction: adjusted total = measured / (0.2×albumin + 0.1)\nFosphenytoin (IV): less phlebitis than phenytoin; same free phenytoin levels result',
         c:'#cc9922'},
        {n:'Aminogly-\ncosides', tgt:'Peak ≥8×MIC\nTrough <1 mg/L\n(EID gentamicin)',
         whn:'Before dose 2\n(trough) and\n1h post-dose (peak)',
         tim:'EID: pre-dose\nlevel <1 mg/L\n(48–72h after start)',
         note:'Extended-interval dosing (EID): 5–7 mg/kg q24h — maximizes Cmax/MIC + ↓ nephrotox\nPeak >10 mg/L (gentamicin): bactericidal + post-antibiotic effect; trough <1 = no accumulation\nOtotoxicity (irreversible): assess baseline hearing; risk with loop diuretic co-administration',
         c:'#9060c0'},
        {n:'Lithium', tgt:'Acute: 0.8–1.2\nMaintenance:\n0.6–1.0 mEq/L',
         whn:'Every 5 days\nuntil stable; AKI;\ndehydration',
         tim:'12h trough\n(standardized)\npost-dose',
         note:'TOXICITY (>1.5 mEq/L): coarse tremor, confusion, hyperreflexia, seizures — dialysis if >4.0\nRenal clearance parallels sodium — volume depletion (NSAIDs, thiazides) rapidly ↑ levels\nICU context: NSAIDs and ACEI/ARB both increase lithium levels — check on all admissions',
         c:'#cc4444'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/rows.length);
    var xs=[4,100,185,270,360,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Drug','Target Level','When to Level','Timing','ICU Notes'];
    ctx.font='bold 7.5px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    rows.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=d.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=d.c;ctx.font='bold 7px sans-serif';ctx.textAlign='left';
        d.n.split('\n').forEach(function(l,li){ctx.fillText(l,xs[0]+2,ry+rh/2-4+li*9);});
        ctx.fillStyle='#eedd88';ctx.font='6px sans-serif';
        d.tgt.split('\n').forEach(function(l,li){ctx.fillText(l,xs[1]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#aaddaa';ctx.font='6px sans-serif';
        d.whn.split('\n').forEach(function(l,li){ctx.fillText(l,xs[2]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#99ccff';ctx.font='6px sans-serif';
        d.tim.split('\n').forEach(function(l,li){ctx.fillText(l,xs[3]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#99aabb';ctx.font='5.8px sans-serif';
        d.note.split('\n').forEach(function(l,li){ctx.fillText(l,xs[4]+2,ry+6+li*9.5);});
        ctx.globalAlpha=1;
        ctx.strokeStyle='#222';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(0,ry+rh);ctx.lineTo(W,ry+rh);ctx.stroke();
    });
    [xs[1],xs[2],xs[3],xs[4]].forEach(function(x){
        ctx.strokeStyle='#222';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(x,hdrH);ctx.lineTo(x,H);ctx.stroke();
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        var lbs=['Vancomycin','Digoxin','Phenytoin','Aminogly','Lithium'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,rows[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: Nephrotoxicity Monitoring ────────────────────────────────────────
RF['nephrotox_monitor'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var rows=[
        {n:'Amino-\nglycosides', mech:'Proximal tubule\naccumulation\n(renal cortex)',
         scr:'SCr ↑ 0.3 mg/dL\nover 48h or\n>1.5× baseline',
         act:'Hold / extend\ninterval; check\ntrough level',
         note:'Onset: 5–10 days into treatment — early SCr rise often precedes symptoms\nRisk factors: pre-existing AKI, volume depletion, advanced age, loop diuretics co-admin\nAmino-associated AKI usually reversible — stop drug and tubular cells regenerate within 2–4 weeks',
         c:'#cc4444'},
        {n:'Vanco +\nPIPC-TAZO', mech:'Synergistic\ntubular toxicity\n↑ vanco AUC',
         scr:'SCr ↑ 0.5 mg/dL\nwithin 24h of\ncombination',
         act:'Switch pip-tazo\nto meropenem;\nmonitor AUC',
         note:'PIPC-TAZO inhibits tubular vancomycin secretion → ↑ vancomycin AUC → nephrotoxicity\nCANWARD/Blumenthal studies: combo 3–5× higher AKI vs meropenem+vanco\nMonitor SCr daily in first 72h of combination; switch early if rising',
         c:'#cc8844'},
        {n:'IV Contrast\n(CMN)', mech:'Renal\nvasoconstriction\n+ direct tubular',
         scr:'SCr ↑ 0.5 mg/dL\nor 25% within\n48–72h post',
         act:'Pre-hydrate\n(NS or NaHCO3);\nminimize volume',
         note:'Contrast-associated nephropathy (CAN): highest risk eGFR <30, DM, dehydration, CHF\nPre-hydration: 1 mL/kg/h NS 6–12h pre+post procedure (or NaHCO3 154 mEq/L at 3 mL/kg/h × 1h)\nNAC 600–1200 mg PO BID × 2 days: mixed evidence but cheap + safe; still widely used',
         c:'#4488cc'},
        {n:'Calcineurin\nInhibitors', mech:'Afferent arteriole\nvasoconstriction\n(TXA2/endothelin)',
         scr:'SCr ↑ from\nbaseline; level\nabove target range',
         act:'Reduce dose;\ncheck trough;\nhold nephrotoxins',
         note:'Tacrolimus: trough goal 8–12 ng/mL (early post-transplant); 5–8 ng/mL (maintenance)\nToxicity REVERSIBLE with dose reduction — biopsy if SCr rising and level therapeutic\nDrug interactions: CYP3A4 inhibitors (azoles, diltiazem) drastically ↑ levels → toxicity',
         c:'#9060c0'},
        {n:'Colistin\nNSAIDs', mech:'Direct tubular\ntoxicity (colistin)\nPG inhibition',
         scr:'Colistin: SCr\ndaily in ICU;\nNSAIDs: any rise',
         act:'Monitor SCr\nq24–48h; avoid\ncombinations',
         note:'Colistin: last-resort for MDR GNR (Acinetobacter, Pseudomonas) — nephrotox 50–60%\nColistin + aminoglycoside or vanco: extreme nephrotoxicity — avoid unless no alternatives\nNSAIDs in ICU: prostaglandin-dependent renal perfusion in low-flow states → acute HRS/prerenal AKI',
         c:'#3a9a5c'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/rows.length);
    var xs=[4,95,185,270,360,616];
    ctx.fillStyle='#1a0a0a';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Drug','Mechanism','SCr Trigger','Action','ICU Notes'];
    ctx.font='bold 7.5px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    rows.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#180d0d':'#1a1010';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=d.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=d.c;ctx.font='bold 7px sans-serif';ctx.textAlign='left';
        d.n.split('\n').forEach(function(l,li){ctx.fillText(l,xs[0]+2,ry+rh/2-4+li*9);});
        ctx.fillStyle='#ff9966';ctx.font='6px sans-serif';
        d.mech.split('\n').forEach(function(l,li){ctx.fillText(l,xs[1]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#ee8888';ctx.font='6px sans-serif';
        d.scr.split('\n').forEach(function(l,li){ctx.fillText(l,xs[2]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#aaddaa';ctx.font='6px sans-serif';
        d.act.split('\n').forEach(function(l,li){ctx.fillText(l,xs[3]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#99aabb';ctx.font='5.8px sans-serif';
        d.note.split('\n').forEach(function(l,li){ctx.fillText(l,xs[4]+2,ry+6+li*9.5);});
        ctx.globalAlpha=1;
        ctx.strokeStyle='#222';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(0,ry+rh);ctx.lineTo(W,ry+rh);ctx.stroke();
    });
    [xs[1],xs[2],xs[3],xs[4]].forEach(function(x){
        ctx.strokeStyle='#222';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(x,hdrH);ctx.lineTo(x,H);ctx.stroke();
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        var lbs=['Aminogly','Vanco+PipTaz','IV Contrast','Calcineurin','Colistin'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,rows[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 3: Vasopressor Endpoints ────────────────────────────────────────────
RF['pressor_endpoints'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['MAP Targets by Condition','CO/CI Endpoints','Shock Reversal Criteria'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a0a0a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#3a1a1a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#cc4444':'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0505';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+12;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#cc4444';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8px sans-serif';ctx.fillText(val,lm+175,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#3a1a1a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('MAP Targets — Individualized by Diagnosis and End-Organ Needs:','','#cc4444');
        hr();
        rw('Septic shock:','MAP ≥65 mmHg (SEPSISPAM: 65 vs 85 — no mortality diff; ↑ AFib at 85)','#eedd88','#99bbdd');
        nt('Higher MAP (75–85) may benefit chronic hypertensive patients — individualize after 6h');
        rw('TBI + ICP:','MAP ≥80 mmHg; CPP = MAP − ICP; target CPP 60–70 mmHg (BTF guidelines)','#eedd88','#99bbdd');
        nt('CPP <50: cerebral ischemia; CPP >70: ARDS risk from aggressive vasopressor use');
        hr();
        rw('Post-cardiac arrest:','MAP 65–80 mmHg (COMACARE pilot — no benefit from MAP >85 post-ROSC)','#eedd88','#99bbdd');
        rw('Hemorrhagic stroke:','SBP 140–160 in ICH (INTERACT2 — lower BP safe; ATACH-2 SBP <140 = ↑ AKI)','#eedd88','#99bbdd');
        rw('Ischemic stroke:','SBP ≤185/110 if tPA given; permissive HTN up to 220 if no tPA (first 24h)','#eedd88','#99bbdd');
        hr();
        rw('Cardiogenic shock:','MAP ≥65 (avoid aggressive vasopressors — ↑ afterload worsens CI)','#eedd88','#99bbdd');
        nt('IABP: reduces afterload + augments diastolic filling — does NOT improve CI (IABP-SHOCK II)');
    } else if(sel===1){
        rw('Cardiac Output / Cardiac Index Endpoints:','','#cc4444');
        hr();
        rw('Normal values:','CO: 4–8 L/min | CI: 2.5–4.0 L/min/m² | SVI: 33–47 mL/m²','#eedd88','#99bbdd');
        nt('CI = CO / BSA — accounts for body size; preferred metric in ICU monitoring');
        hr();
        rw('Cardiogenic shock:','CI <2.2 L/min/m² + SBP <90 + congestion + end-organ hypoperfusion','#cc4444','#ffaa99');
        nt('SHOCK trial (1999): early revascularization ↓ 6-month mortality in AMI-cardiogenic shock');
        rw('Treatment target:','CI >2.2 L/min/m² with dobutamine or milrinone; consider VA-ECMO if refractory','#3a9a5c','#99ddaa');
        hr();
        rw('SvO2 / ScvO2:','Mixed venous SvO2 ≥65% | Central ScvO2 ≥70% = adequate DO2/VO2 balance','#eedd88','#99bbdd');
        nt('Low SvO2 (<60%): ↑ oxygen extraction → cardiac output inadequate for demand');
        nt('PA catheter: SvO2 from PA; ScvO2 from central line — ScvO2 typically 5–7% higher than SvO2');
        rw('DO2 formula:','DO2 = CO × CaO2 = CO × (Hgb × 1.34 × SaO2 + 0.003 × PaO2) × 10','#cc9922','#eecc88');
    } else {
        rw('Shock Reversal Criteria — Evidence of Adequate Resuscitation:','','#cc4444');
        hr();
        rw('MAP:','≥65 mmHg off vasopressors OR MAP ≥65 on stable/weaning dose','#3a9a5c','#99ddaa');
        rw('Heart rate:','HR <100 bpm (septic shock); normalize from admission tachycardia','#3a9a5c','#99ddaa');
        rw('Urine output:','UO ≥0.5 mL/kg/hr (sustained over 2–4h = improving renal perfusion)','#3a9a5c','#99ddaa');
        hr();
        rw('Lactate clearance:','≥10% decline at 2h from baseline OR absolute lactate <2 mmol/L','#eedd88','#99bbdd');
        nt('LACTATES trial: lactate-guided therapy ↓ in-hospital mortality vs clinical assessment alone');
        rw('ScvO2:','≥70% (ProCESS, ProMISe, ARISE: EGDT not superior to usual care when started late)','#eedd88','#99bbdd');
        hr();
        rw('Skin perfusion:','Cap refill <3 sec, warm extremities, no mottling beyond knees','#eedd88','#99bbdd');
        rw('SOFA trend:','SOFA score declining from admission peak (each 1-pt ↓ = ↓ mortality)','#eedd88','#99bbdd');
        nt('Lactate >4 mmol/L persistent at 6h: high mortality despite resuscitation — escalate care');
    }
    if(ctrl){
        ctrl.innerHTML='';
        var crow=document.createElement('div');crow.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        ['MAP Targets','CO/CI','Shock Reversal'].forEach(function(lb,i){
            var b=_mkB(lb,'#cc4444',sel===i,function(on){
                var p2={sel:on?i:0};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
            });crow.appendChild(b);
        });
        ctrl.appendChild(crow);
    }
}
"""

# ── Chart 4: Sedation Endpoints ────────────────────────────────────────────────
RF['sedation_endpoints'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['RASS Targets','CPOT Pain Scale','SAT / SBT Protocol'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#0a0a1a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a2a4a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#9060c0':'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#060508';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+12;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#9060c0';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8px sans-serif';ctx.fillText(val,lm+180,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a2a4a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('Richmond Agitation-Sedation Scale (RASS) — Targets by Clinical Status:','','#9060c0');
        hr();
        rw('ICU default target:','RASS 0 to −1 (Alert/Calm or Drowsy/arousable) — PADIS guideline 2018','#eedd88','#99bbdd');
        nt('Light sedation superior to deep: ↓ ICU LOS, ↓ delirium, ↓ MV duration (SLEAP trial)');
        hr();
        rw('RASS scale:','−5=Unarousable | −4=Deep | −3=Moderate | −2=Light | −1=Drowsy | 0=Alert','#9060c0','#ccaadd');
        rw('','1=Restless | 2=Agitated | 3=Very Agitated | 4=Combative','#9060c0','#ccaadd');
        hr();
        rw('Deep sedation target:','RASS −2 to −3 — for respiratory distress, dyssynchrony, early ARDS','#cc9922','#eecc88');
        rw('NMBA sedation:','RASS −4 to −5 required — BIS 40–60 or TOF monitoring mandatory','#cc4444','#ffaa99');
        nt('NMBA without adequate sedation = patient awake and paralyzed — critical safety issue');
        hr();
        rw('Agitation (RASS +1 to +4):','Rule out PAINAD — treat pain first, then agitation (PAD: Pain-Agitation-Delirium)','#cc9922','#eecc88');
        nt('Dexmedetomidine: preferred for light-moderate sedation; cooperative, arousable, ↓ delirium');
    } else if(sel===1){
        rw('Critical Care Pain Observation Tool (CPOT) — For Non-Verbal/Ventilated Patients:','','#9060c0');
        hr();
        rw('Domains (0–2 each, max 8):','','#eedd88');
        rw('1. Facial expression:','0=Relaxed / 1=Tense / 2=Grimacing','#eedd88','#99bbdd');
        rw('2. Body movements:','0=Absent / 1=Protection / 2=Restlessness','#eedd88','#99bbdd');
        rw('3. Muscle tension:','0=Relaxed / 1=Tense+rigid / 2=Very tense+rigid (passive flex)','#eedd88','#99bbdd');
        rw('4. Vent compliance:','0=Tolerating / 1=Coughing+alarms / 2=Fighting vent','#eedd88','#99bbdd');
        nt('(Or vocalization if extubated: 0=Talking/no pain / 1=Sighing / 2=Crying/moaning)');
        hr();
        rw('Target:','CPOT <3 = acceptable pain control; ≥3 = treat with IV analgesia first','#3a9a5c','#99ddaa');
        nt('ANALGESIA-FIRST approach: address pain before giving sedation (PAD bundle)');
        nt('CPOT validated in ICU; NRS (0–10) preferred when patient can self-report');
        hr();
        rw('Reassess:','Q4h at minimum; after any procedure; after analgesic dosing (30 min post-IV)','#9060c0','#ccaadd');
    } else {
        rw('SAT/SBT Protocol — Daily Awakening + Breathing Trial:','','#9060c0');
        hr();
        rw('SAT Safety Screen (stop if ANY):','','#cc4444');
        nt('Active seizure / alcohol withdrawal / RASS −4 or −5 clinically required');
        nt('FiO2 >70% / PEEP >10 / vasopressor escalation in past 2h / new arrhythmia');
        hr();
        rw('SAT — Daily Awakening Trial:','Stop all continuous sedatives + analgesics; reassess Q1h','#eedd88','#99bbdd');
        nt('PASS: RASS ≥−2, patient interacts with RN, follows 1-step commands');
        nt('FAIL: RASS <−3, new agitation RASS >+1, SaO2 <88%, RR >35, hemodynamic compromise');
        hr();
        rw('SBT — Spontaneous Breathing Trial (after SAT pass):','','#eedd88');
        rw('Mode:','PSV 5–8 cmH2O + PEEP 5 OR T-piece for 30–120 minutes','#eedd88','#99bbdd');
        rw('PASS criteria:','RSBI <105 breaths/min/L, RR <35, SaO2 >90%, HR <140, no distress','#3a9a5c','#99ddaa');
        nt('RSBI = RR / Vt(L) — <105 predicts successful extubation; >105 predicts failure');
        rw('Post-extubation:','HFNC (ROX index ≥4.88 at 12h) or NIV to prevent re-intubation in high-risk','#eedd88','#99bbdd');
    }
    if(ctrl){
        ctrl.innerHTML='';
        var crow=document.createElement('div');crow.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        ['RASS Targets','CPOT Scale','SAT/SBT'].forEach(function(lb,i){
            var b=_mkB(lb,'#9060c0',sel===i,function(on){
                var p2={sel:on?i:0};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
            });crow.appendChild(b);
        });
        ctrl.appendChild(crow);
    }
}
"""

# ── Chart 5: Anticoagulation Monitoring ───────────────────────────────────────
RF['anticoag_monitoring'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['UFH aPTT Nomogram','Argatroban in HIT','Warfarin INR Targets'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#0a1020':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#1a2a3a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#cc9922':'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#080700';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+12;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#cc9922';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8px sans-serif';ctx.fillText(val,lm+185,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a2000';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('UFH Therapeutic aPTT Nomogram — Weight-Based Protocol:','','#cc9922');
        hr();
        rw('Loading dose:','80 units/kg IV bolus (VTE/PE) | 60 units/kg ACS | No bolus if HIT/HIT-like','#eedd88','#99bbdd');
        rw('Initial rate:','18 units/kg/hr (VTE/PE) | 12 units/kg/hr (ACS) — max 1,000 units/hr','#eedd88','#99bbdd');
        hr();
        rw('aPTT Zones:','','#cc9922');
        rw('<40 sec:','Rebolus 40 units/kg + ↑ rate 4 units/kg/hr — recheck aPTT in 6h','#cc4444','#ffaa99');
        rw('40–59 sec:','Rebolus 20 units/kg + ↑ rate 2 units/kg/hr — recheck in 6h','#cc8844','#ffcc88');
        rw('60–100 sec:','THERAPEUTIC — no change; recheck in 6h × 2, then q24h if stable','#3a9a5c','#99ddaa');
        rw('101–120 sec:','↓ rate 1 unit/kg/hr — recheck in 6h','#cc8844','#ffcc88');
        rw('>120 sec:','Hold 1h + ↓ rate 2 units/kg/hr — recheck 6h after restarting','#cc4444','#ffaa99');
        hr();
        nt('Target aPTT: 1.5–2.5× patient baseline (typically 60–100 sec in most labs)');
        nt('Anti-Xa level 0.3–0.7 IU/mL (VTE) or 0.3–0.5 IU/mL (ACS) — more reliable than aPTT');
    } else if(sel===1){
        rw('Argatroban in HIT — Direct Thrombin Inhibitor (DTI) for HIT:','','#cc9922');
        hr();
        rw('Indication:','HIT (4T score ≥4) with thrombosis OR suspected HIT requiring anticoagulation','#eedd88','#99bbdd');
        nt('STOP all heparin (including line flushes, LMWH, heparin-coated catheters) immediately');
        hr();
        rw('Standard dose:','2 mcg/kg/min continuous infusion (no loading dose)','#eedd88','#99bbdd');
        rw('Target aPTT:','1.5–3× patient baseline aPTT (typically 60–100 sec)','#3a9a5c','#99ddaa');
        nt('Check aPTT 2h after start and 2h after each dose adjustment; titrate to target');
        hr();
        rw('HEPATIC FAILURE dose:','Start 0.5 mcg/kg/min (25% of standard) → target aPTT 1.5–2× baseline','#cc4444','#ffaa99');
        nt('Argatroban cleared HEPATICALLY — ↓ dose in liver failure; ↑ effect without adjustment');
        hr();
        rw('Bridging to warfarin:','INR reflects BOTH argatroban + warfarin effects — use INR >4 to guide DC','#eedd88','#99bbdd');
        nt('Stop argatroban when INR >4 on combination; recheck INR 4–6h after stopping');
        nt('Bivalirudin alternative in hepatic failure: partially renally cleared; shorter t½ (25 min)');
    } else {
        rw('Warfarin INR Targets — Indication-Based Goals:','','#cc9922');
        hr();
        rw('AFib / VTE:','INR 2.0–3.0 — standard target for most indications','#eedd88','#99bbdd');
        rw('Mechanical mitral valve:','INR 2.5–3.5 — ↑ thrombotic risk vs aortic valve','#cc4444','#ffaa99');
        rw('Mechanical aortic valve:','INR 2.0–3.0 (low-risk bileaflet); may need 2.5–3.5 (older valves)','#eedd88','#99bbdd');
        rw('Antiphospholipid Ab:','INR 3.0–4.0 (high-risk triple-positive APS with arterial thrombosis)','#cc4444','#ffaa99');
        hr();
        rw('ICU reversal — Major bleeding:','','#cc4444');
        rw('INR 2–9, major bleed:','4F-PCC (Kcentra) 25–50 units/kg + Vit K 10 mg IV slow infusion','#cc4444','#ffaa99');
        nt('4F-PCC onset: 15 min (vs FFP 6–12h+); preferred in life-threatening bleeding');
        rw('INR 4–9, no bleed:','Hold warfarin + Vit K 2.5 mg PO — recheck INR in 24h','#cc9922','#eecc88');
        hr();
        rw('Bridging therapy:','LMWH bridge if high-risk valve/VTE; no bridge needed for AF (BRIDGE trial)','#eedd88','#99bbdd');
        nt('BRIDGE trial: no bridging for AF perioperatively — no ↑ thromboembolism, ↓ bleeding');
    }
    if(ctrl){
        ctrl.innerHTML='';
        var crow=document.createElement('div');crow.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        ['UFH Nomogram','Argatroban HIT','Warfarin INR'].forEach(function(lb,i){
            var b=_mkB(lb,'#cc9922',sel===i,function(on){
                var p2={sel:on?i:0};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
            });crow.appendChild(b);
        });
        ctrl.appendChild(crow);
    }
}
"""

# ── Cards ──────────────────────────────────────────────────────────────────────
_D = DID['monitoring_thresh']
CARDS = [
    # tdm_targets — L1 recognition / L2 mechanism / L3 clinical application
    ('On the TDM targets chart, vancomycin monitoring now targets _______ rather than trough alone, using _______ to estimate this parameter.',
     'AUC/MIC 400–600 mg·h/L → Bayesian PK modeling using two serum levels — replaces trough-only approach per 2020 ASHP/SIDP/IDSA guideline',
     'tier-review', _NM, _D, 'tdm_targets', '{}', 'chart-l1'),
    ('The TDM chart shows digoxin toxicity risk increases when levels exceed _______, with toxicity dramatically worsened by _______.',
     '>2 ng/mL (therapeutic 0.5–2.0; HF target 0.5–0.9 ng/mL) → hypokalemia and hypomagnesemia ↑ digoxin-receptor binding at ANY level — always correct electrolytes',
     'tier-high', _NM, _D, 'tdm_targets', '{}', 'chart-l2'),
    ('On the TDM targets chart, phenytoin requires _______ monitoring when albumin <2 g/dL, using the _______ correction formula.',
     'free phenytoin level (therapeutic 1–2 mg/L, not total) → Winter-Tozer: adjusted total = measured / (0.2 × albumin + 0.1) — total level is falsely low in hypoalbuminemia',
     'tier-critical', _NM, _D, 'tdm_targets', '{}', 'chart-l3'),

    # nephrotox_monitor — L1 recognition / L2 mechanism / L3 clinical application
    ('The nephrotoxicity monitoring chart shows aminoglycoside AKI is triggered when SCr rises _______, with the key prevention strategy being _______.',
     'SCr ↑ 0.3 mg/dL over 48h or >1.5× baseline → extended-interval dosing (EID) 5–7 mg/kg q24h: maximizes Cmax/MIC and minimizes nephrotoxicity vs multiple daily dosing',
     'tier-review', _NM, _D, 'nephrotox_monitor', '{}', 'chart-l1'),
    ('On the nephrotoxicity chart, contrast-associated nephropathy (CAN) prevention requires _______ before the procedure and _______ if used.',
     'IV hydration (1 mL/kg/h NS 6–12h pre+post or NaHCO3) → N-acetylcysteine (NAC) 600–1200 mg PO BID × 2 days — highest risk: eGFR <30, diabetes, dehydration, CHF',
     'tier-high', _NM, _D, 'nephrotox_monitor', '{}', 'chart-l2'),
    ('The nephrotox monitoring chart shows calcineurin inhibitors cause nephrotoxicity via _______, and are worsened by _______ drug interactions.',
     'afferent arteriole vasoconstriction (↑ TXA2/endothelin → ↓ GFR) → CYP3A4 inhibitors (azoles, diltiazem, verapamil) drastically ↑ tacrolimus/cyclosporine levels → toxicity',
     'tier-critical', _NM, _D, 'nephrotox_monitor', '{}', 'chart-l3'),

    # pressor_endpoints — L1 recognition / L2 mechanism / L3 clinical application
    ('The MAP targets chart shows septic shock goal is MAP _______, while TBI with elevated ICP requires MAP _______ to maintain adequate cerebral perfusion pressure.',
     '≥65 mmHg (SEPSISPAM: no mortality benefit from MAP 85 vs 65; ↑ AFib at higher target) → MAP ≥80 mmHg in TBI (CPP = MAP − ICP; target CPP 60–70 mmHg)',
     'tier-review', _NM, _D, 'pressor_endpoints', '{}', 'chart-l1'),
    ('On the cardiac output endpoints chart, cardiogenic shock is defined as CI _______, and treatment targets CI _______ with _______ as preferred inotrope when on beta-blockers.',
     '<2.2 L/min/m² (with SBP <90 + congestion + end-organ hypoperfusion) → target CI >2.2 L/min/m² → milrinone preferred (PDE3i bypasses β-receptor blockade)',
     'tier-high', _NM, _D, 'pressor_endpoints', '{}', 'chart-l2'),
    ('The shock reversal chart identifies lactate clearance of _______ at 2 hours and ScvO2 _______ as resuscitation adequacy targets.',
     '≥10% decline at 2h from baseline (or absolute lactate <2 mmol/L) → ScvO2 ≥70% indicates adequate DO2/VO2 balance and tissue oxygen delivery',
     'tier-critical', _NM, _D, 'pressor_endpoints', '{}', 'chart-l3'),

    # sedation_endpoints — L1 recognition / L2 mechanism / L3 clinical application
    ('The RASS targets chart shows general ICU ventilated patients target RASS _______, while patients on NMBAs require RASS _______ with mandatory _______ monitoring.',
     'RASS 0 to −1 (light sedation — awake/arousable, PADIS 2018 guideline) → RASS −4 to −5 for NMBAs → BIS 40–60 or TOF monitoring mandatory (patient could be awake without movement)',
     'tier-review', _NM, _D, 'sedation_endpoints', '{}', 'chart-l1'),
    ('On the CPOT chart, mechanically ventilated patients scoring _______ require analgesic intervention; the four assessment domains are _______.',
     'CPOT ≥3 (0–2 = acceptable; ≥3 = significant pain requiring treatment) → four domains: facial expression / body movements / muscle tension / ventilator compliance',
     'tier-high', _NM, _D, 'sedation_endpoints', '{}', 'chart-l2'),
    ('The SAT/SBT chart shows a spontaneous breathing trial (SBT) passes when RSBI is _______, where RSBI is calculated as _______.',
     'RSBI <105 breaths/min/L (predicts successful extubation) → RSBI = respiratory rate ÷ tidal volume in liters (RR/Vt); >105 = high extubation failure risk',
     'tier-critical', _NM, _D, 'sedation_endpoints', '{}', 'chart-l3'),

    # anticoag_monitoring — L1 recognition / L2 mechanism / L3 clinical application
    ('The UFH nomogram chart shows an aPTT of 45 seconds requires _______ AND _______ before rechecking in 6 hours.',
     'rebolus 20 units/kg IV → rate increase 2 units/kg/hr — aPTT target 60–100 sec (1.5–2.5× baseline); anti-Xa 0.3–0.7 IU/mL is more reliable than aPTT in some patients',
     'tier-review', _NM, _D, 'anticoag_monitoring', '{}', 'chart-l1'),
    ('On the argatroban monitoring chart, hepatic failure patients require a starting dose of _______ with aPTT target _______, lower than the standard goal.',
     '0.5 mcg/kg/min (25% of standard 2 mcg/kg/min) → aPTT target 1.5–2× baseline (vs 1.5–3× standard) — argatroban is hepatically cleared; ↑ drug effect in liver failure',
     'tier-high', _NM, _D, 'anticoag_monitoring', '{}', 'chart-l2'),
    ('The warfarin INR targets chart shows mechanical mitral valve requires INR _______, and major bleeding with warfarin is reversed using _______ as first-line agent.',
     'INR 2.5–3.5 (higher thrombotic risk vs aortic valve) → 4F-PCC (Kcentra) 25–50 units/kg + Vit K 10 mg IV slow infusion — onset 15 min vs 6–12h+ for FFP',
     'tier-critical', _NM, _D, 'anticoag_monitoring', '{}', 'chart-l3'),
]

# ── Main ───────────────────────────────────────────────────────────────────────
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
        issues = validator.validate(f'c{CHUNK_NUM}_{i}', front, back, badge, tier)
        warns  = validator.results[-1].get('warnings', [])
        ok     = not issues
        print(f"  {'OK' if ok else 'XX'} [{ctype}·{ltag}]{' W8' if warns else ''}  {front[:65]}")
        if not ok:
            for iss in issues: print(f"      x {iss}")
    print(validator.report())
    print()
    for i, card in enumerate(CARDS):
        front, back, tier, badge, did, ctype, pj, ltag = card
        issues = validator.validate(f'c{CHUNK_NUM}_{i}_check', front, back, badge)
        if issues: print(f"  SKIP: {front[:55]}"); continue
        chart_idx = CHART_ORDER.index(ctype) if ctype in CHART_ORDER else i
        mid_int   = MID_BASE + chart_idx
        mkey      = str(mid_int)
        if mkey not in models:
            qfmt, afmt = make_chart_template(ctype, pj, RF[ctype], SHARED_JS, CHART_CSS)
            register_chart_model(models, mid_int, ctype, did, qfmt, afmt, CHART_CSS)
        guid = make_guid(front, back)
        if guid in existing_guids: print(f"  SKIP dup: {front[:50]}"); continue
        existing_guids.add(guid)
        flds = '\x1f'.join([safe_html(front), safe_html(back), tier, badge])
        sfld = re.sub(r'<[^>]+>', '', front)[:100]
        nid  = nid_base + i * 3
        insert_card(db, nid, nid+1, guid, mkey, flds, sfld, did, f' ccrn-pccn-v6 chunk-{CHUNK_NUM} {ltag} ', now)
        added += 1
        print(f"  + [{ctype}·{ltag}]  {front[:65]}")
    save_deck(db, models, WORK_DIR, OUT_PATH)
    db2 = sqlite3.connect(os.path.join(WORK_DIR, 'collection.anki2'))
    total = db2.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    db2.close()
    print(f"\n{'='*65}\n  Chunk {CHUNK_NUM}: {added} cards added | Total deck: {total} cards\n{'='*65}")

if __name__ == '__main__':
    main()
