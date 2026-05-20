#!/usr/bin/env python3
"""chunk55_charts.py — Ph7 Pharmacology: Patient Models (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_54.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_55.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c55')
CHUNK_NUM   = 55
MID_BASE    = 1_800_005_120
CHART_ORDER = ['aki_drug_adjust', 'chf_pharmacology', 'sepsis_patient_pharm',
               'liver_failure_drugs', 'elderly_frail_icu']

_NM = 'Ph7 \U0001f7e1 T3 · Pharmacology — Patient Models'

RF = {}

# ── Chart 1: AKI Drug Adjustment ──────────────────────────────────────────────
RF['aki_drug_adjust'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var rows=[
        {n:'Vancomycin', prob:'Accumulates (renal\nclearance 95%)\nTrough rises rapidly',
         act:'AUC-guided dosing\n(Bayesian PK model)\nExtend interval',
         mon:'AUC/MIC target:\n400–600 mg·h/L\nSCr every 48–72h',
         note:'Avoid trough-only monitoring — AUC/MIC superior (2020 ASHP/SIDP guideline)\nVanco+PIPC-TAZO synergistic nephrotoxicity: switch to meropenem + vanco\nDialysis: supplement dose after each HD session; check post-dialysis level',
         c:'#cc4444'},
        {n:'Enoxaparin', prob:'Accumulates (renal\nclearance >90%)\nAnti-Xa rises',
         act:'CONTRAINDICATED\nCrCl <30 mL/min\nSwitch to UFH',
         mon:'Anti-Xa 4h post-dose\nif used (0.5–1.0 IU/mL)\nUFH: aPTT 60–100s',
         note:'UFH does NOT require renal dose adjustment — hepatic clearance predominates\nHD patients: use UFH for VTE prophylaxis (5000 units SC q8-12h)\nIf enoxaparin must be used: anti-Xa monitoring; never dose-adjust by CrCl alone',
         c:'#cc8844'},
        {n:'Pip-Tazo\n(+Vancomycin)', prob:'Inhibits tubular\nvanco secretion\n↑ vanco AUC',
         act:'Switch pip-tazo\nto meropenem\nwhen MRSA coverage',
         mon:'Vanco AUC spikes\nSCr rising >\n0.5 mg/dL over 24h',
         note:'PIPC/TAZO+vanco: CANWARD/Blumenthal data — 3–5× higher AKI vs meropenem+vanco\nCAUTION: even 24h of combo can precipitate AKI in ICU patients\nMeropenem has no such interaction; cefepime+vanco also lower AKI risk',
         c:'#4488cc'},
        {n:'Metformin', prob:'Accumulates in AKI\n→ lactic acidosis\n(type B, class effect)',
         act:'HOLD: eGFR <30\nDO NOT restart\nuntil renal recovery',
         mon:'Lactate if given\naccidentally; eGFR\nbefore restart',
         note:'Metformin-associated lactic acidosis (MALA): mortality 30–50% — rare but serious\nHold perioperatively and with contrast administration (eGFR <60 risk)\nSafe to restart 48h after procedure when eGFR confirmed stable and >45',
         c:'#3a9a5c'},
        {n:'Gabapentin\nPregabalin', prob:'Renally cleared\n(100% unchanged)\nNeurotoxicity',
         act:'Dose reduce by\n50–75% in AKI\nCrCl-based dosing',
         mon:'Signs of toxicity:\ndrowsiness, ataxia,\nmyoclonus, seizures',
         note:'Gabapentin HD: supplement 100–300 mg after each dialysis session\nGabapentin toxicity in AKI: encephalopathy, myoclonus, respiratory depression\nBoth gabapentin and pregabalin require similar CrCl-based dose reduction tables',
         c:'#9060c0'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/rows.length);
    var xs=[4,90,175,255,355,616];
    ctx.fillStyle='#1a2a1a';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Drug','AKI Problem','Action','Monitor','ICU Notes'];
    ctx.font='bold 7.5px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    rows.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d180d':'#111811';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=d.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=d.c;ctx.font='bold 7px sans-serif';ctx.textAlign='left';
        d.n.split('\n').forEach(function(l,li){ctx.fillText(l,xs[0]+2,ry+rh/2-4+li*9);});
        ctx.fillStyle='#ff9966';ctx.font='6px sans-serif';
        d.prob.split('\n').forEach(function(l,li){ctx.fillText(l,xs[1]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#aaddaa';ctx.font='6px sans-serif';
        d.act.split('\n').forEach(function(l,li){ctx.fillText(l,xs[2]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#eedd88';ctx.font='6px sans-serif';
        d.mon.split('\n').forEach(function(l,li){ctx.fillText(l,xs[3]+2,ry+rh/2-9+li*9);});
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
        var lbs=['Vancomycin','Enoxaparin','Pip-Tazo','Metformin','Gabapentin'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,rows[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: CHF Pharmacology ─────────────────────────────────────────────────
RF['chf_pharmacology'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['HFrEF Pillars','Acute Decompensation','Drugs to Avoid'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#0a1020':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#1a2a3a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#4488cc':'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#050810';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+12;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#4488cc';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8px sans-serif';ctx.fillText(val,lm+185,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#1a2a3a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('HFrEF Four Pillars — ALL reduce mortality (use unless contraindicated):','','#4488cc');
        hr();
        rw('ARNI:','Sacubitril/valsartan — neprilysin inhibitor + ARB; PARADIGM-HF: 20% ↓ CVD mortality','#eedd88','#99bbdd');
        nt('Sacubitril blocks BNP/ANP breakdown → natriuresis; wash out ACEi 36h before starting');
        rw('β-blocker:','Carvedilol (α1+β1+β2) / Metoprolol succinate (β1) / Bisoprolol — START LOW GO SLOW','#eedd88','#99bbdd');
        nt('Contraindicated in decompensated HF, HR <60, SBP <90; titrate to HR 55–65 bpm');
        rw('MRA:','Spironolactone/eplerenone — K⁺-sparing; RALES/EMPHASIS: ↓ mortality ~25%','#eedd88','#99bbdd');
        nt('Avoid if K⁺ >5.0 or eGFR <30; watch for hyperkalemia + gynecomastia (spironolactone)');
        rw('SGLT2i:','Dapagliflozin/empagliflozin — DAPA-HF/EMPEROR-R: ↓ HF hospitalization+CVD death','#eedd88','#99bbdd');
        nt('Benefit independent of diabetic status; hold periop; watch for UTI/DKA (euglycemic)');
    } else if(sel===1){
        rw('Acute Decompensated HF (ADHF) — Decongestion + Perfusion:','','#4488cc');
        hr();
        rw('Diuresis:','IV furosemide — DOSE trial: 2.5× oral dose IV; high-dose strategy superior','#eedd88','#99bbdd');
        nt('DOSE Trial: 2.5× oral dose in mg IV push q12h = better diuresis, no extra AKI risk');
        nt('Resistance: add metolazone 2.5–5 mg PO 30min before furosemide (sequential nephron block)');
        hr();
        rw('Vasodilators:','NTG IV: ↓ preload (PCWP); SNP: ↓ pre+afterload (MAP-guided); avoid if SBP <90','#eedd88','#99bbdd');
        nt('Nesiritide (BNP): vasodilation + natriuresis; no mortality benefit (ASCEND-HF trial)');
        hr();
        rw('Inotropes:','Dobutamine (β1): ↑ CI, ↓ SVR; Milrinone (PDE3i): ↑ CI, ↓ PVR — preferred in BB use','#eedd88','#99bbdd');
        nt('Milrinone preferred when patient on β-blocker (PDE3i bypasses β-receptor blockade)');
        nt('Inotropes bridge to transplant/VAD or palliative; ↑ arrhythmia risk — use shortest duration');
    } else {
        rw('Drugs to Avoid in Heart Failure — Worsen Hemodynamics or Cause HF:','','#cc4444');
        hr();
        rw('NSAIDs / COX-2:','↑ Na retention, ↑ SVR, ↓ diuretic response, ↑ ACS/HF hospitalization risk','#cc4444','#ffaa99');
        nt('Even one dose of ibuprofen can precipitate ADHF — use acetaminophen for pain in HF');
        rw('Verapamil / Diltiazem:','Negative inotropes — worsen HFrEF systolic function; acceptable in HFpEF','#cc4444','#ffaa99');
        nt('CCBs in HFrEF (EF <40%): PRAISE-2 showed amlodipine neutral; only DHP-CCBs acceptable');
        hr();
        rw('Thiazolidinediones:','Rosiglitazone/pioglitazone → fluid retention, ↑ HF hospitalization; CONTRAINDICATED','#cc4444','#ffaa99');
        rw('Dronedarone:','↑ HF mortality in ANDROMEDA trial; CONTRAINDICATED in EF <35% or NYHA III-IV','#cc4444','#ffaa99');
        hr();
        rw('Metformin:','Historically avoided (lactic acidosis risk) — NOW SAFE in compensated HF if eGFR >30','#cc9922','#eecc88');
        nt('HOLD metformin in ADHF (↓ renal perfusion) and with IV contrast; restart when stable');
    }
    if(ctrl){
        ctrl.innerHTML='';
        var crow=document.createElement('div');crow.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        ['HFrEF Pillars','Acute Decomp','Avoid'].forEach(function(lb,i){
            var b=_mkB(lb,'#4488cc',sel===i,function(on){
                var p2={sel:on?i:0};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
            });crow.appendChild(b);
        });
        ctrl.appendChild(crow);
    }
}
"""

# ── Chart 3: Sepsis Patient Pharmacology ──────────────────────────────────────
RF['sepsis_patient_pharm'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Hour-1 Bundle','Corticosteroids','Antibiotic PK/PD'];
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
        rw('SSC Hour-1 Bundle (2018) — ALL 5 Elements Within 1 Hour of Recognition:','','#cc4444');
        hr();
        rw('1. Lactate:','Measure — if >2 mmol/L → remeasure within 2h; >4 mmol/L = high-risk','#eedd88','#99bbdd');
        rw('2. Blood Cx:','Obtain ≥2 sets (aerobic+anaerobic) BEFORE antibiotics if <45 min delay','#eedd88','#99bbdd');
        nt('Do NOT delay antibiotics >45 min waiting for blood cultures — mortality ↑ per hour');
        rw('3. Antibiotics:','Broad-spectrum IV within 1 hour — tailor to source (anti-MRSA if skin/SSTI)','#eedd88','#99bbdd');
        nt('De-escalate by 48–72h when culture data available — stewardship reduces resistance');
        rw('4. IVF:','30 mL/kg crystalloid (NS or LR) IV bolus if hypotension OR lactate ≥4 mmol/L','#eedd88','#99bbdd');
        nt('SMART trial: LR/PlasmaLyte preferred over NS (lower hyperchloremic acidosis + AKI risk)');
        rw('5. Vasopressors:','Norepinephrine if MAP <65 after fluid — target MAP ≥65 mmHg','#eedd88','#99bbdd');
        nt('Can start norepinephrine via peripheral IV while CVC placed (do not delay for CVC access)');
    } else if(sel===1){
        rw('Corticosteroids in Septic Shock — When and How:','','#cc4444');
        hr();
        rw('Indication:','MAP <65 despite norepi ≥0.25 mcg/kg/min — OR vasopressor-dependent >4h','#eedd88','#99bbdd');
        nt('APROCCHSS (2018) and ADRENAL (2018) trials: hydrocortisone ↓ vasopressor duration but');
        nt('no consistent mortality benefit — reduces shock duration (ICU days and vasopressor need)');
        hr();
        rw('Dose:','Hydrocortisone 200 mg/day IV continuous OR 50 mg IV q6h','#cc9922','#eecc88');
        nt('AVOID fludrocortisone (APROCCHSS used it — no clear additive benefit per ADRENAL)');
        rw('Duration:','Taper over 5–7 days when vasopressors weaned — do NOT abrupt discontinue','#cc9922','#eecc88');
        hr();
        rw('Cosyntropin stim test:','NO longer recommended to guide steroid use (CORTICUS trial)','#cc4444','#ffaa99');
        rw('ARDS + Sepsis:','Methylprednisolone 1 mg/kg/day (early diffuse ARDS <14 days — DEXA-ARDS)','#cc9922','#eecc88');
        nt('Dexamethasone 20 mg/day × 5d then 10 mg/day × 5d: mortality benefit in moderate-severe ARDS');
    } else {
        rw('Antibiotic PK/PD Targets — Optimize Pharmacodynamic Efficacy:','','#cc4444');
        hr();
        rw('β-Lactams (%T>MIC):','Time-dependent killing — need ≥40–70% of dosing interval above MIC','#3a9a5c','#99ddaa');
        nt('Extended infusion (3–4h) or continuous infusion achieves higher %T>MIC than q4-6h bolus');
        nt('Standard bolus β-lactam achieves ~50% T>MIC; extended infusion achieves >90% T>MIC');
        hr();
        rw('Vancomycin (AUC/MIC):','AUC/MIC 400–600 mg·h/L — use Bayesian PK modeling','#4488cc','#99bbdd');
        nt('AUC/MIC-based dosing superior to trough-only (↓ nephrotoxicity, ↑ clinical success)');
        rw('Aminoglycosides (Cmax/MIC):','Concentration-dependent — peak/MIC ≥10 for bactericidal effect','#4488cc','#99bbdd');
        nt('Extended-interval dosing (EID) 5–7 mg/kg q24h: maximizes Cmax/MIC + long PAE + ↓ nephrotox');
        hr();
        rw('PK/PD in Sepsis — Volume Changes:','↑ Vd (resuscitation) → sub-therapeutic levels early in sepsis','#cc9922','#eecc88');
        nt('GIVE LOADING DOSES in sepsis — Vd expanded; renal hyperfiltration can ↑ drug clearance');
        nt('Monitor renally-cleared drugs closely: early AUC may be sub-therapeutic due to ↑ GFR');
    }
    if(ctrl){
        ctrl.innerHTML='';
        var crow=document.createElement('div');crow.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        ['Hour-1 Bundle','Corticosteroids','PK/PD'].forEach(function(lb,i){
            var b=_mkB(lb,'#cc4444',sel===i,function(on){
                var p2={sel:on?i:0};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
            });crow.appendChild(b);
        });
        ctrl.appendChild(crow);
    }
}
"""

# ── Chart 4: Liver Failure Drugs ──────────────────────────────────────────────
RF['liver_failure_drugs'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var rows=[
        {n:'Acetami-\nnophen', prob:'Hepatotoxic in\ndecompensated\ncirrhosis',
         adj:'2 g/day MAX\n(compensated)\nAVOID decomp',
         risk:'N-acetyl-p-benzo-\nquinone imine\n(NAPQI) accumulates',
         note:'PREFERRED over NSAIDs in cirrhosis — NSAIDs risk HRS + GI bleed\nStandard doses safe in compensated cirrhosis; 2 g/day limit is conservative but safe\nNAC antidote: N-acetylcysteine IV if APAP overdose (nomogram-guided)',
         c:'#cc8844'},
        {n:'NSAIDs', prob:'↓ Renal PGs\n→ HRS risk\n↑ GI bleed',
         adj:'AVOID in ALL\ncirrhosis patients\n(compensated too)',
         risk:'Hepatorenal\nsyndrome type 1\nvariceal bleed risk',
         note:'NSAIDs contraindicated in cirrhosis regardless of severity — HRS risk with single dose\nCOX-2 prostaglandins maintain afferent arteriole tone in cirrhotic renal vasoconstriction\nAlternative: acetaminophen ≤2 g/day, or opioids (titrated carefully)',
         c:'#cc4444'},
        {n:'Benzo-\ndiazepines', prob:'↓ CYP450\noxidative metab\nActive metabolites',
         adj:'Use lorazepam\nor oxazepam\n(glucuronidation)',
         risk:'Encephalopathy\nRespiratory\ndepression',
         note:'LORAZEPAM preferred in hepatic failure: direct glucuronidation — no active metabolites\nOXAZEPAM also safe (same reason) — avoid diazepam, midazolam (oxidative pathway)\nCIWA protocol in cirrhosis: use lorazepam; adjust CIWA-Ar threshold more conservatively',
         c:'#9060c0'},
        {n:'Opioids', prob:'↑ Bioavailability\n(↓ first pass)\n↑ t½ in cirrhosis',
         adj:'Start 50% dose\nLonger intervals\nFentanyl preferred',
         risk:'HE precipitation\nRespiratory\ndepression',
         note:'FENTANYL preferred: shortest acting, no active metabolites, predictable in liver disease\nMORPHINE: morphine-6-glucuronide active metabolite accumulates — avoid in cirrhosis\nCODEINE: prodrug requires CYP2D6 for activation — unpredictable in cirrhosis; avoid',
         c:'#4488cc'},
        {n:'Hepatotoxic\nAntibiotics', prob:'Direct hepato-\ntoxicity or\ncholestasis risk',
         adj:'Avoid when\nalternatives exist\nMonitor LFTs',
         risk:'Drug-induced\nliver injury (DILI)\nCholestasis',
         note:'AMOXICILLIN-CLAVULANATE: most common cause antibiotic DILI — avoid in cirrhosis\nISONIAZID: avoid or use with B6 + monthly LFT monitoring in active cirrhosis\nFLUCONAZOLE: hepatotoxic at high doses; monitor LFTs; reduce dose in severe hepatic failure',
         c:'#3a9a5c'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/rows.length);
    var xs=[4,100,185,265,355,616];
    ctx.fillStyle='#1a1a0a';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Drug','Effect in Failure','Dose Adjust','Risk','ICU Notes'];
    ctx.font='bold 7.5px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    rows.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#100d00':'#181400';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=d.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=d.c;ctx.font='bold 7px sans-serif';ctx.textAlign='left';
        d.n.split('\n').forEach(function(l,li){ctx.fillText(l,xs[0]+2,ry+rh/2-4+li*9);});
        ctx.fillStyle='#ff9966';ctx.font='6px sans-serif';
        d.prob.split('\n').forEach(function(l,li){ctx.fillText(l,xs[1]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#aaddaa';ctx.font='6px sans-serif';
        d.adj.split('\n').forEach(function(l,li){ctx.fillText(l,xs[2]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#ee8888';ctx.font='6px sans-serif';
        d.risk.split('\n').forEach(function(l,li){ctx.fillText(l,xs[3]+2,ry+rh/2-9+li*9);});
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
        var lbs=['APAP','NSAIDs','Benzos','Opioids','Hepatotox Abx'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,rows[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 5: Elderly/Frail ICU Pharmacology ───────────────────────────────────
RF['elderly_frail_icu'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Altered PK in Elderly','High-Risk Drugs (Beers)','Polypharmacy Mgmt'];
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
        rw('Pharmacokinetic Changes in Elderly ICU Patients (age >65):','','#9060c0');
        hr();
        rw('↓ GFR / CrCl:','Use Cockcroft-Gault (actual BW if cachectic) — SCr may be falsely normal','#eedd88','#99bbdd');
        nt('Elderly may have CrCl <30 mL/min with SCr 0.8 (low muscle mass = low creatinine generation)');
        nt('At-risk renally-cleared drugs: vancomycin, enoxaparin, digoxin, gabapentin, direct oral ACs');
        hr();
        rw('↓ Albumin:','↑ Free drug fraction — phenytoin (use free level 1–2 mg/L), warfarin (↑ sensitivity)','#eedd88','#99bbdd');
        nt('Critically ill elderly: albumin <2 g/dL common — all highly protein-bound drugs affected');
        hr();
        rw('↑ Vd (lipophilic drugs):','Benzodiazepines, opioids accumulate in adipose — prolonged effect','#eedd88','#99bbdd');
        nt('Fentanyl: context-sensitive t½ extends dramatically with prolonged infusion in elderly');
        hr();
        rw('↓ Hepatic first-pass:','↑ bioavailability of oral drugs; ↓ CYP450 activity → accumulation','#eedd88','#99bbdd');
        nt('Phase I (oxidation) reduced more than Phase II (glucuronidation) with aging — practical: prefer');
        nt('lorazepam/oxazepam (glucuronidation) over diazepam/midazolam (CYP450 oxidation) in elderly');
    } else if(sel===1){
        rw('High-Risk Drugs in Elderly ICU — American Geriatrics Society Beers Criteria:','','#9060c0');
        hr();
        rw('Benzodiazepines:','3× ↑ falls and hip fracture risk; ↑ delirium; prolonged t½ — AVOID in ICU','#cc4444','#ffaa99');
        nt('Use dexmedetomidine instead (MENDS trial: ↓ delirium, cooperative sedation)');
        nt('If benzo withdrawal (CIWA): use lorazepam or oxazepam — avoid diazepam (long t½ = accumulation)');
        hr();
        rw('Diphenhydramine:','Strong anticholinergic — confusion, urinary retention, constipation','#cc4444','#ffaa99');
        nt('Common in OTC sleep aids, PM formulations, antiemetics — reconcile home meds on admission');
        rw('Meperidine:','Normeperidine metabolite → seizures + CNS toxicity in elderly; AVOID','#cc4444','#ffaa99');
        rw('First-gen antihistamines:','Hydroxyzine, promethazine — anticholinergic delirium risk; prefer ondansetron','#cc4444','#ffaa99');
        hr();
        rw('Sliding scale insulin:','High hypoglycemia risk — use basal-bolus + glucose monitoring protocol','#cc9922','#eecc88');
        nt('Target glucose 140–180 mg/dL in ICU (NICE-SUGAR trial); tight control ↑ hypoglycemia + mortality');
    } else {
        rw('Polypharmacy Management in Elderly ICU — Reconciliation + Deprescribing:','','#9060c0');
        hr();
        rw('Admission Reconciliation:','Obtain complete med list (caregiver + pharmacy) — ≥5 meds = high risk','#eedd88','#99bbdd');
        nt('High-alert drugs requiring reconciliation: anticoagulants, insulin, vasopressors, immunosuppressants');
        nt('Verify ALL doses against weight + renal function on admission — do not assume outpatient dose is correct');
        hr();
        rw('Deprescribing in ICU:','Stop preventive meds without acute benefit (statins, vitamins, osteoporosis Rx)','#eedd88','#99bbdd');
        nt('Statins: STOP during acute critical illness (myopathy risk; rhabdo with NMBAs) — restart when stable');
        nt('Proton pump inhibitors: CONTINUE if on mechanical ventilation (stress ulcer prophylaxis SUP)');
        hr();
        rw('Drug-Drug Interactions:','QTc-prolonging drug combinations most dangerous in elderly','#cc4444','#ffaa99');
        nt('QTc >500 ms: stop offending agents (azithromycin + haloperidol + methadone + ondansetron)');
        rw('Discharge planning:','Medication reconciliation at discharge — simplify regimen, avoid adding new meds','#9060c0','#ccaadd');
        nt('STOPP/START criteria: evidence-based tool for potentially inappropriate medications in older adults');
    }
    if(ctrl){
        ctrl.innerHTML='';
        var crow=document.createElement('div');crow.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        ['Altered PK','Beers Criteria','Polypharmacy'].forEach(function(lb,i){
            var b=_mkB(lb,'#9060c0',sel===i,function(on){
                var p2={sel:on?i:0};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
            });crow.appendChild(b);
        });
        ctrl.appendChild(crow);
    }
}
"""

# ── Cards ──────────────────────────────────────────────────────────────────────
_D = DID['patient_models']
CARDS = [
    # aki_drug_adjust — L1 recognition / L2 mechanism / L3 clinical application
    ('On the AKI drug adjustment chart, vancomycin in AKI requires _______ monitoring and should target AUC/MIC of _______.',
     'therapeutic drug monitoring (TDM) with Bayesian PK modeling → target AUC/MIC 400–600 mg·h/L (not trough-only — 2020 ASHP/SIDP guideline)',
     'tier-review', _NM, _D, 'aki_drug_adjust', '{}', 'chart-l1'),
    ('The AKI drug chart shows enoxaparin is _______ when CrCl <30 mL/min; the preferred alternative is _______.',
     'contraindicated (accumulates due to renal clearance >90%) → preferred alternative: unfractionated heparin (UFH) — renally independent clearance',
     'tier-high', _NM, _D, 'aki_drug_adjust', '{}', 'chart-l2'),
    ('On the AKI drug chart, piperacillin-tazobactam + vancomycin carries _______ nephrotoxicity risk compared to meropenem + vancomycin.',
     'synergistic nephrotoxicity (3–5× higher AKI rate) → PIPC/TAZO inhibits tubular vancomycin secretion, ↑ AUC; prefer meropenem when MRSA coverage needed',
     'tier-critical', _NM, _D, 'aki_drug_adjust', '{}', 'chart-l3'),

    # chf_pharmacology — L1 recognition / L2 mechanism / L3 clinical application
    ('The CHF pharmacology chart shows the four mortality-reducing pillars for HFrEF are _______, _______, _______, and _______.',
     'ARNI (sacubitril/valsartan) → β-blocker (carvedilol/metoprolol succinate/bisoprolol) → MRA (spironolactone/eplerenone) → SGLT2i (dapagliflozin/empagliflozin)',
     'tier-review', _NM, _D, 'chf_pharmacology', '{}', 'chart-l1'),
    ('On the acute decompensated HF chart, the DOSE trial showed the high-dose furosemide strategy results in _______ without increasing _______.',
     'greater diuresis and symptom relief (better decongestion) → without increasing rates of worsening renal function compared to low-dose strategy',
     'tier-high', _NM, _D, 'chf_pharmacology', '{}', 'chart-l2'),
    ('The CHF drugs-to-avoid chart shows NSAIDs worsen heart failure through _______ and directly opposing the goal of _______.',
     'sodium and fluid retention (↓ renal prostaglandins → ↑ ADH effect) + vasoconstriction (↑ SVR/afterload) → opposing goal of decongestion and afterload reduction',
     'tier-critical', _NM, _D, 'chf_pharmacology', '{}', 'chart-l3'),

    # sepsis_patient_pharm — L1 recognition / L2 mechanism / L3 clinical application
    ('The sepsis bundle chart shows broad-spectrum IV antibiotics must be administered within _______ of septic shock recognition per the SSC Hour-1 Bundle.',
     '1 hour → blood cultures first (if <45 min delay); do NOT delay antibiotics waiting for cultures in high-acuity septic shock — mortality ↑ per hour of delay',
     'tier-review', _NM, _D, 'sepsis_patient_pharm', '{}', 'chart-l1'),
    ('On the sepsis corticosteroid chart, IV hydrocortisone is recommended when MAP remains <65 mmHg despite norepinephrine ≥_______ mcg/kg/min.',
     '0.25 mcg/kg/min (or vasopressor-dependent >4h) → hydrocortisone 200 mg/day IV continuous or 50 mg q6h — reduces vasopressor duration (APROCCHSS, ADRENAL trials)',
     'tier-high', _NM, _D, 'sepsis_patient_pharm', '{}', 'chart-l2'),
    ('The antibiotic PK/PD chart shows β-lactam bactericidal efficacy depends on _______, optimized by _______.',
     '%T>MIC (time free drug exceeds MIC — target >40–70%) → optimized by extended infusion (3–4h) or continuous infusion; standard bolus achieves ~50% T>MIC vs >90% with extended',
     'tier-critical', _NM, _D, 'sepsis_patient_pharm', '{}', 'chart-l3'),

    # liver_failure_drugs — L1 recognition / L2 mechanism / L3 clinical application
    ('The liver failure drug chart shows acetaminophen is _______ in compensated cirrhosis, with a maximum safe dose of _______.',
     'not absolutely contraindicated (preferred over NSAIDs) → 2 g/day maximum; avoid in decompensated cirrhosis, active alcohol use, or acute hepatic failure',
     'tier-review', _NM, _D, 'liver_failure_drugs', '{}', 'chart-l1'),
    ('On the hepatic drug chart, benzodiazepines in liver failure cause _______ because _______ metabolism is impaired; the preferred alternative is _______.',
     'prolonged sedation and hepatic encephalopathy → CYP450 oxidative metabolism is impaired → preferred: lorazepam or oxazepam (direct glucuronidation — no active metabolites)',
     'tier-high', _NM, _D, 'liver_failure_drugs', '{}', 'chart-l2'),
    ('The liver failure drug chart shows opioids require dose reduction in cirrhosis because _______ is reduced; _______ is preferred due to _______.',
     'first-pass hepatic metabolism (↑ bioavailability, prolonged t½) → fentanyl preferred due to short action and no active metabolites (avoid morphine — M6G accumulates)',
     'tier-critical', _NM, _D, 'liver_failure_drugs', '{}', 'chart-l3'),

    # elderly_frail_icu — L1 recognition / L2 mechanism / L3 clinical application
    ('The elderly ICU pharmacokinetics chart shows ↓ albumin increases _______ drug fraction, raising toxicity risk for _______ and _______.',
     'free (unbound) drug fraction → phenytoin toxicity (use free level 1–2 mg/L, not total) → warfarin increased anticoagulant effect at standard doses',
     'tier-review', _NM, _D, 'elderly_frail_icu', '{}', 'chart-l1'),
    ('On the Beers Criteria chart, benzodiazepines in elderly ICU patients triple the risk of _______ and increase _______, making _______ the preferred alternative.',
     'falls and hip fractures → delirium (hypoactive and hyperactive) → dexmedetomidine preferred (cooperative sedation, arousable, ↓ delirium — MENDS trial)',
     'tier-high', _NM, _D, 'elderly_frail_icu', '{}', 'chart-l2'),
    ('The polypharmacy chart shows medication reconciliation at ICU admission must identify _______ drug combinations and stop _______ during acute critical illness.',
     'high-alert interactions (anticoagulants/insulin/QTc-prolonging combinations) → stop preventive medications without acute benefit (statins, vitamins, osteoporosis drugs)',
     'tier-critical', _NM, _D, 'elderly_frail_icu', '{}', 'chart-l3'),
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
