#!/usr/bin/env python3
"""Clean headers and footers from PDF pages using redaction."""

import fitz  # PyMuPDF
import argparse
import math
import os

# Header/footer detection ratios
TOP_RATIO = 0.08
BOTTOM_RATIO = 0.10
HF_EXPAND = 1  # points to expand each detected rect

# Hardcoded footer rects (adjust for your PDF)
FOOTER_RECTS = [
    # 'Copyright ...'
    fitz.Rect(162, 723, 455, 735),
    # 'Page X of Y'
    fitz.Rect(490, 744, 560, 757),
    # 'Confidential'
    fitz.Rect(285, 735, 328, 747),
]


def detect_hf_rects(page):
    """Detect header rects dynamically from text blocks in the top region."""
    H = page.rect.height
    blocks = page.get_text("blocks")
    rects = []
    for b in blocks:
        x0, y0, x1, y1, text, *_ = b
        if not text.strip():
            continue
        if y1 < H * TOP_RATIO:
            rects.append(fitz.Rect(
                math.floor(x0), math.floor(y0),
                math.ceil(x1), math.ceil(y1)))
    return rects


def main():
    parser = argparse.ArgumentParser(description="Clean headers/footers from PDF")
    parser.add_argument("input", help="Input PDF file")
    parser.add_argument("-o", "--output", help="Output PDF file (default: {input}_clean.pdf)")
    args = parser.parse_args()

    input_pdf = args.input
    if not os.path.exists(input_pdf):
        print(f"Error: Input file '{input_pdf}' not found.")
        return

    base = os.path.splitext(input_pdf)[0]
    output_pdf = args.output or f"{base}_clean.pdf"

    if os.path.exists(output_pdf):
        print(f"File already exists: {output_pdf}")
        answer = input("Overwrite? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("Aborted.")
            return

    doc = fitz.open(input_pdf)
    print(f"Processing {len(doc)} pages ({doc[0].rect.width:.0f} x {doc[0].rect.height:.0f})")

    for page_num, page in enumerate(doc, 1):
        # Detect header rects from text blocks
        hf_rects = detect_hf_rects(page)

        # Expand detected rects and add fixed footer rects
        ext_rects = [r + (-HF_EXPAND, -HF_EXPAND, HF_EXPAND, HF_EXPAND) for r in hf_rects]
        ext_rects.extend(FOOTER_RECTS)

        # Apply redaction
        for rect in ext_rects:
            page.add_redact_annot(rect, fill=None)
        page.apply_redactions()

    doc.save(output_pdf, deflate=True, deflate_images=True, deflate_fonts=True)
    doc.close()
    print(f"Saved: {output_pdf}")


if __name__ == "__main__":
    main()
