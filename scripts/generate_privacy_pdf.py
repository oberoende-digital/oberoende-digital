#!/usr/bin/env python3
from pathlib import Path
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, PageBreak
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'docs' / 'legal' / 'privacy-gdpr.md'
OUT = ROOT / 'public' / 'privacy-gdpr.pdf'

# Register a Unicode font available on macOS so Swedish text renders correctly.
font_candidates = [
    '/System/Library/Fonts/Supplemental/Arial.ttf',
    '/Library/Fonts/Arial.ttf',
    '/System/Library/Fonts/Helvetica.ttc',
]
font_name = 'Helvetica'
for f in font_candidates:
    if Path(f).exists() and f.endswith('.ttf'):
        pdfmetrics.registerFont(TTFont('ODBody', f))
        font_name = 'ODBody'
        break

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name='ODTitle', parent=styles['Title'], fontName=font_name,
    fontSize=22, leading=27, textColor=colors.HexColor('#132845'),
    spaceAfter=9*mm,
))
styles.add(ParagraphStyle(
    name='ODH1', parent=styles['Heading1'], fontName=font_name,
    fontSize=15, leading=19, textColor=colors.HexColor('#132845'),
    spaceBefore=5*mm, spaceAfter=2.5*mm,
))
styles.add(ParagraphStyle(
    name='ODH2', parent=styles['Heading2'], fontName=font_name,
    fontSize=12.5, leading=16, textColor=colors.HexColor('#31584D'),
    spaceBefore=3.5*mm, spaceAfter=2*mm,
))
styles.add(ParagraphStyle(
    name='ODBody', parent=styles['BodyText'], fontName=font_name,
    fontSize=9.8, leading=14, spaceAfter=2.4*mm,
))
styles.add(ParagraphStyle(
    name='ODSmall', parent=styles['BodyText'], fontName=font_name,
    fontSize=8.5, leading=12, textColor=colors.HexColor('#4a5568'),
    spaceAfter=2.2*mm,
))
styles.add(ParagraphStyle(
    name='ODBullet', parent=styles['BodyText'], fontName=font_name,
    fontSize=9.5, leading=13.5, leftIndent=4*mm,
))


def esc(s: str) -> str:
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    s = re.sub(r'`([^`]+)`', r'<font face="Courier">\1</font>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    return s


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(font_name, 8)
    canvas.setFillColor(colors.HexColor('#7a8a9a'))
    canvas.drawString(18*mm, 12*mm, 'Oberoende Digital — Privacy Policy, GDPR Notice and Cookie Notice')
    canvas.drawRightString(192*mm, 12*mm, f'Page {doc.page}')
    canvas.restoreState()

text = SRC.read_text(encoding='utf-8')
lines = text.splitlines()
story = []
current_bullets = []

def flush_bullets():
    global current_bullets
    if current_bullets:
        bullet_items = [
            ListItem(Paragraph(esc(item), styles['ODBullet']), bulletColor=colors.HexColor('#31584D'))
            for item in current_bullets
        ]
        story.append(ListFlowable(
            bullet_items,  # type: ignore[arg-type]
            bulletType='bullet', start='circle', leftIndent=8*mm, bulletFontName=font_name,
        ))
        story.append(Spacer(1, 1.5*mm))
        current_bullets = []

for line in lines:
    line = line.rstrip()
    if not line:
        flush_bullets()
        continue
    if line.startswith('# '):
        flush_bullets()
        story.append(Paragraph(esc(line[2:]), styles['ODTitle']))
    elif line.startswith('## '):
        flush_bullets()
        story.append(Paragraph(esc(line[3:]), styles['ODH1']))
    elif line.startswith('### '):
        flush_bullets()
        story.append(Paragraph(esc(line[4:]), styles['ODH2']))
    elif line.startswith('- '):
        current_bullets.append(line[2:])
    else:
        flush_bullets()
        style = styles['ODSmall'] if line.startswith('Reference guidance') or line.startswith('Version:') or line.startswith('Public PDF path:') else styles['ODBody']
        story.append(Paragraph(esc(line), style))
flush_bullets()

OUT.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(
    str(OUT), pagesize=A4,
    rightMargin=18*mm, leftMargin=18*mm, topMargin=18*mm, bottomMargin=18*mm,
    title='Oberoende Digital Privacy Policy, GDPR Notice and Cookie Notice',
    author='Oberoende Digital',
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
print(OUT.stat().st_size)
