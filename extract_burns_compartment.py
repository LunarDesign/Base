import pdfplumber, sys
sys.stdout.reconfigure(encoding='utf-8')

burns_path = r"C:\Users\lunar\Desktop\Cards\CCRN_Cards_Project\Cards\sourcedocs\AACN Essentials of Progressive Care Nursing, Fourth Edition (Suzanne M. Burns  Sarah A. Delgado) (z-library.sk, 1lib.sk, z-lib.sk).pdf"
colson_path = r"C:\Users\lunar\Desktop\Cards\CCRN_Cards_Project\Cards\sourcedocs\CCRN Exam Study Guide - Ace your Adult Critical Care Registered Nurse License on the First Try QA (June 5, 2024)_(B0D6BM8K97) (Colson Ridge) (z-library.sk, 1lib.sk, z-lib.sk).pdf"

print("=== BURNS/DELGADO — Compartment Syndrome pages ===")
with pdfplumber.open(burns_path) as pdf:
    for pg in [438, 439, 430, 376]:
        t = pdf.pages[pg-1].extract_text() or ''
        if t.strip():
            print(f"\n--- PAGE {pg} ---")
            print(t[:2000])

print("\n\n=== COLSON RIDGE — Compartment Syndrome pages ===")
with pdfplumber.open(colson_path) as pdf:
    for pg in [55, 71, 72]:
        t = pdf.pages[pg-1].extract_text() or ''
        if t.strip():
            print(f"\n--- PAGE {pg} ---")
            print(t[:2000])
