
# 📄 Challenge 1A — PDF Outline Extraction  
**Adobe India Hackathon 2025 — Round 1A: Understand Your Document**

---

## 🧠 Overview

Your task is to extract a structured, hierarchical **outline** (Title, H1, H2, H3 with page numbers) from a set of raw PDF documents. This outline serves as the foundational layer for Round 1B and enables future capabilities like semantic navigation, summarization, and intelligent document interaction.

This solution works **offline**, runs on **CPU-only AMD64 machines**, respects **execution time and model size constraints**, and is fully containerized using Docker.

---

## 🚧 Problem Constraints

| Constraint         | Requirement                                      |
|-------------------|--------------------------------------------------|
| 📄 Input Format    | One or more PDFs (up to 50 pages each)          |
| 📤 Output Format   | One JSON file per PDF in the required structure |
| ⏱️ Execution Time  | ≤ 10 seconds per 50-page PDF                    |
| 💾 Model Size      | ≤ 200 MB (if used)                               |
| 🌐 Internet Access | ❌ Not allowed                                   |
| 💻 Platform        | CPU-only, AMD64 (x86_64), Dockerized             |

---

## ⚙️ Build & Run Instructions

### 🔨 Build Docker Image

```bash
docker build --platform linux/amd64 -t pdf-processor .
````

### ▶️ Run the Container

```bash
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-processor
```

📁 Place all PDFs inside the `input/` folder
📁 Extracted JSONs will appear in the `output/` folder

---

## 📤 Output Format

Example output JSON:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

---

## 💡 Solving Methodology

This solution is built using the **PyMuPDF (fitz)** library, which allows efficient access to the content and structure of PDFs.

### 🔍 Heading Detection Strategy

1. **Text Block Parsing**:

   * We iterate through all text blocks on each page using PyMuPDF.
   * Extract bounding boxes, font sizes, and text strings.

2. **Font Size-Based Heuristics**:

   * Headings are detected based on **font size hierarchy** within a document.
   * We record all unique font sizes and cluster them into 3 levels: `H1`, `H2`, and `H3`.

3. **Line Position & Formatting**:

   * Headings are assumed to be top-aligned and often bold or centered.
   * Short length, sentence case, and absence of punctuation help in classification.

4. **Title Extraction**:

   * The largest font on the first page is assumed to be the document title.

5. **Hierarchy Assignment**:

   * Once font sizes are bucketed, each line is tagged with its appropriate level (`H1`, `H2`, `H3`) and page number.

6. **Offline Constraints**:

   * No external models or network calls.
   * Fully rule-based to comply with the ≤200MB constraint.

### 🧪 Testing

* Tested with various real-world PDFs (simple and complex).
* Validated against ground-truth outline schemas.

---

## ✅ Submission Checklist

* [x] Dockerfile with CPU-only, amd64-compatible image
* [x] PDF input handled from `/app/input`
* [x] JSON output written to `/app/output`
* [x] Works offline without internet access
* [x] No hardcoded filenames or file-specific rules
* [x] README includes approach and execution instructions

---


