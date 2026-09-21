# QNB Group — On-Premises Data Lakehouse

Internal executive presentation for senior management, risk, finance, IT, and data teams.

## Files

| File | Purpose |
|---|---|
| `QNB_OnPremises_Data_Lakehouse.pptx` | 12-slide PowerPoint (widescreen 16:9) |
| `SPEAKER_GUIDE.md` | Full outline, talking points, peer metrics, and Q&A |
| `build_presentation.py` | Regenerates the `.pptx` |

## Open the deck

Open `QNB_OnPremises_Data_Lakehouse.pptx` in Microsoft PowerPoint or LibreOffice Impress.

Speaker notes are on every slide (View → Notes). Use `SPEAKER_GUIDE.md` if you want the longer narrative while adapting content.

## Rebuild

```bash
pip install -r requirements.txt
python3 build_presentation.py
```

## Slide map

1. Title — Introducing an On-Premises Data Lakehouse
2. Agenda — Today’s discussion
3. Problem — Too many filing cabinets
4. Concept — Warehouse, lake, lakehouse
5. Architecture — Ingestion, bronze / silver / gold, consumption
6. Why now — Benefits and peer-bank results
7. Platform — On-premises enterprise tools
8. Wave 1 — EDW, reporting, Customer 360
9. Waves 2–3 — Fraud, credit, AML, then AI
10. Governance — Catalog, access, quality, operations
11. AI — Feature store, copilots, examples
12. Ask — Endorsement and 90-day plan

## Brand

| Token | Hex |
|---|---|
| QNB Deep Maroon | `#701C33` |
| Executive Navy | `#0A2540` |
| Premium Gold | `#C5A059` |

Typography: Calibri (standard in PowerPoint).
