#!/usr/bin/env python3
"""chunk39_charts.py — Ph6 Professional Practice & Ethics (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_38.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_39.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c39')
CHUNK_NUM   = 39
MID_BASE    = 1_800_005_040
CHART_ORDER = ['synergy_model', 'ethics_principles', 'palliative_comfort',
               'qi_safety', 'communication_sbar']

_PP = 'Ph6 · \U0001f7e1 T3 · Professional Practice & Ethics'

RF = {}

# ── Chart 1: AACN Synergy Model ───────────────────────────────────────────────
RF['synergy_model'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var rows=[
        ['Resiliency',    'Capacity to return to restorative function',  'Clinical Judgment'],
        ['Vulnerability', 'Susceptibility to adverse stressors',         'Advocacy & Moral Agency'],
        ['Stability',     'Maintain steady-state equilibrium',           'Clinical Judgment'],
        ['Complexity',    'Intricate entanglement of systems/therapies', 'Systems Thinking'],
        ['Rsrc Avail.',   'Extent of personal/social/financial support', 'Facilitating Learning'],
        ['Participation', 'Engagement in care activities',               'Caring Practices'],
        ['Decision-Mkng','Ability to make decisions about care',         'Advocacy & Moral Agency'],
        ['Predictability','Expected trajectory of condition',            'Response to Diversity'],
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var mx=10,tw=W-mx*2,w1=tw*0.24,w2=tw*0.46,w3=tw*0.30;
    ctx.fillStyle='#111';ctx.fillRect(mx,4,tw,16);
    ctx.fillStyle=_TE;ctx.font='bold 9px sans-serif';ctx.textAlign='left';
    ctx.fillText('AACN SYNERGY MODEL  —  Patient Characteristics → Primary Nurse Competency',mx+5,15);
    ctx.fillStyle='#181818';ctx.fillRect(mx,23,tw,15);
    ctx.fillStyle='#444';ctx.font='bold 8px sans-serif';ctx.textAlign='center';
    ctx.fillText('CHARACTERISTIC',mx+w1/2,34);
    ctx.fillText('DEFINITION',mx+w1+w2/2,34);
    ctx.fillStyle=_AM;ctx.fillText('PRIMARY COMPETENCY',mx+w1+w2+w3/2,34);
    var my=41,rh=26;
    rows.forEach(function(r,i){
        var ry=my+i*(rh+2),isHi=(hi===i);
        ctx.fillStyle=isHi?'#061422':(i%2===0?'#0c0c0c':'#111');
        ctx.fillRect(mx,ry,tw,rh);
        if(isHi){ctx.strokeStyle=_TE;ctx.lineWidth=1.5;ctx.strokeRect(mx,ry,tw,rh);}
        ctx.strokeStyle='#1e1e1e';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(mx+w1,ry);ctx.lineTo(mx+w1,ry+rh);ctx.stroke();
        ctx.beginPath();ctx.moveTo(mx+w1+w2,ry);ctx.lineTo(mx+w1+w2,ry+rh);ctx.stroke();
        ctx.fillStyle=isHi?_TE:'#ccc';ctx.font=(isHi?'bold ':'')+'10px sans-serif';ctx.textAlign='left';
        ctx.fillText(r[0],mx+4,ry+rh/2+4);
        ctx.fillStyle=isHi?'#aaa':'#555';ctx.font='8.5px sans-serif';
        ctx.fillText(r[1],mx+w1+4,ry+rh/2+4);
        ctx.fillStyle=isHi?_AM:'#888';ctx.font=(isHi?'bold ':'')+'10px sans-serif';
        ctx.fillText(r[2],mx+w1+w2+4,ry+rh/2+4);
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        var lbl=document.createElement('span');
        lbl.style.cssText='font-size:9px;color:#444;font-weight:800;align-self:center;';
        lbl.textContent='FOCUS:';row.appendChild(lbl);
        var lbs=['Resil.','Vulnr.','Stbl.','Cmplx.','Rsrc.','Partic.','Dcsn.','Pred.'];
        lbs.forEach(function(lb,i){
            (function(idx){
                var b=_mkB(lb,_TE,hi===idx,function(on){
                    var p2={hi:on?idx:-1};
                    cv.setAttribute('data-params',JSON.stringify(p2));
                    _render(cv,ctrl,p2);
                });row.appendChild(b);
            })(i);
        });
        var rst=_mkB('all',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: Bioethics Principles ─────────────────────────────────────────────
RF['ethics_principles'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sc=(P.sc!==undefined)?P.sc:0;
    var pr=[
        {name:'AUTONOMY',        col:_TE, def:"Patient's right to self-determination",  key:'Respect informed consent & refusal'},
        {name:'BENEFICENCE',     col:_GN, def:'Duty to act in patient\'s best interest', key:'Promote good; prevent harm'},
        {name:'NON-MALEFICENCE', col:_OR, def:'Duty to do no harm',                      key:'Avoid futile or harmful interventions'},
        {name:'JUSTICE',         col:_PU, def:'Fair, equitable allocation of resources', key:'Equitable treatment of all patients'},
    ];
    var scens=[
        {title:'',conflict:[],note:''},
        {title:'JW patient refuses life-saving transfusion — competent adult',
         conflict:[0,1],note:'Autonomy (right to refuse) prevails over Beneficence when patient has decision-making capacity'},
        {title:'Aggressive treatment continued despite documented DNR',
         conflict:[2,1],note:'Non-Maleficence violated when futile CPR overrides documented advance directive'},
        {title:'One ICU bed, two critically ill patients of equal acuity',
         conflict:[3,1],note:'Justice (equitable allocation by clinical criteria) guides, not social worth or identity'},
        {title:'Family demands full care for brain-dead patient',
         conflict:[1,2],note:'Beneficence is impossible (no patient); continuing treatment violates Non-Maleficence'},
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    ctx.fillStyle='#ccc';ctx.font='bold 10px sans-serif';ctx.textAlign='center';
    ctx.fillText('BIOETHICS PRINCIPLES',W/2,14);
    var bx=10,by=22,bw=(W-28)/2,bh=92,gap=8;
    var layout=[[0,0],[1,0],[0,1],[1,1]];
    var conf=scens[sc].conflict;
    layout.forEach(function(pos,i){
        var px=bx+pos[0]*(bw+gap),py=by+pos[1]*(bh+gap);
        var p=pr[i],isC=conf.indexOf(i)!==-1;
        ctx.fillStyle=isC?p.col+'33':'#0d0d0d';
        ctx.fillRect(px,py,bw,bh);
        ctx.strokeStyle=isC?p.col:'#2a2a2a';ctx.lineWidth=isC?2:1;
        ctx.strokeRect(px,py,bw,bh);
        ctx.fillStyle=p.col;ctx.font='bold 11px sans-serif';ctx.textAlign='center';
        ctx.fillText(p.name,px+bw/2,py+18);
        ctx.fillStyle='#999';ctx.font='9px sans-serif';
        var dw=bw-12,words=p.def.split(' '),line='',ly=py+34;
        words.forEach(function(w){
            var t=line?line+' '+w:w;
            if(ctx.measureText(t).width>dw){ctx.fillText(line,px+bw/2,ly);line=w;ly+=12;}
            else line=t;
        });
        if(line)ctx.fillText(line,px+bw/2,ly);ly+=14;
        ctx.fillStyle=isC?p.col:'#555';ctx.font=(isC?'bold ':'')+'8.5px sans-serif';
        ctx.fillText(p.key,px+bw/2,ly);
    });
    if(sc>0){
        var sy=by+2*(bh+gap)+2;
        ctx.fillStyle='#111';ctx.fillRect(10,sy,W-20,38);
        ctx.fillStyle=_AM;ctx.font='bold 9px sans-serif';ctx.textAlign='left';
        ctx.fillText(scens[sc].title,14,sy+12);
        ctx.fillStyle='#777';ctx.font='8.5px sans-serif';
        var nt=scens[sc].note,nw=W-28,nl='',nly=sy+24;
        nt.split(' ').forEach(function(w){
            var t=nl?nl+' '+w:w;
            if(ctx.measureText(t).width>nw){ctx.fillText(nl,14,nly);nl=w;nly+=11;}
            else nl=t;
        });
        if(nl)ctx.fillText(nl,14,nly);
    }
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;';
        var sls=['Overview','JW Refusal','DNR Ignored','ICU Triage','Brain Death'];
        sls.forEach(function(lb,i){
            (function(idx){
                var b=_mkB(lb,idx===0?_AX:_AM,sc===idx,function(){
                    cv.setAttribute('data-params',JSON.stringify({sc:idx}));
                    _render(cv,ctrl,{sc:idx});
                });row.appendChild(b);
            })(i);
        });
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 3: WHO Pain Ladder / Palliative Comfort ─────────────────────────────
RF['palliative_comfort'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var pain=(P.pain!==undefined)?P.pain:5;
    var step=pain<=3?0:pain<=6?1:2;
    var steps=[
        {label:'STEP 1',range:'Mild  1–3',col:_GN,
         drugs:['Acetaminophen 650–975 mg q6h','NSAIDs (ibuprofen, ketorolac)','Aspirin (non-malignant pain)'],
         goal:'Non-opioid monotherapy; titrate before escalating'},
        {label:'STEP 2',range:'Moderate  4–6',col:_AM,
         drugs:['Tramadol 50–100 mg q4–6h','Low-dose oxycodone 5–10 mg','Codeine 30–60 mg q4h'],
         goal:'Weak opioid + continue non-opioid base'},
        {label:'STEP 3',range:'Severe  7–10',col:_RE,
         drugs:['Morphine 2–4 mg IV q4h','Hydromorphone 0.2–0.4 mg IV','Fentanyl gtt: titrate to comfort'],
         goal:'Strong opioid + non-opioid + adjuvants'},
    ];
    var adj=['Adjuvants at ALL steps:','Gabapentin/Pregabalin — neuropathic pain',
             'Corticosteroids — bone/tumor inflammation','TCAs (amitriptyline) — neuropathic',
             'Bisphosphonates — bone metastases'];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    ctx.fillStyle='#ccc';ctx.font='bold 10px sans-serif';ctx.textAlign='center';
    ctx.fillText('WHO ANALGESIC LADDER',W/2,13);
    var bw=192,gap=10,by=22,bh=190,mx=12;
    steps.forEach(function(s,i){
        var bx=mx+i*(bw+gap);
        var isA=(step===i);
        ctx.fillStyle=isA?s.col+'22':'#0c0c0c';
        ctx.fillRect(bx,by,bw,bh);
        ctx.strokeStyle=isA?s.col:'#2a2a2a';ctx.lineWidth=isA?2:1;
        ctx.strokeRect(bx,by,bw,bh);
        ctx.fillStyle=s.col;ctx.font='bold 12px sans-serif';ctx.textAlign='center';
        ctx.fillText(s.label,bx+bw/2,by+18);
        ctx.fillStyle='#888';ctx.font='9px sans-serif';
        ctx.fillText(s.range,bx+bw/2,by+32);
        ctx.fillStyle=isA?'#ddd':'#666';ctx.font=(isA?'bold ':'')+'9px sans-serif';ctx.textAlign='left';
        s.drugs.forEach(function(d,j){ctx.fillText('• '+d,bx+6,by+52+j*18);});
        ctx.fillStyle=isA?s.col:'#444';ctx.font='8px sans-serif';ctx.textAlign='center';
        var gw=bw-12,words=s.goal.split(' '),gl='',gly=by+120;
        words.forEach(function(w){
            var t=gl?gl+' '+w:w;
            if(ctx.measureText(t).width>gw){ctx.fillText(gl,bx+bw/2,gly);gl=w;gly+=11;}
            else gl=t;
        });
        if(gl)ctx.fillText(gl,bx+bw/2,gly);
        if(isA){
            ctx.fillStyle=s.col;ctx.font='bold 28px sans-serif';ctx.textAlign='center';
            ctx.fillText(pain+'/10',bx+bw/2,by+162);
        }
    });
    var ay=by+bh+10;
    ctx.fillStyle='#1a1a1a';ctx.fillRect(mx,ay,W-mx*2,52);
    ctx.fillStyle=_TE;ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
    ctx.fillText(adj[0],mx+5,ay+11);
    ctx.fillStyle='#666';ctx.font='8px sans-serif';
    adj.slice(1).forEach(function(a,i){ctx.fillText(a,mx+5,ay+23+i*10);});
    if(ctrl){
        ctrl.innerHTML='';
        var sl=_mkS('Pain',1,10,1,pain,function(v){return Math.round(v)+'/10';},function(v){
            cv.setAttribute('data-params',JSON.stringify({pain:Math.round(v)}));
            _render(cv,ctrl,{pain:Math.round(v)});
        });
        ctrl.appendChild(sl);
    }
}
"""

# ── Chart 4: ABCDEF Bundle ────────────────────────────────────────────────────
RF['qi_safety'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:-1;
    var bundle=[
        {lt:'A',name:'Assess & Manage Pain',col:_TE,
         detail:'CPOT q4h (non-verbal) or NRS (verbal). Analgesia-first: treat pain before adding sedation. Target CPOT <3, NRS <4.'},
        {lt:'B',name:'Spontaneous Breathing Trial',col:_GN,
         detail:'Daily SBT after SAT. Screen: FiO₂≤60%, PEEP≤8, RASS≥-1, no new agitation. PS trial 30 min; extubate if passes.'},
        {lt:'C',name:'Choice of Sedation (analgesia-first)',col:_AM,
         detail:'Target RASS -1 to 0. Propofol or dexmedetomidine preferred. AVOID benzodiazepines (increase delirium risk, MENDS/SLEAP trials).'},
        {lt:'D',name:'Delirium Monitoring',col:_OR,
         detail:'CAM-ICU every shift. Treat: reorient, mobilize, sleep hygiene, correct metabolic causes. Haloperidol for agitated delirium only.'},
        {lt:'E',name:'Early Mobility & Exercise',col:_PU,
         detail:'Begin when RASS ≥-2. Passive ROM → active-assisted → sitting → standing → ambulation. PT/OT consult within 24–48h.'},
        {lt:'F',name:'Family Engagement',col:_PI,
         detail:'Family presence 24/7 (open visitation). Family as partners in reorientation, goal-of-care discussions, and care planning. Reduces ICU delirium duration.'},
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    ctx.fillStyle='#ccc';ctx.font='bold 10px sans-serif';ctx.textAlign='center';
    ctx.fillText('ABCDEF BUNDLE  —  ICU Liberation',W/2,13);
    var bw=192,bh=72,gap=10,by=22,mx=12;
    bundle.forEach(function(b,i){
        var col=Math.floor(i/2),row=i%2;
        var bx=mx+col*(bw+gap),ry=by+row*(bh+gap);
        var isS=(sel===i);
        ctx.fillStyle=isS?b.col+'33':'#0d0d0d';
        ctx.fillRect(bx,ry,bw,bh);
        ctx.strokeStyle=isS?b.col:'#2a2a2a';ctx.lineWidth=isS?2:1;
        ctx.strokeRect(bx,ry,bw,bh);
        ctx.fillStyle=b.col;ctx.font='bold 18px sans-serif';ctx.textAlign='left';
        ctx.fillText(b.lt,bx+8,ry+26);
        ctx.fillStyle=isS?'#ddd':'#888';ctx.font=(isS?'bold ':'')+'9px sans-serif';
        var tw=bw-36,words=b.name.split(' '),line='',ly=ry+16;
        words.forEach(function(w){
            var t=line?line+' '+w:w;
            if(ctx.measureText(t).width>tw){ctx.fillText(line,bx+30,ly);line=w;ly+=12;}
            else line=t;
        });
        if(line)ctx.fillText(line,bx+30,ly);
    });
    var dy=by+2*(bh+gap)+4;
    if(sel>=0){
        ctx.fillStyle='#111';ctx.fillRect(mx,dy,W-mx*2,52);
        ctx.strokeStyle=bundle[sel].col;ctx.lineWidth=1;ctx.strokeRect(mx,dy,W-mx*2,52);
        ctx.fillStyle=bundle[sel].col;ctx.font='bold 9px sans-serif';ctx.textAlign='left';
        ctx.fillText(bundle[sel].lt+' — '+bundle[sel].name,mx+6,dy+13);
        ctx.fillStyle='#888';ctx.font='8.5px sans-serif';
        var dw=W-mx*2-12,dtxt=bundle[sel].detail,dl='',dly=dy+26;
        dtxt.split(' ').forEach(function(w){
            var t=dl?dl+' '+w:w;
            if(ctx.measureText(t).width>dw){ctx.fillText(dl,mx+6,dly);dl=w;dly+=11;}
            else dl=t;
        });
        if(dl)ctx.fillText(dl,mx+6,dly);
    } else {
        ctx.fillStyle='#1a1a1a';ctx.fillRect(mx,dy,W-mx*2,52);
        ctx.fillStyle='#555';ctx.font='9px sans-serif';ctx.textAlign='center';
        ctx.fillText('Click a bundle element to see intervention details',W/2,dy+28);
    }
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;';
        bundle.forEach(function(b,i){
            (function(idx){
                var btn=_mkB(b.lt,b.col,sel===idx,function(on){
                    var p2={sel:on?idx:-1};
                    cv.setAttribute('data-params',JSON.stringify(p2));
                    _render(cv,ctrl,p2);
                });row.appendChild(btn);
            })(i);
        });
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 5: SBAR Communication Framework ────────────────────────────────────
RF['communication_sbar'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sc=(P.sc!==undefined)?P.sc:0;
    var rows=[
        {lt:'S',label:'SITUATION',col:_TE},
        {lt:'B',label:'BACKGROUND',col:_GN},
        {lt:'A',label:'ASSESSMENT',col:_AM},
        {lt:'R',label:'RECOMMENDATION',col:_OR},
    ];
    var scens=[
        ['State the problem: who, what is changing, how urgently',
         'Why here, relevant history, current orders, latest vitals trend',
         'Your clinical interpretation — what you THINK is happening',
         'Specific request: come now / order X / change Y'],
        ['Mr. Jones Rm 4 — SpO₂ 83%, RR 30, tripod positioning, onset 20 min',
         'COPD exacerbation day 2, on 40% Venturi, last ABG: PO₂ 68, pH 7.32',
         'I believe acute respiratory failure — new wheeze, decreased air entry base-L, PEFR dropped 40%',
         'Need you here NOW; anticipate NIV setup and ABG order'],
        ['Ms. Park Rm 9 — MAP 52, HR 122, BP falling 114/70→78/40 over 2 h',
         'Post-CABG day 1, was stable AM; K⁺ 3.2, on amiodarone; no vasopressors',
         'Concerned for distributive vs cardiogenic shock — cool/clammy, new ST depression V4–V6',
         'Need 500 mL LR bolus + vasopressor protocol activation; please come assess now'],
        ['Mr. Davis Rm 6 — acute confusion, right arm drift, slurred speech —15 min ago',
         'HTN, no anticoagulation; last NIHSS was 0; onset during ambulation',
         'I believe acute ischemic stroke — symptom onset 15 min ago, NIHSS now 8',
         'Stat code stroke, CT head now; starting serial NIHSS; neurology needed at bedside'],
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    ctx.fillStyle='#ccc';ctx.font='bold 10px sans-serif';ctx.textAlign='center';
    ctx.fillText('SBAR COMMUNICATION FRAMEWORK',W/2,12);
    var lw=52,rh=60,by=18,mx=10,cw=W-mx*2;
    rows.forEach(function(r,i){
        var ry=by+i*(rh+4);
        ctx.fillStyle='#0d0d0d';ctx.fillRect(mx,ry,cw,rh);
        ctx.strokeStyle=r.col;ctx.lineWidth=1;ctx.strokeRect(mx,ry,cw,rh);
        ctx.fillStyle=r.col+'44';ctx.fillRect(mx,ry,lw,rh);
        ctx.fillStyle=r.col;ctx.font='bold 14px sans-serif';ctx.textAlign='center';
        ctx.fillText(r.lt,mx+lw/2,ry+22);
        ctx.fillStyle=r.col+'cc';ctx.font='7px sans-serif';
        ctx.fillText(r.label,mx+lw/2,ry+35);
        var txt=scens[sc][i],tw=cw-lw-12,words=txt.split(' '),line='',ly=ry+14;
        ctx.fillStyle='#bbb';ctx.font='9px sans-serif';ctx.textAlign='left';
        words.forEach(function(w){
            var t=line?line+' '+w:w;
            if(ctx.measureText(t).width>tw){ctx.fillText(line,mx+lw+8,ly);line=w;ly+=12;}
            else line=t;
        });
        if(line)ctx.fillText(line,mx+lw+8,ly);
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;';
        var sls=['Template','Respiratory','Hemodynamic','Neurological'];
        sls.forEach(function(lb,i){
            (function(idx){
                var b=_mkB(lb,idx===0?_AX:_TE,sc===idx,function(){
                    cv.setAttribute('data-params',JSON.stringify({sc:idx}));
                    _render(cv,ctrl,{sc:idx});
                });row.appendChild(b);
            })(i);
        });
        ctrl.appendChild(row);
    }
}
"""

# ── Cards ─────────────────────────────────────────────────────────────────────
# (front, back, tier, badge, did, ctype, params_json, ltag)
CARDS = [

    # ═══ synergy_model ════════════════════════════════════════════════════════
    (
        "On the Synergy Model table, a patient with high Vulnerability "
        "maps primarily to the nurse competency of _______, "
        "which at its highest level means _______.",

        "Advocacy & Moral Agency — protecting the patient's interests, values, "
        "and rights when they cannot do so themselves, including moral courage "
        "to challenge physicians, policies, or systems that cause harm\n"
        "| Vulnerability = susceptibility to adverse stressors (frail elderly, "
        "unconscious, non-English speaking, mentally ill)\n"
        "→ CCRN KEY: Synergy Model competencies scale 1–5. When patient needs "
        "EXCEED nurse competency level, unsafe care results. Charge nurses must "
        "match patient acuity to nurse competency level during assignments.\n"
        "→ MASTERY NOTE: Advocacy at competency level 5 = systems-level change: "
        "nurse identifies and corrects unit policies that harm vulnerable patients, "
        "not merely protecting one patient at bedside.",

        'tier-review',
        _PP,
        DID['professional'],
        'synergy_model',
        '{"hi":1}',
        'chart-l1'
    ),
    (
        "A post-op CABG patient has Synergy Model scores: Stability 2 "
        "(unstable hemodynamics), Complexity 4 (multi-organ involvement), "
        "Predictability 2 (unexpected deterioration). "
        "The nurse competency constellation most critical is _______ and _______ "
        "because _______.",

        "Clinical Judgment (Stability 2 = complex real-time hemodynamic decisions) "
        "and Systems Thinking (Complexity 4 = coordinating cardiology, pharmacy, "
        "respiratory, CT surgery)\n"
        "| Predictability 2 = unexpected trajectory demands anticipatory thinking "
        "— the nurse must forecast deterioration, not just react to it\n"
        "→ CCRN KEY: Clinical Judgment in the Synergy Model = pattern recognition, "
        "inference, and navigation of uncertainty — not just following protocols. "
        "A nurse at CJ level 3 caring for a level 5 patient = safety risk.\n"
        "→ MASTERY NOTE: Systems Thinking = seeing the patient within the hospital "
        "ecosystem: care transitions, discharge barriers, interdisciplinary "
        "coordination. High-complexity patients require advocacy across every "
        "care interface.",

        'tier-high',
        _PP,
        DID['professional'],
        'synergy_model',
        '{"hi":3}',
        'chart-l2'
    ),
    (
        "A Synergy Model assessment shows Participation in Decision-Making = 1 "
        "(no capacity, no surrogate identified). The nurse is asked to obtain "
        "consent for a high-risk procedure. Per the Synergy Model, "
        "the nurse's role is _______, not _______, because _______.",

        "Role: Advocacy & Moral Agency — escalate to ethics committee; identify "
        "legal decision-maker; document incapacity; delay non-emergent procedure "
        "until proxy is appointed\n"
        "| Not: signing consent as patient representative (nurses cannot serve as "
        "legal surrogate except in specific state statutes)\n"
        "| Because: Advocacy requires protecting the legally incapacitated patient "
        "from procedures they cannot authorize — nurses must not substitute personal "
        "judgment for the patient's legal rights\n"
        "→ CCRN KEY: Capacity (clinical) vs Competency (legal): capacity = "
        "can patient understand, appreciate, reason, communicate a choice? "
        "Competency = court determination. ICU nurses assess capacity; legal "
        "competency requires adjudication.\n"
        "→ MASTERY NOTE: Surrogate hierarchy: 1) patient (if capable), "
        "2) healthcare proxy/POA-HC, 3) next-of-kin by state statute, "
        "4) ethics committee. Never proceed to invasive procedures without "
        "documented incapacity and surrogate identification except in true emergencies.",

        'tier-critical',
        _PP,
        DID['professional'],
        'synergy_model',
        '{"hi":6}',
        'chart-l3'
    ),

    # ═══ ethics_principles ════════════════════════════════════════════════════
    (
        "On the bioethics framework chart, when a competent adult "
        "Jehovah's Witness refuses a life-saving blood transfusion, "
        "the PRIMARY applicable principle is _______, which overrides "
        "_______ because _______.",

        "Autonomy (competent patient's right to refuse any intervention) "
        "overrides Beneficence (clinician's duty to save life)\n"
        "| Document refusal; ensure refusal is informed (patient understands "
        "consequences); notify physician; ethics consult if competency uncertain\n"
        "→ CCRN KEY: Competent adult refusal is binding regardless of prognosis. "
        "Competency assessment: does patient UNDERSTAND information? APPRECIATE "
        "consequences? REASON about the choice? COMMUNICATE a decision? If yes × 4 "
        "→ honor refusal, even life-ending.\n"
        "→ MASTERY NOTE: Unconscious JW patients: valid advance directive or "
        "healthcare proxy expressing refusal must be honored. Without "
        "documentation and in emergency = treat as emergency to preserve life. "
        "'No blood' bracelet alone is insufficient legal protection.",

        'tier-review',
        _PP,
        DID['professional'],
        'ethics_principles',
        '{"sc":1}',
        'chart-l1'
    ),
    (
        "The ethics chart shows Non-Maleficence vs Beneficence conflict "
        "in the Brain Death scenario. Continuing full resuscitative care "
        "on a brain-dead patient at family request is ethically problematic "
        "because _______ and _______.",

        "1. Beneficence is impossible — there is no patient to benefit "
        "(brain death = legal death; no integrative brain function)\n"
        "2. Non-Maleficence is violated — futile procedures cause harm: "
        "false hope for family, prolonged grief, wasted shared resources\n"
        "| Brain death ≠ vegetative state or minimally conscious state "
        "— these have fundamentally different prognoses and ethical frameworks\n"
        "→ CCRN KEY: Brain death criteria (UDDA): irreversible cessation of all "
        "brain function including brainstem. Pre-requisites: known cause, "
        "normothermia, no confounders. Tests: absent brainstem reflexes + "
        "apnea test (PCO₂ rise ≥20 mmHg with no respiratory effort).\n"
        "→ MASTERY NOTE: Nurses must not use 'brain dead' loosely to describe "
        "vegetative state. The legal weight is profound: brain death = "
        "certificate of death; vegetative state = living. Confusing families "
        "about this distinction causes serious harm.",

        'tier-high',
        _PP,
        DID['professional'],
        'ethics_principles',
        '{"sc":4}',
        'chart-l2'
    ),
    (
        "During a mass casualty event, 6 ventilators are available for "
        "8 patients in respiratory failure. The ethics principle guiding "
        "allocation is _______, and decisions must use _______ criteria, "
        "not _______, because _______.",

        "Justice (equitable, fair distribution of scarce resources); "
        "use clinical utility criteria (SOFA score, likelihood of survival "
        "to discharge, reversibility of illness)\n"
        "| Not social worth criteria (age, occupation, 'who is more valuable') "
        "— ethically impermissible and legally prohibited\n"
        "| Because: Justice requires fair access by medical need, not social value; "
        "utilitarian goal = maximize lives saved, not lives deemed worthy\n"
        "→ CCRN KEY: Crisis Standards of Care (CSC): activated during declared "
        "disasters. SOFA-based triage shifts from individual Beneficence to "
        "population-level Justice. Re-assess q24–48h for reallocation if status changes.\n"
        "→ MASTERY NOTE: Nurses working under activated CSC protocols have legal "
        "and ethical protection. Document all triage decisions. Patients who do "
        "not receive scarce resources MUST receive palliative/comfort care — "
        "withdrawal is not abandonment.",

        'tier-critical',
        _PP,
        DID['professional'],
        'ethics_principles',
        '{"sc":3}',
        'chart-l3'
    ),

    # ═══ palliative_comfort ═══════════════════════════════════════════════════
    (
        "On the WHO pain ladder, a patient with 6/10 cancer pain "
        "inadequately controlled on NSAIDs alone is at Step _______, "
        "requiring addition of _______ plus continuation of "
        "_______ therapy.",

        "Step 2 — add a weak opioid (tramadol 50–100 mg q4–6h, "
        "low-dose oxycodone 5–10 mg, or codeine 30–60 mg q4h)\n"
        "| Continue non-opioids (acetaminophen, NSAIDs if no contraindication) "
        "— multimodal analgesia reduces total opioid requirement\n"
        "→ CCRN KEY: WHO Ladder: Step 1 = non-opioids ± adjuvants (mild 1–3); "
        "Step 2 = weak opioid + non-opioid ± adjuvants (moderate 4–6); "
        "Step 3 = strong opioid + non-opioid ± adjuvants (severe 7–10). "
        "Move UP when pain is uncontrolled at current step.\n"
        "→ MASTERY NOTE: Adjuvants treat pain TYPE, not just intensity: "
        "gabapentin/pregabalin (neuropathic), TCAs (neuropathic), "
        "corticosteroids (bone/tumor inflammation), bisphosphonates "
        "(bone metastases). Add adjuvants at any step based on pain mechanism.",

        'tier-review',
        _PP,
        DID['professional'],
        'palliative_comfort',
        '{"pain":6}',
        'chart-l1'
    ),
    (
        "An ICU patient starts morphine 4 mg IV q4h for comfort care. "
        "Per palliative care protocol, three orders must be written "
        "simultaneously as prophylaxis: _______, _______, and _______.",

        "1. Bowel regimen — stimulant laxative (senna ± docusate): "
        "opioid-induced constipation is universal and does NOT resolve "
        "with tolerance; required for ALL opioid patients\n"
        "2. Antiemetic PRN (ondansetron or prochlorperazine): "
        "opioid-induced nausea common first 1–2 weeks, then tolerance develops\n"
        "3. PRN breakthrough dose = 10–15% of total daily scheduled opioid: "
        "if >3 PRN doses/24h, increase scheduled dose\n"
        "→ CCRN KEY: Opioid tolerance develops for: analgesia (requires dose "
        "increases), sedation (resolves), nausea (resolves 1–2 weeks), euphoria. "
        "Tolerance does NOT develop for constipation or miosis → bowel regimen "
        "is lifelong for chronic opioid users.\n"
        "→ MASTERY NOTE: Respiratory depression risk is highest at first doses "
        "in opioid-naive patients. Start low; titrate. Naloxone available but "
        "use ONLY for respiratory depression (RR <8, SpO₂ <90) — do not reverse "
        "for somnolence alone in comfort care patients.",

        'tier-high',
        _PP,
        DID['professional'],
        'palliative_comfort',
        '{"pain":8}',
        'chart-l2'
    ),
    (
        "Comfort-measures-only patient: SpO₂ 72%, respiratory rate 4, "
        "agonal breathing pattern, family at bedside asking if "
        "the patient is 'struggling.' The nurse's clinical priority is "
        "_______ and the communication priority is _______.",

        "Clinical priority: assess for air hunger/distress (grimacing, "
        "agitation, accessory muscle use despite low rate = dyspnea); "
        "if present, titrate opioid/benzodiazepine for symptom relief\n"
        "| Communication priority: normalize the dying process — explain "
        "that agonal breathing (irregular, slow, gasping) does NOT indicate "
        "patient suffering; it is the brainstem's final respiratory pattern; "
        "the patient is not aware of it\n"
        "→ CCRN KEY: Principle of double effect — palliative sedation targets "
        "comfort, not hastening death. Agonal respirations ≠ distress. "
        "Terminal secretions = pooled secretions in posterior pharynx; "
        "glycopyrrolate 0.2 mg IV/SC reduces new secretion production "
        "(does not clear existing secretions; avoid suctioning — stimulates more).\n"
        "→ MASTERY NOTE: Family presence at death: research shows families "
        "present at death have LOWER rates of complicated grief and PTSD than "
        "those not present. Facilitate presence; brief family on expected signs: "
        "color changes, Cheyne-Stokes breathing, mottled extremities, "
        "decreasing urine. 'Permission to go' statements may comfort patients.",

        'tier-critical',
        _PP,
        DID['professional'],
        'palliative_comfort',
        '{"pain":2}',
        'chart-l3'
    ),

    # ═══ qi_safety ════════════════════════════════════════════════════════════
    (
        "On the ABCDEF bundle chart, 'C' represents _______ "
        "and is called the anchor of the bundle because _______.",

        "C = Choice of Analgesia and Sedation — analgesia-first approach; "
        "avoid benzodiazepines as sedatives; target RASS -1 to 0 (light sedation)\n"
        "| It is the anchor because achieving light sedation enables all other "
        "elements: SBT (B) requires patient cooperation, delirium assessment "
        "(D) requires patient be arousable, early mobility (E) requires "
        "RASS ≥ -2\n"
        "→ CCRN KEY: Sedation-analgesia hierarchy: treat pain first → "
        "add propofol or dexmedetomidine if needed → avoid benzodiazepines "
        "(MENDS/SLEAP trials: benzos increase delirium by 1.5–2×). "
        "Daily RASS goal: -1 to 0 unless specific clinical indication.\n"
        "→ MASTERY NOTE: Pain-first protocol: assess CPOT (nonverbal) or NRS "
        "(verbal) before reaching for sedatives. Unrelieved pain causes "
        "agitation that is often mismanaged with sedatives, creating a "
        "cycle of oversedation → delirium → prolonged mechanical ventilation.",

        'tier-review',
        _PP,
        DID['professional'],
        'qi_safety',
        '{"sel":2}',
        'chart-l1'
    ),
    (
        "The ABCDEF bundle chart shows a patient RASS -3, CAM-ICU positive, "
        "on propofol day 4. Components B (SBT) and E (early mobility) "
        "cannot be performed because _______. "
        "The immediate bundle-guided intervention is _______.",

        "B and E require RASS ≥ -1 to -2 (patient must be arousable to "
        "cooperate); RASS -3 = deep sedation — patient cannot participate\n"
        "| Immediate intervention: Spontaneous Awakening Trial (SAT) — "
        "stop all sedatives/analgesics; assess SAT safety screen; allow "
        "patient to awaken; coordinate with respiratory for SAT→SBT sequence\n"
        "→ CCRN KEY: SAT safety screen contraindications: active seizures, "
        "alcohol withdrawal/DTs, RASS ≥+2 agitation, active myocardial ischemia, "
        "elevated ICP. SAT failure: restart sedation at 50% of previous dose.\n"
        "→ MASTERY NOTE: ABCDEF bundle reduces ICU delirium by ~89% when "
        "consistently applied. ICU delirium outcomes: increased 30-day mortality "
        "(×3), prolonged MV, longer LOS, long-term cognitive impairment "
        "(BRAIN-ICU trial). CAM-ICU = 4 features: acute onset/fluctuation, "
        "inattention, altered LOC, disorganized thinking.",

        'tier-high',
        _PP,
        DID['professional'],
        'qi_safety',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "A patient at ICU day 6 develops symmetric proximal weakness, "
        "loss of deep tendon reflexes, and ventilator dependence. "
        "This is ICU-acquired weakness (ICU-AW), reflecting failure of "
        "ABCDEF bundle component _______, with MRC sum score defining "
        "ICU-AW as _______.",

        "Failure of E (Early Mobility/Exercise) combined with risk factors: "
        "sepsis, prolonged corticosteroids, neuromuscular blockade, "
        "hyperglycemia\n"
        "| MRC sum score < 48/60 = ICU-AW "
        "(MRC: 0–5 scale × 6 muscle groups bilateral)\n"
        "→ CCRN KEY: ICU-AW affects 25–50% of mechanically ventilated patients. "
        "Two mechanisms: critical illness myopathy (muscle wasting) and critical "
        "illness polyneuropathy (axonal degeneration). Both cause symmetric "
        "proximal > distal weakness and difficult ventilator weaning.\n"
        "→ MASTERY NOTE: E component protocol: begin when RASS ≥ -2, FiO₂ ≤60%, "
        "PEEP ≤10, stable vasopressor dose, no active arrhythmia. "
        "Sequence: passive ROM → active-assisted ROM → sit at edge of bed → "
        "stand → ambulate. PT/OT consult within 24–48h for high-risk patients "
        "(MV >48h, sepsis, prior deconditioning).",

        'tier-critical',
        _PP,
        DID['professional'],
        'qi_safety',
        '{"sel":4}',
        'chart-l3'
    ),

    # ═══ communication_sbar ════════════════════════════════════════════════════
    (
        "On the SBAR framework chart, the 'A' (Assessment) component "
        "distinguishes a skilled nurse's call from simple data-reporting "
        "because _______.",

        "Assessment = the nurse's clinical synthesis — stating what you "
        "THINK is happening, not just listing data points; allows the "
        "provider to understand severity and likely etiology without "
        "seeing the patient\n"
        "| Example: 'I believe he's developing acute pulmonary edema — "
        "CXR shows vascular congestion, he improved with sitting up' "
        "vs. merely stating 'SpO₂ 88%, RR 28'\n"
        "→ CCRN KEY: SBAR: S = current situation (brief, specific); "
        "B = relevant background (diagnosis, labs, trends); "
        "A = nurse's clinical interpretation; R = specific request "
        "('I need you to come assess' or 'I need a furosemide order'). "
        "Recommendation must be SPECIFIC — avoid 'what do you want me to do?'\n"
        "→ MASTERY NOTE: Joint Commission safety goal: structured communication "
        "reduces handoff errors. IPASS (Illness severity, Patient summary, "
        "Action list, Situation awareness, Synthesis) is validated for "
        "written handoffs and reduces medical errors by 30%.",

        'tier-review',
        _PP,
        DID['professional'],
        'communication_sbar',
        '{"sc":0}',
        'chart-l1'
    ),
    (
        "In the respiratory distress SBAR scenario, the nurse calls: "
        "S = 'SpO₂ 83%, RR 30, tripod positioning.' "
        "Before proceeding to Recommendation, the 'A' component must "
        "include _______ and _______, because _______.",

        "A must include: 1) clinical interpretation of likely etiology "
        "('I believe this is acute COPD exacerbation vs. PE vs. CHF — "
        "new wheeze, PEFR dropped 40%') AND 2) severity statement "
        "('patient is in moderate-severe respiratory distress')\n"
        "| Because: a complete Assessment allows the provider to make a "
        "disposition decision remotely — without it, the provider may "
        "underestimate urgency or give inappropriate empiric orders\n"
        "→ CCRN KEY: If patient is deteriorating rapidly — lead with "
        "'This is an emergency, I need you in the room NOW' — do not "
        "complete the framework when immediate intervention is required. "
        "SBAR is a tool, not a formality.\n"
        "→ MASTERY NOTE: Closed-loop communication: after receiving an order, "
        "repeat it back ('So I'll give 40 mg furosemide IV now — correct?'). "
        "Closed-loop communication reduces transcription and dosing errors, "
        "especially under emergency conditions.",

        'tier-high',
        _PP,
        DID['professional'],
        'communication_sbar',
        '{"sc":1}',
        'chart-l2'
    ),
    (
        "At shift change, the outgoing nurse fails to mention that the "
        "patient's central line is 72 hours old with a bloody, soiled "
        "dressing not yet changed. This handoff failure involves "
        "SBAR component _______ and creates immediate _______ risk.",

        "Failure of B (Background) — relevant current status of IV access "
        "(line age, site assessment, dressing integrity) is required "
        "background information at every handoff\n"
        "| Immediate CLABSI risk: blood under occlusive dressing creates "
        "warm, moist bacterial culture medium; soiled/bloody dressings "
        "must be changed immediately (not at scheduled interval)\n"
        "→ CCRN KEY: CLABSI prevention bundle: daily necessity assessment "
        "(remove line ASAP when no longer needed); chlorhexidine-impregnated "
        "dressing; document insertion date and site assessment at every "
        "handoff; sterile dressing change q7d or PRN soiled/loose/compromised.\n"
        "→ MASTERY NOTE: IPASS handoff mandates required elements to prevent "
        "omissions: Illness severity, Patient summary (events, current status), "
        "Action list (pending tasks), Situation awareness (what could go wrong, "
        "contingency plans), Synthesis (receiver reads back key points). "
        "Standardized handoffs with required fields reduce errors — "
        "open-ended verbal handoffs allow critical information gaps.",

        'tier-critical',
        _PP,
        DID['professional'],
        'communication_sbar',
        '{"sc":2}',
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

    print(f"{'='*65}")
    print(f"CHUNK {CHUNK_NUM} — Validating {len(CARDS)} cards")
    print(f"{'='*65}")

    for i, card in enumerate(CARDS):
        front, back, tier, badge, did, ctype, pj, ltag = card
        issues = validator.validate(f'c{CHUNK_NUM}_{i}', front, back, badge)
        warns  = validator.results[-1].get('warnings', [])
        ok     = not issues
        w_str  = ' W8' if warns else ''
        print(f"  {'OK' if ok else 'XX'} [{ctype}·{ltag}]{w_str}  {front[:65]}")
        if not ok:
            for iss in issues: print(f"      x {iss}")

    print(validator.report())
    print()

    for i, card in enumerate(CARDS):
        front, back, tier, badge, did, ctype, pj, ltag = card
        issues = validator.validate(f'c{CHUNK_NUM}_{i}_check', front, back, badge)
        if issues:
            print(f"  SKIP (invalid): {front[:55]}")
            continue

        chart_idx = CHART_ORDER.index(ctype) if ctype in CHART_ORDER else i
        mid_int   = MID_BASE + chart_idx
        mkey      = str(mid_int)

        if mkey not in models:
            qfmt, afmt = make_chart_template(
                ctype, pj, RF[ctype], SHARED_JS, CHART_CSS)
            register_chart_model(models, mid_int, ctype, did, qfmt, afmt, CHART_CSS)

        guid = make_guid(front, back)
        if guid in existing_guids:
            print(f"  SKIP (duplicate): {front[:50]}")
            continue
        existing_guids.add(guid)

        flds = '\x1f'.join([safe_html(front), safe_html(back), tier, badge])
        sfld = re.sub(r'<[^>]+>', '', front)[:100]
        nid  = nid_base + i * 3
        tags = f' ccrn-pccn-v6 chunk-{CHUNK_NUM} {ltag} '

        insert_card(db, nid, nid+1, guid, mkey, flds, sfld, did, tags, now)
        added += 1
        print(f"  + [{ctype}·{ltag}]  {front[:65]}")

    save_deck(db, models, WORK_DIR, OUT_PATH)

    db2 = sqlite3.connect(os.path.join(WORK_DIR, 'collection.anki2'))
    total = db2.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    db2.close()

    print(f"\n{'='*65}")
    print(f"  Chunk {CHUNK_NUM}: {added} cards added | Total deck: {total} cards")
    print(f"{'='*65}")


if __name__ == '__main__':
    main()
