import datetime
import json

def generate_output_json(persona, job_to_be_done, docs_sections, scored_sections, top_k=5):
    """
    Generate final output JSON.

    scored_sections: list of tuples (doc_name, section_index, score)
    """
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    metadata = {
        "input_documents": list(docs_sections.keys()),
        "persona": persona,
        "job_to_be_done": job_to_be_done,
        "timestamp": timestamp
    }

    extracted_sections = []
    subsection_analysis = []

    for rank, (doc_name, section_idx, _) in enumerate(scored_sections[:top_k], start=1):
        section = docs_sections[doc_name]['sections'][section_idx]
        extracted_sections.append({
            "document": doc_name,
            "section_title": section['section_title'],
            "page": section['page_start'],
            "importance_rank": rank
        })

        refined_text = section['text'].replace('\n', ' ').strip()
        if len(refined_text) > 1000:
            refined_text = refined_text[:1000] + "..."

        subsection_analysis.append({
            "document": doc_name,
            "refined_text": refined_text,
            "page": section['page_start']
        })

    return {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

def save_output_json(output_data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
