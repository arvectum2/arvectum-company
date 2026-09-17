# Arvectum Company Portfolio

Status: `Active`
Version: `0.9.0`
Created: `2026-08-20`
Updated: `2026-09-17`
Owner: `ООО «Арвектум»`
Repository: `arvectum2/arvectum-company`
Current governance baseline: `AC-307 — Approved 1.0.0 / M3 Complete / PASS`

## 1. Publication model

Эта редакция `0.9.0` сохраняет полный portfolio baseline `0.8.0` по immutable git blob и добавляет Owner-directed отдельный product-discovery node `PORT-008 — Arvectum Work` без silent re-ranking существующего портфеля.

Предыдущая редакция:

- version: `0.8.0`;
- path: `docs/portfolio/PORTFOLIO.md`;
- immutable git blob SHA: `8a77be35225f9c8c4958531e52a4131abda13d0f`.

Arvectum Work initiation:

- Owner decision: `docs/governance/decisions/DECISION-2026-09-17-ARVECTUM-WORK-INITIATION.md`;
- Company footprint: `docs/portfolio/ARVECTUM-WORK-PORTFOLIO-FOOTPRINT.md`;
- canonical product repository: `arvectum2/arvectum-work`.

Approved AC-301…AC-307 остаются в силе и являются составными слоями M3 baseline. Добавление PORT-008 является новым attributable portfolio action и не переписывает историческую AC-307 evidence.

## 2. Current governed portfolio map

| ID | Company-level name | Canonical repository | Disposition | Accountable Position | Role | Priority |
|---|---|---|---|---|---|---|
| `PORT-001` | `Arvectum Tender Agent` | `arvectum/tender-agent` | `continue` | `POS-003 — Portfolio & Product Lead` | standalone + `RI-OS-CONSUMER` | `A2` bounded revenue/pilot/evidence |
| `PORT-002` | `Discount Parser` | `arvectum/discount-parser` | `continue` | `POS-003 — Portfolio & Product Lead` | standalone + `RI-OS-CONSUMER + RI-PRODUCT-FAMILY` | `A1` finish/accept/stabilize/maintain |
| `PORT-003` | `Arvectum Proxy Launcher` | `arvectum/proxy-launcher` | `continue` | `POS-003 — Portfolio & Product Lead` | standalone | `B1` named-trigger |
| `PORT-004` | `Creative Test Agent` | `arvectum/creative-test-agent` | `continue` | `POS-003 — Portfolio & Product Lead` | standalone + `RI-OS-CONSUMER` | `B2` named-trigger |
| `PORT-005` | `Tender Small-Volume Calculator` | `arvectum/tender-app` | `contain` | `POS-003 — Portfolio & Product Lead` | `RI-PRODUCT-FAMILY` | `D1` contain/reference |
| `PORT-006` | `Doors Parser` | `arvectum/doors_parser` | `contain` | `POS-003 — Portfolio & Product Lead` | `RI-PRODUCT-FAMILY` | `D2` contain/support/reference |
| `PORT-007` | `Data Platform` | `arvectum/data-platform` | `clarify` | `POS-003 — Portfolio & Product Lead` | clarification-only Company/product-family module candidate | `C1` clarification-only; no material build |
| `PORT-008` | `Arvectum Work` | `arvectum2/arvectum-work` | `discover` | `POS-003 — Portfolio & Product Lead` | separate product discovery; machine-work transaction hypothesis | `Owner-directed bounded discovery; no portfolio re-ranking inferred` |

## 3. Dependency and Arvectum OS boundary

Между `PORT-001…PORT-008` не установлено обязательной hard runtime/code/data dependency только из common ownership, common stack, concept similarity или reference evidence.

Current governed OS correspondence:

| Node | OS boundary | Exact current platform dependency |
|---|---|---|
| `PORT-001` | P6.02 + supplemental P8.03 | `CAP-001 + CAP-004` в exact bounded scopes |
| `PORT-002` | P6.06 | `CAP-004 only` |
| `PORT-004` | P8.06 optional external extension | `CAP-004 only` |
| `PORT-003` | none evidenced | none inferred |
| `PORT-005` | none evidenced | none inferred |
| `PORT-006` | none evidenced | none inferred |
| `PORT-007` | none evidenced | none inferred |
| `PORT-008` | none evidenced | none inferred; no Work Product Contract created by Company decision |

P6.02 historical locator `arutyunoveth/ai-corporation` remains reconciled by its existing Approved Arvectum OS provenance overlay. Existing Product Contracts retain their own lifecycle and semantics.

Reference/reuse evidence does not create shared runtime, library, datastore, module, Platform Capability or Product Contract automatically.

## 4. Default portfolio decision order

The existing AC-307 default decision order remains unchanged:

```text
A1  PORT-002 — Discount Parser
A2  PORT-001 — Arvectum Tender Agent
    ↓
B1  PORT-003 — Arvectum Proxy Launcher   ┐
B2  PORT-004 — Creative Test Agent       ├─ named trigger only
    ↓                                     ┘
C1  PORT-007 — Data Platform — clarification only
    ↓
D1  PORT-005 — Tender Small-Volume Calculator
D2  PORT-006 — Doors Parser
```

`PORT-008 — Arvectum Work` is added as a separate Owner-directed **bounded discovery** initiative. Its addition does not silently assign an A/B/C/D rank, cancel existing obligations, create a funding allocation or make Work the Company flagship.

Until another attributable Company decision says otherwise, Work discovery must remain lightweight and evidence-driven under the existing Company priority rule:

`P0 obligations/cash/material risk → P1 flagship evidence + real operating model → P2 revenue/obligation/evidence-linked product/OS work → P3 speculative expansion`.

## 5. M3 closure result

`M3 — Product/module-candidate portfolio governed as investments` remains:

`Complete / PASS`.

The 2026-09-17 addition of PORT-008 is a prospective portfolio update. It does not invalidate historical M3 evidence or imply that PORT-008 itself has completed market, economic, legal or operational validation.

## 6. Arvectum Work discovery boundary

Current Work phase:

`Discovery`.

Current product sequence:

`AW-000 → AW-010 → AW-020 → AW-030 → AW-040 → AW-050 → AW-060`.

Company expects evidence in the following order:

- buyer demand;
- repeatable machine-executable Job family;
- reliable Acceptance;
- measured Worker/unit economics;
- first real accepted paid end-to-end transaction;
- repeat-demand path;
- evidence that marketplace mechanisms would outperform a simpler managed-service model.

`AW-100 — Marketplace MVP` is not admitted before explicit `AW-060 GO` and applicable scope/budget/architecture authority.

## 7. Carry-forward discipline

Material new evidence must trigger re-evaluation, not silent re-banding.

Especially open:

- PORT-001 — real paid/pilot/deal economics and repeatability;
- PORT-002 — live client acceptance/support boundary and post-delivery decision;
- PORT-003 — legal/IP rights-basis evidence, separate-host gates and per-app stop-gate;
- PORT-004 — real design-partner/customer/commercial evidence;
- PORT-007 — named consumers, common contract and economic/continuity case before material build;
- PORT-008 — buyer demand, paid transaction, repeatability, acceptance reliability, Worker economics, legal/payment/data contour and managed-service-vs-marketplace evidence;
- portfolio-wide — unit economics, profitability, CAC/LTV/ROI and legal/customer readiness where required for the decision at hand.

## 8. Source-of-truth rule

- this file is canonical for the Company-level portfolio map after applicable integration/approval;
- product repositories are canonical for implementation/status/domain semantics;
- `arvectum2/arvectum-work` is canonical for Arvectum Work product discovery and machine-work semantics;
- Arvectum OS is canonical for Product Contracts/platform capabilities;
- legal/accounting/customer systems are canonical for applicable legal, financial, contractual and confidential facts.

Repository locator, technical access, common ownership or common stack do not by themselves create Organizational Authority, legal/IP ownership or cross-product commitment.

## 9. Handoff

Existing Company roadmap order remains unchanged by the PORT-008 addition.

For Arvectum Work, the next product action after AW-000 integration is a combined `AW-010 / AW-020` evidence sprint. The next material Company gate specific to Work is `AW-060 — Go / Pivot / Stop` unless earlier discovery requires a Reserved Owner Decision.
