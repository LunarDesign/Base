#!/usr/bin/env python3
"""
audit_typeb.py — Full audit of chart cards in 57.apkg for multi-domain overload.

Standard: one card should test ONE clinical domain.
Flags cards that mix independent domains (diagnosis, mechanism, drug dose,
monitoring, nursing role, biomarker kinetics, trial evidence, next step, etc.)

Output: audit_typeb_report.txt
"""
import os, re, sys, sqlite3, zipfile, shutil, tempfile
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

CARDS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC   = os.path.join(CARDS_DIR, 'CCRN_PCCN_Mastery_v7_final_57.apkg')
WORK  = os.path.join(tempfile.gettempdir(), 'audit57')
OUT   = os.path.join(CARDS_DIR, 'audit_typeb_report.txt')
SEP   = '\x1f'

# ── domain detectors ───────────────────────────────────────────────────────
# Each domain is (label, [regex patterns]).  A card is credited with a domain
# if ANY of its patterns match the front text (case-insensitive).

DOMAINS = [
    ('clinical_trial',
     [r'\b(trial|NEJM|Lancet|study|RCT|n=\d|p=0\.)',
      r'\b(ADRENAL|APROCCHSS|DEXA.ARDS|RECOVERY|CATS|VASST|SOAP|MENDS|MIDEX'
      r'|ARMA|PROSEVA|PEITHO|MERINO|ZEPHyR|PRORATA|ATHOS|CONFIRM|IABP.SHOCK'
      r'|RENAL|ATN|SMART|CLASSIC|STARRT|RECOVER)\b']),

    ('drug_dose',
     [r'\d+[\.\d]*\s*(mg|mcg|g|units?|mEq|mL)\s*(IV|PO|SQ|IM|/kg|/min|/hr|/day)',
      r'dose\s+of\s+\w',
      r'(loading|infusion|bolus|drip)\s+(dose|rate)',
      r'titrat\w+\s+to']),

    ('drug_mechanism',
     [r'\b(mechanism|works by|inhibit[s]?|activat[es]+|receptor|pathway|blocks?|binds?'
      r'|agonist|antagonist|substrate|synthase|reductase|oxidase|kinase)\b']),

    ('drug_monitoring',
     [r'\b(trough|AUC|anti.Xa|aPTT|INR|level[s]?|check every|q\d+h|monitor\w*'
      r'|target.*mcg|target.*mg|target.*mEq|target.*mmHg)\b']),

    ('biomarker_kinetics',
     [r'\b(rises?|peaks?|returns? to normal|half.life|t½|sensitivity|specificity'
      r'|elevat\w+|troponin.*hour|BNP.*pg|procalcitonin|lactate.*clear)\b']),

    ('diagnosis_criteria',
     [r'\b(diagnosis|classified as|is defined as|Berlin|criteria|staging|KDIGO'
      r'|SOFA|qSOFA|CAM.ICU|RASS|GCS|score of|Stage [123])\b']),

    ('nursing_action',
     [r'\b(nursing|nurse |priority|hold\s+(all|heparin|sedation)|notify|document'
      r'|monitor for|immediately|intervention|bedside|reassess)\b']),

    ('next_step_workup',
     [r'\b(next step|initial test|best test|diagnostic workup|before\s+(endoscopy'
      r'|surgery|intubation)|confirm\w*\s+with|workup|order)\b']),

    ('pathophysiology_rationale',
     [r'\bbecause\b.*\b(cause[sd]?|lead[s]? to|result[s]? in|result\w*|trigger|impair|worsen)\b',
      r'\bwhy\b.*\b(cause[sd]?|lead|result|trigger)\b',
      r'\b(pathophysiology|mechanism of|why does|leads to|result[s]? in)\b']),

    ('clinical_interpretation',
     [r'\b(indicates?|suggests?|consistent with|interpret|diagnos\w+|confirms?'
      r'|pattern match\w*|reading the chart|the chart shows?)\b']),

    ('reversal_antidote',
     [r'\b(reverse[sd]?|reversal|antidote|counteract|neutralize|antagonize)\b']),

    ('formula_calculation',
     [r'[A-Z]{2,6}\s*=\s*[\(\d_]',           # SVR = (__, PVR = __
      r'÷|×\s*80',                             # formula operators
      r'(Vt|FiO2|PaO2|Pplat|PEEP|MAP|CVP|CO)\s*/\s*\(',
      r'calculated\s+as|formula\s+is']),
]

# Patterns that strongly suggest two SEPARATE subjects in one front.
MULTI_SUBJECT = [
    # Two distinct drug names separated by "PLUS", "AND", or a period
    r'(?i)(hydroxocobalamin|atropine|pralidoxime|naloxone|NAC|fomepizole'
    r'|idarucizumab|andexanet|protamine|TXA|flumazenil)\b.{10,200}'
    r'(hydroxocobalamin|atropine|pralidoxime|naloxone|NAC|fomepizole'
    r'|idarucizumab|andexanet|protamine|TXA|flumazenil)\b',

    # Two distinct clinical trials in one front
    r'(?i)(ADRENAL|DEXA.ARDS|RECOVERY|CATS|PROSEVA|PEITHO|MERINO|ZEPHyR'
    r'|ARMA|MENDS|MIDEX|IABP.SHOCK|VASST|SOAP.II|CONFIRM|ATHOS).{10,300}'
    r'(ADRENAL|DEXA.ARDS|RECOVERY|CATS|PROSEVA|PEITHO|MERINO|ZEPHyR'
    r'|ARMA|MENDS|MIDEX|IABP.SHOCK|VASST|SOAP.II|CONFIRM|ATHOS)',

    # "Drug A ... Drug B" — two vasopressors/sedatives tested separately
    r'(?i)(norepinephrine|epinephrine|vasopressin|dopamine|dobutamine|milrinone'
    r'|phenylephrine|angiotensin)\b.{20,300}'
    r'(norepinephrine|epinephrine|vasopressin|dopamine|dobutamine|milrinone'
    r'|phenylephrine|angiotensin)\b',

    r'(?i)(propofol|midazolam|dexmedetomidine|ketamine|lorazepam|fentanyl'
    r'|morphine|hydromorphone)\b.{20,300}'
    r'(propofol|midazolam|dexmedetomidine|ketamine|lorazepam|fentanyl'
    r'|morphine|hydromorphone)\b',
]

# ── scoring ────────────────────────────────────────────────────────────────
def count_blanks(text):
    return text.count('_______')

def detect_domains(front):
    """Return list of domain labels present in the front text."""
    found = []
    fl = front.lower()
    for label, patterns in DOMAINS:
        for pat in patterns:
            if re.search(pat, front, re.IGNORECASE):
                found.append(label)
                break
    return found

def has_multi_subject(front):
    for pat in MULTI_SUBJECT:
        if re.search(pat, front):
            return True
    return False

def severity(domains, blanks, multi_sub):
    """
    HIGH   — 3+ independent domains, or multi-subject card, or 7+ blanks
    MEDIUM — 2 domains from clearly different categories
    LOW    — 2 domains but tightly coupled (e.g., dose + monitoring same drug)
    OK     — 1 domain or all domains tightly coupled
    """
    tight_pairs = {
        frozenset(['drug_dose', 'drug_monitoring']),
        frozenset(['drug_mechanism', 'drug_dose']),
        frozenset(['formula_calculation', 'clinical_interpretation']),
        frozenset(['diagnosis_criteria', 'clinical_interpretation']),
        frozenset(['drug_mechanism', 'reversal_antidote']),
    }
    n = len(domains)
    if multi_sub or blanks >= 7 or n >= 4:
        return 'HIGH'
    if n >= 3:
        return 'HIGH'
    if n == 2:
        pair = frozenset(domains[:2])
        if pair in tight_pairs:
            return 'LOW'
        return 'MEDIUM'
    return 'OK'


# ── apkg helpers ───────────────────────────────────────────────────────────
def unpack(src, work):
    if os.path.exists(work):
        shutil.rmtree(work)
    os.makedirs(work)
    with zipfile.ZipFile(src) as z:
        z.extractall(work)


def get_chunk(tags):
    m = re.search(r'chunk-(\d+)', tags)
    return int(m.group(1)) if m else 0


def get_ltag(tags):
    m = re.search(r'(chart-l\d)', tags)
    return m.group(1) if m else 'chart-??'


# ── main ───────────────────────────────────────────────────────────────────
def main():
    print(f"Unpacking {os.path.basename(SRC)}…")
    unpack(SRC, WORK)
    db = sqlite3.connect(os.path.join(WORK, 'collection.anki2'))

    # Pull all chart cards (tagged chart-l1/l2/l3)
    rows = db.execute(
        "SELECT tags, flds FROM notes WHERE tags LIKE '%chart-l%'"
    ).fetchall()
    db.close()
    shutil.rmtree(WORK)

    print(f"Loaded {len(rows)} chart notes. Analyzing…\n")

    # Group by chunk
    by_chunk = defaultdict(list)
    for tags, flds in rows:
        fields = flds.split(SEP)
        front  = fields[0] if fields else ''
        # strip html tags for analysis
        front_plain = re.sub(r'<[^>]+>', '', front)
        chunk  = get_chunk(tags)
        ltag   = get_ltag(tags)
        blanks = count_blanks(front_plain)
        doms   = detect_domains(front_plain)
        multi  = has_multi_subject(front_plain)
        sev    = severity(doms, blanks, multi)
        by_chunk[chunk].append({
            'ltag':    ltag,
            'blanks':  blanks,
            'domains': doms,
            'multi':   multi,
            'severity':sev,
            'front':   front_plain.strip(),
        })

    # Sort each chunk by severity (HIGH > MEDIUM > LOW > OK)
    SEV_ORDER = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2, 'OK': 3}
    for chunk in by_chunk:
        by_chunk[chunk].sort(key=lambda c: SEV_ORDER[c['severity']])

    # ── write report ───────────────────────────────────────────────────────
    lines = []
    lines.append('TYPE-B MULTI-DOMAIN AUDIT — CCRN/PCCN Mastery Deck (57.apkg)')
    lines.append('Standard: one card = one clinical domain')
    lines.append('=' * 70)

    total_high = total_med = total_low = total_ok = 0

    for chunk in sorted(by_chunk.keys()):
        cards   = by_chunk[chunk]
        n_high  = sum(1 for c in cards if c['severity'] == 'HIGH')
        n_med   = sum(1 for c in cards if c['severity'] == 'MEDIUM')
        n_low   = sum(1 for c in cards if c['severity'] == 'LOW')
        n_ok    = sum(1 for c in cards if c['severity'] == 'OK')
        total_high += n_high; total_med += n_med
        total_low  += n_low;  total_ok  += n_ok

        flagged = n_high + n_med + n_low
        lines.append(f'\nCHUNK {chunk:02d}  ({len(cards)} cards | '
                     f'{n_high} HIGH  {n_med} MEDIUM  {n_low} LOW  {n_ok} OK)')
        lines.append('─' * 70)

        for c in cards:
            if c['severity'] == 'OK':
                continue   # omit clean cards from report

            sev_tag  = f"[{c['severity']:<6}]"
            dom_str  = ', '.join(c['domains']) if c['domains'] else '—'
            multi_tag = '  ★ MULTI-SUBJECT' if c['multi'] else ''
            lines.append(f"\n  {sev_tag} blanks={c['blanks']}  {c['ltag']}{multi_tag}")
            lines.append(f"  Domains : {dom_str}")
            # wrap front at 80 chars
            words, line_buf = c['front'].split(), ''
            wrapped = []
            for w in words:
                if len(line_buf) + len(w) + 1 > 78:
                    wrapped.append('  ' + line_buf)
                    line_buf = w
                else:
                    line_buf = (line_buf + ' ' + w).strip()
            if line_buf:
                wrapped.append('  ' + line_buf)
            lines.append(f"  Front   :")
            lines.extend(wrapped)

        if flagged == 0:
            lines.append('  (no flagged cards in this chunk)')

    # ── summary ────────────────────────────────────────────────────────────
    total_cards   = total_high + total_med + total_low + total_ok
    total_flagged = total_high + total_med + total_low
    lines.append('\n' + '=' * 70)
    lines.append('SUMMARY')
    lines.append('=' * 70)
    lines.append(f"Total chart cards : {total_cards}")
    lines.append(f"Flagged (needs review) : {total_flagged}  "
                 f"({100*total_flagged//total_cards}% of deck)")
    lines.append(f"  HIGH   (must split)   : {total_high}")
    lines.append(f"  MEDIUM (likely split) : {total_med}")
    lines.append(f"  LOW    (review)       : {total_low}")
    lines.append(f"  OK     (single domain): {total_ok}")

    report = '\n'.join(lines)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(report)

    print(report)
    print(f"\nReport saved → {OUT}")


if __name__ == '__main__':
    main()
