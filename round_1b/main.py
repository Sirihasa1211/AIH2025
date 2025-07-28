import os
import argparse
from extract_sections import load_all_sections
from relevance_scoring import HybridScorer
from generate_output import generate_output_json, save_output_json

def main(input_dir, outlines_dir, output_file, persona, job_to_be_done):
    print("[1/4] Loading PDFs and outlines, extracting text sections...")
    docs = load_all_sections(input_dir, outlines_dir)
    if not docs:
        print("No documents processed. Exiting.")
        return

    print("[2/4] Preparing sections for scoring...")
    all_sections = []
    mapping = []  # List of (doc_name, section_index)
    for doc_name, data in docs.items():
        for idx, section in enumerate(data['sections']):
            all_sections.append(section)
            mapping.append((doc_name, idx))
    print(f"Total sections across all documents: {len(all_sections)}")

    print("[3/4] Computing hybrid relevance scores...")
    scorer = HybridScorer()
    query_text = f"{persona}. Job to be done: {job_to_be_done}"
    scored = scorer.score_sections(query_text, all_sections)

    scored_mapped = [(mapping[idx][0], mapping[idx][1], score) for idx, score, _, _ in scored]

    print("[4/4] Generating and saving output JSON...")
    output_json = generate_output_json(persona, job_to_be_done, docs, scored_mapped, top_k=5)
    save_output_json(output_json, output_file)
    print(f"Output saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Round 1B: Persona-Driven Document Intelligence")
    parser.add_argument("--input_dir", type=str, required=True, help="Folder containing PDFs")
    parser.add_argument("--outlines_dir", type=str, required=True, help="Folder containing 1A outlines JSON files")
    parser.add_argument("--output_file", type=str, required=True, help="Output JSON file path")
    parser.add_argument("--persona", type=str, required=True, help="Persona description text")
    parser.add_argument("--job_to_be_done", type=str, required=True, help="Job-to-be-done description text")

    args = parser.parse_args()
    main(args.input_dir, args.outlines_dir, args.output_file, args.persona, args.job_to_be_done)
