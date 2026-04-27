#!/usr/bin/env python3
"""Restore TOC and links from JSON files to a PDF."""

import fitz  # PyMuPDF
import argparse
import re

# Keywords indicating appendix sections (lowercase, for matching level-1 titles)
APPENDIX_KEYWORDS = {
    "appendix",
    "annex",
}
import json
import os


def list_to_rect(lst):
    """Convert [x0, y0, x1, y1] to fitz.Rect."""
    return fitz.Rect(lst[0], lst[1], lst[2], lst[3])


def list_to_point(lst):
    """Convert [x, y] to fitz.Point."""
    return fitz.Point(lst[0], lst[1])


def deserialize_link(d):
    """Convert JSON dict back to a link dict suitable for insert_link()."""
    link = {"kind": d["kind"], "from": list_to_rect(d["from"])}

    if d["kind"] == fitz.LINK_GOTO:
        page = d.get("page", -1)
        if page >= 0:
            link["page"] = page
            link["to"] = list_to_point(d["to"]) if "to" in d else fitz.Point(0, 0)
            link["zoom"] = d.get("zoom", 0)
        elif "name" in d:
            link["name"] = d["name"]
    elif d["kind"] == fitz.LINK_URI:
        link["uri"] = d.get("uri", "")
    elif d["kind"] == fitz.LINK_GOTOR:
        link["page"] = d.get("page", -1)
        link["file"] = d.get("file", "")
        if "to" in d:
            link["to"] = list_to_point(d["to"])
    elif d["kind"] == fitz.LINK_NAMED:
        link["name"] = d.get("name", "")

    return link


def renumber_toc(toc_entries, number_appendix=False):
    """Add hierarchical numbering to TOC entries based on level."""
    counters = {}
    in_appendix = False
    appendix_counters = {}
    result = []
    for entry in toc_entries:
        level = entry[0]
        title = entry[1]
        page = entry[2]
        dest = entry[3] if len(entry) > 3 else 0

        # Detect appendix section (level 1 matching any keyword)
        if level == 1 and any(title.lower().startswith(kw) for kw in APPENDIX_KEYWORDS):
            in_appendix = True
            appendix_counters = {}

        if in_appendix and not number_appendix:
            result.append([level, title, page, dest])
            continue

        counters[level] = counters.get(level, 0) + 1
        # Reset deeper counters
        for deeper in range(level + 1, 10):
            counters.pop(deeper, None)

        parts = [str(counters.get(l, 1)) for l in range(1, level + 1)]
        prefix = '.'.join(parts)

        result.append([level, f"{prefix} {title}", page, dest])
    return result


def main():
    parser = argparse.ArgumentParser(description="Restore TOC/links from JSON to PDF")
    parser.add_argument("input", help="Input PDF (extracted pages without TOC/links)")
    parser.add_argument("--toc", help="TOC JSON file (default: {input}_toc.json)")
    parser.add_argument("--links", help="Links JSON file (default: {input}_links.json)")
    parser.add_argument("-o", "--output", help="Output PDF file (default: {input}_restored.pdf)")
    parser.add_argument("--number-appendix", action="store_true", help="Add numbering to Appendix sections")
    parser.add_argument("--pn", action="store_true", help="Add page numbers to output PDF")
    args = parser.parse_args()

    input_pdf = args.input
    if not os.path.exists(input_pdf):
        print(f"Error: Input file '{input_pdf}' not found.")
        return

    base = os.path.splitext(input_pdf)[0]
    toc_file = args.toc or f"{base}_toc.json"
    links_file = args.links or f"{base}_links.json"
    output_pdf = args.output or f"{base}_restored.pdf"

    # Check existing output file
    if os.path.exists(output_pdf):
        print(f"File already exists: {output_pdf}")
        answer = input("Overwrite? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("Aborted.")
            return

    # --- Load TOC ---
    toc_data = []
    if os.path.exists(toc_file):
        with open(toc_file, "r", encoding="utf-8") as f:
            toc_data = json.load(f)
        print(f"Loaded TOC: {toc_file} ({len(toc_data)} entries)")
    else:
        print(f"Warning: TOC file '{toc_file}' not found, skipping TOC.")

    # --- Renumber TOC ---
    if toc_data:
        toc_data = renumber_toc(toc_data, number_appendix=args.number_appendix)
        print(f"Renumbered TOC entries")

    # --- Load links ---
    links_data = {}
    if os.path.exists(links_file):
        with open(links_file, "r", encoding="utf-8") as f:
            links_data = json.load(f)
        total = sum(len(v) for v in links_data.values())
        print(f"Loaded links: {links_file} ({total} links on {len(links_data)} pages)")
    else:
        print(f"Warning: Links file '{links_file}' not found, skipping links.")

    # --- Open PDF and apply ---
    doc = fitz.open(input_pdf)

    # Apply TOC
    if toc_data:
        # set_toc accepts [level, title, page] or [level, title, page, dest]
        set_toc_list = []
        for entry in toc_data:
            row = [entry[0], entry[1], entry[2]]
            if len(entry) > 3:
                dest = entry[3]
                if isinstance(dest, (int, float)):
                    row.append(dest)
                elif isinstance(dest, dict):
                    # Extract y-coordinate if available, otherwise 0
                    if "to" in dest:
                        to = dest["to"]
                        row.append(to[1] if isinstance(to, list) else 0)
                    elif "y" in dest:
                        row.append(dest["y"])
                    # else: no dest added (3-element row)
            set_toc_list.append(row)
        # Append to existing TOC if present
        existing_toc = doc.get_toc()
        if existing_toc:
            print(f"Appending to existing TOC ({len(existing_toc)} entries)")
            set_toc_list = existing_toc + set_toc_list
        doc.set_toc(set_toc_list)
        print(f"Applied TOC: {len(set_toc_list)} entries")

    # Apply links
    if links_data:
        for page_num_str, link_list in links_data.items():
            page_idx = int(page_num_str) - 1  # Convert to 0-based
            if page_idx >= len(doc):
                print(f"Warning: Page {page_num_str} exceeds document, skipping.")
                continue
            page = doc[page_idx]
            # Delete any existing links first
            for link in reversed(page.get_links()):
                page.delete_link(link)
            # Insert links from JSON
            for ld in link_list:
                link = deserialize_link(ld)
                page.insert_link(link)
        print(f"Applied links on {len(links_data)} pages")

    # Add page numbers
    if args.pn:
        for i, page in enumerate(doc):
            W = page.rect.width
            H = page.rect.height
            text_rect = fitz.Rect(W / 2 - 20, H - 45, W / 2 + 20, H - 25)
            page.insert_textbox(text_rect, str(i + 1), fontsize=11,
                                color=(0, 0, 0), align=1)
        print(f"Added page numbers")

    doc.save(output_pdf,
            deflate=True,           # Enable general compression
            deflate_images=True,    # Compress images
            deflate_fonts=True,     # Compress fonts
            #use_objstms=True,       # Use object streams for better compression
            #compression_effort=9,   # Maximum compression effort
            garbage=4,              # Remove unused objects
            clean=True)             # Clean and optimize document structure
    doc.close()
    print(f"Saved restored PDF: {output_pdf}")


if __name__ == "__main__":
    main()
