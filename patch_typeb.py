#!/usr/bin/env python3
"""
patch_typeb.py — Split 6 Type-B multi-concept overload cards in 56.apkg
into 12 focused single-concept cards.  Output: 57.apkg.
"""
import os, re, sys, shutil, sqlite3, zipfile, hashlib, time, tempfile

sys.stdout.reconfigure(encoding='utf-8')

CARDS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(CARDS_DIR, 'CCRN_PCCN_Mastery_v7_final_56.apkg')
BAK  = SRC + '.bak'
DST  = os.path.join(CARDS_DIR, 'CCRN_PCCN_Mastery_v7_final_57.apkg')
WORK = os.path.join(tempfile.gettempdir(), 'patch57')

SEP = '\x1f'

# ── helpers ────────────────────────────────────────────────────────────────
def make_guid(front, back=''):
    return hashlib.md5(
        re.sub(r'\s+', ' ', (front + back).lower())[:120].encode()
    ).hexdigest()[:10]

def safe_html(t):
    t = re.sub(r'<(\s*[\d_])', r'&lt;\1', t)
    t = re.sub(r'(\d\s*)>(\s*[\d_])', r'\1&gt;\2', t)
    t = re.sub(r'(\d\s*)>(\s*(?:mmHg|mEq|mg|mcg|%|bpm|min|mL|hr|kg|h\b))', r'\1&gt;\2', t)
    return t

def strip_html(t):
    return re.sub(r'<[^>]+>', '', t)

# ── patch definitions ──────────────────────────────────────────────────────
# Each entry: (search_fragment, [(front, back, tier, ltag)])
# mid, did, badge, tags are inherited from the deleted note.

PATCHES = [

    # ── 1. Cyanide + Organophosphate ──────────────────────────────────────
    (
        "Organophosphate toxicity requires",   # unique string only in this card's front
        [
            (
                "The antidote chart shows cyanide poisoning is treated with _______ at _______ grams IV. "
                "This antidote is preferred over sodium nitrite in smoke inhalation because _______.",

                "Cyanide poisoning → Hydroxocobalamin (Cyanokit): 5 g IV over 15 minutes\n"
                "| Preferred in smoke inhalation: safe with concurrent CO (sodium nitrite worsens CO toxicity)\n"
                "| Mechanism: binds CN⁻ → cyanocobalamin (non-toxic, renally excreted)\n"
                "| Expected side effect: red-pink urine — document to prevent alarm\n"
                "| Alternative: sodium thiosulfate (enhances CN→thiocyanate conversion via rhodanese)\n"
                "→ CCRN KEY: Cyanide toxicity in smoke inhalation: consider if CO-poisoned patient "
                "fails to improve with 100% O₂ + lactate > 10 mmol/L. "
                "Sodium nitrite forms methemoglobin to bind CN⁻ — DANGEROUS if CO present "
                "(metHgb + carboxyhgb = severely impaired O₂ carrying capacity).\n"
                "→ MASTERY NOTE: Red-pink urine from hydroxocobalamin: document at medication start to "
                "prevent alarm at shift change. Sodium thiosulfate enhances CN→thiocyanate via rhodanese "
                "enzyme — slower than hydroxocobalamin but can be combined.",

                'tier-critical', 'chart-l3'
            ),
            (
                "On the antidote chart, organophosphate toxicity requires _______ (titrated to _______, "
                "not heart rate) PLUS _______ to reactivate acetylcholinesterase. "
                "Pralidoxime (2-PAM) must be given _______ to be effective.",

                "Organophosphate toxicity → Atropine + Pralidoxime (2-PAM):\n"
                "| Atropine: 2–4 mg IV every 5–10 min; titrate to DRY secretions (not HR or pupil size)\n"
                "| 2-PAM: 1–2 g IV; must give EARLY — AChE 'aging' becomes irreversible at 24–48h\n"
                "| Toxidrome (SLUDGE): Salivation, Lacrimation, Urination, Defecation, GI upset, Emesis\n"
                "| Also: bradycardia, miosis, bronchospasm (muscarinic excess)\n"
                "→ CCRN KEY: Atropine endpoint = DRY secretions + clear lung sounds — NOT HR or pupil size. "
                "Doses up to 20–100 mg may be needed in severe poisoning. "
                "2-PAM prevents new ACh binding but cannot reverse 'aged' (covalently bound) AChE.\n"
                "→ MASTERY NOTE: Pralidoxime window: give within 24–48h before irreversible AChE aging. "
                "After aging: atropine controls symptoms; 2-PAM no longer reactivates. "
                "Sources: pesticides (malathion, parathion), nerve agents (sarin, VX).",

                'tier-critical', 'chart-l3'
            ),
        ]
    ),

    # ── 2. ADRENAL + APROCCHSS ────────────────────────────────────────────
    (
        "ADRENAL found hydrocortisone",
        [
            (
                "The ADRENAL trial (NEJM 2018) studied hydrocortisone _______ mg/day × 7 days in septic "
                "shock, showing faster vasopressor cessation but _______ 90-day mortality benefit.",

                "ADRENAL (NEJM 2018, n=3,800): hydrocortisone 200 mg/day × 7 days\n"
                "| Faster vasopressor cessation: 56.9% vs 51.1% at Day 7\n"
                "| NO 90-day mortality benefit (27.9% vs 28.8%)\n"
                "→ CCRN KEY: Why the null result? ADRENAL used hydrocortisone ALONE — no mineralocorticoid. "
                "Larger (n=3,800) and better powered than APROCCHSS → null result considered more reliable. "
                "SSC 2021: weak recommendation for steroids in vasopressor-dependent septic shock.\n"
                "→ MASTERY NOTE: Hydrocortisone 200 mg/day has inherent mineralocorticoid activity — "
                "may explain why fludrocortisone adds marginal benefit at this dose. "
                "Monitoring: glucose q4–6h (hyperglycemia common), secondary infection surveillance. "
                "Do NOT abruptly stop — taper with vasopressor wean to prevent rebound shock.",

                'tier-review', 'chart-l1'
            ),
            (
                "The APROCCHSS trial (NEJM 2018) added _______ mcg/day of _______ to hydrocortisone "
                "200 mg/day and DID show mortality benefit (_______ vs _______%). "
                "The SSC trigger for steroids in septic shock is NE or Epi ≥ _______ mcg/kg/min.",

                "APROCCHSS (NEJM 2018, n=1,241): hydrocortisone 200 mg/day + fludrocortisone 50 mcg/day × 7 days\n"
                "| MORTALITY BENEFIT: 43.0% vs 49.1% at 90 days (p=0.03)\n"
                "| Key difference from ADRENAL: fludrocortisone (mineralocorticoid) added\n"
                "| SSC trigger: NE or Epi ≥ 0.25 mcg/kg/min despite adequate fluid resuscitation\n"
                "→ CCRN KEY: APROCCHSS vs ADRENAL — why different results?\n"
                "APROCCHSS added fludrocortisone 50 mcg/day PO. Whether fludrocortisone explains the "
                "mortality difference remains debated — different patient populations also differed.\n"
                "→ MASTERY NOTE: Fludrocortisone: mineralocorticoid receptor agonist → Na/water retention, "
                "K excretion. At hydrocortisone 200 mg/day (inherent mineralocorticoid effect), "
                "additional fludrocortisone may be redundant — hence the ongoing controversy.",

                'tier-review', 'chart-l1'
            ),
        ]
    ),

    # ── 3. DEXA-ARDS + RECOVERY-COVID ────────────────────────────────────
    (
        "DEXA-ARDS trial used dexamethasone",
        [
            (
                "The DEXA-ARDS trial (Lancet RM 2020) enrolled moderate–severe ARDS (P/F ≤ _______ "
                "for ≥ 24h) and used dexamethasone _______ mg/day × 5 days then _______ mg/day × 5 days. "
                "Results: +_______ ventilator-free days; 60-day mortality _______ vs 36.4%.",

                "DEXA-ARDS (Lancet Respir Med 2020, n=299):\n"
                "| Enrolled: moderate–severe ARDS (P/F ≤ 200 mmHg) despite LPV for ≥ 24h\n"
                "| Regimen: dexamethasone 20 mg/day × 5d → 10 mg/day × 5d (10 days total)\n"
                "| Results: +4.8 ventilator-free days; 60-day mortality 21.1% vs 36.4%\n"
                "→ CCRN KEY: Mechanism in ARDS: ↓ pro-inflammatory cytokines (TNF-α, IL-6, IL-1β) AND "
                "↓ pulmonary fibroproliferation — steroids target the LATE exudative/fibroproliferative phase. "
                "DEXA-ARDS excluded patients who already received corticosteroids.\n"
                "→ MASTERY NOTE: Dexamethasone preferred over methylprednisolone in ARDS (DEXA-ARDS data). "
                "Advantage: longer t½ (36–72h) → once-daily dosing; no mineralocorticoid activity. "
                "Risks: hyperglycemia (BG target 140–180), secondary infections, ICUAW acceleration.",

                'tier-high', 'chart-l2'
            ),
            (
                "The RECOVERY-COVID trial (NEJM 2020) showed dexamethasone _______ mg/day × 10 days "
                "reduced mortality in ventilated COVID patients from _______ to _______%. "
                "In non-oxygen-requiring COVID-19, dexamethasone showed _______.",

                "RECOVERY-COVID (NEJM 2020):\n"
                "| Dexamethasone 6 mg/day × 10 days in COVID-19 requiring respiratory support\n"
                "| Ventilated patients: mortality 29% vs 41% (28-day) — significant benefit\n"
                "| Oxygen-only patients: mortality benefit present (23% vs 26%)\n"
                "| NO benefit (possibly harmful) in non-oxygen-requiring COVID-19\n"
                "→ CCRN KEY: Why no benefit without O₂? Steroids suppress immune clearance of virus in "
                "early infection — benefit only emerges when hyperinflammation (not viral replication) "
                "drives injury. Same mechanism as DEXA-ARDS: cytokine suppression in late-phase lung injury.\n"
                "→ MASTERY NOTE: RECOVERY-COVID dose (6 mg/day) is lower than DEXA-ARDS (20→10 mg/day) — "
                "reflects different severity populations. Dexamethasone is now standard of care for "
                "hospitalized COVID-19 on O₂ or ventilation.",

                'tier-high', 'chart-l2'
            ),
        ]
    ),

    # ── 4. Dexmedetomidine + β1 locations + Dobutamine ───────────────────
    (
        "β1 receptors are located in the",
        [
            (
                "On the receptor map chart, α2 receptor agonist _______ is used for ICU sedation "
                "because it provides sedation WITHOUT _______ depression — unique among ICU sedatives.",

                "α2 agonist dexmedetomidine: ICU sedation WITHOUT respiratory depression\n"
                "| Mechanism: locus coeruleus (brainstem) α2 → ↓ norepinephrine release → sedation/analgesia\n"
                "| No GABA effect (unlike benzos/propofol) → preserved respiratory drive\n"
                "| Clinical: cooperative ('arousable') sedation — patient responds to voice, follows commands\n"
                "| Also: opioid-sparing, delirium reduction, alcohol/opioid withdrawal adjunct\n"
                "→ CCRN KEY: Dexmedetomidine vs propofol:\n"
                "• Dexmedetomidine: no respiratory depression, cooperative sedation, ↓ delirium (MENDS/MIDEX)\n"
                "• Propofol: rapid onset/offset, no analgesia, PRIS risk at > 4 mg/kg/hr × 48h\n"
                "• Side effects: bradycardia, hypotension (loading dose related) — give loading dose slowly\n"
                "→ MASTERY NOTE: Max FDA-approved: 0.7 mcg/kg/hr; off-label up to 1.5 mcg/kg/hr. "
                "PAD guidelines prefer dexmedetomidine over benzodiazepines for ICU sedation (↓ delirium).",

                'tier-high', 'chart-l2'
            ),
            (
                "On the receptor map chart, β1 receptors are located in the _______, _______, and _______. "
                "Dobutamine acts primarily on _______ receptors, causing _______ and modest _______.",

                "β1 receptors: SA node, AV node, ventricular myocardium\n"
                "| β1 effects: ↑ HR (chronotropy), ↑ contractility (inotropy), ↑ AV conduction (dromotropy)\n"
                "| Dobutamine: β1 + β2 → ↑ CO + modest ↓ SVR; cardiogenic shock (↑ CO without ↑ afterload)\n"
                "→ CCRN KEY: Dobutamine receptor profile:\n"
                "• Primarily β1 (strongest) + β2 (vasodilation) + weak α1\n"
                "• Net: ↑ CO + modest ↓ SVR → preferred inotrope for cardiogenic shock\n"
                "• Tachycardia and arrhythmias at higher doses limit titration\n"
                "→ MASTERY NOTE: Isoproterenol (pure β1 + β2 agonist):\n"
                "• Last resort for bradycardia refractory to atropine — bridge to pacemaker\n"
                "• Torsades de pointes: isoproterenol ↑ HR → shortens QT interval (drug of choice for TdP)\n"
                "• NOT a vasopressor — β2 causes ↓ SVR; BP may paradoxically drop.",

                'tier-high', 'chart-l2'
            ),
        ]
    ),

    # ── 5. Coagulation pathways + UFH + Argatroban ───────────────────────
    (
        "extrinsic pathway is measured by",
        [
            (
                "The coagulation chart shows the extrinsic pathway is measured by _______ (INR) "
                "and the intrinsic pathway by _______. "
                "UFH works by binding _______, which then inhibits factors _______ and _______.",

                "Extrinsic pathway (PT/INR): tissue factor + factor VII → activates factor X\n"
                "| Intrinsic pathway (aPTT): XII → XI → IX → X (with factor VIII as cofactor)\n"
                "| UFH mechanism: binds antithrombin (AT) → AT-UFH complex inhibits IIa (thrombin) + Xa\n"
                "→ CCRN KEY: UFH monitoring options:\n"
                "• aPTT: most widely used; target 60–100s (therapeutic)\n"
                "• Anti-Xa: target 0.3–0.7 IU/mL; preferred in obesity, APS, abnormal baseline aPTT\n"
                "• ACT (activated clotting time): cardiac cath lab/bypass; target > 300s for CPB\n"
                "→ MASTERY NOTE: Why aPTT measures intrinsic pathway: uses a contact activator (kaolin, "
                "silica) to start at factor XII. PT/INR uses tissue factor to start at factor VII. "
                "Both converge at factor X (common pathway).",

                'tier-review', 'chart-l1'
            ),
            (
                "On the coagulation chart, argatroban is used in HIT because it is a direct _______ "
                "inhibitor cleared by _______. "
                "This makes it the preferred anticoagulant in HIT with concomitant _______.",

                "Argatroban: direct thrombin inhibitor (DTI); binds thrombin active site directly\n"
                "| Clearance: hepatic — use in HIT (no cross-reactivity) AND renal failure\n"
                "| Monitoring: aPTT target 1.5–3× baseline; or anti-IIa level\n"
                "→ CCRN KEY: HIT management protocol:\n"
                "• STOP all heparin immediately (including flushes, heparin-coated catheters)\n"
                "• Start NON-heparin anticoagulant: argatroban (hepatic) OR bivalirudin (renal + enzymatic)\n"
                "• Do NOT start warfarin until platelets > 150K (risk of venous gangrene from protein C drop)\n"
                "• 4T score: Thrombocytopenia + Timing + Thrombosis + oTher causes (≤ 3 = low probability)\n"
                "→ MASTERY NOTE: Bivalirudin: renally + enzymatically cleared — preferred when hepatic "
                "failure coexists with HIT. Fondaparinux (indirect Xa via antithrombin): no documented "
                "HIT cross-reactivity — alternative when DTIs unavailable.",

                'tier-review', 'chart-l1'
            ),
        ]
    ),

    # ── 6. CATS trial + vasopressin threshold + epinephrine lactate ───────
    (
        "CATS trial showed NE was superior to dopamine",
        [
            (
                "The CATS trial showed NE was superior to dopamine in shock, with significantly fewer "
                "_______ (_______ vs _______%).",

                "CATS trial: NE vs dopamine in shock — NE superior\n"
                "| Fewer arrhythmias with NE: 10.5% vs 20.6% (P<0.001)\n"
                "| ↓ 28-day mortality in cardiogenic shock subgroup\n"
                "→ CCRN KEY: Why dopamine causes more arrhythmias: activates β1 + variable DA receptors "
                "at the same dose — unpredictable receptor balance. NE: dominant α1 + mild β1 — predictable. "
                "SOAP-II trial same conclusion: dopamine → ↑ 28-day mortality in cardiogenic shock. "
                "SSC: NE recommended first-line vasopressor (strong evidence).\n"
                "→ MASTERY NOTE: Dopamine still has a role: hemodynamically significant bradycardia when "
                "atropine fails (β1 chronotropy without the arrhythmia risk of isoproterenol in this setting). "
                "Neonatal/pediatric septic shock: dopamine first-line in some protocols (different evidence base).",

                'tier-review', 'chart-l1'
            ),
            (
                "On the vasopressor algorithm chart, vasopressin is added at fixed dose _______ units/min "
                "when NE reaches _______ mcg/kg/min. "
                "Epinephrine as a third-line vasopressor raises _______, making _______ clearance "
                "unreliable as a resuscitation endpoint.",

                "Vasopressin: added at 0.03–0.04 units/min (fixed) when NE ≥ 0.25 mcg/kg/min\n"
                "| NOT titrated — fixed dose only; max 0.04 units/min to avoid splanchnic/digital ischemia\n"
                "| V1 receptors (vascular): vasoconstriction — skin, muscle, splanchnic vasculature\n"
                "| Epinephrine third-line: raises serum lactate (β2 → glycogenolysis + liver lactate production)\n"
                "| When epi used: lactate clearance unreliable — use ScvO₂, MAP, or clinical perfusion markers\n"
                "→ CCRN KEY: Vasopressor hierarchy (SSC 2021):\n"
                "1. NE | 2. Vasopressin (add-on) | 3. Epinephrine | 4. Angiotensin II (Giapreza)\n"
                "→ MASTERY NOTE: VASST trial: vasopressin + NE vs NE alone → NO overall 90-day mortality benefit. "
                "Subgroup: less severe septic shock (NE < 15 mcg/min at baseline) showed benefit. "
                "Angiotensin II (ATHOS-3): 20–40 ng/kg/min IV — different units from vasopressin, "
                "watch for order confusion.",

                'tier-review', 'chart-l1'
            ),
        ]
    ),

]


# ── build pipeline ─────────────────────────────────────────────────────────
def unpack(src, work):
    if os.path.exists(work):
        shutil.rmtree(work)
    os.makedirs(work)
    with zipfile.ZipFile(src) as z:
        z.extractall(work)


def repack(work, dst):
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(work):
            for f in files:
                full = os.path.join(root, f)
                z.write(full, os.path.relpath(full, work))


def find_note(db, fragment):
    rows = db.execute(
        "SELECT id, mid, tags, flds FROM notes WHERE flds LIKE ?",
        (f'%{fragment}%',)
    ).fetchall()
    if len(rows) == 0:
        print(f"  !! NOT FOUND: '{fragment}'")
        return None
    if len(rows) > 1:
        print(f"  !! AMBIGUOUS ({len(rows)} matches): '{fragment}' — using first")
    return rows[0]   # (id, mid, tags, flds)


def get_did(db, nid):
    row = db.execute("SELECT did FROM cards WHERE nid=?", (nid,)).fetchone()
    return row[0] if row else None


def delete_note(db, nid):
    db.execute("DELETE FROM cards WHERE nid=?", (nid,))
    db.execute("DELETE FROM notes WHERE id=?",  (nid,))


def insert_note(db, nid, mid, did, tags, front, back, tier, badge, ltag, chunk):
    guid = make_guid(front, back)
    flds = SEP.join([safe_html(front), safe_html(back), tier, badge])
    sfld = strip_html(safe_html(front))[:100]
    now  = int(time.time())
    db.execute(
        "INSERT OR IGNORE INTO notes "
        "(id,guid,mid,mod,usn,tags,flds,sfld,csum,flags,data) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (nid, guid, int(mid), now, -1, tags, flds, sfld, 0, 0, '')
    )
    db.execute(
        "INSERT OR IGNORE INTO cards "
        "(id,nid,did,ord,mod,usn,type,queue,due,ivl,factor,"
        "reps,lapses,left,odue,odid,flags,data) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (nid+1, nid, did, 0, now, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '')
    )


def main():
    # ── backup ────────────────────────────────────────────────────────────
    print(f"Backing up {os.path.basename(SRC)} → {os.path.basename(BAK)}")
    shutil.copy2(SRC, BAK)

    # ── copy src → dst, unpack dst ────────────────────────────────────────
    shutil.copy2(SRC, DST)
    unpack(DST, WORK)
    db = sqlite3.connect(os.path.join(WORK, 'collection.anki2'))

    notes_before = db.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    replaced = 0

    now_ms = int(time.time()) * 1000

    for patch_idx, (fragment, replacements) in enumerate(PATCHES):
        print(f"\n[{patch_idx+1}/{len(PATCHES)}] Searching: '{fragment}'")

        row = find_note(db, fragment)
        if row is None:
            continue

        orig_nid, mid, tags, flds = row
        fields = flds.split(SEP)
        badge  = fields[3] if len(fields) > 3 else ''
        did    = get_did(db, orig_nid)

        orig_front = fields[0][:80].replace('\n', ' ')
        print(f"  Found nid={orig_nid}  front: {orig_front}…")
        print(f"  Deleting original ({len(fragment)}-char fragment match)")
        delete_note(db, orig_nid)

        for r_idx, (front, back, tier, ltag) in enumerate(replacements):
            nid = now_ms + patch_idx * 100 + r_idx * 10
            insert_note(db, nid, mid, did, tags, front, back, tier, badge, ltag, patch_idx)
            print(f"  + Card {r_idx+1}: {front[:70]}…")

        replaced += 1

    db.commit()
    notes_after = db.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    db.close()

    # ── repack ────────────────────────────────────────────────────────────
    os.remove(DST)
    repack(WORK, DST)
    shutil.rmtree(WORK)

    print(f"\n{'='*65}")
    print(f"  Replaced {replaced}/6 Type-B cards")
    print(f"  Notes: {notes_before} → {notes_after} "
          f"(+{notes_after - notes_before} net from splits)")
    print(f"  Output: {os.path.basename(DST)}")
    print(f"  Backup: {os.path.basename(BAK)}")
    print(f"{'='*65}")


if __name__ == '__main__':
    main()
