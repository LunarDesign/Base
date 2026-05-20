import re, html, sys
sys.stdout.reconfigure(encoding='utf-8')

def vis(raw):
    d = html.unescape(raw)
    s = re.sub(r'<[^>]+>', ' ', d)
    s = s.replace('\n', ' ').replace('\t', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return len(s)

proposed = {
    "729_proposed": "Primary (ABCDE): A: Airway; C-spine protection | B: Breathing | C: Circulation — 2 large-bore IVs + warmed LR | D: Disability — neuro screen | E: Expose + warmth; remove clothing | Secondary (FGHI): F: Full vitals + family | G: Pain control | H: History | I: Inspect posterior — log-roll",
    "763_proposed": "widened QRS >100 ms (Na⁺ channel blockade) | sodium bicarbonate 1–2 mEq/kg IV bolus until QRS narrows → CCRN KEY: Bicarb alkalinizes blood (protein-binding of TCA ↑ at higher pH) and provides Na⁺ loading. QRS >160 ms = VF risk. Also: hypotension (α-blockade), anticholinergic toxidrome, seizures.",
}

for label, back in proposed.items():
    c = vis(back)
    status = "OK" if c <= 300 else "OVER"
    print(f"{label}: {c} chars [{status}]")
