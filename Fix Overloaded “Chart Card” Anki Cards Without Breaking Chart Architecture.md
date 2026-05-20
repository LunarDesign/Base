# Fix Overloaded “Chart Card” Anki Cards Without Breaking Chart Architecture

You are working in the NurseAnki CCRN/PCCN Anki deck project.

The issue: cards tagged as card type **“chart card”** are often too dense. They frequently try to test too many things at once, such as:

* diagnosis,
* biomarker kinetics,
* rationale,
* next diagnostic step,
* nursing role,
* clinical interpretation,
* chart interpretation,
* and mechanism

all on one card.

This makes the chart cards inefficient for Anki review, even when the clinical content is valuable.

Your task is to review and revise the existing **chart card** cards so they become more digestible, focused, and reviewable while preserving the interactive chart-card system whenever possible.

## Project location

Work from:

`C:\\Users\\lunar\\Desktop\\Cards`

Use the actual project files as the source of truth.

Review relevant files such as:

* `PROJECT\_CONTEXT.md`
* `README\_CLAUDE\_CODE.md`
* `CHART\_BACKLOG.md`
* `card\_validator.py`
* `build\_utils.py`
* `chunk\_template.py`
* chunk files
* generated `.apkg` files
* any exported card data or deck inspection files
* any documentation that explains chart card architecture, note types, tags, or validation rules

Do not assume the examples in this prompt are exhaustive. Use your knowledge of the actual deck structure and files.

\---

# Primary goal

Fix the **retrieval design** of the chart cards.

This is not a request to rebuild the chart system.

The goal is to make chart cards work better as Anki cards by reducing cognitive overload, not by removing charts.

Each revised chart card should test **one primary recall target**.

The interactive chart should remain as visual support whenever it meaningfully helps the learner.

\---

# Important context

The chart cards were built around interactive physiology and clinical charts. Do not treat them like ordinary text-only cards.

The chart is part of the learning design.

However, the chart should support one focused recall task per card. It should not become an excuse to overload the card with a full mini-lecture.

The original prototype chart cards were intentionally dense. The main deck should not preserve that prototype style. The main deck should use charts as focused, progressive learning tools.

\---

# Do not break the chart system

Preserve the chart-card architecture as much as possible.

Do not remove interactive charts unless the chart is clearly unnecessary for that card.

Do not rewrite chart rendering logic unless absolutely required.

Do not change model IDs, deck IDs, field names, note type structure, JavaScript, CSS, shared utilities, or APKG build logic unless there is no safe alternative.

Prefer revising card content rather than altering chart architecture.

If a card needs to be split, create additional focused chart cards that reuse the same chart type and chart parameters where possible.

\---

# Scope

Review every card tagged as card type:

`chart card`

Do not revise cards tagged as:

`card 1`

or other standard/non-chart card types unless absolutely necessary to support a split and you clearly document why.

This task is focused on chart cards only.

\---

# What counts as an overloaded chart card

A chart card is overloaded if it tests more than one primary learning target at once.

Examples of overload:

* diagnosis + biomarker kinetics + next step
* waveform recognition + treatment + complication
* hemodynamic pattern + drug choice + drug mechanism
* chart interpretation + full nursing role
* lab interpretation + rationale + follow-up diagnostic algorithm
* one front with multiple blanks asking for separate ideas
* a back answer that reads like a mini-lecture instead of a reviewable explanation

The key question:

**Can the learner answer this card quickly and clearly during spaced repetition?**

If not, it likely needs trimming or splitting.

\---

# Main revision rule

Each revised chart card should follow this structure whenever possible:

## Front

* One clinical setup or chart-based observation
* One clear blank: `\_\_\_\_\_\_\_`
* One focused question

## Back

* Direct answer
* One concise explanation
* One `→ CCRN KEY:` annotation
* Optional `→ MASTERY NOTE:` only if it adds essential long-term learning value

Avoid long algorithmic backs unless the algorithm step itself is the single thing being tested.

\---

# Preserve critical information by splitting, not deleting

Do not simply remove important clinical content.

If one chart card contains multiple valuable ideas, split it into multiple smaller cards.

For example, if one card currently tests:

1. whether reinfarction occurred,
2. why flat troponin is not enough,
3. why CK-MB is useful,
4. what the next diagnostic step is,
5. and what the nurse’s role is,

split it into focused cards such as:

* diagnosis pattern
* biomarker kinetics
* next diagnostic step
* nursing role or monitoring priority

Each card may reuse the same interactive chart if the chart still supports the question.

\---

# Keep the interactive chart in mind

For every revised chart card, ask:

1. What is the chart helping the learner see?
2. What single concept should the learner retrieve from the chart?
3. Is the learner interpreting the chart, applying the chart, or just reading a long explanation?
4. Would this card still make sense during a fast Anki review?
5. Does the chart support the question, or is it just decorative?
6. Does the card still fit the intended L1/L2/L3 or progressive-learning structure?

If the chart no longer supports the question well, flag the card for manual review instead of forcing the change.

\---

# Revision categories

Classify every chart card into one of these categories:

## Keep as-is

The card is already focused, digestible, and uses the chart appropriately.

## Light edit

The card is mostly good but needs a shorter front, shorter back, clearer blank, or tighter `→ CCRN KEY:`.

## Split into multiple chart cards

The card contains multiple valuable learning targets that should become 2–4 smaller chart cards.

## Convert one part to a regular card

The chart supports one part of the content, but another part would be better as a normal text card.

Only do this if the deck’s architecture supports it safely.

## Flag for manual review

The card is too complex, clinically uncertain, poorly aligned with the chart, or risky to revise automatically.

Do not modify manual-review cards without approval.

\---

# Required audit before editing

Before making edits, create a review table.

Use this format:

|Card ID / Note ID|Chart Type|Current Problem|Category|Proposed Fix|Risk|
|-|-|-|-|-|-|

Risk levels:

* Low — wording or trimming only
* Medium — split card but preserve chart architecture
* High — chart/card relationship unclear or architecture may be affected
* Manual Review — do not change without approval

After creating this table, proceed only with Low and Medium risk fixes.

Do not modify High or Manual Review items unless I approve.

\---

# Editing rules

When editing chart cards:

1. Preserve the original clinical meaning.
2. Preserve high-yield CCRN/PCCN information.
3. Reduce cognitive overload.
4. Keep one main blank per card whenever possible.
5. Keep the front shorter than the original whenever possible.
6. Keep the back focused and reviewable.
7. Retain `→ CCRN KEY:` when clinically useful.
8. Use `→ MASTERY NOTE:` sparingly.
9. Do not recreate the same overload across multiple long backs.
10. Do not delete clinically important content; split it if needed.
11. Preserve chart functionality.
12. Preserve chart parameters when reused.
13. Preserve subdeck placement unless there is a clear reason to change it.
14. Preserve tags and add new tags only if consistent with project conventions.
15. Preserve the progressive learning sequence if the chart cards use L1/L2/L3 or equivalent levels.

\---

# Ideal back-card length

Aim for:

* answer phrase,
* 1–3 sentence explanation,
* one focused `→ CCRN KEY:`.

Avoid:

* full algorithms,
* multiple paragraphs,
* multiple unrelated teaching points,
* long nurse-role explanations,
* and multi-step diagnostic pathways unless that pathway is the single tested idea.

\---

# Example transformation pattern

Original overloaded chart card style:

```text
Front:
A patient had NSTEMI 5 days ago. Today: new chest pain, troponin 18× ULN unchanged, CK-MB normal. The \_\_\_\_\_\_\_ had a reinfarction because \_\_\_\_\_\_\_. The correct next diagnostic step: \_\_\_\_\_\_\_.

Back:
Long explanation covering reinfarction, troponin kinetics, CK-MB kinetics, serial labs, ECG, echo, physician role, nurse role, and full algorithm.

Better split:

Card A Front:
Five days after NSTEMI, troponin is still high but unchanged and CK-MB is normal. This pattern \_\_\_\_\_\_\_ reinfarction.

Card A Back:
does not confirm → CCRN KEY: Reinfarction requires a new rise/fall pattern. A flat troponin can reflect persistent elevation from the original MI.

Card B Front:
CK-MB helps detect reinfarction days after MI because it usually returns to normal within \_\_\_\_\_\_\_.

Card B Back:
48–72 hours → CCRN KEY: A new CK-MB rise after normalization suggests new myocardial injury.

Card C Front:
Troponin can remain elevated for \_\_\_\_\_\_\_ after MI, making a single elevated value difficult to interpret after recent infarction.

Card C Back:
about 7–14 days → CCRN KEY: Trend troponin for a new rise/fall pattern instead of relying on one persistent elevation.

Card D Front:
Possible reinfarction after recent NSTEMI should be evaluated with serial \_\_\_\_\_\_\_ and \_\_\_\_\_\_\_.

Card D Back:
ECGs and biomarkers → CCRN KEY: New ischemic ECG changes, biomarker rise, instability, or new wall-motion abnormality increases concern for reinfarction.

This is the desired style: preserve the clinical information, but separate it into focused retrieval units.

Validation requirements

After revising chart cards:

Run the existing card\_validator.py.
Confirm all revised cards pass.
Confirm no standard card types were unintentionally changed.
Confirm chart note types still render.
Confirm chart JavaScript/CSS was not accidentally altered.
Confirm model IDs and field names were not broken.
Confirm the deck exports successfully.
If possible, inspect a small sample of revised chart cards on front/back to confirm readability.
If an APKG is generated, clearly state which input deck was used and what output deck was created.
Required final report

After completing the review and safe revisions, provide a report with:

Total chart cards reviewed.
Number kept as-is.
Number lightly edited.
Number split into multiple chart cards.
Number converted partly into regular cards.
Number flagged for manual review.
Total new cards created from splits.
Any chart cards that still feel too dense.
Any chart cards where the chart no longer supports the question well.
Any architecture files touched.
Any protected surfaces touched.
Validation results.
Output APKG/file name, if created.
Whether it is safe to continue building future chart cards.
Important constraints

Do not continue building new chunks during this task.

Do not prioritize increasing card count.

Prioritize review efficiency, digestibility, and preservation of the chart-card system.

The goal is not fewer cards. The goal is better cards.

If important content needs to become multiple smaller cards, that is acceptable.

If a card cannot be safely revised without risking the chart architecture, flag it for manual review instead of forcing a fix.

