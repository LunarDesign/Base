#!/usr/bin/env python3
"""chunk52_charts.py — Ph7 Pharmacology: Targeted Agents & Antidotes (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_51.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_52.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c52')
CHUNK_NUM   = 52
MID_BASE    = 1_800_005_105
CHART_ORDER = ['antidote_pairs', 'pulmonary_vasodilators', 'thrombolytics',
               'corticosteroids_icu', 'vasopressin_methylene']

_NM = 'Ph7 \U0001f7e1 T3 · Pharmacology — Targeted Agents & Antidotes'

RF = {}

# ── Chart 1: Antidote Pairs ───────────────────────────────────────────────────
RF['antidote_pairs'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var rows=[
        {n:'Opioids', ant:'Naloxone', dose:'0.4–2 mg IV\nq2–3 min prn\n(titrate RR)',
         mech:'μ-opioid\ncompetitive\nantagonist',
         note:'Short t½ 30–90 min — RE-NARCOTIZATION risk with long-acting opioids\nInfusion: 2/3 of effective reversal dose per hour; titrate to RR > 12\nDo NOT fully reverse: precipitates acute withdrawal (seizures, vomiting)',
         c:'#cc4444'},
        {n:'APAP\nToxicity', ant:'N-Acetyl\nCysteine\n(NAC)', dose:'150 mg/kg IV\nover 60 min\n→ 21-hr total',
         mech:'Replenishes\nglutathione;\nscavenges\nNAPQI',
         note:'Rumack-Matthew: treatment line = 150 mcg/mL at 4h post-ingestion\nMonitor: ALT/AST, INR, Cr q4–8h (hepatotoxicity trajectory)\nLate (> 24h): give NAC if LFTs elevated — benefit still present',
         c:'#cc8844'},
        {n:'Cyanide', ant:'Hydroxo-\ncobalamin\n(Cyanokit)', dose:'5 g IV over\n15 min',
         mech:'Binds CN⁻\n→ cyano-\ncobalamin\n(renal excr)',
         note:'Safe in smoke inhalation with CO (unlike sodium nitrite + CO = dangerous)\nExpect: red-pink urine (harmless dye) — document to avoid alarm\nSodium thiosulfate alternative: enhances CN→thiocyanate via rhodanese',
         c:'#9060c0'},
        {n:'Benzos', ant:'Flumazenil', dose:'0.2 mg IV/min\nmax 1 mg\n(rarely used)',
         mech:'Competitive\nGABA-A benzo\nsite blocker',
         note:'ICU CAUTION: precipitates seizures in benzo-dependent patients\nShort t½ 45–90 min — re-sedation expected (shorter than most benzos)\nPrefer intubation over flumazenil if airway at risk in ICU patients',
         c:'#4488cc'},
        {n:'Methanol /\nEthylene\nGlycol', ant:'Fomepizole\n(4-MP)', dose:'15 mg/kg IV\nthen 10 mg/kg\nq12h × 4',
         mech:'ADH inhibitor\n→ prevents\ntoxic metabol\nformation',
         note:'Elevated anion gap + osmol gap = suspect MeOH or ethylene glycol\nAdd HD if pH < 7.1, severe AKI, or very high serum level\nEthanol IV (target 100 mg/dL) = backup if fomepizole unavailable',
         c:'#3a9a5c'},
        {n:'Organo-\nphosphates', ant:'Atropine +\nPralidoxime\n(2-PAM)', dose:'Atropine 2–4 mg\nIV q5–10 min\n2-PAM 1–2 g IV',
         mech:'Atropine: mAChR\nantagonist\n2-PAM: AChE\nreactivator',
         note:'SLUDGE: salivation, lacrimation, urination, defecation, GI, emesis\nAtropine: titrate to DRY secretions (NOT HR or pupils) — large doses\n2-PAM EARLY: AChE "aging" irreversible after 24–48 h',
         c:'#e06060'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/rows.length);
    var xs=[4,95,185,255,345,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Poisoning','Antidote','Dose','Mechanism','ICU Notes / Monitoring'];
    ctx.font='bold 7.5px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    rows.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=d.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=d.c;ctx.font='bold 7px sans-serif';ctx.textAlign='left';
        d.n.split('\n').forEach(function(l,li){ctx.fillText(l,xs[0]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#88ccff';ctx.font='bold 7px sans-serif';
        d.ant.split('\n').forEach(function(l,li){ctx.fillText(l,xs[1]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#eedd88';ctx.font='6.5px sans-serif';
        d.dose.split('\n').forEach(function(l,li){ctx.fillText(l,xs[2]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#aaddaa';ctx.font='6.5px sans-serif';
        d.mech.split('\n').forEach(function(l,li){ctx.fillText(l,xs[3]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#99aabb';ctx.font='6px sans-serif';
        d.note.split('\n').forEach(function(l,li){ctx.fillText(l,xs[4]+2,ry+7+li*10);});
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
        var lbs=['Opioids','APAP','Cyanide','Benzos','MeOH/EG','Organo-PO4'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,rows[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: Pulmonary Vasodilators ──────────────────────────────────────────
RF['pulmonary_vasodilators'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Inhaled NO','Prostacyclins','PDE5 Inhibitors'];
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
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+175,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('Inhaled Nitric Oxide (iNO):','','#4488cc');
        hr();
        rw('Mechanism:','Diffuses into pulmonary vascular SMC → ↑ cGMP → vasodilation','#aab','#eedd88');
        rw('Effect:','Selective pulmonary vasodilation — NO systemic hypotension','#aab','#eedd88');
        rw('Dose:','1–40 ppm (start 10–20 ppm; titrate by SpO₂/PaO₂ response)','#aab','#eedd88');
        hr();
        rw('Indications:','','#cc8844');
        nt('ARDS with refractory hypoxemia (P/F < 100 on optimized LPV + PEEP)');
        nt('Right ventricular failure + pulmonary hypertension (post-cardiac surgery)');
        nt('Bridge to definitive therapy (ECMO candidacy, lung transplant workup)');
        hr();
        rw('Monitoring:','','#cc4444');
        nt('Methemoglobin: check q4–8h (NO + Hgb → metHgb); stop if > 5%');
        nt('NO₂ (nitrogen dioxide): toxic byproduct in circuit — monitor with inline detector');
        rw('Key limitation:','NO survival benefit in RCTs (improves oxygenation only temporarily)','#cc4444','#ff9966');
        hr();
        nt('★ Wean gradually: abrupt DC → rebound pulmonary hypertension (↑ PVR)');
    } else if(sel===1){
        rw('Inhaled Prostacyclins:','Epoprostenol (PGI₂) / Iloprost / Treprostinil','#4488cc','#88ccff');
        hr();
        rw('Mechanism:','PGI₂ analog → ↑ cAMP in pulmonary SMC → vasodilation + antiplatelet','#aab','#eedd88');
        rw('Route:','Inhaled via nebulizer — selective pulmonary effect (like iNO)','#aab','#eedd88');
        rw('Advantage over iNO:','No methemoglobin monitoring; no nitrogen dioxide generation','#3a9a5c','#eedd88');
        hr();
        rw('Epoprostenol IV (chronic PAH):','','#cc8844');
        nt('Continuous IV via dedicated central line (very short t½: 2–3 min)');
        nt('Abrupt discontinuation → life-threatening rebound pulmonary hypertension');
        nt('Monitor: systemic hypotension (IV route); fluid-restricted patients at risk');
        hr();
        rw('Treprostinil:','SC / IV / inhaled / oral — longer t½; easier wean than epoprostenol','#9060c0','#eedd88');
        hr();
        nt('★ Inhaled prostacyclins = clinical alternative to iNO in ARDS rescue therapy');
        nt('★ No survival benefit demonstrated; use as bridge to ECMO or transplant');
    } else {
        rw('PDE5 Inhibitors — Sildenafil / Tadalafil:','','#4488cc');
        hr();
        rw('Mechanism:','Inhibit PDE5 → ↑ cGMP in pulmonary SMC → vasodilation','#aab','#eedd88');
        nt('Work downstream of NO/cGMP pathway (same effector as iNO, different entry point)');
        rw('Sildenafil dose:','20 mg PO TID (approved PAH dose); IV formulation available','#aab','#eedd88');
        hr();
        rw('Indications:','','#3a9a5c');
        nt('Pulmonary arterial hypertension (PAH) — oral long-term therapy');
        nt('Weaning from inhaled NO (sildenafil prevents iNO rebound PH)');
        nt('Exercise tolerance in PAH — improves 6-minute walk distance');
        hr();
        rw('CRITICAL CI:','Concurrent nitrates (any route) — additive cGMP → severe hypotension','#cc4444','#ff6644');
        hr();
        rw('Riociguat:','sGC stimulator — similar mechanism; do NOT combine with PDE5i','#9060c0','#eedd88');
        hr();
        nt('★ Macitentan/ambrisentan: endothelin receptor antagonists — teratogenic; monitor LFTs');
        nt('★ Triple combination therapy (ERA + PDE5i + prostacyclin) → best PAH outcomes');
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

# ── Chart 3: Thrombolytics ────────────────────────────────────────────────────
RF['thrombolytics'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Massive PE','Submassive PE / STEMI','Absolute Contraindications'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#2a0a0a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#3a1a1a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#cc4444':'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0f0808';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+13;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#cc4444';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+175,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#3a1a1a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('Massive PE — Definition:','','#cc4444');
        nt('Acute PE + hemodynamic instability: SBP < 90 mmHg OR vasopressor-dependent OR cardiac arrest');
        hr();
        rw('Systemic Thrombolysis — Alteplase:','','#cc4444');
        rw('Standard dose:','100 mg IV over 2 hours (AHA/ACCP guideline)','#aab','#eedd88');
        rw('UFH during lysis:','HOLD heparin during infusion; restart WITHOUT bolus when aPTT < 80','#aab','#eedd88');
        rw('Success:','↑ SBP, ↑ SpO₂, ↓ RV strain on echo — reassess at 2h post-infusion','#aab','#eedd88');
        hr();
        rw('Catheter-Directed Thrombolysis (CDT):','','#3a9a5c');
        nt('Lower dose: 10–20 mg alteplase over 6–24h via pulmonary artery catheter');
        nt('Advantage: ↓ bleeding vs systemic; use for submassive or when systemic CI present');
        hr();
        rw('Surgical Embolectomy:','','#cc8844');
        nt('Massive PE + thrombolysis failed or contraindicated + surgical expertise available');
        nt('ECMO bridge: consider VA-ECMO for massive PE with refractory cardiac arrest');
    } else if(sel===1){
        rw('Submassive PE (Intermediate-Risk):','','#cc8844');
        nt('PE + RV dysfunction (echo RV/LV ratio > 0.9 or CT RV/LV > 1.0) but hemodynamically STABLE');
        hr();
        rw('PEITHO Trial (NEJM 2014):','','#cc8844');
        nt('Systemic thrombolysis (tenecteplase) vs anticoagulation alone in submassive PE');
        nt('Result: ↓ hemodynamic decompensation (5.6% vs 9.3%) — BUT ↑ major bleeding + ICH ≈ 2%');
        nt('ICH risk: ~2% with systemic lysis — unacceptable in most stable patients');
        nt('Current practice: CDT preferred over systemic lysis for submassive PE');
        hr();
        rw('STEMI Thrombolysis (when PCI > 120 min):','','#cc4444');
        nt('Alteplase: 15 mg IV bolus → 0.75 mg/kg over 30 min → 0.5 mg/kg over 60 min');
        nt('TNK (tenecteplase): weight-based single IV bolus; easier to administer');
        nt('Transfer to PCI center after lysis (pharmacoinvasive strategy within 3–24h)');
        hr();
        nt('★ STEMI + cardiogenic shock: PCI preferred over lysis even if time > 120 min');
    } else {
        rw('Absolute Contraindications to Thrombolysis:','','#cc4444');
        hr();
        rw('Intracranial:','Prior intracranial hemorrhage (any time in history)','#cc4444','#ff6644');
        rw('Intracranial:','Known intracranial AVM, neoplasm, or structural lesion','#cc4444','#ff6644');
        rw('Stroke:','Ischemic stroke within 3 months (within 3h: relative CI not absolute)','#cc4444','#ff6644');
        rw('Surgery:','Intracranial/spinal surgery or trauma within 3 months','#cc4444','#ff6644');
        rw('Bleeding:','Active internal bleeding (excluding menses)','#cc4444','#ff6644');
        rw('Aorta:','Suspected aortic dissection','#cc4444','#ff6644');
        hr();
        rw('Relative Contraindications (weigh risk vs benefit):','','#cc8844');
        nt('Ischemic stroke > 3 months ago | SBP > 180 mmHg at presentation');
        nt('Active peptic ulcer | Pregnancy | Non-compressible vascular puncture');
        nt('Recent major surgery (within 3 weeks) | Prolonged CPR (> 10 min)');
        hr();
        nt('★ In massive PE with imminent death: absolute CIs become RELATIVE — weigh against mortality');
        nt('★ ICH 0.5–1% with STEMI lysis; up to 2% with PE lysis (older, sicker population)');
    }
    if(ctrl){
        ctrl.innerHTML='';
        var crow=document.createElement('div');crow.style.cssText='display:flex;gap:6px;margin-top:6px;';
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,'#cc4444',sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });crow.appendChild(b);})(i);});
        ctrl.appendChild(crow);
    }
}
"""

# ── Chart 4: Corticosteroids in ICU ──────────────────────────────────────────
RF['corticosteroids_icu'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Septic Shock','ARDS','Stress Dose Steroids'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a1504':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a2508';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#cc9922':'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0905';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+13;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#cc9922';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+175,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a2508';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('Corticosteroids in Septic Shock — Major Trials:','','#cc9922');
        hr();
        rw('ADRENAL (NEJM 2018, n=3800):','','#4488cc');
        nt('Hydrocortisone 200 mg/day × 7 days vs placebo');
        nt('Result: faster shock reversal (56.9% vs 51.1% at Day 7); NO 90-day mortality benefit');
        hr();
        rw('APROCCHSS (NEJM 2018, n=1241):','','#3a9a5c');
        nt('Hydrocortisone 200 mg/day + fludrocortisone 50 mcg/day × 7 days');
        nt('Result: MORTALITY BENEFIT (43.0% vs 49.1% at 90 days, p=0.03)');
        nt('Key difference from ADRENAL: added fludrocortisone (mineralocorticoid component)');
        hr();
        rw('Clinical application (SSC 2021):','','#cc9922');
        rw('Trigger:','NE or Epi ≥ 0.25 mcg/kg/min despite adequate fluid resuscitation','#aab','#eedd88');
        rw('Regimen:','Hydrocortisone 200 mg/day IV (continuous or q6h dosing × 7 days)','#aab','#eedd88');
        hr();
        nt('★ SSC suggests (weak) using corticosteroids when hemodynamically unstable on vasopressors');
    } else if(sel===1){
        rw('Corticosteroids in ARDS — DEXA-ARDS Trial:','','#cc9922');
        hr();
        rw('DEXA-ARDS (Lancet RM 2020, n=299):','','#3a9a5c');
        nt('Enrolled: moderate–severe ARDS (P/F ≤ 200) despite LPV for ≥ 24h');
        nt('Regimen: dexamethasone 20 mg/day × 5d, then 10 mg/day × 5d (10 days total)');
        nt('Result: ↑ ventilator-free days (+4.8 days); ↓ 60-day mortality (21.1% vs 36.4%)');
        hr();
        rw('RECOVERY-COVID (NEJM 2020):','','#4488cc');
        nt('Dexamethasone 6 mg/day × 10 days in COVID-19 requiring respiratory support');
        nt('Result: ↓ 28-day mortality in ventilated patients (29% vs 41%)');
        nt('NO benefit in non-oxygen-requiring COVID-19 — potentially harmful');
        hr();
        rw('Mechanism:','↓ pro-inflammatory cytokines; ↓ pulmonary fibroproliferation','#aab','#eedd88');
        hr();
        nt('★ Dexamethasone preferred over methylprednisolone in ARDS (DEXA-ARDS data)');
        nt('★ Risks of prolonged steroids: hyperglycemia, secondary infection, ICUAW');
    } else {
        rw('Relative Adrenal Insufficiency in Shock:','','#cc9922');
        hr();
        rw('Diagnosis (SSC 2021 does NOT recommend routine testing):','','#aab');
        nt('Random cortisol < 15 mcg/dL (some institutions use < 18 mcg/dL threshold)');
        nt('Cosyntropin stimulation (250 mcg): delta cortisol < 9 mcg/dL = relative AI');
        nt('SSC 2021: give empirically when vasopressor-dependent — do not wait for test result');
        hr();
        rw('Stress Dose Regimen:','','#cc9922');
        rw('Hydrocortisone:','50 mg IV q6h OR 200 mg/day continuous infusion × 5–7 days','#aab','#eedd88');
        rw('Wean:','Taper with vasopressor wean — do not abruptly discontinue','#aab','#eedd88');
        hr();
        rw('Fludrocortisone:','50 mcg PO daily (add only if hydrocortisone < 300 mg/day)','#aab','#eedd88');
        hr();
        nt('★ Hydrocortisone has intrinsic mineralocorticoid activity at 200 mg/day doses');
        nt('★ Primary AI (Addisonian crisis): hydrocortisone 100 mg IV bolus, then 50–100 mg q6–8h');
    }
    if(ctrl){
        ctrl.innerHTML='';
        var crow=document.createElement('div');crow.style.cssText='display:flex;gap:6px;margin-top:6px;';
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,'#cc9922',sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });crow.appendChild(b);})(i);});
        ctrl.appendChild(crow);
    }
}
"""

# ── Chart 5: Vasopressin & Methylene Blue ────────────────────────────────────
RF['vasopressin_methylene'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Vasopressin','Terlipressin (HRS)','Methylene Blue'];
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
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+175,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('Vasopressin in Septic Shock:','','#9060c0');
        hr();
        rw('Fixed dose:','0.03–0.04 units/min IV — do NOT titrate above 0.04 u/min','#aab','#eedd88');
        rw('Role:','Add-on to NE for catecholamine-sparing when NE ≥ 20–25 mcg/min','#aab','#eedd88');
        hr();
        rw('Receptors:','','#cc8844');
        rw('V1 (VSMC):','Vasoconstriction — skin, skeletal muscle, splanchnic vasculature','#aab','#eedd88');
        rw('V2 (renal):','Antidiuretic — collecting duct water reabsorption (separate effect)','#aab','#eedd88');
        hr();
        rw('VASST Trial:','','#4488cc');
        nt('Vasopressin + NE vs NE alone — NO overall 90-day mortality benefit');
        nt('Subgroup: vasopressin benefit in less severe septic shock (NE < 15 mcg/min at baseline)');
        hr();
        rw('Risks at high dose (> 0.04 u/min):','','#cc4444');
        nt('Splanchnic ischemia | Digital ischemia | Hyponatremia (V2 dilutional effect)');
        hr();
        nt('★ ATHOS-3 trial: angiotensin II (GIAPREZA) — catecholamine-sparing in vasodilatory shock');
    } else if(sel===1){
        rw('Terlipressin — Hepatorenal Syndrome (HRS):','','#9060c0');
        hr();
        rw('Indication:','HRS-AKI (Type 1) — acute kidney injury in decompensated cirrhosis','#aab','#eedd88');
        rw('Mechanism:','V1 agonist → splanchnic vasoconstriction → ↑ renal perfusion pressure','#aab','#eedd88');
        hr();
        rw('CONFIRM Trial (NEJM 2021, n=300):','','#3a9a5c');
        nt('Terlipressin + albumin vs placebo + albumin in HRS-AKI');
        nt('Result: HRS reversal 32.4% vs 16.5% (p<0.001); FDA approved August 2022');
        nt('Reversal = SCr ≤ 1.5 mg/dL for ≥ 48h without RRT or death');
        hr();
        rw('Dosing:','1 mg IV q4–6h; ↑ to 2 mg q4–6h if SCr not ↓ 25% by 48h','#aab','#eedd88');
        rw('Duration:','Up to 14 days or until SCr < 1.5 mg/dL','#aab','#eedd88');
        hr();
        rw('Contraindications:','Ischemic heart disease, severe COPD, peripheral vascular disease','#cc4444','#ff9966');
        nt('Monitor respiratory status closely: albumin + terlipressin → fluid retention');
        hr();
        nt('★ Alternative: midodrine 12.5 mg PO TID + octreotide 200 mcg SQ TID + albumin');
    } else {
        rw('Methylene Blue — Vasoplegic Syndrome:','','#9060c0');
        hr();
        rw('Indication:','Distributive shock refractory to high-dose vasopressors','#aab','#eedd88');
        nt('Post-cardiac surgery (CPB → massive NO release → profound vasoplegia)');
        nt('Severe anaphylaxis refractory to epinephrine; protamine reactions');
        hr();
        rw('Mechanism:','','#cc8844');
        nt('Inhibits NOS (nitric oxide synthase) → ↓ NO production');
        nt('Inhibits guanylate cyclase directly → ↓ cGMP → ↑ vascular smooth muscle tone → ↑ SVR');
        hr();
        rw('Dose:','1–2 mg/kg IV over 15–60 min; repeat q4–6h or infusion 0.25–2 mg/kg/hr','#aab','#eedd88');
        hr();
        rw('Contraindications:','G6PD deficiency (hemolysis); severe renal failure','#cc4444','#ff9966');
        rw('Caution:','SSRIs / MAOIs → serotonin syndrome risk with methylene blue','#cc4444','#ff9966');
        hr();
        rw('Monitoring:','','#cc8844');
        nt('Pulse oximetry: FALSE LOW SpO₂ during infusion — blue dye absorbs at 668 nm');
        nt('Urine: turns blue-green (normal finding — document to prevent confusion)');
        hr();
        nt('★ Hydroxocobalamin (Cyanokit) also treats vasoplegic syndrome via NO scavenging');
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
    # ═══ antidote_pairs ═══════════════════════════════════════════════════════
    (
        "On the antidote chart, opioid toxicity is reversed with _______ at _______ mg IV every 2–3 minutes. "
        "Because its half-life is only _______ minutes, a continuous infusion of _______ of the "
        "effective reversal dose per hour is often needed to prevent _______.",

        "Naloxone (Narcan) — opioid reversal\n"
        "| Dose: 0.4–2 mg IV every 2–3 minutes, titrated to RR > 12/min (not full reversal)\n"
        "| Half-life: 30–90 minutes (shorter than most opioids, especially extended-release)\n"
        "| Infusion: 2/3 of the effective reversal dose per hour (prevents re-narcotization)\n"
        "| Goal: adequate respiratory rate — NOT full reversal (precipitates withdrawal)\n"
        "→ CCRN KEY: Opioid-induced respiratory depression = RR < 12, pinpoint pupils, decreased LOC. "
        "Naloxone in opioid-dependent patients: start with 0.04–0.1 mg titrated doses to avoid "
        "acute withdrawal (seizures, vomiting, hypertensive crisis, dysrhythmia). "
        "Re-narcotization risk is highest with long-acting agents: methadone (t½ 24–36h), "
        "oxycodone ER, fentanyl patches — monitor for 4–12h after reversal.\n"
        "→ MASTERY NOTE: After effective reversal, calculate naloxone infusion as 2/3 of the total "
        "dose needed to achieve reversal, given hourly (e.g., if 2 mg reversed the patient, "
        "infuse 1.3 mg/hr). Observe for at least 2× the expected opioid duration. "
        "Naloxone also available IM/intranasal (Narcan nasal spray 4 mg) — ICU uses IV route. "
        "Subcutaneous or SQ routes slower onset — use only if IV access unavailable.",

        'tier-review',
        _NM,
        DID['targeted_agents'],
        'antidote_pairs',
        '{"hi":0}',
        'chart-l1'
    ),
    (
        "The antidote chart shows APAP toxicity is treated with _______ (NAC). "
        "The Rumack-Matthew nomogram treatment threshold is _______ mcg/mL at _______ hours post-ingestion. "
        "The standard IV NAC protocol runs for _______ hours total, starting with _______ mg/kg over 60 min.",

        "N-Acetylcysteine (NAC) — acetaminophen (APAP) hepatotoxicity\n"
        "| Treatment threshold (Rumack-Matthew nomogram): 150 mcg/mL at 4 hours post-ingestion\n"
        "| IV protocol: 3-bag regimen totaling 21 hours\n"
        "  Bag 1: 150 mg/kg over 60 min (loading)\n"
        "  Bag 2: 50 mg/kg over 4 hours\n"
        "  Bag 3: 100 mg/kg over 16 hours\n"
        "| Late presentation (> 24h): give NAC if ALT/AST elevated — benefit persists\n"
        "→ CCRN KEY: APAP toxicity mechanism — toxic metabolite NAPQI accumulates when "
        "glutathione stores depleted (fasting, alcohol use, malnutrition = higher risk). "
        "Liver injury peaks at 72–96h. Monitor: ALT/AST, INR, Cr, total bilirubin q4–8h. "
        "King's College Criteria: pH < 7.3 OR INR > 6.5 + Cr > 3.4 + grade III-IV encephalopathy "
        "= consider transplant listing.\n"
        "→ MASTERY NOTE: Oral NAC (Mucomyst) = equivalent efficacy to IV — "
        "use IV when: vomiting prevents PO, altered mental status, fulminant hepatic failure. "
        "Adverse effect of rapid IV loading: anaphylactoid reaction (flushing, bronchospasm) — "
        "treat by slowing infusion rate (do NOT stop NAC — continue at reduced rate). "
        "NAC has benefits beyond glutathione replenishment: anti-inflammatory, "
        "improves microcirculatory flow — reason it helps even in late APAP toxicity.",

        'tier-high',
        _NM,
        DID['targeted_agents'],
        'antidote_pairs',
        '{"hi":1}',
        'chart-l2'
    ),
    (
        "The antidote chart shows cyanide poisoning is treated with _______ at _______ grams IV. "
        "This antidote is preferred over sodium nitrite in smoke inhalation because _______. "
        "Organophosphate toxicity requires _______ (titrated to _______, not heart rate) "
        "PLUS _______ to reactivate acetylcholinesterase — which must be given _______ to be effective.",

        "Cyanide poisoning → Hydroxocobalamin (Cyanokit): 5 g IV over 15 minutes\n"
        "| Preferred in smoke inhalation: safe with concurrent CO (sodium nitrite worsens CO toxicity)\n"
        "| Mechanism: binds CN⁻ → cyanocobalamin (non-toxic, renally excreted)\n"
        "| Expected side effect: red-pink urine — document to prevent alarm\n"
        "| Alternative: sodium thiosulfate (enhances CN→thiocyanate conversion via rhodanese)\n"
        "Organophosphate toxicity → Atropine + Pralidoxime (2-PAM):\n"
        "| Atropine: 2–4 mg IV every 5–10 min; titrate to DRY secretions (not HR or pupil size)\n"
        "| 2-PAM: 1–2 g IV; must give EARLY — AChE 'aging' becomes irreversible at 24–48h\n"
        "→ CCRN KEY: Organophosphate toxidrome — SLUDGE/DUMBELS:\n"
        "Salivation, Lacrimation, Urination, Defecation, GI upset, Emesis + bradycardia, miosis, bronchospasm. "
        "Atropine endpoint = DRY secretions + clear lung sounds — doses up to 20–100 mg may be needed. "
        "2-PAM prevents new ACh binding sites but cannot reverse 'aged' (covalently bound) AChE.\n"
        "→ MASTERY NOTE: Cyanide toxicity in smoke inhalation: consider if CO-poisoned patient "
        "fails to improve with 100% O₂ + lactate > 10 mmol/L. "
        "Sodium nitrite (alternative) forms methemoglobin to bind CN⁻ — DANGEROUS if CO present "
        "(metHgb + carboxyhgb = severely impaired O₂ carrying capacity). "
        "Flumazenil (benzo reversal): ICU caution — precipitates seizures in benzo-dependent patients; "
        "intubate rather than reverse in most ICU scenarios.",

        'tier-critical',
        _NM,
        DID['targeted_agents'],
        'antidote_pairs',
        '{"hi":-1}',
        'chart-l3'
    ),

    # ═══ pulmonary_vasodilators ═══════════════════════════════════════════════
    (
        "The pulmonary vasodilators chart shows inhaled NO works by entering pulmonary vascular SMCs "
        "and increasing _______, causing selective pulmonary vasodilation without _______. "
        "Dose range is _______ ppm. "
        "A critical monitoring parameter is _______ (check every 4–8 hours), "
        "and abrupt discontinuation causes _______.",

        "Inhaled NO (iNO) mechanism: diffuses into pulmonary vascular SMC → activates guanylate cyclase → ↑ cGMP → vasodilation\n"
        "| Selective: inactivated by Hgb before reaching systemic circulation — no systemic hypotension\n"
        "| Dose: 1–40 ppm (start 10–20 ppm; titrate to SpO₂/PaO₂ response)\n"
        "| Methemoglobin: NO + Hgb → metHgb; check q4–8h; stop if > 5%\n"
        "| Abrupt discontinuation → rebound pulmonary hypertension (wean gradually over hours)\n"
        "→ CCRN KEY: iNO indication — refractory hypoxemia in ARDS (P/F < 100 despite LPV + PEEP), "
        "RV failure with pulmonary hypertension, post-cardiac surgery PH crisis. "
        "iNO improves V/Q matching (selectively vasodilates ventilated alveolar units). "
        "Multiple RCTs (ARDS): NO survival benefit — temporary oxygenation improvement only. "
        "Use as bridge to ECMO or to allow time for LPV to work.\n"
        "→ MASTERY NOTE: Second monitoring parameter: NO₂ (nitrogen dioxide) — "
        "toxic byproduct when iNO reacts with O₂ in the ventilator circuit. "
        "Monitor with inline NO₂ detector; levels should be < 3 ppm. "
        "Cost: iNO is extremely expensive ($3,000–10,000/day). "
        "Inhaled epoprostenol = cost-effective alternative with equivalent effect and less monitoring burden. "
        "Methemoglobin > 5%: stop iNO; give methylene blue 1–2 mg/kg if symptomatic metHgb.",

        'tier-review',
        _NM,
        DID['targeted_agents'],
        'pulmonary_vasodilators',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the pulmonary vasodilators chart, inhaled prostacyclins (epoprostenol/iloprost) work by "
        "increasing _______ in pulmonary smooth muscle. "
        "The main advantage over iNO is _______. "
        "IV epoprostenol for chronic PAH requires _______ access due to its half-life of only _______. "
        "Abrupt discontinuation of IV epoprostenol causes _______.",

        "Inhaled prostacyclins mechanism: PGI₂ analog → activates adenylyl cyclase → ↑ cAMP → SMC relaxation\n"
        "| Selective pulmonary effect (inhaled route — equivalent to iNO)\n"
        "| Advantage over iNO: no methemoglobin monitoring; no NO₂ generation; lower cost\n"
        "| IV epoprostenol (chronic PAH): requires dedicated IV access (incompatible with most drugs)\n"
        "| Half-life: 2–3 minutes — requires continuous infusion; NO bolus dosing\n"
        "| Abrupt discontinuation → life-threatening rebound pulmonary hypertension\n"
        "→ CCRN KEY: Inhaled epoprostenol in ICU ARDS rescue:\n"
        "• Via nebulizer attached to ventilator circuit\n"
        "• Dose: 0.05 mcg/kg/min (5–50 ng/kg/min range)\n"
        "• Effect: ↑ SpO₂ within 30 min if vasodilator-responsive\n"
        "• If iNO is being weaned: overlap with inhaled prostacyclin to prevent rebound PH\n"
        "→ MASTERY NOTE: PAH drug classes — 3 pathways targeted:\n"
        "1. Prostacyclin pathway: epoprostenol, treprostinil, iloprost, selexipag\n"
        "2. Endothelin pathway: bosentan, ambrisentan, macitentan (teratogenic — REMS program)\n"
        "3. NO/cGMP pathway: sildenafil, tadalafil, riociguat\n"
        "Triple therapy (all 3 classes) → best 5-year outcomes in PAH (AMBITION, GRIPHON trials). "
        "Treprostinil: longer t½ than epoprostenol → SC/oral/inhaled routes; easier to wean.",

        'tier-high',
        _NM,
        DID['targeted_agents'],
        'pulmonary_vasodilators',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "On the PDE5 inhibitor chart, sildenafil inhibits _______, causing _______ accumulation "
        "in pulmonary smooth muscle, leading to vasodilation. "
        "The dose for approved PAH therapy is _______ mg PO _______. "
        "The critical drug interaction that is an absolute contraindication is _______.",

        "PDE5 inhibitors (sildenafil, tadalafil) mechanism: inhibit phosphodiesterase type 5 → ↑ cGMP\n"
        "| cGMP = downstream effector of NO pathway (same target as iNO, different entry point)\n"
        "| Approved PAH dose: sildenafil 20 mg PO TID (IV formulation available for NPO patients)\n"
        "| Absolute CI: concurrent nitrates (any route) — additive cGMP → severe hypotension\n"
        "→ CCRN KEY: Clinical uses of PDE5 inhibitors in ICU/cardiopulmonary:\n"
        "1. PAH long-term therapy (oral; improves 6-minute walk distance + exercise tolerance)\n"
        "2. Weaning from iNO: sildenafil prevents rebound PH when discontinuing iNO\n"
        "3. Bridge therapy in acute RV failure with PH (while escalating to prostacyclin)\n"
        "→ MASTERY NOTE: Riociguat (Adempas) — stimulates soluble guanylate cyclase (sGC):\n"
        "• Approved for PAH AND chronic thromboembolic PH (CTEPH) — unlike PDE5i\n"
        "• DO NOT combine with PDE5 inhibitors (same pathway → severe hypotension)\n"
        "• Also do NOT combine with nitrates or iNO\n"
        "Macitentan/ambrisentan (endothelin receptor antagonists): teratogenic — REMS program, "
        "monthly pregnancy testing required for female patients of childbearing potential. "
        "Monitor LFTs monthly (hepatotoxic class effect with ERA medications).",

        'tier-critical',
        _NM,
        DID['targeted_agents'],
        'pulmonary_vasodilators',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ thrombolytics ════════════════════════════════════════════════════════
    (
        "On the thrombolytics chart, massive PE is defined as acute PE plus _______. "
        "The standard alteplase dose is _______ mg IV over _______ hours. "
        "Heparin should be _______ during infusion and restarted WITHOUT a bolus when aPTT < _______.",

        "Massive PE definition: acute PE + hemodynamic instability\n"
        "| SBP < 90 mmHg OR vasopressor-dependent OR cardiac arrest\n"
        "| Alteplase standard dose: 100 mg IV over 2 hours\n"
        "| Heparin: HOLD during alteplase infusion; restart WITHOUT bolus when aPTT < 80\n"
        "→ CCRN KEY: Indication for systemic thrombolysis = massive PE (hemodynamically unstable). "
        "Do NOT give systemic lysis for submassive PE (intermediate-risk) unless imminent decompensation — "
        "bleeding risk (ICH ~2%) outweighs benefit in stable patients (PEITHO trial). "
        "Assessment after lysis: repeat echo at 2h — expect ↓ RV dilation, ↑ BP, ↑ SpO₂.\n"
        "→ MASTERY NOTE: Catheter-directed thrombolysis (CDT):\n"
        "• Dose: 10–20 mg alteplase over 6–24h via pulmonary artery catheter\n"
        "• Advantage: lower dose → lower bleeding risk vs systemic; preferred for submassive PE\n"
        "• Requires: interventional radiology suite; specialized catheter placement\n"
        "VA-ECMO for massive PE with refractory cardiac arrest:\n"
        "• Bridge to percutaneous thrombectomy or surgical embolectomy\n"
        "• Can also allow thrombolytics to work while maintaining cardiac output on ECMO\n"
        "Surgical embolectomy: consider when lysis fails or is absolutely contraindicated + "
        "surgical expertise and operating room immediately available.",

        'tier-review',
        _NM,
        DID['targeted_agents'],
        'thrombolytics',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the thrombolytics chart, the PEITHO trial studied thrombolysis in _______ PE — "
        "finding ↓ hemodynamic decompensation (5.6% vs 9.3%) but ↑ ICH risk of approximately _______%. "
        "For STEMI when PCI is not available within _______ minutes, alteplase is dosed as "
        "_______ mg bolus → _______ mg/kg over 30 min → _______ mg/kg over 60 min.",

        "PEITHO trial: systemic thrombolysis in SUBMASSIVE (intermediate-risk) PE\n"
        "| Definition: PE + RV dysfunction (echo or CT) but hemodynamically STABLE\n"
        "| Result: ↓ hemodynamic decompensation (5.6% vs 9.3%) — but ICH ≈ 2% with lysis\n"
        "| Conclusion: systemic lysis NOT recommended for submassive PE due to ICH risk\n"
        "| STEMI thrombolysis: when PCI not available within 120 minutes\n"
        "| Alteplase STEMI dose: 15 mg IV bolus → 0.75 mg/kg over 30 min (max 50 mg) → 0.5 mg/kg over 60 min (max 35 mg)\n"
        "→ CCRN KEY: STEMI + thrombolysis → transfer for pharmacoinvasive PCI within 3–24h. "
        "TNK (tenecteplase): weight-based single IV bolus; more fibrin-selective; easier to give. "
        "STEMI + cardiogenic shock: PCI preferred even if time > 120 min (lysis less effective in shock). "
        "Contraindication to lysis in STEMI: prior ICH, ischemic stroke within 3 months, suspected dissection.\n"
        "→ MASTERY NOTE: Submassive PE management algorithm:\n"
        "1. Anticoagulate (UFH preferred — can hold for procedures)\n"
        "2. Monitor closely (ICU, serial echo, vasopressor readiness)\n"
        "3. If deteriorates → CDT first (preferred over systemic lysis for submassive)\n"
        "4. Systemic lysis only if CDT not available AND imminent hemodynamic collapse\n"
        "RV dysfunction markers: RV/LV ratio > 0.9 on echo or CTA, BNP > 600, troponin elevation, "
        "right heart strain on ECG (S1Q3T3, new RBBB, sinus tachycardia).",

        'tier-high',
        _NM,
        DID['targeted_agents'],
        'thrombolytics',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The thrombolytics contraindications chart lists _______ as the only truly time-unlimited "
        "absolute contraindication. "
        "Ischemic stroke within _______ months is absolute. "
        "In massive PE with imminent death, absolute contraindications become _______, "
        "and the ICH risk with pulmonary thrombolysis is approximately _______.",

        "Absolute contraindications to thrombolysis:\n"
        "| Prior intracranial hemorrhage (ICH): ANY time — only time-unlimited absolute CI\n"
        "| Known intracranial AVM, neoplasm, or structural lesion\n"
        "| Ischemic stroke within 3 months (within 3h window: relative for ischemic stroke itself)\n"
        "| Intracranial or spinal surgery/trauma within 3 months\n"
        "| Active internal bleeding (not menses)\n"
        "| Suspected aortic dissection\n"
        "| In massive PE with imminent death: absolute CIs become RELATIVE — individualized risk-benefit\n"
        "| ICH risk with PE thrombolysis: ≈ 1.5–2% (higher than STEMI lysis ~0.5–1%)\n"
        "→ CCRN KEY: Relative contraindications:\n"
        "• SBP > 180 mmHg at presentation (control BP first if possible)\n"
        "• Recent surgery within 3 weeks OR non-compressible vascular puncture\n"
        "• Active peptic ulcer, pregnancy, prolonged CPR > 10 minutes\n"
        "• Ischemic stroke > 3 months ago (not absolute)\n"
        "→ MASTERY NOTE: The key clinical judgment in massive PE:\n"
        "A patient in cardiac arrest from massive PE has essentially 0% survival without intervention. "
        "A prior ICH (normally absolute CI) becomes a relative CI in this context — "
        "the risk of another ICH from lysis must be weighed against near-certain death without it. "
        "Document the shared decision-making process and rationale when overriding contraindications. "
        "Post-lysis monitoring: q15-min neuro checks × 2h, avoid invasive procedures for 24h, "
        "hold anticoagulation until aPTT < 80 (no bolus when restarting).",

        'tier-critical',
        _NM,
        DID['targeted_agents'],
        'thrombolytics',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ corticosteroids_icu ═════════════════════════════════════════════════
    (
        "The corticosteroids chart shows two major septic shock trials: "
        "ADRENAL found hydrocortisone _______ mg/day × 7 days caused faster shock reversal "
        "but _______ 90-day mortality benefit. "
        "APROCCHSS added _______ mcg/day of _______ and DID show mortality benefit (_______ vs _______%). "
        "The SSC trigger for steroids is NE or Epi ≥ _______ mcg/kg/min.",

        "ADRENAL (NEJM 2018, n=3,800): hydrocortisone 200 mg/day × 7 days\n"
        "| Faster vasopressor cessation: 56.9% vs 51.1% at Day 7\n"
        "| NO 90-day mortality benefit (27.9% vs 28.8%)\n"
        "APROCCHSS (NEJM 2018, n=1,241): hydrocortisone 200 mg/day + fludrocortisone 50 mcg/day × 7 days\n"
        "| MORTALITY BENEFIT: 43.0% vs 49.1% at 90 days (p=0.03)\n"
        "| Key difference: fludrocortisone (mineralocorticoid) added to hydrocortisone\n"
        "| SSC trigger: NE or Epi ≥ 0.25 mcg/kg/min despite adequate fluid resuscitation\n"
        "→ CCRN KEY: Why do the two trials disagree? Key differences:\n"
        "1. APROCCHSS added fludrocortisone (50 mcg/day PO) — mineralocorticoid augmentation\n"
        "2. ADRENAL used hydrocortisone ALONE — no mineralocorticoid\n"
        "3. ADRENAL was larger and better powered → null result more reliable?\n"
        "4. SSC 2021: weak recommendation for steroids in vasopressor-dependent septic shock\n"
        "→ MASTERY NOTE: Hydrocortisone 200 mg/day has inherent mineralocorticoid activity — "
        "may explain why fludrocortisone adds marginal benefit at this dose. "
        "At lower hydrocortisone doses (< 100 mg/day), fludrocortisone supplementation more important. "
        "Monitoring on steroids: glucose q4–6h (hyperglycemia common), secondary infection surveillance. "
        "Do NOT abruptly stop — taper with vasopressor wean over days to prevent rebound shock.",

        'tier-review',
        _NM,
        DID['targeted_agents'],
        'corticosteroids_icu',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the corticosteroids chart, the DEXA-ARDS trial used dexamethasone _______ mg/day × 5 days "
        "then _______ mg/day × 5 days in patients with P/F ≤ _______ for ≥ 24 hours. "
        "The results showed _______ more ventilator-free days and 60-day mortality of _______ vs _______%. "
        "The RECOVERY-COVID trial showed dexamethasone _______ mg/day × 10 days reduced mortality in "
        "ventilated COVID patients from _______ to _______.",

        "DEXA-ARDS (Lancet Respir Med 2020, n=299):\n"
        "| Enrolled: moderate–severe ARDS (P/F ≤ 200 mmHg) despite LPV for ≥ 24h\n"
        "| Regimen: dexamethasone 20 mg/day × 5d → 10 mg/day × 5d (10 days total)\n"
        "| Results: +4.8 ventilator-free days; 60-day mortality 21.1% vs 36.4%\n"
        "RECOVERY-COVID (NEJM 2020):\n"
        "| Dexamethasone 6 mg/day × 10 days in COVID-19 requiring respiratory support\n"
        "| Ventilated patients: mortality 29% vs 41% (28-day)\n"
        "| Oxygen-only patients: mortality benefit present (23% vs 26%)\n"
        "| NO benefit (possibly harmful) in non-oxygen-requiring COVID-19\n"
        "→ CCRN KEY: Mechanism in ARDS: "
        "↓ pro-inflammatory cytokines (TNF-α, IL-6, IL-1β) AND ↓ pulmonary fibroproliferation. "
        "Steroids address the LATE exudative/fibroproliferative phase of ARDS. "
        "DEXA-ARDS excluded patients who already received corticosteroids — "
        "don't count pre-hospital or ED dexamethasone toward ARDS treatment.\n"
        "→ MASTERY NOTE: Dexamethasone vs methylprednisolone in ARDS:\n"
        "• DEXA-ARDS specifically studied dexamethasone — guideline preference\n"
        "• Methylprednisolone (ARDS pilot trials): similar benefit but less evidence\n"
        "• Dexamethasone advantage: longer t½ (36–72h) → once-daily dosing; no mineralocorticoid activity\n"
        "Risks of prolonged steroids in ICU: hyperglycemia (BG target 140–180), "
        "secondary infections (fungal surveillance), ICUAW acceleration (minimize NMB if using steroids).",

        'tier-high',
        _NM,
        DID['targeted_agents'],
        'corticosteroids_icu',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The stress dose steroids chart shows the SSC _______ recommends routine cortisol testing "
        "before initiating steroids. "
        "A random cortisol < _______ mcg/dL or cosyntropin stimulation delta < _______ mcg/dL "
        "suggests relative adrenal insufficiency. "
        "The stress dose regimen is hydrocortisone _______ mg every _______ hours or _______ mg/day continuous. "
        "Steroids should be weaned with _______.",

        "SSC 2021: does NOT recommend routine cortisol testing — give empirically when vasopressor-dependent\n"
        "| Relative adrenal insufficiency criteria (if tested):\n"
        "  Random cortisol < 15 mcg/dL (some use < 18 mcg/dL)\n"
        "  Cosyntropin stimulation 250 mcg: delta cortisol < 9 mcg/dL\n"
        "| Stress dose regimen: hydrocortisone 50 mg IV q6h OR 200 mg/day continuous infusion × 5–7 days\n"
        "| Wean: taper in parallel with vasopressor wean — do NOT abruptly discontinue\n"
        "→ CCRN KEY: Stress dose steroids vs. physiologic replacement:\n"
        "• 'Stress dose' = supraphysiologic dose (200 mg/day hydrocortisone)\n"
        "• Normal cortisol production: 25–30 mg/day (baseline) → 300 mg/day (maximal stress)\n"
        "• ICU stress dose bridges the adrenal insufficiency-vasopressor dependence cycle\n"
        "• Goal: allow vasopressor weaning — NOT treating an absolute deficiency in most cases\n"
        "→ MASTERY NOTE: Primary adrenal insufficiency (Addisonian crisis) — different protocol:\n"
        "• Loading dose: hydrocortisone 100 mg IV bolus (or dexamethasone 4 mg if cortisol test pending)\n"
        "• Then: 50–100 mg IV q6–8h\n"
        "• Add fludrocortisone 0.1 mg daily for mineralocorticoid replacement\n"
        "• Trigger: precipitating event (infection, surgery, trauma) in patient with known AI or adrenal anatomy\n"
        "Hydrocortisone 200 mg/day has mineralocorticoid activity — "
        "fludrocortisone supplementation only needed if dose < 100 mg/day.",

        'tier-critical',
        _NM,
        DID['targeted_agents'],
        'corticosteroids_icu',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ vasopressin_methylene ════════════════════════════════════════════════
    (
        "The vasopressin chart shows it is dosed at _______ units/min as a FIXED dose — "
        "it is NOT _______. "
        "Its V1 receptor causes _______ in skin, muscle, and splanchnic vessels. "
        "The VASST trial showed _______ vs norepinephrine alone in septic shock. "
        "The maximum dose limit is _______ units/min to avoid _______.",

        "Vasopressin dosing: 0.03–0.04 units/min IV — fixed rate, NOT titrated\n"
        "| Role: add-on to norepinephrine for catecholamine-sparing (when NE ≥ 20–25 mcg/min)\n"
        "| V1 receptors (vascular): vasoconstriction — skin, skeletal muscle, splanchnic vasculature\n"
        "| V2 receptors (renal): antidiuretic hormone effect on collecting duct\n"
        "| VASST trial: vasopressin + NE vs NE alone → NO overall 90-day mortality benefit\n"
        "  Subgroup benefit: less severe septic shock (NE < 15 mcg/min at baseline)\n"
        "| Max dose: 0.04 units/min — higher doses risk splanchnic/digital ischemia\n"
        "→ CCRN KEY: Why is vasopressin not titrated? "
        "At doses > 0.04 u/min: splanchnic ischemia (gut, liver), digital ischemia, "
        "profound hyponatremia (V2 effect on renal water reabsorption). "
        "Vasopressin is used for catecholamine-sparing — to allow NE dose reduction, "
        "reducing adrenergic side effects (arrhythmia, ischemia, metabolic effects).\n"
        "→ MASTERY NOTE: ATHOS-3 trial — angiotensin II (Giapreza):\n"
        "• New vasopressor for catecholamine-refractory vasodilatory shock\n"
        "• Dose: 20 ng/kg/min to 40 ng/kg/min IV (different units from vasopressin!)\n"
        "• Mechanism: RAAS activation → AT1 receptor → vasoconstriction\n"
        "• FDA approved 2017 for high-output distributive shock\n"
        "• Monitor: DVT risk (venous thromboembolism prophylaxis required).",

        'tier-review',
        _NM,
        DID['targeted_agents'],
        'vasopressin_methylene',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The terlipressin chart shows it is used for _______ syndrome (HRS-AKI). "
        "The CONFIRM trial showed HRS reversal in _______ vs _______% with placebo. "
        "Terlipressin was FDA approved in _______. "
        "Its key contraindications include _______, and the nursing monitoring priority is _______.",

        "Terlipressin indication: Hepatorenal Syndrome (HRS-AKI) in decompensated cirrhosis\n"
        "| CONFIRM trial (NEJM 2021, n=300): terlipressin + albumin vs placebo + albumin\n"
        "| HRS reversal: 32.4% vs 16.5% (SCr ≤ 1.5 mg/dL × 48h without death or dialysis)\n"
        "| FDA approved: August 2022 (first FDA-approved therapy for HRS-AKI in USA)\n"
        "| Dose: 1 mg IV q4–6h; ↑ to 2 mg q4–6h if SCr not ↓ ≥ 25% within 48h\n"
        "| Duration: up to 14 days or until SCr < 1.5 mg/dL\n"
        "| Contraindications: ischemic heart disease, severe COPD, peripheral vascular disease\n"
        "| Monitoring priority: respiratory status (albumin + terlipressin → fluid retention → pulm edema)\n"
        "→ CCRN KEY: HRS-AKI pathophysiology: "
        "cirrhosis → portal hypertension → splanchnic vasodilation → RAAS/SNS activation → "
        "renal vasoconstriction → functional AKI (no structural kidney damage). "
        "Diagnosis: SCr rise ≥ 0.3 mg/dL in 48h OR ≥ 50% from baseline in 7 days, "
        "in cirrhosis with ascites, no shock, no nephrotoxins, no AKI improvement after 48h IVF. "
        "Terlipressin V1 effect: splanchnic vasoconstriction → ↑ effective blood volume → ↑ renal perfusion.\n"
        "→ MASTERY NOTE: Alternative HRS-AKI therapy (if terlipressin unavailable/CI):\n"
        "• Midodrine 12.5 mg PO TID + octreotide 200 mcg SQ TID + albumin 1 g/kg/day × 2 then 20–40 g/day\n"
        "• Less effective than terlipressin (HRS reversal ~20–30% in observational data)\n"
        "• Norepinephrine IV + albumin: ICU alternative; requires vasopressor-capable monitoring\n"
        "Liver transplantation remains definitive treatment — terlipressin is a bridge therapy.",

        'tier-high',
        _NM,
        DID['targeted_agents'],
        'vasopressin_methylene',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "On the vasopressin/methylene blue chart, methylene blue treats _______ syndrome "
        "by inhibiting _______ and _______, reducing cGMP and increasing _______. "
        "Dose is _______ mg/kg IV. "
        "The critical nursing monitoring pitfall is _______, and the absolute contraindication is _______.",

        "Methylene blue indication: vasoplegic syndrome (distributive shock refractory to vasopressors)\n"
        "| Classic settings: post-cardiac surgery (cardiopulmonary bypass), severe anaphylaxis, drug-induced\n"
        "| Mechanism: inhibits NOS (↓ NO production) AND inhibits guanylate cyclase (↓ cGMP)\n"
        "| → ↓ cGMP → vascular smooth muscle contraction → ↑ SVR\n"
        "| Dose: 1–2 mg/kg IV over 15–60 min; may repeat q4–6h; infusion 0.25–2 mg/kg/hr\n"
        "| Absolute CI: G6PD deficiency — oxidative hemolysis\n"
        "| Nursing monitoring PITFALL: pulse oximetry falsely reads LOW (blue dye absorbs at 668 nm)\n"
        "→ CCRN KEY: Vasoplegic syndrome after cardiac surgery:\n"
        "Mechanism: CPB → complement activation + endotoxin exposure + hypothermia → "
        "massive NO release → profound SVR drop (CI normal or ↑, MAP < 65 despite high-dose NE). "
        "Management: NE first-line + vasopressin → if refractory → methylene blue 1–2 mg/kg IV bolus. "
        "Response: ↑ SVR within 1–2h, ↓ vasopressor requirements in 60–70% of cases.\n"
        "→ MASTERY NOTE: Methylene blue pulse ox interference — clinical management:\n"
        "• SpO₂ may read 65–70% despite true normal saturation during infusion\n"
        "• Use ABG for accurate SaO₂ measurement during methylene blue infusion\n"
        "• Effect lasts 30–60 min after infusion ends as dye is metabolized/excreted\n"
        "Serotonin syndrome risk: methylene blue inhibits MAO-A → excess serotonin with SSRIs/MAOIs. "
        "Expected harmless effects: urine blue-green, skin/mucosa appear cyanotic (dye) — "
        "document at medication start to prevent alarm calls from nursing staff change of shift. "
        "Hydroxocobalamin (cyanide antidote) also treats vasoplegic via NO scavenging — alternative.",

        'tier-critical',
        _NM,
        DID['targeted_agents'],
        'vasopressin_methylene',
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
