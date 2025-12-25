#!/usr/bin/env python3
"""
CMMC Compliance Strategy PDF Generator

Generates a professional PDF using only Python standard library.
No external dependencies required.

Furientis Brand Guidelines (adapted for print):
- Typography: Helvetica (PDF built-in, similar to Arial)
- Colors: Black text on white background
- Style: Minimalist, clean hierarchy, professional
"""

import os
import zlib
from datetime import datetime


class PDFDocument:
    """Simple PDF generator using only Python standard library."""

    def __init__(self):
        self.objects = []
        self.pages = []
        self.current_page_content = []
        self.fonts = {}
        self.page_width = 612  # Letter width in points (8.5")
        self.page_height = 792  # Letter height in points (11")
        self.margin_left = 72  # 1 inch
        self.margin_right = 72
        self.margin_top = 72
        self.margin_bottom = 72
        self.current_y = self.page_height - self.margin_top
        self.line_height = 14

    def _add_object(self, content):
        """Add an object and return its number."""
        self.objects.append(content)
        return len(self.objects)

    def _escape_text(self, text):
        """Escape special characters for PDF strings."""
        text = text.replace('\\', '\\\\')
        text = text.replace('(', '\\(')
        text = text.replace(')', '\\)')
        return text

    def _wrap_text(self, text, font_size, max_width):
        """Wrap text to fit within max_width."""
        # Approximate character width (Helvetica average)
        char_width = font_size * 0.5
        chars_per_line = int(max_width / char_width)

        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            word_length = len(word) + 1  # +1 for space
            if current_length + word_length <= chars_per_line:
                current_line.append(word)
                current_length += word_length
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def _new_page(self):
        """Start a new page."""
        if self.current_page_content:
            self.pages.append('\n'.join(self.current_page_content))
        self.current_page_content = []
        self.current_y = self.page_height - self.margin_top

    def _check_page_break(self, needed_height):
        """Check if we need a page break."""
        if self.current_y - needed_height < self.margin_bottom:
            self._new_page()

    def add_title(self, text, size=28):
        """Add a centered title."""
        self._check_page_break(size + 20)
        x = self.page_width / 2
        escaped = self._escape_text(text)
        self.current_page_content.append(f"BT /F1 {size} Tf {x} {self.current_y} Td ({escaped}) Tj ET")
        self.current_y -= size + 20

    def add_heading1(self, text, size=18):
        """Add a heading level 1."""
        self._check_page_break(size + 30)
        self.current_y -= 20  # Space before
        escaped = self._escape_text(text)
        self.current_page_content.append(f"BT /F2 {size} Tf {self.margin_left} {self.current_y} Td ({escaped}) Tj ET")
        self.current_y -= size + 10

    def add_heading2(self, text, size=14):
        """Add a heading level 2."""
        self._check_page_break(size + 20)
        self.current_y -= 15  # Space before
        escaped = self._escape_text(text)
        self.current_page_content.append(f"BT /F2 {size} Tf {self.margin_left} {self.current_y} Td ({escaped}) Tj ET")
        self.current_y -= size + 8

    def add_heading3(self, text, size=12):
        """Add a heading level 3."""
        self._check_page_break(size + 15)
        self.current_y -= 10  # Space before
        escaped = self._escape_text(text)
        self.current_page_content.append(f"BT /F2 {size} Tf {self.margin_left} {self.current_y} Td ({escaped}) Tj ET")
        self.current_y -= size + 6

    def add_paragraph(self, text, size=11, indent=0):
        """Add a paragraph with word wrapping."""
        max_width = self.page_width - self.margin_left - self.margin_right - indent
        lines = self._wrap_text(text, size, max_width)

        for line in lines:
            self._check_page_break(size + 4)
            escaped = self._escape_text(line)
            x = self.margin_left + indent
            self.current_page_content.append(f"BT /F1 {size} Tf {x} {self.current_y} Td ({escaped}) Tj ET")
            self.current_y -= size + 4

        self.current_y -= 6  # Space after paragraph

    def add_bullet_item(self, text, size=11):
        """Add a bullet point item."""
        bullet_indent = 20
        text_indent = 35
        max_width = self.page_width - self.margin_left - self.margin_right - text_indent
        lines = self._wrap_text(text, size, max_width)

        # Draw bullet
        self._check_page_break(size + 4)
        x_bullet = self.margin_left + bullet_indent
        self.current_page_content.append(f"BT /F1 {size} Tf {x_bullet} {self.current_y} Td (\\225) Tj ET")

        # Draw text lines
        x_text = self.margin_left + text_indent
        for i, line in enumerate(lines):
            escaped = self._escape_text(line)
            if i == 0:
                self.current_page_content.append(f"BT /F1 {size} Tf {x_text} {self.current_y} Td ({escaped}) Tj ET")
            else:
                self._check_page_break(size + 4)
                self.current_page_content.append(f"BT /F1 {size} Tf {x_text} {self.current_y} Td ({escaped}) Tj ET")
            self.current_y -= size + 4

    def add_numbered_item(self, number, text, size=11):
        """Add a numbered list item."""
        num_indent = 20
        text_indent = 40
        max_width = self.page_width - self.margin_left - self.margin_right - text_indent
        lines = self._wrap_text(text, size, max_width)

        # Draw number
        self._check_page_break(size + 4)
        x_num = self.margin_left + num_indent
        self.current_page_content.append(f"BT /F1 {size} Tf {x_num} {self.current_y} Td ({number}.) Tj ET")

        # Draw text lines
        x_text = self.margin_left + text_indent
        for i, line in enumerate(lines):
            escaped = self._escape_text(line)
            if i == 0:
                self.current_page_content.append(f"BT /F1 {size} Tf {x_text} {self.current_y} Td ({escaped}) Tj ET")
            else:
                self._check_page_break(size + 4)
                self.current_page_content.append(f"BT /F1 {size} Tf {x_text} {self.current_y} Td ({escaped}) Tj ET")
            self.current_y -= size + 4

    def add_table(self, headers, rows, col_widths=None):
        """Add a simple table."""
        num_cols = len(headers)
        available_width = self.page_width - self.margin_left - self.margin_right
        if col_widths is None:
            col_width = available_width / num_cols
            col_widths = [col_width] * num_cols

        row_height = 20
        font_size = 9
        total_rows = 1 + len(rows)
        table_height = row_height * total_rows

        self._check_page_break(table_height + 20)
        self.current_y -= 10

        # Draw table
        start_y = self.current_y
        x = self.margin_left

        # Header row (with gray background)
        y = start_y
        # Draw header background
        self.current_page_content.append(f"0.9 g")  # Light gray
        self.current_page_content.append(f"{x} {y - row_height} {available_width} {row_height} re f")
        self.current_page_content.append(f"0 g")  # Back to black

        # Draw header text
        curr_x = x + 5
        for i, header in enumerate(headers):
            escaped = self._escape_text(str(header)[:int(col_widths[i]/5)])
            self.current_page_content.append(f"BT /F2 {font_size} Tf {curr_x} {y - 14} Td ({escaped}) Tj ET")
            curr_x += col_widths[i]

        y -= row_height

        # Data rows
        for row in rows:
            curr_x = x + 5
            for i, cell in enumerate(row):
                cell_text = str(cell)[:int(col_widths[i]/4.5)]  # Truncate if too long
                escaped = self._escape_text(cell_text)
                self.current_page_content.append(f"BT /F1 {font_size} Tf {curr_x} {y - 14} Td ({escaped}) Tj ET")
                curr_x += col_widths[i]
            y -= row_height

        # Draw grid lines
        self.current_page_content.append(f"0.7 G")  # Gray lines
        self.current_page_content.append(f"0.5 w")  # Line width

        # Horizontal lines
        for i in range(total_rows + 1):
            line_y = start_y - (i * row_height)
            self.current_page_content.append(f"{x} {line_y} m {x + available_width} {line_y} l S")

        # Vertical lines
        curr_x = x
        for i in range(num_cols + 1):
            self.current_page_content.append(f"{curr_x} {start_y} m {curr_x} {start_y - table_height} l S")
            if i < num_cols:
                curr_x += col_widths[i]

        self.current_page_content.append(f"0 G")  # Back to black
        self.current_y = y - 15

    def add_horizontal_line(self):
        """Add a horizontal line."""
        self._check_page_break(20)
        self.current_y -= 10
        x1 = self.margin_left
        x2 = self.page_width - self.margin_right
        self.current_page_content.append(f"0.5 w {x1} {self.current_y} m {x2} {self.current_y} l S")
        self.current_y -= 10

    def add_page_break(self):
        """Force a page break."""
        self._new_page()

    def add_space(self, height=20):
        """Add vertical space."""
        self._check_page_break(height)
        self.current_y -= height

    def save(self, filename):
        """Save the PDF to a file."""
        # Finalize last page
        if self.current_page_content:
            self.pages.append('\n'.join(self.current_page_content))

        # Build PDF structure
        pdf_lines = ['%PDF-1.4']

        # Object 1: Catalog
        obj1 = "1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj"
        pdf_lines.append(obj1)

        # Object 2: Pages
        page_refs = ' '.join([f"{i+4} 0 R" for i in range(len(self.pages))])
        obj2 = f"2 0 obj\n<< /Type /Pages /Kids [{page_refs}] /Count {len(self.pages)} >>\nendobj"
        pdf_lines.append(obj2)

        # Object 3: Font resources
        obj3 = """3 0 obj
<< /Font <<
    /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
    /F2 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>
>> >>
endobj"""
        pdf_lines.append(obj3)

        # Page objects and content streams
        obj_num = 4
        for i, page_content in enumerate(self.pages):
            # Page object
            content_obj = obj_num + 1
            page_obj = f"""{obj_num} 0 obj
<< /Type /Page /Parent 2 0 R
   /MediaBox [0 0 {self.page_width} {self.page_height}]
   /Resources 3 0 R
   /Contents {content_obj} 0 R >>
endobj"""
            pdf_lines.append(page_obj)
            obj_num += 1

            # Content stream
            stream_data = page_content.encode('latin-1')
            stream_length = len(stream_data)
            content_obj_str = f"""{obj_num} 0 obj
<< /Length {stream_length} >>
stream
{page_content}
endstream
endobj"""
            pdf_lines.append(content_obj_str)
            obj_num += 1

        # Calculate byte offsets for xref
        pdf_content = '\n'.join(pdf_lines) + '\n'
        offsets = [0]
        current_offset = len('%PDF-1.4\n')
        for line in pdf_lines[1:]:
            offsets.append(current_offset)
            current_offset += len(line) + 1

        # Xref table
        xref_offset = len(pdf_content)
        xref = f"xref\n0 {obj_num}\n0000000000 65535 f \n"
        for offset in offsets[1:]:
            xref += f"{offset:010d} 00000 n \n"

        # Trailer
        trailer = f"""trailer
<< /Size {obj_num} /Root 1 0 R >>
startxref
{xref_offset}
%%EOF"""

        # Write file
        with open(filename, 'wb') as f:
            f.write(pdf_content.encode('latin-1'))
            f.write(xref.encode('latin-1'))
            f.write(trailer.encode('latin-1'))

        return filename


def generate_cmmc_pdf(output_path):
    """Generate the CMMC Compliance Strategy PDF."""
    print(f"Generating PDF: {output_path}")

    pdf = PDFDocument()

    # ===== TITLE PAGE =====
    pdf.add_space(100)
    pdf.add_title("FURIENTIS")
    pdf.add_space(20)
    pdf.add_title("CMMC Level 2 Compliance Strategy", size=20)
    pdf.add_space(10)
    pdf.add_paragraph("A Comprehensive Guide to CMMC Certification, Dual-Echelon Architecture, and Operational Excellence", size=12)
    pdf.add_space(30)
    pdf.add_horizontal_line()
    pdf.add_space(20)
    pdf.add_paragraph("Version: 1.0")
    pdf.add_paragraph("Date: December 2025")
    pdf.add_paragraph("Prepared for: Furientis Leadership")
    pdf.add_paragraph("Classification: Internal Use Only")
    pdf.add_page_break()

    # ===== TABLE OF CONTENTS =====
    pdf.add_heading1("Table of Contents")
    toc_items = [
        "Executive Summary",
        "CMMC Level 2 Requirements Overview",
        "Dual-Echelon Architecture",
        "Cloud Infrastructure Strategy",
        "IT Infrastructure Requirements",
        "Software Requirements",
        "Operational TTPs for Engineer Productivity",
        "Vendor Comparison",
        "Cost Estimates",
        "Implementation Roadmap",
        "Risk Assessment and Common Pitfalls",
        "Appendices"
    ]
    for i, item in enumerate(toc_items, 1):
        pdf.add_numbered_item(i, item)
    pdf.add_page_break()

    # ===== SECTION 1: EXECUTIVE SUMMARY =====
    pdf.add_heading1("1. Executive Summary")

    pdf.add_heading2("Purpose")
    pdf.add_paragraph("This document provides Furientis with a comprehensive strategy for achieving Cybersecurity Maturity Model Certification (CMMC) Level 2 compliance while maintaining operational agility for both government and commercial work streams. As a startup pursuing Department of Defense (DoD) contracts involving Controlled Unclassified Information (CUI), Furientis must implement 110 security practices aligned with NIST SP 800-171 Rev. 2.")

    pdf.add_heading2("Key Findings")
    pdf.add_heading3("Compliance Landscape:")
    pdf.add_bullet_item("CMMC 2.0 Phase 1 became effective November 10, 2025")
    pdf.add_bullet_item("Level 2 certification requires third-party assessment by an accredited C3PAO")
    pdf.add_bullet_item("Conditional certification available with 80% compliance score (180 days to remediate)")
    pdf.add_bullet_item("Average preparation timeline: 6-18 months for organizations starting from scratch")

    pdf.add_heading3("Strategic Recommendations:")
    pdf.add_numbered_item(1, "Implement a CUI Enclave Architecture - Isolate government work from commercial operations")
    pdf.add_numbered_item(2, "Adopt Microsoft 365 GCC High - The only Microsoft environment meeting DFARS 7012")
    pdf.add_numbered_item(3, "Leverage AWS GovCloud - FedRAMP High-authorized infrastructure for compute and AI/ML")
    pdf.add_numbered_item(4, "Establish Clear Separation - Physical and logical network segmentation")
    pdf.add_page_break()

    # ===== SECTION 2: CMMC REQUIREMENTS =====
    pdf.add_heading1("2. CMMC Level 2 Requirements Overview")

    pdf.add_heading2("What is CMMC?")
    pdf.add_paragraph("The Cybersecurity Maturity Model Certification (CMMC) is the DoD's verification mechanism to ensure that contractors implement adequate cybersecurity practices to protect sensitive information. CMMC 2.0, finalized in 2024 and enforced beginning November 2025, streamlined the original five-tier model into three levels.")

    pdf.add_table(
        headers=["Level", "Description", "Assessment", "Practices", "Data"],
        rows=[
            ["Level 1", "Foundational", "Self-Assessment", "17", "FCI"],
            ["Level 2", "Advanced", "Third-Party (C3PAO)", "110", "CUI"],
            ["Level 3", "Expert", "Government-led", "110+", "Critical CUI"]
        ]
    )

    pdf.add_heading2("Level 2 Control Families")
    pdf.add_paragraph("CMMC Level 2 directly maps to NIST SP 800-171 Revision 2, requiring implementation of 110 security practices across 14 domains:")

    pdf.add_table(
        headers=["Domain", "ID", "Count", "Focus Areas"],
        rows=[
            ["Access Control", "AC", "22", "Least privilege, remote access"],
            ["Awareness & Training", "AT", "3", "Security awareness"],
            ["Audit & Accountability", "AU", "9", "Logging, audit review"],
            ["Configuration Mgmt", "CM", "9", "Baseline configs"],
            ["ID & Authentication", "IA", "11", "MFA, passwords"],
            ["Incident Response", "IR", "3", "IR capability, testing"],
            ["Maintenance", "MA", "6", "Controlled maintenance"],
            ["Media Protection", "MP", "9", "Media handling"],
            ["Personnel Security", "PS", "2", "Screening"],
            ["Physical Protection", "PE", "6", "Physical access"],
            ["Risk Assessment", "RA", "3", "Vulnerability scanning"],
            ["Security Assessment", "CA", "4", "POA&M"],
            ["System & Comms", "SC", "16", "Encryption, CUI"],
            ["System Integrity", "SI", "7", "Malware protection"]
        ]
    )
    pdf.add_page_break()

    # ===== SECTION 3: DUAL-ECHELON =====
    pdf.add_heading1("3. Dual-Echelon Architecture")

    pdf.add_heading2("Strategic Rationale")
    pdf.add_paragraph("Furientis operates in two distinct contexts: government contracts involving CUI and commercial/research projects without government data or funding. Implementing a dual-echelon architecture provides significant advantages.")

    pdf.add_table(
        headers=["Benefit", "Description"],
        rows=[
            ["Reduced Scope", "Only government echelon requires CMMC controls"],
            ["Flexibility", "Commercial work proceeds without constraints"],
            ["Accountability", "Distinct environments simplify audits"],
            ["Risk Isolation", "Breach in one doesn't compromise other"],
            ["Cost Optimization", "GCC High licensing only for CUI personnel"]
        ]
    )

    pdf.add_heading2("Personnel and Role Separation")
    pdf.add_table(
        headers=["Role", "Enclave Access", "GCC High", "Training"],
        rows=[
            ["Gov Project Engineers", "Full", "Yes (E3/E5)", "CMMC + Role-based"],
            ["Gov Project Managers", "Full", "Yes (E3/E5)", "CMMC Awareness"],
            ["Commercial Engineers", "None", "No", "Basic Security"],
            ["IT Administrators", "Full (privileged)", "Yes (E5)", "CMMC + Privileged"],
            ["Executive Leadership", "Limited", "Yes (E3)", "CMMC Awareness"]
        ]
    )
    pdf.add_page_break()

    # ===== SECTION 4: CLOUD INFRASTRUCTURE =====
    pdf.add_heading1("4. Cloud Infrastructure Strategy")

    pdf.add_heading2("AWS GovCloud Selection")
    pdf.add_paragraph("For Furientis's government echelon, AWS GovCloud (US) is the recommended primary cloud infrastructure provider.")

    pdf.add_table(
        headers=["Factor", "AWS GovCloud Advantage"],
        rows=[
            ["FedRAMP", "High baseline authorization"],
            ["AI/ML", "Amazon Bedrock with Claude, Llama"],
            ["GPU Compute", "NVIDIA P4d, P5, G5 instances"],
            ["Data Residency", "US only, US persons"],
            ["ITAR/EAR", "Export-controlled data support"]
        ]
    )

    pdf.add_heading2("Compute Resources")
    pdf.add_table(
        headers=["Service", "Use Case", "Instance Types"],
        rows=[
            ["EC2", "General compute", "m5, c5, r5"],
            ["EC2 (GPU)", "ML training/inference", "p4d, g5"],
            ["EKS", "Container orchestration", "Managed K8s"],
            ["Lambda", "Serverless", "N/A"],
            ["WorkSpaces", "Virtual desktops", "Various"]
        ]
    )

    pdf.add_heading2("Storage Services")
    pdf.add_table(
        headers=["Service", "Use Case", "Encryption"],
        rows=[
            ["S3", "Object storage, data lakes", "SSE-KMS (FIPS 140-2)"],
            ["EBS", "Block storage", "AES-256 at rest"],
            ["EFS", "Shared file systems", "Transit + rest"],
            ["FSx", "Windows file shares", "AD integration"]
        ]
    )
    pdf.add_page_break()

    # ===== SECTION 5: IT INFRASTRUCTURE =====
    pdf.add_heading1("5. IT Infrastructure Requirements")

    pdf.add_heading2("Endpoint Security Stack")
    pdf.add_table(
        headers=["Layer", "Solution", "Purpose"],
        rows=[
            ["OS Hardening", "CIS/STIG", "Baseline config"],
            ["Disk Encryption", "BitLocker (FIPS)", "Data at rest"],
            ["EDR/XDR", "CrowdStrike/Defender", "Threat detection"],
            ["DLP", "Microsoft Purview", "Prevent exfil"],
            ["VPN", "Always-on", "Encrypted tunnel"],
            ["Patching", "WSUS/Intune/SCCM", "Security updates"]
        ]
    )

    pdf.add_heading2("Identity and Access Management")
    pdf.add_table(
        headers=["Control", "Requirement", "Implementation"],
        rows=[
            ["3.5.1", "Identify users/devices", "Azure AD GCC High"],
            ["3.5.2", "Authenticate", "MFA required"],
            ["3.5.3", "MFA", "Authenticator, FIDO2"],
            ["3.5.7", "Password complexity", "14+ characters"],
            ["3.5.8", "Reuse prevention", "Remember 24"],
            ["3.5.10", "Session lock", "15-min timeout"]
        ]
    )
    pdf.add_page_break()

    # ===== SECTION 6: SOFTWARE =====
    pdf.add_heading1("6. Software Requirements")

    pdf.add_heading2("Microsoft 365 Licensing")
    pdf.add_table(
        headers=["License", "Features", "Cost/User/Month"],
        rows=[
            ["M365 E3", "Core productivity", "$35-40"],
            ["M365 E5", "Advanced security", "$55-60"],
            ["E5 Security Add-on", "E5 security on E3", "$15-20"]
        ]
    )

    pdf.add_heading2("Operating Systems")
    pdf.add_table(
        headers=["OS", "Version", "Notes"],
        rows=[
            ["Windows 11 Enterprise", "23H2+", "Recommended"],
            ["Windows 10 Enterprise", "22H2", "Until Oct 2025"],
            ["Windows Server", "2019/2022", "Server workloads"],
            ["macOS", "Monterey+", "With Intune"],
            ["Linux", "RHEL 8/9, Ubuntu 22.04", "Dev environments"]
        ]
    )

    pdf.add_heading2("Development Tools")
    pdf.add_table(
        headers=["Category", "Tool", "Notes"],
        rows=[
            ["IDE", "VS Code, Visual Studio", "Disable telemetry"],
            ["Source Control", "GitHub Enterprise", "Self-hosted GovCloud"],
            ["CI/CD", "GitHub Actions", "Self-hosted runners"],
            ["Containers", "Docker, Podman", "Scanned images"],
            ["Kubernetes", "EKS GovCloud", "Managed K8s"]
        ]
    )
    pdf.add_page_break()

    # ===== SECTION 7: TTPs =====
    pdf.add_heading1("7. Operational TTPs")

    pdf.add_heading2("Development Workflow Best Practices")
    pdf.add_paragraph("The key to maintaining productivity is proper scoping. By creating a well-segmented CUI enclave, Furientis can significantly reduce in-scope assets.")

    pdf.add_heading3("Practical Implementation:")
    pdf.add_numbered_item(1, "Segment Early, Segment Often - Use network segmentation and access controls")
    pdf.add_numbered_item(2, "Define Clear Data Flows - SSP must map where CUI lives")
    pdf.add_numbered_item(3, "Implement Zones of Trust - Use VLANs, firewalls, network separation")

    pdf.add_heading2("Common Scoping Pitfalls")
    pdf.add_table(
        headers=["Pitfall", "Impact", "Mitigation"],
        rows=[
            ["Over-scoping", "Unnecessary cost", "Only include CUI systems"],
            ["Under-scoping", "Non-compliance", "Thorough CUI analysis"],
            ["Missing flows", "Compliance gaps", "Document all CUI movement"],
            ["Third-party", "Surprise scope", "Verify FedRAMP status"]
        ]
    )
    pdf.add_page_break()

    # ===== SECTION 8: VENDOR COMPARISON =====
    pdf.add_heading1("8. Vendor Comparison")

    pdf.add_heading2("CMMC MSPs")
    pdf.add_table(
        headers=["Provider", "Specialization", "Target"],
        rows=[
            ["Summit 7", "CMMC, Azure, GCC High", "SMBs"],
            ["Coalfire", "CMMC, FedRAMP", "Enterprise"],
            ["Pivot Point", "CMMC, GCC migration", "Small-mid"],
            ["Mirai Security", "CMMC implementation", "SMBs"],
            ["Ariento", "CMMC managed security", "Defense"]
        ]
    )

    pdf.add_heading2("EDR Solutions")
    pdf.add_table(
        headers=["Solution", "Annual Cost/Endpoint", "Strengths"],
        rows=[
            ["CrowdStrike Go", "$60", "Industry leader"],
            ["CrowdStrike Pro", "$100", "+ Firewall mgmt"],
            ["SentinelOne", "$80", "AI/ML response"],
            ["MS Defender P1", "Included in E5", "Native M365"]
        ]
    )
    pdf.add_page_break()

    # ===== SECTION 9: COST ESTIMATES =====
    pdf.add_heading1("9. Cost Estimates")

    pdf.add_heading2("First-Year Cost Summary")
    pdf.add_table(
        headers=["Category", "Low", "Mid", "High"],
        rows=[
            ["GCC High (25 users)", "$6,600", "$10,800", "$21,600"],
            ["AWS GovCloud", "$7,200", "$15,000", "$30,000"],
            ["C3PAO Assessment", "$40,000", "$55,000", "$75,000"],
            ["MSSP Services", "$40,000", "$55,000", "$75,000"],
            ["EDR/Endpoint", "$2,000", "$5,000", "$9,000"],
            ["SIEM Solution", "$8,000", "$15,000", "$25,000"],
            ["Training", "$10,000", "$18,000", "$30,000"],
            ["Consulting", "$30,000", "$50,000", "$80,000"],
            ["Additional Tools", "$20,000", "$35,000", "$60,000"],
            ["Hardware", "$15,000", "$35,000", "$85,000"],
            ["TOTAL YEAR 1", "$178,800", "$293,800", "$490,600"]
        ]
    )

    pdf.add_heading2("Three-Year Investment")
    pdf.add_table(
        headers=["Scenario", "3-Year Total", "Annual Avg"],
        rows=[
            ["Low (Good Posture)", "$366,318", "$122,106"],
            ["Mid (Typical)", "$596,318", "$198,773"],
            ["High (Remediation)", "$960,718", "$320,239"]
        ]
    )
    pdf.add_page_break()

    # ===== SECTION 10: ROADMAP =====
    pdf.add_heading1("10. Implementation Roadmap")

    phases = [
        ("Phase 1: Assessment (Months 1-2)", "$20,000-35,000", ["Gap assessment", "CUI inventory", "Vendor selection"]),
        ("Phase 2: Foundation (Months 3-4)", "$35,000-60,000", ["GCC High licenses", "AWS GovCloud", "Network segmentation"]),
        ("Phase 3: Security (Months 5-6)", "$40,000-70,000", ["M365 migration", "EDR deployment", "SIEM configuration"]),
        ("Phase 4: Controls (Months 7-8)", "$30,000-50,000", ["Complete 110 controls", "SSP documentation", "Training"]),
        ("Phase 5: Validation (Months 9-10)", "$15,000-30,000", ["Mock assessment", "Remediation", "C3PAO scheduling"]),
        ("Phase 6: Certification (Months 11-12)", "$40,000-75,000", ["C3PAO assessment", "Findings remediation", "Certification"])
    ]

    for phase_name, budget, activities in phases:
        pdf.add_heading2(phase_name)
        pdf.add_paragraph(f"Budget: {budget}")
        for activity in activities:
            pdf.add_bullet_item(activity)
    pdf.add_page_break()

    # ===== SECTION 11: RISK ASSESSMENT =====
    pdf.add_heading1("11. Risk Assessment")

    pdf.add_heading2("Common Certification Failures")
    pdf.add_heading3("Scoping Failures (Primary Cause):")
    pdf.add_bullet_item("Over-scoping: Including systems that don't process CUI")
    pdf.add_bullet_item("Under-scoping: Missing necessary systems")
    pdf.add_bullet_item("Undefined CUI data flows")
    pdf.add_bullet_item("Forgotten third-party services")

    pdf.add_heading3("Documentation Failures:")
    pdf.add_bullet_item("SSP doesn't match actual implementation")
    pdf.add_bullet_item("Incomplete asset inventories")
    pdf.add_bullet_item("Missing policies and procedures")

    pdf.add_heading2("Supply Chain Risks")
    pdf.add_bullet_item("Only 28.7% of organizations have completed Level 2 assessment")
    pdf.add_bullet_item("Fewer than 0.6% (459 organizations) certified as of November 2025")
    pdf.add_bullet_item("Assess subcontractor readiness early")
    pdf.add_bullet_item("Include compliance provisions in subcontracts")
    pdf.add_page_break()

    # ===== SECTION 12: APPENDICES =====
    pdf.add_heading1("12. Appendices")

    pdf.add_heading2("Appendix A: Key Acronyms")
    pdf.add_table(
        headers=["Acronym", "Definition"],
        rows=[
            ["C3PAO", "CMMC Third-Party Assessment Organization"],
            ["CUI", "Controlled Unclassified Information"],
            ["DFARS", "Defense Federal Acquisition Reg Supplement"],
            ["DIB", "Defense Industrial Base"],
            ["EDR", "Endpoint Detection and Response"],
            ["FCI", "Federal Contract Information"],
            ["GCC High", "Government Community Cloud High"],
            ["MFA", "Multi-Factor Authentication"],
            ["MSSP", "Managed Security Service Provider"],
            ["NIST", "National Institute of Standards and Technology"],
            ["POA&M", "Plan of Action and Milestones"],
            ["SIEM", "Security Info and Event Management"],
            ["SPRS", "Supplier Performance Risk System"],
            ["SSP", "System Security Plan"]
        ]
    )

    pdf.add_space(30)
    pdf.add_horizontal_line()
    pdf.add_paragraph("Document Version: 1.0")
    pdf.add_paragraph("Last Updated: December 2025")
    pdf.add_paragraph("Next Review: March 2026")
    pdf.add_space(20)
    pdf.add_paragraph("This document is intended for internal planning purposes. Consult with qualified CMMC consultants and legal counsel for specific compliance decisions.")

    # Save
    pdf.save(output_path)
    print(f"Successfully created: {output_path}")
    return output_path


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "Furientis_CMMC_Compliance_Strategy.pdf")
    generate_cmmc_pdf(output_file)
    print("\nPDF generated successfully!")
    print(f"Location: {output_file}")
