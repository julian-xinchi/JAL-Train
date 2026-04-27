#!/usr/bin/env python3
"""Add page offset to TOC and links JSON files."""

import argparse
import json
import os
import fitz  # PyMuPDF


def offset_filename(path, offset):
    """Generate new filename: name_p3.json / name_m3.json"""
    base, ext = os.path.splitext(path)
    prefix = "p" if offset >= 0 else "m"
    return f"{base}_{prefix}{abs(offset)}{ext}"


def shift_toc(toc_data, offset):
    """Add offset to page numbers in TOC entries."""
    result = []
    for entry in toc_data:
        new_entry = list(entry)
        new_entry[2] = entry[2] + offset
        # Also offset dest["page"] if present
        if len(new_entry) > 3 and isinstance(new_entry[3], dict):
            if "page" in new_entry[3]:
                new_entry[3] = dict(new_entry[3])
                new_entry[3]["page"] = new_entry[3]["page"] + offset
        result.append(new_entry)
    return result


def shift_links(links_data, offset):
    """Add offset to page keys and GOTO target page numbers in links."""
    shifted = {}
    for page_str, link_list in links_data.items():
        new_page = int(page_str) + offset
        new_links = []
        for ld in link_list:
            d = dict(ld)
            if d.get("kind") == fitz.LINK_GOTO and d.get("page", -1) >= 0:
                d["page"] = d["page"] + offset
            new_links.append(d)
        shifted[str(new_page)] = new_links
    return shifted


def main():
    parser = argparse.ArgumentParser(description="Add page offset to TOC/links JSON files")
    parser.add_argument("--toc", help="TOC JSON file")
    parser.add_argument("--links", help="Links JSON file")
    parser.add_argument("--ofst", type=int, required=True, help="Page number offset to add: 3/-3")
    args = parser.parse_args()

    if not args.toc and not args.links:
        print("Error: Provide at least --toc or --links")
        return

    if args.toc:
        if not os.path.exists(args.toc):
            print(f"Error: '{args.toc}' not found.")
        else:
            with open(args.toc, "r", encoding="utf-8") as f:
                toc_data = json.load(f)
            toc_data = shift_toc(toc_data, args.ofst)
            out_file = offset_filename(args.toc, args.ofst)
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(toc_data, f, ensure_ascii=False, indent=2)
            print(f"Saved TOC: {out_file} (offset {args.ofst:+d})")

    if args.links:
        if not os.path.exists(args.links):
            print(f"Error: '{args.links}' not found.")
        else:
            with open(args.links, "r", encoding="utf-8") as f:
                links_data = json.load(f)
            links_data = shift_links(links_data, args.ofst)
            out_file = offset_filename(args.links, args.ofst)
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(links_data, f, ensure_ascii=False, indent=2)
            print(f"Saved links: {out_file} (offset {args.ofst:+d})")


if __name__ == "__main__":
    main()
