#!/usr/bin/env python3
"""
CMMC Compliance Strategy DOCX Generator

Generates a professional Word document with Furientis branding using only
Python standard library. Creates valid Office Open XML (OOXML) format.

Furientis Brand Guidelines (adapted for print):
- Primary colors: Black text on white background (inverted from web)
- Typography: Arial, sans-serif
- Visual style: Minimalist, clean hierarchy, professional

Usage:
    python3 generate_cmmc_docx.py
"""

import os
import re
import zipfile
from xml.etree import ElementTree as ET
from datetime import datetime

# OOXML Namespaces
NAMESPACES = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
    'cp': 'http://schemas.openxmlformats.org/package/2006/content-types',
}

# Furientis Brand Colors (for print: inverted from web)
COLORS = {
    'primary': '000000',      # Black text
    'heading1': '000000',     # Black
    'heading2': '1a1a1a',     # Near black
    'heading3': '333333',     # Dark gray
    'accent': '0066cc',       # Blue accent for links/highlights
    'table_header': '000000', # Black table headers
    'table_header_bg': 'e6e6e6',  # Light gray background
    'table_border': 'cccccc', # Light gray borders
}


def create_content_types_xml():
    """Create [Content_Types].xml defining file types in the package."""
    xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
    <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
    <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
    <Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/>
    <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
    <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
    <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''
    return xml


def create_root_rels():
    """Create _rels/.rels - root relationships."""
    xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
    <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
    <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''
    return xml


def create_document_rels():
    """Create word/_rels/document.xml.rels."""
    xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
    <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
    <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable" Target="fontTable.xml"/>
    <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>'''
    return xml


def create_styles_xml():
    """Create word/styles.xml with Furientis branding."""
    xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:docDefaults>
        <w:rPrDefault>
            <w:rPr>
                <w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/>
                <w:sz w:val="22"/>
                <w:szCs w:val="22"/>
                <w:lang w:val="en-US"/>
            </w:rPr>
        </w:rPrDefault>
        <w:pPrDefault>
            <w:pPr>
                <w:spacing w:after="160" w:line="259" w:lineRule="auto"/>
            </w:pPr>
        </w:pPrDefault>
    </w:docDefaults>

    <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
        <w:name w:val="Normal"/>
        <w:qFormat/>
        <w:rPr>
            <w:color w:val="{COLORS['primary']}"/>
        </w:rPr>
    </w:style>

    <w:style w:type="paragraph" w:styleId="Title">
        <w:name w:val="Title"/>
        <w:basedOn w:val="Normal"/>
        <w:qFormat/>
        <w:pPr>
            <w:spacing w:before="480" w:after="240"/>
            <w:jc w:val="center"/>
        </w:pPr>
        <w:rPr>
            <w:b/>
            <w:sz w:val="56"/>
            <w:szCs w:val="56"/>
            <w:color w:val="{COLORS['heading1']}"/>
        </w:rPr>
    </w:style>

    <w:style w:type="paragraph" w:styleId="Subtitle">
        <w:name w:val="Subtitle"/>
        <w:basedOn w:val="Normal"/>
        <w:qFormat/>
        <w:pPr>
            <w:spacing w:before="120" w:after="360"/>
            <w:jc w:val="center"/>
        </w:pPr>
        <w:rPr>
            <w:i/>
            <w:sz w:val="28"/>
            <w:szCs w:val="28"/>
            <w:color w:val="{COLORS['heading2']}"/>
        </w:rPr>
    </w:style>

    <w:style w:type="paragraph" w:styleId="Heading1">
        <w:name w:val="heading 1"/>
        <w:basedOn w:val="Normal"/>
        <w:next w:val="Normal"/>
        <w:qFormat/>
        <w:pPr>
            <w:keepNext/>
            <w:keepLines/>
            <w:spacing w:before="480" w:after="240"/>
            <w:outlineLvl w:val="0"/>
        </w:pPr>
        <w:rPr>
            <w:b/>
            <w:sz w:val="36"/>
            <w:szCs w:val="36"/>
            <w:color w:val="{COLORS['heading1']}"/>
        </w:rPr>
    </w:style>

    <w:style w:type="paragraph" w:styleId="Heading2">
        <w:name w:val="heading 2"/>
        <w:basedOn w:val="Normal"/>
        <w:next w:val="Normal"/>
        <w:qFormat/>
        <w:pPr>
            <w:keepNext/>
            <w:keepLines/>
            <w:spacing w:before="360" w:after="160"/>
            <w:outlineLvl w:val="1"/>
        </w:pPr>
        <w:rPr>
            <w:b/>
            <w:sz w:val="28"/>
            <w:szCs w:val="28"/>
            <w:color w:val="{COLORS['heading2']}"/>
        </w:rPr>
    </w:style>

    <w:style w:type="paragraph" w:styleId="Heading3">
        <w:name w:val="heading 3"/>
        <w:basedOn w:val="Normal"/>
        <w:next w:val="Normal"/>
        <w:qFormat/>
        <w:pPr>
            <w:keepNext/>
            <w:keepLines/>
            <w:spacing w:before="280" w:after="120"/>
            <w:outlineLvl w:val="2"/>
        </w:pPr>
        <w:rPr>
            <w:b/>
            <w:sz w:val="24"/>
            <w:szCs w:val="24"/>
            <w:color w:val="{COLORS['heading3']}"/>
        </w:rPr>
    </w:style>

    <w:style w:type="paragraph" w:styleId="TOCHeading">
        <w:name w:val="TOC Heading"/>
        <w:basedOn w:val="Heading1"/>
        <w:qFormat/>
    </w:style>

    <w:style w:type="paragraph" w:styleId="ListBullet">
        <w:name w:val="List Bullet"/>
        <w:basedOn w:val="Normal"/>
        <w:pPr>
            <w:numPr>
                <w:numId w:val="1"/>
            </w:numPr>
            <w:spacing w:after="60"/>
            <w:ind w:left="720" w:hanging="360"/>
        </w:pPr>
    </w:style>

    <w:style w:type="paragraph" w:styleId="ListNumber">
        <w:name w:val="List Number"/>
        <w:basedOn w:val="Normal"/>
        <w:pPr>
            <w:numPr>
                <w:numId w:val="2"/>
            </w:numPr>
            <w:spacing w:after="60"/>
            <w:ind w:left="720" w:hanging="360"/>
        </w:pPr>
    </w:style>

    <w:style w:type="table" w:styleId="TableGrid">
        <w:name w:val="Table Grid"/>
        <w:basedOn w:val="TableNormal"/>
        <w:tblPr>
            <w:tblBorders>
                <w:top w:val="single" w:sz="4" w:space="0" w:color="{COLORS['table_border']}"/>
                <w:left w:val="single" w:sz="4" w:space="0" w:color="{COLORS['table_border']}"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{COLORS['table_border']}"/>
                <w:right w:val="single" w:sz="4" w:space="0" w:color="{COLORS['table_border']}"/>
                <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{COLORS['table_border']}"/>
                <w:insideV w:val="single" w:sz="4" w:space="0" w:color="{COLORS['table_border']}"/>
            </w:tblBorders>
        </w:tblPr>
    </w:style>

    <w:style w:type="table" w:styleId="TableNormal" w:default="1">
        <w:name w:val="Normal Table"/>
        <w:tblPr>
            <w:tblCellMar>
                <w:top w:w="0" w:type="dxa"/>
                <w:left w:w="108" w:type="dxa"/>
                <w:bottom w:w="0" w:type="dxa"/>
                <w:right w:w="108" w:type="dxa"/>
            </w:tblCellMar>
        </w:tblPr>
    </w:style>

    <w:style w:type="character" w:styleId="Strong">
        <w:name w:val="Strong"/>
        <w:rPr>
            <w:b/>
        </w:rPr>
    </w:style>

    <w:style w:type="character" w:styleId="Emphasis">
        <w:name w:val="Emphasis"/>
        <w:rPr>
            <w:i/>
        </w:rPr>
    </w:style>
</w:styles>'''
    return xml


def create_numbering_xml():
    """Create word/numbering.xml for bullet and numbered lists."""
    xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:abstractNum w:abstractNumId="0">
        <w:multiLevelType w:val="hybridMultilevel"/>
        <w:lvl w:ilvl="0">
            <w:start w:val="1"/>
            <w:numFmt w:val="bullet"/>
            <w:lvlText w:val="\u2022"/>
            <w:lvlJc w:val="left"/>
            <w:pPr>
                <w:ind w:left="720" w:hanging="360"/>
            </w:pPr>
            <w:rPr>
                <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default"/>
            </w:rPr>
        </w:lvl>
    </w:abstractNum>

    <w:abstractNum w:abstractNumId="1">
        <w:multiLevelType w:val="hybridMultilevel"/>
        <w:lvl w:ilvl="0">
            <w:start w:val="1"/>
            <w:numFmt w:val="decimal"/>
            <w:lvlText w:val="%1."/>
            <w:lvlJc w:val="left"/>
            <w:pPr>
                <w:ind w:left="720" w:hanging="360"/>
            </w:pPr>
        </w:lvl>
    </w:abstractNum>

    <w:num w:numId="1">
        <w:abstractNumId w:val="0"/>
    </w:num>

    <w:num w:numId="2">
        <w:abstractNumId w:val="1"/>
    </w:num>
</w:numbering>'''
    return xml


def create_settings_xml():
    """Create word/settings.xml."""
    xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:zoom w:percent="100"/>
    <w:defaultTabStop w:val="720"/>
    <w:characterSpacingControl w:val="doNotCompress"/>
    <w:compat>
        <w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>
    </w:compat>
</w:settings>'''
    return xml


def create_font_table_xml():
    """Create word/fontTable.xml."""
    xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:fonts xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:font w:name="Arial">
        <w:panose1 w:val="020B0604020202020204"/>
        <w:charset w:val="00"/>
        <w:family w:val="swiss"/>
        <w:pitch w:val="variable"/>
    </w:font>
    <w:font w:name="Times New Roman">
        <w:panose1 w:val="02020603050405020304"/>
        <w:charset w:val="00"/>
        <w:family w:val="roman"/>
        <w:pitch w:val="variable"/>
    </w:font>
    <w:font w:name="Symbol">
        <w:panose1 w:val="05050102010706020507"/>
        <w:charset w:val="02"/>
        <w:family w:val="roman"/>
        <w:pitch w:val="variable"/>
    </w:font>
</w:fonts>'''
    return xml


def create_core_properties_xml():
    """Create docProps/core.xml."""
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
                   xmlns:dc="http://purl.org/dc/elements/1.1/"
                   xmlns:dcterms="http://purl.org/dc/terms/"
                   xmlns:dcmitype="http://purl.org/dc/dcmitype/"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <dc:title>Furientis CMMC Level 2 Compliance Strategy</dc:title>
    <dc:subject>CMMC Compliance, Cybersecurity, DoD Contractors</dc:subject>
    <dc:creator>Furientis Inc.</dc:creator>
    <cp:keywords>CMMC, NIST 800-171, CUI, Compliance, Cybersecurity</cp:keywords>
    <dc:description>Comprehensive guide to CMMC certification, dual-echelon architecture, and operational excellence for defense contractors.</dc:description>
    <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
    <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
    <cp:category>Internal Use Only</cp:category>
</cp:coreProperties>'''
    return xml


def create_app_properties_xml():
    """Create docProps/app.xml."""
    xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
    <Application>Furientis Document Generator</Application>
    <Company>Furientis Inc.</Company>
    <AppVersion>1.0</AppVersion>
</Properties>'''
    return xml


def escape_xml(text):
    """Escape special XML characters."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    return text


def create_paragraph(text, style="Normal", bold=False, italic=False):
    """Create a paragraph element."""
    props = f'<w:pStyle w:val="{style}"/>'
    rprops = ""
    if bold:
        rprops += "<w:b/>"
    if italic:
        rprops += "<w:i/>"

    if rprops:
        rprops = f"<w:rPr>{rprops}</w:rPr>"

    return f'''<w:p>
        <w:pPr>{props}</w:pPr>
        <w:r>{rprops}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>
    </w:p>'''


def create_table(headers, rows, col_widths=None):
    """Create a table element with styled header row."""
    num_cols = len(headers)
    if col_widths is None:
        # Default to equal width columns (total 9360 DXA for letter size)
        col_width = 9360 // num_cols
        col_widths = [col_width] * num_cols

    # Table properties
    table_xml = f'''<w:tbl>
        <w:tblPr>
            <w:tblStyle w:val="TableGrid"/>
            <w:tblW w:w="9360" w:type="dxa"/>
            <w:tblBorders>
                <w:top w:val="single" w:sz="4" w:space="0" w:color="{COLORS['table_border']}"/>
                <w:left w:val="single" w:sz="4" w:space="0" w:color="{COLORS['table_border']}"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{COLORS['table_border']}"/>
                <w:right w:val="single" w:sz="4" w:space="0" w:color="{COLORS['table_border']}"/>
                <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{COLORS['table_border']}"/>
                <w:insideV w:val="single" w:sz="4" w:space="0" w:color="{COLORS['table_border']}"/>
            </w:tblBorders>
        </w:tblPr>
        <w:tblGrid>'''

    for width in col_widths:
        table_xml += f'<w:gridCol w:w="{width}"/>'

    table_xml += '</w:tblGrid>'

    # Header row
    table_xml += '<w:tr>'
    for i, header in enumerate(headers):
        table_xml += f'''<w:tc>
            <w:tcPr>
                <w:tcW w:w="{col_widths[i]}" w:type="dxa"/>
                <w:shd w:val="clear" w:color="auto" w:fill="{COLORS['table_header_bg']}"/>
            </w:tcPr>
            <w:p>
                <w:pPr><w:jc w:val="center"/></w:pPr>
                <w:r>
                    <w:rPr><w:b/><w:color w:val="{COLORS['table_header']}"/></w:rPr>
                    <w:t>{escape_xml(header)}</w:t>
                </w:r>
            </w:p>
        </w:tc>'''
    table_xml += '</w:tr>'

    # Data rows
    for row in rows:
        table_xml += '<w:tr>'
        for i, cell in enumerate(row):
            table_xml += f'''<w:tc>
                <w:tcPr>
                    <w:tcW w:w="{col_widths[i]}" w:type="dxa"/>
                </w:tcPr>
                <w:p>
                    <w:r>
                        <w:t>{escape_xml(str(cell))}</w:t>
                    </w:r>
                </w:p>
            </w:tc>'''
        table_xml += '</w:tr>'

    table_xml += '</w:tbl>'
    return table_xml


def create_bullet_list(items):
    """Create a bulleted list."""
    xml = ""
    for item in items:
        xml += f'''<w:p>
            <w:pPr>
                <w:pStyle w:val="ListBullet"/>
                <w:numPr>
                    <w:ilvl w:val="0"/>
                    <w:numId w:val="1"/>
                </w:numPr>
            </w:pPr>
            <w:r><w:t>{escape_xml(item)}</w:t></w:r>
        </w:p>'''
    return xml


def create_numbered_list(items):
    """Create a numbered list."""
    xml = ""
    for item in items:
        xml += f'''<w:p>
            <w:pPr>
                <w:pStyle w:val="ListNumber"/>
                <w:numPr>
                    <w:ilvl w:val="0"/>
                    <w:numId w:val="2"/>
                </w:numPr>
            </w:pPr>
            <w:r><w:t>{escape_xml(item)}</w:t></w:r>
        </w:p>'''
    return xml


def create_page_break():
    """Create a page break."""
    return '''<w:p>
        <w:r>
            <w:br w:type="page"/>
        </w:r>
    </w:p>'''


def create_horizontal_line():
    """Create a horizontal line."""
    return '''<w:p>
        <w:pPr>
            <w:pBdr>
                <w:bottom w:val="single" w:sz="12" w:space="1" w:color="000000"/>
            </w:pBdr>
        </w:pPr>
    </w:p>'''


def generate_document_content():
    """Generate the main document content."""

    # Start document body
    body = ""

    # ===== TITLE PAGE =====
    body += create_paragraph("FURIENTIS", "Title")
    body += create_paragraph("CMMC Level 2 Compliance Strategy", "Subtitle")
    body += create_paragraph("A Comprehensive Guide to CMMC Certification, Dual-Echelon Architecture, and Operational Excellence", "Subtitle")
    body += create_horizontal_line()
    body += create_paragraph("")
    body += create_paragraph("Version: 1.0", "Normal")
    body += create_paragraph("Date: December 2025", "Normal")
    body += create_paragraph("Prepared for: Furientis Leadership", "Normal")
    body += create_paragraph("Classification: Internal Use Only", "Normal")
    body += create_page_break()

    # ===== TABLE OF CONTENTS =====
    body += create_paragraph("Table of Contents", "Heading1")
    toc_items = [
        "1. Executive Summary",
        "2. CMMC Level 2 Requirements Overview",
        "3. Dual-Echelon Architecture",
        "4. Cloud Infrastructure Strategy",
        "5. IT Infrastructure Requirements",
        "6. Software Requirements",
        "7. Operational TTPs for Engineer Productivity",
        "8. Vendor Comparison",
        "9. Cost Estimates",
        "10. Implementation Roadmap",
        "11. Risk Assessment and Common Pitfalls",
        "12. Appendices"
    ]
    body += create_numbered_list(toc_items)
    body += create_page_break()

    # ===== SECTION 1: EXECUTIVE SUMMARY =====
    body += create_paragraph("1. Executive Summary", "Heading1")

    body += create_paragraph("Purpose", "Heading2")
    body += create_paragraph("This document provides Furientis with a comprehensive strategy for achieving Cybersecurity Maturity Model Certification (CMMC) Level 2 compliance while maintaining operational agility for both government and commercial work streams. As a startup pursuing Department of Defense (DoD) contracts involving Controlled Unclassified Information (CUI), Furientis must implement 110 security practices aligned with NIST SP 800-171 Rev. 2.")

    body += create_paragraph("Key Findings", "Heading2")
    body += create_paragraph("Compliance Landscape:", "Heading3")
    body += create_bullet_list([
        "CMMC 2.0 Phase 1 became effective November 10, 2025",
        "Level 2 certification requires third-party assessment by an accredited C3PAO",
        "Conditional certification available with 80% compliance score (180 days to remediate)",
        "Average preparation timeline: 6-18 months for organizations starting from scratch"
    ])

    body += create_paragraph("Strategic Recommendations:", "Heading3")
    body += create_numbered_list([
        "Implement a CUI Enclave Architecture - Isolate government work from commercial operations to reduce compliance scope and cost",
        "Adopt Microsoft 365 GCC High - The only Microsoft environment meeting DFARS 7012 paragraphs (c)-(g)",
        "Leverage AWS GovCloud - Utilize FedRAMP High-authorized infrastructure for compute, storage, and AI/ML workloads",
        "Establish Clear Separation - Physical and logical network segmentation between government and commercial operations"
    ])
    body += create_page_break()

    # ===== SECTION 2: CMMC LEVEL 2 REQUIREMENTS =====
    body += create_paragraph("2. CMMC Level 2 Requirements Overview", "Heading1")

    body += create_paragraph("What is CMMC?", "Heading2")
    body += create_paragraph("The Cybersecurity Maturity Model Certification (CMMC) is the DoD's verification mechanism to ensure that contractors implement adequate cybersecurity practices to protect sensitive information. CMMC 2.0, finalized in 2024 and enforced beginning November 2025, streamlined the original five-tier model into three levels:")

    # CMMC Levels Table
    body += create_table(
        headers=["Level", "Description", "Assessment Type", "Practices", "Data Type"],
        rows=[
            ["Level 1", "Foundational", "Annual Self-Assessment", "17", "FCI"],
            ["Level 2", "Advanced", "Third-Party (C3PAO)", "110", "CUI"],
            ["Level 3", "Expert", "Government-led (DCMA)", "110+", "Critical CUI"]
        ]
    )
    body += create_paragraph("")

    body += create_paragraph("Level 2 Requirements Detail", "Heading2")
    body += create_paragraph("CMMC Level 2 directly maps to NIST SP 800-171 Revision 2, requiring implementation of 110 security practices across 14 domains:")

    # Control Families Table
    body += create_table(
        headers=["Domain", "Abbrev", "Count", "Key Focus Areas"],
        rows=[
            ["Access Control", "AC", "22", "Least privilege, session management, remote access"],
            ["Awareness & Training", "AT", "3", "Security awareness, role-based training"],
            ["Audit & Accountability", "AU", "9", "Logging, audit review, audit protection"],
            ["Configuration Management", "CM", "9", "Baseline configs, change control"],
            ["Identification & Authentication", "IA", "11", "MFA, password policies, device auth"],
            ["Incident Response", "IR", "3", "IR capability, reporting, testing"],
            ["Maintenance", "MA", "6", "Controlled maintenance, remote maintenance"],
            ["Media Protection", "MP", "9", "Media handling, sanitization, transport"],
            ["Personnel Security", "PS", "2", "Screening, personnel actions"],
            ["Physical Protection", "PE", "6", "Physical access, visitor control"],
            ["Risk Assessment", "RA", "3", "Risk assessments, vulnerability scanning"],
            ["Security Assessment", "CA", "4", "Security assessments, POA&M"],
            ["System & Comms Protection", "SC", "16", "Boundary protection, encryption, CUI handling"],
            ["System & Info Integrity", "SI", "7", "Flaw remediation, malware protection"]
        ]
    )
    body += create_paragraph("")

    body += create_paragraph("Key Documentation Requirements", "Heading2")
    body += create_numbered_list([
        "System Security Plan (SSP) - Comprehensive description of security controls implementation",
        "Plan of Action and Milestones (POA&M) - Remediation plan for any gaps",
        "Network Diagram - Current and accurate network architecture",
        "Data Flow Diagrams - How CUI moves through your systems",
        "Policies and Procedures - Written policies for each control family",
        "Evidence of Implementation - Screenshots, logs, configurations proving control implementation"
    ])
    body += create_page_break()

    # ===== SECTION 3: DUAL-ECHELON ARCHITECTURE =====
    body += create_paragraph("3. Dual-Echelon Architecture", "Heading1")

    body += create_paragraph("Strategic Rationale", "Heading2")
    body += create_paragraph("Furientis operates in two distinct contexts: government contracts involving CUI and commercial/research projects without government data or funding. Implementing a dual-echelon architecture provides significant advantages:")

    body += create_table(
        headers=["Benefit", "Description"],
        rows=[
            ["Reduced Compliance Scope", "Only the government echelon requires CMMC controls, reducing overall cost and complexity"],
            ["Operational Flexibility", "Commercial work proceeds without compliance constraints"],
            ["Clear Accountability", "Distinct environments make evidence collection and audit trails simpler"],
            ["Risk Isolation", "A breach in one environment doesn't automatically compromise the other"],
            ["Cost Optimization", "Expensive GCC High licensing only for personnel handling CUI"]
        ]
    )
    body += create_paragraph("")

    body += create_paragraph("CUI Enclave Design Principles", "Heading2")
    body += create_paragraph("The government echelon functions as a CUI Enclave with the following characteristics:")

    body += create_paragraph("Definition (per CyberAB):", "Heading3")
    body += create_paragraph("A set of system resources that operate within the same security domain and that share the protection of a single, common, and continuous security perimeter.", italic=True)

    body += create_paragraph("Key Design Principles:", "Heading3")
    body += create_numbered_list([
        "Strict Boundary Definition - All CUI processing occurs within the enclave",
        "Data Flow Controls - No automated data transfer between echelons",
        "Access Control - Separate identity provider with MFA enforcement",
        "Monitoring and Audit - SIEM collecting logs from all enclave systems"
    ])

    body += create_paragraph("Personnel and Role Separation", "Heading2")
    body += create_table(
        headers=["Role Type", "Enclave Access", "GCC High License", "Training Required"],
        rows=[
            ["Government Project Engineers", "Full", "Yes (E3/E5)", "CMMC Awareness + Role-based"],
            ["Government Project Managers", "Full", "Yes (E3/E5)", "CMMC Awareness"],
            ["Commercial-only Engineers", "None", "No", "Basic Security Awareness"],
            ["IT Administrators", "Full (privileged)", "Yes (E5)", "CMMC + Privileged User"],
            ["Executive Leadership", "Limited (read)", "Yes (E3)", "CMMC Awareness"]
        ]
    )
    body += create_page_break()

    # ===== SECTION 4: CLOUD INFRASTRUCTURE =====
    body += create_paragraph("4. Cloud Infrastructure Strategy", "Heading1")

    body += create_paragraph("Cloud Provider Selection: AWS GovCloud", "Heading2")
    body += create_paragraph("For Furientis's government echelon, AWS GovCloud (US) is the recommended primary cloud infrastructure provider:")

    body += create_table(
        headers=["Factor", "AWS GovCloud Advantage"],
        rows=[
            ["FedRAMP Authorization", "FedRAMP High baseline - highest level for unclassified workloads"],
            ["AI/ML Capabilities", "Amazon Bedrock available with Claude, Llama, and other models"],
            ["GPU Compute", "Full range of NVIDIA GPU instances (P4d, P5, G5) for ML workloads"],
            ["Data Residency", "All data remains in US, operated by US persons on US soil"],
            ["ITAR/EAR Support", "Designed for export-controlled data handling"]
        ]
    )
    body += create_paragraph("")

    body += create_paragraph("AWS GovCloud Services for Furientis", "Heading2")

    body += create_paragraph("Compute Resources:", "Heading3")
    body += create_table(
        headers=["Service", "Use Case", "Instance Types"],
        rows=[
            ["EC2", "General compute, application hosting", "m5, c5, r5 families"],
            ["EC2 (GPU)", "ML training, inference", "p4d.24xlarge, g5.xlarge-48xlarge"],
            ["EKS", "Container orchestration", "Managed Kubernetes"],
            ["Lambda", "Serverless functions", "N/A"],
            ["AWS WorkSpaces", "Virtual desktops for remote access", "Various bundles"]
        ]
    )
    body += create_paragraph("")

    body += create_paragraph("AI/ML Services:", "Heading3")
    body += create_table(
        headers=["Service", "Availability in GovCloud", "Notes"],
        rows=[
            ["Amazon Bedrock", "Available", "Claude 3.5 Sonnet, Llama 3 models available"],
            ["Amazon SageMaker", "Full availability", "Model training, hosting, MLOps"],
            ["SageMaker JumpStart", "Available", "Pre-trained open-weight models"],
            ["AWS Trainium", "Coming 2026", "Custom AI accelerator chips"]
        ]
    )
    body += create_paragraph("")

    body += create_paragraph("Storage Services:", "Heading3")
    body += create_table(
        headers=["Service", "Use Case", "Encryption"],
        rows=[
            ["S3", "Object storage, data lakes", "SSE-S3, SSE-KMS (FIPS 140-2)"],
            ["EBS", "Block storage for EC2", "AES-256 encryption at rest"],
            ["EFS", "Shared file systems", "Encryption in transit and at rest"],
            ["FSx for Windows", "Windows file shares", "Integrates with AD"]
        ]
    )
    body += create_page_break()

    # ===== SECTION 5: IT INFRASTRUCTURE =====
    body += create_paragraph("5. IT Infrastructure Requirements", "Heading1")

    body += create_paragraph("Endpoint Requirements", "Heading2")
    body += create_paragraph("All endpoints accessing CUI must meet specific security requirements:")

    body += create_paragraph("Hardware Standards:", "Heading3")
    body += create_table(
        headers=["Component", "Requirement", "Notes"],
        rows=[
            ["Processor", "Modern x86-64 or ARM", "TPM 2.0 required for Windows 11"],
            ["TPM", "TPM 2.0", "Required for BitLocker, secure boot"],
            ["Storage", "SSD with hardware encryption", "Self-encrypting drives preferred"],
            ["Memory", "16GB+ recommended", "For security tools overhead"]
        ]
    )
    body += create_paragraph("")

    body += create_paragraph("Endpoint Security Stack:", "Heading3")
    body += create_table(
        headers=["Layer", "Solution", "Purpose"],
        rows=[
            ["OS Hardening", "CIS Benchmarks, STIG", "Baseline configuration"],
            ["Disk Encryption", "BitLocker (FIPS mode)", "Data at rest protection"],
            ["EDR/XDR", "CrowdStrike Falcon GovCloud", "Threat detection and response"],
            ["DLP", "Microsoft Purview DLP", "Prevent CUI exfiltration"],
            ["VPN", "Always-on VPN to enclave", "Encrypted tunnel"],
            ["Patch Management", "WSUS, Intune, or SCCM", "Timely security updates"]
        ]
    )
    body += create_paragraph("")

    body += create_paragraph("Identity and Access Management", "Heading2")
    body += create_table(
        headers=["Control", "Requirement", "Implementation"],
        rows=[
            ["3.5.1", "Identify users and devices", "Azure AD/Entra ID in GCC High"],
            ["3.5.2", "Authenticate users/devices", "MFA required for all access"],
            ["3.5.3", "Multi-factor authentication", "Microsoft Authenticator, FIDO2 keys"],
            ["3.5.7", "Password complexity", "14+ characters, complexity rules"],
            ["3.5.8", "Password reuse prevention", "Remember 24 passwords"],
            ["3.5.10", "Session lock", "15-minute inactivity timeout"]
        ]
    )
    body += create_page_break()

    # ===== SECTION 6: SOFTWARE REQUIREMENTS =====
    body += create_paragraph("6. Software Requirements", "Heading1")

    body += create_paragraph("Microsoft 365 Licensing", "Heading2")
    body += create_table(
        headers=["License", "Key Features", "Per User/Month (Est.)"],
        rows=[
            ["M365 E3", "Core productivity, basic security", "$35-40"],
            ["M365 E5", "Advanced security, Defender, eDiscovery", "$55-60"],
            ["E5 Security Add-on", "Add E5 security to E3 base", "$15-20"]
        ]
    )
    body += create_paragraph("")
    body += create_paragraph("Minimum Recommendation: M365 E3 for all CUI users + E5 Security add-on", bold=True)

    body += create_paragraph("Operating System Requirements", "Heading2")
    body += create_table(
        headers=["OS", "Version", "Notes"],
        rows=[
            ["Windows 11 Enterprise", "23H2+", "Recommended; required for new hardware"],
            ["Windows 10 Enterprise", "22H2", "Supported until Oct 2025"],
            ["Windows Server", "2019/2022", "For server workloads"],
            ["macOS", "Monterey (12) or later", "With Intune enrollment"],
            ["Linux", "RHEL 8/9, Ubuntu 22.04 LTS", "For development; requires additional controls"]
        ]
    )
    body += create_paragraph("")

    body += create_paragraph("Development Tools", "Heading2")
    body += create_table(
        headers=["Category", "Tool", "Compliance Notes"],
        rows=[
            ["IDE", "VS Code, Visual Studio, JetBrains", "Disable telemetry, no cloud sync for CUI projects"],
            ["Source Control", "GitHub Enterprise Server", "Self-hosted in GovCloud; or Azure DevOps Server"],
            ["CI/CD", "GitHub Actions (self-hosted)", "Runners in GovCloud"],
            ["Containers", "Docker, Podman", "Images scanned before deployment"],
            ["Kubernetes", "EKS in GovCloud, OpenShift", "Managed K8s in compliant environment"]
        ]
    )
    body += create_page_break()

    # ===== SECTION 7: OPERATIONAL TTPs =====
    body += create_paragraph("7. Operational TTPs for Engineer Productivity", "Heading1")

    body += create_paragraph("Development Workflow Best Practices", "Heading2")
    body += create_paragraph("The key to maintaining productivity is proper scoping. By creating a well-segmented CUI enclave, Furientis can significantly reduce in-scope assets.")

    body += create_paragraph("Practical Implementation:", "Heading3")
    body += create_numbered_list([
        "Segment Early, Segment Often - Use network segmentation and access controls to create isolated environments",
        "Define Clear Data Flows - SSP must map where CUI lives in systems and networks",
        "Implement Zones of Trust - Use VLANs, firewalls, and network separation tools"
    ])

    body += create_paragraph("Automation for Efficiency:", "Heading3")
    body += create_bullet_list([
        "Takes needless work off IT's shoulders",
        "Gives developers compliant resources faster",
        "Reduces pressure during assessments",
        "Handles repetitive tasks like configuration, testing, evidence collection, and reporting"
    ])

    body += create_paragraph("Managing the Boundary Between CUI and Non-CUI Work", "Heading2")
    body += create_paragraph("Common Scoping Pitfalls to Avoid:", "Heading3")
    body += create_table(
        headers=["Pitfall", "Impact", "Mitigation"],
        rows=[
            ["Over-scoping", "Unnecessary complexity and cost", "Only include systems that actually process/store CUI"],
            ["Under-scoping", "Non-compliance findings", "Thorough CUI flow analysis"],
            ["Missing data flows", "Compliance gaps", "Document all CUI movement"],
            ["Third-party services", "Surprise assessment scope", "Verify cloud provider FedRAMP status"]
        ]
    )
    body += create_page_break()

    # ===== SECTION 8: VENDOR COMPARISON =====
    body += create_paragraph("8. Vendor Comparison", "Heading1")

    body += create_paragraph("Managed Service Providers (MSPs) Specializing in CMMC", "Heading2")
    body += create_table(
        headers=["Provider", "Specialization", "Target Market"],
        rows=[
            ["Summit 7", "CMMC, Azure, GCC High", "DoD contractors, SMBs"],
            ["Coalfire", "CMMC, FedRAMP, FISMA", "Mid-large enterprises"],
            ["Pivot Point Security", "CMMC, GCC migration", "Small-mid contractors"],
            ["Mirai Security", "CMMC implementation", "SMB contractors"],
            ["Ariento", "CMMC managed security", "Defense contractors"]
        ]
    )
    body += create_paragraph("")

    body += create_paragraph("SIEM Solutions Comparison", "Heading2")
    body += create_table(
        headers=["Solution", "Deployment", "Best For"],
        rows=[
            ["Microsoft Sentinel", "Cloud (GCC High)", "Microsoft environments"],
            ["Splunk Enterprise Security", "On-prem/cloud", "Maximum customization"],
            ["Elastic SIEM", "Self-hosted/cloud", "Budget-conscious"],
            ["IBM QRadar", "On-prem/cloud", "Regulated industries"]
        ]
    )
    body += create_paragraph("")

    body += create_paragraph("EDR Solutions Comparison", "Heading2")
    body += create_table(
        headers=["Solution", "Annual Cost (per endpoint)", "Strengths"],
        rows=[
            ["CrowdStrike Falcon Go", "$60", "Industry leader, lightweight"],
            ["CrowdStrike Falcon Pro", "$100", "+ Firewall management"],
            ["SentinelOne Control", "$80", "AI/ML autonomous response"],
            ["Microsoft Defender P1", "Included in E5", "Native M365 integration"]
        ]
    )
    body += create_page_break()

    # ===== SECTION 9: COST ESTIMATES =====
    body += create_paragraph("9. Cost Estimates", "Heading1")

    body += create_paragraph("First-Year Cost Summary", "Heading2")
    body += create_table(
        headers=["Category", "Low", "Mid", "High"],
        rows=[
            ["GCC High Licensing (25 users)", "$6,600", "$10,800", "$21,600"],
            ["AWS GovCloud Infrastructure", "$7,200", "$15,000", "$30,000"],
            ["C3PAO Assessment", "$40,000", "$55,000", "$75,000"],
            ["MSSP Services", "$40,000", "$55,000", "$75,000"],
            ["EDR/Endpoint Protection", "$2,000", "$5,000", "$9,000"],
            ["SIEM Solution", "$8,000", "$15,000", "$25,000"],
            ["Training", "$10,000", "$18,000", "$30,000"],
            ["Consulting/Gap Assessment", "$30,000", "$50,000", "$80,000"],
            ["Additional Tools", "$20,000", "$35,000", "$60,000"],
            ["Hardware/One-time Upgrades", "$15,000", "$35,000", "$85,000"],
            ["TOTAL FIRST YEAR", "$178,800", "$293,800", "$490,600"]
        ]
    )
    body += create_paragraph("")

    body += create_paragraph("Three-Year Total Investment", "Heading2")
    body += create_table(
        headers=["Scenario", "3-Year Total", "Annual Average"],
        rows=[
            ["Low (Good Starting Posture)", "$366,318", "$122,106"],
            ["Mid (Typical)", "$596,318", "$198,773"],
            ["High (Significant Remediation)", "$960,718", "$320,239"]
        ]
    )
    body += create_paragraph("")

    body += create_paragraph("Cost Optimization Strategies", "Heading2")
    body += create_table(
        headers=["Strategy", "Potential Savings", "Implementation"],
        rows=[
            ["Hybrid GCC High", "30-50% on licensing", "Only CUI users on GCC High"],
            ["Right-Size Cloud", "20-30% on cloud", "Reserved instances, auto-scaling"],
            ["Leverage Microsoft Stack", "$5,000-15,000/year", "Use included Defender, Sentinel"],
            ["Phased Implementation", "Spread costs", "12-18 month timeline"],
            ["MSSP vs. FTE", "Variable", "MSSP more cost-effective <100 employees"]
        ]
    )
    body += create_page_break()

    # ===== SECTION 10: IMPLEMENTATION ROADMAP =====
    body += create_paragraph("10. Implementation Roadmap", "Heading1")

    phases = [
        ("Phase 1: Assessment & Planning (Months 1-2)", "$20,000-35,000", [
            "Engage CMMC consultant/RPO for gap assessment",
            "Inventory all systems that touch CUI",
            "Create CUI data flow diagrams",
            "Select technology vendors"
        ]),
        ("Phase 2: Foundation Build (Months 3-4)", "$35,000-60,000", [
            "Procure GCC High licenses",
            "Establish AWS GovCloud account",
            "Migrate email to GCC High Exchange",
            "Deploy network segmentation"
        ]),
        ("Phase 3: Security Implementation (Months 5-6)", "$40,000-70,000", [
            "Migrate SharePoint, Teams, OneDrive to GCC High",
            "Deploy EDR on all endpoints",
            "Configure SIEM and log collection",
            "Begin SSP documentation"
        ]),
        ("Phase 4: Control Completion (Months 7-8)", "$30,000-50,000", [
            "Complete remaining technical controls",
            "Finalize policies and procedures",
            "Complete SSP and POA&M",
            "Conduct security awareness training"
        ]),
        ("Phase 5: Validation (Months 9-10)", "$15,000-30,000", [
            "Conduct internal mock assessment",
            "Remediate any identified gaps",
            "Verify all evidence is collected",
            "Engage C3PAO and schedule assessment"
        ]),
        ("Phase 6: Certification (Months 11-12)", "$40,000-75,000", [
            "C3PAO pre-assessment",
            "C3PAO formal assessment",
            "Address any findings",
            "Receive certification"
        ])
    ]

    for phase_name, budget, activities in phases:
        body += create_paragraph(phase_name, "Heading2")
        body += create_paragraph(f"Budget: {budget}", bold=True)
        body += create_bullet_list(activities)
    body += create_page_break()

    # ===== SECTION 11: RISK ASSESSMENT =====
    body += create_paragraph("11. Risk Assessment and Common Pitfalls", "Heading1")

    body += create_paragraph("Common CMMC Certification Failures", "Heading2")
    body += create_paragraph("Scoping Failures (Primary Cause):", "Heading3")
    body += create_bullet_list([
        "Over-scoping: Including systems that don't process CUI",
        "Under-scoping: Missing necessary systems",
        "Undefined CUI data flows",
        "Forgotten third-party services"
    ])

    body += create_paragraph("Documentation Failures:", "Heading3")
    body += create_bullet_list([
        "SSP doesn't match actual implementation",
        "Incomplete asset inventories",
        "Missing policies and procedures",
        "Insufficient evidence",
        "Outdated documentation"
    ])

    body += create_paragraph("Supply Chain and Subcontractor Risks", "Heading2")
    body += create_paragraph("Current State:", "Heading3")
    body += create_bullet_list([
        "Only 28.7% of organizations have completed Level 2 assessment",
        "Fewer than 0.6% (459 organizations) certified as of November 2025",
        "Creates significant supply chain risk"
    ])

    body += create_paragraph("Mitigation:", "Heading3")
    body += create_bullet_list([
        "Assess subcontractor readiness early",
        "Include compliance provisions in subcontracts",
        "Verify cloud provider compliance documentation",
        "Build redundancy in supply chain"
    ])
    body += create_page_break()

    # ===== SECTION 12: APPENDICES =====
    body += create_paragraph("12. Appendices", "Heading1")

    body += create_paragraph("Appendix A: NIST 800-171 Control Families Quick Reference", "Heading2")
    body += create_table(
        headers=["Family", "ID", "Count", "Key Areas"],
        rows=[
            ["Access Control", "AC", "22", "Least privilege, remote access, session controls"],
            ["Awareness & Training", "AT", "3", "Security awareness, role-based training"],
            ["Audit & Accountability", "AU", "9", "Logging, review, protection"],
            ["Configuration Management", "CM", "9", "Baselines, change control"],
            ["Identification & Authentication", "IA", "11", "MFA, passwords, device auth"],
            ["Incident Response", "IR", "3", "Capability, reporting, testing"],
            ["Maintenance", "MA", "6", "Controlled, remote maintenance"],
            ["Media Protection", "MP", "9", "Handling, sanitization, transport"],
            ["Personnel Security", "PS", "2", "Screening, actions"],
            ["Physical Protection", "PE", "6", "Access, visitor control"],
            ["Risk Assessment", "RA", "3", "Assessments, vulnerability scanning"],
            ["Security Assessment", "CA", "4", "Assessments, POA&M"],
            ["System & Communications", "SC", "16", "Boundary, encryption, CUI handling"],
            ["System & Info Integrity", "SI", "7", "Flaw remediation, malware, monitoring"]
        ]
    )
    body += create_paragraph("")

    body += create_paragraph("Appendix B: Key Acronyms", "Heading2")
    body += create_table(
        headers=["Acronym", "Definition"],
        rows=[
            ["C3PAO", "CMMC Third-Party Assessment Organization"],
            ["CUI", "Controlled Unclassified Information"],
            ["DFARS", "Defense Federal Acquisition Regulation Supplement"],
            ["DIB", "Defense Industrial Base"],
            ["EDR", "Endpoint Detection and Response"],
            ["FCI", "Federal Contract Information"],
            ["GCC High", "Government Community Cloud High"],
            ["MFA", "Multi-Factor Authentication"],
            ["MSSP", "Managed Security Service Provider"],
            ["NIST", "National Institute of Standards and Technology"],
            ["POA&M", "Plan of Action and Milestones"],
            ["RPO", "Registered Provider Organization"],
            ["SIEM", "Security Information and Event Management"],
            ["SPRS", "Supplier Performance Risk System"],
            ["SSP", "System Security Plan"]
        ]
    )
    body += create_paragraph("")

    body += create_horizontal_line()
    body += create_paragraph("Document Version: 1.0", "Normal")
    body += create_paragraph("Last Updated: December 2025", "Normal")
    body += create_paragraph("Next Review: March 2026", "Normal")
    body += create_paragraph("")
    body += create_paragraph("This document is intended for internal planning purposes. Consult with qualified CMMC consultants and legal counsel for specific compliance decisions.", italic=True)

    return body


def create_document_xml(body_content):
    """Create the complete document.xml."""
    xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
    <w:body>
        {body_content}
        <w:sectPr>
            <w:pgSz w:w="12240" w:h="15840"/>
            <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720"/>
            <w:cols w:space="720"/>
        </w:sectPr>
    </w:body>
</w:document>'''
    return xml


def create_docx(output_path):
    """Create the complete DOCX file."""
    print(f"Generating DOCX: {output_path}")

    # Generate document content
    body_content = generate_document_content()

    # Create DOCX as a ZIP file
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add required files
        zf.writestr('[Content_Types].xml', create_content_types_xml())
        zf.writestr('_rels/.rels', create_root_rels())
        zf.writestr('word/_rels/document.xml.rels', create_document_rels())
        zf.writestr('word/document.xml', create_document_xml(body_content))
        zf.writestr('word/styles.xml', create_styles_xml())
        zf.writestr('word/settings.xml', create_settings_xml())
        zf.writestr('word/fontTable.xml', create_font_table_xml())
        zf.writestr('word/numbering.xml', create_numbering_xml())
        zf.writestr('docProps/core.xml', create_core_properties_xml())
        zf.writestr('docProps/app.xml', create_app_properties_xml())

    print(f"Successfully created: {output_path}")
    return output_path


if __name__ == "__main__":
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Output file path
    output_file = os.path.join(script_dir, "Furientis_CMMC_Compliance_Strategy.docx")

    # Generate the DOCX
    create_docx(output_file)

    print(f"\nDocument generated successfully!")
    print(f"Location: {output_file}")
    print("\nFurientis Branding Applied:")
    print("  - Typography: Arial (sans-serif)")
    print("  - Colors: Black text on white background (print-optimized)")
    print("  - Style: Minimalist, clean hierarchy, professional tables")
