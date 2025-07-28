
# Challenge 1B — Persona-Driven Document Intelligence

## Overview

This project implements **Round 1B** of the Adobe India Hackathon 2025, building a persona-driven document intelligence pipeline. Given:

- PDF documents (same set as Round 1A)
- JSON outlines extracted from PDFs in Round 1A (headings with page numbers)
- A **persona** description text
- A **job-to-be-done (JTBD)** text

This solution extracts and ranks the most relevant sections (text chunks) from all PDFs based on semantic similarity and keyword relevance to the persona and job. It is fully offline and CPU-only, respecting tight resource constraints.

## Key Features and Constraints

- Processes multiple PDFs with their corresponding 1A outlines as input.
- Extracts logical sections using outline boundaries, not arbitrary pages.
- Uses offline embedding models (`all-MiniLM-L12-v2`) for semantic similarity scoring.
- Applies keyword extraction (via KeyBERT) to enhance relevance scoring.
- Outputs top ≥5 relevant sections ranked with metadata and cleaned text.
- Produces JSON output conforming strictly to challenge specifications.
- Runs entirely offline on CPU (AMD64), no internet or external APIs.
- Fits within a ≤1GB RAM embedding model footprint.
- Containerized with Docker for reproducibility and environment consistency.

## Directory Structure

```
Challenge_1b/
├── Dockerfile
├── requirements.txt
│
├── input/                  # Place your input PDFs here
│   ├── doc1.pdf
│   ├── doc2.pdf
│   └── ...
│
├── outlines/               # JSON outline files from Round 1A (one per PDF)
│   ├── doc1.json
│   ├── doc2.json
│   └── ...
│
├── output/                 # Final output JSON(s) will be saved here
│
├── extract_sections.py     # Extract section text using outlines
├── relevance_scoring.py    # Embedding + keyword based hybrid scoring
├── generate_output.py      # Format and save final JSON output
├── main.py                 # Main orchestration script
└── README.md               # This file
```

## Installation & Setup

If running locally (without Docker), ensure Python 3.8+ is installed.

Install dependencies with:

```
pip install -r requirements.txt
```

### `requirements.txt` contents:

```
pymupdf==1.22.5
sentence-transformers==2.2.2
keybert==0.7.0
scikit-learn==1.2.2
numpy==1.24.3
```

## Usage Instructions

### 1. Prepare Input

- Place all PDFs to process in the `input/` folder.
- Place all their corresponding Round 1A JSON outlines (same filenames with `.json` extension) inside the `outlines/` folder.
- Make sure each PDF has a matching, correctly formatted outline JSON.

### 2. Run the Solution

#### Locally (Example):

```
python main.py \
  --input_dir input \
  --outlines_dir outlines \
  --output_file output/results.json \
  --persona "Investment Analyst" \
  --job_to_be_done "Analyze revenue trends and market positioning strategies"
```

#### Via Docker:

Build Docker image:

```
docker build --platform linux/amd64 -t connecting-dots-1b:latest .
```

Run container with input/output mounts and persona/job specification:

```
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/outlines:/app/outlines \
  -v $(pwd)/output:/app/output \
  --network none \
  connecting-dots-1b:latest \
  --persona "Investment Analyst" \
  --job_to_be_done "Analyze revenue trends and market positioning strategies"
```

> **Note:** Use `${PWD}` or `%cd%` depending on your shell (Linux/macOS/Windows).

## Output Format

The output JSON file in `output/` follows this schema:

- **metadata**  
  Contains input filenames, persona, job-to-be-done, and a timestamp.

- **extracted_sections** (list)  
  Each entry has `document`, `section_title`, `page`, and `importance_rank`.

- **subsection_analysis** (list)  
  Each entry has `document`, `refined_text` (cleaned section text), and `page`.

### Example Output Snippet

```
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "Investment Analyst",
    "job_to_be_done": "Analyze revenue trends and market positioning strategies",
    "timestamp": "2025-07-28T17:30:45Z"
  },
  "extracted_sections": [
    {
      "document": "doc2.pdf",
      "section_title": "Financial Performance Overview",
      "page": 5,
      "importance_rank": 1
    }
    // ...
  ],
  "subsection_analysis": [
    {
      "document": "doc2.pdf",
      "refined_text": "The company’s revenue grew by 8% year-over-year, driven primarily by software sales...",
      "page": 5
    }
    // ...
  ]
}
```

## Validation Checklist

- [ ] All input PDFs in `input/` have matching outlines in `outlines/`.
- [ ] JSON output generated includes `metadata`, `extracted_sections`, and `subsection_analysis`.
- [ ] At least 5 top relevant sections are included, ranked by relevance.
- [ ] JSON output strictly follows the required schema.
- [ ] Execution runs offline without network access.
- [ ] Embedding models load locally and stay within ≤1GB RAM.
- [ ] Solution runs on CPU only and completes efficiently.
- [ ] Works on AMD64 Docker platforms (Windows/Linux/macOS).

## Performance and Best Practices

- Sections are extracted using outline boundaries to improve semantic context.
- Hybrid scoring balances semantic embeddings with keyword relevance for accuracy.
- Text cleaning removes noise for concise refined outputs.
- Models and scoring done offline using `sentence-transformers` and `KeyBERT`.
- Modular design for easy debugging and extensions (e.g., add local summarization if desired).

## Troubleshooting and Support

- Ensure all PDF and JSON filenames match exactly.
- Use Python 3.8+ and install exact package versions from `requirements.txt`.
- Validate JSON outlines against Round 1A output specifications.
- Check Docker mount paths if running containerized.
- Monitor memory usage if processing large documents.

## References

- [PyMuPDF (fitz) Documentation](https://pymupdf.readthedocs.io/en/latest/)
- [SentenceTransformers](https://www.sbert.net/)
- [KeyBERT](https://github.com/MaartenGr/KeyBERT)
- [Docker Documentation](https://docs.docker.com/)

## Contributors

- Adobe India Hackathon 2025 Team  
- Your Name / Team

If you need code samples, help with running, or integration advice, please open an issue or contact challenge support.

---
