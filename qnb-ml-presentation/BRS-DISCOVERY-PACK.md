# QNB Group ML — BRS Discovery Pack

**Status:** Phase 0 discovery baseline  
**Source:** Executive deck [`index.html`](index.html) (business-case agenda)  
**Audience:** ExCo sponsors, Group AI/ML CoE, Model Risk, Technology, Compliance  
**Confidential — For Internal Use Only**

---

## 1. Confirmed decisions

| Decision | Confirmation |
| --- | --- |
| **Wave-1 first go-live (MVP)** | **AML false-positive reduction** — first production use case; highest regulatory urgency, clear KPI, controllable model risk. |
| **Wave-1 sequence after MVP** | Retail next-best-action → Corporate early-warning → Credit decisioning uplift. |
| **Hosting posture** | **Dual-path BRS.** Production posture follows the decision rule below. |
| **Wave-1 model family** | **Tabular / classical ML + rules hybrid** (e.g. gradient boosting). Generative / LLM deferred to Phase 2 (trade document AI, KYC narrative) unless Path A with contractual data controls is explicitly approved. |

### Hosting decision rule

```
IF outbound internet forbidden
   OR customer/transaction/KYC data must not leave bank perimeter
THEN Path B — air-gapped on-prem / private DC, open-source stack, offline model & package import
ELSE IF regulator + residency allow approved CSP (or sovereign / private cloud) with controlled egress
THEN Path A — secure cloud / hybrid landing zone
ENDIF
```

**Restricted-bank default:** Path B is the **primary production** posture for training and inference on sensitive data. Path A may be used only for non-sensitive sandboxes if policy allows.

---

## 2. Discussion focus order

Each item unlocks the next. Do not skip hosting or data boundary before detailed platform design.

1. Hosting posture (Path A vs Path B) — **decided via rule above**
2. First production use case — **AML FP reduction**
3. Data boundary (residency, egress, encryption, retention)
4. Model risk & explainability (SR 11-7–aligned MRM)
5. Integration surfaces (core, TM/AML, CRM, trade, sanctions)
6. Success KPIs & Stage-Gate metrics
7. Operating model (CoE, embedded squads, Board Risk reporting)

```
HostingPosture → Wave1MVP → DataBoundary → ModelRiskMRM → Integrations → KPIsAndGates → OperatingModel
```

---

## 3. Discovery question log

Use this log in Phase 0 workshops. Record owner, answer, and date. Items marked **CONFIRMED** are baselines from this pack; remaining items are open.

### A. Business & scope

| # | Question | Status | Baseline / notes |
| --- | --- | --- | --- |
| A1 | Which Wave-1 case is first go-live? | **CONFIRMED** | AML false-positive reduction |
| A2 | What is explicitly out of scope for Phase 0–1? | Open | Proposed: generative LLM, trade doc AI, IFRS 9 refresh, international franchise rollout |
| A3 | Executive sponsor and ops owner per use case? | Open | AML → Compliance; NBA → Retail; EWS → Corporate Credit; Credit scoring → Retail Credit / Risk |
| A4 | Minimum viable outcome for Stage-Gate 1? | Open — KPI draft in §4 | FP reduction on pilot portfolio with no material increase in true-positive miss rate |
| A5 | International franchise: HQ-first or Group-wide stack? | Open | Recommend HQ-first, then replicate under CoE standards |

### B. Regulatory, risk & audit

| # | Question | Status | Baseline / notes |
| --- | --- | --- | --- |
| B1 | Which supervisors/standards apply? | Open | QCB, correspondent-bank expectations, IFRS 9 (later waves), AML effectiveness |
| B2 | Explainability required per use case? | **CONFIRMED direction** | Credit & AML: reason codes / SHAP-class; NBA: lighter; no black-box for credit decisions |
| B3 | Independent validation & sign-off? | Open | Model inventory + independent validators; Board Risk Committee quarterly |
| B4 | Audit logs, investigator overrides, customer explanation rights? | Open | Required for AML and credit; retention per bank policy |

### C. Data

| # | Question | Status | Baseline / notes |
| --- | --- | --- | --- |
| C1 | Systems of record & freshness SLAs? | Open | TM/AML, core banking, KYC, CRM, trade, sanctions lists |
| C2 | PII/PCI handling; masking; synthetic non-prod? | Open | Mandatory for both paths; Path B: no external processing |
| C3 | Feature store: enterprise vs per-domain? | Open | Recommend shared enterprise feature store from Phase 1 |
| C4 | Labeled AML history (SAR / T/F positives) sufficient? | Open | Gate for supervised AML model; unsupervised / hybrid if labels thin |

### D. Non-functionals

| # | Question | Status | Baseline / notes |
| --- | --- | --- | --- |
| D1 | Latency: real-time vs batch? | Open | AML scoring: near-real-time or intra-day queue; EWS/IFRS 9: batch; credit/NBA: real-time API |
| D2 | Availability, RPO/RTO, DR? | Open | Dual-site for Path B; multi-AZ / secondary region for Path A |
| D3 | Peak volumes (txn/sec, concurrent inference)? | Open | Size GPU/CPU from TM peak + credit decision peaks |
| D4 | Human-in-the-loop & override policy? | Open | Investigator queue prioritisation; RM / underwriter overrides logged |

### E. Security & network (path-splitting)

| # | Question | Status | Baseline / notes |
| --- | --- | --- | --- |
| E1 | Outbound internet for APIs, mirrors, telemetry? | **Decision input** | No → Path B; Yes with controls → Path A possible |
| E2 | IdP, secrets, HSM / key custody? | Open | Bank-approved IdP; CMK / HSM for both paths |
| E3 | May CSP or SaaS LLM vendors touch data? | **Decision input** | No → Path B; Path A only with contractual + technical controls |

### F. People & delivery

| # | Question | Status | Baseline / notes |
| --- | --- | --- | --- |
| F1 | In-house DS vs SI partners; MLOps / MRM gaps? | Open | Hire–build–partner under CoE standards |
| F2 | Change management for investigators / RMs / underwriters? | Open | Adoption metric for Stage-Gates |
| F3 | CapEx (on-prem) vs OpEx (cloud) vs deck envelope? | Open | Path B CapEx-heavy; Path A OpEx; align to QAR 120–180m / 3 yrs framing |

---

## 4. MVP scope — AML false-positive reduction

### In scope (Phase 0–1)

- Score existing TM alerts by true-risk likelihood (supervised and/or unsupervised)
- Suppress or deprioritise low-value noise; prioritise investigator queues
- Reason-code / feature contribution for investigator review
- Champion–challenger vs current rules engine
- Pilot portfolio → production under MRM clearance
- Monitoring: FP rate, TP recall/miss rate, investigator handle time, override rate

### Out of scope (until Phase 2+)

- Generative case narratives / LLM summarisation of SARs
- Full TM engine replacement (uplift scoring layer first)
- Cross-border franchise rollout
- Trade document AI and KYC free-text LLM triage

### Stage-Gate KPI draft (to be baselined in Phase 0)

| KPI | Direction | Gate note |
| --- | --- | --- |
| False-positive rate | ↓ | Primary value metric |
| True-positive miss / recall | Hold or improve | Hard constraint — no material degradation |
| Alerts per investigator FTE | ↓ or productivity ↑ | Adoption / capacity |
| Mean time to disposition | ↓ | Ops outcome |
| Model stability / drift alerts | Within threshold | MRM |
| Override rate | Monitored | Process health |

### Downstream Wave-1 KPIs (after AML MVP)

| Use case | Primary KPI |
| --- | --- |
| Retail NBA | Conversion / product uptake uplift |
| Corporate EWS | Lead time vs traditional watchlist (months earlier) |
| Credit decisioning | Approval uplift for good risk with stable risk metrics |

---

## 5. Shared BRS chapters (both paths)

Regardless of hosting, the BRS / SDD must include:

1. Use cases & KPIs (this pack §§3–4)
2. Data contracts & lineage
3. Model Risk Management (inventory, validation, fairness, explainability)
4. Integration interfaces (TM, core, CRM, sanctions)
5. Non-functional requirements (latency, availability, DR)
6. Security baseline (IdP, secrets, encryption, audit)
7. Stage-Gate funding & Board Risk reporting
8. **Deployment appendix** — Path A or Path B (or hybrid: Path B prod + Path A sandbox)

---

## 6. Architecture appendix — Path A (cloud / hybrid)

**Fit when:** Residency and regulator allow approved CSP (or sovereign / private cloud); controlled egress; managed services under contract + encryption.

### Reference shape

| Layer | Choice |
| --- | --- |
| Landing zone | Private VPC, private endpoints, no public model endpoints |
| Platform | Managed K8s or Databricks / SageMaker-class + feature store + MLOps (registry, CI/CD, monitoring) |
| Models (Wave-1) | Classical ML (GBM family) for AML / NBA / EWS / credit |
| Models (optional later) | Managed LLM / OCR for trade / KYC **only if** data-egress policy allows |
| Integrations | Private link / VPN to on-prem core and TM; streaming or batch |
| Governance | Cloud logging → bank SIEM; model cards in central registry; customer-managed keys |

### Focus discussions

- CSP shortlist and sovereign options
- Data residency per country / franchise entity
- Exit strategy and portability of features / models
- Shared responsibility matrix
- Egress and GPU cost
- Keep LLM out of Wave-1 to reduce risk

### Risks

- Cross-border data movement
- Vendor lock-in
- Shadow AI / unsanctioned SaaS
- Correspondent-bank scrutiny of cloud AML processing

```
[On-prem Core / TM / CRM]
        | private link
[CSP Landing Zone — VPC]
  → Feature store → Training (classical ML)
  → Model registry → Inference APIs
  → Logs → Bank SIEM
  → (Optional later) Managed LLM/OCR if policy allows
```

---

## 7. Architecture appendix — Path B (air-gapped on-prem, open source)

**Fit when:** No outbound internet; customer data never leaves the DC; open-source / licensed models only; weights and packages via **approved offline transfer**.

### Reference shape

| Layer | Choice |
| --- | --- |
| Hardware | CPU / GPU cluster in bank DC (or private cloud with **no egress**); dual-site DR if required |
| Platform (illustrative OSS) | Kubernetes + MLflow / Kubeflow + Feast (or bank feature store) + MinIO (S3-compatible) + Airflow + Prometheus / Grafana — all mirrored offline |
| Models (Wave-1) | XGBoost / LightGBM / scikit-learn for AML, credit, NBA, EWS |
| Models (optional later) | Local OSS LLMs / document VLMs for trade OCR / KYC — after GPU capacity + MRM + license clearance; weights imported via secure media |
| Network | Training and inference fully internal; sanctions lists, OS, and package patches via controlled air-gap pipeline |
| Integrations | On-prem APIs / ESB to TM, core, CRM; **no SaaS LLM calls** |
| Governance | Same MRM as Path A; offline vulnerability scanning; signed model artifacts; no vendor telemetry |

### Focus discussions

- GPU CapEx, power, cooling
- Offline patch / CVE process ownership
- Who maintains the internal model zoo and package mirror
- Max model size if LLM is ever introduced
- Keep Wave-1 non-LLM (recommended)
- License compliance (Apache / MIT vs restrictive weight licenses)

### Risks

- Higher CapEx and ongoing ops burden
- Slower model and CVE refresh cycles
- Scarcity of on-prem MLOps talent
- Underestimating GPU for any future LLM workload

```
[Air-gap boundary — no egress]
[Bank DC]
  Offline import → Package mirror + Model zoo (signed)
  → K8s + MLflow + Feature store + Object store
  → Classical ML training / inference
  → ESB / APIs → TM, Core, CRM
  → SIEM (internal)
```

---

## 8. Path comparison (one page)

| Dimension | Path A — Cloud / hybrid | Path B — Air-gapped on-prem OSS |
| --- | --- | --- |
| Internet egress | Controlled, policy-bound | None for runtime |
| Data residency | CSP region / sovereign cloud | Bank DC only |
| Wave-1 models | Classical ML | Classical ML |
| LLM / OCR | Managed (policy-dependent) | Local OSS only, Phase 2+ |
| Cost profile | OpEx dominant | CapEx dominant |
| Patch / model refresh | Vendor + pipeline | Offline media / DMZ import |
| Time-to-platform | Faster if landing zone exists | Longer (hardware + mirror) |
| Lock-in risk | CSP / managed ML | Ops process & hardware |
| Best for | Approved cloud banking programmes | Restricted / no-internet banks |

---

## 9. Recommended Phase 0 next steps

1. Run discovery workshops using §3 question log; close E1/E3 to lock Path A or Path B for production.
2. Baselined AML KPIs and labeled-data audit (C4).
3. Charter Group AI / Model Risk committee; appoint Compliance sponsor for AML MVP.
4. Produce path-specific landing-zone / DC sizing paper (one of §6 or §7).
5. Stage-Gate 0 exit: hosting locked, AML MVP scope signed, seed funding released.

---

## Document control

| Field | Value |
| --- | --- |
| Version | 1.0 |
| Derived from | QNB ML Business Cases executive deck |
| Related deck slides | Addendum slides 13–15 in `index.html` |
| Change rule | Update this pack when hosting or MVP decisions change; keep question log status current |
