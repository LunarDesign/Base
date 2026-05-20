"""
patch_vari.py — inject context-variation (VARI) into existing apkg chart note types.

Reads:   CCRN_PCCN_Mastery_v7_final_33.apkg  (never modified)
Writes:  CCRN_PCCN_Mastery_v7_final_33_vari.apkg  (new file)

Run this once after flipping VARI_ENABLED = True in build_utils.py, so existing
chunk-28 through chunk-33 chart cards get the same font micro-theme rotation that
future chunk builds will produce automatically via make_chart_template().

Idempotent: running twice produces the same output (no double-injection).
"""
import sqlite3, json, zipfile, shutil, os, tempfile
from build_utils import VARI_JS, VARI_CSS_ADDON

SRC  = 'CCRN_PCCN_Mastery_v7_final_33.apkg'
DEST = 'CCRN_PCCN_Mastery_v7_final_33_vari.apkg'
WORK = os.path.join(tempfile.gettempdir(), 'patch_vari_work')

VARI_SCRIPT = f'<script>{VARI_JS}</script>'
VARI_CSS    = VARI_CSS_ADDON.strip()


def _already_has_vari_js(template_str):
    # Detect prior injection by looking for the unique inner function name
    return '_cv' in template_str and '--cv-ff' in template_str


def _already_has_vari_css(css_str):
    return '--cv-ff' in css_str


def patch():
    # ── 1. Extract source apkg ────────────────────────────────────────────────
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK)
    with zipfile.ZipFile(SRC) as z:
        z.extractall(WORK)

    db = sqlite3.connect(os.path.join(WORK, 'collection.anki2'))
    row = db.execute("SELECT models FROM col").fetchone()
    models = json.loads(row[0])

    # ── 2. Patch each CCRN Chart note type ───────────────────────────────────
    patched = 0
    for mkey, m in models.items():
        if 'CCRN Chart:' not in m.get('name', ''):
            continue

        # CSS
        css = m.get('css', '')
        if not _already_has_vari_css(css):
            m['css'] = css + '\n' + VARI_CSS_ADDON
        else:
            print(f"  [skip css]  {m['name']} — VARI CSS already present")

        # Templates
        for tmpl in m.get('tmpls', []):
            qfmt = tmpl.get('qfmt', '')
            afmt = tmpl.get('afmt', '')

            if not _already_has_vari_js(qfmt):
                tmpl['qfmt'] = VARI_SCRIPT + qfmt
            else:
                print(f"  [skip qfmt] {m['name']} — VARI JS already present")

            if not _already_has_vari_js(afmt):
                tmpl['afmt'] = VARI_SCRIPT + afmt
            else:
                print(f"  [skip afmt] {m['name']} — VARI JS already present")

        patched += 1
        print(f"  Patched: {m['name']}")

    # ── 3. Write back and repack ──────────────────────────────────────────────
    db.execute("UPDATE col SET models=?", (json.dumps(models),))
    db.commit()
    db.close()

    with zipfile.ZipFile(DEST, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in os.listdir(WORK):
            zf.write(os.path.join(WORK, f), f)

    src_kb  = os.path.getsize(SRC)  // 1024
    dest_kb = os.path.getsize(DEST) // 1024
    print(f"\nDone. {patched} note type(s) patched.")
    print(f"  Source:  {SRC}  ({src_kb} KB)")
    print(f"  Output:  {DEST}  ({dest_kb} KB)")
    print(f"\nImport {DEST} into Anki Desktop (File > Import) to activate VARI.")
    print("Original file is unchanged.")


if __name__ == '__main__':
    patch()
