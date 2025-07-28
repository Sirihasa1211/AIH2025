import fitz  # PyMuPDF
import json
import os

def load_outline(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_text_by_sections(pdf_path, outline):
    """
    Extract text from pdf_path, sectioned by heading boundaries from outline.

    Returns list of dicts:
    [
      {
        "section_title": str,
        "page_start": int,
        "page_end": int,
        "text": str
      },
      ...
    ]
    """
    pdf = fitz.open(pdf_path)
    sections = []

    headings = outline.get("outline", [])
    if not headings:
        # fallback: entire document as one section
        full_text = "".join([page.get_text() for page in pdf])
        return [{
            "section_title": "Full Document",
            "page_start": 1,
            "page_end": len(pdf),
            "text": full_text.strip()
        }]

    # Sort headings by page
    headings_sorted = sorted(headings, key=lambda h: h['page'])
    n = len(headings_sorted)

    for i, h in enumerate(headings_sorted):
        start_page = h['page']
        end_page = headings_sorted[i + 1]['page'] - 1 if i + 1 < n else len(pdf)
        section_text = ""
        for pg_num in range(start_page - 1, end_page):
            section_text += pdf[pg_num].get_text()
        sections.append({
            "section_title": h['text'],
            "page_start": start_page,
            "page_end": end_page,
            "text": section_text.strip()
        })
    return sections

def load_all_sections(input_dir, outlines_dir):
    """
    For each PDF in input_dir and its outline JSON in outlines_dir,
    extract all sections with text.
    
    Returns dict:
    {
      "document_name.pdf": {
        "title": str,
        "sections": [list of section dicts]
      },
      ...
    }
    """
    docs = {}
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    for pdf_file in pdf_files:
        outline_file = pdf_file[:-4] + '.json'
        pdf_path = os.path.join(input_dir, pdf_file)
        json_path = os.path.join(outlines_dir, outline_file)
        
        if not os.path.isfile(json_path):
            print(f"Warning: Outline JSON for '{pdf_file}' missing, skipping.")
            continue
        
        outline = load_outline(json_path)
        sections = extract_text_by_sections(pdf_path, outline)
        
        docs[pdf_file] = {
            "title": outline.get("title", "Unknown Document"),
            "sections": sections
        }
    return docs
