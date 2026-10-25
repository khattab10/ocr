#!/usr/bin/env python3
"""Build the QNB Egypt Canva-style lakehouse deck from generated slide images."""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.util import Inches


SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

ROOT = Path(__file__).resolve().parent
SLIDES_DIR = ROOT / "slides"
OUT = ROOT / "QNB_OnPremises_Data_Lakehouse.pptx"

# Generated 16:9 artwork (1280x720) — same visual language as QNB Egypt Canva templates.
SLIDE_FILES = [
    "slide_01_title.png",
    "slide_02_agenda.png",
    "slide_03_problem.png",
    "slide_04_what_is_lakehouse.png",
    "slide_05_how_it_works.png",
    "slide_06_why_we_need_it.png",
    "slide_07_onprem_platform.png",
    "slide_08_wave1.png",
    "slide_09_waves23.png",
    "slide_10_governance.png",
    "slide_11_ai.png",
    "slide_12_next_steps.png",
]

NOTES = [
    """COVER — speaking notes
Open by saying this is not a technology fashion presentation. It is a proposal to give the bank one organised home for its data, inside our own data centres, using enterprise tools with vendor support.

Audience mix: senior management, risk, finance, IT, and data teams. Promise: by the end they will know what a lakehouse is, why we need one, how it stays on-premises, and what changes for the business in three waves.
""",
    """AGENDA — speaking notes
Walk the room through the journey: problem → concept → architecture → business case → tools (all on-premises) → roadmap → control → AI.

Decision we want: endorsement to design and stand up an on-premises lakehouse as the bank’s system of record for analytics, reporting, and future AI — with no data leaving our data centres.
""",
    """THE PROBLEM — speaking notes
Tell it as a story. Today the bank’s data is fragmented: a legacy data warehouse, multiple data marts, core-system extracts, and Excel. Each copy drifts. Finance, Risk, and the business often show different numbers for the “same” KPI.

Consequences:
• Reporting is slow. We spend time reconciling, not deciding.
• Audits and regulatory reviews are painful because lineage is incomplete.
• Customer analytics is incomplete — we do not see one customer across products.
• AI cannot be industrialised on ungoverned copies.

Close: this is not a people problem. It is an architecture problem.
""",
    """WHAT IS A LAKEHOUSE — speaking notes
Warehouse = organised library. Excellent for finance and regulatory reports. Slow to add new kinds of data.

Lake = big storage garage. Economical, but without discipline it becomes a junk pile.

Lakehouse = one building with a garage and a library. Raw material stays in bronze. Clean folders sit in silver. Published reports sit in gold.

One-sentence definition: a single, organised home for all of the bank’s data — economical enough to keep everything, structured enough to trust for reports, risk, and AI.
""",
    """HOW IT WORKS — speaking notes
Supermarket analogy: loading dock → stockroom → shelf.

Ingestion: core banking, cards, loans, digital channels, payments, HR, market data.

Storage with bronze / silver / gold:
• Bronze: raw, like a sealed evidence bag.
• Silver: cleaned and joined. “Customer ID” means the same across the bank.
• Gold: business-ready. The IFRS number, the NPL ratio, the customer 360 view.

Consumption: BI packs, risk engines, finance reports, and data science all drink from the same tap.
""",
    """WHY WE NEED IT — speaking notes
1. One source of truth — stop competing versions of “the number”.
2. Faster reports — month-end, ALCO, and the regulator.
3. Better risk, finance, and Customer 360.
4. AI on data we can explain, mask, and audit.

Peer banks (public case studies, not a forecast):
• Krungsri Bank: 5× platform performance; faster regulatory reporting.
• Bank Mandiri: processing 7 days → hours; loans 5 days → 1 day.
• Regions Bank: +95% fraud capture, −30% false positives, −50% daily fraud losses.
• Bank Danamon: +300% campaign conversion; −30% fraud incidents.
• Bank BRI: fraud detection from two months to seconds.
""",
    """ON-PREMISES PLATFORM — speaking notes
Nothing leaves the bank. Commercial products we deploy and harden in our data centres.

1. Lakehouse suite — Cloudera Data Platform or equivalent, installed here.
2. SQL engine — Starburst Enterprise or native enterprise SQL.
3. Catalog/governance — Collibra / Informatica / platform governance.
4. ETL — Informatica PowerCenter or IBM DataStage.
5. BI — Power BI Report Server or Tableau Server, pointed at on-prem gold.

If asked “why not public cloud?”: bank policy is on-premises. This architecture respects that and still gives us a modern lakehouse.
""",
    """WAVE 1 — speaking notes
0–12 months. Deliberately unglamorous. Foundation first.

• EDW modernisation and consolidation — retire duplicate copies.
• Regulatory and financial reporting with lineage.
• Customer 360 and self-service analytics.

What changes: trust the numbers, close the books faster, see the customer as one person.
""",
    """WAVES 2 AND 3 — speaking notes
Wave 2 (6–18 months): near-real-time fraud; intraday credit and limits; AML with fewer false positives. Risk and financial-crime teams work from live data.

Wave 3 (12–36 months): feature store and MLOps; GenAI assistants; hyper-personalisation. AI runs on the gold data the bank already trusts.

Do not start Wave 3 at scale until lineage, masking, and the model inventory are working.
""",
    """GOVERNANCE — speaking notes
A lakehouse without governance is just a bigger garage.

1. Catalog + lineage — when Audit asks “why is NPL 1.4%?”, we show the path.
2. Access + masking — need-to-know. PII masked by default.
3. Quality gates — bronze can be messy; gold cannot.

Operations: separate BI / risk / data-science workloads; cost monitoring; automated pipelines and models.
""",
    """AI — speaking notes
The lakehouse is the prerequisite for safe AI.

• Unified governed data — no shadow copies for data science.
• Feature store and model registry — explainable to Risk and Audit.
• GenAI copilot — questions in everyday language, only on allowed gold data.

Examples: credit scoring; collections optimisation; RM briefing and regulatory-pack drafting. A human remains accountable. GenAI never becomes a second source of truth.
""",
    """CLOSE — speaking notes
Ask for three things, not a blank cheque:
1. Endorse the on-premises lakehouse as the strategic platform.
2. Sponsor Wave 1 with named executives.
3. Keep it in our data centres with enterprise vendors.

Next 90 days: architecture and product shortlist; Finance / Risk / Customer domains; governance working group; investment case.

Close: we do not need another warehouse, another mart, and another Excel. We need one home for the bank’s data — organised, governed, and here.
""",
]


def build() -> Path:
    missing = [name for name in SLIDE_FILES if not (SLIDES_DIR / name).exists()]
    if missing:
        raise SystemExit(f"Missing slide images in {SLIDES_DIR}: {missing}")

    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    blank = prs.slide_layouts[6]

    for name, note in zip(SLIDE_FILES, NOTES):
        slide = prs.slides.add_slide(blank)
        slide.shapes.add_picture(str(SLIDES_DIR / name), Inches(0), Inches(0), SLIDE_W, SLIDE_H)
        slide.notes_slide.notes_text_frame.text = note.strip()

    prs.save(OUT)
    print(f"Wrote {OUT}")
    return OUT


if __name__ == "__main__":
    build()
