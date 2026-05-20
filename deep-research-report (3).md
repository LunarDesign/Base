# Claude Prompt Plan for Your PCCN and CCRN Anki Deck

## What the prompt should optimize

I reviewed your uploaded `.apkg`, and your clarification makes the scope much cleaner: the task should target **only notes whose Back field exceeds 250 visible characters**. Not the Front. Not the whole deck. Just the long-answer notes. In your deck, the biggest cleanup burden appears to sit in pharmacology, reference, hemodynamics/shock, renal/GI, neurology, and several newer v7 cardio-respiratory specialty subdecks.

Because AACN’s current adult PCCN and adult CCRN blueprints both allocate **80%** of the exam to **Clinical Judgment** and **20%** to **Professional Caring and Ethical Practice**, the prompt should tell Claude to preserve exam-relevant distinctions instead of merely shortening prose. The current adult PCCN test plan applies to exams taken on and after **February 6, 2024**, and the current adult CCRN test plan applies to exams taken on and after **November 12, 2025**. For PCCN, cardiovascular and respiratory are especially prominent at **20%** and **14%**. For adult CCRN, cardiovascular is **13%**, respiratory **12%**, endocrine/hematology/GI/renal/GU/integumentary **21%**, musculoskeletal/neurological/behavioral/psychosocial **18%**, and multisystem **16%**. citeturn3view0turn3view1turn4view0turn5view0turn5view1

Both exams are organized around the **AACN Synergy Model**, so your prompt should also protect cards on advocacy, caring practices, collaboration, systems thinking, facilitation of learning, clinical inquiry, and response to diversity. AACN’s exam handbooks also note a transition toward **generic medication names**, while candidates may still encounter both generic and trade names during the transition. citeturn7view0turn7view2turn2view0turn3view3

## Why the prompt should allow splitting

The only real conflict in your goal is this: if a back is packed with clinically important material, “keep everything” and “cap this one back at 250 characters” are sometimes incompatible. The best workaround is to tell Claude: **compress losslessly when possible; split into sibling cards when not possible**. That fits the long-standing **minimum information principle** in spaced-repetition design, which argues that simpler, more atomic items are easier to retain and that oversized items create more forgetting and interference. citeturn8search0turn8search2turn8search4

So the strongest instruction is not “force every long back under 250 no matter what.” It is: **rewrite any long back to 250 or less if that can be done without losing exam-relevant content; otherwise split the note into two to four linked cards, each with a back of 250 or less**. That preserves your long-term nursing knowledge while making the cards much less exhausting to review.

## Paste-ready master prompt

```text
You already know my deck well. I want you to help me simplify it for readability without dumbing it down.

Deck/task context
- Deck: CCRN_PCCN_Mastery_v7_final_58.apkg
- Note fields: Front, Back, TierClass, PhaseBadge
- I am studying for BOTH AACN PCCN and adult CCRN.
- My job is cardiovascular progressive care, but the deck must remain useful for both certifications and for long-term nursing practice.

Primary rule
- ONLY target notes whose Back field exceeds 250 visible characters.
- Do NOT target cards based on Front length.
- Leave any note with Back <= 250 visible characters unchanged.

Character-count rule
- Count visible/plain-text characters only.
- Strip HTML tags, line breaks, bullet formatting, extra spaces, and repeated whitespace before counting.
- Decode HTML entities.
- Use the final visible Back text for the <=250 limit.

Rewrite goals
- Preserve clinically important information needed for PCCN + CCRN.
- Make the Back faster to read, easier to scan, and easier to recall.
- Keep the content high-yield and exam-relevant.
- Do not omit key facts just to shorten wording.

AACN alignment rules
- Prioritize information that maps to current adult PCCN and adult CCRN exam content and the AACN Synergy Model.
- Preserve high-yield distinctions, thresholds, sequences, first-line actions, priority interventions, hemodynamic logic, ventilation logic, pharmacology pearls, and professional practice concepts.
- Prefer generic drug names. Keep brand names only if they add meaningful recognition value.

Non-negotiables
- Preserve all numbers, cutoffs, formulas, timelines, “first/next/best” actions, contraindications, hallmark differentiators, and cause→effect logic.
- Keep the answer order aligned with the blanks, sequence, or compare structure on the Front.
- Use only standard ICU/progressive-care abbreviations.
- Remove filler, repeated wording, and redundant examples unless the example is necessary to distinguish concepts.
- Make the Back highly scannable using short phrases, semicolons, arrows, ↑/↓, or compact compare formatting.

Decision rule for each long card
1. If the Back can be rewritten LOSSLESSLY to <=250 visible characters, keep the Front unchanged and rewrite the Back.
2. If that is NOT possible without losing exam-relevant information, SPLIT the card into 2-4 sibling cards.
3. When splitting:
   - Keep the original concept intact across the card family.
   - Duplicate TierClass and PhaseBadge.
   - Keep fronts as similar as possible, but revise the Front if needed so each new Back matches only its own answer chunk.
   - Label sibling cards clearly, such as Part 1/2, or rewrite the Front into focused sub-prompts.
4. Never create a vague or incomplete Back just to hit the character limit.

Preferred compression patterns
- Definition cards: diagnosis/process = hallmark + key differentiator + priority management.
- Compare cards: X = cause/findings/management; Y = cause/findings/management.
- Algorithm cards: only essential ordered steps.
- Value/target cards: value + meaning + action.
- Drug cards: class/use/mechanism/main adverse effect/critical caution.
- Device cards: indication + main effect + major complication.
- Professional practice cards: principle + nurse action + why.
- Acronym cards: one-line meaning; split if multiple expansions/contexts are required.

Output format
For each targeted note, return:
- Subdeck
- Original Front
- Original Back visible character count
- Action taken: REWRITE or SPLIT
- New Front(s)
- New Back(s)
- New visible character count for each Back
- One-line rationale if split

Also provide:
1. A changelog table for review.
2. A TSV-ready export block with:
   Front<TAB>Back<TAB>TierClass<TAB>PhaseBadge

Workflow
- Work SUBDECK BY SUBDECK.
- Stop after each subdeck and wait for my approval before moving to the next one.
- Start with the subdeck I name.
- If I say “next,” continue to the next subdeck with the same rules.

Important quality check
Before finalizing each subdeck, compare every rewritten/split output against the original and confirm:
- no numeric thresholds were lost
- no priority intervention was lost
- no exam-relevant differential point was lost
- no required part of the Front/Back alignment was broken

Start now with this subdeck:
[PASTE SUBDECK NAME HERE]
```

## Shorter prompt for a single subdeck

If you want something lighter-weight for iterative batches, use this version:

```text
Process only this subdeck from my deck: [PASTE SUBDECK NAME]

Rules:
- ONLY modify notes whose Back >250 visible characters after stripping HTML and collapsing whitespace.
- Ignore Front length.
- Keep cards with Back <=250 unchanged.
- Preserve PCCN/CCRN exam-relevant content.
- Keep Front unchanged unless a split is necessary to avoid losing information.
- If a rewrite can stay lossless at <=250 chars, rewrite it.
- If not, split into 2-4 sibling cards, each with Back <=250 chars.
- Preserve numbers, thresholds, steps, differentials, pharmacology cautions, device details, and answer order.
- Prefer generic drug names.
- Output a review table plus a TSV-ready block with:
  Front<TAB>Back<TAB>TierClass<TAB>PhaseBadge

Return results in this order:
1. Review table
2. Split-card rationales
3. TSV-ready block
4. A brief “riskiest cards” list where compression was hardest
```

## Audit prompt for Claude after the rewrite

After Claude rewrites a batch, use this audit pass before you accept it:

```text
Audit the rewritten cards against the originals for this subdeck: [PASTE SUBDECK NAME]

Check only the cards that were rewritten or split.

For each card or card family, verify:
- the rewritten version still covers all PCCN/CCRN-relevant facts from the original
- no numeric threshold, sequence, contraindication, differentiator, or priority intervention was lost
- the Back is <=250 visible characters
- the Front still matches the Back
- any split cards are logically grouped and together preserve the original content

Flag any card where information loss occurred.
For flagged cards, propose the smallest fix:
- tighter rewrite, OR
- better split into sibling cards

Return:
1. Pass list
2. Flagged list
3. Corrected replacement version
```

## Best way to run this with your deck

I would run this in batches, not all at once. Based on the uploaded deck, the biggest payoff should come from the long pharmacology and reference sections first, then hemodynamics/shock, renal/GI, neurology, respiratory, and the newer v7 specialty subdecks. That order should reduce reading fatigue quickly while protecting the content that matters most across both exams.

One side note: studying both exams in parallel is reasonable, but make sure you track eligibility timing separately. AACN’s direct-care pathways for both adult PCCN and adult CCRN require either **1,750 hours** in the previous two years with **875** in the most recent year, or a five-year pathway with **2,000 hours** and **144** recent hours. AACN also explicitly lists **intermediate care, stepdown, telemetry, and transitional care** among typical PCCN settings, which fits your current role well. citeturn6search0turn6search1turn0search2