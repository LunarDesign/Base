import pdfplumber, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r"C:\Users\lunar\Desktop\Cards\CCRN_Cards_Project\Cards\sourcedocs\Adult CCRN Exam Premium For the Latest Exam Blueprint, Includes 3 Practice Tests, Comprehensive Review, and Online Study Prep… (Pat Juarez) (z-library.sk, 1lib.sk, z-lib.sk).pdf"

with pdfplumber.open(path) as pdf:
    for pg in [809, 810, 811, 812, 813]:
        t = pdf.pages[pg-1].extract_text() or ''
        print(f"=== PAGE {pg} ===")
        print(t)
        print()
