import pdfplumber, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r"C:\Users\lunar\Desktop\Cards\CCRN_Cards_Project\Cards\sourcedocs\Adult CCRN Exam Premium For the Latest Exam Blueprint, Includes 3 Practice Tests, Comprehensive Review, and Online Study Prep… (Pat Juarez) (z-library.sk, 1lib.sk, z-lib.sk).pdf"
terms = ['compartment', 'fasciotomy', 'delta pressure']

with pdfplumber.open(path) as pdf:
    hits = []
    for i, page in enumerate(pdf.pages, 1):
        t = page.extract_text() or ''
        if any(term.lower() in t.lower() for term in terms):
            hits.append(i)
    print(f"Juarez pages with compartment/fasciotomy/delta: {hits}")
    print()
    # Extract text from hit pages
    for pg in hits[:10]:
        t = pdf.pages[pg-1].extract_text() or ''
        # Find the relevant section
        lines = t.split('\n')
        for j, line in enumerate(lines):
            if any(term.lower() in line.lower() for term in terms):
                start = max(0, j-3)
                end = min(len(lines), j+8)
                print(f"--- Page {pg}, context around match ---")
                print('\n'.join(lines[start:end]))
                print()
                break
