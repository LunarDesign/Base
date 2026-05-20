#!/usr/bin/env python3
"""chunk40_charts.py — Ph7 Vasopressors & Inotropes (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_39.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_40.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c40')
CHUNK_NUM   = 40
MID_BASE    = 1_800_005_045
CHART_ORDER = ['vasopressor_receptors', 'shock_vasopressor', 'inotrope_comparison',
               'pressor_titration', 'vasopressor_weaning']

_VP = 'Ph7 · \U0001f7e1 T3 · Pharmacology — Vasopressors & Inotropes'

RF = {}

# ── Chart 1: Vasopressor Receptor Activity ────────────────────────────────────
RF['vasopressor_receptors'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var drugs=[
        {name:'Norepinephrine', note:'1st-line: septic/distributive',  r:[4,3,1,0,0]},
        {name:'Epinephrine',    note:'2nd-line: refractory/anaphylaxis',r:[4,4,3,0,0]},
        {name:'Dopamine',       note:'Dose-dependent: rarely 1st-line', r:[2,3,1,0,3]},
        {name:'Phenylephrine',  note:'Pure α1: neurogenic/SVT-related', r:[4,0,0,0,0]},
        {name:'Vasopressin',    note:'Add-on: refractory septic shock', r:[0,0,0,4,0]},
        {name:'Dobutamine',     note:'Inotrope: cardiogenic shock',     r:[1,4,2,0,0]},
    ];
    var rcols=[_RE,_TE,_GN,_PU,_AM];
    var rnames=['α1','β1','β2','V1','DA'];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var mx=10, dc=165, rc=(W-dc-mx*2)/5;
    ctx.fillStyle='#111';ctx.fillRect(mx,4,W-mx*2,16);
    ctx.fillStyle=_TE;ctx.font='bold 9px sans-serif';ctx.textAlign='left';
    ctx.fillText('VASOPRESSOR & INOTROPE — Receptor Activity Profile',mx+4,14);
    var hy=23;
    ctx.fillStyle='#181818';ctx.fillRect(mx,hy,W-mx*2,15);
    ctx.fillStyle='#444';ctx.font='bold 8px sans-serif';ctx.textAlign='center';
    ctx.fillText('DRUG / INDICATION',mx+dc/2,hy+11);
    rnames.forEach(function(rn,i){ctx.fillStyle=rcols[i];ctx.fillText(rn,mx+dc+i*rc+rc/2,hy+11);});
    var ry=41, rh=36;
    drugs.forEach(function(d,i){
        var dy=ry+i*(rh+2), isHi=(hi===i);
        ctx.fillStyle=isHi?'#061422':(i%2?'#111':'#0c0c0c');
        ctx.fillRect(mx,dy,W-mx*2,rh);
        if(isHi){ctx.strokeStyle=_TE;ctx.lineWidth=1.5;ctx.strokeRect(mx,dy,W-mx*2,rh);}
        ctx.strokeStyle='#1e1e1e';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(mx+dc,dy);ctx.lineTo(mx+dc,dy+rh);ctx.stroke();
        ctx.fillStyle=isHi?_TE:'#ddd';ctx.font=(isHi?'bold ':'')+'10px sans-serif';ctx.textAlign='left';
        ctx.fillText(d.name,mx+4,dy+14);
        ctx.fillStyle='#555';ctx.font='8px sans-serif';
        ctx.fillText(d.note,mx+4,dy+27);
        d.r.forEach(function(lv,j){
            var cx=mx+dc+j*rc, bw=Math.round((lv/4)*(rc-8)), bh=10;
            var by2=dy+rh/2-bh/2;
            ctx.fillStyle=rcols[j]+'18';ctx.fillRect(cx+2,dy+2,rc-4,rh-4);
            if(lv>0){ctx.fillStyle=rcols[j];ctx.fillRect(cx+4,by2,bw,bh);}
            ctx.fillStyle=lv>0?rcols[j]:'#2a2a2a';ctx.font='bold 9px sans-serif';ctx.textAlign='center';
            ctx.fillText(['-','+','++','+++','++++'][lv],cx+rc/2,by2+bh+11);
        });
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        var lbl=document.createElement('span');lbl.style.cssText='font-size:9px;color:#444;font-weight:800;align-self:center;';
        lbl.textContent='FOCUS:';row.appendChild(lbl);
        var lbs=['Norepi','Epi','Dopa','Phenyl.','Vasopres.','Dobuta.'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,_TE,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('all',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: Shock Type → Vasopressor Selection ───────────────────────────────
RF['shock_vasopressor'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:-1;
    var shocks=[
        {name:'Distributive (Septic)', co:'High/Normal', svr:'LOW', pcwp:'Low/Normal',
         cc:[_GN,_RE,_AM],
         first:'Norepinephrine 0.05–3 mcg/kg/min',
         esc:'+ Vasopressin 0.03 units/min if norepi >0.25 mcg/kg/min',
         note:'SOAP-II: norepi > dopamine (fewer arrhythmias). Epi if cardiac component. Steroids if refractory.'},
        {name:'Cardiogenic', co:'LOW', svr:'High', pcwp:'HIGH',
         cc:[_RE,_OR,_OR],
         first:'Norepinephrine (MAP) + Dobutamine (CO)',
         esc:'Milrinone if on beta-blocker; IABP/Impella if refractory',
         note:'Avoid pure vasopressors alone — raises afterload without improving CO. Target: MAP ≥65 + CI >2.2.'},
        {name:'Obstructive (Massive PE)', co:'LOW', svr:'High', pcwp:'Variable',
         cc:[_RE,_OR,_AM],
         first:'Norepinephrine (bridge to reperfusion)',
         esc:'tPA 100 mg/2h OR catheter-directed if systemic tPA contraindicated',
         note:'Vasopressors = bridge only. NO fluid boluses — worsens RV distension. Treat the obstruction.'},
        {name:'Hypovolemic', co:'LOW', svr:'High', pcwp:'LOW',
         cc:[_RE,_OR,_RE],
         first:'VOLUME REPLACEMENT is definitive therapy',
         esc:'Norepinephrine or phenylephrine as bridge only',
         note:'Identify and stop source. Vasopressors without volume = temporary; organ ischemia worsens.'},
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    if(sel<0){
        ctx.fillStyle='#ccc';ctx.font='bold 10px sans-serif';ctx.textAlign='center';
        ctx.fillText('SHOCK TYPE → VASOPRESSOR SELECTION',W/2,14);
        var bw=(W-30)/2,bh=112,gap=10,by=22;
        shocks.forEach(function(s,i){
            var col=i%2,row=Math.floor(i/2);
            var bx=10+col*(bw+gap),ry=by+row*(bh+gap);
            ctx.fillStyle='#0d0d0d';ctx.fillRect(bx,ry,bw,bh);
            ctx.strokeStyle='#2a2a2a';ctx.lineWidth=1;ctx.strokeRect(bx,ry,bw,bh);
            ctx.fillStyle=_TE;ctx.font='bold 10px sans-serif';ctx.textAlign='center';
            ctx.fillText(s.name,bx+bw/2,ry+15);
            var hk=['CO:','SVR:','PCWP:'],hv=[s.co,s.svr,s.pcwp];
            hk.forEach(function(k,j){
                ctx.fillStyle='#555';ctx.font='8.5px sans-serif';ctx.textAlign='left';ctx.fillText(k,bx+6,ry+30+j*15);
                ctx.fillStyle=s.cc[j];ctx.font='bold 8.5px sans-serif';ctx.fillText(hv[j],bx+40,ry+30+j*15);
            });
            ctx.fillStyle=_GN;ctx.font='8px sans-serif';ctx.textAlign='left';
            ctx.fillText('▶ '+s.first.substring(0,38),bx+6,ry+86);
        });
    } else {
        var s=shocks[sel];
        ctx.fillStyle=_TE;ctx.font='bold 12px sans-serif';ctx.textAlign='left';ctx.fillText(s.name,12,20);
        var hk=['CO','SVR','PCWP'],hv=[s.co,s.svr,s.pcwp];
        hk.forEach(function(k,i){
            var hx=12+i*136;
            ctx.fillStyle='#1a1a1a';ctx.fillRect(hx,26,126,34);
            ctx.fillStyle='#555';ctx.font='8px sans-serif';ctx.textAlign='left';ctx.fillText(k,hx+5,38);
            ctx.fillStyle=s.cc[i];ctx.font='bold 14px sans-serif';ctx.fillText(hv[i],hx+5,53);
        });
        ctx.fillStyle='#111';ctx.fillRect(12,68,W-24,36);
        ctx.strokeStyle=_GN;ctx.lineWidth=1;ctx.strokeRect(12,68,W-24,36);
        ctx.fillStyle=_GN;ctx.font='bold 9px sans-serif';ctx.textAlign='left';ctx.fillText('FIRST LINE:',16,80);
        ctx.fillStyle='#ddd';ctx.font='9px sans-serif';ctx.fillText(s.first,16,94);
        ctx.fillStyle='#111';ctx.fillRect(12,110,W-24,32);
        ctx.strokeStyle=_AM+'88';ctx.lineWidth=1;ctx.strokeRect(12,110,W-24,32);
        ctx.fillStyle=_AM;ctx.font='bold 9px sans-serif';ctx.textAlign='left';ctx.fillText('ESCALATION:',16,122);
        ctx.fillStyle='#aaa';ctx.font='8.5px sans-serif';ctx.fillText(s.esc,16,135);
        ctx.fillStyle='#1a1a1a';ctx.fillRect(12,148,W-24,110);
        ctx.fillStyle='#666';ctx.font='8.5px sans-serif';ctx.textAlign='left';
        var nw=W-32,words=s.note.split(' '),line='',ly=162;
        words.forEach(function(w){var t=line?line+' '+w:w;if(ctx.measureText(t).width>nw){ctx.fillText(line,16,ly);line=w;ly+=11;}else line=t;});
        if(line)ctx.fillText(line,16,ly);
    }
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;';
        var sls=['Overview','Distributive','Cardiogenic','Obstructive','Hypovolemic'];
        sls.forEach(function(lb,i){(function(idx){var b=_mkB(lb,idx===0?_AX:_TE,sel===(idx-1),function(){
            var ns=idx===0?-1:idx-1;cv.setAttribute('data-params',JSON.stringify({sel:ns}));_render(cv,ctrl,{sel:ns});
        });row.appendChild(b);})(i);});
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 3: Inotrope Comparison ──────────────────────────────────────────────
RF['inotrope_comparison'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var drugs=[
        {name:'Dobutamine',   col:_TE,  mech:'β1 agonist (cAMP via receptor)',
         co:4, svr:-2, hr:3, bb:'ATTENUATED by beta-blockers',
         ind:'1st-line inotrope; cardiogenic shock',
         clear:'Hepatic (infusion, short t½)'},
        {name:'Milrinone',    col:_GN,  mech:'PDE-III inhibitor (cAMP receptor-independent)',
         co:4, svr:-3, hr:2, bb:'NOT affected by beta-blockers',
         ind:'On beta-blocker; renal failure (dose-reduce)',
         clear:'Renal — dose-reduce in AKI/CKD'},
        {name:'Levosimendan', col:_AM,  mech:'Ca²⁺ sensitizer + K-ATP opener',
         co:4, svr:-2, hr:2, bb:'NOT affected (unique mechanism)',
         ind:'Acute HF; post-cardiac surgery',
         clear:'Single 24h dose; active metabolite 7–9d'},
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    ctx.fillStyle='#ccc';ctx.font='bold 10px sans-serif';ctx.textAlign='center';
    ctx.fillText('INOTROPE COMPARISON',W/2,13);
    var bw=(W-30)/3,gap=10,by=22,mx=10;
    drugs.forEach(function(d,i){
        var bx=mx+i*(bw+gap),isHi=(hi===i||hi===-1);
        ctx.fillStyle=isHi?d.col+'11':'#080808';
        ctx.fillRect(bx,by,bw,H-by-6);
        ctx.strokeStyle=isHi?d.col:'#1a1a1a';ctx.lineWidth=isHi?1.5:1;
        ctx.strokeRect(bx,by,bw,H-by-6);
        ctx.fillStyle=d.col;ctx.font='bold 11px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.name,bx+bw/2,by+16);
        ctx.fillStyle='#666';ctx.font='8px sans-serif';
        var mw=bw-8,mwords=d.mech.split(' '),ml='',mly=by+30;
        mwords.forEach(function(w){var t=ml?ml+' '+w:w;if(ctx.measureText(t).width>mw){ctx.fillText(ml,bx+bw/2,mly);ml=w;mly+=11;}else ml=t;});
        if(ml)ctx.fillText(ml,bx+bw/2,mly);
        var rows=[
            {lbl:'CO ↑',val:d.co,max:4,col:_GN,dir:1},
            {lbl:'SVR',val:d.svr,max:3,col:d.svr<0?_RE:_GN,dir:d.svr<0?-1:1},
            {lbl:'HR ↑',val:d.hr,max:3,col:_AM,dir:1},
        ];
        var ry=by+60;
        rows.forEach(function(r){
            ctx.fillStyle='#888';ctx.font='8px sans-serif';ctx.textAlign='left';ctx.fillText(r.lbl,bx+4,ry-2);
            ctx.fillStyle='#1a1a1a';ctx.fillRect(bx+32,ry-11,bw-36,10);
            var barsz=Math.abs(r.val)/r.max*(bw-38);
            ctx.fillStyle=r.col+'cc';ctx.fillRect(bx+32,ry-11,barsz,10);
            var labs=['-','±0','+','++','+++','+++++'];
            ctx.fillStyle=r.col;ctx.font='bold 8px sans-serif';ctx.textAlign='right';
            ctx.fillText((r.dir<0?'↓':'↑')+Math.abs(r.val)+'x',bx+bw-4,ry-2);
            ry+=20;
        });
        ctx.fillStyle=isHi?d.col:'#555';ctx.font='bold 7.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.bb,bx+bw/2,ry+8);
        ctx.fillStyle='#666';ctx.font='8px sans-serif';
        var iw=bw-8,iwords=d.ind.split(' '),il='',ily=ry+22;
        iwords.forEach(function(w){var t=il?il+' '+w:w;if(ctx.measureText(t).width>iw){ctx.fillText(il,bx+bw/2,ily);il=w;ily+=10;}else il=t;});
        if(il)ctx.fillText(il,bx+bw/2,ily);ily+=14;
        ctx.fillStyle='#444';ctx.font='7.5px sans-serif';
        ctx.fillText(d.clear,bx+bw/2,ily);
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;';
        var lbs=['Dobutamine','Milrinone','Levosimendan'];
        var cols=[_TE,_GN,_AM];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,cols[idx],hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('all',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 4: MAP Target Zones ─────────────────────────────────────────────────
RF['pressor_titration'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var map=(P.map!==undefined)?P.map:65;
    var zones=[
        {lo:50,hi:60,col:'#ef5350',lbl:'Danger'},
        {lo:60,hi:65,col:'#ff7043',lbl:'Low Alert'},
        {lo:65,hi:75,col:'#4caf50',lbl:'Sepsis Target'},
        {lo:75,hi:90,col:'#29b6f6',lbl:'TBI/SCI Target'},
        {lo:90,hi:110,col:'#ffca28',lbl:'Over-target'},
    ];
    var targets=[
        {cond:'Septic shock (most)',        target:'65–70',    trial:'SEPSISPAM 2014',    col:_GN},
        {cond:'Cardiogenic shock',          target:'≥65',      trial:'MAP + CO optimize', col:_TE},
        {cond:'TBI (ICP >20)',              target:'≥70–80',trial:'CPP = MAP − ICP ≥60',col:_TE},
        {cond:'Spinal cord injury',         target:'85–90',    trial:'7-day protocol',    col:_PU},
        {cond:'Chronic hypertension',       target:'70–80',    trial:'Higher autoregulation threshold',col:_AM},
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    ctx.fillStyle='#ccc';ctx.font='bold 10px sans-serif';ctx.textAlign='center';
    ctx.fillText('MAP TARGETS BY CLINICAL CONTEXT',W/2,13);
    var sx=20,sw=W-40,sy=22,sh=24,minM=50,maxM=110;
    zones.forEach(function(z){
        var x1=sx+(z.lo-minM)/(maxM-minM)*sw;
        var x2=sx+(z.hi-minM)/(maxM-minM)*sw;
        ctx.fillStyle=z.col+'44';ctx.fillRect(x1,sy,x2-x1,sh);
        ctx.strokeStyle=z.col+'88';ctx.lineWidth=1;ctx.strokeRect(x1,sy,x2-x1,sh);
        ctx.fillStyle=z.col;ctx.font='bold 7.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(z.lbl,x1+(x2-x1)/2,sy+10);
        ctx.fillStyle='#666';ctx.font='7px sans-serif';
        ctx.fillText(z.lo+'',x1,sy+sh+9);
    });
    ctx.fillStyle='#555';ctx.font='7px sans-serif';ctx.textAlign='right';
    ctx.fillText('110',sx+sw,sy+sh+9);
    // Current MAP marker
    var mx2=sx+(map-minM)/(maxM-minM)*sw;
    var activeZone=zones.find(function(z){return map>=z.lo&&map<z.hi;})||zones[zones.length-1];
    ctx.strokeStyle=activeZone.col;ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(mx2,sy);ctx.lineTo(mx2,sy+sh+2);ctx.stroke();
    ctx.fillStyle=activeZone.col;ctx.font='bold 11px sans-serif';ctx.textAlign='center';
    ctx.fillText('MAP '+map,mx2,sy-3);
    // Target table
    var ty=58;
    ctx.fillStyle='#181818';ctx.fillRect(10,ty,W-20,16);
    ctx.fillStyle='#444';ctx.font='bold 8px sans-serif';ctx.textAlign='left';
    ctx.fillText('CLINICAL CONTEXT',14,ty+11);
    ctx.fillText('TARGET mmHg',210,ty+11);
    ctx.fillStyle=_TE;ctx.fillText('RATIONALE / TRIAL',360,ty+11);
    ty+=18;
    targets.forEach(function(t,i){
        ctx.fillStyle=i%2?'#0d0d0d':'#111';ctx.fillRect(10,ty,W-20,26);
        ctx.fillStyle='#bbb';ctx.font='9px sans-serif';ctx.textAlign='left';ctx.fillText(t.cond,14,ty+17);
        ctx.fillStyle=t.col;ctx.font='bold 10px sans-serif';ctx.fillText(t.target,210,ty+17);
        ctx.fillStyle='#666';ctx.font='8px sans-serif';ctx.fillText(t.trial,360,ty+17);
        ty+=28;
    });
    if(ctrl){
        ctrl.innerHTML='';
        var sl=_mkS('MAP',50,110,1,map,function(v){return Math.round(v)+' mmHg';},function(v){
            var p2={map:Math.round(v)};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });ctrl.appendChild(sl);
    }
}
"""

# ── Chart 5: Vasopressor Weaning Protocol ─────────────────────────────────────
RF['vasopressor_weaning'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:-1;
    var stages=[
        {title:'Weaning Criteria', col:_AM,
         crit:'MAP ≥65 ×2h, lactate trending ↓, UO ≥0.5 mL/kg/h, vasopressor dose stable or decreasing',
         action:'Confirm all criteria before initiating wean. Check volume status (PLR test).'},
        {title:'Remove Secondary Agent', col:_GN,
         crit:'Vasopressin (or 2nd agent) weaned first — reverse order of addition',
         action:'Wean vasopressin: 0.03 → 0.02 → 0.01 → off. Monitor MAP after each step.'},
        {title:'Taper Primary Vasopressor', col:_TE,
         crit:'Reduce norepinephrine by 25–50% of current dose q1–2h if MAP ≥65',
         action:'Hold wean if: MAP <65, fever spike, lactate re-elevates, new hemodynamic change.'},
        {title:'Vasopressor-Free', col:_PU,
         crit:'Monitor MAP for 4–6h after last dose; reassess volume/infection if MAP falls',
         action:'Adrenal insufficiency may unmask: low-dose hydrocortisone if refractory hypotension.'},
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    ctx.fillStyle='#ccc';ctx.font='bold 10px sans-serif';ctx.textAlign='center';
    ctx.fillText('VASOPRESSOR WEANING PROTOCOL',W/2,13);
    var my=22, rh=46, gap=3, mx=10;
    stages.forEach(function(s,i){
        var ry=my+i*(rh+gap), isS=(sel===i);
        ctx.fillStyle=isS?s.col+'22':'#0d0d0d';
        ctx.fillRect(mx,ry,W-mx*2,rh);
        ctx.strokeStyle=isS?s.col:'#2a2a2a';ctx.lineWidth=isS?1.5:1;
        ctx.strokeRect(mx,ry,W-mx*2,rh);
        var nw=34;
        ctx.fillStyle=s.col+'44';ctx.fillRect(mx,ry,nw,rh);
        ctx.fillStyle=s.col;ctx.font='bold 11px sans-serif';ctx.textAlign='center';
        ctx.fillText(i+1,mx+nw/2,ry+rh/2+4);
        ctx.fillStyle=isS?s.col:'#ccc';ctx.font=(isS?'bold ':'')+'10px sans-serif';ctx.textAlign='left';
        ctx.fillText(s.title,mx+nw+6,ry+16);
        ctx.fillStyle=isS?'#aaa':'#555';ctx.font='8.5px sans-serif';
        var tw=W-mx*2-nw-12,words=s.crit.split(' '),line='',ly=ry+29;
        words.forEach(function(w){var t=line?line+' '+w:w;if(ctx.measureText(t).width>tw){ctx.fillText(line,mx+nw+6,ly);line=w;ly+=11;}else line=t;});
        if(line)ctx.fillText(line,mx+nw+6,ly);
    });
    if(sel>=0){
        var s=stages[sel], dy=my+4*(rh+gap)+4;
        ctx.fillStyle='#111';ctx.fillRect(mx,dy,W-mx*2,50);
        ctx.strokeStyle=stages[sel].col;ctx.lineWidth=1;ctx.strokeRect(mx,dy,W-mx*2,50);
        ctx.fillStyle=stages[sel].col;ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText('▶ ACTION: '+s.action.substring(0,80),mx+6,dy+14);
        if(s.action.length>80)ctx.fillText(s.action.substring(80),mx+6,dy+26);
    }
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;';
        stages.forEach(function(s,i){(function(idx){var b=_mkB('Step '+(idx+1),s.col,sel===idx,function(on){
            var p2={sel:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        ctrl.appendChild(row);
    }
}
"""

# ── Cards ─────────────────────────────────────────────────────────────────────
CARDS = [

    # ═══ vasopressor_receptors ════════════════════════════════════════════════
    (
        "On the vasopressor receptor chart, phenylephrine is the only agent "
        "with pure _______ activity. This makes it preferred for _______, "
        "but contraindicated in _______ because _______.",

        "Pure α1 agonism (no β1, β2, V1, or DA activity); preferred for "
        "neurogenic shock (vasodilation without cardiac dysfunction) and "
        "procedural hypotension with tachycardia (SVT-associated hypotension);\n"
        "contraindicated in cardiogenic shock because pure vasoconstriction "
        "raises SVR/afterload without improving CO, worsening ventricular function\n"
        "→ CCRN KEY: Phenylephrine causes reflex bradycardia (increased SVR "
        "→ baroreceptor activation → vagal slowing). Useful when tachycardia "
        "is the arrhythmia problem (SVT with hypotension — norepi/epi would "
        "accelerate the rate).\n"
        "→ MASTERY NOTE: Neurogenic shock: loss of sympathetic tone after "
        "SCI → vasodilation (↓SVR) AND bradycardia. Triad: hypotension + "
        "bradycardia + warm/dry skin. Unlike septic shock: no fever, no "
        "tachycardia. Phenylephrine raises SVR; atropine for bradycardia.",

        'tier-review',
        _VP,
        DID['vasopressors'],
        'vasopressor_receptors',
        '{"hi":3}',
        'chart-l1'
    ),
    (
        "The receptor chart shows dopamine has dose-dependent receptor "
        "activity. At doses >10 mcg/kg/min, the dominant effect shifts to "
        "_______ because _______, which led the SOAP-II trial to show "
        "dopamine was inferior to norepinephrine primarily due to _______.",

        "Dominant effect: α1 agonism (vasoconstriction) — at high doses, "
        "α1 activity overwhelms the DA and β1 effects, making dopamine "
        "behave similar to norepinephrine but with worse side effects\n"
        "| SOAP-II inferiority: higher arrhythmia rate (2× AF/SVT), "
        "increased mortality in cardiogenic shock subgroup\n"
        "→ CCRN KEY: Dopamine dose ranges (approximate, not precise): "
        "1–5 mcg/kg/min = DA-dominant (renal vasodilation — NOT renally "
        "protective, DOPAMINE trial debunked); 5–10 = β1-dominant (↑CO); "
        ">10 = α1-dominant (vasopressor). Ranges overlap significantly.\n"
        "→ MASTERY NOTE: SOAP-II (2010): 1679 patients, dopamine vs "
        "norepinephrine as first-line vasopressor. Dopamine group: 2× "
        "arrhythmias, worse 28-day mortality in cardiogenic shock subgroup. "
        "Current guidelines: norepinephrine first-line for septic shock; "
        "dopamine reserved for relative bradycardia + low CO without "
        "arrhythmia risk.",

        'tier-high',
        _VP,
        DID['vasopressors'],
        'vasopressor_receptors',
        '{"hi":2}',
        'chart-l2'
    ),
    (
        "On the receptor chart, vasopressin shows no α1, β1, or β2 "
        "activity. This profile explains three clinical facts: "
        "vasopressin (1) does not cause _______, "
        "(2) is fixed-dosed because _______, "
        "and (3) dose >0.04 units/min risks _______ because _______.",

        "(1) Tachycardia or increased myocardial oxygen demand "
        "(zero β1 activity — no cardiac stimulation)\n"
        "(2) Fixed-dose 0.03–0.04 units/min — NOT titrated; "
        "unlike catecholamines, vasopressin has a narrow therapeutic "
        "range; titration increases ischemic risk without further BP benefit\n"
        "(3) Coronary/mesenteric ischemia — V1 receptors in coronary "
        "and splanchnic vasculature cause vasoconstriction → myocardial "
        "and intestinal ischemia at doses >0.04–0.06 units/min\n"
        "→ CCRN KEY: VASST trial: vasopressin 0.03 units/min + "
        "norepinephrine vs norepinephrine alone — vasopressin reduced "
        "norepi requirements; benefit in less severe septic shock "
        "(norepi 5–14 mcg/min subgroup). Vasopressin for late/"
        "refractory septic shock = catecholamine-sparing strategy.\n"
        "→ MASTERY NOTE: Relative vasopressin deficiency develops in "
        "septic shock after initial neurohypophyseal release is exhausted "
        "(~36h). Exogenous vasopressin restores this deficit. Desmopressin "
        "(DDAVP) is V2-selective = antidiuretic only — different drug, "
        "different indication (central DI, bleeding disorders).",

        'tier-critical',
        _VP,
        DID['vasopressors'],
        'vasopressor_receptors',
        '{"hi":4}',
        'chart-l3'
    ),

    # ═══ shock_vasopressor ════════════════════════════════════════════════════
    (
        "On the shock vasopressor chart, distributive shock hemodynamics are "
        "CO _______, SVR _______, PCWP _______. "
        "The evidence-based first-line vasopressor is _______ "
        "(key trial: _______), and the add-on agent threshold is _______.",

        "CO: high or normal (hyperdynamic); SVR: LOW (massive vasodilation); "
        "PCWP: low or normal\n"
        "| First-line: Norepinephrine (SOAP-II 2010: superior to dopamine "
        "in arrhythmia rate and cardiogenic shock outcomes)\n"
        "| Add-on: Vasopressin 0.03 units/min when norepinephrine "
        "exceeds 0.25–0.5 mcg/kg/min\n"
        "→ CCRN KEY: Surviving Sepsis Campaign: norepinephrine is the "
        "recommended first-line vasopressor (strong evidence). Goal: "
        "MAP ≥65 mmHg. Vasopressin is a catecholamine-sparing add-on, "
        "NOT a replacement. Epinephrine: add when cardiac output "
        "component is insufficient despite norepinephrine + vasopressin.\n"
        "→ MASTERY NOTE: Anaphylactic shock (special case): epinephrine "
        "1st line (IM 0.3–0.5 mg) — reverses vasodilation (α1), "
        "bronchospasm (β2), AND cardiac depression (β1). Do NOT use "
        "norepinephrine alone — lacks β2 bronchodilation.",

        'tier-review',
        _VP,
        DID['vasopressors'],
        'shock_vasopressor',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The cardiogenic shock panel shows CO ↓, SVR ↑, PCWP ↑. "
        "The combination shown is norepinephrine PLUS dobutamine. "
        "When the patient is already on metoprolol XL, the preferred "
        "inotrope switches to _______ because _______, "
        "and the main risk of this switch is _______.",

        "Switch to Milrinone — acts downstream of the β1 receptor "
        "(PDE-III inhibitor); metoprolol blocks β1 receptor → dobutamine "
        "cannot bind effectively; milrinone bypasses the blocked receptor\n"
        "| Main risk: milrinone causes significant SVR reduction "
        "(vasodilation) → hypotension risk; requires vasopressor "
        "co-administration and avoidance of loading dose\n"
        "→ CCRN KEY: Milrinone dosing in cardiogenic shock: "
        "start maintenance infusion ONLY (0.125–0.375 mcg/kg/min) — "
        "omit bolus; loading dose 50 mcg/kg causes acute hypotension. "
        "Long half-life (~2.5h); longer in renal failure — hard to reverse.\n"
        "→ MASTERY NOTE: SHOCK trial (1999): early revascularization "
        "(PCI or CABG) for cardiogenic shock from ACS improves 6-month "
        "survival. Vasopressors/inotropes are bridges to definitive "
        "intervention, not definitive therapy.",

        'tier-high',
        _VP,
        DID['vasopressors'],
        'shock_vasopressor',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The obstructive shock panel (massive PE) shows elevated CVP, "
        "right heart distension. The nurse prepares to give a "
        "500 mL NS bolus for 'hemodynamic support.' "
        "This is incorrect because _______, "
        "and the correct immediate intervention is _______.",

        "Incorrect: IV fluids worsen RV distension in massive PE — "
        "RV is already obstructed and overdistended; fluid bolus "
        "→ more RV dilation → septal shift leftward → impairs LV "
        "filling → worsening CO (RV-LV coupling failure)\n"
        "| Correct: Norepinephrine to maintain MAP (preserves RV "
        "coronary perfusion pressure) + emergent systemic "
        "thrombolysis (tPA 100 mg/2h) if high-risk PE confirmed\n"
        "→ CCRN KEY: High-risk PE criteria: hemodynamic instability "
        "(SBP <90 or vasopressor need) OR cardiac arrest. "
        "Echo findings: RV dilation, D-sign (septal shift), "
        "RV hypokinesis. tPA contraindications: prior ICH, "
        "recent major surgery or trauma, active internal bleeding.\n"
        "→ MASTERY NOTE: RV failure treatment strategy: "
        "norepinephrine maintains aortic diastolic pressure = "
        "RV coronary perfusion; inhaled nitric oxide/prostacyclin "
        "reduces RV afterload selectively; avoid systemic vasodilators. "
        "VA-ECMO for refractory RV failure.",

        'tier-critical',
        _VP,
        DID['vasopressors'],
        'shock_vasopressor',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ inotrope_comparison ══════════════════════════════════════════════════
    (
        "On the inotrope comparison chart, the key mechanistic difference "
        "between dobutamine and milrinone is that milrinone acts "
        "_______ the β1 receptor, making it effective when _______.",

        "Downstream of the β1 receptor — PDE-III inhibitor prevents "
        "cAMP breakdown regardless of receptor occupancy; effective "
        "when β1 receptors are blocked (patient on beta-blocker: "
        "metoprolol, carvedilol, bisoprolol)\n"
        "| Dobutamine: β1 agonist → requires receptor binding; "
        "competitive antagonism by beta-blocker reduces effectiveness\n"
        "→ CCRN KEY: Both dobutamine and milrinone raise cAMP → "
        "PKA activation → Ca²⁺ influx → inotropy. "
        "Different entry point: dobutamine at receptor level, "
        "milrinone at phosphodiesterase level. Same downstream result: "
        "increased contractility and decreased SVR.\n"
        "→ MASTERY NOTE: Milrinone disadvantages: long elimination "
        "half-life (~2.5h, up to 20h in severe renal failure); "
        "significant vasodilation (SVR↓↓) requires concurrent vasopressor "
        "in hypotensive patients; not easily reversible. "
        "In CKD: dose-reduce to 0.125–0.2 mcg/kg/min.",

        'tier-review',
        _VP,
        DID['vasopressors'],
        'inotrope_comparison',
        '{"hi":1}',
        'chart-l1'
    ),
    (
        "The inotrope chart shows milrinone causes greater SVR reduction "
        "than dobutamine. For a cardiogenic shock patient with MAP 58 "
        "started on milrinone, the nurse must simultaneously _______ "
        "and the monitoring triad is _______, _______, _______.",

        "Simultaneously: start or increase norepinephrine to counteract "
        "milrinone-induced vasodilation and maintain MAP ≥65\n"
        "| Monitoring triad: MAP ≥65 + Cardiac Index >2.2 L/min/m² "
        "+ evidence of organ perfusion (lactate clearing, "
        "UO ≥0.5 mL/kg/h, improving ScvO₂)\n"
        "→ CCRN KEY: Milrinone + norepinephrine: standard combination "
        "for cardiogenic shock on beta-blockade. Milrinone = inotropy "
        "without receptor stimulation; norepi = vasoconstriction to "
        "maintain perfusion pressure. Monitor for arrhythmias "
        "(less than dobutamine, but still arrhythmogenic).\n"
        "→ MASTERY NOTE: Levosimendan (Ca²⁺ sensitizer) improves "
        "inotropy WITHOUT increasing Ca²⁺ load — less arrhythmogenic. "
        "Single 24h infusion with effects lasting 7–9 days "
        "(active metabolite OR-1896). Not FDA-approved in US; "
        "available in Europe, Canada, Asia. Key trials: LIDO, SURVIVE.",

        'tier-high',
        _VP,
        DID['vasopressors'],
        'inotrope_comparison',
        '{"hi":0}',
        'chart-l2'
    ),
    (
        "A patient with LVEF 15%, on carvedilol 25 mg BID, develops "
        "cardiogenic shock (CI 1.5, PCWP 28). Inotropic support is "
        "initiated. The correct choice is _______, starting dose is "
        "_______, and the loading dose is _______.",

        "Milrinone (carvedilol blocks β1 AND α1 receptors — both "
        "dobutamine's binding sites are blocked)\n"
        "| Starting dose: 0.125–0.25 mcg/kg/min maintenance infusion\n"
        "| Loading dose: OMIT — IV bolus (50 mcg/kg) causes acute "
        "hypotension in cardiogenic shock patients; start maintenance "
        "only and titrate up q30min based on hemodynamic response\n"
        "→ CCRN KEY: Carvedilol = non-selective beta-blocker + α1 blocker. "
        "Blocks α1 (vasodilation) + β1/β2 (cardiac). "
        "Makes both phenylephrine and dobutamine partially ineffective. "
        "Milrinone bypasses all receptor-level blockade.\n"
        "→ MASTERY NOTE: Holding beta-blocker in cardiogenic shock is "
        "controversial — abrupt discontinuation risks rebound "
        "tachycardia/ischemia. Most guidelines: continue at reduced dose, "
        "use milrinone for inotropic support. "
        "If hemodynamics worsen: gradual beta-blocker taper "
        "over 24–48h while optimizing volume status.",

        'tier-critical',
        _VP,
        DID['vasopressors'],
        'inotrope_comparison',
        '{"hi":1}',
        'chart-l3'
    ),

    # ═══ pressor_titration ════════════════════════════════════════════════════
    (
        "On the MAP target chart, the Surviving Sepsis Campaign target "
        "for most septic shock patients is MAP _______ mmHg, "
        "based on the _______ trial, which showed that targeting "
        "MAP 80–85 resulted in _______.",

        "MAP ≥65 mmHg; SEPSISPAM trial (2014)\n"
        "| MAP 80–85 group: no improvement in mortality, AKI, or ICU LOS "
        "vs MAP 65–70; MAP 80–85 associated with 20% increase in atrial "
        "fibrillation and required significantly more norepinephrine\n"
        "→ CCRN KEY: SEPSISPAM (Asfar et al.): 776 patients, "
        "MAP 65–70 vs 80–85 mmHg in septic shock. "
        "No survival difference overall. "
        "Subgroup: chronic hypertension patients → MAP 80–85 reduced "
        "need for renal replacement therapy. "
        "Takeaway: individualize MAP target for HTN history.\n"
        "→ MASTERY NOTE: MAP is a means, not the endpoint. "
        "True perfusion endpoints: lactate ≤2 mmol/L (or "
        "≥10% clearance per 2h), UO ≥0.5 mL/kg/h, "
        "capillary refill <2 sec, ScvO₂ ≥70%, "
        "improving mottling score. Treat the organ, not the number.",

        'tier-review',
        _VP,
        DID['vasopressors'],
        'pressor_titration',
        '{"map":65}',
        'chart-l1'
    ),
    (
        "The MAP target chart shows a TBI patient with ICP 22 mmHg. "
        "MAP 68 is currently within the 'green zone' for septic shock, "
        "but is INADEQUATE for this patient because _______, "
        "and the correct target is _______.",

        "ICP 22 → CPP = MAP − ICP = 68 − 22 = 46 mmHg = inadequate "
        "cerebral perfusion (target CPP 60–70 mmHg)\n"
        "| Correct MAP target: ≥82–92 mmHg to achieve CPP ≥60–70 "
        "(MAP must be set based on CPP calculation, not MAP alone)\n"
        "→ CCRN KEY: Cerebral Perfusion Pressure = MAP − ICP. "
        "Target CPP 60–70 mmHg (Lund Protocol: avoid CPP >70 — "
        "aggressive catecholamine use causes pulmonary complications). "
        "Vasopressor of choice in TBI: norepinephrine "
        "(avoids dopamine-related glucose variability, less tachycardia "
        "than epinephrine).\n"
        "→ MASTERY NOTE: Spinal cord injury: MAP 85–90 mmHg for first "
        "5–7 days (preserves spinal cord perfusion pressure). "
        "Phenylephrine preferred for SCI: raises MAP via α1 "
        "without tachycardia; reflex bradycardia may actually benefit "
        "patients with neurogenic (bradycardic) presentation.",

        'tier-high',
        _VP,
        DID['vasopressors'],
        'pressor_titration',
        '{"map":68}',
        'chart-l2'
    ),
    (
        "Post-cardiac arrest patient 4 hours after ROSC on "
        "targeted temperature management (33°C). "
        "MAP 58, norepinephrine 0.3 mcg/kg/min. "
        "The MAP target for post-arrest TTM is _______ mmHg "
        "and the physiological reason for this target is _______.",

        "MAP target: 65–80 mmHg post-ROSC (most guidelines ≥65, "
        "many target 70–80 during TTM for neuroprotection)\n"
        "| Reason: cerebral autoregulation is impaired post-arrest — "
        "cerebral blood flow is pressure-passive during hypothermia; "
        "higher MAP improves cerebral perfusion when autoregulation "
        "is lost; vasodilation from hypothermia also increases "
        "vasopressor requirement\n"
        "→ CCRN KEY: TTM physiological effects on vasopressors: "
        "hypothermia → vasodilation (α-adrenergic receptor downregulation) "
        "→ increased vasopressor requirement; bradycardia (targeted, "
        "not pathological during TTM); HR 40–60 acceptable if "
        "cardiac output maintained.\n"
        "→ MASTERY NOTE: HYPERION trial and BOX trial data: "
        "MAP ≥70 during first 36h post-ROSC associated with better "
        "neurological outcomes in some analyses. "
        "ScvO₂ monitoring during TTM: goal >70%; hypothermia "
        "shifts oxyhemoglobin curve left → tissue may be well-oxygenated "
        "even at lower mixed venous saturation.",

        'tier-critical',
        _VP,
        DID['vasopressors'],
        'pressor_titration',
        '{"map":58}',
        'chart-l3'
    ),

    # ═══ vasopressor_weaning ══════════════════════════════════════════════════
    (
        "On the vasopressor weaning protocol chart, the three criteria "
        "that must be present before initiating wean are: "
        "MAP _______, lactate _______, and urine output _______. "
        "The FIRST agent removed in septic shock (norepi + vasopressin) is _______.",

        "MAP ≥65 mmHg sustained ×2h; lactate trending down (ideally "
        "<2 mmol/L or clearance ≥10%/2h); UO ≥0.5 mL/kg/h\n"
        "| First agent removed: vasopressin — wean in reverse order "
        "of addition; norepinephrine was primary and is removed last\n"
        "→ CCRN KEY: Vasopressin wean: 0.03 → 0.02 → 0.01 → off, "
        "monitoring MAP after each step (q30–60 min). "
        "Do not decrease two agents simultaneously in marginal stability. "
        "Check volume responsiveness (PLR test) before attributing "
        "MAP drop to vasopressor-dependency.\n"
        "→ MASTERY NOTE: Rapid vasopressor wean risk: "
        "relative adrenal insufficiency may unmask — "
        "if MAP falls despite adequate volume and no new cause, "
        "consider low-dose hydrocortisone 50 mg IV q6h (ADRENAL/APROCCHSS "
        "trial data: faster vasopressor liberation with corticosteroids).",

        'tier-review',
        _VP,
        DID['vasopressors'],
        'vasopressor_weaning',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "The weaning protocol shows Step 3: taper norepinephrine. "
        "During wean from 0.18 to 0.12 mcg/kg/min, the patient "
        "develops new fever (39.1°C), warm extremities, and MAP "
        "drops to 61. The correct response is _______, "
        "not _______, because _______.",

        "Correct: hold wean, restore to prior norepi dose, "
        "reassess for new infectious source (blood cultures, "
        "new CXR, urinalysis, reassess line sites)\n"
        "| Not: continue weaning on pre-set schedule\n"
        "| Because: new fever during vasopressor wean = possible new "
        "infection, inadequately controlled source, or unmasked sepsis — "
        "vasopressor requirement is increasing, not decreasing\n"
        "→ CCRN KEY: Predictors of failed vasopressor wean: "
        "new fever, rising lactate, falling UO, new arrhythmias, "
        "need to increase FiO₂. ANY new clinical deterioration = "
        "reassess before continuing wean protocol.\n"
        "→ MASTERY NOTE: Wean failure is a clinical signal, not a "
        "clinical failure. Document: dose at instability, time from "
        "last reduction, associated changes. Reinstituting vasopressors "
        "and investigating root cause is appropriate high-quality "
        "clinical judgment.",

        'tier-high',
        _VP,
        DID['vasopressors'],
        'vasopressor_weaning',
        '{"sel":2}',
        'chart-l2'
    ),
    (
        "Patient successfully weaned from vasopressors 6 hours ago, "
        "MAP 70. Suddenly MAP drops to 52. "
        "Patient is afebrile, cool extremities, JVD present, "
        "muffled heart sounds. This presentation is NOT "
        "vasopressor wean failure but rather _______, "
        "and vasopressors here serve as _______.",

        "Cardiac tamponade (Beck's triad: hypotension + JVD + "
        "muffled heart sounds) — obstructive shock from pericardial "
        "effusion (post-surgical, post-MI, procedural complication)\n"
        "| Vasopressors: bridge only — norepinephrine maintains "
        "perfusion pressure while preparing for emergency "
        "pericardiocentesis (definitive treatment)\n"
        "→ CCRN KEY: Beck's triad is a LATE sign. Earlier: "
        "pulsus paradoxus >10 mmHg (SBP drops >10 on inspiration), "
        "equalization of RA/RV/PCWP pressures on PA catheter, "
        "electrical alternans on ECG. POCUS is diagnostic: "
        "RA/RV diastolic collapse.\n"
        "→ MASTERY NOTE: Tamponade physiology: NO fluid boluses "
        "(already obstructive, more fluid worsens intrapericardial "
        "pressure). Pericardiocentesis: remove ≥50–100 mL for "
        "immediate hemodynamic improvement. "
        "Surgical drainage if blood is clotted/loculated "
        "(common after cardiac surgery — Beck's triad in "
        "post-op CABG patient = tamponade until proven otherwise).",

        'tier-critical',
        _VP,
        DID['vasopressors'],
        'vasopressor_weaning',
        '{"sel":3}',
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
