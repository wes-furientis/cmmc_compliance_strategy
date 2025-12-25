#!/usr/bin/env python3
"""
CMMC Compliance Strategy PDF Generator - Converts markdown to PDF.
Uses only Python standard library. Shows progress bar.
"""

import os
import re

TOTAL_STEPS = 10
current_step = 0

def progress(msg):
    global current_step
    current_step += 1
    pct = int((current_step / TOTAL_STEPS) * 100)
    bar = "=" * (pct // 5) + ">" + " " * (20 - pct // 5)
    print(f"\r[{bar}] {pct:3d}% {msg[:40]:<40}", end="", flush=True)

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
        sizes = {1: 18, 2: 14, 3: 12, 4: 11}
        size = sizes.get(level, 11)
        self._check_page(size + 20)
        self.y -= 15
        escaped = self._escape(text)
        self.current_content.append(f"BT /F2 {size} Tf {self.margin} {self.y} Td ({escaped}) Tj ET")
        self.y -= size + 8

    def add_para(self, text, indent=0):
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        lines = self._wrap(text, 85 - indent//6)
        for line in lines:
            self._check_page(14)
            escaped = self._escape(line)
            x = self.margin + indent
            self.current_content.append(f"BT /F1 11 Tf {x} {self.y} Td ({escaped}) Tj ET")
            self.y -= 14
        self.y -= 4

    def add_bullet(self, text):
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

    pdf = SimplePDF()
    lines = content.split('\n')
    i = 0
    in_code = False
    code_buf = []
    in_table = False
    table_rows = []
    num_counter = 0

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
            pdf.add_para(line.strip())
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


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    md_file = os.path.join(script_dir, "Furientis_CMMC_Compliance_Strategy.md")
    pdf_file = os.path.join(script_dir, "Furientis_CMMC_Compliance_Strategy.pdf")
    parse_md_and_generate(md_file, pdf_file)
