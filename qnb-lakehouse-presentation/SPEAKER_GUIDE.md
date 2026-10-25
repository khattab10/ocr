# On-premises data lakehouse — speaker guide and slide outline

Internal briefing for a mixed audience: senior management, risk, finance, IT, and data teams.

Use this with `QNB_OnPremises_Data_Lakehouse.pptx`. Each section maps to a slide. Language is plain English; technical terms are explained in one line.

**Constraint for every slide:** the platform is fully on-premises, in the bank’s data centres, using commercially supported enterprise products only.

---

## Suggested 12-slide flow

| # | Title | Job of the slide |
|---|---|---|
| 1 | Introducing an On-Premises Data Lakehouse | Set the frame: one home for data, here, with vendor support |
| 2 | Today’s discussion | Eight topics; the decision we want |
| 3 | Our data lives in too many filing cabinets | Make the pain felt |
| 4 | Library, garage — then both, in one building | Teach the concept |
| 5 | Three layers — like a supermarket supply chain | Show how it works, including bronze / silver / gold |
| 6 | One trusted source — faster answers, safer AI | Benefits + peer-bank metrics |
| 7 | Commercial tools — inside our data centres | Platform building blocks, all on-premises |
| 8 | Wave 1 (0–12 months) | Reporting, consolidation, Customer 360 |
| 9 | Waves 2 and 3 | Fraud, credit, AML, then AI at scale |
| 10 | Know every number. Protect every customer. | Governance and operations |
| 11 | The lakehouse is how the bank does AI safely | Feature store, copilots, examples |
| 12 | Endorse the lakehouse — then spend 90 days | The ask |

---

## 1. The problem today

**Analogy:** a house with too many filing cabinets — or a messy garage. Finance has a labelled box. Risk has another. Cards live in a shoebox of Excel files. A drawer has not been opened since the last system change. When the auditor (or the CEO) asks for one number, we open five boxes.

**What is true today**

- Data is scattered across a legacy data warehouse, multiple data marts, core-system extracts, digital-channel logs, and Excel.
- Each team keeps its own copy. Copies drift. “The number” is not the same in Finance, Risk, and the business.
- Month-end, ALCO, and regulatory packs take days because teams first reconcile whose figure is right.
- Audits are painful: we cannot always show the full path of a number from source system to pack.
- AI and machine learning cannot be industrialised. Models trained on ungoverned copies are a model-risk and privacy problem.

**Close:** this is not a people problem. It is an architecture problem.

---

## 2. What is a data lakehouse?

| Idea | Analogy | In a bank |
|---|---|---|
| **Data warehouse** | Organised **library** | Excellent for finance and regulatory reports. Strict shelves. Expensive and slow when we need new kinds of data (clickstreams, documents, images, model features). |
| **Data lake** | Big storage **garage** | Economical enough to keep everything. Without discipline it becomes a junk pile — hard to find, hard to trust, hard to audit. |
| **Data lakehouse** | **Library + garage in one building** | Keep all data economically. Organise the important parts like a library. One platform for reports, risk, customer analytics, and AI. |

**One-sentence definition (for non-technical managers):**

> A data lakehouse is a single, organised home for all of the bank’s data — economical enough to keep everything, structured enough to trust for reports, risk, and AI.

---

## 3. How a lakehouse works (simple architecture)

**Analogy:** a supermarket supply chain. Goods arrive at the loading dock, are sorted in the stockroom, then appear on the shelf.

### Layer 1 — Ingestion (the loading dock)

Bring data in from core banking, cards, loans, payments, digital channels, HR, and market data. Some of it arrives on a schedule (end of day). Some of it arrives almost as it happens (payments, digital events).

### Layer 2 — Storage with bronze / silver / gold

Same data, three quality levels — like evidence, then a labelled folder, then a published pack.

| Level | Analogy | What it means |
|---|---|---|
| **Bronze** | Sealed evidence bag | Kept exactly as received. We never lose the original. Used when we must replay history or investigate. |
| **Silver** | Well-labelled folder | Cleaned and standardised. Customer IDs, dates, and product codes mean the same thing across the bank. Records are joined. |
| **Gold** | Published management pack | Business-ready tables and metrics. This is what Finance, Risk, ALCO, and the business consume. |

### Layer 3 — Consumption (the shelf)

- BI dashboards (management packs, self-service)
- Risk and finance reports (IFRS, credit, liquidity, capital)
- Data science and AI (models, later copilots)

Keep this conceptual. Do not walk through file formats or cluster design in this room.

---

## 4. Why the bank needs a lakehouse

**Benefits in plain language**

1. **One trusted source of truth** — Customer, product, and risk numbers mean the same thing in every pack.
2. **Faster reports and decisions** — Less time reconciling workbooks; shorter month-end; quicker answers to the regulator.
3. **Better support for risk, finance, and customer analytics** — Credit, liquidity, IFRS, AML, and a true Customer 360 on the same foundation.
4. **Foundation for AI and machine learning** — Models train on data we can explain, mask, and audit.

**Example metrics from real banks** (public case studies on commercially supported platforms; *not* a forecast for us)

| Peer bank | Reported result |
|---|---|
| **Krungsri Bank** | About **5×** platform performance improvement; faster regulatory reporting |
| **Bank Mandiri** | Critical processing from **7 days to hours**; loan qualification from **5 days to 1 day** |
| **Regions Bank** | **+95%** fraud capture, **−30%** false-positive alerts, **−50%** average daily fraud losses |
| **Bank Danamon** | **+300%** marketing campaign conversion; **−30%** fraud incidents |
| **Bank BRI** | Fraud detection from **two months to seconds** |

If challenged: these are vendor-published case studies. Wave 1 will produce our own business case.

---

## 5. On-premises enterprise tools and platform

**Headline:** nothing leaves the bank. Every component is a commercially supported product we deploy, harden, and operate in our own data centres.

| Building block | Typical on-premises product class | What the business should hear |
|---|---|---|
| Enterprise data platform / lakehouse suite | e.g. **Cloudera Data Platform** (or equivalent) installed here | One place for bronze, silver, and gold; built for regulated industries |
| Enterprise SQL / analytics engine | e.g. **Starburst Enterprise** or the platform’s own SQL engine | Finance, Risk, and analysts keep using SQL they already know |
| Enterprise catalog and governance | e.g. **Collibra**, **Informatica**, or the platform’s governance module | Glossary, lineage, and access policy in one catalogue |
| Enterprise integration / ETL | e.g. **Informatica PowerCenter** or **IBM DataStage** | Supported, auditable pipelines from core systems |
| Enterprise BI | e.g. **Power BI Report Server** or **Tableau Server**, connected to on-prem gold | Dashboards without data leaving the data centre |

**Do not use this briefing to discuss public-cloud services or cloud-managed offerings.** The constraint is policy: fully on-premises, vendor-supported, hardened for a regulated bank. Nothing is “open-source only.”

---

## 6. Priority use cases (roadmap in waves)

### Wave 1 — 0 to 12 months — get the house in order

| Use case | What changes for the business |
|---|---|
| **EDW modernisation and data consolidation** | The warehouse, marts, and key Excel extracts move onto one platform. Duplicate copies start to retire. |
| **Regulatory and financial reporting acceleration** | Packs for Finance, the regulator, and ALCO become a production process with lineage, not a heroic workbook exercise. |
| **Customer 360 and self-service analytics** | One view of the customer across products. Analysts explore gold data in BI tools, within their access rights, instead of waiting in an IT queue. |

**Wave 1 outcome:** trust the numbers · close the books faster · see the customer as one person.

### Wave 2 — 6 to 18 months — protect the bank in the moment

| Use case | What changes for the business |
|---|---|
| **Near-real-time fraud detection** | Score transactions as they happen. Stop more fraud; bother genuine customers less. |
| **Intraday credit risk / limits monitoring** | See utilisation and early-warning signals during the day, not in tomorrow’s batch file. |
| **AML optimisation** | Fewer false positives, faster case handling, clearer stories for the regulator. |

**Wave 2 outcome:** Risk and financial-crime teams work from live, trusted data instead of last night’s file.

### Wave 3 — 12 to 36 months — industrialise intelligence

| Use case | What changes for the business |
|---|---|
| **Feature store and MLOps at scale** | Reuse approved data “ingredients.” Models go live the same controlled way every time. |
| **GenAI assistants for analysts / risk / finance** | Ask questions in plain language; draft reports from gold data; a human remains accountable. |
| **Hyper-personalisation and real-time offers** | Right offer, right channel, right moment — on data we can defend to Compliance. |

**Wave 3 outcome:** AI is no longer a pilot on a side system. It runs on the data the bank already trusts.

**Discipline:** Wave 3 does not start at scale until lineage, masking, and the model inventory are working.

---

## 7. Governance and operating model

A lakehouse without governance is just a bigger garage.

### Three controls

1. **Data catalog and lineage** — We know where each number comes from, who owns it, and how it was transformed. Like a library catalogue plus a paper trail. When Audit asks “why is NPL 1.4%?”, we show core system → gold table → pack.
2. **Access control and masking** — Only the right people see sensitive data. Card numbers, national IDs, and salaries are masked by default.
3. **Data quality rules** — Checks for completeness, accuracy, and timeliness before data is promoted to gold. Bad data does not silently reach the management pack.

### Operations

- **Separate workloads** — BI, risk calculations, and data science do not crowd each other out (the daily finance pack is not delayed by a model-training job).
- **Cost monitoring and control** — We see who uses what, so the platform stays affordable.
- **DevOps / automation** — Pipelines and models are deployed the same reliable way every time.

**Owners (keep this light in the room):** Data Management runs the platform with IT. Finance, Risk, and Compliance own their gold products. A governance forum arbitrates definitions.

---

## 8. AI and future work

The lakehouse is how the bank does AI **safely**.

**How it becomes the AI platform**

- **Unified, governed data for models** — No more “can we have a copy for the data science team?”
- **Feature store and model registry** — Approved ingredients; a catalogue of models in production that Risk and Audit can inspect.
- **GenAI copilot for business and risk users** — Questions in everyday language, only on data they are allowed to see.

**Concrete examples**

1. **Credit scoring** — Fairer, more accurate decisions using full customer behaviour, with explanations a credit committee can read.
2. **Collections optimisation** — Who to contact, when, and how — reducing NPLs without harming customers who would have paid anyway.
3. **Regulatory reporting assistant / relationship-manager copilot** — First draft of a supervisory pack, or a pre-meeting brief for an RM, drawn from gold data. A human signs it.

**Guardrail:** GenAI never becomes a second source of truth. It only reads gold. A human remains accountable.

---

## 9. The ask (slide 12)

1. **Endorse** the on-premises lakehouse as the bank’s strategic platform for analytics, reporting, and AI.
2. **Sponsor Wave 1** — EDW modernisation, regulatory/financial reporting, Customer 360 — with named executive sponsors.
3. **Keep it here** — commercially supported tools, fully inside our data centres, hardened for a regulated bank.

**Next 90 days**

1. Confirm target architecture and a short list of on-premises products.
2. Pick Wave 1 data domains (Finance, Risk, Customer) and source systems.
3. Stand up a governance working group: Data, Risk, Finance, IT, Compliance.
4. Produce the investment case, operating model, and success metrics.

**Close line:** we do not need another warehouse, another mart, and another Excel. We need one home for the bank’s data — organised, governed, and here.

---

## Handling likely questions

| Question | Answer in this briefing |
|---|---|
| Are we moving to the public cloud? | No. This design is fully on-premises in our data centres. |
| Is this an open-source science project? | No. Commercial products with vendor support and hardening. |
| What will it cost? | That is the 90-day investment case. Peers recoup via reporting time, fraud, and campaign lift. |
| Is this a multi-year big bang? | No. Three waves. Gold-quality gates. Start with the domains that already hurt. |
| How does this relate to our AI programme? | The lakehouse is the prerequisite. AI on ungoverned copies is a risk issue, not a strategy. |
