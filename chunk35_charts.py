#!/usr/bin/env python3
"""chunk35_charts.py — Ph5 Endocrine: DKA/HHS + Thyroid/Adrenal (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_34.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_35.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c35')
CHUNK_NUM   = 35
MID_BASE    = 1_800_005_020
CHART_ORDER = ['dka_severity', 'dka_hhs_compare', 'anion_gap_delta',
               'thyroid_storm', 'adrenal_crisis']

_DH = 'Ph5 · \U0001f7e0 T2 · Endocrine — DKA, HHS & Metabolic Crisis'
_TA = 'Ph5 · \U0001f7e0 T2 · Endocrine — Thyroid, Adrenal & Other'

RF = {}

# ── Chart 1: DKA Severity Zones (pH vs HCO3) ─────────────────────────────────
RF['dka_severity'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;
    var mx=56, my=16, pw=W-mx-18, ph=H-my-44;
    var xD=25, yLo=6.8, yHi=7.5, yR=yHi-yLo;
    function xp(v){return mx+(v/xD)*pw;}
    function yp(v){return my+ph-(v-yLo)/yR*ph;}

    // [hco3_lo, hco3_hi, pH_lo, pH_hi, label, color]
    var ZN=[
        [18,25, 7.35,7.50, 'Normal',       '#4caf50'],
        [15,18, 7.25,7.30, 'Mild DKA',     '#ffca28'],
        [10,15, 7.00,7.25, 'Moderate DKA', '#ff7043'],
        [0, 10, 6.80,7.00, 'Severe DKA',   '#ef5350']
    ];
    var hi = P.hi != null ? P.hi : -1;

    function draw(){
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);
        ZN.forEach(function(z,i){
            var dim = hi>=0 && hi!==i;
            ctx.fillStyle = z[5]+(dim?'1a':'44');
            var x1=xp(z[0]), x2=xp(z[1]);
            var y1=yp(Math.min(z[3],yHi)), y2=yp(Math.max(z[2],yLo));
            ctx.fillRect(x1,y1,x2-x1,y2-y1);
            ctx.fillStyle = z[5]+(dim?'44':'ee');
            ctx.font='bold 10px sans-serif'; ctx.textAlign='center';
            ctx.fillText(z[4], (x1+x2)/2, (y1+y2)/2+4);
        });
        // boundary lines
        ctx.strokeStyle='#444'; ctx.lineWidth=1; ctx.setLineDash([3,3]);
        [10,15,18].forEach(function(v){
            ctx.beginPath(); ctx.moveTo(xp(v),my); ctx.lineTo(xp(v),my+ph); ctx.stroke();
        });
        [7.00,7.25,7.30,7.35].forEach(function(v){
            ctx.beginPath(); ctx.moveTo(mx,yp(v)); ctx.lineTo(mx+pw,yp(v)); ctx.stroke();
        });
        ctx.setLineDash([]);
        // axes
        _ax(ctx,mx,my,pw,ph);
        // X labels
        ctx.fillStyle='#888'; ctx.font='10px sans-serif'; ctx.textAlign='center';
        [0,5,10,15,18,20,25].forEach(function(v){ ctx.fillText(v,xp(v),my+ph+14); });
        ctx.fillText('HCO₃ (mEq/L)', mx+pw/2, H-3);
        // Y labels
        ctx.textAlign='right';
        [6.8,7.0,7.1,7.25,7.3,7.35,7.4,7.5].forEach(function(v){
            ctx.fillText(v.toFixed(2), mx-5, yp(v)+4);
        });
        _rl(ctx,'Arterial pH',12,my+ph/2);
    }
    draw();

    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;align-items:center;';
        var sp=document.createElement('span');
        sp.style.cssText='font-size:10px;font-weight:800;color:#666;';
        sp.textContent='HIGHLIGHT:'; row.appendChild(sp);
        var cols=['#4caf50','#ffca28','#ff7043','#ef5350'];
        var labs=['Normal','Mild DKA','Moderate','Severe'];
        var btns=[];
        labs.forEach(function(l,i){
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

# ── Chart 2: DKA vs HHS Comparison Table ─────────────────────────────────────
RF['dka_hhs_compare'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;
    var rows=[
        ['Glucose',      '>250 mg/dL (avg ~400)',  '>600 mg/dL (avg ~900)',  false],
        ['Onset',        'Hours (rapid)',           'Days (insidious)',        false],
        ['pH',           '<7.30 (acidosis)',        '>7.30 (near normal)',     false],
        ['HCO₃',   '<18 mEq/L',              '>18 mEq/L',              false],
        ['Ketones',      '++ to +++ Positive',     'Absent / trace',          true],
        ['Anion Gap',    'Elevated (>12)',          'Normal (8–12)',      true],
        ['Osmolality',   '<320 mOsm/kg',           '>320 mOsm/kg',           true],
    ];
    var cW=[120,250,250], rH=32, tL=0, tT=16;

    function draw(){
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);
        // header
        ['Parameter','DKA','HHS'].forEach(function(h,ci){
            var x=tL; for(var k=0;k<ci;k++) x+=cW[k];
            ctx.fillStyle=ci===1?'#ef535044':ci===2?'#ff704344':'#1c1c1c';
            ctx.fillRect(x,tT,cW[ci],rH);
            ctx.strokeStyle='#333'; ctx.lineWidth=1; ctx.strokeRect(x,tT,cW[ci],rH);
            ctx.fillStyle=ci===0?'#aaa':ci===1?'#ef5350':'#ff7043';
            ctx.font='bold 11px sans-serif'; ctx.textAlign='center';
            ctx.fillText(h, x+cW[ci]/2, tT+rH/2+4);
        });
        rows.forEach(function(r,ri){
            var y=tT+(ri+1)*rH, hl=r[3];
            for(var ci=0;ci<3;ci++){
                var x=tL; for(var k=0;k<ci;k++) x+=cW[k];
                ctx.fillStyle=ci===0?(ri%2?'#111':'#0d0d0d'):
                              ci===1?(hl?'#ef535033':'#ef535018'):
                                     (hl?'#ff704333':'#ff704318');
                ctx.fillRect(x,y,cW[ci],rH);
                ctx.strokeStyle='#222'; ctx.lineWidth=1; ctx.strokeRect(x,y,cW[ci],rH);
                ctx.fillStyle=ci===0?(hl?'#ffca28':'#bbb'):
                              ci===1?(hl?'#ff9090':'#ef5350cc'):
                                     (hl?'#ffa07a':'#ff7043cc');
                ctx.font=(hl&&ci>0?'bold ':'')+'10px sans-serif';
                ctx.textAlign=ci===0?'left':'center';
                ctx.fillText(r[ci], ci===0?x+7:x+cW[ci]/2, y+rH/2+4);
            }
        });
        ctx.fillStyle='#ffca2877'; ctx.font='9px sans-serif'; ctx.textAlign='right';
        ctx.fillText('★ = key differentiators', W-6, H-4);
    }
    draw();
}
"""

# ── Chart 3: Anion Gap + Delta-Delta ─────────────────────────────────────────
RF['anion_gap_delta'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;
    var curNa=P.na||138, curCl=P.cl||102, curHco=P.hco||10;

    var mx=14, my=16, barW=110, barH=H-my-54, barGap=20;
    var catX=mx+barW+barGap, natX=mx; // Na bar left, anions bar right of Na

    function draw(){
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);
        var ag=Math.max(0, curNa-curCl-curHco);
        var total=curCl+curHco+ag;
        var scale=barH/Math.max(total,curNa,1);

        // Cations bar (Na)
        var naH=curNa*scale;
        ctx.fillStyle='#29b6f644'; ctx.fillRect(natX, my+barH-naH, barW, naH);
        ctx.strokeStyle='#29b6f6'; ctx.lineWidth=2; ctx.strokeRect(natX, my+barH-naH, barW, naH);
        ctx.fillStyle='#29b6f6'; ctx.font='bold 11px sans-serif'; ctx.textAlign='center';
        ctx.fillText('Na⁺ '+curNa, natX+barW/2, my+barH-naH/2+4);
        ctx.fillStyle='#888'; ctx.font='10px sans-serif';
        ctx.fillText('Cations', natX+barW/2, my+barH+13);

        // Anions bar (Cl + HCO3 + AG)
        var ax=natX+barW+barGap;
        var clH=curCl*scale, hcoH=curHco*scale, agH=ag*scale;
        // Cl segment
        ctx.fillStyle='#4caf5044';
        ctx.fillRect(ax, my+barH-clH, barW, clH);
        ctx.strokeStyle='#4caf50'; ctx.lineWidth=1; ctx.strokeRect(ax, my+barH-clH, barW, clH);
        ctx.fillStyle='#4caf50'; ctx.font='bold 10px sans-serif'; ctx.textAlign='center';
        if(clH>14) ctx.fillText('Cl⁻ '+curCl, ax+barW/2, my+barH-clH/2+4);
        // HCO3 segment
        ctx.fillStyle='#29b6f633';
        ctx.fillRect(ax, my+barH-clH-hcoH, barW, hcoH);
        ctx.strokeStyle='#29b6f6'; ctx.lineWidth=1; ctx.strokeRect(ax, my+barH-clH-hcoH, barW, hcoH);
        ctx.fillStyle='#29b6f6'; ctx.font='bold 10px sans-serif';
        if(hcoH>14) ctx.fillText('HCO₃ '+curHco, ax+barW/2, my+barH-clH-hcoH/2+4);
        // AG segment
        ctx.fillStyle=ag>12?'#ef535066':'#ff704333';
        ctx.fillRect(ax, my+barH-clH-hcoH-agH, barW, agH);
        ctx.strokeStyle=ag>12?'#ef5350':'#ff7043'; ctx.lineWidth=2;
        ctx.strokeRect(ax, my+barH-clH-hcoH-agH, barW, agH);
        ctx.fillStyle=ag>12?'#ef5350':'#ff7043'; ctx.font='bold 10px sans-serif';
        if(agH>12) ctx.fillText('AG='+ag, ax+barW/2, my+barH-clH-hcoH-agH/2+4);

        ctx.fillStyle='#888'; ctx.font='10px sans-serif'; ctx.textAlign='center';
        ctx.fillText('Anions', ax+barW/2, my+barH+13);

        // Delta-delta panel (right side)
        var ddX=ax+barW+barGap+10, ddW=W-ddX-10;
        var dd=(ag-12)/(24-curHco||0.01);
        var ddStr=isFinite(dd)?dd.toFixed(2):'N/A';
        var interp=dd<0.4?'Hyperchloremic':dd<1.0?'Mixed AG/HyperCl':dd<=2.0?'Pure AG Acidosis':'AG + Met Alkalosis';
        var icol=dd<0.4?'#ffca28':dd<1.0?'#ff7043':dd<=2.0?'#4caf50':'#ce93d8';

        ctx.fillStyle='#1a1a1a'; ctx.fillRect(ddX,my,ddW,barH+20);
        ctx.strokeStyle='#333'; ctx.lineWidth=1; ctx.strokeRect(ddX,my,ddW,barH+20);

        ctx.fillStyle='#888'; ctx.font='bold 10px sans-serif'; ctx.textAlign='center';
        ctx.fillText('Δ/Δ Ratio', ddX+ddW/2, my+14);
        ctx.fillStyle=icol; ctx.font='bold 22px sans-serif';
        ctx.fillText(ddStr, ddX+ddW/2, my+50);
        ctx.fillStyle=icol; ctx.font='bold 10px sans-serif';
        var words=interp.split(' ');
        words.forEach(function(w,i){ ctx.fillText(w, ddX+ddW/2, my+68+i*14); });

        // legend
        var legends=[
            {t:'<0.4',c:'#ffca28',s:'Hyperchloraemic'},
            {t:'0.4–1.0',c:'#ff7043',s:'Mixed'},
            {t:'1–2',c:'#4caf50',s:'Pure AG'},
            {t:'>2',c:'#ce93d8',s:'+Met Alk'}
        ];
        var ly=my+barH+30;
        ctx.font='9px sans-serif'; ctx.textAlign='left';
        legends.forEach(function(ln,i){
            ctx.fillStyle=ln.c;
            ctx.fillRect(natX+i*70, ly, 8, 8);
            ctx.fillText(ln.t+' '+ln.s, natX+i*70+10, ly+8);
        });
        ctx.fillStyle='#666'; ctx.font='9px sans-serif'; ctx.textAlign='left';
        ctx.fillText('AG=Na⁺−Cl⁻−HCO₃  Δ/Δ=(AG−12)/(24−HCO₃)',
                     natX, H-4);
    }
    draw();

    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;align-items:center;';
        row.appendChild(_mkS('Cl⁻',80,120,1,curCl,function(v){return v.toFixed(0)+' mEq';},
            function(v){curCl=v;P.cl=v;draw();}));
        row.appendChild(_mkS('HCO₃',2,28,1,curHco,function(v){return v.toFixed(0)+' mEq';},
            function(v){curHco=v;P.hco=v;draw();}));
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 4: Thyroid Storm — Burch-Wartofsky Score ───────────────────────────
RF['thyroid_storm'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;

    // Scoring categories: [name, options_array_of_scores, current_index]
    var cats=[
        {n:'Temp °C', opts:[0,5,10,15,20,25,30],
         lbls:['<37.2','37.2','37.8','38.3','38.9','39.4','≥40'], cur:P.t||0},
        {n:'HR (bpm)',  opts:[0,5,10,15,20,25],
         lbls:['<100','100','110','120','130','≥140'], cur:P.h||0},
        {n:'CNS',       opts:[0,10,20,30],
         lbls:['None','Agitation','Delirium','Seizure/Coma'], cur:P.c||0},
        {n:'GI/Hepatic',opts:[0,10,20],
         lbls:['None','Mod (N/V)','Severe (jaundice)'], cur:P.g||0},
        {n:'AF',        opts:[0,10],
         lbls:['No AF','AF present'], cur:P.a||0},
        {n:'Precipitant',opts:[0,10],
         lbls:['No','Yes'], cur:P.p||0},
    ];

    function score(){
        return cats.reduce(function(s,c){return s+c.opts[c.cur];},0);
    }

    function draw(){
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);
        var sc=score();

        // Score gauge (0-100)
        var gx=16, gy=18, gw=W-32, gh=28;
        var maxSc=100;
        // zone backgrounds
        ctx.fillStyle='#4caf5033'; ctx.fillRect(gx,gy,gw*0.25,gh);
        ctx.fillStyle='#ffca2833'; ctx.fillRect(gx+gw*0.25,gy,gw*0.20,gh);
        ctx.fillStyle='#ef535033'; ctx.fillRect(gx+gw*0.45,gy,gw*0.55,gh);
        // gauge fill
        var fx=Math.min(sc/maxSc,1);
        var fcol=sc<25?'#4caf50':sc<45?'#ffca28':'#ef5350';
        ctx.fillStyle=fcol+'bb';
        ctx.fillRect(gx,gy,gw*fx,gh);
        ctx.strokeStyle='#444'; ctx.lineWidth=1; ctx.strokeRect(gx,gy,gw,gh);
        // zone labels
        ctx.font='bold 10px sans-serif'; ctx.textAlign='center';
        ctx.fillStyle='#4caf50'; ctx.fillText('<25 Unlikely',gx+gw*0.125,gy+gh/2+4);
        ctx.fillStyle='#ffca28'; ctx.fillText('25–44 Impending',gx+gw*0.35,gy+gh/2+4);
        ctx.fillStyle='#ef5350'; ctx.fillText('≥45 Storm',gx+gw*0.725,gy+gh/2+4);
        // tick marks
        [25,45,100].forEach(function(v){
            var tx=gx+gw*(v/maxSc);
            ctx.strokeStyle='#666'; ctx.lineWidth=1;
            ctx.beginPath(); ctx.moveTo(tx,gy); ctx.lineTo(tx,gy+gh); ctx.stroke();
        });

        // Score display
        ctx.fillStyle=fcol; ctx.font='bold 28px sans-serif'; ctx.textAlign='left';
        ctx.fillText(sc, gx, gy+gh+28);
        ctx.fillStyle='#888'; ctx.font='11px sans-serif';
        ctx.fillText('/ 100  Burch-Wartofsky Score', gx+44, gy+gh+24);
        var verdict=sc<25?'Storm Unlikely':sc<45?'Impending Storm':'THYROID STORM';
        ctx.fillStyle=fcol; ctx.font='bold 12px sans-serif';
        ctx.fillText(verdict, gx+44, gy+gh+40);

        // Category breakdown bars
        var barY=gy+gh+52, barH=16, barX=gx;
        ctx.fillStyle='#666'; ctx.font='9px sans-serif'; ctx.textAlign='left';
        cats.forEach(function(c,i){
            var bx=barX+Math.floor(i/3)*(gw/2+8);
            var by=barY+Math.floor(i%3)*(barH+6);
            var sc2=c.opts[c.cur];
            var maxS=c.opts[c.opts.length-1];
            ctx.fillStyle='#1a1a1a'; ctx.fillRect(bx,by,gw/2,barH);
            ctx.fillStyle='#29b6f633';
            ctx.fillRect(bx,by,maxS>0?(gw/2*(sc2/maxS)):0,barH);
            ctx.strokeStyle='#333'; ctx.lineWidth=1; ctx.strokeRect(bx,by,gw/2,barH);
            ctx.fillStyle='#aaa'; ctx.font='9px sans-serif'; ctx.textAlign='left';
            ctx.fillText(c.n+': '+c.lbls[c.cur]+' (+'+sc2+')', bx+4, by+barH/2+3);
        });
    }
    draw();

    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;align-items:center;';
        cats.forEach(function(c,i){
            var b=document.createElement('button');
            var updateBtn=function(){
                b.textContent=c.n+' +'+c.opts[c.cur];
                b.style.cssText='font-size:10px;padding:2px 8px;border-radius:4px;cursor:pointer;'+
                    'border:1px solid #29b6f6;background:#29b6f611;color:#29b6f6;font-weight:700;';
            };
            updateBtn();
            b.addEventListener('click',function(){
                c.cur=(c.cur+1)%c.opts.length;
                var pkeys=['t','h','c','g','a','p'];
                P[pkeys[i]]=c.cur;
                updateBtn(); draw();
            });
            row.appendChild(b);
        });
        var rst=document.createElement('button');
        rst.textContent='Reset';
        rst.style.cssText='font-size:10px;padding:2px 8px;border-radius:4px;cursor:pointer;'+
            'border:1px solid #666;background:transparent;color:#666;';
        rst.addEventListener('click',function(){
            cats.forEach(function(c,i){c.cur=0;var pk=['t','h','c','g','a','p'];P[pk[i]]=0;});
            row.querySelectorAll('button:not(:last-child)').forEach(function(b,i){
                b.textContent=cats[i].n+' +0';
            });
            draw();
        });
        row.appendChild(rst);
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 5: Adrenal Crisis — Cortisol Response Curves ───────────────────────
RF['adrenal_crisis'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;
    var mx=50, my=16, pw=W-mx-18, ph=H-my-46;
    var xD=60, yD=50;
    function xp(v){return mx+(v/xD)*pw;}
    function yp(v){return my+ph-(v/yD)*ph;}

    var showNorm = P.sn!=null?P.sn:true;
    var showInsuf= P.si!=null?P.si:true;
    var showCrit = P.sc!=null?P.sc:false;

    function draw(){
        _cl(ctx,W,H);
        _gd(ctx,mx,my,pw,ph,10,xD,10,yD);
        _ax(ctx,mx,my,pw,ph);

        // Threshold lines
        ctx.strokeStyle=_AM; ctx.lineWidth=1.5; ctx.setLineDash([5,4]);
        ctx.beginPath(); ctx.moveTo(mx,yp(18)); ctx.lineTo(mx+pw,yp(18)); ctx.stroke();
        ctx.fillStyle=_AM; ctx.font='9px sans-serif'; ctx.textAlign='left';
        ctx.fillText('18 mcg/dL (adequacy)',mx+3,yp(18)-4);

        ctx.strokeStyle=_GN; ctx.lineWidth=1; ctx.setLineDash([3,4]);
        ctx.beginPath(); ctx.moveTo(mx,yp(20)); ctx.lineTo(mx+pw,yp(20)); ctx.stroke();
        ctx.fillStyle=_GN+'99'; ctx.fillText('20 (stim response)',mx+3,yp(20)-4);
        ctx.setLineDash([]);

        // Cosyntropin marker
        ctx.strokeStyle='#555'; ctx.lineWidth=1;
        ctx.beginPath(); ctx.moveTo(xp(0),my); ctx.lineTo(xp(0),my+ph); ctx.stroke();
        ctx.fillStyle='#666'; ctx.font='8px sans-serif'; ctx.textAlign='center';
        ctx.fillText('Cosyntropin', xp(0), my+ph+10);
        ctx.fillText('250mcg IV', xp(0), my+ph+20);

        // Normal response curve
        if(showNorm){
            _crv(ctx,function(t){
                return t<=0?20:20+(38-20)*(1-Math.exp(-t/15));
            },0,60,mx,my,pw,ph,xD,yD,_GN,2.5);
            ctx.fillStyle=_GN; ctx.font='bold 9px sans-serif'; ctx.textAlign='left';
            ctx.fillText('Normal Response',xp(5),yp(36));
        }

        // Adrenal insufficiency curve
        if(showInsuf){
            _crv(ctx,function(t){
                return t<=0?4:4+(8-4)*(1-Math.exp(-t/20));
            },0,60,mx,my,pw,ph,xD,yD,_RE,2.5);
            ctx.fillStyle=_RE; ctx.font='bold 9px sans-serif'; ctx.textAlign='left';
            ctx.fillText('Adrenal Insufficiency',xp(5),yp(10));
        }

        // Critical illness-related corticosteroid insufficiency (CIRCI)
        if(showCrit){
            _crv(ctx,function(t){
                return t<=0?10:10+(16-10)*(1-Math.exp(-t/18));
            },0,60,mx,my,pw,ph,xD,yD,_AM,2);
            ctx.fillStyle=_AM; ctx.font='bold 9px sans-serif'; ctx.textAlign='left';
            ctx.fillText('CIRCI (blunted)',xp(5),yp(17));
        }

        // Axes labels
        ctx.fillStyle='#888'; ctx.font='10px sans-serif'; ctx.textAlign='center';
        [0,15,30,45,60].forEach(function(v){ ctx.fillText(v+'min',xp(v),my+ph+14); });
        ctx.fillText('Time after Cosyntropin',mx+pw/2,H-3);
        ctx.textAlign='right';
        [0,10,18,20,30,40,50].forEach(function(v){ ctx.fillText(v,mx-4,yp(v)+4); });
        _rl(ctx,'Cortisol (mcg/dL)',14,my+ph/2);
    }
    draw();

    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;align-items:center;';
        var bn=_mkB('Normal',_GN,showNorm,function(on){
            showNorm=on;P.sn=on;
            bn.style.background=on?_GN+'22':'transparent';bn.style.color=on?_GN:'#555';bn._on=on;draw();});
        var bi=_mkB('Insuf.',_RE,showInsuf,function(on){
            showInsuf=on;P.si=on;
            bi.style.background=on?_RE+'22':'transparent';bi.style.color=on?_RE:'#555';bi._on=on;draw();});
        var bc=_mkB('CIRCI',_AM,showCrit,function(on){
            showCrit=on;P.sc=on;
            bc.style.background=on?_AM+'22':'transparent';bc.style.color=on?_AM:'#555';bc._on=on;draw();});
        row.appendChild(bn); row.appendChild(bi); row.appendChild(bc);
        ctrl.appendChild(row);
    }
}
"""

# ── Card Definitions ──────────────────────────────────────────────────────────
CARDS = [
    # ═══ dka_severity ════════════════════════════════════════════════════════
    (
        "On the DKA Severity chart, Moderate DKA is defined by arterial pH "
        "_______ and serum HCO₃ _______.",

        "pH 7.00–7.24 (below 7.25 but at or above 7.00)\n"
        "| HCO₃ 10–14.9 mEq/L\n"
        "→ CCRN KEY: DKA severity: Mild pH 7.25–7.30 / HCO₃ 15–18; "
        "Moderate pH 7.00–7.24 / HCO₃ 10–14.9; Severe pH <7.00 / HCO₃ <10.\n"
        "→ MASTERY NOTE: Severity drives urgency — severe DKA (pH <7.0) requires "
        "ICU, continuous insulin drip, and hourly labs; do not give bicarb unless pH <6.9 "
        "per ADA guidelines.",

        'tier-review',
        _DH,
        DID['dka_hhs'],
        'dka_severity',
        '{}',
        'chart-l1'
    ),
    (
        "A patient's HCO₃ drops from 16 to 7 mEq/L during DKA treatment. "
        "On the severity chart this represents _______, most likely caused by "
        "_______.",

        "Worsening from Mild to Severe DKA zone\n"
        "| Most likely cause: inadequate insulin dosing, missed potassium "
        "replacement causing insulin hold, or new precipitant\n"
        "→ CCRN KEY: HCO₃ <10 with pH <7.0 = Severe DKA. Falling HCO₃ "
        "despite treatment requires reassessment of insulin rate, fluid choice, "
        "and K⁺ replacement.\n"
        "→ MASTERY NOTE: Insulin cannot be given if K⁺ <3.3 mEq/L "
        "— hypokalemia kills before DKA does. Always replace K⁺ first, "
        "then restart insulin.",

        'tier-high',
        _DH,
        DID['dka_hhs'],
        'dka_severity',
        '{}',
        'chart-l2'
    ),
    (
        "DKA patient: pH 6.91, HCO₃ 6, glucose 510, K⁺ 3.1 mEq/L. "
        "The chart shows Severe DKA. First intervention is _______, not "
        "_______, because _______.",

        "Replace K⁺ to ≥3.3 mEq/L BEFORE starting insulin\n"
        "| Not: start insulin infusion first\n"
        "| Because: insulin drives K⁺ intracellularly — starting insulin "
        "with K⁺ 3.1 risks fatal hypokalemia and cardiac arrhythmia\n"
        "→ CCRN KEY: Severe DKA + K⁺ <3.3 = potassium replacement is the "
        "priority. Hold insulin, give K⁺ 20–40 mEq/hr IV, recheck before "
        "insulin start.\n"
        "→ MASTERY NOTE: Also begin aggressive NS or LR resuscitation "
        "(1–1.5 L/hr first hour) — volume depletion is always present in DKA.",

        'tier-critical',
        _DH,
        DID['dka_hhs'],
        'dka_severity',
        '{"hi":3}',
        'chart-l3'
    ),

    # ═══ dka_hhs_compare ═════════════════════════════════════════════════════
    (
        "On the DKA vs HHS comparison chart, the single most reliable "
        "differentiating feature between the two disorders is _______.",

        "Ketones: DKA shows ++ to +++ ketonemia/ketonuria; HHS shows absent or trace ketones\n"
        "| Anion gap is also key: DKA elevated (>12), HHS normal (8–12)\n"
        "→ CCRN KEY: DKA = insulin deficiency → ketogenesis → anion-gap acidosis. "
        "HHS = relative insulin excess prevents ketosis but not hyperglycemia.\n"
        "→ MASTERY NOTE: Osmolality separates severity in HHS (>320 mOsm/kg "
        "required for diagnosis), while pH separates severity in DKA. "
        "Both can coexist in the same patient.",

        'tier-review',
        _DH,
        DID['dka_hhs'],
        'dka_hhs_compare',
        '{}',
        'chart-l1'
    ),
    (
        "The comparison chart shows HHS glucose averaging >600 mg/dL with "
        "osmolality >320 mOsm/kg. These values are higher than DKA because "
        "_______.",

        "HHS develops over days (insidious onset), allowing extreme hyperglycemia "
        "to accumulate without ketoacidosis halting intake\n"
        "| Residual insulin in HHS prevents lipolysis and ketogenesis but cannot "
        "control glucose; patients often continue eating/drinking concentrated fluids\n"
        "→ CCRN KEY: HHS onset is days vs DKA hours. The longer timeline allows "
        "glucose and osmolality to reach extreme levels. CNS depression (lethargy, "
        "coma) correlates with osmolality, not glucose alone.\n"
        "→ MASTERY NOTE: Free water deficit in HHS is massive (8–10 L). "
        "Use 0.45% NaCl once hemodynamically stable; NS initially for resuscitation.",

        'tier-high',
        _DH,
        DID['dka_hhs'],
        'dka_hhs_compare',
        '{}',
        'chart-l2'
    ),
    (
        "Patient arrives: glucose 740 mg/dL, serum osmolality 338 mOsm/kg, "
        "pH 7.36, HCO₃ 23, ketones trace. The comparison chart pattern "
        "matches _______, requiring _______ as the initial priority, not "
        "_______, because _______.",

        "HHS (Hyperosmolar Hyperglycemic State)\n"
        "| Priority: aggressive IV fluid resuscitation (NS 1 L/hr × first 2 hr, "
        "then 0.45% NaCl) to correct hyperosmolality\n"
        "| Not: high-dose insulin infusion as primary\n"
        "| Because: rapid glucose correction without fluid replacement worsens "
        "hyperosmolality and risks cerebral edema; lower glucose slowly "
        "(target ~50 mg/hr drop)\n"
        "→ CCRN KEY: HHS fluid deficit is 8–10 L. Fluids first, then low-dose "
        "insulin (0.05–0.1 units/kg/hr or none until glucose <300). "
        "Add D5W when glucose reaches 300 mg/dL.\n"
        "→ MASTERY NOTE: HHS mortality (5–20%) exceeds DKA (1–5%) due to "
        "age, precipitating illness, and delayed recognition.",

        'tier-critical',
        _DH,
        DID['dka_hhs'],
        'dka_hhs_compare',
        '{}',
        'chart-l3'
    ),

    # ═══ anion_gap_delta ══════════════════════════════════════════════════════
    (
        "On the anion gap chart with Na 138, Cl 100, HCO₃ 14, the anion "
        "gap = _______ mEq/L, classified as _______.",

        "AG = 138 − (100 + 14) = 24 mEq/L — elevated (normal 8–12)\n"
        "| Classification: high anion gap metabolic acidosis\n"
        "→ CCRN KEY: AG = Na⁺ − (Cl⁻ + HCO₃⁻). "
        "Normal 8–12 mEq/L (without albumin correction). "
        "Elevation indicates unmeasured anions: lactate, ketones, uremia, toxins.\n"
        "→ MASTERY NOTE: MUDPILES mnemonic for high AG causes: "
        "Methanol, Uremia, DKA, Propylene glycol, Isoniazid/Iron, Lactic acidosis, "
        "Ethylene glycol, Salicylates. ICU patients most often: lactate or DKA.",

        'tier-review',
        _DH,
        DID['dka_hhs'],
        'anion_gap_delta',
        '{"na":138,"cl":100,"hco":14}',
        'chart-l1'
    ),
    (
        "A DKA patient has AG 28, HCO₃ 8. The delta-delta ratio = "
        "_______, indicating _______.",

        "Δ/Δ = (28−12) / (24−8) = 16/16 = 1.0 — pure AG metabolic acidosis\n"
        "| Interpretation range: 1.0–2.0 = pure AG acidosis; "
        "<0.4 = hyperchloremic; 0.4–1.0 = mixed; >2.0 = AG + metabolic alkalosis\n"
        "→ CCRN KEY: Delta-delta (AG ratio) reveals hidden mixed acid-base disorders. "
        "In DKA, delta-delta ~1 confirms pure AG acidosis. "
        "After saline resuscitation, delta-delta drops (<1) as hyperchloremic acidosis "
        "develops alongside the resolving ketoacidosis.\n"
        "→ MASTERY NOTE: A delta-delta >2 in a DKA patient suggests pre-existing "
        "metabolic alkalosis (vomiting, diuretics) masking the true HCO₃ deficit.",

        'tier-high',
        _DH,
        DID['dka_hhs'],
        'anion_gap_delta',
        '{"na":138,"cl":102,"hco":8}',
        'chart-l2'
    ),
    (
        "Post-resuscitation DKA: Na 136, Cl 112, HCO₃ 12. "
        "AG = _______, delta-delta = _______, indicating _______, "
        "which is caused by _______.",

        "AG = 136 − (112+12) = 12 (normal range)\n"
        "| Δ/Δ = (12−12)/(24−12) = 0/12 = 0 — hyperchloremic metabolic acidosis\n"
        "| Cause: dilutional hyperchloremic acidosis from large-volume normal saline "
        "(0.9% NaCl = 154 mEq/L Cl⁻)\n"
        "→ CCRN KEY: Resolving DKA with low AG + low delta-delta = "
        "saline-induced hyperchloremic acidosis. This is expected and self-resolving; "
        "do not increase insulin or give bicarb.\n"
        "→ MASTERY NOTE: Balanced crystalloids (LR or PlasmaLyte) have lower "
        "chloride than NS and reduce hyperchloremic acidosis in DKA. "
        "Some protocols now prefer LR after initial resuscitation.",

        'tier-critical',
        _DH,
        DID['dka_hhs'],
        'anion_gap_delta',
        '{"na":136,"cl":112,"hco":12}',
        'chart-l3'
    ),

    # ═══ thyroid_storm ════════════════════════════════════════════════════════
    (
        "On the Burch-Wartofsky scoring chart, thyroid storm is diagnosed "
        "when the score reaches _______ or above. A score of 25–44 "
        "indicates _______.",

        "Score ≥45 = thyroid storm diagnosis\n"
        "| Score 25–44 = impending storm (treat as storm)\n"
        "→ CCRN KEY: Burch-Wartofsky categories: Temperature (–30 pts), "
        "HR (–25 pts), AF (+10), CNS effects (–30 pts), "
        "GI/Hepatic (–20 pts), Precipitant (+10). Maximum score ~125.\n"
        "→ MASTERY NOTE: Treat impending storm (25–44) the same as confirmed storm "
        "— do not wait for confirmatory labs. Thyroid storm is a clinical diagnosis; "
        "TSH and free T4 may not yet be available in acute presentation.",

        'tier-review',
        _TA,
        DID['thyroid_adrenal'],
        'thyroid_storm',
        '{}',
        'chart-l1'
    ),
    (
        "On the scoring chart, a patient with temp 39.5°C (+25), HR 138 (+20), "
        "AF (+10), delirium (+20), precipitant surgery (+10) scores _______. "
        "Treatment priorities include _______ and _______.",

        "Score = 25+20+10+20+10 = 85 — Thyroid Storm\n"
        "| Priority 1: PTU 500–1000 mg loading dose (blocks new hormone synthesis "
        "AND peripheral T4→T3 conversion)\n"
        "| Priority 2: Propranolol IV (controls tachycardia and blocks peripheral T4→T3)\n"
        "| Also: hydrocortisone 100 mg IV q8h (prevents adrenal crisis in thyrotoxicosis)\n"
        "→ CCRN KEY: 4-drug protocol: PTU (or MMI) + iodine (Lugol 1 hr after PTU) + "
        "β-blocker + steroid. Give PTU BEFORE iodine — iodine first can worsen storm.\n"
        "→ MASTERY NOTE: Aspirin is CONTRAINDICATED in thyroid storm "
        "— it displaces thyroid hormone from binding proteins, worsening thyrotoxicosis.",

        'tier-high',
        _TA,
        DID['thyroid_adrenal'],
        'thyroid_storm',
        '{"t":5,"h":4,"a":1,"c":2,"p":1}',
        'chart-l2'
    ),
    (
        "Postoperative thyroidectomy patient: suddenly agitated, temp 40.2°C, "
        "HR 148, AF, new liver enzyme elevation. Burch-Wartofsky score = _______. "
        "You hold _______ and give _______ first because _______.",

        "Score: Temp 40.2°C (+30) + HR 148 (+25) + AF (+10) + "
        "Agitation/CNS moderate (+20) + GI/Hepatic (+10) + Precipitant surgery (+10) = 105\n"
        "| Hold: aspirin (displaces T4 from binding proteins, worsens storm)\n"
        "| Give first: PTU 500 mg PO/NG THEN Lugol iodine 10 drops q8h "
        "(must wait 1 hr after PTU)\n"
        "| Because: iodine given before thionamide causes acute hormone release\n"
        "→ CCRN KEY: Post-thyroidectomy storm typically within 12–24 hr. "
        "Cool patient aggressively (cooling blanket, acetaminophen — NOT aspirin). "
        "ICU admission, continuous cardiac monitoring.\n"
        "→ MASTERY NOTE: Lithium can replace iodine if iodine-allergic. "
        "Dexamethasone 2 mg q6h preferred over hydrocortisone if concurrent "
        "adrenal insufficiency suspected.",

        'tier-critical',
        _TA,
        DID['thyroid_adrenal'],
        'thyroid_storm',
        '{"t":6,"h":5,"a":1,"c":2,"g":1,"p":1}',
        'chart-l3'
    ),

    # ═══ adrenal_crisis ═══════════════════════════════════════════════════════
    (
        "On the cortisol response chart, adrenal insufficiency is confirmed "
        "when post-cosyntropin cortisol at 30–60 min fails to reach "
        "_______ mcg/dL.",

        "Peak cortisol <18 mcg/dL at 30 or 60 min = adrenal insufficiency\n"
        "| Normal response: peak ≥18–20 mcg/dL above baseline, "
        "or absolute peak ≥18 mcg/dL\n"
        "→ CCRN KEY: Cosyntropin (synthetic ACTH) 250 mcg IV; "
        "cortisol drawn at 0, 30, 60 min. "
        "Failure to rise above 18 mcg/dL = adrenal insufficiency.\n"
        "→ MASTERY NOTE: In critical illness (septic shock), a random cortisol "
        "<10 mcg/dL is diagnostic without stimulation testing. "
        "CIRCI (critical illness-related corticosteroid insufficiency) "
        "is defined as delta-cortisol <9 mcg/dL after stim or random <10.",

        'tier-review',
        _TA,
        DID['thyroid_adrenal'],
        'adrenal_crisis',
        '{"sn":1,"si":1,"sc":0}',
        'chart-l1'
    ),
    (
        "The cortisol response chart shows a flat curve staying below 10 mcg/dL "
        "after cosyntropin. This differentiates primary from secondary adrenal "
        "insufficiency by _______.",

        "Primary AI (Addison's): both baseline cortisol AND ACTH are abnormal — "
        "low cortisol + HIGH ACTH (no negative feedback)\n"
        "| Secondary AI (pituitary): low cortisol + LOW/normal ACTH "
        "(pituitary failure = no ACTH signal to adrenal glands)\n"
        "| The stimulation test shows cortisol response (or lack); "
        "ACTH level distinguishes primary vs secondary\n"
        "→ CCRN KEY: Both cause hypocortisolism but mechanism differs. "
        "Primary: adrenal gland destroyed (autoimmune, hemorrhage, infection). "
        "Secondary: pituitary or hypothalamic dysfunction (prolonged steroid use = #1 ICU cause).\n"
        "→ MASTERY NOTE: Waterhouse-Friderichsen syndrome = "
        "bilateral adrenal hemorrhage from meningococcemia — "
        "adrenal crisis in septic patient who deteriorates despite pressors.",

        'tier-high',
        _TA,
        DID['thyroid_adrenal'],
        'adrenal_crisis',
        '{"sn":1,"si":1,"sc":1}',
        'chart-l2'
    ),
    (
        "ICU patient on 3 vasopressors for septic shock, cortisol 7 mcg/dL. "
        "The chart shows an insufficient response. Empiric treatment is "
        "_______, not _______, because _______.",

        "Hydrocortisone 200–300 mg/day IV (50 mg IV q6h or 200 mg continuous infusion)\n"
        "| Not: dexamethasone as first-line in this situation (though dexamethasone "
        "can be used if stim test has NOT yet been drawn)\n"
        "| Because: hydrocortisone replaces both glucocorticoid AND mineralocorticoid "
        "activity needed in adrenal crisis; dexamethasone lacks mineralocorticoid effect "
        "and suppresses the HPA axis, making subsequent stim testing invalid\n"
        "→ CCRN KEY: Vasopressor-refractory shock + cortisol <10 mcg/dL = "
        "empiric stress-dose steroids. "
        "ACTH1-24 stim test can still be done after hydrocortisone if diagnosis uncertain.\n"
        "→ MASTERY NOTE: Fludrocortisone 50 mcg daily added for primary AI. "
        "Expect vasopressor weaning within 24–48 hr of steroid initiation "
        "if adrenal crisis is the cause. Taper steroids when vasopressors weaned.",

        'tier-critical',
        _TA,
        DID['thyroid_adrenal'],
        'adrenal_crisis',
        '{"sn":1,"si":1,"sc":0}',
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
