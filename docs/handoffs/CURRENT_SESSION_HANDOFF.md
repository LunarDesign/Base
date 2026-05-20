# Current Session Handoff

**Session date:** 2026-05-20  
**Project:** CCRN⁄PCCN Mastery v6 Anki deck — Ph3 simplification pass  
**Working directory:** `C:\Users\lunar\Desktop\Cards\CCRN_Cards_Project\Cards`  
**Repository status:** Not a git repository — no git history available

---

## 1. Current Goal

### Original user goal
Systematically simplify all Anki cards in the CCRN⁄PCCN Mastery v6 deck so that no card's Back field exceeds 300 visible characters. The project is a CCRN/PCCN exam-prep deck for a nurse (Mowzee Jones, RN at Duke 7700 Cardiology Step-Down) studying for certification.

### Active task
Ph3 simplification pass is now **complete**. The next session should begin **Ph4 Neurology** subdeck analysis and execution.

### What "done" means for Ph4 Neurology
- All notes in Ph4 Neurology subdecks fetched, counted, classified, and presented in an analysis table
- User approves the table
- SAFE REWRITEs, SAFE SPLITs, and SOURCE-UPDATED cards executed per approved plan
- Originals with splits suspended only after daughter cards confirmed and spot-checked
- Anki synced
- Audit TSV written for each subdeck

### Constraints (carry-forward — never change without explicit user approval)

1. **Back-only targeting.** Do NOT modify Front, TierClass, PhaseBadge, model name, or tags unless explicitly directed.
2. **300 visible-character limit.** Do not edit any card whose Back is ≤300 visible chars (exception: source issue separately approved).
3. **Chart model exemption.** Any card with `modelName` starting with `"CCRN Chart:"` is exempt from the 300-char rule — treat as NO ACTION regardless of Back length.
4. **Approval gate.** Present the classification table and wait for user approval before executing any changes.
5. **Source citation required.** Every source-based update must cite source file name + page/location + reason it matters.
6. **No silent clinical updates.** Do not silently change clinical information. Every source-based update must be explicitly labeled SOURCE-UPDATED REWRITE or SOURCE-UPDATED SPLIT.
7. **EPUB caveat.** If `PolyLearning Edu. EPUB` cannot be parsed reliably, stop and report — do not pretend to use it.
8. **Do not install system packages** without user approval.
9. **PhaseBadge anomalies:** Two chart cards have `&amp;` encoding in PhaseBadge (NIDs 1778808560027 and 1778808560036). Preserve exactly — never edit.

---

## 2. Current Status

### Completed this session (2026-05-20)
- **Ph3 Sepsis (88 notes)** — fully executed in a prior session; TSV written at `ph3_sepsis_simplify_audit.tsv`
- **Ph3 MODS & Trauma (30 notes)** — fully executed; TSV written at `ph3_mods_burns_simplify_audit.tsv`
  - 2 SAFE REWRITEs: NID 1778251562729 (346→287 chars), NID 1778251562763 (301→296 chars)
  - 6 SAFE SPLITs with 16 daughter cards created (NIDs 1779278789594–609)
  - 7 originals suspended
  - 1 SOURCE-UPDATED SPLIT (NID 1778381918069, Compartment Syndrome): delta pressure formula removed, "4-6 hours" → "emergent" per Juarez p.810; 3 daughters 1779280281582/583/584; original NID 1778381918070 suspended
- **Ph3 Burns & Toxicology (12 notes)** — fully executed; included in same TSV file
  - 1 SAFE REWRITE: NID 1778251562763 (301→296 chars)
  - 11 NO ACTION (8 standard + 3 chart-exempt)
- **Process improvements implemented and documented** in plan file and `daughter_verify.py`

### Partially completed work
- `daughter_verify.py` DAUGHTERS dict still contains the compartment syndrome batch (918069_D1/D2/D3). Clear and repopulate at the start of the next split batch.

### Work not yet started
- **Ph4 Neurology subdecks** (next in queue):
  - Ph4 ICP & Neuro Crisis
  - Ph4 Seizures & Status Epilepticus
  - Ph4 Stroke & TBI
- Ph5 through Ph8 subdecks
- v7 subdecks
- Retroactive Ph1 audit

### Blockers / uncertainties
- None currently. Ph3 is fully closed.
- Ph4 deck badge is 🟠 T2 — confirm exact deck name string via `mcp__anki__list_decks` before writing any daughter PhaseBadge.

### Decisions already made (do not relitigate)
- 300-char limit replaces prior 250-char limit
- Chart model cards permanently exempt
- Daughter tags: `["ccrn-pccn-v6", "chunk-XX", "simplify-daughter"]` — no `concept-chain` tag
- `allow_duplicate: false` on all `add_notes` calls
- All source updates must cite Juarez, Burns/Delgado, or Colson Ridge — Claude training knowledge is reasoning support only, not a source of truth

---

## 3. Session History

### This session (2026-05-20) — chronological

1. **Fetched and counted** Back fields for all 30 Ph3 MODS & Trauma notes + 12 Ph3 Burns & Toxicology notes using `notes_info` + inline Python char-counting.

2. **Presented analysis table** — classified all 42 notes (NO ACTION / SAFE REWRITE / SAFE SPLIT / FLAG FOR REVIEW by 300-char rule vs prior 250-char rule). User approved.

3. **Executed SAFE REWRITEs** via `mcp__anki__update_note_fields`:
   - NID 1778251562729: compressed 346 → 287 chars (ABCDE/FGHI format; "survey" removed from headers to save chars)
   - NID 1778251562763 (Burns): compressed 301 → 296 chars ("high risk VF" → "VF risk")

4. **Executed SAFE SPLITs** via `mcp__anki__add_notes` + `mcp__anki__card_management` (suspend):
   - NID 1778381918063 → 3 daughters (594/595/596) — Primary Survey
   - NID 1778381918066 → 3 daughters (597/598/599) — Hemorrhagic Shock
   - NID 1778381918072 → 3 daughters (600/601/602) — Rhabdomyolysis (**tier-high**, not tier-critical)
   - NID 1778436692068 → 2 daughters (603/604) — DCR
   - NID 1778436692071 → 3 daughters (605/606/607) — DCR synthesis
   - NID 1778437755998 → 2 daughters (608/609) — Hemorrhagic Shock navigation

5. **Mid-session process check-in** (user-requested). Identified 4 inefficiencies. User directed: address all 4.

6. **Process improvements implemented:**
   - Created `daughter_verify.py` (persistent verify script with TierClass guard + column output)
   - Documented single-notes_info-call protocol
   - Documented spot-check-before-suspend protocol
   - Added Process Protocol section to plan file

7. **Source-checked NID 1778381918069** (Compartment Syndrome, FLAG FOR REVIEW, 2263 chars):
   - Ran `find_compartment.py` to locate pages in all three source PDFs
   - Ran `extract_juarez_810.py` → output at `juarez_compartment.txt` / `juarez_compartment_full.txt`
   - Ran `extract_burns_compartment.py` → output at `burns_compartment.txt`
   - Finding: Delta pressure formula NOT found in any source; "4-6 hours" NOT found; Juarez p.810 says "emergent decompressive fasciotomy" + absolute threshold >30 mmHg only
   - User selected Option A (SOURCE-UPDATED SPLIT)

8. **Executed SOURCE-UPDATED SPLIT** for NID 1778381918069:
   - 3 daughters created (1779280281582/583/584)
   - Daughter D2 required two char-count reduction passes (319→300 exact)
   - Daughter D3 required one char-count reduction pass (301→292)
   - Ran `daughter_verify.py` — all three daughters confirmed OK
   - Spot-checked D1 via `notes_info` — confirmed fields landed correctly
   - Original NID 1778381918070 suspended

9. **Updated `ph3_mods_burns_simplify_audit.tsv`** with compartment syndrome SOURCE-UPDATED SPLIT row and 3 daughter rows.

10. **Updated plan file** at `C:\Users\lunar\.claude\plans\ticklish-finding-hellman.md`:
    - Cleared stale PENDING entry
    - Added Process Protocol section (items 4/5/8/9)
    - Updated NEXT to Ph4 Neurology

11. **Synced Anki** via `mcp__anki__sync` after each major batch.

### Errors encountered and fixed

| Error | Fix |
|---|---|
| UnicodeEncodeError printing `↓` to PowerShell (cp1252) | Added `sys.stdout.reconfigure(encoding='utf-8')` and redirected output to file via `Out-File -Encoding utf8` |
| NID 729 rewrite was 301 chars (1 over) | Removed "survey" from "Primary survey" / "Secondary survey" → 287 chars |
| Compartment D2 was 319 chars (19 over) | Removed "prevent: " label prefixes; changed "circumferential" → "constricting" (Juarez language) → 300 chars |
| Compartment D3 was 301 chars (1 over) | Removed "nursing " from "nursing error" → 292 chars |
| Plan mode auto-triggered mid-session | Loaded ExitPlanMode, updated plan file, called ExitPlanMode |

---

## 4. Reasoning and Methodology

### Why this approach
Cards with Back > 300 visible chars cause Anki review fatigue and violate the deck's design contract. The simplification task is mechanical (count → classify → execute) but has clinical risk — wrong content removal could cause exam failure or unsafe clinical reasoning. Hence the approval gate and source-citation requirement.

### Assumptions made
- The 300-char limit applies only to the Back field's visible rendered text (HTML stripped, entities decoded)
- Chart model cards are structurally special (chart data + JS rendering) and are always exempt
- Juarez, Burns/Delgado, and Colson Ridge are the authoritative sources for clinical content — Claude's training knowledge is used only for reasoning, never as a source of truth
- `tier-critical` is the default TierClass for most Ph3 cards; exceptions (e.g., `tier-high` for Rhabdomyolysis NID 918072) must be copied verbatim from parent

### Tradeoffs considered
- **SAFE REWRITE vs SAFE SPLIT**: Rewrites are lower risk (no new cards, no suspension) but only work when compression is lossless. When content is too dense or nuanced, splits preserve clinical accuracy at the cost of more cards.
- **SOURCE-UPDATED SPLIT vs keeping original wrong content**: The compartment syndrome card contained a delta pressure formula (diastolic BP − compartment pressure < 30 mmHg) not found in any study source. Keeping it risked exam misguidance. Removing it with a source citation was the correct call.

### Alternatives rejected
- Rewriting chart model cards: rejected per user instruction ("chart model cards are exempt. continue")
- Using Claude training knowledge as a clinical source: rejected per governing rules
- Silent source updates: rejected; every update must be labeled SOURCE-UPDATED

### What still needs validation
- Ph4 Neurology deck name string — must be confirmed via `list_decks` before any daughter card creation
- Ph4 deck badge (🟠 T2) — must be confirmed against live Anki before writing PhaseBadge field on any daughter

---

## 5. Project Structure Map

```
C:\Users\lunar\Desktop\Cards\CCRN_Cards_Project\Cards\
│
├── sourcedocs\                         ← Source PDFs/EPUB — clinical authority tier 2
│   ├── AACN Essentials...Burns Delgado...pdf   (43 MB — progressive care nursing reference)
│   ├── Adult CCRN Exam Premium...Juarez...pdf  (20 MB — primary CCRN study guide)
│   ├── CCRN Exam Study Guide...Colson Ridge...pdf  (965 KB — condensed guide)
│   ├── Adult CCRN Exam Prep...PolyLearning...epub  (912 KB — ⚠️ parse reliability uncertain)
│   ├── ccrnexamhandbook.pdf            ← AACN official CCRN blueprint (tier 1 authority)
│   ├── pccnexamhandbook.pdf            ← AACN official PCCN blueprint (tier 1 authority)
│   ├── extracted_ccrn_handbook.txt     ← pre-extracted CCRN handbook text
│   ├── extracted_colson_ridge.txt      ← pre-extracted Colson Ridge text
│   ├── juarez_sepsis_pages.txt         ← Juarez sepsis page extracts (prior session)
│   ├── colson_ridge_sepsis_hits.txt    ← Colson Ridge sepsis hits (prior session)
│   └── epub_extracted\                 ← EPUB extraction attempt (may be incomplete)
│
├── docs\
│   ├── audits\
│   │   └── chunks-29-56-consistency-rule-adherence-audit.md
│   └── handoffs\
│       └── CURRENT_SESSION_HANDOFF.md  ← THIS FILE
│
├── daughter_verify.py                  ← Persistent batch verification script (process item 4+5)
│                                          Populate DAUGHTERS dict, run before every add_notes
│
├── ph3_sepsis_simplify_audit.tsv       ← Completed audit: Ph3 Sepsis (88 notes)
├── ph3_mods_burns_simplify_audit.tsv   ← Completed audit: Ph3 MODS & Trauma + Burns (42 notes)
│
├── count_backs.py                      ← Char-counting utility (reusable for new subdecks)
├── count_large_cards.py                ← Finds cards over char limit
├── count_results.txt                   ← Output from count run
│
├── find_compartment.py                 ← Finds compartment syndrome pages in all 3 source PDFs
├── extract_juarez_810.py               ← Extracts Juarez pages 809-813
├── extract_burns_compartment.py        ← Extracts Burns/Delgado compartment pages
├── juarez_compartment.txt              ← Juarez compartment syndrome extract (key finding: >30mmHg + "emergent")
├── juarez_compartment_full.txt         ← Fuller Juarez extract
├── burns_compartment.txt               ← Burns/Delgado compartment extract
├── compartment_pages.txt               ← Page index: which pages in each source have compartment content
├── check_juarez_compartment.py         ← Page-search script for Juarez
│
├── verify_918069.txt                   ← Spot-check output for compartment syndrome daughters
├── verify_daughters.py                 ← Earlier (non-persistent) verify script — superseded by daughter_verify.py
├── verify_rewrites.py                  ← Rewrite verification script
├── verify_results.txt                  ← Output from verify_rewrites.py
├── daughter_results.txt                ← add_notes return NID confirmation
│
├── chunk33_charts.py … chunk56_charts.py  ← Card generation scripts (prior build sessions)
├── CCRN_PCCN_Mastery_v7_final_29.apkg … _58.apkg  ← Exported deck snapshots (read-only history)
│
├── audit_typeb.py                      ← Type-B card audit (prior session, unrelated to current task)
├── audit_typeb_report.txt              ← Output from type-B audit
├── patch_typeb.py / patch_typeb2.py    ← Type-B patch scripts (prior sessions)
│
├── PROJECT_CONTEXT.md                  ← High-level project overview
├── README_CLAUDE_CODE.md               ← Claude Code setup notes
├── CHART_BACKLOG.md                    ← Chart card backlog
├── clinical_split_plan_all_chunks.md   ← Prior clinical split planning doc
└── clinical_split_plan_chunk54.md      ← Chunk 54 specific split plan
```

---

## 6. Relevant Files and What They Do

| File path | Purpose | Current relevance | Safe to edit? | Notes |
|---|---|---|---|---|
| `daughter_verify.py` | Persistent verification script — populate DAUGHTERS dict, run before every `add_notes` batch; validates char counts + TierClass | **HIGH — use at start of every split batch** | Yes — clear DAUGHTERS dict and repopulate for each new batch | Currently contains 918069 compartment syndrome entries — clear these before next batch |
| `ph3_mods_burns_simplify_audit.tsv` | Audit trail for Ph3 MODS & Trauma + Burns subdeck (42 notes + daughters) | Complete; read-only reference | No (complete record) | All rows finalized including compartment syndrome SOURCE-UPDATED SPLIT |
| `ph3_sepsis_simplify_audit.tsv` | Audit trail for Ph3 Sepsis (88 notes) | Complete; read-only reference | No (complete record) | Written in prior session |
| `count_backs.py` | Counts visible Back chars for a list of NIDs | Reuse for Ph4 analysis | Yes | Adapt NID list for Ph4 |
| `count_large_cards.py` | Finds all cards over 300 chars in a deck | Reuse for Ph4 analysis | Yes | Adapt deck query |
| `sourcedocs/Adult CCRN Exam Premium...Juarez...pdf` | Primary clinical reference (20 MB) | HIGH — continue using for Ph4 | No | Compartment syndrome: p.810; ICP likely in neuro chapters |
| `sourcedocs/AACN Essentials...Burns Delgado...pdf` | Secondary clinical reference (43 MB) | HIGH — continue using for Ph4 | No | 43 MB; extract specific pages rather than reading whole file |
| `sourcedocs/ccrnexamhandbook.pdf` | AACN CCRN exam blueprint — tier 1 authority | HIGH — confirm Ph4 scope alignment | No | Pre-extracted to `extracted_ccrn_handbook.txt` |
| `sourcedocs/extracted_ccrn_handbook.txt` | Pre-extracted CCRN handbook text | HIGH — search this instead of re-extracting PDF | No | Faster than re-extracting PDF pages |
| `sourcedocs/extracted_colson_ridge.txt` | Pre-extracted Colson Ridge text | Moderate — for Ph4 clinical spot-checks | No | Search for neuro content |
| `C:\Users\lunar\.claude\plans\ticklish-finding-hellman.md` | Active plan file — rules, workflow, process protocol, status | **CRITICAL — read this at session start** | Update status only; never change Active Rules without user approval | Updated this session with Process Protocol section |
| `C:\Users\lunar\.claude\projects\...\memory\MEMORY.md` | Memory index | Read at session start | Update via memory system only | Links to user profile, project state, feedback |
| `C:\Users\lunar\.claude\projects\...\memory\project_ccrn_deck.md` | Project state memory | Read at session start | Via memory system only | Chunk 32 complete; Chunk 33 next; model IDs 1_800_005_010+ |
| `C:\Users\lunar\.claude\projects\...\memory\user_mowzee.md` | Learner profile | Context for card decisions | Via memory system only | RN, CCRN/PCCN prep, former IT PM |
| `C:\Users\lunar\.claude\projects\...\memory\feedback_badge_tiers.md` | Badge/tier feedback | **CRITICAL — check Ph4 badge before writing PhaseBadge** | Via memory system only | Ph4 Neurology = 🟠 T2 |

---

## 7. Protected / Do-Not-Touch Areas

| Area | Reason | What to do instead |
|---|---|---|
| Front field of any note | Governing rules: Back-only targeting | Never modify Front |
| TierClass field of any note | Must be preserved exactly — determines card difficulty routing | Copy verbatim from parent when creating daughters |
| PhaseBadge field of any note | Must be preserved exactly, including `&amp;` anomalies | Copy verbatim from parent when creating daughters |
| Chart model cards (`modelName` starts with `"CCRN Chart:"`) | Exempt from 300-char rule per user instruction | Classify as NO ACTION; never edit |
| PhaseBadge `&amp;` anomaly — NIDs 1778808560027 and 1778808560036 | Known encoding anomaly; changing it would break display | Preserve exactly as-is |
| `ph3_sepsis_simplify_audit.tsv` | Complete audit record | Read-only reference |
| `ph3_mods_burns_simplify_audit.tsv` | Complete audit record | Read-only reference |
| `*.apkg` files | Exported deck snapshots — historical record | Never modify; they're binary |
| `sourcedocs\` PDFs/EPUB | Source authority documents | Read-only; extract pages, do not write |
| Active Rules section of plan file | Locked per user: "do not change without user approval" | Propose changes; wait for approval |
| Any card with Back ≤ 300 chars | Governing rules: no edits unless source issue separately approved | Classify as NO ACTION |

---

## 8. Commands and How to Resume

**This project has no git repository.** All state is in Anki (via AnkiConnect MCP) and local files.

### Step 1: Load required Anki MCP tools at session start

```
ToolSearch: "select:mcp__anki__notes_info,mcp__anki__update_note_fields,mcp__anki__add_notes,mcp__anki__card_management,mcp__anki__sync,mcp__anki__find_notes,mcp__anki__list_decks"
```

### Step 2: Confirm Ph4 deck names and badges

```python
# Call mcp__anki__list_decks to get exact deck name strings for Ph4 Neurology subdecks
# Expected pattern: "CCRN⁄PCCN Mastery v6::Ph4 · 🟠 T2 · ..."
# Confirm PhaseBadge text to use on daughter cards
```

### Step 3: Fetch all Ph4 Neurology notes

```python
# Use mcp__anki__find_notes to get NIDs for each Ph4 subdeck
# Query pattern: deck:"CCRN⁄PCCN Mastery v6::Ph4 · 🟠 T2 · Neurology*"
# Then call mcp__anki__notes_info on ALL NIDs in ONE call (single-call protocol from process item 8)
```

### Step 4: Count visible Back chars

```python
# Use count_backs.py or inline this function:
import re, html
def vis(raw):
    d = html.unescape(raw)
    s = re.sub(r'<[^>]+>', ' ', d)
    s = s.replace('\n', ' ').replace('\t', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return len(s)
# Apply to every note's Back field
# Chart model cards (modelName starts with "CCRN Chart:") → skip (NO ACTION)
```

### Step 5: Classify, cross-check sources, present table

Present classification table to user. Wait for approval before executing anything.

### Step 6: Execute (post-approval only)

```python
# 1. SAFE REWRITEs via update_note_fields
# 2. For each SAFE SPLIT:
#    a. Clear daughter_verify.py DAUGHTERS dict; populate with new daughters
#    b. Run daughter_verify.py — confirm "ALL N daughters OK"
#    c. Call add_notes — confirm NIDs returned
#    d. Spot-check one daughter per parent via notes_info
#    e. ONLY THEN call card_management suspend on parent
# 3. Sync via mcp__anki__sync
# 4. Write audit TSV
```

### Reference: daughter card conventions

```python
# Tags:
["ccrn-pccn-v6", "chunk-XX", "simplify-daughter"]  # XX = chunk number of parent

# Fields required on daughter notes:
{
    "Front": "<question text>",
    "Back": "<answer text — must be ≤300 visible chars>",
    "TierClass": "<copy verbatim from parent>",
    "PhaseBadge": "<copy verbatim from parent>",
    # ... other fields as required by the model
}

# allow_duplicate: false  (always)
```

### Reference: visible char counting

```python
import re, html
def vis(raw):
    d = html.unescape(raw)
    s = re.sub(r'<[^>]+>', ' ', d)
    s = s.replace('\n', ' ').replace('\t', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return len(s)
# Threshold: 300. Over = classify for action. At or under = NO ACTION.
```

### Reference: key Anki NIDs already handled (do not re-process)

| NID | Status | Notes |
|---|---|---|
| 1778381918063 | Suspended | MODS/Trauma Primary Survey — daughters 594/595/596 |
| 1778381918064 | Suspended | (original card form — replaced by daughters) |
| 1778381918066 | Suspended | Hemorrhagic Shock — daughters 597/598/599 |
| 1778381918067 | Suspended | (original card form) |
| 1778381918069 | Suspended | Compartment Syndrome SOURCE-UPDATED — daughters 582/583/584 |
| 1778381918070 | Suspended | (original card form) |
| 1778381918072 | Suspended | Rhabdomyolysis (tier-high) — daughters 600/601/602 |
| 1778381918073 | Suspended | (original card form) |
| 1778436692068 | Suspended | DCR — daughters 603/604 |
| 1778436692069 | Suspended | (original card form) |
| 1778436692071 | Suspended | DCR synthesis — daughters 605/606/607 |
| 1778436692072 | Suspended | (original card form) |
| 1778437755998 | Suspended | Hemorrhagic Shock navigation — daughters 608/609 |
| 1778437755999 | Suspended | (original card form) |
| 1779278789594–609 | Active daughters | MODS/Trauma batch — 16 daughters total |
| 1779280281582–584 | Active daughters | Compartment Syndrome SOURCE-UPDATED batch — 3 daughters |

---

## 9. Source Document Quick Reference

| Source | File | Key use | Page-finding tip |
|---|---|---|---|
| Juarez (primary CCRN guide) | `sourcedocs/Adult CCRN Exam Premium...Juarez...pdf` | Clinical thresholds, management, exam targets | Run `find_compartment.py`-style script; check `compartment_pages.txt` for example |
| Burns/Delgado (AACN Essentials) | `sourcedocs/AACN Essentials...Burns Delgado...pdf` | Progressive care clinical reference | 43 MB — always extract specific pages, not whole document |
| Colson Ridge | `sourcedocs/CCRN Exam Study Guide...Colson Ridge...pdf` | Condensed exam guide; pre-extracted at `extracted_colson_ridge.txt` | Search the .txt file first before opening the PDF |
| AACN CCRN handbook | `sourcedocs/ccrnexamhandbook.pdf` | Exam blueprint — scope/priority authority | Pre-extracted at `extracted_ccrn_handbook.txt` |
| PolyLearning EPUB | `sourcedocs/Adult CCRN Exam Prep...PolyLearning...epub` | MCQ review | ⚠️ Parse reliability uncertain — if extraction fails, stop and report; do not assume content |

---

## 10. Process Protocol (permanent — implemented 2026-05-20)

These four workflow rules are permanent. Apply from the first step of every new subdeck.

### Rule 4 — Persistent verify script
- File: `daughter_verify.py`
- **Before any split batch:** Clear DAUGHTERS dict, populate with new daughters, run script
- Do NOT call `add_notes` until script prints "ALL N daughters OK"
- After batch: leave dict populated for record; clear only at START of next batch

### Rule 5 — TierClass guard
- `daughter_verify.py` validates tier strings against `{tier-critical, tier-high, tier-low}`
- Tier is printed in the output table — visually confirm before `add_notes`
- **Key risk:** `tier-high` parents (e.g., Rhabdomyolysis NID 918072) must NOT have daughters defaulting to `tier-critical`

### Rule 8 — Single `notes_info` call
- Fetch ALL parent fields (Front, Back, TierClass, PhaseBadge, tags) for ALL parents in ONE `notes_info` call
- Draft daughter Backs from that same result — no second fetch
- Populate `daughter_verify.py` DAUGHTERS dict from the same data

### Rule 9 — Spot-check before suspend
- After `add_notes` returns confirmed NIDs: call `notes_info` on **one daughter per parent**
- Verify: Back content correct, TierClass correct, tags present
- ONLY after spot-check passes: call `card_management` suspend on parent
- If field error found: fix via `update_note_fields` on the daughter BEFORE suspending parent
