#!/usr/bin/env python3
"""chunk44_charts.py — Ph7 Vasoactive Antihypertensives (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_43.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_44.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c44')
CHUNK_NUM   = 44
MID_BASE    = 1_800_005_065
CHART_ORDER = ['antihtn_comparison', 'hypertensive_crisis', 'nitroprusside_toxicity',
               'antihtn_by_scenario', 'bp_titration_targets']

_NM = 'Ph7 · \U0001f7e1 T3 · Pharmacology — Vasoactive Antihypertensives'

RF = {}

# ── Chart 1: IV Antihypertensive Comparison ───────────────────────────────────
RF['antihtn_comparison'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var drugs=[
        {name:'Nicardipine', mech:'Dihydropyridine CCB\n(arterial vasodilation)',onset:'5–15 min',dur:'30–40 min',best:'Ischemic stroke, post-op\nPost-SAH BP control',avoid:'HFrEF (neg inotropy)',c:'#4488cc'},
        {name:'Labetalol',   mech:'α1+β blocker (IV α:β=1:7)\n(combined HR + BP)',onset:'5–10 min',dur:'3–6 h',best:'Aortic dissection\nEclampsia, stroke',avoid:'Asthma, acute HF\n2nd/3rd AVB',c:'#3a9a5c'},
        {name:'Esmolol',     mech:'β1-selective blocker\n(ultra-short acting IV)',onset:'1–2 min',dur:'10–30 min',best:'Aortic dissection (HR)\nPost-op tachy+HTN',avoid:'Asthma, bradycardia\nDecomp HF',c:'#cc3333'},
        {name:'Clevidipine', mech:'Dihydropyridine CCB\n(ultra-short, arterial)',onset:'1–2 min',dur:'5–15 min',best:'Cardiac surgery post-op\nRapid fine titration',avoid:'Egg/soy allergy\nSevere AS',c:'#e07020'},
        {name:'Hydralazine',  mech:'Direct arteriolar\nvasodilator (variable)',onset:'15–30 min',dur:'2–6 h',best:'Eclampsia (if lab fails)\nPregnancy safe',avoid:'Aortic dissection\nIHD (reflex tachy)',c:'#9060c0'},
        {name:'Nitroprusside',mech:'NO donor: art+venous\nvasodilator (balanced)',onset:'<2 min',dur:'1–10 min',best:'HTN emerg + acute HF\nDissection (+esmolol)',avoid:'Renal/hepatic failure\n(CN⁻ toxicity risk)',c:'#cc6633'},
        {name:'Nitroglycerin',mech:'NO donor: venodilator\n(preload > afterload)',onset:'1–3 min',dur:'3–5 min',best:'ACS+HTN, acute HF\nPulmonary edema',avoid:'Severe AS, hypovolemia\nPDE-5 inhibitors',c:'#38b2a4'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/drugs.length);
    var xs=[4,110,240,300,365,490,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Drug','Mechanism','Onset','Duration','Best For','Avoid'];
    ctx.font='bold 8.5px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    drugs.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=d.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=d.c;ctx.font='bold 9px sans-serif';ctx.textAlign='left';
        ctx.fillText(d.name,xs[0]+3,ry+rh/2+3);
        ctx.fillStyle='#aab';ctx.font='8px sans-serif';
        d.mech.split('\n').forEach(function(ml,mi){ctx.fillText(ml,xs[1]+3,ry+rh/2-3+mi*9);});
        ctx.fillStyle='#ccc';ctx.font='8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.onset,(xs[2]+xs[3])/2,ry+rh/2+3);
        ctx.fillText(d.dur,(xs[3]+xs[4])/2,ry+rh/2+3);
        ctx.fillStyle='#9ab8aa';ctx.font='8px sans-serif';ctx.textAlign='left';
        d.best.split('\n').forEach(function(bl,bi){ctx.fillText(bl,xs[4]+3,ry+rh/2-3+bi*9);});
        ctx.fillStyle='#cc7766';ctx.font='8px sans-serif';
        d.avoid.split('\n').forEach(function(al,ai){ctx.fillText(al,xs[5]+3,ry+rh/2-3+ai*9);});
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
        var lbs=['Nicardipine','Labetalol','Esmolol','Clevidipine','Hydralazine','SNP','NTG'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,drugs[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: Hypertensive Crisis Classification ───────────────────────────────
RF['hypertensive_crisis'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Emergency vs Urgency','End-Organ Damage','BP Reduction Protocol'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a2a3a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#4488cc':'#555';ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0a1a';ctx.fillRect(4,panelY,W-8,panelH);
    var content=[
        [['HYPERTENSIVE EMERGENCY vs. URGENCY','',
          'Emergency = severe ↑BP + NEW/WORSENING END-ORGAN DAMAGE',
          '  → Requires IV antihypertensives; ICU admission',
          '  → End-organ damage is the defining feature, NOT the BP number',
          '','Urgency = severe ↑BP WITHOUT end-organ damage (asymptomatic)',
          '  → Oral antihypertensives over hours to days (outpatient or ED obs)',
          '  → Do NOT give IV antihypertensives (over-treatment risk)',
          '','Key: BP of 220/130 with no symptoms = urgency',
          '     BP of 175/110 with new confusion = emergency']],
        [['END-ORGAN DAMAGE — Hypertensive Emergency','',
          'NEUROLOGIC: encephalopathy (PRES), ischemic/hemorrhagic stroke,',
          '  hypertensive retinopathy (papilledema, flame hemorrhages)',
          '','CARDIAC: acute coronary syndrome (demand ischemia), acute HF',
          '  with pulmonary edema, aortic dissection (most time-critical)',
          '','RENAL: acute kidney injury, hematuria, proteinuria, oliguria',
          '  (malignant hypertension → fibrinoid necrosis of arterioles)',
          '','OTHER: eclampsia (seizures+HTN in pregnancy), microangiopathy']],
        [['BP REDUCTION PROTOCOL — Hypertensive Emergency','',
          'Phase 1 (first 1 hour): Reduce MAP by ≤25% (ceiling, NOT a target)',
          '  Example: MAP 160 → target MAP ≥120 (no lower than 25% reduction)',
          '  Rationale: chronic HTN shifts autoregulation rightward; rapid',
          '  reduction → cerebral ischemia in previously hypertensive patients',
          '','Phase 2 (2–6 hours): Target BP ≤160/100 mmHg',
          '','Phase 3 (24–48 hours): Normalize BP gradually if stable',
          '','Exceptions (immediate targets, skip Phase 1 ceiling):',
          '  Aortic dissection: SBP <120 ASAP (most aggressive)',
          '  Post-tPA stroke: <180/105; Eclampsia: treat if SBP ≥160']]
    ];
    var col=sel<content.length?content[sel][0]:[];
    var ly=panelY+13;
    col.forEach(function(line){
        if(line===''){ly+=4;return;}
        var isHead=(line.endsWith('Urgency')||line.endsWith('Emergency')||line.endsWith('Damage— Hypertensive Emergency')||line.startsWith('HYPERTENSIVE')||line.startsWith('END-ORGAN')||line.startsWith('BP REDUCTION'));
        var isSub=line.startsWith('  ');
        ctx.fillStyle=isHead?'#4488cc':(isSub?'#778899':'#bbb');
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

# ── Chart 3: Nitroprusside Toxicity ───────────────────────────────────────────
RF['nitroprusside_toxicity'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Mechanism & Risks','Toxicity Signs','Monitoring & Antidotes'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#2a1a0a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#3a2a1a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#cc6633':'#555';ctx.font=(sel===i?'bold ':'')+'9px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0a0a';ctx.fillRect(4,panelY,W-8,panelH);
    var content=[
        [['SODIUM NITROPRUSSIDE (SNP) — Mechanism & Toxicity Risk','',
          'SNP releases 5 CN⁻ ions per molecule on contact with hemoglobin',
          'CN⁻ inhibits cytochrome c oxidase (Complex IV, ETC)',
          '→ Aerobic metabolism blocked → cellular hypoxia → lactic acidosis',
          '→ Tissue hypoxia despite normal PaO₂ and SpO₂ (“paradox”)',
          '','Toxicity risk factors:',
          '  Dose >2 mcg/kg/min for >10 minutes',
          '  Renal failure (thiocyanate accumulation)',
          '  Hepatic failure (impaired CN⁻ detoxification)',
          '  Prolonged infusion (>72h), malnutrition (low thiosulfate)']],
        [['CYANIDE (CN⁻) vs THIOCYANATE (SCN⁻) TOXICITY','',
          'Cyanide toxicity (ACUTE — hours, life-threatening):',
          '  Lactic acidosis (high anion gap), ↑serum lactate',
          '  Tachyphylaxis (need ↑ dose for same BP effect)',
          '  Altered mental status, cardiovascular collapse',
          '  → STOP infusion immediately; give antidote',
          '','Thiocyanate toxicity (SUBACUTE — days/weeks, in renal failure):',
          '  Confusion, ataxia, tinnitus, psychosis, seizures',
          '  Serum thiocyanate >10 mg/dL = toxic (>20 = severe)',
          '  → Hemodialysis removes thiocyanate effectively']],
        [['SNP SAFE USE — Monitoring & Antidotes','',
          'Safe infusion: start 0.25–0.3 mcg/kg/min; max 10 mcg/kg/min (brief)',
          'Watch: dose >2 mcg/kg/min >10 min → check lactate',
          'Protect bag from light (photodecomposition ↑ CN⁻ release)',
          '','Antidotes (in order of priority):',
          '  1. Hydroxocobalamin (Cyanokit) 5 g IV ×15 min — FIRST-LINE',
          '     Chelates CN⁻ → cyanocobalamin (renally excreted); safe, fast',
          '     Note: turns urine/skin red-brown; may affect SpO₂ readings',
          '  2. Sodium thiosulfate 12.5 g IV — donor for CN⁻→SCN⁻ conversion',
          '  3. Sodium nitrite 300 mg IV — induces methemoglobin (use with caution:',
          '     contraindicated in CO poisoning or Hgb disorders)']]
    ];
    var col=sel<content.length?content[sel][0]:[];
    var ly=panelY+13;
    col.forEach(function(line){
        if(line===''){ly+=4;return;}
        var isHead=(line.startsWith('SODIUM')||line.startsWith('CYANIDE')||line.startsWith('SNP SAFE'));
        var isSub=line.startsWith('  ');
        var isKey=line.indexOf('FIRST-LINE')>=0||line.indexOf('STOP')>=0||line.indexOf('Cyanide')>=0||line.indexOf('Thiocyanate')>=0;
        ctx.fillStyle=isHead?'#cc6633':(isKey?'#ee4444':(isSub?'#7799aa':'#bbb'));
        ctx.font=isHead?'bold 9.5px sans-serif':'9px sans-serif';ctx.textAlign='left';
        ctx.fillText(line,10,ly);ly+=isHead?15:12;
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;';
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,'#cc6633',sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 4: Antihypertensive Selection by Clinical Scenario ──────────────────
RF['antihtn_by_scenario'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var scenarios=[
        {name:'Aortic Dissection',      c:'#cc3333'},
        {name:'Ischemic Stroke',         c:'#e07020'},
        {name:'Hemorrhagic Stroke',      c:'#cc6633'},
        {name:'Eclampsia',               c:'#38b2a4'},
        {name:'HTN Encephalopathy',      c:'#4488cc'},
        {name:'Post-Cardiac Surgery',    c:'#9060c0'}
    ];
    var s=scenarios[sel];
    var hdH=22;
    ctx.fillStyle=s.c+'22';ctx.fillRect(4,4,W-8,hdH);
    ctx.strokeStyle=s.c+'66';ctx.lineWidth=1;ctx.strokeRect(4,4,W-8,hdH);
    ctx.fillStyle=s.c;ctx.font='bold 10px sans-serif';ctx.textAlign='center';
    ctx.fillText(s.name,W/2,4+hdH-6);
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0a1a';ctx.fillRect(4,panelY,W-8,panelH);
    var content=[
        [['GOAL: SBP <120 mmHg AND HR <60 bpm (reduce aortic wall stress)','',
          'Step 1 — β-blocker FIRST (HR control before vasodilation):',
          '  Esmolol 500 mcg/kg IV bolus → infusion 50–200 mcg/kg/min',
          '  OR Labetalol 20 mg IV q10 min (has α+β; one agent achieves both)',
          '','Step 2 — Add vasodilator if SBP still >120 after HR <60:',
          '  Nitroprusside 0.25–0.5 mcg/kg/min, titrate slowly',
          '  OR Nicardipine infusion (avoids SNP toxicity concerns)',
          '  NEVER vasodilator alone → reflex tachycardia worsens shear stress',
          '','Type A (ascending): surgical emergency; medical Rx is bridging to OR',
          'Type B (descending): medical management is primary treatment']],
        [['BP TARGET: SBP <185/110 before tPA; <180/105 ×24h after tPA','',
          'Pre-tPA window: treat if BP >185/110 to allow tPA administration',
          '  Labetalol 10–20 mg IV push OR nicardipine infusion',
          '  If BP fails to come below 185/110 → do NOT give tPA',
          '','Without tPA: permissive hypertension policy',
          '  Treat ONLY if SBP >220 OR DBP >120',
          '  Lower by ≤15% over 24h (penumbra depends on collateral flow)',
          '  Exception: concurrent ACS, HF, or dissection → treat to that target',
          '','Post-tPA monitoring: BP check q15 min ×2h, then q30 min ×6h, q1h ×16h']],
        [['BP TARGET: SBP 140–160 mmHg (avoid aggressive lowering to <140)','',
          'ATACH-2 (2016): SBP <140 vs <180 — NO mortality benefit; more renal AEs',
          'INTERACT-2 (2013): SBP <140 reduced composite disability (2° endpoint only)',
          '','First-line agent: Nicardipine infusion (preferred for titratability)',
          '  Start 5 mg/h; titrate by 2.5 mg/h q5–15 min to target',
          '  Labetalol IV is acceptable alternative',
          '','Timing: hematoma expansion most likely in first 6h → BP control is urgent',
          'Avoid hypotension (SBP <100): worsens cerebral perfusion pressure',
          'Monitor q5–15 min in acute phase; q1h once target achieved']],
        [['TREAT if SBP ≥160 OR DBP ≥110 sustained ≥15 min (prevent ICH)','',
          'BP TARGET: SBP 140–155 mmHg; DBP 90–105 mmHg',
          '  Do NOT lower SBP <140 → uteroplacental perfusion at risk',
          '','First-line antihypertensives:',
          '  Labetalol 20 mg IV → repeat 40 mg, 80 mg q10 min (max 300 mg)',
          '  Hydralazine 5–10 mg IV q20 min (if labetalol unavailable/CI)',
          '  Nicardipine infusion (acceptable; preferred by some centers)',
          '','Magnesium sulfate: SEIZURE PROPHYLAXIS only (not antihypertensive)',
          '  Target Mg 4–7 mEq/L | Toxicity: loss DTR >7, resp dep >9, arrest >15',
          '  Antidote: Calcium gluconate 1 g IV over 10 min']],
        [['PRES — Posterior Reversible Encephalopathy Syndrome','',
          'Presentation: severe headache, confusion/AMS, visual disturbances',
          '  (blurred vision, cortical blindness), possible seizures',
          'MRI: T2/FLAIR hyperintensity in posterior parieto-occipital white matter',
          '  (vasogenic edema from loss of cerebrovascular autoregulation)',
          '','BP management: reduce MAP by ≤25% in first hour; then ≤160/100',
          '  Nicardipine or labetalol IV; avoid SNP (limited reflex control needed)',
          '','PRES vs ischemic stroke: PRES = symmetric posterior, reversible',
          '  Ischemic stroke = asymmetric, NOT reversed by BP lowering alone',
          '  This distinction CHANGES MANAGEMENT: PRES → lower BP; Stroke → permissive']],
        [['BP TARGET: SBP 100–140 mmHg in immediate post-op period','',
          'Most time-sensitive BP emergency after cardiac surgery:',
          '  Hypertension worsens graft anastomosis stress, increases bleeding risk',
          '  Hypotension impairs coronary and cerebral perfusion',
          '','First-line: Clevidipine infusion (ultra-short acting, arterial-selective)',
          '  Onset 1–2 min; off →5–15 min; ideal for tight post-CABG titration',
          '  Watch: lipid emulsion load if also on propofol (combined load)',
          '','Alternative: Nicardipine infusion (longer offset, acceptable)',
          '  Nitroglycerin: preferred if coronary spasm or graft occlusion concern',
          'Esmolol: add for rate control if HR driving hypertension (SVT, tachy)']]
    ];
    var col=sel<content.length?content[sel][0]:[];
    var ly=panelY+13;
    col.forEach(function(line){
        if(line===''){ly+=4;return;}
        var isHead=(line.startsWith('GOAL')||line.startsWith('BP TARGET')||line.startsWith('TREAT if')||line.startsWith('PRES')||line.startsWith('Most time'));
        var isSub=line.startsWith('  ');
        var isStep=line.startsWith('Step')||line.startsWith('First-line');
        ctx.fillStyle=isHead?s.c:(isStep?'#ddaa66':(isSub?'#8899aa':'#bbb'));
        ctx.font=isHead?'bold 9.5px sans-serif':'9px sans-serif';ctx.textAlign='left';
        ctx.fillText(line,10,ly);ly+=isHead?15:12;
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        scenarios.forEach(function(sc,i){(function(idx){var b=_mkB(sc.name.split(' ')[0]+(sc.name.split(' ')[1]?' '+sc.name.split(' ')[1]:''),sc.c,sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 5: BP Titration Targets by Diagnosis ────────────────────────────────
RF['bp_titration_targets'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var scenarios=[
        {name:'Aortic Dissection', treat:'Any elevation',target:'SBP <120',    tMin:80, tMax:120,thr:160,col:'#cc3333',
         detail:['Target SBP <120 mmHg AND HR <60 bpm','Esmolol → then nitroprusside or nicardipine','Most aggressive BP target of ALL HTN emergencies','β-blocker must precede vasodilator (prevent reflex tachy)']},
        {name:'Hemorrhagic Stroke',treat:'SBP >150',    target:'SBP 140–160',tMin:130,tMax:160,thr:200,col:'#cc6633',
         detail:['Target SBP 140–160 mmHg (current AHA guideline)','ATACH-2: SBP <140 gave no mortality benefit, ↑ renal AEs','Hematoma expansion risk highest in first 6 hours','Nicardipine preferred (titratable); labetalol acceptable']},
        {name:'Post-tPA Stroke',   treat:'SBP >180',    target:'SBP <180/105', tMin:100,tMax:180,thr:185,col:'#e07020',
         detail:['Maintain <180/105 mmHg for ≥24h after tPA administration','Monitor BP q15 min ×2h, then q30 min ×6h, then q1h ×16h','Labetalol 10 mg IV or nicardipine for values above threshold','Consistent elevation >180 may signal hemorrhagic transformation']},
        {name:'Ischemic Stroke\n(no tPA)',treat:'SBP >220',target:'≤15% first 24h',tMin:170,tMax:215,thr:220,col:'#e0c020',
         detail:['Permissive hypertension policy: treat ONLY if SBP >220 or DBP >120','Reduce by ≤15% over first 24h (preserve penumbra perfusion)','Lower targets worsen outcome — penumbra depends on collaterals','Exception: concurrent ACS/HF/dissection → treat to that target']},
        {name:'Eclampsia',         treat:'SBP ≥160\nDBP ≥110',target:'SBP 140–155',tMin:130,tMax:155,thr:160,col:'#38b2a4',
         detail:['Treat if SBP ≥160 OR DBP ≥110 sustained ≥15 min','Target SBP 140–155, DBP 90–105 (protect uteroplacental flow)','Labetalol first-line; hydralazine if labetalol unavailable','MgSO₄: seizure prophylaxis only (not antihypertensive)']},
        {name:'HTN Emergency\n(general)',treat:'MAP >130 +\nend-organ dmg',target:'↓MAP ≤25%/1h',tMin:110,tMax:160,thr:200,col:'#4488cc',
         detail:['Reduce MAP by ≤25% in first hour (ceiling, not target)','Phase 2 (2–6h): target BP ≤160/100 mmHg','Phase 3 (24–48h): normalize BP gradually','Over-reduction → cerebral ischemia (autoregulation shift in chronic HTN)']}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var titleH=14, barH=25, nSc=scenarios.length;
    var scaleY=titleH+barH*nSc;
    var detailY=scaleY+16;
    ctx.fillStyle='#333';ctx.font='bold 8.5px sans-serif';ctx.textAlign='center';
    ctx.fillText('IV ANTIHYPERTENSIVE — BP TITRATION TARGETS BY DIAGNOSIS',W/2,11);
    var labelW=118, barX=labelW+2, barW=W-labelW-10;
    var scaleMin=80, scaleMax=260;
    var toX=function(sbp){return barX+Math.round((sbp-scaleMin)/(scaleMax-scaleMin)*barW);};
    scenarios.forEach(function(s,ri){
        var ry=titleH+ri*barH;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.15:1;
        ctx.fillStyle=ri%2?'#0a0a12':'#0d0d1a';ctx.fillRect(0,ry,W,barH);
        ctx.fillStyle=s.col;ctx.font=(hi===ri?'bold ':'')+'8px sans-serif';ctx.textAlign='right';
        s.name.split('\n').forEach(function(nl,ni){
            ctx.fillText(nl,labelW-2,ry+barH/2-3+ni*10);
        });
        var bh=10, by=ry+barH/2-bh/2;
        ctx.fillStyle='#111';ctx.fillRect(barX,by,barW,bh);
        var x1=toX(s.thr), xEnd=toX(scaleMax);
        if(x1<barX+barW){ctx.fillStyle='#330000';ctx.fillRect(x1,by,Math.min(xEnd,barX+barW)-x1,bh);}
        ctx.fillStyle=s.col+'88';ctx.fillRect(toX(s.tMin),by,toX(s.tMax)-toX(s.tMin),bh);
        ctx.strokeStyle=s.col;ctx.lineWidth=1.5;ctx.strokeRect(toX(s.tMin),by,toX(s.tMax)-toX(s.tMin),bh);
        ctx.strokeStyle=s.col+'66';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(toX(s.thr),ry+2);ctx.lineTo(toX(s.thr),ry+barH-2);ctx.stroke();
        ctx.fillStyle=s.col;ctx.font='bold 7.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(s.target,toX(s.tMax)+3,ry+barH/2+3);
        ctx.globalAlpha=1;
    });
    ctx.fillStyle='#333';ctx.font='7.5px sans-serif';ctx.textAlign='center';
    [100,120,140,160,180,200,220,240].forEach(function(sbp){
        ctx.fillText(sbp,toX(sbp),scaleY+8);
        ctx.strokeStyle='#1a1a1a';ctx.lineWidth=0.5;
        ctx.beginPath();ctx.moveTo(toX(sbp),titleH);ctx.lineTo(toX(sbp),scaleY);ctx.stroke();
    });
    ctx.fillStyle='#444';ctx.font='7.5px sans-serif';ctx.textAlign='center';
    ctx.fillText('SBP (mmHg)',barX+barW/2,scaleY+18);
    ctx.fillStyle='#0a0a18';ctx.fillRect(4,detailY,W-8,H-detailY-2);
    if(hi>=0){
        var sc=scenarios[hi], ly=detailY+12;
        sc.detail.forEach(function(line,li){
            ctx.fillStyle=li===0?sc.col:'#aaa';ctx.font=li===0?'bold 9px sans-serif':'9px sans-serif';ctx.textAlign='left';
            ctx.fillText(line,8,ly);ly+=li===0?14:12;
        });
    } else {
        ctx.fillStyle='#444';ctx.font='9px sans-serif';ctx.textAlign='center';
        ctx.fillText('Click a scenario for BP target details and clinical notes',W/2,detailY+18);
        ctx.fillStyle='#2a2a3a';ctx.font='8px sans-serif';
        ctx.fillText('Green bar = target zone | Red zone = treat above threshold',W/2,detailY+32);
    }
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        var lbs=['Dissection','ICH','Post-tPA','Stroke-no tPA','Eclampsia','HTN Emerg'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,scenarios[idx].col,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Cards ─────────────────────────────────────────────────────────────────────
CARDS = [
    # ═══ antihtn_comparison ═══════════════════════════════════════════════════
    (
        "On the IV antihypertensive comparison chart, nicardipine is classified "
        "as a _______ CCB. It is the preferred IV agent for _______ because "
        "it does not negatively affect _______ or heart rate.",

        "Dihydropyridine calcium channel blocker (L-type Ca²⁺ channel blockade "
        "on vascular smooth muscle; minimal cardiac effect)\n"
        "| Preferred IV agent for: ischemic stroke (reduces BP without affecting "
        "cerebral autoregulation), post-operative hypertension, post-SAH BP control\n"
        "| Does not negatively affect renal function or heart rate "
        "(arterial-selective; no SA/AV node effect)\n"
        "→ CCRN KEY: Nicardipine vs. nimodipine: Nimodipine (oral) = post-SAH "
        "VASOSPASM PREVENTION (cerebrovascular selectivity). Nicardipine IV = "
        "post-SAH BP MANAGEMENT only. They are not interchangeable. "
        "Never use oral nifedipine (sublingual or bite-and-swallow) — rapid "
        "uncontrolled BP drop → ischemia.\n"
        "→ MASTERY NOTE: Nicardipine has longer offset than clevidipine (~30–40 min "
        "vs 5–15 min after stopping infusion). In rapid titration scenarios "
        "(post-CABG), clevidipine's shorter offset is preferred. For stroke, "
        "nicardipine's stability and renal safety make it the standard choice.",

        'tier-review',
        _NM,
        DID['vasoactive_antihtn'],
        'antihtn_comparison',
        '{"hi":0}',
        'chart-l1'
    ),
    (
        "The antihypertensive chart shows labetalol's IV α:β receptor ratio is "
        "_______. This dual blockade makes it ideal for aortic dissection "
        "because it reduces _______ simultaneously, preventing _______ "
        "that a pure vasodilator would cause.",

        "IV α:β ratio = 1:7 (7× more beta than alpha activity when given IV; "
        "oral form ratio = 1:3)\n"
        "| Reduces both heart rate (β-blockade) AND blood pressure (α-blockade) "
        "simultaneously\n"
        "| Prevents reflex tachycardia — pure vasodilators (hydralazine, "
        "nitroprusside) reflexively increase HR via baroreceptor response, "
        "which worsens aortic wall shear stress in dissection\n"
        "→ CCRN KEY: Aortic dissection sequence: HR control FIRST (esmolol "
        "or labetalol → target HR <60 bpm), THEN add vasodilator if SBP remains "
        ">120 mmHg. Never give vasodilator alone. Labetalol can achieve both "
        "goals with one agent; esmolol requires a separate vasodilator.\n"
        "→ MASTERY NOTE: Labetalol half-life in IV form ~5.5h. This limits its "
        "flexibility compared to esmolol (t½ ~9 min). For peri-operative "
        "dissection management where hemodynamic swings are common, esmolol "
        "+ nitroprusside allows independent titration of HR and BP.",

        'tier-high',
        _NM,
        DID['vasoactive_antihtn'],
        'antihtn_comparison',
        '{"hi":1}',
        'chart-l2'
    ),
    (
        "On the antihypertensive chart, clevidipine differs from nicardipine "
        "by being _______ acting (onset _______). It is formulated as a "
        "_______, making it contraindicated in patients with _______ allergy.",

        "Ultra-short acting (onset 1–2 min; offset 5–15 min after infusion stopped) "
        "vs nicardipine onset 5–15 min, offset 30–40 min\n"
        "| Formulated as a lipid emulsion (10% soybean oil with egg phospholipid "
        "— same vehicle as propofol)\n"
        "| Contraindicated in: egg allergy or soy allergy (lipid emulsion), "
        "severe aortic stenosis (afterload reduction is dangerous with fixed output)\n"
        "→ CCRN KEY: Clevidipine indications: (1) post-cardiac surgery perioperative "
        "hypertension (most common use); (2) any situation needing rapid, precise "
        "BP titration with quick reversibility. FDA-approved for perioperative "
        "hypertension. Not studied extensively in stroke — nicardipine is preferred there.\n"
        "→ MASTERY NOTE: Lipid load concern: clevidipine delivers ~0.2 g fat/mL. "
        "If the patient is simultaneously on propofol, monitor serum triglycerides. "
        "Propofol infusion syndrome risk increases with combined lipid load, "
        "particularly in prolonged ICU stays. Count total lipid calories in nutrition orders.",

        'tier-critical',
        _NM,
        DID['vasoactive_antihtn'],
        'antihtn_comparison',
        '{"hi":3}',
        'chart-l3'
    ),

    # ═══ hypertensive_crisis ══════════════════════════════════════════════════
    (
        "On the hypertensive crisis chart, hypertensive emergency is defined as "
        "severe BP elevation WITH _______. Hypertensive urgency is the same "
        "BP elevation WITHOUT _______, and is managed with _______ agents.",

        "Hypertensive emergency = severe BP elevation WITH new or worsening "
        "end-organ damage (the defining feature — not a specific BP number)\n"
        "| Hypertensive urgency = severe BP WITHOUT end-organ damage (asymptomatic)\n"
        "| Urgency managed with: oral antihypertensives, over hours to days — "
        "IV antihypertensives are not indicated and may cause harm (over-reduction)\n"
        "→ CCRN KEY: End-organ damage categories: Neurologic (encephalopathy/PRES, "
        "stroke), Cardiac (ACS, acute HF/pulmonary edema, aortic dissection), "
        "Renal (AKI, hematuria, proteinuria), Ophthalmic (papilledema, "
        "retinal hemorrhage — grade III/IV hypertensive retinopathy).\n"
        "→ MASTERY NOTE: Common CCRN trap: a patient with BP 200/120 and "
        "'no symptoms' — but the exam may give subtle clues (headache, blurred "
        "vision, chest tightness) that actually indicate end-organ damage. "
        "Always assess for ALL organ systems. The classification determines "
        "treatment setting (ICU vs. outpatient) and urgency.",

        'tier-review',
        _NM,
        DID['vasoactive_antihtn'],
        'hypertensive_crisis',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The hypertensive crisis chart shows the BP reduction protocol. "
        "In the first hour, MAP reduction must not exceed _______%. "
        "For a patient with initial MAP of 150 mmHg, the first-hour "
        "MAP floor is _______.",

        "Maximum first-hour MAP reduction: ≤25%\n"
        "| MAP 150 mmHg × (1 − 0.25) = 112.5 mmHg → floor is 112–113 mmHg\n"
        "| Rationale: chronic hypertension shifts the cerebral autoregulation "
        "curve rightward — rapid reduction to 'normal' BP causes cerebral ischemia "
        "in patients whose brain is 'used to' high pressures\n"
        "→ CCRN KEY: MAP calculation: MAP = (SBP + 2×DBP)/3. "
        "Phase 2 target: BP ≤160/100 mmHg over 2–6 hours. "
        "Phase 3: normalize over 24–48h. The 25% rule is a CEILING — actual "
        "reduction may be gentler for sensitive conditions (ischemic stroke, "
        "hypertensive encephalopathy).\n"
        "→ MASTERY NOTE: Exceptions that bypass the 25% ceiling rule: "
        "(1) Aortic dissection: target SBP <120 immediately regardless of initial BP; "
        "(2) Eclampsia: treat if SBP ≥160 to prevent intracranial hemorrhage; "
        "(3) Post-tPA stroke: keep below 185/110 before giving tPA, then <180/105 after. "
        "These conditions have evidence-based absolute targets that supersede the general rule.",

        'tier-high',
        _NM,
        DID['vasoactive_antihtn'],
        'hypertensive_crisis',
        '{"sel":2}',
        'chart-l2'
    ),
    (
        "On the hypertensive crisis chart, hypertensive encephalopathy is associated "
        "with the radiographic syndrome _______ (acronym). "
        "MRI shows _______ in the _______ white matter.",

        "PRES — Posterior Reversible Encephalopathy Syndrome\n"
        "| MRI: T2/FLAIR hyperintensity (vasogenic edema) in the posterior "
        "parieto-occipital white matter (predominantly)\n"
        "| Mechanism: severe hypertension overwhelms cerebral autoregulation → "
        "breakthrough hyperperfusion → vasogenic edema\n"
        "→ CCRN KEY: PRES clinical features: severe headache, confusion/altered "
        "mental status, visual disturbances (cortical blindness, visual field cuts), "
        "possible seizures. Treatment: BP reduction (≤25% MAP in 1h) is DEFINITIVE — "
        "edema is reversible with BP control. PRES can occur with non-hypertensive "
        "causes: cyclosporine/tacrolimus toxicity, eclampsia, sepsis.\n"
        "→ MASTERY NOTE: PRES vs. ischemic stroke distinction on CCRN: PRES = "
        "symmetric posterior, vasogenic edema, REVERSIBLE with BP treatment. "
        "Ischemic stroke = asymmetric, cytotoxic edema, NOT reversed by BP lowering "
        "(in fact, permissive HTN is preferred in ischemic stroke). Misclassifying "
        "PRES as stroke leads to permissive HTN → worsens edema. Misclassifying "
        "stroke as PRES leads to aggressive BP lowering → worsens infarction.",

        'tier-critical',
        _NM,
        DID['vasoactive_antihtn'],
        'hypertensive_crisis',
        '{"sel":1}',
        'chart-l3'
    ),

    # ═══ nitroprusside_toxicity ════════════════════════════════════════════════
    (
        "On the nitroprusside toxicity chart, each SNP molecule releases "
        "_______ CN⁻ ions. These inhibit _______ in the mitochondria, "
        "causing _______ despite normal SpO₂.",

        "5 CN⁻ ions per SNP molecule released on contact with hemoglobin\n"
        "| CN⁻ inhibits cytochrome c oxidase (Complex IV of the electron transport chain)\n"
        "| Causes lactic acidosis (tissue hypoxia despite normal SpO₂ and PaO₂) — "
        "cells cannot use oxygen aerobically → anaerobic metabolism → lactate\n"
        "→ CCRN KEY: Classic SNP toxicity presentation: patient appears well-oxygenated "
        "(pink skin, SpO₂ 98%) but has: elevated serum lactate, high anion gap "
        "metabolic acidosis, tachyphylaxis (escalating SNP doses needed for same "
        "BP effect), and altered mental status. The \"normal SpO₂ + metabolic "
        "acidosis\" pattern is the key diagnostic clue.\n"
        "→ MASTERY NOTE: CN⁻ vs SCN⁻ toxicity timing: Cyanide = ACUTE (hours), "
        "life-threatening, cardiovascular collapse. Thiocyanate = SUBACUTE "
        "(days to weeks), neurologic (confusion, ataxia, tinnitus, psychosis, seizures), "
        "occurs primarily in renal failure. Screen for thiocyanate in any patient "
        "on SNP >48h with renal impairment.",

        'tier-review',
        _NM,
        DID['vasoactive_antihtn'],
        'nitroprusside_toxicity',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The nitroprusside chart shows toxicity thresholds. "
        "Concern for CN⁻ toxicity arises at doses above _______ mcg/kg/min. "
        "The absolute maximum short-term infusion rate is _______. "
        "SNP bags must be protected from _______ to prevent toxicity.",

        "Concern threshold: >2 mcg/kg/min (monitor serum lactate)\n"
        "| Absolute maximum: 10 mcg/kg/min briefly (short-term rescue only)\n"
        "| Maximum total dose: 0.5 mg/kg/h for ≤10 min if truly required\n"
        "| Protect from: LIGHT — photodecomposition accelerates CN⁻ release; "
        "wrap SNP bags and tubing in opaque foil covers\n"
        "→ CCRN KEY: SNP safe use rules: (1) Start 0.25–0.3 mcg/kg/min; "
        "(2) Dose >2 mcg/kg/min >10 min → check serum lactate and consider "
        "sodium thiosulfate co-infusion; (3) Duration limit: avoid >72h; "
        "(4) High-risk patients: renal failure (SCN⁻ accumulates), hepatic failure "
        "(impaired rhodanese), malnutrition (low thiosulfate substrate).\n"
        "→ MASTERY NOTE: In modern ICU practice, SNP use has decreased significantly "
        "due to toxicity risk. Nicardipine and clevidipine are preferred for most "
        "hypertensive emergencies. SNP retains a niche for: hypertensive emergency "
        "+ acute HF (balanced art + venous vasodilation reduces both preload and "
        "afterload) and aortic dissection adjunct after HR controlled with esmolol.",

        'tier-high',
        _NM,
        DID['vasoactive_antihtn'],
        'nitroprusside_toxicity',
        '{"sel":0}',
        'chart-l2'
    ),
    (
        "On the toxicity chart, confirmed SNP-related CN⁻ toxicity is treated "
        "with _______ as the first-line agent. It works by _______. "
        "The correct dose is _______ given over _______.",

        "Hydroxocobalamin (Cyanokit) — FIRST-LINE for hemodynamically unstable "
        "CN⁻ toxicity\n"
        "| Mechanism: hydroxocobalamin directly chelates CN⁻ → forms cyanocobalamin "
        "(vitamin B₁₂), which is renally excreted; no harmful byproducts\n"
        "| Dose: 5 g IV infused over 15 minutes\n"
        "→ CCRN KEY: Three-agent antidote sequence:\n"
        "1. Hydroxocobalamin 5 g IV × 15 min — FIRST-LINE (safest, fastest)\n"
        "2. Sodium thiosulfate 12.5 g IV — provides sulfur to convert CN⁻ → "
        "thiocyanate via rhodanese enzyme (can combine with hydroxocobalamin)\n"
        "3. Sodium nitrite 300 mg IV — induces methemoglobin to compete for CN⁻ "
        "binding; avoid in CO poisoning or hemoglobin disorders\n"
        "IMMEDIATELY: STOP SNP infusion; give 100% O₂.\n"
        "→ MASTERY NOTE: Hydroxocobalamin side effect: turns urine, skin, and "
        "secretions dark red-brown (can last 24–48h). This is harmless but may "
        "interfere with pulse oximetry readings (false SpO₂ values). Notify "
        "ICU staff to not be alarmed, and confirm O₂ saturation with ABG "
        "rather than SpO₂ during the first 24h post-treatment.",

        'tier-critical',
        _NM,
        DID['vasoactive_antihtn'],
        'nitroprusside_toxicity',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ antihtn_by_scenario ══════════════════════════════════════════════════
    (
        "On the scenario selection chart, aortic dissection requires "
        "controlling _______ before adding a vasodilator. "
        "The first-line drug for HR control is _______; "
        "adding a vasodilator alone first would cause _______, worsening dissection.",

        "Heart rate must be controlled BEFORE adding a vasodilator\n"
        "| First-line HR control: Esmolol IV (β₁-selective; onset 1–2 min, "
        "offset 10–30 min — highly titratable)\n"
        "| Vasodilator alone → reflex tachycardia (baroreceptor response) → "
        "increased heart rate → greater aortic wall shear stress → "
        "propagates dissection\n"
        "→ CCRN KEY: Aortic dissection targets: HR <60 bpm AND SBP <120 mmHg. "
        "Sequence: (1) Esmolol to achieve HR <60; (2) Add nitroprusside or "
        "nicardipine if SBP >120. Alternative single-agent: labetalol "
        "(IV α:β=1:7; controls both HR and BP simultaneously).\n"
        "→ MASTERY NOTE: Type A vs Type B dissection: both require the same "
        "acute pharmacologic management. Type A (ascending aorta) → surgical "
        "emergency; pharmacologic Rx is BRIDGING to OR. Type B (descending "
        "aorta) → medical management is primary; surgery for complications "
        "(rupture, malperfusion syndrome, persistent pain). Assess end-organ "
        "perfusion: renal (Cr, UO), mesenteric (lactate, pain), spinal (neuro exam).",

        'tier-review',
        _NM,
        DID['vasoactive_antihtn'],
        'antihtn_by_scenario',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the scenario chart, eclampsia first-line IV antihypertensives are "
        "_______ and _______. The BP target to protect uteroplacental "
        "flow is SBP _______. Magnesium sulfate is given for "
        "_______, not BP control.",

        "First-line IV antihypertensives: Labetalol (20 mg IV, up to 80 mg boluses) "
        "AND/OR Hydralazine 5–10 mg IV q20 min (second choice)\n"
        "| BP target: SBP 140–155 mmHg (do NOT lower SBP below 140 — "
        "uteroplacental perfusion depends on adequate maternal MAP)\n"
        "| Magnesium sulfate: indication = SEIZURE PROPHYLAXIS (prevents eclamptic "
        "seizures); target serum Mg 4–7 mEq/L; it has minimal antihypertensive effect\n"
        "→ CCRN KEY: Magnesium toxicity progression (memorize in order):\n"
        "• DTR loss (knee/patellar reflex): Mg >7–9 mEq/L — FIRST SIGN\n"
        "• Respiratory depression: Mg >9–12 mEq/L\n"
        "• Cardiac arrest: Mg >15 mEq/L\n"
        "Antidote: Calcium gluconate 1 g IV over 10 min (reverses Mg toxicity)\n"
        "→ MASTERY NOTE: Nifedipine (oral) is also acceptable for acute BP control "
        "in eclampsia per some protocols. Nicardipine IV is used at many centers. "
        "Nitroprusside is RELATIVELY contraindicated in pregnancy (CN⁻ ions can "
        "cross placenta → fetal CN⁻ toxicity). Hydralazine's long, unpredictable "
        "duration makes titration difficult, explaining why labetalol is preferred.",

        'tier-high',
        _NM,
        DID['vasoactive_antihtn'],
        'antihtn_by_scenario',
        '{"sel":3}',
        'chart-l2'
    ),
    (
        "On the scenario chart, ischemic stroke patients eligible for tPA must "
        "have BP _______ before administration. After tPA, target BP is "
        "maintained at _______ for _______ hours to prevent hemorrhagic transformation.",

        "Pre-tPA BP requirement: <185/110 mmHg (treat if above this threshold "
        "before giving tPA; if cannot achieve <185/110, do NOT give tPA)\n"
        "| Post-tPA target: SBP <180 AND DBP <105 mmHg\n"
        "| Duration: maintain <180/105 for ≥24 hours after tPA administration\n"
        "→ CCRN KEY: Post-tPA BP monitoring protocol (AHA guideline):\n"
        "• q15 min × 2h after tPA initiation\n"
        "• q30 min × 6h\n"
        "• q1h × 16h (24h total intensive monitoring)\n"
        "Persistent SBP >180 despite treatment may indicate hemorrhagic transformation.\n"
        "→ MASTERY NOTE: Why 185/110 is the pre-tPA threshold: tPA disrupts "
        "clot lysis but also impairs hemostasis systemically. Very high BP + "
        "anticoagulated state = dramatically increased risk of symptomatic "
        "intracranial hemorrhage (sICH). ECASS III and NINDS data established "
        "these thresholds. The nurse's role: verify and document pre-tPA BP × 2 "
        "readings ≥5 min apart, then continue BP monitoring post-tPA per protocol.",

        'tier-critical',
        _NM,
        DID['vasoactive_antihtn'],
        'antihtn_by_scenario',
        '{"sel":1}',
        'chart-l3'
    ),

    # ═══ bp_titration_targets ═════════════════════════════════════════════════
    (
        "On the BP titration chart, the hemorrhagic stroke SBP target is "
        "_______. Two landmark trials shown are _______ (showed no benefit "
        "for <140) and _______ (showed secondary-endpoint benefit for <140).",

        "SBP target: 140–160 mmHg (current AHA/ASA guideline)\n"
        "| ATACH-2 (2016, NEJM): SBP <140 vs <180 — NO significant reduction "
        "in 90-day death or disability; intensive group had MORE renal adverse events\n"
        "| INTERACT-2 (2013, Lancet): SBP <140 reduced the composite of "
        "death or major disability (significant for secondary/ordinal endpoint, "
        "not primary binary endpoint); established trend toward benefit\n"
        "→ CCRN KEY: Current practice: target SBP 140–160 mmHg. "
        "Avoid SBP <130 (underperfusion risk). Avoid SBP >180 (hematoma expansion risk). "
        "Hematoma expansion occurs in 20–30% of ICH patients in the first 3–6h — "
        "each 10 mmHg ↑ SBP ≈ 9% ↑ expansion risk. BP control is the primary "
        "acute intervention to prevent expansion.\n"
        "→ MASTERY NOTE: Preferred agent for ICH: nicardipine infusion "
        "(smooth, titratable reduction; no reflex tachycardia). Labetalol acceptable. "
        "Avoid hydralazine (unpredictable duration, reflex tachycardia). "
        "Avoid SNP in ICH (may increase intracranial pressure through vasodilation).",

        'tier-review',
        _NM,
        DID['vasoactive_antihtn'],
        'bp_titration_targets',
        '{"hi":1}',
        'chart-l1'
    ),
    (
        "On the BP titration chart, the post-tPA ischemic stroke target shows "
        "SBP <_______/_______ maintained for _______ hours. "
        "A BP check frequency of every _______ minutes is required "
        "for the first two hours post-tPA.",

        "SBP <180 AND DBP <105 mmHg (post-tPA target)\n"
        "| Duration: ≥24 hours after tPA administration\n"
        "| BP check frequency: every 15 minutes × 2 hours\n"
        "| Then: q30 min × 6h, then q1h × 16h (24h total monitoring)\n"
        "→ CCRN KEY: If SBP >180 post-tPA: Labetalol 10 mg IV push (may repeat "
        "once); if not controlled, start nicardipine infusion. Inform provider of "
        "any sustained BP above threshold immediately. Neurologic checks q30 min "
        "post-tPA × 6h, then q1h × 16h (same schedule as BP).\n"
        "→ MASTERY NOTE: The post-tPA period is the ICU nurse's most intensive "
        "monitoring task in stroke care. The combination of lytic state + high BP "
        "= hemorrhagic transformation risk. Any sudden neurologic deterioration "
        "post-tPA: STOP tPA infusion (if still running), STAT head CT, notify "
        "team. Hemorrhagic transformation treatments include cryoprecipitate "
        "(restore fibrinogen), platelets, and TXA depending on severity.",

        'tier-high',
        _NM,
        DID['vasoactive_antihtn'],
        'bp_titration_targets',
        '{"hi":2}',
        'chart-l2'
    ),
    (
        "On the BP titration targets chart, the general hypertensive emergency "
        "protocol limits MAP reduction to ≤_______% in the first hour. "
        "If initial MAP is 160 mmHg, the minimum acceptable MAP at 60 minutes "
        "is _______. The Phase 2 BP target (2–6 hours) is _______.",

        "≤25% MAP reduction in the first hour (ceiling — do not lower more than this)\n"
        "| Minimum MAP at 60 min: 160 × (1 − 0.25) = 120 mmHg\n"
        "| Phase 2 target (2–6 hours): BP ≤160/100 mmHg\n"
        "| Phase 3 (24–48h): normalize BP gradually toward patient baseline\n"
        "→ CCRN KEY: Why ≤25%? In chronic hypertension, cerebral autoregulation "
        "is reset to a higher range (~110–180 mmHg MAP). Rapid reduction below "
        "this range causes: cerebral ischemia (watershed infarcts), AKI "
        "(renal autoregulation also impaired), and cardiac events. The 25% ceiling "
        "keeps MAP within the impaired autoregulation zone.\n"
        "→ MASTERY NOTE: Calculate MAP correctly: MAP = (SBP + 2×DBP)/3. "
        "Example: BP 230/140 → MAP = (230 + 280)/3 = 170 mmHg. "
        "25% reduction = target MAP ≥127.5 mmHg. Corresponding SBP depends on "
        "pulse pressure. Use arterial line for continuous MAP monitoring in "
        "severe hypertensive emergency — intermittent cuff BPs miss dynamic "
        "fluctuations during IV antihypertensive titration.",

        'tier-critical',
        _NM,
        DID['vasoactive_antihtn'],
        'bp_titration_targets',
        '{"hi":5}',
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
