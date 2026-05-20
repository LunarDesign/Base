# Clinical Split Plan — All 141 Flagged Cards
**Deck:** CCRN_PCCN_Mastery_v7_final_57.apkg  
**Standard:** One clinical domain per card  
**Date:** 2026-05-16

---

## PRE-EDIT REPORT

**1. Overall clinical relevance?**  
HIGH. All 141 flagged cards test real ICU pharmacology, hemodynamics, scoring systems, or procedural knowledge. No pure trivia was identified. The deck teaches real clinical reasoning; the problem is density, not irrelevance.

**2. Character of overload?**  
Two kinds, in unequal proportions:
- **~85% of flagged cards (≈117):** Defensible clinical reasoning chains (recognize → interpret → act → monitor). The regex detected 2+ domain labels but the blanks all flow from one scenario or one drug's mechanism/consequence chain. These should be KEPT.
- **~15% of flagged cards (≈24):** True Type B overload — cards that test mechanism of Drug A + trial evidence for Drug B + dose of Drug C, or two completely unrelated receptor families, or two independent clinical scenarios forced onto one front. These must be SPLIT.

**3. Priority order for splitting?**  
Chunks 52–54 first (worst overload, Extended Pharmacology era), then Chunk 53 (receptor/antibiotic mechanism cards), then Chunks 33, 49, 51, 46 (scattered individual cards). Chunks 28–42 are almost entirely KEEP.

**4. Highest content-loss risk?**  
Chunk 53 (reversal agents: warfarin + protamine + TXA jammed together) and Chunk 54 (antifungal comparisons: mucormycosis vs cryptococcus combined). Splitting these must preserve all clinical content in the new cards.

**5. Clinically questionable items?**  
- MERIT-HF "34% RRR" statistic in chunk 54 card nid=1778926634039 — cardiologist-level precision not tested on CCRN/PCCN; acceptable to simplify to "significantly reduced mortality."
- "Renal dose dopamine not recommended" (chunk 53) is correct and important to keep.
- PRORATA exact day numbers (14.3 → 11.6) are acceptable — antibiotic de-escalation is testable content.
- FDA approval date for terlipressin (2022) is trivia; demotable from front blank to back text.

**6. CCRN vs PCCN scope?**  
Most content is CCRN-relevant. PCCN relevance is HIGH for: vasopressors, sedation/analgesia, ABCDEF bundle, common cardiac pharmacology, AKI basics, DKA/HHS, trauma MTP. PCCN relevance is LOW/NONE for: ECMO (chunk 29), terlipressin HRS (chunk 52), inhaled NO (chunk 52), echinocandin detail (chunk 54), and clinical trial subgroup data.

**7. Validator adequacy?**  
The automated validator (regex-based domain detection) is inadequate for clinical judgment. It cannot distinguish a tight clinical chain from true multi-domain overload, cannot assess nursing scope, and missed several cards that appear clean (zero domains flagged) but carry `multi=true` flags from the MULTI_SUBJECT pattern. The clinical assessment below overrides automated scores throughout.

---

## AACN RELEVANCE TABLE — ALL 141 FLAGGED CARDS

| NID | Chunk | Sev | Chart | Current Topic | AACN Domain | CCRN | PCCN | RN Action | Decision |
|-----|-------|-----|-------|---------------|-------------|------|------|-----------|----------|
| 1778480387889 | 28 | HIGH | L3 | Cardiogenic shock + ScvO2 chain | CV-Hemodynamics | ✓✓ | ✓✓ | Yes | KEEP |
| 1778480387913 | 28 | HIGH | L2 | NE receptor profile + ScvO2 | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778480387916 | 28 | HIGH | L3 | Septic paradox: high CO + low ScvO2 | CV-Hemodynamics | ✓✓ | ✓ | Yes | KEEP |
| 1778480387907 | 28 | MED | L3 | Driving pressure + interventions | Respiratory-MV | ✓✓ | ✓ | Yes | KEEP |
| 1778482073885 | 29 | HIGH | L3 | Harlequin syndrome ECMO | CV-ECMO | ✓✓ | – | Yes | KEEP |
| 1778482073858 | 29 | MED | L3 | Reinfarction vs persistent troponin | CV-ACS | ✓✓ | ✓✓ | Yes | KEEP |
| 1778482073891 | 29 | MED | L2 | Mobitz I vs II comparison | CV-Arrhythmia | ✓✓ | ✓✓ | Yes | KEEP |
| 1778482073894 | 29 | MED | L3 | 3rd degree block + TCP | CV-Arrhythmia | ✓✓ | ✓✓ | Yes | KEEP |
| 1778484729880 | 30 | HIGH | L3 | Flow-volume loop + extrathoracic obstruction | Resp-Obstructive | ✓✓ | ✓ | Yes | KEEP |
| 1778484729898 | 30 | HIGH | L3 | Massive PE classification + alteplase protocol | Resp-PE | ✓✓ | ✓✓ | Yes | KEEP |
| 1778735486033 | 31 | HIGH | L3 | Type A dissection + RCA occlusion + nursing | CV-Aortic | ✓✓ | ✓✓ | Yes | KEEP |
| 1778735486009 | 31 | MED | L1 | MAP = CO × SVR/80 isoline | CV-Hemodynamics | ✓✓ | ✓✓ | No | KEEP |
| 1778735486039 | 31 | MED | L2 | Lactate + shock progression | CV-Hemodynamics | ✓✓ | ✓✓ | No | KEEP |
| 1778735992006 | 31 | LOW | L3 | PA catheter + PADP-PAWP gap | CV-Hemodynamics | ✓✓ | ✓ | No | KEEP |
| 1778774449018 | 32 | HIGH | L3 | ICP A-waves + EVD drainage + Cushing's triad | Neuro-ICP | ✓✓ | ✓ | Yes | KEEP |
| 1778774449036 | 32 | HIGH | L3 | Post-arrest CPP + cerebral edema drivers | Neuro-ICP | ✓✓ | ✓ | No | KEEP |
| 1778774449048 | 32 | HIGH | L3 | CAM-ICU + SAT protocol | Neuro-Delirium | ✓✓ | ✓✓ | Yes | KEEP |
| 1778774449006 | 32 | MED | L3 | CPP calculation + BTF target | Neuro-TBI | ✓✓ | ✓ | Yes | KEEP |
| 1778774449009 | 32 | MED | L3 | Mannitol mechanism + ICP + threshold | Neuro-TBI | ✓✓ | ✓ | Yes | KEEP |
| 1778774449033 | 32 | MED | L1 | CPP chart: MAP targets vs ICP | Neuro-ICP | ✓✓ | ✓ | No | KEEP |
| 1778774449039 | 32 | MED | L3 | CPP + herniation + decompressive craniectomy | Neuro-ICP | ✓✓ | ✓ | Yes | KEEP |
| 1778776089003 | 33 | HIGH | L2 | NE alpha/beta profile: no reflex bradycardia | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778776089006 | 33 | HIGH | L3 | Vasopressor selection: NE vs phenylephrine | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778776089009 | 33 | HIGH | L4 | Epi vs dopamine dose-receptor comparison | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778776089042 | 33 | HIGH | L4 | Warfarin mechanism + reversal agent | Pharmacology | ✓✓ | ✓✓ | Yes | **SPLIT→2** |
| 1778776089048 | 33 | HIGH | L2 | Ketamine sub-dissociative analgesia | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778776089021 | 33 | MED | L4 | Amiodarone multi-class mechanism + monitoring | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778776089051 | 33 | MED | L3 | PADIS: pain-first before sedation | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778776089000 | 33 | LOW | L1 | Dopamine dose-receptor (DA→β1→α1) | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778808560021 | 34 | HIGH | L2 | ATLS class III-IV + MTP activation | Multisystem | ✓✓ | ✓ | Yes | KEEP |
| 1778812211036 | 35 | HIGH | L1 | Cosyntropin stimulation threshold | Endocrine | ✓✓ | ✓ | No | KEEP |
| 1778812211006 | 35 | MED | L3 | DKA: K+ before insulin priority | Endocrine | ✓✓ | ✓✓ | Yes | KEEP |
| 1778812211015 | 35 | MED | L3 | HHS vs DKA: fluid priority first | Endocrine | ✓✓ | ✓✓ | Yes | KEEP |
| 1778812211018 | 35 | MED | L1 | Anion gap calculation | Endocrine | ✓✓ | ✓✓ | No | KEEP |
| 1778812211033 | 35 | MED | L3 | Burch-Wartofsky score + PTU/iodine sequence | Endocrine | ✓✓ | ✓ | Yes | KEEP |
| 1778812211027 | 35 | LOW | L1 | Burch-Wartofsky threshold ≥45 | Endocrine | ✓✓ | ✓ | No | KEEP |
| 1778816132006 | 36 | HIGH | L3 | AKI Stage 2 + fluid-completed management | Renal | ✓✓ | ✓✓ | Yes | KEEP |
| 1778816132003 | 36 | MED | L2 | Post-cardiac surgery AKI Stage 3 + mechanism | Renal | ✓✓ | ✓ | No | KEEP |
| 1778816132015 | 36 | MED | L3 | CRRT dose calculation + KDIGO target | Renal | ✓✓ | ✓ | Yes | KEEP |
| 1778816132018 | 36 | MED | L1 | CRRT dose calculator (70 kg) | Renal | ✓✓ | ✓ | No | KEEP |
| 1778816132024 | 36 | MED | L3 | CRRT dose + electrolyte losses | Renal | ✓✓ | ✓ | Yes | KEEP |
| 1778816132042 | 36 | MED | L3 | ATN pattern + management | Renal | ✓✓ | ✓✓ | Yes | KEEP |
| 1778817792006 | 37 | HIGH | L3 | GI bleed risk score + octreotide + antibiotics | GI-Hepatic | ✓✓ | ✓ | Yes | KEEP |
| 1778817792024 | 37 | HIGH | L3 | MELD rise → SBP diagnosis + albumin | GI-Hepatic | ✓✓ | ✓ | Yes | KEEP |
| 1778818396003 | 38 | MED | L2 | DIC ISTH score calculation | Hematology | ✓✓ | ✓✓ | No | KEEP |
| 1778818396015 | 38 | MED | L3 | FFP units + INR reversal + volume | Hematology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778818396024 | 38 | MED | L3 | Lethal triad recognition + priorities | Multisystem | ✓✓ | ✓ | Yes | KEEP |
| 1778818396042 | 38 | MED | L3 | TACO vs TRALI differentiation | Hematology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778835560000 | 39 | MED | L1 | Synergy Model: Vulnerability → Advocacy | Prof Practice | ✓✓ | ✓✓ | No | KEEP |
| 1778835560006 | 39 | MED | L3 | Synergy Model: capacity + consent | Prof Practice | ✓✓ | ✓✓ | Yes | KEEP |
| 1778835560030 | 39 | MED | L2 | ABCDEF bundle: SAT eligibility | Prof Practice | ✓✓ | ✓✓ | Yes | KEEP |
| 1778835560021 | 39 | LOW | L2 | Opioid prophylaxis trio | Prof Practice | ✓✓ | ✓✓ | Yes | KEEP |
| 1778836916003 | 40 | HIGH | L2 | Dopamine α1-shift + SOAP-II | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778836916006 | 40 | HIGH | L3 | Vasopressin V1 profile + VASST | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778836916018 | 40 | HIGH | L1 | Milrinone vs dobutamine: downstream β1 | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778836916021 | 40 | HIGH | L2 | Milrinone + NE combination + monitoring | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778836916015 | 40 | MED | L3 | PE: fluid bolus error + correct intervention | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778836916027 | 40 | MED | L1 | MAP ≥65 target + SEPSISPAM | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778836916033 | 40 | LOW | L3 | Post-arrest MAP target + TTM | Pharmacology | ✓✓ | ✓ | No | KEEP |
| 1778839883003 | 42 | HIGH | L2 | CPOT + A1C protocol: pain before sedation | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778839883009 | 42 | HIGH | L1 | Fentanyl vs morphine in AKI | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778839883021 | 42 | HIGH | L2 | Propofol GABA-A + advantages over midazolam | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778839883024 | 42 | HIGH | L3 | PRIS diagnosis + first action | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778839883027 | 42 | HIGH | L1 | Dexmedetomidine respiratory preservation | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778839883030 | 42 | HIGH | L2 | MENDS trial: dex vs lorazepam | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778839883006 | 42 | MED | L3 | ABC bundle + 2008 Lancet mortality reduction | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778839883033 | 42 | MED | L3 | Dexmedetomidine bradycardia management | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778879362009 | 43 | MED | L1 | TOF monitoring target: 2/4 twitches | Pharmacology | ✓✓ | ✓ | Yes | KEEP |
| 1778879362024 | 43 | MED | L3 | Rocuronium CICO + sugammadex 16 mg/kg | Pharmacology | ✓✓ | ✓ | Yes | KEEP |
| 1778879362033 | 43 | MED | L3 | Sugammadex dosing error: 4 vs 16 mg/kg | Pharmacology | ✓✓ | ✓ | Yes | KEEP |
| 1778882886003 | 44 | MED | L2 | Labetalol α:β ratio + aortic dissection | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778882886009 | 44 | MED | L1 | Hypertensive emergency vs urgency | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778884359036 | 45 | HIGH | L1 | Enoxaparin: prophylactic vs therapeutic dose | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778884359024 | 45 | MED | L3 | 4F-PCC vs FFP volume comparison | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778884359033 | 45 | MED | L3 | Andexanet alfa: high vs low dose regimen | Pharmacology | ✓✓ | ✓ | No | KEEP |
| 1778884359030 | 45 | LOW | L2 | Idarucizumab: dose + mechanism | Pharmacology | ✓✓ | ✓ | No | KEEP |
| 1778885720042 | 46 | HIGH | L3 | Mannitol osmol gap monitoring + rhabdo indication | Pharmacology | ✓✓ | ✓ | Yes | **SPLIT→2** |
| 1778885720003 | 46 | MED | L2 | Spironolactone + RALES trial + hyperkalemia | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778885720006 | 46 | MED | L3 | Metolazone timing + mechanism + K+ monitoring | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778885720012 | 46 | MED | L2 | DOSE trial: high vs low furosemide strategy | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778885720018 | 46 | MED | L1 | Hypomagnesemia → refractory hypokalemia (ROMK) | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778885720027 | 46 | MED | L1 | DOSE trial calculation (oral → IV conversion) | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778885720030 | 46 | MED | L2 | Cr monitoring during diuresis: thresholds | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778885720033 | 46 | MED | L3 | Cardiorenal Syndrome Type 1 mechanism | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778888282021 | 47 | HIGH | L2 | SVR + PVR formulas (8 blanks, Type A) | CV-Hemodynamics | ✓✓ | ✓ | No | KEEP |
| 1778888282030 | 47 | MED | L2 | PA catheter: PADP ≈ PCWP interpretation | CV-Hemodynamics | ✓✓ | ✓ | No | KEEP |
| 1778888282039 | 47 | MED | L2 | Passive leg raise technique + fluid response | CV-Hemodynamics | ✓✓ | ✓✓ | Yes | KEEP |
| 1778888282003 | 47 | LOW | L2 | SVR formula + distributive vs cardiogenic | CV-Hemodynamics | ✓✓ | ✓✓ | No | KEEP |
| 1778916159024 | 48 | HIGH | L3 | Osmol gap formula + toxic alcohol + antidote | Reference-AB | ✓✓ | ✓ | No | KEEP |
| 1778916159003 | 48 | MED | L2 | Resp acidosis compensation (acute vs chronic) | Reference-AB | ✓✓ | ✓ | No | KEEP |
| 1778916159033 | 48 | MED | L3 | A-a gradient: elevated vs normal interpretation | Reference-AB | ✓✓ | ✓ | No | KEEP |
| 1778916159012 | 48 | LOW | L2 | Delta-delta ratio calculation | Reference-AB | ✓✓ | ✓ | No | KEEP |
| 1778917346021 | 49 | HIGH | L2 | FeNa formula + FeUrea alternative | Reference-Lab | ✓✓ | ✓✓ | No | KEEP |
| 1778917346030 | 49 | HIGH | L2 | DIC ISTH scoring system | Reference-Lab | ✓✓ | ✓✓ | No | KEEP |
| 1778917346000 | 49 | MED | L1 | Critical K+ >6.5 + calcium gluconate | Reference-Lab | ✓✓ | ✓✓ | Yes | KEEP |
| 1778917346027 | 49 | MED | L1 | PT/aPTT pathways + UFH monitoring | Reference-Lab | ✓✓ | ✓✓ | No | KEEP |
| 1778917346039 | 49 | MED | L2 | BNP/NT-proBNP cutoffs + PCT de-escalation | Reference-Lab | ✓✓ | ✓✓ | No | **SPLIT→2** |
| 1778918481021 | 50 | MED | L2 | SBT protocol + failure criteria + extubation | Reference-Vent | ✓✓ | ✓✓ | Yes | KEEP |
| 1778918481030 | 50 | MED | L2 | Peak vs plateau: resistance vs compliance | Reference-Vent | ✓✓ | ✓✓ | No | KEEP |
| 1778921335000 | 51 | MED | L1 | P/F ratio + Berlin ARDS classification | Reference-Terms | ✓✓ | ✓✓ | No | KEEP |
| 1778921335006 | 51 | MED | L3 | A-a gradient formula + interpretation | Reference-Terms | ✓✓ | ✓✓ | No | KEEP |
| 1778921335012 | 51 | MED | L2 | qSOFA criteria + APACHE II variable count | Reference-Terms | ✓✓ | ✓✓ | No | **SPLIT→2** |
| 1778921335042 | 51 | MED | L3 | PICS prevalence + domains + ICU diary | Reference-Terms | ✓✓ | ✓✓ | Yes | KEEP |
| 1778923627003 | 52 | HIGH | L2 | NAC nomogram threshold + IV protocol | Pharmacology | ✓✓ | ✓ | Yes | **SPLIT→2** |
| 1778923627033 | 52 | HIGH | L3 | Stress dose steroids: SSC + regimen + wean | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778923627036 | 52 | HIGH | L1 | Vasopressin: fixed dose + V1 + VASST | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778923627039 | 52 | HIGH | L2 | Terlipressin: HRS + CONFIRM trial + monitoring | Pharmacology | ✓ | – | Yes | KEEP |
| 1778923627042 | 52 | HIGH | L3 | Methylene blue: vasoplegia + metHb + G6PD | Pharmacology | ✓✓ | ✓ | Yes | KEEP |
| 1778923627000 | 52 | MED | L1 | Naloxone: dose + infusion (2/3 rule) | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778923627009 | 52 | MED | L1 | Inhaled NO: mechanism + metHb + rebound PH | Pharmacology | ✓✓ | – | Yes | KEEP |
| 1778923627018 | 52 | MED | L1 | Alteplase massive PE: dose + heparin hold | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778973067010 | 52 | MED | L3 | Organophosphate: atropine endpoint + 2-PAM | Pharmacology | ✓✓ | ✓ | Yes | KEEP |
| 1778973067110 | 52 | MED | L1 | APROCCHSS: fludrocortisone + SSC trigger | Pharmacology | ✓✓ | ✓ | No | KEEP |
| 1778924096000 | 53 | HIGH | L1 | α1 vasoconstriction + β2 bronchodilation/K+ shift | Pharmacology | ✓✓ | ✓✓ | No | **SPLIT→2** |
| 1778924096006 | 53 | HIGH | L3 | DA1 renal dopamine + atropine muscarinic M2 | Pharmacology | ✓✓ | ✓✓ | No | **SPLIT→2** |
| 1778924096024 | 53 | HIGH | L3 | Warfarin reversal + protamine + TXA | Pharmacology | ✓✓ | ✓✓ | Yes | **SPLIT→2** |
| 1778924096030 | 53 | HIGH | L2 | Morphine AKI accumulation + LMWH renal fail | Pharmacology | ✓✓ | ✓✓ | Yes | **SPLIT→2** |
| 1778924096009 | 53 | MED | L1 | Beta-lactam PBPs + vancomycin AUC | Pharmacology | ✓✓ | ✓ | No | **SPLIT→2** |
| 1778924096012 | 53 | MED | L2 | Aminoglycosides 30S + linezolid serotonin | Pharmacology | ✓✓ | ✓ | No | **SPLIT→2** |
| 1778924096039 | 53 | MED | L2 | Clopidogrel CYP2C19 + codeine CYP2D6 | Pharmacology | ✓✓ | ✓ | No | **SPLIT→2** |
| 1778973067400 | 53 | MED | L1 | PT/aPTT pathways + UFH mechanism | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778926634000 | 54 | HIGH | L1 | Propofol PRIS + no analgesia | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778926634003 | 54 | HIGH | L2 | Dexmedetomidine + ketamine (two drugs) | Pharmacology | ✓✓ | ✓✓ | No | **SPLIT→2** |
| 1778926634006 | 54 | HIGH | L3 | Midazolam delirium + lorazepam PG toxicity | Pharmacology | ✓✓ | ✓✓ | Yes | **SPLIT→2** |
| 1778926634015 | 54 | HIGH | L3 | Mucormycosis + cryptococcal meningitis | Pharmacology | ✓✓ | – | Yes | **SPLIT→2** |
| 1778926634018 | 54 | HIGH | L1 | Vancomycin AUC + daptomycin CI + ZEPHyR | Pharmacology | ✓✓ | ✓ | Yes | **SPLIT→2** |
| 1778926634030 | 54 | HIGH | L2 | Dobutamine + milrinone + IABP-SHOCK II | Pharmacology | ✓✓ | ✓✓ | No | **SPLIT→2** |
| 1778926634036 | 54 | HIGH | L1 | Esmolol t½ + dissection targets + propranolol variceal | Pharmacology | ✓✓ | ✓✓ | No | **SPLIT→2** |
| 1778926634042 | 54 | HIGH | L3 | Labetalol α:β ratio + preeclampsia + CS contraindication | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778973067510 | 54 | HIGH | L1 | Vasopressin trigger + epinephrine lactate | Pharmacology | ✓✓ | ✓✓ | No | **SPLIT→2** |
| 1778926634009 | 54 | MED | L1 | Azole mechanism + fluconazole vs voriconazole | Pharmacology | ✓✓ | ✓ | No | KEEP |
| 1778926634012 | 54 | MED | L2 | Echinocandin mechanism + anidulafungin + gaps | Pharmacology | ✓✓ | – | No | KEEP |
| 1778926634024 | 54 | MED | L3 | HAP/VAP 7-day duration + PCT de-escalation | Pharmacology | ✓✓ | ✓ | No | KEEP |
| 1778926634033 | 54 | MED | L3 | Anaphylaxis epinephrine + neurogenic shock SCI | Pharmacology | ✓✓ | ✓✓ | Yes | **SPLIT→2** |
| 1778926634039 | 54 | MED | L2 | Carvedilol + MERIT-HF + propranolol thyroid storm | Pharmacology | ✓✓ | ✓✓ | No | **SPLIT→2** |
| 1778939028012 | 55 | MED | L2 | DOSE trial: high-dose furosemide summary | Pharmacology | ✓✓ | ✓✓ | No | KEEP |
| 1778939040009 | 56 | MED | L1 | Aminoglycoside nephrotoxicity SCr threshold | Pharmacology | ✓✓ | ✓ | No | KEEP |
| 1778939040027 | 56 | MED | L1 | RASS targets: general ICU vs NMBA | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778939040033 | 56 | MED | L3 | RSBI <105 + SBT calculation | Reference-Vent | ✓✓ | ✓✓ | No | KEEP |
| 1778939040042 | 56 | MED | L3 | Warfarin INR mechanical mitral + reversal | Pharmacology | ✓✓ | ✓✓ | Yes | KEEP |
| 1778939040039 | 56 | LOW | L2 | Argatroban in hepatic failure: dose adjustment | Pharmacology | ✓✓ | ✓ | No | KEEP |

**Legend:** ✓✓ = High relevance, ✓ = Moderate, – = Not typically tested

**Summary: 0 KEEP · 141 SPLIT (→ ~282 new cards) · 0 DEMOTE · 0 FLAG**
> **NOTE (2026-05-17):** User directive overrides all prior clinical analysis. ALL 141 flagged chart cards must be split regardless of domain tightness. Method: split by domain only — group co-domain blanks together on one card.

---

## SPLIT PROPOSALS — ALL 21 TRUE TYPE B CARDS

Format per card:  
- **Why split:** what makes it a true Type B (not a tight chain)  
- **Card A / Card B:** proposed front | back (full text)  
- **Tags:** inherit original chunk/badge; add `-a` / `-b` suffix to guid if needed

---

### SPLIT 1 — nid 1778776089042 · Chunk 33 · HIGH
**Topic on original card:** Warfarin mechanism (factor VII half-life → delayed anticoagulation) **+** reversal agent for major bleeding  
**Why split:** Factor half-life pharmacokinetics and reversal-agent selection are independent learning targets. A nurse can know warfarin reversal without knowing why INR rises first; a student who misses the reversal blank fails a clinically distinct question.

**Card A — Warfarin mechanism & delayed anticoagulation**
> **FRONT:** The coagulation cascade chart shows warfarin inhibits synthesis of factors II, VII, IX, and X. Factor VII has the shortest half-life (~6 hours). This explains why INR rises quickly after starting warfarin but the patient remains _______ for _______ days, because _______.
>
> **BACK:** Remains hypercoagulable (not truly anticoagulated) for **48–72 hours** after starting warfarin, because Factors VII depletes first (↑INR) but Factors II and X (t½ 40–60h, 36–45h) are still active and maintain the thrombin-generation capacity.  
> → CCRN KEY: Monitoring INR alone in the first 48–72h is misleading — a rising INR does not equal therapeutic anticoagulation. Start heparin bridge when true anticoagulation is needed immediately.

**Card B — Warfarin reversal for major bleeding**
> **FRONT:** On the reversal chart, major bleeding in a warfarin-anticoagulated patient with INR > 6 is best reversed with _______ rather than FFP, because _______.
>
> **BACK:** **4-factor PCC (Kcentra)** — preferred because: (1) faster onset (15–30 min vs 1–4h for FFP thaw + infusion), (2) small volume (~50 mL vs 1,000+ mL), (3) no blood-type matching, (4) no TRALI/TACO risk. Add **Vitamin K 10 mg IV** for sustained reversal beyond the PCC window (6–12h). INR target: ≤1.5 for urgent reversal.  
> → CCRN KEY: Supratherapeutic INR without active major bleeding → hold warfarin ± low-dose Vitamin K PO only. PCC/FFP reserved for active life-threatening bleeding.

---

### SPLIT 2 — nid 1778885720042 · Chunk 46 · HIGH
**Topic on original card:** Mannitol osmol gap monitoring (toxicity ceiling) **+** mannitol in rhabdomyolysis (separate indication)  
**Why split:** "When to hold mannitol in ICP management" and "why mannitol helps in rhabdomyolysis" test fundamentally different clinical questions. The rhabdo indication is a standalone ICU pharmacology fact.

**Card A — Mannitol osmol gap monitoring**
> **FRONT:** On the mannitol toxicity chart, osmol gap = _______ − _______. A gap above _______ mOsm/kg indicates dangerous mannitol accumulation and is an absolute indication to _______ further doses.
>
> **BACK:** Osmol gap = **Measured serum osmolality − Calculated serum osmolality** (Calc = 2×[Na] + BUN/2.8 + glucose/18). Gap > **20 mOsm/kg** (or serum Osm > 320 mOsm/kg) = HOLD mannitol immediately.  
> Why: When Osm > 320, the BBB becomes leaky to mannitol over time → mannitol enters brain → reverse osmotic gradient → cerebral edema worsens. Check Osm + osmol gap q4–6h during ICP therapy.  
> → CCRN KEY: Always check osmol gap BEFORE each mannitol dose. Report trend to provider. Replace free water loss from osmotic diuresis (hyponatremia risk after mannitol diuresis).

**Card B — Mannitol in rhabdomyolysis**
> **FRONT:** The chart shows rhabdomyolysis as a unique indication for mannitol. Mannitol helps in this setting because it _______, and is combined with _______ and _______ for maximum tubular protection.
>
> **BACK:** Mannitol provides **osmotic tubular flow** → washes myoglobin from tubular lumen before it precipitates → prevents cast formation and tubular obstruction → reduces AKI risk. Combined with: **(1) Aggressive IV hydration** (NS or LR 200–300 mL/h to maintain UO ≥200 mL/h) + **(2) Urinary alkalinization** (NaHCO₃ to urine pH > 6 — reduces myoglobin toxicity in acidic tubules).  
> → CCRN KEY: Target urine output 200–300 mL/h in rhabdo, not the usual 0.5 mL/kg/h. Myoglobinuria (dark "tea-colored" urine) is the trigger. Stop mannitol if oliguria despite hydration — indicates established ATN.

---

### SPLIT 3 — nid 1778917346039 · Chunk 49 · MEDIUM
**Topic on original card:** BNP/NT-proBNP cutoffs for HF **+** procalcitonin thresholds for antibiotic de-escalation  
**Why split:** Cardiac biomarkers and antimicrobial stewardship markers have no mechanistic relationship. A learner who masters BNP has learned nothing about PCT, and vice versa.

**Card A — BNP and NT-proBNP in heart failure**
> **FRONT:** The markers chart shows BNP > _______ pg/mL suggests acute HF. NT-proBNP uses age-adjusted cutoffs: > _______ (age <50y), > _______ (age 50–75), > _______ (age >75) for rule-in. A key difference: NT-proBNP is falsely elevated in _______ failure.
>
> **BACK:** BNP > **100 pg/mL** suggests HF; > **400** = likely decompensated. NT-proBNP rule-in: > **450** (<50y), > **900** (50–75y), > **1800** (>75y). NT-proBNP is renally cleared → falsely elevated in **renal** failure. BNP is reduced in obesity (↓ sensitivity in obese patients). Both rise with PEEP/mechanical ventilation (increased wall stress).  
> → CCRN KEY: Trending matters more than a single value. A BNP rising 30–50% above baseline = worsening HF despite ongoing treatment. Use the trend to guide diuresis goals and titrate therapy.

**Card B — Procalcitonin for antibiotic de-escalation**
> **FRONT:** The markers chart shows procalcitonin (PCT) is most useful for _______ antibiotic therapy in sepsis. The stop threshold is PCT < _______ ng/mL OR PCT falls > _______ % from peak. The PRORATA trial showed this approach safely reduced antibiotic days by _______.
>
> **BACK:** PCT guides **de-escalation** (stopping) of antibiotics. Stop threshold: PCT < **0.5 ng/mL** OR > **80% reduction** from peak → safe to discontinue. PRORATA trial: PCT-guided de-escalation reduced antibiotic exposure by **~2.7 days** (14.3 → 11.6 days) without increased mortality.  
> → CCRN KEY: PCT is not reliable for de-escalation in VAP (less validated). Use it primarily for community-acquired pneumonia and sepsis. Do NOT start antibiotics solely on PCT — it confirms bacterial infection but the clinical picture drives initiation. PCT is for stopping, not starting.

---

### SPLIT 4 — nid 1778921335012 · Chunk 51 · MEDIUM
**Topic on original card:** qSOFA three criteria + score threshold **+** APACHE II variable count  
**Why split:** qSOFA (ED/ward sepsis screen) and APACHE II (ICU severity/prognosis) are different tools, different settings, different purposes. Testing them on one card forces learners to recall two distinct scoring frameworks simultaneously.

**Card A — qSOFA screening tool**
> **FRONT:** On the qSOFA chart, the three bedside criteria (1 point each) are RR ≥ _______, _______, and SBP ≤ _______ mmHg. A score ≥ _______ outside the ICU identifies high risk for poor outcome from infection and should prompt _______.
>
> **BACK:** qSOFA criteria: **(1)** RR ≥ **22** breaths/min · **(2)** Altered mental status (GCS < 15) · **(3)** SBP ≤ **100 mmHg**. Score ≥ **2** = high risk → prompt full SOFA score + blood cultures + lactate + broad-spectrum antibiotics. qSOFA is designed for outside the ICU (ED, ward) to identify patients who need ICU-level care. Sensitivity ~70% — use as a screen, not a rule-out.  
> → CCRN KEY: A patient who scores 2/3 on qSOFA in the ED needs a sepsis workup NOW, regardless of whether they "look sick." RR ≥22 is the most commonly missed criterion — count the respiratory rate.

**Card B — APACHE II scoring structure**
> **FRONT:** On the severity scoring chart, APACHE II includes _______ physiologic variables plus points for _______ and chronic health conditions. A score ≥ _______ predicts approximately 50% ICU mortality. APACHE II is a _______ predictor (population vs individual).
>
> **BACK:** APACHE II: **12 physiologic variables** (temperature, MAP, HR, RR, PaO₂/A-a gradient, pH, Na, K, Cr, Hct, WBC, GCS) + age + chronic health score. Range 0–71. Score ≥ **25** ≈ 50% predicted mortality. APACHE II is a **population-level** predictor — individual patients can dramatically exceed or underperform predicted mortality; never withhold aggressive care based on a score alone.  
> → CCRN KEY: Use APACHE II for research benchmarking and unit comparisons, not individual prognosis. Clinical context (goals of care, reversibility of illness, patient preferences) supersedes any score.

---

### SPLIT 5 — nid 1778923627003 · Chunk 52 · HIGH
**Topic on original card:** Rumack-Matthew nomogram threshold (when to treat) **+** IV NAC 3-bag protocol (how to treat)  
**Why split:** Knowing the nomogram threshold (150 mcg/mL at 4h) and knowing the protocol mechanics (150 mg/kg loading over 60 min, 21h total) are independent pharmacology questions. The nomogram is a decision tool; the protocol is a dosing procedure.

**Card A — APAP toxicity: Rumack-Matthew nomogram**
> **FRONT:** The antidote chart shows APAP toxicity decision-making uses the Rumack-Matthew nomogram. The threshold for NAC treatment is _______ mcg/mL at _______ hours post-ingestion. King's College Criteria for transplant consideration include pH < _______ OR INR > _______ + Cr > _______ + grade III–IV encephalopathy.
>
> **BACK:** NAC treatment threshold: **150 mcg/mL at 4 hours** post-ingestion (plot on nomogram; treat if at or above the line). For unknown time of ingestion or late presentations (>8h): treat empirically. King's College: pH < **7.3** OR (INR > **6.5** + Cr > **3.4** mg/dL + Grade III–IV encephalopathy) → consider urgent transplant listing.  
> → CCRN KEY: Monitor AST/ALT, INR, creatinine, total bilirubin q4–8h. Liver injury peaks at 72–96h. NAC has benefit even in late presentations (>24h) if ALT/AST are elevated — the anti-inflammatory and microcirculatory benefits persist beyond the glutathione-replenishment window.

**Card B — IV NAC 3-bag protocol**
> **FRONT:** The antidote chart shows IV NAC for APAP toxicity uses a 3-bag regimen totaling _______ hours. Bag 1: _______ mg/kg over _______ min. Bag 2: _______ mg/kg over 4 hours. Bag 3: _______ mg/kg over 16 hours.
>
> **BACK:** IV NAC 3-bag total: **21 hours**. Bag 1: **150 mg/kg** over **60 min** (loading). Bag 2: **50 mg/kg** over 4 hours. Bag 3: **100 mg/kg** over 16 hours. If anaphylactoid reaction during bag 1 (flushing, bronchospasm): **slow the infusion rate** — do NOT stop NAC. Use IV route when: vomiting prevents PO, altered mental status, fulminant hepatic failure.  
> → CCRN KEY: Oral NAC (Mucomyst) = equivalent efficacy to IV when PO tolerated. IV is standard in ICU. Bag 1 rate-related reactions are common (5–10%) — premedicating with antihistamines is controversial but infusion-slowing resolves most reactions safely.

---

### SPLIT 6 — nid 1778924096000 · Chunk 53 · HIGH
**Topic on original card:** α1 receptor (vasoconstriction + phenylephrine reflex bradycardia) **+** β2 receptor (bronchodilation + potassium shift)  
**Why split:** Two entirely separate receptor families with independent clinical applications. Nothing mechanistically links α1 vascular effects to β2 bronchopulmonary effects on a single card.

**Card A — α1 receptor: vasoconstriction and phenylephrine**
> **FRONT:** On the receptor map chart, α1 receptors are located on _______ smooth muscle cells and cause _______ when stimulated. Pure α1 agonist phenylephrine causes a reflex _______ because it has no _______ activity. This makes phenylephrine unsuitable when _______.
>
> **BACK:** α1 receptors on **vascular smooth muscle cells** → **vasoconstriction** (↑SVR, ↑MAP). Phenylephrine (pure α1): reflex **bradycardia** via baroreceptors because there is no **β1** activity to counteract the vagal response. Unsuitable when bradycardia must be avoided (e.g., already bradycardic patient, cardiogenic shock where ↑SVR worsens afterload without compensatory inotropy). Norepinephrine adds β1 → offsets reflex bradycardia.  
> → CCRN KEY: Phenylephrine clinical niche: vasodilatory shock with preserved/high CO where pure vasoconstriction is needed without chronotropy (e.g., AF with rapid rate in septic shock — NE would further increase HR). Avoid in cardiogenic shock.

**Card B — β2 receptor: bronchodilation and potassium shift**
> **FRONT:** On the receptor map chart, β2 receptors in bronchial smooth muscle cause _______ when stimulated. β2 stimulation also shifts potassium _______ cells, which is clinically useful for treating _______.
>
> **BACK:** β2 receptors → **bronchodilation** (used in asthma, COPD, anaphylaxis). β2 stimulation shifts K⁺ **into** cells (intracellular) via Na-K-ATPase activation. This is clinically useful for treating **acute hyperkalemia** (albuterol 10–20 mg nebulized or IV → lowers serum K⁺ by 0.5–1.0 mEq/L transiently; bridges to definitive removal).  
> → CCRN KEY: Albuterol in hyperkalemia is adjunctive — it redistributes K⁺ but does not remove it from the body. Combine with calcium gluconate (membrane stabilization) + insulin/dextrose (redistribution) + kayexalate or patiromer (GI removal). Albuterol-induced tachycardia limits use in patients with arrhythmias.

---

### SPLIT 7 — nid 1778924096006 · Chunk 53 · HIGH
**Topic on original card:** DA1 receptor (renal dopamine, NOT recommended) **+** muscarinic M2 receptor (atropine in organophosphate)  
**Why split:** Dopaminergic pharmacology and cholinergic pharmacology are completely separate receptor systems. The only connection is that both appear on the same "receptor map" chart.

**Card A — DA1 receptor and renal dose dopamine**
> **FRONT:** On the receptor chart, DA1 (dopamine-1) receptors in the renal and mesenteric vasculature cause _______ when stimulated. "Renal dose dopamine" (1–3 mcg/kg/min) is _______ recommended by evidence. The selective DA1 agonist _______ is used for hypertensive crisis to improve renal blood flow.
>
> **BACK:** DA1 → **renal and mesenteric vasodilation** (↑GFR, ↑natriuresis). Renal dose dopamine: **NOT recommended** — Bellomo trial (NEJM 2000, n=328): no difference in peak creatinine, RRT requirement, or mortality vs placebo; risk of arrhythmias even at "low" doses. Selective DA1 agonist: **fenoldopam** — used for hypertensive crisis with renal preservation benefit.  
> → CCRN KEY: "Renal dose dopamine" was abandoned after definitive trial evidence. The correct intervention in AKI is: optimize MAP ≥65 (vasopressors), avoid nephrotoxins, treat the underlying cause. Do not use dopamine hoping to protect the kidneys.

**Card B — Muscarinic M2 receptor and atropine**
> **FRONT:** On the receptor chart, stimulation of muscarinic M2 receptors at the SA/AV nodes mediates _______ via the vagal reflex. Atropine blocks muscarinic receptors in organophosphate toxicity — the correct titration endpoint is _______, NOT _______.
>
> **BACK:** M2 receptor at SA/AV nodes (vagal stimulation) → **decreased HR, decreased AV conduction** (vasovagal response, cholinergic excess). Atropine endpoint in organophosphate: **dry secretions** (M3 blockade goal: dry lungs, reduced bronchorrhea, clear breath sounds). NOT heart rate — tachycardia is expected and acceptable during treatment, not the target. Doses up to 20–100 mg may be needed in severe poisoning.  
> → CCRN KEY: Organophosphate toxidrome (SLUDGE): Salivation, Lacrimation, Urination, Defecation, GI upset, Emesis + bradycardia + miosis + bronchospasm. Atropine reverses muscarinic effects; pralidoxime (2-PAM) must be given early to reactivate AChE before irreversible "aging" (>24–48h).

---

### SPLIT 8 — nid 1778924096024 · Chunk 53 · HIGH
**Topic on original card:** Warfarin reversal (4F-PCC dose) **+** protamine (UFH reversal) **+** TXA (trauma antifibrinolytic)  
**Why split:** Three independent reversal/hemostasis agents for three different drug scenarios. No clinical scenario requires knowing all three simultaneously.

**Card A — Warfarin reversal: 4F-PCC**
> **FRONT:** On the coagulation reversal chart, warfarin reversal for INR > 6 with life-threatening bleeding requires _______ units/kg of 4F-PCC (max _______) PLUS _______ to prevent re-elevation of INR after PCC activity wanes.
>
> **BACK:** 4F-PCC (KCentra): **50 units/kg IV** (max **5,000 units**) for INR > 6 + life-threatening bleeding. Must also give **Vitamin K 10 mg IV** — PCC factors have short half-lives (6–12h); without Vitamin K, INR will re-elevate as PCC factors are consumed. 4F-PCC over FFP: 20–40 mL volume vs 1,000+ mL, no thaw, no crossmatch, immediate reversal.  
> → CCRN KEY: Supratherapeutic INR WITHOUT active bleeding: hold warfarin ± Vitamin K PO. PCC is for active major bleeding only. After PCC: restart anticoagulation when hemostasis achieved and bleeding risk acceptable.

**Card B — Protamine and TXA: hemostasis agents**
> **FRONT:** On the reversal chart, protamine reverses UFH at _______ mg per _______ units of heparin given (max _______ mg/dose). TXA in trauma must be given within _______ hours of injury because it works by _______.
>
> **BACK:** Protamine: **1 mg per 100 units UFH** (max **50 mg** per dose); only **~60% reversal of LMWH** (partial); does **NOT** reverse fondaparinux. TXA: within **3 hours** of injury (CRASH-2: mortality benefit lost if given >3h, possibly harmful). Mechanism: inhibits plasminogen → prevents fibrinolysis → stabilizes clot.  
> → CCRN KEY: Protamine adverse effects: hypotension, bradycardia, anaphylaxis (especially fish allergy or prior protamine exposure from insulin). Pre-treat with diphenhydramine in high-risk patients. TXA is also used in OB hemorrhage (1g within 3h of delivery, WOMAN trial).

---

### SPLIT 9 — nid 1778924096030 · Chunk 53 · HIGH
**Topic on original card:** Opioid safety in AKI (morphine M6G accumulation) **+** anticoagulant safety in CKD (LMWH → UFH switch)  
**Why split:** Opioid dosing in renal failure and anticoagulant dosing in renal failure are independent safety topics from unrelated drug classes.

**Card A — Opioid selection in AKI/CKD**
> **FRONT:** On the renal dose adjustment chart, morphine is problematic in AKI because its active metabolite _______ accumulates, causing _______. The preferred opioid for continuous infusion in AKI is _______. In ESRD/dialysis, the safest opioid is _______ because _______.
>
> **BACK:** Morphine active metabolite: **M6G (morphine-6-glucuronide)** → accumulates → **respiratory depression**, prolonged sedation, difficult weaning. Preferred in AKI: **hydromorphone** (no active accumulating metabolites in moderate CKD). In ESRD/dialysis: **fentanyl** (hepatic + extrahepatic clearance, no active renal metabolites). Avoid morphine infusions in CKD; avoid meperidine always in CKD (normeperidine → seizures).  
> → CCRN KEY: ICU opioid hierarchy by renal function: Fentanyl = always safe · Hydromorphone = safe through moderate CKD · Morphine = bolus OK if GFR >60, avoid infusions in AKI · Meperidine = never use in CKD.

**Card B — Anticoagulant adjustment in severe CKD**
> **FRONT:** On the renal adjustment chart, therapeutic LMWH (enoxaparin) in CrCl < 30 mL/min should be _______ and replaced with _______ monitored by _______ (two options).
>
> **BACK:** LMWH in CrCl < 30: **avoid therapeutic dose** — anti-Xa accumulates → bleeding risk. Replace with: **UFH (unfractionated heparin)** — cleared by hepatic/reticuloendothelial system, not renally dependent. Monitor UFH with: **aPTT 60–100 seconds** OR **anti-Xa 0.3–0.7 IU/mL** (preferred in obesity or abnormal baseline aPTT). Prophylactic enoxaparin 30 mg SQ q24h (renally dose-reduced) is still used at some centers — check anti-Xa levels.  
> → CCRN KEY: UFH also preferred in patients who may need rapid reversal (protamine available; no LMWH reversal equivalent). CRRT patients: use regional citrate anticoagulation or heparin per circuit protocol.

---

### SPLIT 10 — nid 1778924096009 · Chunk 53 · MEDIUM
**Topic on original card:** Beta-lactam mechanism + cefepime coverage **+** vancomycin mechanism + AUC monitoring  
**Why split:** Two different antibiotic classes with different mechanisms and different monitoring parameters.

**Card A — Beta-lactam antibiotics: mechanism and coverage**
> **FRONT:** The antibiotic chart shows beta-lactams inhibit _______ (PBPs), blocking _______. Cefepime (4th generation cephalosporin) covers gram-negatives including _______. Carbapenems are the treatment of choice for _______ organisms but are NOT active against _______.
>
> **BACK:** Beta-lactams inhibit **PBPs (penicillin-binding proteins = transpeptidases)** → block **cell wall cross-linking** → bacterial lysis. Cefepime covers: Pseudomonas aeruginosa + most gram-positives + some ESBL (not reliably). Carbapenems (meropenem/imipenem): best for **ESBL-producing** organisms. NOT active against: **MRSA** (use ceftaroline or vancomycin). Beta-lactam killing = TIME above MIC (time-dependent kinetics).  
> → CCRN KEY: ESBL (extended-spectrum beta-lactamase) organisms: resistant to all penicillins and most cephalosporins → carbapenem required. CRE (carbapenem-resistant Enterobacteriaceae): use ceftazidime-avibactam.

**Card B — Vancomycin: mechanism and AUC/MIC monitoring**
> **FRONT:** The antibiotic chart shows vancomycin inhibits _______ (different from PBP inhibition). Current monitoring uses _______ target of _______, not trough alone. This monitoring approach was updated by the _______ 2018 guideline.
>
> **BACK:** Vancomycin: inhibits **cell wall transglycosylation** (binds D-Ala–D-Ala peptidoglycan precursors). Monitoring: **AUC/MIC ratio target 400–600** (not trough-only — trough monitoring underestimates exposure and correlates poorly with outcomes). 2018 **ASHP/SIDP/IDSA** consensus guideline updated standard to AUC-guided dosing. AUC-guided: lower nephrotoxicity at same efficacy vs trough-only.  
> → CCRN KEY: When vancomycin fails (MIC ≥ 2 mcg/mL for MRSA): switch to daptomycin (non-pulmonary infections) or linezolid (pneumonia). VISA (vancomycin-intermediate S. aureus): use high-dose daptomycin 8–10 mg/kg.

---

### SPLIT 11 — nid 1778924096012 · Chunk 53 · MEDIUM
**Topic on original card:** Aminoglycoside mechanism + concentration-dependent dosing **+** linezolid MRSA/VRE coverage + serotonin syndrome risk  
**Why split:** Two independent antibiotic classes with no mechanistic relationship.

**Card A — Aminoglycosides: 30S ribosome + once-daily dosing**
> **FRONT:** The antibiotic chart shows aminoglycosides inhibit the _______ ribosomal subunit. The preferred ICU dosing strategy is _______ (once-daily) because aminoglycosides show _______ dependent killing. The two major toxicities requiring monitoring are _______ and _______.
>
> **BACK:** Aminoglycosides inhibit **30S ribosomal subunit** → misreading mRNA → aberrant protein synthesis. Once-daily (extended-interval) dosing: **concentration-dependent killing** — goal is high peak/MIC ratio (Cmax/MIC > 8–10); once-daily achieves this with less nephrotoxicity than multiple daily doses. Toxicities: **(1) nephrotoxicity** (proximal tubule; monitor SCr, ↓ with once-daily) + **(2) ototoxicity** (irreversible, cochlear + vestibular; monitor cumulative dose).  
> → CCRN KEY: Traditional monitoring: trough < 1 mcg/mL (gentamicin/tobramycin). AUC-guided monitoring increasingly preferred. Hold aminoglycosides if SCr rises ≥0.3 mg/dL without other cause.

**Card B — Linezolid: coverage and serotonin syndrome risk**
> **FRONT:** The antibiotic chart shows linezolid (oxazolidinone) inhibits both _______ ribosomal subunits. Its major ICU coverage includes _______ and _______. The critical drug interaction to check before starting: avoid combining with _______ drugs because linezolid inhibits _______.
>
> **BACK:** Linezolid: inhibits **50S + 30S** assembly (unique mechanism; bacteriostatic). Coverage: **MRSA** + **VRE (vancomycin-resistant Enterococcus)**. Preferred over vancomycin for MRSA VAP (ZEPHyR trial: 57.6% vs 46.6% clinical cure). Critical interaction: avoid with **serotonergic drugs** (SSRIs, MAOIs, tramadol, meperidine) because linezolid inhibits **MAO-A** → serotonin accumulates → serotonin syndrome.  
> → CCRN KEY: Linezolid monitoring: thrombocytopenia (CBC weekly, hold if < 100K at courses > 14 days), peripheral neuropathy and optic neuropathy (courses > 28 days). Do not use as empiric coverage without MRSA/VRE indication.

---

### SPLIT 12 — nid 1778924096039 · Chunk 53 · MEDIUM
**Topic on original card:** Clopidogrel as CYP2C19 prodrug (+ PPI interaction) **+** codeine as CYP2D6 prodrug (poor vs ultra-rapid metabolizer)  
**Why split:** Two different drugs, two different CYP enzymes, two different clinical consequences. The only connection is both are prodrugs — insufficient to keep together.

**Card A — Clopidogrel and CYP2C19**
> **FRONT:** The CYP2C19 chart shows clopidogrel is a _______ requiring CYP2C19 activation. PPIs inhibit CYP2C19 — the safest PPI to use with clopidogrel is _______ because it is the _______ CYP2C19 inhibitor. Poor CYP2C19 metabolizers (PM) have _______ platelet inhibition on clopidogrel.
>
> **BACK:** Clopidogrel: **prodrug** — requires CYP2C19 to form active thiol metabolite. Safest PPI with clopidogrel: **pantoprazole** (weakest CYP2C19 inhibitor). Avoid omeprazole (strongest 2C19 inhibitor). CYP2C19 PM: **inadequate platelet inhibition** → higher risk of stent thrombosis. Alternative: prasugrel or ticagrelor (not CYP2C19-dependent).  
> → CCRN KEY: FDA warning 2009: avoid omeprazole + clopidogrel concurrently. In clinical practice: if GI protection needed, prescribe pantoprazole. H2 blockers (famotidine) are not CYP2C19 inhibitors — safe alternative.

**Card B — Codeine and CYP2D6 pharmacogenomics**
> **FRONT:** The CYP2D6 chart shows codeine is a _______ that requires CYP2D6 to convert to _______. CYP2D6 poor metabolizers (PM) receive _______ analgesia. CYP2D6 ultra-rapid metabolizers (UM) face the risk of _______.
>
> **BACK:** Codeine: **prodrug** converted by CYP2D6 to **morphine** (the active analgesic). CYP2D6 PM: **no analgesia** (codeine remains inactive). CYP2D6 UM: **excessive morphine conversion** → respiratory depression, toxicity even at standard doses (fatal cases reported in breastfeeding infants of UM mothers). CPIC guidelines: do not use codeine in PM or UM patients.  
> → CCRN KEY: Tramadol is also CYP2D6-metabolized: PM = no effect, UM = toxicity. In ICU, avoid codeine and tramadol when metabolizer status is unknown. Use fentanyl or hydromorphone for predictable ICU opioid analgesia.

---

### SPLIT 13 — nid 1778926634003 · Chunk 54 · HIGH
**Topic on original card:** Dexmedetomidine (alpha-2 agonist, cooperative sedation) **+** ketamine (NMDA antagonist, dissociative, sympathomimetic)  
**Why split:** Two completely different drugs with different mechanisms, indications, and pharmacologic profiles.

**Card A — Dexmedetomidine: cooperative sedation**
> **FRONT:** The sedation chart shows dexmedetomidine is unique because it provides sedation WITHOUT _______ depression. It acts on _______ receptors in the _______ (brain region). Two clinical settings where this advantage is most important: _______ and _______.
>
> **BACK:** Dexmedetomidine: sedation **without respiratory depression** — acts on **α2-adrenergic receptors** in the **locus coeruleus** (brainstem NE nucleus). Produces "cooperative sedation" — patient is arousable, responds to voice, follows commands, can report pain. Best advantage: **(1)** Non-invasive ventilation (NIV/BiPAP) — patient must keep breathing spontaneously; **(2)** Ventilator weaning — sedation without suppressing respiratory drive facilitates extubation trials.  
> → CCRN KEY: Loading dose 1 mcg/kg over 10–20 min (often omitted in hemodynamically unstable). Maintenance 0.2–0.7 mcg/kg/h. Most common side effect: bradycardia — reduce rate, then atropine 0.5 mg IV if HR < 40 or hemodynamically significant.

**Card B — Ketamine: NMDA antagonism and hemodynamic safety**
> **FRONT:** The sedation chart shows ketamine provides analgesia AND sedation via _______ receptor antagonism. It is preferred for intubation in hemodynamic instability because it is a _______ agent (effect on catecholamines). Ketamine also causes _______, making it useful in _______ RSI.
>
> **BACK:** Ketamine: **NMDA (N-methyl-D-aspartate) receptor antagonist** → dissociative anesthesia + analgesia. Preferred in hemodynamic instability: **sympathomimetic** — endogenous catecholamine release → ↑HR, ↑BP (safe or beneficial in shock). Bronchodilation via β2 stimulation + direct smooth muscle relaxation → useful in **asthma/bronchospasm** RSI. RSI dose: 1–2 mg/kg IV.  
> → CCRN KEY: Co-administer midazolam 0.05 mg/kg to prevent emergence phenomena (hallucinations, dysphoria) in conscious patients. Ketamine and ICP: old teaching (raises ICP) is outdated for mechanically ventilated patients — acceptable for TBI RSI when hemodynamically compromised. Sub-dissociative dose (0.1–0.3 mg/kg/hr): opioid-sparing analgesia in ICU.

---

### SPLIT 14 — nid 1778926634006 · Chunk 54 · HIGH
**Topic on original card:** Midazolam delirium association + preferred benzo in hepatic failure **+** lorazepam propylene glycol toxicity  
**Why split:** "Midazolam causes more delirium" and "lorazepam IV causes propylene glycol toxicity" are two independent clinical safety facts about two different drugs.

**Card A — Midazolam: delirium and when to use**
> **FRONT:** The sedation chart shows midazolam is associated with _______ in ICU compared to propofol and dexmedetomidine. In hepatic failure, the preferred benzodiazepine is _______ because it undergoes _______ without producing active metabolites. Midazolam is first-line for _______.
>
> **BACK:** Midazolam: ↑ **ICU delirium** vs propofol and dexmedetomidine (MENDS/MIDEX trials); accumulates unpredictably in critically ill (active metabolite α-hydroxymidazolam in AKI). In hepatic failure: preferred benzo = **lorazepam** (direct glucuronidation — no CYP450 metabolism, no active metabolites). Midazolam IS first-line for: **acute seizures** (IV push, status epilepticus), alcohol withdrawal (CIWA protocol), procedural sedation.  
> → CCRN KEY: PAD guidelines 2018: minimize benzodiazepines in ICU (each additional day increases delirium risk 22%). Use propofol or dexmedetomidine for light sedation; reserve benzos for their specific indications.

**Card B — IV Lorazepam and propylene glycol toxicity**
> **FRONT:** On the toxicity chart, continuous IV lorazepam infusions carry a unique risk because the carrier vehicle contains _______, which is osmotically active. Toxicity presents as an elevated _______ gap plus anion gap metabolic _______.
>
> **BACK:** IV lorazepam carrier: **propylene glycol (PG)** — present in standard IV lorazepam formulation (not oral or IM). PG toxicity: elevated **osmol gap** (PG is osmotically active → measured Osm > calculated Osm) + **anion gap metabolic acidosis** (PG metabolized to lactic acid and pyruvate). Risk: infusions > 3 days or high-dose lorazepam. Recognize: rising osmol gap in patient on lorazepam infusion. Action: switch to non-PG sedation.  
> → CCRN KEY: Monitoring during lorazepam infusions: measure osmol gap daily if infusion > 48h. Osmol gap = measured Osm − (2×Na + BUN/2.8 + glucose/18); normal < 10. Gap > 20 on lorazepam infusion = propylene glycol toxicity → discontinue/switch.

---

### SPLIT 15 — nid 1778926634015 · Chunk 54 · HIGH
**Topic on original card:** Mucormycosis treatment (liposomal AmB + surgery) **+** Cryptococcal meningitis treatment (AmB + flucytosine → fluconazole)  
**Why split:** Two completely different fungal infections with different organisms, different treatments, and different azole susceptibility profiles.

**Card A — Mucormycosis treatment**
> **FRONT:** The antifungal chart shows mucormycosis requires _______ amphotericin B PLUS surgical _______. Voriconazole is _______ active against Mucorales, which is a common prescribing error. The salvage option when AmB is not tolerated is _______.
>
> **BACK:** Mucormycosis: **liposomal amphotericin B 3–5 mg/kg/day** + **surgical debridement** (essential — antifungals alone are insufficient for angioinvasive Mucorales). Voriconazole: **NOT active** against Mucorales (Aspergillus coverage is NOT Mucor coverage). This is the classic "wrong azole" error in immunocompromised patients. Salvage: **isavuconazole** (some Mucor activity; less nephrotoxic than AmB).  
> → CCRN KEY: AmB monitoring in ICU (daily): BMP (K⁺, Mg²⁺, Cr) — nephrotoxicity + electrolyte wasting. Hypokalemia requires aggressive replacement (often 100–200 mEq/day). Liposomal AmB: significantly less nephrotoxicity than conventional — always use liposomal in ICU.

**Card B — Cryptococcal meningitis treatment**
> **FRONT:** The antifungal chart shows cryptococcal meningitis is treated with an induction regimen of _______ PLUS _______ for _______ weeks, then _______ for consolidation for 8 weeks. The critical nursing monitoring during induction: _______.
>
> **BACK:** Cryptococcus meningitis induction (2 weeks): **liposomal AmB 3–4 mg/kg/day + flucytosine 25 mg/kg PO q6h**. Consolidation (8 weeks): **fluconazole 400 mg/day**. Maintenance (HIV, until CD4 > 200 for 3 months): fluconazole 200 mg/day. Critical monitoring during induction: ICP — cryptococcal meningitis causes obstructive/communicating hydrocephalus → serial LP or lumbar drain for refractory elevated ICP.  
> → CCRN KEY: Flucytosine toxicity: bone marrow suppression (monitor CBC 2×/week), GI toxicity. Do NOT use as monotherapy (rapid resistance). Flucytosine is renally cleared — dose-reduce in AKI; check 5-FC levels (target 20–80 mcg/mL at 2h post-dose).

---

### SPLIT 16 — nid 1778926634018 · Chunk 54 · HIGH
**Topic on original card:** Vancomycin AUC monitoring **+** daptomycin contraindication in pneumonia **+** ZEPHyR trial (linezolid vs vancomycin VAP)  
**Why split:** Vancomycin monitoring, daptomycin avoidance, and linezolid superiority are three separate MRSA pharmacology facts. Each can be tested independently.

**Card A — Vancomycin AUC/MIC monitoring**
> **FRONT:** The MRSA chart shows vancomycin is now monitored by _______ target of _______, not trough alone. This shift was recommended by the _______ 2018 guideline. The advantage over trough-only monitoring is _______.
>
> **BACK:** Vancomycin monitoring: **AUC/MIC ratio target 400–600** (trough-only monitoring underestimates exposure and correlates poorly with outcomes). **ASHP/SIDP/IDSA** 2018 consensus guideline. AUC-guided advantage: **lower nephrotoxicity** at equivalent or better efficacy — trough targeting requires higher doses to hit targets, causing more kidney injury.  
> → CCRN KEY: Practical implication: pharmacy often calculates AUC using two-point Bayesian modeling (one early and one late vancomycin level). Nurses ensure accurate timing of levels and document in EMR. When vancomycin MIC ≥ 2 mcg/mL for MRSA: switch therapy — vancomycin will fail at any dose.

**Card B — Daptomycin and linezolid in MRSA pneumonia**
> **FRONT:** The MRSA chart shows daptomycin is CONTRAINDICATED for MRSA pneumonia because it is inactivated by _______. The ZEPHyR trial found _______ superior to vancomycin for MRSA VAP with clinical cure rates of _______ vs _______.
>
> **BACK:** Daptomycin: contraindicated for **pulmonary infections** — inactivated by **pulmonary surfactant**. Use daptomycin for MRSA bacteremia, endocarditis, SSTI only. ZEPHyR trial (NEJM 2012): **linezolid** vs vancomycin for MRSA VAP — **57.6% vs 46.6%** clinical cure (P=0.042). Linezolid achieves higher lung tissue concentrations than vancomycin and is bacteriostatic vs MRSA (sufficient for pneumonia).  
> → CCRN KEY: For MRSA pneumonia: linezolid preferred. Monitor: thrombocytopenia (CBC weekly), serotonin syndrome risk (avoid SSRIs/MAOIs). Vancomycin is still acceptable for MRSA HAP/VAP when linezolid is not available or contraindicated.

---

### SPLIT 17 — nid 1778926634030 · Chunk 54 · HIGH
**Topic on original card:** Dobutamine β1/β2 mechanism **+** milrinone PDE3 mechanism **+** IABP-SHOCK II trial (no IABP benefit) + CI target  
**Why split:** Dobutamine and milrinone are independent learning targets; IABP-SHOCK II is a third independent fact.

**Card A — Dobutamine vs milrinone: mechanism and indications**
> **FRONT:** The cardiogenic shock chart shows dobutamine primarily stimulates _______ receptors, increasing CO and modestly _______ SVR. Milrinone works by inhibiting _______ — making it effective when _______ is present because it bypasses the receptor level.
>
> **BACK:** Dobutamine: **β1 (+ β2 + weak α1)** agonist → ↑CO + modest ↓SVR. First-line inotrope for cardiogenic shock without beta-blockade. Milrinone: **PDE3 (phosphodiesterase-3) inhibitor** → prevents cAMP breakdown regardless of receptor occupancy → effective when **beta-blocker** is present (competitive antagonism blocks dobutamine; milrinone works downstream). Both raise cAMP → ↑contractility.  
> → CCRN KEY: Milrinone disadvantage: vasodilation can worsen hypotension → requires concurrent norepinephrine to maintain MAP. Long elimination half-life (~2.5h; up to 20h in severe renal failure) — not easily reversible. OPTIME-CHF trial: no mortality difference vs dobutamine in decompensated HF.

**Card B — IABP-SHOCK II and cardiogenic shock targets**
> **FRONT:** The cardiogenic shock chart shows the IABP-SHOCK II trial (NEJM 2012) found IABP _______ 30-day mortality vs medical therapy in AMI cardiogenic shock. The hemodynamic target to confirm adequate cardiac output is CI ≥ _______ L/min/m² with PCWP ≤ _______ mmHg.
>
> **BACK:** IABP-SHOCK II (n=600): IABP **did NOT reduce** 30-day mortality vs medical therapy (39.7% vs 41.3%). IABP no longer class I recommendation for routine AMI-CS. Hemodynamic targets in cardiogenic shock: CI ≥ **2.2 L/min/m²** + PCWP ≤ **18 mmHg**. Mechanical circulatory support evidence: Impella RECOVER trial — no mortality benefit over IABP for routine use. VA-ECMO: reserved for refractory cardiogenic arrest (highest support level).  
> → CCRN KEY: SHOCK trial (NEJM 1999): early revascularization for AMI cardiogenic shock → ↓6-month mortality — still the definitive mortality-reducing intervention. Inotropes and MCS are bridges, not definitive treatment.

---

### SPLIT 18 — nid 1778926634036 · Chunk 54 · HIGH
**Topic on original card:** Esmolol ultra-short half-life (plasma esterase) + dissection HR/SBP targets **+** propranolol for variceal prophylaxis (β2 mechanism)  
**Why split:** Esmolol pharmacokinetics and variceal hemorrhage prevention are unrelated clinical applications despite both involving beta-blockers.

**Card A — Esmolol: pharmacokinetics and aortic dissection**
> **FRONT:** The beta-blocker chart shows esmolol has an ultra-short half-life of _______ minutes because it is metabolized by _______. For type A aortic dissection, the priority sequence is _______ FIRST, then add _______. Target: HR < _______ and SBP < _______ mmHg.
>
> **BACK:** Esmolol half-life: **9 minutes** — metabolized by **plasma esterase (red blood cell esterase)**. No hepatic or renal dependence. Dissection sequence: **HR control FIRST** (esmolol or labetalol) THEN add vasodilator (nitroprusside or nicardipine). Target: HR < **60 bpm** + SBP < **120 mmHg** while awaiting surgical repair. If vasodilator given first → reflex tachycardia → ↑ aortic wall shear force → dissection propagation.  
> → CCRN KEY: Esmolol advantage: 9-minute half-life allows precise titration and rapid offset in hemodynamically unstable patients. Switch to oral agent once stable. Labetalol IV (α+β) achieves both HR and BP goals with one agent but has longer half-life (~5.5h) — less flexible.

**Card B — Propranolol: non-selective beta-blockade and variceal prophylaxis**
> **FRONT:** The beta-blocker chart shows esophageal variceal prophylaxis requires a _______ beta-blocker such as propranolol or nadolol, NOT cardioselective agents like metoprolol. The reason: β2 blockade is required to _______, thereby _______ portal pressure.
>
> **BACK:** Variceal prophylaxis requires **non-selective** beta-blockers (propranolol or nadolol). β2 blockade of splanchnic vasculature → **↓ splanchnic blood flow** (reverses β2-mediated vasodilation) → **↓ portal blood flow → ↓ portal pressure**. Metoprolol (β1-selective) does NOT reduce portal pressure — β1 selectivity spares the splanchnic β2 receptors. Propranolol 20–40 mg BID titrated to HR 55–60 or 25% reduction from baseline.  
> → CCRN KEY: Carvedilol (α+β) is emerging as alternative for variceal prophylaxis (α1 blockade also reduces hepatic venous pressure gradient). Beta-blockers are first-line primary prophylaxis for varices requiring treatment; alternatives: EVL (endoscopic variceal ligation) for patients who cannot tolerate beta-blockers.

---

### SPLIT 19 — nid 1778973067510 · Chunk 54 · HIGH
**Topic on original card:** Vasopressin trigger/fixed dose **+** epinephrine as third-line vasopressor + lactate interference  
**Why split:** "When to add vasopressin" and "why epinephrine makes lactate uninterpretable" are independent clinical safety facts.

**Card A — Vasopressin: fixed dose and trigger**
> **FRONT:** On the vasopressor algorithm chart, vasopressin is added at fixed dose _______ units/min when NE reaches _______ mcg/kg/min. It is NOT _______ — unlike catecholamines. The reason for the dose ceiling of 0.04 units/min is _______.
>
> **BACK:** Vasopressin: fixed **0.03–0.04 units/min** (add-on when NE ≥ **0.25 mcg/kg/min**). NOT titrated — fixed dose only, unlike catecholamines. Ceiling 0.04 units/min: doses above cause **splanchnic and digital ischemia** (V1 receptors in coronary/mesenteric/skin vasculature). Purpose: catecholamine-sparing → allows NE dose reduction → reduces adrenergic side effects.  
> → CCRN KEY: Vasopressin hierarchy: NE first-line → add vasopressin (fixed) as second → epinephrine third. VASST trial: vasopressin + NE vs NE alone → no overall 90-day mortality benefit; subgroup benefit in less severe septic shock (NE < 15 mcg/min).

**Card B — Epinephrine and lactate interference**
> **FRONT:** The vasopressor chart shows epinephrine as a third-line vasopressor raises serum _______ via β2 receptor stimulation. When epinephrine is in use, _______ clearance becomes unreliable as a resuscitation endpoint. The preferred alternative endpoints are _______ and _______.
>
> **BACK:** Epinephrine → elevates **lactate** via β2 stimulation → glycogenolysis → hepatic lactate production (independent of tissue hypoperfusion). When epi is running, **lactate clearance** is unreliable — rising lactate may reflect epinephrine effect, not resuscitation failure. Use instead: **ScvO₂ ≥ 65–70%** and/or **MAP + clinical perfusion markers** (UO, capillary refill, mottling score).  
> → CCRN KEY: Epinephrine also causes tachycardia and increases myocardial oxygen demand. Use the minimum dose necessary. If septic shock requires epinephrine, consider adding vasopressin earlier to spare epinephrine dose.

---

### SPLIT 20 — nid 1778926634033 · Chunk 54 · MEDIUM
**Topic on original card:** Anaphylaxis management (epinephrine IM, site, why not antihistamines first) **+** neurogenic shock characteristics (bradycardia) + MAP target in SCI  
**Why split:** Two completely different shock types with different pathophysiology, different hemodynamics, and different management.

**Card A — Anaphylaxis: epinephrine first**
> **FRONT:** On the specific shock types chart, the FIRST treatment for anaphylaxis is _______ given _______ (site and route), not IV antihistamines. The reason epinephrine takes priority: _______.
>
> **BACK:** First treatment: **epinephrine 0.3–0.5 mg IM** (anterolateral thigh). IM preferred over IV for non-arrest anaphylaxis — faster peak concentration than IV in this setting; SC route is slower. **Antihistamines and steroids are adjuncts only** — they do NOT reverse circulatory collapse (anaphylaxis = mediator storm causing vasodilation + capillary leak; only epinephrine reverses this). Mortality from anaphylaxis = delayed epinephrine.  
> → CCRN KEY: If anaphylaxis progresses to cardiac arrest: epinephrine 1 mg IV q3–5 min (ACLS). IV diphenhydramine and methylprednisolone are given AFTER epi is given — they prevent recurrence (biphasic reaction), not the initial collapse. A second dose of IM epi can be given at 5–15 min if no response.

**Card B — Neurogenic shock: bradycardia pattern and MAP target**
> **FRONT:** The shock types chart shows neurogenic shock from spinal cord injury differs from all other shock types because heart rate is _______ (not elevated). This is because _______ fibers are disrupted at the injury level. The MAP target in acute SCI is ≥ _______ mmHg for _______ days to maintain cord perfusion.
>
> **BACK:** Neurogenic shock: **bradycardia** (not tachycardia) + hypotension — because **cardiac sympathetic fibers** (T1–T4) are disrupted → unopposed vagal tone → ↓HR + loss of systemic vasoconstriction. MAP target: ≥ **85–90 mmHg for 5–7 days** post-injury (spinal cord perfusion pressure). Vasopressor of choice: norepinephrine (α1 + β1 counteracts both hypotension and bradycardia); phenylephrine if tachycardia is present.  
> → CCRN KEY: Neurogenic shock pattern: triad of hypotension + bradycardia + hypothermia (loss of sympathetic vasoconstriction + impaired thermoregulation below injury). Differentiate from hypovolemic shock (hypovolemic = tachycardia + cold extremities + normal or low HR). Identify mechanism before choosing vasopressor.

---

### SPLIT 21 — nid 1778926634039 · Chunk 54 · MEDIUM
**Topic on original card:** Carvedilol α+β receptor profile **+** MERIT-HF (metoprolol XL mortality benefit) **+** propranolol for thyroid storm (T4→T3 conversion inhibition)  
**Why split:** Three different beta-blocker pharmacology facts about three different drugs for three different indications.

**Card A — Beta-blockers in HFrEF: carvedilol and MERIT-HF**
> **FRONT:** The beta-blocker chart shows carvedilol blocks _______, _______, and _______ receptors. The MERIT-HF trial found metoprolol succinate XL reduced all-cause mortality in HFrEF by approximately _______%. The three beta-blockers with proven mortality benefit in HFrEF are _______, _______, and _______.
>
> **BACK:** Carvedilol: **β1 + β2 + α1** (non-selective beta + alpha-1). Additional α1 block → ↓afterload + antioxidant effects. MERIT-HF: metoprolol XL → **34% relative risk reduction** in all-cause mortality in HFrEF (EF ≤ 40%). Three agents with proven HFrEF mortality benefit (class effect NOT generalizable): **carvedilol** (COPERNICUS), **metoprolol succinate XL** (MERIT-HF), **bisoprolol** (CIBIS-II). Atenolol and propranolol: NO proven mortality benefit in HFrEF.  
> → CCRN KEY: Do NOT start beta-blocker in acute decompensated HF with cardiogenic shock. Continue home beta-blocker if hemodynamically stable. Restart when euvolemic and stable.

**Card B — Propranolol in thyroid storm: T4→T3 inhibition**
> **FRONT:** The thyroid storm chart shows propranolol is preferred over cardioselective beta-blockers for thyroid storm because it also inhibits _______ conversion. Cardioselective agents like metoprolol do NOT provide this benefit because _______.
>
> **BACK:** Propranolol: in addition to β-receptor blockade, **inhibits peripheral T4→T3 conversion** (inhibits 5'-deiodinase). This reduces the more active T3 form — important in thyroid storm where T3 excess drives the catecholamine-like storm. Cardioselective agents (metoprolol, atenolol) block only β-receptors — they do NOT inhibit deiodinase → no T4→T3 conversion block.  
> → CCRN KEY: Thyroid storm beta-blocker sequence: propranolol (or esmolol if IV preferred) → then PTU 500 mg PO/NG loading → wait 1 hour → Lugol iodine 10 drops q8h (iodine given BEFORE PTU causes acute hormone release — do not reverse the sequence). Dexamethasone 2 mg q6h also inhibits T4→T3 conversion (synergistic with propranolol).

---

## IMPLEMENTATION NOTES

**Total cards affected:** 141 original cards → ~282 replacement cards (+141 net new)  
**Cards unchanged:** 0  
**Net deck size change:** +141 chart notes (from 455 to ~596)

**Execution approach:** Direct SQLite surgery against 57.apkg (same pattern as patch_typeb.py). For each SPLIT:
1. Delete the original note from `notes` table
2. Delete associated rows from `cards` table (by note id)
3. Insert two new notes with fresh GUIDs, inherited `tags` (same chunk/badge), modified `flds` fields containing Card A and Card B front/back content
4. Insert corresponding rows into `cards` table for each new note

**Tag handling for split cards:**
- Inherit: `chunk-NN chart-lN` (same as parent)  
- Tier/badge: inherit from parent unless content scope changes (antifungals → tier-high; neurogenic shock → tier-review if PCCN-only)
- Do NOT add new tags — keep the existing badge system intact

**Chunk 54 receives the most changes (9 splits → 18 new cards).** Run a post-patch audit using `audit_typeb.py` to confirm no HIGH/MEDIUM cards remain after the patch.

**Prerequisite before patch execution:** Review this document and confirm decisions. Flag any SPLIT decisions where clinical context changes the recommendation.

---

## SPLIT PROPOSALS — ADDITIONAL 120 CARDS (previously KEEP, now required to split)

> Format matches prior splits. Numbered 22–141 continuing from the original 21.

---

### SPLIT 22 — nid 1778480387889 · Chunk 28 · HIGH
**Topic:** Cardiogenic shock recognition + ScvO₂ physiology + dobutamine mechanism  
**Why split:** Shock-type identification, tissue-oxygen delivery physiology, and inotrope mechanism are three testable domains.

**Card A — Cardiogenic shock recognition**
> **FRONT:** Post-MI patient: CO 1.6, SVR 2800, PAOP 28, MAP 54. The hemodynamic space shows _______ shock. The key features that distinguish this from distributive shock are _______ (CO/SVR pattern).
>
> **BACK:** **Cardiogenic shock** — low CO (1.6 L/min), very high SVR (2800, reflex vasoconstriction), severely elevated PAOP (28 = LV cannot empty). Distinguishing from distributive: distributive = high CO + low SVR. Cardiogenic = low CO + high SVR + high filling pressure.  
> → CCRN KEY: Complete cardiogenic hemodynamic profile: ↓CO + ↑SVR + ↑PAOP + ↑CVP. All four confirm pump failure as the primary problem. MAP is maintained by extreme vasoconstriction — not by adequate flow.

**Card B — ScvO₂ and dobutamine in cardiogenic shock**
> **FRONT:** ScvO₂ 42% in this cardiogenic shock patient indicates _______. Adding dobutamine addresses this by _______.
>
> **BACK:** ScvO₂ 42% (normal 65–75%): tissues extracting far more O₂ than normal because DO₂ is critically inadequate → **cellular hypoxia** despite acceptable MAP. Dobutamine: ↑contractility → ↑CO → ↑DO₂ → tissues reduce extraction → ScvO₂ rises toward 65–70%.  
> → CCRN KEY: ScvO₂ < 60% despite treatment = inadequate O₂ delivery. MAP maintained by maximal vasoconstriction can mask covert hemodynamic failure — track ScvO₂ AND MAP together.

---

### SPLIT 23 — nid 1778480387913 · Chunk 28 · HIGH
**Topic:** NE receptor profile + CO effect + ScvO₂ response after NE + vasopressin add-on  
**Why split:** Drug mechanism and clinical monitoring/treatment escalation are distinct learning targets.

**Card A — Norepinephrine receptor profile and CO effect**
> **FRONT:** Norepinephrine acts primarily on _______ receptors to ↑SVR. At clinical doses its net effect on CO is _______ because _______.
>
> **BACK:** Primary: **α1 receptors** → vasoconstriction → ↑SVR → ↑MAP. Also β1 (inotropy/chronotropy) but α1 dominates. Net CO effect: **neutral to mildly decreased** — ↑SVR raises LV afterload. In a compromised heart, the afterload increase can reduce stroke volume despite β1 stimulation.  
> → CCRN KEY: NE dose ranges: <0.1 mcg/kg/min = low/moderate; 0.1–0.5 = significant; >0.5 = high. NE is first-line in septic shock — α1 raises SVR toward normal without the arrhythmia risk of dopamine.

**Card B — ScvO₂ response to NE + vasopressin add-on**
> **FRONT:** This explains why ScvO₂ may _______ after starting norepinephrine alone in septic shock despite MAP improvement. When ScvO₂ remains low despite NE ≥ _______ mcg/kg/min, the next agent to add is _______ at fixed dose _______ units/min.
>
> **BACK:** ScvO₂ may **initially improve** (↑MAP → ↑coronary perfusion → better cardiac function), then **plateau** if CO is still inadequate — ScvO₂ improvement from MAP restoration alone is limited. Add **vasopressin 0.03–0.04 units/min** when NE ≥ 0.25 mcg/kg/min (catecholamine-sparing; acts via V1 not adrenergic receptors).  
> → CCRN KEY: Low ScvO₂ despite adequate MAP + NE → CO is insufficient → add dobutamine (not vasopressin). Vasopressin adds vasoconstriction; dobutamine adds CO. Different endpoints.

---

### SPLIT 24 — nid 1778480387916 · Chunk 28 · HIGH
**Topic:** Septic paradox (high CO + low ScvO₂) explanation + correct next intervention  
**Why split:** Microcirculatory maldistribution pathophysiology and clinical action are separate learning targets.

**Card A — Septic shock paradox: microcirculatory maldistribution**
> **FRONT:** Septic shock: MAP 58 on NE 0.4, CO 5.2, ScvO₂ 48%. The paradox — high CO with low ScvO₂ — is explained by _______.
>
> **BACK:** **Microcirculatory maldistribution** — inflammatory mediators cause: arteriovenous shunting (blood bypasses nutritive capillaries), microthrombi obstructing capillaries, interstitial edema increasing O₂ diffusion distance. Tissues extract more O₂ → ScvO₂ falls despite high global CO. The problem is distribution, not total flow rate.  
> → CCRN KEY: High CO + low ScvO₂ in sepsis = microcirculatory failure / tissue dysoxia. Confirm with lactate: if >4 mmol/L despite apparently 'adequate' hemodynamics → cryptic shock. Macrocirculation looks adequate; microcirculation is failing.

**Card B — Correct intervention in microcirculatory failure**
> **FRONT:** The correct next intervention when ScvO₂ is 48% with CO 5.2 is _______, because _______.
>
> **BACK:** **Optimize the underlying cause** — antibiotics, source control, drain collections. Transfuse if Hgb < 7 (↑CaO₂ → ↑DO₂); reassess volume status. **NOT more vasopressor** — more SVR elevation without fixing microcirculation does not improve tissue O₂ delivery.  
> → CCRN KEY: Two metabolic endpoints confirming successful resuscitation: ScvO₂ ≥65–70% AND lactate clearance ≥10%/2h. Treat tissue endpoints, not the blood pressure number.

---

### SPLIT 25 — nid 1778480387907 · Chunk 28 · MEDIUM
**Topic:** Driving pressure calculation + two interventions to reduce ΔP  
**Why split:** Formula application (calculation domain) vs. intervention selection (clinical action domain).

**Card A — Driving pressure calculation**
> **FRONT:** VCV: Vt 420 mL, PEEP 10, PIP 42, Pplat 34. Driving pressure = _______. This exceeds the target of _______ cmH₂O.
>
> **BACK:** ΔP = Pplat − PEEP = 34 − 10 = **24 cmH₂O**. Target: ≤ **15 cmH₂O** (Amato 2015, NEJM: ΔP >15 associated with increased VILI mortality). ΔP can be excessive even with correct 6 mL/kg IBW Vt — driving pressure is the more physiologically relevant metric.  
> → CCRN KEY: Monitor ΔP at least q4h in ARDS: Pplat via end-inspiratory hold, calculate ΔP = Pplat − PEEP. Document trend. ΔP rising despite stable Vt = compliance worsening → escalate.

**Card B — Interventions to reduce driving pressure**
> **FRONT:** Two interventions that reduce driving pressure WITHOUT increasing Vt: _______ and _______.
>
> **BACK:** **(1) Increase PEEP** — recruits collapsed alveoli → ↑functional lung surface area → ↑compliance → Pplat falls at same Vt → ΔP decreases. **(2) Prone positioning** — distributes ventilation to dorsal units → ↑recruitability → ↑compliance → ↓Pplat → ↓ΔP. Recommended ≥16h/day in moderate-severe ARDS (P/F < 150).  
> → CCRN KEY: If PEEP + prone both fail → further Vt reduction to 4–5 mL/kg IBW with permissive hypercapnia, and/or NMBA for 48h to eliminate dyssynchrony-related volutrauma.

---

### SPLIT 26 — nid 1778482073885 · Chunk 29 · HIGH
**Topic:** Harlequin syndrome — mechanism + monitoring + intervention  
**Why split:** Pathophysiology and nursing surveillance/intervention are independent learning targets.

**Card A — Harlequin syndrome: mechanism**
> **FRONT:** VA ECMO patient: right arm SpO₂ 88%, left arm SpO₂ 98%, ECMO flow 4.8 L/min, patient improving. This is _______ syndrome. The mechanism: _______.
>
> **BACK:** **Harlequin syndrome** (North-South syndrome). Mechanism: as LV recovers and ejects, native cardiac output competes with retrograde ECMO flow in the aorta. If lungs still failing, native LV ejects hypoxic blood → upper body (coronary arteries, brain, right arm) receives deoxygenated blood while lower body receives ECMO-oxygenated blood. Paradoxically more common as patient IMPROVES.  
> → CCRN KEY: Left arm is at the mixing watershed — may show intermediate saturation. Right radial A-line is the sentinel for cerebral and coronary oxygenation.

**Card B — Harlequin syndrome: monitoring and intervention**
> **FRONT:** The monitoring parameter the nurse should have identified earlier: _______. Interventions: _______.
>
> **BACK:** Monitoring: **right radial A-line SpO₂** — routine in all peripheral VA ECMO; SpO₂ discrepancy between right radial and pulse ox = diagnostic finding. Interventions: **(1)** Increase respiratory support (optimize lung recruitment — improve source O₂ of native CO); **(2)** Add VV cannula (VVA configuration) to oxygenate blood entering LV; **(3)** Convert to central cannulation (ascending aortic return bypasses mixing problem).  
> → CCRN KEY: ECMO nursing requires simultaneous monitoring: ECMO flow/pressures + right radial SpO₂ + bilateral limb perfusion + drainage cannula SaO₂.

---

### SPLIT 27 — nid 1778482073858 · Chunk 29 · MEDIUM
**Topic:** Reinfarction biomarker pattern interpretation + next diagnostic step  
**Why split:** Biomarker interpretation (has/has not reinfarction + why) vs. next diagnostic step — two separate clinical questions.

**Card A — Reinfarction biomarker interpretation**
> **FRONT:** Patient had NSTEMI 5 days ago. Today: new chest pain, troponin 18× ULN unchanged, CK-MB 0.8× ULN (normal). The _______ (has/has not) had a reinfarction because _______.
>
> **BACK:** **Has NOT** reinfarction — troponin remains elevated but UNCHANGED (no rise/fall pattern). CK-MB is NORMAL — if new MI, CK-MB would have risen (it normalizes within 48–72h of original event, so new elevation = new injury). Flat troponin + normal CK-MB at 5 days = persistent elevation from original event.  
> → CCRN KEY: Troponin elevation persists 7–14 days after NSTEMI. CK-MB normalizes at 48–72h → it is the reinfarction detector in the late window. The combination is the classic reinfarction diagnostic algorithm.

**Card B — Next diagnostic step for possible reinfarction**
> **FRONT:** The correct next diagnostic step when reinfarction is suspected at 5 days post-NSTEMI is _______.
>
> **BACK:** **Clinical assessment + serial 12-lead ECG + serial CK-MB q6–8h × 24h**. If CK-MB remains normal and chest pain is atypical → likely not reinfarction. If CK-MB rises → new MI confirmed. Echocardiography helps if new wall motion abnormality = new territory ischemia.  
> → CCRN KEY: Nurse's role: serial ECGs (new ST changes in different distribution = new territory), serial CK-MB (timing and collection), continuous cardiac monitoring (new arrhythmias). The biomarker assessment is ordered by provider but the nurse executes timing, collection, and clinical correlation.

---

### SPLIT 28 — nid 1778482073891 · Chunk 29 · MEDIUM
**Topic:** Mobitz II location + danger reason + Mobitz I comparison + ECG pattern distinction  
**Why split:** Anatomical location/mechanism and ECG pattern recognition are separate clinical domains.

**Card A — Mobitz II: location and clinical danger**
> **FRONT:** Mobitz II occurs at the level of the _______ (above/at/below the AV node), making it clinically dangerous because _______.
>
> **BACK:** Mobitz II: at or **below the Bundle of His / bundle branch level** (below the AV node). Dangerous because: **(1)** reserve pacemaker is ventricular escape at 20–40 bpm (wide QRS, unreliable); **(2)** often progresses to complete heart block **without warning** — sudden loss of all conduction below the block level. Requires pacemaker even when asymptomatic.  
> → CCRN KEY: Anterior MI (LAD) causes Mobitz II (bundle branches supplied by LAD septal perforators). Anterior MI + new bifascicular block = immediate pacing consideration.

**Card B — Mobitz I vs II: ECG distinguishing pattern**
> **FRONT:** Mobitz I occurs _______. The ECG pattern distinguishing Mobitz I from Mobitz II is _______.
>
> **BACK:** Mobitz I (Wenckebach): at the **AV node** — more reliable escape pacemaker below (junctional 40–60 bpm, narrow QRS). Usually benign (inferior MI — vagally mediated). ECG: **PR progressively lengthens** until a P wave is blocked (no QRS), then cycle resets; RR intervals shorten just before the dropped beat. Mobitz II: **constant PR interval** then suddenly a P wave is blocked — no progressive change.  
> → CCRN KEY: Inferior MI (RCA) → Mobitz I; transient, responds to atropine. Mobitz II → TCP pads applied and tested immediately while arranging transvenous pacing.

---

### SPLIT 29 — nid 1778482073894 · Chunk 29 · MEDIUM
**Topic:** Complete heart block — dissociation + escape rates by level + immediate nursing action  
**Why split:** Pathophysiology recognition vs. nursing action (TCP) are distinct domains.

**Card A — Complete heart block: recognition and escape rates**
> **FRONT:** Complete heart block means P waves and QRS are _______. Block at His bundle → rate _______, QRS _______. Block below bifurcation → rate _______, QRS _______.
>
> **BACK:** P waves and QRS are **independent (dissociated)** — no P waves conduct through. His bundle level: rate **40–60 bpm**, QRS **narrow** (more reliable). Below bifurcation: rate **20–40 bpm**, QRS **wide and bizarre** (ventricular origin — unreliable, high asystole risk).  
> → CCRN KEY: Lower the block site = slower escape = wider QRS = higher risk. Patient with HR 30 + wide QRS = infranodal block → immediate TCP.

**Card B — Complete heart block: immediate nursing action**
> **FRONT:** Immediate nursing action for complete heart block with hemodynamic instability: _______.
>
> **BACK:** **Transcutaneous pacing (TCP)** — immediately apply pads (anterior chest + posterior back), connect to TCP unit, set rate 60–80 bpm, increase current mA until electrical AND mechanical capture confirmed (palpate femoral pulse with each pacer spike). Simultaneously call for emergency transvenous pacemaker placement.  
> → CCRN KEY: TCP causes painful muscle contractions — if patient is conscious, provide IV analgesia (morphine 2–4 mg IV) and sedation (midazolam 1–2 mg IV) as soon as hemodynamically feasible. Confirm mechanical capture by palpating the femoral pulse — monitor alone may show spikes without actual ventricular contraction.

---

### SPLIT 30 — nid 1778484729880 · Chunk 30 · HIGH
**Topic:** Flow-volume loop pattern (variable extrathoracic obstruction) + bedside assessment  
**Why split:** Loop interpretation (clinical interpretation domain) vs. bedside confirmatory assessment (nursing action domain).

**Card A — Flow-volume loop interpretation**
> **FRONT:** Toggle Upper Airway Obstruction on the loop. The INSPIRATORY limb is _______ while the expiratory limb is _______ — this pattern of variable extrathoracic obstruction indicates _______.
>
> **BACK:** Inspiratory limb: **flat (truncated)** — fixed inspiratory flow cannot increase above plateau. Expiratory limb: **normal** — positive intrathoracic pressure during expiration relieves extrathoracic obstruction. **Variable extrathoracic obstruction**: above the thoracic inlet (larynx, subglottis, trachea above sternum). Examples: tracheomalacia, subglottic stenosis, vocal cord paralysis, large goiter. Fixed obstruction (bilateral): BOTH limbs flattened — box-shaped loop.  
> → CCRN KEY: Post-extubation stridor within 30–60 min = glottic/subglottic edema. Prevention: cuff leak test before extubation.

**Card B — Bedside assessment of upper airway obstruction**
> **FRONT:** Bedside clinical assessment to confirm variable extrathoracic obstruction: _______.
>
> **BACK:** **Inspiratory stridor** (high-pitched noise on inspiration) — hallmark of upper airway obstruction. Auscultate over the larynx/trachea. Positional change: stridor worsens supine (posterior tracheal wall collapses). Direct laryngoscopy or flexible bronchoscopy for visualization. Treatment: racemic epinephrine nebulizer (↓mucosal edema) + IV dexamethasone + heliox (lower density → ↓turbulent flow → ↓work of breathing).  
> → CCRN KEY: Cuff leak test: deflate ETT cuff and occlude tube momentarily — audible air leak should occur. No leak = significant airway edema risk → dexamethasone 8 mg IV 12–24h before extubation.

---

### SPLIT 31 — nid 1778484729898 · Chunk 30 · HIGH
**Topic:** Massive PE classification + alteplase dose + nursing pre-thrombolysis check + heparin hold  
**Why split:** Classification/dose (clinical knowledge) vs. nursing safety checks (nursing action) are separate domains.

**Card A — Massive PE: classification and alteplase dose**
> **FRONT:** PE patient: BP 82/52, HR 138, RV:LV 1.4, McConnell sign. Classification: _______ PE. Dose of alteplase: _______ over _______ hours.
>
> **BACK:** **Massive PE** — hemodynamically UNSTABLE. McConnell sign (RV free wall akinesis with preserved apex) confirms severe acute RV failure. Alteplase: **100 mg IV over 2 hours** (10 mg bolus over 1–2 min, then 90 mg over 2h). Reduced 0.6 mg/kg (max 50 mg) for smaller patients or higher bleeding risk.  
> → CCRN KEY: McConnell sign specificity ~94% for acute RV pressure overload. In chronic PH, the entire RV wall is hypokinetic — preserved apex motion is the acute-specific finding.

**Card B — Nursing pre-thrombolysis checklist and heparin hold**
> **FRONT:** Before systemic thrombolysis, nursing confirms _______ contraindications (checked). For the first 2 hours of infusion, the nurse holds _______.
>
> **BACK:** Absolute contraindications to check: prior intracerebral hemorrhage, recent intracranial surgery/trauma (<3 months), known intracranial neoplasm/AVM, active internal bleeding, ischemic stroke <3 months. **During infusion: HOLD ALL ANTICOAGULATION** — concurrent heparin dramatically increases bleeding risk. Restart heparin WITHOUT bolus 1h after alteplase if aPTT <80.  
> → CCRN KEY: Thrombolysis nursing: neurological checks q30min during infusion (AMS, new headache, pupils = STOP alteplase immediately). No arterial sticks during and 24h after. Have reversal plan: cryoprecipitate/FFP for fibrinogen replacement.

---

### SPLIT 32 — nid 1778735486033 · Chunk 31 · HIGH
**Topic:** Type A dissection + RCA occlusion (why not ACS) + nursing priorities  
**Why split:** Clinical distinction (ST elevation mechanism) and nursing action priorities are separate domains.

**Card A — Type A dissection vs. primary ACS: clinical distinction**
> **FRONT:** CT confirms Type A aortic dissection with new ST elevation in lead II. The ST elevation is caused by _______, NOT primary ACS. This distinction changes management because _______.
>
> **BACK:** Caused by **dissection flap occluding the right coronary artery ostium** → inferior MI (II, III, aVF) from RCA territory ischemia. Management change is critical: primary ACS → PCI + anticoagulation + possible thrombolytics. Type A dissection → **anticoagulation is CONTRAINDICATED** (promotes aortic hemorrhage); PCI would introduce catheter near dissection flap, could extend dissection, delays definitive surgical repair. Taking this patient to PCI would likely cause death.  
> → CCRN KEY: Do NOT give aspirin, heparin, or thrombolytics for concurrent ST elevation until dissection is definitively ruled out. Activate surgical pathway simultaneously with diagnostic workup.

**Card B — Type A dissection: immediate nursing priorities**
> **FRONT:** Immediate nursing priorities: _______, _______, and _______.
>
> **BACK:** **(1) Notify cardiac surgery and OR team immediately** — surgical emergency, mortality 1–2%/hour untreated. **(2) Arterial line in right radial + large-bore IV × 2** — continuous BP monitoring and rapid infusion capacity. **(3) IV esmolol infusion** to target HR <65 and SBP 100–120 mmHg while awaiting OR — reduce dP/dt to slow dissection propagation.  
> → CCRN KEY: Pulse differential >20 mmHg between arms = dissection flap compromising subclavian flow. Always check bilateral BPs and bilateral lower extremity pulses at initial assessment. Malperfusion to any major vessel = urgent intervention.

---

### SPLIT 33 — nid 1778735486009 · Chunk 31 · MEDIUM
**Topic:** MAP formula + two shock examples calculated + both examples interpreted  
**Why split:** Formula application (calculation) vs. clinical interpretation (same MAP, different shock types) are distinct.

**Card A — MAP formula: calculation**
> **FRONT:** MAP = CO × SVR / 80. A patient with CO 2.0 and SVR 2600 has MAP = _______ mmHg. A patient with CO 7.0 and SVR 350 has MAP = _______ mmHg.
>
> **BACK:** CO 2.0 × SVR 2600 / 80 = **65 mmHg** (high SVR compensating for low CO). CO 7.0 × SVR 350 / 80 = **31 mmHg** (low MAP despite high CO because SVR is critically low).  
> → CCRN KEY: MAP = CO × SVR / 80 governs all vasopressor and inotrope decisions. Isoline chart shows the same MAP can be achieved through vastly different CO/SVR combinations.

**Card B — MAP formula: clinical interpretation**
> **FRONT:** Both of these MAP examples represent _______ shock with different mechanisms. Before choosing a drug: identify which component is failing. Low SVR → _______. Low CO → _______. Both failing → _______.
>
> **BACK:** First = **cardiogenic** (low CO + high SVR compensating). Second = **distributive** (high CO + critically low SVR). Treatment: low SVR → **vasopressor (norepinephrine)**; low CO → **inotrope (dobutamine)**; both failing → **combination**. The MAP isoline shows which axis the patient is on.  
> → CCRN KEY: MAP ≥65 is a surrogate for organ perfusion pressure. CPP = MAP − ICP (brain). Coronary perfusion ∝ diastolic MAP − LVEDP. All require MAP ≥65 as minimum floor — optimal may be higher for chronic hypertensives.

---

### SPLIT 34 — nid 1778735486039 · Chunk 31 · MEDIUM
**Topic:** Lactate + covert hemodynamic failure + cardiogenic vs septic shock comparison  
**Why split:** Lactate as marker of covert failure vs. mechanism comparison between shock types are distinct learning targets.

**Card A — Lactate and covert hemodynamic failure**
> **FRONT:** On the shock progression chart, lactate rising past the critical threshold despite adequate MAP indicates _______.
>
> **BACK:** **Covert hemodynamic failure** — macrovascular parameters (MAP, CVP) appear adequate but tissue O₂ delivery has fallen below the critical threshold. Cells switch to anaerobic metabolism. This pattern (acceptable MAP + rising lactate) = 'cryptic shock' — requires immediate reassessment of CO and ScvO₂.  
> → CCRN KEY: Lactate targets: initial >4 mmol/L = high-risk, 6h mortality 40%+. Target: ≥10% clearance per 2h. Resuscitation endpoint is metabolic normalization, not blood pressure.

**Card B — Cardiogenic vs septic shock: lactate comparison**
> **FRONT:** Compare the CO trajectory in Cardiogenic vs Septic Shock. The reason cardiogenic shock has worse early lactate elevation: _______.
>
> **BACK:** In **cardiogenic shock**, CO fails immediately from pump dysfunction → DO₂ deficit begins at onset → early and severe lactate. In **early septic shock**, CO is actually ELEVATED (high-output distributive); initial lactate elevation reflects microcirculatory dysfunction and altered metabolism — not global DO₂ deficit. Absolute DO₂ in early sepsis may be normal or high.  
> → CCRN KEY: Non-shock causes of elevated lactate: hepatic failure, metformin toxicity, thiamine deficiency, seizure activity, beta-agonist toxicity. These 'type B' lactic acidoses must be distinguished from 'type A' (tissue hypoperfusion) before attributing lactate to inadequate resuscitation.

---

### SPLIT 35 — nid 1778735992006 · Chunk 31 · LOW
**Topic:** PA catheter PADP−PAWP gap + complete hemodynamic profile → shock type  
**Why split:** Specific formula/gap interpretation vs. full profile → shock identification are separable.

**Card A — PADP−PAWP gap: calculation and interpretation**
> **FRONT:** PA catheter: CVP 18, PA 52/26, PAWP 24, CO 1.8, SVR 2600. PADP − PAWP = _______ mmHg. This gap indicates _______ is present (or absent).
>
> **BACK:** PADP − PAWP = 26 − 24 = **2 mmHg** — within normal (<5 mmHg). **No elevated PVR** — PADP is a reliable surrogate for PAWP here. Primary pulmonary hypertension is NOT the culprit; elevated PA pressures (52/26) reflect passive back-pressure from elevated LV filling (PAWP 24), not primary pulmonary vascular disease.  
> → CCRN KEY: PA diastolic − PCWP >5 mmHg = intrinsic pulmonary vascular disease (PE, primary PAH, ARDS). Within normal = left heart problem (back-pressure).

**Card B — Complete PA catheter profile → shock type**
> **FRONT:** The hemodynamic profile (low CO 1.8, high SVR 2600, high PAWP 24) confirms _______ shock. PAWP 24 tells you that the _______ is the problem, not volume depletion.
>
> **BACK:** **Cardiogenic shock** — complete profile: ↓CO + ↑SVR (reflex vasoconstriction) + ↑PAWP (LV cannot empty → back-pressure) + ↑CVP (backs up to right heart). PAWP 24 = **left ventricle** is the problem — so severely impaired it cannot empty adequately. **Do NOT give fluids.**  
> → CCRN KEY: Reading the complete PA catheter profile: CVP = right preload; PADP ≈ PAWP (if no PH) = left preload; CO = pump; SVR = afterload. All five together identify shock type and correct intervention.

---

### SPLIT 36 — nid 1778774449018 · Chunk 32 · HIGH
**Topic:** ICP A-waves + CPP during wave + EVD intervention + Cushing's triad  
**Why split:** ICP crisis management (EVD drainage) and herniation recognition (Cushing's triad) are two separate nursing competencies.

**Card A — ICP plateau waves: CPP and EVD intervention**
> **FRONT:** ICP monitor: baseline 22, recurring A waves to 78 mmHg lasting 8 minutes. MAP 85 mmHg. During a plateau wave, CPP = _______. The fastest bedside ICP-reducing intervention if EVD is in place: _______.
>
> **BACK:** CPP = MAP − ICP = 85 − 78 = **7 mmHg** — essentially zero cerebral perfusion. Fastest intervention: **Drain CSF** — open EVD at prescribed drainage level, allow 5–10 mL to drain, reassess ICP immediately. Removing even small CSF volume descends the volume-pressure curve back into the compensated zone, breaking the vasodilatory cascade. Effect: immediate (seconds to minutes).  
> → CCRN KEY: Document: volume drained, ICP before/after, patient response. Multiple A waves = cumulative ischemic injury.

**Card B — Cushing's triad: recognition and emergency response**
> **FRONT:** The clinical triad of HYPERTENSION + BRADYCARDIA + IRREGULAR RESPIRATIONS is called _______ and indicates _______.
>
> **BACK:** **Cushing's triad** — indicates **brainstem compression from impending/active transtentorial herniation**. Brainstem becomes ischemic → autonomic storm: massive sympathetic discharge (hypertension), then vagal reflex (bradycardia), loss of respiratory centers (Biot's or ataxic breathing). Pre-terminal finding.  
> → CCRN KEY: Response: call rapid response/code team immediately. Simultaneously: (1) Drain EVD, (2) Hyperventilate to PaCO₂ 30–35 mmHg, (3) Mannitol or 23.4% NaCl bolus, (4) Notify neurosurgery for emergent decompression. Every minute = irreversible brainstem damage.

---

### SPLIT 37 — nid 1778774449036 · Chunk 32 · HIGH
**Topic:** Post-arrest CPP + what diagnosis + two physiologic drivers of ICP elevation  
**Why split:** CPP calculation + diagnosis vs. mechanistic explanation of ICP drivers are distinct.

**Card A — Post-arrest CPP calculation and diagnosis**
> **FRONT:** Set MAP 70, ICP 35. CPP = _______. This CPP is CRITICAL. The diagnosis producing ICP 35 despite MAP 70 in a post-cardiac arrest patient is _______.
>
> **BACK:** CPP = 70 − 35 = **35 mmHg** — severe ischemia zone, emergency. Diagnosis: **cytotoxic cerebral edema from global ischemia-reperfusion injury** — after cardiac arrest, global ischemia → ATP depletion → Na/K-ATPase failure → intracellular Na and water accumulation → neuronal swelling. Unlike vasogenic edema, cytotoxic edema does NOT respond well to steroids or mannitol (intracellular, not interstitial).  
> → CCRN KEY: Post-ROSC targets: MAP ≥65–70, SpO₂ 94–98%, PaCO₂ 35–45 mmHg, temp 33–36°C per TTM protocol.

**Card B — Two drivers of ICP elevation post-arrest**
> **FRONT:** Two physiologic drivers of ICP elevation after global ischemia-reperfusion: _______ and _______.
>
> **BACK:** **(1) Cytotoxic edema** — neuronal swelling from ischemia-reperfusion, free radical injury, glutamate excitotoxicity. Peaks at 24–72h post-arrest. **(2) Post-ischemic hyperemia** — following ROSC, loss of cerebrovascular autoregulation → pressure-passive CBF → hyperemia → ↑cerebral blood volume → ↑ICP. Mitigated by avoiding MAP >100 (prevents forced hyperemia) and normocapnia (prevents vasodilation from hypercapnia).  
> → CCRN KEY: TTM 33–36°C reduces CMRO₂ (5–7% per °C) → limits ischemia-reperfusion injury → reduces post-arrest cerebral edema. TTM trial (NEJM 2013): 36°C vs 33°C — no significant mortality difference. Most centers use 36°C with strict fever avoidance.

---

### SPLIT 38 — nid 1778774449048 · Chunk 32 · HIGH
**Topic:** CAM-ICU assessment + SAT protocol details + SAT/SBT outcome data  
**Why split:** Delirium assessment (diagnosis) and sedation interruption protocol (procedure) are distinct nursing competencies.

**Card A — CAM-ICU: why unobtainable at RASS −4**
> **FRONT:** A post-op day 2 patient is intubated, RASS −4, on propofol 40 mcg/kg/min + fentanyl. CAM-ICU is _______. Why is this clinically significant?
>
> **BACK:** CAM-ICU: **unable to assess** — RASS −4 (deep sedation) cannot participate in the inattention test. Clinically significant: delirium cannot be ruled in or out. Deep sedation itself is a major delirium risk factor, and the patient cannot demonstrate delirium while deeply sedated. The deeper the sedation, the higher the delirium burden upon awakening.  
> → CCRN KEY: Target RASS −1 to 0 for most ICU patients — allows CAM-ICU assessment, patient communication, and early mobility. Deep sedation (RASS ≤−3) is associated with prolonged MV, ICUAW, PICS.

**Card B — SAT protocol: what is held, what continues, and outcomes**
> **FRONT:** During a SAT, _______ is held while _______ is continued. SAT PASS criterion for RASS: _______ or better for ≥5 minutes. Daily SAT + SBT reduces mechanical ventilation by _______ days.
>
> **BACK:** Hold: **all sedatives** (propofol, benzos, dexmedetomidine). Continue: **analgesia** (fentanyl at maintenance — do not abruptly withdraw). SAT PASS: patient achieves RASS **−1 or better** for ≥5 min without: RASS ≥+2, RR >35, SpO₂ <88%, acute arrhythmia. Combined SAT + SBT reduces MV by **~3 days** (Girard MENDS/SLEAP trials, NEJM 2008).  
> → CCRN KEY: SAT FAIL → restart sedation at HALF prior dose. Then reassess cause: pain → increase analgesia; agitation from hypoxia → check vent/SpO₂/ABG; delirium → non-pharmacologic first.

---

### SPLIT 39 — nid 1778774449006 · Chunk 32 · MEDIUM
**Topic:** CPP calculation + BTF target + how to achieve target (MAP vs ICP approach)  
**Why split:** Formula + target vs. treatment strategy are distinct learning targets.

**Card A — CPP calculation and BTF target**
> **FRONT:** TBI patient: MAP 68, ICP 32. CPP = _______. BTF guideline CPP target for severe TBI: _______ mmHg.
>
> **BACK:** CPP = 68 − 32 = **36 mmHg** — critically below target. BTF target: **60–70 mmHg**. Floor = 60 mmHg minimum. Targets above 70 NOT recommended — associated with ↑ARDS risk without proven neurological benefit.  
> → CCRN KEY: Bedside CPP reflex: after every ICP reading, calculate CPP = MAP − ICP. If CPP <60 → notify provider. Don't report ICP in isolation — always include both values.

**Card B — Achieving CPP target: MAP vs ICP approach**
> **FRONT:** To reach CPP 60 mmHg with ICP 32, MAP must be raised to at least _______ mmHg. To reach CPP 60 with MAP 68, ICP must fall to _______ mmHg. The preferred approach is treating _______ because _______.
>
> **BACK:** MAP needed: 60 + 32 = **92 mmHg** (vasopressors). ICP needed: 68 − 60 = **8 mmHg** (osmotherapy + CSF drainage). Most efficient: **treat both simultaneously** — partial success on each axis (e.g., MAP 80 + ICP 18 = CPP 62) achieves target with lower drug doses.  
> → CCRN KEY: Treating ICP preferred because: (1) addresses the pathology directly; (2) lowers ICP also improves cerebrovascular compliance; (3) raising MAP with intact autoregulation may not improve CBF (vessels autoregulate). ICP treatment is more mechanistically targeted.

---

### SPLIT 40 — nid 1778774449009 · Chunk 32 · MEDIUM
**Topic:** Mannitol mechanism (osmotic + rheological) + osmolality contraindication  
**Why split:** Two mechanisms of action vs. monitoring/contraindication threshold are distinct.

**Card A — Mannitol mechanisms of ICP reduction**
> **FRONT:** TBI patient given mannitol 0.5 g/kg IV. Two mechanisms by which mannitol reduces ICP: _______ and _______.
>
> **BACK:** **(1) Osmotic** — creates osmotic gradient between blood (↑osmolality) and brain interstitium → draws free water from edematous brain into vascular space → reduces cerebral edema and ICP. Onset: 15–30 min. **(2) Rheological** — reduces blood viscosity → ↑cerebral microvascular flow → cerebral arteriolar autoregulatory vasoconstriction (↑flow) → ↓cerebral blood volume → ↓ICP. Onset: immediate (minutes).  
> → CCRN KEY: HTS vs mannitol: HTS reduces ICP via same osmotic mechanism WITHOUT osmotic diuresis → expands intravascular volume (↑MAP) while reducing ICP — preferred in hypotensive TBI.

**Card B — Mannitol contraindication threshold**
> **FRONT:** Mannitol is contraindicated when serum osmolality exceeds _______ mOsm/kg. The reason for this ceiling: _______.
>
> **BACK:** Contraindicated when serum Osm > **320 mOsm/kg**. Reason: above this threshold, the BBB becomes leaky to mannitol → mannitol enters brain tissue → brain Osm rises → water moves INTO brain (reverse osmotic gradient) → cerebral edema **worsens**.  
> → CCRN KEY: Mannitol monitoring: serum Osm + osmol gap q4–6h during ICP therapy. Hold if Osm >320 OR osmol gap >20 mOsm/kg. Also monitor serum Na (hypernatremia) and UO (osmotic diuresis → hypovolemia → ↓MAP → ↓CPP).

---

### SPLIT 41 — nid 1778774449033 · Chunk 32 · MEDIUM
**Topic:** CPP chart variations + BTF target + why ICP treatment preferred over MAP elevation  
**Why split:** Calculation exercise vs. rationale comparison are distinct domains.

**Card A — CPP chart calculations**
> **FRONT:** Set MAP 85, ICP 22 on the CPP chart: CPP = _______. Now set MAP 65, ICP 18: CPP = _______. BTF target for severe TBI: _______ mmHg.
>
> **BACK:** MAP 85 − ICP 22 = **63 mmHg** (target range, acceptable). MAP 65 − ICP 18 = **47 mmHg** — below target, ischemia zone, immediate intervention needed. BTF target: **60–70 mmHg**.  
> → CCRN KEY: After every ICP reading calculate CPP. CPP <60 = notify provider immediately. The first CPP example shows "acceptable" numbers can still require reassessment if trending downward.

**Card B — Why treating ICP is preferred over raising MAP**
> **FRONT:** CPP can be raised by either _______ MAP or _______ ICP. Treating ICP is preferred because _______.
>
> **BACK:** ↑ MAP (vasopressors) OR ↓ ICP (osmotherapy, EVD drainage, HOB 30°, sedation). Treating ICP preferred: **(1)** Directly addresses the PATHOLOGY (swelling, hydrocephalus) rather than compensating around it. **(2)** ↓ICP improves cerebrovascular compliance, reducing further ICP spikes. **(3)** ↑MAP with intact autoregulation causes cerebral vasoconstriction without improving CBF. **(4)** Every 1 mmHg ICP reduction = 1 mmHg CPP gain with no vascular side effects.  
> → CCRN KEY: Report CPP with every ICP value: "ICP is 28, MAP is 80, CPP is 52 — below our target of 60."

---

### SPLIT 42 — nid 1778774449039 · Chunk 32 · MEDIUM
**Topic:** CPP + herniation side + three nursing interventions + craniectomy  
**Why split:** Herniation recognition vs. nursing intervention sequence are separable domains.

**Card A — CPP and herniation pattern recognition**
> **FRONT:** Set MAP 90, ICP 40. CPP = _______. This patient has a blown right pupil and posturing. Herniation pattern: _______ (side) — and why.
>
> **BACK:** CPP = 90 − 40 = **50 mmHg** — below target. Blown RIGHT pupil + right-sided herniation signs = **right-sided uncal herniation** — right temporal lobe uncus herniates through the tentorium → compresses RIGHT CN III → right pupil dilates and becomes non-reactive. LEFT-sided motor deficit expected (right cerebral hemisphere → left corticospinal tract). Exception: Kernohan's notch (ipsilateral motor signs = false localizing sign).  
> → CCRN KEY: Bilateral fixed dilated pupils = bilateral herniation = very poor prognosis. Unilateral = still salvageable with immediate intervention.

**Card B — Three nursing interventions + surgical option**
> **FRONT:** Three simultaneous nursing interventions: _______, _______, and _______. If ICP does not respond, the emergent surgical option is _______.
>
> **BACK:** **(1) Notify neurosurgery and attending emergently** — every minute of herniation = irreversible brainstem damage. **(2) Drain CSF via EVD** if in place (open at prescribed level, drain 5–10 mL) — fastest ICP reduction at bedside. **(3) Emergent hyperventilation to PaCO₂ 30–35 mmHg** — adjust RR on vent immediately; cerebral vasoconstriction ↓ICP in 30–60 sec. Bridge therapy only. Surgical: **decompressive craniectomy** — bone flap removal allows outward expansion.  
> → CCRN KEY: ICP toolkit order: HOB/positioning → sedation/analgesia → EVD drainage → osmotherapy → NMBA → hyperventilation → barbiturate coma/TTM → craniectomy. Herniation signs = jump to items 2+6 with simultaneous surgical consultation.

---

### SPLIT 43 — nid 1778776089003 · Chunk 33 · HIGH
**Topic:** NE alpha-1 dominance explains no reflex bradycardia vs pure alpha agonists  
**Why split:** Receptor mechanism vs. clinical application comparison are distinct.

**Card A — NE receptor mechanism**
> **FRONT:** The chart shows norepinephrine maintains high alpha-1 activity (~80%) with moderate beta-1 (~35%) across all doses. This explains why norepinephrine causes _______ (net hemodynamic effect).
>
> **BACK:** ↑SVR (vasoconstriction) + ↑MAP with **maintained cardiac output** — the moderate β1 activity partially offsets vagal reflexes and supports inotropy, preventing the severe CO drop that pure α1 agonism causes.  
> → CCRN KEY: NE = α1 dominant + β1 support → ↑MAP with maintained CO. First-line in septic shock. Epinephrine shows a crossover on the chart — β1 dominant at low doses, α1 overtakes at high doses.

**Card B — Why NE avoids reflex bradycardia**
> **FRONT:** Norepinephrine does NOT cause the _______ seen with pure alpha agonists like phenylephrine, because _______.
>
> **BACK:** Does not cause **severe reflex bradycardia** — because moderate **β1 activity** partially counteracts the baroreceptor-mediated vagal response that pure α1 agonism (phenylephrine) triggers. Phenylephrine: pure α1 → reflex bradycardia + ↓CO. NE: β1 co-stimulation maintains HR and CO while α1 raises SVR.  
> → CCRN KEY: Phenylephrine clinical niche: vasodilatory shock with preserved/high CO where pure vasoconstriction is needed without chronotropy (e.g., AF with rapid rate + septic shock). Avoid in cardiogenic shock (↑SVR without inotropy worsens afterload).

---

### SPLIT 44 — nid 1778776089006 · Chunk 33 · HIGH
**Topic:** Septic shock vasopressor selection — why NE, not phenylephrine  
**Why split:** Hemodynamic assessment (recognizing which parameter fails) vs. drug selection rationale are distinct.

**Card A — Hemodynamic assessment in hyperdynamic septic shock**
> **FRONT:** A septic shock patient: MAP 55, HR 118, CO 7.2, SVR 480. The chart shows phenylephrine's alpha-1 curve is flat at ~90% with zero beta-1. The hemodynamic problem requiring treatment is _______.
>
> **BACK:** **Critically low SVR (480; normal 800–1200)** despite high CO — distributive/vasodilatory failure. The vasculature is massively dilated; cardiac output is compensatorily high. The MAP is falling because SVR cannot maintain perfusion pressure.  
> → CCRN KEY: In hyperdynamic septic shock: flow is present (high CO), but distribution is wrong (low SVR). Treatment: restore SVR with a vasopressor that does not suppress the compensatory high CO.

**Card B — Drug selection: NE vs phenylephrine**
> **FRONT:** The correct first-line vasopressor is _______, not phenylephrine, because _______.
>
> **BACK:** **Norepinephrine** — not phenylephrine. Phenylephrine's pure α1 effect would raise SVR and MAP but cause reflex bradycardia (HR↓) and ↓CO in an already compensating heart. NE provides α1 (↑SVR/↑MAP) + β1 (maintains CO). Phenylephrine reserved for cases where tachycardia must be avoided.  
> → CCRN KEY: If septic shock persists on NE >0.25 mcg/kg/min, add vasopressin (V1 receptor — different mechanism). If low CO persists despite adequate MAP → add dobutamine.

---

### SPLIT 45 — nid 1778776089009 · Chunk 33 · HIGH
**Topic:** Epi vs dopamine dose-receptor comparison + first-line indications  
**Why split:** Receptor pharmacology comparison vs. clinical indication history are distinct.

**Card A — Epinephrine and dopamine: low-dose receptor profile**
> **FRONT:** Comparing epinephrine and dopamine at equivalent low dose levels: epinephrine shows _______ dominant activity, while dopamine at the same relative dose shows _______.
>
> **BACK:** Epinephrine low dose: **β1 dominant** (↑HR, ↑CO, bronchodilation). Dopamine at equivalent relative dose: **dopaminergic/mixed** (DA receptors + emerging β1) — less pure beta effect.  
> → CCRN KEY: This pharmacologic difference matters in anaphylaxis: epinephrine's β2 bronchodilation + α1 vasoconstriction + β1 cardiac support makes it uniquely suited. Dopamine cannot replicate this profile.

**Card B — First-line indications: epi vs dopamine**
> **FRONT:** This pharmacologic difference explains their different first-line indications: epinephrine for _______, dopamine historically for _______.
>
> **BACK:** Epinephrine: **anaphylaxis** (β2 bronchodilation + α1 vasoconstriction + β1 cardiac) and **cardiac arrest** (ALS protocol). Dopamine: historically cardiogenic shock — but 2019 meta-analyses showed dopamine ↑mortality vs NE in shock (more arrhythmias). Current guidelines: NE first; dopamine only if significant bradycardia is present.  
> → CCRN KEY: SOAP-II (2010): dopamine vs NE — dopamine group had 2× arrhythmias and worse 28-day mortality in cardiogenic shock subgroup. Dopamine is no longer first-line in septic shock.

---

### SPLIT 46 — nid 1778776089048 · Chunk 33 · HIGH
**Topic:** Ketamine sub-dissociative analgesia — NMDA mechanism + opioid comparison  
**Why split:** Receptor mechanism vs. clinical advantage vs. opioids are distinct learning targets.

**Card A — Ketamine: NMDA receptor mechanism**
> **FRONT:** The analgesic ladder shows ketamine at sub-dissociative doses (0.1–0.3 mg/kg IV or 0.1–0.5 mg/kg/hr infusion) provides analgesia via _______ receptor antagonism.
>
> **BACK:** **NMDA (N-methyl-D-aspartate) receptor antagonism** — blocks central sensitization and "wind-up" of pain pathways by preventing glutamate-mediated depolarization at the dorsal horn.  
> → CCRN KEY: Sub-dissociative ketamine does NOT produce full dissociative anesthesia. The patient remains conscious and communicative. RSI dose (1–2 mg/kg) = dissociative. Analgesic dose (0.1–0.3 mg/kg) = sub-dissociative: pain relief without sedation.

**Card B — Ketamine advantages over opioids**
> **FRONT:** Sub-dissociative ketamine offers the advantage of _______ compared to opioids.
>
> **BACK:** Preserves **respiratory drive and airway reflexes** at sub-dissociative doses — useful for procedural analgesia without respiratory depression. Also: **opioid-sparing effect** (↓total opioid dose), bronchodilation (β2 stimulation + direct smooth muscle relaxation), no histamine release.  
> → CCRN KEY: Best uses: procedure-related pain (line placement, dressing changes), opioid-tolerant patients, trauma analgesia, opioid-induced hyperalgesia. Avoid in: uncontrolled hypertension, active psychosis. ICP contraindication is now questioned — may be safe in intubated patients with ICP monitors.

---

### SPLIT 47 — nid 1778776089021 · Chunk 33 · MEDIUM
**Topic:** Amiodarone multi-class mechanism + monitoring requirements  
**Why split:** Multi-phase mechanism (pharmacology) vs. organ toxicity monitoring (nursing) are distinct.

**Card A — Amiodarone multi-class mechanism**
> **FRONT:** Amiodarone is unique because the action potential chart shows it targets _______ phases simultaneously. This multi-class mechanism means it is effective for both _______ and _______.
>
> **BACK:** Targets **all four phases**: Class I (Na+, Phase 0), Class II (β-block, Phase 4), Class III (K+, Phase 3), Class IV (Ca2+, Phase 2) — a "dirty" drug. Effective for both **atrial** (AF/flutter) and **ventricular** (VT/VF) arrhythmias.  
> → CCRN KEY: Amiodarone is the most commonly used antiarrhythmic in the ICU. Safe in HF (no significant negative inotropy at standard doses). Half-life 40–55 days — effects and toxicity persist months after stopping.

**Card B — Amiodarone monitoring requirements**
> **FRONT:** Amiodarone requires monitoring for _______.
>
> **BACK:** Four major toxicities: **(1) Pulmonary toxicity** (CXR, PFTs — most serious; interstitial pneumonitis). **(2) Thyroid dysfunction** (hypo- AND hyperthyroidism — iodine-rich; check TSH q6 months). **(3) Hepatotoxicity** (LFTs). **(4) Corneal microdeposits** (usually asymptomatic; slit-lamp exam). Peripheral neuropathy with long-term use.  
> → CCRN KEY: New hypoxia or new infiltrates on CXR in a patient on amiodarone → consider amiodarone pulmonary toxicity. Discontinue and corticosteroids if suspected. Toxicity can occur even at low doses after prolonged use.

---

### SPLIT 48 — nid 1778776089051 · Chunk 33 · MEDIUM
**Topic:** PADIS pain-first assessment + correct intervention vs. increasing sedation  
**Why split:** Clinical assessment interpretation vs. intervention choice are distinct nursing competencies.

**Card A — PADIS clinical assessment**
> **FRONT:** Intubated patient: NRS pain 7/10, RASS −3 (deeply sedated on propofol + fentanyl), CAM-ICU positive. Per PADIS guidelines, what does this clinical picture represent?
>
> **BACK:** **Pain-driven agitation masked by deep sedation** — the patient has significant uncontrolled pain (NRS 7) AND ICU delirium (CAM-ICU+), but is being deeply sedated. Deep sedation itself worsens ICU delirium and prolongs MV. The pain is the driver; the sedation is a cover.  
> → CCRN KEY: PADIS 2018 sequencing: Assess and treat PAIN first (A-1C = Analgesia-First Care) → target light sedation (RASS −1 to 0) → minimize benzos (↑delirium) → mobilize early → promote sleep.

**Card B — Correct PADIS intervention**
> **FRONT:** The correct PADIS-guided intervention is _______, not increasing sedation, because _______.
>
> **BACK:** Perform SAT (hold sedation, assess), **optimize analgesia** (↑fentanyl or add scheduled acetaminophen/ketamine), target RASS −1 to 0. NOT increasing sedation because: deeper sedation worsens ICU delirium, prolongs MV, increases ICU-acquired weakness, and masks inadequately treated pain.  
> → CCRN KEY: Dexmedetomidine (α2 agonist) provides sedation + analgesia + anxiolysis without respiratory depression and ↓delirium vs midazolam (MENDS trial). Consider for RASS −1 to −2 goal when weaning from deeper sedation.

---

### SPLIT 49 — nid 1778776089000 · Chunk 33 · LOW
**Topic:** Dopamine dose-receptor: DA at low dose + alpha-1 at high dose  
**Why split:** Two distinct receptor effects at two distinct dose ranges — separable learning targets.

**Card A — Dopamine: low-dose DA receptor effect**
> **FRONT:** On the vasopressor dose-response chart, dopamine at low doses (1–3 mcg/kg/min) primarily activates _______ receptors, causing _______.
>
> **BACK:** **Dopaminergic (DA1/DA2) receptors** → renal and mesenteric vasodilation (↑GFR, ↑natriuresis). "Renal dose dopamine" has been disproven (Bellomo trial: no difference in AKI outcomes) — this effect is real but clinically insignificant for renal protection.  
> → CCRN KEY: The chart shows the DA-receptor activity curve is highest at 1–5 mcg/kg/min. The clinical teaching about "renal dose" is obsolete — optimize MAP and avoid nephrotoxins instead.

**Card B — Dopamine: high-dose alpha-1 shift**
> **FRONT:** At high doses (>10 mcg/kg/min), dopamine shifts to activate _______ receptors, causing _______.
>
> **BACK:** **Alpha-1 receptors** → vasoconstriction, ↑SVR. At high doses, dopamine behaves similarly to norepinephrine but with more arrhythmias (atrial fibrillation, SVT).  
> → CCRN KEY: In practice, dopamine's dose-dependent selectivity is less predictable than NE. SOAP-II 2010: dopamine inferior to NE in septic shock (2× arrhythmias). Current guidelines: NE first-line; dopamine only if significant bradycardia present and arrhythmia risk low.

---

### SPLIT 50 — nid 1778808560021 · Chunk 34 · HIGH
**Topic:** ATLS class + blood loss estimate + MTP activation + product ratio  
**Why split:** Shock classification/quantification vs. MTP protocol execution are distinct nursing competencies.

**Card A — ATLS classification and estimated blood loss**
> **FRONT:** A 70 kg trauma patient: HR 136, SBP 74, RR 38, GCS 13. ATLS class is _______, estimated blood loss is _______.
>
> **BACK:** **Class III–IV** — estimated blood loss > **1,500 mL** (>30% of estimated 4.9L blood volume). Class III: 30–40%, 1500–2000 mL. Class IV: >40%, >2000 mL. Both require immediate MTP.  
> → CCRN KEY: ATLS class IV = life-threatening hemorrhage. Don't wait for lab confirmation to activate MTP — activate on clinical grounds (HR >120 + SBP <90 + mechanism).

**Card B — MTP activation: product ratio and adjuncts**
> **FRONT:** The nurse immediately activates _______ targeting a product ratio of _______. Key adjuncts within 3 hours of injury: _______.
>
> **BACK:** **Massive Transfusion Protocol (MTP)**, ratio **1:1:1** (pRBC:FFP:platelets) — PROPPR trial (2015) confirmed this ratio reduces 24h mortality vs historical ratios. Adjuncts: **TXA 1g IV within 3 hours** (CRASH-2: no benefit after 3h, possibly harmful); CaCl₂ 10 mL 10% per 4 units pRBC; permissive hypotension (SBP 80–90 penetrating, MAP 50–65 blunt) until surgical control.  
> → CCRN KEY: Avoid large-volume crystalloid (>1–2L) — causes dilutional coagulopathy, hypothermia, and hyperchloremic acidosis. In class III–IV, blood products ARE the resuscitation fluid.

---

### SPLIT 51 — nid 1778812211036 · Chunk 35 · HIGH
**Topic:** Cosyntropin stimulation test — threshold value + clinical context  
**Why split:** The threshold number (diagnosis criteria) vs. when to test and how to interpret (clinical application) are distinct.

**Card A — Cosyntropin stimulation threshold**
> **FRONT:** On the cortisol response chart, adrenal insufficiency is confirmed when post-cosyntropin cortisol at 30–60 min fails to reach _______ mcg/dL.
>
> **BACK:** Fails to reach **18 mcg/dL** → adrenal insufficiency confirmed. Normal response: peak ≥18–20 mcg/dL above baseline, or absolute peak ≥18 mcg/dL. Cosyntropin (synthetic ACTH) 250 mcg IV; cortisol drawn at 0, 30, 60 min.  
> → CCRN KEY: In septic shock with critical illness, random cortisol <10 mcg/dL is diagnostic without stimulation testing. CIRCI (critical illness-related corticosteroid insufficiency): delta-cortisol <9 mcg/dL after stim, or random <10 mcg/dL.

**Card B — Cosyntropin test: clinical use in ICU**
> **FRONT:** The Surviving Sepsis Campaign 2021 recommendation regarding routine cortisol testing before steroids is _______, because _______.
>
> **BACK:** SSC 2021: does **NOT recommend routine cortisol testing** — give hydrocortisone empirically when vasopressor-dependent (NE or vasopressin still required despite adequate fluid resuscitation). Reason: stimulation test results do not reliably predict steroid responsiveness in septic shock; empirical treatment when indicated is non-inferior.  
> → CCRN KEY: Stress dose regimen: hydrocortisone 50 mg IV q6h OR 200 mg/day continuous × 5–7 days. Wean with vasopressor taper — do NOT abruptly discontinue.

---

### SPLIT 52 — nid 1778812211006 · Chunk 35 · MEDIUM
**Topic:** DKA severe — K+ before insulin (what to do) + why (pathophysiology)  
**Why split:** Nursing action vs. mechanistic rationale are distinct.

**Card A — DKA: first intervention priority**
> **FRONT:** DKA patient: pH 6.91, HCO₃ 6, glucose 510, K⁺ 3.1 mEq/L. First intervention is _______, not _______.
>
> **BACK:** First: **Replace K⁺ to ≥3.3 mEq/L before starting insulin**. Not: start insulin infusion first.  
> → CCRN KEY: K⁺ <3.3 + DKA = potassium replacement is the priority. Hold insulin, give K⁺ 20–40 mEq/hr IV, recheck before insulin start. Also begin aggressive NS or LR resuscitation (1–1.5 L/hr first hour) — volume depletion is always present in DKA.

**Card B — Why K+ before insulin: pathophysiology**
> **FRONT:** The reason K+ must be replaced BEFORE starting insulin in DKA is _______.
>
> **BACK:** Insulin **drives K⁺ intracellularly** — starting insulin with K⁺ 3.1 risks fatal **hypokalemia and cardiac arrhythmia** (VF). The body appears to have near-normal K⁺ because acidosis drives K⁺ extracellularly; as insulin corrects the acidosis and moves K⁺ back into cells, serum K⁺ drops precipitously.  
> → CCRN KEY: DKA total body K⁺ is always depleted even when serum K⁺ appears normal. Anticipate hypokalemia as insulin is started and plan aggressive K⁺ replacement in advance.

---

### SPLIT 53 — nid 1778812211015 · Chunk 35 · MEDIUM
**Topic:** HHS vs DKA pattern recognition + HHS fluid priority + why not high-dose insulin first  
**Why split:** Pattern recognition (diagnosis) vs. treatment priority (nursing action) are distinct.

**Card A — HHS pattern recognition**
> **FRONT:** Patient: glucose 740 mg/dL, serum osmolality 338 mOsm/kg, pH 7.36, HCO₃ 23, ketones trace. The comparison chart pattern matches _______.
>
> **BACK:** **HHS (Hyperosmolar Hyperglycemic State)** — markedly elevated glucose + extreme hyperosmolality (>320) + near-normal pH + minimal ketones. DKA contrast: DKA = lower glucose, normal/low osmolality, low pH, high ketones, gap acidosis.  
> → CCRN KEY: HHS mortality (5–20%) exceeds DKA (1–5%) due to age, precipitating illness, and delayed recognition. Most common in elderly type 2 diabetics; DKA in type 1.

**Card B — HHS treatment: fluid first, why not insulin-first**
> **FRONT:** HHS requires _______ as the initial priority, not _______, because _______.
>
> **BACK:** Priority: **aggressive IV fluid resuscitation** (NS 1 L/hr × first 2h, then 0.45% NaCl) to correct hyperosmolality. Not: high-dose insulin as primary therapy because rapid glucose correction without fluid replacement worsens hyperosmolality and risks **cerebral edema**. Lower glucose slowly (~50 mg/dL/hr). HHS fluid deficit: 8–10 L.  
> → CCRN KEY: Start low-dose insulin (0.05–0.1 units/kg/hr) or none until glucose <300. Add D5W when glucose reaches 300. The hyperosmolality is the emergency — correct it before aggressively correcting glucose.

---

### SPLIT 54 — nid 1778812211018 · Chunk 35 · MEDIUM
**Topic:** Anion gap formula + calculation + classification  
**Why split:** Formula application vs. interpretation/classification are distinct.

**Card A — Anion gap formula and calculation**
> **FRONT:** On the anion gap chart with Na 138, Cl 100, HCO₃ 14, the anion gap = _______ mEq/L.
>
> **BACK:** AG = Na⁺ − (Cl⁻ + HCO₃⁻) = 138 − (100 + 14) = **24 mEq/L**. Formula: AG = Na − (Cl + HCO₃). Normal: 8–12 mEq/L (without albumin correction).  
> → CCRN KEY: Corrected AG for albumin: if albumin = 2 g/dL, add 2.5 × (4 − 2) = 5 to the calculated AG. In ICU patients with low albumin, uncorrected AG may miss a true HAGMA.

**Card B — Anion gap classification and causes**
> **FRONT:** An AG of 24 mEq/L is classified as _______ and indicates _______ in the blood.
>
> **BACK:** **High anion gap metabolic acidosis (HAGMA)** — elevated indicates unmeasured anions: lactate, ketones, uremia, toxins. MUDPILES: Methanol, Uremia, DKA, Propylene glycol, Isoniazid/Iron, Lactic acidosis, Ethylene glycol, Salicylates. ICU most often: lactate or DKA.  
> → CCRN KEY: NAGMA (normal anion gap metabolic acidosis): GI bicarbonate loss (diarrhea), renal tubular acidosis, saline overload (dilutional), Addison's disease. Hyperchloremia from aggressive NS resuscitation is a common ICU cause.

---

### SPLIT 55 — nid 1778812211033 · Chunk 35 · MEDIUM
**Topic:** Burch-Wartofsky score calculation + PTU/iodine sequence + aspirin contraindication  
**Why split:** Score calculation vs. treatment sequence (and common error to avoid) are distinct.

**Card A — Burch-Wartofsky score**
> **FRONT:** Postoperative thyroidectomy patient: temp 40.2°C, HR 148, AF, agitation, new liver enzyme elevation. Burch-Wartofsky score = _______.
>
> **BACK:** Temp 40.2°C (+30) + HR 148 (+25) + AF (+10) + Agitation/CNS moderate (+20) + GI/Hepatic (+10) + Precipitant surgery (+10) = **105** — well above threshold of ≥45 (confirmed storm). Score ≥25 = treat as impending storm; ≥45 = confirmed.  
> → CCRN KEY: Treat impending storm (25–44) the same as confirmed storm. Thyroid storm is a clinical diagnosis — don't wait for TSH/free T4 in an acute presentation.

**Card B — Thyroid storm treatment sequence**
> **FRONT:** You hold _______ and give _______ first because _______.
>
> **BACK:** Hold: **aspirin** (displaces T4 from binding proteins → worsens storm). Give first: **PTU 500 mg PO/NG**, then wait 1 hour, THEN **Lugol iodine 10 drops q8h**. Because: iodine given before thionamide (PTU) causes acute hormone release (Jod-Basedow effect). Sequence is mandatory: PTU blocks synthesis → then iodine blocks release.  
> → CCRN KEY: Also: propranolol (β-blockade + inhibits T4→T3 conversion), dexamethasone 2 mg q6h (inhibits T4→T3 + possible AI), aggressive cooling (cooling blanket, acetaminophen — NOT aspirin). ICU admission, continuous cardiac monitoring.

---

### SPLIT 56 — nid 1778812211027 · Chunk 35 · LOW
**Topic:** Burch-Wartofsky diagnostic threshold + impending storm category  
**Why split:** Threshold (diagnosis criteria) vs. clinical action for each category are distinct.

**Card A — Burch-Wartofsky threshold for confirmed storm**
> **FRONT:** On the Burch-Wartofsky scoring chart, thyroid storm is diagnosed when the score reaches _______ or above.
>
> **BACK:** Score **≥45** = thyroid storm diagnosis (confirmed). Treat immediately with full storm protocol.  
> → CCRN KEY: Maximum possible score ~125. Key highest-point categories: Temperature (up to 30 pts), CNS effects (up to 30 pts), HR (up to 25 pts). High-temp + tachycardia + agitation = rapidly escalating score.

**Card B — Impending storm category and action**
> **FRONT:** A score of 25–44 indicates _______ and should be managed _______.
>
> **BACK:** Score 25–44 = **impending storm** — treat the **same as confirmed storm**. Do not wait for higher score or confirmatory labs. Starting treatment at impending stage prevents escalation to full storm with multi-organ failure.  
> → CCRN KEY: Thyroid storm is a clinical diagnosis; TSH and free T4 may be unavailable or unreliable in acute presentation. Treat the clinical picture, not the lab result.

---

### SPLIT 57 — nid 1778816132006 · Chunk 36 · HIGH
**Topic:** AKI Stage 2 staging + next intervention after fluid resuscitation completed  
**Why split:** Staging criteria vs. management decision (what not to do + what to do) are distinct.

**Card A — AKI staging**
> **FRONT:** Septic patient: creatinine rises 0.9 → 2.1 mg/dL, urine output 0.3 mL/kg/hr × 18 hours. AKI stage = _______.
>
> **BACK:** **Stage 2 AKI** — creatinine 2.3× baseline (2.1/0.9 = 2.3×) AND UO < 0.5 mL/kg/hr × ≥12h (both criteria met). KDIGO staging: Stage 1 = 1.5–2× or UO <0.5 mL/kg/hr ×6–12h; Stage 2 = 2–3× or UO <0.5 ×12–24h; Stage 3 = >3× or UO <0.3 ×24h or anuria ×12h.  
> → CCRN KEY: Always stage AKI using the HIGHER of the Cr and UO criteria. Document baseline Cr (pre-illness) — without it, staging is unreliable.

**Card B — Next intervention post-fluid-resuscitation**
> **FRONT:** Fluid resuscitation has been completed. Next intervention is _______, not _______, because _______.
>
> **BACK:** Next: **optimize MAP ≥65 with vasopressors; hold nephrotoxins; nephrology consult for Stage 2 in ICU**. Not: aggressive additional fluid boluses (after adequate resuscitation, fluid overload in AKI increases mortality — positive balance >10% body weight independently worsens outcomes).  
> → CCRN KEY: Furosemide does NOT prevent AKI progression or reduce need for dialysis — use only for volume overload management, not to "make urine." Monitor hourly UO and trending Cr.

---

### SPLIT 58 — nid 1778816132003 · Chunk 36 · MEDIUM
**Topic:** Post-cardiac surgery AKI Stage 3 + primary mechanism  
**Why split:** Staging vs. mechanism explanation are distinct learning targets.

**Card A — AKI staging: post-cardiac surgery**
> **FRONT:** Post-cardiac surgery patient: creatinine rises 1.0 → 3.2 mg/dL over 48 hours. This represents Stage _______.
>
> **BACK:** **Stage 3 AKI** — creatinine ≥3× baseline (3.2/1.0 = 3.2×). Stage 3 also triggered by absolute Cr ≥4.0 mg/dL with acute rise ≥0.5 mg/dL, or need for RRT.  
> → CCRN KEY: Cardiac surgery is the #2 cause of ICU-acquired AKI (sepsis is #1). Post-surgery Stage 3 = nephrology consult + RRT planning. Avoid nephrotoxins aggressively.

**Card B — Primary mechanism of cardiac surgery AKI**
> **FRONT:** The primary mechanism of AKI after cardiac surgery is _______.
>
> **BACK:** **Renal ischemia** from: reduced cardiac output, hypoperfusion during cardiopulmonary bypass (non-pulsatile flow), and contrast from intraoperative imaging. CPB also causes hemodilution (↓hematocrit → ↓O₂ carrying capacity), microemboli, and inflammatory activation.  
> → CCRN KEY: MAP ≥65 minimum in all AKI; MAP ≥80 in CKD patients with hypertensive history (their autoregulation is reset to higher baselines). Avoid NSAIDs, aminoglycosides, IV contrast in all AKI.

---

### SPLIT 59 — nid 1778816132015 · Chunk 36 · MEDIUM
**Topic:** CRRT dose calculation + KDIGO target + corrective action  
**Why split:** Calculation vs. target-and-action are distinct.

**Card A — CRRT dose calculation**
> **FRONT:** A 90 kg patient on CVVHDF has effluent rate set at 1,350 mL/hr. The CRRT dose chart shows _______ mL/kg/hr.
>
> **BACK:** Dose = 1,350 ÷ 90 = **15 mL/kg/hr** — below KDIGO target.  
> → CCRN KEY: Always calculate actual delivered dose (effluent rate ÷ actual body weight). Use actual (not ideal) weight. Delivered dose in practice is 15–20% less than prescribed due to filter clotting and circuit downtime.

**Card B — KDIGO target and corrective action**
> **FRONT:** This is _______ the KDIGO target, so you should _______.
>
> **BACK:** **Below** KDIGO target (20–25 mL/kg/hr). Action: **notify provider** — prescription should be increased to 25–30 mL/kg/hr to achieve actual dose of 20–25 (accounting for filter downtime and clotting losses). Sub-therapeutic dosing = inadequate solute and fluid removal.  
> → CCRN KEY: Prescribe 25–30 mL/kg/hr to achieve actual 20–25. Document actual delivered dose per shift, not just prescribed dose. Effluent = ultrafiltrate + dialysate (CVVHDF); ultrafiltrate alone (CVVH).

---

### SPLIT 60 — nid 1778816132018 · Chunk 36 · MEDIUM
**Topic:** CRRT dose calculation (70 kg patient) + prescribing principle for downtime  
**Why split:** Calculation vs. prescribing principle (why overprescribe) are distinct.

**Card A — CRRT dose calculation for 70 kg patient**
> **FRONT:** On the CRRT dose calculator, for a 70 kg patient the effluent rate needed to achieve the KDIGO target of 20–25 mL/kg/hr is _______.
>
> **BACK:** Target effluent rate = 20–25 mL/kg/hr × 70 kg = **1,400–1,750 mL/hr**.  
> → CCRN KEY: Document the target rate and verify it matches the pump setting at the start of each shift. If rate drifted down due to alarms/circuit issues, recalculate delivered dose.

**Card B — Why prescribe higher than the target dose**
> **FRONT:** The prescribed CRRT rate should be _______ mL/hr (for 70 kg) to actually ACHIEVE the target dose of 20–25 mL/kg/hr. The reason to prescribe higher: _______.
>
> **BACK:** Prescribe **1,750–2,100 mL/hr** (25–30 mL/kg/hr). Reason: delivered dose is ~15–20% less than prescribed due to filter clotting, line flushes, circuit downtime for labs and procedures. Prescribing at the target means under-delivery.  
> → CCRN KEY: Track cumulative downtime per shift. If circuit is down >30% of the time, notify provider — filter may need replacement or citrate anticoagulation optimization.

---

### SPLIT 61 — nid 1778816132024 · Chunk 36 · MEDIUM
**Topic:** CRRT dose verification + electrolyte losses pattern + nursing action  
**Why split:** Calculation + verification vs. electrolyte management (different clinical domain) are distinct.

**Card A — CRRT dose verification**
> **FRONT:** An 85 kg anuric patient is prescribed 2,100 mL/hr CRRT. Dose = _______ mL/kg/hr.
>
> **BACK:** Dose = 2,100 ÷ 85 = **24.7 mL/kg/hr** — within KDIGO target (20–25 mL/kg/hr). Prescription is appropriate.  
> → CCRN KEY: Always verify at shift start. If weight changes significantly (e.g., post-large fluid removal), recalculate dose with updated weight.

**Card B — CRRT electrolyte losses and nursing action**
> **FRONT:** Morning labs: phosphorus 1.1 mg/dL, magnesium 1.4 mEq/L, potassium 3.0 mEq/L. These electrolyte findings are caused by _______ and you _______.
>
> **BACK:** Caused by **CRRT continuously removing small electrolytes** (phosphorus, magnesium, potassium) via diffusion/convection — repletion in circuit bags or IV supplements required. Action: **replace electrolytes IV; notify provider for CRRT solution adjustment** (add phosphorus to dialysate/replacement bags if available); do NOT hold CRRT without provider order.  
> → CCRN KEY: CRRT-induced hypophosphatemia is common and underrecognized. Phosphorus replacement 15–30 mmol/day often required. Also: hypothermia (blood cools in extracorporeal circuit — use circuit heaters, target normothermia).

---

### SPLIT 62 — nid 1778816132042 · Chunk 36 · MEDIUM
**Topic:** ATN diagnosis (pattern recognition) + ATN management  
**Why split:** Diagnostic pattern identification vs. management (what to do / not do) are distinct.

**Card A — ATN diagnosis**
> **FRONT:** ICU patient post-cardiac arrest: creatinine rising, UO 0.2 mL/kg/hr despite 3L IVF, FeNa 3.2%, BUN:Cr 10:1, muddy brown casts. The chart pattern matches _______, caused by _______.
>
> **BACK:** **ATN (Acute Tubular Necrosis)** — FeNa >2% + muddy brown casts + BUN:Cr 10–15:1 = ATN confirmed. Cause: **ischemic ATN from cardiac arrest and post-resuscitation low-flow state** (global ischemia → tubular cell death). ATN is self-limited (recovery 1–3 weeks) if cause is removed and hemodynamics optimized.  
> → CCRN KEY: ATN diagnostic pattern: FeNa >2%, urine Na >40, muddy brown/granular casts on UA, BUN:Cr 10–15:1. Pre-renal: FeNa <1%, urine Na <20, no casts, BUN:Cr >20:1.

**Card B — ATN management: priorities and what NOT to do**
> **FRONT:** You prioritize _______, not _______, because _______.
>
> **BACK:** Priority: **optimize MAP ≥65 with vasopressors, avoid nephrotoxins, nephrology consult for dialysis planning**. Not: more aggressive fluid boluses (will not reverse established ATN — volume loading after adequate resuscitation causes fluid overload without improving renal function).  
> → CCRN KEY: Post-cardiac arrest ATN often requires temporary dialysis as bridge to recovery. Most ATN patients recover sufficient renal function to discontinue RRT within weeks. Recovery timeline: oliguria phase (1–3 weeks) → polyuric recovery phase → return to baseline (months).

---

### SPLIT 63 — nid 1778817792006 · Chunk 37 · HIGH
**Topic:** GI bleed — risk score + pre-endoscopy interventions + why not immediate endoscopy  
**Why split:** Risk quantification + pharmacology vs. clinical reasoning (sequence/safety) are distinct.

**Card A — GI bleed risk score and pre-endoscopy interventions**
> **FRONT:** Cirrhotic patient with massive hematemesis, SBP 78, HR 128, Hgb 6.1, INR 2.8. Risk score = _______. You initiate _______ and _______ before endoscopy.
>
> **BACK:** Score ~9 (High Risk — SBP <90 +3, HR ≥100 +1, Hgb <10 +3, liver disease +2). Initiate: **octreotide infusion** (25 mcg/hr — reduces portal pressure, variceal bleeding) + **ceftriaxone 1g IV/day** (antibiotic prophylaxis — reduces SBP risk, proven mortality benefit). Resuscitate to SBP ≥90 with blood products.  
> → CCRN KEY: Sequence: resuscitate → octreotide + antibiotics → endoscopy within 12h → TIPS if banding fails. Vasopressin analogs (terlipressin) reduce variceal bleeding mortality by ~35%.

**Card B — Why not immediate endoscopy**
> **FRONT:** Not immediate endoscopy while hemodynamically unstable, because _______.
>
> **BACK:** Blind intubation in shock + variceal bleeding carries high **aspiration and airway risk**; hemodynamic instability (MAP <65) increases procedural mortality. Stabilize first (MAP ≥65 via resuscitation) then scope. Propofol-assisted intubation before endoscopy recommended if Grade III–IV hepatic encephalopathy or hematemesis aspiration risk.  
> → CCRN KEY: Do NOT give MTP ratio blindly in cirrhosis — check TEG/ROTEM. Cirrhotic patients have altered coagulation (low fibrinogen, low platelets, low clotting factors — but also reduced anticoagulant proteins). TEG/ROTEM better characterizes the actual defect.

---

### SPLIT 64 — nid 1778817792024 · Chunk 37 · HIGH
**Topic:** MELD rise → cause + critical intervention (paracentesis + albumin)  
**Why split:** Diagnosing the precipitant vs. the specific treatment are distinct clinical actions.

**Card A — MELD rise: cause identification**
> **FRONT:** Cirrhotic patient's MELD rises from 18 to 32 over 72 hours (Cr 0.9→3.4, Bili 3.2→7.1, INR 1.6→2.8). This rise is most likely caused by _______.
>
> **BACK:** Most likely: **Spontaneous bacterial peritonitis (SBP)** triggering acute-on-chronic liver failure (ACLF) — SBP causes systemic inflammatory response that precipitates rapid organ failure in cirrhosis. MELD trajectory matters more than single value: jump from 18→32 in 3 days signals ACLF.  
> → CCRN KEY: Diagnostic paracentesis to confirm (PMN >250/mm³ in ascitic fluid = SBP). ACLF = organ failures on background of chronic liver disease; MELD >18 in ACLF = ICU-level care required.

**Card B — SBP critical intervention: albumin protocol**
> **FRONT:** The critical intervention within the next 24 hours is _______.
>
> **BACK:** **Diagnostic and therapeutic paracentesis + IV cefotaxime/ceftriaxone + IV albumin 1.5 g/kg on day 1, 1 g/kg on day 3** — proven to prevent HRS and reduce mortality by 33%. Albumin infusion with SBP treatment is standard of care. SBP precipitates HRS and ACLF — early albumin prevents renal failure by maintaining intravascular oncotic pressure and reducing inflammatory mediator release.  
> → CCRN KEY: Do NOT delay albumin infusion. If SBP confirmed → antibiotics + albumin simultaneously. Monitor renal function (Cr) and urine output closely — rising Cr after SBP diagnosis = HRS developing.

---

### SPLIT 65 — nid 1778818396003 · Chunk 38 · MEDIUM
**Topic:** DIC ISTH score calculation + diagnosis confirmation  
**Why split:** Score calculation vs. diagnosis confirmation and treatment priorities are distinct.

**Card A — ISTH DIC score calculation**
> **FRONT:** Septic patient: Plt 38K (↓ from 210K), PT prolonged 7 sec above normal, D-dimer markedly elevated, fibrinogen 0.8 g/L. ISTH score = _______.
>
> **BACK:** Plt <50K (+2) + PT >6s (+2) + D-dimer strongly elevated (+3) + fibrinogen <1 g/L (+1) = **8** — score ≥5 = overt DIC confirmed.  
> → CCRN KEY: ISTH scoring: Platelets: >100K=0, 50–100K=1, <50K=2. D-dimer: no increase=0, moderate=2, strong=3. PT: <3s=0, 3–6s=1, >6s=2. Fibrinogen: ≥1 g/L=0, <1 g/L=1.

**Card B — Overt DIC: treatment priorities**
> **FRONT:** Score 8 confirms overt DIC. Immediate treatment priorities: _______.
>
> **BACK:** **(1) Treat sepsis source** (antibiotics, source control — address the precipitant FIRST). **(2) Transfuse** platelets to ≥50K with active bleeding; FFP for PT/aPTT; cryoprecipitate (10-unit pool) to raise fibrinogen >150 mg/dL. **(3) Heparin in DIC: controversial** — consider only in thrombosis-dominant DIC (purpura fulminans, arterial clots); contraindicated in hemorrhage-dominant DIC.  
> → CCRN KEY: DIC causes by mechanism: tissue factor release (sepsis #1, trauma, amniotic fluid embolism, brain injury); endothelial activation (HELLP, TTP, vasculitis). Classic: APL (M3 AML) — most dramatic DIC, responds to ATRA + arsenic.

---

### SPLIT 66 — nid 1778818396015 · Chunk 38 · MEDIUM
**Topic:** FFP dose + INR result + volume concern + PCC alternative  
**Why split:** What to order (dose + expected result) vs. clinical limitation (volume) + better alternative are distinct.

**Card A — FFP: dose and expected result**
> **FRONT:** ICU patient: INR 2.4, active subarachnoid hemorrhage, urgent procedure needed. You order _______ units FFP, and the expected result is _______.
>
> **BACK:** Order: **4 units FFP** (standard dose for INR reversal in acute bleeding). Expected result: INR reduction by **~30–50%**, typically to 1.3–1.8 range (from 2.4). Does not fully normalize INR in most cases.  
> → CCRN KEY: FFP thaw time: ~20–30 min. In urgent situations this delay matters — 4F-PCC (no thaw, immediate) is preferred when speed is critical.

**Card B — Volume concern and PCC alternative**
> **FRONT:** You must also account for _______, which is why _______ is preferred when available.
>
> **BACK:** Must account for: **volume load** — 4 units FFP = ~1,000 mL, dangerous in cardiac/renal patients (fluid overload → pulmonary edema). Alternative: **4F-PCC (Kcentra) 25–50 units/kg** reverses warfarin within minutes, no crossmatch needed, 20–40 mL volume, no TRALI/TACO risk. Add Vitamin K 10 mg IV for sustained reversal beyond the PCC window.  
> → CCRN KEY: 4F-PCC advantages over FFP: (1) volume 50 mL vs 1,000 mL; (2) onset 15–30 min vs 1–4h; (3) more complete correction; (4) no blood-type matching; (5) no infectious risk. FFP still has a role when PCC unavailable, or for MTP ratio, or TTP (provides ADAMTS13).

---

### SPLIT 67 — nid 1778818396024 · Chunk 38 · MEDIUM
**Topic:** Lethal triad recognition + priorities alongside continued transfusion  
**Why split:** Recognition (what the triad is) vs. prioritized interventions (what to do/not do) are distinct.

**Card A — Lethal triad recognition**
> **FRONT:** Trauma patient receives 12 pRBC, 12 FFP, 4 apheresis platelets × 4 hours. Temperature 35.1°C, pH 7.18, INR 2.1. The chart shows _______ triad.
>
> **BACK:** **Lethal triad**: hypothermia (35.1°C) + acidosis (pH 7.18) + coagulopathy (INR 2.1). Each component worsens the others: hypothermia → impaired enzyme function → worse coagulopathy → more bleeding → more hemorrhagic shock → more acidosis → more hypothermia (self-amplifying cycle).  
> → CCRN KEY: Lethal triad mortality increases dramatically as all three are present simultaneously. Recognition drives damage control resuscitation priorities.

**Card B — Lethal triad: priorities and what NOT to do**
> **FRONT:** You prioritize _______ alongside continued product transfusion, not _______, because _______.
>
> **BACK:** Priority: **warm the patient** (warm IV fluids, warming blanket, warm OR); correct acidosis (resuscitate; vasopressors for hypotension; NaHCO₃ only if pH <7.1 and hemodynamics failing). Not: **aggressive crystalloid** — crystalloid worsens all three components (dilutes clotting factors, increases acidosis, contributes to hypothermia).  
> → CCRN KEY: Damage control resuscitation = limit crystalloid + permissive hypotension (SBP 80–90 before surgical control) + 1:1:1 products + early surgical hemorrhage control. TXA 1g IV then 1g over 8h if within 3 hours of injury.

---

### SPLIT 68 — nid 1778818396042 · Chunk 38 · MEDIUM
**Topic:** TACO vs TRALI differentiation + TACO treatment  
**Why split:** Distinguishing two entities (diagnosis) vs. treatment of the identified condition are distinct.

**Card A — TACO vs TRALI: differentiating features**
> **FRONT:** One hour into FFP transfusion: SpO₂ 84%, bilateral crackles, bilateral infiltrates on CXR, BP 148/90, BNP 820 pg/mL. The chart shows this matches _______, not _______, because _______.
>
> **BACK:** **TACO** (Transfusion-Associated Circulatory Overload), not TRALI. Because: **hypertension + elevated BNP (>250) + JVD pattern** = cardiogenic pulmonary edema from volume overload. TRALI features: normotension/hypotension, BNP typically <250, non-cardiogenic (immune-mediated capillary leak).  
> → CCRN KEY: TACO is now the most common cause of transfusion-related mortality (surpassed TRALI as prevention improved). Risk factors: CHF, CKD, elderly, rapid infusion rate.

**Card B — TACO treatment**
> **FRONT:** Treatment for TACO is _______.
>
> **BACK:** **Stop transfusion**; furosemide 40–80 mg IV; upright positioning (elevate HOB); supplemental O₂; non-invasive ventilation (BiPAP) if needed.  
> → CCRN KEY: Prevention: slow infusion rate (125 mL/hr for at-risk patients), give furosemide between units in CHF/CKD patients, minimize total transfusion volume. TRALI treatment: supportive O₂ and ventilation — no diuretics (not volume overload); usually resolves in 48–96h.

---

### SPLIT 69 — nid 1778835560000 · Chunk 39 · MEDIUM
**Topic:** Synergy Model Vulnerability → nurse competency of Advocacy at level 5  
**Why split:** Which competency maps to which patient characteristic vs. what level 5 means are distinct.

**Card A — Synergy Model: Vulnerability maps to Advocacy**
> **FRONT:** On the Synergy Model table, a patient with high Vulnerability maps primarily to the nurse competency of _______.
>
> **BACK:** **Advocacy & Moral Agency** — protecting the patient's interests, values, and rights when they cannot do so themselves. Vulnerability = susceptibility to adverse stressors (frail elderly, unconscious, non-English speaking, mentally ill).  
> → CCRN KEY: Synergy Model competencies scale 1–5. When patient needs EXCEED nurse competency level, unsafe care results. Charge nurses must match patient acuity to nurse competency level during assignments.

**Card B — Advocacy at competency level 5**
> **FRONT:** At its highest level (5), the Advocacy & Moral Agency competency means _______.
>
> **BACK:** **Systems-level change** — the nurse identifies and corrects unit policies that harm vulnerable patients, not merely protecting one patient at the bedside. Level 5 = moral courage to challenge physicians, policies, or institutional systems when they cause harm; participating in ethics committees; leading policy change.  
> → CCRN KEY: CCRN questions often test Advocacy in the context of a vulnerable patient with no surrogate and an unclear DNR status — the nurse must act as advocate, escalate to ethics, and not proceed with invasive procedures without appropriate authorization.

---

### SPLIT 70 — nid 1778835560006 · Chunk 39 · MEDIUM
**Topic:** Synergy Model: capacity vs consent + nursing role + capacity vs competency distinction  
**Why split:** The nursing role in incapacity vs. the legal distinction (capacity vs competency) are separate domains.

**Card A — Nursing role when patient lacks capacity**
> **FRONT:** Synergy Model: Participation in Decision-Making = 1 (no capacity, no surrogate identified). The nurse is asked to obtain consent for a high-risk procedure. Per the Synergy Model, the nurse's role is _______, not _______.
>
> **BACK:** Role: **Advocacy & Moral Agency** — escalate to ethics committee; identify legal decision-maker; document incapacity; delay non-emergent procedure until proxy is appointed. Not: signing consent as patient representative (nurses cannot serve as legal surrogate except in specific state statutes).  
> → CCRN KEY: Surrogate hierarchy: (1) patient if capable; (2) healthcare proxy/POA-HC; (3) next-of-kin per state statute; (4) ethics committee. Never proceed to invasive procedures without documented incapacity and surrogate identification except in true emergencies.

**Card B — Capacity vs competency**
> **FRONT:** The distinction between clinical capacity and legal competency: capacity is _______, competency is _______.
>
> **BACK:** **Capacity**: clinical determination — can the patient understand the information, appreciate its relevance, reason about options, and communicate a consistent choice? ICU nurses assess capacity at the bedside. **Competency**: legal determination — requires court adjudication; physicians document incapacity and courts determine legal incompetence.  
> → CCRN KEY: A patient can be clinically incapacitated (delirium, encephalopathy) without being legally declared incompetent. For ICU decisions, clinical incapacity assessment by the physician + nurses drives the surrogate activation process — full legal competency adjudication is reserved for long-term guardianship situations.

---

### SPLIT 71 — nid 1778835560030 · Chunk 39 · MEDIUM
**Topic:** ABCDEF bundle: why B and E cannot be performed + immediate intervention  
**Why split:** Assessment of barrier to bundle components vs. the corrective action are distinct.

**Card A — Why B and E cannot be performed**
> **FRONT:** ABCDEF bundle: patient RASS −3, CAM-ICU positive, on propofol day 4. Components B (SBT) and E (early mobility) cannot be performed because _______.
>
> **BACK:** B (SBT) and E (early mobility) require RASS **≥−1 to −2** — patient must be arousable enough to cooperate with breathing trial and participate in mobilization. RASS −3 = deep sedation — patient cannot participate.  
> → CCRN KEY: ABCDEF bundle reduces ICU delirium by ~89% when consistently applied. Each component requires a certain level of consciousness — deep sedation blocks the entire bundle.

**Card B — Immediate bundle-guided intervention**
> **FRONT:** The immediate bundle-guided intervention is _______.
>
> **BACK:** **SAT (Spontaneous Awakening Trial)** — stop all sedatives/analgesics; assess SAT safety screen; allow patient to awaken; coordinate with respiratory for SAT → SBT sequence same day.  
> → CCRN KEY: SAT safety screen contraindications: active seizures, alcohol withdrawal/DTs, RASS ≥+2 agitation, active myocardial ischemia, elevated ICP, active NMB. SAT failure: restart sedation at 50% of previous dose. ABCDEF delirium outcomes: ×3 increased 30-day mortality, prolonged MV, longer LOS, long-term cognitive impairment (BRAIN-ICU trial).

---

### SPLIT 72 — nid 1778835560021 · Chunk 39 · LOW
**Topic:** Opioid prophylaxis trio — three orders for morphine patient  
**Why split:** The three orders have distinct pharmacological rationales — constipation (drug_monitoring) vs. breakthrough dosing rule (drug_dose).

**Card A — Opioid prophylaxis: bowel and antiemetic orders**
> **FRONT:** ICU patient starts morphine 4 mg IV q4h. Per palliative care protocol, two simultaneous prophylactic orders are _______ and _______.
>
> **BACK:** **(1) Bowel regimen** — stimulant laxative (senna ± docusate): opioid-induced constipation is universal and does NOT resolve with tolerance; required for ALL opioid patients. **(2) Antiemetic PRN** (ondansetron or prochlorperazine): opioid-induced nausea common first 1–2 weeks, then tolerance develops.  
> → CCRN KEY: Opioid tolerance develops for: analgesia (dose increases needed), sedation (resolves), nausea (resolves 1–2 weeks), euphoria. Tolerance does NOT develop for constipation or miosis — bowel regimen is lifelong.

**Card B — PRN breakthrough dose rule**
> **FRONT:** The third prophylactic order is a PRN breakthrough dose = _______ % of the total daily scheduled opioid. If >3 PRN doses are needed per 24h, you _______.
>
> **BACK:** Breakthrough dose = **10–15%** of total daily scheduled opioid (e.g., morphine 4 mg q4h = 24 mg/day; breakthrough = 2.4–3.6 mg PRN q1–2h). If >3 PRN doses per 24h → **increase the scheduled dose** (pain is undertreated by the baseline regimen).  
> → CCRN KEY: Respiratory depression risk highest at first doses in opioid-naive patients. Start low; titrate. Naloxone available but use ONLY for respiratory depression (RR <8, SpO₂ <90%) — do not reverse for somnolence alone in comfort care patients.

---

### SPLIT 73 — nid 1778836916003 · Chunk 40 · HIGH
**Topic:** Dopamine receptor shift + SOAP-II trial  
**Why split:** Drug mechanism/dose (α1 shift at high doses) is independent knowledge from trial evidence (SOAP-II outcome data). One card tests pharmacology; the other tests evidence-based practice.

**Card A — Dopamine dose-dependent receptor shift**
> **FRONT:** The receptor chart shows dopamine has dose-dependent receptor activity. At doses >10 mcg/kg/min, the dominant effect shifts to _______ because _______.
>
> **BACK:** Dominant effect: **α1 agonism** (vasoconstriction) — at high doses, α1 activity overwhelms DA and β1 effects, making dopamine behave like norepinephrine but with a worse side-effect profile (higher arrhythmia rate). Dose approximations: 1–5 mcg/kg/min = DA-dominant; 5–10 = β1-dominant; >10 = α1-dominant. Ranges overlap significantly.  
> → CCRN KEY: "Renal-dose dopamine" (1–5 mcg/kg/min for renal protection) is debunked — the DOPAMINE trial showed no reduction in AKI, need for dialysis, or mortality. Do not use it for renal indications.

**Card B — SOAP-II trial: dopamine vs norepinephrine**
> **FRONT:** The SOAP-II trial showed dopamine was inferior to norepinephrine as first-line vasopressor primarily due to _______ and worse mortality in the _______ shock subgroup.
>
> **BACK:** SOAP-II (2010, n=1679): dopamine group had **2× arrhythmia rate** (primarily atrial fibrillation/SVT) and **increased 28-day mortality in cardiogenic shock** subgroup vs norepinephrine. No overall mortality benefit for dopamine in any shock type.  
> → CCRN KEY: Current recommendation: norepinephrine first-line for septic shock. Dopamine reserved only for patients with relative bradycardia + low CO without arrhythmia risk — a narrow indication.

---

### SPLIT 74 — nid 1778836916006 · Chunk 40 · HIGH
**Topic:** Vasopressin receptor profile + VASST trial  
**Why split:** The three clinical facts derived from vasopressin's receptor profile (mechanism/dose) are distinct from the VASST trial evidence (clinical trial). A learner must know the mechanism independently of whether they know the trial.

**Card A — Vasopressin receptor profile: three clinical facts**
> **FRONT:** On the receptor chart, vasopressin shows no α1, β1, or β2 activity. This profile explains: vasopressin (1) does not cause _______, (2) is fixed-dosed because _______, and (3) dose >0.04 units/min risks _______ because _______.
>
> **BACK:** (1) **Tachycardia or increased myocardial O₂ demand** — zero β1 activity, no cardiac stimulation. (2) **Fixed-dose 0.03–0.04 units/min, NOT titrated** — narrow therapeutic range; titration above this increases ischemic risk without further BP benefit. (3) **Coronary/mesenteric ischemia** — V1 receptors in coronary and splanchnic vasculature cause vasoconstriction → myocardial and bowel ischemia at doses >0.04–0.06 units/min.  
> → CCRN KEY: Vasopressin acts via V1 receptors (not adrenergic). It provides vasoconstriction through a completely different pathway from catecholamines — useful when adrenergic receptors are downregulated in refractory shock.

**Card B — VASST trial: vasopressin as catecholamine-sparing strategy**
> **FRONT:** The VASST trial tested vasopressin 0.03 units/min added to norepinephrine vs norepinephrine alone. The primary benefit was _______, and the subgroup with greatest benefit was patients requiring norepinephrine _______ mcg/min.
>
> **BACK:** Primary benefit: **reduced norepinephrine requirements** (catecholamine-sparing); no overall mortality difference. Greatest benefit: less severe septic shock subgroup (norepinephrine 5–14 mcg/min at enrollment) — a lower vasopressor dose threshold than the refractory shock group.  
> → CCRN KEY: Clinical use of vasopressin: add at 0.03–0.04 units/min when norepinephrine exceeds ~0.25–0.5 mcg/kg/min. Goal = spare further norepi escalation, provide vasoconstriction via a separate receptor class. Does NOT improve cardiac output.

---

### SPLIT 75 — nid 1778836916018 · Chunk 40 · HIGH
**Topic:** Milrinone vs dobutamine mechanism (multi-subject: two inotropes)  
**Why split:** Each drug has an independent mechanism requiring its own understanding. Conflating them obscures the pharmacological distinction that drives the clinical decision (beta-blocked patient).

**Card A — Milrinone mechanism: downstream of β1**
> **FRONT:** On the inotrope comparison chart, milrinone acts _______ the β1 receptor, making it effective when _______.
>
> **BACK:** **Downstream** — milrinone is a PDE-III inhibitor that prevents cAMP breakdown regardless of β1 receptor occupancy. Effective when **β1 receptors are blocked** (patient on metoprolol, carvedilol, bisoprolol). Beta-blocker occupies the receptor but milrinone bypasses it entirely.  
> → CCRN KEY: Milrinone disadvantages: long half-life (~2.5h, up to 20h in severe renal failure); significant SVR reduction requires concurrent vasopressor in hypotensive patients; dose-reduce to 0.125–0.2 mcg/kg/min in CKD.

**Card B — Dobutamine mechanism: β1 agonist, why it fails on beta-blockers**
> **FRONT:** Dobutamine requires _______ to exert its inotropic effect, which means its effectiveness is _______ in a patient on carvedilol 25 mg twice daily.
>
> **BACK:** Requires **β1 receptor binding** (direct agonist). In a patient on carvedilol (non-selective beta-blocker), carvedilol competitively antagonizes the receptor → dobutamine's β1 stimulation is blunted or blocked → reduced inotropic response at standard doses.  
> → CCRN KEY: Both dobutamine and milrinone raise cAMP → PKA activation → Ca²⁺ influx → inotropy + SVR reduction. Different entry point: dobutamine at receptor level, milrinone at phosphodiesterase level. On chronic beta-blockade → choose milrinone.

---

### SPLIT 76 — nid 1778836916021 · Chunk 40 · HIGH
**Topic:** Milrinone + NE requirement + monitoring triad  
**Why split:** The concurrent NE action (nursing_action) and the monitoring parameters (drug_monitoring) are distinct exam topics — one is a "what do you do" question, the other is a "what do you watch" question.

**Card A — Nursing action: concurrent vasopressor with milrinone**
> **FRONT:** The inotrope chart shows milrinone causes greater SVR reduction than dobutamine. For a cardiogenic shock patient with MAP 58 started on milrinone, the nurse must simultaneously _______.
>
> **BACK:** **Start or increase norepinephrine** to counteract milrinone-induced vasodilation and maintain MAP ≥65 mmHg. Milrinone's PDE-III inhibition reduces SVR significantly — hypotension is expected and must be pre-empted, not treated reactively.  
> → CCRN KEY: Milrinone + norepinephrine is the standard combination for cardiogenic shock in a patient on chronic beta-blockade. Milrinone = inotropy bypassing blocked receptors; norepi = pressure support while SVR is low.

**Card B — Monitoring triad for milrinone therapy**
> **FRONT:** The monitoring triad for a patient on milrinone + norepinephrine for cardiogenic shock is _______, _______, _______.
>
> **BACK:** (1) **MAP ≥65 mmHg** — perfusion pressure; (2) **Cardiac Index >2.2 L/min/m²** — cardiac output adequacy; (3) **Evidence of organ perfusion** — lactate clearing, UO ≥0.5 mL/kg/h, improving ScvO₂.  
> → CCRN KEY: Monitor for arrhythmias (milrinone is arrhythmogenic, though less so than dobutamine). Levosimendan (Ca²⁺ sensitizer, not FDA-approved in US) achieves inotropy without increasing Ca²⁺ load — less arrhythmogenic; single 24h infusion with 7–9 day effect via active metabolite OR-1896.

---

### SPLIT 77 — nid 1778836916015 · Chunk 40 · MEDIUM
**Topic:** Massive PE — fluid bolus contraindicated + correct intervention  
**Why split:** The pathophysiology explaining *why* fluids harm (biomarker_kinetics/RV physiology) is conceptually distinct from knowing the *correct intervention* (nursing_action: NE + thrombolysis).

**Card A — Why IV fluids worsen massive PE**
> **FRONT:** The obstructive shock panel (massive PE) shows elevated CVP, right heart distension. The nurse prepares to give a 500 mL NS bolus. This is incorrect because _______.
>
> **BACK:** IV fluids **worsen RV distension** in massive PE — the RV is already obstructed and overdistended by the embolus. Fluid bolus → more RV dilation → leftward septal shift → impairs LV filling (RV-LV coupling failure) → further drop in CO and MAP. The already-failing RV is volume-intolerant.  
> → CCRN KEY: RV failure treatment: norepinephrine maintains aortic diastolic pressure → preserves RV coronary perfusion pressure (RV perfuses during both systole and diastole). Inhaled nitric oxide or prostacyclin reduces RV afterload selectively without systemic hypotension.

**Card B — Correct intervention in hemodynamically unstable PE**
> **FRONT:** For massive PE with hemodynamic instability (SBP <90, vasopressor-dependent), the correct immediate interventions are _______ and _______.
>
> **BACK:** (1) **Norepinephrine** — maintain MAP, preserve RV coronary perfusion pressure. (2) **Emergent systemic thrombolysis** — tPA 100 mg over 2h (or 0.6 mg/kg over 15 min for cardiac arrest) if high-risk PE confirmed and no absolute contraindications.  
> → CCRN KEY: High-risk PE = hemodynamic instability (SBP <90 or vasopressor need) OR cardiac arrest. RV enlargement + D-sign on echo confirms RV strain. tPA absolute contraindications: prior intracranial hemorrhage, recent major surgery/trauma, active internal bleeding.

---

### SPLIT 78 — nid 1778836916027 · Chunk 40 · MEDIUM
**Topic:** Septic shock MAP target + SEPSISPAM trial  
**Why split:** The MAP target (drug_monitoring) is the clinical decision point; the SEPSISPAM trial (clinical_trial) is the evidence basis. Both appear on CCRN exams but test different competencies.

**Card A — MAP target in septic shock**
> **FRONT:** On the MAP target chart, the Surviving Sepsis Campaign target for most septic shock patients is MAP _______ mmHg. The exception is patients with _______, in whom a higher target may reduce _______.
>
> **BACK:** MAP ≥**65 mmHg** for most patients. Exception: **chronic hypertension** — targeting MAP 80–85 in this subgroup may reduce need for renal replacement therapy (SEPSISPAM subgroup finding). Individualize the target; treat organs, not numbers.  
> → CCRN KEY: MAP is a proxy — true perfusion endpoints are lactate ≤2 mmol/L (or ≥10% clearance per 2h), UO ≥0.5 mL/kg/h, capillary refill <2 sec, ScvO₂ ≥70%, improving mottling score.

**Card B — SEPSISPAM trial**
> **FRONT:** The SEPSISPAM trial (2014) randomized septic shock patients to MAP 65–70 vs MAP 80–85 mmHg. The MAP 80–85 group showed _______ and _______.
>
> **BACK:** MAP 80–85 group: **no improvement** in mortality, AKI incidence, or ICU LOS vs MAP 65–70. MAP 80–85 associated with **20% increase in atrial fibrillation** and required significantly more norepinephrine. Chronic hypertension subgroup: MAP 80–85 reduced need for renal replacement therapy.  
> → CCRN KEY: SEPSISPAM (Asfar et al., NEJM 2014): 776 patients. Takeaway: higher MAP target = more vasopressor, more AF, no mortality benefit — except in chronic HTN subgroup. Guideline: MAP ≥65 as the default.

---

### SPLIT 79 — nid 1778836916033 · Chunk 40 · LOW
**Topic:** Post-arrest TTM MAP target + physiological rationale  
**Why split:** The target number (drug_dose/monitoring) and the physiological reason (impaired autoregulation during hypothermia) test distinct knowledge even if clinically linked.

**Card A — Post-arrest TTM MAP target**
> **FRONT:** Post-cardiac arrest patient on targeted temperature management (33°C). The MAP target during TTM is _______ mmHg.
>
> **BACK:** MAP ≥**65–80 mmHg** post-ROSC; most centers target **70–80 mmHg** during TTM for neuroprotection. Hypothermia itself causes vasodilation (α-adrenergic receptor downregulation) and bradycardia (HR 40–60 is acceptable if CO maintained) → increased vasopressor requirement is expected.  
> → CCRN KEY: TTM bradycardia during cooling: targeted and expected — not pathological. HR 40–60 acceptable if MAP is maintained. Treat with vasopressors (NE), not rate-increasing agents.

**Card B — Why higher MAP during TTM (impaired autoregulation)**
> **FRONT:** The physiological reason for targeting MAP 70–80 mmHg (rather than 65) during post-arrest TTM is _______, making cerebral blood flow _______ during hypothermia.
>
> **BACK:** **Cerebral autoregulation is impaired** after cardiac arrest — during hypothermia, cerebral blood flow becomes **pressure-passive** (loses autoregulatory buffering). Higher MAP directly improves cerebral perfusion when this buffer is lost. The brain gets more blood only if the pressure goes up.  
> → CCRN KEY: ScvO₂ goal during TTM: >70%. Hypothermia shifts oxyhemoglobin curve left → tissues extract O₂ more efficiently → mixed venous saturation may appear adequate even with reduced CO. BOX trial data: MAP ≥70 during first 36h post-ROSC associated with better neurological outcomes in some analyses.

---

### SPLIT 80 — nid 1778839883003 · Chunk 42 · HIGH
**Topic:** RASS/CPOT scoring + A1C analgesic-first protocol  
**Why split:** Pain assessment scoring (CPOT interpretation) and the protocol sequence (A1C: analgesia before sedation) test different competencies — one is an assessment tool, the other is a clinical decision framework.

**Card A — CPOT pain assessment in ventilated patients**
> **FRONT:** On the RASS/CPOT chart, a vented patient has CPOT = 6. CPOT >2 indicates _______ and the four CPOT components are _______, _______, _______, _______.
>
> **BACK:** CPOT >2 indicates **significant pain** in non-verbal/intubated patients (CPOT range 0–8; each of 4 components scored 0–2). Components: (1) facial expression, (2) body movements, (3) muscle tension, (4) compliance with ventilator (or vocalization if extubated). Score 6/8 = severe pain — analgesic intervention required before escalating sedation.  
> → CCRN KEY: BPS (Behavioral Pain Scale) is an alternative validated tool for intubated patients: facial expression (1–4) + upper limb movements (1–4) + compliance with MV (1–4); total 3–12; >6 = significant pain.

**Card B — A1C protocol: analgesia-first before sedation**
> **FRONT:** Per the A1C (Analgesia-first) protocol, a vented patient at RASS +2 with CPOT = 6: the FIRST intervention before adding sedation is _______. The reason is _______.
>
> **BACK:** **Treat pain first** — increase IV analgesic (e.g., fentanyl 25–50 mcg IV bolus or increase infusion). Reason: pain is the most common undertreated driver of agitation in the ICU; adding sedation without addressing pain suppresses the behavioral response without treating the cause.  
> → CCRN KEY: A1C protocol order: Assess pain (CPOT/BPS) → treat pain → reassess CPOT → assess sedation need (RASS) → treat agitation only if still present after pain control. Always assess reversible agitation causes: full bladder, ETT malposition, hypoxia, metabolic derangements.

---

### SPLIT 81 — nid 1778839883009 · Chunk 42 · HIGH
**Topic:** Morphine M6G accumulation in AKI + opioid selection guide  
**Why split:** The pathophysiology of M6G accumulation (mechanism) is distinct from the clinical opioid selection table (drug safety in renal failure) — two independently testable concepts.

**Card A — Morphine-6-glucuronide (M6G) accumulation in AKI**
> **FRONT:** On the analgesic comparison chart, morphine's active metabolite _______ accumulates in AKI because _______ and causes _______.
>
> **BACK:** **Morphine-6-glucuronide (M6G)** — active opioid metabolite that is renally excreted. In AKI: reduced clearance → accumulation → prolonged sedation, respiratory depression, delayed ventilator weaning, and naloxone-resistant or repeatedly-requiring reversal.  
> → CCRN KEY: M6G is MORE potent than morphine at the μ-opioid receptor. Accumulation in renal failure can produce profound, prolonged opioid effect — even after the morphine infusion is stopped or the dose is reduced.

**Card B — ICU opioid selection by renal function**
> **FRONT:** For a mechanically ventilated patient with AKI (creatinine 4.2, oliguria), the safest opioid infusion is _______ because _______.
>
> **BACK:** **Fentanyl** — hepatically metabolized with no active renally-cleared metabolites; safe in AKI and ESRD. Hydromorphone: H3G mild accumulation — acceptable for PRN bolus dosing, caution with continuous infusions in ESRD. Morphine: avoid continuous infusions in AKI/CKD (M6G accumulates); PRN bolus acceptable when GFR >60.  
> → CCRN KEY: Equianalgesic ICU doses: morphine 10 mg IV = hydromorphone 1.5 mg IV = fentanyl 100 mcg IV. When rotating opioids, reduce new opioid by 25–50% for incomplete cross-tolerance, then titrate up.

---

### SPLIT 82 — nid 1778839883021 · Chunk 42 · HIGH
**Topic:** Propofol mechanism + why preferred over midazolam (two agents)  
**Why split:** Propofol's own mechanism and pharmacokinetic advantage are distinct from the comparison with midazolam — the comparison requires knowing both drugs and PADIS 2018 guideline context.

**Card A — Propofol mechanism and formulation**
> **FRONT:** The propofol chart shows its mechanism: it acts at _______ receptors via _______ modulation. Its formulation (10% intralipid) means the nurse must _______.
>
> **BACK:** **GABA-A receptors** — positive allosteric modulator (same target as benzodiazepines, different binding site; faster onset, shorter context-sensitive half-life, more titratable). Lipid formulation: account for caloric content in nutrition plan — 1 mg/kg/h propofol ≈ 0.1 g fat/kg/day (1.1 kcal/mL). Monitor triglycerides at high doses.  
> → CCRN KEY: Propofol provides NO analgesia — always pair with an analgesic. Propofol-related infections: lipid medium supports bacterial growth; use sterile technique, change tubing per protocol (usually every 12h).

**Card B — Propofol vs midazolam: why preferred for ICU sedation**
> **FRONT:** Two reasons propofol is preferred over midazolam for ICU sedation (PADIS 2018) are _______.
>
> **BACK:** (1) **Predictable, faster offset** — short context-sensitive half-life allows timely SAT and extubation readiness; midazolam accumulates unpredictably (active hepatic metabolites, prolonged sedation especially in hepatic/renal failure). (2) **Lower delirium rates** — PADIS 2018 recommends propofol or dexmedetomidine over benzodiazepines for most ICU sedation.  
> → CCRN KEY: Midazolam disadvantages: active metabolite (1-OH-midazolam) accumulates in renal/hepatic failure; unpredictable sedation depth; GABA-hyperactivation increases delirium risk by 22% per additional benzo day. Reserve benzodiazepines for: alcohol/benzo withdrawal, seizure management, specific procedural sedation.

---

### SPLIT 83 — nid 1778839883024 · Chunk 42 · HIGH
**Topic:** PRIS recognition + first nursing action  
**Why split:** Recognizing PRIS (diagnosis_criteria: matching the lab pattern) and managing it (nursing_action: stop infusion, switch agent) are sequential but distinct skills — recognition must precede action.

**Card A — PRIS recognition: diagnostic criteria**
> **FRONT:** A patient on propofol 60 mcg/kg/min ×72h develops pH 7.22, lactate 7.1, CK 14,000, K⁺ 6.3, TG 690. This is _______, diagnosed by the presence of _______.
>
> **BACK:** **Propofol Infusion Syndrome (PRIS)** — diagnostic criteria: dose **>4 mg/kg/h (67 mcg/kg/min)** for **>48h** PLUS any of: anion-gap metabolic acidosis, rhabdomyolysis (↑CK), hyperkalemia, hypertriglyceridemia, cardiac dysfunction (RBBB, ST changes, fatal arrhythmias). This patient meets all five criteria.  
> → CCRN KEY: PRIS mortality 18–83%; increases significantly with delayed recognition. Rising CK alone is non-specific. The combination of **new AG metabolic acidosis + elevated CK in a patient on high-dose propofol = PRIS until proven otherwise**. Cardiac monitoring is mandatory.

**Card B — PRIS management: first nursing action**
> **FRONT:** PRIS is recognized. The FIRST nursing action is _______, followed by _______.
>
> **BACK:** **FIRST: STOP propofol immediately** — switch to alternative sedation (midazolam 0.02–0.1 mg/kg/h or dexmedetomidine 0.2–0.7 mcg/kg/h). Then: notify provider STAT; treat hyperkalemia per protocol; continuous cardiac monitoring (ECG); vasopressors for hemodynamic instability; consider CRRT for refractory acidosis or K⁺ elevation.  
> → CCRN KEY: PRIS risk factors: young patients, doses >4 mg/kg/h, duration >48h, concurrent catecholamines or corticosteroids, carbohydrate-restricted diet (depletes glycogen → increases fat oxidation reliance).

---

### SPLIT 84 — nid 1778839883027 · Chunk 42 · HIGH
**Topic:** Dexmedetomidine respiratory sparing + two clinical applications  
**Why split:** The mechanism of respiratory sparing (drug_mechanism) and the two clinical scenarios where it matters (nursing_action/clinical application) are separate exam targets.

**Card A — Dexmedetomidine: respiratory sparing mechanism**
> **FRONT:** On the dexmedetomidine chart, dex preserves _______ while midazolam depresses it. The mechanism is _______.
>
> **BACK:** Preserves **spontaneous respiratory drive** — dex is an α2-adrenergic agonist that decreases norepinephrine release from the locus ceruleus, producing sedation without direct respiratory center depression. Unlike GABA-A agents (propofol, benzodiazepines), it does not suppress respiratory drive.  
> → CCRN KEY: Dex dosing: loading 1 mcg/kg over 10–20 min (often omitted in hemodynamically unstable patients); maintenance 0.2–0.7 mcg/kg/h. Most common side effects: bradycardia, hypotension; transient hypertension during loading dose (α2b stimulation).

**Card B — Dexmedetomidine: two clinical applications for respiratory sparing**
> **FRONT:** Name two ICU settings where dexmedetomidine's preservation of respiratory drive is clinically important.
>
> **BACK:** (1) **Non-invasive ventilation (NIV/BiPAP)** — sedation is needed to reduce patient discomfort and agitation, but apnea would eliminate BiPAP efficacy; dex allows adequate sedation while the patient continues breathing spontaneously. (2) **Ventilator weaning** — provides sedation during weaning trials and post-extubation without suppressing the drive to breathe; facilitates safe extubation readiness.  
> → CCRN KEY: Dex also enables cooperative/light sedation (RASS −1 to 0) — patients can follow commands, report pain, and communicate with family. Dex does NOT provide analgesia at standard ICU doses — always pair with analgesic.

---

### SPLIT 85 — nid 1778839883030 · Chunk 42 · HIGH
**Topic:** MENDS trial evidence + PADIS 2018 guideline implication  
**Why split:** The trial facts (what MENDS measured and found) are distinct from the guideline change those findings support — examiners can test either independently.

**Card A — MENDS trial: dexmedetomidine vs lorazepam outcomes**
> **FRONT:** The MENDS trial compared dexmedetomidine vs lorazepam for ICU sedation. Dex patients had fewer _______ days and fewer _______ days.
>
> **BACK:** Fewer **coma days** AND fewer **delirium days** (MENDS, NEJM 2007: median 7 vs 10 days for dex vs lorazepam, p=0.01). No significant mortality difference. SEDCOM trial (propofol vs dex): similar ventilator-free days; dex patients had fewer delirium days, more bradycardia/hypotension but less respiratory depression.  
> → CCRN KEY: Mechanism of benzo-associated delirium: GABA-A hyperactivation disrupts cholinergic neurotransmission in the hippocampus → impaired memory consolidation and orientation. Each additional day of benzodiazepine use increases ICU delirium risk by **22%**.

**Card B — PADIS 2018 guideline: sedation agent recommendation**
> **FRONT:** Based on MENDS and SEDCOM trial data, PADIS 2018 recommends _______ benzodiazepine infusions for routine ICU sedation and prefers _______.
>
> **BACK:** PADIS 2018: **AVOID continuous benzodiazepine infusions** for routine ICU sedation. Prefer **propofol or dexmedetomidine** instead. Reserve benzodiazepines for: alcohol/benzo withdrawal seizures, procedure-specific indications, adjunct for patients not at goal with first-line agents.  
> → CCRN KEY: PADIS = Pain, Agitation/Sedation, Delirium, Immobility, Sleep (2018 SCCM guidelines). Combined MENDS + SEDCOM evidence: dex and propofol are preferred because they reduce delirium days, reduce coma days, and have faster/more predictable offset than benzodiazepines.

---

### SPLIT 86 — nid 1778839883006 · Chunk 42 · MEDIUM
**Topic:** ABC Bundle protocol + 2008 Lancet trial outcomes  
**Why split:** The protocol sequence and safety screening criteria (diagnosis_criteria/nursing process) are distinct from knowing the clinical trial evidence supporting it (clinical_trial).

**Card A — ABC Bundle: protocol and SAT safety screen**
> **FRONT:** Daily SAT combined with SBT is the _______ protocol. The SAT safety screen says to HOLD sedation interruption if _______.
>
> **BACK:** **ABC Bundle** (Awakening and Breathing Coordination). Hold SAT if: SpO₂ <88%, RR >35, FiO₂ >70%, PEEP >12, active seizures, ongoing NMB, alcohol withdrawal, or active agitation/patient safety concern. If SAT fails → restart sedation at 50% prior dose.  
> → CCRN KEY: SAT-SBT sequence: hold sedation → patient opens eyes/follows commands → perform SBT (PS 5/5 cmH₂O or T-piece for 30–120 min) → evaluate extubation readiness. ABCDEF bundle extends this: D=delirium monitoring, E=early mobility, F=family engagement.

**Card B — 2008 Lancet trial: ABC Bundle outcomes**
> **FRONT:** The 2008 Lancet trial (Girard et al.) showed the ABC Bundle reduced 1-year mortality by approximately _______ and reduced mechanical ventilation duration by _______ days.
>
> **BACK:** **32% reduction in 1-year mortality** (HR 0.68, p=0.02) and **~3 fewer days on mechanical ventilation**. Also reduced ICU and hospital length of stay. This was the landmark trial establishing the bundled approach (SAT + SBT) as standard of care.  
> → CCRN KEY: The bundle effect is synergistic — combining SAT with SBT outperforms either alone. SAT without SBT reduces sedation depth but doesn't accelerate liberation; SBT without SAT may not be attempted if sedation prevents assessment.

---

### SPLIT 87 — nid 1778839883033 · Chunk 42 · MEDIUM
**Topic:** Dexmedetomidine bradycardia management sequence  
**Why split:** Drug dose management (slow/stop loading dose) and the step-wise intervention sequence (next_step_workup) test different competency layers — recognition of the cause vs. knowing the correct response order.

**Card A — Dexmedetomidine-induced bradycardia: cause and prevention**
> **FRONT:** On the dex chart, a patient develops HR 36 during dex loading dose. This occurs because _______, and can be prevented by _______.
>
> **BACK:** **α2 agonism decreases sympathetic tone** — loading dose causes the most pronounced bradycardia (bolus-effect). Prevention: slow the loading dose (extend over 20–30 min instead of 10 min), or skip the loading dose entirely in patients with baseline HR <60, cardiac conduction disease, or hemodynamic instability.  
> → CCRN KEY: Dex-induced bradycardia is dose-dependent. The loading dose (1 mcg/kg over 10 min) causes transient hypertension followed by bradycardia/hypotension. Many ICU protocols start without a loading dose to avoid this biphasic response.

**Card B — Dexmedetomidine bradycardia: three-step intervention sequence**
> **FRONT:** HR 36, MAP 70 during dex loading. In order, the three interventions are _______, _______, _______.
>
> **BACK:** 1. **Slow or stop the loading dose** (extend infusion time or discontinue). 2. **Reduce maintenance infusion rate** (toward minimum 0.2 mcg/kg/h). 3. **Atropine 0.5–1 mg IV** if HR remains <40 bpm or patient becomes hemodynamically unstable (MAP <65 despite fluid adjustment).  
> → CCRN KEY: Atropine is the pharmacological rescue for symptomatic dex-induced bradycardia. If bradycardia persists despite all steps → discontinue dex and switch to an alternative sedation agent.

---

### SPLIT 88 — nid 1778879362009 · Chunk 43 · MEDIUM
**Topic:** TOF target during NMB infusion + TOF 0/4 interpretation  
**Why split:** The monitoring target (2/4 twitches during infusion) and interpretation of a specific TOF reading (drug_monitoring vs clinical_interpretation) test separate knowledge — one is a target, one is a scale.

**Card A — TOF monitoring: cisatracurium target**
> **FRONT:** On the TOF monitoring chart, the recommended ICU paralysis target during cisatracurium infusion is _______ twitches and this target is preferred over 0/4 because _______.
>
> **BACK:** Target: **2/4 twitches** — preferred over 0/4 because: allows continuous block-depth assessment, detects early recovery before patient-ventilator dyssynchrony, and reduces ICU-acquired weakness (ICUAW) risk from over-paralysis. TOF site: ulnar nerve at wrist → observe thumb adduction (adductor pollicis). Assess every 4h; rotate electrode site daily.  
> → CCRN KEY: Supramaximal stimulus (30–60 mA) required for accurate TOF — subthreshold stimuli give falsely low twitch counts. Edema or limb positioning affects results; verify with clinical assessment.

**Card B — TOF scale interpretation**
> **FRONT:** On the TOF chart: TOF 0/4 indicates approximately _______ % neuromuscular blockade. TOF 4/4 with no fade indicates approximately _______ % blockade.
>
> **BACK:** TOF 0/4 ≈ **100% blockade** (all twitches absent). TOF 4/4 with no fade ≈ **0% blockade** (full recovery). Scale: 0/4 ≈ 100%, 1/4 ≈ 95%, 2/4 ≈ 90%, 3/4 ≈ 75%, 4/4 ≈ 0%. Always pair TOF with clinical assessment — peripheral TOF does not assess diaphragm or central respiratory drive.  
> → CCRN KEY: TOF monitors block at peripheral muscle only. A patient can have TOF 2/4 at the hand but near-complete diaphragm block — reason why spontaneous ventilatory effort is the true clinical endpoint, not TOF number alone.

---

### SPLIT 89 — nid 1778879362024 · Chunk 43 · MEDIUM
**Topic:** Rocuronium RSI dose + sugammadex reversal doses  
**Why split:** RSI drug selection/dosing (drug_dose) and reversal agent dosing (reversal_antidote) are independently testable — knowing rocuronium's RSI dose does not require knowing sugammadex's CICO rescue dose.

**Card A — Rocuronium RSI: dose and advantage over succinylcholine**
> **FRONT:** On the RSI chart, rocuronium at _______ mg/kg is used as a succinylcholine alternative. Its key advantage is _______.
>
> **BACK:** **1.2 mg/kg IV** (high-dose RSI). Key advantage: **fully reversible with sugammadex** in the "can't intubate, can't oxygenate" (CICO) emergency — unlike succinylcholine, which wears off slowly and cannot be pharmacologically reversed. Onset ~60 sec at 1.2 mg/kg (comparable to succinylcholine).  
> → CCRN KEY: Succinylcholine 1.5 mg/kg: onset 45–60 sec, duration 10–15 min (depolarizing NMBA). Contraindicated in: crush injury/burns/denervation >48h post-injury (hyperkalemic cardiac arrest risk), malignant hyperthermia susceptibility, personal/family history of pseudocholinesterase deficiency.

**Card B — Sugammadex reversal doses**
> **FRONT:** On the reversal chart, sugammadex CICO rescue dose is _______ mg/kg and routine reversal dose (TOF 1–2/4) is _______ mg/kg. Onset of reversal for CICO dose is _______.
>
> **BACK:** CICO rescue: **16 mg/kg IV** → reversal within **1–3 minutes**. Routine reversal (TOF 1–2/4): **4 mg/kg IV** → reversal in 3–5 min. Sugammadex only reverses rocuronium and vecuronium (encapsulation via cyclodextrin) — cannot reverse succinylcholine or cisatracurium.  
> → CCRN KEY: After 16 mg/kg sugammadex, if re-paralysis is needed → wait ≥24h before using rocuronium again (all binding sites occupied); use succinylcholine or cisatracurium as alternatives during this window.

---

### SPLIT 90 — nid 1778879362033 · Chunk 43 · MEDIUM
**Topic:** Sugammadex dose selection by TOF level + post-reversal re-paralysis  
**Why split:** Dose selection based on depth of block (drug_dose) and the clinical implication after full reversal (reversal_antidote clinical context) are independently testable.

**Card A — Sugammadex dose selection: TOF 0/4 vs TOF 1–2/4**
> **FRONT:** On the reversal chart, a patient has TOF 0/4 after rocuronium infusion ×6h. Sugammadex 4 mg/kg is ordered. This dose is _______ for TOF 0/4. The correct dose is _______.
>
> **BACK:** **Incorrect** — 4 mg/kg is for TOF 1–2/4 (routine reversal of moderate block). For TOF 0/4 (deep block): correct dose is **16 mg/kg IV**. Summary: TOF 1–2/4 = 4 mg/kg (reversal in 3–5 min); TOF 0/4 or CICO rescue = 16 mg/kg (reversal in 1–3 min). Dose is weight-based — accurate weight required.  
> → CCRN KEY: Giving 4 mg/kg at TOF 0/4 provides inadequate chelation — incomplete reversal, residual block, risk of re-curarization as sugammadex redistributes. The 16 mg/kg dose provides sufficient cyclodextrin molecules to capture all circulating rocuronium.

**Card B — Post-sugammadex re-paralysis: what to use and when**
> **FRONT:** After 16 mg/kg sugammadex for CICO reversal, if the patient requires re-paralysis within 24h, rocuronium should NOT be used because _______. The alternatives are _______.
>
> **BACK:** Rocuronium is **not available** for 24h after 16 mg/kg sugammadex — all sugammadex cyclodextrin binding sites are occupied with rocuronium molecules; additional rocuronium has no free carrier and will not provide adequate block (or may produce unexpected profound block when carriers become free). Alternatives: **succinylcholine** (if no contraindications) or **cisatracurium** (non-depolarizing, different mechanism, not affected by sugammadex).  
> → CCRN KEY: Vecuronium is also bound by sugammadex — same 24h restriction applies. Cisatracurium (Hofmann elimination) is the preferred alternative when rocuronium and succinylcholine are both contraindicated.

---

### SPLIT 91 — nid 1778882886003 · Chunk 44 · MEDIUM
**Topic:** Labetalol α:β ratio + pathophysiology of aortic dissection treatment  
**Why split:** The pharmacological property (α:β ratio, drug_mechanism) and the clinical reasoning for why it's chosen in dissection (pathophysiology_rationale: prevents reflex tachycardia) test distinct levels of understanding.

**Card A — Labetalol α:β receptor ratio**
> **FRONT:** The antihypertensive chart shows labetalol's IV α:β receptor ratio is _______ and oral α:β ratio is _______.
>
> **BACK:** IV α:β ratio = **1:7** (7× more beta than alpha activity when given intravenously). Oral form = 1:3. IV labetalol is predominantly beta-blocking with some alpha-blockade — this is the relevant form for hypertensive emergencies and ICU use. Half-life IV ≈ 5.5h (less flexible than esmolol t½ ~9 min).  
> → CCRN KEY: Esmolol is a pure β1 blocker (no alpha activity) — requires a separate vasodilator (nitroprusside or nicardipine) for BP control in dissection. Labetalol achieves both HR and BP reduction with one agent — simpler, but less independently titratable.

**Card B — Why labetalol is ideal for aortic dissection**
> **FRONT:** Labetalol's dual α+β blockade makes it ideal for aortic dissection because it reduces _______ simultaneously, preventing _______ that a pure vasodilator would cause.
>
> **BACK:** Reduces both **heart rate** (β-blockade) AND **blood pressure** (α-blockade) simultaneously. Prevents **reflex tachycardia** — pure vasodilators (hydralazine, nitroprusside alone) trigger a baroreceptor-mediated reflex that increases HR, worsening aortic wall shear stress and propagation risk.  
> → CCRN KEY: Aortic dissection treatment sequence: **HR control FIRST** (target HR <60 bpm) with esmolol or labetalol → THEN add vasodilator if SBP >120 mmHg. Never give a vasodilator alone without first controlling heart rate.

---

### SPLIT 92 — nid 1778882886009 · Chunk 44 · MEDIUM
**Topic:** Hypertensive emergency vs urgency — definition + management  
**Why split:** The diagnostic distinction (biomarker_kinetics/end-organ damage as the defining criterion) and the management approach (diagnosis_criteria → oral vs IV agents) are sequential but independently testable competencies.

**Card A — Hypertensive emergency vs urgency: defining distinction**
> **FRONT:** On the hypertensive crisis chart, hypertensive emergency is defined as severe BP elevation WITH _______. Hypertensive urgency has the same BP elevation WITHOUT _______.
>
> **BACK:** Hypertensive emergency = severe BP WITH **new or worsening end-organ damage** — this is the defining feature, not a specific BP number. End-organ categories: Neurologic (encephalopathy/PRES, stroke), Cardiac (ACS, acute HF, aortic dissection), Renal (AKI, hematuria), Ophthalmic (papilledema, grade III/IV retinopathy). Hypertensive urgency = same BP WITHOUT end-organ damage (asymptomatic).  
> → CCRN KEY: Common exam trap: BP 200/120 with subtle symptoms (headache, blurred vision, chest tightness) — always assess ALL organ systems. Subtle symptoms may indicate end-organ damage that reclassifies the presentation from urgency to emergency.

**Card B — Hypertensive urgency management: why IV agents are not used**
> **FRONT:** Hypertensive urgency is managed with _______ agents over _______, NOT IV antihypertensives, because IV reduction causes _______.
>
> **BACK:** **Oral** antihypertensives over **hours to days** — IV antihypertensives are not indicated and may cause harm. Rapid IV reduction can cause: cerebral hypoperfusion (chronic hypertension shifts autoregulation curve right — brain requires higher MAP), myocardial ischemia (coronary perfusion pressure drops), and precipitous hypotension.  
> → CCRN KEY: No specific BP target for urgency — reduce gradually, achieve control over 24–48h as outpatient. The classification determines treatment setting: emergency → ICU with IV agents; urgency → outpatient with oral agents. The key is organ assessment, not the BP number alone.



---

### SPLIT 93 -- nid 1778884359036 * Chunk 45 * HIGH
**Topic:** Enoxaparin prophylaxis vs therapeutic doses
**Why split:** Prophylactic and therapeutic dosing are independent clinical decisions with very different dose ranges -- selecting the wrong category is a high-stakes medication error.

**Card A -- Enoxaparin: prophylactic dosing**
> **FRONT:** On the VTE prophylaxis chart, the standard ICU pharmacologic prophylaxis dose of enoxaparin is _______ mg SQ _______. For higher-risk patients (e.g., morbid obesity, major trauma), dosing may be adjusted to _______.
>
> **BACK:** Standard prophylaxis: **40 mg SQ once daily**. For higher-risk patients, doses may be adjusted (e.g., weight-based or q12h strategies per institutional protocol -- evidence for universal high-risk thresholds varies). In patients with significantly reduced renal function (CrCl <30), dose adjustment or transition to UFH may be appropriate depending on clinical context and protocol.
> -> CCRN KEY: There is no one-size-fits-all adjustment rule for renal impairment -- management depends on bleeding vs clot risk, patient weight, and institutional guidelines. Always verify per pharmacy and protocol.

**Card B -- Enoxaparin: therapeutic dosing and anti-Xa monitoring**
> **FRONT:** The therapeutic dose of enoxaparin for confirmed DVT/PE is _______ mg/kg SQ every 12 hours. Anti-Xa peak monitoring is drawn _______ hours after dose; therapeutic target for q12h dosing is _______.
>
> **BACK:** Therapeutic dose: **1 mg/kg SQ q12h** (or 1.5 mg/kg SQ once daily). Anti-Xa draw: **4 hours after SQ injection** (peak level). Targets: q12h = 0.5-1.0 IU/mL; q24h = 1.0-2.0 IU/mL. Anti-Xa monitoring is indicated in specific populations (morbid obesity, pregnancy, extreme low weight, renal impairment) per institutional protocol.
> -> CCRN KEY: Dose differences are large: prophylaxis ~40 mg vs therapeutic ~70-90 mg for a 70 kg patient. Incorrect category selection -- giving prophylactic dose for therapeutic indication -- is a critical error.

---

### SPLIT 94 -- nid 1778884359024 * Chunk 45 * MEDIUM
**Topic:** 4-factor PCC vs FFP volume + reversal agent comparison
**Why split:** Volume comparison rationale and the full advantage profile of 4F-PCC over FFP test different competencies.

**Card A -- 4F-PCC vs FFP: volume and fluid overload concern**
> **FRONT:** On the warfarin reversal chart, the key volume difference for a 70 kg patient is 4F-PCC approx _______ mL vs FFP approx _______ mL. This difference matters most in patients with _______.
>
> **BACK:** 4F-PCC (Kcentra): ~**30-60 mL** (concentrated product). FFP: ~**1,050-1,400 mL** (15-20 mL/kg x 70 kg). Volume concerns are greatest in patients with: heart failure (large plasma volume may worsen pulmonary edema), renal failure (limited ability to excrete excess fluid), and cirrhosis (portal hypertension and hypoalbuminemia).
> -> CCRN KEY: INR correction speed: 4F-PCC onset 15-30 min vs FFP 1-4h (including thaw time). In active intracranial hemorrhage, speed of reversal is a critical consideration.

**Card B -- 4F-PCC advantages over FFP: full comparison**
> **FRONT:** Name four advantages of 4F-PCC over FFP for warfarin reversal beyond volume.
>
> **BACK:** (1) **Faster INR correction** (15-30 min vs 1-4h). (2) **More complete reversal** at appropriate doses. (3) **No blood-type matching required** (unlike FFP). (4) **Avoids plasma transfusion volume and reduces plasma-associated TRALI/TACO concern.** Note: 4F-PCC carries its own thromboembolic risk (~1-2%) -- weigh in patients with underlying clot risk.
> -> CCRN KEY: FFP still has roles: massive transfusion protocol (plasma source), TTP (provides ADAMTS13 -- 4F-PCC is NOT appropriate for TTP), and when 4F-PCC is unavailable. For isolated warfarin reversal, 4F-PCC is generally preferred when available per protocol.

---

### SPLIT 95 -- nid 1778884359033 * Chunk 45 * MEDIUM
**Topic:** Andexanet alfa -- what it reverses + high vs low dose regimens
**Why split:** Scope and mechanism of reversal and dose selection criteria (drug identity, dose level, AND timing) are independently assessed competencies.

**Card A -- Andexanet alfa: mechanism and scope**
> **FRONT:** On the reversal chart, andexanet alfa is FDA-approved to reverse _______ (names). Its mechanism is _______.
>
> **BACK:** FDA-approved for: **apixaban** and **rivaroxaban** (edoxaban is off-label). Mechanism: recombinant modified factor Xa (catalytically inactive) -- acts as a **decoy receptor** that binds anti-Xa DOACs and sequesters them from endogenous factor Xa, allowing clotting to resume.
> -> CCRN KEY: Andexanet carries ~10-15% thrombotic event rate at 30 days post-reversal -- resume anticoagulation as soon as hemostasis is achieved. 4F-PCC (off-label, ~50 units/kg) is a widely used alternative when andexanet is unavailable or cost-prohibitive.

**Card B -- Andexanet alfa: high vs low dose regimen selection**
> **FRONT:** The HIGH dose andexanet regimen is selected based on three variables: _______, _______, and _______. High dose is _______ mg bolus followed by _______.
>
> **BACK:** Dose selection depends on: **(1) drug identity** (rivaroxaban vs apixaban), **(2) last dose amount** (rivaroxaban >=10 mg; apixaban >=5 mg), and **(3) timing** (last dose <8h or unknown = higher dose needed). LOW dose: lower-dose formulations or last dose >=8h for either drug. **High dose regimen: 800 mg IV bolus then 8 mg/min x 120 min.**
> -> CCRN KEY: Always verify current FDA prescribing information -- dose selection incorporates all three variables. No single factor alone determines the regimen.

---

### SPLIT 96 -- nid 1778884359030 * Chunk 45 * LOW
**Topic:** Idarucizumab -- reverses dabigatran only, dose, mechanism
**Why split:** Drug-specific scope and mechanism are separate knowledge points.

**Card A -- Idarucizumab: scope and dose**
> **FRONT:** On the reversal chart, idarucizumab (Praxbind) reverses _______ only. The dose is _______ IV given as _______.
>
> **BACK:** Reverses **dabigatran only** (direct thrombin inhibitor). Dose: **5 g IV**, given as **two consecutive 2.5 g vials** (IV push or short infusion). Indications: life-threatening or uncontrolled bleeding on dabigatran, or urgent surgery requiring reversal.
> -> CCRN KEY: Onset: near-complete reversal within minutes. Duration ~24h. Dabigatran may be restarted 24h after idarucizumab when clinically appropriate. Dabigatran is ~80% renally cleared -- accumulates in reduced renal function, making idarucizumab availability critical in these patients.

**Card B -- Idarucizumab: mechanism and affinity**
> **FRONT:** Idarucizumab's mechanism is _______ with affinity approximately _______ x that of thrombin, enabling complete reversal at peak plasma dabigatran levels.
>
> **BACK:** Humanized **monoclonal antibody fragment (Fab)** that binds dabigatran with ~**350x greater affinity than thrombin** -- sequesters dabigatran molecules and renders them pharmacologically inactive regardless of plasma level.
> -> CCRN KEY: Hemodialysis can remove dabigatran (small Vd, low protein binding) but takes hours. Idarucizumab is the preferred reversal when available; dialysis may be considered as an adjunct in severe cases or when idarucizumab is unavailable.

---

### SPLIT 97 -- nid 1778885720042 * Chunk 46 * HIGH
**Topic:** Mannitol osmol gap monitoring + rhabdomyolysis management
**Why split:** Osmol gap formula and its role in monitoring mannitol accumulation and the approach to rhabdomyolysis fluid management test independent knowledge domains.

**Card A -- Mannitol osmol gap: formula and monitoring**
> **FRONT:** On the mannitol chart, osmol gap = _______ minus _______. Calculated Osm = _______. A gap above _______ is concerning for mannitol accumulation and supports _______.
>
> **BACK:** Osmol gap = **measured serum osmolality minus calculated serum osmolality**. Calculated Osm = **2x[Na] + BUN/2.8 + glucose/18**. A gap **>20 mOsm/kg** is concerning for accumulation and supports **reassessment and caution per protocol** -- whether to hold, reduce, or continue dosing depends on clinical context and provider judgment. A serum Osm approaching 320 mOsm/kg similarly warrants caution.
> -> CCRN KEY: At high serum Osm, mannitol may begin to cross a disrupted blood-brain barrier -- potentially reversing the osmotic gradient and worsening cerebral edema. Monitoring the osmol gap before repeat dosing is a safety practice, not a standalone decision rule.

**Card B -- Rhabdomyolysis: fluid-first management priorities**
> **FRONT:** On the rhabdomyolysis chart, the cornerstone treatment to prevent AKI is _______, with a goal UO supporting tubular washout. Key labs to monitor include _______.
>
> **BACK:** Cornerstone: **aggressive IV fluid resuscitation** (isotonic crystalloid, targeting UO often 200-300 mL/h or per protocol until CK trending down and urine clearing). Key labs: CK (trending down is the goal), creatinine (monitor for AKI), K+ (hyperkalemia from rhabdomyolysis), phosphate, calcium.
> -> CCRN KEY: Adjuncts such as mannitol or urine alkalinization (NaHCO3) may be ordered per provider and institutional protocol -- evidence supporting routine use is limited. Fluid adequacy and UO are the primary nurse-managed parameters. Escalate rising Cr or K+ to provider promptly.

---

### SPLIT 98 -- nid 1778885720003 * Chunk 46 * MEDIUM
**Topic:** Spironolactone mechanism + RALES trial evidence
**Why split:** Drug mechanism (aldosterone antagonism) and the trial proving mortality benefit (RALES) are independently testable.

**Card A -- Spironolactone mechanism and safety monitoring**
> **FRONT:** On the diuretic chart, spironolactone is an _______ receptor antagonist. Its most dangerous side effect in patients with renal impairment or concurrent RAAS agents is _______.
>
> **BACK:** **Aldosterone receptor antagonist** (blocks mineralocorticoid receptor -- reduces Na reabsorption and promotes K retention in collecting duct). Most dangerous side effect: **hyperkalemia** -- risk is heightened with CrCl <30, concurrent ACEi/ARB/sacubitril-valsartan, supplemental K+, or diabetes.
> -> CCRN KEY: Monitoring: K+ and Cr at 1 week, 1 month, then q3 months. Hold if K+ >5.5 mEq/L or Cr rising significantly -- thresholds vary per protocol. Eplerenone is mineralocorticoid-selective (avoids sex-hormone side effects like gynecomastia) and may be substituted per provider preference.

**Card B -- RALES trial: spironolactone mortality benefit**
> **FRONT:** The RALES trial showed spironolactone reduces all-cause mortality by approximately _______ % in patients with _______ (EF <=___%). The recommended starting dose is _______ mg daily.
>
> **BACK:** RALES (1999, NEJM): ~**30% reduction** in all-cause mortality in HFrEF patients with EF <=35% and NYHA class III-IV. Starting dose: **25 mg once daily**; titrate to 50 mg if tolerated and K+ stable. EPHESUS trial: eplerenone reduces mortality post-MI with EF <40%.
> -> CCRN KEY: Spironolactone's benefit in HF extends beyond diuresis -- aldosterone promotes myocardial fibrosis and adverse cardiac remodeling; blockade may attenuate this, supporting its use even when additional diuresis is not the primary goal.

---

### SPLIT 99 -- nid 1778885720006 * Chunk 46 * MEDIUM
**Topic:** Metolazone + furosemide sequential nephron blockade
**Why split:** Administration timing and monitoring priorities after combination are distinct nurse-performed competencies.

**Card A -- Metolazone: timing and mechanism**
> **FRONT:** On the diuretic chart, metolazone is often given approximately _______ minutes before furosemide per protocol. Its primary site of action is the _______.
>
> **BACK:** Often given **30-60 minutes before furosemide** per institutional protocol -- the timing rationale is pharmacokinetic (allow metolazone to reach tubular sites before furosemide), but exact intervals are not strongly standardized by high-level evidence. Primary site: **distal convoluted tubule (DCT)** via NCC inhibition.
> -> CCRN KEY: Sequential nephron blockade rationale: furosemide blocks the TAL, but compensatory reabsorption at the DCT limits response. Blocking the DCT with metolazone simultaneously reduces this escape, potentially enabling substantial additional diuresis in resistant patients. Typically used short-term (2-3 days) with close monitoring.

**Card B -- Metolazone: critical monitoring after combination**
> **FRONT:** The two most critical electrolyte concerns after metolazone + furosemide combination are _______ and _______. Monitoring frequency should be _______.
>
> **BACK:** **Hypokalemia (K+)** and **hypomagnesemia (Mg2+)** -- the combination can produce profound losses requiring IV replacement. Check BMP **q6-12h after the first combination dose** (or per protocol). Replace Mg2+ first if K+ is refractory -- hypomagnesemia upregulates ROMK, causing ongoing K+ wasting.
> -> CCRN KEY: Prolonged metolazone use risks dangerous cumulative electrolyte depletion. In most HF protocols it is used in brief bursts for acute decongestive needs. Notify provider for K+ <3.5 or Mg2+ <1.5 mEq/L per protocol.

---

### SPLIT 100 -- nid 1778885720012 * Chunk 46 * MEDIUM
**Topic:** DOSE trial -- IV dose strategy + creatinine interpretation
**Why split:** The trial's dosing strategy and the physiological interpretation of the Cr rise test different reasoning skills.

**Card A -- DOSE trial: high-dose IV furosemide strategy for ADHF**
> **FRONT:** The DOSE trial tested a high-dose IV furosemide strategy of _______ x the total daily oral dose. Example: oral furosemide 40 mg BID -- high-dose IV = _______ mg daily.
>
> **BACK:** DOSE trial **tested** a **2.5x the total daily oral dose** IV strategy (not a universal mandate -- this was a trial arm). Example: 40 mg BID = 80 mg/day -- 2.5 x 80 = ~200 mg/day IV (100 mg q12h or ~8 mg/h continuous). DOSE trial found no significant difference between bolus and continuous infusion.
> -> CCRN KEY: DOSE (NEJM 2011): 308 patients. High-dose arm showed more symptom relief and fluid loss but also a modest transient Cr rise. Clinical dosing decisions should account for individual diuretic exposure, renal function, and hemodynamics -- not rigidly apply the 2.5x factor.

**Card B -- DOSE trial: the creatinine rise -- context and meaning**
> **FRONT:** The DOSE trial high-dose arm showed a modest creatinine rise of approximately _______ mg/dL. Clinically, a mild Cr rise during diuresis _______.
>
> **BACK:** ~**0.1 mg/dL** average rise in the high-dose arm. A mild Cr rise during diuresis **requires clinical reassessment** -- it may reflect hemoconcentration (a transient effect of fluid removal) but can also represent reduced renal perfusion or early injury. Context matters: UO, clinical signs of congestion, hemodynamics, and trend all inform the decision.
> -> CCRN KEY: Hemoconcentration tends to stabilize. Hemodynamic AKI tends to progress. Neither a small Cr rise nor a brisk UO alone confirms or rules out harm -- clinical judgment plus trending guides management.

---

### SPLIT 101 -- nid 1778885720018 * Chunk 46 * MEDIUM
**Topic:** Hypomagnesemia causing refractory hypokalemia via ROMK channel
**Why split:** Clinical recognition (refractory hypokalemia) and the molecular mechanism (ROMK upregulation) test different cognitive levels.

**Card A -- Hypomagnesemia causes refractory hypokalemia: clinical rule**
> **FRONT:** On the diuretic electrolyte chart, hypomagnesemia is associated with _______ hypokalemia that may not respond to K+ replacement until _______.
>
> **BACK:** Associated with **refractory hypokalemia** -- K+ may not hold despite replacement when Mg2+ is depleted. Approach: check Mg2+ when K+ remains low despite adequate replacement; replace Mg2+ (IV MgSO4 1-2 g over 20-30 min) and reassess K+ response.
> -> CCRN KEY: Normal Mg2+: 1.7-2.2 mEq/L. Levels <1.5 suggest clinically significant deficiency; <1.0 is associated with arrhythmia risk and neuromuscular excitability. Torsades risk is elevated at low Mg2+ especially with concurrent QT-prolonging agents.

**Card B -- Mechanism: ROMK channel and magnesium**
> **FRONT:** Hypomagnesemia is associated with refractory hypokalemia because magnesium normally inhibits _______ in the collecting duct. Without adequate Mg2+, this channel is _______, contributing to _______.
>
> **BACK:** Mg2+ inhibits **ROMK** (Renal Outer Medullary K+ channel) in the collecting duct. Without Mg2+, ROMK is upregulated -- excess K+ excretion continues even after IV K+ replacement. This is the mechanistic basis for correcting Mg2+ first when K+ is refractory.
> -> CCRN KEY: Loop diuretics waste both K+ and Mg2+. Including Mg2+ in the standard BMP check for diuretic patients is important -- low Mg2+ is a common hidden contributor to persistent hypokalemia.

---

### SPLIT 102 -- nid 1778885720027 * Chunk 46 * MEDIUM
**Topic:** ADHF DOSE trial calculation + decongestion monitoring
**Why split:** Applying the DOSE-based calculation and knowing clinical endpoints of decongestion are different competencies.

**Card A -- ADHF: DOSE-informed IV furosemide dose calculation**
> **FRONT:** A patient on oral furosemide 40 mg BID is admitted for ADHF. Based on the DOSE trial high-dose strategy, an initial IV regimen to consider is _______ mg daily. This may be given as _______.
>
> **BACK:** Based on 2.5x strategy: 80 mg/day oral -- 2.5 x 80 = **~200 mg/day IV** (e.g., 100 mg IV q12h or ~8 mg/h continuous -- DOSE trial found these equivalent). This should be individualized per clinical judgment, protocol, and patient response.
> -> CCRN KEY: Furosemide-naive patients: lower starting doses (40-80 mg IV). Furosemide-tolerant patients may need higher doses for adequate response. Dose escalation should be guided by UO response and clinical assessment.

**Card B -- ADHF decongestion: clinical monitoring endpoints**
> **FRONT:** Clinical signs of successful decongestion in ADHF include _______.
>
> **BACK:** Improving SpO2, decreasing respiratory effort, resolving or improving JVD, improvement in orthopnea, decreasing peripheral edema, and trending improvement in BNP or NT-proBNP (when available). UO response is one metric -- specific targets vary by protocol and patient baseline.
> -> CCRN KEY: BNP and NT-proBNP trends support clinical assessment but are not standalone decision drivers. A patient who is clinically improving with resolving congestion signs is reassuring even if BNP has not normalized. ADHF management is dynamic and requires frequent reassessment.

---

### SPLIT 103 -- nid 1778885720030 * Chunk 46 * MEDIUM
**Topic:** Creatinine monitoring during diuresis + electrolyte priorities
**Why split:** Cr rise interpretation and the electrolyte monitoring priorities during aggressive diuresis are distinct management competencies.

**Card A -- Creatinine monitoring during aggressive diuresis**
> **FRONT:** On the ADHF monitoring chart, a rising creatinine during aggressive diuresis should prompt _______ when it rises more than _______ mg/dL/day.
>
> **BACK:** A Cr rise **>0.3 mg/dL/day** (or rapid progressive rise) should prompt **clinical reassessment** -- not automatic pause. Evaluate: Is the patient clinically over-diuresed (dry, hypotensive, oliguric)? Is the rise stabilizing or accelerating? Is ongoing congestion present justifying continued diuresis? Context determines whether to continue, pause, or adjust.
> -> CCRN KEY: After diuretics are on board, FeNa is unreliable as a differentiator (diuretics increase urinary Na excretion independently of volume status). Clinical signs, hemodynamics, and trends are more informative than FeNa alone.

**Card B -- Electrolyte monitoring during aggressive diuresis**
> **FRONT:** The two electrolytes requiring closest monitoring during aggressive ADHF diuresis are _______ and _______, with goals of _______ and _______ respectively. Monitor BMP at _______ frequency if metolazone is added.
>
> **BACK:** **K+** (goal >4.0 mEq/L, higher preferred in HF to reduce arrhythmia risk) and **Mg2+** (goal >2.0 mEq/L; replace first if K+ is refractory). BMP at least **q12h** if metolazone is added to furosemide. Assess QTc and arrhythmia risk if on concurrent QT-prolonging agents.
> -> CCRN KEY: Hypokalemia + hypomagnesemia + QT-prolonging drug is a setup for torsades de pointes -- a preventable harm. Proactive electrolyte replacement during aggressive diuresis is a core nursing responsibility.

---

### SPLIT 104 -- nid 1778885720033 * Chunk 46 * MEDIUM
**Topic:** Cardiorenal Syndrome Type 1 -- dual mechanism of AKI
**Why split:** Forward failure (decreased CO) and backward failure (venous congestion) are two distinct pathophysiological pathways worth understanding separately.

**Card A -- CRS Type 1: definition and forward failure mechanism**
> **FRONT:** The ADHF chart defines Cardiorenal Syndrome Type 1 as _______ causing _______. The forward failure mechanism is _______ --> decreased renal perfusion pressure --> decreased GFR.
>
> **BACK:** CRS Type 1: **acute cardiac dysfunction causing acute kidney injury**. Forward failure: **decreased cardiac output** leads to decreased renal perfusion pressure and decreased GFR -- the classic "low flow" cardiogenic AKI mechanism.
> -> CCRN KEY: CRS types: Type 1 = Acute HF -> AKI; Type 2 = Chronic HF -> CKD; Type 3 = Acute AKI -> cardiac dysfunction; Type 4 = CKD -> chronic cardiac disease; Type 5 = Systemic disease affecting both (sepsis, DM, amyloid).

**Card B -- CRS Type 1: venous congestion mechanism and diuresis rationale**
> **FRONT:** The elevated _______ pressure in CRS Type 1 may reduce GFR by _______, which supports the use of _______ as treatment -- counterintuitive given rising Cr.
>
> **BACK:** Elevated **renal venous pressure** (venous congestion transmits to renal veins) -- increased renal interstitial pressure -- decreased net filtration pressure -- decreased GFR. This venous congestion pathway may be the dominant mechanism in some patients. Aggressive **diuresis** reduces venous pressure and may improve GFR, even as Cr transiently rises from hemoconcentration.
> -> CCRN KEY: The decision to continue vs hold diuresis in the setting of rising Cr requires provider assessment of volume status, hemodynamics, and clinical trajectory. Nurses should escalate this finding and document clinical signs of congestion vs depletion.

---

### SPLIT 105 -- nid 1778888282021 * Chunk 47 * HIGH
**Topic:** SVR and PVR formulas + normal ranges
**Why split:** SVR (LV afterload) and PVR (RV afterload) have distinct formulas, normal ranges, and clinical implications.

**Card A -- SVR: formula and clinical meaning**
> **FRONT:** On the derived parameters chart, SVR = (_______ - _______) / _______ x 80. Normal SVR is _______ dynes-s/cm5. SVR is clinically significant as a measure of _______.
>
> **BACK:** SVR = **(MAP - CVP) / CO x 80**. Normal: **800-1200 dynes-s/cm5**. SVR reflects **LV systemic afterload** -- the resistance against which the left ventricle ejects. In distributive shock: SVR is low (vasodilation). In cardiogenic/hypovolemic/obstructive shock: SVR is often elevated (compensatory vasoconstriction).
> -> CCRN KEY: SVR is a derived variable -- accuracy requires reliable measurement of MAP, CVP, and CO simultaneously. Clinical goals emphasize adequate MAP and organ perfusion, not normalizing SVR to a specific number.

**Card B -- PVR: formula and clinical meaning**
> **FRONT:** On the derived parameters chart, PVR = (_______ - _______) / _______ x 80. Normal PVR is _______ dynes-s/cm5. Elevated PVR indicates _______ afterload and suggests _______.
>
> **BACK:** PVR = **(mPAP - PCWP) / CO x 80**. Normal: **<250 dynes-s/cm5**. Elevated PVR indicates increased **RV afterload** -- suggests intrinsic pulmonary vascular disease (PAH, PE, ARDS, hypoxic vasoconstriction) rather than simply elevated pulmonary venous pressure from LV failure (which raises mPAP and PCWP proportionally).
> -> CCRN KEY: PA diastolic - PCWP gradient >5 mmHg supports elevated PVR as a distinct finding from elevated left-sided pressures. Untreated elevated PVR risks RV failure -- RV cannot sustain high afterload chronically.

---

### SPLIT 106 -- nid 1778888282030 * Chunk 47 * MEDIUM
**Topic:** PA diastolic as PCWP surrogate + PA-PCWP gradient interpretation
**Why split:** Conditions for valid PA diastolic surrogacy and how to interpret an abnormal PA-PCWP gradient are distinct clinical reasoning steps.

**Card A -- PA diastolic as PCWP surrogate: validity conditions**
> **FRONT:** On the PA catheter chart, PA diastolic pressure closely approximates PCWP when _______ is normal and HR < _______. Why does tachycardia affect this relationship?
>
> **BACK:** PA diastolic approximates PCWP when **PVR is normal** and **HR <100**. Tachycardia: reduced diastolic filling time -- pulmonary circuit does not fully equilibrate -- PA diastolic may overestimate PCWP. High PEEP can also elevate measured PCWP; interpretation requires clinical context.
> -> CCRN KEY: When the catheter cannot be wedged, PA diastolic may serve as a PCWP surrogate IF there is no clinical evidence of elevated PVR. High PEEP effects on PCWP are complex -- always interpret hemodynamic values in full clinical context.

**Card B -- PA diastolic - PCWP gradient: interpretation**
> **FRONT:** On the PA catheter chart, a PA diastolic - PCWP gradient > _______ mmHg is concerning for elevated _______, suggesting _______ rather than pure left heart failure.
>
> **BACK:** Gradient **>5 mmHg** is concerning for elevated **PVR** -- suggests intrinsic pulmonary vascular disease (PE, pulmonary arterial hypertension, ARDS) rather than simply elevated pulmonary venous pressure from LV failure.
> -> CCRN KEY: When PA diastolic rises but PCWP is unchanged -- RV afterload has increased. When both rise proportionally -- LV filling pressures are elevated. This distinction guides treatment: RV afterload reduction (inhaled NO, prostacyclin) vs LV-directed diuresis.

---

### SPLIT 107 -- nid 1778888282039 * Chunk 47 * MEDIUM
**Topic:** PLR technique + positive response criterion
**Why split:** Physical technique and autotransfusion mechanism and the positive response threshold plus clinical utility are sequential but distinct competencies.

**Card A -- Passive leg raise: technique and autotransfusion**
> **FRONT:** On the fluid responsiveness chart, PLR is performed by elevating legs to _______ degrees, producing approximately _______ mL autotransfusion from _______.
>
> **BACK:** Elevate legs to **45 degrees** (lower HOB from semi-recumbent position to flat simultaneously). Autotransfusion: ~**300 mL** from venous reservoir in legs and splanchnic bed. Effect lasts **60-90 seconds** -- CO/SV must be measured during the maneuver, not after returning to baseline.
> -> CCRN KEY: PLR must start from semi-recumbent position (30-45 deg HOB) -- raising legs from flat alone provides minimal additional preload. The simultaneous lowering of HOB is essential.

**Card B -- PLR: positive response and clinical utility**
> **FRONT:** A positive PLR response requires >= _______ % increase in _______, measured by _______. PLR is preferred over PPV/SVV when the patient has _______.
>
> **BACK:** Positive response: **>=10% increase** in **cardiac output or stroke volume**, measured directly via: arterial pulse pressure analysis (APCO), Doppler (LVOT VTI), or PA catheter. Preferred over PPV/SVV in patients with: **spontaneous breathing, arrhythmias, ARDS, or low-tidal-volume ventilation** -- all of which invalidate pulse pressure variation.
> -> CCRN KEY: PLR is a reversible fluid challenge -- a positive result supports giving fluid; a negative result suggests fluid will not increase CO, with no actual fluid administered. Safe for volume-sensitive patients.

---

### SPLIT 108 -- nid 1778888282003 * Chunk 47 * LOW
**Topic:** SVR formula + clinical interpretation of abnormal values
**Why split:** Formula recall and clinical interpretation of SVR values are independently assessable even as a LOW card.

**Card A -- SVR formula (hemodynamic parameters)**
> **FRONT:** The hemo parameters chart: SVR = (_______ - _______) / _______ x 80. Units are _______.
>
> **BACK:** SVR = **(MAP - CVP) / CO x 80** dynes-s/cm5. Normal range: **800-1200 dynes-s/cm5**. SVR reflects LV systemic afterload and is a derived variable -- all input values (MAP, CVP, CO) must be accurately and simultaneously measured.
> -> CCRN KEY: SVR is calculated, not directly measured. Errors in MAP, CVP, or CO propagate to the SVR result. Use it as one component of hemodynamic assessment, not in isolation.

**Card B -- SVR abnormal values: clinical interpretation**
> **FRONT:** SVR below _______ dynes-s/cm5 is concerning for pathologic _______. SVR above _______ is consistent with _______. In septic shock, the clinical focus is on _______.
>
> **BACK:** SVR <**800**: suggests **pathologic vasodilation** -- consistent with distributive/septic shock. SVR >**1200**: consistent with **compensatory vasoconstriction** -- seen in cardiogenic, hypovolemic, or obstructive shock. In septic shock: focus on **adequate MAP and evidence of tissue perfusion** (lactate trend, UO, mentation) rather than targeting a specific SVR number.
> -> CCRN KEY: SVR alone does not determine treatment. Organ perfusion endpoints (lactate, UO, ScvO2) define resuscitation success, not normalization of the SVR value.

---

### SPLIT 109 -- nid 1778916159024 * Chunk 48 * HIGH
**Topic:** Osmol gap formula + toxic alcohol diagnosis + fomepizole antidote
**Why split:** Osmol gap calculation and toxic alcohol pattern recognition and the antidote mechanism and treatment decisions are independent clinical competencies.

**Card A -- Osmol gap formula and toxic alcohol diagnosis**
> **FRONT:** On the osmol gap chart, calculated osmolality = 2x[Na] + BUN/_______ + glucose/_______. An osmol gap > _______ combined with high-AG metabolic acidosis is concerning for _______.
>
> **BACK:** Calculated Osm = 2x[Na] + BUN/**2.8** + glucose/**18** (add EtOH/4.6 if ethanol measured). Osmol gap = measured minus calculated (normal <10 mOsm/kg). Gap **>20** with **HAGMA** is concerning for **toxic alcohol ingestion** (methanol or ethylene glycol) and warrants urgent workup.
> -> CCRN KEY: A normal osmol gap does not rule out toxic alcohol -- late presentations show HAGMA without osmol gap (parent alcohol already metabolized to toxic acids). Methanol toxicity: formate -- optic nerve/retinal damage. Ethylene glycol: oxalate -- calcium oxalate crystals -- AKI.

**Card B -- Fomepizole: antidote mechanism and hemodialysis**
> **FRONT:** The antidote for both methanol and ethylene glycol is _______. Its mechanism is _______ and hemodialysis is indicated when _______.
>
> **BACK:** **Fomepizole** (4-methylpyrazole) -- **competitively inhibits alcohol dehydrogenase (ADH)**, blocking conversion of toxic alcohols to their harmful metabolites (formate/oxalate). Hemodialysis: indicated for severe toxicity to remove parent alcohols and toxic metabolites (severe metabolic acidosis, renal failure, visual symptoms in methanol poisoning).
> -> CCRN KEY: Ethanol infusion may be used as an ADH competitor if fomepizole is unavailable -- same mechanism, less predictable. Fomepizole is preferred. Both buy time by halting toxic metabolite production.

---

### SPLIT 110 -- nid 1778916159003 * Chunk 48 * MEDIUM
**Topic:** Chronic vs acute respiratory acidosis compensation
**Why split:** Formulas for acute and chronic HCO3 compensation test different memory retrieval tasks.

**Card A -- Acute respiratory acidosis: HCO3 compensation formula**
> **FRONT:** On the acid-base chart, acute respiratory acidosis is expected to raise HCO3 by approximately _______ mEq/L per 10 mmHg rise in PaCO2. This occurs via _______.
>
> **BACK:** Acute: **~1 mEq/L per 10 mmHg rise in PaCO2** (Delta-HCO3 = 0.1 x Delta-PaCO2). Buffering via **carbonate and hemoglobin buffer systems** (minutes to hours; no renal involvement). Limited compensation -- pH remains significantly acidemic with large PaCO2 elevations.
> -> CCRN KEY: If HCO3 is much higher than the acute formula predicts, consider a chronic component or concurrent metabolic alkalosis. If lower, consider concurrent metabolic acidosis. Systematic ABG interpretation prevents missing mixed disorders.

**Card B -- Chronic respiratory acidosis: HCO3 compensation and time course**
> **FRONT:** Chronic respiratory acidosis is expected to raise HCO3 by approximately _______ mEq/L per 10 mmHg rise in PaCO2. Renal compensation takes _______ days to fully develop; maximum HCO3 is approximately _______.
>
> **BACK:** Chronic: **~3.5 mEq/L per 10 mmHg** (Delta-HCO3 = 0.35 x Delta-PaCO2). Renal compensation fully develops in **3-5 days** via: increased proximal tubular H+ secretion, NH4+ excretion, and HCO3 reabsorption. Maximum compensation: **~38-40 mEq/L** HCO3.
> -> CCRN KEY: COPD example: baseline PaCO2 60, HCO3 33 (chronic). Acute exacerbation to PaCO2 75 (+15 mmHg) -- expected acute add-on HCO3 = 33 + (0.1 x 15) = ~34.5. pH will still be acidemic. COPD patients tolerate elevated PaCO2 because years of renal compensation have buffered the pH baseline.

---

### SPLIT 111 -- nid 1778916159033 * Chunk 48 * MEDIUM
**Topic:** A-a gradient formula + elevated vs normal A-a interpretation
**Why split:** The gradient formula and elevated meaning and the specific implication when A-a is normal but PaO2 is low are separate reasoning steps.

**Card A -- A-a gradient: formula and elevated meaning**
> **FRONT:** On the ABG chart, A-a gradient = PAO2 - PaO2. An elevated A-a gradient (> approximately _______ mmHg on room air) suggests _______. PAO2 formula = _______.
>
> **BACK:** Normal A-a: approximately **<15-20 mmHg** on room air (age/4 + 4 mmHg as a rough guide). An elevated A-a gradient suggests **parenchymal or vascular lung dysfunction** -- V/Q mismatch, intrapulmonary shunt, or diffusion impairment. PAO2 = **FiO2 x 713 - PaCO2/0.8** (at sea level).
> -> CCRN KEY: The A-a gradient rises with age and with supplemental O2 (on FiO2 1.0, normal A-a can be up to ~100 mmHg). Always interpret in clinical context -- not as an absolute threshold.

**Card B -- Normal A-a gradient with low PaO2: hypoventilation pattern**
> **FRONT:** On the ABG chart, a NORMAL A-a gradient combined with hypoxemia (low PaO2) supports _______ as the cause. The expected PaCO2 in this pattern is _______.
>
> **BACK:** Supports **hypoventilation** as the primary mechanism -- lungs are exchanging gas normally but alveolar ventilation is inadequate. PaCO2 will be **elevated** (CO2 accumulates from insufficient breathing). A-a stays normal because what reaches the alveoli exchanges efficiently.
> -> CCRN KEY: Hypoxemia differential by A-a: Normal A-a + elevated PaCO2 = hypoventilation (treat the breathing). Elevated A-a = parenchymal cause (V/Q mismatch, shunt, diffusion). Shunt (ARDS, large atelectasis) classically does not fully correct with supplemental O2.

---

### SPLIT 112 -- nid 1778916159012 * Chunk 48 * LOW
**Topic:** Delta-delta ratio formula and four-scenario interpretation
**Why split:** Formula recall and knowing what each ratio range means are independently testable steps.

**Card A -- Delta-delta formula**
> **FRONT:** On the compensation chart, the delta-delta ratio formula is (_______ - _______) / (_______ - HCO3).
>
> **BACK:** Delta-delta = **(AG - 12) / (24 - HCO3)**. Numerator: AG elevation above normal (~12). Denominator: HCO3 drop below normal (~24). Together they compare AG change to HCO3 change -- used to detect mixed acid-base disorders in the context of HAGMA.
> -> CCRN KEY: Correct for albumin first: adjusted AG = calculated AG + 2.5 x (4 - albumin). Without correction in hypoalbuminemia (common in ICU), a true HAGMA may be missed.

**Card B -- Delta-delta ratio: four interpretation ranges**
> **FRONT:** Delta-delta: <0.4 suggests _______; 0.4-1.0 suggests _______; 1.0-2.0 is consistent with _______; >2.0 suggests _______.
>
> **BACK:** <0.4 = **pure NAGMA** (no meaningful AG elevation). 0.4-1.0 = **mixed HAGMA + NAGMA** (AG elevated but HCO3 lower than expected for AG alone). 1.0-2.0 = **pure HAGMA** (expected 1:1 relationship). >2.0 = **HAGMA + concurrent metabolic alkalosis** (HCO3 higher than expected -- alkalosis partially masking HCO3 drop).
> -> CCRN KEY: DKA + vomiting: AG = 30, HCO3 = 20 -- delta-delta = (30-12)/(24-20) = 18/4 = 4.5 -- consistent with HAGMA + metabolic alkalosis. Pure DKA HCO3 should be ~6; vomiting raised it to 20. Correcting DKA will unmask the metabolic alkalosis as HCO3 rises back.


---

### SPLIT 113 -- nid 1778917346021 * Chunk 49 * HIGH
**Topic:** FeNa formula and interpretation + FeUrea as alternative in diuretic patients
**Why split:** FeNa calculation and its pre-renal vs ATN interpretation and the FeUrea alternative (required when diuretics confound FeNa) are distinct competencies -- one is the tool, one is when to switch tools.

**Card A -- FeNa: formula and pre-renal vs ATN thresholds**
> **FRONT:** On the renal differentiation chart, FeNa < _______ % suggests pre-renal AKI. FeNa is calculated as _______. FeNa > _______ % is consistent with intrinsic renal damage (ATN).
>
> **BACK:** FeNa < **1%**: suggests pre-renal AKI (kidneys avidly retain Na -- concentrated urine). FeNa > **2%**: consistent with ATN (damaged tubules cannot conserve Na). Formula: **FeNa = (urine Na x plasma Cr) / (plasma Na x urine Cr) x 100%**. Complementary markers: pre-renal also shows urine Osm >500, BUN:Cr >20:1, urine Na <20 mEq/L.
> -> CCRN KEY: FeNa is most reliable in patients not receiving diuretics. After diuretics are given, urinary Na excretion is artificially elevated regardless of volume status -- FeNa loses its discriminatory value. In that setting, FeUrea is more informative.

**Card B -- FeUrea: alternative marker for diuretic patients**
> **FRONT:** In patients receiving diuretics, FeNa is unreliable because _______. Instead, use FeUrea < _______ % to suggest pre-renal AKI.
>
> **BACK:** FeNa unreliable on diuretics because diuretics force Na excretion independently of volume status -- artificially elevating FeNa even in volume-depleted patients. FeUrea < **35%**: suggests pre-renal (urea reabsorption remains intact, reflecting tubular conservation). FeUrea > 35%: suggests intrinsic renal damage.
> -> CCRN KEY: Pre-renal differentiation on diuretics -- use FeUrea as a supplement to clinical assessment. No single urine marker replaces clinical context (fluid balance, hemodynamics, response to IVF, ultrasound findings).

---

### SPLIT 114 -- nid 1778917346030 * Chunk 49 * HIGH
**Topic:** ISTH overt DIC scoring + DIC treatment priorities
**Why split:** The scoring criteria (diagnosis) and the management sequence (treatment: address precipitant first) are independently testable competencies.

**Card A -- ISTH DIC scoring: point thresholds**
> **FRONT:** On the DIC diagnosis chart, the ISTH overt DIC score: Platelets < _______ K = 2 points. D-dimer strongly elevated = _______ points. PT prolonged > _______ seconds = 2 points. Score >= _______ confirms overt DIC.
>
> **BACK:** ISTH Overt DIC: Platelets: >100K = 0; 50-100K = 1; **<50K = 2 points**. D-dimer/fibrin degradation: none = 0; moderate = 2; **strong = 3 points**. PT: <3s = 0; 3-6s = 1; **>6s = 2 points**. Fibrinogen: >=1 g/L = 0; <1 g/L = 1 point. **Score >=5 = overt DIC**; <5 = non-overt or pre-DIC.
> -> CCRN KEY: DIC causes include: sepsis (#1 cause), trauma, amniotic fluid embolism, brain injury (tissue factor release); APL/M3 AML (most dramatic DIC presentation -- responds to ATRA + arsenic); HELLP syndrome. Identifying and treating the precipitant is the primary intervention.

**Card B -- DIC treatment priorities**
> **FRONT:** On the DIC management chart, the FIRST priority in DIC management is _______. Replacement products are: FFP for _______, cryoprecipitate for _______, and platelets for _______.
>
> **BACK:** **FIRST: Address the precipitant** (sepsis -- antibiotics/vasopressors; APL -- ATRA; placental abruption -- delivery). Replacement: FFP for elevated PT/aPTT; cryoprecipitate when fibrinogen <100-150 mg/dL; platelets when <50K with active bleeding. Targets: fibrinogen >100-150, platelets >50K if bleeding.
> -> CCRN KEY: Treating DIC without addressing the precipitant is inadequate -- factors will continue to be consumed. Product replacement supports the patient while the underlying cause is corrected. Heparin use in DIC is controversial and limited to specific indications (thrombosis-dominant DIC).

---

### SPLIT 115 -- nid 1778917346000 * Chunk 49 * MEDIUM
**Topic:** Critical hyperkalemia recognition + calcium gluconate mechanism
**Why split:** Recognizing the critical value and EKG progression (nursing_action/diagnosis) and the mechanism and role of calcium gluconate as first-line (drug_mechanism) test different competency levels.

**Card A -- Critical hyperkalemia: recognition and EKG progression**
> **FRONT:** On the critical labs chart, the critical HIGH potassium value requiring immediate cardiac intervention is > _______ mEq/L. The EKG changes progress in sequence: _______.
>
> **BACK:** Critical high K+: **>6.5 mEq/L** (or >6.0 with EKG changes). EKG progression (early to late): **peaked T waves** (earliest) -> prolonged PR -> widened QRS -> loss of P waves -> sine wave pattern -> ventricular fibrillation -> asystole. Peaked T waves are the most important early warning sign.
> -> CCRN KEY: Notify provider immediately for K+ >6.0 with EKG changes or K+ >6.5 regardless of EKG. Obtain 12-lead ECG, continuous telemetry monitoring. The cardiac membrane is at risk -- the sequence is progressive and can rapidly deteriorate.

**Card B -- Calcium gluconate: first-line mechanism in hyperkalemia**
> **FRONT:** The first medication given for K+ > 6.5 with EKG changes is _______, which works by _______. It does NOT _______.
>
> **BACK:** **Calcium gluconate 1-2 g IV over 5-10 min**. Mechanism: **membrane stabilization** -- raises the threshold potential of myocardial cells, reducing excitability and VF risk. **Does NOT lower K+ level** -- onset 1-3 min, duration 30-60 min. After calcium: insulin 10 units + D50W (shifts K+ into cells) + kayexalate/patiromer (GI removal for gradual reduction).
> -> CCRN KEY: Do NOT confuse calcium gluconate (peripheral IV safe) with calcium chloride (contains 3x more elemental Ca, requires central access -- causes tissue necrosis if extravasated). Calcium chloride is reserved for cardiac arrest scenarios.

---

### SPLIT 116 -- nid 1778917346027 * Chunk 49 * MEDIUM
**Topic:** PT/INR reflects extrinsic pathway + aPTT reflects intrinsic pathway
**Why split:** Understanding what each test measures (drug_mechanism: which coagulation pathway) and knowing the clinical monitoring application for aPTT (drug_monitoring: UFH goal) are distinct competencies.

**Card A -- PT/INR: extrinsic pathway and clinical significance**
> **FRONT:** On the coagulation panel chart, PT/INR reflects the _______ coagulation pathway and is prolonged by _______.
>
> **BACK:** PT/INR reflects the **extrinsic pathway** -- factors VII, X, V, II, fibrinogen. Factor VII has the shortest half-life (~6h) -- PT/INR rises first in liver failure or warfarin use. Prolonged by: **warfarin**, liver disease, vitamin K deficiency, factor VII deficiency.
> -> CCRN KEY: PT/INR is the most sensitive indicator of acute liver synthetic dysfunction (factor VII falls first). In warfarin therapy, INR target depends on indication: most indications = 2-3; mechanical mitral valve = 2.5-3.5.

**Card B -- aPTT: intrinsic pathway and UFH monitoring**
> **FRONT:** aPTT reflects the _______ pathway and is used to monitor _______ therapy. Therapeutic aPTT goal for UFH is _______.
>
> **BACK:** aPTT reflects the **intrinsic pathway** -- factors XII, XI, IX, VIII, X, V, II, fibrinogen. Used to monitor **unfractionated heparin (UFH)** therapy. Therapeutic goal: **1.5-2.5x control** (approximately 60-100 seconds depending on laboratory). UFH mechanism: binds antithrombin (AT) -- AT-UFH complex inhibits IIa (thrombin) + Xa.
> -> CCRN KEY: Elevated aPTT with normal PT -- causes to consider: UFH contamination of sample (draw from opposite arm from heparin drip), hemophilia A/B (factor VIII/IX deficiency), lupus anticoagulant (paradoxically elevated aPTT but THROMBOTIC tendency). Mixing study: if aPTT corrects -- factor deficiency; if does not correct -- inhibitor present.

---

### SPLIT 117 -- nid 1778918481021 * Chunk 50 * MEDIUM
**Topic:** SBT protocol parameters + failure criteria + next step
**Why split:** SBT parameters and trial duration (clinical_trial knowledge) and failure criteria plus the post-SBT next step (next_step_workup) are sequential but distinct clinical decisions.

**Card A -- SBT protocol: parameters and duration**
> **FRONT:** On the SBT protocol chart, a standard spontaneous breathing trial uses pressure support of _______ cmH2O for _______ minutes. The REVA trial showed _______ min duration is adequate.
>
> **BACK:** SBT: **T-piece OR PSV 5-8 cmH2O + PEEP 5** for **30-120 minutes**. REVA trial: no difference between 30 vs 120 min SBT duration -- **30 min is adequate** for most patients. Protocolized daily SBT reduces ICU LOS vs physician-directed weaning. SAT sequence: assess eligibility at 0600 -- perform SAT first -- then SBT same day (SAT before SBT, not reverse).
> -> CCRN KEY: SBT eligibility screen (must pass before SBT): SpO2 >=88% on FiO2 <=70%, PEEP <=12, no active seizures, no NMB, no alcohol withdrawal, hemodynamically stable, no worsening agitation.

**Card B -- SBT failure criteria and post-SBT next step**
> **FRONT:** SBT FAILURE is declared if RR exceeds _______, SpO2 drops below _______ %, or RSBI > _______. After successful SBT, the next step is _______.
>
> **BACK:** Failure criteria -- declare failure and return to prior settings if ANY: **RR >35**, **SpO2 <90%**, **RSBI >105**, HR >140 or change >20%, SBP >180 or <90 mmHg, accessory muscle use, diaphoresis, paradoxical breathing, or agitation. After successful SBT: **extubation assessment** (adequate cough, secretion management, mental status, no stridor on cuff deflation test).
> -> CCRN KEY: Passing an SBT does not guarantee successful extubation -- assess separately: peak cough flow >160 L/min, absence of stridor on cuff deflation, patient awake and following commands. Mental status is independent of RSBI -- a patient can pass RSBI but be too obtunded to protect the airway.

---

### SPLIT 118 -- nid 1778918481030 * Chunk 50 * MEDIUM
**Topic:** Peak pressure troubleshooting -- resistance vs compliance pathology
**Why split:** The resistance pattern (high peak + normal plateau) and the compliance pattern (high peak + high plateau) test different diagnostic reasoning steps -- they have different causes and management.

**Card A -- High peak + normal plateau: resistance problem**
> **FRONT:** On the peak pressure troubleshooting chart, elevated PEAK pressure with NORMAL plateau pressure indicates increased _______. Common causes are _______. Plateau pressure is only valid in a _______ ventilated patient.
>
> **BACK:** Elevated peak + normal plateau = increased **airway resistance (Raw)**. Raw = (Peak Pressure - Plateau) / Flow; normal Raw: 5-15 cmH2O/L/s. Causes: bronchospasm, secretions, ETT kinking or biting, circuit obstruction. Management: suction, bronchodilators, bite block, NMB if patient-vent dyssynchrony. Plateau valid only in **passively ventilated** patients (no spontaneous effort during pause).
> -> CCRN KEY: The two-variable test: Peak pressure alone reflects BOTH resistance and compliance. Plateau pressure isolates compliance (no flow = no resistance component). Large (peak - plateau) gap = resistance problem. Ensure patient is passive (RASS -2 to -3 or NMB) before measuring Pplat.

**Card B -- High peak + high plateau: compliance problem**
> **FRONT:** Elevated BOTH peak AND plateau pressures indicate decreased _______. Common causes in the ICU are _______.
>
> **BACK:** High peak + high plateau = decreased **respiratory system compliance (Crs)**. Crs = Vt / (Pplat - PEEP); normal ~60-100 mL/cmH2O. Causes: worsening ARDS, pulmonary edema, pneumothorax (tension), auto-PEEP, abdominal hypertension, pleural effusion, obesity.
> -> CCRN KEY: When plateau rises acutely -- always consider pneumothorax (check breath sounds, tracheal position, hemodynamics). Lung-protective strategy: maintain Pplat <=30 cmH2O; reduce Vt to 4-6 mL/kg IBW if needed. Pplat >30 = high risk of ventilator-induced lung injury.

---

### SPLIT 119 -- nid 1778921335000 * Chunk 51 * MEDIUM
**Topic:** P/F ratio formula + Berlin ARDS classification
**Why split:** The P/F ratio formula and basic hypoxemia threshold (formula_calculation) and the Berlin ARDS severity classification (diagnosis_criteria) are independently testable.

**Card A -- P/F ratio: formula and hypoxemic respiratory failure threshold**
> **FRONT:** On the oxygenation formulas chart, P/F ratio = PaO2 / FiO2. A P/F ratio < _______ defines hypoxemic respiratory failure. On FiO2 1.0 with PaO2 70 mmHg, the P/F ratio is _______.
>
> **BACK:** P/F < **300 mmHg** = hypoxemic respiratory failure. On FiO2 1.0, PaO2 70: P/F = 70/1.0 = **70** (severe ARDS). FiO2 is expressed as a decimal (0.50, not 50%). P/F < 150 = prone positioning threshold (PROSEVA). P/F < 80 with pH <7.20 = consider VV-ECMO.
> -> CCRN KEY: S/F ratio (SpO2/FiO2) substitutes when ABG unavailable -- S/F <315 correlates with P/F <300. Oxygenation Index (OI) = FiO2 x mean airway pressure x 100 / PaO2 -- OI >25 = severe ARDS; OI >40 = ECMO threshold (accounts for MAP contribution).

**Card B -- Berlin ARDS classification: three severity categories**
> **FRONT:** The Berlin criteria classify ARDS requiring PEEP >= _______ cmH2O as: mild (P/F _______ to _______), moderate (P/F _______ to _______), and severe (P/F < _______).
>
> **BACK:** All require **PEEP >=5 cmH2O** plus: bilateral opacities on CXR/CT (not fully explained by effusion, collapse, or nodules) plus: respiratory failure not fully explained by cardiac failure/fluid overload. **Mild: P/F 200-300** (mortality ~27%). **Moderate: P/F 100-200** (mortality ~32%). **Severe: P/F <100** (mortality ~45%).
> -> CCRN KEY: Berlin criteria (2012) replaced the older ALI/ARDS distinction. PEEP >=5 requirement: ensures oxygenation is assessed under adequate respiratory support. Timing: within 1 week of known clinical insult or new/worsening respiratory symptoms.

---

### SPLIT 120 -- nid 1778921335006 * Chunk 51 * MEDIUM
**Topic:** A-a gradient formula + elevated vs normal A-a interpretation
**Why split:** The gradient formula and how to calculate PAO2 (biomarker_kinetics) and the clinical interpretation distinguishing V/Q mismatch from pure hypoventilation (clinical_interpretation) are separate reasoning steps.

**Card A -- A-a gradient: formula and PAO2 calculation**
> **FRONT:** On the oxygenation chart, A-a gradient = PAO2 - PaO2, where PAO2 = _______. Normal A-a gradient in a young adult is < _______ mmHg.
>
> **BACK:** PAO2 = **(FiO2 x [Patm - PH2O]) - PaCO2/RQ**; simplified on room air at sea level: PAO2 = (0.21 x 713) - PaCO2/0.8 = 150 - PaCO2/0.8. Normal A-a: **<10-15 mmHg** in young adults; increases with age (age/4 + 4 as a rough guide).
> -> CCRN KEY: On FiO2 1.0, normal A-a gradient can be up to ~100 mmHg -- always interpret in the context of FiO2 being used. A-a widens with age, supplemental O2 use, and any parenchymal pathology.

**Card B -- A-a gradient: interpretation in hypoxemia**
> **FRONT:** An elevated A-a gradient with normal PaCO2 suggests _______. A normal A-a gradient with elevated PaCO2 suggests _______.
>
> **BACK:** Elevated A-a + normal PaCO2 = **V/Q mismatch or intrapulmonary shunt** (PE, ARDS, pneumonia -- alveolar-capillary exchange is impaired). Normal A-a + elevated PaCO2 = **pure hypoventilation** (opiates, NMB, neuromuscular disease -- lungs exchange normally, but ventilation is inadequate).
> -> CCRN KEY: Classic shunt pattern: on FiO2 1.0, PaO2 does NOT correct to expected (>600 mmHg) -- blood bypasses ventilated alveoli entirely. PEEP opens collapsed alveoli and recruits shunt units; supplemental FiO2 alone cannot overcome true shunt. Shunt fraction >20% = refractory hypoxemia.

---

### SPLIT 121 -- nid 1778921335042 * Chunk 51 * MEDIUM
**Topic:** PICS incidence and three domains + ICU diary intervention
**Why split:** The epidemiology and three impairment domains (what PICS is) and the evidence-based intervention (ICU diary) test different competency layers.

**Card A -- PICS: incidence and three impairment domains**
> **FRONT:** The PICS chart shows Post-Intensive Care Syndrome affects approximately _______ % of ICU survivors. The three impairment domains are _______, _______, and _______.
>
> **BACK:** PICS affects **25-50%** of ICU survivors (varies by population and follow-up duration). Three domains: (1) **Cognitive** -- memory, attention, executive function deficits (similar to mild TBI; may persist 5+ years); (2) **Physical** -- ICUAW, fatigue, dyspnea, dysphagia, functional disability; (3) **Mental health** -- PTSD (~25%), depression (~30%), anxiety (up to 70%).
> -> CCRN KEY: PICS is not just an ICU issue -- it extends months to years post-discharge. Many survivors cannot return to work at 1 year. Prevention inside the ICU (ABCDEF bundle, early mobility, family engagement) = prevention of PICS after discharge. PICS-Family (PICS-F): 30% of family members develop PTSD, complicated grief, or depression -- ICU diaries benefit both patients and families.

**Card B -- ICU diary: evidence and role in PICS prevention**
> **FRONT:** The intervention shown to reduce PTSD risk by up to _______ % in some trials is _______. This works by _______.
>
> **BACK:** **ICU diary** -- patient and family written record of events during the ICU stay. Reduces PTSD risk by up to **60%** in some trials (varied by study design). Mechanism: provides a narrative framework to fill memory gaps from the ICU experience, reducing the "black hole" that contributes to PTSD and anxiety about what happened.
> -> CCRN KEY: ICU diaries are nurse-led -- any bedside nurse can contribute entries. Include: daily events, procedures, clinical progress, meaningful interactions. Written in plain language the patient can understand when recovered. Survivor clinic programs (multi-disciplinary: medicine, psychology, PT/OT) provide systematic post-ICU follow-up addressing all three PICS domains.

---

### SPLIT 122 -- nid 1778923627033 * Chunk 52 * HIGH
**Topic:** Stress dose steroids -- SSC recommendation + empiric trigger + dose regimen
**Why split:** The SSC recommendation against routine testing (clinical_trial/guideline) and the dose regimen itself (drug_dose) are distinct pieces of clinical knowledge.

**Card A -- Stress dose steroids: SSC 2021 trigger and empiric approach**
> **FRONT:** On the stress dose steroids chart, SSC 2021 _______ (recommends / does not recommend) routine cortisol testing before initiating steroids. The trigger for empiric steroids in septic shock is _______.
>
> **BACK:** SSC 2021: does **NOT recommend routine cortisol testing** -- give steroids **empirically** when vasopressor-dependent despite adequate fluid resuscitation. Trigger: vasopressor requirement persisting (NE or Epi >=0.25 mcg/kg/min per SSC, or per institutional threshold).
> -> CCRN KEY: If cortisol testing is performed (e.g., suspected primary adrenal insufficiency): random cortisol <15-18 mcg/dL OR cosyntropin stimulation (250 mcg) with delta cortisol <9 mcg/dL suggests relative adrenal insufficiency. These thresholds are used when clinical context supports testing -- not routine in septic shock per SSC 2021.

**Card B -- Stress dose steroid regimen and weaning**
> **FRONT:** The stress dose regimen for septic shock is hydrocortisone _______ mg every _______ hours (or _______ mg/day continuous). Steroids should be weaned with _______.
>
> **BACK:** Regimen: hydrocortisone **50 mg IV q6h** OR **200 mg/day continuous infusion** for 5-7 days. Wean: taper in parallel with vasopressor wean -- do NOT abruptly discontinue (may cause adrenal rebound and hemodynamic deterioration).
> -> CCRN KEY: Hydrocortisone 200 mg/day has mineralocorticoid activity -- routine fludrocortisone supplementation is only needed at doses <100 mg/day. For known primary adrenal insufficiency (Addisonian crisis): hydrocortisone 100 mg IV bolus, then 50-100 mg IV q6-8h + fludrocortisone 0.1 mg/day.

---

### SPLIT 123 -- nid 1778923627036 * Chunk 52 * HIGH
**Topic:** Vasopressin fixed dosing + V1 mechanism + VASST trial + safety limit
**Why split:** The pharmacological rationale for fixed dosing (drug_mechanism) and the clinical trial evidence (VASST) are independently testable knowledge.

**Card A -- Vasopressin: fixed dose and V1 mechanism**
> **FRONT:** The vasopressin chart shows it is dosed at _______ units/min as a FIXED dose -- it is NOT _______. Its V1 receptor causes _______ in skin, muscle, and splanchnic vessels.
>
> **BACK:** Dose: **0.03-0.04 units/min IV -- fixed rate, NOT titrated**. V1 receptors (vascular): **vasoconstriction** -- skin, skeletal muscle, and splanchnic vasculature. Maximum dose: 0.04 units/min -- doses above this risk coronary and mesenteric ischemia (V1 receptors in those territories). V2 receptors (renal): antidiuretic (ADH) effect.
> -> CCRN KEY: Vasopressin is NOT a catecholamine -- it acts via V1 receptors (not adrenergic receptors). This is the mechanistic basis for its catecholamine-sparing utility: it provides vasoconstriction through a completely separate receptor class, useful when adrenergic receptors are downregulated in prolonged shock.

**Card B -- VASST trial: vasopressin evidence**
> **FRONT:** The VASST trial compared vasopressin 0.03 units/min + norepinephrine vs norepinephrine alone in septic shock. Primary finding: _______, and the subgroup with greatest benefit was _______.
>
> **BACK:** Primary finding: **reduced norepinephrine requirements** (catecholamine-sparing); no statistically significant mortality difference in the overall cohort. Greatest benefit: **less severe shock subgroup** (NE 5-14 mcg/min at enrollment) -- post-hoc finding suggesting benefit before catecholamine-refractory state develops.
> -> CCRN KEY: Clinical use: add vasopressin at 0.03-0.04 units/min when NE exceeds approximately 0.25-0.5 mcg/kg/min. Goal is catecholamine sparing -- not replacement. Vasopressin does NOT improve cardiac output. Do not use as sole vasopressor.

---

### SPLIT 124 -- nid 1778923627039 * Chunk 52 * HIGH
**Topic:** Terlipressin for HRS + CONFIRM trial + monitoring
**Why split:** The clinical indication and trial evidence and the practical dosing, contraindications, and nursing monitoring priorities are independently testable for the CCRN exam.

**Card A -- Terlipressin: indication and CONFIRM trial**
> **FRONT:** On the terlipressin chart, it is used for _______ syndrome (HRS-AKI). The CONFIRM trial showed HRS reversal in _______ vs _______ % with placebo. FDA approval was in _______.
>
> **BACK:** Indication: **Hepatorenal Syndrome (HRS-AKI)** in decompensated cirrhosis. CONFIRM trial (NEJM 2021, n=300): terlipressin + albumin vs placebo + albumin -- **HRS reversal 32.4% vs 16.5%** (SCr <=1.5 mg/dL x 48h without death or dialysis). FDA approved: **August 2022** (first FDA-approved therapy for HRS-AKI in USA).
> -> CCRN KEY: HRS pathophysiology: cirrhosis -- portal hypertension -- splanchnic vasodilation -- RAAS/SNS activation -- renal vasoconstriction -- functional AKI (no structural kidney damage). Terlipressin V1 effect: splanchnic vasoconstriction -- improves effective blood volume -- increases renal perfusion.

**Card B -- Terlipressin: dosing, contraindications, and nursing monitoring**
> **FRONT:** Terlipressin dose is _______ mg IV q4-6h. Its key contraindications include _______. The primary nursing monitoring priority is _______.
>
> **BACK:** Dose: **1 mg IV q4-6h**; may increase to 2 mg q4-6h if SCr does not decrease >=25% within 48h. Duration: up to 14 days or until SCr <1.5 mg/dL. Contraindications: **ischemic heart disease, severe COPD, peripheral vascular disease**. Nursing monitoring priority: **respiratory status** -- albumin + terlipressin combination can cause fluid retention and pulmonary edema.
> -> CCRN KEY: If terlipressin unavailable or contraindicated, alternatives include: midodrine + octreotide + albumin (less effective, ~20-30% HRS reversal); norepinephrine IV + albumin in ICU setting. Liver transplantation remains definitive treatment -- terlipressin is a bridge.

---

### SPLIT 125 -- nid 1778923627042 * Chunk 52 * HIGH
**Topic:** Methylene blue for vasoplegic syndrome -- mechanism + nursing monitoring pitfall
**Why split:** The mechanism (NOS + guanylate cyclase inhibition) and the critical nursing monitoring pitfall (pulse ox artifact) are independently testable -- confusing them could cause patient harm.

**Card A -- Methylene blue: indication and mechanism**
> **FRONT:** On the vasopressin/methylene blue chart, methylene blue treats _______ syndrome by inhibiting _______ and _______, reducing cGMP and increasing _______. Dose is _______ mg/kg IV.
>
> **BACK:** Indication: **vasoplegic syndrome** (distributive shock refractory to vasopressors -- classic settings: post-cardiac surgery/CPB, severe anaphylaxis, drug-induced). Mechanism: inhibits **NOS** (reduces NO production) AND **guanylate cyclase** (reduces cGMP) -- decreased cGMP causes vascular smooth muscle contraction -- increased SVR. Dose: **1-2 mg/kg IV** over 15-60 min; may repeat q4-6h.
> -> CCRN KEY: Vasoplegic syndrome post-cardiac surgery: CPB activates complement + endotoxin exposure + hypothermia -- massive NO release -- profound SVR drop (CI normal or elevated, MAP <65 despite high-dose NE + vasopressin). Methylene blue response: increased SVR within 1-2h, reduced vasopressor requirements in ~60-70% of cases.

**Card B -- Methylene blue: nursing monitoring pitfall and contraindication**
> **FRONT:** The critical nursing monitoring pitfall with methylene blue is _______, requiring _______ for accurate oxygen saturation. The absolute contraindication is _______.
>
> **BACK:** **Pulse oximetry reads falsely LOW** -- methylene blue dye absorbs at 668 nm, interfering with SpO2 measurement (may falsely read 65-70% despite normal saturation). Use **ABG for accurate SaO2** during methylene blue infusion. Effect lasts 30-60 min after infusion ends. Absolute contraindication: **G6PD deficiency** (causes oxidative hemolysis).
> -> CCRN KEY: Document the methylene blue infusion time in the chart so nursing staff on the next shift understand the pulse ox artifact. Expected harmless effects: urine blue-green, skin and mucosa appear cyanotic (dye) -- document at medication start to prevent alarm calls. Serotonin syndrome risk with SSRIs/MAOIs (methylene blue inhibits MAO-A).

---

### SPLIT 126 -- nid 1778923627000 * Chunk 52 * MEDIUM
**Topic:** Naloxone -- dosing and titration goal + infusion for re-narcotization prevention
**Why split:** Acute reversal dosing and titration endpoint and the infusion calculation for sustained effect test different pharmacological competencies.

**Card A -- Naloxone: dose and titration goal**
> **FRONT:** On the antidote chart, opioid toxicity is reversed with _______ at _______ mg IV every 2-3 minutes. The titration GOAL is _______ (not full reversal), because _______.
>
> **BACK:** **Naloxone (Narcan)**. Dose: **0.4-2 mg IV** every 2-3 min, titrated to **RR >12/min** (not full reversal). Reason: full reversal causes acute opioid withdrawal (agitation, hypertension, tachycardia, seizures, pulmonary edema) and may precipitate pain in patients receiving therapeutic opioids.
> -> CCRN KEY: Start at lower dose (0.04-0.1 mg IV) for opioid-dependent patients or therapeutic opioid users -- titrate cautiously to adequate respirations. Higher initial doses (1-2 mg) for heroin/illicit opioid overdose where dependency is unknown.

**Card B -- Naloxone infusion: half-life and re-narcotization prevention**
> **FRONT:** Naloxone's half-life is only _______ minutes. To prevent re-narcotization, a continuous infusion of _______ of the effective reversal dose per hour is often needed.
>
> **BACK:** Half-life: **30-90 minutes** (shorter than most opioids, especially extended-release formulations). Infusion: **2/3 of the effective reversal dose per hour** (prevents re-narcotization when the opioid outlasts naloxone). Goal: adequate respirations + spontaneous arousal, not forced reversal of analgesia.
> -> CCRN KEY: Re-narcotization risk is highest with: long-acting opioids (methadone, extended-release oxycodone, fentanyl patch), large overdose amounts, renal failure (M6G accumulation with morphine). Continuous monitoring for at least 2-3x the opioid's expected duration is required after naloxone.

---

### SPLIT 127 -- nid 1778923627009 * Chunk 52 * MEDIUM
**Topic:** Inhaled NO mechanism + methemoglobin monitoring + abrupt discontinuation risk
**Why split:** The mechanism of selective pulmonary vasodilation (drug_mechanism) and the methemoglobin monitoring requirement plus rebound hypertension risk (drug_monitoring) are independently testable safety competencies.

**Card A -- Inhaled NO: mechanism and selectivity**
> **FRONT:** The pulmonary vasodilators chart shows inhaled NO works by entering pulmonary vascular SMCs and increasing _______, causing selective pulmonary vasodilation without _______. Dose range is _______ ppm.
>
> **BACK:** iNO diffuses into pulmonary vascular smooth muscle cells -- activates guanylate cyclase -- increases **cGMP** -- vasodilation. **Selective**: NO is inactivated by hemoglobin before reaching systemic circulation -- **no systemic hypotension**. Dose: **1-40 ppm** (start 10-20 ppm; titrate to SpO2/PaO2 response).
> -> CCRN KEY: iNO indications: refractory hypoxemia in ARDS (P/F <100 despite LPV + PEEP), RV failure with pulmonary hypertension, post-cardiac surgery PH crisis. Note: multiple RCTs in ARDS show iNO improves oxygenation temporarily but does NOT improve survival -- use as bridge to ECMO or to allow time for LPV to work. Inhaled epoprostenol is a cost-effective alternative.

**Card B -- Inhaled NO: monitoring and abrupt discontinuation risk**
> **FRONT:** A critical monitoring parameter for iNO is _______, checked every _______ hours; stop if > _______. Abrupt discontinuation causes _______.
>
> **BACK:** Monitor **methemoglobin** (NO + Hgb -- metHgb) every **4-8 hours**. Stop iNO if metHgb **>5%**. Treat symptomatic metHgb: methylene blue 1-2 mg/kg IV. Abrupt discontinuation causes: **rebound pulmonary hypertension** (endogenous NO production has been suppressed -- RV afterload spikes) -- wean gradually over hours when discontinuing.
> -> CCRN KEY: Additional monitoring: NO2 (nitrogen dioxide) -- toxic byproduct when iNO reacts with O2 in ventilator circuit. Monitor with inline NO2 detector; should be <3 ppm. iNO is extremely expensive -- always have a weaning plan. When metHgb >5% -- stop immediately, give supplemental O2, consider methylene blue.

---

### SPLIT 128 -- nid 1778923627018 * Chunk 52 * MEDIUM
**Topic:** Massive PE definition + alteplase dose + heparin protocol around thrombolysis
**Why split:** Knowing what defines massive PE and the thrombolysis indication (diagnosis_criteria) and knowing the specific alteplase dose and heparin timing protocol (drug_monitoring) are independently testable.

**Card A -- Massive PE: definition and thrombolysis indication**
> **FRONT:** On the thrombolytics chart, massive PE is defined as acute PE plus _______. The thrombolysis indication requires _______.
>
> **BACK:** Massive PE = acute PE + **hemodynamic instability** (SBP <90 mmHg OR vasopressor-dependent OR cardiac arrest). Systemic thrombolysis is indicated for massive PE when: hemodynamic instability confirmed AND no absolute contraindications (prior intracranial hemorrhage, recent major surgery/trauma, active internal bleeding).
> -> CCRN KEY: Massive PE differs from submassive PE: submassive (intermediate-risk) = RV dysfunction on echo + troponin elevation WITHOUT hemodynamic instability. Submassive PE does not automatically qualify for systemic thrombolysis -- management is individualized.

**Card B -- Alteplase dose and heparin protocol for PE thrombolysis**
> **FRONT:** The standard alteplase dose for massive PE is _______ mg IV over _______ hours. Heparin should be _______ during infusion and restarted WITHOUT a bolus when aPTT < _______.
>
> **BACK:** Alteplase: **100 mg IV over 2 hours** (or 0.6 mg/kg over 15 min for cardiac arrest). **HOLD heparin** during alteplase infusion. Restart heparin WITHOUT bolus when aPTT **<80 seconds** (indicates fibrinolytic effect has waned enough to safely restart anticoagulation without excessive bleeding risk).
> -> CCRN KEY: If alteplase is given during CPR for massive PE: continue CPR during and after infusion; allow at least 60-90 min before stopping CPR to allow drug to work. Monitor for hemorrhagic complications during and after infusion (neurological changes -- stop immediately if intracranial bleed suspected).

---

### SPLIT 129 -- nid 1778973067010 * Chunk 52 * MEDIUM
**Topic:** Organophosphate antidote -- atropine titration goal + pralidoxime early administration
**Why split:** Atropine dosing/titration endpoint (drug_dose: titrate to secretions not HR) and pralidoxime rationale and timing (reversal_antidote: must be given early before AChE aging) are distinct pharmacological concepts.

**Card A -- Atropine for organophosphate toxicity: dose and titration endpoint**
> **FRONT:** On the antidote chart, organophosphate toxicity requires _______ titrated to _______ (NOT heart rate). The toxidrome is _______.
>
> **BACK:** **Atropine 2-4 mg IV every 5-10 min**; titrate to **DRY secretions** (not HR, not pupil size -- anticholinergic HR response may be absent in some poisonings). The toxidrome is **SLUDGE**: Salivation, Lacrimation, Urination, Defecation, GI cramping, Emesis (cholinergic excess from AChE inhibition -- cannot break down ACh).
> -> CCRN KEY: Large doses of atropine may be required (10s to 100s of mg) in severe organophosphate poisoning -- do not be deterred by the cumulative dose. The endpoint is dry secretions and adequate ventilation, not a specific HR target. Bronchospasm and bronchorrhea are the life-threatening components.

**Card B -- Pralidoxime (2-PAM): mechanism and why early administration is critical**
> **FRONT:** Pralidoxime (2-PAM) must be given _______ to be effective. The reason is _______. Dose is _______ g IV.
>
> **BACK:** Must give **EARLY** (within 24-48h of exposure). Reason: organophosphate causes AChE **"aging"** -- a progressive covalent bond stabilization that becomes irreversible at 24-48h. Once aged, 2-PAM cannot reactivate AChE. Dose: **1-2 g IV** (slow infusion over 15-30 min to avoid rapid infusion toxicity -- hypertension, tachycardia, muscle rigidity).
> -> CCRN KEY: Atropine + 2-PAM combination: atropine blocks muscarinic effects (secretions, bronchospasm); 2-PAM reactivates AChE to break down accumulated ACh at all receptor types. Do not delay 2-PAM waiting for diagnostic confirmation -- in suspected OP poisoning, give empirically.

---

### SPLIT 130 -- nid 1778973067110 * Chunk 52 * MEDIUM
**Topic:** APROCCHSS trial + SSC corticosteroid trigger
**Why split:** The specific trial results (APROCCHSS vs ADRENAL: why results differed) and the SSC trigger for steroids test different evidence-based reasoning.

**Card A -- APROCCHSS trial: findings and key difference from ADRENAL**
> **FRONT:** The APROCCHSS trial (NEJM 2018) used hydrocortisone 200 mg/day PLUS _______ mcg/day of _______ and showed mortality benefit: _______ % vs _______ % at 90 days.
>
> **BACK:** APROCCHSS (n=1,241): hydrocortisone 200 mg/day + **fludrocortisone 50 mcg/day** x 7 days. **Mortality: 43.0% vs 49.1%** at 90 days (p=0.03). Key difference from ADRENAL trial (which showed no mortality benefit): APROCCHSS added **fludrocortisone** (mineralocorticoid) -- the contribution of fludrocortisone to the benefit is debated.
> -> CCRN KEY: ADRENAL (NEJM 2018, n=3,800): hydrocortisone 200 mg/day alone vs placebo -- **no 90-day mortality difference**, but faster vasopressor weaning. Two major RCTs, conflicting primary outcomes -- current practice varies. SSC 2021 recommends steroids in vasopressor-dependent septic shock but does not mandate fludrocortisone.

**Card B -- SSC corticosteroid trigger in septic shock**
> **FRONT:** The SSC trigger for steroids in septic shock is NE or Epi >= _______ mcg/kg/min despite _______.
>
> **BACK:** SSC trigger: NE or Epi **>=0.25 mcg/kg/min** despite **adequate fluid resuscitation**. Some institutional protocols use a lower threshold. Cortisol testing before initiating steroids is NOT recommended by SSC 2021 -- empiric administration is the guidance.
> -> CCRN KEY: The 0.25 mcg/kg/min threshold is a guideline anchor, not an absolute rule -- some patients benefit at lower doses, particularly those with refractory hypotension or other signs of adrenal insufficiency. Clinical judgment applies; the trigger initiates steroid consideration, not a mandate.

---

### SPLIT 131 -- nid 1778973067400 * Chunk 53 * MEDIUM
**Topic:** Coagulation pathways PT/INR vs aPTT + UFH mechanism
**Why split:** Which coagulation pathway each test measures (clinical_interpretation) and the UFH mechanism and monitoring options (drug_mechanism + drug_monitoring) are distinct competencies.

**Card A -- Coagulation pathways: PT/INR vs aPTT**
> **FRONT:** On the coagulation chart, the extrinsic pathway is measured by _______ (INR) and the intrinsic pathway by _______. What triggers each pathway?
>
> **BACK:** **Extrinsic pathway (PT/INR)**: triggered by **tissue factor (factor III)** + factor VII -- tissue damage releases TF -- activates factor X. **Intrinsic pathway (aPTT)**: triggered by contact activation (XII -- XI -- IX -- X, with factor VIII as cofactor) -- activated by foreign surface contact.
> -> CCRN KEY: Both pathways converge at factor X -- forming the common pathway (X + V -- thrombin -- fibrin). A prolonged INR with normal aPTT suggests extrinsic pathway problem (warfarin, liver failure, factor VII deficiency). Prolonged aPTT with normal INR suggests intrinsic pathway problem (heparin, hemophilia A/B, lupus anticoagulant).

**Card B -- UFH mechanism and monitoring options**
> **FRONT:** UFH works by binding _______, which then inhibits factors _______ and _______. UFH monitoring options are _______ and _______.
>
> **BACK:** UFH binds **antithrombin (AT)** -- AT-UFH complex inhibits **IIa (thrombin)** and **Xa**. Monitoring options: (1) **aPTT** (most widely used, target 1.5-2.5x control); (2) **anti-Xa level** (target 0.3-0.7 IU/mL for therapeutic UFH) -- preferred in patients with lupus anticoagulant, antiphospholipid syndrome, or abnormal baseline aPTT.
> -> CCRN KEY: AUC/MIC-guided dosing is now preferred for vancomycin (not UFH -- that's aPTT). UFH monitoring by aPTT is the standard; anti-Xa is reserved for specific populations where aPTT is unreliable. Weight-based UFH nomograms improve time to therapeutic range.

---

### SPLIT 132 -- nid 1778926634000 * Chunk 54 * HIGH
**Topic:** Propofol mechanism + no analgesia + PRIS toxicity
**Why split:** Propofol's GABA-A mechanism and its lack of analgesia (drug_mechanism) and PRIS -- a specific high-dose toxicity with distinct clinical criteria (diagnosis_criteria/nursing_action) -- are independently assessable.

**Card A -- Propofol mechanism and analgesic profile**
> **FRONT:** On the sedation comparison chart, propofol works by _______ and has _______ analgesic effect. The nursing implication is _______.
>
> **BACK:** Propofol: **positive allosteric modulation of GABA-A receptor**. Has **NO analgesic effect** -- always combine with opioid or other analgesic agent for pain management. Formulation: 10% intralipid emulsion (0.1 g fat = 1.1 kcal/mL) -- account for caloric content in nutrition calculations; monitor triglycerides.
> -> CCRN KEY: Common ICU error: titrating propofol higher when the patient appears uncomfortable -- if pain is the driver of agitation, more propofol suppresses behavior without treating pain. Assess CPOT/BPS first; treat pain before escalating sedation.

**Card B -- PRIS: dose threshold, presentation, and immediate action**
> **FRONT:** Propofol has a unique toxicity at doses > _______ mg/kg/hr for > _______ hours called _______ syndrome, presenting with _______, rhabdomyolysis, and _______.
>
> **BACK:** PRIS threshold: doses **>4 mg/kg/hr** for **>48 hours**. Presentation: **lactic acidosis + rhabdomyolysis + AV conduction block (Brugada-like ECG pattern)** + lipemic plasma + renal failure. Early signs: new AG metabolic acidosis, rising lactate, elevated CK. Immediate action: **STOP propofol** -- switch to alternative sedation.
> -> CCRN KEY: Risk factors: high doses, prolonged use, young patients, low carbohydrate intake, concurrent catecholamines or corticosteroids. PRIS mortality is high when recognition is delayed -- rising CK + new metabolic acidosis in a patient on high-dose propofol = PRIS until proven otherwise.

---

### SPLIT 133 -- nid 1778926634042 * Chunk 54 * HIGH
**Topic:** Labetalol receptor profile + clinical applications
**Why split:** The receptor pharmacology (beta:alpha ratio) and the specific clinical applications including contraindications test different knowledge layers.

**Card A -- Labetalol: receptor profile and IV dosing**
> **FRONT:** On the beta-blocker chart, labetalol blocks _______ and _______ receptors. The IV beta:alpha ratio is _______, and IV dosing is _______.
>
> **BACK:** Labetalol blocks **beta1, beta2, AND alpha1** receptors. IV beta:alpha ratio = **7:1** (oral = 3:1). IV dosing: 10-20 mg IV q10-15 min (bolus) OR 2 mg/min infusion; max 300 mg total.
> -> CCRN KEY: IV labetalol is predominantly beta-blocking (7:1) -- the alpha-blocking component reduces the reflex tachycardia seen with pure vasodilators. Dual action achieves both HR reduction and BP reduction with a single agent -- advantageous in aortic dissection and preeclampsia.

**Card B -- Labetalol clinical applications and contraindications**
> **FRONT:** Labetalol is first-line for hypertensive emergency in _______ (pregnancy complication). Beta-blockers are absolutely contraindicated in _______ and relatively contraindicated in _______.
>
> **BACK:** First-line for **preeclampsia/eclampsia hypertension** (preferred over nitroprusside -- maternal/fetal safety profile). Absolute contraindication: **cardiogenic shock** (negative inotropy decreases CO in an already-failing heart). Relative contraindications: severe asthma (beta2 block causes bronchospasm), severe COPD, sick sinus syndrome, AV block >1st degree.
> -> CCRN KEY: Hypertensive emergency agent selection: aortic dissection -- esmolol + vasodilator; preeclampsia -- labetalol IV; hypertensive encephalopathy/stroke -- nicardipine or labetalol; post-CABG -- esmolol + nicardipine. Hydralazine IV is an alternative for preeclampsia when labetalol unavailable.

---

### SPLIT 134 -- nid 1778926634009 * Chunk 54 * MEDIUM
**Topic:** Azole mechanism + fluconazole spectrum + voriconazole monitoring
**Why split:** Azole mechanism and fluconazole's spectrum gaps (drug_mechanism) and voriconazole-specific clinical monitoring and drug interactions (drug_monitoring) are distinct safety competencies.

**Card A -- Azole mechanism and fluconazole spectrum**
> **FRONT:** The antifungal chart shows azoles inhibit _______, reducing ergosterol synthesis. Fluconazole covers _______ but is NOT active against _______.
>
> **BACK:** Azoles inhibit **CYP51 (lanosterol 14-alpha-demethylase)** -- reduced ergosterol synthesis -- fungal membrane disruption. Fluconazole covers: most Candida spp., Cryptococcus (step-down after AmB induction). NOT active against: **C. krusei** (intrinsically resistant), C. glabrata (variable), and invasive mold species (Aspergillus, Mucorales, Fusarium).
> -> CCRN KEY: C. krusei -- always use echinocandin or voriconazole, never fluconazole (intrinsic resistance). C. auris (emerging, often pan-resistant) -- echinocandin first-line, notify infection control. Azoles are fungistatic against Candida; echinocandins are fungicidal.

**Card B -- Voriconazole: indication, monitoring, and drug interaction**
> **FRONT:** Voriconazole is first-line for _______ and is monitored by trough level of _______. The clinically important drug interaction doubling INR is with _______.
>
> **BACK:** Voriconazole: first-line for **invasive aspergillosis** (IDSA 2016). Trough target: **1-5.5 mcg/mL** (sub-therapeutic = treatment failure; supra-therapeutic = toxicity including visual disturbances, QTc prolongation, hepatotoxicity). Drug interaction: **fluconazole + warfarin** doubles INR within 3-5 days -- reduce warfarin dose ~50% on initiation.
> -> CCRN KEY: Voriconazole monitoring parameters: trough level, visual disturbances (photopsia, color changes -- common ~30%, transient), QTc (baseline ECG + weekly monitoring), LFTs (q2 weeks), photosensitivity with prolonged use. IV voriconazole contains cyclodextrin carrier -- avoid in renal failure (use oral or switch to isavuconazole).

---

### SPLIT 135 -- nid 1778926634012 * Chunk 54 * MEDIUM
**Topic:** Echinocandin mechanism + anidulafungin (no organ dose adjustment) + IDSA recommendation
**Why split:** Class mechanism and coverage gaps and the specific agent with no dose adjustment plus IDSA first-line indication are distinct clinical knowledge points.

**Card A -- Echinocandin mechanism and spectrum gaps**
> **FRONT:** The echinocandin chart shows this class inhibits _______, disrupting the fungal cell wall. Echinocandins are NOT active against _______ and _______.
>
> **BACK:** Inhibit **beta-1,3-glucan synthase** -- reduced cell wall glucan -- osmotic lysis (fungicidal against Candida). NOT active against: **Cryptococcus neoformans** (no glucan in capsule), **Fusarium**, Mucorales, Trichosporon. Also: minimal activity against Candida parapsilosis (natural reduced susceptibility).
> -> CCRN KEY: Echinocandin class advantages in ICU: fungicidal (vs fungistatic azoles), excellent biofilm penetration (catheter-associated candidemia), minimal CYP450 drug interactions, safe in both renal AND hepatic failure (major advantage vs azoles and AmB).

**Card B -- Anidulafungin: no dose adjustment + IDSA recommendation for candidemia**
> **FRONT:** The echinocandin requiring NO dose adjustment in renal OR hepatic failure is _______. IDSA recommends echinocandins as first-line for candidemia when the patient is _______.
>
> **BACK:** **Anidulafungin** (enzymatic degradation in plasma -- no hepatic or renal metabolism; no organ adjustment needed). Loading dose: 200 mg x1, then 100 mg/day. IDSA first-line for candidemia when: **critically ill, prior azole exposure, or non-albicans Candida likely**. Step-down to fluconazole acceptable when: isolate confirmed susceptible + patient clinically improving + blood cultures negative for >=5 days.
> -> CCRN KEY: Caspofungin requires dose reduction to 35 mg/day in severe hepatic failure (Child-Pugh B-C). Anidulafungin avoids this issue entirely. Duration of candidemia treatment: 14 days from first negative blood culture plus symptom resolution (IDSA guideline).

---

### SPLIT 136 -- nid 1778926634024 * Chunk 54 * MEDIUM
**Topic:** HAP/VAP antibiotic duration + PCT stopping rule + PRORATA trial
**Why split:** The recommended antibiotic duration and PCT threshold (drug_monitoring) and the PRORATA trial evidence (clinical_trial) test different competencies -- one is the guideline, the other is the evidence behind it.

**Card A -- HAP/VAP duration and PCT stopping rule**
> **FRONT:** On the de-escalation chart, the recommended antibiotic duration for HAP/VAP is _______ days. The PCT stopping threshold is PCT < _______ mcg/mL OR reduction >= _______ % from peak.
>
> **BACK:** HAP/VAP duration: **7 days** (IDSA 2016; SHORT trial confirmed non-inferiority of shorter courses over 8-15 days). PCT stopping threshold: **<0.25 mcg/mL OR >=80% reduction** from peak -- when this is met, stopping antibiotics is supported per protocol. PCT-guided de-escalation is best validated for community-acquired pneumonia and sepsis -- less validated for VAP specifically.
> -> CCRN KEY: PCT-guided de-escalation does not mean stopping antibiotics early if the patient has not clinically improved. Clinical response (fever, WBC, oxygenation, hemodynamics) must accompany PCT trend. Always confirm with provider before de-escalating based on PCT alone.

**Card B -- PRORATA trial: PCT-guided antibiotic de-escalation**
> **FRONT:** The PRORATA trial showed PCT-guided de-escalation reduced antibiotic exposure from _______ to _______ days without _______.
>
> **BACK:** PRORATA trial: PCT-guided vs standard -- **14.3 vs 11.6 days** of antibiotic exposure (reduction of ~2.7 days). Without increasing mortality or ICU LOS. Shorter antibiotic courses reduce: C. difficile risk, antibiotic resistance selection pressure, drug toxicity, and cost.
> -> CCRN KEY: PCT trends are more clinically meaningful than single values. A PCT that is falling (even if not yet <0.25) supports continued de-escalation consideration. A PCT that is rising despite antibiotics suggests treatment failure, undrained focus, or secondary infection -- escalate.

---

### SPLIT 137 -- nid 1778939028012 * Chunk 55 * MEDIUM
**Topic:** DOSE trial -- high-dose strategy outcomes and safety
**Why split:** The efficacy finding (better decongestion) and the safety finding (no increased worsening renal function) are the two arms of the DOSE trial interpretation -- each testable independently.

**Card A -- DOSE trial: high-dose arm efficacy**
> **FRONT:** On the acute decompensated HF chart, the DOSE trial high-dose furosemide strategy (2.5x oral dose IV) resulted in _______ compared to the low-dose strategy.
>
> **BACK:** The high-dose arm resulted in **greater diuresis and symptom relief** -- better decongestion (greater weight loss, net fluid balance, self-reported symptom improvement) compared to the low-dose (1x oral dose IV) strategy. No significant difference found between bolus and continuous infusion delivery method.
> -> CCRN KEY: DOSE tested a specific high-dose strategy -- results inform clinical decision-making but do not mandate the 2.5x factor for every patient. Clinical response, renal function, hemodynamics, and prior diuretic exposure must guide individualized dosing decisions.

**Card B -- DOSE trial: safety finding regarding renal function**
> **FRONT:** The DOSE trial showed the high-dose strategy did NOT increase _______ compared to low-dose. The modest creatinine rise seen in the high-dose arm was consistent with _______.
>
> **BACK:** Did NOT increase **rates of worsening renal function** (death, need for dialysis, or Cr rise >0.3 mg/dL x2) compared to low-dose at 60-day follow-up. The modest Cr rise observed (~0.1 mg/dL) in the high-dose arm was consistent with **acceptable transient hemoconcentration** -- Cr returned toward baseline.
> -> CCRN KEY: This finding is important nursing context: a mild Cr rise during aggressive diuresis for ADHF does not automatically indicate AKI or require stopping diuretics. Clinical reassessment is required -- is the patient still congested, or are there signs of volume depletion?

---

### SPLIT 138 -- nid 1778939040009 * Chunk 56 * MEDIUM
**Topic:** Aminoglycoside nephrotoxicity monitoring + extended-interval dosing prevention
**Why split:** Recognizing the nephrotoxicity trigger (drug_monitoring: SCr rise threshold) and the prevention strategy (extended-interval dosing rationale) test distinct competencies.

**Card A -- Aminoglycoside nephrotoxicity: SCr monitoring trigger**
> **FRONT:** The nephrotoxicity monitoring chart shows aminoglycoside AKI is recognized when SCr rises _______ over 48h. Notify provider for this finding.
>
> **BACK:** SCr rise of **>=0.3 mg/dL over 48h** OR >1.5x baseline within 7 days -- consistent with AKI (KDIGO criteria). This triggers provider notification, dose reassessment, and consideration of drug level review (trough or 24h level). Aminoglycoside nephrotoxicity involves proximal tubule accumulation -- typically reversible with drug discontinuation.
> -> CCRN KEY: Document baseline SCr before starting aminoglycosides and monitor q48h or per protocol. Also monitor audiometric changes (ototoxicity risk). Trough levels (if used) should be undetectable before next dose in extended-interval dosing.

**Card B -- Extended-interval dosing: rationale for nephrotoxicity prevention**
> **FRONT:** The key prevention strategy for aminoglycoside nephrotoxicity is _______, which maximizes _______ while minimizing _______.
>
> **BACK:** **Extended-interval dosing (EID): 5-7 mg/kg q24h**. Maximizes **Cmax/MIC ratio** (concentration-dependent killing -- high peak kills bacteria most effectively) while minimizing nephrotoxicity (low trough = proximal tubular cells recover between doses, reducing intracellular accumulation).
> -> CCRN KEY: Multiple daily dosing keeps trough levels elevated -- continuous tubular exposure drives accumulation and nephrotoxicity. Extended-interval dosing with adequate washout period (trough near undetectable) reduces this risk while maintaining or improving antibacterial efficacy.

---

### SPLIT 139 -- nid 1778939040027 * Chunk 56 * MEDIUM
**Topic:** RASS targets for general ICU vs NMBA patients + mandatory monitoring
**Why split:** The RASS target for general ICU ventilated patients (PADIS guideline) and the special monitoring requirements when NMBAs eliminate behavioral assessment are distinct safety competencies.

**Card A -- RASS target for ICU ventilated patients (PADIS 2018)**
> **FRONT:** The RASS targets chart shows general ICU ventilated patients target RASS _______ per PADIS 2018 guidelines. This level is called _______ sedation.
>
> **BACK:** Target: **RASS 0 to -1** (light sedation -- awake or lightly sedated, arousable, follows commands). PADIS 2018 recommends **light sedation** as the default for most mechanically ventilated ICU patients -- associated with shorter MV duration, less delirium, and better outcomes vs deep sedation.
> -> CCRN KEY: RASS -2 to -3 may be appropriate for specific indications (severe ARDS requiring prone positioning, refractory ICP, status epilepticus). Deep sedation (RASS -4 to -5) is not the default and should require a documented indication with reassessment plan.

**Card B -- RASS targets and monitoring for NMBA patients**
> **FRONT:** Patients on NMBAs require RASS _______ with mandatory _______ monitoring. This monitoring is required because _______.
>
> **BACK:** NMBAs: RASS **-4 to -5** (deep sedation/unconsciousness). Mandatory: **BIS (Bispectral Index) monitoring (target 40-60) OR TOF monitoring** (for neuromuscular block depth). Required because: NMBAs eliminate ALL movement and behavioral pain/distress cues -- the patient **could be fully conscious and in pain without any external evidence**. BIS/TOF are the only ways to verify adequate sedation depth and block depth.
> -> CCRN KEY: Never assume a paralyzed patient is adequately sedated simply because they are not moving. NMBA use requires a dedicated, protocol-driven sedation plan (typically analgesic + sedative combination) with BIS monitoring. Document BIS values per protocol frequency (typically q1-4h).

---

### SPLIT 140 -- nid 1778939040033 * Chunk 56 * MEDIUM
**Topic:** RSBI threshold for extubation prediction + RSBI formula
**Why split:** Knowing the RSBI cutoff (clinical_trial: prediction of extubation success) and calculating RSBI from ventilator data (formula_calculation) are independently testable.

**Card A -- RSBI: extubation prediction threshold**
> **FRONT:** The SAT/SBT chart shows a spontaneous breathing trial passes when RSBI is _______, predicting successful extubation.
>
> **BACK:** RSBI < **105 breaths/min/L** predicts successful extubation (Yang & Tobin, 1991). RSBI >105 = high risk for extubation failure. RSBI is one parameter within the overall SBT assessment -- other criteria (cough strength, secretion management, mental status) must also be evaluated before extubation.
> -> CCRN KEY: RSBI has good negative predictive value (high RSBI reliably predicts failure) but modest positive predictive value (low RSBI does not guarantee success -- up to 30% of patients with RSBI <105 still fail extubation when clinical factors are not considered).

**Card B -- RSBI formula: calculation from ventilator data**
> **FRONT:** RSBI is calculated as _______ / _______ (units). Describe how to obtain both values from the ventilator at the bedside.
>
> **BACK:** RSBI = **RR (breaths/min) / Vt (liters)**. To calculate: obtain RR and Vt during 1 minute of spontaneous breathing on T-piece or low PSV. Convert Vt from mL to L (divide by 1000). Example: RR 24, Vt 350 mL = 0.35 L -- RSBI = 24/0.35 = 68 (below 105 = passes this threshold).
> -> CCRN KEY: RSBI must be measured during spontaneous breathing -- not while on controlled mandatory ventilation. Measure from the ventilator waveforms or use a spirometer during T-piece trial. Rapid shallow breathing (high RR, low Vt) = high RSBI = fatigue pattern = extubation failure risk.

---

### SPLIT 141 -- nid 1778939040042 * Chunk 56 * MEDIUM
**Topic:** Mechanical mitral valve INR target + warfarin reversal with 4F-PCC
**Why split:** INR target for a mechanical mitral valve (drug_monitoring: specific monitoring goal higher than standard) and the reversal strategy for major bleeding (reversal_antidote: 4F-PCC + Vitamin K) test different competencies.

**Card A -- Mechanical mitral valve: INR target and rationale**
> **FRONT:** The warfarin INR targets chart shows mechanical mitral valve requires INR _______ (compared to _______ for most other indications). The reason for the higher target is _______.
>
> **BACK:** Mechanical mitral valve: **INR 2.5-3.5** (higher than standard 2-3). Reason: mechanical mitral valves have higher thromboembolism risk than aortic valves due to lower flow velocity on the left atrial side -- a higher anticoagulation intensity is required to prevent valve thrombosis and systemic embolism.
> -> CCRN KEY: Mechanical aortic valve (lower risk): INR 2-3. Additional risk factors (AF, prior TE, low EF) raise the target for aortic valves too. In ICU: never hold anticoagulation for a mechanical valve without provider-directed bridging plan -- valve thrombosis is life-threatening.

**Card B -- Major warfarin bleeding reversal: 4F-PCC protocol**
> **FRONT:** Major bleeding with warfarin is reversed using _______ as first-line agent (dose _______ units/kg) PLUS _______ for sustained reversal.
>
> **BACK:** **4F-PCC (Kcentra)** as first-line: dose **25-50 units/kg** IV (based on INR at presentation -- INR >6 gets 50 units/kg). PLUS **Vitamin K 10 mg IV** (slow infusion over 30-60 min to prevent anaphylaxis) -- PCC factors last 6-12h; Vit K restores hepatic factor synthesis for sustained reversal.
> -> CCRN KEY: Without Vitamin K, INR will re-elevate as 4F-PCC factors are consumed (~6-12h). The combination (4F-PCC for immediate reversal + Vit K for sustained effect) is the standard protocol. Onset: 4F-PCC ~15 min; FFP ~1-4h + volume burden. For life-threatening ICH, prioritize speed -- 4F-PCC is the first-line choice.

---

### SPLIT 142 -- nid 1778939040039 * Chunk 56 * LOW
**Topic:** Argatroban dose reduction in hepatic failure + aPTT targets
**Why split:** The dose adjustment for hepatic failure (drug_dose) and the modified aPTT monitoring target (drug_monitoring -- lower goal because of altered pharmacokinetics) test distinct competencies even as a LOW card.

**Card A -- Argatroban: standard vs hepatic failure dose**
> **FRONT:** On the argatroban monitoring chart, hepatic failure patients require a starting dose of _______ mcg/kg/min vs the standard _______ mcg/kg/min. Why is this adjustment needed?
>
> **BACK:** Hepatic failure dose: **0.5 mcg/kg/min** (25% of standard **2 mcg/kg/min**). Argatroban is **hepatically cleared** -- in hepatic failure, reduced clearance leads to drug accumulation and excessive anticoagulation at standard doses.
> -> CCRN KEY: Argatroban is a direct thrombin inhibitor (DTI) used for: HIT (heparin-induced thrombocytopenia) when heparin must be avoided, and for percutaneous coronary intervention in HIT. Unlike bivalirudin, argatroban has primarily hepatic clearance -- adjust for liver dysfunction. Bivalirudin is renally cleared (opposite profile).

**Card B -- Argatroban aPTT monitoring targets**
> **FRONT:** The aPTT target for standard argatroban dosing is _______. For hepatic failure patients, the aPTT target is _______ because _______.
>
> **BACK:** Standard aPTT target: **1.5-3x baseline** (approximately 45-90 seconds). Hepatic failure aPTT target: **1.5-2x baseline** (lower target because the drug effect is already enhanced from reduced clearance -- targeting lower aPTT reduces over-anticoagulation and bleeding risk).
> -> CCRN KEY: Monitor aPTT 2h after initiation and after each dose adjustment; then q24h when stable. In hepatic failure: titrate slowly -- small dose changes cause larger aPTT shifts than in normal hepatic function. Document baseline aPTT (pre-argatroban) for accurate therapeutic range calculation.

