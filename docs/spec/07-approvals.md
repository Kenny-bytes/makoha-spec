---
docpipe: 1
phase: 7
title: Completion and Approvals
status: final
version: 1.0
upstream: ["01-prd.md", "02-conops.md", "03-opscon.md", "04-techspec.md", "05-requirements.md", "06-validation.md"]
upstream_hash: {"01-prd.md": "945319a42d20e0ce", "02-conops.md": "978e178898dc37f9", "03-opscon.md": "2566aaa0e9b9bf55", "04-techspec.md": "a3e788961563417d", "05-requirements.md": "182f72a000933d5b", "06-validation.md": "5f7ecdaa17a52a10"}
finalised: 2026-09-25
---

# Completion and Approvals

Record that the Mākoha specification set is complete, consistent and approved for its intended purpose, with the approved versions pinned. Completion evidence is tool output from `docpipe status` and `docpipe build` on 25 Sep 2026. Identifiers minted here: APR- (approvals), CND- (conditions and follow-up actions).

## 1. Scope of approval (confirmed 25 Sep 2026)

What is approved: the seven phase documents at version 1.0 with the hashes in section 3, compiled as `docs/spec/PSD.md`, together with `docpipe.json` conventions and the Mākoha Design Compendium (25 Sep 2026) as the authoritative build specification they map to.

For what use: the build baseline for milestones M1 to M9 of the Tier 3 first release for telehealth and hospital in the home in New Zealand (PRD section 8.1), and the source of requirements, risks and verification evidence captured into Ketryx for the planned regulatory applications. This approval is not a regulatory submission, a clinical governance ratification of any fragment, or an ethics approval of any study; each of those remains with its named role.


## 2. Completion checklist (answered from tool output)

| Item | Result | Evidence |
| --- | --- | --- |
| All phases 1 to 6 final and none stale | Met | `docpipe status` 25 Sep 2026: six rows final v1.0, stale = no |
| Zero open markers | Not met; carried as condition CND-01 | 25 markers remain across phases 1 to 5, every one recorded as deferred with its reason: 11 metric baselines captured at cut-over; 2 metric targets set in Ketryx; voice turn latency at M9; availability, RPO and RTO; web framework at M7; operating organisation; payer or funder; bill tracker; standards list; consumer identity provider; pharmacist-prescriber instrument; terminology release cadence; voice acceptance test |
| Every requirement covered by validation | Met | `docpipe check 6` clean: all 187 identifiers referenced; 176 entries, 11 withdrawn listed |
| All change requests closed | Not met; carried as condition CND-02 | CCR-01 to CCR-04 and OCR-01 to OCR-03 applied upstream; CR-01 (claim-type vocabulary, target the compendium Volume 4.2, amended by CCR-04) remains open because the compendium is outside this set |
| Residual risks accepted | Pending approver | Five residual risks in 06-validation.md section 6: inspection and analysis in place of test for 21 requirements; two deferred numbers; national sandbox access; voice model selection; synthetic practice |
| Requirement syntax and identifier checks | Met | `docpipe check 5` clean apart from the two deferred numbers |
| Traceability export | Met | `docs/spec/traceability.csv` built 25 Sep 2026 |

## 3. Document register at approval

Pasted from `docs/spec/PSD.md`, built 25 Sep 2026.

| # | Document | Status | Version | Finalised | Hash |
|---|---|---|---|---|---|
| 1 | Product Requirements Document | final | 1.0 | 2026-09-25 | 945319a42d20e0ce |
| 2 | Concept of Operations | final | 1.0 | 2026-09-25 | 978e178898dc37f9 |
| 3 | Operations Concept | final | 1.0 | 2026-09-25 | 2566aaa0e9b9bf55 |
| 4 | Technical Specifications | final | 1.0 | 2026-09-25 | a3e788961563417d |
| 5 | Specific Requirements | final | 1.0 | 2026-09-25 | 182f72a000933d5b |
| 6 | Validation Activities | final | 1.0 | 2026-09-25 | 5f7ecdaa17a52a10 |

Conventions: intended purpose as recorded in `docpipe.json`; identifier pattern `\b[A-Z][A-Z0-9]{0,4}-\d{2,3}\b`; requirement syntax EARS.

## 4. Approvals

The product owner is the sole approver for this cycle (stated 25 Sep 2026). Clinical governance, compliance and architecture roles have no named holder yet; their acceptance of residual risks, standards list and deferred stack choices is carried as conditions CND-09 to CND-11.

| Id | Role | Name | Decision | Conditions | Date |
| --- | --- | --- | --- | --- | --- |
| APR-01 | Product owner | Ken Lee | Approve with conditions | CND-01 to CND-11 | 2026-09-25 |

## 5. Release decision

Go: the set is approved with conditions as the build baseline for the Tier 3 New Zealand first release, authorising M1 to M4 to start immediately and M5 onward subject to CND-03 and CND-04 (decided by the product owner, 25 Sep 2026).

## 6. Conditions and follow-up actions

| Id | Condition or action | Owner | Due |
| --- | --- | --- | --- |
| CND-01 | Resolve the 25 deferred markers at the milestone each names (cut-over, M7, M9) or by decision of the named role; none blocks M1 to M4 | Deferred owner | Per marker |
| CND-02 | Close CR-01 by closing the claim-type vocabulary in the compendium Volume 4.2 as the union list | Product owner | Before M4 (compiler templates need the closed list) |
| CND-03 | Arrange national sandbox access (Hira, HealthLink, NZePS) and Ketryx MCP authorisation before ACT-09 | Deferred owner | Before M5 |
| CND-04 | Produce the 10,000-patient synthetic practice before M5 | Deferred owner | Before M5 |
| CND-05 | Select the voice model and GPU node, set REQ-146, before M9 | Deferred owner | Before M9 |
| CND-06 | Appoint the New Zealand sponsor and lodge the WAND notification before the first cohort opens | Compliance | Before MOD-05 for the first site |
| CND-07 | Ratify loss matrices for the ten first-release claim types before the Tier 3 release build | Clinical governance | Before M9 exit |
| CND-08 | Track the Medical Products Bill at every milestone exit | Deferred owner | Each milestone |
| CND-09 | Name a clinical governance holder who accepts or rejects the five residual risks in 06-validation.md section 6 and ratifies fragments | Product owner | Before M4 |
| CND-10 | Name a compliance holder who confirms the standards list, appoints the sponsor and lodges the WAND notification | Product owner | Before M5 |
| CND-11 | Name an architecture holder who takes the deferred stack choices (TechSpec section 5) | Product owner | Before M1 exit |

## 7. Assumptions

| Assumption | Confidence | How it would be checked |
| --- | --- | --- |
| A sole product-owner approval is sufficient for the build baseline; role approvals are needed before the regulatory application | Medium | Reviewed when CND-09 to CND-11 are filled |

## 8. Open questions

- [x] Scope of approval confirmed
- [x] Sole approver: product owner, approve with conditions, 2026-09-25
- [x] Release decision: go
- [ ] Owners for CND-01, CND-03 to CND-05, CND-08: deferred 25 Sep 2026
