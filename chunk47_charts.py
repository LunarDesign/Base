#!/usr/bin/env python3
"""chunk47_charts.py — Ph8 Reference: Hemodynamic Parameters (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_46.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_47.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c47')
CHUNK_NUM   = 47
MID_BASE    = 1_800_005_080
CHART_ORDER = ['hemo_parameters', 'shock_hemodynamics', 'cardiac_output_calcs',
               'pa_catheter', 'fluid_responsiveness']

_NM = 'Ph8 · \U0001f7e1 T3 · Reference — Hemodynamic Parameters'

RF = {}

# ── Chart 1: Hemodynamic Parameter Reference Table ───────────────────────────
RF['hemo_parameters'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var params=[
        {p:'Cardiac Output',       ab:'CO',   nr:'4 – 8',     u:'L/min',         tip:'Total pumping output; CI=CO/BSA'},
        {p:'Cardiac Index',        ab:'CI',   nr:'2.2 – 4.0', u:'L/min/m²',      tip:'<2.2 low output; >4.0 hyperdynamic'},
        {p:'Stroke Volume Index',  ab:'SVI',  nr:'33 – 47',   u:'mL/beat/m²',    tip:'SVI=CI/HR×1000; contractility proxy'},
        {p:'Mean Art. Pressure',   ab:'MAP',  nr:'70 – 100',  u:'mmHg',          tip:'MAP≈DBP+⅓(PP); CPP=MAP−ICP'},
        {p:'CVP / RAP',            ab:'CVP',  nr:'2 – 8',     u:'mmHg',          tip:'RV preload; poor solo volume predictor'},
        {p:'PCWP / PAOP',          ab:'PCWP', nr:'6 – 12',    u:'mmHg',          tip:'>18 congestion; >25 pulm edema; ≈LVEDP'},
        {p:'Syst Vasc Resistance', ab:'SVR',  nr:'800–1200',  u:'dynes·s/cm⁵',   tip:'(MAP−CVP)/CO×80; ↑=vasoconstriction'},
        {p:'Pulm Vasc Resistance', ab:'PVR',  nr:'< 250',     u:'dynes·s/cm⁵',   tip:'(mPAP−PCWP)/CO×80; ↑ in pulm HTN/ARDS'},
        {p:'Mixed Venous O₂ Sat',  ab:'SvO₂', nr:'60 – 80',  u:'%',             tip:'<60%: ↑ extraction or ↓ DO₂; trend matters'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/params.length);
    var xs=[4,135,205,285,385,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Parameter','Abbrev','Normal Range','Units','Clinical Tip'];
    ctx.font='bold 8px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    params.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle='#5599dd33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle='#88bbee';ctx.font='bold 7.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(d.p,xs[0]+3,ry+rh/2+3);
        ctx.fillStyle='#66ddcc';ctx.font='bold 8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.ab,(xs[1]+xs[2])/2,ry+rh/2+3);
        ctx.fillStyle='#eedd88';ctx.font='bold 8px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.nr,(xs[2]+xs[3])/2,ry+rh/2+3);
        ctx.fillStyle='#aabbcc';ctx.font='7.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.u,(xs[3]+xs[4])/2,ry+rh/2+3);
        ctx.fillStyle='#99aabb';ctx.font='7.5px sans-serif';ctx.textAlign='left';
        var tipW=xs[5]-xs[4]-6;
        var words=d.tip.split(' ');var line='';var tipY=ry+rh/2-1;
        words.forEach(function(w){
            var test=line+w+' ';
            if(ctx.measureText(test).width>tipW&&line){
                ctx.fillText(line.trim(),xs[4]+3,tipY);line=w+' ';tipY+=9;
            }else{line=test;}
        });
        ctx.fillText(line.trim(),xs[4]+3,tipY);
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
        var lbs=['CO','CI','SVI','MAP','CVP','PCWP','SVR','PVR','SvO₂'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,'#5599dd',hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: Shock Hemodynamic Profiles ──────────────────────────────────────
RF['shock_hemodynamics'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var shocks=[
        {type:'Distributive\n(Sepsis/SIRS/Anaphylaxis)',co:'↑↑ HIGH\n(hyperdynamic)',svr:'↓↓ LOW\n(vasodilated)',pcwp:'↓ / N',cvp:'↓ / N',svo2:'↑↑ maldist.\nor ↓ late',drug:'Norepinephrine\n± Vasopressin',c:'#cc4444'},
        {type:'Cardiogenic\n(MI / HFrEF / Myocarditis)',co:'↓↓ LOW\n(pump failure)',svr:'↑↑ HIGH\n(compensatory)',pcwp:'↑↑ > 18',cvp:'↑',svo2:'↓↓ high\nextraction',drug:'Dobutamine\n± Norepinephrine',c:'#cc8844'},
        {type:'Obstructive\n(PE / Tamponade / PTX)',co:'↓↓ LOW\n(outflow block)',svr:'↑↑ HIGH\n(compensatory)',pcwp:'↓ / N*',cvp:'↑↑ > 10',svo2:'↓ low\ndelivery',drug:'Treat cause\n(lytics/drain/needle)',c:'#4488cc'},
        {type:'Hypovolemic\n(Hemorrhage / Burns / GI)',co:'↓↓ LOW\n(↓ preload)',svr:'↑↑ HIGH\n(compensatory)',pcwp:'↓↓ < 6',cvp:'↓↓ < 2',svo2:'↓ high\nextraction',drug:'IVF / pRBCs\n+ source control',c:'#3a9a5c'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=20, rh=Math.floor((H-hdrH)/shocks.length);
    var xs=[4,115,185,255,315,375,450,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Shock Type','CO/CI','SVR','PCWP','CVP','SvO₂','First-line Rx'];
    ctx.font='bold 8px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    var cols=['co','svr','pcwp','cvp','svo2','drug'];
    var clrs=['#eedd88','#cc8844','#cc6666','#88aacc','#44aacc','#aabbaa'];
    shocks.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=d.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=d.c;ctx.font='bold 7.5px sans-serif';ctx.textAlign='left';
        d.type.split('\n').forEach(function(l,li){ctx.fillText(l,xs[0]+3,ry+rh/2-5+li*10);});
        cols.forEach(function(k,ci){
            ctx.fillStyle=clrs[ci];ctx.font='7.5px sans-serif';ctx.textAlign='center';
            var cx=(xs[ci+1]+xs[ci+2])/2;
            d[k].split('\n').forEach(function(l,li){ctx.fillText(l,cx,ry+rh/2-4+li*9);});
        });
        ctx.globalAlpha=1;
        ctx.strokeStyle='#222';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(0,ry+rh);ctx.lineTo(W,ry+rh);ctx.stroke();
    });
    [xs[1],xs[2],xs[3],xs[4],xs[5],xs[6]].forEach(function(x){
        ctx.strokeStyle='#222';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(x,hdrH);ctx.lineTo(x,H);ctx.stroke();
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        var lbs=['Distributive','Cardiogenic','Obstructive','Hypovolemic'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,shocks[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 3: Cardiac Output Calculations ─────────────────────────────────────
RF['cardiac_output_calcs'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Thermodilution (PA Cath)','Fick Equation','Derived Parameters'];
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
    var lm=14, ly=panelY+16;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#88bbee';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+170,ly);}
        ly+=14;
    }
    function nt(t){ctx.fillStyle='#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=12;}
    function hr(){ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=6;}
    if(sel===0){
        rw('Method:','Thermodilution via PA catheter');
        nt('Inject cold saline into RA port → measure temp change at PA thermistor');
        hr();
        rw('Principle:','Stewart-Hamilton equation');
        nt('CO inversely proportional to area under the temp-time curve');
        nt('Smaller area (rapid temp return) = higher CO; larger area = lower CO');
        hr();
        rw('Normal CO:','4–8 L/min','#66ddcc','#eedd88');
        rw('Normal CI:','2.2–4.0 L/min/m²','#66ddcc','#eedd88');
        rw('Normal SV:','60–100 mL/beat','#66ddcc','#eedd88');
        hr();
        nt('Limitation: inaccurate with tricuspid regurgitation, shunts, arrhythmias');
        nt('Repeat ×3 and average; avoid during rapid fluid infusion or temperature changes');
    } else if(sel===1){
        rw('Fick Equation:','CO = VO₂ ÷ (CaO₂ − CvO₂) × 10','#66ddcc','#eedd88');
        hr();
        rw('VO₂ (O₂ consumption):','~125 mL/min/m² at rest','#aabb88','#eedd88');
        rw('CaO₂ =','Hgb × 1.34 × SaO₂ + 0.003 × PaO₂','#aab','#bbb');
        rw('CvO₂ =','Hgb × 1.34 × SvO₂ + 0.003 × PvO₂','#aab','#bbb');
        hr();
        rw('Normal A-vDO₂:','3.5–5.5 mL/dL','#aabb88','#eedd88');
        nt('↑ A-vDO₂ (>5.5): low CO — tissues extracting more O₂ (cardiogenic shock)');
        nt('↓ A-vDO₂ (<3.5): maldistribution — cells cannot use O₂ (distributive shock)');
        hr();
        rw('SvO₂ < 60%:','↑ extraction or ↓ delivery → shock state','#cc6666','#ffaa88');
        rw('SvO₂ > 80%:','Maldistribution or ↓ O₂ consumption (sepsis early)','#44aacc','#88ddff');
    } else {
        rw('Cardiac Index:','CI = CO / BSA [Normal: 2.2–4.0 L/min/m²]','#66ddcc','#eedd88');
        hr();
        rw('SVR:','(MAP − CVP) / CO × 80','#cc8844','#eedd88');
        rw('Normal SVR:','800–1200 dynes·s/cm⁵','#aab','#eedd88');
        nt('↑ SVR: vasoconstriction (cardiogenic, hypovolemic, obstructive shock)');
        nt('↓ SVR: vasodilation (distributive/septic shock, anaphylaxis)');
        hr();
        rw('PVR:','(mPAP − PCWP) / CO × 80','#4488cc','#eedd88');
        rw('Normal PVR:','< 250 dynes·s/cm⁵','#aab','#eedd88');
        nt('↑ PVR: pulmonary HTN, PE, ARDS, hypoxic vasoconstriction');
        hr();
        rw('DO₂ (O₂ Delivery):','CO × CaO₂ × 10 [Normal: 900–1100 mL/min]','#aabb88','#eedd88');
        nt('Critical DO₂ ≈ 300 mL/min/m² — below this: O₂ consumption becomes delivery-dependent');
        nt('Markers of critical threshold: ↑ lactate, ↓ SvO₂, ↑ A-vDO₂');
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

# ── Chart 4: PA Catheter Pressure Zones ──────────────────────────────────────
RF['pa_catheter'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var zones=[
        {zone:'Right Atrium\n(RA / CVP)',   sys:'2–8',   dia:'2–8',
         wf:'a wave (atrial contraction)\nx descent (AV valve open)\nv wave (venous filling)',
         clue:'↑ CVP: RHF, fluid overload, TR\nPEEP can falsely ↑ CVP\nKussmaul sign: ↑ JVP with inspiration',c:'#4488cc'},
        {zone:'Right Ventricle\n(RV)',        sys:'15–30', dia:'0–8',
         wf:'Tall systolic peak\nNo dicrotic notch\nDiastolic = RA pressure',
         clue:'RV sys ↑: pulm HTN, PE, ARDS\nRV sys = PA sys (via pulmonic valve)\nRV diastolic = CVP when TV open',c:'#3a9a5c'},
        {zone:'Pulmonary Artery\n(PA)',        sys:'15–30', dia:'6–12',
         wf:'Dicrotic notch (pulmonic\nvalve closure at end-systole)\nSmooth systolic upstroke',
         clue:'PA diastolic ≈ PCWP if PVR normal\nPA sys > 30: pulmonary HTN\nPA diastolic−PCWP >5: ↑ PVR',c:'#cc8844'},
        {zone:'PCWP / Wedge\n(PAOP)',          sys:'6–12',  dia:'6–12',
         wf:'a wave (LA contraction)\nc wave (mitral valve closure)\nv wave (LA passive filling)',
         clue:'Large v wave → mitral regurgitation\n>18: pulm congestion; >25: edema\nEqualization (all ≈15): tamponade',c:'#cc4444'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/zones.length);
    var xs=[4,115,165,215,385,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['PA Cath Zone','Sys','Dia','Waveform Features','Clinical Significance'];
    ctx.font='bold 7.5px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    zones.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=d.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=d.c;ctx.font='bold 7.5px sans-serif';ctx.textAlign='left';
        d.zone.split('\n').forEach(function(l,li){ctx.fillText(l,xs[0]+3,ry+rh/2-5+li*10);});
        ctx.fillStyle='#eedd88';ctx.font='bold 8px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.sys,(xs[1]+xs[2])/2,ry+rh/2+3);
        ctx.fillStyle='#aabb88';ctx.font='bold 8px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.dia,(xs[2]+xs[3])/2,ry+rh/2+3);
        ctx.fillStyle='#88aabb';ctx.font='7.5px sans-serif';ctx.textAlign='left';
        d.wf.split('\n').forEach(function(l,li){ctx.fillText(l,xs[3]+3,ry+rh/2-8+li*9);});
        ctx.fillStyle='#99bbaa';ctx.font='7.5px sans-serif';ctx.textAlign='left';
        d.clue.split('\n').forEach(function(l,li){ctx.fillText(l,xs[4]+3,ry+rh/2-8+li*9);});
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
        var lbs=['RA','RV','PA','PCWP/Wedge'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,zones[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 5: Fluid Responsiveness Assessment ─────────────────────────────────
RF['fluid_responsiveness'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Dynamic Predictors','Passive Leg Raise (PLR)','Fluid Challenge Protocol'];
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
    var lm=14, ly=panelY+14;
    function ln(label,val,c1,c2){
        ctx.fillStyle=c1||'#88bbee';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+195,ly);}
        ly+=13;
    }
    function nt(t){ctx.fillStyle='#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        ln('PPV (Pulse Pressure Variation):','> 13% = fluid responsive','#66ddcc','#eedd88');
        nt('Requires: controlled MV, sinus rhythm, VT ≥8 mL/kg, no significant RV failure');
        hr();
        ln('SVV (Stroke Volume Variation):','> 10–13% = fluid responsive','#66ddcc','#eedd88');
        nt('Same requirements as PPV; SVV preferred with LVAD or significant aortic regurgitation');
        hr();
        ln('IVC Collapsibility (spont. breathing):','> 50% = likely responsive','#aabb88','#eedd88');
        nt('Caval index = (IVCmax − IVCmin) / IVCmax × 100%');
        hr();
        ln('IVC Distensibility (mech. ventilation):','> 12% = likely responsive','#aabb88','#eedd88');
        nt('Distensibility = (IVCmax − IVCmin) / IVCmin × 100%');
        hr();
        nt('★ PPV/SVV INVALID with: spontaneous breathing, arrhythmias, open chest,');
        nt('  abdominal compartment syndrome, low tidal volume ARDS ventilation, RV failure');
    } else if(sel===1){
        ln('PLR — Passive Leg Raise:','Endogenous fluid challenge (~300 mL)','#66ddcc','#eedd88');
        hr();
        ln('Technique:');
        nt('Start: HOB at 30–45°, patient in semi-recumbent position');
        nt('Maneuver: lower HOB flat, raise legs to 45° for 30–90 seconds');
        nt('Autotransfusion ≈ 300 mL from venous reservoir in legs/splanchnic bed');
        hr();
        ln('Positive response:','≥ 10% increase in CO or stroke volume','#3a9a5c','#aaddaa');
        nt('Must measure CO/SV directly (Doppler, PA catheter, NICOM, arterial PP)');
        nt('BP change alone is insufficient — SV may increase without BP change');
        hr();
        ln('Advantages:');
        nt('★ Valid during: spontaneous breathing, arrhythmias, ARDS, RV failure, open abdomen');
        nt('★ Fully reversible — return legs to flat; no volume administered, no risk');
        hr();
        nt('Contraindications: ↑ ICP, unstable spine/pelvis, severe GERD in flat position');
    } else {
        ln('Fluid Challenge:','250–500 mL crystalloid over 15–30 min','#66ddcc','#eedd88');
        hr();
        ln('Responder criteria (positive):');
        nt('↑ CI ≥10–15% OR ↑ MAP ≥10 mmHg OR ↑ SV ≥10% after bolus');
        hr();
        ln('Non-responder / Stop criteria:');
        nt('No improvement in CI/MAP after 2 sequential challenges → stop fluid loading');
        nt('Rising PCWP >18 mmHg, worsening SpO₂, or signs of pulmonary edema → stop');
        hr();
        ln('Balanced crystalloid preferred:');
        nt('SMART trial: LR or PlasmaLyte vs NS → ↓ AKI, ↓ MAKE30 composite endpoint');
        nt('ROSE trial: conservative fluid after initial resuscitation → ↓ renal injury, ↓ MV');
        hr();
        nt('★ Liberal fluids risk: AKI (renal venous congestion), resp failure, abdominal compartment');
        nt('★ Target euvolemia once resuscitation goals met — reassess with each challenge');
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

# ── Cards ─────────────────────────────────────────────────────────────────────
CARDS = [
    # ═══ hemo_parameters ══════════════════════════════════════════════════════
    (
        "On the hemodynamic parameters reference chart, normal Cardiac Index (CI) "
        "is _______ L/min/m². A CI below _______ L/min/m² defines low cardiac output "
        "state, which drives compensatory _______ (elevated SVR) to maintain MAP.",

        "Normal CI: 2.2–4.0 L/min/m²\n"
        "| CI < 2.2: low output state → compensatory vasoconstriction (↑ SVR)\n"
        "| CI > 4.0: hyperdynamic state (distributive shock, thyrotoxicosis, fever)\n"
        "| CI normalizes CO for body size: CO / BSA (m²) → comparable across patients\n"
        "→ CCRN KEY: Cardiogenic shock criteria: CI < 2.2 L/min/m² AND PCWP > 18 mmHg. "
        "Both criteria required — low CI alone may reflect hypovolemia (PCWP will be low).\n"
        "→ MASTERY NOTE: SVI = CI / HR × 1000. Normal SVI 33–47 mL/beat/m². "
        "↓ SVI with ↑ HR = compensated; ↓ SVI with ↓ HR = decompensated (bradycardia + poor contractility).",

        'tier-review',
        _NM,
        DID['hemo_parameters'],
        'hemo_parameters',
        '{"hi":1}',
        'chart-l1'
    ),
    (
        "The hemo parameters chart shows SVR is calculated as: "
        "SVR = (_______ − _______) ÷ _______ × 80. "
        "Normal range is _______ dynes·s/cm⁵. "
        "An SVR below _______ indicates pathologic _______.",

        "SVR = (MAP − CVP) / CO × 80 dynes·s/cm⁵\n"
        "| Normal SVR: 800–1200 dynes·s/cm⁵\n"
        "| SVR < 800: pathologic vasodilation → distributive/septic shock\n"
        "| SVR > 1200: vasoconstriction → cardiogenic, hypovolemic, or obstructive shock\n"
        "→ CCRN KEY: SVR × CO = MAP (simplified). In low CO states, ↑ SVR maintains MAP — "
        "but at the cost of ↓ tissue perfusion (↑ afterload impairs SV further).\n"
        "→ MASTERY NOTE: In septic shock, NorEpi is used to ↑ SVR back toward normal (800+). "
        "Target MAP ≥65 mmHg. SVR alone does not tell you why it's low — need clinical context.",

        'tier-high',
        _NM,
        DID['hemo_parameters'],
        'hemo_parameters',
        '{"hi":6}',
        'chart-l2'
    ),
    (
        "On the reference chart, normal PCWP is _______ mmHg. "
        "PCWP > _______ mmHg indicates moderate pulmonary congestion, "
        "and PCWP > _______ mmHg indicates frank pulmonary edema. "
        "PCWP estimates _______ pressure.",

        "Normal PCWP: 6–12 mmHg\n"
        "| PCWP 12–18: mild-to-moderate pulmonary congestion\n"
        "| PCWP 18–25: moderate congestion → pulmonary edema threshold\n"
        "| PCWP > 25: frank pulmonary edema (fluid floods alveoli)\n"
        "| PCWP estimates LVEDP (left ventricular end-diastolic pressure)\n"
        "→ CCRN KEY: PCWP > 18 + CI < 2.2 = cardiogenic shock profile. "
        "Treatment: diuresis (↓ PCWP) + inotrope (↑ CI). "
        "Vasopressor alone worsens cardiogenic shock by ↑ SVR (more afterload on failing LV).\n"
        "→ MASTERY NOTE: PCWP may UNDERESTIMATE LVEDP in aortic stenosis, LV hypertrophy "
        "(stiff LV), or mitral stenosis. PCWP may OVERESTIMATE LVEDP with high PEEP → "
        "subtract ~50% of applied PEEP above 5 cmH₂O from measured PCWP.",

        'tier-critical',
        _NM,
        DID['hemo_parameters'],
        'hemo_parameters',
        '{"hi":5}',
        'chart-l3'
    ),

    # ═══ shock_hemodynamics ═══════════════════════════════════════════════════
    (
        "The shock hemodynamics chart shows distributive shock (sepsis) presents with "
        "_______ CO/CI, _______ SVR, and _______ SvO2 — due to _______ "
        "of blood flow causing functional cellular hypoxia despite high output.",

        "CO/CI: ↑↑ HIGH (hyperdynamic — ↑ HR + ↓ SVR drives CO up early)\n"
        "| SVR: ↓↓ LOW (profound vasodilation from inflammatory mediators, NO)\n"
        "| SvO₂: ↑↑ elevated (maldistribution — blood bypasses capillaries → cells can't extract O₂)\n"
        "| Late/refractory sepsis: myocardial depression → ↓ CO + ↓ SvO₂ (dual failure)\n"
        "→ CCRN KEY: Septic shock first-line: norepinephrine 0.01–0.5 mcg/kg/min to ↑ SVR "
        "and restore MAP ≥65 mmHg. Add vasopressin 0.03–0.04 units/min as second agent "
        "(catecholamine-sparing). Dobutamine only if concurrent myocardial depression (CI < 2.2).\n"
        "→ MASTERY NOTE: SvO₂ > 70% in early sepsis = maldistribution (not normal O₂ delivery). "
        "ScvO₂ (central) >70% used as resuscitation target in ProCESS/ARISE/ProMISe trials.",

        'tier-review',
        _NM,
        DID['hemo_parameters'],
        'shock_hemodynamics',
        '{"hi":0}',
        'chart-l1'
    ),
    (
        "On the shock chart, cardiogenic shock is distinguished from hypovolemic shock "
        "by _______ PCWP (> _______ mmHg) and _______ SVR — indicating pump "
        "failure with backward _______ congestion and high compensatory _______.",

        "PCWP: ↑↑ HIGH (> 18 mmHg) — backward failure → pulmonary venous congestion\n"
        "| SVR: ↑↑ HIGH — compensatory vasoconstriction (body tries to maintain MAP)\n"
        "| CO/CI: ↓↓ LOW — forward failure (↓ CO from pump dysfunction)\n"
        "| SvO₂: ↓↓ LOW — tissues maximally extracting O₂ due to low delivery\n"
        "| Hypovolemic shock: ↓↓ PCWP + ↓↓ CVP distinguishes from cardiogenic (↑ PCWP)\n"
        "→ CCRN KEY: Cardiogenic shock Rx: dobutamine (↑ contractility, ↓ SVR) ± norepinephrine "
        "(if MAP < 65). Diuresis if severely congested (↑ PCWP → pulmonary edema). "
        "Intra-aortic balloon pump (IABP) → ↓ SVR + ↑ coronary perfusion in MI-related CS.\n"
        "→ MASTERY NOTE: Cold/wet vs warm/wet: cold = ↓ CO + ↑ SVR (classic cardiogenic); "
        "warm = ↓ CO + ↓ SVR (vasodilatory cardiogenic — often requires both inotrope + vasoconstrictor).",

        'tier-high',
        _NM,
        DID['hemo_parameters'],
        'shock_hemodynamics',
        '{"hi":1}',
        'chart-l2'
    ),
    (
        "The shock chart shows obstructive shock (massive PE, tamponade) presents with "
        "_______ CO, _______ CVP, and _______ / normal PCWP — "
        "distinguishing it from hypovolemic shock by elevated _______ despite low output.",

        "CO: ↓↓ LOW — outflow obstruction blocks forward flow\n"
        "| CVP: ↑↑ HIGH (>10 mmHg) — venous back-pressure from obstruction\n"
        "| PCWP: ↓ or normal — unlike cardiogenic shock (low forward → low PCWP)\n"
        "| Key distinguisher from hypovolemic: ↑↑ CVP (vs ↓↓ CVP in hypovolemia)\n"
        "| Tamponade: pressure equalization of RA/RV diastolic/PA diastolic/PCWP (all ≈15–20)\n"
        "→ CCRN KEY: Massive PE Rx: systemic lytics (alteplase 100 mg IV × 2h) if BP <90 mmHg "
        "or hemodynamic collapse. Avoid fluid boluses (RV is already dilated and overloaded). "
        "Cardiac tamponade Rx: pericardiocentesis (needle or surgical window).\n"
        "→ MASTERY NOTE: Beck's triad of tamponade: hypotension + JVD (↑ CVP) + muffled heart sounds. "
        "Pulsus paradoxus (>10 mmHg BP drop with inspiration) is pathognomonic of tamponade.",

        'tier-critical',
        _NM,
        DID['hemo_parameters'],
        'shock_hemodynamics',
        '{"hi":2}',
        'chart-l3'
    ),

    # ═══ cardiac_output_calcs ═════════════════════════════════════════════════
    (
        "The cardiac output calculations chart shows the Fick equation: "
        "CO = _______ ÷ (CaO2 − CvO2) × 10. "
        "Normal resting VO2 is _______ mL/min/m², "
        "and normal arteriovenous O2 difference (A-vDO2) is _______ mL/dL.",

        "Fick equation: CO = VO₂ / (CaO₂ − CvO₂) × 10\n"
        "| Normal VO₂: ~125 mL/min/m² at rest\n"
        "| Normal A-vDO₂: 3.5–5.5 mL/dL\n"
        "| CaO₂ = (Hgb × 1.34 × SaO₂) + (0.003 × PaO₂)\n"
        "| CvO₂ = (Hgb × 1.34 × SvO₂) + (0.003 × PvO₂)\n"
        "→ CCRN KEY: At rest with normal CO (~5 L/min) and VO₂ 125 mL/min/m²: "
        "A-vDO₂ = 125 / 5 × 10 = 4.5 mL/dL → SvO₂ ≈ 70–75% (normal extraction ratio ~25%).\n"
        "→ MASTERY NOTE: Fick is MOST accurate in low CO states (more reliable than thermodilution). "
        "Thermodilution underestimates CO with tricuspid regurgitation — the backflow 'cools' "
        "the thermistor before the true signal passes, falsely widening the temp-time curve.",

        'tier-review',
        _NM,
        DID['hemo_parameters'],
        'cardiac_output_calcs',
        '{"sel":1}',
        'chart-l1'
    ),
    (
        "On the derived parameters chart, SVR formula is "
        "(_______ − _______) ÷ _______ × 80, and PVR formula is "
        "(_______ − _______) ÷ _______ × 80. "
        "Normal SVR is _______ and normal PVR is _______.",

        "SVR = (MAP − CVP) / CO × 80 [Normal: 800–1200 dynes·s/cm⁵]\n"
        "| PVR = (mPAP − PCWP) / CO × 80 [Normal: < 250 dynes·s/cm⁵]\n"
        "| SVR reflects systemic afterload (LV workload)\n"
        "| PVR reflects pulmonary afterload (RV workload)\n"
        "→ CCRN KEY: ↑ PVR (>250): pulmonary arterial hypertension, PE, ARDS, hypoxic vasoconstriction. "
        "RV cannot sustain high PVR long-term → RV failure → ↑ CVP + ↓ CO (right heart syndrome).\n"
        "→ MASTERY NOTE: PA diastolic − PCWP gradient: when >5 mmHg, suggests intrinsic pulmonary "
        "vascular disease (not simply elevated pulmonary venous pressure from left heart failure). "
        "Normal: PA diastolic ≈ PCWP (pulmonary vasculature has negligible resistance at rest).",

        'tier-high',
        _NM,
        DID['hemo_parameters'],
        'cardiac_output_calcs',
        '{"sel":2}',
        'chart-l2'
    ),
    (
        "The calculations chart shows oxygen delivery: DO2 = _______ × _______ × 10. "
        "When DO2 falls below ~_______ mL/min/m², anaerobic metabolism begins — "
        "signaled by rising _______ and falling SvO2.",

        "DO₂ = CO × CaO₂ × 10 [Normal total: 900–1100 mL/min]\n"
        "| Critical DO₂ threshold: ~300 mL/min/m²\n"
        "| Below critical threshold: O₂ consumption (VO₂) becomes delivery-dependent\n"
        "| Anaerobic markers: ↑ lactate (>2 mmol/L), ↓ SvO₂ (<60%), ↑ A-vDO₂ (>5.5)\n"
        "→ CCRN KEY: Normal O₂ extraction ratio (OER) = VO₂/DO₂ ≈ 25% (SvO₂ ≈ 75%). "
        "In shock: OER ↑ to 50–70% as tissues extract more (SvO₂ ↓ to 30–50%). "
        "Lactate > 2 mmol/L with ↓ SvO₂ = inadequate DO₂ → escalate support.\n"
        "→ MASTERY NOTE: Anemia dramatically reduces CaO₂ and DO₂: "
        "Hgb 7 g/dL → CaO₂ ≈ 9.4 mL/dL vs Hgb 14 → CaO₂ ≈ 18.8 mL/dL. "
        "Transfusion target in shock: maintain Hgb ≥7–8 g/dL (TRICC trial); "
        "higher threshold (≥8–9) in active cardiac ischemia or cardiogenic shock.",

        'tier-critical',
        _NM,
        DID['hemo_parameters'],
        'cardiac_output_calcs',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ pa_catheter ══════════════════════════════════════════════════════════
    (
        "On the PA catheter pressure chart, normal RV systolic pressure is _______ mmHg "
        "and equals _______ systolic — because the _______ valve lies between them. "
        "Normal PA diastolic is _______ mmHg.",

        "Normal RV systolic: 15–30 mmHg\n"
        "| RV systolic = PA systolic (15–30 mmHg) via the pulmonic valve\n"
        "| Pulmonic valve: separates RV and PA; opens in systole, closes at end-systole\n"
        "| Normal PA diastolic: 6–12 mmHg\n"
        "| RV diastolic (0–8 mmHg) ≠ PA diastolic — pulmonic valve closure separates them\n"
        "→ CCRN KEY: If PA systolic > 30 mmHg: pulmonary hypertension. "
        "Etiology: left HF (↑ PCWP → reactive pulm HTN), PE, ARDS, or primary pulm HTN. "
        "PA systolic = RV systolic only in the absence of pulmonic stenosis.\n"
        "→ MASTERY NOTE: Thermodilution CO requires passing catheter to PA (wedge position). "
        "Waveform confirmation: RA (low flat a/v waves) → RV (tall systolic peak) → "
        "PA (systolic peak + dicrotic notch) → PCWP (smaller a/v waves, phasic).",

        'tier-review',
        _NM,
        DID['hemo_parameters'],
        'pa_catheter',
        '{"hi":2}',
        'chart-l1'
    ),
    (
        "The PA catheter chart shows PA diastolic pressure (_______ mmHg) "
        "closely approximates _______ when PVR is normal and HR < _______. "
        "A PA diastolic − PCWP gradient > _______ mmHg suggests elevated _______.",

        "Normal PA diastolic: 6–12 mmHg\n"
        "| PA diastolic ≈ PCWP (6–12 mmHg) when PVR is normal and HR < 100\n"
        "| PA diastolic is useful as PCWP/LVEDP surrogate when wedge is not obtainable\n"
        "| PA diastolic − PCWP gradient > 5 mmHg = ↑ PVR (pulmonary vascular disease)\n"
        "| Tachycardia: less diastolic filling time → PA diastolic may overestimate PCWP\n"
        "→ CCRN KEY: Clinical implication: if PA diastolic rises but PCWP is normal, "
        "suspect intrinsic pulmonary vascular disease (PE, primary pulm HTN, ARDS) — "
        "not just left heart failure (which would raise both equally).\n"
        "→ MASTERY NOTE: Cannot obtain PCWP (catheter will not wedge): "
        "use PA diastolic as proxy IF no clinical evidence of ↑ PVR. "
        "If PEEP is high (>10 cmH₂O), measured PCWP is falsely elevated — "
        "temporarily reduce PEEP to 5 cmH₂O or correct: true PCWP ≈ measured − 50% excess PEEP.",

        'tier-high',
        _NM,
        DID['hemo_parameters'],
        'pa_catheter',
        '{"hi":2}',
        'chart-l2'
    ),
    (
        "On the PA catheter chart, a large _______ wave on the PCWP tracing suggests "
        "mitral regurgitation. Normal PCWP waveform has _______ waves (LA contraction) "
        "and _______ waves (passive LA filling). Pressure equalization of all cardiac "
        "chambers at _______ mmHg suggests _______.",

        "Large 'v' wave on PCWP: mitral regurgitation (systolic back-flow into LA → giant v)\n"
        "| 'a' waves: left atrial contraction (presystolic); absent in atrial fibrillation\n"
        "| 'v' waves: passive LA filling during ventricular systole\n"
        "| Large 'a' wave: mitral stenosis or severe LV noncompliance\n"
        "| Pressure equalization (all chambers ≈15–20 mmHg): cardiac tamponade\n"
        "→ CCRN KEY: Tamponade hemodynamic hallmark: RA = RV diastolic = PA diastolic = PCWP "
        "(all equalize ≈15–20 mmHg). This pattern + pulsus paradoxus = tamponade until proven otherwise. "
        "Treatment: immediate pericardiocentesis; avoid vasodilators (will cause cardiovascular collapse).\n"
        "→ MASTERY NOTE: 'c' wave: mitral valve closure (small, often not visible). "
        "Constrictive pericarditis: equalization of pressures + square root sign on RV tracing "
        "(dip-plateau pattern). Distinguished from tamponade by echocardiography.",

        'tier-critical',
        _NM,
        DID['hemo_parameters'],
        'pa_catheter',
        '{"hi":3}',
        'chart-l3'
    ),

    # ═══ fluid_responsiveness ═════════════════════════════════════════════════
    (
        "The fluid responsiveness chart shows PPV > _______ % predicts preload responsiveness. "
        "PPV is INVALID when patients breathe _______, have _______ rhythm, "
        "or receive tidal volumes below _______ mL/kg.",

        "PPV > 13%: fluid responsive (preload-dependent state)\n"
        "| INVALID with: spontaneous breathing (any effort invalidates PPV)\n"
        "| INVALID with: arrhythmias (irregular rhythm → irregular ΔPP)\n"
        "| INVALID with: tidal volume < 8 mL/kg (ARDS low-VT ventilation → false positives)\n"
        "| INVALID with: significant RV dysfunction, open chest, abdominal HTN\n"
        "→ CCRN KEY: PPV mechanism: during controlled MV, inspiration ↑ intrathoracic pressure "
        "→ ↓ RV preload → ↓ LV preload ~2 beats later → ↓ pulse pressure during inspiration. "
        "If LV is on the steep part of the Frank-Starling curve (preload-dependent), "
        "this cycling is exaggerated (large ΔPP = high PPV).\n"
        "→ MASTERY NOTE: ARDS patients on 6 mL/kg: PPV > 13% is common even in non-responders "
        "(low VT causes PPV by mechanical effect, not preload-dependence). "
        "Use PLR or mini-fluid challenge with CO monitoring instead.",

        'tier-review',
        _NM,
        DID['hemo_parameters'],
        'fluid_responsiveness',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the fluid responsiveness chart, passive leg raise is performed by elevating legs "
        "to _______ degrees, producing ~_______ mL autotransfusion. "
        "A _______ % increase in _______ confirms response. "
        "PLR is valid even with _______ breathing.",

        "Elevate legs to 45° (lower HOB flat from semi-recumbent position)\n"
        "| Autotransfusion: ~300 mL from venous reservoir in legs + splanchnic bed\n"
        "| Positive response: ≥10% increase in CO or stroke volume\n"
        "| Must measure CO/SV directly — arterial pulse pressure, Doppler, PA catheter\n"
        "| Valid with: spontaneous breathing, arrhythmias, ARDS, RV failure, low-VT ventilation\n"
        "→ CCRN KEY: PLR is the preferred dynamic test for most ICU patients because the majority "
        "are breathing spontaneously or have arrhythmias that invalidate PPV/SVV. "
        "Effect lasts 60–90 seconds — measure CO during maneuver, not after returning to baseline.\n"
        "→ MASTERY NOTE: PLR mimics a 300 mL fluid challenge but is completely reversible. "
        "A positive PLR tells you to give fluid; a negative PLR (no CO response) tells you not to — "
        "without any actual fluid having been given. This is its core advantage over an actual bolus.",

        'tier-high',
        _NM,
        DID['hemo_parameters'],
        'fluid_responsiveness',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The fluid responsiveness chart shows IVC collapsibility > _______ % during "
        "_______ breathing predicts responsiveness. "
        "IVC distensibility > _______ % during mechanical ventilation predicts responsiveness. "
        "The ROSE trial showed _______ fluid strategy after resuscitation reduces AKI.",

        "IVC collapsibility > 50%: spontaneous breathing → fluid responsive\n"
        "| Collapsibility index = (IVCmax − IVCmin) / IVCmax × 100%\n"
        "| IVC distensibility > 12%: mechanical ventilation → fluid responsive\n"
        "| Distensibility = (IVCmax − IVCmin) / IVCmin × 100%\n"
        "| ROSE trial: conservative (restrictive) fluid strategy after initial resuscitation → ↓ AKI\n"
        "→ CCRN KEY: Large IVC (> 2.1 cm) with < 50% collapsibility = volume overloaded or "
        "non-responder. Small IVC (< 1.5 cm) with > 50% collapse = likely hypovolemic and responsive. "
        "Neither threshold is absolute — use in combination with clinical assessment.\n"
        "→ MASTERY NOTE: SMART trial: balanced crystalloid (LR or PlasmaLyte) vs normal saline "
        "→ LR/PlasmaLyte reduces MAKE30 (major adverse kidney events at 30 days) by 1.1%. "
        "Normal saline: hyperchloremic metabolic acidosis + renal afferent arteriole vasoconstriction "
        "→ ↓ GFR → ↑ AKI risk with large volumes. Use NS primarily for hyponatremia correction.",

        'tier-critical',
        _NM,
        DID['hemo_parameters'],
        'fluid_responsiveness',
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
