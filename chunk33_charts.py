#!/usr/bin/env python3
"""chunk33_charts.py — Ph7 Pharmacology: vasopressor_dose_response, action_potential,
vaughan_williams, anticoag_cascade, analgesic_ladder"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_32.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_33.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c33')
CHUNK_NUM   = 33
MID_BASE    = 1_800_005_010
CHART_ORDER = ['vasopressor_dose_response',
               'action_potential',
               'vaughan_williams',
               'anticoag_cascade',
               'analgesic_ladder']

RF = {}

# ── Chart 1: Vasopressor dose-receptor shift ──────────────────────────────────
RF['vasopressor_dose_response'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;
    var mx=62, my=18, pw=W-mx-16, ph=H-my-56;
    var xD=10, yD=100;

    var DATA = {
        'Dopamine': {
            col:_OR,
            note:'1-3 = DA  |  3-10 = β1  |  >10 = α1 dominant',
            a1:[[0,2],[3,8],[5,25],[7,55],[10,90]],
            b1:[[0,5],[2,35],[4,65],[6,70],[8,50],[10,30]]
        },
        'Norepinephrine': {
            col:_RE,
            note:'Predominantly α1 + moderate β1 across all clinical doses',
            a1:[[0,70],[5,82],[10,88]],
            b1:[[0,25],[5,33],[10,35]]
        },
        'Epinephrine': {
            col:_AM,
            note:'Low (<0.1): β1 dominant → High (>0.2 mcg/kg/min): α1+β1',
            a1:[[0,8],[3,18],[6,55],[8,78],[10,90]],
            b1:[[0,78],[3,85],[6,80],[8,68],[10,58]]
        },
        'Phenylephrine': {
            col:_PU,
            note:'Pure α1 agonist — no β receptor activity (reflex bradycardia)',
            a1:[[0,82],[5,88],[10,92]],
            b1:[[0,2],[5,2],[10,2]]
        }
    };

    var drug = P.drug || 'Dopamine';

    function interp(pts, x) {
        if (x<=pts[0][0]) return pts[0][1];
        if (x>=pts[pts.length-1][0]) return pts[pts.length-1][1];
        for (var i=0;i<pts.length-1;i++) {
            if (x>=pts[i][0]&&x<=pts[i+1][0]) {
                var t=(x-pts[i][0])/(pts[i+1][0]-pts[i][0]);
                return pts[i][1]+t*(pts[i+1][1]-pts[i][1]);
            }
        }
        return 0;
    }

    function draw() {
        _cl(ctx, W, H);
        var d=DATA[drug];
        _gd(ctx,mx,my,pw,ph,2,xD,20,yD);
        _ax(ctx,mx,my,pw,ph);

        ctx.textAlign='right';
        for (var y=0;y<=yD;y+=20)
            _lb(ctx,y+'%',mx-5,my+ph-(y/yD)*ph+4,null,9);
        _rl(ctx,'Receptor Activity',13,my+ph/2);

        ctx.textAlign='center';
        for (var x=0;x<=xD;x+=2)
            _lb(ctx,x,mx+(x/xD)*pw,my+ph+15,null,9);
        _lb(ctx,'Dose (relative: low → high)',mx+pw/2,H-5,null,10);

        var d2=DATA[drug];
        _crv(ctx,function(x){return interp(d2.a1,x);},0,xD,mx,my,pw,ph,xD,yD,_RE,2.5);
        _crv(ctx,function(x){return interp(d2.b1,x);},0,xD,mx,my,pw,ph,xD,yD,_TE,2.5);

        ctx.fillStyle=d.col; ctx.font='bold 12px sans-serif'; ctx.textAlign='left';
        ctx.fillText(drug,mx+6,my+16);

        ctx.font='9px sans-serif'; ctx.fillStyle='#777'; ctx.textAlign='left';
        ctx.fillText(d.note,mx+6,my+ph-6);

        ctx.fillStyle=_RE; ctx.font='10px sans-serif'; ctx.textAlign='right';
        ctx.fillText('─ Alpha-1 (SVR↑)',mx+pw-4,my+14);
        ctx.fillStyle=_TE;
        ctx.fillText('─ Beta-1 (HR/CO↑)',mx+pw-4,my+27);
    }

    draw();

    if (ctrl) {
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;';
        var keys=Object.keys(DATA), btns=[];
        keys.forEach(function(k,i) {
            var col=DATA[k].col;
            var b=_mkB(k,col,k===drug,function(on) {
                P.drug=k; drug=k;
                btns.forEach(function(ob,j) {
                    var act=j===i;
                    ob._on=act;
                    ob.style.background=act?DATA[keys[j]].col+'22':'transparent';
                    ob.style.color=act?DATA[keys[j]].col:'#555';
                });
                draw();
            });
            btns.push(b); row.appendChild(b);
        });
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: Cardiac action potential + Vaughan-Williams class targets ────────
RF['action_potential'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;
    var mx=56, my=14, pw=W-mx-12, ph=H-my-52;
    var xD=400, yD=130;  // y domain: mV+90 (so -90mV→0, +40mV→130)

    // AP waveform control points [ms, shifted_mV]
    var AP=[[0,0],[18,0],[20,130],[28,115],[48,108],[250,103],[380,0],[400,0]];

    function apY(x) {
        if (x<=AP[0][0]) return AP[0][1];
        if (x>=AP[AP.length-1][0]) return AP[AP.length-1][1];
        for (var i=0;i<AP.length-1;i++) {
            if (x>=AP[i][0]&&x<=AP[i+1][0]) {
                var t=(x-AP[i][0])/(AP[i+1][0]-AP[i][0]);
                return AP[i][1]+t*(AP[i+1][1]-AP[i][1]);
            }
        }
        return 0;
    }

    function px(x){ return mx+(x/xD)*pw; }
    function py(y){ return my+ph-(y/yD)*ph; }

    var CLASSES = {
        'I':  {col:_OR, x0:18,  x1:23,  phase:'Ph 0', line1:'Class I — Na⁺ blockers', line2:'Ia: quinidine, procainamide (QT↑ QRS↑)', line3:'Ib: lidocaine (VT/VF only)', line4:'Ic: flecainide, propafenone (QRS↑↑)'},
        'II': {col:_GN, x0:0,   x1:18,  phase:'Ph 4', line1:'Class II — β-blockers', line2:'SA node: ↓automaticity, ↓HR', line3:'AV node: ↓ conduction (PR↑)', line4:'metoprolol, esmolol, propranolol'},
        'III':{col:_PU, x0:250, x1:380, phase:'Ph 3', line1:'Class III — K⁺ blockers', line2:'↑ refractory period → QTc↑↑', line3:'amiodarone (also I, II, IV)', line4:'sotalol, dofetilide, ibutilide'},
        'IV': {col:_TE, x0:48,  x1:250, phase:'Ph 2', line1:'Class IV — Ca²⁺ blockers', line2:'Plateau: ↓ AV conduction', line3:'diltiazem, verapamil', line4:'PR↑, ↓ ventricular rate (AF/flutter)'}
    };

    var sel = P.cls || 'none';

    function draw() {
        _cl(ctx, W, H);
        _gd(ctx,mx,my,pw,ph,50,xD,20,yD);
        _ax(ctx,mx,my,pw,ph);

        // Y labels (mV)
        ctx.textAlign='right';
        [-90,-70,-50,-30,-10,10,30].forEach(function(mv) {
            _lb(ctx,mv,mx-4,py(mv+90)+4,null,9);
        });
        _rl(ctx,'mV',13,my+ph/2);

        // X labels
        ctx.textAlign='center';
        [0,100,200,300,400].forEach(function(x) {
            _lb(ctx,x,px(x),my+ph+14,null,9);
        });
        _lb(ctx,'Time (ms)',mx+pw/2,H-4,null,10);

        // Phase highlight
        if (sel!=='none') {
            var cl=CLASSES[sel];
            ctx.fillStyle=cl.col+'30';
            ctx.fillRect(px(cl.x0),my,px(cl.x1)-px(cl.x0),ph);
            ctx.fillStyle=cl.col;
            ctx.font='bold 9px sans-serif'; ctx.textAlign='center';
            ctx.fillText(cl.phase,(px(cl.x0)+px(cl.x1))/2,my+ph-4);
        }

        // AP curve
        _crv(ctx,apY,0,xD,mx,my,pw,ph,xD,yD,_TE,2.5);

        // Phase number labels on curve
        ctx.font='bold 9px sans-serif'; ctx.fillStyle='#777'; ctx.textAlign='center';
        [[20,130,'0'],[30,115,'1'],[145,108,'2'],[315,50,'3'],[5,0,'4']].forEach(function(p) {
            _lb(ctx,p[2],px(p[0]),py(p[1])-7,'#777',9);
        });

        // Class annotation
        if (sel!=='none') {
            var cl=CLASSES[sel];
            var tx=mx+6, ty=my+16;
            [cl.line1,cl.line2,cl.line3,cl.line4].forEach(function(ln,i) {
                ctx.fillStyle=i===0?cl.col:'#aaa';
                ctx.font=(i===0?'bold ':'')+'9px sans-serif';
                ctx.textAlign='left';
                ctx.fillText(ln,tx,ty+i*13);
            });
        }
    }

    draw();

    if (ctrl) {
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;';
        var ks=['I','II','III','IV'];
        var lbs=['Class I (Na⁺)','Class II (β)','Class III (K⁺)','Class IV (Ca²⁺)'];
        var btns=[];
        ks.forEach(function(k,i) {
            var col=CLASSES[k].col;
            var b=_mkB(lbs[i],col,k===sel,function(on) {
                sel=(on||P.cls!==k)?k:'none';
                P.cls=sel;
                btns.forEach(function(ob,j) {
                    var act=ks[j]===sel;
                    ob._on=act;
                    ob.style.background=act?CLASSES[ks[j]].col+'22':'transparent';
                    ob.style.color=act?CLASSES[ks[j]].col:'#555';
                });
                draw();
            });
            btns.push(b); row.appendChild(b);
        });
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 3: Vaughan-Williams classification bar visual ───────────────────────
RF['vaughan_williams'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;

    var CLASSES = [
        {id:'I',  lbl:'Class I',   ion:'Na⁺ block',  col:_OR,
         sub:'Ia: quinidine, procainamide\nIb: lidocaine, mexiletine\nIc: flecainide, propafenone',
         ecg:'QRS↑ (Ic most)',  use:'VT, VF, AF (Ia)',
         qrs:55, qt:30, pr:10},
        {id:'II', lbl:'Class II',  ion:'β-block',    col:_GN,
         sub:'metoprolol, esmolol\ncarvedilol, propranolol\natenolol, labetalol',
         ecg:'PR↑, HR↓',   use:'AF rate ctrl, post-MI, SVT',
         qrs:5,  qt:5,  pr:65},
        {id:'III',lbl:'Class III', ion:'K⁺ block',   col:_PU,
         sub:'amiodarone, sotalol\ndofetilide, ibutilide\ndronedarone',
         ecg:'QTc↑↑',      use:'AF/flutter, VT/VF prevention',
         qrs:10, qt:80, pr:10},
        {id:'IV', lbl:'Class IV',  ion:'Ca²⁺ block', col:_TE,
         sub:'diltiazem, verapamil\n(NOT dihydropyridines)',
         ecg:'PR↑, HR↓',   use:'AF/flutter rate ctrl, SVT',
         qrs:5,  qt:5,  pr:60}
    ];

    var sel = P.cls || 'none';

    var colW=pw_=(W-30)/4, barH=140, barTop=58, barBot=barTop+barH;
    var mL=14;

    function draw() {
        _cl(ctx, W, H);

        // Title
        ctx.fillStyle='#aaa'; ctx.font='11px sans-serif'; ctx.textAlign='center';
        ctx.fillText('Vaughan-Williams Classification — ECG Effect Comparison',W/2,14);

        // ECG effect legend
        ctx.font='9px sans-serif'; ctx.textAlign='left';
        [['QRS↑',_OR,380],['QTc↑',_PU,430],['PR↑',_GN,480]].forEach(function(it) {
            ctx.fillStyle=it[1]; ctx.fillText(it[0],it[2],14);
        });

        CLASSES.forEach(function(cl,i) {
            var cx=mL+i*colW+colW/2;
            var isSelected=(sel===cl.id);

            // Column background
            if (isSelected) {
                ctx.fillStyle=cl.col+'18';
                ctx.fillRect(mL+i*colW+2,20,colW-4,H-24);
            }

            // Class header box
            ctx.fillStyle=isSelected?cl.col:cl.col+'88';
            ctx.fillRect(mL+i*colW+4,22,colW-8,28);
            ctx.fillStyle='#fff'; ctx.font='bold 11px sans-serif'; ctx.textAlign='center';
            ctx.fillText(cl.lbl,cx,35);
            ctx.font='9px sans-serif';
            ctx.fillText(cl.ion,cx,47);

            // Bars: QRS, QT, PR effect
            var bw=14, gap=6, bx0=cx-((bw*3+gap*2)/2);
            var barData=[[cl.qrs,_OR,'QRS'],[cl.qt,_PU,'QTc'],[cl.pr,_GN,'PR']];
            barData.forEach(function(b,j) {
                var bx=bx0+j*(bw+gap);
                var bh=Math.round((b[0]/100)*barH);
                ctx.fillStyle=b[1]+(isSelected?'cc':'66');
                ctx.fillRect(bx,barBot-bh,bw,bh);
                ctx.fillStyle='#888'; ctx.font='8px sans-serif'; ctx.textAlign='center';
                ctx.fillText(b[2],bx+bw/2,barBot+10);
            });

            // Y axis line for this column
            ctx.strokeStyle='#333'; ctx.lineWidth=1;
            ctx.beginPath(); ctx.moveTo(cx-25,barTop); ctx.lineTo(cx-25,barBot); ctx.stroke();

            // Drugs text
            if (isSelected) {
                var lines=cl.sub.split('\n');
                ctx.fillStyle=cl.col; ctx.font='9px sans-serif'; ctx.textAlign='center';
                lines.forEach(function(ln,li) {
                    ctx.fillText(ln,cx,barBot+26+li*13);
                });
                ctx.fillStyle='#aaa'; ctx.font='8px sans-serif';
                ctx.fillText('Use: '+cl.use,cx,barBot+26+lines.length*13+4);
                ctx.fillText('ECG: '+cl.ecg,cx,barBot+26+lines.length*13+15);
            }
        });

        // Bar height scale
        ctx.fillStyle='#555'; ctx.font='8px sans-serif'; ctx.textAlign='left';
        ctx.fillText('Relative ECG effect',mL,barTop-4);
    }

    var pw_; draw();

    if (ctrl) {
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;';
        var btns=[];
        CLASSES.forEach(function(cl,i) {
            var b=_mkB(cl.lbl,cl.col,cl.id===sel,function(on) {
                sel=(P.cls===cl.id&&!on)?'none':cl.id;
                P.cls=sel;
                btns.forEach(function(ob,j) {
                    var act=CLASSES[j].id===sel;
                    ob._on=act;
                    ob.style.background=act?CLASSES[j].col+'22':'transparent';
                    ob.style.color=act?CLASSES[j].col:'#555';
                });
                draw();
            });
            btns.push(b); row.appendChild(b);
        });
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 4: Coagulation cascade with drug action sites ──────────────────────
RF['anticoag_cascade'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;

    // Factor box positions [cx, cy, label]
    var F = {
        'XII': [120,  40, 'Intrinsic\nXII→XI→IX'],
        'TF':  [500,  40, 'Extrinsic\nTF + VII'],
        'Xa':  [310, 110, 'Factor Xa'],
        'IIa': [310, 175, 'IIa (Thrombin)'],
        'Fbr': [310, 245, 'Fibrin Clot']
    };

    var DRUGS = {
        'UFH/LMWH':    {col:_TE,  sites:['Xa','IIa'], note:'Via Antithrombin III\nInhibits Xa + IIa\nReversed by protamine'},
        'Fondaparinux':{col:_GN,  sites:['Xa'],        note:'Anti-Xa only (via ATIII)\nNo reversal agent\nSafe in HIT'},
        'Xa inhibitors':{col:_OR, sites:['Xa'],        note:'Rivaroxaban, apixaban, edoxaban\nDirect Xa inhibition\nAndexanet alfa reversal'},
        'DTIs':        {col:_PU,  sites:['IIa'],       note:'Argatroban, bivalirudin\nDabigatran (idarucizumab reversal)\nUse in HIT'},
        'Warfarin':    {col:_AM,  sites:['XII','TF','Xa','IIa'], note:'Blocks II, VII, IX, X synthesis\n(VKORC1 inhibition)\nReversed: Vit K, 4-factor PCC'},
        'tPA':         {col:_RE,  sites:['Fbr'],       note:'Plasminogen → Plasmin\nLyses formed fibrin\nRisk: hemorrhage'}
    };

    var sel = P.drug || 'none';

    function boxPts(key) {
        var f=F[key]; var bw=90,bh=30;
        return {x:f[0]-bw/2, y:f[1]-bh/2, w:bw, h:bh, cx:f[0], cy:f[1]};
    }

    function drawArrow(x1,y1,x2,y2,col) {
        ctx.strokeStyle=col||'#444'; ctx.lineWidth=1.5;
        ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke();
        var ang=Math.atan2(y2-y1,x2-x1);
        ctx.fillStyle=col||'#444';
        ctx.beginPath();
        ctx.moveTo(x2,y2);
        ctx.lineTo(x2-8*Math.cos(ang-0.3),y2-8*Math.sin(ang-0.3));
        ctx.lineTo(x2-8*Math.cos(ang+0.3),y2-8*Math.sin(ang+0.3));
        ctx.closePath(); ctx.fill();
    }

    function draw() {
        _cl(ctx, W, H);

        // Title
        ctx.fillStyle='#888'; ctx.font='10px sans-serif'; ctx.textAlign='center';
        ctx.fillText('Coagulation Cascade — Drug Action Sites',W/2,12);

        var d=sel!=='none'?DRUGS[sel]:null;
        var hitSites=d?d.sites:[];

        // Draw arrows
        drawArrow(F['XII'][0],F['XII'][1]+20,F['Xa'][0]-45,F['Xa'][1]-15,'#555');
        drawArrow(F['TF'][0],F['TF'][1]+20,F['Xa'][0]+45,F['Xa'][1]-15,'#555');
        drawArrow(F['Xa'][0],F['Xa'][1]+15,F['IIa'][0],F['IIa'][1]-15,'#555');
        drawArrow(F['IIa'][0],F['IIa'][1]+15,F['Fbr'][0],F['Fbr'][1]-15,'#555');

        // Draw factor boxes
        Object.keys(F).forEach(function(key) {
            var b=boxPts(key);
            var hit=hitSites.indexOf(key)>=0;
            ctx.fillStyle=hit?(d.col+'33'):'#181818';
            ctx.strokeStyle=hit?d.col:'#444';
            ctx.lineWidth=hit?2:1;
            ctx.beginPath();
            ctx.roundRect(b.x,b.y,b.w,b.h,5);
            ctx.fill(); ctx.stroke();

            ctx.fillStyle=hit?d.col:'#ccc';
            ctx.font=(hit?'bold ':'')+'10px sans-serif';
            ctx.textAlign='center';
            var lines=F[key][2].split('\n');
            if (lines.length===1) {
                ctx.fillText(lines[0],F[key][0],F[key][1]+4);
            } else {
                ctx.font='8px sans-serif';
                ctx.fillText(lines[0],F[key][0],F[key][1]-4);
                ctx.fillText(lines[1],F[key][0],F[key][1]+7);
            }

            // Hit marker
            if (hit) {
                ctx.strokeStyle=d.col; ctx.lineWidth=2;
                var r=11;
                ctx.beginPath(); ctx.arc(b.x+b.w-8,b.y+8,r/2,0,Math.PI*2); ctx.stroke();
                ctx.strokeStyle=d.col; ctx.lineWidth=2;
                ctx.beginPath();
                ctx.moveTo(b.x+b.w-11,b.y+5); ctx.lineTo(b.x+b.w-5,b.y+11);
                ctx.moveTo(b.x+b.w-5, b.y+5); ctx.lineTo(b.x+b.w-11,b.y+11);
                ctx.stroke();
            }
        });

        // Drug annotation
        if (d) {
            var lines=d.note.split('\n');
            var tx=14, ty=145;
            ctx.fillStyle=d.col; ctx.font='bold 10px sans-serif'; ctx.textAlign='left';
            ctx.fillText(sel,tx,ty);
            lines.forEach(function(ln,i) {
                ctx.fillStyle='#aaa'; ctx.font='9px sans-serif';
                ctx.fillText(ln,tx,ty+14+i*13);
            });
        }
    }

    draw();

    if (ctrl) {
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        var keys=Object.keys(DRUGS), btns=[];
        keys.forEach(function(k,i) {
            var col=DRUGS[k].col;
            var b=_mkB(k,col,k===sel,function(on) {
                sel=(P.drug===k&&!on)?'none':k;
                P.drug=sel;
                btns.forEach(function(ob,j) {
                    var act=keys[j]===sel;
                    ob._on=act;
                    ob.style.background=act?DRUGS[keys[j]].col+'22':'transparent';
                    ob.style.color=act?DRUGS[keys[j]].col:'#555';
                });
                draw();
            });
            btns.push(b); row.appendChild(b);
        });
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 5: PADIS analgesic ladder ──────────────────────────────────────────
RF['analgesic_ladder'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;

    var STEPS = [
        {n:1, col:_GN,  label:'Step 1 — Non-Opioid First',
         drugs:'Acetaminophen (scheduled)\nNSAIDs (short-term)\nKetamine (low-dose adjunct)\nRegional / nerve block',
         pain:'NRS 1-4 (mild)',  rass:'Goal: RASS -1 to 0'},
        {n:2, col:_AM,  label:'Step 2 — Low-Dose Opioid',
         drugs:'Fentanyl IV (bolus/infusion)\nHydromorphone IV/PO\nMorphine (caution in renal)',
         pain:'NRS 4-7 (moderate)', rass:'Titrate to NRS ≤3, avoid oversedation'},
        {n:3, col:_RE,  label:'Step 3 — Multimodal Escalation',
         drugs:'ATC opioid + PRN breakthrough\nDexmedetomidine (pain+sedation)\nGabapentin (neuropathic)\nMethadone (chronic/weaning)',
         pain:'NRS >7 (severe / refractory)', rass:'SAT daily; target lightest effective sedation'}
    ];

    var ADJUNCTS = [
        {col:_PU, label:'Adjuncts (any step)', drugs:'Dexmedetomidine\nGabapentin / pregabalin\nClonidine\nAcetaminophen scheduled'},
        {col:_TE, label:'PADIS Targets',       drugs:'Pain: NRS ≤3 at rest\nAgitation: RASS -1 to 0\nDelirium: CAM-ICU daily\nSBT + SAT bundle'}
    ];

    var sel = P.step || 0;

    function draw() {
        _cl(ctx, W, H);

        var stepH=62, stepW=300, startX=20, baseY=H-20;

        // Draw steps (staircase going up-right)
        STEPS.forEach(function(s,i) {
            var x=startX+i*24;
            var y=baseY-(i+1)*stepH;
            var w=stepW-i*12;
            var isSelected=(sel===s.n);

            ctx.fillStyle=isSelected?s.col+'33':s.col+'18';
            ctx.strokeStyle=isSelected?s.col:s.col+'66';
            ctx.lineWidth=isSelected?2:1;
            ctx.beginPath(); ctx.roundRect(x,y,w,stepH-4,4); ctx.fill(); ctx.stroke();

            // Step number
            ctx.fillStyle=s.col; ctx.font='bold 18px sans-serif'; ctx.textAlign='left';
            ctx.fillText(s.n,x+8,y+26);

            // Step label
            ctx.font='bold 10px sans-serif';
            ctx.fillText(s.label,x+28,y+17);

            // Pain range
            ctx.fillStyle='#888'; ctx.font='9px sans-serif';
            ctx.fillText(s.pain,x+28,y+30);
            ctx.fillText(s.rass,x+28,y+42);

            // Drugs (when selected)
            if (isSelected) {
                var lines=s.drugs.split('\n');
                ctx.fillStyle=s.col; ctx.font='9px sans-serif'; ctx.textAlign='left';
                lines.forEach(function(ln,li) {
                    ctx.fillText('• '+ln, x+28, y+55+li*13);
                });
            }
        });

        // Adjunct panels (right side)
        ADJUNCTS.forEach(function(a,i) {
            var ax=startX+stepW+14, ay=i*(H/2)+10, aw=W-ax-10, ah=H/2-16;
            ctx.fillStyle=a.col+'18'; ctx.strokeStyle=a.col+'66'; ctx.lineWidth=1;
            ctx.beginPath(); ctx.roundRect(ax,ay,aw,ah,4); ctx.fill(); ctx.stroke();
            ctx.fillStyle=a.col; ctx.font='bold 9px sans-serif'; ctx.textAlign='left';
            ctx.fillText(a.label,ax+6,ay+14);
            ctx.fillStyle='#aaa'; ctx.font='9px sans-serif';
            a.drugs.split('\n').forEach(function(ln,li) {
                ctx.fillText(ln,ax+6,ay+28+li*13);
            });
        });

        // PADIS label
        ctx.fillStyle='#555'; ctx.font='8px sans-serif'; ctx.textAlign='left';
        ctx.fillText('PADIS = Pain, Agitation, Delirium, Immobility, Sleep',startX,H-4);
    }

    draw();

    if (ctrl) {
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;';
        var btns=[];
        STEPS.forEach(function(s,i) {
            var b=_mkB('Step '+s.n,s.col,sel===s.n,function(on) {
                sel=(P.step===s.n&&!on)?0:s.n;
                P.step=sel;
                btns.forEach(function(ob,j) {
                    var act=STEPS[j].n===sel;
                    ob._on=act;
                    ob.style.background=act?STEPS[j].col+'22':'transparent';
                    ob.style.color=act?STEPS[j].col:'#555';
                });
                draw();
            });
            btns.push(b); row.appendChild(b);
        });
        ctrl.appendChild(row);
    }
}
"""

# ── Card Definitions ──────────────────────────────────────────────────────────
# Badges confirmed from live Anki deck (mcp__anki__list_decks, 2026-05-14):
#   Ph7 · 🟡 T3 · Pharmacology — Vasopressors & Inotropes
#   Ph7 · 🟡 T3 · Pharmacology — Antiarrhythmics
#   Ph7 · 🟡 T3 · Pharmacology — Anticoagulants & Reversal
#   Ph7 · 🟡 T3 · Pharmacology — Sedation & Analgesia

_VP  = 'Ph7 · \U0001f7e1 T3 · Pharmacology — Vasopressors & Inotropes'
_AA  = 'Ph7 · \U0001f7e1 T3 · Pharmacology — Antiarrhythmics'
_AC  = 'Ph7 · \U0001f7e1 T3 · Pharmacology — Anticoagulants & Reversal'
_SA  = 'Ph7 · \U0001f7e1 T3 · Pharmacology — Sedation & Analgesia'

CARDS = [
    # ═══ vasopressor_dose_response ═══════════════════════════════════════════
    # L1
    (
        "On the vasopressor dose-response chart, dopamine at low doses (1-3 mcg/kg/min) "
        "primarily activates _______ receptors, causing _______. "
        "At high doses (>10 mcg/kg/min) it shifts to activate _______ receptors.",

        "Dopaminergic (DA1/DA2) receptors → renal and mesenteric vasodilation.\n"
        "| At high doses: alpha-1 receptors → vasoconstriction, ↑SVR.\n"
        "→ CCRN KEY: Dopamine is dose-dependent — low = DA (renal flow), mid = beta-1 "
        "(inotropy/↑HR), high = alpha-1 (vasoconstriction). The chart shows the receptor "
        "activity curves crossing as dose increases.\n"
        "→ MASTERY NOTE: In practice, dopamine's dose-dependent selectivity is less "
        "predictable than norepinephrine, which is why norepi is the first-line vasopressor "
        "in septic shock (Surviving Sepsis 2021).",

        'tier-review',
        _VP,
        DID['vasopressors'],
        'vasopressor_dose_response',
        '{"drug":"Dopamine"}',
        'chart-l1'
    ),
    # L2
    (
        "The chart shows norepinephrine maintains high alpha-1 activity (~80%) with moderate "
        "beta-1 (~35%) across all doses. This explains why norepinephrine causes _______ "
        "without the _______ seen with pure alpha agonists.",

        "↑SVR (vasoconstriction) and ↑MAP without the severe reflex bradycardia seen with "
        "phenylephrine, because the moderate beta-1 activity partially offsets vagal "
        "reflexes and maintains cardiac output.\n"
        "→ CCRN KEY: Norepinephrine = alpha-1 dominant + beta-1 support → ↑MAP with "
        "maintained CO. First-line in septic shock. Phenylephrine (pure alpha-1) causes "
        "reflex bradycardia and ↓CO — use only when tachycardia is problematic.\n"
        "→ MASTERY NOTE: Epinephrine shows a CROSSOVER on the chart — beta-1 dominant at "
        "low doses (useful in anaphylaxis, cardiac arrest), alpha-1 overtakes at high doses.",

        'tier-high',
        _VP,
        DID['vasopressors'],
        'vasopressor_dose_response',
        '{"drug":"Norepinephrine"}',
        'chart-l2'
    ),
    # L3
    (
        "A patient in septic shock has MAP 55 despite 2L fluids. HR 118, CO 7.2 L/min "
        "(hyperdynamic), SVR 480. The chart shows phenylephrine's alpha-1 curve is flat "
        "at ~90% with zero beta-1 activity. "
        "The correct first-line vasopressor is _______, not phenylephrine, because _______.",

        "Norepinephrine — not phenylephrine.\n"
        "| Phenylephrine's pure alpha-1 effect would raise SVR and MAP but cause reflex "
        "bradycardia (HR↓) and ↓CO in an already compensating heart. In distributive "
        "(hyperdynamic) shock, you need ↑SVR with maintained CO.\n"
        "→ CCRN KEY: Norepinephrine provides alpha-1 (↑SVR/MAP) + beta-1 (maintains CO). "
        "Phenylephrine is reserved for cases where tachycardia must be avoided "
        "(e.g., AS with rapid AF) or as vasopressor of last resort.\n"
        "→ MASTERY NOTE: If septic shock persists on norepi >0.25 mcg/kg/min, add "
        "vasopressin (V1 receptor, not shown on alpha/beta chart — different mechanism entirely).",

        'tier-critical',
        _VP,
        DID['vasopressors'],
        'vasopressor_dose_response',
        '{"drug":"Phenylephrine"}',
        'chart-l3'
    ),
    # L4
    (
        "Comparing epinephrine and dopamine on the chart at equivalent dose levels, "
        "epinephrine at low doses shows _______ dominant activity, while dopamine at the "
        "same relative dose shows _______. "
        "This pharmacologic difference explains their different first-line indications: "
        "epinephrine for _______, dopamine historically for _______.",

        "Epinephrine low dose: beta-1 dominant (↑HR, ↑CO, bronchodilation).\n"
        "| Dopamine at equivalent relative dose: dopaminergic/mixed — less pure beta effect.\n"
        "→ CCRN KEY: Epinephrine is first-line in anaphylaxis (beta-2 bronchodilation + "
        "alpha-1 vasoconstriction + beta-1 cardiac support) and cardiac arrest (ALS protocol). "
        "Dopamine was historically used in cardiogenic shock but has higher arrhythmia risk.\n"
        "→ MASTERY NOTE: 2019 meta-analyses showed dopamine ↑mortality vs norepinephrine "
        "in shock (more arrhythmias). Current guidelines: norepinephrine first, dopamine "
        "only if significant bradycardia is present.",

        'tier-high',
        _VP,
        DID['vasopressors'],
        'vasopressor_dose_response',
        '{"drug":"Epinephrine"}',
        'chart-l4'
    ),

    # ═══ action_potential ════════════════════════════════════════════════════
    # L1
    (
        "On the cardiac action potential chart, the rapid upstroke (Phase 0) is produced "
        "by _______ influx. Class _______ antiarrhythmics target this phase, reducing "
        "_______ as their primary mechanism.",

        "Fast Na+ (sodium) influx through voltage-gated Na+ channels.\n"
        "| Class I antiarrhythmics — Na+ channel blockers.\n"
        "| Reducing: conduction velocity (↓depolarization rate → ↓QRS velocity, "
        "some ↑QRS duration).\n"
        "→ CCRN KEY: Class I = Na+ blockers, target Phase 0. Ia widens QRS + QT "
        "(procainamide), Ib shortens (lidocaine, VT/VF only), Ic markedly widens QRS "
        "(flecainide — avoid post-MI).\n"
        "→ MASTERY NOTE: The AP upstroke velocity directly correlates with conduction "
        "speed. Slowing Phase 0 (Class I) terminates re-entry circuits by creating "
        "bidirectional block.",

        'tier-review',
        _AA,
        DID['antiarrhythmics'],
        'action_potential',
        '{"cls":"I"}',
        'chart-l1'
    ),
    # L2
    (
        "The action potential chart shows Phase 3 (repolarization) driven by K+ efflux. "
        "Class III antiarrhythmics block K+ channels here, causing _______. "
        "The key ECG change is _______, and the major clinical risk is _______.",

        "Prolonged repolarization → extended refractory period (longer action potential duration).\n"
        "| ECG change: QTc prolongation (QTc >500ms = high-risk threshold).\n"
        "| Major risk: Torsades de Pointes (TdP) — polymorphic VT triggered by early "
        "afterdepolarizations (EADs) during the prolonged repolarization phase.\n"
        "→ CCRN KEY: Class III drugs (amiodarone, sotalol, dofetilide) prolong Phase 3 "
        "→ ↑refractory period → prevents re-entry. But QTc monitoring is mandatory. "
        "Stop if QTc >500ms or increases >60ms from baseline.\n"
        "→ MASTERY NOTE: Amiodarone has the lowest TdP risk of Class III drugs despite "
        "massive QTc prolongation — unique because it also has Class I, II, and IV effects "
        "that stabilize the membrane.",

        'tier-high',
        _AA,
        DID['antiarrhythmics'],
        'action_potential',
        '{"cls":"III"}',
        'chart-l2'
    ),
    # L3
    (
        "A patient with new-onset Afib and RVR (HR 142, BP 94/60) is hemodynamically "
        "unstable. After cardioversion, rate control is needed. "
        "The AP chart shows Class IV Ca2+ blockers target Phase 2 plateau. "
        "The correct rate-control agent is _______, and Class IV is avoided in _______ "
        "because _______.",

        "Diltiazem IV (or metoprolol — Class II) for rate control in Afib.\n"
        "| Class IV Ca2+ blockers (diltiazem, verapamil) AVOID in: decompensated HFrEF "
        "(EF <40%), pre-excitation (WPW), or hypotension.\n"
        "| Because: Ca2+ blockers ↓myocardial contractility and can precipitate "
        "acute decompensation in systolic HF; in WPW they block AV node but enhance "
        "accessory pathway conduction → can degenerate to VF.\n"
        "→ CCRN KEY: For Afib RVR with preserved EF and no pre-excitation: diltiazem "
        "or beta-blocker. With HFrEF: amiodarone (safe for rate + rhythm control). "
        "With hypotension: DC cardioversion.\n"
        "→ MASTERY NOTE: Digitalis (Class V, not on chart) slows AV conduction via vagal "
        "enhancement — backup option in HF with Afib, slow onset.",

        'tier-critical',
        _AA,
        DID['antiarrhythmics'],
        'action_potential',
        '{"cls":"IV"}',
        'chart-l3'
    ),
    # L4
    (
        "Amiodarone is unique among antiarrhythmics because the action potential chart "
        "shows it targets _______ phases simultaneously. "
        "This multi-class mechanism means it is effective for both _______ and _______, "
        "but requires monitoring for _______.",

        "All four phases: Class I (Na+, Phase 0), Class II (beta-block, Phase 4), "
        "Class III (K+, Phase 3), Class IV (Ca2+, Phase 2) — a 'dirty' drug.\n"
        "→ CCRN KEY: Amiodarone is effective for both atrial (Afib/flutter) and "
        "ventricular (VT/VF) arrhythmias. It is the most commonly used antiarrhythmic "
        "in the ICU. Safe in HF (no negative inotropy at standard doses).\n"
        "→ MASTERY NOTE: Monitoring requirements: pulmonary toxicity (CXR, PFTs), "
        "thyroid dysfunction (hypo- and hyperthyroidism — iodine-rich), hepatotoxicity "
        "(LFTs), corneal microdeposits, peripheral neuropathy. Half-life 40-55 days "
        "— toxicity can persist months after stopping.",

        'tier-high',
        _AA,
        DID['antiarrhythmics'],
        'action_potential',
        '{"cls":"I"}',
        'chart-l4'
    ),

    # ═══ vaughan_williams ════════════════════════════════════════════════════
    # L1
    (
        "On the Vaughan-Williams chart, Class _______ shows the greatest effect on QTc "
        "interval with minimal QRS widening, while Class _______ shows the greatest QRS "
        "widening with minimal QTc effect. "
        "The drug most associated with QTc prolongation and Torsades risk is _______.",

        "Class III (K+ blockers) — greatest QTc prolongation, minimal QRS widening.\n"
        "| Class Ic (subclass of Class I Na+ blockers) — greatest QRS widening "
        "(flecainide, propafenone slow Phase 0 dramatically).\n"
        "| Drug most associated with TdP: dofetilide or sotalol (selective K+ blockers). "
        "Amiodarone also prolongs QTc but has low TdP risk due to multi-class effects.\n"
        "→ CCRN KEY: QRS widening = Na+ block (Class I). QTc prolongation = K+ block "
        "(Class III). PR prolongation = AV node slowing (Class II and IV). "
        "Memorize: I=conduction, II=rate, III=repolarization, IV=rate/AV.\n"
        "→ MASTERY NOTE: Avoid Class Ic agents post-MI (CAST trial: ↑mortality despite "
        "suppressing PVCs). Lidocaine (Class Ib) is the only Class I safe in ischemia.",

        'tier-review',
        _AA,
        DID['antiarrhythmics'],
        'vaughan_williams',
        '{}',
        'chart-l1'
    ),
    # L2
    (
        "A post-cardiac surgery patient develops sustained monomorphic VT. "
        "The Vaughan-Williams chart shows Class II beta-blockers primarily affect PR and HR. "
        "The correct antiarrhythmic for hemodynamically stable sustained VT is _______, "
        "and the Vaughan-Williams class is _______ because _______.",

        "Amiodarone IV (150mg over 10 min, then infusion) — Class III predominantly "
        "(also I, II, IV).\n"
        "| For sustained monomorphic VT with hemodynamic stability: amiodarone or "
        "procainamide (Class Ia) IV. Unstable VT: synchronized cardioversion.\n"
        "→ CCRN KEY: Post-cardiac surgery VT often arises from re-entry around suture "
        "lines/ischemic tissue. Amiodarone is first-line because it suppresses both "
        "atrial and ventricular arrhythmias without significant negative inotropy — "
        "critical in post-op patients with borderline cardiac function.\n"
        "→ MASTERY NOTE: Lidocaine (Class Ib) is second-line for VT — shorter duration, "
        "less effective but rapid onset. Avoid in bradycardia or high-degree AV block.",

        'tier-high',
        _AA,
        DID['antiarrhythmics'],
        'vaughan_williams',
        '{}',
        'chart-l2'
    ),
    # L3
    (
        "The Vaughan-Williams chart shows Class II beta-blockers have high PR/rate effect "
        "with minimal direct QRS or QTc change. "
        "A patient post-STEMI develops asymptomatic PVCs. The correct antiarrhythmic "
        "class is _______, and Class Ic drugs are specifically contraindicated because _______.",

        "Class II (beta-blockers) — metoprolol, carvedilol post-MI.\n"
        "| Class Ic (flecainide, propafenone) are contraindicated post-MI because the "
        "CAST trial (1989) showed they ↑mortality despite suppressing PVCs — proarrhythmic "
        "effect in structurally diseased myocardium (slowing conduction creates new "
        "re-entry circuits around scar tissue).\n"
        "→ CCRN KEY: Post-MI rule: Class II is safe and reduces mortality. "
        "Class Ic = avoid. Class Ia (procainamide, quinidine) = also avoid post-MI "
        "(proarrhythmic in scar). Amiodarone = use only for symptomatic/complex VT.\n"
        "→ MASTERY NOTE: 'Treat the patient, not the PVCs.' Asymptomatic PVCs post-MI "
        "do not require antiarrhythmic therapy beyond beta-blockers and optimization of "
        "ischemia/electrolytes.",

        'tier-critical',
        _AA,
        DID['antiarrhythmics'],
        'vaughan_williams',
        '{}',
        'chart-l3'
    ),

    # ═══ anticoag_cascade ════════════════════════════════════════════════════
    # L1
    (
        "On the coagulation cascade chart, UFH and LMWH act by binding _______ to "
        "inhibit both _______ and _______. "
        "Fondaparinux differs by inhibiting only _______ via the same cofactor.",

        "Antithrombin III (ATIII) — conformational change accelerates its inhibition "
        "1000-fold.\n"
        "| UFH/LMWH inhibit: Factor Xa AND Factor IIa (thrombin).\n"
        "| Fondaparinux inhibits: Factor Xa only (anti-Xa activity, too short to bridge "
        "ATIII to thrombin).\n"
        "→ CCRN KEY: UFH = inhibits Xa + IIa (via ATIII) → monitored by aPTT or "
        "anti-Xa level. LMWH = predominantly anti-Xa (some anti-IIa) → use anti-Xa "
        "level monitoring. Fondaparinux = anti-Xa only, no reversal agent.\n"
        "→ MASTERY NOTE: UFH is preferred over LMWH in AKI, obesity, and when rapid "
        "reversal needed (protamine reverses UFH; only partially reverses LMWH; "
        "does NOT reverse fondaparinux).",

        'tier-review',
        _AC,
        DID['anticoagulants'],
        'anticoag_cascade',
        '{"drug":"UFH/LMWH"}',
        'chart-l1'
    ),
    # L2
    (
        "The coagulation cascade chart shows warfarin affects multiple synthesis sites "
        "(II, VII, IX, X), while direct oral anticoagulants (DOACs) inhibit single "
        "factors. A patient develops HIT after 5 days of UFH. "
        "The correct anticoagulant to transition to is _______, not warfarin, because _______.",

        "A direct thrombin inhibitor (DTI): argatroban (preferred in hepatic dysfunction "
        "caution) or bivalirudin; fondaparinux is also used off-label in HIT.\n"
        "| Not warfarin initially because: warfarin suppresses Protein C (a natural "
        "anticoagulant) before it suppresses the pro-clotting factors (II, IX, X) — "
        "this creates a transient HYPERCOAGULABLE state ('warfarin skin necrosis' risk) "
        "if started during active HIT. Must bridge with a non-heparin anticoagulant first.\n"
        "→ CCRN KEY: HIT = heparin-induced thrombocytopenia. Platelet drop >50% or "
        "to <100k after day 4-10 of heparin. Stop ALL heparin (including flushes). "
        "Start non-heparin anticoagulant. 4T score for probability assessment.\n"
        "→ MASTERY NOTE: Argatroban is monitored by aPTT (like UFH). "
        "Bivalirudin is used in cardiac cath/CPB. Fondaparinux (anti-Xa) is safe in "
        "HIT as it doesn't cross-react with PF4 antibodies.",

        'tier-high',
        _AC,
        DID['anticoagulants'],
        'anticoag_cascade',
        '{"drug":"DTIs"}',
        'chart-l2'
    ),
    # L3
    (
        "On the coagulation cascade chart, tPA targets the fibrin clot directly by "
        "converting _______ to _______, which lyses fibrin. "
        "A patient with acute ischemic stroke receives tPA at 3.5 hours from last known well. "
        "Post-tPA BP target is _______, and the major complication requiring immediate CT is _______.",

        "Plasminogen → Plasmin (serine protease that degrades fibrin cross-links).\n"
        "| Post-tPA BP target: maintain BP below 180/105 mmHg for 24 hours "
        "(avoid hypertension that increases hemorrhagic transformation risk).\n"
        "| Major complication requiring immediate CT: symptomatic intracranial hemorrhage "
        "(sICH) — new neurological deterioration, headache, vomiting, or BP surge "
        "post-tPA requires emergent non-contrast CT.\n"
        "→ CCRN KEY: tPA window for ischemic stroke: 0-4.5h from symptom onset "
        "(or last known well). Contraindicated: recent surgery/trauma, INR >1.7, "
        "platelets <100k, BP uncontrolled >185/110 before infusion, hemorrhagic stroke.\n"
        "→ MASTERY NOTE: Door-to-needle target is 60 minutes. Post-tPA: no anticoagulants "
        "or antiplatelets for 24h. If sICH: stop tPA, order cryoprecipitate "
        "(replace fibrinogen), consider TXA.",

        'tier-critical',
        _AC,
        DID['anticoagulants'],
        'anticoag_cascade',
        '{"drug":"tPA"}',
        'chart-l3'
    ),
    # L4
    (
        "The coagulation cascade chart shows warfarin inhibits synthesis of factors II, "
        "VII, IX, and X. Factor VII has the shortest half-life (~6 hours). "
        "This explains why INR rises quickly after starting warfarin but the patient "
        "remains _______ for _______, and reversal for major bleeding uses _______.",

        "Remains hypercoagulable (not truly anticoagulated) for 48-72 hours after "
        "starting warfarin, because Factor VII depletes first (↑INR) but Factors II "
        "and X with longer half-lives (40-60h, 36-45h) are still active.\n"
        "→ CCRN KEY: For urgent warfarin reversal: 4-factor PCC (Kcentra) is preferred "
        "over FFP — faster onset, lower volume, immediate factor replacement for factors "
        "II, VII, IX, X AND Protein C/S. Add Vitamin K 10mg IV for sustained effect. "
        "FFP: slower, large volume, risk of TRALI/TACO.\n"
        "→ MASTERY NOTE: INR target for mechanical heart valves = 2.5-3.5 (higher than "
        "AF/DVT target of 2-3). Supratherapeutic INR without bleeding: hold warfarin "
        "+/- low-dose Vitamin K PO. Elevated INR alone is NOT an indication to reverse "
        "with PCC unless there is active major bleeding.",

        'tier-high',
        _AC,
        DID['anticoagulants'],
        'anticoag_cascade',
        '{"drug":"Warfarin"}',
        'chart-l4'
    ),

    # ═══ analgesic_ladder ════════════════════════════════════════════════════
    # L1
    (
        "On the PADIS analgesic ladder chart, Step 1 emphasizes non-opioid analgesia first. "
        "The PADIS guideline acronym stands for _______, and the recommended sedation "
        "target in mechanically ventilated ICU patients is RASS _______.",

        "PADIS = Pain, Agitation/Sedation, Delirium, Immobility, Sleep.\n"
        "| RASS target: -1 to 0 (light sedation — calm and cooperative, or briefly "
        "drowsy but arousable to voice). Deeper sedation (RASS -2 to -5) is reserved "
        "for specific indications (ARDS with refractory hypoxemia, ICP crisis, status "
        "epilepticus, patient-ventilator asynchrony).\n"
        "→ CCRN KEY: PADIS 2018 (updated) emphasizes analgesia-FIRST approach: treat "
        "pain before adding sedation. Uncontrolled pain drives agitation. "
        "Light sedation goal ↓ ventilator days, ICU-LOS, delirium incidence, and mortality.\n"
        "→ MASTERY NOTE: Daily SAT (Spontaneous Awakening Trial) paired with SBT "
        "(Spontaneous Breathing Trial) = the 'ABC bundle.' SAT: stop sedation, assess. "
        "SBT: pressure support trial. Together they ↓ventilator days by ~3 days "
        "(Girard NEJM 2008).",

        'tier-review',
        _SA,
        DID['sedation_analgesia'],
        'analgesic_ladder',
        '{"step":1}',
        'chart-l1'
    ),
    # L2
    (
        "The analgesic ladder shows Step 1 non-opioid agents including ketamine. "
        "At sub-dissociative doses (0.1-0.3 mg/kg IV or 0.1-0.5 mg/kg/hr infusion), "
        "ketamine provides analgesia via _______ receptor antagonism and offers the "
        "advantage of _______ compared to opioids.",

        "NMDA (N-methyl-D-aspartate) receptor antagonism — blocks central sensitization "
        "and 'wind-up' of pain pathways.\n"
        "| Advantage over opioids: preserves respiratory drive and airway reflexes at "
        "sub-dissociative doses — useful for procedural analgesia without respiratory "
        "depression. Also: opioid-sparing effect (↓total opioid dose), "
        "bronchodilation (sympathomimetic), no histamine release.\n"
        "→ CCRN KEY: Sub-dissociative ketamine is particularly useful for: "
        "procedure-related pain (line placement, dressing changes), opioid-tolerant "
        "patients, trauma analgesia, and patients with opioid-induced hyperalgesia.\n"
        "→ MASTERY NOTE: Avoid ketamine in: uncontrolled hypertension (sympathomimetic "
        "↑BP/HR), active psychosis, or elevated ICP concerns (though this "
        "contraindication is now questioned — ketamine may be safe with adequate "
        "sedation in intubated patients with ICP monitors).",

        'tier-high',
        _SA,
        DID['sedation_analgesia'],
        'analgesic_ladder',
        '{"step":1}',
        'chart-l2'
    ),
    # L3
    (
        "An intubated patient on the analgesic ladder Step 2 has NRS pain 7/10, "
        "RASS -3 (deeply sedated on propofol + fentanyl infusion), and CAM-ICU positive. "
        "The correct PADIS-guided intervention is _______, not increasing sedation, "
        "because _______.",

        "Perform SAT (hold sedation, assess), optimize analgesia (↑fentanyl or add "
        "scheduled acetaminophen/ketamine), target RASS -1 to 0, reassess delirium.\n"
        "| NOT increasing sedation because: deeper sedation worsens ICU delirium, "
        "prolongs mechanical ventilation, increases ICU-acquired weakness, and masks "
        "inadequately treated pain. The agitation is likely pain-driven, not sedation "
        "deficiency.\n"
        "→ CCRN KEY: PADIS sequence: 1) Assess and treat PAIN first (A-1C = "
        "Analgesia-First Care). 2) Target light sedation (RASS -1 to 0). "
        "3) Minimize benzodiazepines (↑delirium). 4) Mobilize early. 5) Promote sleep.\n"
        "→ MASTERY NOTE: Dexmedetomidine (alpha-2 agonist) provides sedation + "
        "analgesia + anxiolysis without respiratory depression and ↓delirium vs "
        "midazolam (MENDS trial). Consider it for RASS -1 to -2 goal when "
        "weaning from deeper sedation.",

        'tier-critical',
        _SA,
        DID['sedation_analgesia'],
        'analgesic_ladder',
        '{"step":2}',
        'chart-l3'
    ),
]

# ── Build pipeline ────────────────────────────────────────────────────────────
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
        print(f"  {'OK' if ok else 'XX'} [{ctype[:18]}·{ltag}]{w_str}  {front[:55]}")
        if not ok:
            for iss in issues: print(f"      x {iss}")

    print(validator.report())
    print()

    for i, card in enumerate(CARDS):
        front, back, tier, badge, did, ctype, pj, ltag = card

        issues = validator.validate(f'c{CHUNK_NUM}_{i}_build', front, back, badge)
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
        print(f"  + [{ctype[:18]}·{ltag}]  {front[:55]}")

    save_deck(db, models, WORK_DIR, OUT_PATH)

    db2 = sqlite3.connect(os.path.join(WORK_DIR, 'collection.anki2'))
    total = db2.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    db2.close()

    print(f"\n{'='*65}")
    print(f"  Chunk {CHUNK_NUM}: {added} cards added | Total deck: {total} cards")
    print(f"{'='*65}")


if __name__ == '__main__':
    main()
