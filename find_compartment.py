import pdfplumber, sys, os
sys.stdout.reconfigure(encoding='utf-8')

sources = {
    "Juarez": r"C:\Users\lunar\Desktop\Cards\CCRN_Cards_Project\Cards\sourcedocs\Adult CCRN Exam Premium For the Latest Exam Blueprint, Includes 3 Practice Tests, Comprehensive Review, and Online Study Prep… (Pat Juarez) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
    "Colson": r"C:\Users\lunar\Desktop\Cards\CCRN_Cards_Project\Cards\sourcedocs\CCRN Exam Study Guide - Ace your Adult Critical Care Registered Nurse License on the First Try QA (June 5, 2024)_(B0D6BM8K97) (Colson Ridge) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
    "Burns": r"C:\Users\lunar\Desktop\Cards\CCRN_Cards_Project\Cards\sourcedocs\AACN Essentials of Progressive Care Nursing, Fourth Edition (Suzanne M. Burns  Sarah A. Delgado) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
}

terms = ['compartment syndrome', 'fasciotomy', 'delta pressure', 'compartment pressure']

for name, path in sources.items():
    if not os.path.exists(path):
        print(f"{name}: FILE NOT FOUND")
        continue
    try:
        with pdfplumber.open(path) as pdf:
            hits = []
            for i, page in enumerate(pdf.pages, 1):
                t = page.extract_text() or ''
                tl = t.lower()
                if any(term in tl for term in terms):
                    hits.append(i)
            print(f"{name}: pages with compartment/fasciotomy/delta: {hits[:20]}")
    except Exception as e:
        print(f"{name}: ERROR - {e}")
