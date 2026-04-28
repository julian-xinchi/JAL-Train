#!/usr/bin/env python3
"""Extract pages from PDF and save TOC/links metadata to JSON files."""

import fitz  # PyMuPDF
import argparse
import csv
import json
import math
import os
import re

MAX_BODY_TEXT_HEIGHT = 35.0
LINK_RECT_SHRINK = 1


def parse_pages(pages_str):
    """Parse page specification like '1,3,5-7' into a set of page numbers (0-based)."""
    pages = set()
    for part in pages_str.split(','):
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-'))
            pages.update(range(start - 1, end))  # Convert to 0-based
        else:
            pages.add(int(part) - 1)  # Convert to 0-based
    return pages


def rect_to_list(r):
    """Convert fitz.Rect to JSON-serializable list. x0/y0 ceil, x1/y1 floor."""
    return [math.ceil(r.x0) * 1.0, math.ceil(r.y0) * 1.0,
            math.floor(r.x1) * 1.0, math.floor(r.y1) * 1.0]


def point_to_list(p):
    """Convert fitz.Point to JSON-serializable list. x/y ceil."""
    return [math.ceil(p.x) * 1.0, math.ceil(p.y) * 1.0]


def get_filtered_words(page, max_body_height=0, debug=False):
    """Get words from page, excluding watermark words.

    A word is filtered when ALL of:
      1. Its rect is contained in a non-horizontal span's bbox
      2. Its text is found within that span's text
      3. Its height > max_body_height (watermark text is large)
    """
    td = page.get_text("dict")
    # Collect (span_rect, span_text) from non-horizontal spans
    filter_items = []
    for block in td["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            if line.get("dir", (1, 0)) == (1, 0):
                continue
            for span in line["spans"]:
                filter_items.append((fitz.Rect(span["bbox"]), span["text"]))

    if debug and filter_items:
        print(f"  [DEBUG page={page.number + 1}] non-horizontal span filters: {len(filter_items)}")
        for i, (fr, st) in enumerate(filter_items):
            print(f"    filter[{i}]: rect={fr} text={st!r}")

    words = page.get_text("words")
    if not filter_items:
        return words

    result = []
    for w in words:
        wr = fitz.Rect(w[:4])
        wtext = w[4]
        wh = wr.height
        filtered = (wh > max_body_height
                    and any(fr.contains(wr) and wtext in st
                            for fr, st in filter_items))
        if debug and filtered:
            print(f"    FILTERED: Rect({w[0]:.1f},{w[1]:.1f},{w[2]:.1f},{w[3]:.1f})"
                  f" h={wh:.1f} text={wtext!r}")
        if not filtered:
            result.append(w)

    if debug:
        print(f"  [DEBUG page={page.number + 1}] words: {len(words)} total,"
              f" {len(words) - len(result)} filtered, {len(result)} kept")
    return result


def strip_title_numbering(title, level):
    """Strip numbering prefix from title if it matches the expected level depth.
    Level N expects N number groups: "1" for level 1, "1.1" for level 2, etc.
    """
    t = title.strip()
    match = re.match(r'^(\d+(?:\.\d+)*)\s+', t)
    if match:
        parts = match.group(1).split('.')
        if len(parts) == level:
            return t[match.end():]
    return t


def serialize_link(link):
    """Convert a link dict to JSON-serializable dict."""
    d = {"kind": link["kind"]}
    d["from"] = rect_to_list(link["from"])
    if link["kind"] == fitz.LINK_GOTO:
        d["page"] = link.get("page", -1)
        if "to" in link:
            d["to"] = point_to_list(link["to"])
        if "name" in link:
            d["name"] = link["name"]
        d["zoom"] = link.get("zoom", 0)
    elif link["kind"] == fitz.LINK_URI:
        d["uri"] = link.get("uri", "")
    elif link["kind"] == fitz.LINK_GOTOR:
        d["page"] = link.get("page", -1)
        d["file"] = link.get("file", "")
        if "to" in link:
            d["to"] = point_to_list(link["to"])
    elif link["kind"] == fitz.LINK_NAMED:
        d["name"] = link.get("name", "")
    return d


def serialize_dest(dest, page_mapping=None):
    """Convert TOC dest to JSON-serializable form."""
    if isinstance(dest, (int, float)):
        return dest
    if isinstance(dest, dict):
        d = dict(dest)
        if "to" in d and hasattr(d["to"], "x"):
            d["to"] = point_to_list(d["to"])
        if "page" in d and page_mapping is not None:
            old_target = d["page"]
            if old_target in page_mapping:
                d["page"] = page_mapping[old_target] - 1
        return d
    return dest


def extract_text_in_rect(words, rect):
    """Extract sorted text from words that intersect the given rect."""
    matched = [(w[1], w[0], w[4]) for w in words if fitz.Rect(w[:4]).intersects(rect)]
    matched.sort()
    return " ".join(w[2] for w in matched).strip()


def main():
    parser = argparse.ArgumentParser(description="Extract pages from PDF, save TOC/links to JSON")
    parser.add_argument("input", help="Input PDF file")
    parser.add_argument("-o", "--output", help="Output PDF file (default: input_extracted.pdf)")
    parser.add_argument("--pages", required=True, help="Pages to extract (1-based, e.g., '1,3,5-7')")
    parser.add_argument("--max-body-text-height", type=float, default=MAX_BODY_TEXT_HEIGHT,
                        help="Max body text height threshold; words taller than this in non-horizontal spans are filtered (0=disable)")
    parser.add_argument("--debug-page", type=int, default=0,
                        help="Page number to debug word filtering (1-based)")
    args = parser.parse_args()

    input_pdf = args.input
    if not os.path.exists(input_pdf):
        print(f"Error: Input file '{input_pdf}' not found.")
        return

    # Determine output filenames
    output_pdf = args.output or f"{os.path.splitext(input_pdf)[0]}_extracted.pdf"
    out_base = os.path.splitext(output_pdf)[0]
    toc_json = out_base + "_toc.json"
    links_json = out_base + "_links.json"

    # Check existing output files
    existing = [f for f in [output_pdf, toc_json, links_json] if os.path.exists(f)]
    if existing:
        print("The following files already exist:")
        for f in existing:
            print(f"  {f}")
        answer = input("Overwrite? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("Aborted.")
            return

    doc = fitz.open(input_pdf)
    pages_to_process = parse_pages(args.pages)

    # Validate page numbers
    total_pages = len(doc)
    invalid = [p + 1 for p in pages_to_process if p >= total_pages]
    if invalid:
        print(f"Error: Page(s) {invalid} exceed total pages ({total_pages}).")
        doc.close()
        return

    print(f"Extracting {len(pages_to_process)} pages out of {total_pages} total pages.")

    sorted_pages = sorted(pages_to_process)

    # --- Build page mapping (old 0-based idx -> new 1-based page number) ---
    page_mapping = {old: new for new, old in enumerate(sorted_pages, 1)}
    # Reverse mapping: new page number -> old 0-based idx
    rev_mapping = {str(v): k for k, v in page_mapping.items()}

    # --- Pre-compute filtered words per page (once) ---
    page_words = {}
    for old_idx in sorted_pages:
        page = doc[old_idx]
        page_words[old_idx] = get_filtered_words(
            page, args.max_body_text_height,
            debug=(page.number + 1 == args.debug_page))

    # --- Record links from original pages ---
    original_links = {page_idx: doc[page_idx].get_links() for page_idx in sorted_pages}

    # --- Normalize link rects: shrink slightly, then expand to cover actual words ---
    for page_idx in sorted_pages:
        word_rects = [fitz.Rect(w[:4]) for w in page_words[page_idx]]
        for link in original_links[page_idx]:
            if link["kind"] != fitz.LINK_GOTO:
                continue
            rect = link["from"]
            shrunk = fitz.Rect(rect.x0 + LINK_RECT_SHRINK, rect.y0 + LINK_RECT_SHRINK,
                               rect.x1 - LINK_RECT_SHRINK, rect.y1 - LINK_RECT_SHRINK)
            matched = [wr for wr in word_rects if wr.intersects(shrunk)]
            if matched:
                union = matched[0]
                for wr in matched[1:]:
                    union |= wr
                link["from"] = fitz.Rect(
                    math.ceil(union.x0), math.ceil(union.y0),
                    math.floor(union.x1), math.floor(union.y1))

    # --- Merge overlapping LINK_GOTO links with same target on the same page ---
    for page_idx in sorted_pages:
        links = original_links[page_idx]
        merged = []
        used = [False] * len(links)
        for i, link in enumerate(links):
            if used[i] or link["kind"] != fitz.LINK_GOTO:
                continue
            group = [i]
            used[i] = True
            ri = link["from"]
            target = link.get("page", -1)
            name = link.get("name")
            to_point = link.get("to")
            for j in range(i + 1, len(links)):
                if used[j] or links[j]["kind"] != fitz.LINK_GOTO:
                    continue
                rj = links[j]["from"]
                same_target = (target >= 0 and links[j].get("page", -1) == target) or \
                              (not name and links[j].get("name") == name)
                same_pos = (to_point == links[j].get("to")) or \
                           (to_point and links[j].get("to") and
                            abs(to_point.x - links[j]["to"].x) < 1 and
                            abs(to_point.y - links[j]["to"].y) < 1)
                if same_target and same_pos and ri.intersects(rj):
                    group.append(j)
                    used[j] = True
            if len(group) > 1:
                merged_rect = links[group[0]]["from"]
                for k in group[1:]:
                    merged_rect = merged_rect | links[k]["from"]
                merged_link = dict(links[group[0]])
                merged_link["from"] = merged_rect
                merged.append(merged_link)
            else:
                merged.append(link)
        # Append non-GOTO links unchanged
        for i, link in enumerate(links):
            if not used[i]:
                merged.append(link)
        original_links[page_idx] = merged

    # --- Record TOC from original document ---
    original_toc = doc.get_toc(simple=False)

    # --- Extract pages to new PDF ---
    new_doc = fitz.open()

    # Group consecutive pages for batch insertion
    current_range_start = sorted_pages[0]
    current_range_end = sorted_pages[0]

    for page_idx in sorted_pages[1:]:
        if page_idx == current_range_end + 1:
            current_range_end = page_idx
        else:
            new_doc.insert_pdf(doc, from_page=current_range_start, to_page=current_range_end, links=False)
            current_range_start = page_idx
            current_range_end = page_idx

    # Insert final range
    new_doc.insert_pdf(doc, from_page=current_range_start, to_page=current_range_end, links=False)

    # Save PDF without TOC/links
    new_doc.save(output_pdf)
    new_doc.close()
    print(f"Saved extracted PDF: {output_pdf}")

    # --- Build and save TOC JSON ---
    toc_data = []
    for entry in original_toc:
        level, title, old_page_num = entry[0], entry[1], entry[2]
        old_page_idx = old_page_num - 1

        if old_page_idx in pages_to_process:
            new_pn = page_mapping[old_page_idx]
            clean = strip_title_numbering(title, level)
            dest = serialize_dest(entry[3], page_mapping) if len(entry) > 3 else 0
            toc_data.append([level, clean, new_pn, dest])

    with open(toc_json, "w", encoding="utf-8") as f:
        json.dump(toc_data, f, ensure_ascii=False, indent=2)
    print(f"Saved TOC: {toc_json} ({len(toc_data)} entries)")

    # --- Save TOC to CSV ---
    toc_csv = out_base + "_toc.csv"
    with open(toc_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Level", "Title", "Page", "Dest"])
        for entry in toc_data:
            writer.writerow([entry[0], entry[1], entry[2],
                             str(entry[3]) if len(entry) > 3 else ""])
    print(f"Saved TOC CSV: {toc_csv}")

    # --- Build and save links JSON ---
    links_data = {}
    for old_idx in sorted_pages:
        new_pn = page_mapping[old_idx]
        words = page_words[old_idx]
        page_links = []
        for link in original_links.get(old_idx, []):
            sl = serialize_link(link)
            if sl["kind"] == fitz.LINK_GOTO and sl.get("page", -1) >= 0:
                old_target = sl["page"]
                sl["page"] = page_mapping[old_target] - 1 if old_target in page_mapping else -1
            fr = sl.get("from", [])
            if len(fr) == 4:
                sl["_comment"] = extract_text_in_rect(words, fitz.Rect(fr))
            page_links.append(sl)
        if page_links:
            links_data[str(new_pn)] = page_links

    with open(links_json, "w", encoding="utf-8") as f:
        json.dump(links_data, f, ensure_ascii=False, indent=2)
    total_links = sum(len(v) for v in links_data.values())
    print(f"Saved links: {links_json} ({total_links} links on {len(links_data)} pages)")

    # --- Save links to CSV ---
    links_csv = out_base + "_links.csv"
    with open(links_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Page", "Kind", "From(x0)", "From(y0)", "From(x1)", "From(y1)",
                          "TargetPage", "To(x)", "To(y)", "Zoom", "Name", "URI", "Text"])
        for page_str, link_list in links_data.items():
            old_idx = rev_mapping.get(page_str)
            words = page_words.get(old_idx, []) if old_idx is not None else []
            for ld in link_list:
                fr = ld.get("from", [])
                rect = fitz.Rect(fr) if len(fr) == 4 else None
                to = ld.get("to", [])
                text = extract_text_in_rect(words, rect) if rect and words else ""
                fr = list(fr) + [""] * (4 - len(fr))
                to = list(to) + [""] * (2 - len(to))
                writer.writerow([
                    int(page_str), ld.get("kind", ""),
                    fr[0], fr[1], fr[2], fr[3],
                    ld.get("page", ""),
                    to[0], to[1],
                    ld.get("zoom", ""),
                    ld.get("name", ""),
                    ld.get("uri", ""),
                    text
                ])
    print(f"Saved links CSV: {links_csv}")

    # Save page mapping for reference
    mapping_json = out_base + "_mapping.json"
    mapping_data = {str(old + 1): new for old, new in page_mapping.items()}
    with open(mapping_json, "w", encoding="utf-8") as f:
        json.dump(mapping_data, f, indent=2)

    doc.close()
    print("Done.")


if __name__ == "__main__":
    main()
