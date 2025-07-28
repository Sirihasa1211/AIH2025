import fitz  # PyMuPDF
import os
import re
import json
from collections import defaultdict

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    font_stats = defaultdict(list)
    lines_by_page = {}

    # Collect font sizes and text by page
    for page_num, page in enumerate(doc, 1):
        blocks = page.get_text("dict")["blocks"]
        lines_by_page[page_num] = []

        for b in blocks:
            if "lines" not in b:
                continue
            for l in b["lines"]:
                line_text = ""
                max_font = 0
                for s in l["spans"]:
                    if s["text"].strip():
                        line_text += s["text"].strip() + " "
                        font_stats[s["size"]].append(s["text"].strip())
                        max_font = max(max_font, s["size"])
                if line_text.strip():
                    lines_by_page[page_num].append((line_text.strip(), max_font))

    # Identify largest font as title
    largest_font = max(font_stats.keys())
    title_candidates = font_stats[largest_font]
    title = max(title_candidates, key=len) if title_candidates else "Untitled Document"

    # Define heading patterns
    h1_pattern = re.compile(r"^\d+\.\s+.*")
    h2_pattern = re.compile(r"^\d+\.\d+\s+.*")
    headings = []

    for page_num, lines in lines_by_page.items():
        for line, font in lines:
            # Strip filler or repeated noise
            if re.fullmatch(r"[.\s]+", line) or len(line) <= 3:
                continue

            if h1_pattern.match(line):
                headings.append({"level": "H1", "text": line.strip(), "page": page_num})
            elif h2_pattern.match(line):
                headings.append({"level": "H2", "text": line.strip(), "page": page_num})

            # Also check for TOC headings like “Revision History”, “References”, etc.
            elif line.lower().strip() in [
                "revision history", "table of contents", "acknowledgements", "references"
            ]:
                headings.append({"level": "H1", "text": line.strip(), "page": page_num})

    return {
        "title": title.strip(),
        "outline": headings
    }

def process_all_pdfs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            path = os.path.join(input_dir, filename)
            result = extract_headings(path)
            json_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            print(f"Processed: {filename} ➜ {json_path}")

if __name__ == "__main__":
    INPUT_DIR = "input/"
    OUTPUT_DIR = "output/"
    process_all_pdfs(INPUT_DIR, OUTPUT_DIR)
