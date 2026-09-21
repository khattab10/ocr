#!/usr/bin/env python3
"""Build the QNB on-premises data lakehouse executive PowerPoint."""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt
from lxml import etree


# --- Brand (aligned with QNB executive deck) ---
NAVY = RGBColor(0x0A, 0x25, 0x40)
NAVY_MID = RGBColor(0x12, 0x33, 0x52)
NAVY_DEEP = RGBColor(0x07, 0x1A, 0x2E)
MAROON = RGBColor(0x70, 0x1C, 0x33)
MAROON_DEEP = RGBColor(0x5A, 0x16, 0x29)
GOLD = RGBColor(0xC5, 0xA0, 0x59)
GOLD_SOFT = RGBColor(0xF4, 0xEC, 0xD9)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SOFT = RGBColor(0xF8, 0xFA, 0xFC)
LINE = RGBColor(0xE2, 0xE8, 0xF0)
SLATE = RGBColor(0x64, 0x74, 0x8B)
INK = RGBColor(0x1E, 0x29, 0x3B)
BRONZE = RGBColor(0xB8, 0x73, 0x33)
SILVER_TONE = RGBColor(0x6B, 0x7C, 0x93)
GOLD_DEEP = RGBColor(0x9A, 0x7B, 0x3C)

FONT = "Calibri"
FONT_BOLD = "Calibri"

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
ML = Inches(0.52)
MR = Inches(0.52)
CONTENT_W = SLIDE_W - ML - MR
OUT = Path(__file__).resolve().parent / "QNB_OnPremises_Data_Lakehouse.pptx"


def _set_run(run, text, size, color, bold=False, italic=False, font_name=FONT):
    run.text = text
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = font_name
    rPr = run._r.get_or_add_rPr()
    for tag in ("latin", "ea", "cs"):
        el = rPr.find(qn(f"a:{tag}"))
        if el is None:
            el = etree.SubElement(rPr, qn(f"a:{tag}"))
        el.set("typeface", font_name)


def _fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def _fill_line(shape, color, line_color=None, line_pt=0.75):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    if line_color is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(line_pt)


def add_rect(slide, l, t, w, h, color, line=None, rounded=False, radius=0.08):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shp = slide.shapes.add_shape(kind, l, t, w, h)
    _fill_line(shp, color, line)
    if rounded:
        try:
            shp.adjustments[0] = radius
        except Exception:
            pass
    shp.shadow.inherit = False
    return shp


def add_oval(slide, l, t, w, h, color):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, l, t, w, h)
    _fill(shp, color)
    shp.shadow.inherit = False
    return shp


def tb(slide, l, t, w, h, text, size=14, color=INK, bold=False, italic=False,
       align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font_name=FONT):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    try:
        tf._txBody.bodyPr.set("anchor", {
            MSO_ANCHOR.TOP: "t",
            MSO_ANCHOR.MIDDLE: "ctr",
            MSO_ANCHOR.BOTTOM: "b",
        }.get(anchor, "t"))
    except Exception:
        pass
    p = tf.paragraphs[0]
    p.alignment = align
    p.space_before = Pt(0)
    p.space_after = Pt(0)
    _set_run(p.add_run(), text, size, color, bold, italic, font_name)
    return box


def multi(slide, l, t, w, h, paragraphs, anchor=MSO_ANCHOR.TOP):
    """paragraphs: list of dicts with text, size, color, bold, italic, align, space_after, space_before."""
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    try:
        tf._txBody.bodyPr.set("anchor", {
            MSO_ANCHOR.TOP: "t",
            MSO_ANCHOR.MIDDLE: "ctr",
            MSO_ANCHOR.BOTTOM: "b",
        }.get(anchor, "t"))
    except Exception:
        pass
    for i, spec in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = spec.get("align", PP_ALIGN.LEFT)
        p.space_before = Pt(spec.get("sb", 0))
        p.space_after = Pt(spec.get("sa", 4))
        if spec.get("line") is not None:
            p.line_spacing = spec["line"]
        _set_run(
            p.add_run(),
            spec.get("text", ""),
            spec.get("size", 13),
            spec.get("color", INK),
            spec.get("bold", False),
            spec.get("italic", False),
            spec.get("font", FONT),
        )
    return box


def bullets(slide, l, t, w, h, items, size=13, color=INK, gap=6, bullet="•"):
    paras = []
    for i, item in enumerate(items):
        paras.append({
            "text": f"{bullet}  {item}",
            "size": size,
            "color": color,
            "sa": gap,
            "line": 1.12,
        })
    return multi(slide, l, t, w, h, paras)


def header(slide, page, total=12, light=False):
    brand_c = RGBColor(0xFF, 0xFF, 0xFF) if light else MAROON
    page_c = RGBColor(0xB8, 0xC4, 0xD4) if light else SLATE
    tb(slide, ML, Inches(0.18), Inches(5), Inches(0.28),
       "QNB GROUP", 11, brand_c, True)
    tb(slide, SLIDE_W - MR - Inches(1.6), Inches(0.18), Inches(1.6), Inches(0.28),
       f"{page:02d}  /  {total:02d}", 11, page_c, True, align=PP_ALIGN.RIGHT)
    if not light:
        add_rect(slide, ML, Inches(0.48), CONTENT_W, Inches(0.018), GOLD)


def footer(slide, text="Confidential  ·  Internal use only  ·  On-premises data lakehouse"):
    add_rect(slide, Inches(0), Inches(7.22), SLIDE_W, Inches(0.28), SOFT)
    tb(slide, ML, Inches(7.24), CONTENT_W, Inches(0.24),
       text, 10, SLATE, False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)


def eyebrow_title(slide, eyebrow, title, deck=None, y=Inches(0.58)):
    tb(slide, ML, y, CONTENT_W, Inches(0.26), eyebrow.upper(), 11, GOLD, True)
    tb(slide, ML, y + Inches(0.26), CONTENT_W, Inches(0.42), title, 26, NAVY, True)
    if deck:
        tb(slide, ML, y + Inches(0.68), CONTENT_W, Inches(0.36), deck, 14, SLATE, False)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text.strip()


def new_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


# ---------------------------------------------------------------------------
# Slides
# ---------------------------------------------------------------------------

def slide_01_cover(prs):
    s = new_slide(prs)
    add_rect(s, 0, 0, SLIDE_W, SLIDE_H, NAVY)
    add_rect(s, Inches(9.55), 0, Inches(3.783), SLIDE_H, NAVY_DEEP)
    add_rect(s, 0, 0, Inches(0.14), SLIDE_H, GOLD)
    add_rect(s, Inches(9.55), 0, Inches(0.06), SLIDE_H, GOLD)

    tb(s, Inches(0.7), Inches(0.55), Inches(8.4), Inches(0.28),
       "QNB  ·  GROUP", 13, GOLD, True)
    add_rect(s, Inches(0.7), Inches(0.92), Inches(1.6), Inches(0.035), GOLD)

    tb(s, Inches(0.7), Inches(1.35), Inches(8.4), Inches(0.32),
       "INTERNAL DATA STRATEGY BRIEFING", 12, GOLD, True)

    multi(s, Inches(0.7), Inches(1.75), Inches(8.5), Inches(1.9), [
        {"text": "Introducing an", "size": 22, "color": WHITE, "sa": 0, "line": 1.0},
        {"text": "On-Premises", "size": 40, "color": WHITE, "bold": True, "sa": 0, "line": 1.0},
        {"text": "Data Lakehouse", "size": 40, "color": GOLD, "bold": True, "sa": 0, "line": 1.0},
    ])

    tb(s, Inches(0.7), Inches(4.05), Inches(8.4), Inches(1.0),
       "One trusted home for the bank’s data — built in our data centres, "
       "with commercially supported tools, ready for finance, risk, and AI.",
       16, RGBColor(0xC5, 0xD0, 0xDC), False)

    tb(s, Inches(0.7), Inches(6.55), Inches(8.4), Inches(0.4),
       "Confidential  ·  Data Management  ·  2026",
       12, RGBColor(0x8A, 0x9B, 0xAD), False)

    stats = [
        ("100%", "On-premises — in our own data centres"),
        ("3 waves", "Reporting, then protection, then AI"),
        ("1 home", "A single trusted source of truth"),
    ]
    y = Inches(0.85)
    for num, label in stats:
        add_rect(s, Inches(9.85), y, Inches(3.15), Inches(1.65), NAVY_MID, rounded=True, radius=0.1)
        tb(s, Inches(10.05), y + Inches(0.22), Inches(2.75), Inches(0.55),
           num, 28, GOLD, True, align=PP_ALIGN.LEFT)
        tb(s, Inches(10.05), y + Inches(0.88), Inches(2.75), Inches(0.55),
           label, 13, WHITE, False)
        y += Inches(1.9)

    notes(s, """
COVER — speaking notes
Open by saying this is not a technology fashion presentation. It is a proposal to give the bank one organised home for its data, inside our own data centres, using enterprise tools with vendor support.

Audience mix: senior management, risk, finance, IT, and data teams. Keep language plain. Promise: by the end they will know what a lakehouse is, why we need one, how it stays on-premises, and what changes for the business in three waves.
""")


def slide_02_agenda(prs):
    s = new_slide(prs)
    add_rect(s, 0, 0, SLIDE_W, SLIDE_H, WHITE)
    header(s, 2)
    eyebrow_title(
        s, "Agenda", "Today’s discussion",
        "Eight topics — from the filing-cabinet problem to a governed path for AI."
    )

    items = [
        ("01", "The problem today", "Why our data is scattered, slow, and hard to audit."),
        ("02", "What a lakehouse is", "Warehouse, lake, and lakehouse — in plain English."),
        ("03", "How it works", "Ingestion, bronze / silver / gold, and how people use it."),
        ("04", "Why the bank needs it", "One source of truth, faster decisions, peer results."),
        ("05", "On-premises platform", "Enterprise tools that run only in our data centres."),
        ("06", "Use-case roadmap", "Three waves: reporting → protection → AI."),
        ("07", "Governance", "Catalog, access, quality, and how we will operate it."),
        ("08", "Path to AI", "How the lakehouse becomes the bank’s AI foundation."),
    ]
    # 2x4 grid
    card_w = Inches(5.95)
    card_h = Inches(1.05)
    gap_x = Inches(0.22)
    gap_y = Inches(0.14)
    start_y = Inches(1.82)
    for i, (num, title, desc) in enumerate(items):
        col = i % 2
        row = i // 2
        x = ML + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)
        add_rect(s, x, y, card_w, card_h, SOFT, rounded=True, radius=0.12)
        add_rect(s, x, y, Inches(0.08), card_h, GOLD if i < 4 else MAROON)
        tb(s, x + Inches(0.22), y + Inches(0.16), Inches(0.7), Inches(0.32),
           num, 16, GOLD, True)
        tb(s, x + Inches(0.95), y + Inches(0.16), Inches(4.75), Inches(0.32),
           title, 15, NAVY, True)
        tb(s, x + Inches(0.95), y + Inches(0.5), Inches(4.75), Inches(0.42),
           desc, 12, SLATE, False)

    footer(s)
    notes(s, """
AGENDA — speaking notes
Walk the room through the journey: problem → concept → architecture → business case → tools (all on-premises) → roadmap → control → AI.

Decision we want: endorsement to design and stand up an on-premises lakehouse as the bank’s system of record for analytics, reporting, and future AI — with no data leaving our data centres.
""")


def slide_03_problem(prs):
    s = new_slide(prs)
    add_rect(s, 0, 0, SLIDE_W, SLIDE_H, WHITE)
    header(s, 3)
    eyebrow_title(
        s, "The problem today",
        "Our data lives in too many filing cabinets",
        "Every team has a cabinet. Copies multiply. Nobody is sure which folder is the original."
    )

    # Analogy banner
    add_rect(s, ML, Inches(1.78), CONTENT_W, Inches(0.78), GOLD_SOFT, rounded=True, radius=0.08)
    tb(s, ML + Inches(0.28), Inches(1.86), CONTENT_W - Inches(0.5), Inches(0.62),
       "Analogy: a messy garage with a labelled box for Finance, another for Risk, a shoebox of Excel files for Cards, "
       "and a drawer nobody has opened since the last system change. When the auditor — or the CEO — asks for one number, we open five boxes.",
       13, NAVY, False)

    cards = [
        ("Scattered systems",
         "Core banking, cards, loans, digital channels, finance, and risk each keep their own version of the customer and the balance sheet."),
        ("Excel as a system of record",
         "Critical numbers live in personal workbooks. When someone is on leave, the “official” report is missing."),
        ("Slow reporting and decisions",
         "Month-end, ALCO, and regulatory packs take days because teams first argue whose number is right."),
        ("Painful audits — blocked AI",
         "We struggle to show where a figure came from. Data science cannot safely train models on copies we cannot govern."),
    ]
    card_w = Inches(2.95)
    gap = Inches(0.18)
    y = Inches(2.72)
    h = Inches(3.18)
    for i, (title, body) in enumerate(cards):
        x = ML + i * (card_w + gap)
        add_rect(s, x, y, card_w, h, SOFT, rounded=True, radius=0.1)
        add_oval(s, x + Inches(0.22), y + Inches(0.22), Inches(0.38), Inches(0.38), MAROON)
        tb(s, x + Inches(0.22), y + Inches(0.24), Inches(0.38), Inches(0.34),
           str(i + 1), 14, WHITE, True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        tb(s, x + Inches(0.2), y + Inches(0.78), Inches(2.55), Inches(0.7),
           title, 15, NAVY, True)
        tb(s, x + Inches(0.2), y + Inches(1.5), Inches(2.55), Inches(1.5),
           body, 13, INK, False)

    footer(s)
    notes(s, """
THE PROBLEM — speaking notes
Tell it as a story, not an IT architecture complaint.

Today the bank’s data is fragmented: a legacy data warehouse, multiple data marts, core-system extracts, and Excel. Each copy drifts. Finance, Risk, and the business often show different numbers for the “same” KPI.

Consequences in banking language:
• Reporting is slow. We spend time reconciling, not deciding.
• Audits and regulatory reviews are painful because lineage is incomplete.
• Customer analytics is incomplete — we do not see one customer across products.
• AI and machine learning cannot be industrialised. Models trained on ungoverned copies are a model-risk and privacy problem.

Close: this is not a people problem. It is an architecture problem. A lakehouse is how we fix it.
""")


def slide_04_what(prs):
    s = new_slide(prs)
    add_rect(s, 0, 0, SLIDE_W, SLIDE_H, WHITE)
    header(s, 4)
    eyebrow_title(
        s, "What is a data lakehouse?",
        "Library, garage — then both, in one building",
        "Three ideas. One sentence you can repeat in a management meeting."
    )

    cards = [
        (NAVY, WHITE, GOLD, "Data warehouse", "The organised library",
         "Shelves, a catalogue, and strict rules. Excellent for finance and regulatory reports. Expensive and slow when we need new kinds of data — clickstreams, documents, images, or model features."),
        (NAVY_MID, WHITE, GOLD, "Data lake", "The big storage garage",
         "You can put everything in it, economically. Without discipline it becomes a junk pile: hard to find, hard to trust, hard to audit. A lake alone is not enough for a bank."),
        (MAROON, WHITE, GOLD, "Data lakehouse", "Library + garage in one",
         "Keep all data economically. Organise the important parts like a library. One platform for reports, risk, customer analytics, and AI — with the controls a bank needs."),
    ]
    card_w = Inches(3.95)
    gap = Inches(0.2)
    y = Inches(1.78)
    h = Inches(3.55)
    for i, (bg, fg, accent, title, subtitle, body) in enumerate(cards):
        x = ML + i * (card_w + gap)
        add_rect(s, x, y, card_w, h, bg, rounded=True, radius=0.08)
        add_rect(s, x, y, card_w, Inches(0.08), accent)
        tb(s, x + Inches(0.28), y + Inches(0.28), Inches(3.4), Inches(0.28),
           f"0{i+1}", 12, accent, True)
        tb(s, x + Inches(0.28), y + Inches(0.58), Inches(3.4), Inches(0.4),
           title, 18, fg, True)
        tb(s, x + Inches(0.28), y + Inches(1.02), Inches(3.4), Inches(0.36),
           subtitle, 14, accent, True)
        tb(s, x + Inches(0.28), y + Inches(1.5), Inches(3.4), Inches(1.8),
           body, 13, RGBColor(0xE8, 0xEE, 0xF4) if bg != MAROON else RGBColor(0xF3, 0xE4, 0xE8), False)

    add_rect(s, ML, Inches(5.5), CONTENT_W, Inches(1.45), GOLD_SOFT, rounded=True, radius=0.08)
    tb(s, ML + Inches(0.3), Inches(5.62), CONTENT_W - Inches(0.5), Inches(0.28),
       "ONE-SENTENCE DEFINITION  (for non-technical managers)", 11, MAROON, True)
    tb(s, ML + Inches(0.3), Inches(5.92), CONTENT_W - Inches(0.5), Inches(0.85),
       "A data lakehouse is a single, organised home for all of the bank’s data — economical enough to keep everything, "
       "structured enough to trust for reports, risk, and AI.",
       16, NAVY, True)

    footer(s)
    notes(s, """
WHAT IS A LAKEHOUSE — speaking notes
Use the analogies. Do not dive into file formats.

Warehouse = library. We already have one (or several). It is organised, but it cannot cheaply hold everything, and it is slow to change.

Lake = garage. Cheap storage for everything, including messy and new data. On its own, it is not trustworthy enough for finance or the regulator.

Lakehouse = one building with a garage and a library. Raw material stays in the garage (bronze). Clean folders sit on the shelves (silver). Published reports sit on the reading table (gold).

Repeat the one-sentence definition slowly. That is the slide they should remember.
""")


def slide_05_how(prs):
    s = new_slide(prs)
    add_rect(s, 0, 0, SLIDE_W, SLIDE_H, WHITE)
    header(s, 5)
    eyebrow_title(
        s, "How a lakehouse works",
        "Three layers — like a supermarket supply chain",
        "Goods arrive at the loading dock, are sorted in the stockroom, then appear on the shelf for the business."
    )

    layers = [
        ("1", "Ingestion", "Bringing data in",
         "Core banking, cards, loans, payments, digital channels, HR, and market data. Scheduled batches and near-real-time feeds."),
        ("2", "Storage", "Keeping it organised",
         "One platform, three quality levels: bronze, silver, and gold. Same data, increasing trust."),
        ("3", "Consumption", "Putting it to work",
         "BI dashboards, finance and risk reports, customer analytics, and data science / AI — all reading from gold (and silver where needed)."),
    ]
    w = Inches(3.95)
    gap = Inches(0.2)
    y = Inches(1.72)
    for i, (num, title, sub, body) in enumerate(layers):
        x = ML + i * (w + gap)
        add_rect(s, x, y, w, Inches(2.05), SOFT, rounded=True, radius=0.1)
        add_oval(s, x + Inches(0.2), y + Inches(0.2), Inches(0.36), Inches(0.36), NAVY)
        tb(s, x + Inches(0.2), y + Inches(0.22), Inches(0.36), Inches(0.32),
           num, 14, GOLD, True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        tb(s, x + Inches(0.66), y + Inches(0.18), Inches(3.1), Inches(0.28),
           title, 16, NAVY, True)
        tb(s, x + Inches(0.66), y + Inches(0.46), Inches(3.1), Inches(0.24),
           sub, 12, GOLD_DEEP, True)
        tb(s, x + Inches(0.2), y + Inches(0.82), Inches(3.55), Inches(1.1),
           body, 12, INK, False)

    # Bronze / silver / gold
    tb(s, ML, Inches(3.92), CONTENT_W, Inches(0.28),
       "INSIDE STORAGE:  three quality levels", 12, MAROON, True)

    metals = [
        (BRONZE, WHITE, "Bronze  ·  raw", "Sealed evidence bag",
         "Kept exactly as received. We never lose the original. Used when we must replay or investigate."),
        (SILVER_TONE, WHITE, "Silver  ·  cleaned", "Well-labelled folder",
         "Standardised names, dates, and product codes. Records joined so “customer” means the same thing."),
        (GOLD, NAVY, "Gold  ·  business-ready", "Published management pack",
         "Agreed tables and metrics. This is what Finance, Risk, ALCO, and the business consume."),
    ]
    mw = Inches(3.95)
    my = Inches(4.24)
    mh = Inches(2.22)
    for i, (bg, fg, title, analog, body) in enumerate(metals):
        x = ML + i * (mw + gap)
        add_rect(s, x, my, mw, mh, bg, rounded=True, radius=0.1)
        tb(s, x + Inches(0.24), my + Inches(0.16), Inches(3.5), Inches(0.3),
           title, 15, fg, True)
        tb(s, x + Inches(0.24), my + Inches(0.48), Inches(3.5), Inches(0.28),
           analog, 13, fg, False, italic=True)
        tb(s, x + Inches(0.24), my + Inches(0.86), Inches(3.5), Inches(1.2),
           body, 13, fg, False)

    footer(s)
    notes(s, """
HOW IT WORKS — speaking notes
Keep it conceptual. No file formats, no cluster talk.

Layer 1 — Ingestion: we connect once, properly, to core banking, cards, loans, digital channels, payments, HR, and market data.

Layer 2 — Storage with bronze / silver / gold:
• Bronze: raw, immutable, like a sealed evidence bag. Essential for audit.
• Silver: cleaned and joined. “Customer ID” and “product code” mean the same across the bank.
• Gold: business-ready. The IFRS number, the NPL ratio, the customer 360 view.

Layer 3 — Consumption: Power BI / Tableau packs, risk engines, finance reports, and data science all drink from the same tap.

Supermarket analogy: loading dock → stockroom (sorted by quality) → shelf.
""")


def slide_06_why(prs):
    s = new_slide(prs)
    add_rect(s, 0, 0, SLIDE_W, SLIDE_H, WHITE)
    header(s, 6)
    eyebrow_title(
        s, "Why the bank needs a lakehouse",
        "One trusted source — faster answers, safer AI",
        "Benefits in business language, plus publicly reported results from peer banks."
    )

    benefits = [
        ("01", "One source of truth",
         "Customer, product, and risk numbers mean the same thing in every pack — Finance, Risk, and the business."),
        ("02", "Faster reports and decisions",
         "Less time reconciling workbooks. Shorter month-end, faster ALCO, quicker answers to the regulator."),
        ("03", "Better risk, finance, customers",
         "Credit, liquidity, IFRS, AML, and a true Customer 360 sit on the same governed foundation."),
        ("04", "Foundation for AI and ML",
         "Models train on data we can explain, mask, and audit — not on a copy of a copy in a laptop folder."),
    ]
    y = Inches(1.72)
    left_w = Inches(6.15)
    for num, title, body in benefits:
        add_rect(s, ML, y, left_w, Inches(1.18), SOFT, rounded=True, radius=0.1)
        tb(s, ML + Inches(0.18), y + Inches(0.16), Inches(0.55), Inches(0.3),
           num, 13, GOLD, True)
        tb(s, ML + Inches(0.72), y + Inches(0.14), Inches(5.2), Inches(0.3),
           title, 15, NAVY, True)
        tb(s, ML + Inches(0.72), y + Inches(0.48), Inches(5.2), Inches(0.58),
           body, 12, INK, False)
        y += Inches(1.26)

    # Peer metrics panel
    px = Inches(6.9)
    add_rect(s, px, Inches(1.72), Inches(5.9), Inches(5.04), NAVY, rounded=True, radius=0.08)
    tb(s, px + Inches(0.28), Inches(1.86), Inches(5.35), Inches(0.28),
       "WHAT PEER BANKS HAVE REPORTED", 11, GOLD, True)
    tb(s, px + Inches(0.28), Inches(2.14), Inches(5.35), Inches(0.4),
       "Public case studies on commercially supported platforms.", 11, RGBColor(0xB8, 0xC4, 0xD4), False)

    metrics = [
        ("5×", "Faster platform performance", "Krungsri Bank · quicker regulatory packs"),
        ("Hours", "To process data (was 7 days)", "Bank Mandiri · loans 5 days → 1 day"),
        ("+95%", "Fraud capture  ·  −50% losses", "Regions Bank · −30% false-positive alerts"),
        ("+300%", "Campaign conversion", "Bank Danamon · −30% fraud incidents"),
        ("Seconds", "To detect fraud (was months)", "Bank BRI · from overnight files to live"),
    ]
    my = Inches(2.56)
    for num, label, src in metrics:
        tb(s, px + Inches(0.28), my, Inches(1.35), Inches(0.62),
           num, 16, GOLD, True, anchor=MSO_ANCHOR.MIDDLE)
        tb(s, px + Inches(1.7), my, Inches(3.9), Inches(0.32),
           label, 13, WHITE, True)
        tb(s, px + Inches(1.7), my + Inches(0.3), Inches(3.9), Inches(0.28),
           src, 11, RGBColor(0xB8, 0xC4, 0xD4), False)
        my += Inches(0.78)

    footer(s, "Confidential  ·  Peer figures are illustrative, not a forecast for QNB")
    notes(s, """
WHY WE NEED IT — speaking notes
Benefits first, then proof from peers. Stress these are published results from other banks, not a promise of identical outcomes.

1. One source of truth — stop competing versions of “the number”.
2. Speed — reporting and decision cycles compress when reconciliation dies.
3. Risk / finance / customer — same foundation for IFRS, credit, AML, and 360.
4. AI — you cannot industrialise machine learning on Excel extracts.

Peer metrics (cite as public case studies):
• Krungsri Bank: 5× system performance; faster regulatory reporting (Cloudera lakehouse).
• Bank Mandiri: processing 7 days → hours; loan qualification 5 days → 1 day.
• Regions Bank: +95% fraud capture, −30% false positives, −50% average daily fraud losses.
• Bank Danamon: +300% campaign conversion; −30% fraud incidents.
• Bank BRI: fraud detection from two months to seconds.

If challenged on numbers: they are vendor-published case studies. We will build our own business case in Wave 1.
""")


def slide_07_platform(prs):
    s = new_slide(prs)
    add_rect(s, 0, 0, SLIDE_W, SLIDE_H, WHITE)
    header(s, 7)
    eyebrow_title(
        s, "On-premises enterprise platform",
        "Commercial tools — inside our data centres",
        "No data leaves the bank. Every component is a commercially supported product we deploy and harden ourselves."
    )

    blocks = [
        ("01", "Lakehouse platform",
         "Enterprise data platform / lakehouse suite (e.g. Cloudera Data Platform) installed in our data centres. Stores bronze, silver, and gold. Built for regulated industries."),
        ("02", "SQL & analytics engine",
         "Enterprise SQL engine (e.g. Starburst Enterprise or the platform’s own engine). Finance, Risk, and analysts keep using SQL they already know."),
        ("03", "Catalog & governance",
         "Enterprise catalog (e.g. Collibra, Informatica, or the platform’s governance module). Business glossary, lineage, and access policy in one place."),
        ("04", "Integration / ETL",
         "Enterprise integration tool (e.g. Informatica PowerCenter or IBM DataStage). Supported, auditable pipelines from core systems into the lakehouse."),
        ("05", "Business intelligence",
         "On-premises BI (e.g. Power BI Report Server or Tableau Server) connected to gold data. Dashboards never require data to leave the data centre."),
    ]
    cw, ch = Inches(3.95), Inches(2.05)
    gap_x, gap_y = Inches(0.2), Inches(0.16)
    top = Inches(1.72)
    # First row of 3
    for i in range(3):
        x = ML + i * (cw + gap_x)
        y = top
        num, title, body = blocks[i]
        add_rect(s, x, y, cw, ch, SOFT, rounded=True, radius=0.1)
        add_rect(s, x, y, cw, Inches(0.07), GOLD)
        tb(s, x + Inches(0.22), y + Inches(0.18), Inches(3.5), Inches(0.24),
           num, 11, GOLD, True)
        tb(s, x + Inches(0.22), y + Inches(0.42), Inches(3.5), Inches(0.32),
           title, 15, NAVY, True)
        tb(s, x + Inches(0.22), y + Inches(0.78), Inches(3.5), Inches(1.15),
           body, 12, INK, False)
    # Second row of 2, centered
    row2_w = 2 * cw + gap_x
    start_x = ML + (CONTENT_W - row2_w) / 2
    for j in range(2):
        x = start_x + j * (cw + gap_x)
        y = top + ch + gap_y
        num, title, body = blocks[3 + j]
        add_rect(s, x, y, cw, ch, SOFT, rounded=True, radius=0.1)
        add_rect(s, x, y, cw, Inches(0.07), MAROON)
        tb(s, x + Inches(0.22), y + Inches(0.18), Inches(3.5), Inches(0.24),
           num, 11, MAROON, True)
        tb(s, x + Inches(0.22), y + Inches(0.42), Inches(3.5), Inches(0.32),
           title, 15, NAVY, True)
        tb(s, x + Inches(0.22), y + Inches(0.78), Inches(3.5), Inches(1.15),
           body, 12, INK, False)

    add_rect(s, ML, Inches(6.18), CONTENT_W, Inches(0.88), NAVY, rounded=True, radius=0.08)
    tb(s, ML + Inches(0.3), Inches(6.28), CONTENT_W - Inches(0.5), Inches(0.68),
       "All components run inside the bank’s data centres, with vendor support, security hardening, and auditability designed for a regulated environment. "
       "Nothing is “open-source only.” Nothing is operated outside our walls.",
       13, WHITE, False)

    footer(s)
    notes(s, """
ON-PREMISES PLATFORM — speaking notes
This is the slide that answers Risk, Compliance, and IT in one breath: we are not sending customer data outside the bank.

Emphasise:
• Fully on-premises in our data centres.
• Enterprise, commercially supported products only.
• Hardened for a regulated bank (access, encryption, logging, vendor patches).

Building blocks (typical; final shortlist in the design phase):
1. Lakehouse suite — Cloudera Data Platform or equivalent, installed here.
2. SQL engine — Starburst Enterprise or native enterprise SQL on the platform.
3. Catalog/governance — Collibra / Informatica / platform governance (e.g. Cloudera SDX).
4. ETL — Informatica PowerCenter or IBM DataStage.
5. BI — Power BI Report Server or Tableau Server, pointed at on-prem gold.

Do not mention public-cloud services or cloud-managed offerings. If asked “why not cloud?”: the bank’s policy is on-premises; this architecture respects that and still gives us a modern lakehouse.
""")


def slide_08_wave1(prs):
    s = new_slide(prs)
    add_rect(s, 0, 0, SLIDE_W, SLIDE_H, WHITE)
    header(s, 8)
    eyebrow_title(
        s, "Priority use cases  ·  Wave 1",
        "0–12 months — get the house in order",
        "What changes: leaders get one agreed view. Reporting cycles shorten. Analysts serve themselves instead of waiting in a queue."
    )

    cases = [
        ("01", "EDW modernisation & consolidation",
         "Bring the legacy warehouse, data marts, and key Excel extracts onto one platform. Reduce duplicate copies and unofficial “shadow” reports.",
         "IT and Data  ·  Finance  ·  Risk"),
        ("02", "Regulatory & financial reporting",
         "Faster, repeatable packs for Finance, the regulator, and ALCO. Every figure has a lineage trail — from gold table back to the source system.",
         "Finance  ·  Regulatory reporting  ·  Audit"),
        ("03", "Customer 360 & self-service analytics",
         "One view of the customer across deposits, cards, loans, and digital. Business users explore gold data in BI tools, within their access rights.",
         "Retail  ·  Corporate  ·  Marketing  ·  Analytics"),
    ]
    y = Inches(1.72)
    for num, title, body, owners in cases:
        add_rect(s, ML, y, CONTENT_W, Inches(1.42), SOFT, rounded=True, radius=0.1)
        add_rect(s, ML, y, Inches(0.1), Inches(1.42), GOLD)
        tb(s, ML + Inches(0.32), y + Inches(0.16), Inches(0.6), Inches(0.3),
           num, 16, GOLD, True)
        tb(s, ML + Inches(1.0), y + Inches(0.16), Inches(8.5), Inches(0.3),
           title, 16, NAVY, True)
        tb(s, ML + Inches(1.0), y + Inches(0.5), Inches(10.4), Inches(0.5),
           body, 13, INK, False)
        tb(s, ML + Inches(1.0), y + Inches(1.02), Inches(10.4), Inches(0.28),
           owners, 11, MAROON, True)
        y += Inches(1.54)

    add_rect(s, ML, Inches(6.38), CONTENT_W, Inches(0.68), NAVY, rounded=True, radius=0.08)
    tb(s, ML + Inches(0.3), Inches(6.5), CONTENT_W - Inches(0.5), Inches(0.44),
       "Wave 1 outcome:  trust the numbers  ·  close the books faster  ·  see the customer as one person.",
       15, WHITE, True)

    footer(s)
    notes(s, """
WAVE 1 — speaking notes
Wave 1 is deliberately unglamorous. It is the foundation. Without it, fraud AI and GenAI are theatre.

What changes for the business:
• Management packs stop arriving with three versions of the same KPI.
• Finance and regulatory reporting become a production process with lineage, not a heroic Excel exercise.
• A relationship manager or analyst can pull an approved customer 360 without raising a ticket that takes a week.

Scope discipline: do not try to ingest the entire bank in year one. Pick finance, risk, and customer domains that already hurt.

Success measures to mention: cycle time for key reports; number of retired marts/workbooks; % of official KPIs sourced from gold; user adoption of self-service BI.
""")


def slide_09_waves23(prs):
    s = new_slide(prs)
    add_rect(s, 0, 0, SLIDE_W, SLIDE_H, WHITE)
    header(s, 9)
    eyebrow_title(
        s, "Priority use cases  ·  Waves 2 and 3",
        "Protect the bank — then industrialise intelligence",
        "Wave 2 overlaps Wave 1. Wave 3 only starts once gold data and governance are real."
    )

    # Wave 2
    add_rect(s, ML, Inches(1.7), Inches(6.0), Inches(5.08), SOFT, rounded=True, radius=0.08)
    add_rect(s, ML, Inches(1.7), Inches(6.0), Inches(0.7), MAROON)
    tb(s, ML + Inches(0.24), Inches(1.82), Inches(5.5), Inches(0.26),
       "WAVE 2   ·   6–18 MONTHS", 12, GOLD, True)
    tb(s, ML + Inches(0.24), Inches(2.08), Inches(5.5), Inches(0.32),
       "Protect the bank in the moment", 16, WHITE, True)

    w2 = [
        ("Near-real-time fraud",
         "Score transactions as they happen. Stop more fraud, bother genuine customers less."),
        ("Intraday credit & limits",
         "See utilisation and early-warning signals during the day — not in tomorrow’s batch file."),
        ("AML optimisation",
         "Fewer false positives, faster case handling, clearer stories for the regulator."),
    ]
    y = Inches(2.55)
    for title, body in w2:
        tb(s, ML + Inches(0.28), y, Inches(5.45), Inches(0.28), title, 14, NAVY, True)
        tb(s, ML + Inches(0.28), y + Inches(0.28), Inches(5.45), Inches(0.7), body, 13, INK, False)
        y += Inches(1.05)
    tb(s, ML + Inches(0.28), Inches(6.15), Inches(5.45), Inches(0.48),
       "Business change: Risk and financial-crime teams work from live, trusted data instead of last night’s file.",
       12, MAROON, True)

    # Wave 3
    rx = Inches(6.78)
    add_rect(s, rx, Inches(1.7), Inches(6.02), Inches(5.08), NAVY, rounded=True, radius=0.08)
    tb(s, rx + Inches(0.28), Inches(1.86), Inches(5.5), Inches(0.26),
       "WAVE 3   ·   12–36 MONTHS", 12, GOLD, True)
    tb(s, rx + Inches(0.28), Inches(2.14), Inches(5.5), Inches(0.36),
       "Industrialise intelligence", 16, WHITE, True)

    w3 = [
        ("Feature store & MLOps",
         "Reuse approved data “ingredients.” Models go live the same controlled way every time."),
        ("GenAI assistants",
         "Analysts, risk, and finance ask questions in plain language and draft reports from gold data."),
        ("Hyper-personalisation",
         "Right offer, right channel, right moment — on data we can defend to Compliance."),
    ]
    y = Inches(2.62)
    for title, body in w3:
        tb(s, rx + Inches(0.28), y, Inches(5.45), Inches(0.28), title, 14, GOLD, True)
        tb(s, rx + Inches(0.28), y + Inches(0.28), Inches(5.45), Inches(0.7), body, 13, RGBColor(0xD5, 0xDE, 0xE8), False)
        y += Inches(1.05)
    tb(s, rx + Inches(0.28), Inches(6.15), Inches(5.45), Inches(0.48),
       "Business change: AI is no longer a pilot on a side system. It runs on the data the bank already trusts.",
       12, GOLD, False)

    footer(s)
    notes(s, """
WAVES 2 AND 3 — speaking notes
Wave 2 (6–18 months) is where the bank feels protection:
• Fraud: near-real-time scoring. Peer banks have reported large lifts in capture and cuts in false positives.
• Intraday credit: limits and early warning during the day — critical for corporate and cards.
• AML: less noise for investigators, faster cases, better regulator narrative.

Wave 3 (12–36 months) is scale:
• Feature store + MLOps: industrial models, not notebooks on laptops.
• GenAI copilot: natural-language query and report drafting, always on gold, always with access control.
• Hyper-personalisation: next-best offer in real time.

Governance gate: we do not start Wave 3 AI at scale until lineage, masking, and model inventory are working.
""")


def slide_10_gov(prs):
    s = new_slide(prs)
    add_rect(s, 0, 0, SLIDE_W, SLIDE_H, WHITE)
    header(s, 10)
    eyebrow_title(
        s, "Governance and operating model",
        "Know every number. Protect every customer.",
        "A lakehouse without governance is just a bigger garage. These three controls make it a bank platform."
    )

    pillars = [
        ("Catalog and lineage",
         "We know where each number comes from, who owns it, and how it was transformed.",
         "Like a library catalogue plus a paper trail. When Audit asks “why is NPL 1.4%?”, we show the path from core system → gold table → pack."),
        ("Access control and masking",
         "Only the right people see sensitive data — and even then, only what they need.",
         "Card numbers, national IDs, and salaries are masked by default. Role-based access for Finance, Risk, HR, and agencies."),
        ("Data quality rules",
         "Checks run before data is allowed to become “gold.”",
         "Completeness, accuracy, timeliness. If a feed is late or broken, the management pack does not silently go out wrong."),
    ]
    cw = Inches(3.95)
    gap = Inches(0.2)
    y = Inches(1.72)
    for i, (title, lead, body) in enumerate(pillars):
        x = ML + i * (cw + gap)
        add_rect(s, x, y, cw, Inches(3.15), SOFT, rounded=True, radius=0.1)
        add_oval(s, x + Inches(0.22), y + Inches(0.22), Inches(0.36), Inches(0.36), MAROON)
        tb(s, x + Inches(0.22), y + Inches(0.24), Inches(0.36), Inches(0.32),
           str(i + 1), 13, WHITE, True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        tb(s, x + Inches(0.22), y + Inches(0.7), Inches(3.5), Inches(0.6),
           title, 16, NAVY, True)
        tb(s, x + Inches(0.22), y + Inches(1.32), Inches(3.5), Inches(0.7),
           lead, 13, MAROON, False)
        tb(s, x + Inches(0.22), y + Inches(2.05), Inches(3.5), Inches(0.95),
           body, 12, INK, False)

    # Ops row
    ops = [
        ("Separate workloads", "BI, risk calculations, and data science do not crowd each other out."),
        ("Cost monitoring", "We see who uses what, so the platform stays affordable and fair."),
        ("Automation (DevOps)", "Pipelines and models are deployed the same reliable way every time."),
    ]
    oy = Inches(5.02)
    ow = Inches(3.95)
    for i, (title, body) in enumerate(ops):
        x = ML + i * (ow + gap)
        add_rect(s, x, oy, ow, Inches(1.52), NAVY, rounded=True, radius=0.1)
        tb(s, x + Inches(0.22), oy + Inches(0.18), Inches(3.5), Inches(0.36),
           title, 14, GOLD, True)
        tb(s, x + Inches(0.22), oy + Inches(0.58), Inches(3.5), Inches(0.78),
           body, 13, WHITE, False)

    footer(s)
    notes(s, """
GOVERNANCE — speaking notes
This is the slide for Risk, Compliance, Audit, and the CDO.

Three controls:
1. Catalog + lineage — business glossary and end-to-end paper trail. Non-negotiable for regulatory reporting.
2. Access + masking — need-to-know. Privileged access logged. Default mask of PII and secrets.
3. Quality gates — bronze can be messy; gold cannot. Promotion is a controlled step.

Operating model (keep light):
• Workload isolation so a data-science job cannot delay the daily finance pack.
• Chargeback / showback so consumption is visible.
• DevOps for data: versioned pipelines, automated tests, promotion through environments.

Owners: Data Management runs the platform with IT. Finance, Risk, and Compliance own their gold products. A data-governance forum arbitrates definitions.
""")


def slide_11_ai(prs):
    s = new_slide(prs)
    add_rect(s, 0, 0, SLIDE_W, SLIDE_H, WHITE)
    header(s, 11)
    eyebrow_title(
        s, "AI and future work",
        "The lakehouse is how the bank does AI safely",
        "AI is only as trustworthy as the data underneath. This platform is that data — governed, on-premises, and reusable."
    )

    enablers = [
        ("Unified, governed data",
         "Models train on the same gold the bank already reports. No shadow lakes on someone’s server."),
        ("Feature store & model registry",
         "Approved ingredients for models, plus a catalogue of what is in production — explainable to Risk and Audit."),
        ("GenAI copilot",
         "Business and risk users ask questions in everyday language, only on data they are allowed to see."),
    ]
    y = Inches(1.7)
    for i, (title, body) in enumerate(enablers):
        x = ML + i * (Inches(3.95) + Inches(0.2))
        add_rect(s, x, y, Inches(3.95), Inches(1.55), NAVY, rounded=True, radius=0.1)
        tb(s, x + Inches(0.22), y + Inches(0.16), Inches(3.5), Inches(0.5),
           title, 15, GOLD, True)
        tb(s, x + Inches(0.22), y + Inches(0.68), Inches(3.5), Inches(0.72),
           body, 13, WHITE, False)

    tb(s, ML, Inches(3.42), CONTENT_W, Inches(0.32),
       "THREE CONCRETE EXAMPLES", 12, MAROON, True)

    examples = [
        ("Credit scoring",
         "Fairer, more accurate decisions using full customer behaviour — with explanations a credit committee can read.",
         "Risk  ·  Retail  ·  Corporate"),
        ("Collections optimisation",
         "Who to contact, when, and how. Reduce NPLs without harming customers who would have paid anyway.",
         "Retail  ·  Special assets"),
        ("RM & reporting copilots",
         "Brief a relationship manager before a client meeting, or draft a supervisory pack, from gold data — then a human signs it.",
         "Finance  ·  Risk  ·  Corporate RMs"),
    ]
    ey = Inches(3.78)
    for i, (title, body, owners) in enumerate(examples):
        x = ML + i * (Inches(3.95) + Inches(0.2))
        add_rect(s, x, ey, Inches(3.95), Inches(2.55), SOFT, rounded=True, radius=0.1)
        add_rect(s, x, ey, Inches(0.1), Inches(2.55), GOLD)
        tb(s, x + Inches(0.28), ey + Inches(0.22), Inches(3.45), Inches(0.5),
           title, 16, NAVY, True)
        tb(s, x + Inches(0.28), ey + Inches(0.78), Inches(3.45), Inches(1.2),
           body, 13, INK, False)
        tb(s, x + Inches(0.28), ey + Inches(2.08), Inches(3.45), Inches(0.3),
           owners, 12, MAROON, True)

    footer(s)
    notes(s, """
AI — speaking notes
Connect this deck to the bank’s AI / ML agenda. The lakehouse is the prerequisite, not a rival project.

Three platform capabilities:
1. Unified governed data — ends the “can we have a copy for the data science team?” pattern.
2. Feature store + model registry — industrial ML: reusable features, versioned models, challenger/champion, model-risk evidence.
3. GenAI copilot — natural-language query and drafting, bound by the same access and masking as BI.

Examples to make it real:
• Credit scoring / limit management with explainability.
• Collections: contact strategy that lifts recovery and treats good customers fairly.
• Regulatory reporting assistant: first draft of a pack from gold tables, analyst reviews.
• Relationship-manager copilot: “What should I know before I call this corporate client?” drawn from Customer 360.

Guardrail: GenAI never becomes a second source of truth. It only reads gold, and a human remains accountable.
""")


def slide_12_close(prs):
    s = new_slide(prs)
    add_rect(s, 0, 0, SLIDE_W, SLIDE_H, WHITE)
    header(s, 12)
    eyebrow_title(
        s, "Recommendation",
        "Endorse the lakehouse — then spend 90 days making it real",
        "This is not an IT fashion. It is how the bank will trust its numbers, answer the regulator, and use AI without data leaving our walls."
    )

    asks = [
        ("1", "Endorse",
         "Name the on-premises lakehouse as the bank’s strategic platform for analytics, reporting, and AI."),
        ("2", "Sponsor Wave 1",
         "EDW modernisation, regulatory/financial reporting, and Customer 360 — with named executive sponsors."),
        ("3", "Keep it here",
         "Confirm the constraint: commercially supported tools, fully inside our data centres, hardened for a regulated bank."),
    ]
    y = Inches(1.72)
    for num, title, body in asks:
        add_rect(s, ML, y, Inches(7.35), Inches(1.28), SOFT, rounded=True, radius=0.1)
        add_oval(s, ML + Inches(0.22), y + Inches(0.42), Inches(0.44), Inches(0.44), MAROON)
        tb(s, ML + Inches(0.22), y + Inches(0.46), Inches(0.44), Inches(0.36),
           num, 16, WHITE, True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        tb(s, ML + Inches(0.82), y + Inches(0.18), Inches(6.25), Inches(0.36),
           title, 16, NAVY, True)
        tb(s, ML + Inches(0.82), y + Inches(0.56), Inches(6.25), Inches(0.58),
           body, 13, INK, False)
        y += Inches(1.4)

    # 90 days panel
    add_rect(s, Inches(8.12), Inches(1.72), Inches(4.7), Inches(4.08), NAVY, rounded=True, radius=0.08)
    tb(s, Inches(8.36), Inches(1.9), Inches(4.25), Inches(0.32),
       "NEXT 90 DAYS", 12, GOLD, True)
    steps = [
        "Confirm target architecture and a short list of on-premises products.",
        "Pick Wave 1 data domains (Finance, Risk, Customer) and source systems.",
        "Stand up a governance working group: Data, Risk, Finance, IT, Compliance.",
        "Produce the investment case, operating model, and success metrics.",
    ]
    sy = Inches(2.36)
    for i, step in enumerate(steps):
        tb(s, Inches(8.36), sy, Inches(0.4), Inches(0.28),
           f"0{i+1}", 12, GOLD, True)
        tb(s, Inches(8.76), sy, Inches(3.8), Inches(0.75),
           step, 13, WHITE, False)
        sy += Inches(0.82)

    add_rect(s, ML, Inches(6.0), CONTENT_W, Inches(1.05), GOLD_SOFT, rounded=True, radius=0.08)
    tb(s, ML + Inches(0.3), Inches(6.16), CONTENT_W - Inches(0.5), Inches(0.75),
       "The lakehouse is the bank’s filing system, library, and kitchen for AI — in one building we own. "
       "Approve the direction, and we will return with architecture, cost, and a Wave 1 plan.",
       14, NAVY, True)

    footer(s)
    notes(s, """
CLOSE — speaking notes
Ask for three things, not a blank cheque:
1. Strategic endorsement of an on-premises lakehouse.
2. Executive sponsorship of Wave 1 (EDW, reporting, Customer 360).
3. Reconfirmation that the platform stays in our data centres with enterprise vendors.

Then describe the 90-day work: architecture and product shortlist, domain selection, governance forum, investment case.

Close line: “We do not need another warehouse, another mart, and another Excel. We need one home for the bank’s data — organised, governed, and here.”

Handle Q&A:
• Cloud? Out of scope by policy. This design is fully on-premises.
• Open source only? No. Commercial products with support and hardening.
• Cost? 90-day investment case. Peer banks recoup via reporting time, fraud, and campaign lift.
• Risk of big-bang? We will not. Three waves, gold-quality gates, start with painful domains.
""")


def build():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    slide_01_cover(prs)
    slide_02_agenda(prs)
    slide_03_problem(prs)
    slide_04_what(prs)
    slide_05_how(prs)
    slide_06_why(prs)
    slide_07_platform(prs)
    slide_08_wave1(prs)
    slide_09_waves23(prs)
    slide_10_gov(prs)
    slide_11_ai(prs)
    slide_12_close(prs)

    prs.save(OUT)
    print(f"Wrote {OUT}")
    return OUT


if __name__ == "__main__":
    build()
