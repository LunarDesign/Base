#!/usr/bin/env python3
"""chunk53_charts.py — Ph7 Pharmacology: Mechanism Groups (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_52.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_53.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c53')
CHUNK_NUM   = 53
MID_BASE    = 1_800_005_110
CHART_ORDER = ['receptor_map', 'antibiotic_class', 'coagulation_targets',
               'renal_dose_adjust', 'cyp450_interactions']

_NM = 'Ph7 \U0001f7e1 T3 · Pharmacology — Mechanism Groups'

RF = {}

# ── Chart 1: Receptor Map ─────────────────────────────────────────────────────
RF['receptor_map'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var rows=[
        {n:'α1', loc:'Vascular SMC\nIris (dilator)', eff:'↑ SVR\nvasoconstriction',
         drugs:'Phenylephrine\nNE, Epi (high)\nDopamine (>10)',
         note:'Vasopressor: septic/neurogenic shock; phenylephrine = pure α1 (no β → ↑ reflex bradycardia)\nEpi: α1+β1+β2 — all doses; NE: α1>β1 — minimal β2 at clinical doses\nα1 OD: hypertension + reflex bradycardia (treat with phentolamine)',
         c:'#cc4444'},
        {n:'α2', loc:'Presynaptic\nneurons\nSpinal cord', eff:'↓ NE release\nSedation\n↓ sympathetic',
         drugs:'Dexmedetomidine\nClonidine\nXylazine (vet)',
         note:'ICU sedation: dexmedetomidine — opioid-sparing, no resp depression, delirium ↓\nAlcohol/opioid withdrawal adjunct; hypertension crisis (central α2)\nClonidine rebound hypertension on abrupt DC — taper in BP-dependent patients',
         c:'#9060c0'},
        {n:'β1', loc:'SA node\nAV node\nVentricle', eff:'↑ HR ↑ contrac\n↑ AV conduction\n↑ CO',
         drugs:'Dobutamine\nIsoproterenol\nDopamine (mod)\nEpinephrine',
         note:'Cardiogenic shock: dobutamine (β1=β2, ↑ CO, ↓ SVR) or epi (β1+α1)\nIsoproterenol: pure β1+β2 — bradycardia refractory to atropine; bridge to pacer\nDopamine 5–10 mcg/kg/min: primarily β1 (moderate dose range)',
         c:'#4488cc'},
        {n:'β2', loc:'Bronchial SMC\nVascular SMC\nUterus', eff:'Bronchodilation\n↓ SVR\nTocolysis',
         drugs:'Albuterol\nTerbutaline\nSalmeterol\nDobutamine',
         note:'Asthma/COPD bronchospasm: albuterol 2.5 mg neb q20 min × 3 or MDI 4–8 puffs\nTerbutaline: tocolysis for preterm labor (β2 = ↓ uterine tone)\nβ2 side effects: hypokalemia (K⁺ shift intracellular), tremor, tachycardia',
         c:'#3a9a5c'},
        {n:'DA1\nDA2', loc:'Renal/mesenteric\nvessels (DA1)\nPresynaptic (DA2)', eff:'Renal vasodilat\n↑ GFR, natriuresis\n↓ NE release (DA2)',
         drugs:'Dopamine (low)\nFenoldopam\n(selective DA1)',
         note:'Fenoldopam: selective DA1 agonist for hypertensive crisis (↑ renal blood flow)\n"Renal dose dopamine" (1–3 mcg/kg/min): insufficient evidence — NOT recommended for AKI\nDopamine at ANY dose: ↑ HR risk; reserved for bradycardia refractory to other agents',
         c:'#cc8844'},
        {n:'mAChR\n(M2/M3)', loc:'SA/AV node (M2)\nBronchi, GI (M3)\nVascular endo', eff:'↓ HR ↓ AV cond\nBronchoconstric\nGI motility ↑',
         drugs:'Bethanechol (M3)\n[Blocked by atrop\nipratropium]',
         note:'Atropine blocks M2 (↑ HR) + M3 — treats organophosphate toxidrome (SLUDGE)\nIpratropium: inhaled M3 antagonist for COPD bronchospasm (no systemic HR effect)\nM2 stimulation = vagal tone: ↓ HR, ↓ AV conduction — adenosine mimics vagal effect',
         c:'#cc6633'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/rows.length);
    var xs=[4,60,155,230,340,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Rec.','Location','Effect','ICU Agonist Drugs','Clinical Notes'];
    ctx.font='bold 7.5px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    rows.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=d.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=d.c;ctx.font='bold 8px sans-serif';ctx.textAlign='center';
        d.n.split('\n').forEach(function(l,li){ctx.fillText(l,(xs[0]+xs[1])/2,ry+rh/2-4+li*9);});
        ctx.fillStyle='#aaa';ctx.font='6.5px sans-serif';ctx.textAlign='left';
        d.loc.split('\n').forEach(function(l,li){ctx.fillText(l,xs[1]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#eedd88';ctx.font='6.5px sans-serif';
        d.eff.split('\n').forEach(function(l,li){ctx.fillText(l,xs[2]+2,ry+rh/2-9+li*9);});
        ctx.fillStyle='#88ccff';ctx.font='6px sans-serif';
        d.drugs.split('\n').forEach(function(l,li){ctx.fillText(l,xs[3]+2,ry+rh/2-9+li*9);});
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
        var lbs=['α1','α2','β1','β2','DA','mAChR'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,rows[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: Antibiotic Mechanisms ───────────────────────────────────────────
RF['antibiotic_class'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Cell Wall Agents','Protein Synthesis','DNA/Other Targets'];
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
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+175,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#1a2a1a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('Beta-Lactams — inhibit PBPs (transpeptidases) → block cell wall cross-linking:','','#3a9a5c');
        hr();
        rw('Penicillins:','Ampicillin (gram+/anaerobes); Pip-Tazo (gram+ + gram- + anaerobes)','#aab','#eedd88');
        rw('Cephalosporins:','1st–5th gen; Cefepime (4th, gram+ + Pseudomonas); Ceftaroline (5th, MRSA)','#aab','#eedd88');
        rw('Carbapenems:','Meropenem/imipenem = broadest spectrum (incl. ESBL); NOT MRSA','#aab','#eedd88');
        rw('Monobactams:','Aztreonam — gram- only; safe in severe PCN allergy (no cross-reactivity)','#aab','#eedd88');
        hr();
        rw('Glycopeptides — inhibit cell wall transglycosylation:','','#cc8844');
        rw('Vancomycin:','MRSA coverage; AUC/MIC target 400–600 (PK/PD dosing); nephrotoxic','#aab','#eedd88');
        rw('Daptomycin:','Disrupts gram+ membrane potential; skin/soft tissue, bacteremia; NOT lungs','#aab','#eedd88');
        hr();
        nt('★ Beta-lactam resistance: PBP mutations (MRSA), ESBL (hydrolysis), carbapenemases (CRE/KPC)');
        nt('★ Pip-Tazo (4.5g q6h extended infusion 4h): ↑ pharmacodynamic target attainment vs Pseudomonas');
    } else if(sel===1){
        rw('30S Ribosome Inhibitors — prevent aminoacyl-tRNA binding:','','#3a9a5c');
        rw('Aminoglycosides:','Gentamicin, tobramycin, amikacin — gram- synergy; once-daily preferred','#aab','#eedd88');
        nt('Nephrotoxic + ototoxic; peak/trough or AUC monitoring; avoid in AKI when possible');
        rw('Tetracyclines:','Doxycycline, tigecycline (MRSA + ESBL + anaerobes); tigecycline ↑ mortality in VAP','#aab','#eedd88');
        hr();
        rw('50S Ribosome Inhibitors — peptide chain elongation/translocation:','','#4488cc');
        rw('Macrolides:','Azithromycin — atypicals (Legionella, Mycoplasma); QTc prolongation','#aab','#eedd88');
        rw('Clindamycin:','Anaerobes + MSSA; C. diff risk; inhibits toxin production (necrotizing fasciitis)','#aab','#eedd88');
        rw('Linezolid:','MRSA + VRE; bacteriostatic; serotonin syndrome risk; thrombocytopenia','#aab','#eedd88');
        hr();
        rw('Polymyxins — disrupt gram- outer membrane:','','#cc4444');
        nt('Colistin (polymyxin E): CRE, XDR Pseudomonas — last resort; nephrotoxic');
        hr();
        nt('★ Aminoglycosides: concentration-dependent killing — once-daily achieves higher peak/MIC ratio');
        nt('★ Beta-lactams: time-dependent killing — extended infusion or continuous infusion optimal');
    } else {
        rw('Fluoroquinolones — inhibit DNA gyrase (gram-) + topoisomerase IV (gram+):','','#3a9a5c');
        rw('Cipro:','Best Pseudomonas activity among FQ; UTI, HAP/VAP (caution: resistance risk)','#aab','#eedd88');
        rw('Levofloxacin:','Respiratory FQ — CAP (Legionella, Strep); UTI; less Pseudomonas than cipro','#aab','#eedd88');
        rw('Moxifloxacin:','Anaerobic activity; intra-abdominal + CAP; NO renal dose adjust; NO UTI use','#aab','#eedd88');
        nt('Class AEs: QTc prolongation, Achilles tendon rupture, CNS effects, peripheral neuropathy');
        nt('FQ + divalent cations (Mg, Ca, Al, Fe): chelation → ↓ absorption — space apart 2–4h');
        hr();
        rw('Metronidazole — DNA strand breakage (anaerobes + protozoa):','','#cc8844');
        nt('Anaerobes (intra-abdominal, C. diff mild-moderate); Trichomonas, Giardia, amebiasis');
        nt('Disulfiram-like reaction: avoid alcohol × 48h; hepatic metabolism — dose adjust in severe liver disease');
        hr();
        rw('Trimethoprim-Sulfamethoxazole — sequential folate inhibition:','','#9060c0');
        nt('PCP prophylaxis/treatment (high dose); MRSA SSTI; UTI/prostatitis');
        nt('Hyperkalemia (blocks ENaC), nephrotoxicity, bone marrow suppression — monitor CBC + BMP');
        hr();
        nt('★ Antifungals: fluconazole (ergosterol synthesis); echinocandins (β-glucan wall) — see chunk52 drug compare');
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

# ── Chart 3: Coagulation Targets ──────────────────────────────────────────────
RF['coagulation_targets'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Cascade Drug Targets','Factor Xa / DTIs','Reversal Agents'];
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
    ctx.fillStyle='#0a0505';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+13;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#cc4444';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+175,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a1a1a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('Extrinsic Pathway (PT / INR):','Tissue factor + Factor VII → Xa','#cc8844','#eedd88');
        nt('Warfarin: inhibits Vit K-dependent factors (II, VII, IX, X, protein C/S)');
        nt('Factor VIIa (NovoSeven): activates extrinsic; used in refractory bleeding + reversal');
        hr();
        rw('Intrinsic Pathway (aPTT):','XII → XI → IX → X (+ VIII as cofactor)','#4488cc','#eedd88');
        nt('Heparin (UFH): binds antithrombin → inhibits IIa + Xa; monitor aPTT or anti-Xa');
        nt('LMWH (enoxaparin): primarily anti-Xa; monitor anti-Xa in obesity/CKD/pregnancy');
        nt('Argatroban: direct thrombin inhibitor; monitored by aPTT; hepatic clearance (use in HIT)');
        hr();
        rw('Common Pathway — Final Clot Formation:','X → II (thrombin) → I (fibrin)','#cc4444','#eedd88');
        nt('Factor Xa converts prothrombin → thrombin; thrombin converts fibrinogen → fibrin');
        nt('Thrombin also activates: VIII, V, XI, XIII (cross-links fibrin), protein C (anticoag)');
        hr();
        rw('Fibrinolytic Pathway:','tPA → plasminogen → plasmin → fibrin degradation','#9060c0','#eedd88');
        nt('tPA: endogenous; alteplase = recombinant tPA (clot lysis for PE, STEMI, stroke)');
        nt('Antifibrinolytics: tranexamic acid (TXA) — inhibits plasminogen activation; trauma, surgery');
    } else if(sel===1){
        rw('Direct Factor Xa Inhibitors (DOACs):','','#cc4444');
        rw('Rivaroxaban:','Once daily; renal clearance 33%; NOT removed by dialysis','#aab','#eedd88');
        rw('Apixaban:','Twice daily; renal 25%; lowest stroke rate + bleeding (ARISTOTLE)','#aab','#eedd88');
        rw('Edoxaban:','Once daily; renal 50%; requires parenteral bridge × 5–10d','#aab','#eedd88');
        rw('Fondaparinux:','Indirect Xa inhibitor (via AT); SC; HIT alternative; no reversal agent','#aab','#eedd88');
        hr();
        rw('Direct Thrombin Inhibitors (DTIs):','','#4488cc');
        rw('Dabigatran:','Oral DTI; renal 80%; hemodialysis removes; idarucizumab reverses','#aab','#eedd88');
        rw('Argatroban:','IV DTI; hepatic clearance; HIT treatment; monitor aPTT 1.5–3× baseline','#aab','#eedd88');
        rw('Bivalirudin:','IV DTI; renal 20% + enzymatic clearance; PCI/HIT; short t½ (~25 min)','#aab','#eedd88');
        hr();
        rw('Monitoring summary:','','#cc8844');
        nt('UFH: aPTT 60–100s OR anti-Xa 0.3–0.7 IU/mL (therapeutic); anti-Xa preferred in obesity');
        nt('LMWH: anti-Xa 0.5–1.0 IU/mL (therapeutic BID dosing); 4h post-dose level');
        nt('Argatroban/bivalirudin: aPTT 1.5–3× baseline; watch for aPTT lag in liver failure');
        hr();
        nt('★ DOACs: no routine monitoring needed; anti-Xa level for urgent reversal timing (apixaban/rivaroxaban)');
    } else {
        rw('Anticoagulant Reversal Agents:','','#cc4444');
        hr();
        rw('Protamine sulfate:','Reverses UFH (1 mg per 100 units UFH); partially reverses LMWH (~60%)','#aab','#eedd88');
        nt('Protamine CI: fish allergy (derived from salmon sperm); hypotension, pulmonary HTN risk');
        hr();
        rw('Vitamin K:','Reverses warfarin (hours); IV preferred for urgent reversal (effect in 4–6h)','#aab','#eedd88');
        nt('High-dose Vit K (10 mg IV): takes 24–48h for full effect even IV — supplement with PCC');
        rw('4F-PCC (KCentra):','Factors II, VII, IX, X + Prot C/S; immediate INR reversal; use with Vit K','#cc4444','#ff6644');
        nt('4F-PCC dose by INR: INR 2–4 = 25 units/kg; INR 4–6 = 35 units/kg; INR > 6 = 50 units/kg');
        hr();
        rw('Idarucizumab (Praxbind):','Reverses dabigatran; 5 g IV (two 2.5g doses); immediate','#9060c0','#eedd88');
        rw('Andexanet alfa (Andexxa):','Reverses Xa inhibitors (rivaroxaban/apixaban); FDA approved 2018','#9060c0','#eedd88');
        nt('Andexanet: high dose vs low dose by drug + time of last dose; very expensive ($24,000/dose)');
        hr();
        rw('Tranexamic Acid (TXA):','Antifibrinolytic; trauma hemorrhage within 3h (CRASH-2); OB hemorrhage','#cc8844','#eedd88');
        hr();
        nt('★ FFP: reverses ALL factors but volume-dependent; VTE risk; takes 20–30 min to thaw');
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

# ── Chart 4: Renal Dose Adjustment ────────────────────────────────────────────
RF['renal_dose_adjust'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Drugs to Avoid in AKI','Dose Adjust in CKD','CRRT Drug Dosing'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a1504':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a2008';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
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
    function hr(){ctx.strokeStyle='#2a2008';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('High-Risk Nephrotoxins — Avoid or Use with Extreme Caution in AKI:','','#cc4444');
        hr();
        rw('NSAIDs:','↓ prostaglandin → afferent arteriole constriction → ↓ GFR; AVOID in AKI + CKD','#cc4444','#ff9966');
        rw('Aminoglycosides:','Proximal tubule accumulation → tubular necrosis; monitor levels; avoid if CrCl < 30','#cc4444','#ff9966');
        rw('IV Contrast:','Contrast-induced nephropathy; pre-hydrate with isotonic saline; hold metformin 48h','#cc4444','#ff9966');
        rw('ACE-i / ARBs:','↓ efferent arteriole tone → ↓ GFR; hold in AKI; can cause hyperkalemia','#cc4444','#ff9966');
        rw('Metformin:','Lactic acidosis in AKI (↑ metformin accumulation); hold if Cr > 1.4F / 1.5M','#cc4444','#ff9966');
        rw('Calcineurin inhib:','Cyclosporine/tacrolimus — direct vasoconstriction + direct tubular toxicity','#cc4444','#ff9966');
        hr();
        nt('★ Pre-hydrate with isotonic saline before contrast in AKI risk patients (eGFR < 30)');
        nt('★ NAC (N-acetylcysteine) for contrast nephropathy: evidence limited — not routinely recommended');
        nt('★ Amphotericin B: tubular toxicity (hypoK + hypoMg + renal tubular acidosis); use liposomal form');
    } else if(sel===1){
        rw('Renally-Cleared Drugs Requiring Dose Adjustment (CrCl < 30–50 mL/min):','','#cc9922');
        hr();
        rw('Antibiotics:','','#3a9a5c');
        nt('Vancomycin: ↑ interval (q12→q24→q48h); target AUC/MIC 400–600 regardless of frequency');
        nt('Pip-tazobactam: reduce dose in CrCl < 20 (2.25g q6h); cefepime: ↓ dose in CrCl < 30');
        nt('Meropenem: ↓ dose in CrCl 10–25 (1g q12h); carbapenems require GFR-based adjustment');
        hr();
        rw('Analgesics:','','#cc8844');
        nt('Morphine: active metabolite M6G accumulates → respiratory depression; use hydromorphone');
        nt('Gabapentin/pregabalin: accumulates in CKD; ↓ dose or increase interval significantly');
        nt('Ketorolac: avoid in AKI/CKD (NSAID nephrotoxicity + GI bleeding risk)');
        hr();
        rw('Anticoagulants:','','#4488cc');
        nt('LMWH (enoxaparin): avoid therapeutic dose in CrCl < 30; check anti-Xa; use UFH instead');
        nt('Dabigatran: 80% renal — avoid in CrCl < 30; rivaroxaban/apixaban safer in CKD');
        hr();
        rw('Cardiac drugs:','','#9060c0');
        nt('Digoxin: narrow therapeutic window; reduce dose in CKD; trough target 0.5–0.9 ng/mL');
        nt('Atenolol/sotalol: heavily renal — switch to metoprolol/carvedilol in severe CKD');
    } else {
        rw('Continuous Renal Replacement Therapy (CRRT) — Drug Dosing Principles:','','#cc9922');
        hr();
        rw('CRRT removes drugs via:','Filtration (convection) + diffusion; dependent on MW + protein binding','#aab','#eedd88');
        rw('Key principle:','Small MW + low protein binding + high Vd = most removed by CRRT','#aab','#eedd88');
        hr();
        rw('Antibiotics on CRRT:','','#3a9a5c');
        nt('Vancomycin: give standard loading dose; maintenance q24–48h; check trough or AUC');
        nt('Pip-tazobactam: 3.375g q8h extended (4h) infusion on CRRT (use intermittent dosing studies)');
        nt('Meropenem: 1g q8h on CRRT (CVVHDF 25 mL/kg/h); check CRRT effluent flow rate');
        nt('Fluconazole: 400–800 mg q24h on CRRT (moderate removal by dialysis)');
        hr();
        rw('Not significantly removed by CRRT (no dose change):','','#cc8844');
        nt('Propofol, fentanyl (high Vd/protein bound); quinolones (hepatic metabolism)');
        nt('Vancomycin and aminoglycosides: substantial CRRT removal — dose timing post-CRRT filter');
        hr();
        rw('Monitoring on CRRT:','','#aab');
        nt('CRRT dose target: 20–25 mL/kg/h effluent rate (KDIGO: 20 minimum, 25 typical)');
        nt('Drug levels: check at steady state using drug-specific timing (e.g., vanc trough pre-4th dose)');
        hr();
        nt('★ CRRT circuit anticoagulation: regional citrate (preferred) → hypocalcemia risk; systemic UFH alt');
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

# ── Chart 5: CYP450 Drug Interactions ────────────────────────────────────────
RF['cyp450_interactions'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['CYP3A4 Inhibitors/Inducers','CYP2C9/2C19/2D6','Hepatic Failure Drug Adjust'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a0a1a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
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
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+175,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a1a2a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('CYP3A4 — metabolizes ~50% of drugs:','','#9060c0');
        hr();
        rw('Strong INHIBITORS (↑ drug levels):','','#cc4444');
        nt('Azole antifungals: fluconazole, voriconazole, itraconazole — major CYP3A4 + 2C9 inhibitors');
        nt('Macrolides: erythromycin, clarithromycin (not azithromycin — minimal CYP3A4 effect)');
        nt('Amiodarone: strong 2C9 + 3A4 inhibitor → ↑ warfarin, digoxin, statins — INR monitoring essential');
        nt('Ritonavir/cobicistat (HIV): used therapeutically as PK "boosters" for HIV drugs');
        hr();
        rw('Strong INDUCERS (↓ drug levels):','','#3a9a5c');
        nt('Rifampin: strongest inducer — ↓ warfarin, tacrolimus, HIV meds by up to 10-fold');
        nt('Phenytoin, carbamazepine, phenobarbital: ↓ immunosuppressants, anticoagulants, hormones');
        nt('St. John\'s Wort (Hypericum): natural inducer — tell patients to avoid with any chronic meds');
        hr();
        rw('Key CYP3A4 substrates at risk:','','#9060c0');
        nt('Tacrolimus/cyclosporine: narrow therapeutic window — check levels after ANY inhibitor/inducer');
        nt('Statins (simvastatin, atorvastatin): ↑ levels with azoles/macrolides → rhabdomyolysis');
        nt('Fentanyl, midazolam: ↑ levels with azoles → prolonged sedation in ICU; reduce infusion rate');
    } else if(sel===1){
        rw('CYP2C9 — metabolizes warfarin (S-form), NSAIDs, phenytoin:','','#9060c0');
        hr();
        rw('Inhibitors (↑ warfarin effect):','Fluconazole, amiodarone, metronidazole, TMP-SMX','#cc4444','#ff9966');
        nt('Fluconazole + warfarin: INR can double within 3–5 days; reduce warfarin dose ~50%');
        nt('Amiodarone + warfarin: prolonged interaction (amiodarone t½ = 40–55 days); INR monitoring × weeks');
        hr();
        rw('CYP2C19 — metabolizes PPIs, clopidogrel, diazepam:','','#9060c0');
        rw('Clopidogrel:','Prodrug — requires CYP2C19 activation; PPIs inhibit → ↓ platelet effect','#aab','#eedd88');
        nt('PPI + clopidogrel: controversial; use pantoprazole (weakest 2C19 inhibitor) if needed');
        nt('CYP2C19 poor metabolizers (~20% Asian, ~3% Caucasian): inadequate clopidogrel activation');
        hr();
        rw('CYP2D6 — metabolizes codeine, tramadol, TCAs, metoprolol:','','#9060c0');
        rw('Codeine:','Prodrug → morphine via 2D6; ultra-rapid metabolizers → toxicity; PM = no analgesia','#aab','#eedd88');
        nt('Tramadol: 2D6 → active metabolite; PM = no analgesia; UM = respiratory depression risk');
        nt('Metoprolol: 2D6 substrate; fluoxetine/paroxetine inhibit 2D6 → ↑ metoprolol bradycardia');
        hr();
        nt('★ Pharmacogenomics: CPIC guidelines for CYP2C19 (clopidogrel) + CYP2D6 (codeine/tramadol)');
    } else {
        rw('Drug Adjustments in Hepatic Failure (Child-Pugh / MELD):','','#9060c0');
        hr();
        rw('Key pharmacokinetic changes in liver failure:','','#cc8844');
        nt('↓ albumin → ↑ free fraction of highly protein-bound drugs (phenytoin, warfarin, diazepam)');
        nt('↓ synthetic function → ↓ clotting factors, ↓ pseudocholinesterase (SCh metabolism slowed)');
        nt('↑ volume of distribution (ascites) → larger loading doses of water-soluble drugs');
        nt('Portosystemic shunting → ↓ first-pass metabolism → ↑ oral bioavailability of hepatic drugs');
        hr();
        rw('Drugs to avoid / reduce in severe liver failure:','','#cc4444');
        nt('Opioids: morphine/hydromorphone accumulate; fentanyl better (extrahepatic metabolism)');
        nt('Benzodiazepines: accumulate in cirrhosis; use lorazepam (direct conjugation, no active metabolites)');
        nt('NSAIDs: precipitate hepatorenal syndrome; avoid in Child-Pugh C');
        nt('Statins: use low dose; elevated LFTs common; contraindicated in acute hepatic failure');
        hr();
        rw('Drugs requiring no adjustment (non-hepatic):','','#3a9a5c');
        nt('Aminoglycosides, vancomycin, most beta-lactams: renally cleared — adjust for kidney, not liver');
        hr();
        nt('★ Child-Pugh C (score ≥ 10): reduce hepatic drug doses by 50–75%; frequent monitoring');
        nt('★ Encephalopathy risk: opioids, benzodiazepines, sedatives can precipitate HE — use sparingly');
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
    # ═══ receptor_map ═════════════════════════════════════════════════════════
    (
        "On the receptor map chart, α1 receptors are located on _______ smooth muscle cells "
        "and cause _______. Pure α1 agonist _______ causes a reflex _______ because it has no "
        "_______ activity. β2 receptors in bronchial smooth muscle cause _______, "
        "and β2 stimulation also shifts potassium _______.",

        "α1 receptors: vascular SMC → vasoconstriction, ↑ SVR\n"
        "| Pure α1 agonist: phenylephrine — causes reflex bradycardia (baroreceptor response to ↑ BP)\n"
        "| Reflex bradycardia: because phenylephrine has NO β1 activity (NE has β1 → no reflex)\n"
        "| β2 receptors: bronchial SMC → bronchodilation; also peripheral vasodilation, ↓ SVR\n"
        "| β2 stimulation: shifts K⁺ INTO cells (intracellular) → hypokalemia\n"
        "→ CCRN KEY: Receptor profiles of common vasopressors:\n"
        "• Norepinephrine: α1 >> β1 > β2 — vasopressor with mild inotropy; minimal ↓ SVR\n"
        "• Epinephrine: α1 + β1 + β2 — all doses; low dose: β2 dominates (↑ CO, ↓ SVR)\n"
        "• Dopamine dose-dependent: 1–3 = DA; 5–10 = β1; > 10 = α1 (but variable, not precise)\n"
        "• Dobutamine: β1 + β2 (weak α1) — ↑ CO + modest ↓ SVR; cardiogenic shock\n"
        "→ MASTERY NOTE: Phenylephrine clinical niche:\n"
        "Vasodilatory shock with PRESERVED or HIGH cardiac output (septic shock with adequate CO + low SVR). "
        "Advantage: pure vasoconstriction without chronotropy — useful in AF with rapid ventricular rate "
        "when NE would further increase HR. AVOID in cardiogenic shock (↑ afterload → ↑ myocardial O₂ demand). "
        "Also used: nasal decongestant, pupil dilation, spinal anesthesia hypotension.",

        'tier-review',
        _NM,
        DID['mechanism_groups'],
        'receptor_map',
        '{"hi":0}',
        'chart-l1'
    ),
    (
        "On the receptor map chart, α2 receptor agonist _______ is used for ICU sedation "
        "because it provides sedation WITHOUT _______. "
        "β1 receptors are located in the _______, _______, and _______. "
        "Dobutamine acts primarily on _______ receptors causing _______ and modest _______.",

        "α2 agonist dexmedetomidine: ICU sedation WITHOUT respiratory depression\n"
        "| Mechanism: locus coeruleus (brainstem) α2 → ↓ norepinephrine release → sedation/analgesia\n"
        "| No GABA effect (unlike benzos/propofol) → preserved respiratory drive\n"
        "| Also: opioid-sparing, delirium reduction, alcohol/opioid withdrawal adjunct\n"
        "| β1 receptors: SA node, AV node, ventricular myocardium\n"
        "| β1 effects: ↑ HR (chronotropy), ↑ contractility (inotropy), ↑ AV conduction (dromotropy)\n"
        "| Dobutamine: β1 + β2 → ↑ CO + modest ↓ SVR; cardiogenic shock (↑ CO without ↑ afterload)\n"
        "→ CCRN KEY: Dexmedetomidine vs propofol in ICU sedation:\n"
        "• Dexmedetomidine: no respiratory depression, cooperative sedation, ↓ delirium (MENDS/MIDEX trials)\n"
        "• Propofol: rapid onset/offset, no analgesic effect, PRIS risk at > 4 mg/kg/hr × 48h\n"
        "• Dexmedetomidine side effects: bradycardia, hypotension (loading dose related) — give loading dose slowly\n"
        "• Dexmedetomidine max FDA-approved: 0.7 mcg/kg/hr; off-label up to 1.5 mcg/kg/hr in select cases\n"
        "→ MASTERY NOTE: Isoproterenol (pure β1 + β2 agonist):\n"
        "• Last resort for bradycardia refractory to atropine — bridge to pacemaker\n"
        "• Causes profound tachycardia and ↑ myocardial oxygen demand\n"
        "• Torsades de pointes with long QT: isoproterenol ↑ HR → shortens QT (drug of choice for TdP)\n"
        "• NOT a vasopressor — β2 causes ↓ SVR; BP may paradoxically drop with isoproterenol.",

        'tier-high',
        _NM,
        DID['mechanism_groups'],
        'receptor_map',
        '{"hi":2}',
        'chart-l2'
    ),
    (
        "The receptor chart shows dopamine receptors (DA1) cause renal _______, "
        "and 'renal dose dopamine' (1–3 mcg/kg/min) is _______ recommended by evidence. "
        "Muscarinic (mAChR) blockade by _______ treats organophosphate toxicity by drying secretions. "
        "The muscarinic M2 receptor at the SA node mediates _______ when stimulated.",

        "DA1 receptors: renal and mesenteric vasodilation → ↑ GFR + natriuresis\n"
        "| Renal dose dopamine (1–3 mcg/kg/min): NOT recommended — no evidence prevents AKI or reduces mortality\n"
        "| Fenoldopam (selective DA1 agonist): used for hypertensive crisis (↑ renal blood flow + ↓ BP)\n"
        "| mAChR (muscarinic) blockade by atropine: dries secretions, ↑ HR, reverses bronchospasm\n"
        "| M2 receptor at SA/AV nodes: vagal stimulation → ↓ HR, ↓ AV conduction (vasovagal response)\n"
        "→ CCRN KEY: Why is 'renal dose dopamine' no longer used?\n"
        "• Bellomo trial (NEJM 2000, n=328): low-dose dopamine vs placebo in ICU — NO difference in peak Cr, "
        "RRT requirement, or mortality.\n"
        "• Risk: tachyarrhythmias even at 'low' doses; variable receptor activation at same dose\n"
        "• Alternative: optimize volume status, avoid nephrotoxins, treat hypotension with appropriate vasopressors\n"
        "→ MASTERY NOTE: Atropine receptor pharmacology in clinical practice:\n"
        "• Atropine: non-selective mAChR blocker (M1/M2/M3)\n"
        "• M2 blockade → ↑ HR (blocks vagal tone) — use: bradycardia, organophosphate, succinylcholine bradycardia in children\n"
        "• M3 blockade → ↓ secretions, bronchodilation, ↑ pupil (mydriasis)\n"
        "• High-dose atropine in organophosphate poisoning: endpoint is DRY SECRETIONS (M3 effect), "
        "not heart rate — tachycardia is expected and acceptable during treatment.",

        'tier-critical',
        _NM,
        DID['mechanism_groups'],
        'receptor_map',
        '{"hi":4}',
        'chart-l3'
    ),

    # ═══ antibiotic_class ═════════════════════════════════════════════════════
    (
        "The antibiotic mechanisms chart shows beta-lactams inhibit _______ (PBPs), "
        "blocking _______. Cefepime (4th generation) covers gram-negatives including _______. "
        "Vancomycin instead inhibits _______ and is monitored by _______ target of _______.",

        "Beta-lactams inhibit PBPs (penicillin-binding proteins = transpeptidases) → block cell wall cross-linking\n"
        "| Cefepime (4th generation): gram-positive + Pseudomonas aeruginosa + some ESBL (not reliable)\n"
        "| Ceftaroline (5th generation): MRSA-active cephalosporin\n"
        "| Carbapenems (meropenem/imipenem): broadest coverage including ESBL — NOT MRSA\n"
        "| Vancomycin: inhibits cell wall transglycosylation (different from PBP inhibition)\n"
        "| Vancomycin monitoring: AUC/MIC target 400–600 (PK/PD-guided, not just trough)\n"
        "→ CCRN KEY: Beta-lactam resistance mechanisms:\n"
        "• MRSA: altered PBP (PBP2a) — methicillin/oxacillin resistance; all beta-lactams EXCEPT ceftaroline fail\n"
        "• ESBL (extended-spectrum beta-lactamase): hydrolysis of penicillins + cephalosporins; carbapenems active\n"
        "• Carbapenem-resistant Enterobacteriaceae (CRE/KPC): carbapenemase enzymes — use ceftazidime-avibactam\n"
        "→ MASTERY NOTE: Pip-tazobactam (4.5g q6h extended 4-hour infusion) vs standard 30-min infusion:\n"
        "• Beta-lactam killing = TIME above MIC (not peak concentration)\n"
        "• Extended infusion: 4h drip maintains drug concentration above Pseudomonas MIC for 50% of dosing interval\n"
        "• Standard bolus: same dose but rapid clearance → drug level drops below MIC too quickly\n"
        "• Clinical outcome: extended infusion associated with ↓ mortality in P. aeruginosa bacteremia (retrospective).",

        'tier-review',
        _NM,
        DID['mechanism_groups'],
        'antibiotic_class',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The antibiotic chart shows aminoglycosides inhibit the _______ ribosomal subunit. "
        "The preferred dosing strategy is _______ (once-daily) because aminoglycosides show "
        "_______ dependent killing. Linezolid covers _______ and _______, "
        "but causes _______ syndrome risk when combined with serotonergic drugs.",

        "Aminoglycosides: inhibit 30S ribosomal subunit → misreading of mRNA → aberrant protein synthesis\n"
        "| Preferred dosing: once-daily (extended interval) — concentration-dependent killing\n"
        "| Goal: high peak/MIC ratio (Cmax/MIC > 8–10) achieved by larger single dose\n"
        "| Nephrotoxicity: proximal tubule accumulation — less with once-daily than multiple daily doses\n"
        "| Linezolid (oxazolidinone): inhibits 50S + 30S — unique mechanism; bacteriostatic\n"
        "| Coverage: MRSA + VRE (FDA-approved); also resistant gram+ when vancomycin fails\n"
        "| Serotonin syndrome risk: MAO-A inhibition → avoid with SSRIs, MAOIs, tramadol\n"
        "→ CCRN KEY: Aminoglycoside toxicity monitoring:\n"
        "• Nephrotoxicity: ↑ SCr, tubular casts; risk ↑ with: hypovolemia, other nephrotoxins, prolonged course\n"
        "• Ototoxicity: irreversible (cochlear + vestibular); risk ↑ with total cumulative dose\n"
        "• Traditional monitoring: trough < 1 mcg/mL (gentamicin/tobramycin); peak 8–10 mcg/mL\n"
        "• AUC-guided monitoring increasingly used for vancomycin AND aminoglycosides\n"
        "→ MASTERY NOTE: Daptomycin — cell membrane disruption (gram-positive only):\n"
        "• Approved: MRSA bacteremia, endocarditis, SSTI\n"
        "• Do NOT use for pneumonia — inactivated by pulmonary surfactant\n"
        "• Monitor: CK levels (myopathy — check weekly); hold statins if CK ↑\n"
        "• Tigecycline (50S inhibitor): broad spectrum (MRSA + ESBL + anaerobes) — "
        "but ↑ mortality in VAP trial; use only when no alternatives for non-lung infections.",

        'tier-high',
        _NM,
        DID['mechanism_groups'],
        'antibiotic_class',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "On the antibiotic mechanisms chart, fluoroquinolones inhibit _______ in gram-negatives "
        "and _______ in gram-positives. Class-wide adverse effects include _______, "
        "and chelation with _______ ions reduces oral absorption. "
        "Metronidazole works by _______ and treats _______ (note: do NOT use for non-anaerobic gram-positive infections).",

        "Fluoroquinolones: inhibit DNA gyrase (gram-negatives) + topoisomerase IV (gram-positives) → DNA strand breaks\n"
        "| Class AEs: QTc prolongation, Achilles tendon rupture, peripheral neuropathy, CNS effects (seizures)\n"
        "| Chelation: divalent cations (Mg²⁺, Ca²⁺, Al³⁺, Fe²⁺) bind FQ in GI tract → ↓ absorption\n"
        "  Space apart by at least 2–4 hours (give FQ first)\n"
        "| Metronidazole: activated by anaerobic bacteria → DNA strand breakage (electron acceptor mechanism)\n"
        "| Coverage: anaerobes + protozoa (Trichomonas, Giardia, amebiasis); C. diff mild-moderate\n"
        "→ CCRN KEY: Fluoroquinolone clinical niches in ICU:\n"
        "• Ciprofloxacin: best anti-Pseudomonas FQ; HAP/VAP combination therapy; UTI\n"
        "• Levofloxacin: 'respiratory FQ'; CAP (Legionella, Strep) + UTI; less Pseudomonas than cipro\n"
        "• Moxifloxacin: anaerobic coverage + CAP; no renal adjustment needed; NOT for UTI (no urine excretion)\n"
        "→ MASTERY NOTE: TMP-SMX (trimethoprim-sulfamethoxazole) — sequential folate inhibition:\n"
        "• TMP inhibits dihydrofolate reductase; SMX inhibits PABA incorporation\n"
        "• Two-step inhibition = synergistic bactericidal effect\n"
        "• High-dose for PCP (Pneumocystis jirovecii pneumonia): 15–20 mg/kg/day (TMP component) × 21 days\n"
        "• ICU toxicities: hyperkalemia (TMP blocks ENaC, like spironolactone), nephrotoxicity, bone marrow suppression\n"
        "• Also covers: MRSA SSTI (oral step-down); Listeria; Nocardia; Toxoplasma (with pyrimethamine).",

        'tier-critical',
        _NM,
        DID['mechanism_groups'],
        'antibiotic_class',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ coagulation_targets ══════════════════════════════════════════════════
    (
        "The coagulation chart shows the extrinsic pathway is measured by _______ (INR) "
        "and the intrinsic pathway by _______. "
        "UFH mechanism is to bind _______, which then inhibits factors _______ and _______. "
        "Argatroban is used in HIT because it is a direct _______ inhibitor cleared by _______.",

        "Extrinsic pathway (PT/INR): tissue factor + factor VII → activates factor X\n"
        "| Intrinsic pathway (aPTT): XII → XI → IX → X (with factor VIII as cofactor)\n"
        "| UFH mechanism: binds antithrombin (AT) → AT-UFH complex inhibits IIa (thrombin) + Xa\n"
        "| Argatroban: direct thrombin inhibitor (DTI); binds thrombin active site directly\n"
        "| Argatroban clearance: hepatic — use in HIT (no cross-reactivity) AND in renal failure\n"
        "→ CCRN KEY: UFH monitoring options:\n"
        "• aPTT: most widely used; target 60–100s (therapeutic); affected by lupus anticoagulant, factor deficiencies\n"
        "• Anti-Xa: more specific; target 0.3–0.7 IU/mL (therapeutic heparin); preferred in: obesity, APS, abnormal baseline aPTT\n"
        "• ACT (activated clotting time): used in cardiac cath lab/bypass; target > 300s for CPB\n"
        "→ MASTERY NOTE: HIT (Heparin-Induced Thrombocytopenia) — key pharmacology points:\n"
        "• STOP all heparin immediately (including line flushes, heparin-coated catheters)\n"
        "• Start NON-heparin anticoagulant: argatroban (hepatic clearance) OR bivalirudin (renal + enzymatic)\n"
        "• Fondaparinux: alternative (indirect Xa inhibitor; no HIT cross-reactivity documented)\n"
        "• Do NOT start warfarin until platelets > 150K (risk of venous gangrene from protein C drop)\n"
        "• 4T score: Thrombocytopenia + Timing + Thrombosis + oTher causes (≤ 3 = low probability).",

        'tier-review',
        _NM,
        DID['mechanism_groups'],
        'coagulation_targets',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The coagulation chart shows dabigatran is _______ % renally cleared "
        "and can be reversed by _______. "
        "Apixaban + rivaroxaban are reversed by _______ (FDA approved _______). "
        "The DOAC with approved use for both PAH AND CTEPH is _______.",

        "Dabigatran (direct thrombin inhibitor): 80% renal clearance\n"
        "| Reversed by: idarucizumab (Praxbind) — 5 g IV (two 2.5g vials); complete reversal within minutes\n"
        "| Also removed by hemodialysis (80% renal clearance → dialyzable)\n"
        "| Apixaban + rivaroxaban (factor Xa inhibitors) reversed by: andexanet alfa (Andexxa)\n"
        "| Andexanet FDA approved: 2018; administered as IV bolus + infusion; very expensive (~$24,000/dose)\n"
        "| Riociguat: NOT a DOAC — it's a soluble guanylate cyclase stimulator for PAH + CTEPH (not PDE5i)\n"
        "→ CCRN KEY: DOAC reversal decision in ICU:\n"
        "• Life-threatening bleed: give reversal agent + stop DOAC\n"
        "• Urgent surgery: reversal if drug effect suspected (anti-Xa level or dTT for dabigatran)\n"
        "• 4F-PCC: off-label reversal for Xa inhibitors when andexanet unavailable — reasonable alternative\n"
        "→ MASTERY NOTE: Anti-Xa levels for DOAC management:\n"
        "• Rivaroxaban: peak level 2h post-dose; trough 12–24h post-dose\n"
        "• Apixaban: similar timing; lower levels vs rivaroxaban at equivalent clinical dosing\n"
        "• Level > 50 ng/mL at trough = significant drug effect — consider reversal before surgery\n"
        "• Level < 30 ng/mL = minimal drug effect — may proceed with many procedures without reversal\n"
        "Fondaparinux (indirect Xa via AT): NO approved reversal agent; 4F-PCC off-label; wait ~17h (t½).",

        'tier-high',
        _NM,
        DID['mechanism_groups'],
        'coagulation_targets',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "On the coagulation reversal chart, warfarin reversal for INR > 6 with life-threatening bleeding "
        "uses _______ units/kg of 4F-PCC PLUS _______. "
        "Protamine reverses UFH at _______ mg per _______ units of heparin. "
        "Tranexamic acid (TXA) is given in trauma within _______ hours and works by inhibiting _______.",

        "Warfarin reversal — life-threatening bleeding:\n"
        "| 4F-PCC (KCentra) dose: INR > 6 → 50 units/kg IV (max 5,000 units)\n"
        "| Must also give Vitamin K 10 mg IV (prevents re-elevation when PCC factors wear off at 6–12h)\n"
        "| Protamine: 1 mg per 100 units UFH; max 50 mg per dose\n"
        "  Partially reverses LMWH (~60%): give if recent LMWH; does NOT reverse fondaparinux\n"
        "| TXA (tranexamic acid): inhibits plasminogen → prevents fibrinolysis → stabilizes clot\n"
        "| Trauma: give within 3 hours of injury (CRASH-2 trial: ↓ mortality; harmful if > 3h delay)\n"
        "→ CCRN KEY: 4F-PCC vs FFP for warfarin reversal:\n"
        "• 4F-PCC: immediate reversal, small volume (25–50 mL vs liters of FFP), no thaw time\n"
        "• FFP: reverses all factors but requires 15–20 min thaw, 10–15 mL/kg volume → fluid overload risk\n"
        "• 4F-PCC preferred for: urgent reversal, heart failure, volume-sensitive patients\n"
        "→ MASTERY NOTE: TXA clinical applications beyond trauma:\n"
        "• OB hemorrhage: 1 g IV within 3h of delivery (WHO/WOMAN trial — ↓ mortality from PPH)\n"
        "• Cardiac surgery: perioperative TXA → ↓ transfusion requirements (ATACAS trial)\n"
        "• Intracerebral hemorrhage: TICH-2 trial — TXA did NOT improve outcomes at 90 days (no benefit)\n"
        "• Topical: oral rinse for gingival bleeding in anticoagulated patients; ophthalmic surgery\n"
        "TXA adverse effects: venous thromboembolism (monitor), seizures at high doses (GABA antagonism).",

        'tier-critical',
        _NM,
        DID['mechanism_groups'],
        'coagulation_targets',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ renal_dose_adjust ════════════════════════════════════════════════════
    (
        "The renal adjustment chart shows NSAIDs cause AKI by constricting the _______ arteriole. "
        "IV contrast nephropathy is prevented by pre-hydration with _______ and holding _______ for 48 hours. "
        "In patients on ACE-inhibitors who develop AKI, the drug should be _______ because it "
        "reduces _______ arteriole tone, decreasing _______.",

        "NSAIDs cause AKI: inhibit prostaglandins → constrict AFFERENT arteriole → ↓ GFR\n"
        "| (Prostaglandins normally dilate the afferent arteriole to maintain GFR)\n"
        "| IV contrast nephropathy prevention: isotonic saline (0.9% NS or LR) pre- and post-procedure\n"
        "| Hold metformin 48h before AND after contrast (risk of lactic acidosis if contrast causes AKI)\n"
        "| ACE-inhibitors in AKI: reduce EFFERENT arteriole tone → ↓ GFR → hold in AKI\n"
        "| Mechanism: ACEi block angiotensin II → efferent dilation → ↓ glomerular filtration pressure\n"
        "→ CCRN KEY: ACEi/ARB timing in AKI:\n"
        "• Hold if SCr rises > 30% above baseline within 1–2 weeks of starting ACEi\n"
        "• In bilateral renal artery stenosis: ACEi can precipitate acute anuric AKI — absolute CI\n"
        "• In CKD: ACEi/ARB are PROTECTIVE long-term (↓ proteinuria, slow progression) — "
        "hold only in acute decompensation, restart when stable\n"
        "→ MASTERY NOTE: NAC (N-acetylcysteine) for contrast nephropathy:\n"
        "• Multiple meta-analyses: conflicting results; PRESERVE trial (NEJM 2018, n=4,993): "
        "NAC + sodium bicarbonate = NO benefit over isotonic saline alone\n"
        "• Current AHA/ACC guidance: IV isotonic saline is the only evidence-based prevention\n"
        "• NAC may still be ordered (cheap, low risk) but do not rely on it — hydration is the intervention\n"
        "Calcineurin inhibitors (tacrolimus/cyclosporine): nephrotoxic via direct vasoconstriction "
        "(afferent > efferent); check drug levels if AKI develops in transplant patients.",

        'tier-review',
        _NM,
        DID['mechanism_groups'],
        'renal_dose_adjust',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the renal dose adjustment chart, morphine is problematic in AKI because its active metabolite "
        "_______ accumulates, causing _______. The preferred opioid in AKI/CKD is _______. "
        "In CrCl < 30 mL/min, LMWH (enoxaparin) should be _______ and replaced with _______ "
        "monitored by _______.",

        "Morphine in AKI: active metabolite M6G (morphine-6-glucuronide) accumulates → respiratory depression\n"
        "| Preferred opioid in AKI: hydromorphone (no active accumulating metabolites in moderate CKD)\n"
        "| Fentanyl: safe in CKD (hepatic metabolism, extrahepatic clearance) — preferred in severe AKI\n"
        "| LMWH (enoxaparin) in CrCl < 30: AVOID therapeutic dose (anti-Xa accumulation → bleeding)\n"
        "| Replace with: UFH (unfractionated heparin) — not renally cleared; monitor aPTT or anti-Xa\n"
        "| UFH monitoring: aPTT 60–100s or anti-Xa 0.3–0.7 IU/mL\n"
        "→ CCRN KEY: Opioid metabolism in renal failure — summary:\n"
        "• Codeine: avoid in AKI — accumulation of active metabolites; CYP2D6 variability too\n"
        "• Tramadol: avoid in CrCl < 30 — active metabolites accumulate → seizure risk\n"
        "• Meperidine: AVOID in CKD — normeperidine accumulates → tremors, myoclonus, seizures\n"
        "• Hydromorphone: can be used with dose reduction in moderate CKD; avoid in ESRD\n"
        "• Fentanyl: preferred in ESRD/dialysis patients (hepatic/extrahepatic clearance)\n"
        "→ MASTERY NOTE: Gabapentin/pregabalin in CKD:\n"
        "• 100% renally cleared — significant accumulation in CKD\n"
        "• Normal dose: gabapentin 300 mg TID → in CrCl 15–29: 200–700 mg/day (single daily dose)\n"
        "• Clinical effect of accumulation: somnolence, respiratory depression, fall risk\n"
        "• Dialysis patients: gabapentin 100–300 mg after each dialysis session (removed by HD).",

        'tier-high',
        _NM,
        DID['mechanism_groups'],
        'renal_dose_adjust',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The CRRT drug dosing chart shows drugs are removed based on _______ weight, "
        "_______ binding, and volume of distribution. "
        "The KDIGO target effluent rate for CRRT is _______ mL/kg/hour. "
        "Regional citrate anticoagulation for CRRT circuits risks _______ in the patient.",

        "CRRT drug removal depends on: low molecular weight + low protein binding + low volume of distribution\n"
        "| KDIGO CRRT effluent rate target: 20–25 mL/kg/h (minimum 20; typical 25 mL/kg/h)\n"
        "| Regional citrate anticoagulation (RCA): citrate chelates Ca²⁺ in circuit → prevents clotting\n"
        "| RCA risk: hypocalcemia in patient (citrate returns Ca²⁺-depleted blood → systemic Ca²⁺ drops)\n"
        "| Monitor: ionized calcium every 4–6h; replace calcium via separate IV line\n"
        "→ CCRN KEY: Vancomycin dosing on CRRT:\n"
        "• CRRT removes vancomycin significantly — cannot use intermittent dosing without monitoring\n"
        "• Loading dose: 25–30 mg/kg (standard — CRRT doesn't affect loading)\n"
        "• Maintenance: 7.5–15 mg/kg q12–24h (highly variable based on CRRT modality + effluent rate)\n"
        "• Target: AUC/MIC 400–600 — trough-only monitoring underestimates exposure on CRRT\n"
        "• Check vancomycin level: 6h after dose in CRRT (not pre-dose as in standard)\n"
        "→ MASTERY NOTE: CRRT antibiotic dosing principles:\n"
        "• Beta-lactams: time-dependent killing — extended infusion maintains drug level > MIC\n"
        "  Meropenem on CVVHDF: 1g q8h extended infusion (4h) achieves target attainment\n"
        "• Antifungals: fluconazole substantially removed by CRRT → use 400–800 mg/day\n"
        "  Micafungin/caspofungin: highly protein-bound → minimal CRRT removal → standard dosing\n"
        "• Drugs NOT significantly removed by CRRT (standard dosing): propofol, fentanyl, amiodarone "
        "(all high protein binding and/or large Vd — drug stays bound in tissue compartment).",

        'tier-critical',
        _NM,
        DID['mechanism_groups'],
        'renal_dose_adjust',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ cyp450_interactions ══════════════════════════════════════════════════
    (
        "The CYP450 chart shows _______ is the strongest CYP3A4 inducer and can reduce "
        "tacrolimus levels by up to _______-fold. "
        "Strong CYP3A4 inhibitors include the _______ antifungals. "
        "Fentanyl and midazolam are CYP3A4 _______, so azole antifungals can cause _______ "
        "by inhibiting their metabolism in ICU patients.",

        "Strongest CYP3A4 inducer: rifampin (rifampicin) — can ↓ drug levels by 2–10-fold\n"
        "| Tacrolimus: narrow therapeutic window; rifampin can drop levels to sub-therapeutic within 24–48h\n"
        "| Strong CYP3A4 inhibitors: azole antifungals (fluconazole, voriconazole, itraconazole)\n"
        "| Also: macrolides (erythromycin, clarithromycin); amiodarone; ritonavir\n"
        "| Fentanyl + midazolam: CYP3A4 substrates — azoles inhibit metabolism → drug accumulation\n"
        "| Clinical: prolonged sedation + respiratory depression in ICU when azoles added to fentanyl/midazolam infusions\n"
        "→ CCRN KEY: Amiodarone drug interactions in ICU (very common):\n"
        "• Amiodarone inhibits CYP2C9 + CYP3A4 + P-glycoprotein\n"
        "• Amiodarone + warfarin: INR can increase 2–3× → reduce warfarin dose 30–50% on initiation\n"
        "• Amiodarone + digoxin: ↑ digoxin levels → reduce digoxin dose by 50%\n"
        "• Amiodarone t½ = 40–55 days → interaction persists for months after stopping amiodarone\n"
        "→ MASTERY NOTE: Voriconazole (strongest azole for invasive aspergillosis) drug interactions:\n"
        "• Inhibits CYP2C9 + CYP2C19 + CYP3A4 — broadest CYP inhibition of all azoles\n"
        "• Voriconazole + tacrolimus: reduce tacrolimus dose by 67–75% (3-fold interaction)\n"
        "• Voriconazole + warfarin: daily INR monitoring during first week\n"
        "• Voriconazole + sirolimus: ABSOLUTE CI — sirolimus levels increase > 10-fold\n"
        "• Monitor: visual disturbances (most common), QTc prolongation, hepatotoxicity.",

        'tier-review',
        _NM,
        DID['mechanism_groups'],
        'cyp450_interactions',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The CYP2C19 chart shows clopidogrel is a _______ requiring CYP2C19 activation. "
        "PPIs inhibit CYP2C19 — the safest PPI to use with clopidogrel is _______ "
        "because it is the weakest CYP2C19 inhibitor. "
        "Patients who are CYP2D6 poor metabolizers cannot effectively convert _______ to morphine, "
        "resulting in _______.",

        "Clopidogrel: prodrug — must be activated by CYP2C19 to active thiol metabolite\n"
        "| PPIs inhibit CYP2C19 → ↓ clopidogrel activation → ↓ platelet inhibition\n"
        "| Safest PPI with clopidogrel: pantoprazole (weakest CYP2C19 inhibitor)\n"
        "| Avoid: omeprazole (strongest 2C19 inhibitor — most clinical concern with clopidogrel)\n"
        "| CYP2D6 poor metabolizers (PM): cannot convert codeine → morphine (no analgesic effect)\n"
        "| CYP2D6 ultra-rapid metabolizers (UM): excessive morphine conversion → respiratory depression\n"
        "→ CCRN KEY: Clinical implications of clopidogrel-PPI interaction:\n"
        "• FDA warning (2009): avoid omeprazole + clopidogrel concurrently\n"
        "• Clinical evidence: COGENT trial — omeprazole + clopidogrel: no ↑ CV events (underpowered)\n"
        "• Current practice: use pantoprazole if GI protection needed with clopidogrel-based therapy\n"
        "→ MASTERY NOTE: Pharmacogenomics in ICU pain management:\n"
        "• CPIC guidelines: do not use codeine in CYP2D6 UM or PM patients\n"
        "• Tramadol: 2D6-metabolized; PM = no effect; UM = toxicity; avoid when status unknown\n"
        "• Metoprolol: 2D6 substrate; fluoxetine/paroxetine (2D6 inhibitors) → ↑ metoprolol → bradycardia\n"
        "• Routine pharmacogenomic testing increasingly available — relevant for long-term ICU pain management.",

        'tier-high',
        _NM,
        DID['mechanism_groups'],
        'cyp450_interactions',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The hepatic failure drug chart shows that cirrhosis causes _______ of albumin, "
        "increasing the _______ fraction of highly protein-bound drugs. "
        "Among benzodiazepines, _______ is preferred in hepatic failure because it undergoes "
        "direct conjugation without active metabolites. "
        "Portosystemic shunting _______ first-pass metabolism, increasing oral bioavailability of hepatic drugs.",

        "Cirrhosis effects on pharmacokinetics:\n"
        "| ↓ Albumin synthesis → ↑ free fraction of protein-bound drugs (phenytoin, warfarin, diazepam)\n"
        "| ↓ Hepatic synthetic function → ↓ clotting factors, ↓ pseudocholinesterase (↓ SCh metabolism)\n"
        "| Portosystemic shunting → ↓ first-pass metabolism → ↑ oral bioavailability of hepatic drugs\n"
        "| Preferred benzodiazepine in hepatic failure: lorazepam (direct glucuronidation — no active metabolites)\n"
        "| Avoid: diazepam, midazolam (active metabolites accumulate in liver failure → prolonged sedation)\n"
        "→ CCRN KEY: Drug selection in liver failure — summary:\n"
        "• Opioids: fentanyl preferred (extrahepatic metabolism); morphine accumulates\n"
        "• Benzodiazepines: lorazepam > oxazepam > midazolam = diazepam (worst)\n"
        "• NSAIDs: avoid — precipitate hepatorenal syndrome in Child-Pugh C cirrhosis\n"
        "• Statins: use low dose cautiously; contraindicated in acute liver failure\n"
        "→ MASTERY NOTE: Pseudocholinesterase (plasma cholinesterase) in liver disease:\n"
        "• Synthesized by liver; ↓ in cirrhosis, malnutrition, pregnancy\n"
        "• Metabolizes: succinylcholine (SCh) + mivacurium + ester local anesthetics (procaine, chloroprocaine)\n"
        "• Pseudocholinesterase deficiency: prolonged SCh block ('succinylcholine apnea') — "
        "patient remains paralyzed after RSI; manage with ventilator support until drug wears off naturally\n"
        "• Genetic variant (dibucaine number): screen in patients with prior SCh sensitivity or family history.",

        'tier-critical',
        _NM,
        DID['mechanism_groups'],
        'cyp450_interactions',
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
