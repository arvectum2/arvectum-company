# Arvectum Exchange — hypothesis discovery

Status: `Draft / Discovery`
Created: `2026-09-17`
Owner: `ООО «Арвектум»`
Repository: `arvectum2/arvectum-company`

## 1. Working name

**Arvectum Exchange**

Short name: `AX`.

Working descriptor:

> Российская API-first биржа машинного труда: заказчик публикует проверяемую цифровую задачу, программные исполнители конкурируют за неё, выполняют, предоставляют evidence, а расчёты происходят через российский платёжный контур.

The name is provisional until trademark/domain and market-conflict checks are completed.

## 2. Hypothesis, not portfolio promotion

Arvectum Exchange is currently a bounded Company discovery hypothesis. It is not yet an approved Product, portfolio node, capital-allocation commitment or change to the current flagship Company strategy.

Promotion requires evidence that:

1. customers will pay for machine-executable outcomes rather than only for AI implementation projects;
2. enough tasks can be specified and accepted objectively;
3. autonomous or semi-autonomous executors can deliver with acceptable quality and dispute rates;
4. Russian settlement, legal and data-locality requirements can be supported without Arvectum becoming an unlicensed financial intermediary;
5. marketplace economics can become attractive despite the two-sided liquidity problem.

## 3. Core proposition

The unit of trade is not an “AI agent” profile. The unit of trade is a **verifiable task outcome**.

Conceptual flow:

`Customer → Task → Bid/Assignment → Executor → Evidence → Acceptance → Settlement`

Legal/economic responsibility remains with a human or legal Principal. AI/software is an executor, not an independent source of Organizational Authority.

## 4. Russia-first differentiation

The discovery will test whether a Russia-first execution exchange can build a defensible advantage around:

- RUB-native settlement;
- Russian banking and SBP integration;
- digital-ruble readiness;
- Russian legal entities / individual entrepreneurs / self-employed principals;
- Russian data-locality and sovereignty requirements;
- local/self-hosted executor support;
- procurement-compatible packaging where legally applicable;
- machine-verifiable capability and execution history rather than marketing-only agent profiles.

Crypto/digital-asset settlement is not an MVP assumption and requires a separate legal and regulated-operator analysis.

## 5. Initial wedge

The first validation wedge should be narrow and objectively testable:

- code / bug-fix tasks with automated tests;
- document extraction / classification with benchmark datasets;
- structured web/research/data tasks with machine-checkable output schemas.

The first internal executor may be Arvectum's existing 24/7 local-LLM host, used as a reference worker and evidence source. This does not prove external market demand by itself.

## 6. Discovery success criteria

The hypothesis should not be promoted on architecture alone. Minimum discovery evidence should include:

- real buyer interviews or demand signals;
- real task corpus and price observations;
- at least one end-to-end paid or contractually committed pilot if legally feasible;
- measured executor success/rework/dispute economics;
- payment/legal architecture review;
- explicit stop/continue decision.

## 7. Draft roadmap

### AX-000 — Discovery framing and baseline
Status: `Current`

- define customer and task taxonomy;
- competitor / substitute map;
- Russian payments/legal/procurement boundary;
- measurable economics and evidence model;
- validate working name conflict/trademark/domain risk.

Exit: evidence-backed discovery brief and explicit assumptions register.

### AX-010 — Demand validation

- interview prospective buyers;
- collect 50–100 real task examples from public markets and target customers;
- identify recurring task categories, budgets, acceptance criteria and procurement/payment friction;
- test willingness to buy outcomes instead of bespoke agent development.

Exit: at least one validated buyer segment and one repeatable task family, or stop.

### AX-020 — Supply and execution validation

- adapt the existing 24/7 host as first bounded worker;
- implement task intake, profitability/risk filter, isolated execution and QA;
- run historical and live task simulations;
- measure completion, acceptance, latency, compute cost and human-intervention rate.

Exit: one task family with reproducible positive execution economics and bounded risk, or stop.

### AX-030 — Transaction prototype

- Principal / Executor identity;
- Task Contract;
- Assignment;
- artifact/evidence submission;
- acceptance/revision/dispute state machine;
- settlement intent and reconciliation records;
- RUB-first payment adapter prototype without Arvectum custody of customer funds.

Exit: one controlled end-to-end transaction with complete evidence trail.

### AX-040 — Closed pilot

- 3–5 buyers;
- Arvectum worker plus 2–5 external executors if available;
- one narrow category;
- real money where legally/operationally approved;
- manual exception handling allowed but measured.

Exit target: repeated paid transactions, measurable acceptance rate, bounded dispute/rework, and evidence of repeat demand.

### AX-050 — Marketplace viability review

Evaluate:

- GMV and take-rate potential;
- buyer acquisition cost / channel;
- executor supply quality;
- liquidity / time-to-match;
- payment cost;
- dispute cost;
- compliance / support burden;
- owner workload;
- strategic fit with Arvectum Company and Arvectum OS.

Decision: `STOP`, `ITERATE`, or `PROMOTE TO PORTFOLIO`.

### AX-060 — Portfolio promotion, only if approved

If AX-050 passes and the Owner explicitly approves:

- create Product Contract / ownership boundary;
- add to `docs/portfolio/PORTFOLIO.md`;
- create dedicated product repository if justified;
- define Product Owner / accountable Position;
- authorize budget, payment/provider contracts and production scope separately;
- build public MVP.

## 8. Hard boundaries during discovery

Discovery does not authorize:

- public launch;
- accepting customer funds or acting as escrow/custodian;
- signing payment-provider or regulated-financial contracts;
- production procurement integrations;
- claims of 44-FZ/223-FZ compliance without current legal verification;
- crypto settlement;
- new external spend;
- changes to Arvectum OS universal contracts for Company-specific convenience;
- treating internal execution success as proof of external market demand.
