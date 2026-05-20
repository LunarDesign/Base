import re, html, sys
sys.stdout.reconfigure(encoding='utf-8')

def vis(raw):
    d = html.unescape(raw)
    s = re.sub(r'<[^>]+>', ' ', d)
    s = s.replace('\n', ' ').replace('\t', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return len(s)

daughters = {
    # NID 918063 — Trauma ABCDE Primary Survey (3 daughters)
    "918063_D1": "A = Airway + C-spine protection (jaw thrust, not head-tilt; RSI if unmaintainable) | B = Breathing — bilateral sounds; tension PTX → CLINICAL dx → needle decompression 2nd ICS midclavicular immediately, no imaging first | C = Circulation — 2 large-bore IVs or IO; type/cross; hemorrhage control",
    "918063_D2": "D = Disability — AVPU/GCS; pupils; blood glucose (reversible ↓LOC) | E = Exposure + warmth — fully undress; warm blankets + warm IVFs | Triad of Death: hypothermia + coagulopathy + acidosis — interlinked; hypothermia impairs clotting → ↑hemorrhage → ↑acidosis; unbroken triad often fatal",
    "918063_D3": "Hemorrhage control (direct pressure, tourniquet, wound packing) BEFORE IV fluids — fluids without source control dilute clotting factors → worsens coagulopathy → more bleeding. Control the source first; then replace what was lost.",

    # NID 918066 — Hemorrhagic Shock Classes + Permissive Hypotension (3 daughters)
    "918066_D1": "Class I: ≤750 mL (<15%); HR <100; BP normal; fully compensated | Class III: 1500–2000 mL (30–40%); HR >120; BP ↓ (systolic falls — compensation failing); confusion, ↓UO; transfusion required | Class IV: >2000 mL (>40%); HR >140; SURVIVAL REQUIRES IMMEDIATE SURGICAL HEMORRHAGE CONTROL",
    "918066_D2": "Tachycardia = first compensation for ↓SV (CO = SV × HR) | Class II: 750–1500 mL; HR 100–120; BP stays normal (tachycardia + vasoconstriction compensate) | HR 110 + normal BP = ~1000 mL lost, Class II — deceptively stable; prepare MTP + blood products + OR notification before BP falls",
    "918066_D3": "Permissive hypotension: SBP 80–90 mmHg (not 120) until surgical hemorrhage control | Rationale: ↑BP → ↑hydrostatic pressure at bleeding site → clot shear + dilutes clotting factors | Exceptions: TBI (CPP ≥60); elderly; penetrating cardiac injury; blunt multi-organ trauma",

    # NID 918072 — Rhabdomyolysis (3 daughters)
    "918072_D1": "Massive skeletal muscle destruction releasing intracellular contents (myoglobin, CK, K⁺, phosphate, uric acid) into systemic circulation | CK >5,000–10,000 U/L = significant; CK >100,000 U/L = severe AKI risk",
    "918072_D2": "Clinical triad: myalgia (diffuse/focal) + profound weakness + dark brown urine (cola-colored myoglobinuria) | AKI mechanism: myoglobin precipitates at acidic pH → tubular toxicity (iron-mediated free radical injury); myoglobin → afferent arteriolar vasoconstriction → ↓GFR",
    "918072_D3": "UO target 200–300 mL/hr (5–8× standard 0.5 mL/kg/hr) — high flow flushes myoglobin before precipitation | IVF: NS or LR at 1–1.5 L/hr initially; titrate to UO target | K⁺ q4–6h — muscle rupture releases intracellular K⁺ rapidly; K⁺ >6.5 + ECG changes = cardiac emergency",

    # NID 692068 — DCR Steps 1-2 (2 daughters)
    "692068_D1": "Step 1: HEMORRHAGE CONTROL before IV fluids — direct pressure, wound packing (hemostatic gauze), tourniquet for extremity hemorrhage | Rationale: fluids before source control dilute clotting factors → worsens coagulopathy → ↑bleeding. Stop the source first; replace volume after.",
    "692068_D2": "Step 2: PERMISSIVE HYPOTENSION — SBP 80–90 mmHg until surgical hemorrhage control | Rationale: ↑BP → ↑hydrostatic pressure at bleeding site → clot dislodgement + clotting factor dilution | Exceptions: TBI (CPP ≥60); elderly; penetrating cardiac injury; blunt multi-organ trauma",

    # NID 692071 — DCR Full Synthesis (3 daughters)
    "692071_D1": "Step 1: Hemorrhage control (direct pressure/tourniquet/packing) before IV fluids — prevents clotting factor dilution and clot dislodgement | Step 2: Permissive hypotension SBP 80–90 mmHg until surgical control — reduces hydrostatic pressure on forming clots | Exception: TBI (CPP ≥60)",
    "692071_D2": "Step 3: MTP 1:1:1 (pRBC:FFP:platelets) + TXA 1000 mg IV within 3 HOURS of injury — antifibrinolytic (inhibits plasminogen activation, stabilizes forming clots) | TXA after 3h: ↑mortality — fibrinolysis has served its protective role; late TXA prevents normal fibrinolysis → ↑thrombotic risk",
    "692071_D3": "Step 4: DEFINITIVE SURGICAL HEMORRHAGE CONTROL — only intervention that stops the bleeding; steps 1–3 are bridges | Minimize crystalloid: large-volume NS/LR dilutes clotting factors → consumptive coagulopathy; blood products provide volume AND clotting factors",

    # NID 755998 — Hemorrhagic Shock Class Thresholds (2 daughters)
    "755998_D1": "Class I: ≤750 mL (<15%); HR normal/<100; BP normal; fully compensated | Class II: 750–1500 mL (15–30%); HR 100–120; BP normal/slightly ↓ | Earliest distinguishing sign: TACHYCARDIA — HR rises first as CO drops (CO = SV × HR); tachycardia + vasoconstriction maintain normal BP through Class II",
    "755998_D2": "Class II→III threshold: SBP BEGINS TO FALL — blood loss 1500–2000 mL; HR >120; compensation failing; blood products urgently needed, crystalloid alone insufficient | Class III→IV: >2000 mL; hemodynamic collapse; HR >140; SURVIVAL REQUIRES IMMEDIATE SURGICAL HEMORRHAGE CONTROL",
}

all_ok = True
for label, back in daughters.items():
    c = vis(back)
    status = "OK" if c <= 300 else f"OVER by {c - 300}"
    if c > 300:
        all_ok = False
    print(f"{label}: {c} chars [{status}]")

print()
print("ALL OK" if all_ok else "SOME OVER LIMIT - FIX BEFORE ADDING")
