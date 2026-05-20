#!/usr/bin/env python3
"""chunk42_charts.py — Ph7 Sedation & Analgesia (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_41.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_42.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c42')
CHUNK_NUM   = 42
MID_BASE    = 1_800_005_055
CHART_ORDER = ['sedation_scale', 'analgesic_ladder', 'propofol_pris',
               'dexmedetomidine', 'cam_icu']

_SA = 'Ph7 · \U0001f7e1 T3 · Pharmacology — Sedation & Analgesia'

RF = {}

# ── Chart 1: RASS Sedation Scale ──────────────────────────────────────────────
RF['sedation_scale'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var rval=(P.rval!==undefined)?P.rval:-2;
    var levels=[
        {r:+4,lbl:'Combative',      desc:'Overtly combative; violent; immediate danger to staff',    tgt:false,c:'#cc1111'},
        {r:+3,lbl:'Very Agitated',  desc:'Pulls or removes tubes; aggressive',                       tgt:false,c:'#cc2222'},
        {r:+2,lbl:'Agitated',       desc:'Frequent non-purposeful movement; fights ventilator',      tgt:false,c:'#cc4422'},
        {r:+1,lbl:'Restless',       desc:'Anxious, apprehensive; not aggressive',                    tgt:false,c:'#cc8800'},
        {r: 0,lbl:'Alert & Calm',   desc:'Spontaneously pays attention to caregiver',                tgt:true, c:'#3a9a5c'},
        {r:-1,lbl:'Drowsy',         desc:'Sustained eye opening >10 sec to voice',                   tgt:true, c:'#4488cc'},
        {r:-2,lbl:'Light Sedation', desc:'Brief eye awakening <10 sec to voice; no eye contact',     tgt:true, c:'#3366aa'},
        {r:-3,lbl:'Mod Sedation',   desc:'Movement or eye opening to voice; no eye contact',         tgt:false,c:'#224488'},
        {r:-4,lbl:'Deep Sedation',  desc:'No response to voice; movement to physical stimulus only', tgt:false,c:'#112266'},
        {r:-5,lbl:'Unarousable',    desc:'No response to voice or physical stimulation',             tgt:false,c:'#0a0a33'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var scaleX=28, scaleW=W-56, barY=10, barH=30;
    var zW=Math.floor(scaleW/levels.length);
    levels.forEach(function(lv,i){
        var x=scaleX+i*zW;
        var sel=(lv.r===rval);
        ctx.fillStyle=sel?lv.c:lv.c+'88';ctx.fillRect(x,barY,zW,barH);
        if(sel){ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.strokeRect(x,barY,zW,barH);}
        ctx.fillStyle='#fff';ctx.font='bold 9px sans-serif';ctx.textAlign='center';
        ctx.fillText((lv.r>0?'+':'')+lv.r,x+zW/2,barY+13);
        if(lv.tgt){ctx.fillStyle='#ffd700';ctx.font='bold 8px sans-serif';ctx.fillText('★',x+zW/2,barY+26);}
    });
    ctx.fillStyle='#555';ctx.font='8px sans-serif';ctx.textAlign='left';
    ctx.fillText('★ = PADIS target',scaleX,barY+barH+12);
    ctx.fillStyle='#cc4422';ctx.fillText('← Agitated',scaleX+scaleW*0.05,barY+barH+12);
    ctx.fillStyle='#3366aa';ctx.fillText('Sedated →',scaleX+scaleW*0.72,barY+barH+12);
    var lv=levels.find(function(l){return l.r===rval;})||levels[6];
    var panelY=barY+barH+22, panelH=H-panelY-4;
    ctx.fillStyle='#0a0a1a';ctx.fillRect(4,panelY,W-8,panelH);
    ctx.strokeStyle=lv.c;ctx.lineWidth=2;ctx.strokeRect(4,panelY,W-8,panelH);
    ctx.fillStyle=lv.c;ctx.font='bold 16px sans-serif';ctx.textAlign='left';
    ctx.fillText('RASS '+(lv.r>0?'+':'')+lv.r+' — '+lv.lbl,12,panelY+22);
    ctx.fillStyle='#ccc';ctx.font='10.5px sans-serif';
    ctx.fillText(lv.desc,12,panelY+40);
    var tgtMsg=lv.tgt?'✓ TARGET — PADIS 2018 goal (RASS −2 to 0)':'✗ Not a routine sedation target';
    ctx.fillStyle=lv.tgt?'#ffd700':'#cc6633';ctx.font='bold 10px sans-serif';
    ctx.fillText(tgtMsg,12,panelY+58);
    var actions={
        4:'Immediate safety: call for help, restrain if necessary, assess/treat pain (CPOT), reverse precipitants',
        3:'Assess pain first (CPOT/NRS); treat agitation cause; titrate analgesic before escalating sedation',
        2:'Assess and treat pain; consider PRN sedative; investigate reversible causes (full bladder, tube position)',
        1:'Continue to monitor; assess for pain; consider whether sedation is needed',
        0:'Optimal — maintain with comfort-focused care; reassess sedation need',
       '-1':'Perform SAT if on continuous infusion; assess readiness for SBT',
       '-2':'PADIS target for most vented pts; reassess q4h; daily SAT when stable',
       '-3':'Assess whether deeper sedation is clinically indicated; consider reducing dose',
       '-4':'Too deep — perform SAT; assess for PRIS if on propofol; wean sedation',
       '-5':'UTA (Unable to Assess) for CAM-ICU; evaluate reversible causes of unresponsiveness'
    };
    var akey=''+lv.r;
    var actionText=actions[akey]||'Reassess sedation need';
    ctx.fillStyle='#aaa';ctx.font='9.5px sans-serif';
    var words=actionText.split(' '),line='',ly=panelY+76,maxW=W-24;
    words.forEach(function(w){var t=line?line+' '+w:w;if(ctx.measureText(t).width>maxW){ctx.fillText(line,12,ly);line=w;ly+=12;}else line=t;});
    if(line)ctx.fillText(line,12,ly);
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin-top:6px;';
        var sl=_mkS('RASS:',-5,4,1,rval,function(v){return (v>0?'+':'')+v;},function(v){
            var p2={rval:v};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });
        row.appendChild(sl);ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: ICU Analgesic Comparison ────────────────────────────────────────
RF['analgesic_ladder'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var analgs=[
        {name:'Fentanyl IV',     on:'1–2 min', dur:'30–60 min',  renal:'SAFE\nno active metabolites', adv:'1st-line ICU opioid\ntitratable infusion',  c:'#3a9a5c'},
        {name:'Morphine IV',     on:'5–10 min',dur:'3–4 h',      renal:'AVOID infusions\nM6G accumulates → ↑ sedation',adv:'Acute bolus pain/dyspnea\nnot recommended infusion', c:'#cc3333'},
        {name:'Hydromorphone IV',on:'5–10 min',dur:'3–4 h',      renal:'Caution\nmild accumulation (ESRD)',adv:'5–7× more potent\nthan morphine',       c:'#e07020'},
        {name:'Ketamine IV',     on:'~1 min',  dur:'15–20 min',  renal:'SAFE',                         adv:'NMDA antagonist\nPreserves resp. drive',  c:'#4488cc'},
        {name:'IV Acetaminophen',on:'15–30 min',dur:'6 h',       renal:'SAFE\nreduce dose hepatic failure', adv:'No respiratory depression\nopioid-sparing 20–30%', c:'#38b2a4'},
        {name:'Ketorolac IV',    on:'30 min',  dur:'4–6 h',      renal:'AVOID GFR<30\nAKI risk; max 5 days',adv:'NSAID; no resp. depression\nmax 5 days duration',c:'#9060c0'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=20, rh=Math.floor((H-hdrH)/analgs.length);
    var xs=[4,130,200,265,430,618];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Drug','Onset','Duration','Renal Safety','Key Advantage'];
    ctx.font='bold 9px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-5);});
    analgs.forEach(function(ag,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=ag.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=ag.c;ctx.font='bold 9.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(ag.name,xs[0]+4,ry+rh/2+3);
        ctx.fillStyle='#bbb';ctx.font='10px sans-serif';ctx.textAlign='center';
        ctx.fillText(ag.on,(xs[1]+xs[2])/2,ry+rh/2+3);
        ctx.fillText(ag.dur,(xs[2]+xs[3])/2,ry+rh/2+3);
        var renalL=ag.renal.split('\n'),renalC=renalL[0].startsWith('AVOID')?'#ee4444':(renalL[0].startsWith('Caution')?'#e07020':'#3a9a5c');
        ctx.fillStyle=renalC;ctx.font='bold 9px sans-serif';ctx.textAlign='left';
        ctx.fillText(renalL[0],xs[3]+4,ry+rh/2-2);
        if(renalL[1]){ctx.fillStyle='#778';ctx.font='8.5px sans-serif';ctx.fillText(renalL[1],xs[3]+4,ry+rh/2+9);}
        ctx.fillStyle='#9ab8aa';ctx.font='9px sans-serif';
        ag.adv.split('\n').forEach(function(al,ai){ctx.fillText(al,xs[4]+4,ry+rh/2-2+ai*11);});
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
        var lbs=['Fentanyl','Morphine','Hydrmrph.','Ketamine','IV APAP','Ketorolac'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,analgs[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 3: Propofol & PRIS ──────────────────────────────────────────────────
RF['propofol_pris'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Mechanism & Use','Dosing & Monitoring','PRIS Recognition'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a2a3a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#60d0c0':'#555';ctx.font=(sel===i?'bold ':'')+'9.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0a1a';ctx.fillRect(4,panelY,W-8,panelH);
    var content=[
        [['MECHANISM','GABA-A receptor: positive allosteric modulator (same target as benzodiazepines; faster onset)',
          'Formulation: 10% lipid emulsion (1.1 kcal/mL, 0.1 g fat/mL) — accounts for as TPN calories',
          'Onset: 30–45 sec (bolus) | Duration: 3–8 min (bolus); context-sensitive half-life increases with duration',
          'Highly lipophilic → rapid CNS distribution; metabolized hepatically (glucuronidation + CYP2C9)',
          'Advantages: titratable, short offset, lower delirium vs. benzos, antiemetic at low doses']],
        [['DOSING',
          'ICU sedation (RASS −2 to 0): 5–50 mcg/kg/min (0.3–3 mg/kg/h)',
          'Procedural sedation: 1–2 mg/kg IV induction bolus',
          'Refractory status epilepticus: 1–5 mg/kg/h infusion',
          '','MONITORING',
          'Max recommended: ≤4–5 mg/kg/h (67–83 mcg/kg/min) to reduce PRIS risk',
          'Triglycerides: check at baseline, then every 72h; hold if TG >400 mg/dL',
          'Lipid accounting: 1 mg/kg/h propofol = 0.1 g fat/kg/day (max 1.5 g fat/kg/day)',
          'Change infusion line every 12h (lipid emulsion supports bacterial growth)']],
        [['PRIS DIAGNOSTIC CRITERIA (all 3 required for diagnosis)',
          'Dose: >4–5 mg/kg/h (>67 mcg/kg/min) for >48h',
          'Metabolic acidosis: new anion-gap metabolic acidosis (↑ AG, ↓ HCO₃, ↑ lactate)',
          'PLUS ≥1 organ feature: Rhabdomyolysis (CK >5000), Cardiac arrhythmia/failure,',
          'Renal failure, Hyperkalemia (K⁺ >6.0), Hypertriglyceridemia (TG >500)','',
          'MANAGEMENT: STOP propofol → switch sedation (midazolam/dexmedetomidine) →',
          'Vasopressors for hemodynamic support → CRRT for refractory acidosis/hyperkalemia',
          'Treat arrhythmias → supportive care. PRIS mortality 18–83% if unrecognized.']]
    ];
    var col=sel<content.length?content[sel][0]:[];
    var ly=panelY+14;
    col.forEach(function(line){
        if(line===''){ly+=4;return;}
        var isSect=(line===line.toUpperCase()&&line.length>2&&!line.includes('.'));
        ctx.fillStyle=isSect?'#60d0c0':'#bbb';
        ctx.font=isSect?'bold 10px sans-serif':'9.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(line,10,ly);ly+=isSect?15:13;
    });
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;';
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,_TE,sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        ctrl.appendChild(row);
    }
}
"""

# ── Chart 4: Dexmedetomidine vs Midazolam ────────────────────────────────────
RF['dexmedetomidine'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var rows=[
        {prop:'Mechanism',  dex:'α2 agonist (locus ceruleus)\n↓ NE release → sedation', benz:'GABA-A potentiation\n(benzodiazepine receptor)',  note:'Dex mimics natural sleep\npathways (NE pathway)',  c:'#4488cc'},
        {prop:'Resp. Drive',dex:'PRESERVED ✓\nNo apnea at therapeutic doses', benz:'DEPRESSED ✗\nApnea risk even at low doses',note:'Dex: safe for NIV\nBenzo: vent-dependent risk', c:'#3a9a5c'},
        {prop:'Delirium',   dex:'REDUCED risk ↓\n(MENDS trial)',              benz:'INCREASED risk ↑↑\n(independent risk factor)', note:'Benzo: independent delirium\nrisk factor (avoid)',     c:'#e07020'},
        {prop:'Sedation Quality',dex:'Cooperative/arousable\nPatient can follow commands',benz:'Amnestic/dissociative\nDifficult to arouse', note:'Dex: ideal for SAT\nBenzo: longer wake-up',    c:'#38b2a4'},
        {prop:'Weaning',    dex:'Low withdrawal risk\n(clonidine taper if prolonged)', benz:'HIGH withdrawal risk\nSeizures / rebound anxiety', note:'Benzo: taper required >5d\nDex: usually abrupt OK', c:'#cc3366'},
        {prop:'Evidence',   dex:'MENDS (2007): dex ↓\ncoma+delirium vs. lorazepam',benz:'PADIS 2018: AVOID benzos\nfor routine ICU sedation',  note:'Propofol or dex preferred\nover benzodiazepines',   c:'#9060c0'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=20, rh=Math.floor((H-hdrH)/rows.length);
    var xs=[4,120,295,460,618];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Property','Dexmedetomidine','Midazolam (Benzo)','Clinical Note'];
    ctx.font='bold 9px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-5);});
    rows.forEach(function(row,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=row.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=row.c;ctx.font='bold 9px sans-serif';ctx.textAlign='center';
        ctx.fillText(row.prop,(xs[0]+xs[1])/2,ry+rh/2+3);
        ctx.fillStyle='#7ecca0';ctx.font='9.5px sans-serif';ctx.textAlign='left';
        row.dex.split('\n').forEach(function(dl,di){ctx.fillText(dl,xs[1]+4,ry+rh/2-2+di*11);});
        ctx.fillStyle='#cc8888';ctx.font='9.5px sans-serif';
        row.benz.split('\n').forEach(function(bl,bi){ctx.fillText(bl,xs[2]+4,ry+rh/2-2+bi*11);});
        ctx.fillStyle='#8899aa';ctx.font='8.5px sans-serif';
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
        var lbs=['Mechanism','Resp Drive','Delirium','Sedation','Weaning','Evidence'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,rows[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 5: CAM-ICU Delirium Assessment ─────────────────────────────────────
RF['cam_icu'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:-1;
    var features=[
        {n:'Feature 1',  lbl:'Acute Onset\nor Fluctuating',  c:'#e07020',
         q:'Assessment: Review nursing notes + ask family/team',
         a:['• Acute change from baseline mental status?','• OR fluctuation in mental status in past 24h?','• Compare to baseline (family, prior notes, chart)','• Positive: YES to either question → Feature 1 PRESENT'],
         tip:'Any change from the patient\'s normal cognition = positive Feature 1'},
        {n:'Feature 2',  lbl:'Inattention',                  c:'#38b2a4',
         q:'Assessment: ASE (Attention Screening Examination)',
         a:['• Say: "Squeeze my hand each time I say the letter A"','• Read: S-A-V-E-A-H-A-A-R-T (patient should squeeze on A = 4 times)','• Score errors: missed A squeezes + false squeezes for non-A','• Positive: >2 errors → Feature 2 PRESENT'],
         tip:'Alternative: picture ASE for hearing-impaired or non-verbal patients'},
        {n:'Feature 3',  lbl:'Altered Level\nof Consciousness',c:'#c07828',
         q:'Assessment: Check RASS score at time of assessment',
         a:['• Normal: RASS = 0 (Alert and Calm)','• Positive: RASS ≠ 0 (any value except zero)','• Includes: RASS +1/+2 (agitated/restless)','• AND: RASS −1/−2 (drowsy/lightly sedated)'],
         tip:'RASS −4 or −5 = Unable to Assess (UTA) — do not score as delirium'},
        {n:'Feature 4',  lbl:'Disorganized\nThinking',        c:'#9060c0',
         q:'Assessment: Yes/No questions + command test',
         a:['• 4 Yes/No questions (e.g., "Does a stone float on water?")','• Command: "Hold up this many fingers" (show 2) → other hand same','• Score errors: wrong yes/no + wrong finger count','• Positive: >1 error → Feature 4 PRESENT'],
         tip:'CAM-ICU POSITIVE: Feature 1 AND 2 AND (Feature 3 OR 4)'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var cols=2, nrows=2, gap=6;
    var bw=Math.floor((W-gap*(cols+1))/cols), bh=56, gridY=4;
    features.forEach(function(ft,i){
        var col=i%cols, row=Math.floor(i/cols);
        var bx=gap+col*(bw+gap), by=gridY+row*(bh+gap);
        var active=(sel===i);
        ctx.fillStyle=active?ft.c+'33':'#0d0d18';ctx.fillRect(bx,by,bw,bh);
        ctx.strokeStyle=active?ft.c:'#2a2a2a';ctx.lineWidth=active?2:1;ctx.strokeRect(bx,by,bw,bh);
        ctx.fillStyle=ft.c;ctx.font='bold 10px sans-serif';ctx.textAlign='left';
        ctx.fillText(ft.n,bx+6,by+17);
        ctx.fillStyle='#ccc';ctx.font='9px sans-serif';
        ft.lbl.split('\n').forEach(function(ll,li){ctx.fillText(ll,bx+6,by+30+li*12);});
    });
    // Algorithm reminder at top right edge
    ctx.fillStyle='#444';ctx.font='8px sans-serif';ctx.textAlign='right';
    ctx.fillText('RASS ≥ −3 required to assess',W-4,gridY+12);
    ctx.fillText('CAM+ = F1 AND F2 AND (F3 OR F4)',W-4,gridY+23);
    var panelY=gridY+nrows*(bh+gap)+4, panelH=H-panelY-4;
    ctx.fillStyle='#0a0a1a';ctx.fillRect(4,panelY,W-8,panelH);
    ctx.strokeStyle='#222';ctx.lineWidth=1;ctx.strokeRect(4,panelY,W-8,panelH);
    if(sel<0){
        ctx.fillStyle='#444';ctx.font='10px sans-serif';ctx.textAlign='center';
        ctx.fillText('Select a feature above to view assessment instructions',W/2,panelY+panelH/2-6);
        ctx.fillStyle='#334';ctx.font='9px sans-serif';
        ctx.fillText('CAM-ICU takes <2 min | Assess twice daily | RASS gate: ≥ −3 to proceed',W/2,panelY+panelH/2+10);
    } else {
        var ft=features[sel];
        ctx.fillStyle=ft.c;ctx.font='bold 11px sans-serif';ctx.textAlign='left';
        ctx.fillText(ft.n+': '+ft.lbl.replace('\n',' '),10,panelY+16);
        ctx.fillStyle='#88b0cc';ctx.font='bold 9px sans-serif';
        ctx.fillText(ft.q,10,panelY+30);
        ctx.fillStyle='#bbb';ctx.font='9.5px sans-serif';
        ft.a.forEach(function(al,ai){ctx.fillText(al,10,panelY+44+ai*13);});
        ctx.fillStyle='#556';ctx.font='italic 8.5px sans-serif';
        ctx.fillText(ft.tip,10,panelY+44+ft.a.length*13+4);
    }
    if(ctrl){
        ctrl.innerHTML='';
        var row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;';
        features.forEach(function(ft,i){(function(idx){var b=_mkB(ft.n,ft.c,sel===idx,function(on){
            var ns=on?idx:-1;cv.setAttribute('data-params',JSON.stringify({sel:ns}));_render(cv,ctrl,{sel:ns});
        });row.appendChild(b);})(i);});
        var rst=_mkB('Overview',_AX,sel===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Cards ─────────────────────────────────────────────────────────────────────
CARDS = [
    # ═══ sedation_scale ══════════════════════════════════════════════════════
    (
        "On the RASS sedation scale chart, the target sedation for most "
        "mechanically ventilated ICU patients per PADIS 2018 guidelines is "
        "RASS _______ to _______. A patient at RASS −4 (no eye opening to voice) "
        "requires _______.",

        "RASS −2 to 0 (light sedation to alert and calm)\n"
        "| RASS −4 (Deep Sedation): movement only to physical stimulus; "
        "no response to voice → perform SAT (Spontaneous Awakening Trial) and "
        "reduce sedation dose toward target range\n"
        "→ CCRN KEY: PADIS = Pain, Agitation/Sedation, Delirium, Immobility, Sleep "
        "(SCCM 2018 guidelines). Deep sedation (RASS ≤ −3) is associated with "
        "longer mechanical ventilation, increased delirium, ICU-acquired weakness, "
        "and worse long-term outcomes. Reserved for: severe ARDS (P-SILI risk), "
        "refractory elevated ICP, status epilepticus, and therapeutic paralysis.\n"
        "→ MASTERY NOTE: RASS −2 to 0 is not just a preference — it is a quality "
        "metric. Every shift: assess pain (CPOT/NRS), assess sedation (RASS), "
        "target RASS −2 to 0. Document the score, not the drip rate.",

        'tier-review',
        _SA,
        DID['sedation_analgesia'],
        'sedation_scale',
        '{"rval":-2}',
        'chart-l1'
    ),
    (
        "The RASS chart shows a vented patient at RASS +2 (fighting ventilator, "
        "CPOT = 6). Per the A1C (Analgesia-first) protocol, "
        "the FIRST intervention before adding sedation is _______.",

        "Treat PAIN first — increase IV analgesic dose (fentanyl 25–50 mcg IV "
        "bolus or increase infusion rate)\n"
        "| Rationale: CPOT >2 = significant pain in non-verbal patients. Pain "
        "is the most common and undertreated driver of agitation in the ICU. "
        "Adding sedation without addressing pain simply suppresses the response "
        "without treating the cause.\n"
        "→ CCRN KEY: A1C protocol order: Assess pain (CPOT/BPS) → treat pain → "
        "reassess CPOT → assess sedation (RASS) → treat agitation if still present "
        "after pain control. CPOT components: facial expression, body movements, "
        "muscle tension, compliance with ventilator. Each 0–2 points; total 0–8.\n"
        "→ MASTERY NOTE: Also assess and treat reversible agitation causes before "
        "escalating sedation: full bladder (straight cath), ETT malposition "
        "(verify on CXR), kinked NG tube, constipation, hypoxia, hypercapnia, "
        "metabolic derangements. These cause agitation — sedation covers them up.",

        'tier-high',
        _SA,
        DID['sedation_analgesia'],
        'sedation_scale',
        '{"rval":2}',
        'chart-l2'
    ),
    (
        "On the RASS chart, daily sedation interruption (SAT) combined with "
        "spontaneous breathing trials (SBT) is the _______ protocol. "
        "Per the 2008 Lancet trial, this reduces 1-year mortality by approximately _______.",

        "ABC Bundle — Awakening and Breathing Coordination\n"
        "| 2008 Lancet trial (Girard et al.): ABC protocol reduced 1-year mortality "
        "by 32% (HR 0.68) and median time on mechanical ventilation by ~3 days, "
        "reduced ICU and hospital length of stay\n"
        "| SAT safety screen (hold sedation if): SpO₂ <88%, RR >35, FiO₂ >70%, "
        "PEEP >12, active seizures, ongoing NMB, alcohol withdrawal, or agitation\n"
        "→ CCRN KEY: SAT-SBT sequence: Hold sedation → patient opens eyes/follows "
        "commands → perform SBT (PS 5/5 or T-piece for 30–120 min) → "
        "evaluate extubation readiness. Fail SAT → restart at 50% prior dose.\n"
        "→ MASTERY NOTE: ABCDEF bundle extends ABC: D = Delirium monitoring/management "
        "(CAM-ICU), E = Early mobility and exercise, F = Family engagement and "
        "empowerment. Each component independently improves outcomes; synergistic "
        "when combined. The bundle, not individual components, is the goal.",

        'tier-critical',
        _SA,
        DID['sedation_analgesia'],
        'sedation_scale',
        '{"rval":-1}',
        'chart-l3'
    ),

    # ═══ analgesic_ladder ════════════════════════════════════════════════════
    (
        "On the analgesic comparison chart, fentanyl is preferred over morphine "
        "for continuous opioid infusions in AKI because morphine's active metabolite "
        "_______ accumulates in renal failure and causes _______.",

        "Morphine-6-glucuronide (M6G) — active opioid metabolite renally excreted\n"
        "| Accumulation causes: prolonged sedation, respiratory depression, "
        "delayed weaning from mechanical ventilation, and difficult-to-reverse "
        "opioid toxicity (naloxone may be required repeatedly)\n"
        "→ CCRN KEY: ICU opioid safety by renal function: "
        "Fentanyl = SAFE (no active metabolites, hepatically metabolized); "
        "Hydromorphone = use with caution (H3G mild accumulation — OK for "
        "bolus dosing, caution with infusions in ESRD); "
        "Morphine = avoid infusions in AKI/CKD (PRN bolus acceptable when GFR >60).\n"
        "→ MASTERY NOTE: Equianalgesic ICU doses: morphine 10 mg IV = "
        "hydromorphone 1.5 mg IV = fentanyl 100 mcg IV. When converting between "
        "opioids (rotation), reduce new opioid by 25–50% for incomplete "
        "cross-tolerance — then titrate up.",

        'tier-review',
        _SA,
        DID['sedation_analgesia'],
        'analgesic_ladder',
        '{"hi":0}',
        'chart-l1'
    ),
    (
        "The analgesic chart shows IV ketamine as an opioid-sparing adjunct. "
        "Its two key advantages over opioids are _______ and _______. "
        "The receptor mechanism is _______.",

        "Preserved spontaneous respiratory drive — no apnea risk at "
        "sub-anesthetic doses (NMDA receptor antagonist, not opioid receptor)\n"
        "| Bronchodilation — relaxes bronchial smooth muscle via sympathomimetic "
        "effect (preferred adjunct in asthma/bronchospasm patients)\n"
        "| Mechanism: NMDA (N-methyl-D-aspartate) receptor antagonist — "
        "blocks glutamate-mediated pain transmission; also blunts "
        "opioid-induced hyperalgesia (OIH) with sub-anesthetic doses\n"
        "→ CCRN KEY: ICU ketamine dosing: 0.1–0.5 mg/kg/h as adjunct "
        "analgesic (sub-anesthetic). Reduces opioid requirements by 30–50%. "
        "At higher procedural doses (1–2 mg/kg IV), causes dissociative sedation "
        "with preserved protective airway reflexes — useful for non-intubated procedures.\n"
        "→ MASTERY NOTE: Ketamine contraindications/cautions: severe hypertension "
        "(sympathomimetic: ↑BP, ↑HR), elevated ICP (historically avoided; "
        "now acceptable with controlled ventilation), psychosis history "
        "(hallucinations at higher doses). Pre-medicate with midazolam 0.02 mg/kg "
        "to reduce emergence reactions.",

        'tier-high',
        _SA,
        DID['sedation_analgesia'],
        'analgesic_ladder',
        '{"hi":3}',
        'chart-l2'
    ),
    (
        "On the analgesic chart, IV acetaminophen 1000 mg q6h is ordered. "
        "A patient weighs 45 kg with ALT 480 U/L. "
        "Two required medication adjustments are _______.",

        "Dose reduction required: weight <50 kg → reduce dose to 650 mg q6h "
        "(or 12.5 mg/kg q6h)\n"
        "| Hepatotoxicity risk: ALT 480 U/L = >3× ULN → acetaminophen is "
        "hepatically metabolized via CYP2E1 to NAPQI (toxic metabolite); "
        "active liver disease increases NAPQI accumulation risk → reduce dose "
        "to 325–650 mg q6h OR consider alternative analgesic\n"
        "→ CCRN KEY: IV acetaminophen absolute dose limits: ≤4 g/day healthy "
        "adults; ≤2 g/day for hepatic impairment, weight <50 kg, malnutrition, "
        "or active alcohol use disorder. ICU advantage: no respiratory depression, "
        "no GI motility effects, opioid-sparing 20–30%.\n"
        "→ MASTERY NOTE: Acetaminophen hepatotoxicity threshold: "
        ">150 mg/kg in acute overdose, but much lower in chronic liver disease or "
        "CYP2E1 induction (alcohol, isoniazid). ICU nurses often administer "
        "scheduled acetaminophen without weight-based adjustment — "
        "always verify dose relative to weight AND hepatic function.",

        'tier-critical',
        _SA,
        DID['sedation_analgesia'],
        'analgesic_ladder',
        '{"hi":4}',
        'chart-l3'
    ),

    # ═══ propofol_pris ════════════════════════════════════════════════════════
    (
        "On the propofol chart, Propofol Infusion Syndrome (PRIS) occurs at "
        "doses _______ for >48 hours. The earliest lab finding is "
        "new _______ metabolic acidosis.",

        "Dose threshold: >4–5 mg/kg/h (>67 mcg/kg/min) for >48h\n"
        "| Earliest lab finding: new anion-gap metabolic acidosis "
        "(↑ AG, ↓ HCO₃, rising lactate — before other organ manifestations)\n"
        "| Full PRIS: metabolic acidosis + rhabdomyolysis (CK >5000) + "
        "cardiac arrhythmia/failure + hyperkalemia + hypertriglyceridemia\n"
        "→ CCRN KEY: PRIS management: STOP propofol immediately → switch to "
        "midazolam, dexmedetomidine, or ketamine → vasopressors for hemodynamic "
        "support → CRRT for refractory acidosis/hyperkalemia → treat arrhythmias. "
        "PRIS mortality 18–83% if diagnosis is delayed.\n"
        "→ MASTERY NOTE: PRIS prevention: limit propofol to ≤4 mg/kg/h; "
        "check triglycerides every 72h (hold if TG >400 mg/dL); "
        "account for lipid calories (1 mg/kg/h propofol = 0.1 g fat/kg/day; "
        "max total lipid 1.5 g fat/kg/day including TPN/EN); "
        "change infusion line every 12h.",

        'tier-review',
        _SA,
        DID['sedation_analgesia'],
        'propofol_pris',
        '{"sel":2}',
        'chart-l1'
    ),
    (
        "The propofol chart shows its mechanism: it acts at _______ receptors. "
        "Two reasons propofol is preferred over midazolam for ICU sedation are _______.",

        "GABA-A receptors — positive allosteric modulator (same receptor target as "
        "benzodiazepines, different binding site; faster onset and more titratable)\n"
        "| Preferred over midazolam because:\n"
        "(1) Predictable, faster offset — short context-sensitive half-life "
        "allows timely wake-up and SAT; midazolam accumulates unpredictably "
        "(hepatic metabolites, prolonged sedation in critically ill)\n"
        "(2) Lower delirium rates — PADIS 2018 recommends propofol or "
        "dexmedetomidine over benzodiazepines for most ICU sedation\n"
        "→ CCRN KEY: Propofol formulation: 10% intralipid emulsion (1.1 kcal/mL). "
        "Account for caloric content in nutrition plan — "
        "1 mg/kg/h propofol = 0.1 g fat/kg/day. Triglycerides elevation "
        "at high doses. Does NOT provide analgesia — always pair with an analgesic.\n"
        "→ MASTERY NOTE: Propofol advantages vs. midazolam: shorter mechanical "
        "ventilation duration, earlier extubation, faster neurological assessment. "
        "Disadvantages: higher cost, PRIS risk, hypotension with bolus dosing, "
        "propofol-related infections (lipid medium for bacterial growth).",

        'tier-high',
        _SA,
        DID['sedation_analgesia'],
        'propofol_pris',
        '{"sel":0}',
        'chart-l2'
    ),
    (
        "On the propofol chart, a patient on propofol 60 mcg/kg/min ×72h "
        "develops pH 7.22, lactate 7.1, CK 14,000, K⁺ 6.3, TG 690 mg/dL. "
        "This is _______. The FIRST nursing action is _______.",

        "PROPOFOL INFUSION SYNDROME (PRIS) — all diagnostic criteria met: "
        "dose >67 mcg/kg/min >48h + anion-gap metabolic acidosis + "
        "rhabdomyolysis + hyperkalemia + hypertriglyceridemia\n"
        "| FIRST action: STOP propofol infusion immediately — "
        "switch to alternative sedation (midazolam 0.02–0.1 mg/kg/h or dexmedetomidine)\n"
        "| Concurrent: notify provider STAT; treat hyperkalemia; "
        "continuous cardiac monitoring; vasopressors for hemodynamic support; "
        "consider CRRT for refractory acidosis/K⁺ elevation\n"
        "→ CCRN KEY: Early recognition is critical — PRIS mortality is "
        "18–83% and increases significantly when diagnosis is delayed. "
        "Rising CK alone (without acidosis) is non-specific; "
        "the combination of new AG metabolic acidosis + CK elevation "
        "in a patient on high-dose propofol = PRIS until proven otherwise.\n"
        "→ MASTERY NOTE: Risk factors for PRIS: young patients, "
        "doses >4 mg/kg/h, duration >48h, concurrent catecholamines or steroids, "
        "carbohydrate-restricted diet (depletes glycogen, increases fat oxidation). "
        "Cardiac manifestations: right bundle branch block, ST changes, "
        "fatal arrhythmias — ECG monitoring is mandatory.",

        'tier-critical',
        _SA,
        DID['sedation_analgesia'],
        'propofol_pris',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ dexmedetomidine ══════════════════════════════════════════════════════
    (
        "On the dexmedetomidine comparison chart, dex preserves _______ while "
        "midazolam depresses it. Name two settings where this advantage is clinically important.",

        "Preserves spontaneous respiratory drive (α2 agonist → ↓ NE release "
        "from locus ceruleus → sedation without respiratory center depression)\n"
        "| Important clinical settings:\n"
        "(1) Non-invasive ventilation (NIV/BiPAP): sedation needed but apnea "
        "would eliminate BiPAP efficacy — dex allows sedation while patient "
        "continues to breathe spontaneously\n"
        "(2) Ventilator weaning: sedation needed during weaning trials without "
        "depressing drive to breathe; facilitates extubation readiness\n"
        "→ CCRN KEY: Dex dosing: loading dose 1 mcg/kg over 10–20 min "
        "(often omitted in hemodynamically unstable patients); maintenance "
        "0.2–0.7 mcg/kg/h. Side effects: bradycardia (most common), "
        "hypotension, transient hypertension during loading dose.\n"
        "→ MASTERY NOTE: Dex bradycardia management: reduce infusion rate → "
        "atropine 0.5–1 mg IV if HR <40 or hemodynamically significant → "
        "hold infusion if persistent. Avoid loading dose in patients with "
        "preexisting bradycardia, 2nd/3rd degree AV block, or severe hypotension.",

        'tier-review',
        _SA,
        DID['sedation_analgesia'],
        'dexmedetomidine',
        '{"hi":1}',
        'chart-l1'
    ),
    (
        "The dexmedetomidine comparison chart shows MENDS trial results. "
        "Dexmedetomidine vs. lorazepam for ICU sedation: dex patients had "
        "fewer _______ and _______ days. What guideline does this support?",

        "Fewer coma days AND fewer delirium days "
        "(median 7 vs. 10 days for dex vs. lorazepam, p=0.01; MENDS trial, NEJM 2007)\n"
        "| Supports: PADIS 2018 SCCM guidelines recommendation to AVOID "
        "continuous benzodiazepine infusions for routine ICU sedation — "
        "prefer propofol or dexmedetomidine instead\n"
        "→ CCRN KEY: SEDCOM trial (propofol vs. dex): similar ventilator-free "
        "days; dex patients had fewer days of delirium, more bradycardia/hypotension "
        "but less respiratory depression. Combined MENDS+SEDCOM evidence: "
        "dex and propofol are preferred over benzodiazepines.\n"
        "→ MASTERY NOTE: Mechanism of benzo-associated delirium: GABA-A "
        "hyperactivation disrupts cholinergic neurotransmission in the "
        "hippocampus → impaired memory consolidation and orientation → "
        "delirium. Benzodiazepines are an INDEPENDENT risk factor for ICU "
        "delirium — each additional day of benzo use increases delirium risk by 22%.",

        'tier-high',
        _SA,
        DID['sedation_analgesia'],
        'dexmedetomidine',
        '{"hi":2}',
        'chart-l2'
    ),
    (
        "On the dex chart, a patient develops HR 36, MAP 70 during dexmedetomidine "
        "loading dose. In order, the three interventions are _______.",

        "1. Slow or stop the loading dose (loading: 1 mcg/kg over 10–20 min — "
        "extend infusion time or discontinue if hemodynamically unstable)\n"
        "2. Reduce maintenance infusion rate (from starting dose toward minimum "
        "0.2 mcg/kg/h; many protocols skip loading entirely in high-risk patients)\n"
        "3. Atropine 0.5–1 mg IV if HR remains <40 bpm or patient becomes "
        "hemodynamically unstable (MAP <65 despite fluid)\n"
        "→ CCRN KEY: Dex-induced bradycardia is dose-dependent — loading dose "
        "causes the most pronounced effect. Prevention: avoid or slow the loading "
        "dose in patients with baseline HR <60, cardiac conduction disease, "
        "or hemodynamic instability. This is the most common side effect.\n"
        "→ MASTERY NOTE: Dex does NOT provide analgesia at standard ICU doses — "
        "must still assess and treat pain with opioid or non-opioid agents. "
        "Dex cooperative sedation (RASS −1 to 0) allows patients to report "
        "pain on NRS and communicate with family — a unique clinical advantage "
        "that deepens with adequate analgesia co-administration.",

        'tier-critical',
        _SA,
        DID['sedation_analgesia'],
        'dexmedetomidine',
        '{"hi":0}',
        'chart-l3'
    ),

    # ═══ cam_icu ══════════════════════════════════════════════════════════════
    (
        "On the CAM-ICU assessment chart, the tool is positive when "
        "Feature 1 AND Feature _______ AND (Feature _______ OR Feature _______) "
        "are all present. What is the RASS gate to begin assessment?",

        "Feature 1 AND Feature 2 AND (Feature 3 OR Feature 4)\n"
        "| RASS gate: RASS ≥ −3 required to proceed with CAM-ICU. "
        "RASS −4 or −5 = Unable to Assess (UTA) — document as UTA, "
        "not 'CAM-ICU negative.' Deep sedation prevents delirium assessment, "
        "not absence of delirium.\n"
        "→ CCRN KEY: Feature summary: F1 = Acute/fluctuating mental status change; "
        "F2 = Inattention (ASE: letter squeeze test, >2 errors); "
        "F3 = Altered LOC (RASS ≠ 0); F4 = Disorganized thinking (4 yes/no + "
        "command test, >1 error). CAM-ICU takes <2 minutes once trained.\n"
        "→ MASTERY NOTE: Delirium subtypes: Hyperactive (RASS >0, agitated) = "
        "obvious and over-diagnosed; Hypoactive (RASS 0 to −2, quiet/withdrawn) = "
        "60% of ICU delirium cases, most commonly MISSED; Mixed = fluctuates. "
        "Hypoactive delirium has the WORST prognosis — worse outcomes than hyperactive.",

        'tier-review',
        _SA,
        DID['sedation_analgesia'],
        'cam_icu',
        '{}',
        'chart-l1'
    ),
    (
        "The CAM-ICU chart shows Feature 2 (Inattention) assessment. "
        "The ASE asks the patient to squeeze hand on the letter _______ "
        "in a 10-letter sequence. More than _______ errors = inattention present.",

        "'A' — Standard sequence: S-A-V-E-A-H-A-A-R-T "
        "(patient should squeeze hand 4 times, at each 'A')\n"
        "| More than 2 errors = inattention present → Feature 2 POSITIVE\n"
        "| Errors counted: missed squeezes on 'A' + incorrect squeezes on non-'A' letters\n"
        "→ CCRN KEY: Inattention is the cardinal feature of delirium — "
        "a patient can answer simple conversational questions (preserved long-term "
        "memory) yet have severe inattention. Never substitute a conversation "
        "for the ASE test. Alternative: Visual ASE (pictures) for "
        "hearing-impaired, non-English speaking, or non-verbal intubated patients.\n"
        "→ MASTERY NOTE: Feature 4 (Disorganized Thinking): 4 yes/no questions "
        "('Does a stone float on water?' 'Are there fish in the sea?' "
        "'Does one pound weigh more than two pounds?' 'Can you use a hammer "
        "to pound a nail?') + command test (hold up N fingers → other hand). "
        ">1 error = positive Feature 4.",

        'tier-high',
        _SA,
        DID['sedation_analgesia'],
        'cam_icu',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "On the CAM-ICU chart, a patient screens positive for delirium. "
        "Non-pharmacological interventions from the ABCDEF bundle include "
        "_______ (name at least four). Is haloperidol recommended for treatment?",

        "Non-pharmacological bundle interventions:\n"
        "| A: Assess and treat pain — uncontrolled pain drives delirium\n"
        "| B: Daily SAT + SBT — minimizes sedation exposure\n"
        "| C: Choice of sedation — prefer propofol/dex over benzodiazepines\n"
        "| D: Delirium monitoring — CAM-ICU twice daily\n"
        "| E: Early mobilization — PT/OT even on mechanical ventilation\n"
        "| F: Family engagement — reorientation, familiar voices, photo boards\n"
        "| Environmental: orient q shift (day/date/place); lights on daytime, "
        "off at night; hearing aids + glasses in place; minimize nocturnal interruptions\n"
        "| Haloperidol: NO — MIND trial and HOPE-ICU trial showed haloperidol "
        "does NOT reduce delirium duration or improve outcomes vs. placebo. "
        "Use ONLY for severe agitation with safety risk, not routine delirium treatment.\n"
        "→ CCRN KEY: THINK mnemonic for ICU delirium risk factors: T=Toxic medications "
        "(benzos, anticholinergics, opioids), H=Hypoxemia, I=Infection/Immobility, "
        "N=Non-pharmacological factors (sleep deprivation, sensory loss, pain), "
        "K=K⁺ and metabolic disturbances.\n"
        "→ MASTERY NOTE: Each day of ICU delirium is associated with a 10% increase "
        "in mortality and long-term cognitive impairment. Delirium is modifiable — "
        "the nurse's role in ABCDEF bundle execution directly affects outcomes.",

        'tier-critical',
        _SA,
        DID['sedation_analgesia'],
        'cam_icu',
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
