from io import BytesIO
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table as DocxTable
from docx.text.paragraph import Paragraph as DocxParagraph
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph as PdfParagraph,
    Spacer,
    Table,
    TableStyle,
)
from xml.sax.saxutils import escape


SOURCE = Path("docs/Relatorio_Final_Orcamento_Imobiliario_RM.docx")
OUTPUT = Path("output/pdf/Relatorio_Final_Orcamento_Imobiliario_RM.pdf")
ACCENT = colors.HexColor("#17365D")
ACCENT_2 = colors.HexColor("#D9EAF7")
LIGHT = colors.HexColor("#F4F7FA")
TEXT = colors.HexColor("#222222")


def register_fonts():
    candidates = [
        ("Arial", r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\arialbd.ttf"),
        ("Calibri", r"C:\Windows\Fonts\calibri.ttf", r"C:\Windows\Fonts\calibrib.ttf"),
    ]
    for name, regular, bold in candidates:
        if Path(regular).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont(name, regular))
            pdfmetrics.registerFont(TTFont(name + "-Bold", bold))
            return name, name + "-Bold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = register_fonts()


def iter_block_items(doc):
    for child in doc.element.body.iterchildren():
        if child.tag == qn("w:p"):
            yield DocxParagraph(child, doc)
        elif child.tag == qn("w:tbl"):
            yield DocxTable(child, doc)


def image_from_paragraph(paragraph, max_width=16.4 * cm, max_height=18 * cm):
    images = []
    for blip in paragraph._p.xpath(".//a:blip"):
        rid = blip.get(qn("r:embed"))
        if not rid:
            continue
        part = paragraph.part.related_parts[rid]
        data = part.blob
        with PILImage.open(BytesIO(data)) as pil:
            width, height = pil.size
        scale = min(max_width / width, max_height / height)
        images.append(Image(BytesIO(data), width=width * scale, height=height * scale))
    return images


def make_styles():
    base = getSampleStyleSheet()
    return {
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=10.2,
            leading=15,
            textColor=TEXT,
            alignment=TA_JUSTIFY,
            spaceAfter=7,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=10.1,
            leading=14,
            leftIndent=14,
            firstLineIndent=-8,
            bulletIndent=4,
            textColor=TEXT,
            spaceAfter=5,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName=FONT_BOLD,
            fontSize=16,
            leading=20,
            textColor=ACCENT,
            spaceBefore=12,
            spaceAfter=8,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName=FONT_BOLD,
            fontSize=12.5,
            leading=16,
            textColor=ACCENT,
            spaceBefore=9,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "quote": ParagraphStyle(
            "Quote",
            parent=base["Code"],
            fontName=FONT,
            fontSize=9.2,
            leading=12,
            leftIndent=14,
            rightIndent=10,
            borderColor=ACCENT_2,
            borderWidth=0.8,
            borderPadding=6,
            backColor=LIGHT,
            spaceAfter=4,
        ),
        "caption": ParagraphStyle(
            "Caption",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=9,
            leading=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#555555"),
            spaceBefore=4,
            spaceAfter=7,
        ),
        "cover_title": ParagraphStyle(
            "CoverTitle",
            fontName=FONT_BOLD,
            fontSize=23,
            leading=29,
            alignment=TA_CENTER,
            textColor=ACCENT,
            spaceAfter=16,
        ),
        "cover_sub": ParagraphStyle(
            "CoverSub",
            fontName=FONT,
            fontSize=13,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#404040"),
            spaceAfter=12,
        ),
        "toc": ParagraphStyle(
            "TOC",
            fontName=FONT,
            fontSize=10,
            leading=13,
            leftIndent=6,
            textColor=TEXT,
            spaceAfter=2,
        ),
        "cell": ParagraphStyle(
            "Cell",
            fontName=FONT,
            fontSize=8.2,
            leading=10.5,
            textColor=TEXT,
        ),
        "cell_head": ParagraphStyle(
            "CellHead",
            fontName=FONT_BOLD,
            fontSize=8.4,
            leading=10.5,
            textColor=colors.white,
            alignment=TA_CENTER,
        ),
    }


STYLES = make_styles()


def clean_text(text):
    return escape(text.replace("\u2011", "-").replace("\u00a0", " ").strip())


def table_flowable(docx_table):
    rows = []
    for r_idx, row in enumerate(docx_table.rows):
        cells = []
        for cell in row.cells:
            text = "<br/>".join(clean_text(p.text) for p in cell.paragraphs if p.text.strip())
            cells.append(PdfParagraph(text or " ", STYLES["cell_head" if r_idx == 0 else "cell"]))
        rows.append(cells)
    ncols = max(1, len(rows[0]))
    usable = 16.4 * cm
    if ncols == 2:
        widths = [usable * 0.28, usable * 0.72]
    elif ncols == 3:
        widths = [usable * 0.22, usable * 0.31, usable * 0.47]
    elif ncols == 4:
        widths = [usable * 0.27, usable * 0.24, usable * 0.24, usable * 0.25]
    else:
        widths = [usable / ncols] * ncols
    table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#8FA6BA")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


class ReportDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=2.3 * cm,
            rightMargin=2.3 * cm,
            topMargin=2.1 * cm,
            bottomMargin=1.9 * cm,
            title="Relatório Final - Sistema de Orçamento Imobiliário R.M",
            author="Projeto acadêmico",
        )
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="normal",
        )
        self.addPageTemplates(
            PageTemplate(id="report", frames=frame, onPage=self.draw_page)
        )

    def draw_page(self, canvas, doc):
        canvas.saveState()
        if doc.page > 1:
            canvas.setStrokeColor(ACCENT_2)
            canvas.line(2.3 * cm, A4[1] - 1.4 * cm, A4[0] - 2.3 * cm, A4[1] - 1.4 * cm)
            canvas.setFont(FONT, 8)
            canvas.setFillColor(colors.HexColor("#5A6670"))
            canvas.drawString(2.3 * cm, A4[1] - 1.15 * cm, "Sistema de Orçamento Imobiliário R.M")
            canvas.drawRightString(A4[0] - 2.3 * cm, 1.15 * cm, f"Página {doc.page}")
        canvas.restoreState()


def build():
    docx = Document(SOURCE)
    story = []
    blocks = list(iter_block_items(docx))
    cover_done = False

    # Preserve the source order, while translating Word styles into a stable PDF layout.
    for block in blocks:
        if isinstance(block, DocxTable):
            story.extend([table_flowable(block), Spacer(1, 8)])
            continue

        text = block.text.strip()
        style_name = block.style.name if block.style else "Normal"
        imgs = image_from_paragraph(block)
        if not text and not imgs:
            continue

        if not cover_done and style_name in {"Title", "Subtitle"}:
            style = STYLES["cover_title" if style_name == "Title" else "cover_sub"]
            story.append(PdfParagraph(clean_text(text), style))
            if style_name == "Subtitle":
                story.append(Spacer(1, 10))
            continue

        if not cover_done and style_name == "Heading 1":
            story.append(PageBreak())
            cover_done = True

        if style_name == "Heading 1":
            story.append(PdfParagraph(clean_text(text), STYLES["h1"]))
        elif style_name == "Heading 2":
            story.append(PdfParagraph(clean_text(text), STYLES["h2"]))
        elif style_name == "List Bullet":
            story.append(PdfParagraph(clean_text(text), STYLES["bullet"], bulletText="•"))
        elif style_name == "Intense Quote":
            story.append(PdfParagraph(clean_text(text), STYLES["quote"]))
        elif style_name == "Caption":
            story.append(PdfParagraph(clean_text(text), STYLES["caption"]))
        elif "TOC" in style_name.upper():
            story.append(PdfParagraph(clean_text(text), STYLES["toc"]))
        elif text:
            story.append(PdfParagraph(clean_text(text), STYLES["body"]))

        for img in imgs:
            img.hAlign = "CENTER"
            story.extend([Spacer(1, 4), img, Spacer(1, 8)])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ReportDoc(str(OUTPUT)).build(story)
    print(OUTPUT.resolve())


if __name__ == "__main__":
    build()
