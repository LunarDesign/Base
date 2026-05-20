#!/usr/bin/env python3
"""
patch_typeb2.py
Apply all 142 domain splits from clinical_split_plan_all_chunks.md to
CCRN_PCCN_Mastery_v7_final_57.apkg -> CCRN_PCCN_Mastery_v7_final_58.apkg

Each split: delete original note, insert Card A + Card B with inherited
tier / badge / tags / model from the source note.
"""
import os, re, sys, shutil, sqlite3, zipfile, hashlib, time, tempfile

sys.stdout.reconfigure(encoding='utf-8')

CARDS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(CARDS_DIR, 'CCRN_PCCN_Mastery_v7_final_57.apkg')
DST  = os.path.join(CARDS_DIR, 'CCRN_PCCN_Mastery_v7_final_58.apkg')
BAK  = SRC + '.bak'
PLAN = os.path.join(CARDS_DIR, 'clinical_split_plan_all_chunks.md')
WORK = os.path.join(tempfile.gettempdir(), 'patch58')
SEP  = '\x1f'


# ── text helpers ─────────────────────────────────────────────────────────────

def make_guid(nid, card_letter):
    raw = f'{nid}-{card_letter}'
    return hashlib.md5(raw.encode()).hexdigest()[:10]


def safe_html(t):
    """Escape numeric < / > comparisons only; leave HTML tags intact."""
    t = re.sub(r'<(\s*[\d_])',                                          r'&lt;\1',   t)
    t = re.sub(r'(\d\s*)>(\s*[\d_])',                                   r'\1&gt;\2', t)
    t = re.sub(r'(\d\s*)>(\s*(?:mmHg|mEq|mg|mcg|%|bpm|min|mL|hr|kg|h\b))',
               r'\1&gt;\2', t)
    return t


def md_to_html(text):
    """Convert markdown bold/italic to HTML and newlines to <br>."""
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)',
                  r'<i>\1</i>', text, flags=re.DOTALL)
    text = text.replace('\n', '<br>')
    return text


def normalize(text):
    """Normalize ASCII arrows and strip trailing whitespace."""
    text = text.replace('->', '→')   # -> to right arrow
    text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)
    return text


def build_flds(front, back, tier, badge):
    f = safe_html(md_to_html(normalize(front.strip())))
    b = safe_html(md_to_html(normalize(back.strip())))
    return SEP.join([f, b, tier, badge])


# ── plan parser ──────────────────────────────────────────────────────────────

def strip_bq(line):
    """Strip blockquote '> ' prefix; return content or None if not a bq line."""
    m = re.match(r'^>\s?(.*)', line.rstrip('\r\n'))
    return m.group(1) if m else None


def extract_card(block_lines, letter):
    """
    Extract {front, back} for Card A or B from a list of lines that
    make up one split block.
    """
    # Find positions of all card headers in this block
    card_pos = {}
    for j, line in enumerate(block_lines):
        m = re.match(r'^\*\*Card ([AB])\b', line.strip())
        if m:
            card_pos[m.group(1)] = j + 1   # content starts after header line

    if letter not in card_pos:
        return None

    start = card_pos[letter]

    # End of this card's section = start of the other card header (if after us)
    end = len(block_lines)
    for other in ('A', 'B'):
        if other != letter and other in card_pos and card_pos[other] > start:
            end = min(end, card_pos[other] - 1)

    card_lines = block_lines[start:end]

    front_parts = []
    back_parts  = []
    state       = 'pre'    # pre -> front -> gap -> back

    for line in card_lines:
        bq = strip_bq(line)
        if bq is None:
            # Non-blockquote line ends the back section
            if state == 'back' and back_parts:
                break
            continue

        if state in ('pre', 'front'):
            if bq.startswith('**FRONT:**'):
                front_parts.append(bq[len('**FRONT:**'):].strip())
                state = 'front'
            elif state == 'front':
                if bq == '':
                    state = 'gap'
                else:
                    front_parts.append(bq)         # multi-line front (rare)

        elif state == 'gap':
            if bq.startswith('**BACK:**'):
                back_parts.append(bq[len('**BACK:**'):].strip())
                state = 'back'

        elif state == 'back':
            back_parts.append(bq)

    if not front_parts or not back_parts:
        return None

    return {
        'front': ' '.join(front_parts),
        'back':  '\n'.join(back_parts),
    }


def parse_plan(path):
    """
    Parse the split plan and return a list of dicts:
      {split_n, nid, card_a_front, card_a_back, card_b_front, card_b_back}
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(path, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()

    # Header pattern: ### SPLIT N — nid NNNNN * ...
    # Handles em-dash, ASCII --, asterisks, middle dots
    header_re = re.compile(r'^### SPLIT (\d+)\s+[^\d]*nid\s+(\d+)')

    # Collect (line_idx, split_n, nid) for every header
    headers = []
    for i, line in enumerate(lines):
        m = header_re.match(line)
        if m:
            headers.append((i, int(m.group(1)), int(m.group(2))))

    splits = []
    for h_idx, (line_i, split_n, nid) in enumerate(headers):
        # Block runs from one header to the next (exclusive)
        block_start = line_i + 1
        block_end   = headers[h_idx + 1][0] if h_idx + 1 < len(headers) else len(lines)
        block       = lines[block_start:block_end]

        card_a = extract_card(block, 'A')
        card_b = extract_card(block, 'B')

        if card_a and card_b:
            splits.append({
                'split_n':      split_n,
                'nid':          nid,
                'card_a_front': card_a['front'],
                'card_a_back':  card_a['back'],
                'card_b_front': card_b['front'],
                'card_b_back':  card_b['back'],
            })
        else:
            print(f'  !! SPLIT {split_n} nid={nid}: parse failed '
                  f'(A={bool(card_a)}, B={bool(card_b)})')

    return splits


# ── database helpers ─────────────────────────────────────────────────────────

def unpack(src, work):
    if os.path.exists(work):
        shutil.rmtree(work)
    os.makedirs(work)
    with zipfile.ZipFile(src) as z:
        z.extractall(work)


def repack(work, dst):
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(work):
            for fname in files:
                full = os.path.join(root, fname)
                z.write(full, os.path.relpath(full, work))


def get_note(db, nid):
    """Return (mid, did, tags, flds) or None."""
    row = db.execute(
        "SELECT n.mid, c.did, n.tags, n.flds "
        "FROM notes n JOIN cards c ON c.nid = n.id "
        "WHERE n.id = ?",
        (nid,)
    ).fetchone()
    return row


def delete_note(db, nid):
    db.execute("DELETE FROM cards WHERE nid = ?", (nid,))
    db.execute("DELETE FROM notes WHERE id = ?",  (nid,))


def insert_note(db, nid, card_id, mid, did, tags, flds):
    sfld = re.sub(r'<[^>]+>', '', flds.split(SEP)[0])[:100]
    guid = make_guid(nid, str(card_id))
    now  = int(time.time())
    db.execute(
        "INSERT OR IGNORE INTO notes "
        "(id, guid, mid, mod, usn, tags, flds, sfld, csum, flags, data) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (nid, guid, int(mid), now, -1, tags, flds, sfld, 0, 0, '')
    )
    db.execute(
        "INSERT OR IGNORE INTO cards "
        "(id, nid, did, ord, mod, usn, type, queue, due, ivl, factor, "
        "reps, lapses, left, odue, odid, flags, data) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (card_id, nid, did, 0, now, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '')
    )


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    print(f'Parsing: {os.path.basename(PLAN)}')
    splits = parse_plan(PLAN)
    print(f'Parsed {len(splits)} splits.\n')

    if len(splits) == 0:
        print('ERROR: no splits parsed — aborting.')
        return

    print(f'Backing up {os.path.basename(SRC)}')
    shutil.copy2(SRC, BAK)

    shutil.copy2(SRC, DST)
    print(f'Unpacking to work dir…')
    unpack(DST, WORK)

    db = sqlite3.connect(os.path.join(WORK, 'collection.anki2'))
    notes_before = db.execute("SELECT COUNT(*) FROM notes").fetchone()[0]

    # Base nid for new notes: current timestamp in ms
    # Spacing: each split uses 4 ids (nid_a, card_id_a, nid_b, card_id_b)
    base_ms = int(time.time()) * 1000
    applied  = 0
    skipped  = 0
    parse_err = 0

    for idx, sp in enumerate(splits):
        nid = sp['nid']
        row = get_note(db, nid)

        if row is None:
            print(f"  [SKIP] SPLIT {sp['split_n']} nid={nid} — not in DB")
            skipped += 1
            continue

        mid, did, tags, orig_flds = row
        parts = orig_flds.split(SEP)
        tier  = parts[2] if len(parts) > 2 else 'tier-high'
        badge = parts[3] if len(parts) > 3 else ''

        nid_a    = base_ms + idx * 4
        card_a   = nid_a + 1
        nid_b    = base_ms + idx * 4 + 2
        card_b   = nid_b + 1

        flds_a = build_flds(sp['card_a_front'], sp['card_a_back'], tier, badge)
        flds_b = build_flds(sp['card_b_front'], sp['card_b_back'], tier, badge)

        delete_note(db, nid)
        insert_note(db, nid_a, card_a, mid, did, tags, flds_a)
        insert_note(db, nid_b, card_b, mid, did, tags, flds_b)

        front_preview = sp['card_a_front'][:55].replace('\n', ' ')
        print(f"  [OK] SPLIT {sp['split_n']:3d}  nid={nid} -> A:{nid_a} B:{nid_b}  |  {front_preview}…")
        applied += 1

    db.commit()
    notes_after = db.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    db.close()

    os.remove(DST)
    repack(WORK, DST)
    shutil.rmtree(WORK)

    delta = notes_after - notes_before
    print(f'\n{"="*65}')
    print(f'  Applied  : {applied}/{len(splits)} splits')
    print(f'  Skipped  : {skipped}  (nid not found in DB)')
    print(f'  Notes    : {notes_before} -> {notes_after}  ({delta:+d})')
    print(f'  Output   : {os.path.basename(DST)}')
    print(f'  Backup   : {os.path.basename(BAK)}')
    print(f'{"="*65}')


if __name__ == '__main__':
    main()
