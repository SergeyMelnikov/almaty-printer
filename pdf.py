from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import uuid
import os
import subprocess

TEMP_LOCATION = "temp"


def make_filename():
    return os.path.join(TEMP_LOCATION, str(uuid.uuid4()) + ".pdf")


PAGE_SIZE = A4
TOP_MARGIN = 20  # mm
LEFT_MARGIN = 20  # mm
RIGHT_MARGIN = LEFT_MARGIN
BOTTOM_MARGIN = TOP_MARGIN
LINE_NUM_MARGIN = 10  # mm
BODY_MARGIN = 5  # mm
POINT = 10 # mm
LINE_HEIGHT = POINT * 0.9
CHAR_WIDTH = POINT * 0.55  # mm fixed for consolas. use fonttools to calculate according to text width
WATERMARK_GRAY = 0.95

CHAR_LINE = int((PAGE_SIZE[0] -
             LEFT_MARGIN -
             RIGHT_MARGIN -
             LINE_NUM_MARGIN -
             BODY_MARGIN) / CHAR_WIDTH)  # how many characters in a line
CHAR_PAGE = int((PAGE_SIZE[1] - TOP_MARGIN - BOTTOM_MARGIN) / LINE_HEIGHT)  # how many lines on a page


def split_text(body):
    pages = [[]]
    lines = body.split("\n")
    page_i = 0
    for line in lines:
        line_i = 0
        while len(line) > line_i:
            pages[-1].append(line[line_i: line_i + CHAR_LINE])
            line_i += CHAR_LINE
            page_i += 1
            if page_i >= CHAR_PAGE:
                pages.append([])
                page_i = 0
    if not pages[-1]:
        pages.pop()
    return pages


def get_string_width(string):
    return len(string) * CHAR_WIDTH

pdfmetrics.registerFont(TTFont('Consolas', 'Consolas.ttf'))


def make_pdf(filename, body, watermark):
    WATERMARK_CHAR_WIDTH = (PAGE_SIZE[1] - TOP_MARGIN - BOTTOM_MARGIN) / len(watermark)
    WATERMARK_POINT = WATERMARK_CHAR_WIDTH / 0.55
#    filename = make_filename()
    splitted = split_text(body)
    c = canvas.Canvas(filename, pagesize=A4)
    line_num = 1
    for page in splitted:
        # c.setStrokeGray(0.8)
        # c.rect(LEFT_MARGIN, BOTTOM_MARGIN, PAGE_SIZE[0] - LEFT_MARGIN - RIGHT_MARGIN, PAGE_SIZE[1] - BOTTOM_MARGIN - TOP_MARGIN)
        c.setFillGray(WATERMARK_GRAY)
        c.setFont("Consolas", WATERMARK_POINT)
        c.rotate(-90)
#        c.drawString(-(PAGE_SIZE[1] - TOP_MARGIN), LEFT_MARGIN, watermark)
        c.rotate(180)
        c.drawString(BOTTOM_MARGIN, -(PAGE_SIZE[0] - RIGHT_MARGIN), watermark)

        c.resetTransforms()
        c.setFillGray(0)
        c.setFont("Consolas", POINT)
        for page_line_num, line in enumerate(page):
            line_num_str = str(line_num)
            y = PAGE_SIZE[1] - (TOP_MARGIN + LINE_HEIGHT * (page_line_num + 1))
            c.drawString(LEFT_MARGIN + LINE_NUM_MARGIN - get_string_width(line_num_str),
                         y,
                         line_num_str)
            x = LEFT_MARGIN + LINE_NUM_MARGIN + BODY_MARGIN

            c.drawString(x, y, line.rstrip())
            line_num += 1
        c.showPage()
    c.save()
    return filename


def print_pdf(pdf_file):
    subprocess.Popen(["PDFtoPrinter.exe", pdf_file], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
#    subprocess.check_output(["PDFtoPrinter.exe", pdf_file])
