#!/usr/bin/env python3
"""chunk36_charts.py — Ph5 Renal: AKI, CRRT & Electrolytes (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_35.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_36.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c36')
CHUNK_NUM   = 36
MID_BASE    = 1_800_005_025
CHART_ORDER = ['aki_stages', 'crrt_modes', 'crrt_dose',
               'hyperkalemia_ecg', 'prerenal_intrinsic']

_RL = 'Ph5 · \U0001f7e0 T2 · Renal — AKI, CRRT & Electrolytes'

RF = {}

# ── Chart 1: KDIGO AKI Staging Table ─────────────────────────────────────────
RF['aki_stages'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;
    var curRatio = P.cr != null ? P.cr : 1.0;

    var stages=[
        {name:'Baseline', cr:'< 1.5×  (or Δ < 0.3 mg/dL)', uo:'Normal / ≥ 0.5 mL/kg/hr', col:'#4caf50'},
        {name:'Stage 1',  cr:'1.5–1.9×  or  Δ≥0.3 mg/dL (48h)', uo:'< 0.5 mL/kg/hr  ×  6–12 h', col:'#ffca28'},
        {name:'Stage 2',  cr:'2.0–2.9×  baseline',           uo:'< 0.5 mL/kg/hr  ×  ≥12 h',    col:'#ff7043'},
        {name:'Stage 3',  cr:'≥3×  or  ≥4.0 mg/dL  or  RRT', uo:'< 0.3 mL/kg/hr ×24 h  or  anuria ×12 h', col:'#ef5350'},
    ];

    function stageForRatio(r){
        if(r<1.5) return 0;
        if(r<2.0) return 1;
        if(r<3.0) return 2;
        return 3;
    }
    var activeStage = stageForRatio(curRatio);

    var colW=[90, 265, 265], rH=52, tL=0, tT=12;
    var hdrH=26;

    function draw(){
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);

        // Header row
        ['Stage','Creatinine Criteria','Urine Output Criteria'].forEach(function(h,ci){
            var x=tL; for(var k=0;k<ci;k++) x+=colW[k];
            ctx.fillStyle='#1c1c1c';
            ctx.fillRect(x, tT, colW[ci], hdrH);
            ctx.strokeStyle='#333'; ctx.lineWidth=1; ctx.strokeRect(x,tT,colW[ci],hdrH);
            ctx.fillStyle='#aaa'; ctx.font='bold 10px sans-serif'; ctx.textAlign='center';
            ctx.fillText(h, x+colW[ci]/2, tT+hdrH/2+4);
        });

        stages.forEach(function(s,ri){
            var y = tT+hdrH+ri*rH;
            var hl = ri===activeStage;
            for(var ci=0;ci<3;ci++){
                var x=tL; for(var k=0;k<ci;k++) x+=colW[k];
                ctx.fillStyle = hl ? s.col+'33' : (ri%2?'#111':'#0d0d0d');
                ctx.fillRect(x,y,colW[ci],rH);
                if(hl){ ctx.strokeStyle=s.col; ctx.lineWidth=2; }
                else  { ctx.strokeStyle='#222'; ctx.lineWidth=1; }
                ctx.strokeRect(x,y,colW[ci],rH);
            }
            // Stage name
            ctx.fillStyle = hl ? s.col : s.col+'99';
            ctx.font = 'bold '+(hl?'12':'11')+'px sans-serif';
            ctx.textAlign='center';
            ctx.fillText(s.name, tL+colW[0]/2, y+rH/2+4);
            // CR criteria
            ctx.fillStyle = hl ? '#eee' : '#888';
            ctx.font = (hl?'bold ':'')+'10px sans-serif'; ctx.textAlign='center';
            ctx.fillText(s.cr, tL+colW[0]+colW[1]/2, y+rH/2+4);
            // UO criteria
            ctx.fillStyle = hl ? '#eee' : '#888';
            ctx.fillText(s.uo, tL+colW[0]+colW[1]+colW[2]/2, y+rH/2+4);
        });

        // Slider label
        var stg=stages[activeStage];
        ctx.fillStyle=stg.col; ctx.font='bold 10px sans-serif'; ctx.textAlign='right';
        ctx.fillText('Cr ratio '+curRatio.toFixed(1)+'× → '+stg.name,
                     W-6, H-5);
    }
    draw();

    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;align-items:center;';
        row.appendChild(_mkS('Cr × Baseline', 1.0, 4.5, 0.1, curRatio,
            function(v){ return v.toFixed(1)+'×'; },
            function(v){ curRatio=v; P.cr=v; draw(); }));
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: CRRT Mode Comparison Table ───────────────────────────────────────
RF['crrt_modes'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;

    var rows=[
        ['Mechanism',        'Convection',              'Diffusion',                  'Both'],
        ['Driving force',    'Hydrostatic pressure',    'Concentration gradient',     'Hydrostatic + gradient'],
        ['Small solutes',    'Good',                    'Excellent',                  'Excellent'],
        ['Middle molecules', 'Excellent',               'Limited',                    'Good'],
        ['Replacement fluid','Required (pre/post)',     'None needed',                'Required + dialysate'],
        ['Dialysate',        'None',                    'Required',                   'Required'],
        ['Best for',         'Cytokine removal, sepsis','Standard AKI clearance',     'Versatile; standard ICU'],
    ];
    var modes=['CVVH','CVVHD','CVVHDF'];
    var mcols=['#29b6f6','#4caf50','#ce93d8'];
    var hi = P.hi != null ? P.hi : -1;

    var cW=[140, 160, 160, 160], rH=30, tT=10;

    function draw(){
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);

        // Header
        var hdrs=['Feature'].concat(modes);
        hdrs.forEach(function(h,ci){
            var x=0; for(var k=0;k<ci;k++) x+=cW[k];
            var dim=hi>=0&&hi!==ci-1&&ci>0;
            ctx.fillStyle=ci===0?'#1c1c1c':(dim?mcols[ci-1]+'11':mcols[ci-1]+'33');
            ctx.fillRect(x,tT,cW[ci],30);
            ctx.strokeStyle=ci===0?'#333':(dim?mcols[ci-1]+'44':mcols[ci-1]);
            ctx.lineWidth=ci>0?2:1; ctx.strokeRect(x,tT,cW[ci],30);
            ctx.fillStyle=ci===0?'#aaa':(dim?mcols[ci-1]+'66':mcols[ci-1]);
            ctx.font='bold 11px sans-serif'; ctx.textAlign='center';
            ctx.fillText(h, x+cW[ci]/2, tT+20);
        });

        rows.forEach(function(r,ri){
            var y=tT+30+ri*rH;
            r.forEach(function(cell,ci){
                var x=0; for(var k=0;k<ci;k++) x+=cW[k];
                var dim=hi>=0&&hi!==ci-1&&ci>0;
                ctx.fillStyle=ci===0?(ri%2?'#111':'#0d0d0d'):
                    (dim?mcols[ci-1]+'08':(ri%2?mcols[ci-1]+'18':mcols[ci-1]+'10'));
                ctx.fillRect(x,y,cW[ci],rH);
                ctx.strokeStyle=ci===0?'#222':(dim?mcols[ci-1]+'22':mcols[ci-1]+'44');
                ctx.lineWidth=1; ctx.strokeRect(x,y,cW[ci],rH);
                ctx.fillStyle=ci===0?'#999':(dim?mcols[ci-1]+'55':mcols[ci-1]+'dd');
                ctx.font='9px sans-serif'; ctx.textAlign=ci===0?'left':'center';
                ctx.fillText(cell, ci===0?x+5:x+cW[ci]/2, y+rH/2+4);
            });
        });
    }
    draw();

    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;align-items:center;';
        var sp=document.createElement('span');
        sp.style.cssText='font-size:10px;font-weight:800;color:#666;';
        sp.textContent='FOCUS:'; row.appendChild(sp);
        var btns=[];
        modes.forEach(function(m,i){
            var b=_mkB(m,mcols[i],hi===i,function(on){
                hi=on?i:-1; P.hi=hi;
                btns.forEach(function(x,j){
                    x._on=j===i&&on;
                    x.style.background=x._on?mcols[j]+'22':'transparent';
                    x.style.color=x._on?mcols[j]:'#555';
                });
                draw();
            });
            btns.push(b); row.appendChild(b);
        });
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 3: CRRT Dose Calculator ────────────────────────────────────────────
RF['crrt_dose'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;
    var curWt=P.wt||70, curRate=P.rate||1500;

    function draw(){
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);
        var dose=curRate/curWt;
        var col=dose<15?_RE:dose<=25?_GN:dose<=30?_AM:_RE;

        // Large dose display
        ctx.fillStyle=col; ctx.font='bold 54px sans-serif'; ctx.textAlign='center';
        ctx.fillText(dose.toFixed(1), W/2, 80);
        ctx.fillStyle='#888'; ctx.font='14px sans-serif';
        ctx.fillText('mL/kg/hr', W/2, 100);

        // Formula display
        ctx.fillStyle='#555'; ctx.font='11px sans-serif';
        ctx.fillText('Effluent '+curRate+' mL/hr  ÷  Weight '+curWt+' kg', W/2, 126);

        // Target range gauge
        var gx=40, gy=140, gw=W-80, gh=22;
        var minD=5, maxD=50, dRange=maxD-minD;
        function dp(v){return gx+(v-minD)/dRange*gw;}

        // Zones
        ctx.fillStyle='#ef535022'; ctx.fillRect(gx,gy,dp(15)-gx,gh);
        ctx.fillStyle='#ffca2822'; ctx.fillRect(dp(15),gy,dp(20)-dp(15),gh);
        ctx.fillStyle='#4caf5033'; ctx.fillRect(dp(20),gy,dp(25)-dp(20),gh);
        ctx.fillStyle='#ffca2822'; ctx.fillRect(dp(25),gy,dp(30)-dp(25),gh);
        ctx.fillStyle='#ef535022'; ctx.fillRect(dp(30),gy,dp(50)-dp(30),gh);
        ctx.strokeStyle='#333'; ctx.lineWidth=1; ctx.strokeRect(gx,gy,gw,gh);

        // Target zone label
        ctx.fillStyle='#4caf5099'; ctx.font='9px sans-serif'; ctx.textAlign='center';
        ctx.fillText('TARGET 20–25',dp(22.5),gy+gh/2+3);
        ctx.fillStyle='#ef535066';
        ctx.fillText('Sub-therapeutic',dp(10),gy+gh/2+3);
        ctx.fillStyle='#ef535066';
        ctx.fillText('Supra',dp(38),gy+gh/2+3);

        // Tick marks
        [15,20,25,30].forEach(function(v){
            ctx.strokeStyle='#555'; ctx.lineWidth=1;
            ctx.beginPath(); ctx.moveTo(dp(v),gy); ctx.lineTo(dp(v),gy+gh); ctx.stroke();
            ctx.fillStyle='#666'; ctx.font='9px sans-serif'; ctx.textAlign='center';
            ctx.fillText(v,dp(v),gy+gh+11);
        });
        ctx.fillStyle='#555'; ctx.font='9px sans-serif'; ctx.textAlign='center';
        ctx.fillText('mL/kg/hr', gx+gw/2, gy+gh+22);

        // Patient marker
        var px=Math.max(gx,Math.min(gx+gw,dp(dose)));
        ctx.fillStyle=col;
        ctx.beginPath(); ctx.moveTo(px,gy-2); ctx.lineTo(px-6,gy-12); ctx.lineTo(px+6,gy-12); ctx.closePath(); ctx.fill();

        // Verdict
        var verdict=dose<15?'SUB-THERAPEUTIC — increase rate':
                    dose<=25?'WITHIN TARGET (20–25 mL/kg/hr)':
                    dose<=30?'ABOVE TARGET — verify order':
                             'EXCESSIVE — reduce rate';
        ctx.fillStyle=col; ctx.font='bold 11px sans-serif'; ctx.textAlign='center';
        ctx.fillText(verdict, W/2, gy+gh+40);

        // Note
        ctx.fillStyle='#444'; ctx.font='9px sans-serif';
        ctx.fillText('KDIGO target: 20–25 mL/kg/hr effluent dose (prescribe 25–30 to achieve 20–25 actual)',
                     W/2, H-5);
    }
    draw();

    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;align-items:center;';
        row.appendChild(_mkS('Weight',30,130,5,curWt,
            function(v){return v.toFixed(0)+' kg';},
            function(v){curWt=v;P.wt=v;draw();}));
        row.appendChild(_mkS('Effluent',500,3000,100,curRate,
            function(v){return v.toFixed(0)+' mL/hr';},
            function(v){curRate=v;P.rate=v;draw();}));
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 4: Hyperkalemia ECG Progression ─────────────────────────────────────
RF['hyperkalemia_ecg'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;
    var curK = P.k != null ? P.k : 5.5;

    var bands=[
        {lo:2.5, hi:3.5, label:'Hypokalemia',  sub:'Flat T, U wave prominent',     col:'#29b6f6'},
        {lo:3.5, hi:5.0, label:'Normal',        sub:'Normal P, QRS, T',             col:'#4caf50'},
        {lo:5.0, hi:6.0, label:'Mild Hyper-K',  sub:'Peaked (tented) T waves',      col:'#ffca28'},
        {lo:6.0, hi:7.0, label:'Moderate',      sub:'PR prolonged, P wave flattens',col:'#ff7043'},
        {lo:7.0, hi:8.0, label:'Severe',        sub:'Wide QRS, P disappears',       col:'#ef5350'},
        {lo:8.0, hi:9.0, label:'Critical',      sub:'Sine wave → VF / asystole',col:'#ce93d8'},
    ];

    var treatments=[
        {k:5.5, tx:'Kayexalate/patiromer, dietary K⁺ restriction', col:'#ffca28'},
        {k:6.0, tx:'Insulin 10u + D50, repeat ECG stat',              col:'#ff7043'},
        {k:6.5, tx:'Calcium gluconate 1–2g IV (membrane stabilization)', col:'#ef5350'},
        {k:7.0, tx:'Sodium bicarb, albuterol neb, emergent dialysis', col:'#ce93d8'},
    ];

    var mx=54, my=10, pw=W-mx-12, ph=H-my-80;
    var kLo=2.5, kHi=9.0, kR=kHi-kLo;
    function xp(v){return mx+(v-kLo)/kR*pw;}

    function activeBand(k){
        for(var i=0;i<bands.length;i++) if(k<bands[i].hi) return i;
        return bands.length-1;
    }
    var ab=activeBand(curK);

    function draw(){
        ab=activeBand(curK);
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);

        // Band rectangles
        bands.forEach(function(b,i){
            var dim=i!==ab;
            ctx.fillStyle=b.col+(dim?'18':'33');
            ctx.fillRect(xp(b.lo),my,xp(b.hi)-xp(b.lo),ph);
            // vertical dividers
            ctx.strokeStyle='#333'; ctx.lineWidth=1; ctx.setLineDash([2,3]);
            ctx.beginPath(); ctx.moveTo(xp(b.hi),my); ctx.lineTo(xp(b.hi),my+ph); ctx.stroke();
            ctx.setLineDash([]);
            // labels
            var mid=(xp(b.lo)+xp(b.hi))/2;
            ctx.fillStyle=b.col+(dim?'55':'ff');
            ctx.font='bold 9px sans-serif'; ctx.textAlign='center';
            ctx.fillText(b.label, mid, my+14);
            ctx.fillStyle=b.col+(dim?'44':'cc');
            ctx.font='8px sans-serif';
            // wrap sub-label across two lines if needed
            var words=b.sub.split(', ');
            ctx.fillText(words[0], mid, my+27);
            if(words[1]) ctx.fillText(words[1], mid, my+38);
        });

        // Axes
        _ax(ctx,mx,my,pw,ph);
        ctx.fillStyle='#888'; ctx.font='10px sans-serif'; ctx.textAlign='center';
        [3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0].forEach(function(v){
            ctx.fillText(v.toFixed(1), xp(v), my+ph+12);
        });
        ctx.fillText('Serum K⁺ (mEq/L)', mx+pw/2, my+ph+24);
        _rl(ctx,'ECG Severity',14,my+ph/2);

        // Treatment threshold markers
        treatments.forEach(function(t){
            ctx.strokeStyle=t.col; ctx.lineWidth=1.5; ctx.setLineDash([4,3]);
            ctx.beginPath(); ctx.moveTo(xp(t.k),my); ctx.lineTo(xp(t.k),my+ph); ctx.stroke();
            ctx.setLineDash([]);
        });

        // Patient marker
        var px=xp(curK);
        ctx.fillStyle=bands[ab].col;
        ctx.beginPath(); ctx.arc(px, my+ph/2, 7, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle='#000'; ctx.font='bold 8px sans-serif'; ctx.textAlign='center';
        ctx.fillText(curK.toFixed(1), px, my+ph/2+3);

        // Active treatment
        var aTx=null;
        for(var i=treatments.length-1;i>=0;i--) if(curK>=treatments[i].k){ aTx=treatments[i]; break; }
        if(aTx){
            ctx.fillStyle=aTx.col; ctx.font='bold 9px sans-serif'; ctx.textAlign='center';
            ctx.fillText('▶ '+aTx.tx, mx+pw/2, my+ph+38);
        } else {
            ctx.fillStyle=bands[ab].col; ctx.font='bold 9px sans-serif'; ctx.textAlign='center';
            ctx.fillText('K⁺ '+curK.toFixed(1)+' — '+bands[ab].label+': '+bands[ab].sub,
                mx+pw/2, my+ph+38);
        }
    }
    draw();

    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;align-items:center;';
        row.appendChild(_mkS('K⁺',2.5,9.0,0.1,curK,
            function(v){return v.toFixed(1)+' mEq/L';},
            function(v){curK=v;P.k=v;draw();}));
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 5: Prerenal vs Intrinsic AKI (ATN) vs Postrenal ────────────────────
RF['prerenal_intrinsic'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;

    var rows=[
        {label:'FeNa',            pre:'< 1%',          atn:'> 2%',                  post:'Variable'},
        {label:'BUN : Cr ratio',  pre:'> 20 : 1',      atn:'< 15 : 1',              post:'Variable'},
        {label:'Urine Na',        pre:'< 20 mEq/L',    atn:'> 40 mEq/L',            post:'Variable'},
        {label:'Urine Sp. Grav.', pre:'> 1.020',       atn:'≈1.010 (isosthenuria)', post:'Variable'},
        {label:'Urine sediment',  pre:'Normal / hyaline','atn':'Muddy brown granular casts', post:'Normal'},
        {label:'Response to IVF', pre:'Improves',      atn:'No improvement',         post:'Partial improve'},
        {label:'Etiology',        pre:'Volume depletion\ndehydration\nheart failure', atn:'Ischemia\nnephrotoxins\nsepsis', post:'Obstruction\nBPH, stones\nneurogenic'},
    ];

    var cols=['#29b6f6','#ef5350','#ff7043'];
    var hi=P.hi!=null?P.hi:-1;

    var cW=[108,171,171,170], rH=30, hdrH=28, tT=10;
    // last row gets double height for etiology
    var lastH=44;

    function draw(){
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);

        // Header
        ['Finding','Prerenal','ATN / Intrinsic','Postrenal'].forEach(function(h,ci){
            var x=0; for(var k=0;k<ci;k++) x+=cW[k];
            var dim=hi>=0&&hi!==ci-1&&ci>0;
            ctx.fillStyle=ci===0?'#1c1c1c':(dim?cols[ci-1]+'11':cols[ci-1]+'33');
            ctx.fillRect(x,tT,cW[ci],hdrH);
            ctx.strokeStyle=ci===0?'#333':(dim?cols[ci-1]+'44':cols[ci-1]);
            ctx.lineWidth=ci>0?2:1; ctx.strokeRect(x,tT,cW[ci],hdrH);
            ctx.fillStyle=ci===0?'#aaa':(dim?cols[ci-1]+'66':cols[ci-1]);
            ctx.font='bold 10px sans-serif'; ctx.textAlign='center';
            ctx.fillText(h, x+cW[ci]/2, tT+hdrH/2+4);
        });

        var y=tT+hdrH;
        rows.forEach(function(r,ri){
            var isLast=(ri===rows.length-1);
            var rowH=isLast?lastH:rH;
            for(var ci=0;ci<4;ci++){
                var x=0; for(var k=0;k<ci;k++) x+=cW[k];
                var dim=hi>=0&&hi!==ci-1&&ci>0;
                ctx.fillStyle=ci===0?(ri%2?'#111':'#0d0d0d'):
                    (dim?cols[ci-1]+'08':(ri%2?cols[ci-1]+'18':cols[ci-1]+'10'));
                ctx.fillRect(x,y,cW[ci],rowH);
                ctx.strokeStyle=ci===0?'#222':(dim?cols[ci-1]+'22':cols[ci-1]+'44');
                ctx.lineWidth=1; ctx.strokeRect(x,y,cW[ci],rowH);

                var vals=[r.label,r.pre,r.atn,r.post];
                var cell=vals[ci];
                ctx.fillStyle=ci===0?'#999':(dim?cols[ci-1]+'55':cols[ci-1]+'dd');
                ctx.font='9px sans-serif'; ctx.textAlign=ci===0?'left':'center';
                if(isLast&&ci>0){
                    var lines=cell.split('\n');
                    lines.forEach(function(ln,j){
                        ctx.fillText(ln, ci===0?x+5:x+cW[ci]/2, y+13+(j*13));
                    });
                } else {
                    ctx.fillText(cell, ci===0?x+5:x+cW[ci]/2, y+rowH/2+4);
                }
            }
            y+=rowH;
        });
    }
    draw();

    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;align-items:center;';
        var sp=document.createElement('span');
        sp.style.cssText='font-size:10px;font-weight:800;color:#666;';
        sp.textContent='FOCUS:'; row.appendChild(sp);
        var hdr=['Prerenal','ATN','Postrenal'];
        var btns=[];
        hdr.forEach(function(l,i){
            var b=_mkB(l,cols[i],hi===i,function(on){
                hi=on?i:-1; P.hi=hi;
                btns.forEach(function(x,j){
                    x._on=j===i&&on;
                    x.style.background=x._on?cols[j]+'22':'transparent';
                    x.style.color=x._on?cols[j]:'#555';
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
CARDS = [
    # ═══ aki_stages ══════════════════════════════════════════════════════════
    (
        "On the KDIGO AKI staging chart, Stage 2 AKI is defined by a serum "
        "creatinine ratio of _______ times baseline, or urine output _______.",

        "Creatinine 2.0–2.9× baseline\n"
        "| Urine output < 0.5 mL/kg/hr for ≥12 hours\n"
        "→ CCRN KEY: KDIGO stages: Stage 1 (1.5–1.9× or +0.3 mg/dL), "
        "Stage 2 (2.0–2.9×), Stage 3 (≥3× or ≥4.0 mg/dL absolute or RRT). "
        "Either creatinine OR urine output criteria alone qualifies.\n"
        "→ MASTERY NOTE: AKI staging drives intervention urgency. "
        "Stage 3 = highest mortality and strongest RRT indication. "
        "The KDIGO UO criterion is often met hours before the creatinine rises — "
        "oliguria is an earlier warning sign.",

        'tier-review',
        _RL,
        DID['renal_crrt'],
        'aki_stages',
        '{"cr":2.4}',
        'chart-l1'
    ),
    (
        "A post-cardiac-surgery patient's creatinine rises from 1.0 to 3.2 mg/dL "
        "over 48 hours. On the AKI chart, this represents Stage _______, "
        "and the primary mechanism is _______.",

        "Stage 3 AKI (3.2× baseline)\n"
        "| Primary mechanism: renal ischemia from reduced cardiac output, "
        "hypoperfusion during CPB, and contrast from intraoperative imaging\n"
        "→ CCRN KEY: Post-cardiac surgery AKI is Stage 3 when Cr ≥3× baseline. "
        "Cardiac surgery is the #2 cause of ICU-acquired AKI (sepsis is #1). "
        "Cardiopulmonary bypass causes hemodilution, microemboli, and non-pulsatile flow.\n"
        "→ MASTERY NOTE: Avoid nephrotoxins (NSAIDs, aminoglycosides, IV contrast) in "
        "all AKI. Optimize hemodynamics: MAP ≥65 mmHg minimum, "
        "MAP ≥80 in CKD patients with hypertensive history.",

        'tier-high',
        _RL,
        DID['renal_crrt'],
        'aki_stages',
        '{"cr":3.2}',
        'chart-l2'
    ),
    (
        "Septic patient: creatinine rises from 0.9 to 2.1 mg/dL, urine output "
        "0.3 mL/kg/hr for 18 hours. AKI stage = _______. Fluid resuscitation "
        "has been completed. Next intervention is _______, not _______, "
        "because _______.",

        "Stage 2 AKI (creatinine 2.3×, UO < 0.5 mL/kg/hr ≥12h)\n"
        "| Next: optimize MAP ≥65 with vasopressors if fluid-resuscitated; "
        "hold nephrotoxins; consider nephrology consult for Stage 2 in ICU\n"
        "| Not: aggressive additional fluid boluses without hemodynamic indication\n"
        "| Because: after adequate resuscitation, fluid overload in AKI increases "
        "mortality — positive fluid balance >10% body weight independently worsens outcomes\n"
        "→ CCRN KEY: Stage 2+ AKI after fluid resuscitation = vasopressor optimization "
        "and nephrotoxin avoidance, not more fluid. Monitor hourly UO and trending Cr.\n"
        "→ MASTERY NOTE: Furosemide does NOT prevent AKI progression or reduce need for "
        "dialysis — use only for volume overload management, not to make urine.",

        'tier-critical',
        _RL,
        DID['renal_crrt'],
        'aki_stages',
        '{"cr":2.3}',
        'chart-l3'
    ),

    # ═══ crrt_modes ══════════════════════════════════════════════════════════
    (
        "On the CRRT modes chart, the mode that removes middle molecules "
        "(cytokines) most effectively through convection is _______.",

        "CVVH (Continuous Veno-Venous Hemofiltration)\n"
        "| Mechanism: convection — hydrostatic pressure drives fluid and solutes "
        "through the membrane (solute drag)\n"
        "| Replacement fluid required pre- or post-filter to replace lost volume\n"
        "→ CCRN KEY: CVVH uses convection → best middle-molecule clearance (cytokines, "
        "β2-microglobulin). CVVHD uses diffusion → best small-solute clearance. "
        "CVVHDF combines both mechanisms.\n"
        "→ MASTERY NOTE: In septic shock, CVVH is often preferred for "
        "potential cytokine removal, though clinical benefit remains debated. "
        "Most North American ICUs default to CVVHDF for versatility.",

        'tier-review',
        _RL,
        DID['renal_crrt'],
        'crrt_modes',
        '{}',
        'chart-l1'
    ),
    (
        "The CRRT comparison chart shows CVVHD requires dialysate fluid but no "
        "replacement fluid. This differs from CVVH because _______.",

        "CVVHD uses diffusion (concentration gradient across membrane) as its "
        "primary mechanism — solutes move from high-concentration blood into "
        "low-concentration dialysate without bulk fluid removal\n"
        "| CVVH uses convection — bulk fluid (ultrafiltrate) is removed by pressure, "
        "carrying solutes with it; replacement fluid restores volume\n"
        "→ CCRN KEY: Diffusion (CVVHD) = excellent small-solute clearance, "
        "limited middle molecules. Convection (CVVH) = excellent middle molecules, "
        "good small solutes. Think: diffusion = dialysis, convection = filtration.\n"
        "→ MASTERY NOTE: Nurses manage replacement fluid and dialysate bags separately "
        "in CVVHDF. Both rates are prescribed — confusing them is a critical error. "
        "Always verify the circuit configuration with the Prismaflex/NxStage order set.",

        'tier-high',
        _RL,
        DID['renal_crrt'],
        'crrt_modes',
        '{}',
        'chart-l2'
    ),
    (
        "A 90 kg patient on CVVHDF has effluent rate set at 1,350 mL/hr. "
        "The CRRT dose chart shows _______ mL/kg/hr. This is _______ the "
        "KDIGO target, so you should _______.",

        "Dose = 1,350 ÷ 90 = 15 mL/kg/hr — below KDIGO target\n"
        "| KDIGO target: 20–25 mL/kg/hr effluent dose\n"
        "| Action: notify provider — prescription should be increased to "
        "25–30 mL/kg/hr to achieve actual dose of 20–25 (accounting for filter "
        "downtime and clotting losses)\n"
        "→ CCRN KEY: KDIGO recommends 20–25 mL/kg/hr effluent dose. "
        "Prescribe 25–30 mL/kg/hr to account for 15–20% downtime. "
        "Sub-therapeutic dosing = inadequate solute/fluid removal.\n"
        "→ MASTERY NOTE: Effluent = ultrafiltrate + dialysate. "
        "In CVVH: effluent = ultrafiltrate alone. "
        "Document actual delivered dose per shift, not just prescribed dose.",

        'tier-critical',
        _RL,
        DID['renal_crrt'],
        'crrt_modes',
        '{}',
        'chart-l3'
    ),

    # ═══ crrt_dose ════════════════════════════════════════════════════════════
    (
        "On the CRRT dose calculator, for a 70 kg patient the effluent rate "
        "needed to achieve the KDIGO target of 20–25 mL/kg/hr is _______.",

        "Target effluent rate = 20–25 mL/kg/hr × 70 kg = 1,400–1,750 mL/hr\n"
        "| Prescribe 25–30 mL/kg/hr (1,750–2,100 mL/hr) to achieve actual "
        "dose of 20–25, accounting for filter downtime\n"
        "→ CCRN KEY: KDIGO target is 20–25 mL/kg/hr effluent dose. "
        "Use actual (not ideal) body weight for obese patients to avoid overdosing. "
        "Effluent rate = ultrafiltrate ± dialysate depending on mode.\n"
        "→ MASTERY NOTE: Delivered dose in practice is ~15–20% less than prescribed "
        "due to filter clotting, line flushes, and circuit downtime for labs/procedures. "
        "Higher prescriptions compensate for this loss.",

        'tier-review',
        _RL,
        DID['renal_crrt'],
        'crrt_dose',
        '{"wt":70,"rate":1750}',
        'chart-l1'
    ),
    (
        "A 55 kg patient's CRRT is running at 2,000 mL/hr effluent. "
        "The dose calculator shows _______ mL/kg/hr — this is _______ "
        "and may cause _______.",

        "Dose = 2,000 ÷ 55 = 36.4 mL/kg/hr — well above KDIGO target (20–25)\n"
        "| Risk: electrolyte depletion (hypophosphatemia, hypomagnesemia, "
        "hypokalemia), hypothermia from over-rapid fluid cooling, "
        "removal of essential nutrients and medications\n"
        "→ CCRN KEY: Supra-therapeutic CRRT dose (>35 mL/kg/hr) does not improve "
        "outcomes and increases electrolyte depletion risk. "
        "Monitor phosphorus, magnesium, and potassium every 6 hours on CRRT.\n"
        "→ MASTERY NOTE: Drug dosing on CRRT is complex — highly variable clearance. "
        "Anti-infectives (vancomycin, piperacillin-tazobactam) require dose "
        "adjustment and therapeutic drug monitoring. Pharmacy consultation is essential.",

        'tier-high',
        _RL,
        DID['renal_crrt'],
        'crrt_dose',
        '{"wt":55,"rate":2000}',
        'chart-l2'
    ),
    (
        "An 85 kg anuric patient is prescribed 2,100 mL/hr CRRT. "
        "Morning labs: phosphorus 1.1 mg/dL, magnesium 1.4 mEq/L, "
        "potassium 3.0 mEq/L. Dose = _______ mL/kg/hr. "
        "These electrolyte findings are caused by _______ and you _______.",

        "Dose = 2,100 ÷ 85 = 24.7 mL/kg/hr (within target)\n"
        "| Cause: CRRT continuously removes small electrolytes (phosphorus, "
        "magnesium, potassium) via diffusion/convection; repletion in circuit "
        "bags or IV supplements is required\n"
        "| Action: replace electrolytes IV; notify provider for CRRT solution "
        "adjustment (add phosphorus to dialysate/replacement bags if available); "
        "do NOT hold CRRT without provider order\n"
        "→ CCRN KEY: CRRT-induced hypophosphatemia is common and underrecognized. "
        "Phosphorus replacement 15–30 mmol/day often required. "
        "Hypomagnesemia and hypokalemia also need aggressive replacement.\n"
        "→ MASTERY NOTE: Hypothermia is a CRRT complication — blood cools as it "
        "traverses the extracorporeal circuit. Use circuit heaters; target normothermia.",

        'tier-critical',
        _RL,
        DID['renal_crrt'],
        'crrt_dose',
        '{"wt":85,"rate":2100}',
        'chart-l3'
    ),

    # ═══ hyperkalemia_ecg ════════════════════════════════════════════════════
    (
        "On the hyperkalemia ECG progression chart, peaked (tented) T waves "
        "first appear at K⁺ approximately _______ mEq/L. The first treatment "
        "initiated at K⁺ ≥6.0–6.5 is _______, given because _______.",

        "Peaked T waves: K⁺ ~5.0–6.0 mEq/L\n"
        "| First treatment at K⁺ ≥6.0: calcium gluconate 1–2g IV (or calcium chloride)\n"
        "| Given because: calcium stabilizes the cardiac membrane (increases threshold "
        "potential), protecting against arrhythmia — it does NOT lower K⁺\n"
        "→ CCRN KEY: ECG progression: peaked T → PR prolongation → P wave loss → "
        "wide QRS → sine wave → VF. Calcium gluconate at K⁺ ≥6.0 or any ECG change. "
        "Onset in 1–3 min, duration 30–60 min (bridge only).\n"
        "→ MASTERY NOTE: Calcium chloride contains 3× more elemental calcium than "
        "calcium gluconate but causes severe tissue necrosis if it extravasates — "
        "give only through central line. Calcium gluconate is safe peripherally.",

        'tier-review',
        _RL,
        DID['renal_crrt'],
        'hyperkalemia_ecg',
        '{"k":5.5}',
        'chart-l1'
    ),
    (
        "The hyperkalemia chart shows a patient at K⁺ 7.2 mEq/L with wide QRS "
        "on ECG. Immediate treatment sequence is _______, then _______, "
        "then _______.",

        "Step 1: Calcium gluconate 1–2g IV STAT (membrane stabilization, fastest onset)\n"
        "| Step 2: Insulin 10 units regular IV + D50W 50 mL (shifts K⁺ into cells, "
        "onset 15–30 min, lasts 4–6 hr)\n"
        "| Step 3: Sodium bicarbonate 50–150 mEq IV (shifts K⁺ into cells via "
        "alkalosis, especially if pH <7.2)\n"
        "→ CCRN KEY: K⁺ >7.0 + wide QRS = life-threatening emergency. "
        "Treat simultaneously if possible. All three above are temporizing — "
        "K⁺ is shifted, not eliminated. Elimination requires kayexalate, "
        "furosemide (if UO present), or emergent dialysis.\n"
        "→ MASTERY NOTE: Albuterol 10–20 mg nebulized shifts K⁺ ~0.5–1.5 mEq/L "
        "within 30 min — underused but highly effective adjunct. "
        "Continuous cardiac monitoring mandatory throughout treatment.",

        'tier-high',
        _RL,
        DID['renal_crrt'],
        'hyperkalemia_ecg',
        '{"k":7.2}',
        'chart-l2'
    ),
    (
        "ESRD patient on CRRT circuit alarm, K⁺ 8.1 mEq/L on labs, ECG shows "
        "sine wave pattern. On the chart this is _______ range. "
        "You call the provider and initiate _______ as the definitive treatment "
        "because _______, and simultaneously do _______.",

        "K⁺ 8.1 = Critical range (sine wave → imminent VF/asystole)\n"
        "| Definitive: emergent dialysis (hemodialysis or CRRT restart) — "
        "only modality that actually removes K⁺ from the body rapidly\n"
        "| Because: calcium/insulin/bicarb only shift K⁺ temporarily; "
        "at K⁺ >8.0 with sine wave the risk of VF is immediate\n"
        "| Simultaneously: calcium gluconate 1–2g IV STAT, insulin 10u + D50, "
        "continuous cardiac monitoring, crash cart at bedside, code team notification\n"
        "→ CCRN KEY: Sine wave ECG = imminent VF. Treat aggressively while pursuing "
        "definitive elimination. If CRRT circuit is clotted and unavailable, "
        "intermittent HD must be emergently arranged.\n"
        "→ MASTERY NOTE: Sodium polystyrene sulfonate (Kayexalate) and patiromer "
        "bind K⁺ in the gut — onset 2–6 hours, NOT appropriate for emergency management.",

        'tier-critical',
        _RL,
        DID['renal_crrt'],
        'hyperkalemia_ecg',
        '{"k":8.1}',
        'chart-l3'
    ),

    # ═══ prerenal_intrinsic ══════════════════════════════════════════════════
    (
        "On the prerenal vs ATN comparison chart, a FeNa of _______ % "
        "distinguishes prerenal AKI from ATN (intrinsic renal failure).",

        "Prerenal AKI: FeNa < 1% (kidney aggressively reabsorbs Na⁺ to preserve volume)\n"
        "| ATN/Intrinsic: FeNa > 2% (tubular damage impairs Na⁺ reabsorption)\n"
        "| Formula: FeNa = (Urine Na × Plasma Cr) / (Plasma Na × Urine Cr) × 100\n"
        "→ CCRN KEY: FeNa < 1% = prerenal (or other causes of intact tubular function). "
        "FeNa > 2% = intrinsic (ATN). Gray zone 1–2% is indeterminate. "
        "BUN:Cr > 20:1 also suggests prerenal (urea reabsorbed with water).\n"
        "→ MASTERY NOTE: FeNa is UNRELIABLE in patients on diuretics "
        "(FeNa artificially elevated). Use FEUrea instead: "
        "FEUrea < 35% suggests prerenal even on diuretics.",

        'tier-review',
        _RL,
        DID['renal_crrt'],
        'prerenal_intrinsic',
        '{}',
        'chart-l1'
    ),
    (
        "The comparison chart shows prerenal AKI has urine specific gravity > 1.020 "
        "while ATN shows ~1.010 (isosthenuria). This difference occurs because "
        "_______.",

        "Prerenal: intact tubular function — ADH stimulation causes maximum water "
        "reabsorption → concentrated urine (SG > 1.020, osmolality > 500 mOsm/kg)\n"
        "| ATN: tubular cell damage impairs concentrating ability → isosthenuria "
        "(SG ~1.010 = same as plasma osmolality ~280–300 mOsm/kg)\n"
        "→ CCRN KEY: Isosthenuria (SG ~1.010, urine Osm ~300) = hallmark of "
        "tubular dysfunction in ATN. Muddy brown granular casts (sloughed tubular "
        "cells) in urine sediment confirm ATN.\n"
        "→ MASTERY NOTE: Contrast nephropathy and myoglobinuria (rhabdomyolysis) "
        "cause intrinsic AKI but may have FeNa < 1% due to intense vasoconstriction — "
        "these are exceptions where FeNa is misleading for distinguishing ATN.",

        'tier-high',
        _RL,
        DID['renal_crrt'],
        'prerenal_intrinsic',
        '{}',
        'chart-l2'
    ),
    (
        "ICU patient post-cardiac arrest: creatinine rising, urine output "
        "0.2 mL/kg/hr despite 3L IVF. FeNa 3.2%, BUN:Cr 10:1, urine sediment "
        "shows muddy brown casts. The chart pattern matches _______, caused by "
        "_______. You prioritize _______, not _______, because _______.",

        "ATN (Acute Tubular Necrosis) — all findings consistent\n"
        "| Cause: ischemic ATN from cardiac arrest and post-resuscitation "
        "low-flow state (global ischemia → tubular cell death)\n"
        "| Priority: optimize MAP ≥65 mmHg with vasopressors, avoid nephrotoxins, "
        "nephrology consult for dialysis planning\n"
        "| Not: more aggressive fluid boluses (will not reverse ATN)\n"
        "| Because: ATN is established tubular injury — volume loading after "
        "adequate resuscitation causes fluid overload without improving renal function\n"
        "→ CCRN KEY: Muddy brown casts + FeNa >2% + BUN:Cr <15 = ATN confirmed. "
        "ATN is self-limited (recovery 1–3 weeks) if the cause is removed and "
        "hemodynamics are optimized.\n"
        "→ MASTERY NOTE: Post-cardiac arrest ATN often requires temporary dialysis "
        "as a bridge to recovery. Most ATN patients recover sufficient renal function "
        "to discontinue RRT within weeks.",

        'tier-critical',
        _RL,
        DID['renal_crrt'],
        'prerenal_intrinsic',
        '{}',
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
