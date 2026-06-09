#!/usr/bin/env python3
"""Dump all block/line/span info for specified PDF pages to CSV."""

import csv
import fitz  # PyMuPDF
import argparse


COLUMNS = [
    "page", "page_width", "page_height",
    "block_idx", "block_type",
    "block_x0", "block_y0", "block_x1", "block_y1",
    "block_img_width", "block_img_height", "block_img_ext", "block_img_size",
    "line_idx",
    "line_x0", "line_y0", "line_x1", "line_y1",
    "line_wmode", "line_dir",
    "span_idx", "span_text",
    "span_x0", "span_y0", "span_x1", "span_y1",
    "span_font", "span_size", "span_color", "span_flags",
    "span_origin_x", "span_origin_y",
    "span_ascent", "span_descent",
]


def parse_pages(page_str, max_page):
    pages = set()
    for part in page_str.split(','):
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-'))
            pages.update(range(start, end + 1))
        else:
            pages.add(int(part))
    return sorted(p for p in pages if 1 <= p <= max_page)


def row_base(page_num, page_w, page_h, bi, block):
    bb = block["bbox"]
    return {
        "page": page_num,
        "page_width": round(page_w, 1),
        "page_height": round(page_h, 1),
        "block_idx": bi,
        "block_type": block["type"],
        "block_x0": round(bb[0], 1),
        "block_y0": round(bb[1], 1),
        "block_x1": round(bb[2], 1),
        "block_y1": round(bb[3], 1),
    }


def main():
    parser = argparse.ArgumentParser(description="Dump block/line/span structure of PDF pages to CSV")
    parser.add_argument("input", help="Input PDF file")
    parser.add_argument("--page", required=True, help="Page number(s) (1-based, e.g., '1' or '1,3,5-7')")
    parser.add_argument("-o", "--output", help="Output CSV file (default: <input>_structure.csv)")
    args = parser.parse_args()

    output = args.output or args.input.rsplit(".", 1)[0] + "_structure.csv"

    doc = fitz.open(args.input)
    pages = parse_pages(args.page, len(doc))

    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()

        for pn in pages:
            page = doc[pn - 1]
            pw, ph = page.rect.width, page.rect.height
            td = page.get_text("dict")

            for bi, block in enumerate(td["blocks"]):
                base = row_base(pn, pw, ph, bi, block)

                if block["type"] == 1:  # image block
                    base["block_img_width"] = block.get("width")
                    base["block_img_height"] = block.get("height")
                    base["block_img_ext"] = block.get("ext")
                    base["block_img_size"] = len(block.get("image", b""))
                    writer.writerow(base)
                    continue

                # text block
                for li, line in enumerate(block["lines"]):
                    lb = line["bbox"]
                    for si, span in enumerate(line["spans"]):
                        sb = span["bbox"]
                        row = dict(base)
                        row.update({
                            "line_idx": li,
                            "line_x0": round(lb[0], 1),
                            "line_y0": round(lb[1], 1),
                            "line_x1": round(lb[2], 1),
                            "line_y1": round(lb[3], 1),
                            "line_wmode": line.get("wmode"),
                            "line_dir": line.get("dir"),
                            "span_idx": si,
                            "span_text": span["text"],
                            "span_x0": round(sb[0], 1),
                            "span_y0": round(sb[1], 1),
                            "span_x1": round(sb[2], 1),
                            "span_y1": round(sb[3], 1),
                            "span_font": span.get("font"),
                            "span_size": span.get("size"),
                            "span_color": f"#{span.get('color', 0):06x}",
                            "span_flags": span.get("flags"),
                            "span_origin_x": round(span["origin"][0], 1),
                            "span_origin_y": round(span["origin"][1], 1),
                            "span_ascent": round(span.get("ascent", 0), 2),
                            "span_descent": round(span.get("descent", 0), 2),
                        })
                        writer.writerow(row)

    doc.close()
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
