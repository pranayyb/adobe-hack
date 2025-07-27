import json
from datetime import datetime
from pathlib import Path
import sys

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

sys.path.append(str(Path(__file__).resolve().parent.parent))
from challenge_1a.main import process_pdf2


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "challenge_1a" / "input"
OUTPUT_DIR = BASE_DIR / "challenge_1b" / "output"
MODEL_PATH = "./minilm"


def flatten_outline(sections, doc_title):
    flat = []
    for sec in sections:
        flat.append(
            {
                "text": sec["text"],
                "page": sec["page"],
                "level": sec["level"],
                "refined_text": "",
                "document": doc_title,
            }
        )
        paragraphs = [
            sub["text"] for sub in sec.get("subsections", []) if "level" not in sub
        ]
        if paragraphs:
            flat[-1]["refined_text"] = " ".join(paragraphs).strip()
        for sub in sec.get("subsections", []):
            if "level" in sub:
                flat.extend(flatten_outline([sub], doc_title))
    return flat


def load_pdfs(input_dir):
    pdfs = list(input_dir.glob("*.pdf"))
    print(f"Processing {len(pdfs)} input PDFs...")
    return pdfs


def extract_sections(input_pdfs):
    all_sections = []
    for input_pdf in input_pdfs:
        result = process_pdf2(input_pdf)
        doc_title = input_pdf.name
        flat = flatten_outline(result["outline"], doc_title)
        all_sections.extend(flat)
    return all_sections


def rank_sections(all_sections, query, model_path):
    texts = [sec["text"] for sec in all_sections]
    refined_texts = [sec.get("refined_text", "") for sec in all_sections]

    model = SentenceTransformer(model_path)
    all_embeds = model.encode(
        texts + [query], convert_to_numpy=True, show_progress_bar=True
    )

    sec_embeds = all_embeds[:-1]
    qry_embed = all_embeds[-1].reshape(1, -1)
    sims = cosine_similarity(sec_embeds, qry_embed).flatten()

    for i, sec in enumerate(all_sections):
        sec["score"] = float(sims[i])

    ranked = sorted(all_sections, key=lambda x: -x["score"])
    for idx, sec in enumerate(ranked, start=1):
        sec["importance_rank"] = idx

    return ranked


def generate_output(ranked_sections, persona, job):
    output = {
        "metadata": {
            "input_documents": list(set(sec["document"] for sec in ranked_sections)),
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.utcnow().isoformat() + "Z",
        },
        "extracted_sections": [
            {
                "document": sec["document"],
                "section_title": sec["text"],
                "importance_rank": sec["importance_rank"],
                "page_number": sec["page"],
            }
            for sec in ranked_sections[:10]
        ],
        "subsection_analysis": [
            {
                "document": sec["document"],
                "refined_text": sec["refined_text"],
                "page_number": sec["page"],
            }
            for sec in ranked_sections[:10]
            if sec["refined_text"].strip()
        ],
    }
    return output


def save_output(output_data, output_dir, filename="challenge1b_output.json"):
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename
    output_file.write_text(json.dumps(output_data, indent=2))
    print(
        f"{output_file} written with {len(output_data['extracted_sections'])} sections."
    )


def main():
    persona = "A software engineer with expertise in agile methodologies"
    job = "Prepare a comprehensive analysis on agile testing methodologies, focusing on their evolution, current practices, and future trends"
    query = f"{persona}. Task: {job}"

    input_pdfs = load_pdfs(INPUT_DIR)
    all_sections = extract_sections(input_pdfs)
    ranked_sections = rank_sections(all_sections, query, MODEL_PATH)
    output = generate_output(ranked_sections, persona, job)
    save_output(output, OUTPUT_DIR)


if __name__ == "__main__":
    main()
