"""
Persistent daughter card verify script.
Usage: populate DAUGHTERS dict, run, check output.
Reuse this file for every split batch — just replace the dict contents.

Each entry: "label": {"back": "...", "tier": "tier-critical|tier-high|tier-low", "parent_nid": 12345}

Checks:
  - Visible char count <= 300
  - TierClass matches declared parent tier (catches copy-paste tier errors)
  - Prints summary: OK / OVER / TIER MISMATCH
"""

import re, html, sys
sys.stdout.reconfigure(encoding='utf-8')

def vis(raw):
    d = html.unescape(raw)
    s = re.sub(r'<[^>]+>', ' ', d)
    s = s.replace('\n', ' ').replace('\t', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return len(s)

# --- POPULATE THIS FOR EACH BATCH ---
# Format: "label": {"back": "...", "tier": "tier-critical", "parent_nid": NID}
DAUGHTERS = {
    # NID 1778381918069 — Compartment Syndrome SOURCE-UPDATED SPLIT (3 daughters)
    # Changes: delta pressure formula removed (not in Juarez/Burns); "4-6 hours" → "emergent" (Juarez p.810)
    "918069_D1": {
        "back": "Pressure >30 mmHg (normal 0–8 mmHg) → emergent decompressive fasciotomy | PAIN WITH PASSIVE STRETCH — extend fingers/toes → severe compartment pain before Doppler pulse loss; only finding present before objective pressure threshold | Loss of pulse/pallor = LATE signs; unreliable for early detection",
        "tier": "tier-critical",
        "parent_nid": 1778381918069,
    },
    "918069_D2": {
        "back": "VA ECMO femoral cannula → limb ischemia (distal perfusion cannula) | Massive fluid resuscitation → abdominal compartment syndrome (bladder pressure monitoring) | Causes: crush injury, fracture, reperfusion after embolectomy, constricting casts | Fasciotomy restores perfusion; prevents rhabdomyolysis",
        "tier": "tier-critical",
        "parent_nid": 1778381918069,
    },
    "918069_D3": {
        "back": "Delayed fasciotomy → muscle necrosis → myoglobin + CK + K⁺ released → rhabdomyolysis → AKI → fatal hyperkalemia | CCRN KEY: pain out of proportion = escalate IMMEDIATELY; most common error: escalating opioids while delaying compartment pressure check; trust the pain before the objective exam",
        "tier": "tier-critical",
        "parent_nid": 1778381918069,
    },
}

# --- VALIDATION ---
VALID_TIERS = {"tier-critical", "tier-high", "tier-low"}
errors = []
all_ok = True

if not DAUGHTERS:
    print("DAUGHTERS dict is empty — populate it before running.")
    sys.exit(0)

print(f"{'Label':<20} {'Chars':>6}  {'Tier':<14}  Status")
print("-" * 62)

for label, d in DAUGHTERS.items():
    back = d.get("back", "")
    tier = d.get("tier", "")
    parent = d.get("parent_nid", "?")

    c = vis(back)
    char_ok = c <= 300
    tier_ok = tier in VALID_TIERS

    issues = []
    if not char_ok:
        issues.append(f"OVER by {c - 300}")
    if not tier_ok:
        issues.append(f"UNKNOWN TIER '{tier}'")

    status = "OK" if not issues else " | ".join(issues)
    if issues:
        all_ok = False
        errors.append(label)

    print(f"{label:<20} {c:>6}  {tier:<14}  {status}")

print()
if all_ok:
    print(f"ALL {len(DAUGHTERS)} daughters OK — safe to add_notes.")
else:
    print(f"ERRORS in: {', '.join(errors)} — fix before add_notes.")
