#!/usr/bin/env python3
"""chunk38_charts.py — Ph5 Hematology & Coagulation (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_37.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_38.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c38')
CHUNK_NUM   = 38
MID_BASE    = 1_800_005_035
CHART_ORDER = ['dic_score', 'blood_products', 'massive_transfusion',
               'hit_4t', 'transfusion_reactions']

_HM = 'Ph5 · \U0001f7e1 T2 · Hematology & Coagulation'

RF = {}

# ── Chart 1: DIC — ISTH Overt DIC Score ──────────────────────────────────────
RF['dic_score'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;

    var cats=[
        {n:'Platelet count',  opts:[{s:0,l:'>100k'},{s:1,l:'50–100k'},{s:2,l:'<50k'}],      k:'p', cur:P.p||0},
        {n:'PT prolongation', opts:[{s:0,l:'< 3 sec'},{s:1,l:'3–6 sec'},{s:2,l:'> 6 sec'}], k:'pt',cur:P.pt||0},
        {n:'D-dimer',         opts:[{s:0,l:'No increase'},{s:2,l:'Moderate'},{s:3,l:'Strong / marked'}], k:'d', cur:P.d||0},
        {n:'Fibrinogen',      opts:[{s:0,l:'> 1 g/L'},{s:1,l:'≤ 1 g/L'}],                   k:'f', cur:P.f||0},
    ];

    function score(){ return cats.reduce(function(s,c){return s+c.opts[c.cur].s;},0); }

    function draw(){
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);
        var sc=score();
        var col=sc>=5?_RE:sc>=3?_AM:_GN;
        var verdict=sc>=5?'OVERT DIC — treat underlying cause + support':
                    sc>=3?'Non-overt DIC — monitor, treat cause':
                          'Score < 3 — DIC unlikely';

        // Score display
        ctx.fillStyle=col; ctx.font='bold 46px sans-serif'; ctx.textAlign='left';
        ctx.fillText(sc, 14, 56);
        ctx.font='bold 12px sans-serif'; ctx.fillText('ISTH DIC Score', 14, 74);
        ctx.fillStyle='#888'; ctx.font='11px sans-serif'; ctx.fillText(verdict, 14, 92);

        // Gauge
        var gx=14, gy=100, gw=W-28, gh=16;
        ctx.fillStyle=_GN+'22'; ctx.fillRect(gx,gy,gw*3/9,gh);
        ctx.fillStyle=_AM+'22'; ctx.fillRect(gx+gw*3/9,gy,gw*2/9,gh);
        ctx.fillStyle=_RE+'22'; ctx.fillRect(gx+gw*5/9,gy,gw*4/9,gh);
        ctx.fillStyle=col+'88'; ctx.fillRect(gx,gy,gw*Math.min(sc/9,1),gh);
        ctx.strokeStyle='#444'; ctx.lineWidth=1; ctx.strokeRect(gx,gy,gw,gh);
        [3,5,9].forEach(function(v){
            var tx=gx+gw*(v/9);
            ctx.strokeStyle='#555'; ctx.beginPath(); ctx.moveTo(tx,gy); ctx.lineTo(tx,gy+gh); ctx.stroke();
            ctx.fillStyle='#666'; ctx.font='9px sans-serif'; ctx.textAlign='center';
            ctx.fillText(v, tx, gy+gh+10);
        });
        ctx.fillStyle='#444'; ctx.font='9px sans-serif';
        ctx.fillText('< 3 = unlikely',gx+gw*1.5/9,gy+gh+10);
        ctx.fillStyle='#ffca2888'; ctx.fillText('≥ 5 = overt DIC',gx+gw*6.5/9,gy+gh+10);

        // Category rows
        cats.forEach(function(c,i){
            var y=128+i*30;
            var opt=c.opts[c.cur];
            ctx.fillStyle=opt.s>0?col+'22':'#111';
            ctx.fillRect(14,y,W-28,26);
            ctx.strokeStyle=opt.s>0?col:'#222'; ctx.lineWidth=opt.s>0?2:1;
            ctx.strokeRect(14,y,W-28,26);
            ctx.fillStyle=opt.s>0?col:'#666';
            ctx.font=(opt.s>0?'bold ':'')+'10px sans-serif'; ctx.textAlign='left';
            ctx.fillText(c.n+': '+opt.l+(opt.s>0?' (+'+opt.s+')':'  (0)'), 22, y+17);
        });
    }
    draw();

    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;align-items:center;';
        cats.forEach(function(c){
            var b=document.createElement('button');
            var upd=function(){
                var opt=c.opts[c.cur];
                b.textContent=c.n.split(' ')[0]+': +'+opt.s;
                var hl=opt.s>0;
                b.style.cssText='font-size:10px;padding:2px 8px;border-radius:4px;cursor:pointer;font-weight:700;'+
                    'border:1px solid '+_OR+';background:'+(hl?_OR+'22':'transparent')+';color:'+(hl?_OR:'#555')+';';
            };
            upd();
            b.addEventListener('click',function(){
                c.cur=(c.cur+1)%c.opts.length; P[c.k]=c.cur; upd(); draw();
            });
            row.appendChild(b);
        });
        var rst=document.createElement('button');
        rst.textContent='Reset';
        rst.style.cssText='font-size:10px;padding:2px 8px;border-radius:4px;cursor:pointer;border:1px solid #666;background:transparent;color:#666;';
        rst.addEventListener('click',function(){
            cats.forEach(function(c){c.cur=0;P[c.k]=0;});
            row.querySelectorAll('button:not(:last-child)').forEach(function(b,i){
                b.textContent=cats[i].n.split(' ')[0]+': +0';
                b.style.background='transparent'; b.style.color='#555';
            });
            draw();
        });
        row.appendChild(rst);
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: Blood Products Comparison Table ──────────────────────────────────
RF['blood_products'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;

    var prods=[
        {n:'pRBC',   col:'#ef5350', vol:'250–350 mL', incr:'↑ Hgb ~1 g/dL / unit', ind:'Hgb <7 stable; <8 active bleed/ACS',   note:'Type & screen; irradiate if immunosupp.'},
        {n:'FFP',    col:'#ffca28', vol:'250 mL',      incr:'25–30% factor activity / unit', ind:'INR >1.5 + active bleed / pre-procedure', note:'Thaw 20–30 min; ABO compatible'},
        {n:'Plt',    col:'#29b6f6', vol:'50–300 mL',   incr:'30–60k / unit (apheresis)',      ind:'<10k prophy; <50k bleed/procedure',        note:'Expire in 5 days; bacterial risk'},
        {n:'Cryo',   col:'#4caf50', vol:'~15 mL/unit', incr:'Fibrinogen +5–10 mg/dL/unit',    ind:'Fibrinogen <100–150 mg/dL; DIC; TTP', note:'Pool 5–10 units for DIC; contains VIII, vWF'},
    ];

    var hi=P.hi!=null?P.hi:-1;
    var cW=[50,80,130,170,190], rH=42, tT=10, hdrH=24;

    function draw(){
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);

        // Header
        ['Type','Volume','Increment','Indication','Key Note'].forEach(function(h,ci){
            var x=0; for(var k=0;k<ci;k++) x+=cW[k];
            var dim=hi>=0&&hi!==ci-1&&ci>0&&ci<=4;
            // ci 0 = Type label, ci 1-4 = columns for each product? No, these are feature columns not product columns
            ctx.fillStyle='#1c1c1c'; ctx.fillRect(x,tT,cW[ci],hdrH);
            ctx.strokeStyle='#333'; ctx.lineWidth=1; ctx.strokeRect(x,tT,cW[ci],hdrH);
            ctx.fillStyle='#aaa'; ctx.font='bold 9px sans-serif'; ctx.textAlign='center';
            ctx.fillText(h, x+cW[ci]/2, tT+hdrH/2+4);
        });

        prods.forEach(function(pr,ri){
            var y=tT+hdrH+ri*rH;
            var hl=ri===hi;
            var vals=[pr.n, pr.vol, pr.incr, pr.ind, pr.note];
            for(var ci=0;ci<5;ci++){
                var x=0; for(var k=0;k<ci;k++) x+=cW[k];
                ctx.fillStyle=hl?pr.col+'33':(ri%2?'#111':'#0d0d0d');
                ctx.fillRect(x,y,cW[ci],rH);
                ctx.strokeStyle=hl?pr.col:'#222'; ctx.lineWidth=hl?2:1;
                ctx.strokeRect(x,y,cW[ci],rH);
                ctx.fillStyle=hl?pr.col:(ci===0?pr.col+'cc':'#777');
                ctx.font=(ci===0?'bold ':'')+(hl&&ci>0?'bold ':'')+
                    (ci>=3?'8':'9')+'px sans-serif';
                ctx.textAlign=ci===0?'center':'left';
                ctx.fillText(vals[ci], ci===0?x+cW[ci]/2:x+4, y+rH/2+4);
            }
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
        prods.forEach(function(pr,i){
            var b=_mkB(pr.n,pr.col,hi===i,function(on){
                hi=on?i:-1; P.hi=hi;
                btns.forEach(function(x,j){
                    x._on=j===i&&on;
                    x.style.background=x._on?prods[j].col+'22':'transparent';
                    x.style.color=x._on?prods[j].col:'#555';
                });
                draw();
            });
            btns.push(b); row.appendChild(b);
        });
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 3: Massive Transfusion Protocol — 1:1:1 Ratio ──────────────────────
RF['massive_transfusion'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;
    var showOld=P.old||0;

    var barW=80, barGap=12, groupGap=40;
    var mx=20, my=20, barH=H-my-80;

    // 1:1:1 ratio (current DCR standard)
    var modern=[
        {n:'pRBC',  ratio:1, col:'#ef5350'},
        {n:'FFP',   ratio:1, col:'#ffca28'},
        {n:'Plt',   ratio:1, col:'#29b6f6'},
    ];
    // Historical 10:1 (packed cells dominant)
    var historic=[
        {n:'pRBC',  ratio:10, col:'#ef5350'},
        {n:'FFP',   ratio:2,  col:'#ffca28'},
        {n:'Plt',   ratio:1,  col:'#29b6f6'},
    ];

    function draw(){
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);

        var set1=modern, set2=showOld?historic:null;
        var maxRatio=showOld?10:1;
        var scale=barH/maxRatio;

        var g1x=mx+barGap;
        var g2x=showOld?g1x+(barW+barGap)*3+groupGap:null;

        // Group labels
        ctx.fillStyle=_GN; ctx.font='bold 10px sans-serif'; ctx.textAlign='center';
        ctx.fillText('DCR 1:1:1 (PROPPR Trial)', g1x+(barW*1.5+barGap), my-6);
        if(showOld){
            ctx.fillStyle=_AM;
            ctx.fillText('Historical 10:2:1', g2x+(barW*1.5+barGap), my-6);
        }

        function drawGroup(prods, gx, maxR, hl){
            prods.forEach(function(p,i){
                var bx=gx+i*(barW+barGap);
                var bh=p.ratio/maxR*barH;
                var by=my+barH-bh;
                ctx.fillStyle=p.col+(hl?'44':'33');
                ctx.fillRect(bx,by,barW,bh);
                ctx.strokeStyle=p.col+(hl?'ff':'88'); ctx.lineWidth=hl?2:1;
                ctx.strokeRect(bx,by,barW,bh);
                ctx.fillStyle=p.col; ctx.font='bold 11px sans-serif'; ctx.textAlign='center';
                ctx.fillText(p.n, bx+barW/2, by+bh/2+4);
                ctx.fillStyle='#888'; ctx.font='10px sans-serif';
                ctx.fillText(p.ratio+'u', bx+barW/2, my+barH+14);
            });
        }

        drawGroup(modern, g1x, 1, !showOld);
        if(showOld) drawGroup(historic, g2x, 10, true);

        // Ratio annotation
        ctx.fillStyle=_GN+'bb'; ctx.font='bold 13px sans-serif'; ctx.textAlign='center';
        ctx.fillText('1 : 1 : 1', g1x+barW*1.5+barGap, my+barH+30);
        if(showOld){
            ctx.fillStyle=_AM+'bb';
            ctx.fillText('10 : 2 : 1', g2x+barW*1.5+barGap, my+barH+30);
        }

        // MTP threshold note
        ctx.fillStyle='#555'; ctx.font='9px sans-serif'; ctx.textAlign='left';
        ctx.fillText('MTP activation: >10u pRBC/24h; SBP <90; HR >120; penetrating trauma; clinical judgment', mx, H-8);

        // PROPPR benefit box (right side)
        if(!showOld){
            var bx=g1x+(barW+barGap)*3+20, bw=W-bx-16;
            ctx.fillStyle='#4caf5011'; ctx.fillRect(bx,my,bw,barH);
            ctx.strokeStyle='#4caf5044'; ctx.lineWidth=1; ctx.strokeRect(bx,my,bw,barH);
            ctx.fillStyle='#4caf50'; ctx.font='bold 9px sans-serif'; ctx.textAlign='center';
            ctx.fillText('PROPPR Trial Benefits', bx+bw/2, my+14);
            var lines=['↓ 24h mortality','↓ coagulopathy','↓ PRBC use','Less crystalloid','Hemostasis in 24h'];
            ctx.fillStyle='#888'; ctx.font='9px sans-serif';
            lines.forEach(function(l,i){ ctx.fillText(l,bx+bw/2,my+30+i*18); });
        }
    }
    draw();

    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;align-items:center;';
        var b=_mkB('Compare Historical 10:2:1',_AM,showOld,function(on){
            showOld=on?1:0; P.old=showOld;
            b._on=on; b.style.background=on?_AM+'22':'transparent'; b.style.color=on?_AM:'#555';
            draw();
        });
        row.appendChild(b);
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 4: HIT — 4T Score ──────────────────────────────────────────────────
RF['hit_4t'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;

    var cats=[
        {n:'Thrombocytopenia',
         opts:[{s:0,l:'< 30% fall or nadir < 10k'},{s:1,l:'30–50% fall or nadir 10–19k'},{s:2,l:'> 50% fall and nadir ≥ 20k'}],
         k:'T1', cur:P.T1||0},
        {n:'Timing of plt fall',
         opts:[{s:0,l:'< 4 days (no recent heparin)'},{s:1,l:'> 10 days or unclear timing'},{s:2,l:'5–10 days; or ≤ 1 day + heparin in prior 30 days'}],
         k:'T2', cur:P.T2||0},
        {n:'Thrombosis / skin necrosis',
         opts:[{s:0,l:'None'},{s:1,l:'Progressive or recurrent thrombosis'},{s:2,l:'New confirmed thrombosis or skin necrosis'}],
         k:'T3', cur:P.T3||0},
        {n:'oTher causes of plt fall',
         opts:[{s:0,l:'Definite other cause present'},{s:1,l:'Possible other cause'},{s:2,l:'No alternative cause identified'}],
         k:'T4', cur:P.T4||0},
    ];

    function score(){ return cats.reduce(function(s,c){return s+c.opts[c.cur].s;},0); }

    function draw(){
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);
        var sc=score();
        var col=sc<=3?_GN:sc<=5?_AM:_RE;
        var verdict=sc<=3?'Low probability (<1%) — HIT unlikely; continue heparin':
                    sc<=5?'Intermediate (10–30%) — stop heparin; send HIT antibody':
                          'High probability (>80%) — stop heparin STAT; start argatroban/bivalirudin';

        ctx.fillStyle=col; ctx.font='bold 46px sans-serif'; ctx.textAlign='left';
        ctx.fillText(sc+' / 8', 14, 56);
        ctx.font='bold 11px sans-serif'; ctx.fillText('4T Score — HIT Probability', 14, 74);
        ctx.fillStyle='#888'; ctx.font='9px sans-serif';
        // wrap verdict
        var words=verdict.split(';'), vy=90;
        words.forEach(function(w){ ctx.fillText(w.trim(), 14, vy); vy+=11; });

        // Gauge
        var gx=14, gy=113, gw=W-28, gh=14;
        ctx.fillStyle=_GN+'22'; ctx.fillRect(gx,gy,gw*4/8,gh);
        ctx.fillStyle=_AM+'22'; ctx.fillRect(gx+gw*4/8,gy,gw*2/8,gh);
        ctx.fillStyle=_RE+'22'; ctx.fillRect(gx+gw*6/8,gy,gw*2/8,gh);
        ctx.fillStyle=col+'88'; ctx.fillRect(gx,gy,gw*sc/8,gh);
        ctx.strokeStyle='#444'; ctx.lineWidth=1; ctx.strokeRect(gx,gy,gw,gh);
        [4,6,8].forEach(function(v){
            var tx=gx+gw*v/8;
            ctx.strokeStyle='#555'; ctx.beginPath(); ctx.moveTo(tx,gy); ctx.lineTo(tx,gy+gh); ctx.stroke();
            ctx.fillStyle='#666'; ctx.font='9px sans-serif'; ctx.textAlign='center';
            ctx.fillText(v, tx, gy+gh+10);
        });

        // Category rows
        cats.forEach(function(c,i){
            var y=135+i*30;
            var opt=c.opts[c.cur];
            ctx.fillStyle=opt.s>0?col+'22':'#111';
            ctx.fillRect(14,y,W-28,26);
            ctx.strokeStyle=opt.s>0?col:'#222'; ctx.lineWidth=opt.s>0?2:1;
            ctx.strokeRect(14,y,W-28,26);
            ctx.fillStyle=opt.s>0?col:'#555';
            ctx.font=(opt.s>0?'bold ':'')+'9px sans-serif'; ctx.textAlign='left';
            ctx.fillText(c.n+': '+opt.l+'  (+'+opt.s+')', 22, y+17);
        });
    }
    draw();

    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;align-items:center;';
        cats.forEach(function(c){
            var b=document.createElement('button');
            var upd=function(){
                b.textContent='T: +'+c.opts[c.cur].s;
                var hl=c.opts[c.cur].s>0;
                b.style.cssText='font-size:10px;padding:2px 8px;border-radius:4px;cursor:pointer;font-weight:700;'+
                    'border:1px solid '+_RE+';background:'+(hl?_RE+'22':'transparent')+';color:'+(hl?_RE:'#555')+';';
            };
            upd();
            b.addEventListener('click',function(){ c.cur=(c.cur+1)%c.opts.length; P[c.k]=c.cur; upd(); draw(); });
            row.appendChild(b);
        });
        var rst=document.createElement('button');
        rst.textContent='Reset';
        rst.style.cssText='font-size:10px;padding:2px 8px;border-radius:4px;cursor:pointer;border:1px solid #666;background:transparent;color:#666;';
        rst.addEventListener('click',function(){
            cats.forEach(function(c){c.cur=0;P[c.k]=0;});
            row.querySelectorAll('button:not(:last-child)').forEach(function(b){
                b.textContent='T: +0'; b.style.background='transparent'; b.style.color='#555';
            });
            draw();
        });
        row.appendChild(rst);
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 5: Transfusion Reactions — TRALI vs TACO vs Hemolytic vs FNHTR ──────
RF['transfusion_reactions'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;

    var reactions=[
        {n:'TRALI',    col:'#ef5350',
         onset:'<6 hr',
         sx:'Hypoxia, bilateral infiltrates, fever; NO hypertension; SpO₂ <90%',
         tx:'Stop transfusion; supportive O₂/vent; NO diuretics; NO steroids',
         prev:'Plasma from male-only donors; leukoreduction'},
        {n:'TACO',     col:'#29b6f6',
         onset:'<6 hr',
         sx:'Hypertension, crackles, ↑BNP, bilateral infiltrates, JVD',
         tx:'Stop transfusion; furosemide; O₂; upright positioning',
         prev:'Slow infusion rate; avoid in CHF/renal failure'},
        {n:'Acute Hemolytic', col:'#ce93d8',
         onset:'During (mins)',
         sx:'Fever/chills, flank/back pain, hemoglobinuria (tea urine), DIC, shock',
         tx:'STOP IMMEDIATELY; NS; maintain UO; furosemide; never restart',
         prev:'Two-person verification of patient ID and blood label'},
        {n:'FNHTR',    col:'#ffca28',
         onset:'During–4 hr',
         sx:'Fever ≥1°C rise, chills; no hemolysis; no hypoxia',
         tx:'Slow/pause; acetaminophen; restart if no deterioration',
         prev:'Leukoreduction filter; pre-medicate with acetaminophen'},
    ];

    var hi=P.hi!=null?P.hi:-1;
    var cW=[80,55,175,185,125], rH=46, tT=10, hdrH=22;

    function draw(){
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);

        ['Reaction','Onset','Key Symptoms','Treatment','Prevention'].forEach(function(h,ci){
            var x=0; for(var k=0;k<ci;k++) x+=cW[k];
            ctx.fillStyle='#1c1c1c'; ctx.fillRect(x,tT,cW[ci],hdrH);
            ctx.strokeStyle='#333'; ctx.lineWidth=1; ctx.strokeRect(x,tT,cW[ci],hdrH);
            ctx.fillStyle='#aaa'; ctx.font='bold 9px sans-serif'; ctx.textAlign='center';
            ctx.fillText(h, x+cW[ci]/2, tT+hdrH/2+4);
        });

        reactions.forEach(function(r,ri){
            var y=tT+hdrH+ri*rH;
            var hl=ri===hi;
            var vals=[r.n, r.onset, r.sx, r.tx, r.prev];
            for(var ci=0;ci<5;ci++){
                var x=0; for(var k=0;k<ci;k++) x+=cW[k];
                ctx.fillStyle=hl?r.col+'33':(ri%2?'#111':'#0d0d0d');
                ctx.fillRect(x,y,cW[ci],rH);
                ctx.strokeStyle=hl?r.col:'#222'; ctx.lineWidth=hl?2:1;
                ctx.strokeRect(x,y,cW[ci],rH);
                ctx.fillStyle=hl?(ci===0?r.col:'#eee'):r.col+(ci===0?'bb':'44');
                ctx.font=(ci===0?'bold ':'')+
                    (hl&&ci>0?'bold ':'')+
                    (ci>=2?'7.5':'9')+'px sans-serif';
                ctx.textAlign=ci===0?'center':'left';
                ctx.fillText(vals[ci], ci===0?x+cW[ci]/2:x+3, y+rH/2+3);
            }
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
        reactions.forEach(function(r,i){
            var b=_mkB(r.n,r.col,hi===i,function(on){
                hi=on?i:-1; P.hi=hi;
                btns.forEach(function(x,j){
                    x._on=j===i&&on;
                    x.style.background=x._on?reactions[j].col+'22':'transparent';
                    x.style.color=x._on?reactions[j].col:'#555';
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
    # ═══ dic_score ════════════════════════════════════════════════════════════
    (
        "On the ISTH DIC scoring chart, overt DIC is diagnosed when "
        "the score reaches _______ or higher. The four scored parameters are "
        "_______.",

        "Score ≥5 = overt DIC\n"
        "| Four parameters: (1) Platelet count (<100k = +1, <50k = +2), "
        "(2) PT prolongation (<3s = 0, 3–6s = +1, >6s = +2), "
        "(3) D-dimer (no increase = 0, moderate = +2, strong = +3), "
        "(4) Fibrinogen (>1 g/L = 0, ≤1 g/L = +1)\n"
        "→ CCRN KEY: DIC = simultaneous microvascular clotting AND hemorrhage. "
        "Lab pattern: ↓ platelets + ↑ PT/INR + ↑ D-dimer + ↓ fibrinogen. "
        "D-dimer most sensitive early finding.\n"
        "→ MASTERY NOTE: Treat the underlying cause (sepsis, obstetric, trauma) — "
        "DIC does not resolve without removing the trigger. "
        "Support with platelets >50k for bleeding, FFP for INR >2, cryo for fibrinogen <100.",

        'tier-review',
        _HM,
        DID['hematology'],
        'dic_score',
        '{}',
        'chart-l1'
    ),
    (
        "A septic patient's labs show: Plt 38k (↓ from 210k), PT prolonged "
        "7 sec above normal, D-dimer markedly elevated, fibrinogen 0.8 g/L. "
        "ISTH score = _______, confirming _______.",

        "Plt <50k (+2) + PT >6s (+2) + D-dimer strong (+3) + fibrinogen <1 g/L (+1) = 8 — Overt DIC\n"
        "| Confirms: Overt DIC secondary to sepsis\n"
        "→ CCRN KEY: Score 8 = severe overt DIC. Immediate priorities: "
        "treat sepsis source (antibiotics, source control); "
        "transfuse platelets to ≥50k; FFP to correct INR; "
        "cryoprecipitate (10-unit pool) to raise fibrinogen >150 mg/dL.\n"
        "→ MASTERY NOTE: Heparin in DIC is controversial — consider only in "
        "thrombosis-dominant DIC (purpura fulminans, arterial clots). "
        "Contraindicated in hemorrhage-dominant DIC. "
        "Low-molecular-weight heparin for prophylaxis only when bleeding controlled.",

        'tier-high',
        _HM,
        DID['hematology'],
        'dic_score',
        '{"p":2,"pt":2,"d":2,"f":1}',
        'chart-l2'
    ),
    (
        "Post-partum patient: DIC score 7, oozing from IV sites and "
        "surgical incision, Plt 42k, fibrinogen 90 mg/dL. You give _______ "
        "first, then _______, not _______, because _______.",

        "First: Cryoprecipitate 10-unit pool IV (contains fibrinogen, factor VIII, vWF; "
        "fastest way to raise fibrinogen)\n"
        "| Then: pRBC to maintain Hgb, platelets to ≥50k, FFP for INR correction\n"
        "| Not: heparin\n"
        "| Because: this is hemorrhage-dominant DIC (oozing, low fibrinogen) — "
        "heparin would worsen bleeding; fibrinogen replacement is the priority\n"
        "→ CCRN KEY: Obstetric DIC is hemorrhage-dominant. "
        "Cryoprecipitate target: fibrinogen >150–200 mg/dL. "
        "Each 10-unit cryo pool raises fibrinogen ~50–100 mg/dL in average adult.\n"
        "→ MASTERY NOTE: Tranexamic acid (TXA) 1g IV within 3h of delivery "
        "reduces mortality in post-partum hemorrhage (WOMAN trial). "
        "Can be given concurrently with blood products.",

        'tier-critical',
        _HM,
        DID['hematology'],
        'dic_score',
        '{"p":2,"pt":1,"d":2,"f":1}',
        'chart-l3'
    ),

    # ═══ blood_products ═══════════════════════════════════════════════════════
    (
        "On the blood products comparison chart, one unit of packed red blood "
        "cells raises hemoglobin approximately _______ g/dL, and the "
        "transfusion threshold in a stable ICU patient is _______.",

        "One unit pRBC raises Hgb ~1 g/dL (in 70 kg adult)\n"
        "| Transfusion threshold: Hgb <7 g/dL in stable ICU patients (TRICC trial)\n"
        "| Exception: Hgb <8 for active coronary artery disease, active GI bleed, "
        "or hemodynamic instability\n"
        "→ CCRN KEY: Restrictive transfusion (Hgb <7) = non-inferior to liberal "
        "(<10) in most ICU patients with LOWER infection and transfusion reaction risk. "
        "Check post-transfusion Hgb 15–30 min after unit completion.\n"
        "→ MASTERY NOTE: Irradiated pRBC required for: immunocompromised, "
        "hematopoietic stem cell transplant, premature neonates, directed donor blood. "
        "CMV-negative blood for: CMV-negative immunocompromised patients.",

        'tier-review',
        _HM,
        DID['hematology'],
        'blood_products',
        '{"hi":0}',
        'chart-l1'
    ),
    (
        "The blood products chart shows cryoprecipitate contains fibrinogen, "
        "factor VIII, and vWF. The primary ICU indication for cryoprecipitate "
        "is _______, and the typical dose is _______.",

        "Primary indication: fibrinogen <100–150 mg/dL with active bleeding (DIC, "
        "massive transfusion, liver failure, obstetric emergency)\n"
        "| Also: von Willebrand disease (when desmopressin fails) and hemophilia A "
        "(when factor VIII concentrate unavailable)\n"
        "| Typical dose: 10-unit pool IV (raises fibrinogen ~50–100 mg/dL in adult)\n"
        "→ CCRN KEY: Cryoprecipitate dose: 1 unit/5–10 kg body weight (usually 10 pools). "
        "Each unit is ~15 mL, derived from thawed FFP precipitate. "
        "Must be ABO compatible; infuse within 4h of thawing.\n"
        "→ MASTERY NOTE: In massive transfusion, give cryo in the 1:1:1 protocol as "
        "part of the total FFP component (FFP contains fibrinogen, but not as concentrated "
        "as cryo). Target fibrinogen >200 mg/dL during active MTP.",

        'tier-high',
        _HM,
        DID['hematology'],
        'blood_products',
        '{"hi":3}',
        'chart-l2'
    ),
    (
        "An ICU patient has INR 2.4, active subarachnoid hemorrhage, urgent "
        "procedure needed. The blood products chart shows FFP is indicated. "
        "You order _______ units, and the expected result is _______, "
        "but you must also account for _______.",

        "Order: 4 units FFP (standard dose for INR reversal in acute bleeding)\n"
        "| Expected result: INR reduction by ~30–50%, typically to 1.3–1.8 range\n"
        "| Must account for: FFP thaw time (~20–30 min) and the volume load "
        "(4 units = ~1,000 mL) which risks fluid overload in cardiac/renal patients\n"
        "→ CCRN KEY: FFP contains all coagulation factors; 4-factor PCC "
        "(prothrombin complex concentrate) is faster (no thaw, smaller volume) "
        "for urgent INR reversal — preferred over FFP when speed is critical.\n"
        "→ MASTERY NOTE: 4-factor PCC (Kcentra) 25–50 units/kg reverses warfarin "
        "within minutes, no crossmatch needed, 20–40 mL volume. "
        "Also give vitamin K 10 mg IV for sustained reversal beyond the PCC window.",

        'tier-critical',
        _HM,
        DID['hematology'],
        'blood_products',
        '{"hi":1}',
        'chart-l3'
    ),

    # ═══ massive_transfusion ══════════════════════════════════════════════════
    (
        "On the massive transfusion protocol chart, the PROPPR trial–supported "
        "ratio is _______, meaning _______ unit(s) of FFP and platelets for "
        "every unit of pRBC.",

        "1:1:1 ratio — pRBC : FFP : Platelets\n"
        "| 1 unit FFP and 1 unit platelets for every 1 unit pRBC\n"
        "| Replaces older 6:4:1 or 10:1 approaches dominated by packed cells\n"
        "→ CCRN KEY: PROPPR trial (2015): 1:1:1 ratio reduces 24-hour mortality "
        "and achieves hemostasis faster vs 1:1:2. "
        "Rationale: hemorrhagic shock depletes ALL components equally — replace all.\n"
        "→ MASTERY NOTE: Activation threshold: >10 pRBC units in 24h, "
        "hemodynamic instability (SBP <90), ongoing hemorrhage. "
        "Consider viscoelastic testing (TEG/ROTEM) to guide component ratios "
        "when available — more precise than empiric 1:1:1.",

        'tier-review',
        _HM,
        DID['hematology'],
        'massive_transfusion',
        '{}',
        'chart-l1'
    ),
    (
        "The MTP ratio chart shows that older 10:1 (pRBC:FFP) protocols "
        "caused worse outcomes than 1:1:1. This occurred because _______.",

        "High-volume packed cells without sufficient FFP/platelets = "
        "dilutional coagulopathy — factors fall below hemostatic threshold as "
        "blood is replaced with only cells and crystalloid\n"
        "| Also: crystalloid resuscitation worsens acidosis, hypothermia, "
        "and coagulopathy (the trauma triad of death)\n"
        "→ CCRN KEY: The 'lethal triad' of trauma = hypothermia + acidosis + "
        "coagulopathy. 1:1:1 breaks the triad by replacing coagulation factors "
        "alongside RBCs instead of diluting them.\n"
        "→ MASTERY NOTE: Calcium is depleted during massive transfusion "
        "(citrate in blood products chelates ionized calcium). "
        "Give calcium chloride 1g or calcium gluconate 3g IV per 4–6 units transfused. "
        "Ionized Ca <0.9 mmol/L = supplement.",

        'tier-high',
        _HM,
        DID['hematology'],
        'massive_transfusion',
        '{"old":1}',
        'chart-l2'
    ),
    (
        "Trauma patient receives 12 pRBC, 12 FFP, 4 apheresis platelets over "
        "4 hours. MTP is activated. Temperature 35.1°C, pH 7.18, INR 2.1. "
        "The chart shows _______ triad. You prioritize _______ alongside "
        "continued product transfusion, not _______, because _______.",

        "Lethal triad: hypothermia (35.1°C) + acidosis (pH 7.18) + coagulopathy (INR 2.1)\n"
        "| Priority: warm the patient (warm fluids, warming blanket, warm OR); "
        "correct acidosis (resuscitate, vasopressors for hypotension; sodium bicarb "
        "only if pH <7.1 and hemodynamics failing)\n"
        "| Not: aggressive crystalloid infusion to correct pH\n"
        "| Because: crystalloid worsens all three components of the triad — "
        "dilutes clotting factors, increases acidosis, and contributes to hypothermia\n"
        "→ CCRN KEY: Damage control resuscitation = limit crystalloid, "
        "permissive hypotension (SBP 80–90 before surgical control), "
        "1:1:1 products, early surgical hemorrhage control.\n"
        "→ MASTERY NOTE: TXA (tranexamic acid) 1g IV over 10 min, then 1g over 8h — "
        "reduces mortality in trauma if given within 3 hours of injury (CRASH-2 trial). "
        "No benefit if given after 3h; possibly harmful.",

        'tier-critical',
        _HM,
        DID['hematology'],
        'massive_transfusion',
        '{}',
        'chart-l3'
    ),

    # ═══ hit_4t ═══════════════════════════════════════════════════════════════
    (
        "On the HIT 4T scoring chart, a high-probability score of 6–8 "
        "requires _______ as the immediate action, and anticoagulation "
        "should be switched to _______.",

        "Immediate action: STOP all heparin products (IV, flushes, heparin-coated catheters)\n"
        "| Switch to: direct thrombin inhibitor — argatroban (preferred if renal failure) "
        "or bivalirudin; fondaparinux is an alternative\n"
        "→ CCRN KEY: 4T Score ≤3 = HIT low probability; 4–5 = intermediate; "
        "6–8 = high. For intermediate/high: stop heparin immediately AND start "
        "alternative anticoagulation (do NOT wait for PF4 antibody results). "
        "HIT creates a paradoxical prothrombotic state — stopping heparin without "
        "alternative anticoagulation still risks thrombosis.\n"
        "→ MASTERY NOTE: LMWH (enoxaparin) is contraindicated in HIT — "
        "cross-reacts with heparin antibodies ~85–95% of the time. "
        "Warfarin is also contraindicated acutely — worsens protein C depletion.",

        'tier-review',
        _HM,
        DID['hematology'],
        'hit_4t',
        '{}',
        'chart-l1'
    ),
    (
        "A patient on heparin infusion for PE has platelet count fall from "
        "280k to 90k on day 7 (68% drop), new DVT discovered, no other "
        "cause identified. 4T score = _______. Next action: _______.",

        "Thrombocytopenia: >50% drop, nadir ≥20k (+2); "
        "Timing: 5–10 days (+2); Thrombosis: new DVT (+2); Other cause: none (+2) = 8 — High\n"
        "| Next action: STOP heparin STAT; order anti-PF4/heparin antibody (SRA confirmatory); "
        "start argatroban IV infusion; notify provider\n"
        "→ CCRN KEY: High 4T = treat as HIT without waiting for confirmatory lab. "
        "Argatroban: continuous infusion 2 mcg/kg/min, titrate aPTT to 1.5–3× baseline "
        "(reduce to 0.5–1.2 mcg/kg/min in hepatic failure).\n"
        "→ MASTERY NOTE: Skin necrosis at heparin injection sites = pathognomonic "
        "for HIT (without needing 4T score). "
        "Platelet nadir in HIT typically 20–150k — very rarely <20k "
        "(unlike thrombocytopenic purpura). Severe bleeding is uncommon.",

        'tier-high',
        _HM,
        DID['hematology'],
        'hit_4t',
        '{"T1":2,"T2":2,"T3":2,"T4":2}',
        'chart-l2'
    ),
    (
        "HIT patient was switched to argatroban 3 days ago. Platelet count "
        "now recovering (180k). Provider orders transition to warfarin. "
        "You hold warfarin and notify the provider because _______.",

        "Warfarin must not be started until platelets recover to ≥150k AND "
        "argatroban has been therapeutic for ≥4–5 days\n"
        "| Reason: warfarin depletes protein C and S before depleting "
        "pro-coagulant factors — this creates a hypercoagulable window, "
        "worsening HIT thrombosis risk (limb gangrene, venous limb gangrene)\n"
        "| If platelets <150k at transition: HIT antibodies still active; "
        "protein C depletion by warfarin = catastrophic\n"
        "→ CCRN KEY: Safe warfarin transition in HIT: platelets ≥150k + "
        "overlap argatroban + warfarin for ≥5 days + INR therapeutic ≥2.0 "
        "before stopping argatroban.\n"
        "→ MASTERY NOTE: Fondaparinux (anti-Xa only, no anti-thrombin) has minimal "
        "cross-reactivity with HIT antibodies and is an alternative bridge to warfarin. "
        "Rivaroxaban/apixaban being studied for HIT — not yet standard of care.",

        'tier-critical',
        _HM,
        DID['hematology'],
        'hit_4t',
        '{"T1":2,"T2":2,"T3":2,"T4":2}',
        'chart-l3'
    ),

    # ═══ transfusion_reactions ════════════════════════════════════════════════
    (
        "On the transfusion reactions chart, the key finding that "
        "distinguishes TRALI from TACO is _______, because _______.",

        "TRALI: hypotension (or normotension) — no hypertension; "
        "TACO: hypertension from volume overload\n"
        "| TRALI mechanism: donor anti-WBC antibodies → neutrophil activation → "
        "non-cardiogenic pulmonary edema (low BNP, low PAWP)\n"
        "| TACO mechanism: fluid overload → cardiogenic pulmonary edema "
        "(high BNP, high PAWP)\n"
        "→ CCRN KEY: TRALI = stop transfusion, supportive O₂/ventilation, "
        "NO diuretics (worsens non-cardiogenic edema), NO steroids. "
        "TACO = stop transfusion, furosemide, O₂.\n"
        "→ MASTERY NOTE: TRALI differential: BNP >250 pg/mL favors TACO. "
        "Echo: TACO shows reduced EF or diastolic dysfunction; "
        "TRALI shows normal cardiac function. "
        "BNP <250 + hypotension + fever + bilateral infiltrates = TRALI until proven otherwise.",

        'tier-review',
        _HM,
        DID['hematology'],
        'transfusion_reactions',
        '{}',
        'chart-l1'
    ),
    (
        "During pRBC transfusion a patient develops acute flank pain, fever, "
        "dark amber urine, and hypotension within 15 minutes. The reaction "
        "chart matches _______, and the first nursing action is _______.",

        "Acute hemolytic transfusion reaction (ABO incompatibility)\n"
        "| First action: STOP TRANSFUSION IMMEDIATELY, keep IV access with NS flush\n"
        "| Then: notify blood bank and provider STAT; send blood bag and patient "
        "sample to lab for crossmatch recheck; urine for hemoglobinuria; "
        "aggressive NS to maintain UO >0.5 mL/kg/hr; furosemide if needed\n"
        "→ CCRN KEY: Acute hemolytic reaction = the most dangerous transfusion "
        "reaction. Hemolytic cascade activates complement, causing DIC, renal failure, "
        "shock. Mortality correlates with volume transfused — STOP immediately. "
        "NEVER restart the implicated unit.\n"
        "→ MASTERY NOTE: The most common cause is clerical error — wrong patient "
        "blood type. Two-RN verification of patient ID, blood product label, and "
        "MRN at bedside before EVERY transfusion is the only prevention.",

        'tier-high',
        _HM,
        DID['hematology'],
        'transfusion_reactions',
        '{"hi":2}',
        'chart-l2'
    ),
    (
        "One hour into a FFP transfusion, a patient develops SpO₂ 84%, "
        "bilateral crackles, CXR shows bilateral infiltrates, BP 148/90, "
        "BNP 820 pg/mL. The chart shows this matches _______, not _______, "
        "because _______, and treatment is _______.",

        "TACO (Transfusion-Associated Circulatory Overload)\n"
        "| Not: TRALI\n"
        "| Because: hypertension + elevated BNP (>250) + JVD pattern = "
        "cardiogenic pulmonary edema from volume overload, not immune-mediated "
        "capillary leak. TRALI = normotension/hypotension + BNP typically <250.\n"
        "| Treatment: stop transfusion; furosemide 40–80 mg IV; "
        "upright positioning; supplemental O₂; non-invasive ventilation if needed\n"
        "→ CCRN KEY: TACO is now the most common cause of transfusion-related "
        "mortality (surpassed TRALI as prevention improved). "
        "Risk factors: CHF, CKD, elderly, rapid infusion rate.\n"
        "→ MASTERY NOTE: Prevention: slow infusion rate (125 mL/hr for at-risk patients), "
        "give furosemide between units in CHF/CKD patients, "
        "minimize total transfusion volume, use leukoreduced products.",

        'tier-critical',
        _HM,
        DID['hematology'],
        'transfusion_reactions',
        '{"hi":1}',
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
