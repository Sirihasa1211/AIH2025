


# Challenge 1A: PDF Processing Solution

## Overview

This project provides a sample solution for **Challenge 1A** of the Adobe India Hackathon 2025. The objective is to extract **structured data** from PDF documents and output JSON files representing hierarchical outlines (sections/headings) with corresponding page numbers.

The solution must:

- Run **offline** without internet access
- Be **CPU-only**, compatible with AMD64 architecture
- Process all PDFs placed in the `input/` folder
- Output JSON files in `output/`, one per PDF with the same basename
- Be containerized using Docker for portability and reproducibility
- Complete processing within restrictions on execution time and memory usage

## Directory Structure

```
Challenge_1a/
├── Dockerfile           # Defines the container image
├── process_pdfs.py      # Main script processing PDFs
├── input/               # Place input PDF files here (read-only inside container)
├── output/              # JSON output files will be generated here
└── README.md            # This documentation file
```

## Build Command

Build the Docker image for AMD64 platform:

```
docker build --platform linux/amd64 -t pdf-processor .
```

## Run Command

Run the container to process all PDFs in the `input/` folder and output JSONs to `output/`:

```
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-processor
```

**Note:**  
- Input PDFs must be located in the local `input` folder before running.  
- Output JSON files will be written to the local `output` folder after processing.  
- `--network none` disables network access to enforce offline execution.

## Sample `process_pdfs.py` Behavior

- Scans `/app/input` for all PDF files.
- For each PDF, extracts hierarchical headings / outlines (currently a placeholder generating dummy data).
- Writes a JSON file per PDF in `/app/output` folder, matching the PDF filename but with `.json` extension.
- The JSON output conforms to the official schema required by the challenge.

## Expected Output Format

- JSON files use the same basename as input PDFs (e.g., `document1.pdf` → `document1.json`).
- Each JSON contains:
  - Document title
  - Outline array of headings with level (`H1`, `H2`, `H3`), text, and page number
- The output matches the schema located in `sample_dataset/schema/output_schema.json` (if provided).

## Critical Constraints

- Execution time: ≤ 10 seconds for a 50-page PDF
- Model size: ≤ 200MB (if ML models are used)
- Runtime: CPU-only AMD64 platform (no ARM-specific code)
- Memory: ≤ 16 GB RAM usage
- Network: No internet or external API calls allowed during execution

## Testing Your Solution Locally

Use the commands above to build and test with your PDF files placed in the `input/` folder.

Example:

```
mkdir input output
# place PDFs in input/
docker build --platform linux/amd64 -t pdf-processor .

docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-processor
```

## Validation Checklist

- [ ] All PDFs in `input/` directory are processed.
- [ ] JSON output files are generated with correct filenames in `output/`.
- [ ] Output JSON strictly matches the required schema.
- [ ] Execution completes within time and resource limits.
- [ ] No external network calls during runtime.
- [ ] Compatible with AMD64 Docker environments.
- [ ] Works with simple and complex PDFs.

---

## Notes

- This repository currently contains a placeholder processing script generating dummy outputs.
- For production/challenge submission, implement actual PDF parsing and outline extraction logic.
- Use open-source libraries like PyMuPDF (`fitz`) for offline PDF text and structure parsing.

## References

- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/en/latest/)
- [Docker Documentation](https://docs.docker.com/)
- Adobe India Hackathon 2025 official challenge page

---

# End of README
