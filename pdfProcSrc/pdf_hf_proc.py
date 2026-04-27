import fitz  # PyMuPDF
import argparse
import os
import re

# Maximum TOC level to include (1=chapter, 2=section, 3=subsection, etc.)
MAX_TOC_LEVEL = 4

def clean_title(title):
    """Remove numbering from title (e.g., '1.1 Introduction' -> 'Introduction')"""
    # Match patterns like "1.", "1.1", "6.2.5" at the beginning
    pattern = r'^\d+(\.\d+)*\s+'
    return re.sub(pattern, '', title).strip()

def renumber_toc_entries(toc_entries):
    """Renumber TOC entries to maintain consecutive numbering after deletions"""
    if not toc_entries:
        return toc_entries, {}

    # Group entries by level
    level_counters = {}  # level -> current counter
    renumbered_entries = []
    numbering_map = {}  # old_numbering -> new_numbering

    for level, title, page in toc_entries:
        # Extract old numbering from title
        old_numbering_match = re.match(r'^(\d+(?:\.\d+)*)', title.strip())
        old_numbering = old_numbering_match.group(1) if old_numbering_match else ""

        # Initialize counter for this level if not exists
        if level not in level_counters:
            level_counters[level] = 1
        else:
            level_counters[level] += 1

        # Reset counters for deeper levels
        for deeper_level in range(level + 1, 5):  # Include level 4
            if deeper_level in level_counters:
                level_counters[deeper_level] = 0

        # Build new numbering prefix
        numbering = []
        for l in range(1, level + 1):
            numbering.append(str(level_counters.get(l, 1)))
        numbering_prefix = '.'.join(numbering)

        # Remove old numbering and add new one
        clean_title_text = clean_title(title)
        if level == 4:
            # For level 4, don't add numbering prefix
            new_title = clean_title_text
        else:
            new_title = f"{numbering_prefix} {clean_title_text}"

        # Store mapping for cross-references
        if old_numbering:
            numbering_map[old_numbering] = numbering_prefix

        renumbered_entries.append([level, new_title, page])

    return renumbered_entries, numbering_map

def parse_pages(pages_str):
    """Parse page specification like '1,3,5-7' into a set of page numbers (0-based)."""
    pages = set()
    for part in pages_str.split(','):
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-'))
            pages.update(range(start-1, end))  # Convert to 0-based
        else:
            pages.add(int(part) - 1)  # Convert to 0-based
    return pages

def update_cross_references(doc, numbering_map):
    """Update cross-references in the document text"""
    if not numbering_map:
        return

    # Common cross-reference patterns
    patterns = [
        r'\bsection\s+(\d+(?:\.\d+)*)\b',
        r'\bSection\s+(\d+(?:\.\d+)*)\b',
        r'\bchapter\s+(\d+(?:\.\d+)*)\b',
        r'\bChapter\s+(\d+(?:\.\d+)*)\b',
        r'\bfigure\s+(\d+(?:\.\d+)*)\b',
        r'\bFigure\s+(\d+(?:\.\d+)*)\b',
        r'\btable\s+(\d+(?:\.\d+)*)\b',
        r'\bTable\s+(\d+(?:\.\d+)*)\b',
        r'\bsee\s+section\s+(\d+(?:\.\d+)*)\b',
        r'\bsee\s+Section\s+(\d+(?:\.\d+)*)\b',
        r'\bsee\s+chapter\s+(\d+(?:\.\d+)*)\b',
        r'\bsee\s+Chapter\s+(\d+(?:\.\d+)*)\b',
    ]

    updated_count = 0

    for page in doc:
        for pattern in patterns:
            # Find all matches on the page
            text_instances = page.search_for(pattern)

            for inst in text_instances:
                # Extract the text around the match
                rect = fitz.Rect(inst)
                # Expand rectangle slightly to get more context
                expanded_rect = rect + (-10, -5, 10, 5)

                try:
                    page_text = page.get_textbox(expanded_rect)

                    # Find the numbering in the extracted text
                    match = re.search(pattern, page_text, re.IGNORECASE)
                    if match:
                        old_numbering = match.group(1)
                        if old_numbering in numbering_map:
                            new_numbering = numbering_map[old_numbering]

                            # Replace the old numbering with new one
                            updated_text = re.sub(r'\b' + re.escape(old_numbering) + r'\b', new_numbering, page_text)

                            # Remove the old text and add the updated text
                            page.add_redact_annot(expanded_rect, fill=(1, 1, 1))
                            page.apply_redactions()

                            # Insert updated text
                            page.insert_textbox(expanded_rect, updated_text, fontsize=10, color=(0, 0, 0))
                            updated_count += 1

                except Exception as e:
                    # Skip if text extraction fails
                    continue

    if updated_count > 0:
        print(f"Updated {updated_count} cross-references in the document")

    return updated_count
    """Parse page specification like '1,3,5-7' into a set of page numbers (0-based)."""
    pages = set()
    for part in pages_str.split(','):
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-'))
            pages.update(range(start-1, end))  # Convert to 0-based
        else:
            pages.add(int(part) - 1)  # Convert to 0-based
    return pages

def main():
    parser = argparse.ArgumentParser(description="Clean PDF by removing headers, footers, and watermarks")
    parser.add_argument("input", help="Input PDF file")
    parser.add_argument("-o", "--output", help="Output PDF file (default: input_rm.pdf)")
    parser.add_argument("--pages", help="Pages to process (1-based, e.g., '1,3,5-7'). If not specified, process all pages.")
    parser.add_argument("--crop", help="Crop margins in points: top,bottom,left,right (e.g., 50,70,20,20). 0 means no crop; default no crop.")
    parser.add_argument("--redact", action="store_true", help="Use true redaction (content removal) for header/footer rectangles instead of drawing white boxes")
    args = parser.parse_args()

    redact_mode = args.redact


    # Parse crop margins
    crop_margins = (0, 0, 0, 0)
    if args.crop:
        parts = [p.strip() for p in args.crop.split(',')]
        if len(parts) != 4:
            print("Error: --crop requires 4 values: top,bottom,left,right")
            return
        try:
            crop_margins = tuple(float(p) for p in parts)
        except ValueError:
            print("Error: --crop values must be numeric")
            return

    input_pdf = args.input
    if not os.path.exists(input_pdf):
        print(f"Error: Input file '{input_pdf}' not found.")
        return

    # Determine output filename
    if args.output:
        output_pdf = args.output + ".pdf"
    else:
        # Generate output filename with _rm suffix
        base, ext = os.path.splitext(input_pdf)
        output_pdf = f"{base}_rm{ext}"

    # Check if output file already exists (only when different from input)
    if output_pdf != input_pdf and os.path.exists(output_pdf):
        response = input(f"Output file '{output_pdf}' already exists. Overwrite? (y/N): ")
        if response.lower() not in ('y', 'yes'):
            print("Operation cancelled.")
            return

    # Open the PDF for reading
    doc = fitz.open(input_pdf)

    # Determine which pages to process
    if args.pages:
        pages_to_process = parse_pages(args.pages)
        total_pages = len(doc)
        pages_to_process = {p for p in pages_to_process if 0 <= p < total_pages}
        if not pages_to_process:
            print("Warning: No valid pages to process.")
            doc.close()
            return
    else:
        pages_to_process = set(range(len(doc)))

    print(f"Processing {len(pages_to_process)} pages out of {len(doc)} total pages.")

    # Create new PDF with selected pages (batch insert for better performance)
    new_doc = fitz.open()

    # Sort pages and create page ranges for batch insertion
    sorted_pages = sorted(pages_to_process)

    # Create mapping from old page numbers to new page numbers
    page_mapping = {}  # old_page_index -> new_page_number (1-based)
    new_page_num = 1

    # Group consecutive pages for batch insertion
    if sorted_pages:
        current_range_start = sorted_pages[0]
        current_range_end = sorted_pages[0]

        for page_idx in sorted_pages[1:]:
            if page_idx == current_range_end + 1:
                # Extend current range
                current_range_end = page_idx
            else:
                # Insert current range
                new_doc.insert_pdf(doc, from_page=current_range_start, to_page=current_range_end)
                # Update mapping for this range
                for i in range(current_range_start, current_range_end + 1):
                    page_mapping[i] = new_page_num
                    new_page_num += 1
                # Start new range
                current_range_start = page_idx
                current_range_end = page_idx

        # Insert final range
        new_doc.insert_pdf(doc, from_page=current_range_start, to_page=current_range_end)
        for i in range(current_range_start, current_range_end + 1):
            page_mapping[i] = new_page_num
            new_page_num += 1

    # Get original TOC and filter/update it
    original_toc = doc.get_toc()
    new_toc = []

    for level, title, old_page_num in original_toc:
        # Convert to 0-based index
        old_page_idx = old_page_num - 1

        # Check if this TOC entry's page is in our selected pages
        if old_page_idx in pages_to_process:
            # Update page number to new position
            new_page_num = page_mapping[old_page_idx]
            new_toc.append([level, title, new_page_num])

    # Renumber TOC entries to maintain consecutive numbering
    new_toc, numbering_map = renumber_toc_entries(new_toc)

    # Update cross-references in the new document
    update_cross_references(new_doc, numbering_map)

    # Set the updated TOC to the new document
    new_doc.set_toc(new_toc)

    # Write TOC to text file in pdfpages addtotoc format
    base_name = os.path.splitext(input_pdf)[0]
    toc_file = f"{base_name}_bm.txt"

    # Filter TOC entries by MAX_TOC_LEVEL and collect entries
    toc_entries = []
    for level, title, page in new_toc:
        if level <= MAX_TOC_LEVEL:
            # Title is already renumbered, use as-is for LaTeX TOC
            toc_title = title
            # Map level to LaTeX section type
            section_type = {1: "chapter", 2: "section", 3: "subsection", 4: "subsubsection"}.get(level, f"level{level}")
            # Create label from cleaned title (remove numbering for label)
            cleaned_title = clean_title(title)
            label = cleaned_title.lower().replace(' ', '-').replace(',', '').replace('.', '').replace('(', '').replace(')', '').replace(':', '').replace(';', '')
            toc_entries.append(f"{page},{section_type},{level},{toc_title},{label}")

            # Print to console with indentation
            indent = "  " * (level - 1)
            # print(f"{indent}{toc_title}  -> page {page}")

    # Write to file in single addtotoc format
    with open(toc_file, 'w', encoding='utf-8') as f:
        f.write("% pdfpages addtotoc entries for PDF Table of Contents\n")
        f.write(f"% MAX_TOC_LEVEL = {MAX_TOC_LEVEL}\n")
        f.write("% Usage: \\includepdf[addtotoc={")
        f.write(",\n                  ".join(toc_entries))
        f.write("}]{filename}\n\n")

        # Also write individual entries for reference
        f.write("% Individual entries:\n")
        for entry in toc_entries:
            f.write(f"% addtotoc={{{entry}}}\n")

    print(f"pdfpages addtotoc entries written to: {toc_file}")
    print(f"Included TOC levels 1-{MAX_TOC_LEVEL}")

    # Process each page in the new document: clean headers/footers
    first_page = True  # Flag to print dimensions only once
    page_counter = 1
    for page in new_doc:
        W = page.rect.width
        H = page.rect.height

        if first_page:  # Only print for first page
            print(f"Page dimensions: {W} x {H}")
            first_page = False

        # ===== Regions to be erased (adjust as needed) =====

        # Header area (top of page) - precise coverage without extending beyond content
        header_rect = fitz.Rect(0, 0, W, 70)

        # Footer area (bottom of page) - precise coverage without extending beyond content
        footer_rect = fitz.Rect(0, H - 70, W, H)

        if redact_mode:
            # Method for PyMuPDF 1.22.5: use redaction first, then minimal overlay
            for rect in (header_rect, footer_rect):
                # Apply redaction to remove content
                page.add_redact_annot(rect, fill=None)
            page.apply_redactions()
        else:
            # Alternative method: use precise white overlay without any potential borders
            for rect in (header_rect, footer_rect):
                # Use only fill parameter to avoid any border artifacts
                page.draw_rect(rect, fill=(1, 1, 1))

        # ===== Add page number ===== (COMMENTED OUT)
        # Position page number in the center bottom of the page (compact)
        page_number_text = f"{page_counter}"  # Just the number to save space
        text_rect = fitz.Rect(W/2 - 20, H - 45, W/2 + 20, H - 25)

        # Add page number with smaller font for minimal size increase
        page.insert_textbox(text_rect, page_number_text,
                          fontsize=11,   # Smaller font
                          color=(0, 0, 0),  # Black text
                          align=1)  # Center alignment

        page_counter += 1

    # Save the new document with aggressive compression options to minimize file size
    new_doc.save(output_pdf,
                deflate=True,           # Enable general compression
                deflate_images=True,    # Compress images
                deflate_fonts=True,     # Compress fonts
                use_objstms=True,       # Use object streams for better compression
                compression_effort=9,   # Maximum compression effort
                garbage=4,              # Remove unused objects
                clean=True)             # Clean and optimize document structure

    print(f"Clean PDF with updated TOC and page numbers generated: {output_pdf}")
    print(f"Original pages: {len(doc)} -> Selected pages: {len(pages_to_process)} -> Final pages: {page_counter-1}")
    print("TOC has been updated to reflect new page numbering.")

    new_doc.close()
    doc.close()

if __name__ == "__main__":
    main()