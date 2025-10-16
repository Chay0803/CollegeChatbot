import os
from pypdf import PdfReader, PdfWriter


def clean_pdf(input_path, pages_to_remove):
    """Removes unwanted pages and saves as _clean.pdf"""
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        if i not in pages_to_remove:
            writer.add_page(page)

    base, ext = os.path.splitext(input_path)
    output_path = base + "_clean.pdf"

    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"Cleaned PDF saved as {output_path}")
    return output_path


def merge_pdfs(pdf_list, output_path="merged_clean.pdf"):
    writer = PdfWriter()
    for pdf in pdf_list:
        reader = PdfReader(pdf)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"Merged PDF saved as {output_path}")




folder = "data"  
pdf_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".pdf")]

cleaned_files = []

for pdf in pdf_files:
    print(f"\n Processing {pdf}")
    total_pages = len(PdfReader(pdf).pages)
    print(f"   → Total pages: {total_pages} (1 to {total_pages})")

    # Ask which pages to remove (human numbering)
    remove_str = input(f"Enter pages to remove from {os.path.basename(pdf)} (e.g. 3,4 or leave empty): ").strip()
    if remove_str:
        pages_to_remove = [int(x)-1 for x in remove_str.split(",") if x.isdigit()]
    else:
        pages_to_remove = []

    cleaned_file = clean_pdf(pdf, pages_to_remove)
    cleaned_files.append(cleaned_file)


merge_pdfs(cleaned_files, os.path.join(folder, "final_chatbot_data.pdf"))
