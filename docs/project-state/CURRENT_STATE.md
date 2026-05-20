# Current Project State

> **Future session: read this file first.** It is the authoritative one-page briefing.

---

## What This Project Is

Anki card simplification pass for the **CCRN⁄PCCN Mastery v6** deck. Every card's Back field must be ≤ 300 visible characters. Cards over the limit are rewritten (if compressible) or split into 2–4 daughter cards (if too dense). Source accuracy is cross-checked against clinical reference PDFs before any change is made. No card is edited without explicit user approval of a classification table first.

---

## Current Phase

| Phase | Status |
|---|---|
| Ph3 Sepsis (88 notes) | ✅ Complete — `audit-results/ph3_sepsis_simplify_audit.tsv` |
| Ph3 MODS & Trauma (30 notes + Compartment Syndrome SOURCE-UPDATED SPLIT) | ✅ Complete — `audit-results/ph3_mods_burns_simplify_audit.tsv` |
| Ph3 Burns & Toxicology (12 notes) | ✅ Complete — same TSV as above |
| **Ph4 Neurology** | ⏳ **NOT STARTED — this is next** |
| Ph5–Ph8 and all subsequent subdecks | Not started |

---

## Ph4 Neurology — What's Known

- Subdecks: ICP & Neuro Crisis, Seizures & Status Epilepticus, Stroke & TBI
- Deck badge: **🟠 T2** — confirm exact deck name string via `mcp__anki__list_decks` before writing any PhaseBadge on daughter cards
- No notes have been fetched, counted, or classified yet

---

## Active Rules (do not change without user approval)

1. **Back-only targeting.** 300 visible-character limit. Never touch Front, TierClass, PhaseBadge, or model name.
2. **Chart model exemption.** Any card whose `modelName` starts with `"CCRN Chart:"` → NO ACTION, regardless of Back length.
3. **Approval gate.** Present classification table; wait for explicit user approval before executing any edits.
4. **Source citation required.** Every source-based update must cite file name + page + reason it matters for CCRN/PCCN.
5. **No silent clinical updates.** Label every source change explicitly as SOURCE-UPDATED REWRITE or SOURCE-UPDATED SPLIT.
6. **No edits to Back ≤300 cards** unless a source issue is found and separately approved.

### Character counting method (7 steps)

```python
import re, html
def vis(raw):
    d = html.unescape(raw)
    s = re.sub(r'<[^>]+>', ' ', d)
    s = s.replace('\n', ' ').replace('\t', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return len(s)
```

### Classification categories

| Category | Condition |
|---|---|
| NO ACTION | Back ≤ 300 chars, no source issue |
| SAFE REWRITE | Back > 300; compressible losslessly to ≤ 300 |
| SAFE SPLIT | Back > 300; too dense to compress safely |
| FLAG FOR REVIEW | Back > 300; ambiguous/nuanced content |
| FLAG FOR SOURCE CHECK | Back > 300; high-risk clinical claim needs source check |
| SOURCE-UPDATED REWRITE | Back > 300; source shows inaccuracy; fits ≤ 300 after update |
| SOURCE-UPDATED SPLIT | Back > 300; source update needed + too dense for one card |
| SOURCE ISSUE IN ≤300 CARD | Back ≤ 300; source reveals significant problem — flag only, do not edit |

---

## Process Protocol (locked — permanent)

### Rule 4 — Persistent verify script
- Script: `scripts/anki/daughter_verify.py`
- Before any split batch: clear DAUGHTERS dict, populate, run. Must print "ALL N daughters OK" before calling `add_notes`.

### Rule 5 — TierClass guard
- Script validates tier strings against `{tier-critical, tier-high, tier-low}`.
- Visual confirmation in output table before add_notes.
- **Key risk:** `tier-high` parents must not have daughters defaulting to `tier-critical`.

### Rule 8 — Single `notes_info` call
- Fetch ALL parent fields (Front, Back, TierClass, PhaseBadge, tags) in ONE call for ALL parents in the batch.

### Rule 9 — Spot-check before suspend
- After `add_notes` returns NIDs: verify one daughter per parent via `notes_info`.
- Only after spot-check passes: call `card_management` suspend on the parent.

---

## Scripts to Use

| Script | Purpose |
|---|---|
| `scripts/anki/daughter_verify.py` | Pre-add_notes batch verification (char count + TierClass) |
| `scripts/anki/count_backs.py` | Count visible Back chars for a list of NIDs |
| `scripts/anki/count_large_cards.py` | Find all cards over 300 chars in a deck |
| `scripts/anki/verify_rewrites.py` | Verify rewritten Backs after update_note_fields |

> ⚠️ Migration note: A prior version of `docs/handoffs/CURRENT_SESSION_HANDOFF.md` references these scripts at the root path (e.g., `daughter_verify.py`). The canonical paths are now `scripts/anki/daughter_verify.py` etc.

---

## Audit Files

| File | Contents |
|---|---|
| `audit-results/ph3_sepsis_simplify_audit.tsv` | Ph3 Sepsis — 88 notes |
| `audit-results/ph3_mods_burns_simplify_audit.tsv` | Ph3 MODS & Trauma + Burns — 42 notes + all daughters |

---

## MCP Dependencies

AnkiConnect must be running (Anki desktop open) before any MCP tool calls.

Required tools (load via ToolSearch at session start):
```
mcp__anki__notes_info
mcp__anki__update_note_fields
mcp__anki__add_notes
mcp__anki__card_management
mcp__anki__sync
mcp__anki__find_notes
mcp__anki__list_decks
```

---

## Source Authority Hierarchy

1. **AACN PCCN/CCRN exam handbooks** — exam scope and blueprint alignment (pre-extracted: `sourcedocs/extracted_ccrn_handbook.txt`)
2. **Study PDFs** — Juarez, Burns/Delgado, Colson Ridge (local only — see `docs/project-state/SOURCE_DOCUMENT_MANIFEST.md`)
3. **Existing card Back field** — preserve when accurate
4. **Claude's training knowledge** — reasoning support only; never a source of truth

---

## Key NID Reference — Cards Already Processed (do not re-process)

| NIDs | Status | Notes |
|---|---|---|
| 1778381918063–064 | Suspended | Primary Survey → daughters 594/595/596 |
| 1778381918066–067 | Suspended | Hemorrhagic Shock → daughters 597/598/599 |
| 1778381918069–070 | Suspended | Compartment Syndrome SOURCE-UPDATED → daughters 582/583/584 |
| 1778381918072–073 | Suspended | Rhabdomyolysis (tier-high) → daughters 600/601/602 |
| 1778436692068–069 | Suspended | DCR → daughters 603/604 |
| 1778436692071–072 | Suspended | DCR synthesis → daughters 605/606/607 |
| 1778437755998–999 | Suspended | Hemorrhagic Shock navigation → daughters 608/609 |
| 1779278789594–609 | Active daughters | MODS/Trauma batch (16 daughters) |
| 1779280281582–584 | Active daughters | Compartment Syndrome SOURCE-UPDATED batch (3 daughters) |
