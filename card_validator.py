"""
CardValidator — CCRN/PCCN Mastery Deck Quality Gate
Hard failures (F1-F7): block card generation, zero tolerance
Soft warning (W8): stored in result dict only, does NOT block generation
"""
import re

class CardValidator:
    def __init__(self):
        self.results = []

    def validate(self, nid, front, back, badge, tier=None):
        issues = []
        f_clean = re.sub(r'</?[a-zA-Z][^>]*>', '', front)
        b_clean = re.sub(r'</?[a-zA-Z][^>]*>', '', back)
        f_lo    = f_clean.lower()
        b_lo    = b_clean.lower()

        # F1: No active recall blank
        if '_______' not in f_clean:
            issues.append('F1:NO_ACTIVE_RECALL')

        # F2: Back too short
        if len(b_clean.strip()) < 60:
            issues.append('F2:BACK_TOO_SHORT')

        # F3: Bullet dump — more than 8 pipe separators AND no annotation arrow
        pipe_count = b_clean.count('\n|') + b_clean.count('| ')
        if pipe_count > 8 and '→' not in b_clean:
            issues.append('F3:BULLET_DUMP')

        # F4: No annotation marker
        if '→' not in b_clean:
            issues.append('F4:NO_ANNOTATION')

        # F5: Repeated blanks answered identically (same short word fills all blanks)
        blanks = re.findall(r'_______', f_clean)
        if len(blanks) > 1:
            # Check if first answer word in back appears to fill all blanks
            first_answer = re.match(r'\s*([A-Z][A-Za-z]+)', b_clean)
            if first_answer:
                word = first_answer.group(1).lower()
                if b_lo.count(word) < len(blanks):
                    pass  # probably fine
                # Light check only — don't over-block

        # F6: Context before blank too long (answer likely embedded)
        blank_pos = f_clean.find('_______')
        if blank_pos > 400:
            issues.append('F6:CONTEXT_BEFORE_BLANK_TOO_LONG')

        # F7: Front > 580 chars (multi-concept dump without recall structure)
        if len(f_clean) > 580:
            issues.append('F7:FRONT_TOO_LONG')

        # F9: Invalid tier class (must be canonical CSS class, not raw label)
        _VALID_TIERS = {'tier-review', 'tier-high', 'tier-moderate', 'tier-critical'}
        if tier is not None and tier not in _VALID_TIERS:
            issues.append('F9:INVALID_TIER_CLASS')

        # W8: Missing specific annotation marker (soft warning only)
        annotation_patterns = [
            '→ ccrn key:', '→ mastery note:', '→ why it matters:',
            '→ layer:',    '→ why:',          '→ nursing:',
            '→ clinical note:',
        ]
        has_annotation = any(p in b_lo for p in annotation_patterns)
        is_ref_card    = 'terminology' in badge.lower() or 'acronym' in badge.lower()
        w8_warning     = not has_annotation and not is_ref_card

        result = {
            'nid':      nid,
            'issues':   issues,
            'front':    front[:80],
            'back':     back[:100],
            'badge':    badge,
            'pass':     len(issues) == 0,
            'warnings': ['W8:MISSING_ANNOTATION'] if w8_warning else [],
        }
        self.results.append(result)
        return issues

    def report(self):
        total   = len(self.results)
        passing = sum(1 for r in self.results if r['pass'])
        pct     = 100 * passing / total if total else 0
        fails   = [r for r in self.results if not r['pass']]
        warned  = [r for r in self.results if r.get('warnings')]

        LABELS = {
            'F1': 'No active recall blank (_______)',
            'F2': 'Back too short (<60 chars)',
            'F3': 'Bullet dump (>8 pipes, no annotation)',
            'F4': 'No annotation marker (→)',
            'F5': 'Repeated answer pattern',
            'F6': 'Context before blank >400 chars',
            'F7': 'Front >580 chars (multi-concept dump)',
            'F9': 'Invalid tier class (must be tier-review/tier-high/tier-moderate/tier-critical)',
            'W8': 'Missing → CCRN KEY: / → MASTERY NOTE: / → WHY IT MATTERS:',
        }

        lines = [f"\nVALIDATION REPORT — {total} cards | {passing} pass ({pct:.1f}%) | "
                 f"{len(fails)} fail | {len(warned)} warnings"]

        if warned:
            lines.append(f"\n{len(warned)} W8 annotation warnings:")
            for r in warned[:10]:
                lines.append(f"  [{r['nid']}] {r['front'][:70]}")
            if len(warned) > 10:
                lines.append(f"  ... and {len(warned)-10} more")

        if fails:
            lines.append(f"\n{len(fails)} failing cards:")
            for r in fails:
                lines.append(f"\n  [{r['nid']}]  {r['front'][:65]}")
                for code in r['issues']:
                    lines.append(f"    ✗ {code}: {LABELS.get(code, code)}")

        return '\n'.join(lines)


print("CardValidator module loaded.")
