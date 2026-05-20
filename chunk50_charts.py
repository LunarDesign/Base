#!/usr/bin/env python3
"""chunk50_charts.py — Ph8 Reference: Ventilator Settings (15 cards)"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_49.apkg'
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_50.apkg'
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'c50')
CHUNK_NUM   = 50
MID_BASE    = 1_800_005_095
CHART_ORDER = ['vent_modes', 'lung_protective', 'weaning_sbt', 'vent_alarms', 'niv_hfnc']

_NM = 'Ph8 · \U0001f7e1 T3 · Reference — Ventilator Settings'

RF = {}

# ── Chart 1: Ventilator Modes ─────────────────────────────────────────────────
RF['vent_modes'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var hi=(P.hi!==undefined)?P.hi:-1;
    var modes=[
        {n:'VC-AC\n(Vol Control)',trg:'Patient/time',rate:'Yes — guaranteed',set:'Tidal Volume\n(mL/kg IBW)',use:'ARDS (LPV protocol)\nMost common ICU\nFixed Vt; variable Paw',c:'#4488cc'},
        {n:'PC-AC\n(Pres Control)',trg:'Patient/time',rate:'Yes — guaranteed',set:'Insp Pressure\n(cmH₂O)',use:'Decelerating flow\nVariable Vt; limit Paw\nWatch Vt if compliance↓',c:'#3a9a5c'},
        {n:'SIMV',trg:'Patient+timer',rate:'Yes — mandatory',set:'Vt + PS level\n(for spont breaths)',use:'Weaning (less common)\nMandatory + spont\nSlower wean vs SBT',c:'#cc8844'},
        {n:'PSV\n(Pres Support)',trg:'Patient ONLY',rate:'NO — apnea risk',set:'Pressure Support\n(cmH₂O above PEEP)',use:'Weaning / SBT\nPatient drives RR+Vt\nRequires intact drive',c:'#9060c0'},
        {n:'APRV\n(BiPAP-vent)',trg:'Spont (any phase)',rate:'P-high sustained',set:'P-high/T-high\nP-low/T-low',use:'Refractory ARDS\nSustained recruitment\nAlt to proning',c:'#cc6633'}
    ];
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var hdrH=18, rh=Math.floor((H-hdrH)/modes.length);
    var xs=[4,105,165,235,320,616];
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,hdrH);
    var hdrs=['Mode','Trigger','Rate Guaranteed','Primary Parameter','ICU Use Case'];
    ctx.font='bold 7.5px sans-serif';ctx.textAlign='center';ctx.fillStyle='#aaa';
    hdrs.forEach(function(h,i){ctx.fillText(h,(xs[i]+xs[i+1])/2,hdrH-4);});
    modes.forEach(function(d,ri){
        var ry=hdrH+ri*rh;
        var faded=(hi>=0&&hi!==ri);
        ctx.globalAlpha=faded?0.2:1;
        ctx.fillStyle=ri%2?'#0d0d18':'#111122';ctx.fillRect(0,ry,W,rh);
        ctx.fillStyle=d.c+'33';ctx.fillRect(xs[0],ry,xs[1]-xs[0],rh);
        ctx.fillStyle=d.c;ctx.font='bold 8px sans-serif';ctx.textAlign='left';
        d.n.split('\n').forEach(function(l,li){ctx.fillText(l,xs[0]+3,ry+rh/2-5+li*10);});
        ctx.fillStyle='#aabbcc';ctx.font='7.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(d.trg,(xs[1]+xs[2])/2,ry+rh/2+3);
        ctx.fillStyle=(d.rate==='NO — apnea risk')?'#ff6644':'#88cc88';
        ctx.font='7.5px sans-serif';ctx.textAlign='center';
        d.rate.split('\n').forEach(function(l,li){ctx.fillText(l,(xs[2]+xs[3])/2,ry+rh/2-3+li*9);});
        ctx.fillStyle='#eedd88';ctx.font='7.5px sans-serif';ctx.textAlign='left';
        d.set.split('\n').forEach(function(l,li){ctx.fillText(l,xs[3]+3,ry+rh/2-5+li*10);});
        ctx.fillStyle='#99aabb';ctx.font='7px sans-serif';ctx.textAlign='left';
        d.use.split('\n').forEach(function(l,li){ctx.fillText(l,xs[4]+3,ry+rh/2-9+li*9);});
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
        var lbs=['VC-AC','PC-AC','SIMV','PSV','APRV'];
        lbs.forEach(function(lb,i){(function(idx){var b=_mkB(lb,modes[idx].c,hi===idx,function(on){
            var p2={hi:on?idx:-1};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });row.appendChild(b);})(i);});
        var rst=_mkB('All',_AX,hi===-1,function(){cv.setAttribute('data-params','{}');_render(cv,ctrl,{});});
        row.appendChild(rst);ctrl.appendChild(row);
    }
}
"""

# ── Chart 2: Lung-Protective Ventilation ──────────────────────────────────────
RF['lung_protective'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['ARDSNet Protocol','Driving Pressure','Prone Positioning'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a2a1a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a3a2a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#3a9a5c':'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#080a08';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+14;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#88bbee';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+190,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a3a2a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('Tidal Volume:','6 mL/kg IBW (range 4–8; target 6)','#3a9a5c','#eedd88');
        nt('IBW (male): 50 + 2.3 × [height(in) − 60]  |  (female): 45.5 + 2.3 × [height(in) − 60]');
        nt('If Pplat > 30 cmH₂O → reduce Vt by 1 mL/kg steps down to minimum 4 mL/kg');
        rw('Plateau Pressure:','≤ 30 cmH₂O (inspiratory hold 0.5–1.0s, passive patient)','#3a9a5c','#eedd88');
        nt('Check Pplat q4h and after every Vt or PEEP change');
        rw('Rate:','14–24 breaths/min; titrate to pH ≥ 7.20–7.25','#3a9a5c','#eedd88');
        hr();
        rw('PEEP/FiO₂ Pairing (ARDSNet low-PEEP table):','','#88bbee');
        nt('FiO₂ 0.30–0.40 → PEEP 5   |  0.40–0.50 → PEEP 5–8   |  0.50–0.60 → PEEP 8–10');
        nt('FiO₂ 0.60–0.80 → PEEP 10–14  |  0.80–1.0 → PEEP 14–22');
        nt('Goal: PaO₂ 55–80 mmHg or SpO₂ 88–95%');
        hr();
        nt('★ ARMA trial (NEJM 2000): 6 vs 12 mL/kg IBW → 31.0% vs 39.8% mortality (P=0.007)');
        nt('★ Use IBW NOT actual weight — a 150 kg patient still gets Vt based on height');
    } else if(sel===1){
        rw('Driving Pressure (ΔP):','Pplat − PEEP','#eedd88','#ffcc44');
        rw('Target:','≤ 15 cmH₂O (Amato et al. NEJM 2015)','#3a9a5c','#eedd88');
        nt('ΔP strongest predictor of ARDS survival — stronger than Vt or Pplat alone');
        nt('ΔP = Vt ÷ Crs: higher ΔP = fewer open alveoli = overdistension of remaining lung');
        hr();
        rw('Respiratory Compliance (Crs):','Vt ÷ (Pplat − PEEP)','#88bbee','#eedd88');
        nt('Normal: 60–100 mL/cmH₂O  |  Mild ARDS: 40–60  |  Mod: 25–40  |  Severe: < 25');
        nt('Falling Crs over time = worsening disease or new process (edema, atelectasis)');
        hr();
        rw('VILI (Ventilator-Induced Lung Injury):','','#cc8844');
        nt('Volutrauma: excessive stretch (high Vt) → disrupts alveolar-capillary membrane');
        nt('Atelectrauma: cyclic open/close of unstable alveoli → shear stress → injury');
        nt('Biotrauma: mechanical injury → IL-6/IL-8 cytokine release → systemic inflammation');
        nt('Optimal PEEP prevents atelectrauma without causing overdistension (high ΔP)');
        hr();
        nt('★ LUNG SAFE study: LPV underutilized globally; many ARDS patients receive > 8 mL/kg IBW');
    } else {
        rw('Indication:','P/F < 150 mmHg despite LPV + PEEP ≥ 10 cmH₂O','#cc8844','#ffcc88');
        rw('Duration:','≥ 16 hours per day (prone session); repeat daily','#3a9a5c','#eedd88');
        rw('PROSEVA trial:','28-day mortality 16.0% prone vs 32.8% supine (P<0.001, NNT=6)','#3a9a5c','#66ff88');
        nt('Initiate early: within 36h of ARDS onset with LPV established');
        hr();
        rw('Contraindications:','','#cc4444');
        nt('Unstable spine / recent sternotomy / anterior wounds / open abdomen');
        nt('Uncontrolled elevated ICP; hemodynamic instability; massive facial trauma');
        hr();
        rw('Nursing Considerations:','','#88bbee');
        nt('Secure ETT before turning; ≥ 5 staff; RT holds airway during log-roll');
        nt('Pad: forehead, chin, chest, knees q2h; eye lubricant + gentle tape — corneal abrasion risk');
        nt('CXR after prone to confirm ETT position (target: 3–5 cm above carina)');
        nt('Return to supine if: SpO₂ < 88%, SBP < 60, VT, accidental extubation');
    }
    if(ctrl){
        ctrl.innerHTML='';
        var crow=document.createElement('div');crow.style.cssText='display:flex;gap:6px;margin-top:6px;';
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,'#3a9a5c',sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });crow.appendChild(b);})(i);});
        ctrl.appendChild(crow);
    }
}
"""

# ── Chart 3: Weaning & SBT ────────────────────────────────────────────────────
RF['weaning_sbt'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['Weaning Readiness','SBT Protocol','Post-Extubation'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a1a2e':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#4488cc':'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#08080f';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+14;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#88bbee';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+185,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('RSBI (Rapid Shallow Breathing Index):','f ÷ VT(L); goal < 105','#4488cc','#eedd88');
        nt('RSBI < 80: high likelihood of success  |  RSBI > 105: high likelihood of failure');
        nt('Measured during 1–3 min of CPAP or T-piece before SBT (not sustained effort)');
        hr();
        rw('SBT Eligibility Criteria (all required):','','#88bbee');
        nt('FiO₂ ≤ 50%  AND  PEEP ≤ 8 cmH₂O  AND  SpO₂ ≥ 90%');
        nt('Hemodynamically stable (no escalating vasopressors)');
        nt('Awake, following commands, GCS ≥ 13; intact cough/gag reflex');
        nt('Reversal of primary reason for intubation');
        hr();
        rw('Additional weaning parameters (supplemental):','','#aaa');
        nt('NIF (MIP): more negative than −20 to −30 cmH₂O (tests inspiratory muscle strength)');
        nt('Vital capacity: > 10–15 mL/kg IBW');
        hr();
        nt('★ Daily SBT screening protocol (Ely AJRCCM 1996): reduces ventilator days and ICU LOS');
        nt('★ ABC bundle: Awakening (SAT) + Breathing Coordination (SBT) → synergistic benefit');
    } else if(sel===1){
        rw('SBT Method:','T-piece OR PSV 5–8 cmH₂O + PEEP 5','#4488cc','#eedd88');
        rw('Duration:','30–120 min (30 min adequate per REVA trial)','#4488cc','#eedd88');
        hr();
        rw('SBT FAILURE — return to prior settings if ANY:','','#cc4444');
        nt('RR > 35 breaths/min  OR  SpO₂ < 90%  OR  RSBI > 105 during SBT');
        nt('HR > 140 or change > 20%  OR  SBP > 180 or < 90 mmHg');
        nt('Increasing accessory muscle use, paradoxical breathing, diaphoresis, agitation');
        hr();
        rw('SBT PASS → Extubation Assessment:','','#3a9a5c');
        nt('Able to follow commands; adequate secretion clearance; peak cough flow > 160 L/min');
        nt('No stridor on cuff deflation; hemodynamically stable without new vasopressor need');
        hr();
        nt('★ TRICC / Ely trials: protocolized daily SBT superior to physician-directed weaning');
        nt('★ SAT before SBT (ABC bundle): reduces mechanical ventilation days by 3 days (MICU)');
    } else {
        rw('Post-Extubation HFNC (high-risk patients):','','#4488cc');
        rw('Flow:','30–60 L/min (start 40–50); FiO₂ to SpO₂ ≥ 92%','#aab','#eedd88');
        nt('LOZANO trial: prophylactic HFNC post-extubation reduces reintubation vs standard O₂');
        nt('Especially: P/F < 300, age > 65, COPD/CHF, prolonged ventilation > 7 days');
        hr();
        rw('ROX Index:','(SpO₂/FiO₂) ÷ RR','#88bbee','#ffcc44');
        rw('Failure threshold:','ROX < 4.88 at 12 hours → predict HFNC failure → intubate','#cc4444','#ff6644');
        nt('ROX > 4.88 at 12h: likely to succeed; continue monitoring');
        hr();
        rw('Post-Extubation NIV (BiPAP):','','#9060c0');
        nt('Preferred over HFNC when CO₂ retention is concern (COPD exacerbation post-extubation)');
        nt('OPTIEX trial: HFNC non-inferior to NIV for post-extubation respiratory failure');
        nt('Do NOT delay reintubation — early intubation in HFNC failure → better outcomes than late');
        hr();
        nt('★ High-risk extubation: age > 65, prolonged MV > 7d, weak cough, excessive secretions');
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

# ── Chart 4: Ventilator Alarms & Troubleshooting ─────────────────────────────
RF['vent_alarms'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['DOPES — Acute Deterioration','Peak Pressure Troubleshoot','Auto-PEEP (Air Trapping)'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#2a1a0a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#3a2a1a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#cc8844':'#555';
        ctx.font=(sel===i?'bold ':'')+'8px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#0a0804';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+14;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#cc8844';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+185,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a1a0a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('FIRST action: DISCONNECT and manually bag (100% FiO₂ BVM)','','#ff6644');
        nt('Removing vent eliminates equipment as variable: if improves → vent problem; if not → patient');
        hr();
        rw('D — Displacement:','ETT dislodged, right mainstem, too deep/shallow','#eedd88');
        nt('Right mainstem: absent LEFT breath sounds; pull ETT back 1–2 cm; CXR confirm');
        rw('O — Obstruction:','Secretions, mucus plug, kink, bite, circuit blockage','#eedd88');
        nt('Suction ETT; insert bite block; straighten circuit; auscultate for stridor');
        rw('P — Pneumothorax:','Tension: absent BS, tracheal deviation, hemodynamic collapse','#ff6644');
        nt('Needle decompression 2nd ICS MCL (then chest tube) — do NOT delay for CXR');
        rw('E — Equipment failure:','Vent malfunction, circuit disconnect, cuff leak','#eedd88');
        nt('Check all connections; listen for leak; pilot balloon deflated = cuff failure');
        rw('S — Stacked breaths:','Auto-PEEP, bronchospasm, agitation/dyssynchrony','#eedd88');
        nt('Bronchospasm: wheezing; give albuterol; adjust I:E ratio; sedation if dyssynchrony');
    } else if(sel===1){
        rw('Peak Pressure ↑ + Plateau NORMAL:','→ Increased Airway RESISTANCE','#cc8844','#ffcc44');
        nt('Raw = (Peak − Plateau) ÷ Flow  |  Normal Raw: 5–15 cmH₂O/L/s');
        nt('Causes: bronchospasm, secretions, ETT kinking, patient biting ETT, circuit obstruction');
        nt('Intervention: suction, bronchodilators, bite block, NMB if patient-vent dyssynchrony');
        hr();
        rw('Peak Pressure ↑ + Plateau ↑:','→ Decreased Compliance (Crs)','#cc4444','#ff6644');
        nt('Crs = Vt ÷ (Pplat − PEEP)  |  Causes: worsening ARDS, pulmonary edema, pneumothorax');
        nt('Also: atelectasis, auto-PEEP, abdominal hypertension, pleural effusion');
        nt('Intervention: treat underlying cause; consider PEEP optimization; diuresis if overloaded');
        hr();
        rw('Plateau Pressure Measurement:','Inspiratory hold 0.5–1.0 sec','#88bbee','#eedd88');
        nt('ONLY valid in PASSIVELY ventilated patient — spontaneous effort invalidates Pplat reading');
        nt('Ensure adequate sedation (RASS −2 to −3) or NMB before interpreting Pplat');
        hr();
        nt('★ High Peak + Normal Plateau = RESISTANCE problem (airway) — NOT compliance');
        nt('★ High Peak + High Plateau = COMPLIANCE problem (lung/chest wall)');
    } else {
        rw('Auto-PEEP (Intrinsic PEEP):','Air trapped due to incomplete exhalation','#cc8844','#ffcc44');
        nt('Detection: expiratory hold maneuver — occlude exp port; pressure rises = intrinsic PEEP');
        nt('Normal expiratory time insufficient when: high RR, high Vt, high MV, bronchospasm');
        hr();
        rw('Causes:','','#eedd88');
        nt('COPD/asthma (expiratory obstruction → slow exhalation) — most common in ICU');
        nt('High set respiratory rate (inadequate expiratory time per breath)');
        nt('Bronchospasm (dynamic airway obstruction during exhalation)');
        hr();
        rw('Interventions to Reduce Auto-PEEP:','','#3a9a5c');
        nt('1. Decrease set RR (fewer breaths = longer expiration per breath)');
        nt('2. Increase inspiratory flow rate (shorter insp → longer expiratory time)');
        nt('3. Decrease tidal volume (less air in = less air to exhale)');
        nt('4. Treat bronchospasm (albuterol, ipratropium, heliox)');
        hr();
        rw('Auto-PEEP consequences:','','#cc4444');
        nt('Hemodynamic compromise: ↑ intrathoracic pressure → ↓ venous return → ↓ CO → hypotension');
        nt('Triggering difficulty: patient must generate effort > intrinsic PEEP to trigger breath');
        nt('Emergency: disconnect vent briefly (allow full exhalation) in acute auto-PEEP crisis');
    }
    if(ctrl){
        ctrl.innerHTML='';
        var crow=document.createElement('div');crow.style.cssText='display:flex;gap:6px;margin-top:6px;';
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,'#cc8844',sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });crow.appendChild(b);})(i);});
        ctrl.appendChild(crow);
    }
}
"""

# ── Chart 5: NIV & HFNC ──────────────────────────────────────────────────────
RF['niv_hfnc'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    var sel=(P.sel!==undefined)?P.sel:0;
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    var tabs=['BiPAP/NIV Settings','HFNC','NIV vs Intubation'];
    var tabW=(W-8)/tabs.length, tabH=22;
    tabs.forEach(function(t,i){
        var tx=4+i*tabW;
        ctx.fillStyle=(sel===i)?'#1a1a2a':'#0d0d0d';ctx.fillRect(tx,4,tabW,tabH);
        ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.strokeRect(tx,4,tabW,tabH);
        ctx.fillStyle=sel===i?'#9060c0':'#555';
        ctx.font=(sel===i?'bold ':'')+'8.5px sans-serif';ctx.textAlign='center';
        ctx.fillText(t,tx+tabW/2,4+tabH-6);
    });
    var panelY=30, panelH=H-panelY-4;
    ctx.fillStyle='#08080e';ctx.fillRect(4,panelY,W-8,panelH);
    var lm=14, ly=panelY+14;
    function rw(label,val,c1,c2){
        ctx.fillStyle=c1||'#9060c0';ctx.font='bold 8.5px sans-serif';ctx.textAlign='left';
        ctx.fillText(label,lm,ly);
        if(val){ctx.fillStyle=c2||'#eedd88';ctx.font='8.5px sans-serif';ctx.fillText(val,lm+185,ly);}
        ly+=13;
    }
    function nt(t,c){ctx.fillStyle=c||'#889988';ctx.font='italic 8px sans-serif';ctx.textAlign='left';ctx.fillText(t,lm+4,ly);ly+=11;}
    function hr(){ctx.strokeStyle='#2a2a3a';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lm,ly-2);ctx.lineTo(W-lm,ly-2);ctx.stroke();ly+=5;}
    if(sel===0){
        rw('EPAP:','= PEEP → improves oxygenation (recruits alveoli, ↑ FRC)','#9060c0','#eedd88');
        rw('IPAP:','= EPAP + driving pressure → CO₂ elimination / ventilation','#9060c0','#eedd88');
        rw('Pressure Support:','IPAP − EPAP (the driving force for ventilation)','#9060c0','#eedd88');
        nt('Start: IPAP 10–14 cmH₂O / EPAP 4–8 cmH₂O; FiO₂ to SpO₂ ≥ 92%');
        nt('Higher IPAP−EPAP gradient = more CO₂ clearance (more ventilatory support)');
        hr();
        rw('NIV Indications (Level I evidence):','','#88bbee');
        nt('COPD exacerbation with hypercapnia: reduces intubation/mortality (Brochard NEJM 1995)');
        nt('Acute cardiogenic pulmonary edema: CPAP or BiPAP (CPAP sufficient for pure oxygenation)');
        nt('Immunocompromised: avoid intubation infection risk if possible');
        nt('Post-extubation COPD respiratory failure (not de novo hypoxemic failure)');
        hr();
        rw('CPAP vs BiPAP:','','#cc8844');
        nt('CPAP = one constant pressure (PEEP + FiO₂) → oxygenation only; no ventilatory boost');
        nt('BiPAP = cycles IPAP/EPAP → oxygenation + CO₂ clearance; use when hypercapnia present');
    } else if(sel===1){
        rw('HFNC Settings:','Flow 30–60 L/min; FiO₂ 0.21–1.0','#4488cc','#eedd88');
        nt('Heated/humidified: reduces WOB, liquefies secretions, improves comfort vs NIV mask');
        nt('Dead space washout: high flow flushes anatomic dead space → ↑ alveolar minute vent');
        nt('Each 10 L/min ≈ 0.5–1 cmH₂O CPAP effect (variable; less with mouth open)');
        hr();
        rw('ROX Index:','(SpO₂/FiO₂) ÷ RR','#88bbee','#ffcc44');
        rw('Failure threshold:','< 4.88 at 12 hours → predict failure → intubate','#cc4444','#ff6644');
        nt('ROX > 4.88 at 12h: likely to succeed on HFNC; continue monitoring');
        hr();
        rw('FLORALI trial (NEJM 2015):','','#3a9a5c');
        nt('HFNC reduced 90-day mortality vs standard O₂ or NIV in hypoxemic RF (P/F < 300)');
        nt('HFNC now first-line for non-hypercapnic hypoxemic failure: ARDS, pneumonia, post-op');
        hr();
        rw('HFNC Failure Signs → escalate:','','#cc4444');
        nt('RR > 30–35, accessory muscle use, diaphoresis, paradoxical breathing');
        nt('Rising PaCO₂ (HFNC provides minimal CO₂ clearance → CO₂ retention = intubate)');
    } else {
        rw('NIV Absolute Contraindications:','','#cc4444');
        nt('Respiratory arrest / apnea → intubate immediately');
        nt('Inability to protect airway: absent gag/cough, GCS < 8, severe AMS');
        nt('Vomiting / active upper GI bleed (aspiration risk with positive pressure mask)');
        hr();
        rw('NIV Relative Contraindications:','','#cc8844');
        nt('Hemodynamic instability requiring vasopressors (brief bridge acceptable)');
        nt('Uncooperative / agitated patient (cannot maintain mask seal → air leak → failure)');
        nt('Excessive secretions not clearable without intubation');
        nt('Facial trauma, burns, or anatomic barrier to mask fit');
        hr();
        rw('NIV Failure → Intubate within 1–2 hours if:','','#cc4444');
        nt('No improvement in PaO₂/FiO₂ (< 175 at 1h), RR, or pH after starting NIV');
        nt('APACHE II > 29, pneumonia as etiology, excessive secretions: high failure risk');
        hr();
        rw('★ Failure predictors:','','#eedd88');
        nt('pH < 7.25 at 1h on NIV → intubate rather than prolong failed NIV trial');
        nt('HELMET interface: allows higher IPAP (20–30) without leak → specialized centers');
    }
    if(ctrl){
        ctrl.innerHTML='';
        var crow=document.createElement('div');crow.style.cssText='display:flex;gap:6px;margin-top:6px;';
        tabs.forEach(function(t,i){(function(idx){var b=_mkB(t,'#9060c0',sel===idx,function(){
            var p2={sel:idx};cv.setAttribute('data-params',JSON.stringify(p2));_render(cv,ctrl,p2);
        });crow.appendChild(b);})(i);});
        ctrl.appendChild(crow);
    }
}
"""

# ── Cards ─────────────────────────────────────────────────────────────────────
CARDS = [
    # ═══ vent_modes ═══════════════════════════════════════════════════════════
    (
        "On the vent modes chart, Volume Control AC (VC-AC) delivers a guaranteed "
        "_______ volume with each breath. "
        "The trade-off is that airway _______ pressure varies unpredictably "
        "if lung compliance decreases — requiring Pplat monitoring with a target ≤ _______ cmH₂O.",

        "VC-AC delivers a set tidal volume (6 mL/kg IBW in ARDS) with each breath\n"
        "| Trade-off: peak and plateau pressure vary with changes in lung compliance/resistance\n"
        "| Pplat target: ≤ 30 cmH₂O (ARDSNet); check q4h and after every Vt/PEEP change\n"
        "| If Pplat > 30: reduce Vt by 1 mL/kg steps down to minimum 4 mL/kg\n"
        "→ CCRN KEY: VC-AC vs PC-AC: in VC-AC, volume is guaranteed and pressure varies. "
        "In PC-AC, pressure is set and volume varies. VC-AC allows precise Vt control per ARDSNet "
        "but requires Pplat monitoring. PC-AC may limit pressure injury but Vt can drop "
        "undetected if compliance worsens — always monitor Vt closely in PC-AC.\n"
        "→ MASTERY NOTE: ALWAYS use IBW (ideal body weight), NOT actual body weight for Vt. "
        "A 150 kg patient with height 5'8\" has IBW ≈ 71 kg → Vt = 6 × 71 = 426 mL. "
        "Using actual weight (150 kg) gives 900 mL — volutrauma and near-certain VILI. "
        "IBW formula: male = 50 + 2.3 × (height in inches − 60); female = 45.5 + 2.3 × (inches − 60).",

        'tier-review',
        _NM,
        DID['vent_settings'],
        'vent_modes',
        '{"hi":0}',
        'chart-l1'
    ),
    (
        "On the modes chart, Pressure Support Ventilation (PSV) provides _______ "
        "for each breath but requires the patient to _______ every breath. "
        "If the patient becomes apneic on PSV, the ventilator will _______. "
        "PSV is used clinically for _______ and _______.",

        "PSV provides pressure augmentation (typically 5–20 cmH₂O above PEEP) per breath\n"
        "| Patient must trigger EVERY breath — NO backup mandatory rate in pure PSV\n"
        "| Apnea: alarm fires → ventilator switches to backup apnea mode (vent-specific)\n"
        "| PSV used for: (1) Spontaneous breathing trials (SBT at 5–8 cmH₂O), "
        "(2) supportive ventilation in cooperative, breathing patients\n"
        "→ CCRN KEY: Monitor PSV Vt: if < 6 mL/kg IBW → insufficient support (↑ PS level); "
        "if > 10 mL/kg → patient over-assisted (↓ PS level — over-assistance causes diaphragm atrophy). "
        "Also monitor for patient-vent dyssynchrony: double-triggering, flow starvation, reverse triggering.\n"
        "→ MASTERY NOTE: PAV (Proportional Assist Ventilation) and NAVA (Neurally Adjusted Ventilatory Assist) "
        "are advanced modes that titrate support in real time to patient effort. "
        "NAVA uses diaphragmatic EMG signal (Edi catheter) to trigger and proportion the breath — "
        "near-elimination of patient-vent dyssynchrony. Not universally available but CCRN may test "
        "as 'newer modes that optimize patient-ventilator synchrony.'",

        'tier-high',
        _NM,
        DID['vent_settings'],
        'vent_modes',
        '{"hi":3}',
        'chart-l2'
    ),
    (
        "The modes chart shows APRV maintains sustained high pressure (P-high) "
        "for _______ seconds (T-high) to recruit alveoli, then releases to P-low ≈ _______ cmH₂O "
        "for _______ seconds (T-low) for CO₂ elimination. "
        "APRV is contraindicated in patients with _______ due to worsened air trapping.",

        "APRV: P-high held for T-high = 4–6 seconds (sustained alveolar recruitment)\n"
        "| P-low = 0 cmH₂O (or 0–5); T-low = 0.4–0.8 seconds (short release for CO₂ elimination)\n"
        "| T-low set to retain 75% of peak expiratory flow — maintains auto-PEEP intentionally\n"
        "| Primary use: refractory ARDS when conventional LPV fails\n"
        "| Contraindicated in: COPD/asthma (high expiratory resistance + short T-low = severe air trapping)\n"
        "→ CCRN KEY: APRV allows unrestricted spontaneous breathing throughout the respiratory cycle "
        "(patient can breathe at P-high phase without triggering WOB penalty). "
        "Improves V/Q matching and may reduce sedation needs. "
        "However, APRV has NOT been shown superior to LPV in clinical trials — "
        "ACURASYS and StART trials showed no mortality benefit over conventional LPV.\n"
        "→ MASTERY NOTE: Additional APRV contraindications: (1) elevated ICP — sustained high mean "
        "airway pressure → ↓ venous return → ↓ CPP; (2) severe bronchopleural fistula — "
        "long P-high drives continuous air leak through fistula; "
        "(3) hemodynamic instability — high intrathoracic pressure impairs venous return.",

        'tier-critical',
        _NM,
        DID['vent_settings'],
        'vent_modes',
        '{"hi":4}',
        'chart-l3'
    ),

    # ═══ lung_protective ══════════════════════════════════════════════════════
    (
        "The ARDSNet protocol chart shows lung-protective ventilation targets "
        "tidal volume _______ mL/kg _______ body weight. "
        "If plateau pressure exceeds _______ cmH₂O, reduce Vt by _______ mL/kg "
        "steps to a minimum of _______ mL/kg.",

        "Target Vt: 6 mL/kg IBW (ideal body weight — NOT actual body weight)\n"
        "| Plateau pressure target: ≤ 30 cmH₂O (inspiratory hold, passive patient)\n"
        "| If Pplat > 30: reduce Vt by 1 mL/kg per step, minimum 4 mL/kg\n"
        "| Permissive hypercapnia allowed: maintain pH ≥ 7.20–7.25 by adjusting RR\n"
        "| RR: 14–24 breaths/min; SpO₂ goal 88–95% (PaO₂ 55–80 mmHg)\n"
        "→ CCRN KEY: ARMA trial (NEJM 2000): 6 mL/kg vs 12 mL/kg IBW — "
        "28-day mortality 31.0% vs 39.8% (P=0.007), NNT=12. "
        "This established LPV as standard of care for ARDS. "
        "Mortality benefit comes entirely from preventing VILI — the lung IS the ventilator target.\n"
        "→ MASTERY NOTE: IBW calculation — Male: 50 + 2.3 × (height in inches − 60). "
        "Female: 45.5 + 2.3 × (height in inches − 60). "
        "For 5'10\" male: IBW = 50 + 23 = 73 kg → Vt = 438 mL. "
        "A 300 lb (136 kg) patient with same height still gets 438 mL — "
        "the obese lung is not bigger, it is stiffer and more prone to VILI.",

        'tier-review',
        _NM,
        DID['vent_settings'],
        'lung_protective',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the lung-protective chart, driving pressure is calculated as _______ minus _______. "
        "The target is ≤ _______ cmH₂O per the Amato et al. analysis. "
        "Respiratory system compliance equals _______ divided by _______.",

        "Driving pressure (ΔP) = Pplat − PEEP\n"
        "| Target: ΔP ≤ 15 cmH₂O (Amato et al. NEJM 2015 — strongest predictor of ARDS survival)\n"
        "| ΔP reflects: Vt ÷ Crs (functional lung size) — high ΔP = overdistension of fewer alveoli\n"
        "| Respiratory compliance (Crs) = Vt ÷ (Pplat − PEEP)\n"
        "| Normal Crs: 60–100 mL/cmH₂O; ARDS: 20–40 mL/cmH₂O\n"
        "→ CCRN KEY: ΔP is more predictive than Vt or Pplat alone because it accounts for "
        "the functional size of the lung. Reducing PEEP can paradoxically INCREASE ΔP "
        "(fewer alveoli open → each gets more volume stress). "
        "Never decrease PEEP without re-assessing ΔP and compliance.\n"
        "→ MASTERY NOTE: Three mechanisms of VILI — all addressed by LPV:\n"
        "• Volutrauma: excessive Vt → alveolar overdistension → membrane disruption\n"
        "• Atelectrauma: cyclic opening/closing of unstable alveoli with insufficient PEEP → shear stress\n"
        "• Biotrauma: mechanical stretch → IL-6/IL-8/TNF-α release → systemic inflammation → MODS\n"
        "Optimal PEEP opens unstable alveoli (prevents atelectrauma) without overdistension (high ΔP).",

        'tier-high',
        _NM,
        DID['vent_settings'],
        'lung_protective',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The prone positioning tab shows PROSEVA trial reduced 28-day mortality "
        "from 32.8% to _______ % in ARDS patients with P/F < _______ mmHg. "
        "Duration is ≥ _______ hours per session, initiated within _______ hours of ARDS onset.",

        "PROSEVA trial (NEJM 2013): prone 16.0% vs supine 32.8% — P<0.001, NNT=6\n"
        "| Criteria: P/F < 150 mmHg on FiO₂ ≥ 0.60 + PEEP ≥ 5 + LPV already established\n"
        "| Duration: ≥ 16 hours per prone session; cycle daily until P/F > 150 in supine position\n"
        "| Timing: early prone (within 36 hours of ARDS onset) — timing is critical for benefit\n"
        "→ CCRN KEY: Physiology of prone benefit: dorsal lung (dependent/compressed in supine) "
        "has the best blood flow. When prone, the previously dorsal (now ventral) lung has "
        "better aeration relative to perfusion → improved V/Q matching. "
        "Additionally, cardiac weight no longer compresses posterior lung — dorsal alveoli recruit.\n"
        "→ MASTERY NOTE: Nursing complications of prone positioning and prevention:\n"
        "• Facial/anterior pressure injuries: pad forehead, chin, shoulders, knees; rotate q2h\n"
        "• Corneal abrasions: lubricant drops + gentle tape; check eyes q2h\n"
        "• ETT displacement: document tube marking BEFORE turning; RT holds airway during turn\n"
        "• Line/tube dislodgement: suspend all non-essential infusions during turn; verify after\n"
        "• Requires ≥ 5-person coordinated team: designated RT + 4 nurses minimum",

        'tier-critical',
        _NM,
        DID['vent_settings'],
        'lung_protective',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ weaning_sbt ══════════════════════════════════════════════════════════
    (
        "The weaning readiness chart shows RSBI (f/VT) < _______ predicts successful extubation. "
        "RSBI is calculated as respiratory rate divided by _______. "
        "SBT screening requires FiO₂ ≤ _______ % and PEEP ≤ _______ cmH₂O.",

        "RSBI < 105 breaths/min/L predicts successful extubation (Yang & Tobin, NEJM 1991)\n"
        "| RSBI = f (RR in breaths/min) ÷ VT (in liters — not mL)\n"
        "| RSBI < 80: high likelihood of success; RSBI > 105: high likelihood of failure\n"
        "| SBT screen requires: FiO₂ ≤ 50% AND PEEP ≤ 8 cmH₂O AND SpO₂ ≥ 90%\n"
        "| Also: hemodynamically stable, awake/following commands, intact cough, reversal of intubation cause\n"
        "→ CCRN KEY: RSBI sensitivity 97%, specificity 64% for extubation success. "
        "Limitation: RSBI predicts breathing effort but NOT aspiration risk or secretion clearance. "
        "A patient passes RSBI but can still fail extubation from secretion burden or upper airway obstruction. "
        "Always assess cough strength and secretion volume alongside RSBI.\n"
        "→ MASTERY NOTE: Additional weaning parameters (less commonly used alone):\n"
        "• NIF (MIP): more negative than −20 to −30 cmH₂O (inspiratory muscle strength)\n"
        "• Vital capacity: > 10–15 mL/kg IBW\n"
        "• ABC Bundle (Awakening + Breathing Coordination): SAT followed by SBT daily "
        "reduces MV days by 3 days vs usual care (MICU trial). Pair with early mobility.",

        'tier-review',
        _NM,
        DID['vent_settings'],
        'weaning_sbt',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the SBT protocol chart, a standard spontaneous breathing trial uses "
        "pressure support of _______ cmH₂O for _______ minutes. "
        "SBT FAILURE is declared if RR exceeds _______ or SpO₂ drops below _______ %. "
        "After successful SBT, the next step is _______.",

        "SBT: T-piece OR PSV 5–8 cmH₂O + PEEP 5 for 30–120 minutes\n"
        "| 30 min adequate (REVA trial: no difference between 30 vs 120 min SBT duration)\n"
        "| Failure criteria — return to prior settings if ANY:\n"
        "  • RR > 35 breaths/min | SpO₂ < 90% | RSBI > 105 during SBT\n"
        "  • HR > 140 or change > 20% | SBP > 180 or < 90 mmHg\n"
        "  • Accessory muscle use, diaphoresis, paradoxical breathing, agitation\n"
        "| After successful SBT: extubation assessment (cough, secretions, mental status, stridor test)\n"
        "→ CCRN KEY: Protocolized daily SBT (vs physician-directed) reduces ICU LOS. "
        "SAT before SBT (ABC bundle): sedation holiday → SBT the SAME DAY → reduced MV days. "
        "Key sequence: assess eligibility at 0600 → SAT → then SBT (not SBT before SAT).\n"
        "→ MASTERY NOTE: Extubation readiness beyond passing SBT:\n"
        "• Adequate secretion management: peak cough flow > 160 L/min (manual cuff deflation test)\n"
        "• No stridor on cuff deflation test (if stridor present → racemic epinephrine or steroids)\n"
        "• Alert, following commands — mental status is independent of RSBI\n"
        "• Tracheostomy patients: cuff deflation trial → speaking valve (Passy-Muir) → capping → decannulation",

        'tier-high',
        _NM,
        DID['vent_settings'],
        'weaning_sbt',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The post-extubation chart shows HFNC at _______ L/min reduces reintubation "
        "in high-risk patients. The ROX index = _______ divided by _______. "
        "A ROX index < _______ at _______ hours predicts HFNC failure requiring intubation.",

        "Post-extubation HFNC: 30–60 L/min (start at 40–50 L/min)\n"
        "| LOZANO trial: prophylactic HFNC post-extubation reduces reintubation in P/F < 300 or age > 65\n"
        "| ROX index = (SpO₂/FiO₂) ÷ RR\n"
        "| Failure threshold: ROX < 4.88 at 12 hours → predict HFNC failure → intubate\n"
        "| ROX > 4.88 at 12h: likely to succeed; continue monitoring with serial assessments\n"
        "→ CCRN KEY: HFNC vs NIV post-extubation: OPTIEX trial showed HFNC non-inferior to NIV "
        "for high-risk post-extubation failure. Preferred for patient comfort and tolerance. "
        "NIV preferred when CO₂ retention is the primary concern (COPD exacerbation post-extubation).\n"
        "→ MASTERY NOTE: High-risk extubation criteria — patients most likely to need post-extubation support:\n"
        "• Age > 65 | COPD, CHF, or obesity hypoventilation | prolonged MV > 7 days\n"
        "• Failed ≥ 2 prior SBTs | excessive secretions | weak cough\n"
        "• Upper airway stridor post-extubation (treat: racemic epinephrine + dexamethasone)\n"
        "For high-risk patients: apply prophylactic HFNC IMMEDIATELY after extubation — "
        "do not wait for failure to develop (late HFNC/NIV rescue is less effective).",

        'tier-critical',
        _NM,
        DID['vent_settings'],
        'weaning_sbt',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ vent_alarms ══════════════════════════════════════════════════════════
    (
        "The vent alarms chart uses DOPES for acute patient-ventilator deterioration. "
        "D = _______, O = _______, P = _______, E = _______, S = _______. "
        "The FIRST intervention when a ventilated patient acutely desaturates is to _______.",

        "DOPES — Acute Ventilator Deterioration:\n"
        "| D = Displacement (ETT dislodged, right mainstem intubation, depth change)\n"
        "| O = Obstruction (secretions, mucus plug, biting ETT, circuit kink)\n"
        "| P = Pneumothorax (tension: absent BS, tracheal deviation, hemodynamic collapse)\n"
        "| E = Equipment failure (vent malfunction, disconnection, cuff leak, circuit problem)\n"
        "| S = Stacked breaths / bronchospasm (auto-PEEP, dyssynchrony, secretion load)\n"
        "| FIRST action: disconnect from vent and manually bag with 100% FiO₂ BVM\n"
        "→ CCRN KEY: Bagging eliminates equipment as a variable. "
        "Improves with bagging → vent/circuit problem. Does NOT improve → patient problem. "
        "Then: systematic DOPES workup — auscultate, suction, confirm ETT position (waveform capnography), "
        "assess for tension pneumothorax (immediate needle decompression if suspected — 2nd ICS MCL).\n"
        "→ MASTERY NOTE: Right mainstem intubation (most common ETT displacement): "
        "ETT migrates into right bronchus (wider, less angled than left). "
        "Signs: absent LEFT breath sounds (not right); right chest moving well; SpO₂ drops. "
        "Intervention: pull ETT back 1–2 cm → bilateral auscultation → CXR confirmation. "
        "ETT tip target on CXR: 3–5 cm above carina (carina = T4–T5 vertebral level).",

        'tier-review',
        _NM,
        DID['vent_settings'],
        'vent_alarms',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the peak pressure troubleshooting chart, elevated PEAK pressure "
        "with NORMAL plateau pressure indicates increased _______. "
        "Elevated BOTH peak AND plateau indicates decreased _______. "
        "Plateau pressure is only valid in a _______ ventilated patient.",

        "High Peak + Normal Plateau → increased airway RESISTANCE (Raw)\n"
        "| Raw = (Peak Pressure − Plateau) ÷ Flow | Normal Raw: 5–15 cmH₂O/L/s\n"
        "| Causes of ↑ Raw: bronchospasm, secretions, ETT kinking, biting, circuit obstruction\n"
        "| Management: suction, bronchodilators, bite block, NMB if patient-vent dyssynchrony\n"
        "| High Peak + High Plateau → decreased COMPLIANCE (Crs = Vt/Pplat−PEEP)\n"
        "| Causes of ↓ Crs: worsening ARDS, pulmonary edema, pneumothorax, auto-PEEP, abdominal HTN\n"
        "| Plateau pressure: ONLY valid in passively ventilated patient (no spontaneous effort)\n"
        "→ CCRN KEY: Remember the two-variable test: (1) Peak pressure tells you about both "
        "resistance AND compliance combined. (2) Plateau pressure isolates compliance only "
        "(resistance = zero during pause/no flow). Their relationship pinpoints the problem:\n"
        "• (Peak − Plateau) large → RESISTANCE problem (airway)\n"
        "• (Plateau − PEEP) large → COMPLIANCE problem (lung/chest wall)\n"
        "→ MASTERY NOTE: Ensure RASS −2 to −3 or NMB before measuring Pplat. "
        "Spontaneous breathing effort during inspiratory hold causes artifactual Pplat changes "
        "that misguide clinical decision-making. When in doubt, give a brief paralyzing dose "
        "and measure Pplat immediately after (neuromuscular blockade wears off quickly for single doses).",

        'tier-high',
        _NM,
        DID['vent_settings'],
        'vent_alarms',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The auto-PEEP chart shows air trapping occurs most commonly in patients with _______. "
        "The two primary ventilator interventions to reduce auto-PEEP are to decrease _______ "
        "and to _______. Auto-PEEP causes hemodynamic compromise by _______.",

        "Auto-PEEP most common in: COPD and asthma (high expiratory resistance → slow exhalation)\n"
        "| Also: high set RR, high minute ventilation, bronchospasm, secretion plugging\n"
        "| Intervention 1: Decrease set respiratory rate → longer expiratory time per breath\n"
        "| Intervention 2: Increase inspiratory flow rate → shorter inspiration → longer expiration\n"
        "| Also: decrease tidal volume, treat bronchospasm (albuterol, ipratropium, heliox)\n"
        "| Hemodynamic compromise: ↑ intrathoracic pressure → ↓ venous return → ↓ CO → hypotension\n"
        "→ CCRN KEY: Detect auto-PEEP with expiratory hold maneuver: "
        "occlude expiratory port at end-exhalation → vent displays intrinsic PEEP level. "
        "Normal auto-PEEP = 0–1 cmH₂O. Clinically significant: > 5–8 cmH₂O. "
        "Also worsens triggering: patient must generate effort GREATER than auto-PEEP level to trigger — "
        "leads to patient-vent dyssynchrony and increased WOB.\n"
        "→ MASTERY NOTE: Emergency management of acute auto-PEEP crisis (breath-stacking): "
        "disconnect ventilator briefly to allow complete exhalation ('disconnect maneuver'). "
        "This is potentially life-saving in severe asthma or COPD when auto-PEEP causes "
        "hemodynamic collapse despite adequate vasopressor support. "
        "After disconnect: reassess, reduce RR, increase flow, add bronchodilators, reassess.",

        'tier-critical',
        _NM,
        DID['vent_settings'],
        'vent_alarms',
        '{"sel":2}',
        'chart-l3'
    ),

    # ═══ niv_hfnc ═════════════════════════════════════════════════════════════
    (
        "The NIV chart shows BiPAP uses IPAP and EPAP. "
        "EPAP is equivalent to _______ and primarily improves _______. "
        "IPAP minus EPAP equals the _______ that targets CO₂ elimination. "
        "Initial ICU settings are IPAP _______ / EPAP _______.",

        "EPAP = PEEP → improves oxygenation (recruits alveoli, increases FRC)\n"
        "| IPAP − EPAP = pressure support → drives ventilation / CO₂ elimination\n"
        "| Higher IPAP−EPAP gradient = greater CO₂ clearance (more ventilatory support)\n"
        "| Initial settings: IPAP 10–14 cmH₂O / EPAP 4–8 cmH₂O; FiO₂ to SpO₂ ≥ 92%\n"
        "→ CCRN KEY: NIV Level I evidence indications:\n"
        "• COPD exacerbation with hypercapnia: reduces intubation rate + mortality (Brochard NEJM 1995)\n"
        "• Acute cardiogenic pulmonary edema: CPAP or BiPAP reduces preload/afterload + improves O₂\n"
        "• Immunocompromised respiratory failure: avoid intubation infection risk\n"
        "• Post-extubation COPD failure (NOT de novo hypoxemic respiratory failure)\n"
        "→ MASTERY NOTE: BiPAP vs CPAP distinction:\n"
        "• CPAP = one constant pressure throughout cycle (PEEP + FiO₂) → oxygenation ONLY; no ventilatory boost\n"
        "• BiPAP = cycles between IPAP and EPAP → BOTH oxygenation AND CO₂ clearance\n"
        "• CHF: CPAP often sufficient (oxygenation problem). COPD + hypercapnia: BiPAP required "
        "(needs pressure support gradient to drive CO₂ out). Choose based on pathophysiology.",

        'tier-review',
        _NM,
        DID['vent_settings'],
        'niv_hfnc',
        '{"sel":0}',
        'chart-l1'
    ),
    (
        "On the HFNC chart, the ROX index = SpO₂/FiO₂ divided by _______. "
        "A ROX index < _______ at _______ hours predicts HFNC failure. "
        "The FLORALI trial showed HFNC reduced 90-day mortality vs NIV or standard O₂ "
        "in patients with P/F < _______ mmHg.",

        "ROX index = (SpO₂/FiO₂) ÷ RR (respiratory rate)\n"
        "| ROX < 4.88 at 12 hours: predict HFNC failure → intubate\n"
        "| ROX > 4.88 at 12h: likely to succeed on HFNC; serial monitoring q2–4h\n"
        "| FLORALI (NEJM 2015): HFNC reduced 90-day mortality in P/F < 300 vs mask O₂ or NIV\n"
        "| HFNC first-line for: non-hypercapnic hypoxemic respiratory failure (ARDS, pneumonia, post-op)\n"
        "→ CCRN KEY: HFNC benefits over conventional O₂:\n"
        "• Heated/humidified: reduces WOB from breathing dry gas; loosens secretions\n"
        "• Dead space washout: continuous high flow flushes CO₂ from nasopharynx → ↑ alveolar MV\n"
        "• Precise FiO₂: 0.21–1.0 deliverable accurately (NRB mask inconsistent at high flows)\n"
        "• CPAP effect: mild positive pressure recruits alveoli (1 cmH₂O per ~10 L/min of flow)\n"
        "→ MASTERY NOTE: HFNC failure signs — escalate to NIV or intubation when:\n"
        "• RR persistently > 30–35 breaths/min (increasing effort despite support)\n"
        "• Accessory muscle use, diaphoresis, paradoxical abdominal movement\n"
        "• PaCO₂ rising (HFNC provides minimal CO₂ clearance → CO₂ retention = need for BiPAP/intubation)\n"
        "• SpO₂ declining despite FiO₂ titration | Agitation preventing interface maintenance\n"
        "CRITICAL: Do NOT delay intubation — late intubation in hypoxemic RF → worse outcomes than early.",

        'tier-high',
        _NM,
        DID['vent_settings'],
        'niv_hfnc',
        '{"sel":1}',
        'chart-l2'
    ),
    (
        "The NIV chart shows non-invasive ventilation is ABSOLUTELY contraindicated in _______. "
        "Relative contraindications include _______ and _______. "
        "NIV failure is declared if there is no improvement within _______ hours, "
        "and pH < _______ at 1 hour predicts high NIV failure risk.",

        "NIV Absolute Contraindications:\n"
        "| Respiratory arrest / apnea (intubate immediately — cannot protect airway)\n"
        "| GCS < 8 / severe altered mental status / inability to protect airway\n"
        "| Active vomiting / upper GI bleed (aspiration with positive pressure = lethal)\n"
        "| Relative Contraindications:\n"
        "| Hemodynamic instability requiring escalating vasopressors\n"
        "| Uncooperative/agitated patient (cannot maintain mask seal → air leak → failure)\n"
        "| Excessive secretions not clearable without intubation\n"
        "| Facial trauma, burns, or anatomic barrier to mask fit\n"
        "| NIV failure: no improvement in PaO₂/FiO₂, RR, or pH within 1–2 hours → intubate\n"
        "| pH < 7.25 at 1h on NIV → high failure risk → early intubation recommended\n"
        "→ CCRN KEY: NIV failure predictors (intubate early rather than prolong failed trial):\n"
        "• APACHE II > 29 | pneumonia as etiology | excessive secretions\n"
        "• P/F < 147 at 1h on NIV | pH < 7.25 at 1h | RSBI > 105 on NIV\n"
        "→ MASTERY NOTE: Helmet interface for NIV: allows higher IPAP (20–30 cmH₂O) without "
        "mask leak → better adherence and potentially improved oxygenation in ARDS "
        "(HELMET trial). Risk: CO₂ rebreathing in small helmets — requires flush flows ≥ 30 L/min. "
        "Available at specialized centers; not routinely used in most ICUs. "
        "Standard interface choice: full-face mask (oronasal) → better seal than nasal mask alone.",

        'tier-critical',
        _NM,
        DID['vent_settings'],
        'niv_hfnc',
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
