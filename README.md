# CCRN⁄PCCN Mastery v6 — Deck Simplification Project

This repository tracks an ongoing Anki card simplification project for the CCRN⁄PCCN Mastery v6 deck. Every card's Back field is being reviewed and compressed to ≤ 300 visible characters. Cards that are too dense to compress safely are split into 2–4 focused daughter cards. All changes are cross-checked against clinical source documents and require explicit user approval before execution.

---

## Claude Code Session Continuity

### Start here

Every new Claude Code session should begin by reading these files in order:

```
1. docs/project-state/CURRENT_STATE.md       ← what phase, what rules, what's done
2. docs/handoffs/CURRENT_SESSION_HANDOFF.md  ← full detail of the last session
3. docs/project-state/PROTECTED_SURFACES.md ← what must never be changed
4. docs/project-state/NEXT_ACTIONS.md        ← exact ordered action list
5. docs/handoffs/HANDOFF_INDEX.md            ← session history log
```

Do not begin any Anki work until you have read all five.

### What not to touch

- **Front field** of any Anki note — never
- **TierClass** or **PhaseBadge** fields — copy verbatim from parent when creating daughters; never edit on existing cards
- **Chart model cards** (modelName starts with `"CCRN Chart:"`) — always NO ACTION regardless of Back length
- **Any card with Back ≤ 300 visible chars** — NO ACTION unless a source issue is separately approved
- **Source PDFs/EPUBs** in `sourcedocs/` — local only, never commit; see `docs/project-state/SOURCE_DOCUMENT_MANIFEST.md`
- **Completed audit TSVs** in `audit-results/` — read-only records
- **The Active Rules section** of the plan file — do not change without explicit user approval

### How to resume after reading the files

1. Load Anki MCP tools via ToolSearch
2. Confirm Anki desktop is open and AnkiConnect is responding
3. Follow `docs/project-state/NEXT_ACTIONS.md` step by step
4. Present a classification table to the user; wait for approval before executing any edits

### How to close a session and update GitHub

At the end of each session:

```bash
# 1. Update these files to reflect what was done:
#    - docs/project-state/CURRENT_STATE.md
#    - docs/project-state/NEXT_ACTIONS.md
#    - docs/handoffs/HANDOFF_INDEX.md  (add new row)
#    - docs/handoffs/CURRENT_SESSION_HANDOFF.md  (replace with new handoff)
#    - audit-results/  (add or update TSV for the phase just completed)

# 2. Commit and push
git add docs/ audit-results/
git commit -m "Session close: <one-line summary of what was done>"
git push origin main
```

### How to update audit files

Each completed subdeck gets one TSV in `audit-results/`. Name pattern:
```
ph<N>_<subdeck-name>_simplify_audit.tsv
```

TSV columns:
```
NID | Action | Front (truncated) | Old visible Back count | New visible Back count |
Prior 250-rule action | New 300-rule action | Changed by 300-rule? | Clinical risk? |
Flag type | Flag reason | AACN relevance | Notes
```

---

## Repository Structure

```
docs/
  handoffs/
    CURRENT_SESSION_HANDOFF.md  ← full detail of last session
    HANDOFF_INDEX.md            ← session history log
  audits/
    chunks-29-56-consistency-rule-adherence-audit.md
  project-state/
    CURRENT_STATE.md            ← READ FIRST
    NEXT_ACTIONS.md             ← ordered action list
    PROTECTED_SURFACES.md       ← no-touch contract
    SOURCE_DOCUMENT_MANIFEST.md ← source doc paths and caveats

audit-results/
  ph3_sepsis_simplify_audit.tsv
  ph3_mods_burns_simplify_audit.tsv
  (future: ph4_neurology_simplify_audit.tsv, ...)

scripts/
  anki/
    daughter_verify.py    ← persistent batch verification (use before every add_notes)
    count_backs.py        ← count visible Back chars for a list of NIDs
    count_large_cards.py  ← find all cards over 300 chars in a deck
    verify_daughters.py   ← older verify script (superseded by daughter_verify.py)
    verify_rewrites.py    ← verify rewritten Backs after update_note_fields

sourcedocs/             ← local only; PDFs/EPUBs excluded by .gitignore
  extracted_ccrn_handbook.txt   ← pre-extracted CCRN handbook text
  extracted_colson_ridge.txt    ← pre-extracted Colson Ridge text
  colson_ridge_sepsis_hits.txt
  juarez_sepsis_pages.txt
  epub_extracted/
```

---

## Local-Only Files (not in this repo)

These files must be present locally but are excluded by `.gitignore`:

- `sourcedocs/Adult CCRN Exam Premium...Juarez...pdf` (~20 MB)
- `sourcedocs/AACN Essentials...Burns Delgado...pdf` (~43 MB)
- `sourcedocs/CCRN Exam Study Guide...Colson Ridge...pdf` (~965 KB)
- `sourcedocs/Adult CCRN Exam Prep...PolyLearning...epub` (~912 KB)
- `sourcedocs/ccrnexamhandbook.pdf` (~3.9 MB)
- `sourcedocs/pccnexamhandbook.pdf` (~3.8 MB)

See `docs/project-state/SOURCE_DOCUMENT_MANIFEST.md` for full details and parsing caveats.
