# Tasks — Mission Control traceability candidate

All tasks remain open. Checked means verified, not merely implemented. Cancelled/superseded items stay visible in the ledger.

- [ ] MC-T001 [inventory] Сверить все проекты, архивы, чаты и источники; явно перечислить неизвестные. Requirements: MC-R001, MC-R009. Dependencies: none.
- [ ] MC-T002 [inventory] Зафиксировать независимые исходные списки требований/задач и версий для всех проектов. Requirements: MC-R002, MC-R003, MC-R004. Dependencies: MC-T001.
- [ ] MC-T003 [briefs] Закончить управленческие дорожные карты со ссылками на спецификации. Requirements: MC-R002, MC-R007. Dependencies: MC-T001.
- [ ] MC-T004 [controls] Связать evidence и approvals с существующими регистрами AC-401/402/403/404. Requirements: MC-R005, MC-R008. Dependencies: MC-T002.
- [ ] MC-T005 [controls] Проверить нативные пакеты, legacy adapters и миграцию без потерь; внедрить coverage gate. Requirements: MC-R004, MC-R006, MC-R009. Dependencies: MC-T002.
- [ ] MC-T006 [queues] Сформировать очереди разрешённой работы, owner action, external waiting, held. Requirements: MC-R003, MC-R007, MC-R008. Dependencies: MC-T003, MC-T004.
- [ ] MC-T007 [projection] Подготовить derived projection; допустить через применимый WSF-05 boundary. Requirements: MC-R001, MC-R005, MC-R007. Dependencies: MC-T005, MC-T006.
- [ ] MC-T008 [cadence] Подключить сверку событий и регулярные AC-407 checkpoints. Requirements: MC-R006, MC-R010. Dependencies: MC-T007.
- [ ] MC-T009 [cadence] Проверить целостность на реальной ежедневной работе собственника, включая negative controls. Requirements: MC-R001, MC-R005, MC-R008, MC-R010. Dependencies: MC-T008.
