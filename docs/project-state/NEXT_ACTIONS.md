# Next Actions

> Do not execute any of these without first reading `CURRENT_STATE.md` and confirming no work was done in the interim.

---

## Immediate Next: Ph4 Neurology Simplification Pass

### Pre-flight (do before any note fetching)

- [ ] 1. Confirm Anki desktop is open and AnkiConnect is responding
- [ ] 2. Load required MCP tools via ToolSearch:
  ```
  select:mcp__anki__notes_info,mcp__anki__update_note_fields,mcp__anki__add_notes,mcp__anki__card_management,mcp__anki__sync,mcp__anki__find_notes,mcp__anki__list_decks
  ```
- [ ] 3. Call `mcp__anki__list_decks` — confirm exact name strings for Ph4 Neurology subdecks
  - Expected pattern: `CCRN⁄PCCN Mastery v6::Ph4 · 🟠 T2 · Neurology — ...`
  - Capture PhaseBadge text exactly as it appears — this goes on every daughter card verbatim
- [ ] 4. Clear `scripts/anki/daughter_verify.py` DAUGHTERS dict (currently contains compartment syndrome entries from prior session — replace at start of first split batch, not before)

### Analysis (present table, do not execute)

- [ ] 5. Use `mcp__anki__find_notes` to get NIDs for each Ph4 subdeck
- [ ] 6. Fetch ALL Ph4 note fields in ONE `notes_info` call (Rule 8 — single call for all parents)
- [ ] 7. Count visible Back chars for every note using `scripts/anki/count_backs.py` or inline `vis()` function
  - Chart model cards (`modelName` starts with `"CCRN Chart:"`) → NO ACTION, skip counting
- [ ] 8. Classify all notes and present analysis table to user
  - Columns: `NID | Action | Front (truncated) | Back char count | Classification | Clinical risk | Notes`
  - **WAIT FOR USER APPROVAL before any execution**

### Execution (only after approval)

- [ ] 9. Execute SAFE REWRITEs via `update_note_fields`
- [ ] 10. For each SAFE SPLIT:
  - [ ] a. Populate `scripts/anki/daughter_verify.py` DAUGHTERS dict
  - [ ] b. Run verify script — confirm "ALL N daughters OK"
  - [ ] c. Call `add_notes` — confirm NIDs returned
  - [ ] d. Spot-check one daughter per parent via `notes_info` (Rule 9)
  - [ ] e. Call `card_management` suspend on parent ONLY after spot-check passes
- [ ] 11. Sync via `mcp__anki__sync`
- [ ] 12. Write audit TSV to `audit-results/ph4_neurology_simplify_audit.tsv`

### Post-session

- [ ] 13. Update `docs/project-state/CURRENT_STATE.md` — mark Ph4 as complete
- [ ] 14. Update `docs/handoffs/HANDOFF_INDEX.md` — add new row
- [ ] 15. Create `docs/handoffs/CURRENT_SESSION_HANDOFF.md` — full handoff for next session
- [ ] 16. Commit and push to GitHub:
  ```bash
  git add docs/ audit-results/
  git commit -m "Ph4 Neurology complete — audit TSV + state docs updated"
  git push origin main
  ```

---

## After Ph4 — Subsequent Phases

- Ph5 through Ph8 subdecks (exact deck names TBD via `list_decks`)
- v7 subdecks (separate deck family — confirm before starting)
- Retroactive Ph1 audit (may be lower priority — confirm with user)

---

## Daughter Card Conventions (reference)

```python
# Tags
["ccrn-pccn-v6", "chunk-XX", "simplify-daughter"]  # XX = chunk number of parent

# Fields
{
    "Front": "<question>",
    "Back": "<answer — must be ≤300 visible chars>",
    "TierClass": "<copy verbatim from parent>",
    "PhaseBadge": "<copy verbatim from parent>",
    # ... all other fields the model requires
}

# allow_duplicate: false  (always)
```
