#!/usr/bin/env python3
"""chunk48_charts.py — Ph8 Reference: Acid-Base (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_47.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_48.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c48')
CHUNK_NUM   = 48
MID_BASE    = 1_800_005_085
CHART_ORDER = ['acid_base_map', 'compensation_formulas', 'anion_gap',
               'blood_gas_steps', 'clinical_acid_base']

_NM = 'Ph8 · \U0001f7e1 T3 · Reference — Acid-Base'

RF = {}

# ── Chart 1: Primary Acid-Base Disorder Map ───────────────────────────────────
RF['acid_base_map'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var disorders=[
        {name:'Metabolic\nAcidosis',ph:'↓ < 7.35',co2:'↓ compensated',hco3:'↓ < 22',
         comp:"PaCO₂ = 1.5×HCO₃ + 8 ± 2\n(Winter's formula)\nMin PaCO₂ ≈ 10–15 mmHg",
         cause:'Lactic acidosis, DKA,\nrenal failure, diarrhea,\ntoxic ingestion (MUDPILES)',c:'#cc4444'},
        {name:'Metabolic\nAlkalosis',ph:'↑ > 7.45',co2:'↑ compensated',hco3:'↑ > 26',
         comp:'PaCO₂ = 0.7×HCO₃ + 21 ± 2\n(reflex hypoventilation)\nMax PaCO₂ ≈ 55–60 mmHg',
         cause:'Vomiting, NG suction,\nloop/thiazide diuretics,\nhyperaldosteronism, antacids',c:'#cc8844'},
        {name:'Respiratory\nAcidosis',ph:'↓ < 7.35',co2:'↑ > 45',hco3:'↑ compensated',
         comp:'Acute: ΔHCO₃ = 0.1×ΔCO₂\nChronic: ΔHCO₃ = 0.35×ΔCO₂\n(renal retention of HCO₃)',
         cause:'Hypoventilation: COPD,\nsedation, NMB, obesity\nhypoventilation, permissive',c:'#4488cc'},
        {name:'Respiratory\nAlkalosis',ph:'↑ > 7.45',co2:'↓ < 35',hco3:'↓ compensated',
         comp:'Acute: ΔHCO₃ = 0.2×ΔCO₂\nChronic: ΔHCO₃ = 0.5×ΔCO₂\n(renal excretion of HCO₃)',
         cause:'Hyperventilation: anxiety,\npain, sepsis (early),\npregnancy, liver failure',c:'#3a9a5c'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=20, rh=Math.floor((H-hdrH)/disorders.length);
    var xs=[4,115,170,230,285,450,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Disorder','pH','PaCO₂','HCO₃','Compensation Formula','Common ICU Causes'];
    ctx.font='bold 8px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    disorders.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=d.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=d.c;ctx.font='bold 8px sans-serif';ctx.textAlign='left';
        d.name.split('\n').forEach(function(l,li){ctx.fillText(l,xs[0]+3,ry+rh/2-5+li*11);});
        ctx.fillStyle='#eedd88';ctx.font='bold 8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.ph,(xs[1]+xs[2])/2,ry+rh/2+3);
        ctx.fillStyle='#88bbee';ctx.font='8px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.co2,(xs[2]+xs[3])/2,ry+rh/2+3);
        ctx.fillStyle='#aabb88';ctx.font='8px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.hco3,(xs[3]+xs[4])/2,ry+rh/2+3);
        ctx.fillStyle='#ccbbaa';ctx.font='7.5px sans-serif';ctx.textAlign='left';
        d.comp.split('\n').forEach(function(l,li){ctx.fillText(l,xs[4]+3,ry+rh/2-8+li*9);});
        ctx.fillStyle='#99aabb';ctx.font='7.5px sans-serif';ctx.textAlign='left';
        d.cause.split('\n').forEach(function(l,li){ctx.fillText(l,xs[5]+3,ry+rh/2-8+li*9);});
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
        var lbs=['Met Acidosis','Met Alkalosis','Resp Acidosis','Resp Alkalosis'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,disorders[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: Compensation Formulas ───────────────────────────────────────────
RF['compensation_formulas'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Metabolic Compensation','Respiratory Compensation','Mixed Disorder Detection'];
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
    var lm=14, ly=panelY+15;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#88bbee';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+200,ly);}
        ly+=14;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=12;}
    function hr(){ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=6;}
    if(sel===0){
        rw('METABOLIC ACIDOSIS → Expected PaCO₂:','','#cc6666');
        rw("Winter's Formula:","PaCO₂ = 1.5 × HCO₃ + 8 ± 2",'#aab','#eedd88');
        nt('If measured PaCO₂ > expected → concurrent Resp Acidosis (inadequate compensation)');
        nt("If measured PaCO₂ < expected → concurrent Resp Alkalosis (additional hyperventilation)");
        nt("Minimum PaCO₂ achievable ≈ 10–15 mmHg (physiologic limit of hyperventilation)");
        hr();
        rw('METABOLIC ALKALOSIS → Expected PaCO₂:','','#cc8844');
        rw('Compensation:','PaCO₂ = 0.7 × HCO₃ + 21 ± 2','#aab','#eedd88');
        nt('Alt: ΔPaCO₂ = 0.6 × ΔHCO₃ (CO₂ rises ~0.6 for each 1 mEq/L HCO₃ rise)');
        nt('Maximum PaCO₂ ≈ 55–60 mmHg (hypoxic drive limits hypoventilation)');
        hr();
        nt('★ Metabolic compensation = respiratory response (fast: minutes to hours)');
        nt('  Respiratory compensation for metabolic = always FULL; assess with formula');
    } else if(sel===1){
        rw('RESPIRATORY ACIDOSIS → Expected HCO₃:','','#4488cc');
        rw('Acute (< 24h):','ΔHCO₃ = 0.1 × ΔPaCO₂   [~1 mEq/L per 10 mmHg CO₂↑]','#aab','#eedd88');
        rw('Chronic (> 3–5d):','ΔHCO₃ = 0.35 × ΔPaCO₂  [~3.5 mEq/L per 10 mmHg CO₂↑]','#aab','#eedd88');
        nt('HCO₃ max in chronic resp acidosis ≈ 38–40 mEq/L (renal limit)');
        hr();
        rw('RESPIRATORY ALKALOSIS → Expected HCO₃:','','#3a9a5c');
        rw('Acute (< 24h):','ΔHCO₃ = 0.2 × ΔPaCO₂   [~2 mEq/L per 10 mmHg CO₂↓]','#aab','#eedd88');
        rw('Chronic (> 3–5d):','ΔHCO₃ = 0.5 × ΔPaCO₂  [~5 mEq/L per 10 mmHg CO₂↓]','#aab','#eedd88');
        nt('HCO₃ min in chronic resp alkalosis ≈ 12–15 mEq/L (renal limit)');
        hr();
        nt('★ KEY: Renal compensation = metabolic response (slow: 3–5 days for FULL effect)');
        nt('  Acute = buffering only; chronic = true renal HCO₃ adjustment');
    } else {
        rw('Anion Gap:','Na − (Cl + HCO₃)  [Normal: 8–12 mEq/L]','#cc4444','#eedd88');
        rw('Corrected AG:','AG + 2.5 × (4.0 − albumin g/dL)','#aab','#eedd88');
        nt('Hypoalbuminemia LOWERS the AG — correct before interpreting HAGMA vs NAGMA');
        hr();
        rw('Delta-Delta Ratio:','(AG − 12) / (24 − HCO₃)','#cc8844','#eedd88');
        rw('< 0.4','Pure NAGMA (hyperchloremic; no AG elevation)','#aab','#88ccff');
        rw('0.4–1.0','Mixed: HAGMA + concurrent NAGMA','#aab','#88ffcc');
        rw('1.0–2.0','Pure HAGMA (expected drop in HCO₃ matches AG rise)','#aab','#ffdd88');
        rw('> 2.0','HAGMA + concurrent Metabolic Alkalosis (HCO₃ not as low as expected)','#aab','#ffaa88');
        hr();
        nt('★ Example: DKA + vomiting → HAGMA from ketones + met alkalosis from vomiting');
        nt('  → delta-delta > 2; HCO₃ 20 (should be ~10 for pure HAGMA with AG 30)');
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

# ── Chart 3: Anion Gap — MUDPILES, NAGMA, Osmol Gap ──────────────────────────
RF['anion_gap'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['HAGMA — MUDPILES','NAGMA Causes','Osmol Gap'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a0a0a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#3a1a1a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?_RE:'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0808';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+14;
    function nt(t,c){ctx.fillStyle=c||'#aab';ctx.font='8.5px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm,ly);ly+=13;}
    function sm(t){ctx.fillStyle='#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+12,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a1a1a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        var items=[
            {l:'M','n':'Methanol','tip':'Osmol gap ↑↑; visual disturbance; retinal toxicity; treat: fomepizole'},
            {l:'U','n':'Uremia (renal failure)','tip':'BUN/Cr ↑; sulfates/phosphates accumulate; no osmol gap'},
            {l:'D','n':'DKA / Alcoholic / Starvation Ketosis','tip':'β-hydroxybutyrate ↑; ketones on UA; glucose ↑ in DKA'},
            {l:'P','n':'Propylene glycol / Propofol infusion','tip':'Osmol gap ↑; propofol >67 mcg/kg/min × >48h → PRIS'},
            {l:'I','n':'Isoniazid / Iron poisoning','tip':'INH: seizures + gap; Fe: GI→hepatic→cardiovascular stages'},
            {l:'L','n':'Lactic acidosis','tip':'Type A: hypoperfusion; Type B: metformin, thiamine def, mitochondrial'},
            {l:'E','n':'Ethylene glycol','tip':'Osmol gap ↑; calcium oxalate crystals in urine; renal failure'},
            {l:'S','n':'Salicylates (ASA toxicity)','tip':'Mixed: primary resp alkalosis + anion gap met acidosis; tinnitus'}
        ];
        items.forEach(function(it){
            ctx.fillStyle=_RE;ctx.font='bold 9px sans-serif';ctx.textAlign='left';
            ctx.fillText(it.l,lm,ly);
            ctx.fillStyle='#eebb88';ctx.font='bold 8px sans-serif';
            ctx.fillText(it.n,lm+12,ly);
            ctx.fillStyle='#889988';ctx.font='italic 7.5px sans-serif';
            ctx.fillText(it.tip,lm+12,ly+10);
            ly+=23;
        });
    } else if(sel===1){
        nt('NAGMA = Normal Anion Gap Metabolic Acidosis (Hyperchloremic)','#cc8844');
        nt('AG: 8–12 mEq/L (normal); Cl⁻ compensates for HCO₃ loss','#888');
        hr();
        nt('GI Bicarbonate LOSS:','#eebb88');
        sm('Diarrhea (most common) — massive HCO₃ loss in stool');
        sm('Ileostomy / intestinal fistula / biliary drainage');
        sm('Pancreatic fistula (pancreatic juice rich in HCO₃)');
        hr();
        nt('Renal Tubular Acidosis (RTA):','#eebb88');
        sm('Type 1 (Distal): cannot excrete H⁺ → urine pH > 5.5 despite acidosis; hypokalemia');
        sm('Type 2 (Proximal): cannot reabsorb HCO₃ → bicarb wasting; hypokalemia; Fanconi');
        sm('Type 4 (Hypoaldosteronism): HYPERKALEMIA + NAGMA; ACEi/ARB, DM, adrenal insuff');
        hr();
        nt('Iatrogenic / Drug-Induced:','#eebb88');
        sm('Large-volume Normal Saline (hyperchloremia → dilutes HCO₃, adds Cl⁻)');
        sm('Acetazolamide (blocks PCT HCO₃ reabsorption → bicarb wasting)');
        sm('Cholestyramine, toluene inhalation (rare)');
    } else {
        nt('Osmol Gap = Measured Osm − Calculated Osm','#66ddcc');
        nt('Calc Osm = 2×[Na] + BUN/2.8 + glucose/18  (+EtOH/4.6 if relevant)','#aab');
        sm('Normal osmol gap: < 10 mOsm/kg');
        hr();
        nt('Elevated Osmol Gap (> 10–20):','#cc8844');
        sm('Toxic alcohols: Methanol (>20 + HAGMA = call toxicology)');
        sm('Ethylene glycol (antifreeze) — renal failure + calcium oxalate crystals');
        sm('Isopropanol (no acidosis — metabolized to acetone, not acid)');
        sm('Mannitol accumulation (monitor q6h in ICP mgmt)');
        sm('Propylene glycol (propofol solvent, lorazepam IV solvent)');
        hr();
        nt('Critical pattern: HAGMA + elevated osmol gap = TOXIC ALCOHOL until proven otherwise','#cc4444');
        sm('Fomepizole (4-MP): antidote for methanol AND ethylene glycol toxicity');
        sm('Blocks alcohol dehydrogenase → prevents conversion to toxic acid metabolites');
        sm('Hemodialysis: removes parent alcohol AND acidic metabolites; use if severe');
        hr();
        nt('Normal osmol gap does NOT rule out toxic alcohol (gap may normalize after metabolism)','#888');
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

# ── Chart 4: 5-Step ABG Interpretation ───────────────────────────────────────
RF['blood_gas_steps'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var steps=[
        {step:'Step 1',param:'pH',normal:'7.35–7.45',
         rule:'< 7.35 = Acidosis\n> 7.45 = Alkalosis\n7.35–7.45 = Normal',
         tip:'Check for compensation:\nnormal pH with abnormal\nPaCO₂/HCO₃ = mixed disorder',c:'#cc4444'},
        {step:'Step 2',param:'PaCO₂',normal:'35–45 mmHg',
         rule:'↑ PaCO₂ > 45 = Resp Acidosis\n↓ PaCO₂ < 35 = Resp Alkalosis\nNormal = no primary resp disorder',
         tip:'Is PaCO₂ change SAME direction\nas pH? → Primary resp disorder\nOPPOSITE? → Compensation',c:'#4488cc'},
        {step:'Step 3',param:'HCO₃',normal:'22–26 mEq/L',
         rule:'↓ HCO₃ < 22 = Met Acidosis\n↑ HCO₃ > 26 = Met Alkalosis\nNormal = no primary met disorder',
         tip:'Is HCO₃ SAME direction as pH?\n→ Primary metabolic disorder\nOPPOSITE? → Compensation',c:'#3a9a5c'},
        {step:'Step 4',param:'Compensation',normal:'Per formula',
         rule:"Met Acidosis: PaCO₂=1.5×HCO₃+8±2\nMet Alkalosis: PaCO₂=0.7×HCO₃+21±2\nAcute RA: ΔHCO₃=0.1×ΔCO₂",
         tip:'Under/over-compensated\n= mixed disorder\nCheck delta-delta if HAGMA',c:'#cc8844'},
        {step:'Step 5',param:'Oxygenation',normal:'PaO₂ 80–100\nSpO₂ ≥95%',
         rule:'A-a gradient = PAO₂−PaO₂\nPAO₂=FiO₂×(760−47)−PaCO₂/0.8\nNormal A-a: age/4+4 mmHg',
         tip:'A-a gap > 20 mmHg:\nV/Q mismatch, shunt, diffusion\nNormal A-a: hypoventilation only',c:'#9060c0'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/steps.length);
    var xs=[4,60,135,215,390,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Step','Parameter','Normal','Interpretation Rule','Clinical Tip'];
    ctx.font='bold 8px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    steps.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=d.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=d.c;ctx.font='bold 8px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.step,(xs[0]+xs[1])/2,ry+rh/2+3);
        ctx.fillStyle='#eedd88';ctx.font='bold 8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.param,(xs[1]+xs[2])/2,ry+rh/2+3);
        ctx.fillStyle='#aabb88';ctx.font='8px sans-serif';ctx.textAlign='center';
        d.normal.split('\n').forEach(function(l,li){
            var n=d.normal.split('\n').length;
            ctx.fillText(l,(xs[2]+xs[3])/2,ry+rh/2+(li-(n-1)/2)*10);
        });
        ctx.fillStyle='#ccbbaa';ctx.font='7.5px sans-serif';ctx.textAlign='left';
        d.rule.split('\n').forEach(function(l,li){ctx.fillText(l,xs[3]+3,ry+rh/2-9+li*9);});
        ctx.fillStyle='#99aabb';ctx.font='7.5px sans-serif';ctx.textAlign='left';
        d.tip.split('\n').forEach(function(l,li){ctx.fillText(l,xs[4]+3,ry+rh/2-9+li*9);});
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
        var lbs=['pH','PaCO₂','HCO₃','Compensation','Oxygenation'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,steps[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 5: Clinical Acid-Base Scenarios ────────────────────────────────────
RF['clinical_acid_base'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Lactic Acidosis','Permissive Hypercapnia','Mixed Disorders'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a0a0a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#3a1a1a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?_RE:'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0808';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+14;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#88bbee';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+185,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a1a1a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('Type A Lactic Acidosis:','Tissue hypoperfusion','#cc4444','#ffaa88');
        nt('Causes: septic shock, cardiogenic shock, hemorrhage, mesenteric ischemia');
        nt('Mechanism: anaerobic glycolysis → pyruvate → lactate (not oxidized via TCA cycle)');
        hr();
        rw('Type B Lactic Acidosis:','No overt hypoperfusion','#cc8844','#ffcc88');
        nt('B1: Underlying disease (liver failure, malignancy, HIV)');
        nt('B2: Drugs/toxins (metformin*, thiamine deficiency, linezolid, NRTIs)');
        nt('  *Metformin-associated LA: rare, but risk ↑ with AKI/hepatic failure');
        nt('B3: Inborn errors of metabolism, mitochondrial disease');
        hr();
        rw('Lactate Targets:','','#eedd88');
        rw('Goal:','Lactate < 2 mmol/L (normal: < 2)','#aab','#eedd88');
        rw('Sepsis high risk:','Lactate ≥ 4 mmol/L → 30 mL/kg IVF, ICU, vasopressors','#aab','#ffaa88');
        hr();
        rw('Bicarbonate therapy:','pH < 7.10–7.15 ONLY (still controversial)','#cc4444','#eedd88');
        nt('Evidence: small benefit in renal failure; no mortality benefit in sepsis (BICAR-ICU trial)');
        nt('Risk: ↑ CO₂ production, ↑ intracellular acidosis, ↓ ionized Ca²⁺, fluid overload');
    } else if(sel===1){
        rw('Permissive Hypercapnia:','Intentional ↑ PaCO₂ in ARDS','#4488cc','#88ccff');
        nt('Goal: minimize ventilator-induced lung injury (VILI) by using low tidal volumes (6 mL/kg)');
        nt('PaCO₂ may rise to 45–70 mmHg (accept respiratory acidosis to protect lungs)');
        hr();
        rw('Target pH:','≥ 7.20 (minimum; some accept ≥ 7.15 briefly)','#aab','#eedd88');
        rw('Buffer if pH < 7.20:','NaHCO₃ IV OR THAM (tromethamine)','#aab','#eedd88');
        nt('THAM: buffers without increasing CO₂ production (unlike NaHCO₃ → CO₂ + H₂O)');
        hr();
        rw('CONTRAINDICATIONS to permissive hypercapnia:','','#cc4444');
        nt('1. ↑ ICP (TBI, stroke, post-craniotomy) — CO₂ = potent cerebral vasodilator');
        nt('   CO₂ ↑ → ↑ CBF → ↑ ICP → herniation risk; keep PaCO₂ 35–40 in ↑ ICP');
        nt('2. Pulmonary arterial hypertension — hypercapnia + acidosis → ↑ PVR → RV failure');
        nt('3. Severe right ventricular dysfunction — avoid acid-induced ↑ PVR');
        hr();
        nt('ARDSNet: 6 mL/kg IBW tidal volumes + permissive hypercapnia → 22% mortality ↓ vs 12 mL/kg');
    } else {
        rw('MIXED DISORDER RECOGNITION:','','#cc8844');
        nt('Mixed = two or more simultaneous PRIMARY acid-base disorders');
        hr();
        rw('Example 1: DKA + Vomiting','','#eebb88');
        nt('HAGMA from ketonemia (AG 30) + Met Alkalosis from vomiting');
        nt('Delta-delta: (30−12)/(24−18) = 18/6 = 3.0 → > 2.0 = concurrent met alkalosis');
        nt('HCO₃ 18 (should be ~6 if pure HAGMA; vomiting rescued HCO₃ toward normal)');
        hr();
        rw('Example 2: COPD + Loop Diuretics','','#eebb88');
        nt('Chronic resp acidosis (PaCO₂ 60, HCO₃ 33) + Met Alkalosis from furosemide');
        nt('pH may be normal (7.42) despite both disorders — compensation masks each');
        nt('Clue: HCO₃ 33 is too high even for chronic resp acidosis alone (ΔHCO₃=0.35×20=7 → expected 31)');
        hr();
        rw('Example 3: Sepsis Early','','#eebb88');
        nt('Met Acidosis (lactate) + Resp Alkalosis (sepsis-driven tachypnea)');
        nt('pH may be 7.38 (near normal) with PaCO₂ 28 and HCO₃ 16 → both disorders primary');
        nt('Clue: expected CO₂ for HCO₃ 16 = 1.5×16+8 = 32; measured 28 < 32 → extra hyperventilation');
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

# ── Cards ─────────────────────────────────────────────────────────────────────
CARDS = [
    # ═══ acid_base_map ════════════════════════════════════════════════════════
    (
        "On the acid-base map chart, metabolic acidosis shows pH _______, "
        "HCO3 < _______ mEq/L, and expected PaCO2 by Winter's formula = "
        "_______ × HCO3 + _______ ± 2.",

        "Metabolic acidosis: pH < 7.35; HCO₃ < 22 mEq/L\n"
        "| Winter's formula: expected PaCO₂ = 1.5 × HCO₃ + 8 ± 2\n"
        "| Example: HCO₃ = 10 → expected PaCO₂ = 1.5×10+8 = 23 ± 2 mmHg\n"
        "| Minimum achievable PaCO₂ ≈ 10–15 mmHg (physiologic limit of hyperventilation)\n"
        "→ CCRN KEY: Measured PaCO₂ > Winter's expected = concurrent respiratory acidosis "
        "(inadequate compensation, e.g., COPD patient with DKA). "
        "Measured PaCO₂ < Winter's expected = concurrent respiratory alkalosis "
        "(extra hyperventilation, e.g., sepsis-driven tachypnea + DKA).\n"
        "→ MASTERY NOTE: Winter's formula verifies whether the respiratory system is compensating "
        "appropriately. In metabolic acidosis, the drive is: low pH → stimulates medullary "
        "chemoreceptors → ↑ minute ventilation → ↓ PaCO₂ → raises pH toward normal.",

        'tier-review',
        _NM,
        DID['ref_acid_base'],
        'acid_base_map',
        '{"hi":0}',
        'chart-l1'
    ),
    (
        "The acid-base chart shows respiratory acidosis (chronic) compensates by "
        "raising HCO3 by _______ mEq/L per 10 mmHg rise in PaCO2 — "
        "compared to only _______ mEq/L per 10 mmHg in acute respiratory acidosis. "
        "This renal compensation takes _______ days to fully develop.",

        "Chronic respiratory acidosis: ΔHCO₃ = 0.35 × ΔPaCO₂ (~3.5 mEq/L per 10 mmHg)\n"
        "| Acute respiratory acidosis: ΔHCO₃ = 0.1 × ΔPaCO₂ (~1 mEq/L per 10 mmHg)\n"
        "| Renal compensation fully develops in 3–5 days\n"
        "| Maximum HCO₃ in chronic resp acidosis ≈ 38–40 mEq/L (renal retention limit)\n"
        "→ CCRN KEY: COPD exacerbation example: baseline PaCO₂ 60 (chronic, HCO₃ 33). "
        "Acute exacerbation raises PaCO₂ to 75 → acute-on-chronic. "
        "Expected HCO₃ = 33 + 0.1×15 = 34.5 (acute add-on). pH will still be very acidemic.\n"
        "→ MASTERY NOTE: Acute buffering (immediate, hours) = carbonate/hemoglobin buffers. "
        "Chronic renal compensation (3–5 days) = proximal tubule ↑ H⁺ secretion + "
        "↑ NH₄⁺ excretion + ↑ HCO₃ reabsorption. This is why COPD patients 'tolerate' "
        "PaCO₂ 60+ with near-normal pH — their kidneys have fully compensated.",

        'tier-high',
        _NM,
        DID['ref_acid_base'],
        'acid_base_map',
        '{"hi":2}',
        'chart-l2'
    ),
    (
        "On the acid-base map, respiratory alkalosis (chronic) lowers HCO3 by "
        "_______ mEq/L per 10 mmHg fall in PaCO2. "
        "Common ICU causes of respiratory alkalosis include _______, _______, and _______.",

        "Chronic respiratory alkalosis: ΔHCO₃ = 0.5 × ΔPaCO₂ (~5 mEq/L per 10 mmHg↓)\n"
        "| Acute: ΔHCO₃ = 0.2 × ΔPaCO₂ (~2 mEq/L per 10 mmHg↓)\n"
        "| Minimum HCO₃ in chronic resp alkalosis ≈ 12–15 mEq/L\n"
        "| Common ICU causes: sepsis (early, cytokine-driven tachypnea), pain/anxiety, "
        "pregnancy, liver failure (cirrhosis), mechanical overventilation, PE\n"
        "→ CCRN KEY: Early sepsis = respiratory alkalosis (compensatory hyperventilation for metabolic "
        "acidosis) PLUS metabolic acidosis from lactate = mixed disorder. "
        "pH may be near-normal but both primary disorders are present. "
        "Check: PaCO₂ 28, HCO₃ 16 — Winter's gives expected 32, measured 28 < 32 → extra alkalosis.\n"
        "→ MASTERY NOTE: Liver failure causes chronic resp alkalosis because ammonia and other "
        "toxins stimulate the respiratory center directly. Hepatic encephalopathy patients may "
        "have PaCO₂ 28–32 chronically with HCO₃ 18–20 — this is compensated, not crisis.",

        'tier-critical',
        _NM,
        DID['ref_acid_base'],
        'acid_base_map',
        '{"hi":3}',
        'chart-l3'
    ),

    # ═══ compensation_formulas ════════════════════════════════════════════════
    (
        "The compensation formulas chart shows Winter's formula: expected PaCO2 = "
        "_______ × HCO3 + _______ ± _______. "
        "If measured PaCO2 is HIGHER than the Winter's result, a concurrent "
        "_______ disorder is present.",

        "Winter's formula: expected PaCO₂ = 1.5 × HCO₃ + 8 ± 2\n"
        "| Measured PaCO₂ > expected → concurrent respiratory acidosis (inadequate ventilation)\n"
        "| Measured PaCO₂ < expected → concurrent respiratory alkalosis (excess hyperventilation)\n"
        "| Only applies to metabolic acidosis; not used for other primary disorders\n"
        "→ CCRN KEY: Clinical example: HCO₃ = 12 → Winter's expected PaCO₂ = 1.5×12+8 = 26. "
        "If PaCO₂ = 35 (measured > 26): patient has respiratory acidosis on top of met acidosis "
        "(COPD + DKA, or fatigue from compensating). "
        "If PaCO₂ = 18 (measured < 26): concurrent respiratory alkalosis (sepsis-driven).\n"
        "→ MASTERY NOTE: An easy shortcut: in pure met acidosis, the last 2 digits of pH "
        "approximately equal the PaCO₂ (e.g., pH 7.25 → PaCO₂ ~25). This quick check confirms "
        "adequate compensation before doing the full Winter's calculation.",

        'tier-review',
        _NM,
        DID['ref_acid_base'],
        'compensation_formulas',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the compensation chart, delta-delta ratio = (AG − _______) ÷ (_______ − HCO3). "
        "A ratio > _______ indicates a concurrent _______ "
        "in addition to the high-AG metabolic acidosis.",

        "Delta-delta = (AG − 12) / (24 − HCO₃)\n"
        "| < 0.4: pure NAGMA (no AG elevation beyond normal)\n"
        "| 0.4–1.0: mixed HAGMA + NAGMA (AG rises but HCO₃ drops more than expected)\n"
        "| 1.0–2.0: pure HAGMA (expected 1:1 relationship)\n"
        "| > 2.0: HAGMA + concurrent metabolic alkalosis (HCO₃ not as low as expected for the AG)\n"
        "→ CCRN KEY: DKA + vomiting example: AG = 30 (HAGMA). HCO₃ = 20. "
        "Delta-delta = (30−12)/(24−20) = 18/4 = 4.5 → WAY > 2. "
        "HCO₃ should be ~6 if pure HAGMA; the vomiting rescued it to 20. "
        "Clinical implication: correcting DKA will unmask the metabolic alkalosis.\n"
        "→ MASTERY NOTE: Corrected AG for albumin: if albumin = 2 g/dL (low in ICU patients), "
        "add 2.5×(4−2) = 5 to the calculated AG. Without correction, you may miss a true HAGMA "
        "because low albumin artificially lowers the measured AG.",

        'tier-high',
        _NM,
        DID['ref_acid_base'],
        'compensation_formulas',
        '{"sel":2}',
        'chart-l2'
    ),
    (
        "The compensation chart shows metabolic alkalosis compensation: "
        "expected PaCO2 = _______ × HCO3 + _______ ± 2. "
        "The maximum PaCO2 achievable through hypoventilation is approximately _______ mmHg, "
        "limited by the _______.",

        "Met alkalosis compensation: PaCO₂ = 0.7 × HCO₃ + 21 ± 2\n"
        "| Maximum compensatory PaCO₂ ≈ 55–60 mmHg (limited by hypoxic ventilatory drive)\n"
        "| Limited by: hypoxic drive — as PaCO₂ rises, PaO₂ falls → hypoxia stimulates ventilation\n"
        "| Alt formula: ΔPaCO₂ = 0.6 × ΔHCO₃\n"
        "→ CCRN KEY: Example: HCO₃ = 40 (severe met alkalosis from massive diuresis). "
        "Expected PaCO₂ = 0.7×40+21 = 49. Measured PaCO₂ = 49 → appropriate compensation. "
        "If PaCO₂ = 60 (> 49): concurrent respiratory acidosis (e.g., COPD + severe alkalosis).\n"
        "→ MASTERY NOTE: Treatment of metabolic alkalosis depends on 'chloride-responsive' vs "
        "'chloride-resistant': Cl-responsive (urine Cl < 20 mEq/L) = volume depletion, vomiting, "
        "diuretics → treat with saline + KCl. Cl-resistant (urine Cl > 20) = hyperaldosteronism, "
        "Cushing's, Bartter/Gitelman → address underlying cause.",

        'tier-critical',
        _NM,
        DID['ref_acid_base'],
        'compensation_formulas',
        '{"sel":0}',
        'chart-l3'
    ),

    # ═══ anion_gap ════════════════════════════════════════════════════════════
    (
        "On the anion gap chart, AG = Na − (_______ + _______). "
        "Normal AG is _______ mEq/L. "
        "In a patient with albumin 2 g/dL, the corrected AG adds _______ mEq/L "
        "to the measured value.",

        "AG = Na − (Cl + HCO₃) [Normal: 8–12 mEq/L]\n"
        "| Albumin correction: corrected AG = measured AG + 2.5 × (4.0 − albumin g/dL)\n"
        "| With albumin 2 g/dL: add 2.5×(4−2) = +5 mEq/L\n"
        "| Why: albumin carries a negative charge — low albumin lowers the 'unmeasured anion' baseline\n"
        "→ CCRN KEY: ICU patients are commonly hypoalbuminemic (critical illness, malnutrition). "
        "An AG of 12 with albumin 2 g/dL is actually corrected AG = 17 → HIGH AG metabolic acidosis "
        "was hiding. Always correct the AG before declaring it 'normal' in the ICU.\n"
        "→ MASTERY NOTE: The AG represents 'unmeasured anions' (albumin, phosphate, sulfate, lactate, "
        "ketones, organic acids). When an exogenous acid is added (DKA, lactic acidosis), "
        "it displaces HCO₃ and raises the AG. The mnemonic MUDPILES lists the high-AG causes.",

        'tier-review',
        _NM,
        DID['ref_acid_base'],
        'anion_gap',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The MUDPILES chart lists high-AG metabolic acidosis causes. "
        "M = _______, U = _______, D = _______, L = _______, E = _______, S = _______.",

        "MUDPILES — High Anion Gap Metabolic Acidosis:\n"
        "| M = Methanol (osmol gap ↑↑; visual toxicity; retinal damage)\n"
        "| U = Uremia (renal failure; sulfates/phosphates accumulate)\n"
        "| D = DKA / Alcoholic ketoacidosis / Starvation ketosis\n"
        "| P = Propylene glycol (propofol solvent) / Propofol infusion syndrome\n"
        "| I = Isoniazid / Iron poisoning\n"
        "| L = Lactic acidosis (Type A: hypoperfusion; Type B: metformin/thiamine)\n"
        "| E = Ethylene glycol (antifreeze; calcium oxalate crystals → renal failure)\n"
        "| S = Salicylates (mixed: resp alkalosis + HAGMA; tinnitus; tachypnea)\n"
        "→ CCRN KEY: Methanol and ethylene glycol both cause: HAGMA + elevated osmol gap. "
        "Treat with fomepizole (blocks alcohol dehydrogenase) + hemodialysis if severe. "
        "Isopropanol: osmol gap ↑ but NO metabolic acidosis (→ acetone, not acid).\n"
        "→ MASTERY NOTE: Salicylate toxicity produces a unique mixed pattern: "
        "direct CNS stimulation → respiratory alkalosis (primary) early; "
        "as toxicity progresses → high AG metabolic acidosis (salicylate, lactate) accumulates. "
        "Final picture: pH near normal with low PaCO₂ AND low HCO₃ — unmistakable pattern.",

        'tier-high',
        _NM,
        DID['ref_acid_base'],
        'anion_gap',
        '{"sel":0}',
        'chart-l2'
    ),
    (
        "The osmol gap chart shows calculated osmolality = 2×[Na] + BUN/_______ + glucose/_______. "
        "An osmol gap > _______ combined with a high-AG metabolic acidosis suggests _______. "
        "The antidote for both methanol and ethylene glycol toxicity is _______.",

        "Calculated Osm = 2×[Na] + BUN/2.8 + glucose/18 (+ EtOH/4.6 if ethanol present)\n"
        "| Osmol gap = measured Osm − calculated Osm [Normal: < 10 mOsm/kg]\n"
        "| Gap > 20 with HAGMA: toxic alcohol (methanol, ethylene glycol) until proven otherwise\n"
        "| Antidote: fomepizole (4-methylpyrazole) — blocks alcohol dehydrogenase\n"
        "| Hemodialysis: removes both parent alcohol and toxic metabolites in severe cases\n"
        "→ CCRN KEY: Methanol → formate (optic nerve damage → blindness). "
        "Ethylene glycol → oxalate → calcium oxalate crystals in urine → renal failure. "
        "Both require URGENT fomepizole. Ethanol (ethyl alcohol) competes for ADH as alternative "
        "if fomepizole unavailable — but fomepizole is preferred (more predictable).\n"
        "→ MASTERY NOTE: Normal osmol gap does NOT rule out toxic alcohol ingestion. "
        "The parent alcohol causes the osmol gap; once metabolized to toxic acids, "
        "the gap normalizes but HAGMA persists. Late presentation: HAGMA without osmol gap "
        "= worst prognosis (all alcohol converted to toxic metabolites).",

        'tier-critical',
        _NM,
        DID['ref_acid_base'],
        'anion_gap',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ blood_gas_steps ══════════════════════════════════════════════════════
    (
        "On the 5-step ABG chart, Step 1 assesses pH: acidosis < _______, "
        "alkalosis > _______. Step 2 identifies respiratory acidosis as PaCO2 > _______ mmHg "
        "and respiratory alkalosis as PaCO2 < _______ mmHg.",

        "Step 1 — pH: Acidosis < 7.35 | Alkalosis > 7.45 | Normal: 7.35–7.45\n"
        "| Step 2 — PaCO₂: Resp acidosis > 45 mmHg | Resp alkalosis < 35 mmHg\n"
        "| Determine: Is the PaCO₂ change in the SAME direction as the pH abnormality?\n"
        "  → Same direction = primary respiratory disorder\n"
        "  → Opposite direction = respiratory compensation for metabolic disorder\n"
        "→ CCRN KEY: Step 1 gives you 'acid or base'; Step 2 tells you if the lungs are the primary cause "
        "or are responding to a metabolic problem. The lungs compensate in minutes; "
        "the kidneys compensate in days. ABG interpretation must consider timeline.\n"
        "→ MASTERY NOTE: pH 7.38 with PaCO₂ 50 and HCO₃ 28 = mixed disorder (NOT simple comp). "
        "A PaCO₂ of 50 should cause acidosis, but HCO₃ of 28 is compensating too well → "
        "both chronic respiratory acidosis AND metabolic alkalosis are primary.",

        'tier-review',
        _NM,
        DID['ref_acid_base'],
        'blood_gas_steps',
        '{"hi":0}',
        'chart-l1'
    ),
    (
        "The ABG chart Step 4 checks compensation: in metabolic acidosis, if measured PaCO2 "
        "equals Winter's formula result, this confirms _______ compensation. "
        "If PaCO2 is BELOW the Winter's result, the patient has concurrent _______.",

        "Measured PaCO₂ = Winter's expected → appropriate (adequate) compensation only\n"
        "| Measured PaCO₂ > Winter's expected → concurrent respiratory acidosis (double-trouble)\n"
        "| Measured PaCO₂ < Winter's expected → concurrent respiratory alkalosis\n"
        "| 'Appropriate' compensation = NOT over-compensation; the body never fully corrects pH\n"
        "→ CCRN KEY: Step 4 is where you find mixed disorders. NEVER assume compensation is "
        "adequate without checking — in the ICU, concurrent respiratory failure commonly "
        "impairs the compensatory hyperventilation that metabolic acidosis requires.\n"
        "→ MASTERY NOTE: Important rule: COMPENSATION NEVER OVERCORRECTS pH. "
        "If pH is normal but both PaCO₂ and HCO₃ are abnormal in the expected direction, "
        "there must be two primary disorders (not just one with compensation). "
        "Example: pH 7.40, PaCO₂ 60, HCO₃ 36 = metabolic alkalosis + resp acidosis (COPD + diuretics).",

        'tier-high',
        _NM,
        DID['ref_acid_base'],
        'blood_gas_steps',
        '{"hi":3}',
        'chart-l2'
    ),
    (
        "On the ABG chart, Step 5 assesses oxygenation via A-a gradient = PAO2 − PaO2. "
        "An elevated A-a gradient (> _______ mmHg) indicates parenchymal dysfunction. "
        "A NORMAL A-a gradient with low PaO2 indicates _______ as the cause of hypoxemia.",

        "Normal A-a gradient ≈ age/4 + 4 mmHg (roughly < 15–20 on room air in young adults)\n"
        "| Elevated A-a (> 20 mmHg): V/Q mismatch, intrapulmonary shunt, diffusion impairment\n"
        "| Normal A-a with low PaO₂: hypoventilation is the sole cause (PaCO₂ will be elevated)\n"
        "| PAO₂ = FiO₂ × (760 − 47) − PaCO₂/0.8  [or: PAO₂ = FiO₂ × 713 − PaCO₂/0.8]\n"
        "→ CCRN KEY: Clinical differentiation of hypoxemia mechanisms:\n"
        "• Hypoventilation (normal A-a): sedation, NMB, neuromuscular — give more ventilation\n"
        "• V/Q mismatch (↑ A-a): PE, pneumonia, COPD — supplement O₂ improves\n"
        "• Shunt (↑ A-a, fails O₂): ARDS, pulmonary edema, large PNA — O₂ does NOT fully correct\n"
        "→ MASTERY NOTE: P/F ratio (PaO₂/FiO₂) is the ARDS diagnostic tool: "
        "ARDS criteria: P/F ≤ 300 (mild), ≤ 200 (moderate), ≤ 100 (severe). "
        "P/F ratio is faster than A-a gradient in clinical practice.",

        'tier-critical',
        _NM,
        DID['ref_acid_base'],
        'blood_gas_steps',
        '{"hi":4}',
        'chart-l3'
    ),

    # ═══ clinical_acid_base ═══════════════════════════════════════════════════
    (
        "The lactic acidosis chart shows Type A lactic acidosis results from _______. "
        "In sepsis, a lactate ≥ _______ mmol/L triggers fluid resuscitation and ICU admission. "
        "The BICAR-ICU trial showed bicarbonate therapy in lactic acidosis benefits pH only "
        "when pH < _______ AND AKI is _______.",

        "Type A lactic acidosis: tissue hypoperfusion (inadequate O₂ delivery → anaerobic)\n"
        "| Causes: septic shock, cardiogenic shock, hemorrhage, mesenteric ischemia, severe anemia\n"
        "| Sepsis Surviving Sepsis Campaign: lactate ≥ 4 mmol/L → 30 mL/kg IVF + vasopressors + ICU\n"
        "| Lactate ≥ 2 mmol/L: elevated; target < 2 with resuscitation\n"
        "| BICAR-ICU: NaHCO₃ benefits only when pH < 7.20 AND AKI stage 2–3 present\n"
        "→ CCRN KEY: Sodium bicarbonate risks in lactic acidosis:\n"
        "• Generates CO₂ (NaHCO₃ + H⁺ → Na⁺ + H₂O + CO₂↑) — worsens intracellular acidosis\n"
        "• ↓ Ionized calcium → cardiac depression\n"
        "• Fluid and sodium load → worsens edema\n"
        "→ MASTERY NOTE: Type B lactic acidosis — metformin: risk highest with AKI/hepatic failure. "
        "Mechanism: metformin inhibits mitochondrial complex I → impairs oxidative phosphorylation "
        "→ ↑ pyruvate → lactate. Hold metformin pre-procedure with contrast and in AKI.",

        'tier-review',
        _NM,
        DID['ref_acid_base'],
        'clinical_acid_base',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The permissive hypercapnia tab shows ARDS patients may tolerate PaCO2 up to "
        "_______ mmHg with pH ≥ _______. "
        "The primary contraindication is _______ because CO2 causes cerebral _______. "
        "THAM is preferred over NaHCO3 for buffering because it does not generate _______.",

        "ARDS permissive hypercapnia: PaCO₂ 45–70 mmHg acceptable; pH goal ≥ 7.20\n"
        "| Primary contraindication: elevated ICP (TBI, hemorrhagic stroke, post-craniotomy)\n"
        "| CO₂ = potent cerebral vasodilator → ↑ CBF → ↑ ICP → herniation risk\n"
        "| Target PaCO₂ 35–40 mmHg in ↑ ICP patients\n"
        "| THAM preferred if buffering needed: does NOT generate CO₂ (unlike NaHCO₃ + H⁺ → CO₂ + H₂O)\n"
        "→ CCRN KEY: ARDSNet protocol (NEJM 2000): 6 mL/kg IBW tidal volume vs 12 mL/kg → "
        "22% absolute mortality reduction. Accept PaCO₂ rise to protect lungs. "
        "PEEP titrated to FiO₂ per ARDSNet table (higher PEEP with higher FiO₂ need).\n"
        "→ MASTERY NOTE: Second contraindication: pulmonary arterial hypertension. "
        "Hypercapnia + acidosis → ↑ PVR → acute RV failure (cor pulmonale). "
        "In severe PAH patients requiring mechanical ventilation, maintain pH > 7.30 "
        "and avoid hypercarbia — the RV cannot tolerate the acute PVR increase.",

        'tier-high',
        _NM,
        DID['ref_acid_base'],
        'clinical_acid_base',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The mixed disorders tab shows a patient with DKA and 3 days of vomiting. "
        "The anion gap is 30. HCO3 is 20. "
        "Delta-delta = _______, indicating _______ is present in addition to the ketoacidosis. "
        "The expected HCO3 for this AG alone (without vomiting) would be _______.",

        "Delta-delta = (AG − 12) / (24 − HCO₃) = (30−12) / (24−20) = 18/4 = 4.5\n"
        "| Delta-delta > 2.0 = concurrent metabolic alkalosis (vomiting rescued HCO₃)\n"
        "| Expected HCO₃ for pure HAGMA with AG 30: 24 − (30−12) = 24 − 18 = 6 mEq/L\n"
        "| Measured HCO₃ 20 >> expected 6 → vomiting added ~14 mEq/L of metabolic alkalosis\n"
        "→ CCRN KEY: Clinical implication: as DKA resolves with insulin + fluids, "
        "the ketoacidosis clears (AG normalizes) but the metabolic alkalosis remains — "
        "pH may overshoot to alkalotic after DKA treatment. Monitor closely; avoid excess bicarb.\n"
        "→ MASTERY NOTE: COPD + furosemide = chronic resp acidosis + metabolic alkalosis. "
        "Both disorders are primary. pH 7.42 looks normal but PaCO₂ 60 AND HCO₃ 38 = "
        "compensatory rules broken (chronic RA should only raise HCO₃ to ~31; 38 is too high). "
        "The 'extra' HCO₃ came from diuretic-induced contraction alkalosis.",

        'tier-critical',
        _NM,
        DID['ref_acid_base'],
        'clinical_acid_base',
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
