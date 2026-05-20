# Protected Surfaces — Do Not Touch Without Explicit Approval

> This file defines the no-touch contract for the CCRN⁄PCCN deck simplification project.
> If a future session is tempted to edit anything on this list, stop and ask the user first.

---

## Anki Card Fields

| Field | Rule | Reason |
|---|---|---|
| `Front` | Never modify | Back-only targeting is the governing rule |
| `TierClass` | Never modify on existing cards; copy verbatim from parent when creating daughters | Determines card difficulty routing; wrong tier breaks review scheduling |
| `PhaseBadge` | Never modify on existing cards; copy verbatim from parent when creating daughters | Badge must match exactly, including `&amp;` encoding anomalies (see below) |
| `modelName` | Never change | Determines which Anki template renders the card |

### PhaseBadge encoding anomalies — preserve exactly

Two chart cards have `&amp;` literal in their PhaseBadge field instead of `&`. Do NOT normalize or fix them:

| NID | Anomaly |
|---|---|
| 1778808560027 | PhaseBadge contains `&amp;` — preserve as-is |
| 1778808560036 | PhaseBadge contains `&amp;` — preserve as-is |

---

## Card Categories — Always Exempt

| Category | Rule |
|---|---|
| Chart model cards (`modelName` starts with `"CCRN Chart:"`) | **Always NO ACTION** — exempt from 300-char rule entirely; never edit |
| Any card with Back ≤ 300 visible chars | **NO ACTION** — do not edit unless a source issue is found AND separately approved by user |

---

## Completed Audit Files — Read Only

Do not re-process notes that appear in completed audit TSVs. Do not edit the TSVs themselves.

| File | Phase covered |
|---|---|
| `audit-results/ph3_sepsis_simplify_audit.tsv` | Ph3 Sepsis — 88 notes |
| `audit-results/ph3_mods_burns_simplify_audit.tsv` | Ph3 MODS & Trauma + Burns — 42 notes + daughters |

---

## Suspended Cards — Do Not Reactivate Without Approval

These originals were suspended after daughters were confirmed created. Do not unsuspend without user instruction.

| NID | What it was |
|---|---|
| 1778381918064 | Primary Survey original |
| 1778381918067 | Hemorrhagic Shock original |
| 1778381918070 | Compartment Syndrome SOURCE-UPDATED original |
| 1778381918073 | Rhabdomyolysis original |
| 1778436692069 | DCR original |
| 1778436692072 | DCR synthesis original |
| 1778437755999 | Hemorrhagic Shock navigation original |

---

## Source Documents — Never Commit

| File type | Rule |
|---|---|
| `sourcedocs/*.pdf` | Local only — excluded by `.gitignore`; see `SOURCE_DOCUMENT_MANIFEST.md` |
| `sourcedocs/*.epub` | Local only — excluded by `.gitignore` |
| `sourcedocs/epub_extracted/*.txt` | Committed (user approved); do not remove from repo |

---

## Anki Deck Exports

| File | Rule |
|---|---|
| `CCRN_PCCN_Mastery_v7_final_*.apkg` | Historical snapshots — read only; do not delete |
| `*.apkg.bak` | Backup copies — read only |

---

## Active Rules in the Plan File

The `Active Rules` section of `C:\Users\lunar\.claude\plans\ticklish-finding-hellman.md` must not be changed without explicit user approval. These rules have been stable across multiple sessions and changing them could silently break the simplification workflow.

---

## Source Authority Hierarchy — Do Not Invert

1. AACN exam handbooks (exam blueprint — scope authority)
2. Juarez, Burns/Delgado, Colson Ridge PDFs (clinical detail authority)
3. Existing card Back field (preserve when accurate)
4. Claude's training knowledge (reasoning support only — **never cite as a source of truth**)

Inverting this hierarchy — e.g., using Claude's training as a source to update clinical card content — is a safety violation.
