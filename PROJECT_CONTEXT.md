# CCRN/PCCN Mastery Deck — Claude Code Project Context

## Current State (as of Chunk 56)
- **Deck file:** `CCRN_PCCN_Mastery_v7_final_56.apkg`
- **Total cards:** 1,443
- **Total subdecks:** 47
- **Chunks complete:** 1–56
- **Chart chunks complete:** 28–56 (29 chart chunks, 795 chart cards added)
- **All DID registry entries exhausted** (100–106, 110–117, 120–123, 130–133, 140–141, 150–152, 160, 170–181, 190–193, 195)

---

## Historical State (Chunk 32 Snapshot)
*State as of 2026-05-13, before Claude Code handoff and chunks 33–56.*
- **Deck file:** `CCRN_PCCN_Mastery_v7_final_32.apkg`
- **Total cards:** 1,080
- **Total subdecks:** 47
- **Chunks complete:** 1–32
- **Chart chunks complete:** 28–32 (86 chart cards added)

---

## Deck Architecture

### Main Note Type
- **Name:** CCRN Mastery v6
- **Model ID (mid):** `1800000010`
- **Fields:** Front, Back, TierClass, PhaseBadge
- **Format:** ~92% blank-fill (`_______`)
- **Answers use labeled prefixes:**
  - `→ CCRN KEY:` (required)
  - `→ MASTERY NOTE:` (required)
  - `→ WHY IT MATTERS:` (reference cards)
- **Pipe separator** `|` for multi-point answers (pre-wrap rendered)

### CSS Tier System (5px left border)
| TierClass | Color | Hex | Use |
|---|---|---|---|
| `tier-critical` | Red | `#ef5350` | Life-threatening, <5 min decisions |
| `tier-high` | Orange | `#ff7043` | Urgent clinical decisions |
| `tier-moderate` | Amber | `#ffca28` | Important assessment/monitoring |
| `tier-review` | Teal | `#26c6da` | Foundational knowledge |

### PhaseBadge Format
`Ph1 · 🔴 T1 · Cardiovascular — [Subdeck Name]`
Tier emoji: T1=🔴 T2=🟠 T3=🟡 T4=🟢

**Observed format variants (both accepted):**
- Chunks 28–51: `'Ph{N} · 🟡 T{N} · {Category} — {Subdeck}'` (` · ` before emoji)
- Chunks 52–56: `'Ph{N} 🟡 T{N} · {Category} — {Subdeck}'` (no ` · ` before emoji)

### Card Format Rules (enforced by CardValidator)
- **F1:** Front MUST contain `_______`
- **F2:** Back must be ≥60 chars
- **F3:** No bullet dumps (>8 pipes without `→`)
- **F4:** Back must contain `→` (U+2192 literal — not `->`)
- **F5:** Don't repeat same answer for multiple blanks
- **F6:** Context before blank must be <400 chars
- **F7:** Front must be <580 chars
- **F9:** TierClass must be a canonical CSS class — `tier-review`/`tier-high`/`tier-moderate`/`tier-critical` (pass as optional 5th arg: `validate(nid, front, back, badge, tier)`)
- **W8:** Back should contain `→ CCRN KEY:` + `→ MASTERY NOTE:` (soft warning only)

---

## Chart Card Architecture

### Overview
Interactive HTML5 Canvas cards. Each chart type has its **own note type**
(separate model ID) with the chart JavaScript hardcoded in the template.
Chart type and initial parameters are passed via HTML `data-*` attributes
on the canvas element — NOT via `{{FieldName}}` inside JS strings.

### Chart Note Type Fields
Same 4 fields as main note type: **Front, Back, TierClass, PhaseBadge**

### Chart Note Type IDs Used
| Range | Used for |
|---|---|
| `1800002000`–`1800002007` | Chunk 28 (8 chart types) |
| `1800003000`–`1800003004` | Chunk 29 (5 chart types) |
| `1800004000`–`1800004004` | Chunk 30 (5 chart types) |
| `1800005000`–`1800005004` | Chunk 31 (5 chart types) |
| `1800005005`–`1800005009` | Chunk 32 (5 chart types) |
| `1800005010`–`1800005129` | Chunks 33–56 (5 chart types each, MID_BASE increments by 5 per chunk) |
| **`1800005130`+** | **Next available — use for Chunk 57+** |

### Chart Template Pattern
```html
<canvas class="physio" id="physio-canvas" width="620" height="280"
  data-chart="CHART_TYPE_NAME"
  data-params='{"key": value}'></canvas>
```
```javascript
// JS reads from data attributes (avoids HTML entity encoding issues):
var P = JSON.parse(canvas.getAttribute('data-params') || '{}');
```

### Progressive L1/L2/L3 System
- **L1** `chart-l1` → `tier-review` — Recognition: identify what the chart shows
- **L2** `chart-l2` → `tier-high` — Mechanism: why the chart looks that way
- **L3** `chart-l3` → `tier-critical` — Clinical application: what do you DO

Each chart produces exactly 3 cards (occasionally 4 for rich concepts).
All 3 cards use the SAME chart note type — only the question changes.

**D2 fixed (2026-05-16):** Chunks 47–54 had arbitrary tier assignments across all levels — 89 of 120 notes were wrong. Patched directly in `_56.apkg` via `patch_d2.py`; source files corrected via `fix_d2_sources.py`. All 150 notes in chunks 47–56 now pass tier/ltag consistency check.

### Tags
`ccrn-pccn-v6 chunk-NN chart-l1` (or chart-l2, chart-l3)

### Context Variation (VARI)
`VARI_ENABLED = True` in `build_utils.py`. A ~10-line JS snippet randomizes font-family (system-ui / Georgia) and font-size (14px / 15px) for `.question`/`.answer` text only. Canvas, badges, colors, and clinical content are never affected.

---

## All 47 Subdeck DIDs

### Ph1 Cardiovascular
| DID | Subdeck |
|---|---|
| 1800000100 | Hemodynamics & Shock |
| 1800000101 | ACS & Coronary |
| 1800000102 | Heart Failure & Devices |
| 1800000103 | Arrhythmias & Conduction |
| 1800000104 | Aortic & Vascular |
| 1800000105 | Post-Cardiac Surgery |
| 1800000106 | ECMO & Mechanical Support |

### Ph2 Respiratory
| DID | Subdeck |
|---|---|
| 1800000110 | ARDS & Lung Protection |
| 1800000111 | Mechanical Ventilation |
| 1800000112 | Failure & Weaning |
| 1800000114 | Obstructive Disease |
| 1800000115 | Acid-Base Interpretation |
| 1800000116 | Pneumonia & Lung Infection |
| 1800000117 | Pulmonary Embolism |

### Ph3 Multisystem
| DID | Subdeck |
|---|---|
| 1800000120 | Sepsis & Septic Shock |
| 1800000121 | MODS & Trauma |
| 1800000122 | Burns & Toxicology |
| 1800000123 | Deterioration & Escalation |

### Ph4 Neurology
| DID | Subdeck |
|---|---|
| 1800000130 | Stroke & TBI |
| 1800000131 | Seizures & Status Epilepticus |
| 1800000132 | ICP & Neuro Crisis |
| 1800000133 | Delirium & Behavioral |

### Ph5 Endocrine/Renal/GI/Heme
| DID | Subdeck |
|---|---|
| 1800000140 | DKA, HHS & Metabolic Crisis |
| 1800000141 | Thyroid, Adrenal & Other |
| 1800000150 | AKI, CRRT & Electrolytes |
| 1800000151 | Critical GI & Hepatic |
| 1800000152 | Hematology & Coagulation |

### Ph6 Professional Practice
| DID | Subdeck |
|---|---|
| 1800000160 | Professional Practice & Ethics |

### Ph7 Pharmacology
| DID | Subdeck |
|---|---|
| 1800000170 | Vasopressors & Inotropes |
| 1800000171 | Antiarrhythmics |
| 1800000172 | Sedation & Analgesia |
| 1800000173 | NMBAs |
| 1800000174 | Vasoactive & Antihypertensives |
| 1800000175 | Anticoagulants & Reversal |
| 1800000176 | Diuretics & Osmotherapy |
| 1800000177 | Targeted Agents |
| 1800000178 | Mechanism Groups |
| 1800000179 | Drug Comparisons |
| 1800000180 | Patient Mental Models |
| 1800000181 | Monitoring Thresholds |

### Ph8 Reference
| DID | Subdeck |
|---|---|
| 1800000190 | Hemodynamic Parameters |
| 1800000191 | Acid-Base Interpretation |
| 1800000192 | Lab Values & Monitoring |
| 1800000193 | Vent Settings & Targets |
| 1800000195 | Medical Terminology & Acronyms |

---

## Chunk History

| Chunk | Content | Cards |
|---|---|---|
| 01–23 | Clinical content across all phases | 591 |
| 24 | Phase 1 sequence cards | 31 |
| 25–27 | Grading scales, comparison tables | 26 |
| **28** | Chart cards: Frank-Starling, O2-Hgb, Hemodynamic 2×2, Acid-Base Map, Vent Waveforms, Vasoactive Drugs, PV Loop, DO2 Components | **24** |
| **29** | Chart cards: Troponin curves, IABP waveform, Starling forces, ECMO VV vs VA, Conduction pathway | **15** |
| **30** | Chart cards: PV compliance, Flow-volume loop, V/Q shunt, PE severity, Auto-PEEP | **15** |
| **31** | Chart cards: PA catheter waveform, MAP isolines, Cardiac cycle, Aortic dissection, Shock progression | **15** |
| **32** | Chart cards: Cerebral autoregulation, ICP waveforms, Monro-Kellie, CPP interactive, RASS scale | **17** |
| **33** | Chart cards: vasopressor_dose_response (Ph7), action_potential + vaughan_williams (Ph7), anticoag_cascade (Ph7), analgesic_ladder (Ph7) | **18** |
| **34** | Chart cards: lactate_clearance, do2_vo2_curve, hemorrhagic_shock (Ph3 Sepsis), damage_control, parkland_formula (Ph3 Burns/Trauma) | **15** |
| **35** | Chart cards: dka_severity, dka_hhs_compare, anion_gap_delta (Ph5 DKA/HHS), thyroid_storm, adrenal_crisis (Ph5 Thyroid/Adrenal) | **15** |
| **36** | Chart cards: aki_stages, crrt_modes, crrt_dose, hyperkalemia_ecg, prerenal_intrinsic (Ph5 Renal/CRRT) | **15** |
| **37** | Chart cards: gi_bleed_severity, hepatic_enceph, meld_score, pancreatitis_bisap, abdominal_compartment (Ph5 GI/Hepatic) | **15** |
| **38** | Chart cards: dic_score, blood_products, massive_transfusion, hit_4t, transfusion_reactions (Ph5 Hematology) | **15** |
| **39** | Chart cards: synergy_model, ethics_principles, palliative_comfort, qi_safety, communication_sbar (Ph6 Professional Practice) | **15** |
| **40** | Chart cards: vasopressor_receptors, shock_vasopressor, inotrope_comparison, pressor_titration, vasopressor_weaning (Ph7 Vasopressors) | **15** |
| **41** | Chart cards: vaughan_williams (extended), antiarrhythmic_selection, amiodarone_toxicity, adenosine_svt, qt_prolongation (Ph7 Antiarrhythmics) | **15** |
| **42** | Chart cards: sedation_scales, analgesic_comparison, propofol_infusion, dexmedetomidine, cpot_assessment (Ph7 Sedation & Analgesia) | **15** |
| **43** | Chart cards: nmba_comparison, train_of_four, sux_rsi, nmba_reversal, icu_paralysis (Ph7 NMBAs) | **15** |
| **44** | Chart cards: antihtn_comparison, hypertensive_crisis, nitroprusside_toxicity, antihtn_by_scenario, bp_titration_targets (Ph7 Vasoactive/Antihypertensives) | **15** |
| **45** | Chart cards: anticoagulant_comparison, heparin_protocol, warfarin_management, anticoagulant_reversal, vte_prophylaxis (Ph7 Anticoagulants) | **15** |
| **46** | Chart cards: diuretic_comparison, loop_diuretic_protocol, diuretic_electrolytes, acute_decompensated_hf, mannitol_hypertonic (Ph7 Diuretics) | **15** |
| **47** | Chart cards: hemo_parameters, shock_hemodynamics, cardiac_output_calcs, pa_catheter, fluid_responsiveness (Ph8 Hemodynamic Parameters) | **15** |
| **48** | Chart cards: acid_base_map, compensation_formulas, anion_gap, blood_gas_steps, clinical_acid_base (Ph8 Acid-Base) | **15** |
| **49** | Chart cards: critical_labs, electrolyte_abnormalities, renal_labs, coagulation_labs, cardiac_markers (Ph8 Lab Values) | **15** |
| **50** | Chart cards: vent_modes, lung_protective, weaning_sbt, vent_alarms, niv_hfnc (Ph8 Vent Settings) | **15** |
| **51** | Chart cards: oxygenation_formulas, clinical_scoring, ards_berlin, sepsis_definitions, icu_syndromes (Ph8 Terminology) | **15** |
| **52** | Chart cards: antidote_pairs, pulmonary_vasodilators, thrombolytics, corticosteroids_icu, vasopressin_methylene (Ph7 Ext — Targeted Agents) | **15** |
| **53** | Chart cards: receptor_map, antibiotic_class, coagulation_targets, renal_dose_adjust, cyp450_interactions (Ph7 Ext — Mechanism Groups) | **15** |
| **54** | Chart cards: sedation_compare, antifungal_compare, antibiotic_spectrum, pressor_selection, beta_blocker_compare (Ph7 Ext — Drug Comparisons) | **15** |
| **55** | Chart cards: aki_drug_adjust, chf_pharmacology, sepsis_patient_pharm, liver_failure_drugs, elderly_frail_icu (Ph7 Ext — Patient Models) | **15** |
| **56** | Chart cards: tdm_targets, nephrotox_monitor, pressor_endpoints, sedation_endpoints, anticoag_monitoring (Ph7 Ext — Monitoring Thresholds) | **15** |

---

## Build Pipeline (per chunk)

```python
# Standard chunk build pattern (current — as of chunk 33+):
from build_utils import *
from card_validator import CardValidator

# 1. Load deck
db, models, existing_guids = load_deck('CCRN_PCCN_Mastery_v7_final_NN.apkg')
main_css = get_main_css(models)
CHART_CSS = main_css + CHART_CSS_ADDON

# 2. Define render function (JS string)
RF = {}
RF['my_chart_type'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if(!ctx) return;
    // ... draw chart using _cl, _gd, _ax, _lb, _rl, _dot, _crv, _mkB, _mkS helpers
}
"""

# 3. Define cards — canonical tuple format:
#   (front, back, tier_str, badge_str, did_int, chart_type, params_json, ltag)
#   tier_str:    CSS class — 'tier-review' / 'tier-high' / 'tier-critical'
#   params_json: valid JSON string — use '{}' if no params
#   ltag:        'chart-l1' / 'chart-l2' / 'chart-l3'
CARDS = [
    ("Front with _______ blank.", "→ CCRN KEY: answer.\n→ MASTERY NOTE: context.",
     'tier-review', 'Ph1 · 🔴 T1 · Cardiovascular — Hemodynamics & Shock',
     DID['hemodynamics'], 'my_chart_type', '{}', 'chart-l1'),
    # ... L2 card with 'tier-high' / 'chart-l2'
    # ... L3 card with 'tier-critical' / 'chart-l3'
]

# 4. Validate — pass tier as 5th arg for F9 check
validator = CardValidator()
now = int(time.time())
nid_base = now * 1000
mid_base = 1_800_005_130  # next available after chunk 56; increment by 5 per chart type

for i, card in enumerate(CARDS):
    front, back, tier, badge, did, ctype, pj, ltag = card
    issues = validator.validate(f'cNN_{i}', front, back, badge, tier)
    if issues:
        print(f'  FAIL card {i}: {issues}')
        continue
    # insert card...

# 5. Register model + insert
qfmt, afmt = make_chart_template(ctype, pj, RF[ctype], SHARED_JS, CHART_CSS)
mkey = register_chart_model(models, mid_base+chart_idx, ctype, did, qfmt, afmt, CHART_CSS)
insert_card(db, nid, nid+1, guid, mkey, flds, sfld, did, tags, now)

# 6. Save
save_deck(db, models, out_path='CCRN_PCCN_Mastery_v7_final_NN.apkg')
```

---

## Shared JavaScript Helpers Reference

All helpers use short names to reduce template size:

| Helper | Signature | Purpose |
|---|---|---|
| `_cl(c,W,H)` | ctx, width, height | Clear canvas to black |
| `_gd(c,mx,my,pw,ph,xs,xD,ys,yD)` | — | Draw grid |
| `_ax(c,mx,my,pw,ph)` | — | Draw L-shaped axes |
| `_lb(c,t,x,y,col,sz,al)` | — | Draw label text |
| `_rl(c,t,cx,cy)` | — | Rotated y-axis label |
| `_dot(c,x,y,r,col)` | — | Filled circle |
| `_crv(c,fn,x0,x1,mx,my,pw,ph,xD,yD,col,lw)` | — | Smooth curve from function |
| `_mkB(lbl,col,on,cb)` | label, color, initial state, callback | Toggle button |
| `_mkS(lab,min,max,step,init,fmt,cb)` | label, range params, format fn, callback | Slider |

### Color palette
```
_TE = '#29b6f6'  (sky blue  — tier-review)
_RE = '#ef5350'  (red       — tier-critical, patient dots, warnings)
_GN = '#4caf50'  (green     — positive, normal, correct)
_AM = '#ffca28'  (amber     — tier-moderate, caution)
_OR = '#ff7043'  (orange    — tier-high)
_PU = '#ce93d8'  (purple    — secondary)
_PI = '#f06292'  (pink      — HR, secondary markers)
_GR = '#2a2a2a'  (dark grey — grid)
_AX = '#666666'  (grey      — axes)
_LB = '#888888'  (light grey — labels)
```

---

## Learner Context

**Name:** Mowzee Jones, RN  
**Unit:** Duke Health 7700 — Cardiology Step-Down  
**Goal:** CCRN/PCCN certification  
**Background:** Former IT project manager (Fortune 500)  

**Language calibration by level:**
- **L1:** New grad RN on cardiology step-down — no assumed prior cardiology depth
- **L2:** 3–6 months clinical experience — pattern recognition building
- **L3:** CCRN preparation — full clinical reasoning chains expected
