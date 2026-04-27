#!/usr/bin/env python3
"""Convert _toc.json to pdfpages addtotoc format and write to _bm.txt."""

import fitz  # PyMuPDF
import argparse
import json
import os
import re

PRT_TOC_LEVEL = 3

# Keywords indicating appendix sections (lowercase, for matching level-1 titles)
APPENDIX_KEYWORDS = {
    "appendix",
    "annex",
}


def clean_title(title):
    """Remove numbering from title (e.g., '1.1 Introduction' -> 'Introduction')"""
    pattern = r'^\d+(\.\d+)*\s+'
    title = re.sub(pattern, '', title).strip()
    return title


def format_title(title):
    already_wrapped = title.startswith('{') and title.endswith('}')

    if ',' in title and not already_wrapped:
        title = f'{{{title}}}'

    if '_' in title and not (r'\texorpdfstring' in title):
        latex_t = title.replace('_', r'\_')
        pdf_t = rf'\detokenize{{{title}}}'
        title = rf'\texorpdfstring{{{latex_t}}}{{{pdf_t}}}'

    return title


def renumber_toc(toc_entries, number_appendix=False):
    """Add hierarchical numbering to TOC entries based on level."""
    counters = {}
    in_appendix = False
    result = []
    for entry in toc_entries:
        level = entry[0]
        title = entry[1]
        page = entry[2]
        dest = entry[3] if len(entry) > 3 else 0

        # Detect appendix section (level 1 matching any keyword)
        if level == 1 and any(title.lower().startswith(kw) for kw in APPENDIX_KEYWORDS):
            in_appendix = True

        if in_appendix and not number_appendix:
            result.append([level, title, page, dest])
            continue

        counters[level] = counters.get(level, 0) + 1
        for deeper in range(level + 1, 10):
            counters.pop(deeper, None)

        parts = [str(counters.get(l, 1)) for l in range(1, level + 1)]
        prefix = '.'.join(parts)

        result.append([level, f"{prefix} {title}", page, dest])
    return result


def main():
    parser = argparse.ArgumentParser(description="Convert _toc.json to pdfpages addtotoc format")
    parser.add_argument("input", help="Input _toc.json file or base PDF path")
    parser.add_argument("-o", "--output", help="Output _bm.txt file (default: based on input)")
    parser.add_argument("--level", type=int, default=PRT_TOC_LEVEL,
                        help=f"Max TOC level to include (default: {PRT_TOC_LEVEL})")
    parser.add_argument("--number-appendix", action="store_true",
                        help="Add numbering to Appendix sections")
    args = parser.parse_args()

    # Determine toc json file
    input_path = args.input
    if input_path.endswith("_toc.json"):
        toc_file = input_path
    else:
        toc_file = f"{os.path.splitext(input_path)[0]}_toc.json"

    if not os.path.exists(toc_file):
        print(f"Error: TOC file '{toc_file}' not found.")
        return

    # Output file
    if args.output:
        bm_file = args.output
    else:
        bm_file = os.path.splitext(toc_file.replace("_toc.json", ""))[0] + "_bm.txt"

    # Load TOC
    with open(toc_file, "r", encoding="utf-8") as f:
        toc_data = json.load(f)
    print(f"Loaded TOC: {toc_file} ({len(toc_data)} entries)")

    # Renumber
    toc_data = renumber_toc(toc_data, number_appendix=args.number_appendix)
    print("Renumbered TOC entries")

    # Build addtotoc entries
    toc_entries = []
    for entry in toc_data:
        level, title, page = entry[0], entry[1], entry[2]
        if level > args.level:
            continue
        section_type = {1: "section", 2: "subsection", 3: "subsubsection",
                        4: "paragraph"}.get(level, f"level{level}")
        cleaned_title = clean_title(title)
        formatted_title = format_title(cleaned_title)
        label = cleaned_title.lower()\
                .replace(' ', '-')\
                .replace('_', '-')\
                .replace(',', '')\
                .replace('.', '')\
                .replace('(', '')\
                .replace(')', '')\
                .replace('{', '')\
                .replace('}', '')\
                .replace(':', '')\
                .replace(';', '')
        toc_entries.append(f"{page},{section_type},{level},{formatted_title},{label}")

    # Write _bm.txt
    with open(bm_file, 'w', encoding='utf-8') as f:
        f.write("% pdfpages addtotoc entries for PDF Table of Contents\n")
        f.write(f"% PRT_TOC_LEVEL = {args.level}\n")
        f.write("% Usage: \\includepdf[addtotoc={")
        f.write(",\n                  ".join(toc_entries))
        f.write("}]{filename}\n\n")

        f.write("% Individual entries:\n")
        for entry in toc_entries:
            f.write(f"% addtotoc={{{entry}}}\n")

    print(f"pdfpages addtotoc entries written to: {bm_file}")
    print(f"Included TOC levels 1-{args.level}")


if __name__ == "__main__":
    main()
