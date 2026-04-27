#!/usr/bin/env python3
"""Extract pages from PDF and save TOC/links metadata to JSON files."""

import fitz  # PyMuPDF
import argparse
import json
import math
import os
import re


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
        # Remap "page" field if present
        if "page" in d and page_mapping is not None:
            old_target = d["page"]
            if old_target in page_mapping:
                d["page"] = page_mapping[old_target] - 1  # 0-based
        return d
    return dest


def main():
    parser = argparse.ArgumentParser(description="Extract pages from PDF, save TOC/links to JSON")
    parser.add_argument("input", help="Input PDF file")
    parser.add_argument("-o", "--output", help="Output PDF file (default: input_extracted.pdf)")
    parser.add_argument("--pages", required=True, help="Pages to extract (1-based, e.g., '1,3,5-7')")
    args = parser.parse_args()

    input_pdf = args.input
    if not os.path.exists(input_pdf):
        print(f"Error: Input file '{input_pdf}' not found.")
        return

    # Determine output filename
    base_name = os.path.splitext(input_pdf)[0]
    output_pdf = args.output or f"{base_name}_extracted.pdf"
    toc_json = os.path.splitext(output_pdf)[0] + "_toc.json"
    links_json = os.path.splitext(output_pdf)[0] + "_links.json"

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
    page_mapping = {}
    new_page_num = 1
    for old_idx in sorted_pages:
        page_mapping[old_idx] = new_page_num
        new_page_num += 1

    # --- Record links from original pages ---
    original_links = {}
    for page_idx in sorted_pages:
        original_links[page_idx] = doc[page_idx].get_links()

    # --- Normalize link rects: shrink slightly, avoiding watermarks and hidden text ---
    SHRINK = 1
    WATERMARK_KEYWORDS = {
        "confidential", "for confidential", "confidentiality",
        "confidential information", "proprietary", "internal use only",
        "Confidential,Semidrive only",
    }
    for page_idx in original_links:
        page = doc[page_idx]
        words = page.get_text("words")
        word_rects = []
        for w in words:
            text = w[4].strip()
            if not text:
                continue
            lower_text = text.lower()
            if any(keyword in lower_text for keyword in WATERMARK_KEYWORDS):
                continue
            word_rects.append(fitz.Rect(w[:4]))

        for link in original_links[page_idx]:
            rect = link["from"]
            if link["kind"] != fitz.LINK_GOTO:
                link["from"] = fitz.Rect(
                    math.ceil(rect.x0), math.ceil(rect.y0),
                    math.floor(rect.x1), math.floor(rect.y1))
                continue

            shrunk = fitz.Rect(rect.x0 + SHRINK, rect.y0 + SHRINK,
                               rect.x1 - SHRINK, rect.y1 - SHRINK)
            matched = [wr for wr in word_rects if wr.intersects(shrunk)]
            if matched:
                word_rect = matched[0]
                for wr in matched[1:]:
                    word_rect |= wr
                adjusted_rect = fitz.Rect(
                    math.ceil(word_rect.x0), math.ceil(word_rect.y0),
                    math.floor(word_rect.x1), math.floor(word_rect.y1))
                if adjusted_rect.get_area() <= rect.get_area() * 2:
                    link["from"] = adjusted_rect
                else:
                    link["from"] = fitz.Rect(
                        math.ceil(rect.x0), math.ceil(rect.y0),
                        math.floor(rect.x1), math.floor(rect.y1))
            else:
                link["from"] = fitz.Rect(
                    math.ceil(rect.x0), math.ceil(rect.y0),
                    math.floor(rect.x1), math.floor(rect.y1))

    # --- Merge overlapping LINK_GOTO links with same target on the same page ---
    for page_idx in original_links:
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
                    merged_rect |= links[k]["from"]
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
    import csv
    toc_csv = os.path.splitext(output_pdf)[0] + "_toc.csv"
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
        page = doc[old_idx]
        words = page.get_text("words")
        page_links = []
        for link in original_links.get(old_idx, []):
            sl = serialize_link(link)
            # Remap GOTO page numbers
            if sl["kind"] == fitz.LINK_GOTO and sl.get("page", -1) >= 0:
                old_target = sl["page"]
                if old_target in page_mapping:
                    sl["page"] = page_mapping[old_target] - 1  # 0-based for insert_link
                else:
                    sl["page"] = -1  # target not in extracted pages
            # Extract text from link rect
            fr = sl.get("from", [])
            if len(fr) == 4:
                rect = fitz.Rect(fr)
                matched = [(w[1], w[0], w[4]) for w in words
                           if fitz.Rect(w[:4]).intersects(rect)]
                matched.sort()
                sl["_comment"] = " ".join(w[2] for w in matched).strip()
            page_links.append(sl)
        if page_links:
            links_data[str(new_pn)] = page_links

    with open(links_json, "w", encoding="utf-8") as f:
        json.dump(links_data, f, ensure_ascii=False, indent=2)
    total_links = sum(len(v) for v in links_data.values())
    print(f"Saved links: {links_json} ({total_links} links on {len(links_data)} pages)")

    # --- Save links to CSV ---
    links_csv = os.path.splitext(output_pdf)[0] + "_links.csv"
    # Pre-compute words per page for text extraction
    page_words = {}
    for old_idx in sorted_pages:
        page_words[old_idx] = doc[old_idx].get_text("words")
    with open(links_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Page", "Kind", "From(x0)", "From(y0)", "From(x1)", "From(y1)",
                          "TargetPage", "To(x)", "To(y)", "Zoom", "Name", "URI", "Text"])
        for page_str, link_list in links_data.items():
            old_idx = [k for k, v in page_mapping.items() if str(v) == page_str]
            old_idx = old_idx[0] if old_idx else None
            words = page_words.get(old_idx, []) if old_idx is not None else []
            word_rects = [fitz.Rect(w[:4]) for w in words]
            for ld in link_list:
                fr = ld.get("from", [])
                rect = fitz.Rect(fr) if len(fr) == 4 else None
                to = ld.get("to", [])
                # Extract text from link rect
                text = ""
                if rect and word_rects:
                    matched = [(w[1], w[0], w[4]) for w, wr in zip(words, word_rects)
                               if wr.intersects(rect)]
                    matched.sort()
                    text = " ".join(w[2] for w in matched).strip()
                writer.writerow([
                    int(page_str), ld.get("kind", ""),
                    fr[0] if len(fr) > 0 else "",
                    fr[1] if len(fr) > 1 else "",
                    fr[2] if len(fr) > 2 else "",
                    fr[3] if len(fr) > 3 else "",
                    ld.get("page", ""),
                    to[0] if len(to) > 0 else "",
                    to[1] if len(to) > 1 else "",
                    ld.get("zoom", ""),
                    ld.get("name", ""),
                    ld.get("uri", ""),
                    text
                ])
    print(f"Saved links CSV: {links_csv}")

    # Save page mapping for reference
    mapping_json = os.path.splitext(output_pdf)[0] + "_mapping.json"
    mapping_data = {str(old + 1): new for old, new in page_mapping.items()}
    with open(mapping_json, "w", encoding="utf-8") as f:
        json.dump(mapping_data, f, indent=2)

    doc.close()
    print("Done.")


if __name__ == "__main__":
    main()
