#!/usr/bin/env python3
"""chunk37_charts.py — Ph5 GI/Hepatic: Critical GI & Hepatic (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_36.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_37.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c37')
CHUNK_NUM   = 37
MID_BASE    = 1_800_005_030
CHART_ORDER = ['gi_bleed_severity', 'hepatic_enceph', 'meld_score',
               'pancreatitis_bisap', 'abdominal_compartment']

_GI = 'Ph5 · \U0001f7e0 T2 · GI — Critical GI & Hepatic'

RF = {}

# ── Chart 1: Upper GI Bleed — Blatchford Risk Score ───────────────────────────
RF['gi_bleed_severity'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;

    var items=[
        {n:'SBP < 90 mmHg',       pts:3, k:'s'},
        {n:'HR ≥ 100 bpm',         pts:1, k:'h'},
        {n:'Hgb < 10 g/dL',        pts:3, k:'g'},
        {n:'BUN > 25 mg/dL',       pts:2, k:'b'},
        {n:'Melena or syncope',    pts:2, k:'m'},
        {n:'Liver/cardiac disease',pts:2, k:'l'},
    ];
    items.forEach(function(it){ it.on = P[it.k]||0; });

    function score(){ return items.reduce(function(s,it){return s+(it.on?it.pts:0);},0); }

    var actions=[
        {lo:0, hi:2,  label:'Low Risk',       sub:'Outpatient management possible',  col:'#4caf50'},
        {lo:3, hi:5,  label:'Moderate Risk',  sub:'Admission, PPI, GI consult 24h',  col:'#ffca28'},
        {lo:6, hi:10, label:'High Risk',       sub:'ICU, scope within 12 h',          col:'#ff7043'},
        {lo:11,hi:20, label:'Severe / Shock',  sub:'MTP, scope STAT, ICU',            col:'#ef5350'},
    ];

    function draw(){
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);
        var sc=score();
        var act=actions[sc<=2?0:sc<=5?1:sc<=10?2:3];

        // Score gauge
        var gx=14,gy=16,gw=W-28,gh=26,maxSc=14;
        var fx=Math.min(sc/maxSc,1);
        ctx.fillStyle='#4caf5022'; ctx.fillRect(gx,gy,gw*2/14,gh);
        ctx.fillStyle='#ffca2822'; ctx.fillRect(gx+gw*2/14,gy,gw*3/14,gh);
        ctx.fillStyle='#ff704322'; ctx.fillRect(gx+gw*5/14,gy,gw*5/14,gh);
        ctx.fillStyle='#ef535022'; ctx.fillRect(gx+gw*10/14,gy,gw*4/14,gh);
        ctx.fillStyle=act.col+'bb'; ctx.fillRect(gx,gy,gw*fx,gh);
        ctx.strokeStyle='#444'; ctx.lineWidth=1; ctx.strokeRect(gx,gy,gw,gh);

        ctx.font='9px sans-serif'; ctx.textAlign='center';
        ctx.fillStyle='#4caf50'; ctx.fillText('Low 0–2',gx+gw*1/14,gy+gh/2+3);
        ctx.fillStyle='#ffca28'; ctx.fillText('Mod 3–5',gx+gw*3.5/14,gy+gh/2+3);
        ctx.fillStyle='#ff7043'; ctx.fillText('High 6–10',gx+gw*7.5/14,gy+gh/2+3);
        ctx.fillStyle='#ef5350'; ctx.fillText('Severe >10',gx+gw*12/14,gy+gh/2+3);

        // Score + verdict
        ctx.fillStyle=act.col; ctx.font='bold 30px sans-serif'; ctx.textAlign='left';
        ctx.fillText(sc, gx, gy+gh+34);
        ctx.font='bold 13px sans-serif';
        ctx.fillText(act.label, gx+44, gy+gh+26);
        ctx.fillStyle='#888'; ctx.font='11px sans-serif';
        ctx.fillText(act.sub, gx+44, gy+gh+42);

        // Item breakdown bars
        var barY=gy+gh+60, barH=18;
        items.forEach(function(it,i){
            var bx=gx+Math.floor(i/3)*(gw/2+8);
            var by=barY+Math.floor(i%3)*(barH+5);
            ctx.fillStyle=it.on?act.col+'33':'#111';
            ctx.fillRect(bx,by,gw/2,barH);
            ctx.strokeStyle=it.on?act.col:'#2a2a2a';
            ctx.lineWidth=it.on?2:1; ctx.strokeRect(bx,by,gw/2,barH);
            ctx.fillStyle=it.on?act.col:'#555';
            ctx.font=(it.on?'bold ':'')+'9px sans-serif'; ctx.textAlign='left';
            ctx.fillText((it.on?'✓ ':'   ')+it.n+' (+'+it.pts+')', bx+4, by+barH/2+3);
        });
    }
    draw();

    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;align-items:center;';
        var btns=[];
        items.forEach(function(it,i){
            var b=_mkB(it.n, _AM, it.on, function(on){
                it.on=on?1:0; P[it.k]=it.on;
                b._on=on;
                b.style.background=on?_AM+'22':'transparent';
                b.style.color=on?_AM:'#555';
                draw();
            });
            b._on=it.on; b.style.background=it.on?_AM+'22':'transparent'; b.style.color=it.on?_AM:'#555';
            btns.push(b); row.appendChild(b);
        });
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: Hepatic Encephalopathy — West Haven Grade Progression ─────────────
RF['hepatic_enceph'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;
    var curGrade = P.g != null ? P.g : 0;

    var grades=[
        {g:0,  label:'Grade 0 (Covert)',  nh3:'Normal',  cli:'No overt symptoms; subtle psychomotor slowing',    tx:'Identify precipitant; lactulose titrate',col:'#4caf50'},
        {g:1,  label:'Grade I',           nh3:'55–99',   cli:'Shortened attention, sleep disturbance, mild confusion', tx:'Lactulose 30 mL BID-TID (goal 2-3 BM/day)', col:'#8bc34a'},
        {g:2,  label:'Grade II',          nh3:'100–149', cli:'Lethargy, disorientation, asterixis (flap)',       tx:'Lactulose + rifaximin 550 mg BID; fall precautions', col:'#ffca28'},
        {g:3,  label:'Grade III',         nh3:'150–199', cli:'Marked confusion, somnolent but rousable, incoherent', tx:'ICU; lactulose via NG; rifaximin; zinc; airway watch', col:'#ff7043'},
        {g:4,  label:'Grade IV (Coma)',   nh3:'>200',    cli:'Unresponsive; decerebrate/decorticate; coma',      tx:'Intubate for airway; ICU; ICP monitoring if ALF; transplant eval', col:'#ef5350'},
    ];

    var g=grades[Math.min(curGrade, grades.length-1)];

    var rH=42, tT=12, cW=[120,70,200,230];

    function draw(){
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);

        // Header
        ['Grade','NH₃ (µg/dL)','Clinical Features','ICU Management'].forEach(function(h,ci){
            var x=0; for(var k=0;k<ci;k++) x+=cW[k];
            ctx.fillStyle='#1c1c1c'; ctx.fillRect(x,tT,cW[ci],24);
            ctx.strokeStyle='#333'; ctx.lineWidth=1; ctx.strokeRect(x,tT,cW[ci],24);
            ctx.fillStyle='#aaa'; ctx.font='bold 9px sans-serif'; ctx.textAlign='center';
            ctx.fillText(h, x+cW[ci]/2, tT+16);
        });

        grades.forEach(function(gr,ri){
            var y=tT+24+ri*rH;
            var hl=ri===curGrade;
            var vals=[gr.label, gr.nh3, gr.cli, gr.tx];
            for(var ci=0;ci<4;ci++){
                var x=0; for(var k=0;k<ci;k++) x+=cW[k];
                ctx.fillStyle=hl?gr.col+'33':(ri%2?'#111':'#0d0d0d');
                ctx.fillRect(x,y,cW[ci],rH);
                ctx.strokeStyle=hl?gr.col:'#222'; ctx.lineWidth=hl?2:1;
                ctx.strokeRect(x,y,cW[ci],rH);
                ctx.fillStyle=hl?(ci===0?gr.col:'#eee'):gr.col+(ci===0?'99':'44');
                ctx.font=(hl&&ci===0?'bold ':'')+'9px sans-serif';
                ctx.textAlign=ci===0?'center':'left';
                // word wrap manually (2 lines)
                var txt=vals[ci], maxW=cW[ci]-8;
                ctx.fillText(txt, ci===0?x+cW[ci]/2:x+4, y+rH/2+(ci>1?-5:4));
            }
        });

        // Active grade callout
        ctx.fillStyle=g.col; ctx.font='bold 10px sans-serif'; ctx.textAlign='right';
        ctx.fillText('Active: Grade '+curGrade+' — NH₃ '+g.nh3+' µg/dL', W-6, tT+24+grades.length*rH+14);
    }
    draw();

    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;align-items:center;';
        var sp=document.createElement('span');
        sp.style.cssText='font-size:10px;font-weight:800;color:#666;';
        sp.textContent='GRADE:'; row.appendChild(sp);
        var btns=[];
        grades.forEach(function(gr,i){
            var b=_mkB(''+gr.g,gr.col,curGrade===i,function(on){
                curGrade=i; P.g=i;
                g=grades[i];
                btns.forEach(function(x,j){
                    x._on=j===i;
                    x.style.background=j===i?grades[j].col+'22':'transparent';
                    x.style.color=j===i?grades[j].col:'#555';
                });
                draw();
            });
            btns.push(b); row.appendChild(b);
        });
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 3: MELD Score Calculator ───────────────────────────────────────────
RF['meld_score'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;
    var curCr=P.cr||1.5, curBili=P.bi||3.0, curINR=P.inr||1.8;

    var mort=[
        {lo:0,  hi:9,  m:'< 4%',  label:'<10',    col:'#4caf50'},
        {lo:10, hi:19, m:'~27%',  label:'10–19',  col:'#ffca28'},
        {lo:20, hi:29, m:'~76%',  label:'20–29',  col:'#ff7043'},
        {lo:30, hi:39, m:'~83%',  label:'30–39',  col:'#ef5350'},
        {lo:40, hi:99, m:'~100%', label:'≥40',    col:'#ce93d8'},
    ];

    function meld(cr,bi,inr){
        var c=Math.max(1.0,Math.min(4.0,cr));
        var b=Math.max(1.0,bi);
        var r=Math.max(1.0,inr);
        return Math.round(3.78*Math.log(b)+11.2*Math.log(r)+9.57*Math.log(c)+6.43);
    }
    function mortRow(sc){
        for(var i=0;i<mort.length;i++) if(sc<=mort[i].hi) return mort[i];
        return mort[mort.length-1];
    }

    function draw(){
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);
        var sc=meld(curCr,curBili,curINR);
        var mr=mortRow(sc);

        // Big score
        ctx.fillStyle=mr.col; ctx.font='bold 60px sans-serif'; ctx.textAlign='center';
        ctx.fillText(sc, W/2, 74);
        ctx.fillStyle='#666'; ctx.font='12px sans-serif';
        ctx.fillText('MELD Score', W/2, 94);

        // Formula display
        ctx.fillStyle='#444'; ctx.font='10px sans-serif'; ctx.textAlign='center';
        ctx.fillText('3.78·ln(bili '+curBili.toFixed(1)+') + 11.2·ln(INR '+curINR.toFixed(1)+') + 9.57·ln(Cr '+curCr.toFixed(1)+') + 6.43',
            W/2, 112);

        // Gauge
        var gx=16, gy=122, gw=W-32, gh=22, maxSc=45;
        var ranges=[[0,10,'#4caf5033'],[10,20,'#ffca2833'],[20,30,'#ff704333'],[30,40,'#ef535033'],[40,45,'#ce93d833']];
        ranges.forEach(function(r){
            var x=gx+gw*(r[0]/maxSc);
            ctx.fillStyle=r[2]; ctx.fillRect(x,gy,gw*(r[1]-r[0])/maxSc,gh);
        });
        var fx=Math.min(sc/maxSc,1);
        ctx.fillStyle=mr.col+'99'; ctx.fillRect(gx,gy,gw*fx,gh);
        ctx.strokeStyle='#444'; ctx.lineWidth=1; ctx.strokeRect(gx,gy,gw,gh);

        // Tick marks
        [10,15,20,30,40].forEach(function(v){
            var tx=gx+gw*(v/maxSc);
            ctx.strokeStyle='#555'; ctx.lineWidth=1;
            ctx.beginPath(); ctx.moveTo(tx,gy); ctx.lineTo(tx,gy+gh); ctx.stroke();
            ctx.fillStyle='#666'; ctx.font='9px sans-serif'; ctx.textAlign='center';
            ctx.fillText(v,tx,gy+gh+11);
        });

        // Mortality table
        var tx2=gx, ty=gy+gh+22, colW=gw/5;
        mort.forEach(function(m,i){
            var hl=sc>=m.lo&&sc<=m.hi;
            ctx.fillStyle=hl?m.col+'33':'#0d0d0d';
            ctx.fillRect(tx2+i*colW, ty, colW, 40);
            ctx.strokeStyle=hl?m.col:'#222'; ctx.lineWidth=hl?2:1;
            ctx.strokeRect(tx2+i*colW, ty, colW, 40);
            ctx.fillStyle=hl?m.col:'#555';
            ctx.font=(hl?'bold ':'')+'9px sans-serif'; ctx.textAlign='center';
            ctx.fillText(m.label, tx2+i*colW+colW/2, ty+15);
            ctx.fillText(m.m+' 90d', tx2+i*colW+colW/2, ty+30);
        });

        // Transplant threshold note
        ctx.fillStyle='#ff704388'; ctx.font='9px sans-serif'; ctx.textAlign='right';
        ctx.fillText('UNOS listing threshold ≥ 15',W-6,H-5);
    }
    draw();

    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;align-items:center;';
        row.appendChild(_mkS('Creatinine',0.5,4.0,0.1,curCr,
            function(v){return v.toFixed(1)+' mg/dL';},
            function(v){curCr=v;P.cr=v;draw();}));
        row.appendChild(_mkS('Bilirubin',0.5,30,0.5,curBili,
            function(v){return v.toFixed(1)+' mg/dL';},
            function(v){curBili=v;P.bi=v;draw();}));
        row.appendChild(_mkS('INR',1.0,5.0,0.1,curINR,
            function(v){return v.toFixed(1);},
            function(v){curINR=v;P.inr=v;draw();}));
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 4: Pancreatitis BISAP Score ────────────────────────────────────────
RF['pancreatitis_bisap'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;

    var items=[
        {n:'B — BUN > 25 mg/dL',              k:'B', sub:'Marker of volume depletion and systemic response'},
        {n:'I — Impaired mental status',      k:'I', sub:'Any disorientation, lethargy, or obtundation'},
        {n:'S — SIRS criteria (≥2)',          k:'S', sub:'Temp <36/>38, HR>90, RR>20, WBC <4k/>12k'},
        {n:'A — Age > 60 years',              k:'A', sub:'Independent predictor of severity'},
        {n:'P — Pleural effusion on imaging', k:'P', sub:'CT or CXR; marker of severe systemic inflammation'},
    ];
    items.forEach(function(it){ it.on=P[it.k]||0; });

    function score(){ return items.reduce(function(s,it){return s+(it.on?1:0);},0); }

    function draw(){
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);
        var sc=score();
        var col=sc<=2?_GN:sc<=3?_AM:_RE;
        var verdict=sc<=2?'Low Risk — mortality <1%':sc<=3?'Moderate Risk — mortality ~5%':'High Risk — mortality >15%';

        // Score display
        ctx.fillStyle=col; ctx.font='bold 46px sans-serif'; ctx.textAlign='left';
        ctx.fillText(sc+' / 5', 16, 56);
        ctx.font='bold 12px sans-serif'; ctx.fillText('BISAP Score', 16, 74);
        ctx.fillStyle='#888'; ctx.font='11px sans-serif'; ctx.fillText(verdict, 16, 92);

        // Score gauge
        var gx=16, gy=100, gw=W-32, gh=16;
        ctx.fillStyle=_GN+'22'; ctx.fillRect(gx,gy,gw*2/5,gh);
        ctx.fillStyle=_AM+'22'; ctx.fillRect(gx+gw*2/5,gy,gw*1/5,gh);
        ctx.fillStyle=_RE+'22'; ctx.fillRect(gx+gw*3/5,gy,gw*2/5,gh);
        ctx.fillStyle=col+'88'; ctx.fillRect(gx,gy,gw*sc/5,gh);
        ctx.strokeStyle='#444'; ctx.lineWidth=1; ctx.strokeRect(gx,gy,gw,gh);
        [1,2,3,4].forEach(function(v){
            var tx=gx+gw*v/5;
            ctx.strokeStyle='#555'; ctx.beginPath(); ctx.moveTo(tx,gy); ctx.lineTo(tx,gy+gh); ctx.stroke();
            ctx.fillStyle='#666'; ctx.font='9px sans-serif'; ctx.textAlign='center';
            ctx.fillText(v,tx,gy+gh+10);
        });

        // Item checklist
        items.forEach(function(it,i){
            var y=128+i*26;
            ctx.fillStyle=it.on?col+'22':'#111';
            ctx.fillRect(16,y,W-32,22);
            ctx.strokeStyle=it.on?col:'#222'; ctx.lineWidth=it.on?2:1;
            ctx.strokeRect(16,y,W-32,22);
            // checkbox
            ctx.fillStyle=it.on?col:'#333'; ctx.fillRect(22,y+5,12,12);
            ctx.fillStyle='#000'; if(it.on){ ctx.font='bold 10px sans-serif'; ctx.textAlign='center'; ctx.fillText('✓',28,y+15); }
            ctx.fillStyle=it.on?col:'#666';
            ctx.font=(it.on?'bold ':'')+'10px sans-serif'; ctx.textAlign='left';
            ctx.fillText(it.n, 40, y+13);
            ctx.fillStyle=it.on?col+'99':'#444';
            ctx.font='8px sans-serif'; ctx.fillText(it.sub, 40, y+22);
        });
    }
    draw();

    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;align-items:center;';
        var keys=['B','I','S','A','P'];
        keys.forEach(function(k,i){
            var it=items[i];
            var b=_mkB(k, _AM, it.on, function(on){
                it.on=on?1:0; P[k]=it.on;
                b._on=on; b.style.background=on?_AM+'22':'transparent'; b.style.color=on?_AM:'#555';
                draw();
            });
            b._on=it.on; b.style.background=it.on?_AM+'22':'transparent'; b.style.color=it.on?_AM:'#555';
            row.appendChild(b);
        });
        var rst=document.createElement('button');
        rst.textContent='Reset';
        rst.style.cssText='font-size:10px;padding:2px 8px;border-radius:4px;cursor:pointer;border:1px solid #666;background:transparent;color:#666;';
        rst.addEventListener('click',function(){
            items.forEach(function(it){ it.on=0; }); keys.forEach(function(k){ P[k]=0; });
            row.querySelectorAll('button:not(:last-child)').forEach(function(b){
                b._on=false; b.style.background='transparent'; b.style.color='#555';
            });
            draw();
        });
        row.appendChild(rst);
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 5: Abdominal Compartment Syndrome — IAP Zones ──────────────────────
RF['abdominal_compartment'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;
    var curIAP = P.iap != null ? P.iap : 12;

    var zones=[
        {lo:0,  hi:11, label:'Normal',    sub:'IAP 5–7 mmHg at rest',       col:'#4caf50'},
        {lo:12, hi:15, label:'IAH Grade I',sub:'Monitor; optimize fluids',    col:'#8bc34a'},
        {lo:16, hi:20, label:'IAH Grade II',sub:'Medical decompression; check organ function', col:'#ffca28'},
        {lo:21, hi:25, label:'IAH Grade III',sub:'Surgical decompression if organ dysfunction', col:'#ff7043'},
        {lo:26, hi:35, label:'IAH Grade IV',sub:'Decompressive laparotomy; > 25 = ACS threshold', col:'#ef5350'},
    ];
    var ACS_LINE=20;

    var mx=50, my=12, pw=W-mx-16, ph=H-my-58;
    var xLo=0, xHi=35, xR=xHi-xLo;
    function xp(v){return mx+(v-xLo)/xR*pw;}

    function activeZone(iap){
        for(var i=0;i<zones.length;i++) if(iap<=zones[i].hi) return i;
        return zones.length-1;
    }
    var az=activeZone(curIAP);

    function draw(){
        az=activeZone(curIAP);
        ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);

        // Zone bands
        zones.forEach(function(z,i){
            var dim=i!==az;
            ctx.fillStyle=z.col+(dim?'1a':'33');
            ctx.fillRect(xp(z.lo),my,xp(z.hi+1)-xp(z.lo),ph);
            ctx.fillStyle=z.col+(dim?'55':'cc');
            ctx.font='bold 8px sans-serif'; ctx.textAlign='center';
            var mx2=(xp(z.lo)+xp(z.hi+1))/2;
            ctx.fillText(z.label, mx2, my+14);
            ctx.fillStyle=z.col+(dim?'44':'99');
            ctx.font='7px sans-serif';
            // wrap sub at space
            var words=z.sub.split('; ');
            ctx.fillText(words[0], mx2, my+26);
            if(words[1]) ctx.fillText(words[1], mx2, my+36);
        });

        // Zone boundaries
        ctx.strokeStyle='#333'; ctx.lineWidth=1; ctx.setLineDash([2,3]);
        [12,16,21,26].forEach(function(v){
            ctx.beginPath(); ctx.moveTo(xp(v),my); ctx.lineTo(xp(v),my+ph); ctx.stroke();
        });
        ctx.setLineDash([]);

        // ACS threshold line
        ctx.strokeStyle=_RE; ctx.lineWidth=2; ctx.setLineDash([5,3]);
        ctx.beginPath(); ctx.moveTo(xp(ACS_LINE),my-4); ctx.lineTo(xp(ACS_LINE),my+ph); ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle=_RE; ctx.font='bold 9px sans-serif'; ctx.textAlign='center';
        ctx.fillText('ACS if organ', xp(ACS_LINE), my+ph+12);
        ctx.fillText('dysfunction', xp(ACS_LINE), my+ph+22);

        // Axes
        _ax(ctx,mx,my,pw,ph);
        ctx.fillStyle='#888'; ctx.font='10px sans-serif'; ctx.textAlign='center';
        [0,5,10,12,15,20,25,30,35].forEach(function(v){ ctx.fillText(v,xp(v),my+ph+12); });
        ctx.fillText('Intra-Abdominal Pressure (mmHg)',mx+pw/2,H-3);
        _rl(ctx,'IAH Grade',14,my+ph/2);

        // Patient marker
        var px=xp(curIAP);
        var zc=zones[az].col;
        ctx.fillStyle=zc;
        ctx.beginPath(); ctx.arc(px,my+ph/2,8,0,Math.PI*2); ctx.fill();
        ctx.fillStyle='#000'; ctx.font='bold 8px sans-serif'; ctx.textAlign='center';
        ctx.fillText(curIAP,px,my+ph/2+3);

        // Active verdict
        var z2=zones[az];
        ctx.fillStyle=z2.col; ctx.font='bold 10px sans-serif'; ctx.textAlign='left';
        ctx.fillText(curIAP+' mmHg — '+z2.label+': '+z2.sub, mx, H-6);
    }
    draw();

    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');
        row.style.cssText='display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;align-items:center;';
        row.appendChild(_mkS('Bladder Pressure',0,35,1,curIAP,
            function(v){return v.toFixed(0)+' mmHg';},
            function(v){curIAP=v;P.iap=v;draw();}));
        ctrl.appendChild(row);
    }
}
"""

# ── Card Definitions ──────────────────────────────────────────────────────────
CARDS = [
    # ═══ gi_bleed_severity ═══════════════════════════════════════════════════
    (
        "On the upper GI bleed risk chart, a patient with SBP 86 mmHg, "
        "HR 118, Hgb 8.2 g/dL, and liver cirrhosis scores _______ points, "
        "placing them in the _______ risk category.",

        "SBP <90 (+3) + HR ≥100 (+1) + Hgb <10 (+3) + liver disease (+2) = Score 9 — High Risk\n"
        "| Requires: ICU admission, GI consult for scope within 12 hours, "
        "2 large-bore IVs, type and crossmatch, PPI infusion\n"
        "→ CCRN KEY: Blatchford score ≥6 = high risk requiring inpatient endoscopy. "
        "Score ≥0 with any instability = ICU. Hemodynamic resuscitation precedes endoscopy "
        "unless uncontrolled bleeding.\n"
        "→ MASTERY NOTE: Target Hgb ≥7 g/dL for resuscitation in GI bleed "
        "(not ≥10 — over-transfusion worsens portal hypertension and variceal rebleeding). "
        "Exception: ACS or hemodynamic instability: target ≥8–9.",

        'tier-review',
        _GI,
        DID['gi_hepatic'],
        'gi_bleed_severity',
        '{"s":1,"h":1,"g":1,"l":1}',
        'chart-l1'
    ),
    (
        "The GI bleed risk chart shows high scores driven primarily by "
        "hemodynamic instability. This places variceal bleeding at higher "
        "risk than peptic ulcer bleeding because _______.",

        "Variceal bleeding: portal hypertension drives higher flow; "
        "concurrent coagulopathy (cirrhosis impairs clotting factor synthesis); "
        "massive hemorrhage risk; rebleeding rate 30–40% without treatment\n"
        "| Peptic ulcer: usually lower portal pressure; coagulopathy less common; "
        "rebleeding ~15–20%\n"
        "→ CCRN KEY: Variceal bleed treatment = octreotide 25–50 mcg/hr infusion "
        "(reduces portal pressure) + antibiotics (norfloxacin/ceftriaxone reduces "
        "SBP and mortality) + band ligation. Balloon tamponade (Blakemore) for "
        "refractory bleeding as bridge to TIPS.\n"
        "→ MASTERY NOTE: Octreotide is given for 3–5 days post-banding. "
        "Non-selective β-blockers (propranolol/nadolol) are secondary prophylaxis "
        "after variceal banding — do NOT give acutely during active hemorrhage.",

        'tier-high',
        _GI,
        DID['gi_hepatic'],
        'gi_bleed_severity',
        '{"s":1,"h":1,"g":1,"l":1,"b":1}',
        'chart-l2'
    ),
    (
        "Cirrhotic patient with massive hematemesis, SBP 78, HR 128, Hgb 6.1, "
        "INR 2.8. Risk score = _______. You initiate _______ and _______ "
        "before endoscopy, not _______, because _______.",

        "Score: SBP <90 (+3) + HR ≥100 (+1) + Hgb <10 (+3) + liver disease (+2) = 9 — High Risk\n"
        "| Initiate: octreotide infusion (25 mcg/hr) + ceftriaxone 1g IV/day "
        "(reduce SBP risk, mortality benefit)\n"
        "| Before endoscopy: resuscitate to SBP ≥90, give FFP/platelets for INR >2 "
        "(do NOT give MTP ratio blindly — check TEG/ROTEM in cirrhosis)\n"
        "| Not: immediate endoscopy while hemodynamically unstable\n"
        "| Because: blind intubation in shock + variceal bleeding carries high aspiration "
        "and airway risk; stabilize first (MAP ≥65) then scope\n"
        "→ CCRN KEY: Sequence: resuscitate → octreotide + antibiotics → endoscopy "
        "within 12 h → TIPS if banding fails. Propofol-assisted intubation before "
        "endoscopy in Grade III–IV HE or hematemesis risk.\n"
        "→ MASTERY NOTE: Vasopressin analogs (terlipressin, not available in US; "
        "use octreotide/somatostatin) reduce variceal bleeding mortality by ~35%.",

        'tier-critical',
        _GI,
        DID['gi_hepatic'],
        'gi_bleed_severity',
        '{"s":1,"h":1,"g":1,"l":1,"b":1,"m":1}',
        'chart-l3'
    ),

    # ═══ hepatic_enceph ═══════════════════════════════════════════════════════
    (
        "On the hepatic encephalopathy chart, Grade II HE is characterized by "
        "_______ and an NH₃ approximately _______. The hallmark physical "
        "finding is _______.",

        "Grade II: Lethargy, disorientation, confusion — NH₃ ~100–149 µg/dL\n"
        "| Hallmark finding: asterixis (hepatic flap) — coarse tremor on wrist extension\n"
        "→ CCRN KEY: West Haven grades: 0=subtle, I=attention/sleep, II=lethargy/asterixis, "
        "III=marked confusion/somnolent, IV=coma. "
        "NH₃ correlates loosely — treat the grade, not just the number.\n"
        "→ MASTERY NOTE: Asterixis is not specific to HE — also occurs in uremia, "
        "CO₂ retention, and drug toxicity. "
        "Precipitants of HE (mnemonic TIPS): "
        "Toxins (drugs/EtOH), Infection (SBP), Portal shunting, "
        "Sedatives/GI bleed/electrolytes.",

        'tier-review',
        _GI,
        DID['gi_hepatic'],
        'hepatic_enceph',
        '{"g":2}',
        'chart-l1'
    ),
    (
        "The HE grade chart shows Grade III as 'somnolent but rousable.' "
        "ICU management differs from Grade II by adding _______ because "
        "_______.",

        "Add: airway protection planning (early intubation if Grade IV imminent); "
        "NG tube for lactulose if cannot swallow; fall/aspiration precautions; "
        "hold sedatives and benzodiazepines; consider NH₃-lowering measures\n"
        "| Because: Grade III = high aspiration risk; rapid progression to Grade IV "
        "coma occurs; lactulose via NG ensures continued gut acidification\n"
        "→ CCRN KEY: Lactulose target: 2–3 soft bowel movements/day. "
        "Lactulose works by acidifying colon (NH₃→NH₄⁺ = trapped and excreted). "
        "Rifaximin 550 mg BID added for secondary prophylaxis (reduces gut bacteria "
        "that generate ammonia).\n"
        "→ MASTERY NOTE: Protein restriction is OUTDATED — current guidelines "
        "recommend normal protein intake (1.2–1.5 g/kg/day). "
        "Zinc supplementation supports urea cycle enzyme function.",

        'tier-high',
        _GI,
        DID['gi_hepatic'],
        'hepatic_enceph',
        '{"g":3}',
        'chart-l2'
    ),
    (
        "Cirrhotic patient: NH₃ 210, unresponsive to voice, decerebrate posturing. "
        "Grade _______ HE. Immediate priorities are _______ and _______, "
        "not _______, because _______.",

        "Grade IV HE (coma)\n"
        "| Priority 1: Intubate for airway protection (GCS ≤8, coma = no airway reflex)\n"
        "| Priority 2: Identify and treat precipitant (check UA for UTI/SBP, "
        "cultures, HCT for GI bleed, electrolytes for hyponatremia)\n"
        "| Not: first-line lactulose orally without securing airway\n"
        "| Because: Grade IV = aspiration risk is extreme; aspirating lactulose "
        "in a comatose patient is fatal\n"
        "→ CCRN KEY: Grade IV HE in acute liver failure requires ICP monitoring "
        "(elevated ICP in ALF can cause herniation). "
        "Mannitol for ICP, HOB 30°, avoid hypotonic fluids. "
        "Urgent transplant evaluation if ALF (not cirrhosis) is the cause.\n"
        "→ MASTERY NOTE: Avoid propofol for sedation in HE — accumulates in liver "
        "failure. Use low-dose fentanyl or dexmedetomidine. "
        "Benzodiazepines are absolutely contraindicated.",

        'tier-critical',
        _GI,
        DID['gi_hepatic'],
        'hepatic_enceph',
        '{"g":4}',
        'chart-l3'
    ),

    # ═══ meld_score ═══════════════════════════════════════════════════════════
    (
        "On the MELD score calculator, a patient with Cr 1.8, Bilirubin 4.2, "
        "INR 1.9 has a MELD of approximately _______, predicting "
        "_______ 90-day mortality.",

        "MELD = 3.78×ln(4.2) + 11.2×ln(1.9) + 9.57×ln(1.8) + 6.43\n"
        "= 3.78×1.44 + 11.2×0.64 + 9.57×0.59 + 6.43 ≈ 5.4+7.2+5.6+6.4 = 24\n"
        "| MELD 20–29 predicts ~76% 90-day mortality without transplant\n"
        "→ CCRN KEY: MELD formula uses natural log (ln) of three labs: "
        "bilirubin (liver synthetic function), INR (coagulation/hepatic synthesis), "
        "creatinine (renal function = hepatorenal syndrome risk). "
        "Minimum value: 1.0 for each component.\n"
        "→ MASTERY NOTE: MELD ≥15 = transplant listing threshold. "
        "MELD ≥25 = high waitlist mortality. "
        "MELD-Na adds sodium: hyponatremia worsens prognosis beyond what MELD alone captures.",

        'tier-review',
        _GI,
        DID['gi_hepatic'],
        'meld_score',
        '{"cr":1.8,"bi":4.2,"inr":1.9}',
        'chart-l1'
    ),
    (
        "The MELD calculator shows creatinine capped at 4.0 mg/dL even when "
        "higher values are present. This design reflects that _______.",

        "Creatinine is capped at 4.0 mg/dL in the MELD formula to prevent "
        "any single component from dominating the score unduly\n"
        "| Dialysis patients automatically receive Cr = 4.0 mg/dL "
        "(regardless of actual lab value) because dialysis removes creatinine\n"
        "→ CCRN KEY: Dialysis = automatic Cr 4.0 in MELD. "
        "This reflects that ESRD requiring dialysis represents maximal renal "
        "component score. Hepatorenal syndrome (HRS) Type 1 "
        "= rapidly rising Cr in cirrhosis = major MELD driver.\n"
        "→ MASTERY NOTE: HRS Type 1 (AKI form) = Cr doubles to >2.5 mg/dL within 2 weeks, "
        "triggered by infection, bleeding, or large-volume paracentesis without albumin. "
        "Terlipressin + albumin (or norepinephrine + albumin in US) is first-line treatment.",

        'tier-high',
        _GI,
        DID['gi_hepatic'],
        'meld_score',
        '{"cr":3.8,"bi":6.0,"inr":2.2}',
        'chart-l2'
    ),
    (
        "Cirrhotic patient's MELD rises from 18 to 32 over 72 hours: "
        "Cr 0.9→3.4, Bili 3.2→7.1, INR 1.6→2.8. This rise is caused by "
        "_______, and the critical intervention within the next 24 hours is "
        "_______.",

        "MELD rise from 18 to ~32 = acute decompensation of cirrhosis\n"
        "| Most likely cause: Spontaneous bacterial peritonitis (SBP) "
        "triggering acute-on-chronic liver failure (ACLF) — diagnostic paracentesis "
        "to confirm (PMN >250/mm³ in ascitic fluid)\n"
        "| Critical intervention: diagnostic and therapeutic paracentesis + "
        "IV cefotaxime/ceftriaxone + IV albumin 1.5 g/kg on day 1, 1 g/kg on day 3 "
        "(proven to prevent HRS and reduce mortality by 33%)\n"
        "→ CCRN KEY: Albumin infusion with SBP treatment is standard of care. "
        "SBP precipitates HRS and ACLF — early albumin prevents renal failure. "
        "ACLF = organ failures on a background of chronic liver disease; MELD >18 "
        "in ACLF = ICU-level care.\n"
        "→ MASTERY NOTE: MELD trajectory matters more than a single value. "
        "A MELD jumping from 18→32 in 3 days signals ACLF, "
        "which carries higher mortality than stable MELD 32.",

        'tier-critical',
        _GI,
        DID['gi_hepatic'],
        'meld_score',
        '{"cr":3.4,"bi":7.1,"inr":2.8}',
        'chart-l3'
    ),

    # ═══ pancreatitis_bisap ═══════════════════════════════════════════════════
    (
        "On the BISAP pancreatitis severity chart, the 5 criteria are "
        "_______. A score of _______ or higher identifies high-risk "
        "patients with >15% mortality.",

        "B — BUN >25 mg/dL\n"
        "| I — Impaired mental status (disorientation)\n"
        "| S — SIRS criteria (≥2 of: temp <36/>38°C, HR >90, RR >20, WBC <4k/>12k)\n"
        "| A — Age >60 years\n"
        "| P — Pleural effusion on imaging\n"
        "| Score ≥3 = high risk (>15% mortality); score 0–2 = low risk (<1%)\n"
        "→ CCRN KEY: BISAP predicts severity at admission — calculated from "
        "first 24-hour data. More practical than Ranson criteria (Ranson requires "
        "48-hour data). Score 0–2: low risk; 3–5: high risk.\n"
        "→ MASTERY NOTE: Ranson criteria (historical): 11 criteria over 48 hours, "
        "score ≥3 = severe. BISAP performs comparably with fewer variables. "
        "CT severity index (CTSI) adds imaging — necrotizing pancreatitis requires CT.",

        'tier-review',
        _GI,
        DID['gi_hepatic'],
        'pancreatitis_bisap',
        '{}',
        'chart-l1'
    ),
    (
        "A 65-year-old presents with acute pancreatitis: BUN 32, confused, "
        "temp 38.4°C/HR 104/RR 22 (SIRS positive), pleural effusion on CXR. "
        "BISAP = _______ and initial management priorities are _______ "
        "and _______.",

        "BISAP = B(1) + I(1) + S(1) + A(1, age >60) + P(1) = 5 — High Risk\n"
        "| Priority 1: Aggressive IV fluid resuscitation — LR preferred over NS "
        "(reduces systemic inflammation via pH effect); goal 250–500 mL/hr initially\n"
        "| Priority 2: ICU admission, NPO, pain control (hydromorphone IV), "
        "monitor urine output hourly\n"
        "→ CCRN KEY: Acute pancreatitis fluid resuscitation: Lactated Ringer's "
        "250–500 mL/hr × 24–48h (reduces pancreatic necrosis vs NS). "
        "Target UO >0.5 mL/kg/hr, BUN trending down. "
        "Early feeding (within 24–72h) via NG reduces complications.\n"
        "→ MASTERY NOTE: Antibiotics NOT indicated for uncomplicated pancreatitis "
        "— give only for confirmed infected necrosis (fever persisting >7 days, "
        "CT-guided FNA showing bacteria). Routine prophylactic antibiotics = harmful.",

        'tier-high',
        _GI,
        DID['gi_hepatic'],
        'pancreatitis_bisap',
        '{"B":1,"I":1,"S":1,"A":1,"P":1}',
        'chart-l2'
    ),
    (
        "Pancreatitis patient BISAP 4, day 5 of admission: persistent fever 38.9°C, "
        "WBC 22k, CT shows 60% pancreatic necrosis with gas bubbles. "
        "The chart now shows _______ severity. Next intervention is _______, "
        "not _______, because _______.",

        "BISAP 4 + CT findings = Severe necrotizing pancreatitis with suspected "
        "infected necrosis\n"
        "| Intervention: CT-guided fine needle aspiration (FNA) for Gram stain and culture "
        "to confirm infection; if confirmed → IV antibiotics (imipenem or meropenem)\n"
        "| Not: immediate surgical necrosectomy or empiric antibiotics without confirmation\n"
        "| Because: Step-up approach (drain first, then necrosectomy only if fails) "
        "has lower mortality than primary surgery; empiric antibiotics promote resistance\n"
        "→ CCRN KEY: Infected pancreatic necrosis = only indication for antibiotics "
        "and intervention in pancreatitis. Percutaneous catheter drainage first; "
        "endoscopic or surgical necrosectomy if drainage insufficient.\n"
        "→ MASTERY NOTE: ERCP within 24–48h only if gallstone pancreatitis with "
        "concurrent cholangitis (not routine for all gallstone pancreatitis). "
        "Cholecystectomy during same hospitalization prevents recurrence.",

        'tier-critical',
        _GI,
        DID['gi_hepatic'],
        'pancreatitis_bisap',
        '{"B":1,"I":0,"S":1,"A":1,"P":1}',
        'chart-l3'
    ),

    # ═══ abdominal_compartment ════════════════════════════════════════════════
    (
        "On the intra-abdominal pressure chart, abdominal compartment syndrome "
        "(ACS) is defined as IAP > _______ mmHg sustained, combined with "
        "_______.",

        "IAP > 20 mmHg sustained + new organ dysfunction (renal, respiratory, "
        "cardiovascular, or CNS failure)\n"
        "| Intra-abdominal hypertension (IAH) grades: I=12–15, II=16–20, "
        "III=21–25, IV=>25 mmHg\n"
        "→ CCRN KEY: ACS definition requires BOTH: IAP >20 mmHg AND new organ "
        "dysfunction. IAH alone (without organ failure) = aggressive medical management. "
        "Measured via bladder pressure via Foley catheter (gold standard).\n"
        "→ MASTERY NOTE: IAP measurement technique: instill 20–25 mL NS into bladder "
        "via Foley, wait 30–60 sec, measure at end-expiration with patient supine. "
        "Measure every 4–6 hours in at-risk patients (massive resuscitation, "
        "abdominal trauma, ileus, pancreatitis).",

        'tier-review',
        _GI,
        DID['gi_hepatic'],
        'abdominal_compartment',
        '{"iap":22}',
        'chart-l1'
    ),
    (
        "The IAP chart shows Grade III IAH at 23 mmHg. Organ dysfunction "
        "develops: Cr rises, peak airway pressure increases. This is ACS. "
        "Organ failure occurs because _______.",

        "Elevated IAP compresses abdominal vena cava → reduced venous return "
        "→ decreased cardiac output → renal hypoperfusion (↑Cr)\n"
        "| Diaphragm pushed cephalad → decreased lung compliance and FRC → "
        "higher airway pressures, atelectasis, hypoxemia\n"
        "| Direct compression of renal veins → renal venous hypertension "
        "→ obstructive AKI (reduced GFR despite adequate MAP)\n"
        "→ CCRN KEY: ACS organ injury mechanism: direct compression + reduced CO. "
        "Target MAP >60 mmHg AND reduce IAP. "
        "Plateau pressure rising without lung change = clue to worsening IAP.\n"
        "→ MASTERY NOTE: Abdominal perfusion pressure (APP) = MAP − IAP. "
        "Target APP ≥60 mmHg for adequate perfusion. "
        "IAP 23 mmHg + MAP 75 = APP 52 = inadequate perfusion.",

        'tier-high',
        _GI,
        DID['gi_hepatic'],
        'abdominal_compartment',
        '{"iap":23}',
        'chart-l2'
    ),
    (
        "Post-massive resuscitation trauma patient: IAP 28 mmHg, Cr doubling, "
        "plateau pressure 38 cmH₂O, MAP 68. Chart shows IAH Grade IV + ACS. "
        "Initial management is _______, not _______, because _______.",

        "Initial management: medical decompression first — "
        "NG/rectal decompression (decompress bowel gas), remove abdominal binders, "
        "optimize sedation/analgesia (muscle relaxation reduces IAP 10–15%), "
        "neuromuscular blockade (cisatracurium) if other measures fail\n"
        "| Not: immediate decompressive laparotomy as first step\n"
        "| Because: surgery has high morbidity; medical measures can reduce IAP by "
        "5–10 mmHg and may avoid surgery; IAP >25 with failed medical management "
        "= surgical threshold\n"
        "→ CCRN KEY: Medical management steps: decompress GI tract → optimize "
        "fluid balance (avoid further resuscitation if possible) → NMB → "
        "surgical decompression if refractory.\n"
        "→ MASTERY NOTE: Decompressive laparotomy: abdomen left open with "
        "temporary closure (Bogota bag or vacuum-assisted). "
        "Immediate IAP normalization; fascial closure after edema resolves (48–72h+). "
        "Risk: evisceration, infection, fistula.",

        'tier-critical',
        _GI,
        DID['gi_hepatic'],
        'abdominal_compartment',
        '{"iap":28}',
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
