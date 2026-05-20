#!/usr/bin/env python3
"""chunk54_charts.py — Ph7 Pharmacology: Drug Comparisons (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_53.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_54.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c54')
CHUNK_NUM   = 54
MID_BASE    = 1_800_005_115
CHART_ORDER = ['sedation_compare', 'antifungal_compare', 'antibiotic_spectrum',
               'pressor_selection', 'beta_blocker_compare']

_NM = 'Ph7 \U0001f7e1 T3 · Pharmacology — Drug Comparisons'

RF = {}

# ── Chart 1: Sedation Comparison ──────────────────────────────────────────────
RF['sedation_compare'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var rows=[
        {n:'Propofol', mech:'GABA-A potentiation\n(allosteric)',
         pk:'Onset: 30–60 sec\nt½: 2–8h (dist)\nClear: hepatic',
         adr:'PRIS (> 4 mg/kg/hr × 48h)\nHypoTN/bradycardia\nHypertriglyceridemia',
         note:'Gold standard for MV sedation; no analgesia — combine with opioid\nPRIS: lactic acidosis + rhabdo + AV block; check TG weekly; no lipid emulsion\nRapid offset (context-sensitive t½): wake-up easily for SAT; preferred for short-term',
         c:'#cc8844'},
        {n:'Dexmede-\ntomidine', mech:'α2-agonist\n(locus ceruleus;\nno GABA)',
         pk:'Onset: 5–15 min\nt½: 2h\nClear: hepatic',
         adr:'Bradycardia/hypotension\n(loading dose)\nNo resp depression',
         note:'Cooperative sedation: patient arousable, follows commands — ideal for SBT trials\nDelirium prevention (MENDS, MIDEX trials); opioid-sparing + analgesic properties\nMax approved: 0.7 mcg/kg/hr; off-label up to 1.5 mcg/kg/hr; avoid abrupt DC (rebound)',
         c:'#4488cc'},
        {n:'Midazolam', mech:'GABA-A potentiation\n(benzo site)',
         pk:'Onset: 2–5 min\nt½: 3–11h (accum)\nClear: hepatic',
         adr:'Prolonged sedation\n(accumulates, elderly)\nRespiratory depression',
         note:'Seizure first-line (IV); alcohol/benzo withdrawal (CIWA protocol); procedural sedation\nICU CAUTION: accumulates with prolonged infusion; active metabolite α-OH-midazolam in AKI\nPAIN AGITATION DELIRIUM (PAD): associated with ↑ delirium vs propofol/dex (MIDEX trial)',
         c:'#9060c0'},
        {n:'Ketamine', mech:'NMDA receptor\nantagonist\n(dissociative)',
         pk:'Onset: 30–60 sec IV\nt½: 2–3h\nClear: hepatic',
         adr:'Dissociation/emergence\nHypersalivation\n↑ secretions',
         note:'Hemodynamic stability: sympathomimetic (↑ HR, ↑ BP) — safe in shock states\nBronchodilator: preferred for asthma/bronchospasm RSI; analgesic + sedative\nCaution: ↑ ICP (controversial — may be safe in mechanically ventilated patients)\nCo-administer benzodiazepine to prevent emergence phenomena',
         c:'#3a9a5c'},
        {n:'Lorazepam', mech:'GABA-A potentiation\n(benzo site)\n(longer t½)',
         pk:'Onset: 1–5 min\nt½: 10–20h\nClear: conjugation',
         adr:'PG carrier toxicity\n(PEG/benzyl alcohol)\nAccumulates elderly',
         note:'Hepatic failure preferred benzo (direct glucuronidation — no active metabolites)\nAlcohol withdrawal: titrated to CIWA-Ar score; also for status epilepticus management\nPG carrier (propylene glycol) toxicity in infusions: high osmol gap + metabolic acidosis',
         c:'#cc6633'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/rows.length);
    var xs=[4,85,165,255,365,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Agent','Mechanism','Onset/t½/Clear','Key ADR','ICU Indication / Notes'];
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
        ctx.fillStyle='#aaa';ctx.font='6px sans-serif';
        d.mech.split('\n').forEach(function(l,li){ctx.fillText(l,xs[1]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#eedd88';ctx.font='6px sans-serif';
        d.pk.split('\n').forEach(function(l,li){ctx.fillText(l,xs[2]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#ff9966';ctx.font='6px sans-serif';
        d.adr.split('\n').forEach(function(l,li){ctx.fillText(l,xs[3]+2,ry+rh/2-9+li*9);});
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
        var lbs=['Propofol','Dexmede','Midazolam','Ketamine','Lorazepam'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,rows[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: Antifungal Comparison ────────────────────────────────────────────
RF['antifungal_compare'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Azoles','Echinocandins','Polyenes & Selection'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#150a1a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a1a2a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#9060c0':'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#090509';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+13;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#9060c0';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+190,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a1a2a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('Azoles — Inhibit CYP51 (lanosterol 14α-demethylase) → ↓ ergosterol synthesis:','','#9060c0');
        hr();
        rw('Fluconazole:','Candida (NOT C. krusei or C. glabrata); Cryptococcus; oral/IV','#aab','#eedd88');
        nt('Dose: 400–800 mg daily; renally adjusted in AKI; C. albicans first-line if susceptible');
        nt('Drug interactions: strong CYP2C9 + 3A4 inhibitor — ↑ warfarin, tacrolimus, statins');
        hr();
        rw('Voriconazole:','Aspergillus (mold) + Candida spp.; invasive fungal infections','#cc8844','#eedd88');
        nt('Dose: 6 mg/kg IV q12h × 2 loads → 4 mg/kg q12h; oral bioavailability 96%');
        nt('Inhibits CYP2C9+2C19+3A4 — most drug interactions of all azoles');
        nt('Monitoring: trough level 1–5.5 mcg/mL; visual disturbances (photopsia), QTc, LFTs');
        hr();
        rw('Posaconazole:','Prophylaxis (neutropenic/GVHD) + salvage aspergillosis/mucormycosis','#3a9a5c','#eedd88');
        nt('IV preferred in malabsorption; requires fat for oral absorption (delayed-release tab)');
        hr();
        nt('★ Isavuconazole: broad mold + Candida; fewer interactions; no QTc prolongation (shortened QTc)');
    } else if(sel===1){
        rw('Echinocandins — Inhibit β-1,3-glucan synthase → ↓ fungal cell wall:','','#3a9a5c');
        hr();
        rw('Micafungin:','150 mg daily (tx) / 50 mg daily (prophylaxis); hepatic clearance','#aab','#eedd88');
        rw('Caspofungin:','70 mg load → 50 mg daily; reduce to 35 mg in severe hepatic failure','#aab','#eedd88');
        rw('Anidulafungin:','200 mg load → 100 mg daily; NO hepatic or renal dose adjustment needed','#aab','#eedd88');
        hr();
        rw('Class advantages:','','#3a9a5c');
        nt('Minimal drug interactions (not CYP450 substrates/inhibitors)');
        nt('Safe in renal AND hepatic failure (anidulafungin: no adjustment at all)');
        nt('Excellent Candida biofilm penetration — preferred for Candida biofilm (line-related)');
        nt('Fungicidal against Candida (azoles are fungistatic for most Candida spp.)');
        hr();
        rw('Spectrum:','Candida (all species incl. C. glabrata) + Aspergillus (static, not cidal)','#aab','#eedd88');
        rw('NOT active:','Cryptococcus, Fusarium, Mucorales, Trichosporon','#cc4444','#ff9966');
        hr();
        rw('IDSA guidance:','Echinocandin preferred for IC (candidemia) if: unstable, azole exposure, non-albicans','#aab','#eedd88');
        hr();
        nt('★ Step-down to fluconazole at 5 days if: isolate susceptible, improved, no endophthalm');
    } else {
        rw('Amphotericin B — Binds ergosterol → membrane pores → cell death (fungicidal):','','#cc4444');
        hr();
        rw('Conventional (deoxycholate):','Highest toxicity — infusion reactions, nephrotoxicity, electrolyte loss','#cc4444','#ff9966');
        rw('Liposomal (L-AmB):','↓ nephrotoxicity, ↓ infusion reactions; 3–5 mg/kg/day; expensive','#3a9a5c','#eedd88');
        nt('Broadest spectrum: Candida, Aspergillus, Mucorales (zygomycetes), Cryptococcus');
        nt('Drug of choice: mucormycosis (Rhizopus/Mucor) — azoles ineffective, echinocandins ineffective');
        nt('Monitoring: Cr, K⁺, Mg²⁺ daily (nephrotoxic + kaliuresis + hypoMg)');
        hr();
        rw('Selection Algorithm:','','#cc8844');
        rw('Candidemia (stable):','Fluconazole (if no prior azole, C. albicans likely, not critically ill)','#aab','#eedd88');
        rw('Candidemia (unstable):','Echinocandin first-line (IDSA 2016 guidelines)','#aab','#eedd88');
        rw('Aspergillosis:','Voriconazole first-line (IDSA 2016) OR isavuconazole','#aab','#eedd88');
        rw('Mucormycosis:','Liposomal amphotericin B; surgery essential (debridement)','#aab','#eedd88');
        rw('Cryptococcus:','L-AmB + flucytosine induction × 2 wk → fluconazole consolidation','#aab','#eedd88');
        hr();
        nt('★ Flucytosine (5-FC): synergistic with AmB for Cryptococcus; bone marrow toxicity — check CBC');
        nt('★ Candida endophthalmitis: ophthalmology consult; azole with vitreous penetration (vori, fluconazole)');
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

# ── Chart 3: Antibiotic Spectrum Comparison ───────────────────────────────────
RF['antibiotic_spectrum'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['MRSA Coverage Options','Gram-Negative Coverage','De-escalation'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#0a1a0a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#1a2a1a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#3a9a5c':'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#050a05';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+13;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#3a9a5c';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+185,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#1a2a1a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('MRSA Coverage — Comparison:','','#cc4444');
        hr();
        rw('Vancomycin:','MRSA bacteremia/endocarditis/SSTI; AUC/MIC target 400–600','#aab','#eedd88');
        nt('Nephrotoxic (especially with pip-tazo); slow infusion to avoid red man syndrome');
        nt('MIC creep: vancomycin MIC ≥ 2 → poor outcomes; consider daptomycin or ceftaroline');
        hr();
        rw('Daptomycin:','6 mg/kg/day (skin); 8–10 mg/kg/day (bacteremia); NOT for pneumonia','#aab','#eedd88');
        nt('Inactivated by pulmonary surfactant — do NOT use for MRSA pneumonia');
        nt('Monitor CK weekly; hold statins; preferred for vancomycin MIC ≥ 2 or VISA');
        hr();
        rw('Linezolid:','MRSA pneumonia (better lung penetration than vancomycin per ZEPHyR)','#aab','#eedd88');
        nt('ZEPHyR trial: linezolid superior to vancomycin for MRSA VAP (clinical cure 57% vs 47%)');
        nt('ADR: thrombocytopenia (check CBC weekly), serotonin syndrome, optic neuropathy (> 28 days)');
        hr();
        rw('Ceftaroline:','5th-gen cephalosporin; MRSA SSTI + CAP; NOT approved for bacteremia','#aab','#eedd88');
        hr();
        rw('Telavancin:','Lipoglycopeptide; MRSA HAP/VAP; nephrotoxic; QTc prolongation','#aab','#eedd88');
        hr();
        nt('★ MRSA decolonization: mupirocin nasal 2% TID × 5d + chlorhexidine baths for ICU patients');
    } else if(sel===1){
        rw('Broad Gram-Negative Coverage — Comparison:','','#3a9a5c');
        hr();
        rw('Pip-Tazo (4.5g q6h):','Gram+ + gram- + anaerobes; Pseudomonas (intermediate activity)','#aab','#eedd88');
        nt('Extended infusion (4h): improved Pseudomonas target attainment vs 30-min bolus');
        nt('NOT for ESBL: pip-tazo inoculum effect — use meropenem for ESBL-confirmed infections');
        hr();
        rw('Cefepime (2g q8h):','Gram+ + Pseudomonas; limited anaerobes; no ESBL activity','#aab','#eedd88');
        nt('HAP/VAP empiric therapy; extends interval in CrCl < 30 mL/min');
        nt('Neurotoxicity: non-convulsive seizures in elderly + CKD (check EEG if AMS develops)');
        hr();
        rw('Meropenem (1–2g q8h):','Broadest gram- (ESBL); Pseudomonas; anaerobes; NOT MRSA','#cc8844','#eedd88');
        nt('ESBL confirmed: meropenem preferred over pip-tazo (MERINO trial: meropenem ↓ mortality)');
        nt('Extended infusion (3h): ↑ pharmacodynamic target vs Pseudomonas with high MIC');
        hr();
        rw('Ceftazidime-Avibactam:','KPC/CRE + ESBL + MDR Pseudomonas; NOT Acinetobacter MBL','#cc8844','#eedd88');
        nt('Avibactam: beta-lactamase inhibitor (class A/C/some D enzymes); does NOT inhibit MBL (NDM)');
        hr();
        rw('Colistin (polymyxin E):','XDR Pseudomonas, CRE, Acinetobacter — last resort only','#cc4444','#eedd88');
        nt('Nephrotoxicity + neurotoxicity; use with meropenem or rifampin; dose by CrCl');
    } else {
        rw('Antibiotic De-escalation Principles:','','#3a9a5c');
        hr();
        rw('Definition:','Narrowing antibiotic spectrum based on culture results + clinical response','#aab','#eedd88');
        rw('Goal:','Reduce: collateral damage, C. diff risk, resistance selection, cost','#aab','#eedd88');
        hr();
        rw('De-escalation decision points:','','#cc8844');
        nt('48–72h: culture results available — narrow to most susceptible, narrowest spectrum drug');
        nt('48–72h: if no pathogen identified + improving → consider stopping or narrowing empiric therapy');
        nt('5–7d: reassess duration — most HAP/VAP respond to 7 days (IDSA HAP guideline 2016)');
        hr();
        rw('Antibiotic duration evidence:','','#3a9a5c');
        nt('CAP (non-severe, ambulatory): 5 days (IDSA 2019)');
        nt('HAP/VAP: 7 days (IDSA 2016 — SHORT trial confirmed shorter courses non-inferior)');
        nt('Bacteremia (S. aureus): 14 days minimum; endocarditis 4–6 weeks; Candida 14 days after clearance');
        nt('Uncomplicated UTI: 3–5 days (IDSA); catheter-associated UTI: 7 days if respond');
        hr();
        rw('Procalcitonin (PCT)-guided de-escalation:','','#4488cc');
        nt('PCT < 0.25 mcg/L or ↓ by 80% from peak → consider stopping antibiotics');
        nt('PRORATA trial: PCT-guided therapy → ↓ antibiotic exposure (14.3 vs 11.6 days) no ↑ mortality');
        hr();
        nt('★ Blood culture negativity at 72h in low-risk patient + improving clinically = de-escalate signal');
        nt('★ Never de-escalate S. aureus or Candida empirically — always treat confirmed infection');
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

# ── Chart 4: Vasopressor Selection ────────────────────────────────────────────
RF['pressor_selection'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Septic Shock Algorithm','Cardiogenic Shock','Specific Shock Types'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a0a0a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a1a1a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
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
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+180,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a1a1a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('Septic Shock Vasopressor Algorithm (SSC 2021):','','#cc4444');
        hr();
        rw('First line:','Norepinephrine — target MAP ≥ 65 mmHg; titrate from 0.01 mcg/kg/min','#aab','#eedd88');
        nt('CATS trial: NE superior to dopamine (↓ mortality 52% vs 48%); ↓ arrhythmias 10.5% vs 20.6%');
        hr();
        rw('Add vasopressin when NE ≥ 0.25 mcg/kg/min:','(catecholamine-sparing)','#cc8844','#eedd88');
        nt('Fixed dose 0.03–0.04 u/min; VASST: no overall mortality benefit; subgroup benefit in less severe');
        hr();
        rw('Add epinephrine if MAP target not achieved:','(third-line vasopressor)','#cc4444','#ff6644');
        nt('Epi: strong α1 + β1 + β2; ↑ lactate (β2 glycogenolysis) — do not use lactate clearance to guide');
        hr();
        rw('Consider angiotensin II (Giapreza):','','#9060c0');
        nt('ATHOS-3: ↑ MAP in catecholamine-refractory shock; dose 20 ng/kg/min → titrate');
        nt('SE: VTE risk — ensure DVT prophylaxis when starting angiotensin II');
        hr();
        rw('Add low-dose corticosteroids when:','NE or Epi ≥ 0.25 mcg/kg/min (SSC 2021)','#aab','#eedd88');
        hr();
        nt('★ Phenylephrine: pure α1 — use in high CO + low SVR (septic) with tachyarrhythmia concerns');
        nt('★ Dopamine: ↑ arrhythmias (CATS) — use only for specific bradycardia indication');
    } else if(sel===1){
        rw('Cardiogenic Shock — Low CO + High SVR + High PCWP:','','#4488cc');
        hr();
        rw('Dobutamine:','β1+β2 → ↑ CO + mild ↓ SVR; start 2–5 mcg/kg/min','#aab','#eedd88');
        nt('First-line inotrope in cardiogenic shock; ↑ HR + arrhythmia risk at higher doses');
        nt('DOSE target: ↑ CI ≥ 2.2 L/min/m², ↓ PCWP ≤ 18, ↑ urine output');
        hr();
        rw('Milrinone:','PDE3 inhibitor → ↑ cAMP → ↑ inotropy + vasodilation (lusitropic)','#aab','#eedd88');
        nt('No tolerance (unlike dobutamine); renally cleared (↓ dose in CKD); ↓ SVR → hypotension risk');
        nt('OPTIME-CHF: no benefit over standard care in acute decompensated HF; similar outcomes to dobutamine');
        hr();
        rw('Epinephrine:','β1+α1+β2 → ↑ CO + ↑ SVR; use with profound hypotension','#cc4444','#ff6644');
        nt('Post-cardiac surgery cardiogenic shock: epi most commonly used (β1 inotrope + vasopressor)');
        hr();
        rw('Mechanical Support:','','#cc8844');
        nt('IABP (intra-aortic balloon pump): ↑ diastolic BP + ↓ afterload; limited mortality benefit (IABP-SHOCK II)');
        nt('Impella: LV unloading + ↑ forward flow; LVAD bridge; DTCS/RECOVER trials ongoing');
        nt('VA-ECMO: complete hemodynamic support; use in refractory cardiogenic arrest + escalation');
        hr();
        nt('★ SHOCK trial: early revascularization (PCI/CABG) in cardiogenic shock ↓ 6-month mortality');
    } else {
        rw('Shock by Type — Vasopressor Selection:','','#cc4444');
        hr();
        rw('Neurogenic shock (spinal cord injury):','','#4488cc');
        nt('Loss of sympathetic tone: ↓ HR + ↓ BP (unlike other shock types with tachycardia)');
        nt('Phenylephrine (pure α1) + norepinephrine; target MAP ≥ 85–90 in SCI (spinal cord perfusion)');
        nt('Bradycardia: atropine / transcutaneous pacing; dopamine (β1 + α1) if persistent bradycardia');
        hr();
        rw('Anaphylactic shock:','','#cc8844');
        nt('EPINEPHRINE 0.3–0.5 mg IM (anterolateral thigh) — FIRST TREATMENT; do not delay for IV access');
        nt('If refractory: epi IV infusion 0.1–1 mcg/kg/min; vasopressin or NE as adjuncts');
        nt('Diphenhydramine + H2 blocker + steroids: adjuncts only — do NOT substitute for epi');
        hr();
        rw('Obstructive shock (massive PE / tamponade):','','#9060c0');
        nt('PE: IVF 500 mL (↑ RV preload) + NE (↑ coronary perfusion) → thrombolysis or thrombectomy');
        nt('Tamponade: maintain HR + preload (IVF); NE to support BP; pericardiocentesis is definitive');
        nt('Both: RV failure — vasopressors support while treating cause; iNO may temporize');
        hr();
        rw('Distributive (non-septic):','','#cc4444');
        nt('Drug-induced vasoplegia: methylene blue 1–2 mg/kg; hydroxocobalamin as alternative');
        nt('Adrenal crisis: hydrocortisone 100 mg IV bolus → 50 mg q6h; IVF; vasopressors prn');
        hr();
        nt('★ Hypovolemic shock: IVF resuscitation FIRST (30 mL/kg); vasopressors only if ↓ BP persist');
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

# ── Chart 5: Beta-Blocker Comparison ─────────────────────────────────────────
RF['beta_blocker_compare'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var rows=[
        {n:'Metoprolol', sel:'β1 selective\n(cardiosel)', pk:'PO/IV\nt½: 3–7h',
         use:'Rate control\nHF (MERIT-HF)\nSTEMI/ACS',
         note:'Oral: metoprolol succinate XL preferred in HF (MERIT-HF: ↓ mortality 34%)\nIV: metoprolol 5 mg IV q5 min × 3 for rate control in SVT/AF; watch for hypotension\nDo NOT use in decompensated HF (acutely) — can worsen acute cardiogenic shock',
         c:'#4488cc'},
        {n:'Carvedilol', sel:'β1+β2+α1\n(non-selective)', pk:'PO only\nt½: 6–10h',
         use:'HF (↓ mortality)\nPost-MI\nHTN',
         note:'COPERNICUS + CARVEDILOL: mortality benefit in HFrEF (EF ≤ 35%), similar to metoprolol succinate\nα1 component: ↓ afterload + antioxidant effects (beyond pure β-blockade)\nMost evidence for HFrEF of all beta-blockers; start low (3.125 mg BID), titrate slowly',
         c:'#9060c0'},
        {n:'Esmolol', sel:'β1 selective\nUltra-short', pk:'IV only\nt½: 9 min\nLoad + infusion',
         use:'Acute AF/SVT\nHypertensive crisis\nAortic dissection',
         note:'Loading dose: 500 mcg/kg IV over 1 min → infusion 50–200 mcg/kg/min\nUltra-short t½: plasma esterase clearance (NOT renal/hepatic) — safe in organ failure\nType A aortic dissection: esmolol + nitroprusside/nicardipine (HR target < 60, SBP < 120)',
         c:'#3a9a5c'},
        {n:'Labetalol', sel:'β1+β2+α1\n(3:1 β:α ratio)', pk:'IV or PO\nt½: 5–8h',
         use:'Hypertensive\nemergency\nPreeclampsia',
         note:'IV: 10–20 mg IV q10–15 min (bolus) OR infusion 2 mg/min; max 300 mg\nPreeclampsia/eclampsia: first-line IV antihypertensive (hydralazine alternative)\nDO NOT use in: asthma/severe COPD (β2 block), cardiogenic shock, bradycardia',
         c:'#cc8844'},
        {n:'Propranolol', sel:'β1+β2\n(non-selective)', pk:'PO/IV\nt½: 3–6h',
         use:'Thyrotoxicosis\nEsoph varices\nTremor/migraine',
         note:'Thyroid storm: propranolol blocks T4→T3 conversion AND sympathomimetic effects\nPortal HTN: non-selective required for splanchnic β2 effect (↓ portal pressure); NOT metoprolol\nLong-acting (Inderal LA): tremor, migraine prophylaxis, situational anxiety',
         c:'#cc4444'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/rows.length);
    var xs=[4,85,155,215,295,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Agent','Selectivity','Route/t½','Key ICU Use','Clinical Notes'];
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
        ctx.fillStyle='#aaa';ctx.font='6.5px sans-serif';
        d.sel.split('\n').forEach(function(l,li){ctx.fillText(l,xs[1]+2,ry+rh/2-4+li*9);});
        ctx.fillStyle='#eedd88';ctx.font='6.5px sans-serif';
        d.pk.split('\n').forEach(function(l,li){ctx.fillText(l,xs[2]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#88ccff';ctx.font='6.5px sans-serif';
        d.use.split('\n').forEach(function(l,li){ctx.fillText(l,xs[3]+2,ry+rh/2-9+li*9);});
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
        var lbs=['Metoprolol','Carvedilol','Esmolol','Labetalol','Propranolol'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,rows[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Cards ─────────────────────────────────────────────────────────────────────
CARDS = [
    # ═══ sedation_compare ════════════════════════════════════════════════════
    (
        "On the sedation comparison chart, propofol works by _______ and has a unique toxicity "
        "at doses > _______ mg/kg/hr for > 48 hours called _______ syndrome, "
        "which presents with _______, rhabdomyolysis, and _______. "
        "Propofol has _______ analgesic effect.",

        "Propofol mechanism: potentiates GABA-A receptor (allosteric modulation)\n"
        "| PRIS (Propofol Infusion Syndrome): doses > 4 mg/kg/hr for > 48 hours\n"
        "| PRIS presentation: lactic acidosis + rhabdomyolysis + AV conduction block + lipemic plasma\n"
        "| NO analgesic effect — always combine with opioid or other analgesic\n"
        "| Propofol 1%: 0.1 g fat (10 kcal) per mL → monitor triglycerides weekly\n"
        "→ CCRN KEY: PRIS recognition in ICU:\n"
        "• Risk factors: high doses, prolonged use, children, low carbohydrate intake, catecholamine/steroid use\n"
        "• Early signs: metabolic acidosis (elevated anion gap), rising lactate, ↑ CK\n"
        "• Late signs: cardiac arrhythmia (AV block, Brugada-like pattern on ECG), renal failure\n"
        "• Action: STOP propofol immediately; switch to alternative sedation; supportive care ± CVVH\n"
        "→ MASTERY NOTE: Propofol vs dexmedetomidine for ICU sedation (key differences):\n"
        "• Propofol: faster onset/offset; no respiratory depression at low doses (< 50 mcg/kg/min)\n"
        "  BUT: no analgesia, hypotension/bradycardia, PRIS risk, hypertriglyceridemia\n"
        "• Dexmedetomidine: cooperative sedation (patient arousable), analgesic, no GABA mechanism\n"
        "  BUT: slower onset, bradycardia from loading dose, more expensive\n"
        "• PAD guidelines prefer dexmedetomidine over benzodiazepines for ICU sedation (↓ delirium).",

        'tier-review',
        _NM,
        DID['drug_comparisons'],
        'sedation_compare',
        '{"hi":0}',
        'chart-l1'
    ),
    (
        "On the sedation chart, dexmedetomidine is unique because it provides sedation WITHOUT "
        "_______ depression. It acts on _______ receptors in the _______. "
        "Ketamine provides sedation AND analgesia via _______ receptor antagonism and is preferred "
        "for intubation in _______ because it is a _______ agent. "
        "Ketamine also causes _______ making it useful in asthma.",

        "Dexmedetomidine: sedation WITHOUT respiratory depression (unique among ICU sedatives)\n"
        "| Mechanism: α2-adrenergic receptors in locus coeruleus (brainstem) → ↓ NE release → sedation\n"
        "| Clinical: cooperative ('arousable') sedation — patient responds to voice, follows commands\n"
        "| Ketamine: NMDA (N-methyl-D-aspartate) receptor antagonist → dissociative analgesia/anesthesia\n"
        "| Preferred for intubation in hemodynamic instability (hemorrhagic shock, trauma, sepsis)\n"
        "| Sympathomimetic: ketamine ↑ HR, ↑ BP (endogenous catecholamine release) — safe in shock\n"
        "| Bronchodilation: via β2 stimulation + direct smooth muscle relaxation → use in asthma RSI\n"
        "→ CCRN KEY: Ketamine RSI (rapid sequence intubation) indications:\n"
        "• Hemodynamic instability: safest induction agent (↑ BP vs ↓ with propofol/etomidate)\n"
        "• Status asthmaticus requiring intubation: bronchodilator + induction agent\n"
        "• Ketamine dose: 1–2 mg/kg IV (induction) or 0.1–0.5 mg/kg/hr (ICU analgesic/sedation adjunct)\n"
        "• Co-administer midazolam 0.05–0.1 mg/kg to prevent emergence phenomena (hallucinations)\n"
        "→ MASTERY NOTE: Ketamine and ICP — the controversy:\n"
        "• Old teaching: ketamine raises ICP (avoid in TBI) — based on spontaneously breathing patients\n"
        "• Modern evidence: mechanically ventilated patients with controlled ventilation → ICP does NOT rise\n"
        "• Current practice: ketamine is acceptable for RSI in TBI patients — no absolute contraindication\n"
        "Ketamine analgesic use: 0.1–0.3 mg/kg/hr IV → opioid-sparing; useful in opioid-tolerant patients.",

        'tier-high',
        _NM,
        DID['drug_comparisons'],
        'sedation_compare',
        '{"hi":3}',
        'chart-l2'
    ),
    (
        "The sedation chart shows midazolam is associated with _______ in ICU compared to "
        "propofol and dexmedetomidine. "
        "In hepatic failure, the preferred benzodiazepine is _______ because it undergoes "
        "_______ without producing active metabolites. "
        "Lorazepam IV infusions can cause toxicity from the carrier _______, presenting as "
        "_______ gap and metabolic _______.",

        "Midazolam in ICU: associated with ↑ delirium vs propofol and dexmedetomidine (MIDEX/MENDS trials)\n"
        "| Accumulates with prolonged infusion (active metabolite α-hydroxymidazolam in AKI)\n"
        "| Indicated for: seizures (first-line IV benzo for status epilepticus), alcohol withdrawal, procedural sedation\n"
        "| Hepatic failure preferred benzo: lorazepam (direct glucuronidation — no CYP450, no active metabolites)\n"
        "| Lorazepam IV carrier: propylene glycol (PG) — osmotically active\n"
        "| PG toxicity: elevated osmol gap + anion gap metabolic acidosis (lactic acidosis from PG itself)\n"
        "→ CCRN KEY: Identifying propylene glycol toxicity in ICU:\n"
        "• Patient on continuous lorazepam infusion > 3 days OR high-dose requirements\n"
        "• Labs: ↑ osmol gap (osmol gap = measured − calculated osmolality; normal < 10)\n"
        "• Progression: metabolic acidosis (PG metabolized to lactic acid and pyruvate)\n"
        "• Management: switch to non-PG formulation OR alternative sedative\n"
        "→ MASTERY NOTE: Benzodiazepine selection in ICU — hierarchy:\n"
        "• Short-term procedural/seizure: midazolam (fastest onset, shortest duration)\n"
        "• Alcohol withdrawal (CIWA-Ar protocol): lorazepam or diazepam — titrated to CIWA score\n"
        "• Hepatic failure + ongoing sedation: lorazepam (no active metabolites via direct conjugation)\n"
        "• Avoid diazepam: very long t½ (20–100h) + active metabolite desmethyldiazepam → prolonged sedation\n"
        "PAD guidelines (2018): minimize benzos in ICU; prefer propofol or dexmedetomidine for light sedation.",

        'tier-critical',
        _NM,
        DID['drug_comparisons'],
        'sedation_compare',
        '{"hi":2}',
        'chart-l3'
    ),

    # ═══ antifungal_compare ═══════════════════════════════════════════════════
    (
        "The antifungal chart shows azoles inhibit _______, reducing ergosterol synthesis. "
        "Fluconazole covers _______ but NOT _______. "
        "Voriconazole is first-line for _______ and is monitored by trough level of _______. "
        "The azole-fluconazole drug interaction that doubles INR is with _______.",

        "Azoles mechanism: inhibit CYP51 (lanosterol 14α-demethylase) → ↓ ergosterol → fungal membrane disruption\n"
        "| Fluconazole spectrum: Candida spp. (NOT C. krusei or C. glabrata/parapsilosis — variable MIC)\n"
        "| Fluconazole: also Cryptococcus neoformans (step-down after AmB induction)\n"
        "| Voriconazole: first-line for invasive aspergillosis (IDSA 2016)\n"
        "| Voriconazole trough target: 1–5.5 mcg/mL (trough monitoring reduces toxicity + ensures efficacy)\n"
        "| Fluconazole + warfarin: INR doubles within 3–5 days — reduce warfarin dose ~50% on initiation\n"
        "→ CCRN KEY: Which Candida species are resistant to fluconazole:\n"
        "• C. krusei: intrinsically resistant to fluconazole — always use echinocandin or voriconazole\n"
        "• C. glabrata: often reduced susceptibility (step-up dosing or switch to echinocandin)\n"
        "• C. auris (emerging): often pan-resistant; notify infection control; use echinocandin first-line\n"
        "→ MASTERY NOTE: Voriconazole monitoring parameters:\n"
        "1. Trough level: 1–5.5 mcg/mL (sub-therapeutic → treatment failure; supra-therapeutic → toxicity)\n"
        "2. Visual disturbances (photopsia, color changes): common (30%) — transient, dose-related\n"
        "3. QTc prolongation: baseline ECG + weekly monitoring; avoid with other QTc-prolonging drugs\n"
        "4. LFTs: monitor q2 weeks; ↑ ALT/AST common; rarely hepatotoxic\n"
        "5. Photosensitivity + squamous cell skin changes: long-term use in immunocompromised patients.",

        'tier-review',
        _NM,
        DID['drug_comparisons'],
        'antifungal_compare',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The echinocandin chart shows this class inhibits _______, disrupting the fungal cell wall. "
        "The echinocandin requiring NO dose adjustment in renal OR hepatic failure is _______. "
        "Echinocandins are NOT active against _______ and _______. "
        "The IDSA guideline recommends echinocandins as first-line for candidemia when the patient is _______.",

        "Echinocandins mechanism: inhibit β-1,3-glucan synthase → ↓ cell wall glucan → osmotic lysis\n"
        "| No dose adjustment needed: anidulafungin (enzymatic degradation in plasma — no organ metabolism)\n"
        "| Not active against: Cryptococcus neoformans (no glucan in capsule) + Fusarium + Mucorales + Trichosporon\n"
        "| IDSA: echinocandin first-line for candidemia when: critically ill, prior azole exposure, non-albicans Candida likely\n"
        "→ CCRN KEY: Echinocandin class advantages in ICU:\n"
        "• Fungicidal against Candida (azoles are fungistatic) → faster bloodstream clearance\n"
        "• Excellent Candida biofilm penetration → preferred for catheter-associated candidemia\n"
        "• Minimal CYP450 drug interactions (not CYP substrates or inhibitors)\n"
        "• Safe in renal AND hepatic failure — major advantage in critically ill patients\n"
        "→ MASTERY NOTE: Echinocandin specific differences:\n"
        "• Micafungin: approved for prophylaxis (50 mg/day) in SCT and for Candida treatment (150 mg/day)\n"
        "• Caspofungin: reduce to 35 mg/day in severe hepatic failure (Child-Pugh B-C)\n"
        "• Anidulafungin: loading dose 200 mg × 1, then 100 mg/day; no organ adjustment needed\n"
        "Step-down to fluconazole from echinocandin when:\n"
        "• Isolate confirmed susceptible to fluconazole (C. albicans or fluconazole-susceptible C. glabrata)\n"
        "• Clinical improvement (afebrile, hemodynamically stable, negative blood cultures)\n"
        "• After minimum 5 days of echinocandin therapy (IDSA guideline)\n"
        "Duration of candidemia treatment: 14 days from first NEGATIVE blood culture + symptom resolution.",

        'tier-high',
        _NM,
        DID['drug_comparisons'],
        'antifungal_compare',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The antifungal selection chart shows mucormycosis requires _______ amphotericin B "
        "PLUS surgical _______. "
        "Cryptococcus meningitis is treated with _______ PLUS _______ for induction × _______ weeks, "
        "then _______ for consolidation. "
        "The key difference between conventional and liposomal amphotericin B is _______.",

        "Mucormycosis treatment: liposomal amphotericin B 3–5 mg/kg/day PLUS surgical debridement (essential)\n"
        "| Azoles (including voriconazole) and echinocandins: NOT active against Mucorales\n"
        "| Isavuconazole: some activity against Mucor — salvage therapy when AmB not tolerated\n"
        "Cryptococcus meningitis (HIV/immunocompromised):\n"
        "| Induction (2 weeks): liposomal amphotericin B 3–4 mg/kg/day + flucytosine 25 mg/kg PO q6h\n"
        "| Consolidation (8 weeks): fluconazole 400 mg/day\n"
        "| Maintenance (HIV, CD4 > 200 × 3 months): fluconazole 200 mg/day\n"
        "| Conventional vs liposomal AmB: liposomal has ↓ nephrotoxicity + ↓ infusion reactions — preferred in ICU\n"
        "→ CCRN KEY: Amphotericin B monitoring in ICU:\n"
        "• BMP daily (K⁺, Mg²⁺, Cr): AmB causes dose-dependent nephrotoxicity + electrolyte wasting\n"
        "• Hypokalemia: treat aggressively (IV KCl) — often requires 100–200 mEq/day replacement\n"
        "• Hypomagnesemia: concurrent — replacement required (potassium hard to correct without Mg normalization)\n"
        "• Infusion-related reactions (conventional AmB): rigors, fever, hypotension — premedicate with acetaminophen\n"
        "→ MASTERY NOTE: Flucytosine (5-FC) in combination therapy:\n"
        "• Mechanism: converted to 5-fluorouracil inside fungal cells → DNA/RNA synthesis inhibition\n"
        "• Synergistic with AmB for Cryptococcus (standard of care — CSF sterilization at 2 weeks)\n"
        "• Toxicity: bone marrow suppression (monitor CBC 2×/week), GI toxicity, hepatotoxicity\n"
        "• Renally cleared: dose adjust in AKI (check 5-FC levels, target 20–80 mcg/mL at 2h post-dose)\n"
        "• Do NOT use flucytosine as monotherapy: resistance develops rapidly.",

        'tier-critical',
        _NM,
        DID['drug_comparisons'],
        'antifungal_compare',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ antibiotic_spectrum ══════════════════════════════════════════════════
    (
        "The MRSA coverage chart shows vancomycin is monitored by _______ target of _______ "
        "(not trough alone). "
        "Daptomycin is CONTRAINDICATED for MRSA _______ because it is inactivated by _______. "
        "The ZEPHyR trial found _______ superior to vancomycin for MRSA VAP with a clinical cure rate "
        "of _______ vs _______.",

        "Vancomycin monitoring: AUC/MIC ratio target 400–600 (PK/PD-guided dosing)\n"
        "| Trough-only monitoring underestimates exposure — AUC-guided preferred (2018 ASHP/SIDP guideline)\n"
        "| Daptomycin contraindicated for: pneumonia (lung infections) — inactivated by pulmonary surfactant\n"
        "| ZEPHyR trial (NEJM 2012): linezolid vs vancomycin for MRSA VAP\n"
        "| Result: linezolid clinical cure 57.6% vs vancomycin 46.6% (P=0.042); ↑ nephrotoxicity with vancomycin\n"
        "→ CCRN KEY: When to prefer linezolid over vancomycin for MRSA:\n"
        "• MRSA pneumonia (VAP/HAP): linezolid achieves better lung tissue penetration than vancomycin\n"
        "• Vancomycin MIC ≥ 2 mcg/mL (MIC creep): poor outcomes — switch to daptomycin (non-pulmonary) or linezolid\n"
        "• VISA (vancomycin-intermediate S. aureus): vancomycin fails — use daptomycin 8–10 mg/kg + adjunct\n"
        "→ MASTERY NOTE: Linezolid adverse effects requiring nursing monitoring:\n"
        "1. Thrombocytopenia: platelets < 100K in ~30% of patients > 14 days — CBC weekly\n"
        "2. Serotonin syndrome: MAO-A inhibitor — do NOT combine with SSRIs, MAOIs, meperidine, tramadol\n"
        "3. Optic neuropathy: rare, with courses > 28 days — baseline visual acuity assessment\n"
        "4. Peripheral neuropathy: long-term use > 28 days; irreversible\n"
        "5. Lactic acidosis: rare; from mitochondrial toxicity (inhibits mitochondrial protein synthesis).",

        'tier-review',
        _NM,
        DID['drug_comparisons'],
        'antibiotic_spectrum',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the gram-negative coverage chart, the MERINO trial showed that for ESBL-producing organisms, "
        "_______ was superior to pip-tazobactam with lower 30-day mortality (_______% vs _______%). "
        "Ceftazidime-avibactam covers _______ organisms including KPC but does NOT cover "
        "_______ (MBL-producing) gram-negatives. "
        "Cefepime in CKD/elderly patients can cause _______, presenting as AMS.",

        "MERINO trial (NEJM 2018): meropenem vs pip-tazobactam for ESBL/AmpC bacteremia\n"
        "| Meropenem 30-day mortality: 8.4% vs pip-tazobactam 12.3% (P=0.02) — meropenem superior\n"
        "| Message: pip-tazobactam inoculum effect makes it unreliable for ESBL despite in vitro susceptibility\n"
        "| Ceftazidime-avibactam: covers KPC (class A carbapenemase), ESBL, MDR Pseudomonas\n"
        "| Avibactam does NOT inhibit: metallo-beta-lactamase (NDM, VIM, IMP) — carbapenem-resistant organisms\n"
        "| For NDM-producing organisms: use aztreonam-avibactam (in trials) or ceftazidime-avibactam + aztreonam\n"
        "| Cefepime neurotoxicity: non-convulsive seizures — check EEG if new AMS in patient on cefepime with CKD\n"
        "→ CCRN KEY: Empiric antibiotic selection for HAP/VAP (IDSA 2016):\n"
        "• Low-risk (no septic shock, no MDR risk factors): pip-tazobactam OR cefepime OR meropenem\n"
        "• MRSA risk factors: add vancomycin or linezolid\n"
        "• MDR Pseudomonas risk: use 2 anti-pseudomonal agents (combination therapy)\n"
        "• MDR risk factors: prior antibiotic use, hospitalization × 5+ days, structural lung disease\n"
        "→ MASTERY NOTE: Pip-tazobactam vs meropenem for Pseudomonas:\n"
        "• Both active against Pseudomonas but meropenem > pip-tazo for high-MIC strains\n"
        "• Extended infusion pip-tazo (4.5g over 4h q8h): improves pharmacodynamic target attainment\n"
        "• For confirmed Pseudomonas bacteremia: review sensitivities — cipro/pip-tazo/cefepime/meropenem options\n"
        "• Combination therapy (2 drugs) for Pseudomonas: reduces resistance emergence in some settings.",

        'tier-high',
        _NM,
        DID['drug_comparisons'],
        'antibiotic_spectrum',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The de-escalation chart shows the recommended duration for HAP/VAP is _______ days. "
        "Procalcitonin < _______ mcg/mL or ↓ by _______ % from peak is a signal to stop antibiotics. "
        "The PRORATA trial showed PCT-guided de-escalation reduced antibiotic exposure "
        "from _______ to _______ days without increasing mortality.",

        "HAP/VAP duration: 7 days (IDSA 2016; SHORT trial confirmed non-inferiority of shorter courses)\n"
        "| PCT-guided stopping threshold: PCT < 0.25 mcg/mL OR ↓ ≥ 80% from peak → consider stopping\n"
        "| PRORATA trial: PCT-guided vs standard — antibiotic days 14.3 vs 11.6 days (↓ by 2.7 days)\n"
        "| No increase in mortality or ICU-free days — PCT guidance safe and reduces antibiotic exposure\n"
        "→ CCRN KEY: De-escalation principles in ICU:\n"
        "• 48–72h review: assess cultures, clinical response, organ function — de-escalate if improving\n"
        "• Never de-escalate: S. aureus bacteremia, Candida, Aspergillosis without minimum treatment\n"
        "• CAP duration: 5 days (IDSA 2019 update) if afebrile × 48h, hemodynamically stable\n"
        "• S. aureus bacteremia: minimum 14 days from first negative blood culture (28 days if complicated/endocarditis)\n"
        "→ MASTERY NOTE: Antibiotic duration by source:\n"
        "• Uncomplicated UTI (CAUTI): 7 days if respond; catheter removal shortens duration needed\n"
        "• Intra-abdominal infection (post-source control): 4 days adequate (STOP-IT trial, NEJM 2015)\n"
        "• Skin/soft tissue (cellulitis): 5 days if improved (step-down oral as soon as able)\n"
        "• Clostridium difficile (non-severe): fidaxomicin 200 mg BID × 10d OR vancomycin 125 mg QID × 10d\n"
        "Broad antibiotic exposure consequence: C. diff, antibiotic-resistant organism selection, microbiome disruption — "
        "every unnecessary day of antibiotics has measurable adverse effects.",

        'tier-critical',
        _NM,
        DID['drug_comparisons'],
        'antibiotic_spectrum',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ pressor_selection ════════════════════════════════════════════════════
    (
        "The vasopressor algorithm chart shows norepinephrine is first-line for septic shock. "
        "The CATS trial showed NE was superior to dopamine with lower mortality "
        "and significantly fewer _______ (_______ vs _______%). "
        "Vasopressin is added at fixed dose of _______ units/min when NE reaches _______ mcg/kg/min. "
        "Epinephrine as a third-line vasopressor raises _______, making _______ clearance unreliable as a resuscitation endpoint.",

        "CATS trial: NE vs dopamine in shock — NE superior\n"
        "| CATS: fewer arrhythmias with NE: 10.5% vs 20.6% (P<0.001); ↓ 28-day mortality in cardiogenic shock subgroup\n"
        "| Vasopressin: added at 0.03–0.04 units/min (fixed) when NE ≥ 0.25 mcg/kg/min\n"
        "| Epinephrine third-line: raises serum lactate (β2 stimulation → glycogenolysis + liver lactate production)\n"
        "| When epi used: lactate clearance unreliable as resuscitation endpoint — use other perfusion markers\n"
        "→ CCRN KEY: Vasopressor hierarchy in septic shock (SSC 2021):\n"
        "1. Norepinephrine: first-line (strong α1 + mild β1; minimal arrhythmia vs dopamine)\n"
        "2. Vasopressin 0.03–0.04 u/min: add when NE ≥ 0.25 mcg/kg/min (catecholamine-sparing)\n"
        "3. Epinephrine: third-line if MAP target not achieved with NE + vasopressin\n"
        "4. Angiotensin II (Giapreza): fourth-line for catecholamine-refractory distributive shock\n"
        "5. Dopamine: NOT recommended first-line; reserve for select bradycardia situations\n"
        "→ MASTERY NOTE: Dopamine historical context:\n"
        "• Previously used for 'renal protection' at low doses (1–3 mcg/kg/min) — now disproven\n"
        "• CATS trial confirmed dopamine → ↑ arrhythmias vs NE in all shock types\n"
        "• Dopamine still has role: hemodynamically significant bradycardia when atropine fails\n"
        "• Neonatal/pediatric septic shock: dopamine remains first-line in some protocols (different evidence base).",

        'tier-review',
        _NM,
        DID['drug_comparisons'],
        'pressor_selection',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The cardiogenic shock chart shows dobutamine primarily stimulates _______ receptors, "
        "increasing cardiac output and modestly _______ SVR. "
        "Milrinone works by inhibiting _______, which is different from dobutamine. "
        "The IABP-SHOCK II trial showed IABP _______ mortality in cardiogenic shock. "
        "The hemodynamic target in cardiogenic shock is cardiac index ≥ _______ L/min/m².",

        "Dobutamine: β1 (+ β2 + weak α1) agonist → ↑ CO + modest ↓ SVR (β2 vasodilation)\n"
        "| Cardiogenic shock first-line inotrope; dose 2–20 mcg/kg/min; tachycardia + arrhythmia at higher doses\n"
        "| Milrinone: PDE3 (phosphodiesterase-3) inhibitor → ↑ cAMP → ↑ inotropy + lusitropy + vasodilation\n"
        "| Milrinone advantage: no catecholamine receptor tolerance; renally cleared (↓ dose in CKD)\n"
        "| IABP-SHOCK II (NEJM 2012, n=600): IABP vs medical therapy in AMI cardiogenic shock\n"
        "| Result: NO mortality benefit from IABP (30-day mortality: 39.7% vs 41.3%)\n"
        "| Cardiogenic shock CI target: ≥ 2.2 L/min/m² (PCWP target ≤ 18 mmHg)\n"
        "→ CCRN KEY: Dobutamine vs milrinone for cardiogenic shock:\n"
        "• Both ↑ CO and ↓ SVR — similar hemodynamic effect\n"
        "• Dobutamine: more arrhythmogenic (β-receptor stimulation); tachycardia limits dosing\n"
        "• Milrinone: vasodilation can worsen hypotension — often needs NE added; avoid in severe hypotension\n"
        "• OPTIME-CHF trial: milrinone vs dobutamine in decompensated HF — no mortality difference\n"
        "→ MASTERY NOTE: Mechanical circulatory support in cardiogenic shock:\n"
        "• Impella (CP/5.5): LV mechanical support → ↑ forward flow + ↓ LV work (unloads LV)\n"
        "  RECOVER trial: no mortality benefit from routine Impella in AMI-CS (vs IABP)\n"
        "• VA-ECMO: complete heart + lung bypass — most support possible; for refractory arrest\n"
        "  Complications: ↑ LV afterload (LV venting often needed: Impella + ECMO = ECMELLA)\n"
        "• SHOCK trial (NEJM 1999): early revascularization for STEMI cardiogenic shock → ↓ 6-month mortality.",

        'tier-high',
        _NM,
        DID['drug_comparisons'],
        'pressor_selection',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "On the specific shock types chart, the FIRST treatment for anaphylaxis is _______ "
        "given _______ (site and route), not IV antihistamines. "
        "Neurogenic shock from spinal cord injury differs from other shock types because the heart rate is "
        "_______ (not elevated). "
        "The MAP target in acute spinal cord injury is ≥ _______ mmHg to maintain cord perfusion.",

        "Anaphylaxis first treatment: epinephrine 0.3–0.5 mg IM (anterolateral thigh)\n"
        "| IM preferred over IV for non-arrest anaphylaxis (faster peak concentration than IV in this setting)\n"
        "| Do NOT delay epi for IV access: mortality from anaphylaxis = delayed epinephrine\n"
        "| Diphenhydramine + steroids: adjuncts only — they do NOT reverse circulatory collapse\n"
        "| Neurogenic shock: ↓ HR (bradycardia from loss of cardiac sympathetic fibers) + ↓ BP\n"
        "| Distinguishing feature: shock with BRADYCARDIA (not tachycardia as in other shock types)\n"
        "| MAP target in SCI: ≥ 85–90 mmHg for 5–7 days (spinal cord perfusion pressure maintenance)\n"
        "→ CCRN KEY: Neurogenic shock vasopressor selection:\n"
        "• Phenylephrine (pure α1): for hypotension WITHOUT bradycardia — avoids reflex tachycardia\n"
        "• Norepinephrine (α1 + β1): useful when bradycardia + hypotension coexist\n"
        "• Dopamine: β1 + α1 — can use when bradycardia limits phenylephrine choice\n"
        "• Atropine: for symptomatic bradycardia in spinal shock\n"
        "→ MASTERY NOTE: Obstructive shock management:\n"
        "• Massive PE: IVF 500 mL bolus (↑ RV preload) + NE (maintains coronary perfusion) → thrombolysis or thrombectomy\n"
        "• Cardiac tamponade: maintain HR (NE/dopamine) + preload (IVF) + heart rate to compensate fixed stroke volume\n"
        "  Pericardiocentesis: definitive; ultrasound-guided\n"
        "  Avoid: PEEP (↑ intrathoracic pressure → ↓ venous return → cardiac arrest)\n"
        "• Tension pneumothorax: needle decompression (2nd ICS MCL) → tube thoracostomy — vasopressors temporize.",

        'tier-critical',
        _NM,
        DID['drug_comparisons'],
        'pressor_selection',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ beta_blocker_compare ═════════════════════════════════════════════════
    (
        "On the beta-blocker comparison chart, esmolol has an ultra-short half-life of _______ minutes "
        "because it is metabolized by _______. "
        "For type A aortic dissection, the target heart rate is _______ and SBP < _______ mmHg, "
        "achieved with esmolol PLUS _______. "
        "The non-selective beta-blocker required for esophageal variceal prophylaxis is _______ "
        "because it requires _______ receptor blockade.",

        "Esmolol half-life: 9 minutes — metabolized by plasma esterase (red blood cell esterase)\n"
        "| No hepatic or renal dependence — safe in organ failure; easily titrated (load + infusion)\n"
        "| Type A aortic dissection targets: HR < 60 bpm + SBP < 120 mmHg (then surgical repair)\n"
        "| Esmolol + nicardipine OR nitroprusside: combination for dissection (β-blocker FIRST to prevent reflex tachycardia from vasodilator)\n"
        "| Esophageal variceal prophylaxis: propranolol (or nadolol) — non-selective required\n"
        "| Reason: β2 blockade → ↓ portal blood flow (splanchnic vasodilation reversed by β2 block)\n"
        "| Metoprolol (β1 selective) does NOT reduce portal pressure — cannot substitute\n"
        "→ CCRN KEY: Aortic dissection drug sequence:\n"
        "1. Control HR FIRST with IV esmolol or metoprolol\n"
        "2. THEN add vasodilator (nitroprusside/nicardipine) to control BP\n"
        "• If vasodilator given first: reflex tachycardia → ↑ aortic shear force → propagation of dissection\n"
        "→ MASTERY NOTE: Beta-blocker selectivity comparison:\n"
        "• β1 selective (cardioselective): metoprolol, atenolol, bisoprolol, esmolol\n"
        "  Relative selectivity — NOT absolute: still block β2 at high doses\n"
        "  Relative safety in mild-moderate COPD/asthma (vs non-selective)\n"
        "• Non-selective (β1+β2): propranolol, carvedilol, labetalol, nadolol\n"
        "  β2 blockade → ↑ risk of bronchospasm in asthma — avoid in severe asthma\n"
        "• Alpha + beta: carvedilol (α1+β1+β2), labetalol (α1+β1+β2, 3:1 β:α)\n"
        "  Additional α1 block → ↓ afterload + antioxidant effects (carvedilol in HFrEF).",

        'tier-review',
        _NM,
        DID['drug_comparisons'],
        'beta_blocker_compare',
        '{"hi":2}',
        'chart-l1'
    ),
    (
        "The beta-blocker chart shows carvedilol has _______ receptor blocking activity. "
        "The MERIT-HF trial showed metoprolol _______ XL reduced mortality in HFrEF by _______%. "
        "In thyroid storm, propranolol is preferred over cardioselective beta-blockers because it "
        "also inhibits _______ conversion.",

        "Carvedilol receptor blocking activity: β1 + β2 + α1 (non-selective beta + alpha-1)\n"
        "| Additional α1 block: ↓ afterload + antioxidant properties beyond pure beta-blockade\n"
        "| MERIT-HF trial: metoprolol succinate (XL) vs placebo in HFrEF (EF < 40%)\n"
        "| Result: 34% relative risk reduction in all-cause mortality (34% RRR); also ↓ sudden cardiac death\n"
        "| Propranolol in thyroid storm: blocks T4 → T3 peripheral conversion (in addition to β-blockade)\n"
        "| Selective agents (metoprolol): only block β-receptors — do NOT inhibit T4→T3 conversion\n"
        "→ CCRN KEY: Beta-blockers with mortality benefit in HFrEF (class effect only for 3 agents):\n"
        "• Carvedilol (COPERNICUS trial)\n"
        "• Metoprolol succinate XL (MERIT-HF trial)\n"
        "• Bisoprolol (CIBIS-II trial)\n"
        "• NOT extended to all beta-blockers — class effect is NOT proven for all\n"
        "• Atenolol, propranolol: no mortality benefit in HFrEF — do NOT substitute\n"
        "→ MASTERY NOTE: Beta-blocker in ACUTE decompensated HF:\n"
        "• Do NOT start new beta-blocker in acute decompensated HF with cardiogenic shock\n"
        "• Continue home beta-blocker if hemodynamically stable (stopping worsens outcomes)\n"
        "• If hemodynamically unstable: reduce or hold dose temporarily; restart when euvolemic and stable\n"
        "Carvedilol start: 3.125 mg PO BID with food; double every 2 weeks as tolerated to max 25 mg BID.",

        'tier-high',
        _NM,
        DID['drug_comparisons'],
        'beta_blocker_compare',
        '{"hi":1}',
        'chart-l2'
    ),
    (
        "On the beta-blocker chart, labetalol blocks _______ and _______ receptors in a _______ to _______ β:α ratio. "
        "It is first-line for hypertensive emergency in _______ (pregnancy complication). "
        "Beta-blockers are absolutely contraindicated in _______ (type of shock) and relatively "
        "contraindicated in _______ and severe bradycardia.",

        "Labetalol receptor profile: β1 + β2 + α1 blockade in 3:1 β:α ratio (oral) / 7:1 (IV)\n"
        "| IV dosing: 10–20 mg IV q10–15 min (bolus) OR 2 mg/min infusion; max 300 mg\n"
        "| First-line for preeclampsia/eclampsia hypertension (preferred over nitroprusside — maternal/fetal safety)\n"
        "| Hydralazine: alternative for preeclampsia when labetalol unavailable\n"
        "| Absolute contraindication for all beta-blockers: cardiogenic shock (↓ contractility → ↓ CO)\n"
        "| Relative CI: severe asthma (bronchospasm from β2 block), severe COPD, sick sinus syndrome, AV block > 1st degree\n"
        "→ CCRN KEY: Hypertensive emergency beta-blocker selection:\n"
        "• Acute aortic dissection: esmolol IV (fastest titration) + vasodilator\n"
        "• Preeclampsia: labetalol IV (preferred) or hydralazine IV\n"
        "• Hypertensive encephalopathy/stroke: nicardipine or labetalol (clevidipine for post-cardiac surgery)\n"
        "• Post-CABG hypertension: esmolol + nicardipine; rapidly reversible\n"
        "→ MASTERY NOTE: Beta-blocker reversal if overdose (or adverse reaction):\n"
        "• Glucagon: 5–10 mg IV bolus → 1–5 mg/hr infusion (bypasses β-receptor → ↑ cAMP directly)\n"
        "• Calcium chloride: 1 g IV (improves calcium-mediated contractility, especially with CCB co-ingestion)\n"
        "• Atropine: for bradycardia component (less effective in complete AV block from OD)\n"
        "• High-dose insulin (HDI): 1 unit/kg/hr with dextrose — positive inotropy independent of β-receptors\n"
        "• Lipid emulsion therapy: for lipophilic beta-blocker overdose (propranolol, metoprolol).",

        'tier-critical',
        _NM,
        DID['drug_comparisons'],
        'beta_blocker_compare',
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
