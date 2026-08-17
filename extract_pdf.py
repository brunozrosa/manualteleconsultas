import os
import sys

# Ensure stdout uses UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Try to import pypdf, if not found try to install it
try:
    import pypdf
except ImportError:
    print("pypdf not installed. Attempting to install...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
    import pypdf

def extract_text_from_pdf(pdf_path, output_txt_path):
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        return False
        
    try:
        reader = pypdf.PdfReader(pdf_path)
        print(f"Successfully opened {pdf_path}. Total pages: {len(reader.pages)}")
        
        extracted_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            extracted_text.append(f"--- PAGE {i+1} ---")
            extracted_text.append(text)
            
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(extracted_text))
            
        print(f"Success! Extracted text saved to {output_txt_path}")
        return True
    except Exception as e:
        print(f"Error during PDF extraction: {e}")
        return False

# Look for the PDF in the parent directory
parent_dir = ".."
pdf_candidates = [
    os.path.join(parent_dir, f) for f in os.listdir(parent_dir)
    if "manual" in f.lower() and "tele" in f.lower() and f.endswith(".pdf")
]

if pdf_candidates:
    # Use the first match
    pdf_path = pdf_candidates[0]
    print(f"Found PDF candidate: {pdf_path}")
    extract_text_from_pdf(pdf_path, "manual_extracted_from_pdf.txt")
else:
    print("No matching PDF files found in parent directory.")
    print("All files containing 'manual' or 'tele' in parent directory:")
    for f in os.listdir(parent_dir):
        if "manual" in f.lower() or "tele" in f.lower():
            print(f"- {f}")
