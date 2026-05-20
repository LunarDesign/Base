"""
build_utils.py — shared helpers for all chunk build scripts
Import at the top of every chunk script:
    from build_utils import *
"""
import sqlite3, json, zipfile, shutil, os, hashlib, re, time

DECK_PATH  = 'CCRN_PCCN_Mastery_v7_final.apkg'  # adjust if needed
WORK_DIR   = '/tmp/deck_work'

# ── Subdeck DID registry ─────────────────────────────────────────────────────
DID = {
    # Ph1 Cardiovascular
    'hemodynamics':        1_800_000_100,
    'acs_coronary':        1_800_000_101,
    'heart_failure':       1_800_000_102,
    'arrhythmias':         1_800_000_103,
    'aortic_vascular':     1_800_000_104,
    'post_cardiac_surg':   1_800_000_105,
    'ecmo':                1_800_000_106,
    # Ph2 Respiratory
    'ards':                1_800_000_110,
    'mechanical_vent':     1_800_000_111,
    'vent_failure_wean':   1_800_000_112,
    'obstructive':         1_800_000_114,
    'acid_base':           1_800_000_115,
    'pneumonia':           1_800_000_116,
    'pulmonary_embolism':  1_800_000_117,
    # Ph3 Multisystem
    'sepsis':              1_800_000_120,
    'mods_trauma':         1_800_000_121,
    'burns_tox':           1_800_000_122,
    'deterioration':       1_800_000_123,
    # Ph4 Neurology
    'stroke_tbi':          1_800_000_130,
    'seizures':            1_800_000_131,
    'icp_neuro':           1_800_000_132,
    'delirium':            1_800_000_133,
    # Ph5 Endocrine/Renal/GI/Heme
    'dka_hhs':             1_800_000_140,
    'thyroid_adrenal':     1_800_000_141,
    'renal_crrt':          1_800_000_150,
    'gi_hepatic':          1_800_000_151,
    'hematology':          1_800_000_152,
    # Ph6 Professional
    'professional':        1_800_000_160,
    # Ph7 Pharmacology
    'vasopressors':        1_800_000_170,
    'antiarrhythmics':     1_800_000_171,
    'sedation_analgesia':  1_800_000_172,
    'nmbas':               1_800_000_173,
    'vasoactive_antihtn':  1_800_000_174,
    'anticoagulants':      1_800_000_175,
    'diuretics':           1_800_000_176,
    'targeted_agents':     1_800_000_177,
    'mechanism_groups':    1_800_000_178,
    'drug_comparisons':    1_800_000_179,
    'patient_models':      1_800_000_180,
    'monitoring_thresh':   1_800_000_181,
    # Ph8 Reference
    'hemo_parameters':     1_800_000_190,
    'ref_acid_base':       1_800_000_191,
    'lab_values':          1_800_000_192,
    'vent_settings':       1_800_000_193,
    'terminology':         1_800_000_195,
}

# ── Note type ID ranges ───────────────────────────────────────────────────────
# Main blank-fill note type:  1_800_000_010
# Chart note types:           1_800_002_000 – 1_800_004_999  (chunks 28-30 used some)
# Next available range:       1_800_005_000+  (use for new chunks)

CHART_CSS_ADDON = """
.chart-canvas-wrap{margin-top:14px;background:#080808;border-radius:8px;
  padding:10px;border:1px solid #2a2a2a;}
canvas.physio{display:block;width:100%;max-width:100%;border-radius:4px;}
.physio-ctrl{min-height:34px;}
@media(prefers-color-scheme:light){.chart-canvas-wrap{background:#fafafa;border-color:#ddd;}}
.night_mode .chart-canvas-wrap,.nightMode .chart-canvas-wrap{background:#080808;}
"""

# ── Context variation (anti-visual-memorization) ──────────────────────────────
# Flip VARI_ENABLED=True to inject subtle font micro-theme rotation into chart
# card templates. Affects ONLY .question and .answer text (font-family, font-size).
# Canvas rendering, badges, colors, tier indicators, and clinical text are NEVER
# modified. Deterministic per card (hash of question text) so Q and A sides match.
# Toggle off: set False, then run patch_vari.py OR re-import previous .apkg.
VARI_ENABLED = True

# Injected as <script> tag prepended to qfmt/afmt when VARI_ENABLED=True.
# Picks 1 of 4 micro-themes based on a hash of the card's question text.
# Uses 80ms setTimeout so DOM is settled before applying custom properties.
VARI_JS = r"""
(function(){
  var ts=[
    {ff:'system-ui,-apple-system,sans-serif',fs:'15px'},
    {ff:'Georgia,serif',                     fs:'15px'},
    {ff:'system-ui,-apple-system,sans-serif',fs:'14px'},
    {ff:'Georgia,serif',                     fs:'14px'}
  ];
  function _cv(){
    var q=document.querySelector('.question');
    var h=q?(q.textContent||'').split('').reduce(function(a,c){return(a*31+c.charCodeAt(0))>>>0;},0):0;
    var t=ts[h%ts.length];
    [].forEach.call(document.querySelectorAll('.card-inner'),function(el){
      el.style.setProperty('--cv-ff',t.ff);
      el.style.setProperty('--cv-fs',t.fs);
    });
  }
  if(document.readyState==='loading')
    document.addEventListener('DOMContentLoaded',function(){setTimeout(_cv,80);});
  else setTimeout(_cv,80);
})();
"""

# Appended to chart note type CSS when VARI_ENABLED=True.
# Uses var() with fallbacks so cards render correctly even if VARI_JS fails.
# Scoped to .card-inner children only — badge, canvas, controls are unaffected.
VARI_CSS_ADDON = """
.card-inner .question,.card-inner .answer{
  font-family:var(--cv-ff,system-ui,-apple-system,sans-serif);
  font-size:var(--cv-fs,15px);
}
"""

SHARED_JS = r"""
var _BG='#000',_GR='#2a2a2a',_AX='#666',_LB='#888',_TX='#e8e8e8';
var _TE='#29b6f6',_RE='#ef5350',_GN='#4caf50',_AM='#ffca28',_OR='#ff7043',_PU='#ce93d8',_PI='#f06292';
function _cl(c,W,H){c.fillStyle=_BG;c.fillRect(0,0,W,H);}
function _gd(c,mx,my,pw,ph,xs,xD,ys,yD){c.strokeStyle=_GR;c.lineWidth=1;
  for(var y=0;y<=yD;y+=ys){var py=my+ph-(y/yD)*ph;c.beginPath();c.moveTo(mx,py);c.lineTo(mx+pw,py);c.stroke();}
  for(var x=0;x<=xD;x+=xs){var px=mx+(x/xD)*pw;c.beginPath();c.moveTo(px,my);c.lineTo(px,my+ph);c.stroke();}}
function _ax(c,mx,my,pw,ph){c.strokeStyle=_AX;c.lineWidth=2;c.beginPath();c.moveTo(mx,my);c.lineTo(mx,my+ph);c.lineTo(mx+pw,my+ph);c.stroke();}
function _lb(c,t,x,y,col,sz,al){c.fillStyle=col||_LB;c.font=(sz||11)+'px -apple-system,sans-serif';c.textAlign=al||'center';c.fillText(t,x,y);}
function _rl(c,t,cx,cy){c.save();c.fillStyle=_LB;c.font='11px -apple-system,sans-serif';c.textAlign='center';c.translate(cx,cy);c.rotate(-Math.PI/2);c.fillText(t,0,0);c.restore();}
function _dot(c,x,y,r,col){c.fillStyle=col;c.beginPath();c.arc(x,y,r,0,Math.PI*2);c.fill();}
function _crv(c,fn,x0,x1,mx,my,pw,ph,xD,yD,col,lw){
  c.strokeStyle=col;c.lineWidth=lw||2.5;c.beginPath();
  var st=(x1-x0)/250,first=true;
  for(var x=x0;x<=x1+st;x+=st){var y=Math.max(0,Math.min(yD,fn(x)));
    var cx2=mx+(x/xD)*pw,cy2=my+ph-(y/yD)*ph;
    if(first){c.moveTo(cx2,cy2);first=false;}else c.lineTo(cx2,cy2);}
  c.stroke();}
function _mkB(lbl,col,on,cb){var b=document.createElement('button');b.textContent=lbl;
  b.style.cssText='font-size:11px;padding:3px 9px;border-radius:4px;cursor:pointer;font-weight:700;'+
    'border:1px solid '+col+';background:'+(on?col+'22':'transparent')+';color:'+(on?col:'#555')+';';
  b.addEventListener('click',function(){cb(!b._on);});b._on=on;return b;}
function _mkS(lab,min,max,step,init,fmt,cb){var w=document.createElement('div');
  w.style.cssText='display:flex;align-items:center;gap:7px;';
  var l=document.createElement('span');l.style.cssText='font-size:10px;font-weight:800;color:#666;min-width:46px;';l.textContent=lab;
  var v=document.createElement('span');v.style.cssText='font-size:12px;font-weight:800;color:'+_TE+';min-width:48px;';v.textContent=fmt(init);
  var s=document.createElement('input');s.type='range';s.min=min;s.max=max;s.step=step;s.value=init;
  s.style.cssText='width:100px;accent-color:'+_TE+';';
  s.addEventListener('input',function(){v.textContent=fmt(parseFloat(s.value));cb(parseFloat(s.value));});
  w.appendChild(l);w.appendChild(s);w.appendChild(v);return w;}
"""

# ── Core pipeline helpers ─────────────────────────────────────────────────────

def load_deck(src=DECK_PATH, work_dir=WORK_DIR):
    """Extract apkg, return (db, models, existing_guids)."""
    shutil.rmtree(work_dir, ignore_errors=True); os.makedirs(work_dir)
    with zipfile.ZipFile(src) as z: z.extractall(work_dir)
    db = sqlite3.connect(os.path.join(work_dir, 'collection.anki2'))
    models_raw = db.execute("SELECT models FROM col").fetchone()[0]
    models     = json.loads(models_raw)
    existing   = {r[0] for r in db.execute("SELECT guid FROM notes").fetchall()}
    return db, models, existing

def save_deck(db, models, work_dir=WORK_DIR, out_path=DECK_PATH):
    """Write updated models to col, repack apkg."""
    db.execute("UPDATE col SET models=?", (json.dumps(models),))
    db.commit(); db.close()
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in os.listdir(work_dir):
            zf.write(os.path.join(work_dir, f), f)
    print(f"Saved: {out_path}  ({os.path.getsize(out_path)//1024} KB)")

def make_guid(front, back=''):
    import re, hashlib
    return hashlib.md5(re.sub(r'\s+', ' ', (front+back).lower())[:120].encode()).hexdigest()[:10]

def safe_html(t):
    t = re.sub(r'<(\s*[\d_])', r'&lt;\1', t)
    t = re.sub(r'(\d\s*)>(\s*[\d_])', r'\1&gt;\2', t)
    t = re.sub(r'(\d\s*)>(\s*(?:mmHg|mEq|mg|mcg|%|bpm|min|mL|hr|kg|h\b))', r'\1&gt;\2', t)
    return t

def get_main_css(models):
    """Extract CSS from the main blank-fill note type."""
    for mid, m in models.items():
        if 'Mastery' in m.get('name', '') or 'CCRN' in m.get('name', ''):
            return m.get('css', '')
    return ''

def make_chart_template(chart_type, params_json, render_fn, shared_js, chart_css_addon):
    """
    Build qfmt and afmt for a chart note type.
    render_fn: JS string defining function _render(cv, ctrl, P)
    """
    script = f"""<script>(function(){{{shared_js}
{render_fn}
  function init(){{var cv=document.getElementById('physio-canvas');if(!cv)return;
    var P={{}};try{{P=JSON.parse(cv.getAttribute('data-params')||'{{}}');}}catch(e){{}}
    var ctrl=document.getElementById('physio-controls');_render(cv,ctrl,P);}}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){{setTimeout(init,100);}});
  else setTimeout(init,100);}})();</script>"""

    canvas = (f'<div class="chart-canvas-wrap">'
              f'<canvas class="physio" id="physio-canvas" width="620" height="280"'
              f' data-chart="{chart_type}" data-params=\'{params_json}\'></canvas>'
              f'<div class="physio-ctrl" id="physio-controls"></div></div>')

    vari_snippet = f'<script>{VARI_JS}</script>' if VARI_ENABLED else ''

    qfmt = (f'{vari_snippet}<div class="card-wrap {{{{TierClass}}}}"><div class="card-inner">\n'
            f'  <div class="badge">{{{{PhaseBadge}}}}</div>\n'
            f'  <div class="question">{{{{Front}}}}</div>\n'
            f'  {canvas}\n</div></div>\n{script}')

    afmt = (f'{vari_snippet}<div class="card-wrap {{{{TierClass}}}}"><div class="card-inner">\n'
            f'  <div class="badge">{{{{PhaseBadge}}}}</div>\n'
            f'  <div class="question">{{{{Front}}}}</div>\n'
            f'  {canvas}\n</div></div>\n'
            f'<hr id="answer">\n'
            f'<div class="card-inner" style="padding-top:0">\n'
            f'  <div class="answer-label">✓ Answer</div>\n'
            f'  <div class="answer">{{{{Back}}}}</div>\n'
            f'</div>\n{script}')
    return qfmt, afmt

def register_chart_model(models, mid_int, chart_type, did, qfmt, afmt, chart_css):
    """Add a chart note type to the models dict if not already present."""
    mkey = str(mid_int)
    if mkey not in models:
        css = chart_css + (VARI_CSS_ADDON if VARI_ENABLED else '')
        models[mkey] = {
            "id": mkey, "name": f"CCRN Chart: {chart_type}",
            "type": 0, "mod": int(time.time()), "usn": -1,
            "sortf": 0, "did": did,
            "tmpls": [{"name":"Chart Card","ord":0,"qfmt":qfmt,"afmt":afmt,
                       "bqfmt":"","bafmt":"","did":None,"bfont":"","bsize":0}],
            "flds": [
                {"name":"Front",    "ord":0,"sticky":False,"rtl":False,"font":"Arial","size":20},
                {"name":"Back",     "ord":1,"sticky":False,"rtl":False,"font":"Arial","size":20},
                {"name":"TierClass","ord":2,"sticky":False,"rtl":False,"font":"Arial","size":20},
                {"name":"PhaseBadge","ord":3,"sticky":False,"rtl":False,"font":"Arial","size":20},
            ],
            "css": css, "latexPre":"","latexPost":"","vers":[],"tags":[],
        }
    return mkey

def insert_card(db, nid, nid_card, guid, mid, flds, sfld, did, tags, now):
    db.execute(
        "INSERT INTO notes (id,guid,mid,mod,usn,tags,flds,sfld,csum,flags,data) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (nid, guid, int(mid), now, -1, tags, flds, sfld, 0, 0, ''))
    db.execute(
        "INSERT INTO cards (id,nid,did,ord,mod,usn,type,queue,due,ivl,factor,"
        "reps,lapses,left,odue,odid,flags,data) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (nid_card, nid, did, 0, now, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ''))
