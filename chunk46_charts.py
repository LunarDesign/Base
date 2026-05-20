#!/usr/bin/env python3
"""chunk46_charts.py — Ph7 Diuretics (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_45.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_46.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c46')
CHUNK_NUM   = 46
MID_BASE    = 1_800_005_075
CHART_ORDER = ['diuretic_comparison', 'loop_diuretic_protocol', 'diuretic_electrolytes',
               'acute_decompensated_hf', 'mannitol_hypertonic']

_NM = 'Ph7 · \U0001f7e1 T3 · Pharmacology — Diuretics'

RF = {}

# ── Chart 1: Diuretic Class Comparison ────────────────────────────────────────
RF['diuretic_comparison'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var drugs=[
        {name:'Loop Diuretics\n(Furosemide/Torsemide)',mech:'Inhibit Na-K-2Cl\ncotransporter (NKCC2)',site:'Thick ascending\nlimb (TAL)',pot:'HIGH\n(ceiling effect)',use:'ADHF, pulmonary edema\nAKI-associated fluid OL',elec:'↓K⁺ ↓Mg²⁺ ↓Ca²⁺\nMetabolic alkalosis',c:'#4488cc'},
        {name:'Thiazides\n(HCTZ/Chlorthalidone)',mech:'Inhibit NaCl\ncotransporter (NCC)',site:'Distal convoluted\ntubule (DCT)',pot:'MODERATE\n(low ceiling)',use:'HTN (outpatient)\nLoop adjunct (DM2)',elec:'↓K⁺ ↓Na⁺ ↓Mg²⁺\n↑Ca²⁺ (retention)',c:'#3a9a5c'},
        {name:'Metolazone\n(Zaroxolyn)',mech:'NCC inhibitor (DCT)\n+ proximal tubule',site:'DCT + proximal\ntubule (dual)',pot:'POTENT thiazide-like\n(unique proximal action)',use:'Sequential blockade\nwith loop (resistance)',elec:'Profound ↓K⁺ ↓Mg²⁺\n↓Na⁺ (monitor closely)',c:'#38b2a4'},
        {name:'Aldosterone Antagonist\n(Spironolactone/Eplerenone)',mech:'Block aldosterone\nreceptor in collecting duct',site:'Collecting duct\n(cortical)',pot:'WEAK diuretic\n(strong K-sparing)',use:'HFrEF (RALES: ↓mort)\nCirrhosis/ascites',elec:'↑K⁺ (hyperkalemia)\n↑Na⁺ (antikaliuresis)',c:'#e07020'},
        {name:'Acetazolamide\n(Diamox)',mech:'Inhibit carbonic\nanhydrase (CA)',site:'Proximal convoluted\ntubule (PCT)',pot:'WEAK diuretic\n(bicarb wasting)',use:'Metabolic alkalosis Rx\nGlaucoma; AMS/altitude',elec:'↓HCO₃⁻ (acidosis)\nHyperchloremic NAGMA',c:'#9060c0'},
        {name:'Mannitol\n(Osmitrol)',mech:'Osmotic diuresis\n(filtered, not reabsorbed)',site:'Entire nephron\n(proximal + TAL + CD)',pot:'MODERATE diuresis\n(osmotic driver)',use:'ICP reduction, cerebral\nedema; rhabdomyolysis',elec:'↓Na⁺ (dilutional)\n↑Serum osmolality',c:'#cc6633'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/drugs.length);
    var xs=[4,110,228,292,362,476,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Drug/Class','Mechanism','Site','Potency','ICU Use','Electrolyte Effect'];
    ctx.font='bold 8px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    drugs.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=d.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=d.c;ctx.font='bold 8px sans-serif';ctx.textAlign='left';
        d.name.split('\n').forEach(function(nl,ni){ctx.fillText(nl,xs[0]+3,ry+rh/2-4+ni*10);});
        ctx.fillStyle='#aab';ctx.font='7.5px sans-serif';
        d.mech.split('\n').forEach(function(ml,mi){ctx.fillText(ml,xs[1]+3,ry+rh/2-3+mi*9);});
        ctx.fillStyle='#88aabb';ctx.font='7.5px sans-serif';
        d.site.split('\n').forEach(function(sl,si){ctx.fillText(sl,xs[2]+3,ry+rh/2-3+si*9);});
        ctx.fillStyle='#ccaa88';ctx.font='7.5px sans-serif';
        d.pot.split('\n').forEach(function(pl,pi){ctx.fillText(pl,xs[3]+3,ry+rh/2-3+pi*9);});
        ctx.fillStyle='#9ab8aa';ctx.font='7.5px sans-serif';
        d.use.split('\n').forEach(function(ul,ui){ctx.fillText(ul,xs[4]+3,ry+rh/2-3+ui*9);});
        ctx.fillStyle='#cc9988';ctx.font='7.5px sans-serif';
        d.elec.split('\n').forEach(function(el,ei){ctx.fillText(el,xs[5]+3,ry+rh/2-3+ei*9);});
        ctx.globalAlpha=1;
        ctx.strokeStyle='#222';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(0,ry+rh);ctx.lineTo(W,ry+rh);ctx.stroke();
    });
    [xs[1],xs[2],xs[3],xs[4],xs[5]].forEach(function(x){
        ctx.strokeStyle='#222';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(x,hdrH);ctx.lineTo(x,H);ctx.stroke();
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        var lbs=['Loop','Thiazide','Metolazone','Aldosterone','Acetazolamide','Mannitol'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,drugs[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: Loop Diuretic Protocol ──────────────────────────────────────────
RF['loop_diuretic_protocol'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Dosing & Bioavailability','Bolus vs Infusion (DOSE)','Diuretic Resistance'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a2a3a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a3a4a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#4488cc':'#555';ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0a1a';ctx.fillRect(4,panelY,W-8,panelH);
    var content=[
        [['LOOP DIURETIC — IV/ORAL DOSING & BIOAVAILABILITY','',
          'Furosemide (Lasix): Oral bioavailability ~50% (range 10–100%)',
          '  IV dose ≈ ½ total daily oral dose per administration',
          '  Example: oral 40 mg BID (80 mg/day) → IV 40 mg q12h',
          '  Exception: gut edema in decompensated HF ↓ oral absorption further',
          '','Torsemide (Demadex): Oral bioavailability ~80% (more predictable)',
          '  Oral:IV ratio ≈ 1:1; longer t½ (3.5h vs 1.5h) → fewer doses needed',
          '  Oral torsemide 10 mg ≈ oral furosemide 40 mg',
          '','Bumetanide (Bumex): Oral bioavailability ~80%',
          '  1 mg bumetanide ≈ 40 mg furosemide (potency ratio 1:40)',
          '  NOT sulfa-allergy safe — bumetanide also contains sulfonamide moiety']],
        [['DOSE TRIAL (NEJM 2011) — ADHF: High vs Low Dose, Bolus vs Continuous','',
          'HIGH dose (2.5× total daily oral dose IV) vs LOW dose (1:1 equivalent IV):',
          '  High dose: MORE effective — greater global symptom improvement,',
          '  more weight/fluid loss, more net negative balance',
          '  High dose: modest transient Cr rise (reversible, not long-term harm)',
          '  RECOMMENDATION: Use HIGH dose (2.5× oral) for acute decompensation',
          '','Bolus q12h vs Continuous infusion:',
          '  NO significant difference in primary endpoints',
          '  Continuous infusion: more consistent urine output, avoids peaks/troughs',
          '  Bolus: simpler, standard at most ICUs',
          '  Either approach is acceptable; continuous preferred when titration needed']],
        [['DIURETIC RESISTANCE — Causes and Sequential Nephron Blockade','',
          'Causes: "braking phenomenon" (compensatory ↑ NaCl reabsorption between doses),',
          '  RAAS activation, gut edema ↓ absorption, CKD ↓ tubular drug secretion',
          '','SEQUENTIAL NEPHRON BLOCKADE STRATEGIES (in order of escalation):',
          '  1. Switch oral → IV (eliminate bioavailability problem)',
          '  2. Increase IV dose (max ~400–600 mg/day; diminishing returns >200 mg)',
          '  3. ADD METOLAZONE 2.5–5 mg oral 30 min BEFORE furosemide',
          '     (blocks DCT + proximal tubule; synergistic → massive diuresis)',
          '     → Must monitor K⁺ and Mg²⁺ closely — profound electrolyte loss',
          '  4. Switch to continuous infusion (avoids post-dose Na retention)',
          '  5. Add acetazolamide (blocks PCT HCO₃⁻; treats metabolic alkalosis)',
          '  6. Ultrafiltration (cardiorenal failure, refractory volume overload)']]
    ];
    var col=sel<content.length?content[sel][0]:[];
    var ly=panelY+13;
    col.forEach(function(line){
        if(line===''){ly+=4;return;}
        var isHead=(line.startsWith('LOOP')||line.startsWith('DOSE TRIAL')||line.startsWith('DIURETIC RESISTANCE'));
        var isSub=line.startsWith('  ');
        var isStep=line.match(/^\s+\d\./);
        ctx.fillStyle=isHead?'#4488cc':(isStep?'#ddaa66':(isSub?'#8899aa':'#bbb'));
        ctx.font=isHead?'bold 9.5px sans-serif':'9px sans-serif';ctx.textAlign='left';
        ctx.fillText(line,10,ly);ly+=isHead?15:12;
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;';
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,'#4488cc',sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 3: Diuretic Electrolyte Effects ─────────────────────────────────────
RF['diuretic_electrolytes'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var rows=[
        {eff:'Hypokalemia',cause:'Loop + Thiazide\n(Loop > Thiazide)',mech:'↑ distal Na delivery → ↑ K⁺\nwasting in collecting duct',mgmt:'KCl replacement (goal K⁺ >4.0)\nAdd K-sparing (spiro/amiloride)\nMg must be replaced first',c:'#cc3333'},
        {eff:'Hypomagnesemia',cause:'Loop diuretics\n(Thiazide also)',mech:'Renal Mg wasting at TAL\n(NKCC2 inhibition impairs\nMg reabsorption)',mgmt:'Mg replacement first!\nHypoK⁺ refractory without Mg\nIV MgSO₄ 2g × 20 min PRN',c:'#e07020'},
        {eff:'Metabolic\nAlkalosis',cause:'Loop diuretics\n(contraction alk.)',mech:'Volume contraction → ↑ aldosterone\n→ ↑ H⁺ secretion + bicarb\nretention (paradox aciduria)',mgmt:'Replete volume (NaCl) if able\nKCl replacement → ↓ aldosterone\nAcetazolamide: bicarb wasting',c:'#cc6633'},
        {eff:'Hyponatremia',cause:'Thiazides >> Loop\n(thiazides most common)',mech:'Thiazides block diluting segment\nbut preserve ADH action →\nfree water retention',mgmt:'STOP thiazide; fluid restrict\nCorrect slowly (≤10–12 mEq/L/24h)\nIf severe: 3% NaCl (osmotic demyelin)',c:'#9060c0'},
        {eff:'Hyperkalemia',cause:'K-sparing diuretics\n(spiro/eplerenone/amiloride)',mech:'Block aldosterone receptor or\nENaC → ↓ K⁺ excretion in\ncollecting duct',mgmt:'Hold K-sparing diuretic\nRestrict dietary K⁺\nCaution: ACEi/ARB + K-sparing',c:'#38b2a4'},
        {eff:'Hypercalcemia\nvs Hypocalcemia',cause:'Thiazide → ↑Ca²⁺\nLoop → ↓Ca²⁺ (calciuresis)',mech:'Thiazide: ↑ distal Ca reabsorption\n(useful for nephrolithiasis)\nLoop: forces Ca excretion at TAL',mgmt:'Thiazide: useful in\nhypercalcemia of malignancy\nLoop: caution in hypoparathyroid',c:'#4488cc'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/rows.length);
    var xs=[4,110,240,390,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Effect','Diuretic Cause','Mechanism','Management'];
    ctx.font='bold 8.5px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    rows.forEach(function(row,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=row.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=row.c;ctx.font='bold 8.5px sans-serif';ctx.textAlign='center';
        row.eff.split('\n').forEach(function(el,ei){ctx.fillText(el,(xs[0]+xs[1])/2,ry+rh/2-4+ei*10);});
        ctx.fillStyle='#88aabb';ctx.font='8px sans-serif';ctx.textAlign='left';
        row.cause.split('\n').forEach(function(cl,ci){ctx.fillText(cl,xs[1]+3,ry+rh/2-3+ci*9);});
        ctx.fillStyle='#aab8aa';ctx.font='7.5px sans-serif';
        row.mech.split('\n').forEach(function(ml,mi){ctx.fillText(ml,xs[2]+3,ry+rh/2-3+mi*9);});
        ctx.fillStyle='#ccaa88';ctx.font='7.5px sans-serif';
        row.mgmt.split('\n').forEach(function(ml,mi){ctx.fillText(ml,xs[3]+3,ry+rh/2-3+mi*9);});
        ctx.globalAlpha=1;
        ctx.strokeStyle='#222';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(0,ry+rh);ctx.lineTo(W,ry+rh);ctx.stroke();
    });
    [xs[1],xs[2],xs[3]].forEach(function(x){
        ctx.strokeStyle='#222';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(x,hdrH);ctx.lineTo(x,H);ctx.stroke();
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        var lbs=['Hypokalemia','Hypomagnesemia','Met Alk','Hyponatremia','Hyperkalemia','Ca Effects'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,rows[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 4: Acute Decompensated Heart Failure ────────────────────────────────
RF['acute_decompensated_hf'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Initial Dosing (DOSE)','Monitoring Response','Cardiorenal Syndrome'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a1a2e':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a2a3e';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?_AM:'#555';ctx.font=(sel===i?'bold ':'')+'9px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0a14';ctx.fillRect(4,panelY,W-8,panelH);
    var content=[
        [['ADHF INITIAL DIURETIC STRATEGY — DOSE Trial Guidance','',
          'Step 1 — Estimate daily oral dose equivalent:',
          '  Example: patient on oral furosemide 40 mg BID = 80 mg/day total',
          '','Step 2 — Calculate IV dose using HIGH-DOSE strategy:',
          '  HIGH dose: 2.5 × daily oral dose IV = 200 mg/day IV',
          '  Give as: furosemide 100 mg IV q12h OR 8 mg/h continuous',
          '  Furosemide-naive: start 40–80 mg IV q6–12h; titrate by response',
          '','Step 3 — Assess decongestion endpoint (see Monitoring tab):',
          '  Target ≥200–300 mL/h urine output for first 2–6 hours',
          '  Daily net negative balance goal: −1 to −2 L/day',
          '  If inadequate response after 2–4h: dose-escalate or add agent']],
        [['MONITORING DIURETIC RESPONSE IN ADHF','',
          'Urine output goals:',
          '  Acute phase (first 6h): ≥200–300 mL/h (aggressive decongestion)',
          '  24h goal: −1,000 to −2,000 mL net fluid balance',
          '  Daily weight: goal −0.5 to −1 kg/day (chronic); −1 to −2 kg/day (acute)',
          '','Labs (check every 24–48h at minimum; more if aggressive diuresis):',
          '  BMP: K⁺ >3.5 (replace aggressively), Mg²⁺ >2.0 (prevent arrhythmia)',
          '  Creatinine: mild transient rise acceptable; rising >0.3 mg/dL/day = pause',
          '  BUN/Cr ratio: rising ratio → hemoconcentration (goal of decongestion)',
          '  BNP or NT-proBNP: trend toward lower confirms decongestion',
          '','Signs of clinical decongestion: relief of dyspnea, orthopnea, JVD, edema']],
        [['CARDIORENAL SYNDROME (CRS) — Types and ICU Relevance','',
          'CRS Type 1 — Acute Cardiorenal (most common ICU):',
          '  Acute HF → AKI: ↓ CO → ↓ renal perfusion + ↑ venous back-pressure',
          '  Mechanism: ↓ GFR via ↑ renal venous pressure (NOT just forward failure)',
          '  Management: optimize CO (diuresis, afterload reduction), avoid nephrotoxins',
          '  Furosemide is still indicated — decongestion ↓ renal venous pressure',
          '','CRS Type 2 — Chronic Cardiorenal:',
          '  Chronic HF → progressive CKD (neurohormonal activation, chronic low-flow)',
          '','CRS Type 3 — Acute Renocardiac:',
          '  Acute AKI → acute cardiac dysfunction (uremia → myocardial depression)',
          '','Key point: rising Cr during diuresis does NOT automatically mean stop',
          '  — hemodynamic Cr rise from hemoconcentration resolves; AKI from',
          '  over-diuresis (hypovolemia) requires dose reduction']]
    ];
    var col=sel<content.length?content[sel][0]:[];
    var ly=panelY+13;
    col.forEach(function(line){
        if(line===''){ly+=4;return;}
        var isHead=(line.startsWith('ADHF')||line.startsWith('MONITORING')||line.startsWith('CARDIORENAL'));
        var isSub=line.startsWith('  ');
        ctx.fillStyle=isHead?_AM:(isSub?'#8899aa':'#bbb');
        ctx.font=isHead?'bold 9.5px sans-serif':'9px sans-serif';ctx.textAlign='left';
        ctx.fillText(line,10,ly);ly+=isHead?15:12;
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;';
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,_AM,sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 5: Mannitol & Hypertonic Saline — ICP Management ───────────────────
RF['mannitol_hypertonic'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Mannitol','Hypertonic Saline','Comparison & Selection'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#2a1a0a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#3a2a1a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?_OR:'#555';ctx.font=(sel===i?'bold ':'')+'9px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0a0a';ctx.fillRect(4,panelY,W-8,panelH);
    var content=[
        [['MANNITOL (Osmitrol) — Osmotic Diuretic for ICP Reduction','',
          'Mechanism: raises serum osmolality → osmotic gradient draws water',
          '  from brain (cytotoxic edema) into blood → ↓ cerebral edema + ICP',
          '  Also: modest ↓ blood viscosity → ↑ cerebral blood flow',
          '','Dose: 0.25–1 g/kg IV over 15–30 min (bolus only; NOT infusion)',
          '  Standard: 1 g/kg for acute herniation; 0.5 g/kg for maintenance',
          '  Example: 70 kg patient → 70 g mannitol = 350 mL of 20% solution',
          '','Monitoring: serum osmolality q6h; target <320 mOsm/kg (toxicity risk)',
          '  Osmol gap = measured osm − calculated osm (normal <10); >20 = danger',
          '  Contraindication: serum osm >320 mOsm/kg; oliguria/anuria (accumulates)',
          '','Onset: 15–30 min | Duration: 2–6h | Side effect: diuresis → hypovolemia']],
        [['HYPERTONIC SALINE (HTS) — Osmotic Agent for ICP','',
          'Mechanism: ↑ serum Na⁺ → osmotic gradient → draws water from brain;',
          '  maintains intravascular volume (unlike mannitol which causes diuresis)',
          '','Formulations and doses:',
          '  3% NaCl: 250 mL IV bolus (over 20–30 min) for acute ICP elevation',
          '  23.4% NaCl: 30 mL IV × 15 min (central line ONLY — causes phlebitis)',
          '    Central venous access required for concentrations ≥3% continuous',
          '','Monitoring: serum Na⁺ q2–4h; target Na 145–155 mEq/L (therapeutic range)',
          '  Max target: 160 mEq/L (some protocols); avoid >160 mEq/L',
          '  Do NOT correct rapidly — hypernatremia risk; do NOT use in hypernatremia',
          '','Duration of effect: 4–6h (longer than mannitol); no diuresis → fluid neutral']],
        [['MANNITOL vs HYPERTONIC SALINE — Selection Guide','',
          'Prefer HYPERTONIC SALINE when:',
          '  Patient is hypovolemic or hypotensive (HTS maintains volume; mannitol diureses)',
          '  Serum osmolality already ≥320 mOsm/kg (mannitol CI)',
          '  Need for sustained or repeated dosing (less accumulation risk than mannitol)',
          '  Traumatic brain injury with hemorrhagic shock (most common TBI ICU scenario)',
          '','Prefer MANNITOL when:',
          '  Central line not yet available (3% NaCl requires central access)',
          '  Hypernatremia already present (HTS would worsen Na⁺)',
          '  Rhabdomyolysis with renal protection needed (mannitol flushes myoglobin)',
          '  Acute glaucoma (osmotic reduction of intraocular pressure)',
          '','Both: onset 15–30 min; goal ICP <20–22 mmHg; CPP >60 mmHg']]
    ];
    var col=sel<content.length?content[sel][0]:[];
    var ly=panelY+13;
    col.forEach(function(line){
        if(line===''){ly+=4;return;}
        var isHead=(line.startsWith('MANNITOL')||line.startsWith('HYPERTONIC SALINE')||line.startsWith('MANNITOL vs'));
        var isSub=line.startsWith('  ');
        ctx.fillStyle=isHead?_OR:(isSub?'#8899aa':'#bbb');
        ctx.font=isHead?'bold 9.5px sans-serif':'9px sans-serif';ctx.textAlign='left';
        ctx.fillText(line,10,ly);ly+=isHead?15:12;
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;';
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,_OR,sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        ctrl.appendChild(row);
    }
}
"""

# ── Cards ─────────────────────────────────────────────────────────────────────
CARDS = [
    # ═══ diuretic_comparison ══════════════════════════════════════════════════
    (
        "On the diuretic comparison chart, loop diuretics work by inhibiting "
        "the _______ cotransporter at the _______. This explains why they cause "
        "hypocalcemia: the same transporter also reabsorbs _______.",

        "Loop diuretics inhibit the Na-K-2Cl cotransporter (NKCC2) at the "
        "thick ascending limb (TAL) of the loop of Henle\n"
        "| Same transporter reabsorbs calcium — NKCC2 inhibition forces "
        "calciuria → hypocalcemia (forced Ca²⁺ excretion)\n"
        "| Clinical application: loops are used to TREAT hypercalcemia of malignancy "
        "(force Ca²⁺ excretion) after adequate saline hydration\n"
        "→ CCRN KEY: Loop diuretic mnemonic: TAL → NKCC2 → loss of K⁺, Mg²⁺, Ca²⁺, "
        "and H⁺ (metabolic alkalosis). The TAL reabsorbs 25–30% of filtered NaCl — "
        "loss of this reabsorption explains the high diuretic ceiling of loop diuretics "
        "compared to thiazides (DCT reabsorbs only 5–10% of NaCl).\n"
        "→ MASTERY NOTE: Calcium paradox in diuretics: Loops = hypocalcemia "
        "(force Ca²⁺ excretion at TAL). Thiazides = hypercalcemia "
        "(↑ distal Ca²⁺ reabsorption at DCT). Thiazides are therefore used in "
        "patients with renal calcium stones (thiazides ↓ urinary Ca²⁺ → ↓ stone formation).",

        'tier-review',
        _NM,
        DID['diuretics'],
        'diuretic_comparison',
        '{"hi":0}',
        'chart-l1'
    ),
    (
        "On the diuretic chart, spironolactone is an aldosterone receptor antagonist. "
        "The RALES trial showed it reduces _______ mortality by _______% "
        "in patients with _______. "
        "The most dangerous side effect in renal failure is _______.",

        "RALES trial (1999, NEJM): spironolactone reduced ALL-CAUSE MORTALITY "
        "by 30% (relative risk reduction) in HFrEF patients with EF ≤35% "
        "(NYHA class III–IV, severe systolic HF)\n"
        "| Most dangerous side effect in renal failure: HYPERKALEMIA\n"
        "  Risk factors: CrCl <30, co-administration with ACEi/ARB/sacubitril-valsartan, "
        "  K⁺ supplementation, diabetes\n"
        "→ CCRN KEY: Spironolactone dosing for HF: 25 mg once daily (RALES protocol); "
        "titrate to 50 mg daily if tolerated. Monitor K⁺ and Cr at 1 week, 1 month, "
        "then q3 months. HOLD if K⁺ >5.5 mEq/L or Cr rising rapidly.\n"
        "→ MASTERY NOTE: Spironolactone vs eplerenone: spironolactone is non-selective "
        "(blocks androgen receptors → gynecomastia, menstrual irregularities in 10%). "
        "Eplerenone is selective for mineralocorticoid receptor → fewer sex-hormone "
        "side effects. EPHESUS trial: eplerenone reduces mortality post-MI with EF <40%. "
        "Eplerenone is used when spironolactone causes gynecomastia.",

        'tier-high',
        _NM,
        DID['diuretics'],
        'diuretic_comparison',
        '{"hi":3}',
        'chart-l2'
    ),
    (
        "On the diuretic chart, metolazone is given _______ minutes BEFORE "
        "furosemide for sequential nephron blockade. It differs from other "
        "thiazides by also blocking the _______ in addition to the DCT. "
        "The critical monitoring priority after this combination is _______.",

        "Metolazone is given 30 minutes BEFORE furosemide (allows metolazone "
        "to reach its site of action before furosemide arrives)\n"
        "| Unique: also blocks the proximal convoluted tubule (PCT) in addition to DCT "
        "(thiazide-like inhibition of NCC at DCT + additional proximal action → "
        "more powerful than standard thiazides)\n"
        "| Critical monitoring: Potassium (K⁺) — the combination causes profound "
        "hypokalemia and hypomagnesemia; may need aggressive IV KCl + MgSO₄ replacement\n"
        "→ CCRN KEY: Sequential nephron blockade rationale: furosemide blocks TAL → "
        "compensatory ↑ NaCl reabsorption at distal sites (DCT/CD). Metolazone "
        "blocks DCT simultaneously → no compensatory escape → massive diuresis.\n"
        "This combination can produce 5–10 L/day urine output in resistant patients.\n"
        "→ MASTERY NOTE: Metolazone only needs to be given ONCE (30–60 min before "
        "morning furosemide dose) — not every furosemide dose. Monitor BMP q6–12h "
        "after first dose combination. Often used 2–3 days then stopped when "
        "decongestion goal achieved; prolonged use leads to dangerous electrolyte depletion.",

        'tier-critical',
        _NM,
        DID['diuretics'],
        'diuretic_comparison',
        '{"hi":2}',
        'chart-l3'
    ),

    # ═══ loop_diuretic_protocol ════════════════════════════════════════════════
    (
        "On the loop diuretic protocol chart, oral furosemide bioavailability "
        "is approximately _______%. Therefore, when converting a patient from "
        "oral furosemide 80 mg BID to IV, the equivalent IV dose is _______.",

        "Oral furosemide bioavailability: approximately 50% (range 10–100%; "
        "highly variable, especially worse in decompensated HF with gut edema)\n"
        "| IV equivalent: 80 mg oral × 50% = 40 mg IV per dose "
        "(IV dose = ½ the oral dose because IV bypasses absorption losses)\n"
        "| Example: oral 80 mg BID (160 mg/day) → IV 40 mg q12h (or 80 mg IV daily if once-daily)\n"
        "→ CCRN KEY: Comparison of loop diuretics by bioavailability:\n"
        "• Furosemide: 50% oral (unreliable in HF) → double-dose for IV equivalent\n"
        "• Torsemide: 80% oral (more predictable) → ~1:1 oral:IV ratio\n"
        "• Bumetanide: 80% oral → 1:1 ratio; 1 mg = 40 mg furosemide (potency ratio)\n"
        "→ MASTERY NOTE: In decompensated HF with gut edema, oral furosemide "
        "bioavailability may fall to <20%. This is why patients admitted for ADHF "
        "often seem 'diuretic refractory' on their home oral dose — it's an absorption "
        "problem, not true drug resistance. Switching to IV corrects this immediately.",

        'tier-review',
        _NM,
        DID['diuretics'],
        'loop_diuretic_protocol',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The loop diuretic protocol chart summarizes the DOSE trial. "
        "The recommended initial IV dose strategy for ADHF is _______ × "
        "the total daily oral dose. The trial showed this causes a modest "
        "_______ rise, which is considered _______.",

        "Recommended: HIGH dose = 2.5× the total daily oral dose IV\n"
        "| Example: oral 40 mg BID = 80 mg/day → 2.5 × 80 = 200 mg/day IV "
        "(give as 100 mg IV q12h or 8 mg/h continuous)\n"
        "| High dose causes a modest, transient creatinine rise "
        "(average ~0.1 mg/dL) — considered acceptable and not long-term harmful\n"
        "→ CCRN KEY: DOSE trial (NEJM 2011) key findings:\n"
        "• High dose (2.5×): more symptoms relief, greater weight loss/net fluid balance\n"
        "• Low dose (1×): less Cr rise but less effective decongestion\n"
        "• Bolus q12h vs continuous infusion: NO significant difference in outcomes\n"
        "• Bottom line: push the dose; the temporary Cr rise is a price worth paying\n"
        "→ MASTERY NOTE: The modest Cr rise with aggressive diuresis reflects "
        "hemoconcentration (renal blood flow is actually preserved or improved as "
        "venous congestion decreases). The error is STOPPING diuresis for a small "
        "Cr rise — this leaves the patient volume-overloaded while the 'improved Cr' "
        "is just from reduced diuresis. Clinical rule: if the patient feels better "
        "and is making urine, continue diuresis despite minor Cr elevation.",

        'tier-high',
        _NM,
        DID['diuretics'],
        'loop_diuretic_protocol',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "On the resistance chart, the first-line strategy for diuretic "
        "resistance is _______, followed by adding _______ given "
        "_______ minutes before furosemide. This combination is called "
        "_______ nephron blockade.",

        "First-line: switch from oral to IV furosemide (eliminates bioavailability problem)\n"
        "| Next: add metolazone (thiazide-like) given 30 minutes before furosemide\n"
        "| This combination is called SEQUENTIAL NEPHRON BLOCKADE\n"
        "→ CCRN KEY: Complete resistance escalation ladder:\n"
        "1. Switch oral → IV (bioavailability fix)\n"
        "2. ↑ IV dose (max ~400–600 mg/day; ceiling effect above 200 mg)\n"
        "3. Add metolazone 2.5–5 mg oral 30 min before furosemide\n"
        "4. Switch to continuous infusion (avoid post-dose Na retention)\n"
        "5. Add acetazolamide (blocks PCT + treats metabolic alkalosis → "
        "   restores tubular drug responsiveness)\n"
        "6. Ultrafiltration for refractory cardiorenal failure\n"
        "→ MASTERY NOTE: Metabolic alkalosis contributes to loop resistance: "
        "alkalosis impairs NKCC2 function (the transporter that furosemide "
        "blocks works less when alkalotic). Acetazolamide corrects the alkalosis "
        "by causing bicarb wasting at the PCT, restoring NKCC2 sensitivity. "
        "This is why ADVOR trial (2022) showed acetazolamide + loop diuretics "
        "→ more decongestion in ADHF than loops alone.",

        'tier-critical',
        _NM,
        DID['diuretics'],
        'loop_diuretic_protocol',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ diuretic_electrolytes ═════════════════════════════════════════════════
    (
        "On the diuretic electrolyte chart, hypomagnesemia from loop diuretics "
        "is clinically important because it causes _______ hypokalemia. "
        "This is because magnesium inhibits _______ in the collecting duct.",

        "Hypomagnesemia causes REFRACTORY hypokalemia that cannot be corrected "
        "until magnesium is replaced first\n"
        "| Mechanism: magnesium inhibits ROMK (renal outer medullary K⁺ channel) "
        "in the collecting duct — this channel normally allows K⁺ to be wasted. "
        "Without adequate Mg²⁺, ROMK is upregulated → excessive K⁺ excretion "
        "even after K⁺ is replaced\n"
        "→ CCRN KEY: Clinical rule: any time you replace K⁺ and it doesn't "
        "hold (K⁺ keeps falling or stays low despite replacement), check and "
        "replace Mg²⁺ FIRST. Give IV MgSO₄ 2 g over 20 min, then recheck. "
        "K⁺ will then respond to replacement. This sequence is essential.\n"
        "→ MASTERY NOTE: Normal serum Mg²⁺: 1.7–2.2 mEq/L. Below 1.5 mEq/L "
        "= significant deficiency; below 1.0 mEq/L = dangerous (arrhythmia risk, "
        "neuromuscular excitability). Torsades de pointes risk increases at low Mg²⁺ — "
        "especially in patients on QT-prolonging drugs (amiodarone, quinolones, "
        "antipsychotics). Always include Mg²⁺ in your ICU electrolyte panel.",

        'tier-review',
        _NM,
        DID['diuretics'],
        'diuretic_electrolytes',
        '{"hi":1}',
        'chart-l1'
    ),
    (
        "The electrolyte chart shows thiazides cause the most dangerous "
        "_______ of all diuretics. The mechanism differs from loops because "
        "thiazides block the _______ segment AND preserve _______ action.",

        "Thiazides cause the most dangerous HYPONATREMIA of all diuretics\n"
        "| Mechanism difference: thiazides block the DCT (diluting segment) "
        "— this segment normally dilutes urine by reabsorbing NaCl without water. "
        "Blocking it impairs free water excretion.\n"
        "| Thiazides PRESERVE ADH action on the collecting duct (unlike loops, "
        "which also impair the medullary gradient needed for ADH to work)\n"
        "| Net result: thiazides = impaired free water excretion + intact ADH "
        "free water retention = hyponatremia\n"
        "→ CCRN KEY: Thiazide hyponatremia correction: STOP thiazide (most important); "
        "restrict free water; correct slowly (≤10–12 mEq/L per 24 hours). "
        "Correction faster than 12 mEq/L/24h risks osmotic demyelination syndrome "
        "(central pontine myelinolysis) — irreversible neurological damage. "
        "If Na⁺ <120 mEq/L with symptoms: consider 3% NaCl for controlled correction.\n"
        "→ MASTERY NOTE: Loops can also cause hyponatremia but it's usually mild "
        "and less common than with thiazides. The difference: loops impair the "
        "medullary concentrating gradient (blunts ADH response), partially protecting "
        "against hyponatremia. Thiazides leave ADH fully functional while blocking "
        "dilution — creating the perfect setup for profound hyponatremia.",

        'tier-high',
        _NM,
        DID['diuretics'],
        'diuretic_electrolytes',
        '{"hi":3}',
        'chart-l2'
    ),
    (
        "The electrolyte chart shows loop diuretics cause metabolic alkalosis "
        "by _______ mechanism. The specific treatment for metabolic alkalosis "
        "from loops when volume cannot be replaced is _______, which works by _______.",

        "Metabolic alkalosis mechanism: volume contraction → ↑ aldosterone → "
        "↑ H⁺ secretion in collecting duct + ↑ bicarbonate reabsorption. "
        "Also: K⁺ depletion → intracellular H⁺ shifts maintain extracellular alkalosis. "
        "Called 'contraction alkalosis' — the bicarb is concentrated as ECF contracts\n"
        "| Treatment when volume cannot be replaced: Acetazolamide\n"
        "| Mechanism: inhibits carbonic anhydrase at PCT → impairs HCO₃⁻ reabsorption "
        "→ bicarb wasted in urine (renal bicarbonate diuresis) → lowers serum pH\n"
        "→ CCRN KEY: Why K⁺ must be replaced before treating alkalosis: "
        "K⁺ depletion perpetuates alkalosis — the kidney 'prefers' to reabsorb K⁺ "
        "and excrete H⁺ when K⁺ is depleted (protective of K⁺ stores at the cost "
        "of worsening alkalosis). Replacing K⁺ breaks this cycle first.\n"
        "→ MASTERY NOTE: Metabolic alkalosis impairs loop diuretic response: "
        "the NKCC2 transporter works less effectively when tubular pH is alkalotic. "
        "This is the mechanistic rationale for the ADVOR trial (2022) showing "
        "acetazolamide + loop diuretic improves decongestion in ADHF — "
        "acetazolamide corrects alkalosis AND adds independent diuresis.",

        'tier-critical',
        _NM,
        DID['diuretics'],
        'diuretic_electrolytes',
        '{"hi":2}',
        'chart-l3'
    ),

    # ═══ acute_decompensated_hf ════════════════════════════════════════════════
    (
        "On the ADHF dosing chart, a patient on oral furosemide 40 mg BID "
        "(80 mg/day) is admitted for ADHF. Per DOSE trial guidance, "
        "the recommended initial IV dose is _______ mg daily. "
        "The target urine output in the first 6 hours is _______.",

        "DOSE trial HIGH dose: 2.5 × 80 mg/day = 200 mg/day IV total\n"
        "| Give as: furosemide 100 mg IV q12h (or 8 mg/h continuous infusion)\n"
        "| Target urine output first 6 hours: ≥200–300 mL/h (aggressive acute decongestion)\n"
        "→ CCRN KEY: ADHF diuretic management goals:\n"
        "• Acute phase (first 24–48h): −1 to −2 L net balance/day\n"
        "• Daily weight: −1 to −2 kg/day acceptable; avoid >2 kg/day (over-diuresis)\n"
        "• BNP/NT-proBNP: trend toward improvement confirms decongestion\n"
        "• SpO₂, respiratory effort, JVD: clinical decongestion endpoints\n"
        "→ MASTERY NOTE: Furosemide-naive patient (no prior diuretics): "
        "start with furosemide 40–80 mg IV q6–12h and titrate. "
        "Furosemide-tolerant patient (chronic high-dose diuretics): "
        "the 2.5× rule often requires 200–400 mg/day IV to achieve adequate response. "
        "There is no harm in going higher if closely monitored — the ceiling effect "
        "for furosemide is around 400–600 mg/dose beyond which no additional diuresis occurs.",

        'tier-review',
        _NM,
        DID['diuretics'],
        'acute_decompensated_hf',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the ADHF monitoring chart, rising creatinine during aggressive "
        "diuresis should prompt concern when it rises more than _______ mg/dL/day. "
        "However, a mild rise is often _______ rather than true AKI. "
        "The key electrolytes to replace during aggressive diuresis are "
        "_______ and _______.",

        "Concerning Cr rise: >0.3 mg/dL/day (or rising rapidly without return "
        "toward baseline → pause diuresis and reassess volume status)\n"
        "| Mild rise is often hemoconcentration — fluid is being removed from "
        "the vascular space (desired), blood thickens slightly → BUN/Cr rises. "
        "This is not true AKI (tubular function intact; resolves as volume normalizes)\n"
        "| Key electrolytes: Potassium (K⁺ goal >4.0 mEq/L to prevent arrhythmia) "
        "AND Magnesium (Mg²⁺ goal >2.0 mEq/L — replace first if hypokalemia refractory)\n"
        "→ CCRN KEY: ADHF BMP monitoring frequency: every 24–48h during aggressive "
        "diuresis; every 12h if metolazone added. Check K⁺ before each potassium-replacing "
        "dose. Monitor QTc if on amiodarone or other antiarrhythmics (hypokalemia + "
        "hypomagnesemia + QT-prolonging drug = torsades risk).\n"
        "→ MASTERY NOTE: Distinguishing hemoconcentration vs AKI: hemoconcentration "
        "shows rising BUN:Cr ratio (>20:1) and rising hematocrit — these indicate "
        "concentrated blood, not kidney damage. True AKI from over-diuresis shows "
        "FeNa <1% (prerenal pattern), oliguria, and improvement with fluid. "
        "The clinical picture (ongoing pulmonary edema vs dry patient) guides the decision.",

        'tier-high',
        _NM,
        DID['diuretics'],
        'acute_decompensated_hf',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The ADHF chart defines Cardiorenal Syndrome Type 1 as _______ causing "
        "_______. The mechanism involves not just reduced cardiac output, "
        "but also elevated _______ pressure that directly reduces GFR.",

        "CRS Type 1: Acute cardiac dysfunction (acute HF) causing acute kidney injury\n"
        "| Mechanism is dual:\n"
        "1. ↓ Cardiac output → ↓ renal perfusion pressure → ↓ GFR (forward failure)\n"
        "2. Elevated renal VENOUS pressure (venous congestion transmits to renal veins) "
        "→ ↑ renal interstitial pressure → ↓ net filtration pressure → ↓ GFR "
        "(backward failure — venous congestion may be the dominant mechanism)\n"
        "→ CCRN KEY: Clinical implication of dual mechanism: aggressive DIURESIS "
        "in CRS Type 1 often IMPROVES renal function (reduces venous congestion → "
        "reduces renal venous pressure → improves GFR). This is counterintuitive — "
        "nurses may be hesitant to give diuretics to a patient with rising Cr, "
        "but decongestion is the treatment for venous-congestion-mediated AKI.\n"
        "→ MASTERY NOTE: CRS classification (5 types):\n"
        "Type 1 = Acute HF → AKI (most common in ICU)\n"
        "Type 2 = Chronic HF → CKD\n"
        "Type 3 = Acute AKI → acute cardiac dysfunction\n"
        "Type 4 = CKD → chronic cardiac dysfunction\n"
        "Type 5 = Systemic disease → both (sepsis, DM, amyloid)\n"
        "CCRN most tests Type 1 and Type 3.",

        'tier-critical',
        _NM,
        DID['diuretics'],
        'acute_decompensated_hf',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ mannitol_hypertonic ═══════════════════════════════════════════════════
    (
        "On the mannitol chart, the standard dose for acute ICP elevation "
        "is _______ g/kg IV over _______ minutes. "
        "The serum osmolality ceiling to prevent toxicity is _______.",

        "Standard dose: 0.25–1 g/kg IV over 15–30 minutes (bolus, NOT infusion)\n"
        "| Acute herniation: 1 g/kg; maintenance/repeat dosing: 0.25–0.5 g/kg\n"
        "| Serum osmolality ceiling: <320 mOsm/kg (stop mannitol if at or above this)\n"
        "| Monitor via osmol gap (measured Osm − calculated Osm); stop if gap >20 mOsm/kg\n"
        "→ CCRN KEY: Mannitol mechanism: raises serum osmolality → osmotic gradient "
        "draws free water out of brain (cytotoxic edema) into bloodstream → "
        "reduces cerebral water content → reduces ICP. Secondary effect: "
        "↓ blood viscosity → ↑ cerebral blood flow and O₂ delivery.\n"
        "Contraindications: serum Osm >320 (toxicity), oliguria/anuria (accumulates, "
        "causes AKI), severe heart failure (volume shift worsens fluid overload).\n"
        "→ MASTERY NOTE: Osmol gap calculation: Calc Osm = 2[Na] + BUN/2.8 + glucose/18 "
        "(+ ETOH/4.6 if applicable). If measured Osm >> calculated Osm: mannitol "
        "is accumulating. Mannitol accumulation causes paradoxical worsening of "
        "cerebral edema (osmotic gradient reverses — mannitol enters the brain).",

        'tier-review',
        _NM,
        DID['diuretics'],
        'mannitol_hypertonic',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the mannitol/HTS comparison chart, hypertonic saline is preferred "
        "over mannitol when the patient is _______. "
        "The 23.4% NaCl concentration requires _______ access. "
        "The target serum sodium during HTS therapy is _______.",

        "HTS preferred when patient is HYPOVOLEMIC or HYPOTENSIVE "
        "(HTS maintains or expands intravascular volume; mannitol causes diuresis → "
        "worsens hypotension)\n"
        "| 23.4% NaCl requires CENTRAL venous access (causes phlebitis at peripheral "
        "sites; only appropriate concentration for peripheral use is 3% NaCl in slow bolus)\n"
        "| Target serum sodium during HTS: 145–155 mEq/L (therapeutic hypernatremia)\n"
        "→ CCRN KEY: HTS formulations for ICP:\n"
        "• 3% NaCl: 250 mL bolus over 20–30 min (peripheral or central)\n"
        "• 23.4% NaCl: 30 mL bolus over 15 min (CENTRAL LINE ONLY)\n"
        "• Continuous 3% NaCl: rate titrated to Na 145–155 mEq/L\n"
        "Monitor: serum Na q2–4h; avoid Na >160; do NOT use in hypernatremia.\n"
        "→ MASTERY NOTE: Duration advantage of HTS over mannitol: HTS reduces "
        "ICP for 4–6 hours vs mannitol ~2–4 hours. HTS does NOT cause diuresis, "
        "so it doesn't cause the systemic fluid and electrolyte shifts that mannitol "
        "does. This makes HTS more appealing in TBI with hemorrhagic shock — "
        "HTS provides simultaneous volume expansion AND ICP reduction.",

        'tier-high',
        _NM,
        DID['diuretics'],
        'mannitol_hypertonic',
        '{"sel":2}',
        'chart-l2'
    ),
    (
        "On the mannitol chart, the osmol gap is used to monitor for "
        "mannitol toxicity. It is calculated as _______ minus _______. "
        "A gap above _______ indicates dangerous mannitol accumulation. "
        "Rhabdomyolysis is a unique indication for mannitol because it _______.",

        "Osmol gap = MEASURED serum osmolality MINUS CALCULATED serum osmolality\n"
        "| Calculated Osm = 2×[Na] + BUN/2.8 + glucose/18\n"
        "| Gap >20 mOsm/kg = dangerous mannitol accumulation → HOLD further doses\n"
        "| Also hold if serum Osm >320 mOsm/kg\n"
        "→ CCRN KEY: Rhabdomyolysis indication for mannitol: mannitol provides "
        "osmotic tubular flow → washes out myoglobin from tubules → prevents "
        "myoglobin precipitation → reduces AKI risk from tubular cast formation. "
        "Also used in combination with IV fluid (aggressive hydration: "
        "200–300 mL/h + mannitol) and urine alkalinization (NaHCO₃).\n"
        "→ MASTERY NOTE: Mannitol paradox at high serum Osm: when serum Osm >320, "
        "the blood-brain barrier becomes leaky to mannitol over time. Mannitol "
        "crosses into brain tissue → brain Osm rises → water moves INTO brain "
        "(reverse osmotic gradient) → cerebral edema WORSENS. This is why "
        "the 320 mOsm/kg ceiling is absolute — above this, mannitol is harmful "
        "for ICP. The osmol gap detects this accumulation before the ceiling is reached.",

        'tier-critical',
        _NM,
        DID['diuretics'],
        'mannitol_hypertonic',
        '{"sel":0}',
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
