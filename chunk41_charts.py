#!/usr/bin/env python3
"""chunk41_charts.py — Ph7 Antiarrhythmics (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_40.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_41.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c41')
CHUNK_NUM   = 41
MID_BASE    = 1_800_005_050
CHART_ORDER = ['vaughan_williams', 'antiarrhythmic_selection', 'amiodarone_toxicity',
               'adenosine_svt', 'qt_prolongation']

_AR = 'Ph7 · \U0001f7e1 T3 · Pharmacology — Antiarrhythmics'

RF = {}

# ── Chart 1: Vaughan Williams Classification ──────────────────────────────────
RF['vaughan_williams'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var rows=[
        {cl:'IA', m1:'Na⁺ block (mod)',    m2:'+ K⁺ block',       apd:'↑ APD',   d:'Procainamide\nQuinidine',  u:'A-Fib / flutter\nVT prophylaxis',       c:'#c07828'},
        {cl:'IB', m1:'Na⁺ block (weak)',   m2:'fast off-rate',         apd:'↓ APD',   d:'Lidocaine\nMexiletine',    u:'Ischemic VT\nDigitalis toxicity',        c:'#3a9a5c'},
        {cl:'IC', m1:'Na⁺ block (strong)', m2:'slow off-rate',         apd:'No Δ APD',d:'Flecainide\nPropafenone',  u:'SVT / parox A-Fib\nNo struct disease',  c:'#38b2a4'},
        {cl:'II', m1:'β-receptor block',   m2:'↓ automaticity',   apd:'— APD',   d:'Metoprolol\nEsmolol',      u:'Rate ctrl A-Fib\nSVT / sinus tachy',    c:'#4488cc'},
        {cl:'III',m1:'K⁺ channel block',   m2:'↑ refractoriness', apd:'↑↑ APD',d:'Amiodarone\nSotalol',    u:'VT / V-Fib\nA-Fib rhythm ctrl',         c:'#e07020'},
        {cl:'IV', m1:'Ca²⁺ ch. block',m2:'(L-type, AV node)',     apd:'— APD',   d:'Verapamil\nDiltiazem',     u:'SVT (AV nodal)\nA-Fib rate ctrl',       c:'#9060c0'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=20, rh=Math.floor((H-hdrH)/rows.length);
    var xs=[4,52,185,245,390,618];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Class','Mechanism','APD Effect','Key Drugs','Clinical Use'];
    ctx.font='bold 9px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-5);});
    rows.forEach(function(row,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=row.c;ctx.fillRect(xs[0]+2,ry+4,xs[1]-xs[0]-4,rh-8);
        ctx.fillStyle='#000';ctx.font='bold 11px sans-serif';ctx.textAlign='center';
        ctx.fillText(row.cl,(xs[0]+xs[1])/2,ry+rh/2+4);
        ctx.fillStyle='#ccd';ctx.font='10px sans-serif';ctx.textAlign='left';
        ctx.fillText(row.m1,xs[1]+4,ry+rh/2-2);
        ctx.fillStyle='#556';ctx.font='9px sans-serif';
        ctx.fillText(row.m2,xs[1]+4,ry+rh/2+9);
        var apdCol=row.apd.startsWith('↑')?'#e05050':(row.apd.startsWith('↓')?'#50b050':'#888');
        ctx.fillStyle=apdCol;ctx.font='bold 10px sans-serif';ctx.textAlign='center';
        ctx.fillText(row.apd,(xs[2]+xs[3])/2,ry+rh/2+4);
        ctx.fillStyle='#dde';ctx.font='10px sans-serif';ctx.textAlign='left';
        row.d.split('\n').forEach(function(dl,di){ctx.fillText(dl,xs[3]+4,ry+rh/2-2+di*11);});
        ctx.fillStyle='#aab8aa';ctx.font='9px sans-serif';
        row.u.split('\n').forEach(function(ul,ui){ctx.fillText(ul,xs[4]+4,ry+rh/2-2+ui*11);});
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
        var lbs=['IA','IB','IC','II','III','IV'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,rows[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: Antiarrhythmic Selection by Arrhythmia ──────────────────────────
RF['antiarrhythmic_selection'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var rows=[
        {arr:'A-Fib Rate\nControl',    fl:'IV Diltiazem / Metoprolol',       alt:'Digoxin (low EF)\nAmiodarone (EF<40)',   note:'Target HR ≤110 bpm\nAcute; 60–80 chronic',  c:'#4488aa'},
        {arr:'A-Fib Rhythm\nControl',  fl:'IV Amiodarone\nIV Ibutilide',      alt:'Flecainide/Propaf\n(no struct disease)', note:'≥48h/unstable: DCCV\nAnticoag before DCCV',   c:'#aa4488'},
        {arr:'SVT\n(AVNRT / AVRT)',    fl:'Adenosine 6→12→12 mg\nRapid IV push + flush',alt:'Diltiazem/Verapamil\nMetoprolol',note:'WPW: avoid CCBs\nUse procainamide',      c:'#3a9a5c'},
        {arr:'Stable\nMonomorphic VT', fl:'Amiodarone 150 mg IV\nover 10 min',alt:'Lidocaine 1–1.5\nmg/kg IV',         note:'ACLS preferred\nin struct disease',                  c:'#e07020'},
        {arr:'V-Fib /\nPulseless VT',  fl:'Defibrillation + CPR\n+ Epi 1 mg IV',alt:'Amiodarone 300 mg IV\nor Lidocaine 1.5mg/kg',note:'SHOCK FIRST always\nAntiarrhythmic 2nd', c:'#cc2222'},
        {arr:'Torsades\nde Pointes',   fl:'MgSO₄ 2 g IV\nover 10 min',   alt:'Overdrive pacing\nIsoproterenol',        note:'Stop QT-prolonging\ndrugs; K⁺ goal >4.0',     c:'#cc3366'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=20, rh=Math.floor((H-hdrH)/rows.length);
    var xs=[4,155,305,450,618];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Arrhythmia','First-Line Rx','Alternative','Clinical Note'];
    ctx.font='bold 9px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-5);});
    rows.forEach(function(row,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=row.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=row.c;ctx.font='bold 9px sans-serif';ctx.textAlign='left';
        row.arr.split('\n').forEach(function(al,ai){ctx.fillText(al,xs[0]+4,ry+rh/2-2+ai*11);});
        ctx.fillStyle='#5aba5a';ctx.font='10px sans-serif';
        row.fl.split('\n').forEach(function(fl,fi){ctx.fillText(fl,xs[1]+4,ry+rh/2-2+fi*11);});
        ctx.fillStyle='#7799aa';ctx.font='9px sans-serif';
        row.alt.split('\n').forEach(function(al,ai){ctx.fillText(al,xs[2]+4,ry+rh/2-2+ai*11);});
        ctx.fillStyle='#887766';ctx.font='9px sans-serif';
        row.note.split('\n').forEach(function(nl,ni){ctx.fillText(nl,xs[3]+4,ry+rh/2-2+ni*11);});
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
        var lbs=['A-Fib Rate','A-Fib Rhythm','SVT','VT','V-Fib','TdP'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,rows[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 3: Amiodarone Multi-Organ Toxicity ─────────────────────────────────
RF['amiodarone_toxicity'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:-1;
    var organs=[
        {name:'Thyroid',     short:'Hypo / Hyperthyroid', c:'#e07020',
         eff:['T4→T3 blocked → hypothyroidism (most common)','Jod-Basedow: iodine load → hyperthyroidism','Type 2 AIT: destructive thyroiditis'],
         mon:'TFTs at baseline, then every 3–6 months',
         mgmt:'Hypo: levothyroxine (continue amio) | Hyper T1: thionamides | Hyper T2: steroids'},
        {name:'Pulmonary',   short:'Interstitial pneumonitis', c:'#cc2222',
         eff:['Interstitial pneumonitis → fibrosis (2–5%)','CXR: bilateral infiltrates | HRCT: diagnostic','PFTs: restrictive pattern + ↓ DLCO'],
         mon:'Annual CXR + PFTs; HRCT if symptomatic',
         mgmt:'DISCONTINUE immediately | Corticosteroids for severe cases'},
        {name:'Hepatic',     short:'Transaminase elevation', c:'#c07828',
         eff:['Hepatotoxicity (phospholipidosis)','AST/ALT elevation: mild, very common','Cirrhosis: rare, long-term use'],
         mon:'LFTs at baseline, then every 6 months',
         mgmt:'Discontinue if >3× ULN or symptomatic hepatitis'},
        {name:'Corneal',     short:'Microdeposits (reversible)', c:'#38b2a4',
         eff:['Corneal verticillata: near-universal >6 mo','Visual halos, photophobia (usually mild)','Optic neuropathy: rare but IRREVERSIBLE'],
         mon:'Annual slit-lamp ophthalmology exam',
         mgmt:'Microdeposits: benign, resolve on D/C | Optic neuropathy: stop immediately'},
        {name:'Skin',        short:'Photosensitivity / blue-gray', c:'#9060c0',
         eff:['Photosensitivity: sunburn with minimal UV','Blue-gray discoloration: late effect (years)','High iodine accumulates in dermis'],
         mon:'Clinical inspection; UV protection education',
         mgmt:'Sunscreen + protective clothing | Discoloration may persist after D/C'},
        {name:'Neurological',short:'Neuropathy / tremor', c:'#3a9a5c',
         eff:['Peripheral neuropathy: dose-related','Tremor, ataxia, cognitive changes','Proximal muscle weakness'],
         mon:'Neurological exam; patient-reported symptoms',
         mgmt:'Dose reduction | B6 supplementation may help neuropathy'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var cols=3, ncols=cols, nrows=2, gap=6;
    var bw=Math.floor((W-gap*(ncols+1))/ncols), bh=58;
    var gridY=4;
    organs.forEach(function(org,i){
        var col=i%ncols, row=Math.floor(i/ncols);
        var bx=gap+col*(bw+gap), by=gridY+row*(bh+gap);
        var active=(sel===i);
        ctx.fillStyle=active?org.c+'33':'#0d0d18';ctx.fillRect(bx,by,bw,bh);
        ctx.strokeStyle=active?org.c:'#2a2a2a';ctx.lineWidth=active?2:1;ctx.strokeRect(bx,by,bw,bh);
        ctx.fillStyle=org.c;ctx.font='bold 11px sans-serif';ctx.textAlign='center';
        ctx.fillText(org.name,bx+bw/2,by+20);
        ctx.fillStyle='#778';ctx.font='8.5px sans-serif';
        ctx.fillText(org.short,bx+bw/2,by+34);
    });
    var panelY=gridY+nrows*(bh+gap)+4;
    var panelH=H-panelY-4;
    ctx.fillStyle='#0a0a1a';ctx.fillRect(4,panelY,W-8,panelH);
    ctx.strokeStyle='#222';ctx.lineWidth=1;ctx.strokeRect(4,panelY,W-8,panelH);
    if(sel<0){
        ctx.fillStyle='#444';ctx.font='11px sans-serif';ctx.textAlign='center';
        ctx.fillText('Select an organ system above to view toxicity details',W/2,panelY+panelH/2+4);
    } else {
        var org=organs[sel];
        ctx.fillStyle=org.c;ctx.font='bold 12px sans-serif';ctx.textAlign='left';
        ctx.fillText(org.name+' Toxicity',12,panelY+16);
        ctx.fillStyle='#ccc';ctx.font='10px sans-serif';
        org.eff.forEach(function(e,ei){ctx.fillText('• '+e,12,panelY+30+ei*13);});
        var baseY=panelY+30+org.eff.length*13+5;
        ctx.fillStyle='#778';ctx.font='9px sans-serif';
        ctx.fillText('Monitor: '+org.mon,12,baseY);
        ctx.fillStyle='#c07828';ctx.font='9px sans-serif';
        var mgmt=org.mgmt, maxW=W-24, words=mgmt.split(' '), line='', ly=baseY+13;
        words.forEach(function(w){var t=line?line+' '+w:w;if(ctx.measureText(t).width>maxW){ctx.fillText(line,12,ly);line=w;ly+=12;}else line=t;});
        if(line)ctx.fillText(line,12,ly);
    }
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        organs.forEach(function(org,i){(function(idx){var b=_mkB(org.name,org.c,sel===idx,function(on){
            var ns=on?idx:-1;cv.setAttribute('data-params',JSON.stringify({sel:ns}));_render(cv,ctrl,{sel:ns});
        });row.appendChild(b);})(i);});
        var rst=_mkB('Overview',_AX,sel===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 4: Adenosine SVT Algorithm ─────────────────────────────────────────
RF['adenosine_svt'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var doseData=[
        {mg:'6 mg', lbl:'Initial Dose', note:'Rapid push + 20 mL flush', c:'#3a9a5c'},
        {mg:'12 mg',lbl:'Repeat ×1',  note:'If no conversion (1–2 min)', c:'#e07020'},
        {mg:'12 mg',lbl:'Repeat ×2',  note:'If still no conversion',c:'#cc2222'}
    ];
    var bg=20, bw=180, bh=74, by=4;
    var boxXs=[bg, bg+bw+bg, bg+2*(bw+bg)];
    doseData.forEach(function(d,i){
        var bx=boxXs[i];
        ctx.fillStyle='#0a180a';ctx.fillRect(bx,by,bw,bh);
        ctx.strokeStyle=d.c;ctx.lineWidth=1.5;ctx.strokeRect(bx,by,bw,bh);
        ctx.fillStyle=d.c;ctx.font='bold 26px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.mg,bx+bw/2,by+36);
        ctx.fillStyle='#aaa';ctx.font='bold 9px sans-serif';
        ctx.fillText(d.lbl,bx+bw/2,by+51);
        ctx.fillStyle='#556';ctx.font='8.5px sans-serif';
        ctx.fillText(d.note,bx+bw/2,by+63);
    });
    ctx.fillStyle='#556';ctx.font='bold 14px sans-serif';ctx.textAlign='center';
    ctx.fillText('▶',boxXs[1]-bg/2,by+bh/2+5);
    ctx.fillText('▶',boxXs[2]-bg/2,by+bh/2+5);
    var panelY=by+bh+6, panelH=H-panelY-4;
    ctx.fillStyle='#0a0a1a';ctx.fillRect(4,panelY,W-8,panelH);
    var tabs=['Mechanism','Contraindications','Alternative Agents','Key Facts'];
    var tabW=(W-8)/tabs.length, tabH=20;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a2a3a':'#0d0d0d';ctx.fillRect(tx,panelY,tabW,tabH);
        ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.strokeRect(tx,panelY,tabW,tabH);
        ctx.fillStyle=sel===i?'#38b2a4':'#555';ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,panelY+13);
    });
    var content=[
        ['Adenosine → A₁ receptor → ↑ K⁺ conductance → hyperpolarization',
         'SA node depression + transient AV nodal block (10–15 sec)',
         'Interrupts AV-nodal re-entry circuit (AVNRT / AVRT)',
         'Half-life: ~10 seconds | Effective for ~80% of SVT',
         'Diagnostic: slows A-Fib/flutter → reveals flutter waves if no conversion'],
        ['ABSOLUTE: WPW with pre-excitation (→ V-Fib via accessory pathway)',
         'ABSOLUTE: 2nd / 3rd degree AV block (without pacemaker)',
         'ABSOLUTE: Sick sinus syndrome (without pacemaker)',
         'ABSOLUTE: Severe reactive airway disease / active asthma (bronchospasm)',
         'RELATIVE: Dipyridamole (↑ adenosine effect ×4) | Carbamazepine | Heart transplant'],
        ['Asthma / AV block → Verapamil 2.5–5 mg IV or Diltiazem 0.25 mg/kg IV',
         'WPW with pre-excitation → Procainamide 15–17 mg/kg IV (NO AV nodal blockers)',
         'Hemodynamically unstable → Synchronized cardioversion immediately',
         'Wide-complex (unknown type) → Amiodarone preferred over adenosine',
         'Heart transplant → Use ¼ dose (1.5–3 mg): denervated heart hypersensitive'],
        ['Route: Antecubital or central IV → rapid push → 20 mL NS flush immediately',
         'Half-life: 8–10 seconds (enzymatic degradation by adenosine deaminase)',
         'Side effects: flushing, dyspnea, chest pressure (transient — warn patient)',
         'Expected response: brief AV block / pause (seconds) — normal and required',
         'Not effective for: A-Fib, A-Flutter, V-Tach (not AV-nodal dependent)']
    ];
    var ly=panelY+tabH+14;
    content[sel].forEach(function(line){
        ctx.fillStyle='#bbb';ctx.font='9.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(line,12,ly);ly+=13;
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,_TE,sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 5: QTc Prolongation & Torsades Risk ────────────────────────────────
RF['qt_prolongation'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var qval=(P.qval!==undefined)?P.qval:450;
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var QMN=300, QMX=620, scaleX=30, scaleW=W-60;
    var ms2x=function(ms){return scaleX+(ms-QMN)/(QMX-QMN)*scaleW;};
    var barY=20, barH=28;
    var zones=[
        {lo:300,hi:440,c:'#1a5a1a'},{lo:440,hi:500,c:'#5a3a00'},{lo:500,hi:620,c:'#5a1a1a'}
    ];
    zones.forEach(function(z){
        ctx.fillStyle=z.c;ctx.fillRect(ms2x(z.lo),barY,ms2x(z.hi)-ms2x(z.lo),barH);
    });
    ctx.strokeStyle='#333';ctx.lineWidth=1;ctx.strokeRect(scaleX,barY,scaleW,barH);
    var ticks=[300,400,440,500,600];
    ticks.forEach(function(ms){
        var x=ms2x(ms);
        ctx.strokeStyle='#444';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(x,barY+barH);ctx.lineTo(x,barY+barH+4);ctx.stroke();
        ctx.fillStyle='#666';ctx.font='8px sans-serif';ctx.textAlign='center';
        ctx.fillText(ms+'ms',x,barY+barH+13);
    });
    ctx.fillStyle='#333';ctx.font='8px sans-serif';ctx.textAlign='left';
    ctx.fillText('Normal',scaleX+4,barY+12);
    ctx.fillStyle='#aa7020';ctx.fillText('Caution',ms2x(440)+4,barY+12);
    ctx.fillStyle='#cc2222';ctx.fillText('High Risk',ms2x(500)+4,barY+12);
    var qx=ms2x(qval);
    var qcol=qval<440?'#50c050':(qval<500?'#e07020':'#ee3333');
    ctx.strokeStyle=qcol;ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(qx,barY-6);ctx.lineTo(qx,barY+barH+4);ctx.stroke();
    ctx.fillStyle=qcol;
    ctx.beginPath();ctx.moveTo(qx-5,barY-12);ctx.lineTo(qx+5,barY-12);ctx.lineTo(qx,barY-4);ctx.closePath();ctx.fill();
    ctx.fillStyle=qcol;ctx.font='bold 10px sans-serif';ctx.textAlign='center';
    ctx.fillText('QTc '+qval+'ms',qx,barY-14);
    var interpY=barY+barH+20;
    var interp=qval<440?'Normal QTc — routine monitoring':(qval<500?'CAUTION: Monitor ECG; avoid addl QT-prolonging agents; replete K⁺/Mg²⁺':'HIGH RISK (>500ms): Discontinue causative agent(s); continuous monitoring; Torsades risk');
    ctx.fillStyle=qcol;ctx.font='bold 9px sans-serif';ctx.textAlign='left';
    ctx.fillText(interp,scaleX,interpY);
    var panelY=interpY+16, panelH=H-panelY-4;
    ctx.fillStyle='#0a0a1a';ctx.fillRect(4,panelY,W-8,panelH);
    var tabs=['Drug Offenders','Risk Factors','Management'];
    var tabW=(W-8)/tabs.length, tabH=20;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a2a3a':'#0d0d0d';ctx.fillRect(tx,panelY,tabW,tabH);
        ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.strokeRect(tx,panelY,tabW,tabH);
        ctx.fillStyle=sel===i?_TE:'#555';ctx.font=(sel===i?'bold ':'')+'9px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,panelY+13);
    });
    var content=[
        ['Antibiotics: Azithromycin, Fluoroquinolones (Ciprofloxacin, Levofloxacin)',
         'Antifungals: Fluconazole, Voriconazole, Itraconazole',
         'Antipsychotics: Haloperidol, Droperidol, Quetiapine, Ziprasidone',
         'Other: Methadone, Ondansetron (IV), Cisapride, Chloroquine',
         'Cardiac (Class III): Amiodarone, Sotalol, Dofetilide, Ibutilide'],
        ['Electrolytes: Hypokalemia (K⁺ <3.5), Hypomagnesemia (Mg²⁺ <1.7), Hypocalcemia',
         'Bradycardia (HR <50): pause-dependent TdP | Post-cardioversion pause',
         'Female sex (longer baseline QTc) | Age >65 | Congenital long QT syndrome',
         'Cardiac: CHF, LVH, myocardial ischemia, cardiomyopathy',
         '≥2 QT-prolonging drugs simultaneously = exponential risk increase'],
        ['QTc 440–500ms: Avoid additional QT drugs; replete K⁺ >4.0, Mg²⁺ >2.0; telemetry',
         'QTc >500ms or ΔQTc >60ms: DISCONTINUE causative agent(s); continuous telemetry',
         'TdP (with pulse): MgSO₄ 2 g IV over 10 min; correct electrolytes',
         'Recurrent TdP: Overdrive pacing 90–100 bpm (shortens QT) or isoproterenol infusion',
         'Pulseless TdP / V-Fib: Unsynchronized defibrillation — cannot sync polymorphic VT']
    ];
    var ly=panelY+tabH+13;
    content[sel].forEach(function(line){
        ctx.fillStyle='#bbb';ctx.font='9.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(line,10,ly);ly+=13;
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin-top:6px;';
        var sl=_mkS('QTc:',300,620,5,qval,function(v){return v+'ms';},function(v){
            var p2={qval:v,sel:sel};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });
        row.appendChild(sl);
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,_TE,sel===idx,function(){
            var p2={qval:qval,sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        ctrl.appendChild(row);
    }
}
"""

# ── Cards ─────────────────────────────────────────────────────────────────────
CARDS = [
    # ═══ vaughan_williams ════════════════════════════════════════════════════
    (
        "On the Vaughan Williams chart, Class IC agents (flecainide, "
        "propafenone) are _______ in patients with structural heart "
        "disease or prior MI. The landmark trial that proved this is _______.",

        "CONTRAINDICATED — Class IC agents are proarrhythmic in diseased myocardium\n"
        "| CAST trial (Cardiac Arrhythmia Suppression Trial, 1989): IC agents "
        "suppressed PVCs post-MI but DOUBLED mortality from fatal arrhythmias\n"
        "→ CCRN KEY: Class IC = most potent Na⁺ channel blockers (slow on/off rate "
        "→ action potential prolonged at faster rates). Safe only in structurally "
        "normal hearts for paroxysmal SVT or A-Fib. Any prior MI, LVH, CHF, or EF <40% "
        "= absolute contraindication.\n"
        "→ MASTERY NOTE: Class IC 'use-dependence' explains why they are dangerous "
        "in ischemia: faster HR (as in VT) = greater Na⁺ block = more proarrhythmia. "
        "Normal hearts tolerate this; scarred myocardium cannot.",

        'tier-review',
        _AR,
        DID['antiarrhythmics'],
        'vaughan_williams',
        '{"hi":2}',
        'chart-l1'
    ),
    (
        "The Vaughan Williams chart shows Class III antiarrhythmics "
        "prolong action potential duration by blocking _______ channels. "
        "Which Class III drug ALSO has Class I, II, and IV properties?",

        "K⁺ (potassium) channels — blocking K⁺ efflux prolongs repolarization "
        "(↑ APD, ↑ effective refractory period)\n"
        "| Amiodarone — the 'dirty' antiarrhythmic: blocks Na⁺ (Class I), "
        "K⁺ (Class III), Ca²⁺ (Class IV), AND β-receptors (Class II)\n"
        "→ CCRN KEY: Amiodarone's multi-channel activity = highly effective for "
        "VT/V-Fib and A-Fib, but also drives multi-organ toxicity (thyroid, "
        "pulmonary, hepatic, corneal, skin, neurological). Half-life 40–55 days "
        "means side effects outlast the drug after discontinuation.\n"
        "→ MASTERY NOTE: Other Class III agents: Sotalol (also Class II — beta-blocker), "
        "Dofetilide (pure K⁺ blocker, requires in-hospital initiation with QTc monitoring), "
        "Ibutilide (IV only, A-Fib/flutter cardioversion).",

        'tier-high',
        _AR,
        DID['antiarrhythmics'],
        'vaughan_williams',
        '{"hi":4}',
        'chart-l2'
    ),
    (
        "On the Vaughan Williams chart, a patient has narrow-complex SVT "
        "refractory to two doses of adenosine. The class that slows AV "
        "conduction via L-type Ca²⁺ channel blockade is Class _______. "
        "Name two drugs and one key contraindication.",

        "Class IV — L-type Ca²⁺ channel blockade slows conduction through "
        "the AV node (which depends on slow Ca²⁺ currents, unlike ventricle)\n"
        "| Drugs: Verapamil 2.5–5 mg IV (diltiazem 0.25 mg/kg IV)\n"
        "| Key contraindication: WPW with pre-excitation — Class IV blocks AV "
        "node but leaves accessory pathway open → impulses conduct exclusively "
        "via accessory pathway → very rapid ventricular rate → V-Fib\n"
        "→ CCRN KEY: Class IV is also used for A-Fib rate control (oral diltiazem "
        "or verapamil). Avoid in EF <40% — significant negative inotropic effect "
        "worsens hemodynamics in low-output states.\n"
        "→ MASTERY NOTE: Adenosine vs. verapamil for SVT: adenosine preferred "
        "first-line (ultra-short half-life, easily reversed). Verapamil is used "
        "when adenosine fails or is contraindicated (asthma, transplant).",

        'tier-critical',
        _AR,
        DID['antiarrhythmics'],
        'vaughan_williams',
        '{"hi":5}',
        'chart-l3'
    ),

    # ═══ antiarrhythmic_selection ═════════════════════════════════════════════
    (
        "On the antiarrhythmic selection chart, acute rate control of A-Fib "
        "with hypotension (SBP 82) and EF 25% should use IV _______ "
        "instead of calcium channel blockers. Explain why.",

        "IV Amiodarone (150 mg over 10 minutes)\n"
        "| Reason: CCBs (diltiazem, verapamil) are strong negative inotropes "
        "→ further reduce EF and worsen hypotension in cardiogenic/low-output states\n"
        "| Amiodarone provides rate control with less hemodynamic compromise\n"
        "→ CCRN KEY: A-Fib with hemodynamic compromise (any EF) = synchronized "
        "cardioversion if unstable. If marginally stable with low EF: amiodarone "
        "for rate control. Digoxin IV is an option for rate control without "
        "negative inotropy but has slow onset (hours).\n"
        "→ MASTERY NOTE: The 48-hour rule for A-Fib cardioversion: if onset "
        ">48h or unknown → anticoagulate ≥3 weeks before elective DCCV, OR "
        "perform TEE to rule out left atrial thrombus before urgent cardioversion.",

        'tier-review',
        _AR,
        DID['antiarrhythmics'],
        'antiarrhythmic_selection',
        '{"hi":0}',
        'chart-l1'
    ),
    (
        "The antiarrhythmic selection chart shows Torsades de Pointes "
        "management. First-line treatment is IV _______ _______ g "
        "over 10 minutes. If TdP recurs, the next intervention is _______.",

        "Magnesium sulfate (MgSO₄) 2 g IV over 10 minutes\n"
        "| Mechanism: MgSO₄ stabilizes cardiac membrane and suppresses "
        "early afterdepolarizations (EADs) that trigger TdP\n"
        "| Works even with NORMAL serum Mg²⁺ levels\n"
        "| If TdP recurs: overdrive pacing at 90–100 bpm (higher HR "
        "shortens QT interval, eliminating pause-dependent trigger) "
        "OR isoproterenol infusion (increases HR pharmacologically)\n"
        "→ CCRN KEY: Simultaneously correct: K⁺ >4.0 mEq/L, Mg²⁺ >2.0 mg/dL, "
        "Ca²⁺. Hypokalemia worsens QTc and potentiates TdP. Discontinue all "
        "QT-prolonging medications.\n"
        "→ MASTERY NOTE: TdP is pause-dependent — usually triggered by "
        "bradycardia or a long pause (long-short cycle). This is why overdrive "
        "pacing and isoproterenol work: they prevent the long pause.",

        'tier-high',
        _AR,
        DID['antiarrhythmics'],
        'antiarrhythmic_selection',
        '{"hi":5}',
        'chart-l2'
    ),
    (
        "On the selection chart, a hemodynamically stable patient has "
        "sustained wide-complex VT with known prior MI (structural disease). "
        "Per ACLS, the preferred IV antiarrhythmic is _______. "
        "If the patient becomes unstable, the next step is _______.",

        "Amiodarone 150 mg IV over 10 minutes (preferred over lidocaine "
        "for stable monomorphic VT in structural heart disease)\n"
        "| Lidocaine 1–1.5 mg/kg IV is the alternative\n"
        "| If becomes hemodynamically unstable → synchronized cardioversion\n"
        "→ CCRN KEY: ACLS stable monomorphic VT algorithm: amiodarone OR "
        "procainamide OR sotalol IV. Amiodarone is most commonly used. "
        "Procainamide 15–17 mg/kg IV is alternative (especially for WPW-related VT). "
        "Do NOT give amiodarone AND procainamide together (additive QT prolongation).\n"
        "→ MASTERY NOTE: Pulseless VT = treat like V-Fib: defibrillation (200J "
        "biphasic) → CPR → epinephrine → amiodarone 300 mg IV push. The distinction "
        "stable VT vs. pulseless VT is made at the bedside — not by rhythm alone.",

        'tier-critical',
        _AR,
        DID['antiarrhythmics'],
        'antiarrhythmic_selection',
        '{"hi":3}',
        'chart-l3'
    ),

    # ═══ amiodarone_toxicity ══════════════════════════════════════════════════
    (
        "On the amiodarone toxicity chart, new bilateral pulmonary "
        "infiltrates on CXR in a patient on chronic amiodarone suggests "
        "_______ toxicity. The required immediate action is _______.",

        "Amiodarone pulmonary toxicity (APT) — interstitial pneumonitis\n"
        "| Discontinue amiodarone immediately; initiate corticosteroids "
        "for moderate-to-severe cases (prednisone 40–60 mg/day)\n"
        "| Confirm with HRCT (ground-glass/bilateral infiltrates) + "
        "PFTs (restrictive + ↓ DLCO) + BAL (foamy macrophages = lipid-laden)\n"
        "→ CCRN KEY: APT occurs in 2–5% of patients; can be subacute (months) "
        "or acute. CXR appearance mimics PNA or heart failure — distinguish "
        "with HRCT and clinical context. Annual CXR + PFTs are standard monitoring.\n"
        "→ MASTERY NOTE: Amiodarone accumulates in lung tissue (high lipid "
        "solubility, 40-day half-life). Even after stopping, drug persists weeks "
        "to months — corticosteroids needed to suppress ongoing inflammation. "
        "Pulmonary toxicity is the most life-threatening long-term side effect.",

        'tier-high',
        _AR,
        DID['antiarrhythmics'],
        'amiodarone_toxicity',
        '{"sel":1}',
        'chart-l1'
    ),
    (
        "The amiodarone toxicity chart shows thyroid effects. Amiodarone "
        "inhibits _______ conversion AND contains 37% iodine by weight. "
        "Distinguish Type 1 from Type 2 amiodarone-induced thyrotoxicosis (AIT).",

        "T4 → T3 conversion (inhibits peripheral deiodinase = type 1 deiodinase)\n"
        "| Type 1 AIT: excess iodine load → increased thyroid hormone synthesis "
        "(Jod-Basedow effect) — seen in patients with pre-existing thyroid disease "
        "or nodular goiter. Treat with thionamides (methimazole/PTU).\n"
        "| Type 2 AIT: destructive thyroiditis — direct drug-induced destruction "
        "of thyroid follicles → hormone release. Treat with corticosteroids.\n"
        "→ CCRN KEY: Hypothyroidism is more common than hyperthyroidism on amiodarone. "
        "Hypothyroid: treat with levothyroxine — do NOT stop amiodarone for this "
        "alone (benefit vs. risk). Monitor TFTs at baseline, 3 months, then q6 months.\n"
        "→ MASTERY NOTE: Amiodarone's iodine load = 200 mg tablet provides "
        "~75 mg iodine/day (vs. daily requirement of 150 mcg). This overwhelms "
        "the thyroid's ability to regulate iodine uptake.",

        'tier-critical',
        _AR,
        DID['antiarrhythmics'],
        'amiodarone_toxicity',
        '{"sel":0}',
        'chart-l2'
    ),
    (
        "On the amiodarone toxicity chart, a patient on long-term therapy "
        "reports visual halos and photophobia. The corneal finding is _______. "
        "Is this reversible? Distinguish from the rare, serious eye complication.",

        "Corneal microdeposits (corneal verticillata / whirl-like deposits)\n"
        "| Reversible — deposits resolve within months of discontinuation\n"
        "| Nearly universal in patients on amiodarone >6 months; usually asymptomatic "
        "or causes mild halos/photophobia; does NOT typically impair visual acuity\n"
        "| Rare serious complication: OPTIC NEUROPATHY (amiodarone-induced optic "
        "neuropathy/AION) — IRREVERSIBLE vision loss; requires immediate "
        "discontinuation\n"
        "→ CCRN KEY: Monitor with annual slit-lamp ophthalmology exam. "
        "Distinguish: corneal deposits (benign, reversible, very common) vs. "
        "optic neuropathy (vision changes, reduced acuity, afferent pupillary defect — "
        "rare but serious and not reversible).\n"
        "→ MASTERY NOTE: Amiodarone toxicity monitoring checklist: TFTs, LFTs, "
        "annual PFTs + CXR, annual ophthalmology, skin assessment, neurological review. "
        "Document at every visit — multi-organ monitoring is part of nursing scope.",

        'tier-high',
        _AR,
        DID['antiarrhythmics'],
        'amiodarone_toxicity',
        '{"sel":3}',
        'chart-l3'
    ),

    # ═══ adenosine_svt ════════════════════════════════════════════════════════
    (
        "On the adenosine SVT algorithm chart, the initial IV dose for "
        "narrow-complex SVT is _______ mg. If ineffective after 1–2 min, "
        "the repeat dose is _______ mg. What must immediately follow each push?",

        "Initial: 6 mg IV rapid push → Repeat: 12 mg IV (can give twice)\n"
        "| Must immediately follow with 20 mL NS rapid flush — flushes drug "
        "to central circulation before enzymatic degradation (half-life 10 sec)\n"
        "→ CCRN KEY: Use proximal (antecubital or central) IV — peripheral "
        "hand/wrist IV may deliver insufficient drug due to short half-life "
        "before reaching the AV node. Some protocols use 12 mg initial dose "
        "for peripheral IVs. Failure rate increases significantly without "
        "proper flush technique.\n"
        "→ MASTERY NOTE: Adenosine dose sequence: 6 → 12 → 12 mg. If three "
        "doses fail to convert SVT, the rhythm may not be AV-nodal dependent "
        "(consider atrial tachycardia, A-Fib with rapid ventricular response, "
        "WPW pre-excitation). Proceed to alternative agents or cardioversion.",

        'tier-review',
        _AR,
        DID['antiarrhythmics'],
        'adenosine_svt',
        '{}',
        'chart-l1'
    ),
    (
        "The adenosine SVT algorithm shows its mechanism: adenosine "
        "temporarily blocks _______ conduction via A₁ receptor activation, "
        "causing transient _______ to terminate the re-entry circuit.",

        "AV nodal conduction — A₁ receptor → ↑ K⁺ conductance → "
        "hyperpolarization of nodal cells → SA node depression + AV block\n"
        "| Transient AV block (10–15 seconds) terminates the re-entry circuit "
        "that keeps AVNRT or AVRT running\n"
        "→ CCRN KEY: Adenosine is effective ONLY for tachycardias that require "
        "the AV node as part of the re-entry circuit (AVNRT, AVRT). It will NOT "
        "terminate A-Fib or A-Flutter — but it will transiently slow the rate "
        "and reveal flutter waves (useful diagnostically).\n"
        "→ MASTERY NOTE: After conversion, a brief pause or AV block of 5–15 "
        "seconds is EXPECTED and normal — warn the patient about flushing, "
        "chest tightness, and 'heart stopping' sensation (terrifying but harmless "
        "and self-terminating). Have atropine available for prolonged pauses.",

        'tier-high',
        _AR,
        DID['antiarrhythmics'],
        'adenosine_svt',
        '{"sel":0}',
        'chart-l2'
    ),
    (
        "On the SVT chart, adenosine is absolutely contraindicated in "
        "_______ (two conditions). The alternative AV nodal agent is _______. "
        "In WPW with pre-excitation, what is the correct agent?",

        "Absolute contraindications:\n"
        "1. WPW with pre-excitation (delta waves on ECG, wide complex): "
        "AV node block → impulse forced exclusively via accessory pathway "
        "→ extremely rapid ventricular rate → V-Fib\n"
        "2. Severe reactive airway disease / active asthma: A₁ receptor "
        "activation causes bronchospasm → life-threatening bronchospasm\n"
        "| Also: 2nd/3rd degree AV block, sick sinus syndrome (without pacer)\n"
        "| Alternative AV nodal agent (for asthma/AV block): Verapamil 2.5–5 mg IV\n"
        "| WPW with pre-excitation: Procainamide 15–17 mg/kg IV (Class IA — "
        "slows accessory pathway without blocking AV node)\n"
        "→ CCRN KEY: WPW + A-Fib = medical emergency. ALL AV nodal blockers "
        "(adenosine, CCBs, digoxin, beta-blockers) are contraindicated — each "
        "increases accessory pathway conduction → V-Fib. Procainamide or "
        "synchronized cardioversion are the only safe options.\n"
        "→ MASTERY NOTE: Pre-excitation on ECG = short PR, delta wave, wide QRS. "
        "Recognize this BEFORE giving adenosine for 'SVT.'",

        'tier-critical',
        _AR,
        DID['antiarrhythmics'],
        'adenosine_svt',
        '{"sel":1}',
        'chart-l3'
    ),

    # ═══ qt_prolongation ══════════════════════════════════════════════════════
    (
        "On the QTc prolongation chart, a corrected QT interval > 500 ms "
        "requires _______. The life-threatening arrhythmia triggered by "
        "this degree of QT prolongation is _______, which can degenerate to _______.",

        "QTc >500ms: Discontinue or reduce QT-prolonging agents; correct "
        "electrolytes (K⁺ >4.0, Mg²⁺ >2.0); continuous cardiac monitoring\n"
        "| Consider withholding scheduled QT-prolonging medications and "
        "notifying the provider\n"
        "| Life-threatening arrhythmia: Torsades de Pointes (TdP) — "
        "polymorphic ventricular tachycardia with characteristic twisting "
        "QRS axis around the isoelectric line\n"
        "| Can degenerate to: Ventricular Fibrillation (V-Fib)\n"
        "→ CCRN KEY: QTc calculation: QT / √RR (Bazett formula). Normal: "
        "men <440ms, women <450ms. High-risk threshold: >500ms OR ΔQTc >60ms "
        "from baseline. Obtain 12-lead ECG before and during QT-prolonging "
        "drug therapy in ICU patients.\n"
        "→ MASTERY NOTE: The ICU 'triple threat' for TdP: QT-prolonging drug + "
        "hypokalemia + bradycardia. Any combination of two or more exponentially "
        "increases risk. Proactive electrolyte repletion is a nursing priority.",

        'tier-review',
        _AR,
        DID['antiarrhythmics'],
        'qt_prolongation',
        '{"qval":510,"sel":2}',
        'chart-l1'
    ),
    (
        "The QTc chart shows a patient receiving IV haloperidol, "
        "IV fluconazole, and K⁺ 3.0 mEq/L. These three factors _______ "
        "the QTc synergistically. The priority nursing action is _______.",

        "Synergistically PROLONG the QTc (two QT-prolonging drugs + "
        "hypokalemia = compounded risk)\n"
        "| Priority action: Obtain 12-lead ECG immediately to measure "
        "current QTc; notify provider; replete K⁺ to >4.0 mEq/L; "
        "hold repeat haloperidol if QTc >500ms pending provider order\n"
        "→ CCRN KEY: Common ICU QT-prolonging drug pairs to avoid: "
        "azithromycin + fluconazole, haloperidol + methadone, ondansetron + "
        "ciprofloxacin. Use crediblemeds.org risk classification when uncertain.\n"
        "→ MASTERY NOTE: Hypokalemia potentiates drug-induced QT prolongation "
        "because K⁺ efflux through hERG channel drives repolarization — "
        "lower K⁺ = slower repolarization = longer QTc. Repletion to K⁺ >4.0 "
        "(not just ≥3.5) provides extra buffer in high-risk patients.",

        'tier-high',
        _AR,
        DID['antiarrhythmics'],
        'qt_prolongation',
        '{"qval":480,"sel":0}',
        'chart-l2'
    ),
    (
        "On the QTc chart, a patient develops Torsades de Pointes "
        "that degenerates to pulselessness. Immediate treatment includes "
        "IV _______ 2 g AND _______ shock delivery (synchronized/unsynchronized). "
        "For recurrent TdP with pulse, the next intervention is _______.",

        "Magnesium sulfate (MgSO₄) 2 g IV rapid push\n"
        "| UNSYNCHRONIZED defibrillation (360J monophasic or 200J biphasic) — "
        "polymorphic VT has no consistent R wave to sync to; attempting "
        "synchronization wastes time and may fail to deliver shock\n"
        "| For recurrent TdP with pulse: overdrive pacing at 90–100 bpm "
        "(eliminates the pause-dependent trigger) OR isoproterenol infusion "
        "0.5–2 mcg/min (increases HR pharmacologically)\n"
        "→ CCRN KEY: Pulseless TdP = treat identically to V-Fib: "
        "immediate defibrillation → CPR → epinephrine → MgSO₄ 2 g IV. "
        "Do NOT delay defibrillation to give MgSO₄ — electricity first.\n"
        "→ MASTERY NOTE: Synchronized vs. unsynchronized distinction: "
        "synchronized cardioversion for rhythms WITH a detectable R wave "
        "(A-Fib, A-Flutter, monomorphic VT with pulse). Unsynchronized "
        "defibrillation for V-Fib, pulseless VT, and polymorphic VT "
        "(TdP) — no consistent R wave to trigger synchronization.",

        'tier-critical',
        _AR,
        DID['antiarrhythmics'],
        'qt_prolongation',
        '{"qval":530,"sel":2}',
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
