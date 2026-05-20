# NurseAnki Chunks 29–56 Consistency & Rule-Adherence Audit

**Audit date:** 2026-05-16 | **Scope:** Chunks 29–56 (1,443 cards) | **Status:** Complete + Addendum

---

## Part I — Main Audit (Chunks 29–56)

### Step 1 — Rule Reconstruction

Canonical rules derived from `chunk_template.py`, `build_utils.py`, `card_validator.py`, and `PROJECT_CONTEXT.md`:

| Rule | Source | Canonical Value |
|------|--------|-----------------|
| TierClass field | chunk_template.py | `'tier-review'` / `'tier-high'` / `'tier-critical'` |
| PhaseBadge field | PROJECT_CONTEXT.md | `'Ph{N} · 🔴/🟠/🟡 T{N} · {Category} — {Subdeck Name}'` |
| ltag field | chunk_template.py | `'chart-l1'` / `'chart-l2'` / `'chart-l3'` |
| Back structure | PROJECT_CONTEXT.md | Must include `→ CCRN KEY:` and `→ MASTERY NOTE:` |
| Card tuple | chunk_template.py | `(front, back, tier_str, badge_str, did_int, chart_type, params_json, ltag)` |
| insert_card signature | build_utils.py | 10 positional args |
| validate() return | card_validator.py | `issues` list (not tuple) |
| F4 validator | card_validator.py | Requires literal `→` (U+2192) in back |

---

### Step 2 — Chunk Inventory

All 56 chunks confirmed complete. DID registry fully exhausted (entries 100–106, 110–117, 120–123, 130–133, 140–141, 150–152, 160, 170–181, 190–193, 195). Total: 1,443 cards across 56 chunks.

---

### Step 3 — Rule Adherence (Confirmed Deviations)

**DEVIATION D1 — CRITICAL: TierClass and PhaseBadge corruption in chunks 55–56**

Database inspection confirmed:
```
chunks 55-56:  tier_field='T3'     (invalid CSS class — should be 'tier-critical'/'tier-high'/'tier-review')
               badge_field='🟡'   (truncated — should be 'Ph7 🟡 T3 · Pharmacology — ...' full string)
               ltag='ph7-xxx'      (wrong — should be 'chart-l1'/'chart-l2'/'chart-l3')
               pj=<chart_type>     (non-JSON string — should be '{}')

chunks 52-54:  tier_field='tier-high'    ✓ correct
               badge_field='Ph7 🟡 T3 · Pharmacology — ...'  ✓ correct
```
Impact (pre-fix): 30 cards had no CSS left-border color and showed only an emoji in the badge div.
**Status: FIXED — chunks 55 and 56 rebuilt from chunk54 (2026-05-16).**

**DEVIATION D2 — MEDIUM: `tier-review` absent from chunks 47–56**

All L1 foundational cards in chunks 47–56 used `'tier-high'` instead of `'tier-review'`. The canonical progression is: `tier-review` (teal, L1 recognition) → `tier-high` (orange, L2 application) → `tier-critical` (red, L3 synthesis). In chunks 47–54, the teal foundational border was missing for ~40 L1 cards. Post-audit inspection also found L2 and L3 assignments were arbitrary (not just L1) — 89 of 120 notes in chunks 47–54 had wrong tier values.

Note: D1 fix for chunks 55–56 restored correct `tier-review` for those 10 cards.
**Status: FIXED 2026-05-16** — `patch_d2.py` corrected all 89 misassigned notes in `_56.apkg`; `fix_d2_sources.py` corrected corresponding CARDS tuples in chunk47–54 source files. Verified: 150 notes (chunks 47–56) all pass tier/ltag consistency check.

**DEVIATION D3 — LOW: Badge format separator inconsistency**

Chunks 33–51 use: `'Ph7 · 🟡 T3 · Pharmacology — ...'` (with ` · ` before emoji)
Chunks 52–56 use: `'Ph7 🟡 T3 · Pharmacology — ...'` (missing ` · ` before emoji)

Both render legibly. Cosmetic inconsistency only.

**DEVIATION D4 — LOW: W8 warnings in chunks 55–56**

15 W8 soft warnings per chunk (30 total) — backs do not include `→ CCRN KEY:` / `→ MASTERY NOTE:` scaffold. No cards were blocked (W8 is a soft warning). Chunks 47–54 do not have this issue.

---

### Step 4 — Progression Model

L1/L2/L3 tier distribution:
- Chunks 28–46: canonical `tier-review`/`tier-high`/`tier-critical` used correctly
- Chunks 47–54: tier assignments were arbitrary across all levels (D2, **FIXED 2026-05-16**)
- Chunks 55–56 (post-fix): canonical tier progression restored

---

### Step 5 — Information Density

Cards reviewed as clinically appropriate density for CCRN/PCCN level. All 56 chunks passed F2/F7 validators (no front >580 chars, no back <60 chars). Chunks 28–41 use interactive physiology curves (single-concept focus). Chunks 42–56 use highlight tables and 3-tab panels — appropriate for Ph7/Ph8 reference content. No clinical compression artifacts found.

---

### Step 6 — Validator Adequacy

CardValidator (F1–F7 + W8) is adequate for text card structure validation.

**Gap identified and fixed (2026-05-16):** CardValidator did not check TierClass validity. `'T3'` was silently accepted. Added F9 check: `tier in {'tier-review', 'tier-high', 'tier-moderate', 'tier-critical'}` with optional `tier` parameter to `validate()`. New call pattern: `validator.validate(nid, front, back, badge, tier)`.

---

### Step 7 — Architecture Consistency

`make_chart_template()` / `register_chart_model()` / `insert_card()` API consistent across all 56 chunks. VARI_ENABLED=True confirmed in `build_utils.py` — anti-visual-memorization JS active in all chart templates. DID routing correct across all chunks.

---

### Step 8 — Protected Surfaces

| Surface | Status |
|---------|--------|
| Canvas rendering | ✓ Intact — CSS-immune |
| `.badge` div structural position | ✓ Intact — content fixed in chunks 55–56 |
| SHARED_JS color vars | ✓ Intact |
| `safe_html()` | ✓ Intact |
| `card_validator.py` | ✓ Extended with F9 (additive, no breaking changes) |
| DID registry | ✓ All entries correct |
| Night mode selectors | ✓ Intact |

---

### Step 9 — Backlog Reconciliation

`CHART_BACKLOG.md` is severely outdated — reflects planned state as of chunk 32, does not match chunks 33–56. No clinical content was dropped; the backlog was a planning artifact, not a contract. The file is misleading for future developers.

---

### Step 10 — Documentation Consistency

`PROJECT_CONTEXT.md` reads "Current State: as of Chunk 32" — 24 chunks behind. Canonical rules it documents (tier names, badge format, back structure) are accurate to original spec but do not reflect chunk 47–56 reality. **Update pending (LOW priority, approved 2026-05-16).**

---

### Step 11 — Clinical Sanity Check

Spot-checked clinical content in chunks 47–56. Content accurate for CCRN/PCCN scope: KDIGO staging, ISTH DIC criteria, DOSE trial diuretic dosing, ARDSNet protocol, Sepsis-3 definitions, TDM targets. No clinical content errors identified.

---

### Step 12 — Deviation Classification

| ID | Severity | Chunks | Cards | Root Cause | Status |
|----|----------|--------|-------|------------|--------|
| D1 | CRITICAL | 55–56 | 30 | Rushed error-recovery; short literals used instead of CSS class names | **FIXED 2026-05-16** |
| D2 | MEDIUM | 47–54 | 89 | Tier assignments arbitrary across all levels; no L1 card used `tier-review` | **FIXED 2026-05-16** |
| D3 | LOW | 52–56 | 75 | Badge format string dropped ` · ` separator before emoji | Cosmetic; accepted |
| D4 | LOW | 55–56 | 30 | Chart backs use condensed structure without annotation labels | Accepted (W8 soft only) |
| D5 | LOW | All | — | `PROJECT_CONTEXT.md` and `CHART_BACKLOG.md` frozen at chunk 32 | Pending (LOW priority) |

---

## Part II — Supplemental Addendum: Prototype-to-Main-Deck Transition Review

### Transition Evidence

**1. Original deck architecture (pre-chart)**
Documented in `PROJECT_CONTEXT.md`: Main note type `CCRN Mastery v6` (MID `1800000010`), 4 fields (Front/Back/TierClass/PhaseBadge), ~92% blank-fill, CSS 5px tier border system, `CardValidator` F1–F7. No JavaScript in original main note type.

**2. Original chart recommendation**
No "prototype-only" recommendation is documented in any project file. `PROJECT_CONTEXT.md` presents chart cards as an established co-equal architecture feature. No "zero-JS rule" appears in any surviving project file.

**3. Prototype isolation**
No standalone prototype file exists in the project directory. `CHUNK 30 .txt` shows chunk 30 output directly into the main deck (`CCRN_PCCN_Mastery_v7_final.apkg`). Charts were in the main deck by chunk 28, before the Claude Code handoff.

**4. Testing evidence**
`README_CLAUDE_CODE.md` documents a testing protocol (Anki Desktop, AnkiWeb, interactive controls). No formal pass/fail records exist. Protocol is defined; execution records are absent.

**5. User approval of integration**
`CHART_BACKLOG.md` plans 57 remaining charts across all phases in the main deck. `README_CLAUDE_CODE.md` was authored as a handoff for continued main-deck chart development. These documents are the implicit approval record. No explicit written authorization statement exists.

**6. Transition documentation**
No document describes when/why charts moved from any prior state to the main deck. The governance record of the original decision is absent from all surviving project files.

**7. Zero-JS rule status**
The zero-JS rule does not appear in any current project file. It cannot be confirmed or denied from surviving documentation. The chart system uses JavaScript in separate note types only; the main blank-fill note type remains JS-free.

**8. Main note type preservation**
Yes — confirmed. `build_utils.py` comment: "Main blank-fill note type: 1_800_000_010." `get_main_css()` is read-only. All chart note types use separate IDs (1_800_002_000+). No chunk script writes to `1800000010`.

**9. Chart note type separation**
Yes — confirmed. Chart note types use entirely separate model IDs. They share the 4-field schema with the main type by design (documented in `PROJECT_CONTEXT.md`). No contamination path exists.

**10. Protected surface modifications**
None detected across all 56 chunks. Canvas rendering, SHARED_JS, `safe_html()`, badge structure, and DID registry were not modified by any chart build script.

**11. Cross-platform safety**
Architecture present (dark mode CSS, `max-width:100%` canvas, conservative VARI font sizes). No formal cross-platform test records documented.

**12. Information density**
Consistent with stated phase goals. Ph7/Ph8 reference-table style is appropriate for reference phase content. L1/L2/L3 question structure preserved (with D2 exception in chunks 47–54).

**13. Chart style drift**
Ph8 chunks (47–51) use denser reference-table formats appropriate for that phase. This is a documented style evolution, not arbitrary drift. Not formally noted in project docs — a documentation gap only.

---

### Transition Classification

**Technically valid but governance gap**

The architecture is sound: charts use separate note types, main note type is intact, field schema is compatible by design, CSS protection is in place, testing protocol exists. However: no document records when/why JavaScript was introduced, no formal test pass logs exist, `PROJECT_CONTEXT.md` is 24 chunks stale, and the decision history predating chunk 28 is unrecoverable from current project files.

---

### Prompt Gap Reconciliation

| Concern | Addressed? | Evidence | Remaining Gap |
|---------|------------|----------|---------------|
| Original zero-JS architecture | Partially | Not documented in any project file — unresolvable from evidence | Decision log predating chunk 28 absent |
| Prototype-only recommendation | Partially | No prototype file exists; `CHUNK 30 .txt` confirms direct main-deck integration | Pre-chunk-28 history absent |
| User approval/evolution trail | Partially | `CHART_BACKLOG.md` + `README_CLAUDE_CODE.md` are implicit approval evidence | No explicit authorization statement |
| Separate chart note types | Fully | `build_utils.py` ID ranges confirm complete separation | None |
| Existing non-chart cards protected | Fully | `get_main_css()` read-only; MID 1800000010 never written by chart scripts | None |
| `CCRN Mastery v6` / model 1800000010 | Fully | Not present in any chart build script's model registration path | None |
| `CardValidator` adequacy | Fully | F9 tier check added (2026-05-16); all other rules remain appropriate | None |
| Chart density/progression risks | Fully | L1/L2/L3 structure confirmed; Ph8 style shift documented; D2 recorded | None |
| Cross-platform assumptions | Partially | Dark mode CSS confirmed; conservative VARI range confirmed | No mobile test records |
| Documentation updated | Not yet | `PROJECT_CONTEXT.md` frozen at chunk 32; `CHART_BACKLOG.md` obsolete | Pending LOW-priority update |

---

## Part III — Final Status

### Confirmed bugs and their status

| ID | Issue | Status |
|----|-------|--------|
| D1 | TierClass/PhaseBadge corruption in chunks 55–56 (30 cards) | **FIXED 2026-05-16** |
| F9 validator gap | CardValidator silently accepted invalid tier strings | **FIXED 2026-05-16** |
| D2 | Tier assignments wrong in chunks 47–54 (89 notes) — L1/L2/L3 all affected | **FIXED 2026-05-16** |
| D3 | Badge separator inconsistency chunks 52–56 | Accepted (cosmetic) |
| D4 | W8 warnings in chunks 55–56 (no annotation labels) | Accepted (soft warning only) |
| D5 | `PROJECT_CONTEXT.md` / `CHART_BACKLOG.md` stale | Pending (LOW priority) |

### Safe to continue to Chunk 57?

**Yes.** D1 is fixed. The final deck (`CCRN_PCCN_Mastery_v7_final_56.apkg`) is clean. Use `chunk_template.py` or chunk 54 as the template for chunk 57 — not chunks 55/56 (even though they are now fixed, the template is the canonical reference).

### Decisions made (2026-05-16)

1. D1 fix — **approved and executed**
2. D2 (restore `tier-review` chunks 47–54) — **approved, LOW priority, not yet executed**
3. F9 validator check — **approved and executed**
4. D5 (`PROJECT_CONTEXT.md` update) — **approved, LOW priority, not yet executed**
5. `docs/audits/` directory creation — **approved and executed**
