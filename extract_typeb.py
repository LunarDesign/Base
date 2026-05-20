"""
Extract full front+back content for cards with 5+ blanks.
These are the primary Type B (multi-concept overload) candidates.
"""
import re, os, sys

blank = '_______'
SEP = '\x1f'
OUT = []

for n in range(30, 57):
    fname = f'chunk{n}_charts.py'
    if not os.path.exists(fname):
        continue
    with open(fname, encoding='utf-8') as f:
        src = f.read()

    cards_start = src.find('CARDS = [')
    if cards_start == -1:
        continue

    lines = src[cards_start:].split('\n')
    in_tuple = False
    paren_depth = 0
    card_texts = []
    current_card_lines = []

    for line in lines:
        if line.strip().startswith('(') and not in_tuple:
            in_tuple = True
            paren_depth = 1
            current_card_lines = [line]
        elif in_tuple:
            current_card_lines.append(line)
            paren_depth += line.count('(') - line.count(')')
            if paren_depth <= 0:
                in_tuple = False
                card_texts.append('\n'.join(current_card_lines))
                current_card_lines = []

    for i, card in enumerate(card_texts):
        cnt = card.count(blank)
        if cnt < 5:
            continue

        # Extract ltag
        ltag_match = re.search(r"'(chart-l[123])'", card)
        ltag = ltag_match.group(1) if ltag_match else '?'

        # Extract chart_type (6th element — after params_json)
        ctype_matches = re.findall(r"'([a-z_]+)'(?:\s*,\s*'(?:\{|chart))", card)
        ctype = ctype_matches[0] if ctype_matches else '?'

        # Extract string content: join all quoted strings
        # Find all string literals in order
        strings = re.findall(r'"((?:[^"\\]|\\.)*)"', card, re.DOTALL)
        if len(strings) < 2:
            strings = re.findall(r"'((?:[^'\\]|\\.)*)'", card, re.DOTALL)

        # First string(s) = front, next = back
        # Front ends before '→' typically appears in back
        # Simple heuristic: join strings, split at first '→ CCRN KEY' or '→ MASTERY'
        all_text = ' '.join(strings)

        # Find split point
        back_start = all_text.find('→ CCRN KEY:')
        if back_start == -1:
            back_start = all_text.find('→ MASTERY')
        if back_start == -1:
            back_start = len(all_text) // 2

        front_text = all_text[:back_start].strip()
        back_text = all_text[back_start:].strip()

        entry = (
            f"\n{'='*70}\n"
            f"CHUNK {n}  CARD[{i}]  blanks={cnt}  ltag={ltag}\n"
            f"{'─'*70}\n"
            f"FRONT: {front_text}\n"
            f"{'─'*70}\n"
            f"BACK:  {back_text}\n"
        )
        OUT.append(entry)

output = '\n'.join(OUT)
sys.stdout.buffer.write(output.encode('utf-8', errors='replace'))
sys.stdout.buffer.write(b'\n')
print(f'\nTotal 5+ blank cards: {len(OUT)}', file=sys.stderr)
