#!/usr/bin/env python3
"""
CMMC Compliance Strategy DOCX Generator - Converts markdown to DOCX with full content.
Shows progress bar during generation.
"""

import os
import re
import sys
import zipfile
from datetime import datetime

# Progress tracking
TOTAL_STEPS = 12
current_step = 0

def progress(msg):
    global current_step
    current_step += 1
    pct = int((current_step / TOTAL_STEPS) * 100)
    bar = "=" * (pct // 5) + ">" + " " * (20 - pct // 5)
    print(f"\r[{bar}] {pct:3d}% {msg[:40]:<40}", end="", flush=True)

COLORS = {
    'primary': '000000',
    'heading1': '000000',
    'heading2': '1a1a1a',
    'heading3': '333333',
    'table_header_bg': 'e6e6e6',
    'table_border': 'cccccc',
}

def escape_xml(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def strip_markdown(text):
    """Remove markdown formatting from text."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.+?)\*', r'\1', text)  # Italic
    text = re.sub(r'__(.+?)__', r'\1', text)  # Bold alt
    text = re.sub(r'_(.+?)_', r'\1', text)  # Italic alt
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # Links
    text = re.sub(r'`([^`]+)`', r'\1', text)  # Inline code
    return text

def parse_markdown(md_path):
    """Parse markdown file into structured content."""
    with open(md_path, 'r') as f:
        content = f.read()

    elements = []
    lines = content.split('\n')
    i = 0
    in_code_block = False
    code_content = []
    in_table = False
    table_rows = []

    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.startswith('```'):
            if in_code_block:
                elements.append(('code', '\n'.join(code_content)))
                code_content = []
                in_code_block = False
            else:
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            code_content.append(line)
            i += 1
            continue

        # Tables
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
            if table_rows:
                elements.append(('table', table_rows))
            in_table = False
            table_rows = []

        # Headers
        if line.startswith('# '):
            elements.append(('h1', line[2:].strip()))
        elif line.startswith('## '):
            elements.append(('h2', line[3:].strip()))
        elif line.startswith('### '):
            elements.append(('h3', line[4:].strip()))
        elif line.startswith('#### '):
            elements.append(('h4', line[5:].strip()))
        # Bullets
        elif line.strip().startswith('- '):
            elements.append(('bullet', line.strip()[2:]))
        elif re.match(r'^\d+\.\s', line.strip()):
            elements.append(('numbered', re.sub(r'^\d+\.\s', '', line.strip())))
        # Horizontal rule
        elif line.strip() == '---':
            elements.append(('hr', ''))
        # Regular paragraph
        elif line.strip():
            # Handle bold/italic in text
            text = line.strip()
            elements.append(('para', text))

        i += 1

    # Handle trailing table
    if in_table and table_rows:
        elements.append(('table', table_rows))

    return elements

def create_paragraph_xml(text, style="Normal"):
    text = strip_markdown(text)
    return f'''<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>
<w:r><w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r></w:p>'''

def create_code_block_xml(text):
    lines = text.split('\n')
    xml = ""
    for line in lines:
        xml += f'''<w:p><w:pPr><w:pStyle w:val="Code"/></w:pPr>
<w:r><w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/><w:sz w:val="18"/></w:rPr>
<w:t xml:space="preserve">{escape_xml(line)}</w:t></w:r></w:p>'''
    return xml

def create_table_xml(rows):
    if not rows:
        return ""
    num_cols = len(rows[0])
    col_width = 9360 // num_cols

    xml = f'''<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/>
<w:tblBorders>
<w:top w:val="single" w:sz="4" w:color="{COLORS['table_border']}"/>
<w:left w:val="single" w:sz="4" w:color="{COLORS['table_border']}"/>
<w:bottom w:val="single" w:sz="4" w:color="{COLORS['table_border']}"/>
<w:right w:val="single" w:sz="4" w:color="{COLORS['table_border']}"/>
<w:insideH w:val="single" w:sz="4" w:color="{COLORS['table_border']}"/>
<w:insideV w:val="single" w:sz="4" w:color="{COLORS['table_border']}"/>
</w:tblBorders></w:tblPr><w:tblGrid>'''

    for _ in range(num_cols):
        xml += f'<w:gridCol w:w="{col_width}"/>'
    xml += '</w:tblGrid>'

    for idx, row in enumerate(rows):
        xml += '<w:tr>'
        for cell in row:
            shading = f'<w:shd w:val="clear" w:fill="{COLORS["table_header_bg"]}"/>' if idx == 0 else ''
            bold = '<w:b/>' if idx == 0 else ''
            cell_text = strip_markdown(str(cell))
            xml += f'''<w:tc><w:tcPr><w:tcW w:w="{col_width}" w:type="dxa"/>{shading}</w:tcPr>
<w:p><w:r><w:rPr>{bold}</w:rPr><w:t>{escape_xml(cell_text)}</w:t></w:r></w:p></w:tc>'''
        xml += '</w:tr>'

    xml += '</w:tbl>'
    return xml

def create_styles_xml():
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr>
<w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:styleId="Normal" w:default="1"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>
<w:pPr><w:jc w:val="center"/><w:spacing w:after="200"/></w:pPr>
<w:rPr><w:b/><w:sz w:val="56"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>
<w:pPr><w:spacing w:before="400" w:after="200"/><w:outlineLvl w:val="0"/></w:pPr>
<w:rPr><w:b/><w:sz w:val="36"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>
<w:pPr><w:spacing w:before="300" w:after="150"/><w:outlineLvl w:val="1"/></w:pPr>
<w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/>
<w:pPr><w:spacing w:before="200" w:after="100"/><w:outlineLvl w:val="2"/></w:pPr>
<w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading4"><w:name w:val="heading 4"/>
<w:pPr><w:spacing w:before="150" w:after="80"/></w:pPr>
<w:rPr><w:b/><w:sz w:val="22"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListBullet"><w:name w:val="List Bullet"/>
<w:pPr><w:numPr><w:numId w:val="1"/></w:numPr></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="ListNumber"><w:name w:val="List Number"/>
<w:pPr><w:numPr><w:numId w:val="2"/></w:numPr></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/>
<w:pPr><w:shd w:val="clear" w:fill="f5f5f5"/><w:spacing w:after="0"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/><w:sz w:val="18"/></w:rPr></w:style>
</w:styles>'''

def create_numbering_xml():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0">
<w:numFmt w:val="bullet"/><w:lvlText w:val="\u2022"/>
<w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl></w:abstractNum>
<w:abstractNum w:abstractNumId="1"><w:lvl w:ilvl="0">
<w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/>
<w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl></w:abstractNum>
<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
<w:num w:numId="2"><w:abstractNumId w:val="1"/></w:num>
</w:numbering>'''

def generate_docx(md_path, output_path):
    print(f"Generating DOCX from: {md_path}")

    progress("Parsing markdown...")
    elements = parse_markdown(md_path)

    progress("Building document structure...")
    body_xml = ""

    progress("Processing content sections...")
    section_count = 0
    for elem_type, content in elements:
        if elem_type == 'h1':
            body_xml += create_paragraph_xml(content, "Heading1")
            section_count += 1
            if section_count % 3 == 0:
                progress(f"Section {section_count}...")
        elif elem_type == 'h2':
            body_xml += create_paragraph_xml(content, "Heading2")
        elif elem_type == 'h3':
            body_xml += create_paragraph_xml(content, "Heading3")
        elif elem_type == 'h4':
            body_xml += create_paragraph_xml(content, "Heading4")
        elif elem_type == 'para':
            body_xml += create_paragraph_xml(content, "Normal")
        elif elem_type == 'bullet':
            body_xml += f'''<w:p><w:pPr><w:pStyle w:val="ListBullet"/>
<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr></w:pPr>
<w:r><w:t>{escape_xml(strip_markdown(content))}</w:t></w:r></w:p>'''
        elif elem_type == 'numbered':
            body_xml += f'''<w:p><w:pPr><w:pStyle w:val="ListNumber"/>
<w:numPr><w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr></w:pPr>
<w:r><w:t>{escape_xml(strip_markdown(content))}</w:t></w:r></w:p>'''
        elif elem_type == 'code':
            body_xml += create_code_block_xml(content)
        elif elem_type == 'table':
            body_xml += create_table_xml(content)
        elif elem_type == 'hr':
            body_xml += '''<w:p><w:pPr><w:pBdr>
<w:bottom w:val="single" w:sz="12" w:color="000000"/></w:pBdr></w:pPr></w:p>'''

    progress("Creating document XML...")
    doc_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<w:body>{body_xml}
<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>
<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>
</w:body></w:document>'''

    progress("Creating content types...")
    content_types = '''<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>'''

    progress("Creating relationships...")
    root_rels = '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

    doc_rels = '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>'''

    progress("Writing DOCX archive...")
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', root_rels)
        zf.writestr('word/_rels/document.xml.rels', doc_rels)
        zf.writestr('word/document.xml', doc_xml)
        zf.writestr('word/styles.xml', create_styles_xml())
        zf.writestr('word/numbering.xml', create_numbering_xml())

    progress("Complete!")
    print(f"\n\nCreated: {output_path}")
    print(f"Size: {os.path.getsize(output_path):,} bytes")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    md_file = os.path.join(script_dir, "Furientis_CMMC_Compliance_Strategy.md")
    docx_file = os.path.join(script_dir, "Furientis_CMMC_Compliance_Strategy.docx")
    generate_docx(md_file, docx_file)
