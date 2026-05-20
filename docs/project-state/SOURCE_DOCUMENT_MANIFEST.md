# Source Document Manifest

> These documents are **local only** and are never committed to the repository.
> PDFs and EPUBs are excluded by `.gitignore` (`*.pdf`, `*.epub`).
> Future sessions must have these files present locally before performing source checks.

---

## Source Documents

| Document | Expected local path | Approx. size | Authority tier | Purpose | Required for validation | Commit? |
|---|---|---|---|---|---|---|
| Juarez — Adult CCRN Exam Premium | `sourcedocs/Adult CCRN Exam Premium For the Latest Exam Blueprint, Includes 3 Practice Tests, Comprehensive Review, and Online Study Prep… (Pat Juarez) (z-library.sk, 1lib.sk, z-lib.sk).pdf` | ~20 MB | Tier 2 | Clinical thresholds, management protocols, exam targets | Yes | Never |
| Burns/Delgado — AACN Essentials | `sourcedocs/AACN Essentials of Progressive Care Nursing, Fourth Edition (Suzanne M. Burns  Sarah A. Delgado) (z-library.sk, 1lib.sk, z-lib.sk).pdf` | ~43 MB | Tier 2 | Progressive care clinical reference | Yes | Never |
| Colson Ridge — CCRN Study Guide | `sourcedocs/CCRN Exam Study Guide - Ace your Adult Critical Care Registered Nurse License on the First Try QA (June 5, 2024)_(B0D6BM8K97) (Colson Ridge) (z-library.sk, 1lib.sk, z-lib.sk).pdf` | ~965 KB | Tier 2 | Condensed exam guide | Yes | Never |
| PolyLearning — MCQ EPUB | `sourcedocs/Adult CCRN Exam Prep - Ultimate MCQ Review for Critical Care Nursing Certification - Comprehensive Question Bank to Ace the… (PolyLearning Edu.) (z-library.sk, 1lib.sk, z-lib.sk).epub` | ~912 KB | Tier 2 | MCQ bank | No | Never |
| AACN CCRN Exam Handbook | `sourcedocs/ccrnexamhandbook.pdf` | ~3.9 MB | **Tier 1** | Official CCRN exam blueprint — scope authority | Yes | Never |
| AACN PCCN Exam Handbook | `sourcedocs/pccnexamhandbook.pdf` | ~3.8 MB | **Tier 1** | Official PCCN exam blueprint — scope authority | Yes | Never |

---

## Caveats and Parsing Notes

### Burns/Delgado (43 MB)
- Do NOT attempt to load the entire PDF at once — extract specific pages only
- Use `pdfplumber` with targeted page numbers
- Relevant chapters are large; budget extra time for page scans

### PolyLearning EPUB
- Parse reliability is uncertain — extraction produced only partial content (`sourcedocs/epub_extracted/`)
- **If extraction fails or is incomplete: stop and report to user. Do not pretend to have used it.**
- User may need to convert to PDF/markdown/text before this source is usable

### CCRN/PCCN Handbooks
- Both are pre-extracted to text: `sourcedocs/extracted_ccrn_handbook.txt` (in repo)
- Search the pre-extracted `.txt` file before opening the PDF — much faster
- No pre-extracted version of the PCCN handbook exists yet

### Colson Ridge
- Pre-extracted to `sourcedocs/extracted_colson_ridge.txt` (in repo)
- Sepsis-specific search results cached at `sourcedocs/colson_ridge_sepsis_hits.txt`
- Search `.txt` files first

### Juarez
- No full pre-extraction; use targeted page extraction scripts
- Sepsis pages cached at `sourcedocs/juarez_sepsis_pages.txt`
- Compartment syndrome pages cached at `juarez_compartment.txt` (repo root)
- Page-finding script: `find_compartment.py` (finds compartment/fasciotomy/delta pages across all sources)

---

## Pre-Extracted Text Files (committed to repo)

These are small text extracts derived from the source PDFs — they are committed and can be searched directly without opening the PDFs.

| File | Source PDF | Contents |
|---|---|---|
| `sourcedocs/extracted_ccrn_handbook.txt` | ccrnexamhandbook.pdf | Full text extraction of CCRN handbook |
| `sourcedocs/extracted_colson_ridge.txt` | Colson Ridge PDF | Full text extraction of Colson Ridge |
| `sourcedocs/colson_ridge_sepsis_hits.txt` | Colson Ridge PDF | Sepsis-related hits |
| `sourcedocs/juarez_sepsis_pages.txt` | Juarez PDF | Sepsis chapter pages |
| `sourcedocs/epub_extracted/part*.txt` | PolyLearning EPUB | Partial EPUB extraction |
| `juarez_compartment.txt` (root) | Juarez PDF | Compartment syndrome pages |
| `juarez_compartment_full.txt` (root) | Juarez PDF | Extended compartment syndrome extract |
| `burns_compartment.txt` (root) | Burns/Delgado PDF | Compartment syndrome pages |
| `compartment_pages.txt` (root) | All three PDFs | Page index: which pages have compartment content in each source |

---

## If a Source Document Is Missing Locally

1. Do not attempt the source check
2. Report which document is missing and its expected path
3. Ask user to provide the file before continuing
4. Do not use Claude's training knowledge as a substitute
