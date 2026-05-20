# CCRN/PCCN Mastery Deck — Claude Code Handoff

## Quick Start

1. Open terminal in this folder: `C:\Users\lunar\Desktop\Cards\CCRN_Cards_Project\Cards`
2. Start Claude Code: `claude`
3. First message:

```
Read PROJECT_CONTEXT.md and CHART_BACKLOG.md. The deck file is
CCRN_PCCN_Mastery_v7_final_32.apkg. Chunks 28-32 are complete (86
chart cards added, deck at 1,080 cards). Build Chunk 33 next
using the priority order in CHART_BACKLOG.md. Use chunk_template.py
as your starting point and build_utils.py for shared helpers.
Validate all cards with card_validator.py before inserting.
```

## File Overview

| File | Purpose |
|---|---|
| `CCRN_PCCN_Mastery_v7_final.apkg` | The Anki deck — source of truth |
| `card_validator.py` | Quality gate (F1-F7 hard failures, W8 soft warning) |
| `build_utils.py` | Shared helpers: load_deck, save_deck, make_chart_template, DID registry |
| `chunk_template.py` | Template for building Chunk 31+ |
| `PROJECT_CONTEXT.md` | Full architecture reference |
| `CHART_BACKLOG.md` | All 57 remaining charts organized by phase |
| `README_CLAUDE_CODE.md` | This file |

## Per-Chunk Workflow

```
chunk_NN_charts.py
  ↓ imports card_validator.py, build_utils.py
  ↓ loads CCRN_PCCN_Mastery_v7_final.apkg
  ↓ defines RF{} dict (render functions for each chart)
  ↓ defines CARDS[] list (front, back, tier, badge, did, chart_type, params, level)
  ↓ validates all cards → F1-F7 must pass
  ↓ registers chart note types in models
  ↓ inserts notes + cards
  ↓ saves updated CCRN_PCCN_Mastery_v7_final.apkg
```

## Model ID Allocation

```
Chunks 28-30 used: 1_800_002_000 – 1_800_004_999
Chunk 31 used:     1_800_005_000 – 1_800_005_004 (5 chart types)
Chunk 32:          1_800_005_005 – 1_800_005_009  ✓ complete
Chunk 33:          1_800_005_010 – 1_800_005_014
... increment by 5 per chunk
```

## Chart Card Rules (critical)

- **data-* attributes** on canvas — NOT `{{FieldName}}` inside JS strings
- **One note type per chart type** (different render function = different model ID)
- **Front has exactly one `_______` blank** for active recall
- **Back structure:** answer pipes `|` then `→ CCRN KEY:` then `→ MASTERY NOTE:`
- **L1** = tier-review, L2 = tier-high, L3 = tier-critical
- **Canvas size:** width=620, height=280, `setTimeout(init, 100)`
- **No {{FrontSide}}** in afmt — chart renders independently on back

## Testing After Each Chunk

1. Import updated .apkg into Anki Desktop (replace existing)
2. Study 1–2 cards from the new chunk to verify canvas renders
3. Check AnkiWeb sync (confirm JavaScript executes through browser)
4. Confirm controls (buttons/sliders) are interactive

