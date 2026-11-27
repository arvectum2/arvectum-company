# AIC-01 / AIC-03 — evidence checkpoint (2026-11-27)

Status: candidate / partial evidence. No whole-account-loss rehearsal or policy approval.

## Portable starter
Six files under tools/ai_continuity, all read back from the draft branch and matched to local tested Git blob hashes:
- import_export.py: c9f2a3951c5537f207f7ea97dbd03612097ed783
- search_history.py: 7f7fcf2127b0b7d2697b199fa47892c76fdef220
- test_import.py: 4f8aafda8b6fe6f46f016b6260c03a8f89303ad7
- BOOTSTRAP.md: f0fffd4b5d0dce284c5ec114eed671fd1c41ca35
- HANDOFF.template.json: 0fa4db58028cf20fab5fe6bb18e29fc11206ba73
- README.md: 120772ef976a137abc889030132bb8c054464abb

Synthetic tests in isolated ChatGPT execution container: 9/9 unittest PASS, py_compile PASS; ZIP integrity PASS. Downloadable kit SHA-256 e404021d11d56e00776be9c6c2e4a46bf93e638634126b9b636e9a6a1609a6bc. No real account export tested. No production deployment, attachment reconstruction, full memory migration, scheduler restore or cross-provider upload. Mac mini runtime tests of the importer still pending.

## Dependency inventory (partial; no private prompts or data in Git)
| Dependency | Observation | Required preservation / gap |
|---|---|---|
| Company source | main roadmap v0.62.0 blob cf925d26d448c6891534b027ca9cfbf7fbdfe653 | retain canonical refs; no competing state |
| OS Workspace | WSF delivery blob b32d3ab489c6c62a45a8e97095288c39a173086a | existing loopback model constraint; WSF-07 AI/MCP subject to separate contract gate |
| Chat history | official account export requested by Owner, not received | retain encrypted original; validate actual parser coverage |
| ChatGPT memory, project instructions, files | incomplete inventory | review export membership and separately capture authorized missing material |
| Skills | repository exists; protected versions unchanged | verify exact published/private versions, portability and alternative execution |
| Automations | live private inventory returned 25 records; 3 enabled, 22 not enabled based on returned flags | preserve exact definitions, schedules, enable flags, last-run state privately; no auto-activation; no private prompts in Git |
| ChatGPT Sites/plugins | ARC currently reachable via existing client | independently authenticate MCP with a different client; inventory private app configurations without secrets |
| Local AI | Ollama and llama-server loopback listeners observed; five installed Ollama models reported | choose and test actual dialogue runtime; no new trust grant or model download |
| Offsite backup | current independent restore not proven | encrypted offsite copy + verified restore |

## Local AI probe
ARC run_command was used only for bounded local read and synthetic inference. Ollama had no active loaded models before each tested Ollama invocation; keep_alive=0 requested. No configurations, installed models, permissions, production queues or actual external messages changed.

One synthetic case, expected exact JSON:
{"status":"BLOCKED","next_action":"RECONCILE","resend_allowed":false}

- Qwen3-Embedding-4B, llama-server: FAIL, output not valid JSON and proposed resend; 31.21 s. This is an embedding model and not a valid dialogue replacement candidate.
- Qwen2.5:3b, Ollama: FAIL, BLOCKED/RESEND/true; 17.47 s.
- Qwen3:4b, Ollama: PASS, exact expected JSON; 17.43 s (one sample, temperature 0, think false).
No external messages sent. No independent review, model-quality equivalence, full workflow continuity or ChatGPT-free control-plane claim. Inference was local, but initiated through the existing ChatGPT/ARC connection. A single PASS is not grounds to admit autonomous consequential actions. Deterministic policy enforcement and multi-case evaluation remain required.

## State
AIC-01: partial, bootstrap and handoff template saved; complete project/account inventory and exact private definitions remain.
AIC-02: prototype tested on synthetic archive; actual export pending.
AIC-03: local independent inference evidence exists; whole-account-loss access remains CE-1, independent client and auth not tested.
AIC-04: live automation inventory observed; private export, reconciliation and scheduler migration not executed.
AIC-05/06: not executed.
Next: store exact automation definitions in an approved owner-controlled encrypted destination (not Git), verify recoverability; conduct a clean non-ChatGPT client read-only ARC test. Do not automatically reactivate inactive/expired tasks. Preserve prior WSF and Company gates.
