import os
import re
import json
import pickle
import warnings
from collections import Counter
from pdfminer.high_level import extract_pages
from pathlib import Path
from pdfminer.layout import LTTextContainer, LTTextLineHorizontal, LTChar
import pandas as pd

warnings.filterwarnings("ignore")


def is_bold(fontname: str) -> bool:
    return bool(re.search(r"Bold|Black|Semibold|BD", fontname or "", re.IGNORECASE))


def is_italic(fontname: str) -> bool:
    return bool(re.search(r"Italic|Oblique", fontname or "", re.IGNORECASE))


def has_numeric_prefix(text: str) -> bool:
    return bool(re.match(r"^(\d+\.|[IVX]+\.|[A-Za-z]\))", text.strip()))


def is_bulleted(raw: str) -> bool:
    return bool(re.match(r"^[\s]*[\u2022\u2023\u25E6\*\-\u2024]+[\s]+", raw))


def clean_text(raw: str) -> str:
    text = re.sub(r"[\r\n\t]+", " ", raw)
    text = "".join(ch for ch in text if 32 <= ord(ch) <= 127)
    return re.sub(r" +", " ", text).strip()


def get_text_case(text: str) -> str:
    if text.isupper():
        return "upper"
    if text.islower():
        return "lower"
    if len(text) > 1 and text[0].isupper() and text[1:].islower():
        return "sentence"
    return "mixed"


def extract_spans(pdf_path: str):
    spans = []
    for page_num, page in enumerate(extract_pages(pdf_path), start=1):
        for element in page:
            if isinstance(element, LTTextContainer):
                for line in element:
                    if not isinstance(line, LTTextLineHorizontal):
                        continue
                    fontname, size = None, None
                    for obj in line:
                        if isinstance(obj, LTChar):
                            fontname, size = obj.fontname, round(obj.size, 1)
                            break
                    raw = line.get_text()
                    text = clean_text(raw)
                    if not text:
                        continue
                    spans.append(
                        {
                            "text": text,
                            "raw": raw,
                            "size": size,
                            "fontname": fontname,
                            "bold": is_bold(fontname),
                            "italic": is_italic(fontname),
                            "num_prefix": has_numeric_prefix(text),
                            "bulleted": is_bulleted(raw),
                            "page": page_num,
                        }
                    )
    return spans


def spans_to_df(spans):
    sizes = [s["size"] for s in spans if s["size"] is not None]
    common = Counter(sizes).most_common(1)[0][0] if sizes else 0
    data = []
    for s in spans:
        data.append(
            {
                "size": s["size"],
                "bold": int(s["bold"]),
                "italic": int(s["italic"]),
                "text_len": len(s["text"]),
                "num_prefix": int(s["num_prefix"]),
                "is_larger_than_common_font": int(s["size"] > common),
                "text_case": get_text_case(s["text"]),
                "is_bulleted": int(s["bulleted"]),
                "text": s["text"],
            }
        )
    return pd.DataFrame(data)


def classify_spans_with_model(spans, clf, case_encoder, label_encoder, scaler):
    df = spans_to_df(spans)
    if df.empty:
        return []
    df["text_case"] = case_encoder.transform(df["text_case"])
    features = [
        "size",
        "bold",
        "italic",
        "text_len",
        "num_prefix",
        "is_larger_than_common_font",
        "text_case",
        "is_bulleted",
    ]
    X = df[features]
    scaled_values = scaler.transform(X[["size", "text_len"]])
    X.loc[:, ["size", "text_len"]] = scaled_values.astype(float)
    preds = clf.predict(X)
    labels = label_encoder.inverse_transform(preds)
    return list(zip(spans, labels))


def process_pdf(pdf_path):
    with open("models/model.pkl", "rb") as f:
        clf = pickle.load(f)
    with open("models/le_case.pkl", "rb") as f:
        case_encoder = pickle.load(f)
    with open("models/le_label.pkl", "rb") as f:
        label_encoder = pickle.load(f)
    with open("models/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    spans = extract_spans(pdf_path)

    classified = classify_spans_with_model(
        spans, clf, case_encoder, label_encoder, scaler
    )

    outline = []
    for span, level in classified:
        if level.startswith("H"):
            outline.append({"level": level, "text": span["text"], "page": span["page"]})

    title = ""
    for span, level in classified:
        if span["bold"] and level == "H1":
            title = span["text"]
            break
    if not title and outline:
        title = outline[0]["text"]
    if not title:
        title = "Untitled Document"

    return {"title": title, "outline": outline}


def process_pdf2(pdf_path):
    base_dir = Path(__file__).resolve().parent
    model_dir = base_dir / "models"

    with open(model_dir / "model.pkl", "rb") as f:
        clf = pickle.load(f)
    with open(model_dir / "le_case.pkl", "rb") as f:
        case_encoder = pickle.load(f)
    with open(model_dir / "le_label.pkl", "rb") as f:
        label_encoder = pickle.load(f)
    with open(model_dir / "scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    spans = extract_spans(pdf_path)
    classified = classify_spans_with_model(
        spans, clf, case_encoder, label_encoder, scaler
    )

    outline = []
    stack = []
    paragraph_buffer = []
    current_page = None

    def flush_paragraph():
        nonlocal paragraph_buffer, current_page
        if paragraph_buffer and stack:
            paragraph_text = " ".join(paragraph_buffer).strip()
            stack[-1]["subsections"].append(
                {"text": paragraph_text, "page": current_page}
            )
            paragraph_buffer.clear()

    for span, label in classified:
        if label.startswith("H"):
            flush_paragraph()
            level = int(label[1])
            heading = {
                "level": label,
                "text": span["text"],
                "page": span["page"],
                "subsections": [],
            }

            while stack and int(stack[-1]["level"][1]) >= level:
                stack.pop()

            if stack:
                stack[-1]["subsections"].append(heading)
            else:
                outline.append(heading)

            stack.append(heading)

        elif label == "P":
            paragraph_buffer.append(span["text"])
            current_page = span["page"]
        else:
            flush_paragraph()

    flush_paragraph()

    title = next(
        (span["text"] for span, level in classified if span["bold"] and level == "H1"),
        "",
    )
    if not title and outline:
        title = outline[0]["text"]
    if not title:
        title = "Untitled Document"

    return {"title": title, "outline": outline}


def main():
    base_dir = Path(__file__).resolve().parent
    input_dir = base_dir / "input"
    output_dir = base_dir / "output"

    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_pdf = input_dir / filename
            output_json = output_dir / f"{Path(filename).stem}.json"
            result = process_pdf(str(input_pdf))
            with open(output_json, "w") as f:
                json.dump(result, f, indent=2)
            print(f"Processed {filename} → {output_json}")


if __name__ == "__main__":
    main()
