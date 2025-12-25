#!/usr/bin/env python3
"""
CMMC Compliance Strategy DOCX Generator - Converts markdown to DOCX with full content.
Supports embedded images. Shows progress bar during generation.
"""

import os
import re
import sys
import zipfile
from datetime import datetime

# Progress tracking
TOTAL_STEPS = 15
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

def get_image_size(image_path):
    """Get image dimensions from PNG file."""
    try:
        with open(image_path, 'rb') as f:
            # Check PNG signature
            sig = f.read(8)
            if sig[:8] != b'\x89PNG\r\n\x1a\n':
                return 5000000, 3750000  # Default size in EMUs (about 5.5" x 4")

            # Find IHDR chunk
            while True:
                chunk_len = int.from_bytes(f.read(4), 'big')
                chunk_type = f.read(4)
                if chunk_type == b'IHDR':
                    width = int.from_bytes(f.read(4), 'big')
                    height = int.from_bytes(f.read(4), 'big')
                    # Convert pixels to EMUs (914400 EMUs = 1 inch, assume 96 DPI)
                    # Scale to fit page width (max ~6 inches = 5486400 EMUs)
                    max_width_emu = 5486400
                    emu_per_px = 914400 / 96
                    width_emu = int(width * emu_per_px)
                    height_emu = int(height * emu_per_px)
                    # Scale if too wide
                    if width_emu > max_width_emu:
                        scale = max_width_emu / width_emu
                        width_emu = int(width_emu * scale)
                        height_emu = int(height_emu * scale)
                    return width_emu, height_emu
                else:
                    f.read(chunk_len + 4)  # Skip chunk data and CRC
                    if f.tell() > 1000:  # Safety limit
                        break
    except Exception as e:
        pass
    return 5000000, 3750000  # Default fallback

def parse_markdown(md_path):
    """Parse markdown file into structured content."""
    with open(md_path, 'r') as f:
        content = f.read()

    base_dir = os.path.dirname(md_path)
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

        # Images - ![alt](path)
        img_match = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)\s*$', line.strip())
        if img_match:
            alt_text = img_match.group(1)
            img_path = img_match.group(2)
            # Resolve relative path
            full_path = os.path.join(base_dir, img_path)
            if os.path.exists(full_path):
                elements.append(('image', (full_path, alt_text)))
            i += 1
            continue

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
        # Regular paragraph (including italics for captions)
        elif line.strip():
            text = line.strip()
            # Check if it's an italic caption line
            if text.startswith('*') and text.endswith('*') and not text.startswith('**'):
                elements.append(('caption', text[1:-1]))  # Remove surrounding asterisks
            else:
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

def create_caption_xml(text):
    """Create italic centered caption paragraph."""
    text = strip_markdown(text)
    return f'''<w:p><w:pPr><w:pStyle w:val="Caption"/><w:jc w:val="center"/></w:pPr>
<w:r><w:rPr><w:i/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r></w:p>'''

def create_image_xml(rel_id, width_emu, height_emu, alt_text=""):
    """Create drawing XML for an embedded image."""
    return f'''<w:p><w:pPr><w:jc w:val="center"/></w:pPr>
<w:r>
<w:drawing>
<wp:inline distT="0" distB="0" distL="0" distR="0"
xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
<wp:extent cx="{width_emu}" cy="{height_emu}"/>
<wp:effectExtent l="0" t="0" r="0" b="0"/>
<wp:docPr id="1" name="{escape_xml(alt_text)}" descr="{escape_xml(alt_text)}"/>
<wp:cNvGraphicFramePr>
<a:graphicFrameLocks noChangeAspect="1" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>
</wp:cNvGraphicFramePr>
<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:nvPicPr>
<pic:cNvPr id="0" name="{escape_xml(alt_text)}"/>
<pic:cNvPicPr/>
</pic:nvPicPr>
<pic:blipFill>
<a:blip r:embed="{rel_id}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>
<a:stretch><a:fillRect/></a:stretch>
</pic:blipFill>
<pic:spPr>
<a:xfrm>
<a:off x="0" y="0"/>
<a:ext cx="{width_emu}" cy="{height_emu}"/>
</a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
</pic:spPr>
</pic:pic>
</a:graphicData>
</a:graphic>
</wp:inline>
</w:drawing>
</w:r></w:p>'''

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
<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="Caption"/>
<w:pPr><w:spacing w:before="60" w:after="200"/><w:jc w:val="center"/></w:pPr>
<w:rPr><w:i/><w:sz w:val="20"/><w:color w:val="666666"/></w:rPr></w:style>
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

    # Collect images
    images = []
    image_rels = []
    rel_id_counter = 3  # Start after styles and numbering

    progress("Processing images...")
    for elem_type, content in elements:
        if elem_type == 'image':
            img_path, alt_text = content
            rel_id = f"rId{rel_id_counter}"
            rel_id_counter += 1
            ext = os.path.splitext(img_path)[1].lower()
            img_name = f"image{len(images) + 1}{ext}"
            width_emu, height_emu = get_image_size(img_path)
            images.append((img_path, img_name))
            image_rels.append((rel_id, img_name, width_emu, height_emu, alt_text))

    progress("Building document structure...")
    body_xml = ""

    progress("Processing content sections...")
    section_count = 0
    image_idx = 0
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
        elif elem_type == 'caption':
            body_xml += create_caption_xml(content)
        elif elem_type == 'image':
            if image_idx < len(image_rels):
                rel_id, _, width_emu, height_emu, alt_text = image_rels[image_idx]
                body_xml += create_image_xml(rel_id, width_emu, height_emu, alt_text)
                image_idx += 1
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
xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
<w:body>{body_xml}
<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>
<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>
</w:body></w:document>'''

    progress("Creating content types...")
    content_types = '''<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="png" ContentType="image/png"/>
<Default Extension="jpg" ContentType="image/jpeg"/>
<Default Extension="jpeg" ContentType="image/jpeg"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>'''

    progress("Creating relationships...")
    root_rels = '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

    # Build document relationships including images
    doc_rels_content = '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'''

    for rel_id, img_name, _, _, _ in image_rels:
        doc_rels_content += f'''
<Relationship Id="{rel_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{img_name}"/>'''

    doc_rels_content += '''
</Relationships>'''

    progress("Writing DOCX archive...")
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', root_rels)
        zf.writestr('word/_rels/document.xml.rels', doc_rels_content)
        zf.writestr('word/document.xml', doc_xml)
        zf.writestr('word/styles.xml', create_styles_xml())
        zf.writestr('word/numbering.xml', create_numbering_xml())

        # Add images
        progress("Embedding images...")
        for img_path, img_name in images:
            with open(img_path, 'rb') as img_file:
                zf.writestr(f'word/media/{img_name}', img_file.read())

    progress("Complete!")
    print(f"\n\nCreated: {output_path}")
    print(f"Size: {os.path.getsize(output_path):,} bytes")
    print(f"Images embedded: {len(images)}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    md_file = os.path.join(script_dir, "Furientis_CMMC_Compliance_Strategy.md")
    docx_file = os.path.join(script_dir, "Furientis_CMMC_Compliance_Strategy.docx")
    generate_docx(md_file, docx_file)
