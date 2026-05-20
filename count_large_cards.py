import re, html

def vis(raw):
    d = html.unescape(raw)
    s = re.sub(r'<[^>]+>', ' ', d)
    s = s.replace('\n', ' ').replace('\t', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return len(s), s

backs = {
    1778381918063: r"""A = AIRWAY with cervical spine protection (blunt trauma until C-spine cleared) — assess patency; jaw thrust (NOT head-tilt with C-spine concern); suction; definitive airway (RSI) if not maintainable
| B = BREATHING (ventilation, not just airway) — bilateral breath sounds; inspect for asymmetry, tracheal deviation; tension pneumothorax (absent unilateral breath sounds + tracheal deviation AWAY from affected side + JVD + hemodynamic collapse) → CLINICAL diagnosis → needle decompression 2nd ICS midclavicular line IMMEDIATELY without imaging
| C = CIRCULATION with hemorrhage control — BP, HR, skin; IV access ×2 large bore or IO; type and crossmatch; control external bleeding
| D = DISABILITY — AVPU or GCS; pupils; blood glucose (rapidly reversible cause of ↓ LOC)
| E = EXPOSURE (fully undress to identify ALL injuries including posterior thorax, axillae, perineum) + TEMPERATURE CONTROL (warm blankets, warm IV fluids immediately after exposure)
| Preventing HYPOTHERMIA because hypothermia + coagulopathy + acidosis = TRAUMA TRIAD OF DEATH — each worsens the others: hypothermia impairs clotting factor enzyme function → worsening coagulopathy → more hemorrhage → more lactic acidosis → more hypothermia. Unbroken triad is often fatal.
| HEMORRHAGE CONTROL (direct pressure, tourniquet, wound packing) BEFORE IV fluid resuscitation — control the source of blood loss first; fluid given without source control dilutes clotting factors and delays definitive hemostasis
→ CCRN KEY: Tension pneumothorax is a CLINICAL diagnosis requiring immediate treatment without imaging. The patient will die in 2-3 minutes without needle decompression. Classic triad: unilateral absent breath sounds + tracheal deviation away from the affected side + hemodynamic collapse. Treat first, confirm later.
→ MASTERY NOTE: The primary survey is a 5-minute life-threats-only assessment — not a comprehensive history or detailed physical exam. Each letter identifies ONE immediate threat and ONE intervention. Everything else waits until ABCDE is completed. The nurse who stops to document, ask history, or prepare medications before completing the primary survey is delaying life-saving identification of the next immediate threat.
→ Layer: Ph3 | Trauma Primary Survey""",

    1778381918066: r"""Class I: up to 750 mL (<15% blood volume) | HR: normal to <100 | BP: normal | minimal findings (mild anxiety; fully compensated)
| Class III: 1500-2000 mL (30-40% blood volume) | HR: >120 bpm | BP: ↓ (systolic beginning to fall — compensation failing) | confusion, tachypnea, low urine output; blood transfusion typically required
| Class IV: blood loss >2000 mL (>40%) | SURVIVAL REQUIRES IMMEDIATE SURGICAL OR INTERVENTIONAL HEMORRHAGE CONTROL — no amount of fluid resuscitation sustains life without stopping the source; HR >140, BP severely ↓, altered consciousness, no UO
| TACHYCARDIA — HR rises as the first compensation for falling stroke volume (HR increases to maintain CO = SV × HR). A trauma patient with HR 110 and "normal" BP has likely lost ~1000 mL and is in Class II. BP remains normal through Class II because tachycardia + vasoconstriction compensate.
| SBP 80-90 mmHg (not normal 120 mmHg) until surgical hemorrhage control is achieved | aggressively normalizing BP with fluids before surgical control: (1) dilutes clotting factors → worsens coagulopathy; (2) ↑ hydrostatic pressure at the bleeding site → ↑ clot shear → ↑ ongoing hemorrhage; (3) delays operative intervention by giving the appearance of stabilization
→ CCRN KEY: "Don't be fooled by a normal blood pressure." Tachycardia with normal BP in a trauma patient = active compensation for hemorrhage (Class I-II). The class transition from II to III (when BP begins to fall) represents compensatory mechanism failure — this is the urgent window before decompensation. The nurse who identifies Class II and prepares for Class III (MTP activation, blood products ready, OR notification) is practicing expert anticipatory care.
→ MASTERY NOTE: Permissive hypotension is only appropriate in the PREHOSPITAL or early in-hospital phase with UNCONTROLLED hemorrhage and PENETRATING trauma. After surgical control of hemorrhage, MAP is normalized. Permissive hypotension is NOT used in TBI (must maintain CPP ≥60) or in blunt trauma with multi-organ involvement where hypotension may cause end-organ injury.
→ Layer: Ph3 | Hemorrhagic Shock""",

    1778381918069: r"""Compartment pressure >30 mmHg | delta pressure <30 mmHg (more physiologically relevant — if diastolic is 50 and compartment pressure is 35, delta = 15 → ischemia despite absolute pressure <30)
| FASCIOTOMY — surgical release of all compartment fasciae of the affected limb | within 4-6 hours of pressure elevation (delay → irreversible muscle necrosis → rhabdomyolysis → AKI → permanent disability or limb loss)
| PAIN WITH PASSIVE STRETCH of the muscles within the compartment — gently extend the fingers or toes in a suspected tibial compartment → severe pain in the compartment even before Doppler pulse loss. This is the only finding that can be present before objective pressure thresholds are crossed.
| VA ECMO femoral arterial cannula causing ipsilateral limb ischemia (prevented by distal perfusion cannula — Chunk 11) | Massive fluid resuscitation causing ABDOMINAL compartment syndrome (prevented by bladder pressure monitoring — Chunk 06) | Also: traumatic fracture, crush injury, reperfusion after arterial embolectomy, circumferential casts
| Delayed or incomplete fasciotomy → ischemic muscle necrosis → myoglobin + CK + K+ released into circulation → RHABDOMYOLYSIS → AKI → potentially fatal hyperkalemia. The preventive cascade: recognize compartment syndrome → emergent fasciotomy → prevents rhabdomyolysis → prevents AKI → prevents hyperkalemia.
→ CCRN KEY: The 4-6 hour fasciotomy window is absolute. The nurse who identifies pain out of proportion and escalates immediately (NOT the next morning, NOT at the next rounding) is preventing permanent disability or limb loss. The most common nursing error in compartment syndrome: treating pain with escalating opioids while delaying the compartment pressure check.
→ MASTERY NOTE: The "pain out of proportion to exam" teaching applies to THREE ischemic compartment emergencies in this deck: (1) mesenteric ischemia — Chunk 06; (2) compartment syndrome — this card; (3) by analogy, aortic dissection. In all three: the subjective pain severity vastly exceeds what the objective examination reveals, because the ischemia is in structures that don't produce surface peritoneal or inflammatory signs early. Trusting the pain before the exam is the clinical skill.
→ Layer: Ph3 | Compartment Syndrome""",

    1778381918072: r"""Massive skeletal muscle cell destruction releasing intracellular contents (myoglobin, CK, potassium, phosphate, uric acid) into systemic circulation
| CK >5,000-10,000 U/L (significant); >100,000 U/L (severe AKI risk)
| MYALGIA (diffuse or focal muscle pain) | PROFOUND WEAKNESS (may be unable to ambulate) | DARK BROWN URINE ("cola-colored" or "tea-colored" myoglobinuria — often the presenting complaint)
| Myoglobin precipitates in renal tubules at acidic pH → direct tubular toxicity via iron-mediated free radical injury; myoglobin causes afferent arteriolar vasoconstriction → ↓ GFR; hyperkalemia and hyperphosphatemia from muscle release → additional renal injury
| 200-300 mL/hr (significantly HIGHER than standard ICU target of 0.5 mL/kg/hr ≈ 35 mL/hr) | High urine flow flushes myoglobin through renal tubules before it can precipitate → requires aggressive IV hydration at 1-1.5 L/hr initially (NS or LR), titrated to the high UO target
| POTASSIUM — massive muscle cell rupture releases intracellular K+ → potentially fatal hyperkalemia rapidly (K+ >6.5 mEq/L + ECG changes = cardiac emergency). Also: phosphate (↑ hyperphosphatemia → binds calcium → hypocalcemia → tetany and cardiac dysfunction). Check electrolytes q4-6h.
→ CCRN KEY: Hyperkalemia from rhabdomyolysis can cause cardiac arrest before AKI is apparent on creatinine — creatinine takes 24-48h to rise significantly from baseline. K+ rises IMMEDIATELY from muscle release. A patient with massive muscle injury needs K+ monitoring hourly in the first 4-6h, not just daily.
→ MASTERY NOTE: Rhabdomyolysis urine output target (200-300 mL/hr) is 5-8× the standard ICU target. The nurse who "protects the kidneys" by limiting fluids in a rhabdomyolysis patient to avoid "giving too much" will inadvertently cause preventable AKI. High-flow flushing is the mechanism that prevents myoglobin precipitation — the target is deliberately high and must be maintained with IV hydration, not achieved by the patient's baseline intake.
→ Layer: Ph3 | Rhabdomyolysis""",

    1778436692068: r"""STEP 1: HEMORRHAGE CONTROL — before IV fluid resuscitation. Direct pressure, wound packing with hemostatic gauze (QuikClot, Combat Gauze), tourniquet for extremity hemorrhage.
| Rationale: giving fluid before source control dilutes clotting factors faster than it replaces volume → worsens coagulopathy → more bleeding from the same site. The hemorrhage must be stopped or controlled FIRST, then fluid is given to replace what was already lost.
| Step 2: PERMISSIVE HYPOTENSION — target SBP 80–90 mmHg (NOT the normal 120 mmHg) until surgical hemorrhage control is achieved
| Rationale: aggressive BP normalization with fluids → ↑ hydrostatic pressure at the bleeding vessel → dislodges forming clots → ↑ hemorrhage rate. Also: high-volume crystalloid → dilutes clotting factors → consumptive coagulopathy worsens.
| EXCEPTIONS (do NOT use permissive hypotension): TBI (must maintain CPP ≥60 mmHg — MAP ≥65–70 + ICP-based calculation); elderly with less cardiovascular reserve; penetrating cardiac injury (very short transport to OR acceptable); blunt trauma with multi-organ involvement
→ CCRN KEY: The permissive hypotension target (SBP 80–90) is a TEMPORIZING measure during the window between injury and surgical hemorrhage control — not a long-term strategy. Once the bleeding vessel is ligated or packed, MAP is normalized.
→ MASTERY NOTE: Damage control resuscitation (DCR) replaced the older aggressive crystalloid approach. The PROPPR trial validated the 1:1:1 blood product ratio. CRASH-2 validated TXA within 3 hours. DCR is the synthesis: hemorrhage control + permissive hypotension + balanced blood product resuscitation + TXA + early surgical control = the current standard.""",

    1778436692071: r"""Step 1: HEMORRHAGE CONTROL (direct pressure, tourniquet, wound packing) — before any IV fluid; prevents coagulation factor dilution and clot dislodgement
| Step 2: PERMISSIVE HYPOTENSION — SBP 80–90 mmHg until surgical control; reduces hydrostatic pressure on forming clots; exception: TBI (need CPP ≥60)
| Step 3: MTP (Massive Transfusion Protocol) 1:1:1 ratio (pRBC:FFP:platelets) + TXA (tranexamic acid) 1000 mg IV loading dose within 3 HOURS of injury (mechanism: antifibrinolytic — inhibits plasminogen activation, stabilizes forming clots). After 3h: TXA ↑ mortality (fibrinolysis has already served its protective purpose)
| Step 4: DEFINITIVE SURGICAL HEMORRHAGE CONTROL — the only intervention that actually stops the bleeding. Steps 1–3 are bridges. The surgeon ligates, repairs, or packs the bleeding source. Without this, the patient dies regardless of resuscitation quality.
| MINIMIZE CRYSTALLOID — large-volume NS or LR dilutes clotting factors → consumptive coagulopathy → vicious cycle. Goal: minimal crystalloid until hemorrhage is controlled; blood products provide the volume AND the clotting factors.
→ CCRN KEY: TXA 3-hour window is absolute. After 3 hours, fibrinolysis has already completed its protective role (clearing microthrombi); TXA at this point prevents normal fibrinolysis → ↑ thrombotic risk → ↑ mortality. This is one of the clearest time-dependent drug administration rules in trauma.
→ MASTERY NOTE: DCR is conceptually the trauma analog of time-sensitive reperfusion therapy in STEMI and stroke: there is a window, a specific intervention, and a biological rationale for urgency. The nurse's role: activate MTP early (don't wait for lab confirmation of coagulopathy), prepare blood products, administer TXA within the window, monitor the trauma triad (hypothermia, acidosis, coagulopathy) and communicate trends.""",

    1778437755998: r"""Class I / II threshold: Class I ≤750 mL (<15% blood volume), HR normal to <100, BP normal. Class II 750–1500 mL (15–30%), HR 100–120, BP normal/slightly decreased. Earliest distinguishing sign: TACHYCARDIA — HR is the first vital sign to rise as cardiac output drops with hemorrhage (baroreceptor reflex increases HR to maintain CO = SV × HR). BP stays normal through Class II because tachycardia + vasoconstriction compensate.
| Class II / III threshold: Class III begins when SYSTOLIC BLOOD PRESSURE BEGINS TO FALL — blood loss 1500–2000 mL (30–40%), HR >120. The BP drop marks the failure of compensatory mechanisms (tachycardia and vasoconstriction are now insufficient to maintain pressure). This is the inflection where blood products are urgently needed — crystalloid alone is no longer adequate.
| Class III / IV threshold: Class IV defined by blood loss >2000 mL (>40%) with life-threatening hemodynamic collapse — HR >140, BP severely decreased, altered consciousness. The defining clinical feature: SURVIVAL REQUIRES IMMEDIATE SURGICAL OR INTERVENTIONAL HEMORRHAGE CONTROL. No amount of resuscitation fluid sustains life without stopping the source.
→ CCRN KEY: The Class II→III transition (BP begins to fall) is the most critical and most testable inflection in the hemorrhagic shock classification. A HR of 110 with normal BP is Class II — this is the deceptively stable patient who is actively hemorrhaging and needs immediate action (large-bore access, type/cross, prepare MTP) before they deteriorate to Class III.
→ MASTERY NOTE: Class I-II hemorrhage can be missed because the vital signs appear acceptable. The compensatory physiology (tachycardia + vasoconstriction) masks the volume deficit. HR is the only reliable early indicator. A trauma patient with HR 108 and "normal" BP has lost approximately 1000 mL — they are in Class II and deteriorating if not controlled.""",
}

import sys
sys.stdout.reconfigure(encoding='utf-8')

for nid, back in backs.items():
    count, plain = vis(back)
    print(f"NID {nid}: {count} chars")
