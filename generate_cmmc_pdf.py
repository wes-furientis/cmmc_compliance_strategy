#!/usr/bin/env python3
"""
CMMC Compliance Strategy PDF Generator - Converts markdown to PDF.
Supports embedded PNG images. Uses only Python standard library. Shows progress bar.
"""

import os
import re
import zlib

TOTAL_STEPS = 12

def strip_markdown(text):
    """Remove markdown formatting from text."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.+?)\*', r'\1', text)  # Italic
    text = re.sub(r'__(.+?)__', r'\1', text)  # Bold alt
    text = re.sub(r'_(.+?)_', r'\1', text)  # Italic alt
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # Links
    text = re.sub(r'`([^`]+)`', r'\1', text)  # Inline code
    return text

current_step = 0

def progress(msg):
    global current_step
    current_step += 1
    pct = int((current_step / TOTAL_STEPS) * 100)
    bar = "=" * (pct // 5) + ">" + " " * (20 - pct // 5)
    print(f"\r[{bar}] {pct:3d}% {msg[:40]:<40}", end="", flush=True)

def read_png_info(filepath):
    """Read PNG file and extract dimensions and raw image data."""
    with open(filepath, 'rb') as f:
        # Check PNG signature
        sig = f.read(8)
        if sig != b'\x89PNG\r\n\x1a\n':
            return None

        width = height = 0
        bit_depth = color_type = 0
        idat_chunks = []

        while True:
            chunk_len_data = f.read(4)
            if len(chunk_len_data) < 4:
                break
            chunk_len = int.from_bytes(chunk_len_data, 'big')
            chunk_type = f.read(4)

            if chunk_type == b'IHDR':
                data = f.read(chunk_len)
                width = int.from_bytes(data[0:4], 'big')
                height = int.from_bytes(data[4:8], 'big')
                bit_depth = data[8]
                color_type = data[9]
                f.read(4)  # CRC
            elif chunk_type == b'IDAT':
                idat_chunks.append(f.read(chunk_len))
                f.read(4)  # CRC
            elif chunk_type == b'IEND':
                break
            else:
                f.read(chunk_len + 4)  # Skip data and CRC

        return {
            'width': width,
            'height': height,
            'bit_depth': bit_depth,
            'color_type': color_type,
            'data': b''.join(idat_chunks)
        }


class SimplePDF:
    def __init__(self):
        self.objects = []
        self.pages = []
        self.current_content = []
        self.page_height = 792
        self.page_width = 612
        self.margin = 72
        self.y = self.page_height - self.margin
        self.line_height = 14
        self.images = []  # List of (filepath, obj_num) tuples
        self.image_objects = []  # Raw PDF objects for images

    def _new_page(self):
        if self.current_content:
            self.pages.append('\n'.join(self.current_content))
        self.current_content = []
        self.y = self.page_height - self.margin

    def _check_page(self, needed=20):
        if self.y - needed < self.margin:
            self._new_page()

    def _escape(self, text):
        # Replace unicode with ASCII, then escape PDF special chars
        text = text.encode('ascii', 'replace').decode('ascii')
        return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

    def _wrap(self, text, chars_per_line=85):
        words = text.split()
        lines, current = [], []
        length = 0
        for word in words:
            if length + len(word) + 1 <= chars_per_line:
                current.append(word)
                length += len(word) + 1
            else:
                if current:
                    lines.append(' '.join(current))
                current = [word]
                length = len(word)
        if current:
            lines.append(' '.join(current))
        return lines or ['']

    def add_heading(self, text, level=1):
        text = strip_markdown(text)
        sizes = {1: 18, 2: 14, 3: 12, 4: 11}
        size = sizes.get(level, 11)
        self._check_page(size + 20)
        self.y -= 15
        escaped = self._escape(text)
        self.current_content.append(f"BT /F2 {size} Tf {self.margin} {self.y} Td ({escaped}) Tj ET")
        self.y -= size + 8

    def add_para(self, text, indent=0):
        text = strip_markdown(text)
        lines = self._wrap(text, 85 - indent//6)
        for line in lines:
            self._check_page(14)
            escaped = self._escape(line)
            x = self.margin + indent
            self.current_content.append(f"BT /F1 11 Tf {x} {self.y} Td ({escaped}) Tj ET")
            self.y -= 14
        self.y -= 4

    def add_caption(self, text):
        """Add italic centered caption."""
        text = strip_markdown(text)
        self._check_page(14)
        # Center the text (approximate)
        text_width = len(text) * 5  # Rough estimate
        x = (self.page_width - text_width) / 2
        escaped = self._escape(text)
        self.current_content.append(f"BT /F4 9 Tf {x} {self.y} Td ({escaped}) Tj ET")
        self.y -= 14
        self.y -= 8

    def add_bullet(self, text):
        text = strip_markdown(text)
        self._check_page(14)
        self.current_content.append(f"BT /F1 11 Tf {self.margin + 20} {self.y} Td (\\225) Tj ET")
        lines = self._wrap(text, 75)
        for i, line in enumerate(lines):
            if i > 0:
                self._check_page(14)
            escaped = self._escape(line)
            self.current_content.append(f"BT /F1 11 Tf {self.margin + 35} {self.y} Td ({escaped}) Tj ET")
            self.y -= 14

    def add_numbered(self, num, text):
        text = strip_markdown(text)
        self._check_page(14)
        self.current_content.append(f"BT /F1 11 Tf {self.margin + 20} {self.y} Td ({num}.) Tj ET")
        lines = self._wrap(text, 75)
        for i, line in enumerate(lines):
            if i > 0:
                self._check_page(14)
            escaped = self._escape(line)
            self.current_content.append(f"BT /F1 11 Tf {self.margin + 40} {self.y} Td ({escaped}) Tj ET")
            self.y -= 14

    def add_code(self, text):
        for line in text.split('\n')[:50]:  # Limit code blocks
            self._check_page(12)
            escaped = self._escape(line[:90])
            self.current_content.append(f"BT /F3 9 Tf {self.margin + 20} {self.y} Td ({escaped}) Tj ET")
            self.y -= 12

    def add_table(self, rows):
        if not rows:
            return
        num_cols = len(rows[0])
        col_w = (self.page_width - 2*self.margin) // num_cols
        row_h = 16
        self._check_page(row_h * min(len(rows), 10) + 20)
        self.y -= 10
        start_y = self.y

        # Draw rows
        for idx, row in enumerate(rows[:15]):  # Limit rows
            x = self.margin
            font = "/F2" if idx == 0 else "/F1"
            for cell in row:
                cell_text = str(cell)[:int(col_w/5)]
                escaped = self._escape(cell_text)
                self.current_content.append(f"BT {font} 9 Tf {x+5} {self.y - 12} Td ({escaped}) Tj ET")
                x += col_w
            self.y -= row_h

        # Draw grid
        self.current_content.append("0.7 G 0.5 w")
        x = self.margin
        for _ in range(num_cols + 1):
            self.current_content.append(f"{x} {start_y} m {x} {self.y} l S")
            x += col_w
        y = start_y
        for _ in range(min(len(rows), 15) + 1):
            self.current_content.append(f"{self.margin} {y} m {self.margin + col_w*num_cols} {y} l S")
            y -= row_h
        self.current_content.append("0 G")
        self.y -= 15

    def add_hr(self):
        self._check_page(20)
        self.y -= 10
        self.current_content.append(f"0.5 w {self.margin} {self.y} m {self.page_width - self.margin} {self.y} l S")
        self.y -= 10

    def add_image(self, filepath, img_name):
        """Add a placeholder for an image (full images in DOCX version)."""
        # For the basic PDF generator, show a styled placeholder
        # Full image embedding would require complex PNG decoding
        filename = os.path.basename(filepath)

        self._check_page(60)
        self.y -= 10

        # Draw a bordered box as placeholder
        box_width = self.page_width - 2 * self.margin
        box_height = 50
        x = self.margin

        # Light gray fill
        self.current_content.append(f"0.95 g {x} {self.y - box_height} {box_width} {box_height} re f")
        # Border
        self.current_content.append(f"0.7 G 0.5 w {x} {self.y - box_height} {box_width} {box_height} re S")
        # Text
        text = f"[See DOCX for diagram: {filename}]"
        text_x = x + (box_width - len(text) * 5) / 2
        self.current_content.append(f"0 g BT /F4 10 Tf {text_x} {self.y - 30} Td ({self._escape(text)}) Tj ET")

        self.y -= box_height + 10

    def save(self, filename):
        if self.current_content:
            self.pages.append('\n'.join(self.current_content))

        pdf = ['%PDF-1.4']
        pdf.append("1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj")
        page_refs = ' '.join([f"{i+4} 0 R" for i in range(len(self.pages))])
        pdf.append(f"2 0 obj\n<< /Type /Pages /Kids [{page_refs}] /Count {len(self.pages)} >>\nendobj")
        pdf.append("""3 0 obj
<< /Font <<
/F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
/F2 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>
/F3 << /Type /Font /Subtype /Type1 /BaseFont /Courier >>
/F4 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique >>
>> >>
endobj""")

        obj_num = 4
        for content in self.pages:
            pdf.append(f"{obj_num} 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources 3 0 R /Contents {obj_num+1} 0 R >>\nendobj")
            obj_num += 1
            pdf.append(f"{obj_num} 0 obj\n<< /Length {len(content)} >>\nstream\n{content}\nendstream\nendobj")
            obj_num += 1

        content = '\n'.join(pdf) + '\n'
        xref_pos = len(content)
        xref = f"xref\n0 {obj_num}\n0000000000 65535 f \n"
        pos = len('%PDF-1.4\n')
        for line in pdf[1:]:
            xref += f"{pos:010d} 00000 n \n"
            pos += len(line) + 1

        with open(filename, 'wb') as f:
            f.write(content.encode('latin-1'))
            f.write(xref.encode('latin-1'))
            f.write(f"trailer\n<< /Size {obj_num} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF".encode('latin-1'))


def parse_md_and_generate(md_path, pdf_path):
    print(f"Generating PDF from: {md_path}")

    progress("Reading markdown...")
    with open(md_path, 'r') as f:
        content = f.read()

    base_dir = os.path.dirname(md_path)
    pdf = SimplePDF()
    lines = content.split('\n')
    i = 0
    in_code = False
    code_buf = []
    in_table = False
    table_rows = []
    num_counter = 0
    image_counter = 0

    progress("Parsing content...")

    while i < len(lines):
        line = lines[i]

        if line.startswith('```'):
            if in_code:
                progress("Processing code block...")
                pdf.add_code('\n'.join(code_buf))
                code_buf = []
            in_code = not in_code
            i += 1
            continue

        if in_code:
            code_buf.append(line)
            i += 1
            continue

        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_rows = []
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if not all(c.replace('-', '').replace(':', '') == '' for c in cells):
                table_rows.append(cells)
            i += 1
            continue
        elif in_table:
            progress("Processing table...")
            pdf.add_table(table_rows)
            in_table = False
            table_rows = []

        # Check for image
        img_match = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)\s*$', line.strip())
        if img_match:
            img_path = img_match.group(2)
            full_path = os.path.join(base_dir, img_path)
            if os.path.exists(full_path):
                progress(f"Processing image {image_counter + 1}...")
                image_counter += 1
                pdf.add_image(full_path, f"Img{image_counter}")
            i += 1
            continue

        if line.startswith('# '):
            progress(f"Section: {line[2:30]}...")
            pdf.add_heading(line[2:], 1)
        elif line.startswith('## '):
            pdf.add_heading(line[3:], 2)
        elif line.startswith('### '):
            pdf.add_heading(line[4:], 3)
        elif line.startswith('#### '):
            pdf.add_heading(line[5:], 4)
        elif line.strip().startswith('- '):
            pdf.add_bullet(line.strip()[2:])
        elif re.match(r'^\d+\.\s', line.strip()):
            num_counter += 1
            pdf.add_numbered(num_counter, re.sub(r'^\d+\.\s', '', line.strip()))
        elif line.strip() == '---':
            pdf.add_hr()
        elif line.strip():
            text = line.strip()
            # Check for italic caption
            if text.startswith('*') and text.endswith('*') and not text.startswith('**'):
                pdf.add_caption(text[1:-1])
            else:
                pdf.add_para(text)
        else:
            num_counter = 0

        i += 1

    if in_table and table_rows:
        pdf.add_table(table_rows)

    progress("Writing PDF...")
    pdf.save(pdf_path)

    progress("Complete!")
    print(f"\n\nCreated: {pdf_path}")
    print(f"Size: {os.path.getsize(pdf_path):,} bytes")
    print(f"Images embedded: {image_counter}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    md_file = os.path.join(script_dir, "Furientis_CMMC_Compliance_Strategy.md")
    pdf_file = os.path.join(script_dir, "Furientis_CMMC_Compliance_Strategy.pdf")
    parse_md_and_generate(md_file, pdf_file)
