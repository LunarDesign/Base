#!/usr/bin/env python3
"""chunk49_charts.py — Ph8 Reference: Lab Values (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_48.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_49.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c49')
CHUNK_NUM   = 49
MID_BASE    = 1_800_005_090
CHART_ORDER = ['critical_labs', 'electrolyte_abnormalities', 'renal_labs',
               'coagulation_labs', 'cardiac_markers']

_NM = 'Ph8 · \U0001f7e1 T3 · Reference — Lab Values'

RF = {}

# ── Chart 1: Critical Lab Value Reference ─────────────────────────────────────
RF['critical_labs'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var labs=[
        {n:'Sodium (Na⁺)',    lo:'< 120',nr:'135–145', hi2:'> 160',act:'120–130: restrict H₂O/3% NaCl if sx\n<120 or acute: 3% NaCl at 1–2 mL/kg/h\nMax correction: 10–12 mEq/L per 24h',cl:'#4488cc'},
        {n:'Potassium (K⁺)',  lo:'< 2.5', nr:'3.5–5.0',hi2:'> 6.5', act:'<2.5: IV KCl (max 10–20 mEq/h central)\n>6.0: Ca gluconate + insulin/dextrose\n>6.5/EKG changes: emergent dialysis',cl:'#cc4444'},
        {n:'Glucose',         lo:'< 50',  nr:'70–110', hi2:'> 500', act:'<70: D50W 25g (50 mL) IV push\n>180 ICU: insulin infusion (titrate)\n>500: hyperosmolar coma risk → IVF',cl:'#cc8844'},
        {n:'Ionized Calcium', lo:'< 0.9', nr:'1.15–1.35',hi2:'> 1.5',act:'<0.9: CaGluconate 1–2g IV over 10–20m\nChvostek/Trousseau signs → treat\n>1.5: IVF, furosemide, bisphosphonate',cl:'#3a9a5c'},
        {n:'Magnesium (Mg²⁺)',lo:'< 1.0', nr:'1.8–2.4', hi2:'> 9.0', act:'<1.0: MgSO₄ 2–4g IV over 30–60 min\nRefractory hypokalemia: replete Mg first\n>9.0: Ca gluconate + HD if severe',cl:'#9060c0'},
        {n:'pH (arterial)',   lo:'< 7.20',nr:'7.35–7.45',hi2:'> 7.60',act:'<7.20: identify cause; bicarb if AKI/pH<7.1\n>7.60: identify cause (alkalosis drivers)\nSevere: respiratory correction fastest',cl:'#cc6633'},
        {n:'Lactate',         lo:'—',     nr:'< 2.0',   hi2:'> 4.0', act:'2–4: investigate cause, resuscitate\n>4 in sepsis: 30 mL/kg IVF + vasopressor\nTrend: goal clearance >10% per 2h',cl:'#e06060'},
        {n:'Platelet Count',  lo:'< 20K', nr:'150–400K',hi2:'—',      act:'<20K (or <50K with bleeding): transfuse\n<50K + planned surgery: transfuse\nHIT suspected: STOP heparin immediately',cl:'#5599cc'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/labs.length);
    var xs=[4,75,150,225,300,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Lab','Critical Low','Normal Range','Critical High','Immediate Nursing Action'];
    ctx.font='bold 7.5px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    labs.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=d.cl+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=d.cl;ctx.font='bold 7.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(d.n,xs[0]+2,ry+rh/2+3);
        ctx.fillStyle='#6699ff';ctx.font='bold 8px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.lo,(xs[1]+xs[2])/2,ry+rh/2+3);
        ctx.fillStyle='#66cc88';ctx.font='7.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.nr,(xs[2]+xs[3])/2,ry+rh/2+3);
        ctx.fillStyle='#ff7766';ctx.font='bold 8px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.hi2,(xs[3]+xs[4])/2,ry+rh/2+3);
        ctx.fillStyle='#aabbaa';ctx.font='7px sans-serif';ctx.textAlign='left';
        d.act.split('\n').forEach(function(l,li){ctx.fillText(l,xs[4]+3,ry+rh/2-8+li*8);});
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
        var lbs=['Na','K','Glucose','iCa','Mg','pH','Lactate','Platelets'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,labs[idx].cl,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: Electrolyte Abnormalities ───────────────────────────────────────
RF['electrolyte_abnormalities'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Sodium Disorders','Potassium Disorders','Calcium & Magnesium'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a2a3a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a3a4a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#4488cc':'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0a1a';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+14;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#88bbee';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+195,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('HYPONATREMIA (Na < 135):','','#6699ff');
        rw('Symptomatic / severe (< 120):','3% NaCl at 1–2 mL/kg/h','#aab','#eedd88');
        nt('Target: raise Na by 1–2 mEq/L/h until symptoms resolve (seizure/altered)');
        nt('Max correction: 10–12 mEq/L per 24h → osmotic demyelination risk if faster');
        rw('Mild (130–134):','Treat underlying cause (restrict H₂O if SIADH)','#aab','#bbb');
        nt('SIADH: urine Na > 20, urine Osm > serum Osm, euvolemic');
        hr();
        rw('HYPERNATREMIA (Na > 145):','','#ff7766');
        rw('Cause:','Free water deficit; assess volume status first','#aab','#bbb');
        nt('Free water deficit (L) = TBW × (Na/140 − 1); TBW = 0.6 × weight (kg)');
        rw('Correction rate:','Max 10–12 mEq/L per 24h (cerebral edema if too fast)','#aab','#eedd88');
        nt('Replace with D5W (or enteral free water) — NOT NS (worsens hypernatremia)');
        nt('Monitor Na q2–4h during active correction');
        hr();
        nt('★ Central DI (ADH-deficient): urine Osm < serum Osm; treat with DDAVP');
        nt('★ Nephrogenic DI (ADH-resistant): urine Osm variably low; treat underlying cause');
    } else if(sel===1){
        rw('HYPOKALEMIA (K < 3.5):','','#6699ff');
        rw('Moderate (2.5–3.5):','KCl 20–40 mEq oral or slow IV','#aab','#eedd88');
        rw('Severe (< 2.5 or EKG Δ):','KCl 10–20 mEq/h IV via central line','#aab','#ffaa88');
        nt('EKG changes: U waves (early), flattened T waves, ST depression, widened QRS');
        nt('Replace Mg first if < 1.8 — hypoMg causes refractory hypoK (renal K wasting)');
        nt('Risk: arrhythmia, ↑ digoxin toxicity, respiratory muscle weakness');
        hr();
        rw('HYPERKALEMIA (K > 5.5):','','#ff7766');
        rw('K 5.5–6.5, no EKG Δ:','Kayexalate 15–30g PO/PR; restrict K intake','#aab','#eedd88');
        rw('K > 6.0 or peaked T waves:','Insulin 10u + D50W; sodium bicarb if acidotic','#aab','#ffaa88');
        rw('K > 6.5 or wide QRS/sine:','CaGluconate 1g IV (membrane stabilizer) STAT','#aab','#ff6644');
        nt('EKG progression: peaked T → PR prolongation → wide QRS → sine wave → VF');
        nt('Ca gluconate: stabilizes myocardium (onset 1–3 min); does NOT lower K level');
        nt('Definitive: hemodialysis (fastest K removal) or Patiromer/SPS (hours-days)');
    } else {
        rw('HYPOCALCEMIA (iCa < 1.15 mmol/L):','','#6699ff');
        rw('Symptoms:','Tetany, Trousseau, Chvostek, QTc prolongation, seizures','#aab','#ffaa88');
        rw('Acute Rx:','CaGluconate 1–2g IV over 10–20 min (repeat prn)','#aab','#eedd88');
        nt('Ionized Ca preferred over total Ca (total affected by albumin)');
        nt('Causes in ICU: pancreatitis, sepsis, post-parathyroidectomy, CRRT, massive transfusion');
        nt('Hyperphosphatemia precipitates Ca → worsens hypocalcemia');
        hr();
        rw('HYPERCALCEMIA (iCa > 1.35 mmol/L):','','#ff7766');
        rw('Mild–Moderate:','IVF (NS 200–300 mL/h) + furosemide (after volume replete)','#aab','#eedd88');
        nt('Causes: malignancy (PTHrP), hyperparathyroidism, granulomatous disease, Vit D tox');
        hr();
        rw('HYPOMAGNESEMIA (Mg < 1.8 mg/dL):','','#6699ff');
        rw('Rx:','MgSO₄ 2–4g IV over 30–60 min; repeat daily if ongoing losses','#aab','#eedd88');
        nt('Critical: must replete Mg before hypokalemia will correct (Mg needed for renal K retention)');
        nt('Causes: loop/thiazide diuretics, diarrhea, alcoholism, PPI use (prolonged)');
        nt('EKG: prolonged QTc, torsades risk when Mg < 1.0 + hypoK coexist');
    }
    if(ctrl){
        ctrl.innerHTML='';
        var crow=document.createElement('div');crow.style.cssText='display:flex;gap:6px;margin-top:6px;';
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,'#4488cc',sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });crow.appendChild(b);})(i);});
        ctrl.appendChild(crow);
    }
}
"""

# ── Chart 3: Renal Labs — AKI Staging & Differentiation ──────────────────────
RF['renal_labs'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['KDIGO AKI Staging','Pre/Intrinsic/Post-Renal','CRRT Indications'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a2a3a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a3a4a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#4488cc':'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0a1a';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+13;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#88bbee';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+175,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('KDIGO AKI — 3-Stage Criteria (either Cr OR urine output):','','#eedd88');
        hr();
        rw('Stage 1:','Cr ×1.5–1.9 baseline OR +0.3 mg/dL in 48h','#cc6666','#ffaa88');
        nt('Urine output: < 0.5 mL/kg/h for 6–12 hours');
        nt('Action: identify/remove nephrotoxins; optimize perfusion; daily labs');
        hr();
        rw('Stage 2:','Cr ×2.0–2.9 baseline','#cc8844','#ffcc88');
        nt('Urine output: < 0.5 mL/kg/h for ≥ 12 hours');
        nt('Action: nephrology consult; consider CRRT if not improving; avoid contrast');
        hr();
        rw('Stage 3:','Cr ×3.0+ OR Cr ≥4.0 mg/dL OR RRT initiated','#cc4444','#ff6644');
        nt('Urine output: < 0.3 mL/kg/h for ≥ 24h OR anuria ≥ 12h');
        nt('Action: renal replacement therapy (CRRT/HD); restrict volume; K+/bicarb management');
        hr();
        nt('★ Recovery: return toward baseline Cr within 7 days = AKI episode (not CKD)');
        nt('★ AKI on CKD: baseline Cr from 3-month prior labs (if available)');
    } else if(sel===1){
        rw('PRE-RENAL (↓ perfusion):','','#4488cc');
        rw('BUN:Cr ratio:','> 20:1 (avid urea reabsorption)','#aab','#eedd88');
        rw('FeNa:','< 1% (kidneys avidly retain Na)','#aab','#eedd88');
        rw('Urine Na:','< 20 mEq/L (concentrating urine)','#aab','#eedd88');
        rw('Urine Osm:','> 500 mOsm/kg','#aab','#eedd88');
        nt('FeNa = (UNa × PCr) / (PNa × UCr) × 100%');
        nt('FeNa invalid if on diuretics → use FeUrea (<35% = pre-renal) instead');
        hr();
        rw('INTRINSIC RENAL (tubular damage / ATN):','','#cc4444');
        rw('FeNa:','> 2% (damaged tubules cannot conserve Na)','#aab','#ffaa88');
        rw('Urine Na:','> 40 mEq/L; muddy brown casts on UA','#aab','#ffaa88');
        rw('BUN:Cr:','10–15:1 (parallel rise, no preferential urea retention)','#aab','#bbb');
        hr();
        rw('POST-RENAL (obstruction):','','#3a9a5c');
        nt('Bilateral obstruction (or unilateral in single-functioning kidney) → AKI');
        nt('Bladder scan: residual > 300 mL → Foley catheter (fastest intervention)');
        nt('Renal US: hydronephrosis; CT for stone/mass; urology consult');
    } else {
        rw('CRRT INDICATIONS (AEIOU mnemonic):','','#eedd88');
        hr();
        rw('A — Acidosis:','pH < 7.15–7.20 despite treatment','#cc4444','#ffaa88');
        rw('E — Electrolytes:','K > 6.5 or refractory hyperkalemia','#cc4444','#ffaa88');
        rw('I — Ingestion:','Dialyzable toxins (Li, metformin, salicylate, EtOH)','#cc8844','#ffcc88');
        rw('O — Overload:','Refractory fluid overload / pulmonary edema','#4488cc','#88ccff');
        rw('U — Uremia:','BUN > 100 or uremic symptoms (pericarditis, encephalopathy)','#9060c0','#cc99ff');
        hr();
        rw('CRRT vs Intermittent HD:','','#88bbee');
        nt('CRRT: hemodynamically unstable patients (continuous gentle fluid/solute removal)');
        nt('IHD: hemodynamically stable; faster K removal; 3–4h sessions');
        nt('CRRT rate: typically 20–25 mL/kg/h effluent dose (KDIGO recommendation)');
        hr();
        nt('★ RENAL trial: no mortality benefit of higher vs standard dose CRRT (25 vs 40 mL/kg/h)');
        nt('★ ATN trial: no benefit of early vs late RRT initiation in non-urgent AKI');
    }
    if(ctrl){
        ctrl.innerHTML='';
        var crow=document.createElement('div');crow.style.cssText='display:flex;gap:6px;margin-top:6px;';
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,'#4488cc',sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });crow.appendChild(b);})(i);});
        ctrl.appendChild(crow);
    }
}
"""

# ── Chart 4: Coagulation Labs ─────────────────────────────────────────────────
RF['coagulation_labs'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Coagulation Panel','DIC Diagnosis (ISTH)','Anticoag Monitoring'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#2a1a1a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#3a2a2a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?_RE:'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0808';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+13;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#88bbee';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+195,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a1a1a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('PT / INR:','Normal PT 11–13.5s; INR 0.8–1.2','#cc4444','#eedd88');
        nt('Extrinsic pathway: Factor VII → X → V → II → fibrinogen');
        nt('Prolonged by: warfarin, liver disease (VII shortest t½), Vit K deficiency');
        rw('aPTT:','Normal 25–35 seconds','#cc4444','#eedd88');
        nt('Intrinsic pathway: XII → XI → IX → VIII → X → V → II → fibrinogen');
        nt('Prolonged by: UFH, heparin contamination, factor deficiency (VIII=hemophilia A), lupus anticoag');
        hr();
        rw('Fibrinogen:','Normal 200–400 mg/dL','#cc8844','#eedd88');
        nt('<100: severe coagulopathy; replace with cryoprecipitate (10 units → ↑ fibrinogen ~50–100)');
        rw('D-dimer:','Normal < 0.5 mcg/mL (FEU)','#cc8844','#eedd88');
        nt('Very sensitive, not specific: elevated in PE, DVT, sepsis, pregnancy, trauma, post-op');
        nt('Negative D-dimer: rules out PE/DVT in LOW pretest probability (Wells ≤ 4)');
        hr();
        rw('Platelet Count:','Normal 150–400K','#9060c0','#eedd88');
        nt('< 100K: thrombocytopenia; investigate (HIT, DIC, ITP, drug-induced)');
        nt('< 50K: avoid invasive procedures without transfusion (goal > 50K for surgery)');
        nt('< 20K: spontaneous bleeding risk; transfuse prophylactically');
    } else if(sel===1){
        rw('ISTH Overt DIC Score:','≥ 5 = Overt DIC','#cc4444','#ff6644');
        hr();
        rw('Platelet count:','','#cc8844');
        nt('> 100K = 0 pts  |  50–100K = 1 pt  |  < 50K = 2 pts');
        rw('D-dimer / fibrin degradation:','','#cc8844');
        nt('No increase = 0  |  Moderate = 2  |  Strong increase = 3 pts');
        rw('PT prolongation:','','#cc8844');
        nt('< 3s = 0 pts  |  3–6s = 1 pt  |  > 6s = 2 pts');
        rw('Fibrinogen:','','#cc8844');
        nt('≥ 1 g/L = 0 pts  |  < 1 g/L = 1 pt');
        hr();
        rw('DIC Treatment:','Treat underlying cause FIRST','#eedd88');
        nt('Bleeding DIC: FFP (all factors), cryoprecipitate (fibrinogen), pRBC, platelets');
        nt('Thrombotic DIC: low-dose UFH (controversial); treat sepsis/malignancy aggressively');
        nt('Target: fibrinogen > 100–150, platelets > 50K if bleeding, PT < 1.5× normal');
        hr();
        nt('★ DIC causes: sepsis #1, malignancy (APL classic), trauma, obstetric emergencies');
    } else {
        rw('UFH Monitoring:','','#4488cc');
        rw('Therapeutic aPTT goal:','1.5–2.5× control (≈ 60–100 seconds)','#aab','#eedd88');
        nt('Weight-based protocol: bolus 80 u/kg, then 18 u/kg/h; adjust per nomogram');
        nt('Check aPTT 6h after initiation or dose change; recheck until therapeutic × 2');
        rw('Anti-Xa for UFH:','0.3–0.7 units/mL (heparin monitoring; less lab interference)','#aab','#eedd88');
        hr();
        rw('LMWH Monitoring:','','#3a9a5c');
        rw('Therapeutic anti-Xa:','0.5–1.0 units/mL (peak, 4h post-dose)','#aab','#eedd88');
        nt('Prophylactic anti-Xa goal: 0.2–0.5 units/mL');
        nt('Monitor anti-Xa in: renal failure (CrCl < 30), obesity (> 120 kg), pregnancy');
        hr();
        rw('Warfarin (INR goals):','','#cc8844');
        rw('Standard VTE / AF:','INR 2.0–3.0','#aab','#eedd88');
        rw('Mechanical heart valves:','INR 2.5–3.5 (mitral); 2.0–3.0 (aortic)','#aab','#eedd88');
        hr();
        rw('Argatroban (HIT):','aPTT 1.5–3.0× baseline (HIT: do NOT use heparin)','#aab','#eedd88');
        nt('DTIs (argatroban, bivalirudin): monitored via aPTT; no specific antidote');
        nt('Reversal: idarucizumab → dabigatran; andexanet alfa → Xa inhibitors (rivaroxaban, apixaban)');
    }
    if(ctrl){
        ctrl.innerHTML='';
        var crow=document.createElement('div');crow.style.cssText='display:flex;gap:6px;margin-top:6px;';
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,_RE,sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });crow.appendChild(b);})(i);});
        ctrl.appendChild(crow);
    }
}
"""

# ── Chart 5: Cardiac & Sepsis Markers ────────────────────────────────────────
RF['cardiac_markers'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var markers=[
        {n:'High-Sensitivity\nTroponin (hsTnI/T)',rise:'1–3h',peak:'12–24h',
         cut:'99th %ile cutoff\n(lab-specific)',
         use:'MI diagnosis (NSTEMI/STEMI)\nNon-cardiac elevation: PE, myocarditis,\nsepsis, ESRD, demand ischemia',c:'#cc4444'},
        {n:'CK-MB',           rise:'3–6h', peak:'12–24h',
         cut:'> 5 ng/mL\n(or CK-MB index > 5%)',
         use:'Reinfarction detection post-MI\n(troponin stays elevated; CK-MB\nreturns to baseline → re-rises)',c:'#cc8844'},
        {n:'BNP / NT-proBNP', rise:'Hours', peak:'Hours–days',
         cut:'BNP > 100 pg/mL\nNT-proBNP > 300 pg/mL',
         use:'Heart failure diagnosis/monitoring\nBNP > 400: likely decompensated HF\nDecreasing trend = responding to Rx',c:'#4488cc'},
        {n:'Procalcitonin\n(PCT)',rise:'4–6h', peak:'24–48h',
         cut:'> 0.5 ng/mL: bacterial\n> 2.0: likely sepsis\n> 10: severe sepsis/shock',
         use:'Bacterial infection vs viral/sterile\nDe-escalation: stop abx if < 0.5\nor > 80% drop from peak (PROACT)',c:'#3a9a5c'},
        {n:'Lactate\n(serum)',  rise:'Acute',peak:'Immediate',
         cut:'Normal: < 2.0 mmol/L\nElevated: 2–4 mmol/L\nCritical: > 4.0 mmol/L',
         use:'Tissue hypoperfusion marker\nSepsis resuscitation goal: < 2\nClearance > 10% per 2h = target',c:'#e06060'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/markers.length);
    var xs=[4,110,165,220,340,500,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Marker','Rise','Peak','Critical Cutoff','ICU Clinical Use'];
    ctx.font='bold 8px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    // Only 5 columns rendered (skip xs[5] header), adjust:
    var hdrs2=['Marker','Rise','Peak','Critical Cutoff','ICU Clinical Use'];
    var hxs=[4,110,165,220,340,616];
    hdrs2.forEach(function(h,i){ctx.fillText(h,(hxs[i]+hxs[i+1])/2,hdrH-4);});
    markers.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=d.c+'33';ctx.fillRect(hxs[0],ry,hxs[1]-hxs[0],rh);
        ctx.fillStyle=d.c;ctx.font='bold 7.5px sans-serif';ctx.textAlign='left';
        d.n.split('\n').forEach(function(l,li){ctx.fillText(l,hxs[0]+3,ry+rh/2-5+li*10);});
        ctx.fillStyle='#eedd88';ctx.font='8px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.rise,(hxs[1]+hxs[2])/2,ry+rh/2+3);
        ctx.fillStyle='#aabb88';ctx.font='8px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.peak,(hxs[2]+hxs[3])/2,ry+rh/2+3);
        ctx.fillStyle='#ffcc88';ctx.font='7.5px sans-serif';ctx.textAlign='left';
        d.cut.split('\n').forEach(function(l,li){ctx.fillText(l,hxs[3]+3,ry+rh/2-8+li*9);});
        ctx.fillStyle='#99aabb';ctx.font='7px sans-serif';ctx.textAlign='left';
        d.use.split('\n').forEach(function(l,li){ctx.fillText(l,hxs[4]+3,ry+rh/2-9+li*9);});
        ctx.globalAlpha=1;
        ctx.strokeStyle='#222';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(0,ry+rh);ctx.lineTo(W,ry+rh);ctx.stroke();
    });
    [hxs[1],hxs[2],hxs[3],hxs[4]].forEach(function(x){
        ctx.strokeStyle='#222';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(x,hdrH);ctx.lineTo(x,H);ctx.stroke();
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        var lbs=['hsTroponin','CK-MB','BNP','Procalcitonin','Lactate'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,markers[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Cards ─────────────────────────────────────────────────────────────────────
CARDS = [
    # ═══ critical_labs ════════════════════════════════════════════════════════
    (
        "On the critical labs chart, the critical HIGH potassium value requiring "
        "immediate cardiac intervention is > _______ mEq/L. "
        "The first medication given for K+ > 6.5 with EKG changes is _______, "
        "which works by _______.",

        "Critical high K⁺: > 6.5 mEq/L (or > 6.0 with EKG changes)\n"
        "| First medication: calcium gluconate 1g IV over 5–10 min\n"
        "| Mechanism: membrane stabilization — raises the threshold potential of myocardial cells → "
        "reduces risk of VF. Does NOT lower K⁺ level.\n"
        "| Onset: 1–3 min | Duration: 30–60 min\n"
        "| Then: insulin 10u + D50W (moves K into cells) + kayexalate/patiromer (GI removal)\n"
        "→ CCRN KEY: EKG progression in hyperkalemia (memorize sequence): "
        "peaked T waves (earliest) → prolonged PR → widened QRS → loss of P waves → "
        "sine wave pattern → ventricular fibrillation → asystole. "
        "Calcium gluconate addresses the CARDIAC MEMBRANE threat; it is the emergency drug.\n"
        "→ MASTERY NOTE: Do NOT confuse calcium gluconate (preferred, peripheral OK) with "
        "calcium chloride (more elemental Ca, must be central — causes tissue necrosis if extravasated). "
        "Calcium chloride contains 3× more elemental Ca than gluconate: use in cardiac arrest only.",

        'tier-review',
        _NM,
        DID['lab_values'],
        'critical_labs',
        '{"hi":1}',
        'chart-l1'
    ),
    (
        "The critical labs chart shows the maximum safe sodium correction rate is "
        "_______ mEq/L per 24 hours. Exceeding this rate risks _______. "
        "Critical hyponatremia (Na < _______ mEq/L) with seizures is treated with _______.",

        "Maximum correction rate: 10–12 mEq/L per 24 hours (some protocols allow up to 12–15 in severe)\n"
        "| Too-rapid correction risk: osmotic demyelination syndrome (ODS) = central pontine myelinolysis\n"
        "| ODS: irreversible demyelination of pons → quadriplegia, locked-in syndrome, death\n"
        "| Critical hyponatremia < 120 mEq/L with symptoms (seizure, coma): 3% NaCl\n"
        "| Acute severe: 3% NaCl 100–150 mL bolus; repeat × 1–2 until seizures stop\n"
        "→ CCRN KEY: Formula to estimate Na rise: Δ[Na] = (infusate Na − serum Na) / (TBW + 1). "
        "For 3% NaCl (513 mEq/L) in 70 kg male (TBW = 42L): "
        "Δ[Na] per liter = (513 − 115) / (42 + 1) ≈ 9.3 mEq/L. "
        "At 1 mL/kg/h = 70 mL/h: check Na q2h, adjust to stay within 10–12 mEq/24h.\n"
        "→ MASTERY NOTE: Hyponatremia causes: SIADH (most common in ICU) vs hypovolemic (GI losses, diuretics) "
        "vs hypervolemic (CHF, cirrhosis, nephrotic). SIADH: euvolemic, urine Na > 20, "
        "urine Osm > serum Osm. Treat SIADH with fluid restriction ± tolvaptan.",

        'tier-high',
        _NM,
        DID['lab_values'],
        'critical_labs',
        '{"hi":0}',
        'chart-l2'
    ),
    (
        "On the critical labs chart, a lactate > _______ mmol/L in a septic patient "
        "triggers the Surviving Sepsis Campaign bundle. "
        "The lactate clearance goal at 2 hours is > _______ %, "
        "and the target for initial resuscitation is lactate < _______ mmol/L.",

        "Lactate > 4.0 mmol/L → SSC 1-hour bundle: 30 mL/kg IVF + vasopressors + cultures + abx\n"
        "| Lactate 2–4 mmol/L → also requires resuscitation bundle (sepsis, not just septic shock)\n"
        "| Lactate clearance goal: > 10% reduction per 2 hours (serial measurements)\n"
        "| Target: lactate < 2.0 mmol/L (normalization)\n"
        "→ CCRN KEY: Lactate clearance-guided resuscitation vs ScvO₂-guided: "
        "LACTATES trial showed lactate-guided resuscitation was equivalent to ScvO₂-guided "
        "and more practical (no central line required for lactate). "
        "Serial lactate every 1–2h during resuscitation is standard of care.\n"
        "→ MASTERY NOTE: Elevated lactate with normal perfusion (Type B):\n"
        "• Metformin-associated lactic acidosis: AKI + metformin use → accumulation\n"
        "• Thiamine deficiency: inhibits pyruvate dehydrogenase → pyruvate → lactate\n"
        "• Propofol infusion syndrome: lipid + mitochondrial dysfunction → lactate, lipemia, RF\n"
        "In Type B: treating the underlying cause (not just volume) is the key intervention.",

        'tier-critical',
        _NM,
        DID['lab_values'],
        'critical_labs',
        '{"hi":6}',
        'chart-l3'
    ),

    # ═══ electrolyte_abnormalities ════════════════════════════════════════════
    (
        "The electrolyte chart shows hyponatremia with seizures requires correction "
        "with _______ at _______ mL/kg/h. "
        "The maximum safe correction is _______ mEq/L per 24 hours to prevent "
        "_______.",

        "Acute symptomatic hyponatremia: 3% NaCl at 1–2 mL/kg/h until symptoms resolve\n"
        "| Maximum correction: 10–12 mEq/L per 24 hours\n"
        "| Prevent: osmotic demyelination syndrome (ODS = central pontine myelinolysis)\n"
        "| After seizures stop: slow 3% NaCl to maintain < 10–12 mEq/L/24h total rise\n"
        "→ CCRN KEY: SIADH management (euvolemic hyponatremia, urine Na > 20):\n"
        "• Fluid restriction (< 1 L/day) — first-line for mild-moderate\n"
        "• Tolvaptan (V2 receptor antagonist): blocks ADH → free water excretion without Na loss\n"
        "• Demeclocycline: blocks ADH action at collecting duct (takes days)\n"
        "• 3% NaCl: only for symptomatic (seizures, obtundation)\n"
        "→ MASTERY NOTE: Pseudohyponatremia: sodium is normal but measured as low due to "
        "hyperlipidemia or hyperproteinemia displacing water fraction in serum. "
        "Ion-selective electrode method avoids this artifact. Check lipid panel if Na unexpectedly low.",

        'tier-review',
        _NM,
        DID['lab_values'],
        'electrolyte_abnormalities',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the potassium disorders chart, the EKG progression of hyperkalemia begins "
        "with _______ waves (earliest sign), then PR interval _______, "
        "then QRS _______, then _______ wave pattern before cardiac arrest.",

        "EKG progression of hyperkalemia (in order):\n"
        "1. Peaked (tall, narrow) T waves — K⁺ > 5.5 mEq/L (earliest, most sensitive)\n"
        "2. PR interval prolongation — K⁺ > 6.0\n"
        "3. QRS widening (bundle branch pattern) — K⁺ > 6.5\n"
        "4. Loss of P waves — K⁺ > 7.0\n"
        "5. Sine wave pattern (merged QRS + T) — K⁺ > 8.0 → imminent VF/asystole\n"
        "→ CCRN KEY: EKG changes do NOT always correlate with K⁺ level — some patients "
        "tolerate K⁺ 7.5 with minimal changes; others develop arrhythmia at 6.0. "
        "ALWAYS treat based on EKG findings, not K⁺ level alone.\n"
        "→ MASTERY NOTE: Hypokalemia EKG changes (different pattern): "
        "U waves (after T wave, especially visible V2–V3), flat/inverted T waves, "
        "ST depression, prolonged QU interval. Hypokalemia + digoxin = especially dangerous "
        "(low K⁺ potentiates digoxin toxicity → arrhythmias at 'therapeutic' digoxin levels).",

        'tier-high',
        _NM,
        DID['lab_values'],
        'electrolyte_abnormalities',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The calcium/magnesium tab shows hypomagnesemia causes refractory hypokalemia "
        "because Mg is required for renal _______ conservation. "
        "The ICU treatment dose for hypomagnesemia is _______ g of _______ IV, "
        "and the most dangerous cardiac risk when Mg < 1.0 + hypokalemia coexist is _______.",

        "Mg required for: renal potassium conservation (Mg-dependent K reabsorption at TALH)\n"
        "| Without Mg: Na-K-ATPase in renal tubules impairs → K wasted in urine\n"
        "| Treatment: MgSO₄ 2–4g IV over 30–60 min; repeat daily if ongoing losses\n"
        "| Replace Mg FIRST before potassium if both are depleted (K won't correct without Mg)\n"
        "| Cardiac risk with Mg < 1.0 + hypoK: torsades de pointes (prolonged QTc → polymorphic VT)\n"
        "→ CCRN KEY: Torsades treatment: MgSO₄ 2g IV push (even if Mg is 'normal' → pharmacologic). "
        "MgSO₄ suppresses early afterdepolarizations that trigger torsades. "
        "Also: correct K⁺ > 4.0, correct underlying QTc-prolonging drugs, "
        "overdrive pacing if refractory.\n"
        "→ MASTERY NOTE: Loop diuretics cause ALL of: ↓K⁺, ↓Mg²⁺, ↓Ca²⁺, metabolic alkalosis. "
        "ICU patients on prolonged furosemide need routine electrolyte replacement protocols. "
        "PPI therapy (omeprazole, pantoprazole) causes hypomagnesemia with chronic use "
        "by impairing active Mg absorption in small intestine.",

        'tier-critical',
        _NM,
        DID['lab_values'],
        'electrolyte_abnormalities',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ renal_labs ═══════════════════════════════════════════════════════════
    (
        "The AKI staging chart shows KDIGO Stage 2 AKI is defined as Cr _______ "
        "× baseline, or urine output < _______ mL/kg/h for ≥ _______ hours. "
        "Stage 3 criteria include Cr ≥ _______ mg/dL OR initiation of _______.",

        "KDIGO Stage 2: Cr ×2.0–2.9 baseline OR UO < 0.5 mL/kg/h for ≥ 12 hours\n"
        "| Stage 1: Cr ×1.5–1.9 or +0.3 mg/dL in 48h; UO < 0.5 mL/kg/h for 6–12h\n"
        "| Stage 3: Cr ×3.0+ OR Cr ≥ 4.0 mg/dL OR RRT initiated; UO < 0.3 mL/kg/h ×24h\n"
        "| Either criterion (Cr or UO) is sufficient for staging\n"
        "→ CCRN KEY: AKI management priorities at each stage:\n"
        "• Stage 1: identify/remove nephrotoxins; optimize MAP ≥ 65; avoid contrast; daily BMP\n"
        "• Stage 2: nephrology consult; consider CRRT if not recovering; loop diuretic trial\n"
        "• Stage 3: CRRT/HD; restrict Na/K/phosphorus; dose-adjust all renally cleared medications\n"
        "→ MASTERY NOTE: Urine output criteria require a Foley catheter — always place Foley in "
        "critically ill patients where AKI is suspected. UO criteria identify AKI before Cr rises "
        "(Cr lags 24–48h behind glomerular injury because it's a marker of excretory function, "
        "not injury itself).",

        'tier-review',
        _NM,
        DID['lab_values'],
        'renal_labs',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The renal differentiation chart shows FeNa < _______ % indicates pre-renal AKI. "
        "FeNa is calculated as _______. "
        "In patients receiving diuretics, FeNa is unreliable — instead use "
        "FeUrea < _______ % to identify pre-renal AKI.",

        "FeNa < 1%: pre-renal AKI (kidneys avidly retain Na → concentrated urine)\n"
        "| FeNa > 2%: intrinsic renal damage (ATN — tubules cannot conserve Na)\n"
        "| FeNa = (urine Na × plasma Cr) / (plasma Na × urine Cr) × 100%\n"
        "| FeNa invalid on diuretics (they force Na excretion regardless of volume status)\n"
        "| FeUrea < 35%: pre-renal (urea reabsorption intact); > 35%: intrinsic\n"
        "→ CCRN KEY: Pre-renal vs ATN differentiation:\n"
        "| Pre-renal: FeNa < 1%, urine Na < 20, urine Osm > 500, BUN:Cr > 20:1\n"
        "| ATN: FeNa > 2%, urine Na > 40, muddy brown/granular casts on UA, BUN:Cr 10–15:1\n"
        "→ MASTERY NOTE: Contrast-induced nephropathy (CIN) prevention:\n"
        "• Hydration: NS 1 mL/kg/h × 12h before and after (POSEIDON trial)\n"
        "• Use iso-osmolar or low-osmolar contrast; minimize contrast volume\n"
        "• Hold nephrotoxins (NSAIDs, ACEi, ARBs) peri-procedure\n"
        "• N-acetylcysteine (NAC): meta-analyses inconclusive but low risk/cost → still commonly used",

        'tier-high',
        _NM,
        DID['lab_values'],
        'renal_labs',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The CRRT indications chart uses the AEIOU mnemonic. "
        "A = _______, E = _______, I = _______, O = _______, U = _______. "
        "The recommended CRRT effluent dose per the KDIGO guideline is _______ mL/kg/h.",

        "AEIOU — CRRT/Dialysis Indications:\n"
        "| A = Acidosis: pH < 7.15–7.20 refractory to treatment\n"
        "| E = Electrolytes: K⁺ > 6.5 or refractory hyperkalemia\n"
        "| I = Ingestion: dialyzable toxins (lithium, metformin, salicylate, methanol, EG)\n"
        "| O = Overload: refractory fluid overload / pulmonary edema despite diuretics\n"
        "| U = Uremia: BUN > 100 or uremic symptoms (pericarditis, encephalopathy, platelet dysfunction)\n"
        "| KDIGO recommended effluent dose: 20–25 mL/kg/h\n"
        "→ CCRN KEY: CRRT vs intermittent hemodialysis (IHD):\n"
        "• CRRT: hemodynamically unstable (MAP < 65, vasopressors); gentle 24h fluid removal\n"
        "• IHD: stable patients; faster K⁺/toxin removal; 3–4h sessions\n"
        "• SLED (sustained low-efficiency dialysis): intermediate option for moderately unstable\n"
        "→ MASTERY NOTE: RENAL trial (NEJM 2009): higher-intensity CRRT (40 mL/kg/h) showed NO "
        "mortality benefit over standard dose (25 mL/kg/h). "
        "ATN trial: no benefit of early vs late RRT initiation in non-emergent AKI. "
        "STARRT-AKI: liberal strategy (waiting for 'urgent indications') was non-inferior.",

        'tier-critical',
        _NM,
        DID['lab_values'],
        'renal_labs',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ coagulation_labs ═════════════════════════════════════════════════════
    (
        "On the coagulation panel chart, PT/INR reflects the _______ coagulation pathway "
        "and is prolonged by _______. aPTT reflects the _______ pathway "
        "and is used to monitor _______ therapy.",

        "PT/INR: extrinsic pathway — factors VII (shortest t½), X, V, II, fibrinogen\n"
        "| Prolonged by: warfarin, liver disease, vitamin K deficiency, factor VII deficiency\n"
        "| aPTT: intrinsic pathway — XII, XI, IX, VIII, X, V, II, fibrinogen\n"
        "| aPTT used to monitor: unfractionated heparin (UFH) therapy\n"
        "| Therapeutic aPTT goal: 1.5–2.5× control (≈ 60–100 seconds)\n"
        "→ CCRN KEY: Factor VII has the shortest half-life (6h) → PT/INR rises first in liver failure "
        "or warfarin use. PT/INR is the most sensitive indicator of acute liver synthetic dysfunction. "
        "aPTT prolonged by heparin (intrinsic pathway inhibition via antithrombin III potentiation).\n"
        "→ MASTERY NOTE: Elevated aPTT with normal PT — causes:\n"
        "• UFH contamination of sample (draw from opposite arm from heparin drip)\n"
        "• Factor VIII/IX deficiency (hemophilia A/B)\n"
        "• von Willebrand disease (type 3)\n"
        "• Lupus anticoagulant (paradoxical: ↑ aPTT but THROMBOTIC, not bleeding disorder)\n"
        "Mixing study: if aPTT corrects → factor deficiency; if does NOT correct → inhibitor present.",

        'tier-review',
        _NM,
        DID['lab_values'],
        'coagulation_labs',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The DIC diagnosis chart uses the ISTH scoring system. "
        "Platelets < _______ K = 2 points. "
        "D-dimer strongly elevated = _______ points. "
        "PT prolonged > _______ seconds = 2 points. "
        "A score ≥ _______ confirms overt DIC.",

        "ISTH Overt DIC Score:\n"
        "| Platelets: > 100K = 0; 50–100K = 1 point; < 50K = 2 points\n"
        "| D-dimer/fibrin degradation: no increase = 0; moderate = 2; strong = 3 points\n"
        "| PT prolongation: < 3s = 0; 3–6s = 1 point; > 6s = 2 points\n"
        "| Fibrinogen: ≥ 1 g/L = 0; < 1 g/L = 1 point\n"
        "| Score ≥ 5 = overt DIC; < 5 = non-overt or pre-DIC\n"
        "→ CCRN KEY: DIC treatment priorities:\n"
        "• Address the precipitant FIRST (sepsis → abx/vasopressors; APL → ATRA; placental abruption → delivery)\n"
        "• Replace consumed factors: FFP (PT/aPTT), cryoprecipitate (fibrinogen < 100), platelets (< 50K with bleeding)\n"
        "• Target: fibrinogen > 100–150, platelets > 50K if bleeding, PT < 1.5× normal\n"
        "→ MASTERY NOTE: DIC causes by mechanism:\n"
        "• Tissue factor release: sepsis (#1), trauma, amniotic fluid embolism, brain injury\n"
        "• Endothelial activation: HELLP syndrome, TTP, vasculitis\n"
        "• Classic presentation: APL (M3 AML) — the most dramatic DIC, responds to ATRA + arsenic",

        'tier-high',
        _NM,
        DID['lab_values'],
        'coagulation_labs',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "On the anticoagulation monitoring chart, therapeutic UFH targets aPTT "
        "_______ × control. For LMWH, therapeutic monitoring uses anti-Xa level "
        "of _______ units/mL drawn _______ hours post-dose. "
        "Anti-Xa monitoring of LMWH is indicated in _______ patients.",

        "UFH therapeutic aPTT: 1.5–2.5× control (≈ 60–100 seconds)\n"
        "| UFH anti-Xa alternative: 0.3–0.7 units/mL (less subject to lab interference)\n"
        "| LMWH therapeutic anti-Xa: 0.5–1.0 units/mL (peak, drawn 4 hours post-dose)\n"
        "| LMWH prophylactic anti-Xa: 0.2–0.5 units/mL\n"
        "| Anti-Xa monitoring for LMWH indicated in: renal failure (CrCl < 30), obesity (> 120 kg), pregnancy\n"
        "→ CCRN KEY: Check aPTT 6h after UFH initiation or dose change; continue checks q6h "
        "until ≥ 2 consecutive therapeutic values, then q24h. "
        "Subtherapeutic aPTT in first 24h → ↑ VTE recurrence risk. "
        "Supratherapeutic → bleeding risk.\n"
        "→ MASTERY NOTE: DOACs (rivaroxaban, apixaban, dabigatran) do NOT require routine monitoring. "
        "Special reversal agents: idarucizumab (Praxbind) for dabigatran; "
        "andexanet alfa (Andexxa) for factor Xa inhibitors (rivaroxaban, apixaban). "
        "4-factor PCC (Kcentra) is also used off-label for Xa inhibitor reversal when andexanet unavailable.",

        'tier-critical',
        _NM,
        DID['lab_values'],
        'coagulation_labs',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ cardiac_markers ══════════════════════════════════════════════════════
    (
        "On the cardiac markers chart, high-sensitivity troponin begins rising "
        "within _______ hours of MI and peaks at _______ hours. "
        "A troponin that remains elevated for > _______ days after MI helps "
        "estimate _______ size.",

        "hsTroponin rises: 1–3 hours after myocardial injury\n"
        "| Peak: 12–24 hours (conventional); may stay elevated days\n"
        "| Remains elevated: 7–14 days (estimates infarct size — larger MI = longer elevation)\n"
        "| Cutoff: 99th percentile of normal population (lab-specific, typically 0.04–0.06 ng/mL)\n"
        "→ CCRN KEY: Rule-in/rule-out MI protocols using hsTroponin:\n"
        "• 0/1h protocol: baseline + 1h (ESC recommended); delta > 5–6 ng/L = rule-in\n"
        "• 0/3h protocol: baseline + 3h; validated for most hospitals\n"
        "• Serial troponins: ↑ delta (rising pattern) = acute injury; flat elevation = chronic\n"
        "→ MASTERY NOTE: Non-cardiac troponin elevation (false-positive for ACS):\n"
        "• PE (RV strain), myocarditis, sepsis-induced cardiomyopathy, stress (Takotsubo)\n"
        "• ESRD (impaired clearance), ARDS, rhabdomyolysis, direct myocardial contusion\n"
        "Key distinction: clinical context + EKG + wall motion abnormality on echo + delta troponin pattern. "
        "Isolated troponin elevation without rising delta or EKG changes = less likely ACS.",

        'tier-review',
        _NM,
        DID['lab_values'],
        'cardiac_markers',
        '{"hi":0}',
        'chart-l1'
    ),
    (
        "The markers chart shows BNP > _______ pg/mL suggests heart failure. "
        "NT-proBNP > _______ pg/mL (age-adjusted) indicates significant HF. "
        "Procalcitonin (PCT) is most useful for _______ antibiotic therapy "
        "when PCT drops to < _______ ng/mL or falls > _______ % from peak.",

        "BNP > 100 pg/mL: suggests HF; BNP > 400: likely decompensated HF\n"
        "| NT-proBNP: age-adjusted cutoffs — > 300 (any age) for acute HF exclusion cutoff\n"
        "| NT-proBNP rule-in: > 450 (< 50y), > 900 (50–75y), > 1800 (> 75y)\n"
        "| PCT use: DE-ESCALATION (stopping) antibiotic therapy in sepsis/bacterial infections\n"
        "| PCT stop rule: PCT < 0.5 ng/mL OR > 80% reduction from peak → safe to stop abx\n"
        "→ CCRN KEY: PROACT-3 and SAPS trials: PCT-guided antibiotic de-escalation reduces "
        "antibiotic duration by 2–3 days without increased mortality. "
        "Most effective in community-acquired pneumonia and sepsis. "
        "PCT does NOT guide de-escalation in ventilator-associated pneumonia (less validated).\n"
        "→ MASTERY NOTE: BNP vs NT-proBNP differences:\n"
        "• BNP: shorter t½ (20 min), more affected by obesity (↓ BNP in obese patients)\n"
        "• NT-proBNP: longer t½ (120 min), higher in renal failure (renally cleared)\n"
        "• Both rise with PEEP and mechanical ventilation (↑ myocardial wall stress)\n"
        "• Trending is more important than a single value",

        'tier-high',
        _NM,
        DID['lab_values'],
        'cardiac_markers',
        '{"hi":2}',
        'chart-l2'
    ),
    (
        "On the cardiac markers chart, procalcitonin (PCT) > _______ ng/mL "
        "supports severe sepsis/septic shock. PCT is falsely elevated in non-infectious "
        "conditions including _______ and _______. "
        "CK-MB is uniquely useful after MI to detect _______ because troponin remains elevated.",

        "PCT > 2.0 ng/mL: likely sepsis; > 10 ng/mL: severe sepsis/septic shock\n"
        "| PCT falsely elevated (non-infectious): major surgery/trauma, burns, cardiogenic shock, "
        "pancreatitis, medullary thyroid carcinoma\n"
        "| PCT falsely low: early infection, localized infection, viral/fungal (PCT is bacterial-specific)\n"
        "| CK-MB: useful for REINFARCTION detection — returns to baseline 24–72h after MI\n"
        "| If CK-MB re-rises after normalizing = new MI (troponin stays elevated days, masking re-infarction)\n"
        "→ CCRN KEY: Sepsis biomarker interpretation:\n"
        "• No single biomarker diagnoses sepsis — use clinical picture + sequential assessment\n"
        "• PCT trend > single value: rising PCT = inadequate treatment; falling = responding\n"
        "• CRP (C-reactive protein): less specific than PCT; useful for trending inflammation\n"
        "→ MASTERY NOTE: Point-of-care lactate testing enables rapid triage in sepsis screening. "
        "Lactate > 2 mmol/L in a febrile patient with suspected infection = sepsis by Sepsis-3 "
        "definition (regardless of whether septic shock criteria met). "
        "Lactate-guided resuscitation (target < 2) is now preferred over ScvO₂ targets "
        "in most protocols (more accessible, no central line required).",

        'tier-critical',
        _NM,
        DID['lab_values'],
        'cardiac_markers',
        '{"hi":3}',
        'chart-l3'
    ),
]

# ── Build pipeline ─────────────────────────────────────────────────────────────
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
