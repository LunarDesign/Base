#!/usr/bin/env python3
"""
chunk_NN_charts.py — TEMPLATE for building a new chart chunk
Copy this file, rename it (e.g. chunk31_charts.py), fill in:
  1. CHUNK_NUM
  2. RF dict — one entry per chart type with the _render JS function
  3. CARDS list — 3 cards per chart (L1, L2, L3)
  4. MID_BASE — use 1_800_005_000 for Chunk 31, increment by 5 per chunk
  5. CHART_ORDER — list of chart type keys in RF, for stable model ID assignment
"""
import sys, os, json, sqlite3, zipfile, shutil, hashlib, re, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from build_utils import (
    load_deck, save_deck, make_guid, safe_html, get_main_css,
    make_chart_template, register_chart_model, insert_card,
    SHARED_JS, CHART_CSS_ADDON, DID
)
from card_validator import CardValidator

# ── Configuration ─────────────────────────────────────────────────────────────
# Workflow: write one RF function + 3 cards → run → fix failures → repeat
# Do NOT pre-validate cards mentally — the validator is the quality gate.
# Badge tier (T1/T2/T3) MUST match live Anki subdeck: check mcp__anki__list_decks first.
DECK_PATH   = 'CCRN_PCCN_Mastery_v7_final_NN.apkg'   # ← previous chunk output
OUT_PATH    = 'CCRN_PCCN_Mastery_v7_final_MM.apkg'   # ← this chunk output
WORK_DIR    = os.path.join(tempfile.gettempdir(), 'cNN')
CHUNK_NUM   = NN                       # ← change for each chunk; set VARI_ENABLED=True in build_utils.py to activate context variation
MID_BASE    = 1_800_005_NNN            # ← Chunk 33 = 1_800_005_010, increment by 5
CHART_ORDER = ['chart_type_1',         # ← list chart keys in same order as RF dict
               'chart_type_2',
               'chart_type_3',
               'chart_type_4',
               'chart_type_5']

# ── Render Functions (one per chart) ─────────────────────────────────────────
# Each RF entry is a JS string defining:
#   function _render(cv, ctrl, P) { ... }
# where:
#   cv    = canvas element (width=620, height=280)
#   ctrl  = controls div element
#   P     = parsed params object from data-params attribute
# Available helpers: _cl _gd _ax _lb _rl _dot _crv _mkB _mkS
# Available colors:  _TE _RE _GN _AM _OR _PU _PI _GR _AX _LB

RF = {}

RF['chart_type_1'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;
    var mx=58, my=18, pw=W-mx-14, ph=H-my-50;

    // Example: simple curve chart
    // X domain: 0-100, Y domain: 0-200
    var xD=100, yD=200;

    function draw() {
        _cl(ctx, W, H);
        _gd(ctx, mx, my, pw, ph, 10, xD, 20, yD);
        _ax(ctx, mx, my, pw, ph);

        // Axis labels
        ctx.textAlign='center';
        for (var x=0; x<=xD; x+=10)
            _lb(ctx, x, mx+(x/xD)*pw, my+ph+15, null, 10);
        ctx.textAlign='right';
        for (var y=0; y<=yD; y+=20)
            _lb(ctx, y, mx-6, my+ph-(y/yD)*ph+4, null, 10, 'right');
        _lb(ctx, 'X Axis Label', mx+pw/2, H-5, null, 11);
        _rl(ctx, 'Y Axis Label', 14, my+ph/2);

        // Draw a curve
        _crv(ctx,
            function(x) { return x * 2; },  // y = f(x)
            0, xD,                           // x range
            mx, my, pw, ph, xD, yD,
            _TE, 2.5);                       // color, line width
    }

    draw();

    // Controls
    if (ctrl) {
        ctrl.innerHTML = '';
        var row = document.createElement('div');
        row.style.cssText = 'display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;align-items:center;';
        // Example button
        var b = _mkB('Toggle', _TE, false, function(on) {
            b.style.background = on ? _TE+'22' : 'transparent';
            b.style.color = on ? _TE : '#555';
            b._on = on;
            draw();
        });
        row.appendChild(b);
        // Example slider
        row.appendChild(_mkS('Value', '0', '100', '1', P.val||50,
            function(v) { return v.toFixed(0); },
            function(v) { P.val = v; draw(); }));
        ctrl.appendChild(row);
    }
}
"""

# Add more RF entries for each chart type...
RF['chart_type_2'] = r"""
function _render(cv, ctrl, P) {
    var W=cv.width, H=cv.height, ctx=cv.getContext('2d');
    if (!ctx) return;
    // TODO: implement chart_type_2
    _cl(ctx, W, H);
    ctx.fillStyle='#555'; ctx.font='14px sans-serif'; ctx.textAlign='center';
    ctx.fillText('chart_type_2 — not yet implemented', W/2, H/2);
}
"""

# ── Card Definitions ──────────────────────────────────────────────────────────
# Tuple: (front, back, tier, badge, did, chart_type, params_json, level_tag)
#
# tier:      'tier-review' | 'tier-high' | 'tier-moderate' | 'tier-critical'
# level_tag: 'chart-l1'   | 'chart-l2'  | 'chart-l3'
# did:       use DID['hemodynamics'] etc. from build_utils
#
# Card format rules:
#   - Front MUST contain _______
#   - Back MUST contain → CCRN KEY: and → MASTERY NOTE:
#   - Use | on new lines for multi-point answers
#   - Keep front <580 chars, context before blank <400 chars

CARDS = [
    # ═══ chart_type_1 ════════════════════════════════════════════════════
    # L1 — Recognition
    (
        "On the [chart name], _______ represents [concept]. "
        "This is clinically important because _______.",

        "ANSWER to first blank — explanation.\n"
        "| Answer to second blank — clinical implication.\n"
        "→ CCRN KEY: The key clinical takeaway in 1-2 sentences.\n"
        "→ MASTERY NOTE: Deeper mechanism or edge case the CCRN exam tests.",

        'tier-review',
        'Ph1 · 🔴 T1 · Cardiovascular — Hemodynamics & Shock',
        DID['hemodynamics'],
        'chart_type_1',
        '{}',
        'chart-l1'
    ),
    # L2 — Mechanism
    (
        "When [condition changes], the chart shows _______. "
        "This occurs because _______.",

        "ANSWER — mechanism explanation.\n"
        "| Clinical relevance.\n"
        "→ CCRN KEY: Mechanism-level takeaway.\n"
        "→ MASTERY NOTE: Nuance or contraindication.",

        'tier-high',
        'Ph1 · 🔴 T1 · Cardiovascular — Hemodynamics & Shock',
        DID['hemodynamics'],
        'chart_type_1',
        '{"param": 0}',
        'chart-l2'
    ),
    # L3 — Clinical application
    (
        "Clinical scenario with specific values. "
        "The chart shows _______. "
        "Correct intervention: _______, not _______, because _______.",

        "ANSWER — clinical decision with rationale.\n"
        "| Why the wrong choice fails.\n"
        "→ CCRN KEY: Clinical decision rule.\n"
        "→ MASTERY NOTE: Nursing assessment that identifies this state.",

        'tier-critical',
        'Ph1 · 🔴 T1 · Cardiovascular — Hemodynamics & Shock',
        DID['hemodynamics'],
        'chart_type_1',
        '{"patient": {"x": 0, "y": 0}}',
        'chart-l3'
    ),
    # Add more cards for chart_type_2, etc.
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
        print(f"  {'✅' if ok else '❌'} [{ctype}·{ltag}]{w_str}  {front[:65]}")
        if not ok:
            for iss in issues: print(f"      ✗ {iss}")

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
        print(f"  ✓ [{ctype}·{ltag}]  {front[:65]}")

    save_deck(db, models, WORK_DIR, OUT_PATH)

    db2 = sqlite3.connect(os.path.join(WORK_DIR, 'collection.anki2'))
    total = db2.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    db2.close()

    print(f"\n{'='*65}")
    print(f"  Chunk {CHUNK_NUM}: {added} cards added | Total deck: {total} cards")
    print(f"{'='*65}")


if __name__ == '__main__':
    main()
