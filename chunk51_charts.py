#!/usr/bin/env python3
"""chunk51_charts.py — Ph8 Reference: Clinical Terminology (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_50.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_51.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c51')
CHUNK_NUM   = 51
MID_BASE    = 1_800_005_100
CHART_ORDER = ['oxygenation_formulas', 'clinical_scoring', 'ards_berlin',
               'sepsis_definitions', 'icu_syndromes']

_NM = 'Ph8 · \U0001f7e1 T3 · Reference — Clinical Terminology'

RF = {}

# ── Chart 1: Oxygenation Formulas ─────────────────────────────────────────────
RF['oxygenation_formulas'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var rows=[
        {n:'P/F Ratio',
         calc:'PaO₂ ÷ FiO₂\n(FiO₂ as decimal)',
         norm:'> 400',
         crit:'< 300 = hypox RF\n< 200 = mod ARDS\n< 100 = severe ARDS',
         use:'ARDS Berlin staging\nVentilation decision\nProning threshold (<150)',
         c:'#4488cc'},
        {n:'A-a Gradient',
         calc:'PAO₂ − PaO₂\nPAO₂=[FiO₂×(713)]−PaCO₂/0.8',
         norm:'< 10–15 mmHg\n(young adult, RA)',
         crit:'> 30 mmHg = sig\nincreases with age\n(age/4 + 4 = expected)',
         use:'Distinguish V/Q from\nhypoventilation:\nNormal A-a + low PaO₂ = hypovent',
         c:'#3a9a5c'},
        {n:'Oxygenation\nIndex (OI)',
         calc:'FiO₂ × Paw × 100\n÷ PaO₂',
         norm:'< 5',
         crit:'> 25 = severe\n> 40 = ECMO\nthreshold (neonates)',
         use:'ARDS severity, ECMO\nHigh OI = worse lung\nInverse of P/F × Paw',
         c:'#cc8844'},
        {n:'CaO₂\n(O₂ content)',
         calc:'(Hgb×1.34×SaO₂)\n+ (PaO₂×0.003)',
         norm:'19–21 mL/dL',
         crit:'< 10 mL/dL = severe\nHgb dominant term\n(dissolved O₂ minor)',
         use:'DO₂ calculation\nAnemia impact: ↓Hgb\n→ ↓ CaO₂ → ↓ DO₂',
         c:'#9060c0'},
        {n:'DO₂\n(O₂ Delivery)',
         calc:'CO × CaO₂ × 10',
         norm:'950–1150 mL/min',
         crit:'< 300 mL/min =\ncritical threshold;\ntissue O₂ debt begins',
         use:'Global O₂ supply\nOptimize: CO, Hgb, SaO₂\nSepsis resuscitation target',
         c:'#cc4444'},
        {n:'O₂ER\n(O₂ Extraction)',
         calc:'(SaO₂−SvO₂) ÷ SaO₂\nOR: VO₂ ÷ DO₂ × 100',
         norm:'22–30%',
         crit:'> 40–50% =\nsupply-dependent\nconsumption (crisis)',
         use:'Adequacy of DO₂;\nSvO₂ < 60% = ↑O₂ER\nNormal SvO₂: 65–75%',
         c:'#e06060'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/rows.length);
    var xs=[4,80,195,270,355,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Index','Formula','Normal','Critical','ICU Interpretation'];
    ctx.font='bold 7.5px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    rows.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=d.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=d.c;ctx.font='bold 7.5px sans-serif';ctx.textAlign='left';
        d.n.split('\n').forEach(function(l,li){ctx.fillText(l,xs[0]+2,ry+rh/2-4+li*9);});
        ctx.fillStyle='#eedd88';ctx.font='7px sans-serif';ctx.textAlign='left';
        d.calc.split('\n').forEach(function(l,li){ctx.fillText(l,xs[1]+2,ry+rh/2-7+li*9);});
        ctx.fillStyle='#88cc88';ctx.font='7px sans-serif';ctx.textAlign='left';
        d.norm.split('\n').forEach(function(l,li){ctx.fillText(l,xs[2]+2,ry+rh/2-7+li*9);});
        ctx.fillStyle='#ff9966';ctx.font='7px sans-serif';ctx.textAlign='left';
        d.crit.split('\n').forEach(function(l,li){ctx.fillText(l,xs[3]+2,ry+rh/2-7+li*9);});
        ctx.fillStyle='#99aabb';ctx.font='7px sans-serif';ctx.textAlign='left';
        d.use.split('\n').forEach(function(l,li){ctx.fillText(l,xs[4]+2,ry+rh/2-9+li*9);});
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
        var lbs=['P/F Ratio','A-a Gradient','OI','CaO₂','DO₂','O₂ER'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,rows[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: Clinical Scoring Systems ─────────────────────────────────────────
RF['clinical_scoring'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['SOFA Score','qSOFA + APACHE II','Glasgow Coma Scale'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a2a1a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a3a2a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#3a9a5c':'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#080a08';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+13;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#3a9a5c';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+195,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a3a2a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('SOFA — 6 Organ Systems (each scored 0–4):','','#eedd88');
        hr();
        nt('Respiratory: PaO₂/FiO₂  0=≥400 | 1=300–399 | 2=200–299 | 3=100–199 | 4=<100 on MV');
        nt('Coagulation: Platelets  0=≥150K | 1=100–149K | 2=50–99K | 3=20–49K | 4=<20K');
        nt('Liver: Bilirubin  0=<1.2 | 1=1.2–1.9 | 2=2.0–5.9 | 3=6.0–11.9 | 4=≥12 mg/dL');
        nt('CNS: GCS  0=15 | 1=13–14 | 2=10–12 | 3=6–9 | 4=<6');
        nt('Cardiovascular: MAP or vasopressor dose (0=MAP≥70; 4=NE/Epi>0.1 mcg/kg/min)');
        nt('Renal: Creatinine or UO (0=<1.2 | 4=≥5.0 mg/dL or UO<200 mL/24h)');
        hr();
        rw('Sepsis definition:','SOFA increase ≥ 2 from baseline','#cc4444','#ff6644');
        rw('SOFA ≥ 11:','> 50% predicted ICU mortality','#cc4444','#ff6644');
        nt('Total range 0–24; score 2-week before baseline assumed = 0 if no prior organ dysfunction');
    } else if(sel===1){
        rw('qSOFA (3-item bedside screen):','Score ≥ 2 = high risk','#4488cc','#eedd88');
        nt('1. Respiratory rate ≥ 22 breaths/min');
        nt('2. Altered mental status (GCS < 15)');
        nt('3. Systolic BP ≤ 100 mmHg');
        nt('Use OUTSIDE ICU to identify infection + risk of poor outcome (≥ 2 = initiate workup)');
        nt('Sensitivity ~70% for sepsis; does NOT replace SOFA for diagnosis inside ICU');
        hr();
        rw('APACHE II (12 physiologic variables + age + chronic health):','','#cc8844');
        nt('Variables: temp, MAP, HR, RR, PaO₂ or A-a gradient, pH, Na, K, Cr, Hct, WBC, GCS');
        nt('Age points: 0 (< 44) to 6 (≥ 75)  |  Chronic health: 2 pts (elective) or 5 pts (emergency)');
        nt('Range 0–71; APACHE II ≥ 25 = ~50% predicted mortality; used for ICU risk stratification');
        hr();
        rw('SAPS II (Simplified Acute Physiology Score):','','#9060c0');
        nt('17 variables; score 0–163; used in European ICUs; similar predictive value to APACHE II');
        nt('★ Scores predict POPULATION mortality — individual patients may exceed or fall short');
    } else {
        rw('Glasgow Coma Scale (GCS):','Range 3–15','#eedd88','#ffcc44');
        hr();
        rw('Eye Opening (E):','4 = spontaneous | 3 = to voice | 2 = to pain | 1 = none','#4488cc','#eedd88');
        rw('Verbal (V):','5 = oriented | 4 = confused | 3 = words | 2 = sounds | 1 = none','#3a9a5c','#eedd88');
        rw('Motor (M):','6 = follows | 5 = localizes | 4 = withdraws | 3 = flex | 2 = ext | 1 = none','#cc8844','#eedd88');
        hr();
        rw('Thresholds:','','#cc4444');
        nt('GCS ≤ 8: "comatose" — conventional intubation threshold (assess airway protection)');
        nt('GCS < 15: altered mental status (use as AMS criterion for qSOFA and CAM-ICU)');
        nt('GCS 3 (minimum): no eye, verbal, or motor response — deeply comatose');
        hr();
        rw('Motor score alone (M):','','#88bbee');
        nt('M score 1–6 predicts outcome as well as full GCS for TBI prognostication');
        nt('M ≤ 4 (abnormal flexion or worse) = severe injury; M = 6 = following commands normally');
        hr();
        nt('★ Document: 3 subscores (e.g., E3V4M5 = GCS 12), not just total — captures trend better');
    }
    if(ctrl){
        ctrl.innerHTML='';
        var crow=document.createElement('div');crow.style.cssText='display:flex;gap:6px;margin-top:6px;';
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,'#3a9a5c',sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });crow.appendChild(b);})(i);});
        ctrl.appendChild(crow);
    }
}
"""

# ── Chart 3: ARDS Berlin Definition ──────────────────────────────────────────
RF['ards_berlin'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Berlin Definition','ARDS Management Tiers','ARDS Mimics'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a1a2e':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#4488cc':'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#08080f';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+13;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#4488cc';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+185,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('ARDS Berlin Definition — 3 Required Criteria:','','#eedd88');
        hr();
        rw('1. Timing:','Within 1 week of known clinical insult or new/worsening symptoms','#4488cc','#eedd88');
        rw('2. Chest Imaging:','Bilateral opacities — not fully explained by effusions, atelectasis, nodules','#4488cc','#eedd88');
        rw('3. Origin of Edema:','Not fully explained by heart failure or fluid overload','#4488cc','#eedd88');
        nt('If no risk factor: echocardiogram to exclude hydrostatic edema; PCWP or BNP may help');
        hr();
        rw('Severity Classification (P/F with PEEP ≥ 5 cmH₂O):','','#cc8844');
        rw('Mild:','P/F 200–300 mmHg; PEEP ≥ 5','#3a9a5c','#eedd88');
        rw('Moderate:','P/F 100–200 mmHg; PEEP ≥ 5','#cc8844','#ffcc88');
        rw('Severe:','P/F < 100 mmHg; PEEP ≥ 5','#cc4444','#ff6644');
        hr();
        nt('★ Berlin replaced the 1994 American-European Consensus (AECC) definition in 2012');
        nt('★ Mortality: Mild ~27% | Moderate ~32% | Severe ~45%');
    } else if(sel===1){
        rw('Stepwise ARDS Management (escalate in order):','','#eedd88');
        hr();
        rw('Step 1 (all ARDS):','LPV: Vt 6 mL/kg IBW, Pplat ≤ 30, optimize PEEP/FiO₂','#3a9a5c','#eedd88');
        rw('Step 2 (moderate–severe):','Driving pressure ΔP ≤ 15 cmH₂O; reassess compliance q4h','#3a9a5c','#eedd88');
        rw('Step 3 (P/F < 150):','Prone positioning ≥ 16h/day (PROSEVA: NNT=6)','#cc8844','#ffcc88');
        rw('Step 4 (P/F < 150 + refractory):','NMBA 48h (ROSE trial: no benefit vs deep sedation alone)','#cc8844','#ffcc88');
        rw('Step 5 (severe, refractory):','VV-ECMO if P/F < 80 or pH < 7.20 despite optimization','#cc4444','#ff6644');
        hr();
        rw('Rescue therapies (limited evidence):','','#9060c0');
        nt('Inhaled NO / iloprost: temporary oxygenation improvement; no mortality benefit');
        nt('Recruitment maneuvers: ART trial showed HARM in moderate-severe ARDS — avoid routine use');
        nt('High-frequency oscillatory ventilation (HFOV): OSCILLATE/OSCAR — no benefit, possibly harmful');
        hr();
        nt('★ ROSE trial (NEJM 2019): early NMBA (cisatracurium ×48h) not superior to light sedation');
    } else {
        rw('ARDS Mimics — Must Exclude Before Diagnosing ARDS:','','#cc4444');
        hr();
        rw('Cardiogenic Pulmonary Edema:','PCWP > 18, BNP elevated, responds to diuresis','#4488cc','#eedd88');
        nt('Distinguishing: PCWP or BNP; echo showing diastolic dysfunction / EF low / LVEDD ↑');
        nt('Response to furosemide with ↑ PaO₂: suggests cardiogenic, NOT ARDS');
        hr();
        rw('Diffuse Alveolar Hemorrhage (DAH):','','#cc4444');
        nt('Progressive hemoptysis + bilateral opacities + ↓ Hgb; serial bloody BAL is diagnostic');
        nt('Causes: vasculitis (ANCA/anti-GBM), SLE, coagulopathy, bone marrow transplant');
        nt('Treatment: high-dose steroids; treat underlying cause');
        hr();
        rw('Acute Eosinophilic Pneumonia:','','#cc8844');
        nt('BAL eosinophils > 25%; often young smokers; rapid response to steroids');
        hr();
        rw('Transfusion-Related (TRALI):','','#9060c0');
        nt('ARDS within 6h of transfusion; donor antibodies (anti-HLA/anti-HNA); treat supportively');
        hr();
        nt('★ Cryptogenic Organizing Pneumonia (COP): basilar consolidation + tree-in-bud; steroid-responsive');
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

# ── Chart 4: Sepsis Definitions ───────────────────────────────────────────────
RF['sepsis_definitions'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Sepsis-3 Definitions','Hour-1 Bundle','Source Control'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#2a1a0a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#3a2a1a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#cc6633':'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0804';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+13;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#cc6633';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+200,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#3a2a1a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('SEPSIS (Sepsis-3, 2016):','','#cc6633');
        nt('Life-threatening organ dysfunction caused by a dysregulated host response to infection');
        nt('Organ dysfunction = acute SOFA increase ≥ 2 (assumed baseline SOFA = 0 if unknown)');
        nt('Associated hospital mortality > 10%');
        hr();
        rw('SEPTIC SHOCK:','','#cc4444');
        nt('Sepsis + vasopressor requirement to maintain MAP ≥ 65 mmHg');
        nt('AND serum lactate > 2 mmol/L DESPITE adequate fluid resuscitation');
        nt('Associated hospital mortality > 40%');
        hr();
        rw('SIRS (Sepsis-1/2 era — no longer diagnostic for sepsis):','','#aaa');
        nt('Temp > 38°C or < 36°C | HR > 90 | RR > 20 or PaCO₂ < 32 | WBC > 12K or < 4K or > 10% bands');
        nt('SIRS can occur without infection (trauma, burns, pancreatitis) — low specificity for sepsis');
        hr();
        rw('qSOFA (outside ICU screen):','','#cc8844');
        nt('RR ≥ 22 | AMS | SBP ≤ 100; score ≥ 2 = high risk → prompt evaluation + SOFA');
    } else if(sel===1){
        rw('SSC Hour-1 Bundle (2018 update — 5 elements):','','#cc6633');
        hr();
        rw('1. Measure lactate:','(Repeat if > 2 mmol/L; serial q2h until < 2)','#cc8844','#eedd88');
        rw('2. Blood cultures:','Obtain BEFORE antibiotics (≥ 2 sets; do not delay abx > 45 min)','#cc8844','#eedd88');
        rw('3. Antibiotics:','Broad-spectrum within 1 HOUR of sepsis/shock recognition','#cc4444','#ff6644');
        rw('4. Crystalloids:','30 mL/kg IV if hypotensive or lactate ≥ 4 mmol/L','#4488cc','#88ccff');
        rw('5. Vasopressors:','Norepinephrine first-line; start if MAP < 65 despite IVF','#cc4444','#ff6644');
        hr();
        rw('Lactate-guided resuscitation targets:','','#3a9a5c');
        nt('Goal: lactate < 2 mmol/L (normalization)');
        nt('Clearance goal: ≥ 10% reduction per 2 hours (LACTATES trial — equivalent to ScvO₂-guided)');
        hr();
        nt('★ 1-hour antibiotic target: every hour of delay in septic shock = ~7% ↑ mortality');
        nt('★ 30 mL/kg IVF: reassess after each 500 mL bolus with dynamic fluid responsiveness test');
    } else {
        rw('Source Control — Definition:','','#cc6633');
        nt('Physical measures to control infectious focus: drainage, debridement, device removal');
        nt('Optimal timing: within 6–12 hours of septic shock recognition');
        hr();
        rw('Source Control by Pathology:','','#cc8844');
        nt('Intra-abdominal abscess: percutaneous drainage (IR) — preferred if accessible');
        nt('Ruptured appendix/diverticular perf: surgical drainage/resection (emergent)');
        nt('Cholangitis/biliary sepsis: ERCP with biliary drainage (within 24h)');
        nt('Necrotizing fasciitis: immediate surgical debridement (mortality doubles per hour of delay)');
        nt('Infected device (CVC, urinary catheter, prosthesis): remove + culture + new access at new site');
        hr();
        rw('Infected IV Device Protocol:','','#4488cc');
        nt('Central line: remove if S. aureus, Candida, or clinical septic shock attributable to line');
        nt('Catheter-related BSI (CRBSI): culture catheter tip + peripheral blood + catheter blood');
        nt('Lock therapy (salvage attempt): only for coagulase-negative Staph in non-tunneled lines');
        hr();
        nt('★ SSC recommendation: source control within 6–12h; do NOT delay for hemodynamic stability');
    }
    if(ctrl){
        ctrl.innerHTML='';
        var crow=document.createElement('div');crow.style.cssText='display:flex;gap:6px;margin-top:6px;';
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,'#cc6633',sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });crow.appendChild(b);})(i);});
        ctrl.appendChild(crow);
    }
}
"""

# ── Chart 5: ICU Syndromes ────────────────────────────────────────────────────
RF['icu_syndromes'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['ICUAW & MODS','Delirium / CAM-ICU','PICS & Recovery'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a1a2a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#9060c0':'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#08080e';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+13;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#9060c0';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+195,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('ICU-Acquired Weakness (ICUAW):','','#9060c0');
        rw('Incidence:','25–50% of patients with sepsis/ARDS on MV > 7 days','#aab','#eedd88');
        rw('Diagnosis:','MRC sum score < 48 of 60 (6 muscle groups × 5 bilaterally)','#aab','#eedd88');
        nt('Subtypes: CIP (Critical Illness Polyneuropathy) | CIM (Myopathy) | CIPNM (combined)');
        nt('CIP: EMG shows axonal neuropathy | CIM: myopathic changes + ↑ CK');
        rw('Risk factors:','SIRS, sepsis, NMB, prolonged immobility, hyperglycemia, steroids','#aab','#bbb');
        rw('Prevention:','ABCDEF bundle (E = Exercise/Early Mobility); glycemic control 140–180','#3a9a5c','#eedd88');
        hr();
        rw('MODS (Multi-Organ Dysfunction Syndrome):','','#cc4444');
        nt('Sequential organ failure following severe systemic insult (sepsis, trauma, burns, ischemia)');
        nt('Typically progresses over 3–7 days; lung and kidney fail first → liver → coag → CNS');
        nt('SOFA score tracks progression; prevention = early source control + organ-protective strategy');
        hr();
        nt('★ ICUAW independently associated with prolonged MV, LOS, and 1-year mortality');
    } else if(sel===1){
        rw('DELIRIUM in the ICU:','Prevalence 20–80% of MV patients','#9060c0','#eedd88');
        nt('Hyperactive: agitated, pulling lines; Hypoactive (more common, worse outcomes): quiet/withdrawn');
        nt('Mixed: alternates. Hypoactive delirium most missed because patient appears "calm"');
        hr();
        rw('CAM-ICU (Confusion Assessment Method):','Positive = Delirium','#cc8844','#ffcc44');
        hr();
        rw('Feature 1:','ACUTE onset or FLUCTUATING course of mental status change','#4488cc','#eedd88');
        rw('Feature 2:','INATTENTION (letter recognition: SAVEAHAART; < 8/10 = fail)','#4488cc','#eedd88');
        rw('Feature 3:','DISORGANIZED thinking (4 yes/no questions + 3 commands)','#4488cc','#eedd88');
        rw('Feature 4:','ALTERED level of consciousness (RASS ≠ 0)','#4488cc','#eedd88');
        nt('CAM-ICU POSITIVE: Feature 1 AND Feature 2 AND (Feature 3 OR Feature 4)');
        hr();
        rw('Non-Pharmacologic Prevention (ABCDEF bundle):','','#3a9a5c');
        nt('A = Awakening (daily SAT)  |  B = Breathing (SBT)  |  C = Choice of sedation');
        nt('D = Delirium monitoring (CAM-ICU q4-8h)  |  E = Early Mobility  |  F = Family engagement');
        nt('Pharmacologic: NO proven delirium prevention drug (haloperidol, quetiapine = treatment only)');
    } else {
        rw('PICS (Post-Intensive Care Syndrome):','','#9060c0');
        rw('Incidence:','25–50% of ICU survivors; persists months to years','#aab','#eedd88');
        hr();
        rw('Three Domains of PICS Impairment:','','#cc8844');
        rw('1. Cognitive:','Memory, attention, executive function deficits (similar to mild TBI)','#cc8844','#eedd88');
        rw('2. Physical:','ICUAW, fatigue, dyspnea, dysphagia (functional disability)','#cc8844','#eedd88');
        rw('3. Mental Health:','PTSD (25%), depression (30%), anxiety (70%) in ICU survivors','#cc8844','#eedd88');
        hr();
        rw('Prevention Strategies:','','#3a9a5c');
        nt('ABCDEF bundle (all elements): reduces delirium → reduces long-term cognitive impairment');
        nt('ICU Diary: patient/family written record of events → reduces PTSD risk (60% in some trials)');
        nt('Early mobility protocol → reduces ICUAW and functional disability at 6 months');
        nt('Sleep hygiene: noise reduction, light control, cluster care, melatonin (limited evidence)');
        hr();
        rw('PICS-Family (PICS-F):','','#88bbee');
        nt('30% of family members of ICU patients develop PTSD, complicated grief, or depression');
        nt('Bereavement rounds, family meetings, communication training → reduce PICS-F burden');
        hr();
        nt('★ Survivor clinic programs: systematic post-ICU follow-up at 1, 3, 6 months → address PICS');
    }
    if(ctrl){
        ctrl.innerHTML='';
        var crow=document.createElement('div');crow.style.cssText='display:flex;gap:6px;margin-top:6px;';
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,'#9060c0',sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });crow.appendChild(b);})(i);});
        ctrl.appendChild(crow);
    }
}
"""

# ── Cards ─────────────────────────────────────────────────────────────────────
CARDS = [
    # ═══ oxygenation_formulas ═════════════════════════════════════════════════
    (
        "On the oxygenation formulas chart, P/F ratio = PaO₂ ÷ FiO₂. "
        "A P/F ratio < _______ defines hypoxemic respiratory failure. "
        "The Berlin criteria classify mild ARDS as P/F _______ to _______ mmHg "
        "with PEEP ≥ _______ cmH₂O.",

        "P/F < 300 mmHg = hypoxemic respiratory failure (general threshold)\n"
        "| Berlin ARDS classification (all require PEEP ≥ 5 cmH₂O):\n"
        "  • Mild ARDS: P/F 200–300 mmHg (hospital mortality ≈ 27%)\n"
        "  • Moderate ARDS: P/F 100–200 mmHg (mortality ≈ 32%)\n"
        "  • Severe ARDS: P/F < 100 mmHg (mortality ≈ 45%)\n"
        "→ CCRN KEY: P/F ratio uses FiO₂ as a decimal (0.50, not 50%). "
        "On room air (FiO₂ = 0.21): PaO₂ of 84 mmHg → P/F = 84/0.21 = 400 (normal). "
        "On 100% FiO₂: PaO₂ of 70 mmHg → P/F = 70/1.0 = 70 (severe ARDS). "
        "P/F < 150: prone positioning threshold (PROSEVA). P/F < 80 with pH < 7.20: VV-ECMO consideration.\n"
        "→ MASTERY NOTE: S/F ratio (SpO₂/FiO₂) can substitute when ABG unavailable — "
        "S/F < 315 correlates with P/F < 300. "
        "OI (Oxygenation Index) = FiO₂ × mean airway pressure × 100 ÷ PaO₂ — "
        "inverse of P/F, weighted by pressure: OI > 25 = severe ARDS; > 40 = ECMO threshold. "
        "OI better accounts for mean airway pressure contribution to oxygenation.",

        'tier-review',
        _NM,
        DID['terminology'],
        'oxygenation_formulas',
        '{"hi":0}',
        'chart-l1'
    ),
    (
        "The oxygenation chart shows oxygen delivery (DO₂) = _______ × _______ × 10. "
        "Normal DO₂ is _______ mL/min. "
        "The arterial oxygen content (CaO₂) formula is _______.",

        "DO₂ = CO × CaO₂ × 10 (the ×10 converts dL to L)\n"
        "| Normal DO₂: 950–1150 mL/min\n"
        "| CaO₂ = (Hgb × 1.34 × SaO₂) + (PaO₂ × 0.003)\n"
        "| Normal CaO₂: 19–21 mL/dL\n"
        "| Critical DO₂ threshold: < 300 mL/min → supply-dependent oxygen consumption → lactic acidosis\n"
        "→ CCRN KEY: The three determinants of DO₂ — CO, Hgb, and SaO₂. "
        "Hgb contributes most (1.34 mL O₂ per gram bound to hemoglobin vs 0.003 mL dissolved per mmHg PaO₂). "
        "Clinical implication: in anemia, increasing Hgb from 7→9 g/dL raises DO₂ by ~200 mL/min — "
        "more than any vasopressor manipulation. Transfusion threshold in sepsis: Hgb < 7 (TRISS trial, ICU).\n"
        "→ MASTERY NOTE: O₂ extraction ratio (O₂ER) = VO₂ ÷ DO₂ × 100% = (SaO₂ − SvO₂) ÷ SaO₂. "
        "Normal O₂ER: 22–30%. Body normally extracts 25% of delivered O₂ — large reserve. "
        "When DO₂ falls → O₂ER rises (tissues extract more). "
        "O₂ER > 40–50% = supply-dependent consumption — increased mortality. "
        "ScvO₂ < 60% (central venous) or SvO₂ < 50% (mixed venous) = high O₂ER = inadequate DO₂.",

        'tier-high',
        _NM,
        DID['terminology'],
        'oxygenation_formulas',
        '{"hi":4}',
        'chart-l2'
    ),
    (
        "On the oxygenation chart, the A-a gradient = PAO₂ − PaO₂, "
        "where PAO₂ = _______. "
        "A normal A-a gradient in a young adult is < _______ mmHg. "
        "An elevated A-a gradient with a normal PaCO₂ indicates _______, "
        "while a normal A-a gradient with elevated PaCO₂ indicates _______.",

        "PAO₂ = (FiO₂ × [Patm − PH₂O]) − PaCO₂/RQ\n"
        "| Simplified on room air at sea level: PAO₂ = (0.21 × 713) − PaCO₂/0.8 = 150 − PaCO₂/0.8\n"
        "| Normal A-a gradient: < 10–15 mmHg in young adults; increases with age (age/4 + 4)\n"
        "| Elevated A-a gradient + normal PaCO₂ → V/Q mismatch or intrapulmonary shunt\n"
        "| Normal A-a gradient + elevated PaCO₂ → pure hypoventilation (airway closed, lungs normal)\n"
        "→ CCRN KEY: The A-a gradient distinguishes CAUSE of hypoxemia:\n"
        "• Normal A-a (< 15) + ↑ PaCO₂ = hypoventilation (opiates, NMD, respiratory muscle failure)\n"
        "• Elevated A-a + normal/↑ PaCO₂ = V/Q mismatch (PE, ARDS, pneumonia) or shunt\n"
        "• Classic shunt: 100% FiO₂ does NOT correct PaO₂ (blood bypasses alveoli entirely)\n"
        "→ MASTERY NOTE: Shunt fraction (Qs/Qt) = (CcO₂ − CaO₂) / (CcO₂ − CvO₂). "
        "Normal shunt: 3–5% (bronchial and thebesian veins). "
        "Intrapulmonary shunt > 20% = refractory hypoxemia not correctable by FiO₂ alone "
        "(true shunt: atelectasis, consolidation, alveolar flooding). "
        "PEEP treats shunt by re-opening collapsed alveoli; FiO₂ alone cannot overcome shunt.",

        'tier-critical',
        _NM,
        DID['terminology'],
        'oxygenation_formulas',
        '{"hi":1}',
        'chart-l3'
    ),

    # ═══ clinical_scoring ═════════════════════════════════════════════════════
    (
        "The SOFA scoring chart covers _______ organ systems, each scored 0–4. "
        "Sepsis is defined by an acute SOFA increase ≥ _______. "
        "The respiratory component uses _______ ratio; "
        "a respiratory SOFA score of 4 requires _______.",

        "SOFA covers 6 organ systems: Respiratory / Coagulation / Liver / CNS / Cardiovascular / Renal\n"
        "| Sepsis = acute SOFA increase ≥ 2 from baseline\n"
        "| Respiratory component: PaO₂/FiO₂ ratio\n"
        "  • 0 = P/F ≥ 400 | 1 = P/F 300–399 | 2 = P/F 200–299\n"
        "  • 3 = P/F 100–199 on ventilatory support\n"
        "  • 4 = P/F < 100 on ventilatory support\n"
        "| Respiratory SOFA 4 requires: P/F < 100 AND mechanical ventilation\n"
        "→ CCRN KEY: SOFA score tracks organ dysfunction progression. "
        "Rising SOFA over 24–48h = trajectory toward MODS. "
        "Cardiovascular SOFA 4 = norepinephrine or epinephrine > 0.1 mcg/kg/min. "
        "SOFA ≥ 11 → > 50% predicted ICU mortality. "
        "SOFA better than SIRS for identifying sepsis: more specific, outcome-validated.\n"
        "→ MASTERY NOTE: SOFA coagulation component (platelets) is linear:\n"
        "• 0 = platelets ≥ 150K | 1 = 100–149K | 2 = 50–99K | 3 = 20–49K | 4 = < 20K\n"
        "The CNS component uses GCS:\n"
        "• 0 = GCS 15 | 1 = GCS 13–14 | 2 = GCS 10–12 | 3 = GCS 6–9 | 4 = GCS < 6",

        'tier-review',
        _NM,
        DID['terminology'],
        'clinical_scoring',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the qSOFA chart, the three bedside criteria are RR ≥ _______, "
        "_______, and SBP ≤ _______ mmHg. "
        "A qSOFA score ≥ _______ outside the ICU identifies high risk for poor outcome. "
        "APACHE II includes _______ physiologic variables plus age and chronic health points.",

        "qSOFA — 3 criteria (1 point each):\n"
        "| 1. RR ≥ 22 breaths/min\n"
        "| 2. Altered mental status (GCS < 15)\n"
        "| 3. SBP ≤ 100 mmHg\n"
        "| Score ≥ 2: high risk for poor outcome from infection — prompt workup + escalation\n"
        "| APACHE II: 12 physiologic variables + age + chronic health score (range 0–71)\n"
        "| Variables: temp, MAP, HR, RR, PaO₂/A-a gradient, pH, Na, K, Cr, Hct, WBC, GCS\n"
        "→ CCRN KEY: qSOFA intended for use OUTSIDE the ICU (ED, ward) to identify patients "
        "who need transfer to higher level of care. Not for ICU patients — use full SOFA inside ICU. "
        "Sensitivity ~70% for sepsis — use as screen, not rule-out tool. "
        "Positive qSOFA → perform full SOFA score + blood cultures + lactate + broadspectrum abx.\n"
        "→ MASTERY NOTE: APACHE II score ≥ 25 = approximately 50% predicted ICU mortality. "
        "However, APACHE/SOFA predict POPULATION outcomes — individual patients can dramatically "
        "exceed (or underperform) predicted mortality. "
        "Never use a score alone to withhold aggressive ICU care — use in context with goals of care discussion. "
        "SAPS II: European equivalent of APACHE II (17 variables, 0–163, similar predictive validity).",

        'tier-high',
        _NM,
        DID['terminology'],
        'clinical_scoring',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The GCS chart shows total score range _______ to _______. "
        "GCS ≤ _______ is the conventional intubation threshold for airway protection. "
        "The motor subscore ranges from _______ (no response) to _______ (follows commands). "
        "When documenting GCS, you should record _______.",

        "GCS total range: 3 (minimum) to 15 (maximum)\n"
        "| Intubation threshold: GCS ≤ 8 (conventional — assess airway protection ability)\n"
        "| Motor subscore: 1 = no response | 2 = abnormal extension | 3 = abnormal flexion\n"
        "  4 = withdrawal | 5 = localizes pain | 6 = follows commands\n"
        "| Documentation: record all 3 subscores (e.g., E3V4M5 = GCS 12)\n"
        "→ CCRN KEY: GCS ≤ 8 = severe TBI — initiate intubation. "
        "BUT: GCS is a guide, not an absolute rule. A patient with GCS 9 who is vomiting "
        "and obtunded may need intubation sooner than one with GCS 7 who is cooperative. "
        "Assess: airway patency, gag reflex, secretion clearance ability, trend direction.\n"
        "→ MASTERY NOTE: GCS limitations in the ICU:\n"
        "• Verbal score (V) cannot be assessed in intubated patients → use E+M only, document as 'Vt'\n"
        "• Sedation confounds all components — only interpret GCS after SAT (sedation holiday)\n"
        "• GCS poor for posterior fossa lesions (brainstem/cerebellar) — patients may have intact motor\n"
        "• Motor component alone (M score) predicts TBI outcome as well as full GCS in most studies\n"
        "• FOUR Score (Full Outline of UnResponsiveness) = alternative that assesses brainstem reflexes",

        'tier-critical',
        _NM,
        DID['terminology'],
        'clinical_scoring',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ ards_berlin ══════════════════════════════════════════════════════════
    (
        "The ARDS Berlin definition requires: onset within _______ of a clinical insult, "
        "bilateral _______ on chest imaging not fully explained by effusion/atelectasis/nodules, "
        "and exclusion of _______ as primary cause. "
        "Severe ARDS is P/F < _______ mmHg with PEEP ≥ _______ cmH₂O.",

        "ARDS Berlin — 3 Required Criteria:\n"
        "| 1. Timing: within 1 week of known clinical insult or new/worsening respiratory symptoms\n"
        "| 2. Imaging: bilateral opacities — not fully explained by effusions, atelectasis, or nodules\n"
        "| 3. Origin: not fully explained by heart failure or fluid overload\n"
        "| (If no risk factor: echo to exclude hydrostatic edema; PCWP or BNP may assist)\n"
        "| Severity with PEEP ≥ 5 cmH₂O: Mild P/F 200–300 | Moderate 100–200 | Severe < 100 mmHg\n"
        "→ CCRN KEY: Berlin definition replaced the 1994 AECC definition in 2012. "
        "Key change: eliminated PCWP threshold (> 18 = cardiogenic) because cardiogenic pulmonary edema "
        "and ARDS can coexist. Also added PEEP requirement for P/F staging to eliminate "
        "PEEP-sensitive oxygenation variation from masking true severity.\n"
        "→ MASTERY NOTE: ARDS requires all THREE criteria simultaneously. "
        "Common trap: bilateral infiltrates on CXR alone does NOT diagnose ARDS — "
        "must exclude hydrostatic edema as primary cause. "
        "'Not fully explained' allows coexistence: a patient can have ARDS + mild volume overload. "
        "When in doubt: diuretic trial + echo + BNP + PA catheter (if needed) to characterize edema origin.",

        'tier-review',
        _NM,
        DID['terminology'],
        'ards_berlin',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The ARDS management chart shows stepwise escalation. "
        "After LPV fails to achieve P/F > _______, prone positioning (≥ 16h) is added. "
        "Neuromuscular blockade for 48h (ROSE trial) was found to be _______ compared to deep sedation alone. "
        "Refractory severe ARDS with P/F < _______ despite all optimization may require _______.",

        "ARDS management steps:\n"
        "| Step 1 (all ARDS): LPV — Vt 6 mL/kg IBW, Pplat ≤ 30, ΔP ≤ 15, optimize PEEP/FiO₂\n"
        "| Step 2 (moderate-severe): prone positioning if P/F < 150 (PROSEVA: NNT=6)\n"
        "| Step 3: NMBA 48h — ROSE trial (NEJM 2019): NO benefit over light sedation → no longer routine\n"
        "| Step 4 (refractory severe, P/F < 80, pH < 7.20): VV-ECMO consideration\n"
        "→ CCRN KEY: ROSE trial reversed earlier ACURASYS trial finding. "
        "ACURASYS (2010) suggested early NMBA improved 90-day survival → widely adopted. "
        "ROSE (2019, larger, adequate power): cisatracurium × 48h = no mortality benefit vs light sedation. "
        "Current guideline: early NMBA NOT routinely recommended for ARDS (reserve for severe dyssynchrony).\n"
        "→ MASTERY NOTE: VV-ECMO for ARDS criteria (EOLIA trial thresholds):\n"
        "• P/F < 50 for > 3h OR P/F < 80 for > 6h on optimized LPV + prone\n"
        "• pH < 7.25 + PaCO₂ > 60 for > 6h despite RR ≤ 35\n"
        "• EOLIA trial: 60-day mortality 35% ECMO vs 46% control (P=0.07 — crossed over 28% of controls). "
        "Expert consensus: VV-ECMO at experienced centers for salvageable patients with no contraindications.",

        'tier-high',
        _NM,
        DID['terminology'],
        'ards_berlin',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "On the ARDS mimics chart, cardiogenic pulmonary edema is distinguished from ARDS "
        "by PCWP > _______ mmHg or elevated _______. "
        "The mimic characterized by progressive hemoptysis + bilateral opacities + falling hemoglobin "
        "on serial BAL is _______, caused by _______ or coagulopathy.",

        "Cardiogenic pulmonary edema vs ARDS: PCWP > 18 mmHg = cardiogenic (hydrostatic)\n"
        "| Also: BNP/NT-proBNP elevated; echo showing ↓ EF, diastolic dysfunction, ↑ LVEDD\n"
        "| Response to diuresis (↑ PaO₂, ↓ CXR opacities) → cardiogenic, NOT ARDS\n"
        "| Progressive hemoptysis + bilateral opacities + falling Hgb on serial BAL = Diffuse Alveolar Hemorrhage (DAH)\n"
        "| DAH caused by: ANCA vasculitis (GPA/MPA), anti-GBM (Goodpasture), SLE, HSCT, coagulopathy\n"
        "| Treatment: high-dose steroids + treat underlying cause; plasma exchange for anti-GBM\n"
        "→ CCRN KEY: Berlin definition says 'not FULLY explained by HF' — allowing coexistence. "
        "If CXR pattern + clinical story fit cardiogenic edema, treat that first. "
        "If bilateral opacities persist despite diuresis and cardiac optimization → ARDS may coexist.\n"
        "→ MASTERY NOTE: TRALI (Transfusion-Related Acute Lung Injury) — ARDS mimic:\n"
        "• Bilateral opacities + hypoxemia within 6 hours of blood product transfusion\n"
        "• Mechanism: donor anti-HLA or anti-neutrophil antibodies activate recipient neutrophils\n"
        "• Non-cardiogenic (PCWP normal); treatment: supportive (LPV if mechanically ventilated)\n"
        "• Prevention: male-predominant plasma (female multiparous donors → HLA antibodies from pregnancy)\n"
        "• Distinguish from TACO (Transfusion-Associated Circulatory Overload): cardiogenic, responds to diuresis",

        'tier-critical',
        _NM,
        DID['terminology'],
        'ards_berlin',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ sepsis_definitions ═══════════════════════════════════════════════════
    (
        "The Sepsis-3 chart defines sepsis as life-threatening _______ from infection. "
        "Organ dysfunction is quantified by SOFA increase ≥ _______. "
        "Septic shock requires vasopressor maintaining MAP ≥ _______ AND lactate > _______ mmol/L "
        "despite adequate fluid resuscitation.",

        "Sepsis (Sepsis-3 definition, 2016 JAMA consensus):\n"
        "| Life-threatening organ dysfunction caused by a dysregulated host response to infection\n"
        "| Organ dysfunction: acute SOFA ≥ 2 from baseline (SOFA = 0 assumed if no prior dysfunction)\n"
        "| Hospital mortality > 10%\n"
        "| Septic shock = sepsis + vasopressor to maintain MAP ≥ 65 mmHg + lactate > 2 mmol/L\n"
        "| Septic shock hospital mortality > 40%\n"
        "→ CCRN KEY: Sepsis-3 eliminated SIRS criteria from the definition. "
        "SIRS (temp >38°C/<36°C, HR >90, RR >20, WBC >12K/<4K) has poor specificity "
        "(surgery, trauma, pancreatitis all cause SIRS without infection). "
        "Sepsis-3 focuses on ORGAN DYSFUNCTION (SOFA), not inflammatory response (SIRS). "
        "A patient can have infection without sepsis (bacteremia without organ dysfunction = not sepsis).\n"
        "→ MASTERY NOTE: Bacteremia ≠ sepsis. Sepsis ≠ septicemia (old term). "
        "The new sepsis vocabulary:\n"
        "• Infection: microbial invasion of normally sterile tissue\n"
        "• Bacteremia: bacteria in bloodstream (can be transient, asymptomatic)\n"
        "• Sepsis: infection + organ dysfunction (SOFA ≥ 2)\n"
        "• Septic shock: sepsis + vasopressor + lactate > 2 (the most severe form)\n"
        "'Septicemia' is obsolete — do not use on CCRN or in clinical documentation.",

        'tier-review',
        _NM,
        DID['terminology'],
        'sepsis_definitions',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the Hour-1 bundle chart, the _______ SSC components include: "
        "measure _______, obtain blood cultures before _______, "
        "give broad-spectrum _______ within 1 hour, administer _______ mL/kg crystalloid "
        "if hypotensive or lactate ≥ 4, and apply _______ to maintain MAP ≥ 65.",

        "SSC Hour-1 Bundle (2018 update) — 5 components:\n"
        "| 1. Measure lactate (repeat if initial > 2 mmol/L; goal: clearance ≥ 10% per 2h)\n"
        "| 2. Obtain ≥ 2 blood culture sets BEFORE antibiotics\n"
        "   (Do NOT delay antibiotics > 45 min waiting for cultures)\n"
        "| 3. Broad-spectrum antibiotics within 1 hour of sepsis/septic shock recognition\n"
        "| 4. Administer 30 mL/kg crystalloid if MAP < 65 or lactate ≥ 4 mmol/L\n"
        "| 5. Vasopressors (norepinephrine first) if MAP < 65 despite IVF\n"
        "→ CCRN KEY: Every hour of antibiotic delay in septic shock increases mortality by ~7%. "
        "The '1-hour' target is from sepsis recognition, not patient arrival. "
        "Cultures in 2 sets (ideally from 2 separate sites) → improves sensitivity for BSI detection. "
        "Blood cultures should NOT delay antibiotics — if culture-draw will take > 45 min, give abx first.\n"
        "→ MASTERY NOTE: 30 mL/kg IVF bundle requirement — controversy:\n"
        "• In cardiogenic shock or known severe HF: may cause pulmonary edema\n"
        "• Reassess after each 500 mL bolus using fluid responsiveness: PPV, IVC collapsibility, PLR\n"
        "• SMART trial: balanced crystalloid (LR) superior to NS in sepsis (↓ AKI, ↓ RRT need)\n"
        "• After initial resuscitation: restrictive strategy (CLASSIC/ROSE) → less fluid overload",

        'tier-high',
        _NM,
        DID['terminology'],
        'sepsis_definitions',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The source control chart shows optimal timing for septic shock source control "
        "is within _______ hours. "
        "For necrotizing fasciitis, the intervention is _______ and delay of even _______ hours "
        "significantly increases mortality. "
        "Infected central venous catheters are always removed immediately if the organism is _______.",

        "Source control optimal timing: within 6–12 hours of septic shock recognition\n"
        "| Necrotizing fasciitis: immediate surgical debridement — mortality doubles per hour of delay\n"
        "  (\"No imaging required\" if clinical diagnosis clear — OR directly from ED)\n"
        "| Infected IV device: remove immediately if S. aureus, Candida, or tunneled catheter infection\n"
        "→ CCRN KEY: Source Control by Pathology:\n"
        "• Intra-abdominal abscess: percutaneous drainage (IR) preferred if accessible\n"
        "• Biliary sepsis/cholangitis: ERCP with biliary drainage within 24h\n"
        "• Empyema: chest tube or VATS decortication\n"
        "• Urinary obstruction: Foley catheter ± ureteral stent/nephrostomy\n"
        "• Infected prosthesis (joint, valve): discussion with surgery (hardware removal vs suppression)\n"
        "→ MASTERY NOTE: CRBSI (Catheter-Related Bloodstream Infection) management:\n"
        "• Mandatory removal: S. aureus (high relapse risk), Candida (biofilm), "
        "tunneled catheter fungemia, septic thrombophlebitis\n"
        "• Possible salvage: coagulase-negative Staph in non-tunneled line → antibiotic lock therapy\n"
        "• If catheter removed: new access at DIFFERENT site (never over guidewire through infected line)\n"
        "• Blood cultures: peripheral AND from catheter simultaneously "
        "(differential time to positivity > 2h = catheter is source)",

        'tier-critical',
        _NM,
        DID['terminology'],
        'sepsis_definitions',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ icu_syndromes ════════════════════════════════════════════════════════
    (
        "The ICU syndromes chart shows ICU-acquired weakness (ICUAW) affects _______ % "
        "of patients with sepsis or ARDS on mechanical ventilation > 7 days. "
        "ICUAW is diagnosed by MRC sum score < _______ out of 60. "
        "The three ICUAW subtypes are _______, _______, and _______.",

        "ICUAW incidence: 25–50% of patients with sepsis/ARDS requiring prolonged MV\n"
        "| MRC sum score: 6 muscle groups × bilateral (wrist ext, elbow flex, shoulder abd, ankle dorsiflex, knee ext, hip flex) × 0–5 each\n"
        "| Diagnostic: MRC sum < 48 of 60 (or Medical Research Council < 4 in ≥ 2 bilateral groups)\n"
        "| Three subtypes: CIP (Critical Illness Polyneuropathy), CIM (Myopathy), CIPNM (combined)\n"
        "| CIP: EMG = axonal sensorimotor neuropathy | CIM: myopathic EMG + ↑ CK | CIPNM: both\n"
        "→ CCRN KEY: Risk factors for ICUAW (all modifiable or partially so):\n"
        "• Sepsis / SIRS (systemic inflammation injures nerve/muscle)\n"
        "• Prolonged immobility (disuse atrophy — 2–5% muscle loss per day in ICU)\n"
        "• Corticosteroids (especially > 400 mg hydrocortisone equivalent/day)\n"
        "• NMB agents (especially with concurrent steroids — steroid myopathy + NMB)\n"
        "• Hyperglycemia (neuropathic effect)\n"
        "→ MASTERY NOTE: ABCDEF bundle — the comprehensive ICU prevention strategy for ICUAW:\n"
        "A = Assess/prevent pain | B = Both SAT+SBT | C = Choice of analgesia-sedation\n"
        "D = Delirium monitoring | E = Early mobility and Exercise | F = Family engagement\n"
        "ICUAW independently predicts prolonged MV, ICU/hospital LOS, and 1-year mortality — "
        "it is not merely a complication; it is a preventable outcome.",

        'tier-review',
        _NM,
        DID['terminology'],
        'icu_syndromes',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the delirium chart, CAM-ICU is POSITIVE when Feature 1 (_______ onset or _______ course), "
        "Feature 2 (_______), AND either Feature 3 (_______) OR Feature 4 (_______) are ALL present. "
        "The most COMMON and most MISSED subtype is _______ delirium.",

        "CAM-ICU positive = Feature 1 AND Feature 2 AND (Feature 3 OR Feature 4):\n"
        "| Feature 1: ACUTE onset or FLUCTUATING course (mental status change from baseline)\n"
        "| Feature 2: INATTENTION (letter attention test: SAVEAHAART — squeeze on 'A'; < 8/10 = fail)\n"
        "| Feature 3: DISORGANIZED THINKING (4 yes/no questions + 3 commands: open fist/touch nose/count)\n"
        "| Feature 4: ALTERED LOC (RASS ≠ 0 — anything other than alert and calm)\n"
        "| Most common + most missed: HYPOACTIVE delirium (patient quiet, withdrawn, 'looks calm')\n"
        "→ CCRN KEY: Delirium subtypes and outcomes:\n"
        "• Hyperactive: agitated, pulls lines, climbing out of bed (~25%) — most noticed by nurses\n"
        "• Hypoactive: quiet, lethargic, withdrawn (~50%) — WORSE prognosis, longer MV, higher mortality\n"
        "• Mixed: alternates between both (~25%)\n"
        "Hyperactive delirium is NOT more dangerous — hypoactive has higher mortality.\n"
        "→ MASTERY NOTE: Non-pharmacologic delirium prevention (ABCDEF bundle — D component):\n"
        "• Environment: reduce noise at night, natural light cycles, keep family at bedside\n"
        "• Reorientation: clock/calendar, glasses/hearing aids in place, family photos\n"
        "• Mobility: out of bed within 72h of ICU admission if hemodynamically stable\n"
        "Pharmacologic prevention: haloperidol, quetiapine, dexmedetomidine — "
        "NO drug has Level I evidence for PREVENTION. Treat delirium when present, but prevention is non-pharmacologic.",

        'tier-high',
        _NM,
        DID['terminology'],
        'icu_syndromes',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The PICS chart shows Post-Intensive Care Syndrome affects _______ % of ICU survivors. "
        "The three impairment domains are _______, _______, and _______. "
        "The intervention shown to reduce PTSD risk by up to 60% in some trials is _______.",

        "PICS affects: 25–50% of ICU survivors (varies by population and follow-up duration)\n"
        "| Three PICS domains:\n"
        "  1. Cognitive: memory, attention, executive function deficits (similar to mild TBI)\n"
        "  2. Physical: ICUAW, fatigue, dyspnea, dysphagia, functional disability\n"
        "  3. Mental health: PTSD (25%), depression (30%), anxiety (up to 70%)\n"
        "| ICU diary: patient/family written record of events → reduces PTSD risk (up to 60% in trials)\n"
        "→ CCRN KEY: PICS is not just about ICU events — it extends months to years post-discharge. "
        "Survivors often cannot return to work at 1 year. "
        "Cognitive impairment may persist 5+ years after ARDS (Hopkins et al., NEJM 1999). "
        "Prevention inside the ICU = prevention of PICS outside the ICU — they are the same bundle.\n"
        "→ MASTERY NOTE: PICS-Family (PICS-F):\n"
        "• 30% of family members develop PTSD, complicated grief, or depression after ICU\n"
        "• Risk factors: unexpected admission, family present at death, perceived poor communication\n"
        "• Protective: structured family meetings, proactive communication, bereavement rounds\n"
        "• ICU Diary benefits BOTH patient AND family (reduces PTSD in both groups)\n"
        "Survivor clinic programs (multi-disciplinary: medicine, psychology, PT/OT, pharmacy) "
        "provide systematic post-ICU follow-up at 1, 3, and 6 months — "
        "addressing all three PICS domains and providing PICS-F support.",

        'tier-critical',
        _NM,
        DID['terminology'],
        'icu_syndromes',
        '{"sel":2}',
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
