#!/usr/bin/env python3
"""chunk45_charts.py — Ph7 Anticoagulants (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_44.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_45.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c45')
CHUNK_NUM   = 45
MID_BASE    = 1_800_005_070
CHART_ORDER = ['anticoagulant_comparison', 'heparin_protocol', 'warfarin_management',
               'anticoagulant_reversal', 'vte_prophylaxis']

_NM = 'Ph7 · \U0001f7e1 T3 · Pharmacology — Anticoagulants'

RF = {}

# ── Chart 1: Anticoagulant Comparison ────────────────────────────────────────
RF['anticoagulant_comparison'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var drugs=[
        {name:'UFH',          mech:'Activates antithrombin\n→ inhibits IIa + Xa',     mon:'aPTT 60–100 sec\nor anti-Xa 0.3–0.7',rev:'Protamine\n1 mg/100 u (complete)',use:'VTE/PE treatment\nCardiac surgery',c:'#4488cc'},
        {name:'Enoxaparin\n(LMWH)',mech:'Activates antithrombin\n→ primarily inhibits Xa',mon:'Anti-Xa 0.5–1.0\n(4h post-dose, PRN)',rev:'Protamine (partial\n~60% efficacy)',   use:'VTE prophylaxis/Rx\nACS/STEMI/NSTEMI',c:'#3a9a5c'},
        {name:'Fondaparinux', mech:'Indirect Xa inhibitor\n(antithrombin-dependent)',  mon:'Anti-Xa if needed\n(predictable kinetics)',rev:'None specific\n(4F-PCC off-label)',  use:'HIT alternative\nCaution CrCl <30',c:'#38b2a4'},
        {name:'Argatroban',   mech:'Direct thrombin (IIa)\ninhibitor — IV infusion',   mon:'aPTT 1.5–3× base\nor dTT/ECT',          rev:'None (stop infusion\nt½ 39–51 min)',     use:'HIT anticoagulation\nRenal failure safe',c:'#cc3333'},
        {name:'Bivalirudin',  mech:'Direct thrombin (IIa)\ninhibitor — IV infusion',   mon:'aPTT 1.5–2.5×\nor ACT (cardiac)',       rev:'None (stop infusion\nt½ 25 min)',        use:'PCI/cardiac surgery\nHIT + cardiac procs',c:'#e07020'},
        {name:'Warfarin',     mech:'Vit K antagonist\n→ ↓ factors II,VII,IX,X',       mon:'INR (target 2–3\nmost indications)',      rev:'4F-PCC + Vit K IV\nor FFP (large vol)', use:'AF, mechanical valves\nVTE long-term Rx',c:'#cc6633'},
        {name:'Apixaban/\nRivaroxaban',mech:'Direct Xa inhibitor\n(oral, no monitoring)',mon:'No routine lab\n(predictable kinetics)',rev:'Andexanet alfa\nor 4F-PCC off-label', use:'AF, DVT/PE, ACS\nNo INR monitoring',c:'#9060c0'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/drugs.length);
    var xs=[4,90,210,295,390,500,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Drug','Mechanism','Monitor','Reversal','Key ICU Use'];
    ctx.font='bold 8.5px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    drugs.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=d.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=d.c;ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        d.name.split('\n').forEach(function(nl,ni){ctx.fillText(nl,xs[0]+3,ry+rh/2-3+ni*10);});
        ctx.fillStyle='#aab';ctx.font='8px sans-serif';
        d.mech.split('\n').forEach(function(ml,mi){ctx.fillText(ml,xs[1]+3,ry+rh/2-3+mi*9);});
        ctx.fillStyle='#88aabb';ctx.font='8px sans-serif';
        d.mon.split('\n').forEach(function(ml,mi){ctx.fillText(ml,xs[2]+3,ry+rh/2-3+mi*9);});
        ctx.fillStyle='#cc8866';ctx.font='8px sans-serif';
        d.rev.split('\n').forEach(function(rl,ri2){ctx.fillText(rl,xs[3]+3,ry+rh/2-3+ri2*9);});
        ctx.fillStyle='#9ab8aa';ctx.font='8px sans-serif';
        d.use.split('\n').forEach(function(ul,ui){ctx.fillText(ul,xs[4]+3,ry+rh/2-3+ui*9);});
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
        var lbs=['UFH','LMWH','Fondaparinux','Argatroban','Bivalirudin','Warfarin','DOAC-Xa'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,drugs[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: UFH Heparin Protocol ─────────────────────────────────────────────
RF['heparin_protocol'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var aptt=(P.aptt!==undefined)?P.aptt:62;
    var zones=[
        {lo:0,  hi:39,  lbl:'aPTT <40 sec',   action:'IV Bolus 80 u/kg → ↑ infusion 4 u/kg/h',      col:'#cc3333'},
        {lo:40, hi:49,  lbl:'aPTT 40–49 sec',  action:'IV Bolus 40 u/kg → ↑ infusion 2 u/kg/h',      col:'#cc6633'},
        {lo:50, hi:75,  lbl:'aPTT 50–75 sec',  action:'NO CHANGE — Therapeutic range ★',              col:'#3a9a5c'},
        {lo:76, hi:100, lbl:'aPTT 76–100 sec', action:'↓ infusion by 2 u/kg/h  (no bolus, no hold)',  col:'#e07020'},
        {lo:101,hi:120, lbl:'aPTT 101–120',    action:'HOLD 30 min → ↓ infusion by 2 u/kg/h',         col:'#cc6633'},
        {lo:121,hi:999, lbl:'aPTT >120 sec',   action:'HOLD 60 min → ↓ infusion by 3 u/kg/h',         col:'#cc3333'}
    ];
    var curZ=zones.length-1;
    for(var z=0;z<zones.length;z++){if(aptt<=zones[z].hi){curZ=z;break;}}

    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    ctx.fillStyle='#4488cc';ctx.font='bold 9.5px sans-serif';ctx.textAlign='center';
    ctx.fillText('UFH WEIGHT-BASED HEPARIN PROTOCOL',W/2,11);
    ctx.fillStyle='#666';ctx.font='8px sans-serif';
    ctx.fillText('Initial: Bolus 80 u/kg IV | Infusion 18 u/kg/h | Target aPTT 50–75 sec  |  Anti-Xa 0.3–0.7 IU/mL',W/2,22);

    var barX=44, barW=W-88, barY=28, barBH=16, maxSc=160;
    var toX=function(v){return barX+Math.round(Math.min(v,maxSc)/maxSc*barW);};
    var zCols=['#cc3333','#cc6633','#3a9a5c','#e07020','#cc6633','#cc3333'];
    var zLims=[0,40,50,75,100,120,160];
    for(var zi=0;zi<6;zi++){
        var x1=toX(zLims[zi]),x2=toX(zLims[zi+1]);
        ctx.fillStyle=zCols[zi]+'55';ctx.fillRect(x1,barY,x2-x1,barBH);
        ctx.strokeStyle=zCols[zi]+'88';ctx.lineWidth=0.5;ctx.strokeRect(x1,barY,x2-x1,barBH);
    }
    var mx=toX(Math.min(aptt,maxSc));
    ctx.fillStyle=zones[curZ].col;
    ctx.beginPath();ctx.moveTo(mx-5,barY-5);ctx.lineTo(mx+5,barY-5);ctx.lineTo(mx,barY-1);ctx.closePath();ctx.fill();
    ctx.fillStyle='#fff';ctx.font='bold 7px sans-serif';ctx.textAlign='center';
    ctx.fillText(aptt,mx,barY-7);
    ctx.fillStyle='#555';ctx.font='7px sans-serif';ctx.textAlign='center';
    [0,40,50,75,100,120].forEach(function(v){ctx.fillText(v,toX(v),barY+barBH+8);});
    ctx.fillStyle='#444';ctx.textAlign='left';ctx.fillText('sec',barX+barW+4,barY+barBH+8);

    var tY=barY+barBH+14, rh=Math.floor((H-tY)/zones.length);
    zones.forEach(function(z,ri){
        var ry=tY+ri*rh, isAct=(ri===curZ);
        ctx.fillStyle=isAct?z.col+'33':(ri%2?'#0a0a10':'#0d0d14');ctx.fillRect(0,ry,W,rh);
        if(isAct){ctx.strokeStyle=z.col;ctx.lineWidth=1.5;ctx.strokeRect(1,ry+1,W-2,rh-2);}
        ctx.fillStyle=z.col;ctx.font=(isAct?'bold ':'')+'8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(z.lbl,4,ry+rh/2+3);
        ctx.fillStyle=isAct?'#eee':'#999';ctx.font=(isAct?'bold ':'')+'9px sans-serif';
        ctx.fillText(z.action,130,ry+rh/2+3);
        ctx.strokeStyle='#1a1a1a';ctx.lineWidth=0.5;
        ctx.beginPath();ctx.moveTo(0,ry+rh);ctx.lineTo(W,ry+rh);ctx.stroke();
    });

    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:6px;';
        var sl=_mkS('aPTT:',20,180,2,aptt,function(v){return Math.round(v)+' sec';},function(v){
            var p2={aptt:Math.round(v)};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });
        row.appendChild(sl);ctrl.appendChild(row);
    }
}
"""

# ── Chart 3: Warfarin Management & Reversal ───────────────────────────────────
RF['warfarin_management'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var scenarios=[
        {name:'Major Bleeding / ICH',        c:'#cc3333'},
        {name:'No Bleed — INR 4–9',           c:'#e07020'},
        {name:'No Bleed — INR >9',            c:'#cc6633'},
        {name:'Urgent Pre-op Reversal',       c:'#9060c0'}
    ];
    var s=scenarios[sel];
    var hdH=22;
    ctx.fillStyle=s.c+'22';ctx.fillRect(4,4,W-8,hdH);
    ctx.strokeStyle=s.c+'66';ctx.lineWidth=1;ctx.strokeRect(4,4,W-8,hdH);
    ctx.fillStyle=s.c;ctx.font='bold 10px sans-serif';ctx.textAlign='center';
    ctx.fillText('WARFARIN: '+s.name.toUpperCase(),W/2,4+hdH-6);
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0a1a';ctx.fillRect(4,panelY,W-8,panelH);
    var content=[
        [['EMERGENCY REVERSAL — any INR, active major bleeding / ICH','',
          '1. STOP warfarin immediately',
          '2. 4-Factor PCC (Kcentra) 25–50 units/kg IV — FIRST-LINE',
          '   Reverses factors II, VII, IX, X within 15–30 min',
          '   Target INR <1.5 (or per indication; <1.2 for neurosurgery)',
          '3. Vitamin K 10 mg IV slow infusion (30–60 min) — given with PCC',
          '   Vit K restores endogenous factor synthesis for sustained effect',
          '   (PCC reversal lasts only 6–12h without Vit K co-administration)',
          '4. FFP if 4F-PCC unavailable: 15–20 mL/kg IV (large volume; slower)',
          '','Note: ICH reversal → target INR ≤1.3 BEFORE neurosurgery if needed']],
        [['SUPRATHERAPEUTIC — No Bleeding, INR 4.0–9.0','',
          '1. HOLD warfarin (1–2 doses)',
          '2. Vitamin K oral 1–2.5 mg (INR 4–6) or 2.5–5 mg (INR 6–9)',
          '   Oral Vit K achieves INR reduction in 24–48 hours',
          '   IV Vit K is faster (hours) but risks anaphylaxis and warfarin',
          '   resistance — reserve IV route for bleeding or urgent reversal',
          '3. Recheck INR in 24 hours; restart warfarin at lower dose when INR <3',
          '','Risk factors requiring closer monitoring: age >65, concurrent NSAID,',
          'recent surgery, frequent falls, prior GI bleed, liver disease']],
        [['CRITICALLY HIGH — No Bleeding, INR >9.0','',
          '1. HOLD warfarin',
          '2. Vitamin K oral 5–10 mg (higher dose for faster reduction)',
          '3. Recheck INR in 24h; repeat Vit K dose if INR still >6',
          '','Hospitalization/close follow-up considerations:',
          '  Stable patient, INR 9–12: oral Vit K + close outpatient follow-up',
          '  INR >12 or high bleeding risk: consider admission for monitoring',
          '','After INR normalized: restart warfarin at ≤50% of prior dose;',
          'consider evaluation for drug-drug interaction, dietary change, or illness',
          'driving INR elevation before resuming previous dose']],
        [['PRE-OPERATIVE REVERSAL — Urgent (<4–6 h to procedure)','',
          'Target INR: <1.5 for most surgery; <1.2 for neurosurgery/spinal',
          '','1. 4-Factor PCC (Kcentra): 10–50 units/kg dose based on INR',
          '   INR 2–3.9 → 25 units/kg; INR 4–6 → 35 units/kg; >6 → 50 units/kg',
          '   Onset: INR reduction within 15–30 min (fastest option)',
          '2. Vitamin K 10 mg IV slow (30–60 min) — concurrent; sustains effect',
          '','FFP alone NOT appropriate for urgent pre-op: 15–20 mL/kg required;',
          '  takes 2–4h to thaw+infuse; INR correction incomplete and unpredictable',
          '','Fresh frozen plasma is acceptable only when 4F-PCC is unavailable']]
    ];
    var col=sel<content.length?content[sel][0]:[];
    var ly=panelY+13;
    col.forEach(function(line){
        if(line===''){ly+=4;return;}
        var isHead=(line.startsWith('EMERGENCY')||line.startsWith('SUPRATHERAPEUTIC')||line.startsWith('CRITICALLY')||line.startsWith('PRE-OPERATIVE'));
        var isSub=line.startsWith('   ')||line.startsWith('  ');
        var isStep=(line.match(/^\d\./));
        ctx.fillStyle=isHead?s.c:(isStep?'#ddaa66':(isSub?'#8899aa':'#bbb'));
        ctx.font=isHead?'bold 9.5px sans-serif':'9px sans-serif';ctx.textAlign='left';
        ctx.fillText(line,10,ly);ly+=isHead?15:12;
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        scenarios.forEach(function(sc,i){(function(idx){var b=_mkB(sc.name,sc.c,sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 4: Anticoagulant Reversal Agents ────────────────────────────────────
RF['anticoagulant_reversal'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var rows=[
        {agent:'Protamine\nSulfate',  reverses:'UFH (complete)\nLMWH (≈60% partial)',dose:'1 mg/100 u UFH given\npast 2–4h; max 50 mg IV',onset:'5–15 min',notes:'Slow IV push (<5 mg/min)\nAdverse: hypotension,\nbradycardia, anaphylaxis',c:'#4488cc'},
        {agent:'Vitamin K\n(phytonadione)',reverses:'Warfarin (VKA)\n(restores factors II,VII,IX,X)',dose:'Oral: 1–10 mg PRN\nIV: 10 mg slow × 30–60 min',onset:'Oral 24–48h\nIV 6–12h',notes:'IV risk: anaphylaxis\n(give slowly). Does NOT\nreverse immediately.',c:'#3a9a5c'},
        {agent:'4-Factor PCC\n(Kcentra)',reverses:'Warfarin — rapid complete\n(contains II,VII,IX,X,C,S)',dose:'INR 2–3.9: 25 u/kg\nINR 4–6: 35 u/kg; >6: 50u/kg',onset:'15–30 min',notes:'Give WITH Vit K IV\n(PCC alone reversal lasts\nonly 6–12h without Vit K)',c:'#cc6633'},
        {agent:'Idarucizumab\n(Praxbind)',reverses:'Dabigatran ONLY\n(direct thrombin inhibitor)',dose:'5 g IV in 2 vials\n(2.5 g each) IV push/inf',onset:'Minutes\n(near-complete)',notes:'Humanized antibody fragment\nbinds dabigatran with\n350× higher affinity than thrombin',c:'#cc3333'},
        {agent:'Andexanet Alfa\n(Andexxa)',reverses:'Xa inhibitors:\napixaban, rivaroxaban, edoxaban',dose:'High: 800 mg bolus +\n8 mg/min × 120 min\nLow: 400 mg + 4 mg/min × 120m',onset:'2–5 min\n(anti-Xa reversal)',notes:'High dose: last dose\n>7–8h OR rivaroxaban any\nLow dose: apixaban <8h ago',c:'#9060c0'},
        {agent:'FFP\n(Fresh Frozen Plasma)',reverses:'Warfarin, multiple factors\n(contains all clotting factors)',dose:'15–20 mL/kg IV\n(large volume required)',onset:'1–4h\n(thaw + infuse)',notes:'Volume overload risk\n(1000–1500 mL for 70 kg)\nSecond-line to 4F-PCC',c:'#888888'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/rows.length);
    var xs=[4,95,230,360,420,540,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Agent','Reverses','Dose','Onset','Key Notes'];
    ctx.font='bold 8.5px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    rows.forEach(function(row,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=row.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=row.c;ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        row.agent.split('\n').forEach(function(al,ai){ctx.fillText(al,xs[0]+3,ry+rh/2-4+ai*10);});
        ctx.fillStyle='#88aabb';ctx.font='8px sans-serif';
        row.reverses.split('\n').forEach(function(rl,ri2){ctx.fillText(rl,xs[1]+3,ry+rh/2-3+ri2*9);});
        ctx.fillStyle='#ccaa88';ctx.font='7.5px sans-serif';
        row.dose.split('\n').forEach(function(dl,di){ctx.fillText(dl,xs[2]+3,ry+rh/2-3+di*9);});
        ctx.fillStyle='#88cc88';ctx.font='8px sans-serif';ctx.textAlign='center';
        row.onset.split('\n').forEach(function(ol,oi){ctx.fillText(ol,(xs[3]+xs[4])/2,ry+rh/2-3+oi*9);});
        ctx.fillStyle='#9999aa';ctx.font='7.5px sans-serif';ctx.textAlign='left';
        row.notes.split('\n').forEach(function(nl,ni){ctx.fillText(nl,xs[4]+3,ry+rh/2-3+ni*9);});
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
        var lbs=['Protamine','Vitamin K','4F-PCC','Idarucizumab','Andexanet','FFP'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,rows[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 5: VTE Prophylaxis and Treatment in the ICU ─────────────────────────
RF['vte_prophylaxis'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['VTE Prophylaxis','VTE Treatment','Renal Adjustment'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a2a1a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a3a2a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?_GN:'#555';ctx.font=(sel===i?'bold ':'')+'9px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0a1a';ctx.fillRect(4,panelY,W-8,panelH);
    var content=[
        [['ICU VTE PROPHYLAXIS — Standard & High-Risk Patients','',
          'PHARMACOLOGIC (preferred when no CI):',
          '  Enoxaparin 40 mg SQ daily (standard ICU prophylaxis)',
          '  UFH 5,000 units SQ q8–12h (renal failure, CrCl <30)',
          '  Fondaparinux 2.5 mg SQ daily (HIT history, CI to heparin)',
          '','MECHANICAL (add to pharmacologic, or use alone if pharm CI):',
          '  Sequential compression devices (SCDs) on lower extremities',
          '  Graduated compression stockings (GCS) — less effective alone',
          '','High-risk: trauma, orthopedic surgery, obesity, cancer, prior DVT',
          '  Consider enoxaparin 40 mg q12h or fondaparinux 2.5 mg daily',
          '  IVC filter: only if pharmacologic + mechanical contraindicated AND',
          '  high DVT risk (NOT routine prophylaxis — clot can form on filter)']],
        [['VTE TREATMENT — DVT and Pulmonary Embolism','',
          'DVT or Non-massive PE:',
          '  Enoxaparin 1 mg/kg SQ q12h OR 1.5 mg/kg SQ once daily',
          '  UFH infusion (weight-based) with aPTT monitoring (if bridging,',
          '  rapid reversal required, or severe renal failure)',
          '  Rivaroxaban 15 mg BID ×21d then 20 mg daily (oral DOAC option)',
          '  Apixaban 10 mg BID ×7d then 5 mg BID (oral DOAC option)',
          '','Massive PE (hemodynamic instability, SBP <90 or >40 mmHg drop):',
          '  Systemic thrombolytics (tPA 100 mg IV × 2h) if no contraindications',
          '  UFH therapeutic DURING and AFTER thrombolytics (hold during infusion)',
          '','Sub-massive PE (RV dysfunction + troponin rise, no hypotension):',
          '  Anticoagulation alone OR catheter-directed thrombolytics (discuss)']],
        [['ANTICOAGULANT DOSE ADJUSTMENT — Renal Impairment','',
          'Enoxaparin (LMWH):',
          '  CrCl ≥30: Standard dosing (40 mg daily prophylaxis; 1 mg/kg q12h Rx)',
          '  CrCl 15–29: Prophylaxis 30 mg daily; Therapeutic 1 mg/kg once daily',
          '  CrCl <15 or HD: AVOID enoxaparin (use UFH — titratable, reversible)',
          '  Anti-Xa monitoring recommended at CrCl 15–29 and extremes of weight',
          '','UFH: No dose adjustment needed for renal failure',
          '  UFH is preferred in: AKI, rapidly changing renal function,',
          '  need for rapid reversal (protamine), ESRD/hemodialysis patients',
          '','Fondaparinux: AVOID if CrCl <30 (renally cleared, accumulates)',
          '  Use with caution CrCl 30–50; monitor anti-Xa levels',
          '','DOACs: See package insert for CrCl-based dose reductions;',
          '  most DOACs CONTRAINDICATED in ESRD or CrCl <15–25 mL/min']]
    ];
    var col=sel<content.length?content[sel][0]:[];
    var ly=panelY+13;
    col.forEach(function(line){
        if(line===''){ly+=4;return;}
        var isHead=(line.startsWith('ICU VTE')||line.startsWith('VTE TREATMENT')||line.startsWith('ANTICOAGULANT DOSE'));
        var isSub=line.startsWith('  ');
        ctx.fillStyle=isHead?_GN:(isSub?'#8899aa':'#bbb');
        ctx.font=isHead?'bold 9.5px sans-serif':'9px sans-serif';ctx.textAlign='left';
        ctx.fillText(line,10,ly);ly+=isHead?15:12;
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;';
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,_GN,sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        ctrl.appendChild(row);
    }
}
"""

# ── Cards ─────────────────────────────────────────────────────────────────────
CARDS = [
    # ═══ anticoagulant_comparison ═════════════════════════════════════════════
    (
        "On the anticoagulant comparison chart, UFH monitoring uses aPTT "
        "(therapeutic target _______ sec). In obese patients or those with "
        "antiphospholipid syndrome, _______ monitoring is preferred because aPTT "
        "is _______ in these conditions.",

        "Therapeutic aPTT target: 60–100 seconds (corresponds to anti-Xa 0.3–0.7 IU/mL)\n"
        "| Preferred monitoring in obese/antiphospholipid: Anti-Xa level (peak 4h post-dose)\n"
        "| aPTT is unreliable in these conditions because:\n"
        "  - Obese patients: heparin volume of distribution altered; aPTT poorly reflects drug level\n"
        "  - Antiphospholipid syndrome (APS): lupus anticoagulant prolongs baseline aPTT "
        "  even without heparin → cannot interpret heparin effect on aPTT\n"
        "→ CCRN KEY: Anti-Xa level targets for UFH infusion: 0.3–0.7 IU/mL (therapeutic VTE); "
        "0.1–0.4 IU/mL (prophylaxis if monitoring required). Drawn as a peak at "
        "6h after infusion start or dose change.\n"
        "→ MASTERY NOTE: aPTT reagent variability between laboratories means the therapeutic "
        "range varies by institution. Some institutions use a ratio (patient aPTT/control aPTT "
        "of 1.5–2.5×) rather than an absolute value. Always check your hospital's specific "
        "heparin protocol. Anti-Xa monitoring bypasses this variability.",

        'tier-review',
        _NM,
        DID['anticoagulants'],
        'anticoagulant_comparison',
        '{"hi":0}',
        'chart-l1'
    ),
    (
        "On the comparison chart, argatroban and bivalirudin are both "
        "direct thrombin inhibitors used for HIT. They differ in clearance: "
        "argatroban is cleared _______, making it preferred in _______ failure. "
        "Bivalirudin is cleared _______ and preferred in _______ failure.",

        "Argatroban: hepatic clearance — preferred in RENAL failure (safe in AKI, ESRD)\n"
        "| Bivalirudin: predominantly renal/enzymatic clearance (proteolytic) — "
        "preferred in HEPATIC failure (safe in liver disease)\n"
        "| Key distinction: Argatroban is the standard HIT anticoagulant in ICU "
        "(most HIT patients have co-existing renal failure from critical illness).\n"
        "→ CCRN KEY: Argatroban monitoring: aPTT target 1.5–3× baseline (45–90 sec). "
        "Important caveat: argatroban elevates INR by ~0.5 units — "
        "when bridging to warfarin, use a chromogenic factor X assay to monitor "
        "warfarin effect (not INR alone) until argatroban is stopped.\n"
        "→ MASTERY NOTE: Bivalirudin advantage in CICO scenario: 80% of metabolism "
        "is enzyme-mediated (in blood) — t½ only 25 min means it self-clears rapidly "
        "even in renal failure (only 20% renally excreted). This makes bivalirudin "
        "the agent of choice for HIT patients undergoing cardiac surgery "
        "(PCI or CABG) where short t½ and procedural hemostasis are critical.",

        'tier-high',
        _NM,
        DID['anticoagulants'],
        'anticoagulant_comparison',
        '{"hi":3}',
        'chart-l2'
    ),
    (
        "The comparison chart shows enoxaparin (LMWH) is contraindicated when "
        "CrCl is _______ mL/min because it is _______ cleared. "
        "The preferred alternative in severe renal failure is _______.",

        "Contraindicated (or use with extreme caution + anti-Xa monitoring) when CrCl <30 mL/min\n"
        "| LMWH is primarily renally cleared → accumulates in renal failure → "
        "unpredictable drug levels → bleeding risk\n"
        "| Preferred alternative in CrCl <30 (or AKI, ESRD): UFH infusion (weight-based) "
        "— titrated by aPTT; instantly reversible with protamine\n"
        "→ CCRN KEY: Renal dosing for enoxaparin:\n"
        "CrCl ≥30: Standard (1 mg/kg q12h therapeutic; 40 mg daily prophylaxis)\n"
        "CrCl 15–29: Reduce to 1 mg/kg once daily (therapeutic); 30 mg daily (prophylaxis)\n"
        "CrCl <15 or HD: AVOID — use UFH (titratable, reversible, not renally cleared)\n"
        "→ MASTERY NOTE: Anti-Xa monitoring for LMWH at CrCl 15–29: draw peak anti-Xa "
        "4h after SQ dose. Target: 0.5–1.0 IU/mL (q12h dosing) or 1.0–2.0 IU/mL (q24h). "
        "In obesity (BMI >40) and very low body weight (<45 kg), monitor anti-Xa even "
        "with normal renal function — pharmacokinetics are altered at extremes of weight.",

        'tier-critical',
        _NM,
        DID['anticoagulants'],
        'anticoagulant_comparison',
        '{"hi":1}',
        'chart-l3'
    ),

    # ═══ heparin_protocol ═════════════════════════════════════════════════════
    (
        "On the heparin protocol chart, the initial weight-based UFH regimen "
        "is bolus _______ units/kg IV followed by infusion _______ units/kg/h. "
        "The therapeutic aPTT target is _______ seconds.",

        "Initial bolus: 80 units/kg IV (rounded to nearest 100 units)\n"
        "| Initial infusion: 18 units/kg/h (rounded to nearest 50 units/h)\n"
        "| Therapeutic aPTT target: 50–75 seconds (or per institutional protocol; "
        "corresponds to anti-Xa 0.3–0.7 IU/mL)\n"
        "→ CCRN KEY: Weight-based heparin (Raschke protocol) reduces time to "
        "therapeutic anticoagulation compared to fixed-dose protocols. "
        "Recheck aPTT: 6h after initiation (or dose change). Adjust using nomogram. "
        "For monitoring: do NOT draw aPTT from the line through which heparin is infusing "
        "— draw from a separate peripheral site or alternate lumen.\n"
        "→ MASTERY NOTE: Heparin resistance: requires unusually high doses to reach "
        "therapeutic aPTT. Causes: (1) Antithrombin III deficiency (heparin needs AT-III "
        "to work — supplement with FFP if AT-III deficient); (2) High acute-phase reactants "
        "(factor VIII elevation in sepsis/inflammation elevates aPTT baseline); "
        "(3) Large clot burden (heparin consumed by clot). Switch to anti-Xa monitoring.",

        'tier-review',
        _NM,
        DID['anticoagulants'],
        'heparin_protocol',
        '{"aptt":62}',
        'chart-l1'
    ),
    (
        "On the heparin protocol chart with aPTT >120 sec, the correct action "
        "is hold the infusion for _______ minutes then decrease by _______ u/kg/h. "
        "This differs from aPTT 101–120 sec, which requires hold of _______.",

        "aPTT >120 sec: HOLD infusion 60 minutes, then ↓ rate by 3 u/kg/h\n"
        "| aPTT 101–120 sec: HOLD infusion 30 minutes, then ↓ rate by 2 u/kg/h\n"
        "| After holding: recheck aPTT 6h post-restart\n"
        "→ CCRN KEY: Full UFH aPTT adjustment table:\n"
        "aPTT <40: Bolus 80 u/kg + ↑ 4 u/kg/h\n"
        "aPTT 40–49: Bolus 40 u/kg + ↑ 2 u/kg/h\n"
        "aPTT 50–75: No change ★ (therapeutic)\n"
        "aPTT 76–100: ↓ 2 u/kg/h (no hold, no bolus)\n"
        "aPTT 101–120: Hold 30 min → ↓ 2 u/kg/h\n"
        "aPTT >120: Hold 60 min → ↓ 3 u/kg/h\n"
        "→ MASTERY NOTE: Before attributing supratherapeutic aPTT to heparin excess, "
        "rule out: acquired coagulopathy (DIC, liver failure), factor deficiency, "
        "lupus anticoagulant, or lab error (fibrin interference in aPTT assay). "
        "If patient has unexplained bleeding WITH aPTT >120, consider anti-Xa monitoring "
        "rather than just dose reduction — the aPTT elevation may not be due to heparin.",

        'tier-high',
        _NM,
        DID['anticoagulants'],
        'heparin_protocol',
        '{"aptt":130}',
        'chart-l2'
    ),
    (
        "On the heparin protocol chart, anti-Xa monitoring is preferred over aPTT "
        "in two specific patient populations: _______ and _______. "
        "The anti-Xa therapeutic target for UFH infusion is _______.",

        "Preferred anti-Xa monitoring populations:\n"
        "1. Obesity (BMI >40 or weight >120 kg): aPTT poorly correlates with "
        "heparin levels due to altered volume of distribution and factor VIII elevation\n"
        "2. Antiphospholipid syndrome (APS): lupus anticoagulant prolongs baseline "
        "aPTT unpredictably, making aPTT uninterpretable as heparin monitor\n"
        "| Anti-Xa therapeutic target for UFH: 0.3–0.7 IU/mL\n"
        "→ CCRN KEY: Additional anti-Xa indications: extreme low weight (<45 kg), "
        "unexplained heparin resistance (requiring very high doses), discordance "
        "between clinical anticoagulation status and aPTT. Draw: ideally 6h after "
        "infusion start or dose change (steady-state sample).\n"
        "→ MASTERY NOTE: Anti-Xa for LMWH is drawn differently (peak at 4h post-SQ dose). "
        "The same anti-Xa assay platform can measure both UFH and LMWH, but the "
        "target ranges differ: UFH = 0.3–0.7; LMWH therapeutic = 0.5–1.0 IU/mL "
        "(q12h dosing) or 1.0–2.0 IU/mL (q24h dosing). Specify which agent when "
        "ordering the anti-Xa level.",

        'tier-critical',
        _NM,
        DID['anticoagulants'],
        'heparin_protocol',
        '{"aptt":62}',
        'chart-l3'
    ),

    # ═══ warfarin_management ══════════════════════════════════════════════════
    (
        "On the warfarin management chart, major bleeding (any INR) requires "
        "two immediate treatments: _______ and _______. "
        "The reason Vitamin K must be given WITH 4-factor PCC is _______.",

        "4-Factor PCC (Kcentra) 25–50 units/kg IV — immediate factor replacement "
        "(factors II, VII, IX, X, Protein C and S); reverses INR within 15–30 min\n"
        "| Vitamin K 10 mg IV slow infusion (30–60 min) — given concurrently\n"
        "| Reason to combine: PCC provides immediate reversal but effect lasts only "
        "6–12 hours (factors are consumed and not replenished). Vitamin K restores "
        "endogenous hepatic factor synthesis, sustaining the reversal effect.\n"
        "→ CCRN KEY: Major bleeding targets: INR <1.5 for most bleeding; INR <1.2 "
        "before neurosurgery. If 4F-PCC unavailable, use FFP 15–20 mL/kg (large volume, "
        "slower onset — second-line). For intracranial hemorrhage: highest urgency "
        "reversal; neurosurgical consultation immediately alongside pharmacologic reversal.\n"
        "→ MASTERY NOTE: 3-factor vs 4-factor PCC: 3-factor PCC (Bebulin, Profilnine) "
        "contains II, IX, X but NOT factor VII. Factor VII has the shortest half-life "
        "and is critical for initial INR correction. 4-factor PCC (Kcentra) contains "
        "all four vitamin K-dependent factors and is preferred for warfarin reversal. "
        "Always verify which PCC product your institution stocks.",

        'tier-review',
        _NM,
        DID['anticoagulants'],
        'warfarin_management',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The warfarin management chart shows INR 5–9 with no bleeding: "
        "the management is hold warfarin and give Vitamin K _______ mg by "
        "_______ route. The monitoring plan is recheck INR in _______ hours.",

        "Hold warfarin (1–2 doses)\n"
        "| Vitamin K: oral 2.5–5 mg (INR 5–9)\n"
        "| Recheck INR in 24 hours; restart warfarin at lower dose once INR <3\n"
        "→ CCRN KEY: Oral vs IV Vitamin K:\n"
        "• Oral: preferred for non-bleeding supratherapeutic INR — achieves INR "
        "reduction in 24–48h; safe; no anaphylaxis risk\n"
        "• IV: faster (reduction in 6–12h) but risk of anaphylaxis (0.03%) and "
        "subsequent warfarin resistance. Reserve IV for bleeding or urgent reversal.\n"
        "• SQ/IM routes: erratic absorption — avoid (especially IM: hematoma risk)\n"
        "→ MASTERY NOTE: Why oral Vit K causes warfarin resistance: when large doses "
        "are given (>5 mg), hepatic vitamin K stores are repleted beyond the warfarin "
        "inhibitory threshold. Restarting warfarin may require weeks of higher doses "
        "to re-achieve therapeutic INR. Use the minimum effective dose of Vit K to "
        "correct to a safe range while minimizing subsequent resistance.",

        'tier-high',
        _NM,
        DID['anticoagulants'],
        'warfarin_management',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "On the warfarin reversal chart, 4-factor PCC reverses INR faster than FFP. "
        "The key volume difference is 4F-PCC dose _______ mL vs FFP _______ mL "
        "for a 70 kg patient. This difference is clinically important because _______.",

        "4-Factor PCC (Kcentra): ~30–60 mL (concentrated product; dose-based)\n"
        "| FFP: ~1,000–1,400 mL for 15–20 mL/kg × 70 kg = 1,050–1,400 mL\n"
        "| Clinically important because: large FFP volume causes fluid overload, "
        "especially dangerous in patients with: heart failure (↑ pulmonary edema), "
        "renal failure (cannot excrete fluid), cirrhosis (hypoalbuminemia + portal HTN)\n"
        "→ CCRN KEY: Advantages of 4F-PCC over FFP for warfarin reversal:\n"
        "1. Volume: ~50 mL vs 1,000+ mL (less fluid overload)\n"
        "2. Onset: 15–30 min vs 1–4h (including thaw time for FFP)\n"
        "3. Efficacy: more complete INR correction\n"
        "4. No blood-type matching required (unlike FFP)\n"
        "5. No TRALI/TACO risk (unlike plasma products)\n"
        "→ MASTERY NOTE: FFP still has a role: (1) when 4F-PCC is unavailable; "
        "(2) as a plasma source in massive transfusion (ratio-based 1:1:1 protocol); "
        "(3) TTP (provides ADAMTS13 enzyme). For isolated warfarin reversal, "
        "4F-PCC should be the default when available.",

        'tier-critical',
        _NM,
        DID['anticoagulants'],
        'warfarin_management',
        '{"sel":0}',
        'chart-l3'
    ),

    # ═══ anticoagulant_reversal ════════════════════════════════════════════════
    (
        "On the reversal chart, protamine sulfate dose for UFH is _______ mg "
        "per _______ units of UFH given in the past 2–4 hours. "
        "The maximum single dose is _______ mg. "
        "The most dangerous administration complication is _______.",

        "Protamine dose: 1 mg per 100 units of UFH given in the past 2–4 hours\n"
        "| Maximum single dose: 50 mg IV (excess protamine itself has anticoagulant effects)\n"
        "| Most dangerous administration complication: hypotension and bradycardia "
        "(give slowly — max 5 mg/min); also: anaphylaxis/anaphylactoid reactions "
        "(higher risk in patients with prior protamine exposure, fish allergy, "
        "vasectomy, or NPH insulin use)\n"
        "→ CCRN KEY: UFH time-based dosing for protamine (amount given in past X hours):\n"
        "• Given ≤30 min ago: dose = total units in last 30 min\n"
        "• Given 30–60 min: reduce dose by 50%\n"
        "• Given >2h: minimal protamine needed (heparin t½ = 60–90 min)\n"
        "Protamine reverses LMWH only partially (~60%): 1 mg protamine per 1 mg enoxaparin "
        "given in past 8h; if anti-Xa still elevated, repeat 0.5 mg/1 mg enoxaparin.\n"
        "→ MASTERY NOTE: Protamine does NOT reverse fondaparinux or direct thrombin "
        "inhibitors (argatroban, bivalirudin). No structural binding site.",

        'tier-review',
        _NM,
        DID['anticoagulants'],
        'anticoagulant_reversal',
        '{"hi":0}',
        'chart-l1'
    ),
    (
        "On the reversal chart, idarucizumab (Praxbind) reverses _______ only. "
        "The dose is _______ IV given as _______. "
        "Its mechanism is _______ with affinity _______ that of thrombin.",

        "Idarucizumab reverses: DABIGATRAN only (direct thrombin inhibitor)\n"
        "| Dose: 5 g IV, given as two consecutive 2.5 g vials (IV push or infusion)\n"
        "| Mechanism: humanized monoclonal antibody fragment (Fab) that binds "
        "dabigatran with ~350× greater affinity than thrombin → completely sequesters "
        "the drug, rendering it pharmacologically inactive\n"
        "→ CCRN KEY: Idarucizumab indications: (1) life-threatening or uncontrolled "
        "bleeding on dabigatran; (2) urgent surgery requiring reversal of dabigatran. "
        "Onset: near-complete reversal within minutes. Duration: 24h. "
        "If dabigatran re-exposure needed after reversal: can restart 24h after idarucizumab.\n"
        "→ MASTERY NOTE: Dabigatran is renally cleared (80%); it accumulates in "
        "renal failure — idarucizumab is especially important for dialysis-dependent patients "
        "on dabigatran (rare but high-risk if bleeding occurs). Hemodialysis can also "
        "remove dabigatran (small volume of distribution) but takes longer than idarucizumab.",

        'tier-high',
        _NM,
        DID['anticoagulants'],
        'anticoagulant_reversal',
        '{"hi":3}',
        'chart-l2'
    ),
    (
        "On the reversal chart, andexanet alfa reverses _______ oral anticoagulants. "
        "The HIGH dose regimen applies when the last dose of rivaroxaban or apixaban "
        "was taken _______ hours ago. "
        "The high dose is _______ mg bolus followed by _______.",

        "Reverses: factor Xa inhibitors — apixaban, rivaroxaban, edoxaban\n"
        "| HIGH dose applies: rivaroxaban (any timing) OR apixaban/edoxaban taken "
        "≤7–8 hours ago (peak drug levels) OR unknown last dose timing\n"
        "| High dose regimen: 800 mg IV bolus (over 15–30 min) then 8 mg/min × 120 min infusion\n"
        "| LOW dose regimen (apixaban >8h ago): 400 mg bolus then 4 mg/min × 120 min\n"
        "→ CCRN KEY: Andexanet alfa mechanism: recombinant modified factor Xa "
        "(catalytically inactive) — acts as a decoy receptor, binding anti-Xa DOACs "
        "and sequestering them away from endogenous factor Xa. It does NOT affect "
        "INR, aPTT, or anti-IIa activity.\n"
        "→ MASTERY NOTE: Andexanet alfa limitations: (1) very expensive; "
        "(2) high thrombotic risk post-reversal (~10–15% DVT/PE at 30 days) — "
        "resume anticoagulation as soon as hemostasis achieved; "
        "(3) FDA-approved for apixaban and rivaroxaban only (edoxaban and betrixaban "
        "are off-label). 4-factor PCC (50 units/kg) is an off-label but widely used "
        "alternative when andexanet alfa is unavailable or cost-prohibitive.",

        'tier-critical',
        _NM,
        DID['anticoagulants'],
        'anticoagulant_reversal',
        '{"hi":4}',
        'chart-l3'
    ),

    # ═══ vte_prophylaxis ══════════════════════════════════════════════════════
    (
        "On the VTE prophylaxis chart, the standard ICU pharmacologic "
        "prophylaxis dose of enoxaparin is _______ mg SQ _______. "
        "The distinct therapeutic dose for confirmed DVT/PE is _______ mg/kg SQ.",

        "Prophylactic dose: 40 mg SQ DAILY (once every 24h)\n"
        "| Therapeutic dose: 1 mg/kg SQ every 12 hours (or 1.5 mg/kg SQ once daily)\n"
        "| KEY distinction: the doses are very different — 40 mg vs 70–90 mg for a "
        "70 kg patient. Incorrect dose selection (prophylactic for therapeutic indication) "
        "is a high-stakes clinical error.\n"
        "→ CCRN KEY: Enoxaparin dosing summary:\n"
        "• Prophylaxis (standard): 40 mg SQ q24h\n"
        "• High-risk prophylaxis: 40 mg SQ q12h (obesity, major trauma, orthopedic surgery)\n"
        "• DVT/PE treatment: 1 mg/kg SQ q12h OR 1.5 mg/kg SQ q24h\n"
        "• ACS/STEMI: 1 mg/kg SQ q12h (+ 30 mg IV bolus for STEMI <75 yo, CrCl >30)\n"
        "→ MASTERY NOTE: Anti-Xa monitoring for therapeutic LMWH: draw peak level "
        "4 hours after SQ injection. Therapeutic targets: q12h dosing = 0.5–1.0 IU/mL; "
        "q24h dosing = 1.0–2.0 IU/mL. Trough levels (12–24h post-dose) are less "
        "clinically standardized but may detect accumulation in renal impairment.",

        'tier-review',
        _NM,
        DID['anticoagulants'],
        'vte_prophylaxis',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the VTE prophylaxis chart, UFH is preferred over LMWH for "
        "therapeutic anticoagulation when CrCl is _______ mL/min. "
        "Two additional ICU reasons to choose UFH over LMWH are _______ and _______.",

        "UFH preferred when CrCl <30 mL/min (LMWH accumulates; avoid in severe renal failure)\n"
        "| Additional ICU reasons to choose UFH:\n"
        "1. Rapidly changing renal function (AKI progression) — LMWH dosing becomes "
        "unpredictable; UFH titratable by aPTT regardless of renal function\n"
        "2. Need for rapid reversal — protamine fully reverses UFH in 5–15 min; "
        "LMWH reversal with protamine is only 60% effective; DOACs require specific agents\n"
        "→ CCRN KEY: Additional UFH advantages in ICU: (1) Uninterrupted monitoring "
        "via continuous infusion + serial aPTTs; (2) Immediate dose adjustment; "
        "(3) No SQ injection needed (central line or IV route); "
        "(4) Traditional standard for anticoagulation in cardiac surgery.\n"
        "→ MASTERY NOTE: Despite UFH advantages, LMWH is preferred for most outpatient "
        "and lower-acuity VTE (less monitoring, once-daily SQ, predictable kinetics). "
        "In the ICU, the balance shifts toward UFH infusion when any of these risks "
        "apply. Know BOTH agents — CCRN tests the clinical decision between them.",

        'tier-high',
        _NM,
        DID['anticoagulants'],
        'vte_prophylaxis',
        '{"sel":2}',
        'chart-l2'
    ),
    (
        "On the renal adjustment chart, enoxaparin therapeutic dose must be "
        "reduced to _______ mg/kg _______ daily when CrCl is _______. "
        "Below CrCl _______ mL/min, enoxaparin should be avoided entirely.",

        "Enoxaparin therapeutic dose at CrCl 15–29: reduce to 1 mg/kg ONCE daily "
        "(instead of 1 mg/kg q12h)\n"
        "| Prophylactic dose at CrCl 15–29: reduce to 30 mg once daily "
        "(instead of 40 mg once daily)\n"
        "| Avoid enoxaparin entirely: CrCl <15 mL/min or hemodialysis (ESRD)\n"
        "→ CCRN KEY: Renal adjustment decision tree:\n"
        "CrCl ≥30: Standard dosing\n"
        "CrCl 15–29: Reduce dose + monitor anti-Xa\n"
        "CrCl <15 or HD: AVOID LMWH → use UFH\n"
        "Fondaparinux: avoid CrCl <30 (renally cleared, no reversal agent)\n"
        "DOACs: each has specific CrCl cutoffs per package insert; most "
        "contraindicated at ESRD (CrCl <15–25)\n"
        "→ MASTERY NOTE: Anti-Xa monitoring imperative at CrCl 15–29: draw peak "
        "4h post-SQ dose. For reduced-dose q24h therapeutic: target anti-Xa "
        "1.0–2.0 IU/mL. Accumulation leads to supratherapeutic levels before "
        "clinical bleeding is apparent. ICU nurses should flag patients on "
        "enoxaparin with rapidly rising creatinine for provider reassessment of "
        "anticoagulant choice.",

        'tier-critical',
        _NM,
        DID['anticoagulants'],
        'vte_prophylaxis',
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
