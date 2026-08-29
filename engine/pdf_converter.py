import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

class PDFConverter:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        
        # Custom clean ATS-friendly resume styles
        self.title_style = ParagraphStyle(
            'ResumeTitle',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=20,
            leading=24,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=4
        )
        
        self.contact_style = ParagraphStyle(
            'ResumeContact',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor('#475569'),
            spaceAfter=10
        )
        
        self.section_heading = ParagraphStyle(
            'ResumeSectionHeading',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=15,
            textColor=colors.HexColor('#1e3a8a'),
            spaceBefore=8,
            spaceAfter=4,
            textTransform='uppercase'
        )
        
        self.body_style = ParagraphStyle(
            'ResumeBody',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=4
        )
        
        self.bullet_style = ParagraphStyle(
            'ResumeBullet',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            leftIndent=12,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=3
        )

    def convert_markdown_to_pdf(self, md_filepath, pdf_filepath=None):
        """Converts a Markdown resume file to a clean, professional ATS PDF file."""
        if not pdf_filepath:
            pdf_filepath = md_filepath.replace(".md", ".pdf")

        with open(md_filepath, "r", encoding="utf-8") as f:
            md_text = f.read()

        doc = SimpleDocTemplate(
            pdf_filepath,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        story = []
        lines = md_text.split("\n")

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue

            # Header / Name (# Sonia Pegu)
            if line_str.startswith("# "):
                name = line_str.replace("# ", "").strip()
                story.append(Paragraph(f"<b>{name}</b>", self.title_style))

            # Contact Line / Subtitle (**Bangalore, Karnataka** | ...)
            elif line_str.startswith("**Bangalore") or line_str.startswith("Bangalore"):
                clean_contact = re.sub(r'\*\*', '', line_str)
                story.append(Paragraph(clean_contact, self.contact_style))
                story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

            # Section Headers (## PROFESSIONAL SUMMARY, ## PROFESSIONAL EXPERIENCE, etc.)
            elif line_str.startswith("## "):
                heading = line_str.replace("## ", "").strip()
                story.append(Paragraph(f"<b>{heading}</b>", self.section_heading))
                story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#1e3a8a'), spaceBefore=1, spaceAfter=6))

            # Subheaders (### ICICI Bank Ltd. | Chief Manager ...)
            elif line_str.startswith("### "):
                sub_heading = line_str.replace("### ", "").strip()
                sub_heading = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', sub_heading)
                story.append(Spacer(1, 4))
                story.append(Paragraph(f"<b>{sub_heading}</b>", self.body_style))

            # Dates / Locations (*Aug 2023 - Present | Bangalore, India*)
            elif line_str.startswith("*") and line_str.endswith("*") and not line_str.startswith("- "):
                italic_text = line_str.strip("*").strip()
                story.append(Paragraph(f"<i>{italic_text}</i>", ParagraphStyle('ItalicSub', parent=self.body_style, textColor=colors.HexColor('#64748b'), spaceAfter=4)))

            # Bullet Points (- **7.5x Commercial Revenue Growth**: ...)
            elif line_str.startswith("- ") or line_str.startswith("* "):
                bullet_content = line_str[2:].strip()
                # Format markdown bold (**text**) to HTML (<b>text</b>)
                bullet_content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', bullet_content)
                bullet_content = re.sub(r'\*(.*?)\*', r'<i>\1</i>', bullet_content)
                story.append(Paragraph(f"• {bullet_content}", self.bullet_style))

            # Separator rules (---)
            elif line_str == "---":
                continue

            # Standard body text
            else:
                formatted_line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line_str)
                formatted_line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', formatted_line)
                story.append(Paragraph(formatted_line, self.body_style))

        doc.build(story)
        print(f"✅ Created PDF resume at: {pdf_filepath}")
        return pdf_filepath

if __name__ == "__main__":
    converter = PDFConverter()
    sample_md = "tailored_resumes/Resume_SoniaPegu_Amazon_Enterprise_Sales_Manager__Direct_Sales.md"
    if os.path.exists(sample_md):
        converter.convert_markdown_to_pdf(sample_md)
