#!/usr/bin/env python3
"""chunk43_charts.py — Ph7 Neuromuscular Blocking Agents (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_42.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_43.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c43')
CHUNK_NUM   = 43
MID_BASE    = 1_800_005_060
CHART_ORDER = ['nmba_comparison', 'train_of_four', 'sux_rsi',
               'nmba_reversal', 'icu_paralysis']

_NM = 'Ph7 · \U0001f7e1 T3 · Pharmacology — Neuromuscular Blocking Agents'

RF = {}

# ── Chart 1: NMBA Drug Comparison ─────────────────────────────────────────────
RF['nmba_comparison'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var drugs=[
        {name:'Succinylcholine',type:'Depolarizing\n(Phase I → II)',onset:'30–60 sec',dur:'5–10 min',clear:'Plasma pseudocholinesterase',use:'RSI induction only\n(CI in many states)',c:'#cc3333'},
        {name:'Rocuronium',     type:'Non-depol\n(aminosteroid)', onset:'60–90 sec\n(1.2 mg/kg)',dur:'25–45 min',clear:'Hepatic/biliary\n(renal minor)',use:'RSI alternative to sux\nReversible with sugammadex',c:'#3a9a5c'},
        {name:'Vecuronium',     type:'Non-depol\n(aminosteroid)', onset:'3–5 min',     dur:'20–35 min',clear:'Hepatic (active\nmetabolite in hepatic failure)',use:'Short procedures\nAvoid liver failure',c:'#4488cc'},
        {name:'Cisatracurium',  type:'Non-depol\n(benzylisoquinol)',onset:'2–3 min',   dur:'25–45 min',clear:'Hofmann elimination\n(organ-independent)',use:'PREFERRED: prolonged\nICU paralysis',c:'#e07020'},
        {name:'Pancuronium',    type:'Non-depol\n(aminosteroid)', onset:'3–5 min',     dur:'60–100 min',clear:'Renal (avoid AKI)\nHepatically active',use:'AVOID in ICU\n(tachycardia, accumulation)',c:'#9060c0'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=20, rh=Math.floor((H-hdrH)/drugs.length);
    var xs=[4,130,230,295,385,618];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Drug','Type','Onset','Duration','Clearance','ICU Use'];
    ctx.font='bold 8.5px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-5);});
    drugs.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=d.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=d.c;ctx.font='bold 9px sans-serif';ctx.textAlign='left';
        ctx.fillText(d.name,xs[0]+3,ry+rh/2+3);
        ctx.fillStyle='#aab';ctx.font='8.5px sans-serif';
        d.type.split('\n').forEach(function(tl,ti){ctx.fillText(tl,xs[1]+3,ry+rh/2-2+ti*10);});
        ctx.fillStyle='#ccc';ctx.font='9px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.onset.split('\n')[0],(xs[2]+xs[3])/2,ry+rh/2+3);
        ctx.fillText(d.dur,(xs[3]+xs[4])/2,ry+rh/2+3);
        ctx.fillStyle='#778';ctx.font='8.5px sans-serif';ctx.textAlign='left';
        d.clear.split('\n').forEach(function(cl,ci){ctx.fillText(cl,xs[4]+3,ry+rh/2-2+ci*10);});
        ctx.fillStyle=d.use.startsWith('AVOID')?'#cc4444':(d.use.startsWith('PREFERRED')?'#e07020':'#9ab8aa');
        ctx.font='9px sans-serif';
        d.use.split('\n').forEach(function(ul,ui){ctx.fillText(ul,xs[5]+3,ry+rh/2-2+ui*10);});
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
        var lbs=['Sux','Roc','Vec','Cis','Pan'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,drugs[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: Train-of-Four Monitoring ────────────────────────────────────────
RF['train_of_four'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var tof=(P.tof!==undefined)?P.tof:2;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    ctx.fillStyle='#333';ctx.font='bold 9px sans-serif';ctx.textAlign='center';
    ctx.fillText('TRAIN-OF-FOUR (TOF) MONITORING — Ulnar Nerve',W/2,13);
    var bx0=60, bw=100, bh=60, by=20, gap=28;
    var colors4=[_GN,_GN,_GN,_GN];
    var colors2=['#e07020','#e07020','#333','#333'];
    var colors1=['#cc3333','#555','#555','#555'];
    var getCol=function(i){return i<tof?(tof===4?_GN:(tof===3?_GN:(tof===2?'#e07020':'#cc3333'))):'#1a1a1a';};
    for(var ti=0;ti<4;ti++){
        var bxi=bx0+ti*(bw+gap);
        var present=(ti<tof);
        var col=present?(tof>=3?_GN:(tof===2?'#e07020':'#cc3333')):'#1a1a1a';
        ctx.fillStyle=col;ctx.fillRect(bxi,by,bw,bh);
        ctx.strokeStyle=present?col:'#2a2a2a';ctx.lineWidth=present?2:1;ctx.strokeRect(bxi,by,bw,bh);
        if(present){
            ctx.fillStyle='#000';ctx.font='bold 20px sans-serif';ctx.textAlign='center';
            ctx.fillText('T'+(ti+1),bxi+bw/2,by+28);
            ctx.fillStyle='#000';ctx.font='bold 10px sans-serif';
            ctx.fillText('TWITCH',bxi+bw/2,by+46);
        } else {
            ctx.fillStyle='#333';ctx.font='bold 20px sans-serif';ctx.textAlign='center';
            ctx.fillText('T'+(ti+1),bxi+bw/2,by+28);
            ctx.fillStyle='#2a2a2a';ctx.font='bold 10px sans-serif';
            ctx.fillText('ABSENT',bxi+bw/2,by+46);
        }
    }
    var countY=by+bh+14;
    var tofCol=tof>=4?_GN:(tof>=2?'#e07020':'#cc3333');
    ctx.fillStyle=tofCol;ctx.font='bold 18px sans-serif';ctx.textAlign='left';
    ctx.fillText('TOF: '+tof+'/4',20,countY);
    var pct=tof===4?'~0%':tof===3?'~75%':tof===2?'~90%':tof===1?'~95%':'100%';
    ctx.fillStyle='#777';ctx.font='10px sans-serif';
    ctx.fillText('Estimated neuromuscular block: '+pct,140,countY);
    var barX=20,barW=W-40,barY2=countY+8,barH2=16;
    ctx.fillStyle='#1a3a1a';ctx.fillRect(barX,barY2,barW,barH2);
    var blockFrac=tof===4?0.02:tof===3?0.75:tof===2?0.90:tof===1?0.95:1.0;
    ctx.fillStyle=tofCol;ctx.fillRect(barX,barY2,Math.round(barW*blockFrac),barH2);
    ctx.strokeStyle='#333';ctx.lineWidth=1;ctx.strokeRect(barX,barY2,barW,barH2);
    ctx.fillStyle='#666';ctx.font='7.5px sans-serif';ctx.textAlign='left';
    ctx.fillText('0% block',barX,barY2+barH2+10);
    ctx.textAlign='right';ctx.fillText('100% block',barX+barW,barY2+barH2+10);
    var panelY=countY+barH2+20, panelH=H-panelY-4;
    ctx.fillStyle='#0a0a1a';ctx.fillRect(4,panelY,W-8,panelH);
    var interps={
        0:['Deep block (TOF 0/4): T1 absent — no twitches present','ARDS paralysis adequate; sustained >72h without reassessment = ICU-AW risk',
           'Action: Assess if deep block is clinically required; ensure analgesia/sedation adequate','Never use TOF 0/4 as routine ICU target'],
        1:['Moderate-deep block (TOF 1/4): only T1 present','Near 95% receptor occupancy — appropriate for intubation, severe ARDS',
           'ICU target: 2/4 is preferred (allows some monitoring of depth)','If consistently 1/4: consider dose reduction to achieve 2/4 target'],
        2:['Moderate block (TOF 2/4): T1 and T2 present — ICU TARGET ★','~90% neuromuscular blockade — appropriate for ARDS paralysis (ACURASYS)',
           'Action: Maintain current dose; reassess q4h; rotate electrode sites','Ensure deep sedation (RASS −4 to −5) and analgesia while paralyzed'],
        3:['Mild block (TOF 3/4): T1–T3 present','~75% receptor occupancy — may be recovering or under-dosed',
           'Action: Consider increasing infusion rate if deeper block required','Ensure patient still has adequate sedation/analgesia'],
        4:['Minimal/no block (TOF 4/4): all twitches present','Block has recovered OR dose is insufficient','Action: Assess need for NMB; consider bolus or increase infusion',
           'Before extubation: TOF 4/4 required; additional reversal if T4/T1 ratio <0.9']
    };
    var interp=interps[tof]||interps[2];
    var ly=panelY+14;
    interp.forEach(function(line,li){
        var isFirst=(li===0);
        ctx.fillStyle=isFirst?tofCol:'#aaa';ctx.font=isFirst?'bold 10px sans-serif':'9.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(line,10,ly);ly+=isFirst?16:13;
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin-top:6px;';
        var sl=_mkS('TOF:',0,4,1,tof,function(v){return v+'/4';},function(v){
            var p2={tof:Math.round(v)};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });
        row.appendChild(sl);ctrl.appendChild(row);
    }
}
"""

# ── Chart 3: Succinylcholine & RSI Decision ───────────────────────────────────
RF['sux_rsi'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['RSI Protocol','Sux: Indications','Sux: Contraindications','Roc: Alternative'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a2a3a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#cc6633':'#555';ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0a1a';ctx.fillRect(4,panelY,W-8,panelH);
    var content=[
        [['RSI (Rapid Sequence Intubation) — 7-Step Sequence','',
          '1. PREPARATION: IV access, monitors, suction, bag-mask, videolaryngoscope ready',
          '2. PREOXYGENATION: 100% FiO₂ × 3 min (NRB or BVM at 15 L/min); SpO₂ ≥95%',
          '3. PRETREATMENT (optional): Lidocaine 1.5 mg/kg (head injury), Atropine (peds)',
          '4. INDUCTION: Ketamine 1–2 mg/kg IV OR Etomidate 0.3 mg/kg IV',
          '5. PARALYTIC: Succinylcholine 1.5 mg/kg IV OR Rocuronium 1.2 mg/kg IV',
          '6. SELLICK\'S MANEUVER: Cricoid pressure (controversial — use with BVM not intubation)',
          '7. INTUBATE: Laryngoscopy after 45–60 sec; confirm placement (capnography + CXR)']],
        [['SUCCINYLCHOLINE — When to USE','',
          'RSI in patients WITHOUT contraindications',
          'FULL STOMACH / aspiration risk (most common RSI indication in ED/ICU)',
          'Need for very short paralysis (laryngospasm, brief laryngoscopy)',
          'Unknown difficult airway where RAPID recovery is essential',
          'Obese patients, pregnancy (standard doses, not dose-adjusted)',
          'Pediatric emergencies (IM dosing possible: 4 mg/kg if no IV)']],
        [['SUCCINYLCHOLINE — CONTRAINDICATIONS','',
          '★ Hyperkalemia risk (↑K⁺ by 0.5–1 mEq/L normally; life-threatening in:)',
          '  - Crush injuries, rhabdomyolysis, severe burns (>48h post-injury)',
          '  - Prolonged immobilization (>72h), denervation injuries (stroke, SCI)',
          '  - UMN/LMN lesions, Guillain-Barré, muscular dystrophy',
          '★ Personal/family history of malignant hyperthermia (MH) — ABSOLUTE CI',
          '★ Pseudocholinesterase deficiency — prolonged block (hours, not minutes)',
          '★ Open globe injury or acutely elevated ICP (transient ↑IOP with fasciculations)']],
        [['ROCURONIUM as RSI Alternative','',
          'RSI dose: 1.2 mg/kg IV (twice normal intubation dose) → onset 60–90 sec',
          'PREFERRED when succinylcholine is contraindicated',
          'FULLY reversible with sugammadex 16 mg/kg IV (reverses within 3 min)',
          'Cannot bite-reverse-rebreathe (CBRR) scenario is now managed with sugammadex',
          '','SUGAMMADEX REVERSAL OF ROCURONIUM:',
          'Routine reversal: 4 mg/kg IV (TOF ≥1 twitch)',
          'Immediate rescue reversal: 16 mg/kg IV (can-\'t intubate-can\'t oxygenate)']]
    ];
    var col=sel<content.length?content[sel][0]:[];
    var ly=panelY+14;
    col.forEach(function(line){
        if(line===''){ly+=4;return;}
        var isSect=(line.startsWith('RSI')||line.startsWith('SUC')||line.startsWith('ROC')||line.startsWith('SUG'));
        var isStar=line.startsWith('★');
        ctx.fillStyle=isSect?'#cc6633':(isStar?'#ee4444':'#bbb');
        ctx.font=(isSect||isStar)?'bold 9.5px sans-serif':'9.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(line,10,ly);ly+=isSect?15:12;
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

# ── Chart 4: NMBA Reversal Agents ────────────────────────────────────────────
RF['nmba_reversal'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var rows=[
        {prop:'Mechanism',     neo:'Acetylcholinesterase inhibitor\n(↑ ACh at NMJ)',       sug:'Chelating agent\n(binds + encapsulates rocuronium)',        c:'#4488cc'},
        {prop:'Target NMBAs',  neo:'All non-depolarizing NMBAs\n(vec, roc, pan, cis)',      sug:'ONLY rocuronium and vecuronium\n(does NOT reverse cis or pan)',    c:'#3a9a5c'},
        {prop:'TOF Required',  neo:'TOF ≥2/4 required\n(inadequate at deeper block)',       sug:'TOF 1–2/4: 4 mg/kg\nTOF 0/4 (rescue): 16 mg/kg',              c:'#e07020'},
        {prop:'Onset',         neo:'Slow: 10–15 min\n(must give atropine/glyco first)',     sug:'Rapid: 3–5 min (4mg/kg)\n1–3 min (16mg/kg rescue)',            c:'#38b2a4'},
        {prop:'Muscarinic SE', neo:'Yes — requires atropine 0.6–1.2 mg\nor glycopyrrolate 0.2 mg to prevent bradycardia/secretions', sug:'No muscarinic effects\n(clean reversal)',  c:'#cc3366'},
        {prop:'Key Advantage', neo:'Works for ALL non-depol NMBAs\nLower cost',             sug:'Rapid complete reversal\nCan-\'t-intubate-can\'t-oxygenate rescue',c:'#9060c0'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=20, rh=Math.floor((H-hdrH)/rows.length);
    var xs=[4,120,290,460,618];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Property','Neostigmine','Sugammadex','Notes'];
    ctx.font='bold 9px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-5);});
    rows.forEach(function(row,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=row.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=row.c;ctx.font='bold 9px sans-serif';ctx.textAlign='center';
        ctx.fillText(row.prop,(xs[0]+xs[1])/2,ry+rh/2+3);
        ctx.fillStyle='#bb9988';ctx.font='9px sans-serif';ctx.textAlign='left';
        row.neo.split('\n').forEach(function(nl,ni){ctx.fillText(nl,xs[1]+3,ry+rh/2-2+ni*10);});
        ctx.fillStyle='#88bbaa';ctx.font='9px sans-serif';
        row.sug.split('\n').forEach(function(sl,si){ctx.fillText(sl,xs[2]+3,ry+rh/2-2+si*10);});
        ctx.fillStyle='#8899aa';ctx.font='8.5px sans-serif';
        row.c.toString(); // just accessing c to avoid empty block
        ctx.fillStyle='#556678';ctx.font='8px sans-serif';
        ctx.fillText('',xs[3]+3,ry+rh/2+3);
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
        var lbs=['Mechanism','Target','TOF Req','Onset','Muscarinic','Advantage'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,rows[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 5: ICU Prolonged Paralysis & ICUAW ─────────────────────────────────
RF['icu_paralysis'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['ARDS Indication','Monitoring Protocol','ICUAW & Complications'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a2a3a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?_OR:'#555';ctx.font=(sel===i?'bold ':'')+'9px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0a1a';ctx.fillRect(4,panelY,W-8,panelH);
    var content=[
        [['ARDS INDICATION FOR NMBA (Cisatracurium preferred)','',
          'ACURASYS trial (2010, NEJM): Cisatracurium ×48h in early severe ARDS reduced',
          '90-day mortality and increased ventilator-free days vs. placebo',
          'Criteria: P/F <150 + PEEP ≥8 + FiO₂ ≥60% despite optimization','',
          'ROSE trial (2019, NEJM): Early NMBA did NOT improve outcomes vs. lighter sedation',
          'Current guidance: Consider NMBA for ≤48h in P/F <150 when P-SILI is a concern',
          'or when prone positioning requires it, NOT as routine ARDS management']],
        [['ICU PARALYSIS MONITORING BUNDLE (must do ALL while patient is paralyzed)','',
          'Sedation: Maintain deep sedation (RASS −4 to −5) — paralyzed patient CANNOT',
          'signal pain or distress; assess with physiological cues (HR, BP, diaphoresis)',
          'Analgesia: Ensure adequate IV opioid; paralysis masks pain expression',
          'TOF: Monitor every 4h; target 2/4 twitches; rotate electrode site daily',
          'Eye care: Lubricating drops q2h (blink reflex absent → corneal ulceration)',
          'Skin: Full body turn q2h (pressure injury from immobility; cannot self-reposition)',
          'Oral care: Q4h oral hygiene (VAP prevention; cough reflex absent)']],
        [['ICU-ACQUIRED WEAKNESS (ICUAW) — Major Complication of Prolonged NMBA','',
          'Definition: Profound muscle weakness developing during/after critical illness',
          'Risk factors: Prolonged NMB use (>48h), corticosteroids, aminoglycosides,',
          'hyperglycemia, immobility, sepsis, organ failure, female sex',
          'Presentation: Difficulty weaning from ventilator, flaccid weakness, ↓DTRs',
          '','Prevention: Limit NMB to ≤48h; early mobility when NMB stopped; glucose control',
          'Other complications: Aspiration (absent cough), corneal injury, venous thrombosis,',
          'anaphylaxis (1:10,000), malignant hyperthermia (aminosteroid NMBAs, sux)']]
    ];
    var col=sel<content.length?content[sel][0]:[];
    var ly=panelY+14;
    col.forEach(function(line){
        if(line===''){ly+=4;return;}
        var isSect=line.endsWith(')') && line.toUpperCase()===line.toUpperCase() && !line.startsWith(' ');
        var isHead=(line.indexOf('BUNDLE')>=0||line.indexOf('ARDS INDICATION')>=0||line.indexOf('ICU-ACQUIRED')>=0);
        ctx.fillStyle=isHead?_OR:'#bbb';
        ctx.font=isHead?'bold 9.5px sans-serif':'9.5px sans-serif';ctx.textAlign='left';
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
    # ═══ nmba_comparison ══════════════════════════════════════════════════════
    (
        "On the NMBA comparison chart, cisatracurium is the PREFERRED agent "
        "for prolonged ICU paralysis. Its unique clearance mechanism is _______, "
        "which makes it safe when both _______ and _______ are impaired.",

        "Hofmann elimination — spontaneous, non-enzymatic degradation at "
        "physiologic pH and temperature; does NOT require liver or kidneys\n"
        "| Safe when both hepatic AND renal function are impaired simultaneously\n"
        "| Other NMBAs: Rocuronium = hepatic (accumulates in liver failure); "
        "Vecuronium = hepatic (active metabolite accumulates); "
        "Pancuronium = renal (accumulates in AKI; also causes tachycardia)\n"
        "→ CCRN KEY: Cisatracurium dosing for ICU paralysis: 0.03–0.06 mg/kg/h "
        "infusion. Titrate to TOF 2/4 twitches. Hofmann degradation products "
        "(laudanosine) are pharmacologically inactive at clinical doses.\n"
        "→ MASTERY NOTE: Atracurium (cisatracurium's parent compound) produces "
        "higher laudanosine levels — can cause CNS excitation/seizures at "
        "high doses. Cisatracurium (the R/R isomer) produces 4× lower laudanosine "
        "and is preferred. Never confuse atracurium and cisatracurium.",

        'tier-review',
        _NM,
        DID['nmbas'],
        'nmba_comparison',
        '{"hi":3}',
        'chart-l1'
    ),
    (
        "The NMBA chart shows succinylcholine's unique mechanism: it is a "
        "_______ agent. Unlike non-depolarizing NMBAs, it causes _______ "
        "before producing paralysis, which can cause K⁺ to _______.",

        "Depolarizing NMBA — binds ACh receptors and causes sustained "
        "depolarization (Phase I block)\n"
        "| Causes fasciculations (brief uncoordinated muscle contractions) "
        "before flaccid paralysis — visible at onset\n"
        "| K⁺ increases by 0.5–1.0 mEq/L normally (safe in healthy patients)\n"
        "| In susceptible states (burns, crush, denervation): K⁺ can rise by "
        "5–10 mEq/L → fatal hyperkalemia and cardiac arrest\n"
        "→ CCRN KEY: Phase II block with succinylcholine occurs with prolonged "
        "or repeated doses (Phase I → Phase II transition) — block becomes "
        "non-depolarizing in character, prolonged, unpredictable. Avoid repeated "
        "dosing; use rocuronium infusion instead for sustained paralysis.\n"
        "→ MASTERY NOTE: Succinylcholine is the ONLY NMBA with dose = "
        "1.5 mg/kg (not 0.1–0.15 mg/kg like non-depolarizing NMBAs). "
        "The high dose saturates plasma cholinesterase rapidly for fast onset.",

        'tier-high',
        _NM,
        DID['nmbas'],
        'nmba_comparison',
        '{"hi":0}',
        'chart-l2'
    ),
    (
        "On the NMBA chart, pancuronium is listed as 'AVOID in ICU.' "
        "Two reasons are _______ and _______. "
        "The appropriate alternative for brief ICU procedures is _______.",

        "Reason 1: Prolonged duration (60–100 min) → unpredictable prolonged block, "
        "accumulates in renal failure (renally cleared)\n"
        "Reason 2: Tachycardia — blocks muscarinic (M2) receptors → ↑HR, ↑BP "
        "(can precipitate ischemia in cardiac patients)\n"
        "| Alternative for brief ICU procedures: Vecuronium 0.1 mg/kg IV "
        "(onset 3–5 min, duration 20–35 min, no cardiovascular effects)\n"
        "→ CCRN KEY: ICU NMBA selection rules: Cisatracurium = prolonged infusions "
        "(organ failure safe); Rocuronium = RSI alternative (sugammadex reversible); "
        "Vecuronium = short procedures (no hemodynamic effects); "
        "Succinylcholine = RSI when no contraindications; Pancuronium = avoid.\n"
        "→ MASTERY NOTE: Historical note: pancuronium was the original ICU NMBA "
        "and is still in use in some facilities due to low cost. ICU nurses must "
        "recognize prolonged or unexpected weakness after any NMBA as potential "
        "accumulation, pseudocholinesterase deficiency, or ICUAW.",

        'tier-critical',
        _NM,
        DID['nmbas'],
        'nmba_comparison',
        '{"hi":4}',
        'chart-l3'
    ),

    # ═══ train_of_four ════════════════════════════════════════════════════════
    (
        "On the TOF monitoring chart, the recommended ICU paralysis target "
        "during cisatracurium infusion is _______ twitches. "
        "TOF of 0/4 indicates _______ % blockade.",

        "Target: 2/4 twitches (TOF 2/4) — moderate neuromuscular block\n"
        "| TOF 0/4 indicates approximately 100% blockade (all 4 twitches absent)\n"
        "| 2/4 is preferred over 0/4: allows assessment of block adequacy, "
        "detects early recovery, reduces ICUAW risk from over-paralysis\n"
        "→ CCRN KEY: TOF monitoring site: ulnar nerve at wrist (stimulate) + "
        "observe adductor pollicis twitch (thumb adduction). Supramaximal stimulus "
        "(30–60 mA) required. Assess every 4h, rotate electrode site daily "
        "(skin burns from repeated stimulation at same site).\n"
        "→ MASTERY NOTE: TOF correlation: 0/4 ≈ 100% block; 1/4 ≈ 95%; "
        "2/4 ≈ 90%; 3/4 ≈ 75%; 4/4 ≈ 0% block. Higher TOF = less block. "
        "Always pair TOF with clinical assessment — TOF monitors block at "
        "peripheral muscle but does NOT assess diaphragm or central drive.",

        'tier-review',
        _NM,
        DID['nmbas'],
        'train_of_four',
        '{"tof":2}',
        'chart-l1'
    ),
    (
        "The TOF chart shows TOF 0/4 for a patient on cisatracurium infusion "
        "for ARDS at hour 52. Per ARDS paralysis guidelines, "
        "the appropriate action is _______.",

        "Reassess whether continued NMB is clinically necessary — if not, "
        "discontinue infusion and allow recovery (ARDS paralysis protocols "
        "limit duration to ≤48h per ACURASYS data)\n"
        "| If continued paralysis is indicated: target TOF 2/4, NOT 0/4 — "
        "reduce infusion rate until 2 twitches return\n"
        "| Ensure at hour 52: deep sedation maintained (RASS −4 to −5), "
        "adequate analgesia, eye care, pressure relief, oral care\n"
        "→ CCRN KEY: Sustained TOF 0/4 beyond 48h without clinical necessity "
        "significantly increases ICUAW risk. The ROSE trial (2019) showed "
        "early NMBA (≤48h cisatracurium) did not improve outcomes vs. "
        "lighter sedation — routine prolonged paralysis is not supported.\n"
        "→ MASTERY NOTE: After NMBA discontinuation, expect TOF to return "
        "progressively. Return of 2/4 twitches in 15–30 min confirms clearance. "
        "If no return after 60 min with known dose: suspect pseudocholinesterase "
        "deficiency (if sux was used) or accumulation (in organ failure).",

        'tier-high',
        _NM,
        DID['nmbas'],
        'train_of_four',
        '{"tof":0}',
        'chart-l2'
    ),
    (
        "On the TOF chart, a patient has completed ARDS paralysis. "
        "Before assessing for extubation readiness, "
        "TOF must show _______ twitches, and the additional test "
        "confirming adequate reversal is _______.",

        "TOF must show 4/4 twitches (full recovery of all 4 twitches)\n"
        "| Additional test: TOF ratio T4/T1 ≥0.9 (fade ratio) — "
        "4 twitches present but fade (T4 weaker than T1) indicates residual block; "
        "T4/T1 ≥0.9 confirms adequate neuromuscular recovery\n"
        "| If TOF 4/4 but T4/T1 ratio <0.9: give reversal agent before extubation "
        "(sugammadex 2 mg/kg if used rocuronium, neostigmine 0.05 mg/kg if others)\n"
        "→ CCRN KEY: Residual neuromuscular block at extubation is a "
        "patient safety risk — impaired pharyngeal muscle function → "
        "aspiration, impaired airway protective reflexes, apnea. "
        "TOF ratio <0.9 = unsafe for extubation regardless of clinical appearance.\n"
        "→ MASTERY NOTE: In ICU, quantitative TOF monitoring (acceleromyography) "
        "is more sensitive than qualitative (visual) assessment for detecting "
        "residual block. Qualitative assessment cannot detect T4/T1 fade ratios "
        "below 0.7 — significant residual block may be present without visible fade.",

        'tier-critical',
        _NM,
        DID['nmbas'],
        'train_of_four',
        '{"tof":4}',
        'chart-l3'
    ),

    # ═══ sux_rsi ══════════════════════════════════════════════════════════════
    (
        "On the RSI protocol chart, the two most common induction agents "
        "used before the paralytic are _______ and _______. "
        "Which is preferred in hemodynamically unstable ICU patients?",

        "Etomidate 0.3 mg/kg IV and Ketamine 1–2 mg/kg IV\n"
        "| Hemodynamically unstable: Ketamine preferred — sympathomimetic "
        "effect (↑HR, ↑BP via catecholamine release) provides cardiovascular "
        "support during intubation; safe in hypovolemia, septic shock, trauma\n"
        "| Etomidate: hemodynamically neutral (good for most ICU intubations) "
        "BUT inhibits adrenal 11β-hydroxylase → cortisol suppression × 24h "
        "(adrenal insufficiency risk in sepsis — controversial for repeat dosing)\n"
        "→ CCRN KEY: Propofol (1–2 mg/kg) is a third option for RSI induction "
        "but causes hypotension — AVOID in hemodynamically unstable patients. "
        "Midazolam (0.1 mg/kg) is slower onset, causes hypotension, NOT ideal for RSI.\n"
        "→ MASTERY NOTE: RSI preoxygenation: 3 minutes of 100% O₂ or 8 vital "
        "capacity breaths. Goal: maximize O₂ reservoir in FRC. "
        "High-flow nasal cannula during apnea (apneic oxygenation) extends "
        "safe apnea time by 5–10 min — used in difficult airway situations.",

        'tier-review',
        _NM,
        DID['nmbas'],
        'sux_rsi',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The RSI chart lists succinylcholine contraindications. "
        "A burn patient 72h after injury requires emergent intubation. "
        "Succinylcholine is contraindicated because burns >48h cause upregulation of "
        "_______ receptors → massive _______ efflux → cardiac arrest. "
        "The safe RSI alternative is _______ at dose _______.",

        "Contraindicated: Burns >48h post-injury cause upregulation of "
        "extrajunctional ACh receptors throughout the body — "
        "succinylcholine binds these extra receptors → massive K⁺ efflux → "
        "life-threatening hyperkalemia (K⁺ may rise 5–10 mEq/L) → cardiac arrest\n"
        "| Safe alternative: Rocuronium 1.2 mg/kg IV (RSI dose) → onset 60–90 sec, "
        "fully reversible with sugammadex 16 mg/kg if needed\n"
        "→ CCRN KEY: Hyperkalemia-risk succinylcholine contraindications: "
        "Burns (>24–48h), crush injury/rhabdomyolysis, prolonged immobility (>72h), "
        "denervation injuries, upper/lower motor neuron lesions, "
        "Guillain-Barré syndrome, muscular dystrophy. "
        "The K⁺ risk is ABSENT in the first 24h of injury (receptors not yet upregulated).\n"
        "→ MASTERY NOTE: The classic 'safe window' for succinylcholine in burns: "
        "first 24h = safe; after 24–48h = avoid indefinitely (risk persists years "
        "if denervation is permanent). Same principle applies to SCI patients: "
        "safe in acute phase of neurogenic shock, contraindicated after 3+ days.",

        'tier-high',
        _NM,
        DID['nmbas'],
        'sux_rsi',
        '{"sel":2}',
        'chart-l2'
    ),
    (
        "On the RSI chart, rocuronium at 1.2 mg/kg is used as succinylcholine "
        "alternative. Its key advantage is full reversal with _______ in the "
        "'can't intubate, can't oxygenate' (CICO) emergency at dose _______.",

        "Sugammadex — cyclodextrin chelating agent that encapsulates and "
        "inactivates rocuronium and vecuronium molecules\n"
        "| CICO rescue dose: 16 mg/kg IV (immediate reversal) — "
        "restores neuromuscular function within 1–3 minutes\n"
        "| Routine reversal (TOF 2/4): sugammadex 4 mg/kg IV (reversal in 3–5 min)\n"
        "→ CCRN KEY: Sugammadex indications: (1) Routine reversal of roc/vec "
        "at end of procedure; (2) Rescue reversal in CICO emergency; "
        "(3) Reversal after 1.2 mg/kg roc RSI if intubation fails. "
        "Cannot reverse succinylcholine (mechanism is chelation, not AChE inhibition).\n"
        "→ MASTERY NOTE: Before sugammadex, rocuronium RSI was 'one-way' — "
        "if intubation failed, deep block could not be rapidly reversed. "
        "Sugammadex changed RSI practice: rocuronium 1.2 mg/kg + sugammadex "
        "16 mg/kg available = 'safe RSI' (full reversal possible if needed). "
        "Cost remains a barrier; require pharmacy stocking for CICO rescue.",

        'tier-critical',
        _NM,
        DID['nmbas'],
        'sux_rsi',
        '{"sel":3}',
        'chart-l3'
    ),

    # ═══ nmba_reversal ════════════════════════════════════════════════════════
    (
        "On the NMBA reversal chart, neostigmine requires co-administration "
        "of _______ to prevent _______ side effects. "
        "Neostigmine is INEFFECTIVE when TOF is _______.",

        "Atropine 0.6–1.2 mg IV OR glycopyrrolate 0.2 mg IV — "
        "given before neostigmine\n"
        "| Prevents muscarinic side effects: bradycardia, bronchospasm, "
        "excessive secretions, abdominal cramping, urination (↑ACh at "
        "muscarinic receptors throughout body)\n"
        "| Neostigmine INEFFECTIVE: TOF 0/4 (deep block) — when >95% of "
        "receptors are occupied, additional ACh cannot overcome the block; "
        "must wait for spontaneous partial recovery (TOF ≥2/4) before neostigmine\n"
        "→ CCRN KEY: Neostigmine dose: 0.04–0.07 mg/kg IV (max 5 mg). "
        "Glycopyrrolate preferred over atropine: does NOT cross BBB "
        "(no CNS effects), provides longer antisecretory action. "
        "Neostigmine ceiling: cannot fully reverse deep block — risk of "
        "'recurarization' if used too early.\n"
        "→ MASTERY NOTE: Neostigmine mechanism: reversible acetylcholinesterase "
        "inhibition → ↑ACh at NMJ competes with NMBA for receptors. "
        "The maximum ACh increase is finite — cannot overcome full blockade. "
        "Timing: give at TOF ≥2/4 for reliable reversal.",

        'tier-review',
        _NM,
        DID['nmbas'],
        'nmba_reversal',
        '{"hi":0}',
        'chart-l1'
    ),
    (
        "The reversal chart shows sugammadex targets ONLY _______ and "
        "_______. A patient paralyzed with cisatracurium cannot be "
        "reversed with sugammadex because _______.",

        "Sugammadex targets ONLY rocuronium and vecuronium "
        "(aminosteroid NMBAs — sugammadex is specifically designed to "
        "encapsulate steroid-based NMBA molecules)\n"
        "| Cisatracurium CANNOT be reversed with sugammadex — it is a "
        "benzylisoquinolinium NMBA (different structural class, does not "
        "fit inside the sugammadex cyclodextrin cage)\n"
        "| Must use neostigmine (+ atropine) for cisatracurium reversal, "
        "OR wait for spontaneous Hofmann elimination\n"
        "→ CCRN KEY: Reversal decision chart: "
        "Rocuronium or vecuronium → sugammadex preferred (faster, cleaner); "
        "Cisatracurium, pancuronium, atracurium → neostigmine + anticholinergic; "
        "Succinylcholine → NO reversal agent (must wait for pseudocholinesterase degradation)\n"
        "→ MASTERY NOTE: Sugammadex in renal failure: the sugammadex-rocuronium "
        "complex is renally excreted. In severe renal failure (GFR <30), complex "
        "may recirculate → delayed 're-paralysis' is theoretically possible "
        "but clinically rare at standard doses. Use cautiously; have monitoring in place.",

        'tier-high',
        _NM,
        DID['nmbas'],
        'nmba_reversal',
        '{"hi":1}',
        'chart-l2'
    ),
    (
        "On the reversal chart, a patient has TOF 0/4 after rocuronium "
        "infusion ×6h. The anesthesiologist orders sugammadex 4 mg/kg. "
        "This dose is _______ for TOF 0/4. The correct dose is _______.",

        "INCORRECT — sugammadex 4 mg/kg is for TOF 1–2/4 (routine reversal)\n"
        "| Correct dose for TOF 0/4 (deep/immediate reversal): 16 mg/kg IV\n"
        "| Dose summary: TOF 1–2/4 = 4 mg/kg; TOF 0/4 or rescue = 16 mg/kg\n"
        "| Onset: 4 mg/kg → reversal in 3–5 min; 16 mg/kg → reversal in 1–3 min\n"
        "→ CCRN KEY: The 16 mg/kg rescue dose is used in two scenarios: "
        "(1) Deep block after RSI rocuronium when intubation fails (CICO); "
        "(2) Deep block requiring immediate reversal (e.g., anaphylaxis to NMBA, "
        "clinical deterioration requiring reversal). This is a weight-based dose — "
        "must know the patient's weight accurately.\n"
        "→ MASTERY NOTE: After 16 mg/kg sugammadex, if re-paralysis is needed "
        "(e.g., intubation still needed), wait ≥24h before using rocuronium again "
        "(all sugammadex binding sites occupied). Use succinylcholine or "
        "cisatracurium as alternative during this window.",

        'tier-critical',
        _NM,
        DID['nmbas'],
        'nmba_reversal',
        '{"hi":2}',
        'chart-l3'
    ),

    # ═══ icu_paralysis ════════════════════════════════════════════════════════
    (
        "On the ICU paralysis chart, the ACURASYS trial showed cisatracurium "
        "for _______ hours in early severe ARDS (P/F < _______) reduced "
        "90-day mortality. What did the subsequent ROSE trial show?",

        "ACURASYS (2010, NEJM): 48 hours, P/F <150 + PEEP ≥8 + FiO₂ ≥60%\n"
        "| ACURASYS: Cisatracurium ×48h reduced 90-day mortality (hazard ratio 0.68) "
        "and increased ventilator-free days vs. placebo\n"
        "| ROSE trial (2019, NEJM): Did NOT replicate ACURASYS benefit — "
        "early NMBA (≤48h) vs. lighter sedation showed NO difference in 90-day "
        "mortality; ROSE used lighter sedation (RASS −2 to −3) in control arm\n"
        "→ CCRN KEY: Current SCCM/PADIS guidance: NMBAs may be considered "
        "for ≤48h in P/F <150 when P-SILI (patient self-inflicted lung injury) "
        "is a concern OR when prone positioning is required. NOT routine. "
        "Lighter sedation (as in ROSE control arm) may achieve similar outcomes.\n"
        "→ MASTERY NOTE: ROSE vs. ACURASYS discrepancy: control arm sedation "
        "differs. ACURASYS control = deep sedation; ROSE control = lighter "
        "sedation. The benefit seen in ACURASYS may reflect harms of deep "
        "sedation in the control arm, not benefits of paralysis per se.",

        'tier-review',
        _NM,
        DID['nmbas'],
        'icu_paralysis',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The ICU paralysis monitoring chart shows eye care is required every "
        "_______ hours during NMBA infusion. Explain why and what happens if omitted.",

        "Lubricating eye drops every 2 hours (artificial tears or ointment)\n"
        "| Why: Blink reflex is abolished under NMBA — orbicularis oculi is "
        "paralyzed → eyes may remain open continuously → tear film evaporation → "
        "corneal desiccation, ulceration, and potentially permanent vision loss\n"
        "| If omitted: corneal ulceration → corneal scarring → vision impairment\n"
        "→ CCRN KEY: Full ICU paralysis monitoring bundle: "
        "(1) Deep sedation + analgesia (cannot signal pain or distress); "
        "(2) TOF q4h (target 2/4 twitches); "
        "(3) Eye lubrication q2h (corneal protection); "
        "(4) Full body turn q2h (pressure injury prevention — cannot self-reposition); "
        "(5) Oral hygiene q4h (VAP prevention — cough reflex absent).\n"
        "→ MASTERY NOTE: Pressure injury risk during NMBA: the patient has "
        "absolutely zero ability to shift weight or respond to discomfort. "
        "Schedule turns and use pressure-redistribution surfaces. "
        "All 5 bundle components must be executed for every paralyzed patient — "
        "omitting any one creates patient harm.",

        'tier-high',
        _NM,
        DID['nmbas'],
        'icu_paralysis',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "On the ICU paralysis chart, ICU-Acquired Weakness (ICUAW) is defined "
        "as profound weakness developing during critical illness. "
        "Three modifiable risk factors shown are _______, _______, and _______.",

        "Modifiable risk factors for ICUAW:\n"
        "1. Prolonged NMBA use (>48h) — directly causes neuromuscular dysfunction\n"
        "2. Corticosteroids (especially high-dose; mechanism: muscle protein catabolism)\n"
        "3. Hyperglycemia (impairs mitochondrial function in muscle)\n"
        "4. Immobility/bed rest — loss of muscle mass at 1–2% per day\n"
        "5. Aminoglycoside antibiotics (neuromuscular junction blockade potentiation)\n"
        "→ CCRN KEY: ICUAW prevention: limit NMBAs to ≤48h; glycemic control "
        "(target 140–180 mg/dL); minimize corticosteroids; EARLY MOBILIZATION "
        "— PT/OT even during MV when NMBAs discontinued. "
        "Presentation: failure to wean from ventilator, symmetric flaccid weakness, "
        "decreased or absent deep tendon reflexes.\n"
        "→ MASTERY NOTE: ICUAW affects 25–50% of ICU patients and is a major "
        "driver of long-term disability and PTSD after critical illness. "
        "Three subtypes: (1) Critical illness myopathy (CIM) — most common; "
        "(2) Critical illness polyneuropathy (CIP) — axonal neuropathy; "
        "(3) Mixed CIM+CIP. Electromyography (EMG) distinguishes subtypes. "
        "Recovery takes months to years; some patients never fully recover.",

        'tier-critical',
        _NM,
        DID['nmbas'],
        'icu_paralysis',
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
