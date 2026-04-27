#!/usr/bin/env python3
"""Print footer text blocks from specified PDF pages, with gap-based segmentation."""

import fitz  # PyMuPDF
import argparse
import math

BOTTOM_RATIO = 0.10
MIN_DISTANCE = 20.0
X_SHRINK = 1.0
Y_SHRINK = 1.0


def segment_words_by_gap(words, rect, min_dist):
    """Split words in rect into groups separated by horizontal gaps > min_dist."""
    matched = []
    for w in words:
        wr = fitz.Rect(w[:4])
        if wr.intersects(rect):
            matched.append((w[0], w[1], w[4], wr))  # x0, y0, text, word_rect

    if not matched:
        return []

    matched.sort(key=lambda m: m[0])
    groups = [[matched[0]]]
    for m in matched[1:]:
        prev_right = groups[-1][-1][3].x1
        if m[0] - prev_right > min_dist:
            groups.append([m])
        else:
            groups[-1].append(m)

    # Build result per group: bounding rect + text
    result = []
    for g in groups:
        gx0 = min(w[3].x0 for w in g)
        gy0 = min(w[3].y0 for w in g)
        gx1 = max(w[3].x1 for w in g)
        gy1 = max(w[3].y1 for w in g)
        text = " ".join(w[2] for w in g).strip()
        result.append((fitz.Rect(gx0, gy0, gx1, gy1), text))
    return result


def main():
    parser = argparse.ArgumentParser(description="Get footer text blocks from PDF pages")
    parser.add_argument("input", help="Input PDF file")
    parser.add_argument("--page", required=True, help="Page number(s) to inspect (1-based, e.g., '1' or '1,3,5-7')")
    parser.add_argument("--min-dist", type=float, default=MIN_DISTANCE,
                        help=f"Min horizontal gap to split segments (default: {MIN_DISTANCE})")
    args = parser.parse_args()

    doc = fitz.open(args.input)

    # Parse page numbers
    pages = set()
    for part in args.page.split(','):
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-'))
            pages.update(range(start, end + 1))
        else:
            pages.add(int(part))

    for pn in sorted(pages):
        if pn < 1 or pn > len(doc):
            print(f"Page {pn}: out of range (1-{len(doc)})")
            continue

        page = doc[pn - 1]
        H = page.rect.height
        blocks = page.get_text("blocks")
        words = page.get_text("words")
        threshold = H * (1 - BOTTOM_RATIO)

        print(f"\n=== Page {pn} ({page.rect.width:.0f} x {H:.0f}, footer zone: y > {threshold:.1f}) ===")

        for b in blocks:
            x0, y0, x1, y1, text, *_ = b
            text = text.strip()
            if not text:
                continue
            if y0 > threshold:
                block_rect = fitz.Rect(
                    math.ceil(x0) + X_SHRINK,
                    math.ceil(y0) + Y_SHRINK,
                    math.floor(x1) - X_SHRINK,
                    math.floor(y1) - Y_SHRINK
                )
                segments = segment_words_by_gap(words, block_rect, args.min_dist)
                if len(segments) <= 1:
                    print(f"  Rect({math.floor(x0)}, {math.floor(y0)}, {math.ceil(x1)}, {math.ceil(y1)}): {text}")
                else:
                    print(f"  Block Rect({math.floor(x0)}, {math.floor(y0)}, {math.ceil(x1)}, {math.ceil(y1)}) split into {len(segments)} segments:")
                    for seg_rect, seg_text in segments:
                        print(f"    Rect({math.floor(seg_rect.x0)}, {math.floor(seg_rect.y0)}, {math.ceil(seg_rect.x1)}, {math.ceil(seg_rect.y1)}): {seg_text}")

    doc.close()


if __name__ == "__main__":
    main()
