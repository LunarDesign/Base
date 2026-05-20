# Clinical Split Plan — Chunk 54
## Pre-Edit Report + Proposed Card Splits
Date: 2026-05-16 | Standard: one clinical domain per card | Source: 57.apkg

---

## PART 1 — PRE-EDIT REPORT (7 Questions)

### 1. Are the flagged cards clinically relevant overall?
YES — HIGH relevance. Chunk 54 covers ICU pharmacology that CCRN candidates must know: ICU sedation safety (PRIS, delirium, dexmedetomidine), antifungal stewardship (MRSA coverage, candidemia, mucormycosis), beta-blocker differentiation (aortic dissection, preeclampsia, variceal prophylaxis), and vasopressor escalation. These are not trivia. The problem is content packaging, not content value.

### 2. Is the overload from valuable clinical reasoning or unnecessary detail?
Mostly valuable reasoning packed into too-small containers. Only three items across all 16 cards qualify as demotable trivia:
- MERIT-HF exact mortality reduction percentage (34%) — cardiologist-level outcome data
- Echinocandin coverage gaps for Fusarium/Trichosporon — organism-level microbiology beyond nursing scope
- ZEPHyR cure rate exact numbers (59% vs 35%) — the concept matters; the decimal precision does not

Everything else has a clear nursing application: recognizing toxicity, monitoring drug levels, selecting the right route/agent, escalating when targets are missed.

### 3. Which chunks are most clinically high-yield to fix first?
Priority order:
1. **Chunk 54** (current) — sedation + antifungal + vasopressor + beta-blocker pharmacology
2. **Chunk 42** — 6 HIGH, content unknown until reviewed
3. **Chunks 52–53** — Extended Pharm era, 5 HIGH + 5 MED each
4. **Chunks 28–29** — no source .py files, smaller card count, lower severity

### 4. Which chunks have greatest risk of losing content if split poorly?
Chunk 54 itself is highest risk. The antifungal cards (mucormycosis, crypto meningitis, azoles) contain interconnected clinical reasoning chains — mechanism → spectrum gap → monitoring → clinical selection rule. Splitting at the wrong seam creates orphaned facts with no clinical context. The beta-blocker cards are the same — the dissection card only makes sense if esmolol's short half-life is understood.

### 5. Does any card content appear clinically questionable?
All clinical facts checked. No accuracy concerns found. Specific verifications:
- PRIS threshold (>4 mg/kg/hr >48h): correct per standard references
- Vancomycin AUC/MIC target (400–600): correct per 2020 ASHP/SIDP guideline
- Vasopressin max (0.04 units/min): correct for septic shock protocols
- Type A dissection targets (HR<60, SBP<120): correct per AHA
- Cryptococcal meningitis induction (AmB + 5-FC × 2 weeks): correct per IDSA
- Lorazepam/oxazepam/temazepam glucuronidation in hepatic failure: correct
- Daptomycin surfactant inactivation: correct
- Labetalol β:α ratio (3:1 oral / 7:1 IV): correct

No cards contain unsupported absolutes or implied independent prescribing.

### 6. Should cleanup prioritize CCRN, PCCN, or both?
Chunk 54 skews CCRN. ICU sedation protocols, complex antifungals, and vasopressor escalation are ICU-only content. However:
- Anaphylaxis card: BOTH (high-yield for PCU nurses too)
- Preeclampsia/labetalol: BOTH
- Beta-blocker contraindications: BOTH
- Cardiogenic shock hemodynamics: primarily CCRN; PCCN moderate
- Antifungal stewardship depth: CCRN only; PCCN nurses should know candidemia first-line but not organism-level gaps

Proposed tagging: **[CCRN+PCCN]** vs **[CCRN]** on each card header.

### 7. Is the current validator insufficient?
YES — critically so. The regex heuristic:
- **Missed NOTE 1778926634021** (MERINO trial + ceftazidime-avibactam coverage) — classified as OK because only one domain label was detected, despite two independent clinical topics
- Cannot distinguish physician-level diagnostic nuance from nursing-scope content
- Cannot check AACN test plan alignment
- Cannot assess clinical accuracy
- Tight-pair detection is too narrow (e.g., `drug_mechanism + drug_monitoring` classified LOW even when the drugs are different agents)
- Cannot detect multi-subject cards when subject names don't match the hardcoded drug lists

Recommendation: After split-plan review, update the validator to add a clinical relevance pass (AACN domain tagging) and tighten multi-subject detection to catch cross-drug mechanism cards.

---

## PART 2 — CHUNK 54 AACN RELEVANCE TABLE (High + Medium flagged cards)

| Note ID | Chunk | Chart Type | Current Topic | Likely AACN Domain | CCRN Relevance | PCCN Relevance | RN Action Tested? | Decision |
|---|---|---|---|---|---|---|---|---|
| 1778926634000 | 54 | chart-l1 | Propofol mechanism + PRIS + no analgesia | Pharmacology — Sedation | High | Moderate | No (tests mechanism, not action) | Split → 2 cards |
| 1778926634003 | 54 | chart-l2 | Dexmedetomidine + Ketamine (two drugs) | Pharmacology — Sedation | High | Moderate | No (tests mechanism) | Split → 2 cards |
| 1778926634006 | 54 | chart-l3 | Midazolam delirium + hepatic benzo + lorazepam toxicity | Pharmacology — Sedation | High | Moderate | Partial | Split → 3 cards (lorazepam tox → regular card) |
| 1778926634015 | 54 | chart-l3 | Mucormycosis + Crypto meningitis + AmB formulations | Pharmacology — Antifungals | Moderate | Low | No | Split → 3 cards |
| 1778926634018 | 54 | chart-l1 | Vancomycin AUC + Daptomycin CI + ZEPHyR trial | Pharmacology — MRSA | High | Moderate | Partial | Split → 3 cards |
| 1778926634030 | 54 | chart-l2 | Dobutamine + Milrinone + IABP trial + CI target | Cardiovascular — Cardiogenic shock | High | Moderate | Partial | Split → 2 cards |
| 1778926634036 | 54 | chart-l1 | Esmolol PK + dissection targets + variceal BB | Cardiovascular — Hypertensive emergency | High | Moderate | Partial | Split → 3 cards (varices → regular card) |
| 1778926634042 | 54 | chart-l3 | Labetalol profile + preeclampsia + BB contraindications | Cardiovascular — Hypertensive emergency | High | High | Partial | Split → 2 cards |
| 1778973067510 | 54 | chart-l1 | Vasopressin dose + epinephrine lactate interference | Cardiovascular — Septic shock | High | Low | Partial | Split → 2 cards |
| 1778926634009 | 54 | chart-l1 | Azole mechanism + fluconazole gaps + voriconazole + warfarin | Pharmacology — Antifungals | Moderate | Low | No | Split → 2 cards; warfarin DDI → demote |
| 1778926634012 | 54 | chart-l2 | Echinocandin mechanism + no-adjust agent + coverage gaps | Pharmacology — Antifungals | Moderate | Low | No | Split → 2 cards; organism gaps → fold into back |
| 1778926634024 | 54 | chart-l3 | HAP/VAP duration + PCT threshold + PRORATA trial | Pharmacology — Antibiotic stewardship | High | Moderate | Partial | Keep as 1 card; demote PRORATA numbers |
| 1778926634033 | 54 | chart-l3 | Anaphylaxis first Tx + neurogenic bradycardia + MAP target | Multisystem — Shock types | High | High | Yes | Split → 2 cards |
| 1778926634039 | 54 | chart-l2 | Carvedilol profile + MERIT-HF + thyroid storm | Cardiovascular + Endocrine | High (thyroid) / Low (MERIT-HF) | Moderate | Partial | Split → 1 card (thyroid); demote MERIT-HF |

---

## PART 3 — PROPOSED CLINICAL SPLITS (detailed)

---

### ORIGINAL: NOTE 1778926634000 — Propofol (HIGH, 6 blanks, chart-l1)
**Front:** "On the sedation comparison chart, propofol works by _______ and has a unique toxicity at doses > _______ mg/kg/hr for > 48 hours called _______ syndrome, which presents with _______, rhabdomyolysis, and _______. Propofol has _______ analgesic effect."

**Learning targets identified:**
- T1: Mechanism (GABA-A potentiation)
- T2: PRIS dose threshold (>4 mg/kg/hr / >48h)
- T3: PRIS syndrome name
- T4: PRIS presentation (lactic acidosis + rhabdo + AV block)
- T5: Lipemic plasma as PRIS sign
- T6: No analgesic effect

**CCRN/PCCN high-yield:** T1+T6 (mechanism/analgesic gap), T2–T5 (PRIS recognition — ICU nurse must catch this)
**Keep:** All
**Split:** Yes — mechanism separate from toxicity
**Demote:** None
**Remove:** None

| Target # | New Card Type | AACN Domain | CCRN/PCCN | RN Action | Keep Chart? | Proposed Front | Proposed Back |
|---:|---|---|---|---|---|---|---|
| T1+T6 | Chart card | Pharmacology — Sedation | High / Moderate | anticipate, prevent harm | YES | On the sedation comparison chart, propofol produces sedation by _______. Unlike opioids, it has _______ analgesic effect — meaning a separate _______ must always be co-administered. | GABA-A receptor potentiation (allosteric modulation) \| No analgesic effect \| Always pair with opioid or other analgesic (analgo-sedation protocol) \| Failure to provide analgesia causes pain-driven agitation even under deep sedation |
| T2–T5 | Chart card | Pharmacology — Sedation / Safety | High / Moderate | recognize, monitor, escalate | YES | A patient has been on propofol infusion for 60 hours at 5 mg/kg/hr. The nurse notes a new metabolic _______ gap acidosis, rising CK, and a new _______ block on the monitor. This presentation is called _______ and requires _______. | PRIS (Propofol Infusion Syndrome) \| Anion gap metabolic acidosis + rhabdomyolysis + AV conduction block + lipemic plasma \| Triggered by >4 mg/kg/hr for >48h \| STOP propofol immediately, notify provider, switch sedative agent |

---

### ORIGINAL: NOTE 1778926634003 — Dexmedetomidine + Ketamine (HIGH, 7 blanks, chart-l2)
**Front:** "On the sedation chart, dexmedetomidine is unique because it provides sedation WITHOUT _______ depression. It acts on _______ receptors in the _______. Ketamine provides sedation AND analgesia via _______ receptor antagonism and is preferred for intubation in _______ because it is a _______ agent. Ketamine also causes _______ making it useful in asthma."

**Learning targets:**
- T1: Dex — no respiratory depression
- T2: Dex mechanism — α2 receptors, locus coeruleus
- T3: Ketamine mechanism — NMDA antagonism
- T4: Ketamine preferred for intubation in hemodynamically unstable/bronchospasm patients
- T5: Ketamine = sympathomimetic
- T6: Ketamine causes bronchodilation

**Two completely different drugs — split.**

| Target # | New Card Type | AACN Domain | CCRN/PCCN | RN Action | Keep Chart? | Proposed Front | Proposed Back |
|---:|---|---|---|---|---|---|---|
| T1+T2 | Chart card | Pharmacology — Sedation | High / Moderate | differentiate, monitor | YES | On the sedation comparison chart, dexmedetomidine is unique among ICU sedatives because it provides sedation WITHOUT _______. It achieves this by acting on _______ receptors in the _______, reducing norepinephrine release. | Respiratory depression \| α2-adrenergic receptors in the locus coeruleus \| Clinical advantage: patient remains arousable and can follow commands; safe to maintain during ventilator weaning; no apnea risk at standard doses |
| T3–T6 | Chart card | Pharmacology — Sedation | High / Moderate | differentiate, anticipate | YES | On the sedation chart, ketamine is preferred for intubation in patients with _______ because it causes _______. Ketamine is a _______ agent — meaning it _______ heart rate and blood pressure, making it safe when hemodynamics are marginal. | Severe bronchospasm or asthma \| Bronchodilation (β2 + anticholinergic effect) \| Sympathomimetic \| Increases HR and BP via catecholamine release \| NMDA receptor antagonist \| Monitor for: emergence reactions (hallucinations on waking) — benzodiazepine pretreatment reduces incidence |

---

### ORIGINAL: NOTE 1778926634006 — Midazolam/Benzos (HIGH, 6 blanks, chart-l3)
**Front:** "The sedation chart shows midazolam is associated with _______ in ICU compared to propofol and dexmedetomidine. In hepatic failure, the preferred benzodiazepine is _______ because it undergoes _______ without producing active metabolites. Lorazepam IV infusions can cause toxicity from the carrier _______, presenting as _______ gap and metabolic _______."

**Learning targets:**
- T1: Midazolam → more ICU delirium
- T2: Hepatic failure → lorazepam (glucuronidation, no active metabolites)
- T3: Lorazepam IV → propylene glycol toxicity → anion gap + metabolic acidosis

**Three separate clinical concerns — split.**

| Target # | New Card Type | AACN Domain | CCRN/PCCN | RN Action | Keep Chart? | Proposed Front | Proposed Back |
|---:|---|---|---|---|---|---|---|
| T1 | Chart card | Pharmacology — Sedation / Delirium | High / Moderate | differentiate, monitor | YES | On the sedation comparison chart, prolonged midazolam infusion in the ICU is associated with _______ rates of delirium compared to propofol and dexmedetomidine. Current SCCM guidelines recommend _______ benzodiazepines for routine ICU sedation. | Higher delirium rates (MIDEX and MENDS trials) \| AGAINST routine benzo sedation \| Midazolam also accumulates in prolonged use (active metabolite in AKI/hepatic dysfunction) \| Appropriate benzo uses: status epilepticus (first-line), alcohol withdrawal, procedural sedation |
| T2 | Chart card | Pharmacology — Hepatic dosing | High / Moderate | differentiate, prevent harm | YES | A patient with decompensated cirrhosis requires sedation for a bedside procedure. The preferred benzodiazepine is _______ because it is metabolized by _______, which does not require hepatic oxidation and produces _______. | Lorazepam (or oxazepam/temazepam — the "LOT" benzos) \| Glucuronidation (Phase II conjugation — preserved in hepatic disease) \| No active metabolites \| Midazolam contraindicated in severe liver failure — oxidative metabolism impaired → active metabolite accumulates |
| T3 | Regular card (no chart) | Pharmacology — Drug toxicity | Moderate / Low | monitor, escalate | NO | A patient on prolonged IV lorazepam infusion develops an unexplained anion gap metabolic acidosis. The likely cause is toxicity from the IV diluent _______. The nurse should also check _______ gap elevation and monitor _______. | Propylene glycol (PG carrier in IV lorazepam and diazepam) \| Osmol gap (PG measurable) \| Renal function (PG nephrotoxicity) \| Management: discontinue IV lorazepam, switch to enteral benzo or alternative sedative \| Threshold: lorazepam >0.1 mg/kg/hr for >48h — monitor proactively |

---

### ORIGINAL: NOTE 1778926634015 — Antifungals: Mucormycosis + Crypto + AmB (HIGH, 7 blanks, chart-l3)

**Learning targets:**
- T1: Mucormycosis = liposomal AmB + surgical debridement
- T2: Crypto meningitis induction = AmB + 5-FC × 2 weeks
- T3: Crypto meningitis consolidation = fluconazole
- T4: Conventional vs liposomal AmB (nephrotoxicity)

| Target # | New Card Type | AACN Domain | CCRN/PCCN | RN Action | Keep Chart? | Proposed Front | Proposed Back |
|---:|---|---|---|---|---|---|---|
| T1 | Chart card | Pharmacology — Antifungals | Moderate / Low | prepare for intervention, monitor | YES | On the antifungal selection chart, mucormycosis requires two simultaneous treatments: _______ amphotericin B AND _______. Importantly, azoles (including voriconazole) and echinocandins are _______ against Mucorales. | Liposomal amphotericin B (3–5 mg/kg/day) \| Surgical debridement — mandatory (necrotic tissue is fungal reservoir; antifungals alone fail) \| NOT active against Mucorales — common dangerous error \| Isavuconazole: salvage only, not first-line |
| T2+T3 | Chart card | Pharmacology — Antifungals | Moderate / Low | monitor, anticipate | YES | Cryptococcal meningitis is treated in two phases: induction with _______ PLUS _______ for _______ weeks, then consolidation with _______. The nursing priority during induction is monitoring for _______. | AmB + flucytosine (5-FC) × 2 weeks \| Fluconazole consolidation \| Monitor: AmB nephrotoxicity (K+, Mg2+, creatinine — prehydrate), elevated ICP (cryptococcal meningitis often causes dangerously high ICP — serial LPs may be needed), 5-FC bone marrow suppression (CBC) |
| T4 | Regular card (no chart) | Pharmacology — Antifungals | Moderate / Low | monitor, prevent harm | NO | Liposomal amphotericin B is preferred over conventional amphotericin B primarily because of lower _______. Both formulations have equivalent _______. Before any amphotericin B infusion, the nurse should _______. | Nephrotoxicity (lipid formulation reduces drug delivery to renal tubules) \| Antifungal efficacy \| Prehydrate with 500–1000 mL NS; monitor BMP (K+, Mg2+, Cr) \| Both formulations: infusion reactions common (rigors, fever, chills) — premedicate with acetaminophen ± diphenhydramine |

---

### ORIGINAL: NOTE 1778926634018 — MRSA: Vancomycin AUC + Daptomycin CI + ZEPHyR (HIGH, 7 blanks, chart-l1)

**Learning targets:**
- T1: Vancomycin monitored by AUC/MIC
- T2: AUC target 400–600
- T3: Daptomycin contraindicated for lung infections — surfactant inactivation
- T4: ZEPHyR trial — linezolid superior to vancomycin for MRSA VAP
- T5: ZEPHyR cure rates (~59% vs ~35%)

| Target # | New Card Type | AACN Domain | CCRN/PCCN | RN Action | Keep Chart? | Proposed Front | Proposed Back |
|---:|---|---|---|---|---|---|---|
| T1+T2 | Chart card | Pharmacology — MRSA / Monitoring | High / Moderate | monitor | YES | Current guidelines recommend monitoring vancomycin by _______ ratio, targeting _______. Trough-only monitoring is now considered inadequate because it _______. | AUC/MIC ratio \| Target 400–600 mg·h/L \| Trough alone underestimates exposure → both nephrotoxicity risk and underdosing possible \| 2020 ASHP/IDSA/SIDP guideline change \| Nursing: report rising creatinine promptly — key trigger for pharmacy AUC recalculation |
| T3 | Chart card | Pharmacology — MRSA / Safety | High / Moderate | differentiate, prevent harm | YES | Daptomycin is contraindicated for MRSA _______ infections because it is inactivated by _______. For MRSA pneumonia, appropriate alternatives include _______ and _______. | Pulmonary (pneumonia) \| Pulmonary surfactant binds daptomycin → inactivates it in the alveoli \| Alternatives: vancomycin, linezolid, ceftaroline \| Critical safety trap: daptomycin covers MRSA bacteremia — nurses may see it ordered and must recognize pneumonia as contraindication |
| T4+T5 | Chart card | Pharmacology — MRSA / Evidence | Moderate / Low | differentiate | YES | The ZEPHyR trial found _______ superior to vancomycin for MRSA VAP, with higher clinical cure rates. The nurse should monitor patients on linezolid for _______ (CBC finding) and signs of _______. | Linezolid \| Thrombocytopenia (monitor CBC) \| Serotonin syndrome risk (especially with concurrent SSRIs, MAOIs) \| ZEPHyR numbers optional: ~59% vs ~35% clinical cure — know linezolid wins for MRSA pneumonia, not the exact percentages |

---

### ORIGINAL: NOTE 1778926634030 — Cardiogenic shock: Dobutamine + Milrinone + IABP + CI target (HIGH, 5 blanks, chart-l2)

**Learning targets:**
- T1: Dobutamine mechanism (β1 + β2 + weak α1) + ↓ SVR
- T2: Milrinone mechanism (PDE3 inhibitor → ↑ cAMP)
- T3: IABP-SHOCK II — IABP did not reduce mortality
- T4: CI target ≥ 2.2 L/min/m²

| Target # | New Card Type | AACN Domain | CCRN/PCCN | RN Action | Keep Chart? | Proposed Front | Proposed Back |
|---:|---|---|---|---|---|---|---|
| T1+T2 | Chart card | Cardiovascular — Cardiogenic shock | High / Moderate | differentiate, monitor | YES | On the cardiogenic shock chart, dobutamine increases CO by stimulating _______ receptors, while milrinone works by inhibiting _______ to increase cAMP. A key clinical advantage of milrinone is that its effect is _______ by concurrent beta-blocker therapy. | β1 (+ β2 + weak α1) receptors \| PDE3 (phosphodiesterase-3) \| NOT blunted — milrinone acts downstream of β receptors \| Dobutamine effect reduced by beta-blockers \| Both: monitor for hypotension, arrhythmia; milrinone has prolonged effect in renal failure (renally cleared) |
| T3+T4 | Chart card | Cardiovascular — Cardiogenic shock | High / Moderate | interpret, evaluate response | YES | In cardiogenic shock, the hemodynamic target for cardiac index is ≥ _______ L/min/m². The IABP-SHOCK II trial showed that IABP _______ 30-day mortality compared to medical therapy alone — changing practice away from routine IABP use. | ≥ 2.2 L/min/m² \| Did NOT reduce (no mortality benefit) \| IABP: still used; nurses must know IABP timing (inflation at dicrotic notch, deflation before systole), counterpulsation physiology, and limb ischemia monitoring |

---

### ORIGINAL: NOTE 1778926634036 — Beta-blockers: Esmolol PK + Aortic Dissection + Variceal Prophylaxis (HIGH, 7 blanks, chart-l1)

**Learning targets:**
- T1: Esmolol half-life (9 min) — plasma esterase metabolism
- T2+T3: Type A dissection targets (HR<60, SBP<120) + add nicardipine
- T4+T5: Non-selective BB for varices — propranolol — β2 reduces portal flow

| Target # | New Card Type | AACN Domain | CCRN/PCCN | RN Action | Keep Chart? | Proposed Front | Proposed Back |
|---:|---|---|---|---|---|---|---|
| T1 | Chart card | Pharmacology — Beta-blockers | High / Moderate | anticipate, monitor | YES | On the beta-blocker comparison chart, esmolol's ultra-short half-life of _______ minutes is due to metabolism by _______. This makes esmolol preferred when _______ of effect is critical. | 9 minutes \| Plasma esterase (red blood cell esterase — no hepatic or renal dependence) \| Rapid on/off — preferred for aortic dissection, rate control with unstable hemodynamics, titration when effect must be quickly reversible |
| T2+T3 | Chart card | Cardiovascular — Hypertensive emergency | High / Moderate | monitor, escalate, prepare for intervention | YES | For type A aortic dissection, the nurse should titrate esmolol to HR _______ bpm and SBP < _______ mmHg. If BP target is not met with esmolol alone, _______ is added. Hydralazine is AVOIDED because _______. | <60 bpm \| <120 mmHg \| Nicardipine (or nitroprusside) \| Reflex tachycardia worsens dissection shear force \| Definitive treatment: emergent surgical repair for Type A |
| T4+T5 | Regular card (no chart) | Pharmacology — Beta-blockers / GI | Moderate / Low | differentiate | NO | Esophageal variceal prophylaxis requires a _______ beta-blocker (e.g., propranolol or carvedilol) rather than a cardioselective one. The reason is that _______ receptor blockade reduces _______, lowering portal pressure. | Non-selective \| β2 \| Splanchnic blood flow (β2 block → splanchnic vasoconstriction → ↓ portal inflow) \| Cardioselective agents (metoprolol, esmolol) block only β1 — insufficient portal pressure reduction |

---

### ORIGINAL: NOTE 1778926634042 — Labetalol + Preeclampsia + BB Contraindications (HIGH, 7 blanks, chart-l3)

**Learning targets:**
- T1: Labetalol — β1+β2+α1, 3:1 ratio oral / 7:1 IV
- T2: First-line for preeclampsia — preferred over nitroprusside (fetal cyanide risk)
- T3: BB absolutely contraindicated in cardiogenic shock
- T4: Relatively contraindicated in asthma/COPD (bronchospasm)

| Target # | New Card Type | AACN Domain | CCRN/PCCN | RN Action | Keep Chart? | Proposed Front | Proposed Back |
|---:|---|---|---|---|---|---|---|
| T1+T2 | Chart card | Cardiovascular — Hypertensive emergency | High / HIGH | monitor, escalate, prevent harm | YES | On the beta-blocker chart, labetalol is first-line for hypertensive emergency in _______ because it _______ (mechanism advantage). Nitroprusside is avoided in this population because _______. | Preeclampsia/eclampsia \| Combined α1+β blockade — reduces BP without reflex tachycardia \| Nitroprusside: fetal cyanide risk from thiocyanate metabolite \| Target: SBP <160, DBP <105 in preeclampsia \| Also watch for: magnesium toxicity (loss of DTRs → respiratory depression) |
| T3+T4 | Chart card | Pharmacology — Beta-blockers / Safety | High / HIGH | differentiate, prevent harm | YES | Beta-blockers are absolutely contraindicated in _______ shock because they _______. They are relatively contraindicated in _______ and _______ because β2 blockade causes _______. | Cardiogenic shock — BB reduce HR and contractility, worsening low output state \| Asthma, COPD — β2 blockade → bronchoconstriction \| Monitor: HR <50, bronchospasm, signs of worsening HF |

---

### ORIGINAL: NOTE 1778973067510 — Vasopressor Algorithm: Vasopressin + Epinephrine Lactate (HIGH, 4 blanks, chart-l1)

**Learning targets:**
- T1: Vasopressin dose (0.03–0.04 units/min fixed)
- T2: When to add (NE ≥ 0.25 mcg/kg/min)
- T3: NOT titrated
- T4: Epinephrine raises lactate via β2 glycolysis — not tissue hypoperfusion

| Target # | New Card Type | AACN Domain | CCRN/PCCN | RN Action | Keep Chart? | Proposed Front | Proposed Back |
|---:|---|---|---|---|---|---|---|
| T1–T3 | Chart card | Cardiovascular — Septic shock | High / Low | monitor, prevent harm | YES | On the vasopressor algorithm chart, vasopressin is added when norepinephrine reaches _______ mcg/kg/min. The dose is fixed at _______ units/min and is _______ (titrated/not titrated). Exceeding _______ units/min risks splanchnic and digital ischemia. | NE ≥ 0.25 mcg/kg/min \| 0.03–0.04 units/min \| NOT titrated (fixed-dose adjunct) \| 0.04 units/min maximum \| V1 receptor mechanism: direct vasoconstriction — no β effects |
| T4 | Chart card | Cardiovascular — Septic shock | High / Low | interpret, differentiate | YES | When epinephrine is used as a vasopressor, serum lactate becomes an unreliable resuscitation marker because epinephrine _______ lactate via _______. The nurse should assess tissue perfusion using _______ instead. | Raises lactate via β2-stimulated aerobic glycolysis in skeletal muscle (NOT from tissue ischemia) \| Use: ScvO₂, urine output, mental status, skin perfusion, MAP trend \| Do not escalate vasopressors based on rising lactate alone when epinephrine is running |

---

### ORIGINAL: NOTE 1778926634009 — Azoles: Mechanism + Fluconazole Spectrum + Voriconazole + Warfarin DDI (MEDIUM, 6 blanks, chart-l1)

| Target # | New Card Type | AACN Domain | CCRN/PCCN | RN Action | Keep Chart? | Proposed Front | Proposed Back |
|---:|---|---|---|---|---|---|---|
| T1+T2 | Chart card | Pharmacology — Antifungals | Moderate / Low | differentiate | YES | On the antifungal chart, azoles work by inhibiting _______, blocking ergosterol synthesis. Fluconazole covers most Candida but is unreliable for _______ (intrinsic) and _______ (variable resistance). | CYP51 (lanosterol 14α-demethylase) \| C. krusei (intrinsic resistance) \| C. glabrata / C. parapsilosis (variable — check susceptibilities) \| Candida auris: often multiresistant — always check susceptibilities |
| T3 | Chart card | Pharmacology — Antifungals | Moderate / Low | monitor | YES | Voriconazole is first-line for _______ in immunocompromised patients. Therapeutic monitoring uses _______ levels. The nurse should assess for voriconazole-specific toxicities every shift: _______ and _______. | Invasive aspergillosis \| Trough levels (target 1–5.5 mcg/mL) \| Visual disturbances (photopsia/phosphenes — ask patient daily) \| Hepatotoxicity (monitor LFTs) \| Also: hallucinations, photosensitivity |
| T4 (warfarin DDI) | DEMOTE — regular note | Pharmacology — DDI | Low / Low | monitor | NO | **Demote** — If kept: "A patient on warfarin is started on fluconazole. The nurse should anticipate INR to _______ and notify the provider to _______ warfarin dose." Answer: increase; reduce. \| Reason for demotion: pharmacist-flagged interaction; nurse's role is INR monitoring (which applies to all azoles + many drugs) — the CYP2C9 mechanism is not CCRN bedside nursing content |

---

### ORIGINAL: NOTE 1778926634012 — Echinocandins: Mechanism + No-Adjust Agent + Coverage Gaps + Candidemia (MEDIUM, 5 blanks, chart-l2)

| Target # | New Card Type | AACN Domain | CCRN/PCCN | RN Action | Keep Chart? | Proposed Front | Proposed Back |
|---:|---|---|---|---|---|---|---|
| T1+T4 | Chart card | Pharmacology — Antifungals | Moderate / Moderate | anticipate | YES | Echinocandins inhibit _______, disrupting the fungal cell wall. IDSA guidelines recommend echinocandins as first-line for candidemia in _______ patients. Step-down to fluconazole is appropriate when the patient is _______ AND cultures confirm susceptibility. | β-1,3-glucan synthase (→ osmotic lysis) \| Critically ill or hemodynamically unstable \| Clinically stable + susceptible organism confirmed + repeat blood cultures negative \| Nursing: monitor IV line site (peripheral OK for short-term candidemia treatment) |
| T2 | Chart card | Pharmacology — Antifungals | Moderate / Low | anticipate, prevent harm | YES | Among the echinocandins, _______ requires NO dose adjustment in renal OR hepatic failure because it is eliminated by _______ rather than organ-dependent metabolism. | Anidulafungin \| Chemical (non-enzymatic) plasma degradation \| Other echinocandins: caspofungin requires hepatic dose adjustment; micafungin — no adjustment needed but long-term hepatotoxicity concern |
| T3 (coverage gaps) | FOLD INTO BACK | — | — | — | — | **Fold into Card 11A back text** — Cryptococcus, Fusarium, Mucorales, Trichosporon gaps are physician-level organism knowledge. Nurses need to know echinocandins don't cover everything; specific organisms are not CCRN content. |

---

### ORIGINAL: NOTE 1778926634024 — De-escalation: HAP/VAP Duration + PCT + PRORATA (MEDIUM, 5 blanks, chart-l3)

**Assessment:** Topics are clinically interconnected (duration + PCT-guided stopping = one workflow). Keep as one card. Demote PRORATA exact numbers to back-of-card optional detail.

| Target # | New Card Type | AACN Domain | CCRN/PCCN | RN Action | Keep Chart? | Proposed Front | Proposed Back |
|---:|---|---|---|---|---|---|---|
| T1+T2 | Chart card (revised, 1 card) | Pharmacology — Antibiotic stewardship | High / Moderate | evaluate response, monitor | YES | IDSA guidelines recommend _______ days of antibiotics for HAP/VAP regardless of organism. A PCT level < _______ mcg/mL OR ↓ by _______ % from peak supports antibiotic discontinuation. | 7 days \| <0.25 mcg/mL OR ↓ ≥80% from peak \| Nursing: trend PCT daily with the team; communicate to provider when threshold is met \| Longer courses do not improve outcomes and increase C. diff risk and resistance |
| T3 (PRORATA trial) | DEMOTE to back text | — | Low / Low | — | — | **Demote** — concept (PCT-guided = shorter, safe) is captured in Card above. Trial name and exact day counts (14.3 vs 11.6 days) are not CCRN bedside nursing content. Include as optional back note only. |

---

### ORIGINAL: NOTE 1778926634033 — Shock Types: Anaphylaxis + Neurogenic Bradycardia + MAP Target (MEDIUM, 4 blanks, chart-l3)

**Three completely different clinical scenarios on one card — all high-yield individually.**

| Target # | New Card Type | AACN Domain | CCRN/PCCN | RN Action | Keep Chart? | Proposed Front | Proposed Back |
|---:|---|---|---|---|---|---|---|
| T1 | Chart card | Multisystem — Anaphylaxis | High / HIGH | prioritize, escalate | YES | A patient develops urticaria, angioedema, and hypotension after receiving IV contrast. The FIRST nursing intervention is _______ given _______ (site and route). IV antihistamines are considered _______ (first-line/adjunct). | Epinephrine 0.3–0.5 mg IM, anterolateral thigh \| Adjunct only \| Call rapid response immediately \| Do NOT delay epinephrine for IV access — mortality from anaphylaxis = delayed epinephrine \| Diphenhydramine and steroids given AFTER epi |
| T2+T3 | Chart card | Multisystem — Neurogenic shock | High / Moderate | differentiate, monitor | YES | A patient with T4 spinal cord injury presents with BP 78/50. Unlike other distributive shock states, neurogenic shock is distinguished by _______ heart rate. The MAP goal is ≥ _______ mmHg to maintain spinal cord perfusion. | Bradycardia or normal HR (paradox — loss of sympathetic tone removes reflex tachycardia; unopposed vagal tone) \| MAP ≥ 85 mmHg (some sources ≥ 90 for 7 days post-injury) \| Treatment: IV fluids + vasopressors (phenylephrine or NE) + atropine for severe bradycardia |

---

### ORIGINAL: NOTE 1778926634039 — Carvedilol + MERIT-HF + Thyroid Storm (MEDIUM, 4 blanks, chart-l2)

| Target # | New Card Type | AACN Domain | CCRN/PCCN | RN Action | Keep Chart? | Proposed Front | Proposed Back |
|---:|---|---|---|---|---|---|---|
| T3 (thyroid storm) | Chart card | Endocrine — Thyroid storm | High / Moderate | differentiate, anticipate | YES | In thyroid storm, _______ is preferred over cardioselective beta-blockers because it also inhibits _______. This provides two simultaneous benefits: controlling _______ and reducing _______. | Propranolol (or carvedilol) \| Peripheral T4→T3 conversion \| Adrenergic symptoms (HR, tremor, agitation, diaphoresis) AND active thyroid hormone level \| Carvedilol acceptable alternative \| Monitor: HR, BP, temperature (antipyretics — avoid ASA, raises free T4); avoid beta-blockers in decompensated HF |
| T1 (carvedilol receptor profile) | DEMOTE | Pharmacology | Low / Low | — | — | **Demote** — β1+β2+α1 profile is covered clinically in other cards (labetalol card, BB contraindications). Isolated receptor-number card is trivia without nursing action attached. |
| T2 (MERIT-HF trial) | REMOVE | — | Low / Low | — | — | **Remove** — MERIT-HF (metoprolol succinate 34% mortality reduction in HFrEF) is cardiologist-level outcome data. The clinical concept (BB reduce mortality in HFrEF) belongs in a HF module note, not an Anki card for CCRN nursing. |

---

## PART 4 — AUDIT VALIDATOR GAP IDENTIFIED

**NOTE 1778926634021** (MERINO trial + ceftazidime-avibactam spectrum) was classified **OK** by the automated audit but contains two independent clinical topics:
- T1: MERINO trial — meropenem superior to pip-tazo for ESBL bacteremia (8.4% vs 12.3% mortality)
- T2: Ceftazidime-avibactam — covers KPC but NOT MBL (metallo-β-lactamase) organisms

**Recommended action:** Flag as MEDIUM. Split into (1) MERINO trial + pip-tazo inoculum concept and (2) ceft-avibactam spectrum gaps. Or demote T1 to a single factoid card and retain T2 as the primary nursing-relevant content (knowing ceft-avibactam doesn't cover Metallo-BL organisms prevents wrong-drug coverage assumptions).

---

## PART 5 — CHUNK 54 NET CARD COUNT ESTIMATE

| Original cards | Cards after splits | Change |
|---|---|---|
| 16 chart notes | ~28 focused cards | +12 net |
| 9 HIGH → ~19 cards | — | — |
| 5 MEDIUM → ~9 cards | — | — |
| 2 OK → 2 cards | — | — |
| 2 DEMOTED/REMOVED from MEDIUM | ~0 | — |

**Cards to REMOVE:** MERIT-HF standalone (1 card)
**Cards to DEMOTE to regular card (no chart):** Lorazepam PG toxicity, variceal BB rationale, AmB formulation comparison, warfarin DDI (4 cards)
**Cards to fold into back text:** Echinocandin coverage gaps, PRORATA trial exact numbers

---

*Do not edit the deck until this plan is reviewed and approved.*
