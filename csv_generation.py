import re
import csv
import os
import glob
from collections import Counter
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLineHorizontal, LTChar


def is_bold(fontname: str) -> bool:
    return bool(re.search(r"Bold|Black|Semibold|BD", fontname or "", re.IGNORECASE))


def is_italic(fontname: str) -> bool:
    return bool(re.search(r"Italic|Oblique", fontname or "", re.IGNORECASE))


def has_numeric_prefix(text: str) -> bool:
    return bool(re.match(r"^(\d+\.|[IVX]+\.|[A-Za-z]\))", text.strip()))


def is_bulleted(text: str) -> bool:
    return bool(re.match(r"^[\s]*[\u2022\u2023\u25E6\u2023\*\-\u2024]+[\s]+", text))


def clean_text(text: str) -> str:
    text = re.sub(r"[\r\n\t]+", " ", text)
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


def extract_spans_from_pdf(pdf_path: str) -> list:
    spans = []
    for page in extract_pages(pdf_path):
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
                            "size": size,
                            "fontname": fontname,
                            "text": text,
                            "bulleted": int(is_bulleted(raw)),
                        }
                    )
    return spans


def process_pdfs(pdf_dir: str, output_csv: str):
    pdfs = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    if not pdfs:
        print(f"No PDFs found in {pdf_dir}")
        return
    fieldnames = [
        "size",
        "bold",
        "italic",
        "text_len",
        "num_prefix",
        "is_larger_than_common_font",
        "text_case",
        "is_bulleted",
        "text",
    ]
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
    for pdf in pdfs:
        spans = extract_spans_from_pdf(pdf)
        if not spans:
            with open(output_csv, "a", encoding="utf-8") as f:
                f.write("\n")
            continue
        common_size = Counter([s["size"] for s in spans]).most_common(1)[0][0]
        rows = []
        for s in spans:
            size, fn, text = s["size"], s["fontname"], s["text"]
            rows.append(
                {
                    "size": size,
                    "bold": int(is_bold(fn)),
                    "italic": int(is_italic(fn)),
                    "text_len": len(text),
                    "num_prefix": int(has_numeric_prefix(text)),
                    "is_larger_than_common_font": int(size > common_size),
                    "text_case": get_text_case(text),
                    "is_bulleted": s["bulleted"],
                    "text": text,
                }
            )
        with open(output_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerows(rows)
            f.write("\n")
        print(f"Processed {os.path.basename(pdf)}: {len(rows)} spans")
    print(f"All done. Features written to {output_csv}")


if __name__ == "__main__":
    pdf_dir = "pdfs"
    output_csv = "features.csv"
    process_pdfs(pdf_dir, output_csv)
