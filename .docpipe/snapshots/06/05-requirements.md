---
docpipe: 1
phase: 5
title: Specific Requirements
status: final
version: 1.0
upstream: ["01-prd.md", "03-opscon.md", "04-techspec.md"]
upstream_hash: {"01-prd.md": "945319a42d20e0ce", "03-opscon.md": "2566aaa0e9b9bf55", "04-techspec.md": "a3e788961563417d"}
finalised: 2026-09-25
---

# Specific Requirements

The deterministic, atomic, testable requirement set for the Mākoha platform, derived mechanically from the PRD (01-prd.md), the Operations Concept (03-opscon.md) and the Technical Specifications (04-techspec.md), all final v1.0, by the seven derivation rules of this phase. Convention: EARS, one obligation per sentence, system name "Mākoha platform". Identifier family minted here: REQ-nnn, minted once, never renumbered; a removed requirement is moved to section 15 with a reason. Columns: requirement; upward trace; verification method (Test, Inspection, Analysis, Demonstration); acceptance criterion a tester applies without asking anyone. Numbers are quoted from the TechSpec targets and are signed configuration defaults, not code literals.

## 1. Argument, gate and ledger invariants

Derived from PRD section 5 (the ten laws), OpsCon MN-01 to MN-05, MN-10 to MN-13, TechSpec COMP-11 to COMP-13.

| Id | Requirement | Trace | Verification | Acceptance criterion |
| --- | --- | --- | --- | --- |
| REQ-001 | The Mākoha platform shall store every clinical record entry in one append-only ledger from which the patient, clinician and governance faces read as authorised views. | Law 1; MN-11 | Test | An attempt to update or delete a ledger row is rejected by the database and no second copy of ledger data exists in any face store. |
| REQ-002 | The Mākoha platform shall deliver every recommendation, alert, coding proposal, reminder and pre-intake summary to a face only as an argument object with claim, grounds, warrant, backing, qualifier and rebuttals. | Law 2; MN-03 | Test | A face request for an item that is not an argument returns no content; every rendered item carries an argument id and an attempt id in its response headers. |
| REQ-003 | The Mākoha platform shall represent the six qualifier signals (posterior, coverage, membership, reliability, fit, ignorance) as separate fixed-point types with no conversion, averaging or comparison across kinds. | Law 3; MN-04 | Test | Code that adds, averages or compares two signal kinds fails to compile; the draft schema rejects JSON numbers with a fraction. |
| REQ-004 | The Mākoha platform shall assign one of the three verdicts released, flagged or held to every argument only through the evaluator's five fixed stages. | Law 4; MN-03 | Test | No code path outside the evaluator crate writes a verdict; an argument reaching a face without an attempt is absent from every face. |
| REQ-005 | When the evaluator evaluates a draft, the Mākoha platform shall record on the attempt the content hashes of all eight pin classes S, R, K, I, W, F, M, P and U. | Law 5; MN-05 | Test | An attempt insert with any pin absent is rejected by the NOT NULL and completeness check. |
| REQ-006 | When an attempt is replayed with the same pins, the Mākoha platform shall reproduce the same verdict and trace byte for byte. | Law 5; TGT-14 | Test | Replay of every attempt in a regulator bundle yields an identical attempt hash. |
| REQ-007 | The Mākoha platform shall admit guidelines, thresholds, codebooks, templates, ontology bindings and evidence into the runtime only as signed fragments that have passed the eleven compiler gates. | Law 6; MN-05 | Test | Only the compiler role holds INSERT on the pin registry and generic-argument tables; a fragment failing any gate is rejected with the gate's report and no override exists. |
| REQ-008 | The Mākoha platform shall run every engine as a pure function of typed signals and pinned knowledge with no input, output, clock or random access. | Law 7 | Test | The seccomp profile denies clock, random, socket and open calls; the two-process harness byte-compares outputs on at least 50 fixtures per claim type. |
| REQ-009 | When a released argument is rendered into the clinician, patient or regulator register, the Mākoha platform shall include every rebuttal and every qualifier signal of that argument in the same order. | Law 8; TGT-16 | Test | The render-invariance property test passes for every register template in force. |
| REQ-011 | The Mākoha platform shall show at most three flagged items with a fired rebuttal and at most five released plan-changing items on the disposition line per encounter, with deterministic hard stops never suppressed. | Law 9; Volume 9.6 | Test | A synthetic encounter with ten flagged items renders three inline and lists seven as suppressed with a suppression record. |
| REQ-012 | If an item is withheld from a brief or disposition line by the suppression policy, then the Mākoha platform shall write a suppression record naming the policy pin and the suppressed argument ids and keep the item reachable through "show all". | MN-10 | Test | Every brief with a footer count has a matching suppression record; "show all" returns the suppressed items. |
| REQ-013 | The Mākoha platform shall reject any test case, sealed envelope or feedback signal that reaches the compiler with evaluation-zone provenance. | Law 10; MN-12 | Test | Compiler gate 1 rejects a fragment carrying an evaluation-zone label. |
| REQ-014 | The Mākoha platform shall not learn online in production. | NG-02; MN-12 | Inspection | No code path updates engine weights at runtime; every weight file is a pinned artefact with a registered hash. |
| REQ-015 | The Mākoha platform shall not fuse probabilities from different engines into a single score. | NG-03; MN-04 | Inspection | No function accepts two engines' signals and returns one scalar. |
| REQ-016 | The Mākoha platform shall not rank patients or clinicians by a composite score. | NG-05; MN-13 | Inspection | Risk registers list each suspect with its own argument; no view sorts principals by a composite. |
| REQ-017 | The Mākoha platform shall not present a base model's judgement of its own output as a control. | NG-04; MN-03 | Test | Every class-3 output is queued and never assigned released or flagged by its own class-3 tester. |
| REQ-018 | When a clinician or patient reads an argument, the Mākoha platform shall apply the single view-authorisation function, returning not-found for a held argument to every face, forbidden for a flagged argument to the patient face, and the argument to the patient face only when a sign-off act exists. | MN-02; POL-03 | Test | The four cases return 404, 403, 200 and 200 in the documented combinations; row-level security returns the same outcome when the function is bypassed. |
| REQ-020 | When an argument's state changes, the Mākoha platform shall record the change as a new argument naming the superseded argument id, leaving the original row unchanged. | Volume 8.4; MN-11 | Test | After supersession both rows exist, the original hash is unchanged and the new row references it. |

## 2. Telehealth consultation (SCN-01)

| Id | Requirement | Trace | Verification | Acceptance criterion |
| --- | --- | --- | --- | --- |
| REQ-021 | When an appointment is booked, the Mākoha platform shall seed a pre-intake session with the patient's facts asserted Present within the pinned recency window and open it by the patient's chosen channel. | SCN-01.1 | Test | A booking event yields a pre-intake session whose context equals the Present facts within the window; channel matches the patient preference. |
| REQ-022 | While a pre-intake session is open, the Mākoha platform shall not ask a question whose answer a documented fact already provides. | SCN-01.3; MN-07 | Test | A patient with a documented smoking status is not asked about smoking. |
| REQ-023 | When the patient answers a pre-intake question, the Mākoha platform shall store the answer verbatim as a questionnaire response item with the dialogue span and the structured extraction. | SCN-01.3; DAT-06 | Test | The stored item contains the verbatim text, a span into the transcript and the extraction with its extractor pin. |
| REQ-024 | When the pre-intake dialogue reaches the medication reconciliation step, the Mākoha platform shall walk the current medication list line by line and record each conflict between the list and the patient's report as a disagreement row with source patient-reported. | SCN-01.3 | Test | A patient reporting a different dose yields a disagreement row before the session ends. |
| REQ-025 | If a pre-intake answer fires a red-flag rule, then the Mākoha platform shall emit a critical-lane event within 100 ms, send an escalation packet to the practice queue and tell the patient in plain words what happens next. | SCN-01.4; TGT-02 | Test | The event timestamp minus the answer commit is under 100 ms at p99; the packet exists in the queue; the patient message contains no clinical advice. |
| REQ-027 | When a pre-intake session completes, the Mākoha platform shall write the pre-intake summary as patient-reported facts plus a queued draft composition in which every sentence cites a fact. | SCN-01.5 | Test | Every sentence of the queued composition resolves to a fact id. |
| REQ-028 | The Mākoha platform shall not render a pre-intake summary or any class-3 draft to the patient face. | SCN-01.5; MN-03 | Test | A patient-face request for the summary returns 404. |
| REQ-029 | When a session join is imminent, the Mākoha platform shall assemble the consult-prep brief from released arguments and profile-permitted flagged arguments, ordered by priority, within the reading budget, in under 3 s at p95. | SCN-01.6; TGT-01 | Test | Brief assembly timing on the synthetic practice is under 3 s at p95; the brief contains no held argument. |
| REQ-030 | When a clinician accepts or rejects a pre-intake summary line, the Mākoha platform shall record the decision as a signed act naming the argument. | SCN-01.7 | Test | An act row with the clinician principal and the argument id exists for each decision. |
| REQ-031 | While a consultation session is in progress, the Mākoha platform shall produce session facts from ambient audio within 2 s of the utterance at p95, marked draft-session. | SCN-01.8; TGT-04 | Test | Transcript timestamp to fact commit is under 2 s at p95; each fact carries the draft-session marker. |
| REQ-032 | While a note is unsigned, the Mākoha platform shall exclude draft-session facts from the grounds of any evaluation request. | SCN-01.8; Volume 1A.3 | Test | An evaluation request built during an unsigned session contains no draft-session fact id. |
| REQ-033 | When a new session fact is committed, the Mākoha platform shall update the flagged "consider" differential with discriminators and an ordered next-best-question list within 500 ms at p95. | SCN-01.9; TGT-04 | Test | Attempt timing is under 500 ms at p95; the differential verdict is flagged and never released. |
| REQ-034 | When a medication is mentioned in a session or an order is drafted, the Mākoha platform shall run the prescribing check against the reconciled medication list, allergies, problems and latest observations under the clinician's scope fragment and return a verdict within 200 ms at p95. | SCN-01.11; TGT-05 | Test | Synchronous check timing under 200 ms at p95; the request grounds include the reconciled list. |
| REQ-035 | If a prescribing check rebuttal fires on a deterministic contraindication, then the Mākoha platform shall present a modal hard stop at the action it blocks. | SCN-01.11; Volume 9.6 | Test | A coded allergy to the ordered drug produces a modal at the order action that cannot be dismissed without an override act with reason. |
| REQ-036 | When a consultation session ends, the Mākoha platform shall draft the note, orders, letters and patient-register summary from signed facts within 10 s at p95, with every sentence citing a fact and every draft unsigned. | SCN-01.13; TGT-06 | Test | Draft commit within 10 s at p95; no draft carries a signature; every sentence resolves to a fact. |
| REQ-037 | If a class-3 draft sentence lacks a fact citation, then the Mākoha platform shall reject the draft through the fidelity tester and retry within the bounded loop. | SCN-01 exceptions; Volume 7.5 | Test | A draft with an uncited sentence is not queued; the loop log shows the retry. |
| REQ-039 | If three consecutive class-3 drafts fail the bounded-loop testers, then the Mākoha platform shall queue a no-draft note for the clinician in place of a draft. | Volume 7.5 | Test | After three logged failures the queue holds a no-draft note and no composition. |
| REQ-040 | When a clinician signs a note, the Mākoha platform shall supersede draft-session facts with signed-note facts and log the graph difference. | SCN-01.15 | Test | Session facts show superseded-by references; a diff record exists. |
| REQ-041 | When a signed plan contains a planned action, the Mākoha platform shall create exactly one task per planned fact with owner, due date and span link within 1 s of the sign act at p95. | SCN-01.15; TGT-09 | Test | Task count equals planned-fact count; each task links a span; timing under 1 s at p95. |
| REQ-042 | When a sign-off act exists for a patient-register summary, the Mākoha platform shall deliver the summary by a consented channel with the automated-message label. | SCN-01.15; MN-08 | Test | Delivery occurs only after the act; the communication carries the label and a reach-a-person route. |
| REQ-043 | When a patient-register summary is delivered, the Mākoha platform shall follow it with a comprehension check of two to four items and create a clinician task on a failed check. | SCN-01.16; Volume 2A.1 | Test | A failed check yields a task; a passed check yields none. |
| REQ-044 | If the patient declines pre-intake, then the Mākoha platform shall assemble the brief from the record alone. | SCN-01 variations | Test | A declined session still yields a brief before the join. |
| REQ-045 | If the patient's preferences record an interpreter language, then the Mākoha platform shall run the pre-intake dialogue in the matching locale pack. | SCN-01 variations | Test | The session's locale pin equals the pack for the recorded language. |

## 3. HITH supervision and deterioration (SCN-02, SCN-03)

| Id | Requirement | Trace | Verification | Acceptance criterion |
| --- | --- | --- | --- | --- |
| REQ-046 | When a device reading arrives, the Mākoha platform shall store it with the device identity, calibration status, sampling rate and declared accuracy. | SCN-02.2; TIF-10 | Test | The stored observation carries all four attributes and the device pin. |
| REQ-047 | If a device's calibration status is unknown, then the Mākoha platform shall apply the reliability floor to every observation promoted from that device. | SCN-02.2; RSK-04 | Test | A promoted observation from an uncalibrated device has reliability equal to the floor. |
| REQ-048 | When a device stream breaches a threshold for the configured window, the Mākoha platform shall promote a discrete observation by the pinned rule and emit a critical-lane event within 100 ms of promotion at p99. | SCN-02.2; TGT-07 | Test | Sustained SpO2 below threshold yields an observation and an event within 100 ms at p99. |
| REQ-049 | When any fact for a patient changes, the Mākoha platform shall re-score each enabled risk engine once per 30 s burst and complete within 10 s of the fact commit at p95. | SCN-02.3; TGT-07 | Test | A burst of five fact commits within 30 s yields one attempt per engine within 10 s of the last commit. |
| REQ-051 | When a risk engine drafts an argument, the Mākoha platform shall list as its evidence exactly the facts the engine consumed. | SCN-02.3; CAP-08 | Test | The evidence list equals the engine input fact set. |
| REQ-052 | The Mākoha platform shall cap the verdict of every class-2 engine output at flagged. | PRD section 8.2; Volume 5.4 | Test | No attempt with a class-2 decisive signal carries the verdict released. |
| REQ-053 | When a HITH visit is recorded, the Mākoha platform shall generate next-day visit tasks from the care plan and signed facts and queue a daily physician summary draft citing facts. | SCN-02.6 | Test | Tasks for the next day exist; the summary is queued, unsigned and fully cited. |
| REQ-054 | The Mākoha platform shall plot a HITH patient's risk trajectory from the attempts in the ledger so that replay reproduces the trajectory identically. | SCN-02.4; MET-05 | Test | Trajectory rendered from replayed attempts equals the live trajectory. |
| REQ-056 | If a device stream is interrupted, then the Mākoha platform shall render the interval as a gap with no imputed value. | SCN-02 variations | Test | The trajectory view shows a gap and the series contains no observation for the interval. |
| REQ-057 | When a deterioration rule fires, the Mākoha platform shall evaluate the deterioration argument as flagged with severity tier and rebuttals and emit a critical-lane event. | SCN-03.1 | Test | The attempt verdict is flagged; the argument carries a severity tier; an event exists. |
| REQ-058 | When a deterioration argument is flagged, the Mākoha platform shall assemble a signed escalation packet containing the current brief, session and device facts, every open attempt with its verdict, and the acts taken. | SCN-03.2; RSK-05 | Test | The packet manifest lists the four parts and a signature over their hashes. |
| REQ-059 | When an escalation packet is assembled, the Mākoha platform shall notify the profile's escalation target, create a same-day contact task, and message the patient citing only released content. | SCN-03.3 | Test | Notification, task and message exist; the patient message references only released argument ids. |
| REQ-060 | If a notification channel fails, then the Mākoha platform shall create a task and send by the next channel in the escalation target. | SCN-03 exceptions | Test | A forced SMS failure yields a task and an email attempt. |
| REQ-061 | When a HITH episode ends, the Mākoha platform shall build a handover document containing the episode summary and extracted actions in which every line cites a fact or a task. | SCN-03.6 | Test | Every line of the handover resolves to a fact id or task id. |
| REQ-062 | When a handover document is signed, the Mākoha platform shall send it to the receiving service by secure messaging and store the transport and application acknowledgements. | SCN-03.6; TIF-02 | Test | Both acknowledgement records exist for the sent document. |

## 4. Inbound documents and reconciliation (SCN-04, SCN-05)

| Id | Requirement | Trace | Verification | Acceptance criterion |
| --- | --- | --- | --- | --- |
| REQ-063 | When a secure message arrives, the Mākoha platform shall verify its signature, store the original content-addressed by hash, and pass it to the inbound pipeline. | SCN-04.1; TIF-02 | Test | The original is retrievable by hash and byte-identical after filing. |
| REQ-064 | If a secure message signature fails verification, then the Mākoha platform shall quarantine the message unfiled and raise a task. | SCN-05.1 | Test | A tampered message is absent from every patient record and a task names it. |
| REQ-065 | When an inbound document is received, the Mākoha platform shall match it to a patient and to any open order or referral, classify its type, extract facts with spans and reliability, and route it by urgency within 5 s at p95. | SCN-04.1; TGT-08 | Test | Intake to route timing under 5 s at p95 on the synthetic set; each extracted fact has a span. |
| REQ-066 | If a document's patient or order match weight is below the configured threshold, then the Mākoha platform shall place it in the reconciliation queue with the candidate matches and their weights. | SCN-05.1; MN-06 | Test | A low-weight document is in the queue with candidates and is absent from every record. |
| REQ-067 | The Mākoha platform shall not file an inbound item to a patient or order whose match weight is below the threshold. | MN-06 | Test | No filing act exists for any item below threshold. |
| REQ-068 | When a discharge summary is filed, the Mākoha platform shall compare its extracted medications with the reconciled list and patient-reported facts and write a disagreement row for each conflict before any clinician opens the document. | SCN-04.2 | Test | The disagreement row timestamp precedes the first clinician read audit event. |
| REQ-069 | When a discharge summary is filed, the Mākoha platform shall open the post-discharge engagement loop with its schedule materialised. | SCN-04.2; Volume 2A.1 | Test | A loop instance with daily check-ins for the window exists after filing. |
| REQ-070 | When a medication disagreement row is written, the Mākoha platform shall emit a critical-lane event and create a pharmacist call task due within 48 h. | SCN-04.4 | Test | The task owner role is pharmacist prescriber and the due date is filing time plus 48 h. |
| REQ-071 | When a pharmacist records the reconciled list as an act, the Mākoha platform shall use that list as grounds for the next prescribing check of the affected class. | SCN-04.6 | Test | The next check request's grounds contain the reconciled list version. |
| REQ-072 | When an inbound document contains a follow-up request, the Mākoha platform shall create a task proposal with the request's span and due date. | SCN-04.6; SCN-01.15 | Test | "Bloods in one week" yields a task proposal with a span and a due date seven days out. |
| REQ-073 | When a result message matches an order, the Mākoha platform shall move the order to resulted and update the cumulative view. | SCN-05.3; Volume 3.3 | Test | The order state machine shows the resulted transition with the result id. |
| REQ-074 | If a result matches an order already reconciled, then the Mākoha platform shall write a disagreement row instead of a second result. | SCN-05 exceptions | Test | A duplicate result yields one disagreement row and no new result resource. |
| REQ-075 | If an inbound item remains unfiled beyond the configured age, then the Mākoha platform shall escalate it to the clinician queue. | SCN-05.4 | Test | An item aged past the configured value appears in the clinician queue. |
| REQ-076 | The Mākoha platform shall hold no inbound item unrouted for more than 24 h. | TGT-08; MET-11 | Test | The nightly queue-age report shows zero items unrouted over 24 h. |

## 5. Scope of practice and escalation (SCN-06)

| Id | Requirement | Trace | Verification | Acceptance criterion |
| --- | --- | --- | --- | --- |
| REQ-077 | When a prescriber drafts an order, the Mākoha platform shall evaluate it under the prescriber's signed scope fragment. | SCN-06.2; POL-04 | Test | The attempt pins include the profile pin of the prescriber. |
| REQ-078 | If an ordered medication is outside the prescriber's formulary, then the Mākoha platform shall hold the order. | SCN-06.2; Volume 1A.4 | Test | The attempt verdict is held and the order cannot be signed. |
| REQ-079 | If an out-of-scope predicate fires, then the Mākoha platform shall create an escalation packet containing the argument ids and the open attempt and route it to the escalation target named in the profile. | SCN-06.2 | Test | The packet exists in the target's queue with the ids. |
| REQ-080 | When the escalation target acts on a packet, the Mākoha platform shall continue the protocol step machine from that act on the same graph. | SCN-06.4 | Test | The protocol state advances after the GP act with no re-entry of data. |
| REQ-081 | If the escalation target does not act within the configured interval, then the Mākoha platform shall route the packet to the next target in the chain. | SCN-06 exceptions | Test | After the interval the packet appears in the second target's queue. |
| REQ-082 | The Mākoha platform shall count every escalation and whether its packet carried the full context, for the advanced-practice scope measure. | SCN-06.5; MET-07 | Test | The MeasureReport numerator and denominator equal the packet counts in the ledger. |

## 6. Prospective studies and research (SCN-07)

| Id | Requirement | Trace | Verification | Acceptance criterion |
| --- | --- | --- | --- | --- |
| REQ-083 | When a study owner registers a study, the Mākoha platform shall append a sealed envelope holding the public hash of the question, cohort query, outcome query and analysis plan with the window and registration time. | SCN-07.2; POL-08 | Test | The envelope row exists with the hash and sealed content; the content is unreadable before the window end. |
| REQ-084 | If a study names a Measure without a validation record, then the Mākoha platform shall refuse the registration. | SCN-07.2 | Test | Registration with an unvalidated Measure returns a refusal naming the Measure. |
| REQ-085 | When a phenotype match event occurs for a registered study, the Mākoha platform shall enrol the patient on first match with time and pins only when the consent scope for secondary use is present. | SCN-07.3; MN-09 | Test | A matching patient without the scope is not enrolled; with it, an enrolment resource exists. |
| REQ-086 | The Mākoha platform shall not contact a patient for eligibility without the contact-for-eligibility consent scope. | MN-09; POL-05 | Test | An eligibility message is refused for a patient lacking the scope. |
| REQ-087 | While a study window is open, the Mākoha platform shall permit interim endpoint reads that cannot alter the sealed plan. | SCN-07.5 | Test | An interim read returns values and the envelope hash is unchanged afterwards. |
| REQ-088 | If a pin that a study depends on changes, then the Mākoha platform shall create a revalidation task for the study. | SCN-07.5 | Test | A dependency pin change yields a task naming the study. |
| REQ-089 | When a study window ends, the Mākoha platform shall verify the envelope hash, run the cohort and outcome queries with the pins as of the window start, run the analysis plan, and produce a report bearing the envelope hash. | SCN-07.6 | Test | The report cover hash equals the envelope hash; the queries used the window-start pins. |
| REQ-090 | If a study plan is changed after registration, then the Mākoha platform shall register a new envelope and report the original as abandoned. | SCN-07 exceptions | Test | Two envelopes exist; the first carries the abandoned status. |
| REQ-091 | If a patient withdraws the secondary-use consent scope, then the Mākoha platform shall exclude the patient from the next de-identified extract. | SCN-07 exceptions; POL-05 | Test | The next extract manifest lacks the withdrawn patient. |
| REQ-092 | If a release-capable fragment lacks an evaluation-register entry, then the Mākoha platform shall refuse its admission at the compiler. | SCN-07 preconditions; Volume 2A.3 | Test | Compiler gate 11 rejects the fragment naming the missing entry. |

## 7. Onboarding, drift and outage (SCN-08, SCN-09, SCN-10)

| Id | Requirement | Trace | Verification | Acceptance criterion |
| --- | --- | --- | --- | --- |
| REQ-093 | When incumbent data is migrated, the Mākoha platform shall attach lineage to every migrated resource and mark unstructured content as an original for extraction. | SCN-08.4 | Test | Every migrated resource carries a source and a migration batch id. |
| REQ-095 | If migrated data conflicts with an existing fact, then the Mākoha platform shall record the conflict as a disagreement row leaving the existing fact unchanged. | SCN-08 exceptions | Test | The existing fact hash is unchanged and a disagreement row references both sources. |
| REQ-096 | While a cohort is in onboarding mode, the Mākoha platform shall capture cut-over baselines for MET-01 to MET-11 as MeasureReports before any engine drafts an argument for that cohort. | SCN-08.5; MOD-05 | Test | Baseline reports are timestamped before the first attempt for any cohort patient. |
| REQ-097 | When a class-2 engine's rolling conformal coverage or calibration breaches its bound for the configured window in any subgroup, the Mākoha platform shall mark the engine pin retired, write a sentinel entry and fall its claim types back to class-1 rules. | SCN-09.1; MOD-02 | Test | After a forced breach the pin shows retired, a sentinel entry exists and the next attempt for the claim type has a class-1 decisive signal. |
| REQ-098 | While an engine pin is retired, the Mākoha platform shall display the retirement on the governance face and on every affected disposition line. | MOD-02 | Test | The disposition line for an affected claim type carries the retirement marker. |
| REQ-099 | When a replacement engine pin is submitted, the Mākoha platform shall replay the sentinel decision set against it before it may draft. | SCN-09.4 | Test | The pin's admission record references a completed sentinel replay. |
| REQ-100 | While an edge node is offline, the Mākoha platform shall continue notes, prescribing checks with local pins, local extraction and paper script printing for at least 8 h. | SCN-10.1; TGT-12; MOD-03 | Demonstration | An 8 h outage drill completes with all four functions exercised. |
| REQ-101 | While an edge node is offline, the Mākoha platform shall queue e-prescriptions and register uploads and mark class-2 and class-3 outputs unavailable rather than substituting values. | SCN-10.1 | Test | The queue holds the transactions; affected outputs show unavailable. |
| REQ-102 | When an edge node reconnects, the Mākoha platform shall sync resource versions additively by hash, record conflicting fields as disagreement rows, and flush queued national transactions in commit order. | SCN-10.3; TIF-18 | Test | After reconnect both versions of a concurrently edited patient exist, a disagreement row exists, and transaction transmit order equals commit order. |
| REQ-103 | When a print job is rendered, the Mākoha platform shall render from a pinned template, store the PDF as a document reference with the template pin, and write an audit event. | Volume 3A.12 | Test | Reprint from the stored reference is byte-identical; an audit event names the job. |
| REQ-104 | The Mākoha platform shall ship the event log and object store continuously to a second region with per-tenant keys. | TechSpec section 8 | Inspection | Replication lag and key scoping are shown in the operations dashboard. |
| REQ-105 | When an operator restores to a commit or timestamp, the Mākoha platform shall rebuild the relational, columnar and time-series stores by replay and verify the ledger chain end to end before serving writes. | MOD-04; TechSpec section 8 | Test | Restore to a timestamp reproduces the ledger hashes up to that point and writes resume only after verification. |
| REQ-106 | The Mākoha platform shall run an automated restore drill weekly on a scratch node with hash comparison and produce a report. | TechSpec section 8 | Inspection | A weekly drill report exists for every week of operation. |
| REQ-107 | If a node's start-up attestation does not match its signed manifest, then the Mākoha platform shall refuse to serve. | TechSpec section 8 | Test | A node with an altered binary exits without opening its listener. |
| REQ-108 | If the per-patient hash chain or the Merkle anchor detects a mismatch, then the Mākoha platform shall write a sentinel entry naming the affected range. | TechSpec section 6 | Test | A mutated ledger row is detected by the chain check and a sentinel entry names its position. |

## 8. Modes of operation

| Id | Requirement | Trace | Verification | Acceptance criterion |
| --- | --- | --- | --- | --- |
| REQ-109 | While in normal mode, the Mākoha platform shall enforce the class ceilings released for class 1, flagged for class 2 and queue only for class 3 on every attempt. | MOD-01; PRD section 8.2 | Test | No attempt carries a verdict above its decisive signal's ceiling. |
| REQ-110 | When a signed build starts, the Mākoha platform shall attest its manifest and enter normal mode only when every pin class the manifest lists is present in the registry. | MOD-01 | Test | A node missing a listed pin class does not enter normal mode. |
| REQ-111 | While in maintenance and restore mode, the Mākoha platform shall serve faces read-only and create no new attempts. | MOD-04 | Test | A write during restore returns a read-only error; the attempt count is unchanged. |
| REQ-112 | When a governance act opens normal mode for an onboarded cohort, the Mākoha platform shall begin drafting arguments for that cohort's patients. | MOD-05 | Test | No attempt for a cohort patient predates the opening act. |
| REQ-113 | The Mākoha platform shall give the evaluation zone read access to the ledger and no write path to the pin registry, compiler input or any training set. | TechSpec COMP-20 | Test | The evaluation-zone database role holds SELECT only; a write attempt is denied. |
| REQ-114 | The Mākoha platform shall provide no training mode. | MOD-05 note; NG-02 | Inspection | No mode, flag or endpoint enables weight updates. |

## 9. Technical interfaces

| Id | Requirement | Trace | Verification | Acceptance criterion |
| --- | --- | --- | --- | --- |
| REQ-115 | When a patient is registered, the Mākoha platform shall resolve the NHI through the Hira API and accept both the AAA111# and the AAA11A# formats. | TIF-01 | Test | Both formats validate; the lookup returns the national demographics. |
| REQ-116 | When a practitioner account is created, the Mākoha platform shall bind the HPI practitioner identifier, registration and scope profile into the professional token. | TIF-01; TIF-11 | Test | The token claims contain HPI, registration and profile pin. |
| REQ-118 | When a clinical document is sent by secure messaging, the Mākoha platform shall sign it with the provider certificate from the hardware-backed store and encrypt it to the recipient certificate from the directory. | TIF-02 | Test | The sent payload verifies against the provider certificate and decrypts only with the recipient key. |
| REQ-119 | When a secure message acknowledgement arrives, the Mākoha platform shall store it against the message and retry with backoff until application acknowledgement or the configured limit. | TIF-02 | Test | Timeout yields retries then a task at the limit. |
| REQ-121 | When a shared health summary is uploaded, the Mākoha platform shall generate it from the reconciled record as an NZIPS document from a pinned template. | TIF-03 | Test | The uploaded content equals the reconciled list at upload time and names the template pin. |
| REQ-122 | If a patient's national-record consent is absent or withdrawn, then the Mākoha platform shall refuse the upload. | TIF-03; POL-05 | Test | Upload without the flag returns a refusal and no upload record. |
| REQ-123 | When a national-record document is downloaded, the Mākoha platform shall pass it through the inbound pipeline with source national record and log the view with its purpose on the patient's access report. | TIF-03 | Test | The extracted facts carry the source; the access report lists the view with purpose. |
| REQ-124 | When a prescription is signed, the Mākoha platform shall transmit it through the New Zealand ePrescription Service in conformance with its specification and record the dispense records it returns. | TIF-04 | Test | Conformance suite passes; dispense records attach to the order. |
| REQ-125 | When an HL7 v2 result message arrives, the Mākoha platform shall parse it by the sender's profile and match it to the order by identifier before the probabilistic matcher. | TIF-05 | Test | A result with a matching order identifier is matched without invoking the matcher. |
| REQ-126 | When a terminology edition is imported, the Mākoha platform shall register the edition date as pin class S and rebuild the terminology graph read-only. | TIF-07 | Test | The registry holds the edition pin; lookups return the edition's concepts. |
| REQ-127 | When an SMS or email is sent, the Mākoha platform shall check per-channel consent and quiet hours and honour opt-out keywords automatically. | TIF-08; MN-08 | Test | A send to an opted-out channel is refused with a logged reason. |
| REQ-128 | The Mākoha platform shall not send an urgent result notification by an SMS template. | TIF-08; Volume 3A.11 | Test | The urgent result class has no SMS template and a send attempt is refused. |
| REQ-129 | When a telehealth session is created, the Mākoha platform shall issue a short-lived join token bound to the encounter and the principal. | TIF-09 | Test | A join with an expired token is refused. |
| REQ-130 | The Mākoha platform shall record a telehealth session only when a consent resource for recording exists. | TIF-09; POL-05 | Test | Recording without the resource is refused. |
| REQ-131 | When a face calls the gateway, the Mākoha platform shall require mutual TLS and an OAuth2 bearer token and apply attribute-based authorisation per request. | TIF-13; CST-07 | Test | A call without a client certificate or token is refused; a tenant A token reading tenant B returns 404. |
| REQ-132 | When a sidecar returns a draft, the Mākoha platform shall validate it against the ArgumentDraft JSON Schema at the process boundary and treat an invalid draft as an engine fault. | TIF-17 | Test | An invalid draft produces an engine fault record and no held argument. |
| REQ-133 | When the ledger root is published, the Mākoha platform shall write it to the independent append-only log and store the receipt. | TIF-14; D-08 | Test | A receipt exists for every published root. |
| REQ-134 | When a requirement, risk or verification result changes, the Mākoha platform shall export it to Ketryx through the Ketryx API or MCP server with lineage to its identifier in this set. | TIF-16 | Demonstration | A changed requirement appears in Ketryx with its REQ identifier within the export cycle. |

## 10. Performance and capacity

| Id | Requirement | Trace | Verification | Acceptance criterion |
| --- | --- | --- | --- | --- |
| REQ-135 | The Mākoha platform shall commit a resource write in under 10 ms at p99 on the 10,000-patient synthetic practice. | TGT-11 | Test | Performance suite result at p99 under 10 ms. |
| REQ-136 | The Mākoha platform shall return a search in under 50 ms on the synthetic practice. | TGT-11 | Test | Performance suite result under 50 ms. |
| REQ-137 | The Mākoha platform shall return a terminology lookup in under 1 ms. | TGT-11 | Test | Performance suite result under 1 ms. |
| REQ-138 | The Mākoha platform shall deliver a committed event to subscribers in under 100 ms at p99. | TGT-11 | Test | Commit-to-subscriber timing at p99 under 100 ms. |
| REQ-139 | The Mākoha platform shall sustain over 25,000 writes per second for 60 s with 10 writer threads on the synthetic practice. | TGT-11 | Test | Performance suite throughput result over 25,000 writes per second. |
| REQ-140 | The Mākoha platform shall complete the nightly register and recall run in under 30 min for 10,000 patients. | TGT-10 | Test | Job duration under 30 min. |
| REQ-141 | The Mākoha platform shall answer a cohort query over one year in under 2 s. | TGT-10 | Test | Query timing under 2 s. |
| REQ-142 | The Mākoha platform shall replay 1% of the attempts in every regulator bundle with identical results. | TGT-14 | Test | The bundle replay report shows zero mismatches. |
| REQ-143 | When an engine is registered, the Mākoha platform shall pass the two-process purity harness on at least 50 fixtures per claim type and 1,000 corruption-engine inputs with byte-identical outputs. | TGT-15 | Test | The registration record cites a passed harness run with the fixture counts. |
| REQ-144 | The Mākoha platform shall run the performance suite, purity harness, render-invariance property and compiler gate fixtures on every build. | TechSpec section 8 | Inspection | The CI log for every build shows the four suites. |
| REQ-145 | The Mākoha platform shall meet availability, recovery point and recovery time values of {{TBD: deferred with PERF-12 and TGT-13}}. | TGT-13 | Analysis | Deferred. |
| REQ-146 | When a voice turn ends, the Mākoha platform shall begin the spoken response within {{TBD: turn latency, set at M9}} at p95. | TGT-03 | Test | Sidecar timing log on the scripted dialogue set. |
| REQ-147 | The Mākoha platform shall reproduce a MeasureReport with an identical hash when computed again for the same period and pins. | Volume 1A.6 | Test | Two computations of one report yield one hash. |
| REQ-148 | The Mākoha platform shall rebuild the columnar layer from event replay to an identical NDJSON export hash. | Volume 3A.1 | Test | Drop and replay yields the same export hash. |
| REQ-149 | The Mākoha platform shall render a brief within a reading budget of 90 s at 200 words per minute by default. | Volume 9.5 | Test | Brief word count does not exceed 300 words at the default budget. |
| REQ-150 | The Mākoha platform shall reach a brief-before-session rate of at least 99% over a quarter. | MET-08 | Analysis | Quarterly MeasureReport at or above 99%. |
| REQ-151 | The Mākoha platform shall deliver a signed patient-register summary within 24 h of sign-off for at least 95% of summaries. | MET-09 | Analysis | Monthly MeasureReport at or above 95%. |
| REQ-152 | The Mākoha platform shall report the coverage gap per fact type on the governance face monthly. | MET-01 | Test | A monthly coverage-gap MeasureReport exists per fact type. |

## 11. Security and privacy

| Id | Requirement | Trace | Verification | Acceptance criterion |
| --- | --- | --- | --- | --- |
| REQ-153 | The Mākoha platform shall require a second factor by time-based one-time password for every clinician and governance face login. | TechSpec section 6 | Test | Login without the second factor is refused. |
| REQ-154 | The Mākoha platform shall hash passwords with argon2id. | TechSpec section 6 | Inspection | The credential store holds argon2id hashes only. |
| REQ-155 | When any request is served, the Mākoha platform shall write one audit event with actor, purpose and patient, including model inferences. | TechSpec section 6; MN-11 | Test | Every request in a test run has exactly one audit event; an inference request names the model pin. |
| REQ-156 | When a patient requests their access report, the Mākoha platform shall list every read of their record with who, when and purpose in plain language, including agents and models. | Volume 2A.1 | Test | A model inference appears on the report with its purpose. |
| REQ-157 | When a break-glass access is requested, the Mākoha platform shall require a reason, write an act, set the session variable for one transaction and write a sentinel entry. | POL-06; CST-07 | Test | Break-glass without a reason is refused; with one, all three records exist and the access expires after one transaction. |
| REQ-158 | The Mākoha platform shall evaluate consent scopes per request for secondary use, research export, agent contact and each communication channel. | POL-05 | Test | A request lacking the scope is refused for each of the four uses. |
| REQ-159 | When a consent scope is withdrawn, the Mākoha platform shall deliver the withdrawal event to subscribers within 100 ms and refuse the next secondary-use read. | POL-05; TechSpec section 6 | Test | Event delivery under 100 ms; the next read returns a refusal. |
| REQ-160 | The Mākoha platform shall scope every resource to a tenant and return not-found for a request from another tenant. | TechSpec section 4 | Test | A cross-tenant read returns 404. |
| REQ-161 | The Mākoha platform shall run every sidecar in a separate process under a seccomp profile with no network namespace and stdin and stdout as its only channels. | CST-05; TECH-08 | Test | A sidecar attempting a socket call is killed and the kill is logged. |
| REQ-162 | The Mākoha platform shall depend on no secret for any clinical behaviour, holding secrets only for transport and signing keys in a hardware-backed store. | CST-08 | Inspection | Secret inventory lists transport and signing keys only. |
| REQ-163 | When a build is produced, the Mākoha platform shall emit a signed manifest with build hash, profile, features, crate hashes, sidecar image digests, SBOM, seccomp profiles and pin classes present. | CST-02 | Inspection | The manifest contains the eight fields and verifies against the build. |
| REQ-164 | The Mākoha platform shall encrypt data at rest at the store level and maintain a per-patient hash chain and Merkle anchor independent of that encryption. | CST-06 | Test | Encryption is enabled; the chain verifies after a restore. |
| REQ-166 | When a de-identified export is produced, the Mākoha platform shall use an export type whose schema has no identifier field. | CAP-14 | Test | The export type fails to compile with an identifier field. |
| REQ-167 | The Mākoha platform shall keep the residual identifier rate of de-identified text on the adjudicated set below the declared value in the de-identifier's pin. | CAP-14 | Test | The adjudicated-set run reports a rate below the declared value. |
| REQ-168 | The Mākoha platform shall grant the pre-intake and voice agent a scope token that can write only QuestionnaireResponse and patient-reported Observation for the patient in session. | ROL-12; MN-07 | Test | An agent write of any other resource type, or for another patient, is refused. |
| REQ-169 | When an identity administrator creates, suspends or revokes an account, the Mākoha platform shall record the change as an audited act. | ROL-15 | Test | Each account change has an act row with the administrator principal. |
| REQ-170 | The Mākoha platform shall bind every custom operation script to a sandbox with no file, network or clock access beyond typed bindings. | Volume 3A.1 | Test | A script calling the network fails closed. |

## 12. Regulatory, knowledge and data

| Id | Requirement | Trace | Verification | Acceptance criterion |
| --- | --- | --- | --- | --- |
| REQ-171 | The Mākoha platform shall produce a regulator bundle for a time window containing the arguments, attempts, acts and conflicts, every referenced pin with bytes or a signed locator, a replay report, the corruption campaign report, coverage declarations, an obligations extract and a manifest with a sha256 per file signed by the governance key. | TIF-12; STD-01 | Test | The published offline verifier validates the manifest and re-runs replay on a sample bundle. |
| REQ-172 | The Mākoha platform shall keep an obligations register with the New Zealand sponsor, WAND notification, safety evidence and post-market records and, when in force, the TGA and FDA classification records. | STD-01; STD-03; CST-03 | Inspection | The register lists the obligations with evidence links. |
| REQ-173 | Where a template is provisional, the Mākoha platform shall cap arguments drafted from it at flagged. | CST-09; D-02 | Test | An attempt on a provisional template never carries released. |
| REQ-174 | The Mākoha platform shall include a loss matrix in a Tier 3 release build only when it carries a ratification signature from the clinical governance role. | CST-10; D-05 | Test | A build containing an unratified matrix for a shipped claim type fails the manifest check. |
| REQ-175 | When a fragment is submitted, the Mākoha platform shall require the signatures of the compiler key and the ratifying role and derive its identifier from its content hash. | Volume 6.3 gate 11 | Test | An unsigned fragment is rejected; the identifier equals the sha256 of the content. |
| REQ-176 | When a pin changes, the Mākoha platform shall replay the sentinel decision set against the new pin before admitting it. | TechSpec section 8 | Test | Admission records cite a completed sentinel replay. |
| REQ-178 | The Mākoha platform shall retain every ledger row, resource version and original indefinitely, archived by window with a Merkle anchor, exceeding the ten-year statutory minimum. | OpsCon section 6; STD-05 | Inspection | No deletion path exists; archive windows carry anchors. |
| REQ-179 | The Mākoha platform shall pin the SNOMED CT New Zealand edition by edition date and record its licence in the obligations register. | CST-04; STD-09 | Inspection | The registry holds the edition pin; the register holds the licence. |
| REQ-180 | The Mākoha platform shall store every behaviour-governing number as a signed, versioned configuration value and not as a code literal. | PRD section 5 conventions | Inspection | Threshold sets, budgets and coverage levels resolve to pinned fragments; no literal appears in the evaluator source. |

## 13. Voice interaction (CAP-20)

| Id | Requirement | Trace | Verification | Acceptance criterion |
| --- | --- | --- | --- | --- |
| REQ-181 | Where the patient selects the voice channel, the Mākoha platform shall conduct pre-intake, check-ins and messaging as a full-duplex spoken dialogue in which the patient may interrupt. | CAP-20; SCN-01.2 | Demonstration | A scripted interruption is handled without loss of the prior answer. |
| REQ-182 | The Mākoha platform shall run the voice model as a self-hosted sidecar whose weights are content-hash pinned as class W. | CST-13; DEC-02 | Inspection | The sidecar image contains the weights; the registry holds their hash; no outbound network path exists. |
| REQ-183 | When a spoken answer is captured, the Mākoha platform shall store the transcript with spans and treat it exactly as a typed answer under REQ-023. | CAP-20; RSK-09 | Test | The questionnaire response item carries a transcript span. |
| REQ-184 | If the voice sidecar is unavailable, then the Mākoha platform shall offer the typed channel and record the fallback. | SCN-01 exceptions | Test | With the sidecar stopped, the session continues typed and a fallback record exists. |
| REQ-185 | The Mākoha platform shall not record voice audio without a consent resource for recording. | POL-05; TIF-09 | Test | Recording without the resource is refused. |
| REQ-186 | The Mākoha platform shall pass every voice-generated text through the bounded loop's class-2 testers before it reaches a person. | Law 4; RSK-11 | Test | A voice utterance to the patient with a claim outside released facts is refused with a hand-off. |

## 14. Coverage of upstream

Every TechSpec target TGT-01 to TGT-16 is quoted: TGT-01 REQ-029; TGT-02 REQ-025; TGT-03 REQ-146; TGT-04 REQ-031, REQ-033; TGT-05 REQ-034; TGT-06 REQ-036; TGT-07 REQ-048, REQ-049; TGT-08 REQ-065, REQ-076; TGT-09 REQ-041; TGT-10 REQ-140, REQ-141; TGT-11 REQ-135 to REQ-139; TGT-12 REQ-100; TGT-13 REQ-145; TGT-14 REQ-006, REQ-142; TGT-15 REQ-143; TGT-16 REQ-009. Every OpsCon must-never MN-01 to MN-13 has a requirement: MN-01 REQ-187; MN-02 REQ-018; MN-03 REQ-017, REQ-028; MN-04 REQ-003, REQ-015; MN-05 REQ-005, REQ-007; MN-06 REQ-067; MN-07 REQ-022, REQ-168; MN-08 REQ-042, REQ-127; MN-09 REQ-086; MN-10 REQ-012; MN-11 REQ-001; MN-12 REQ-013, REQ-014; MN-13 REQ-016.

| Id | Requirement | Trace | Verification | Acceptance criterion |
| --- | --- | --- | --- | --- |
| REQ-187 | The Mākoha platform shall not transmit, dispense or act on an order, prescription or plan without a signing clinician's act. | MN-01; NG-01; POL-01 | Test | An order without a sign act cannot reach the transmitted state. |

## 15. Withdrawn

Withdrawn identifiers are kept here with their original text and reason and are never reused. Each was split because it carried more than one obligation.

| Id | Original text | Trace | Verification | Reason |
| --- | --- | --- | --- | --- |
| REQ-010 | The Mākoha platform shall limit interruptive items per encounter to the counts of the attention budget in force and shall not exceed them. | Law 9; MN-10 | Test | Withdrawn: replaced by REQ-011 and REQ-012 because it carried two obligations. |
| REQ-019 | When an argument is superseded, the Mākoha platform shall create a new argument that names the superseded one and shall leave the original unchanged. | Volume 8.4 | Test | Withdrawn: two obligations; replaced by REQ-020. |
| REQ-026 | When a pre-intake session completes, the Mākoha platform shall write the pre-intake summary as patient-reported facts plus a queued draft composition citing a fact per sentence, and shall not show the summary to the patient. | SCN-01.5 | Test | Withdrawn: two obligations; replaced by REQ-027 and REQ-028. |
| REQ-038 | If three consecutive class-3 drafts fail the bounded-loop testers, then the Mākoha platform shall produce no draft and shall place a note in the clinician queue. | Volume 7.5; TechSpec section 8 | Test | Withdrawn: two obligations; replaced by REQ-039. |
| REQ-050 | When a risk engine drafts an argument, the Mākoha platform shall list as its evidence exactly the facts the engine consumed and shall cap its verdict at flagged. | SCN-02.3 | Test | Withdrawn: two obligations; replaced by REQ-051 and REQ-052. |
| REQ-055 | If a device stream is interrupted, then the Mākoha platform shall display the gap and shall not impute values. | SCN-02 variations | Test | Withdrawn: two obligations; replaced by REQ-056. |
| REQ-094 | If migrated data conflicts with existing facts, then the Mākoha platform shall write disagreement rows and shall not overwrite. | SCN-08 exceptions | Test | Withdrawn: two obligations; replaced by REQ-095. |
| REQ-117 | When a clinical document is sent by secure messaging, the Mākoha platform shall sign it with the provider certificate held in the hardware-backed store, encrypt it to the recipient's certificate from the directory, and store transport and application acknowledgements. | TIF-02 | Test | Withdrawn: three obligations; replaced by REQ-118 and REQ-119. |
| REQ-120 | When a patient's shared health summary is uploaded to Hira, the Mākoha platform shall generate it from the reconciled record as an NZIPS document from a pinned template and shall refuse the upload without the patient's consent flag. | TIF-03 | Test | Withdrawn: two obligations; replaced by REQ-121 and REQ-122. |
| REQ-165 | When a de-identified export is produced, the Mākoha platform shall use an export type that cannot hold identifier fields and shall keep the residual identifier rate on the adjudicated set below the declared value. | CAP-14 | Test | Withdrawn: two obligations; replaced by REQ-166 and REQ-167. |
| REQ-177 | The Mākoha platform shall retain every ledger row, resource version and original for at least ten years from the patient's last treatment and shall not delete them. | OpsCon section 6; STD-05 | Test | Withdrawn: two obligations; replaced by REQ-178. |

## 16. Change requests to upstream

None.

## 17. Assumptions

| Assumption | Confidence | How it would be checked |
| --- | --- | --- |
| The configured values named "configured threshold", "configured window" and "configured interval" are each a pinned fragment by go-live | High | Compiler registry lists them |
| The synthetic practice of 10,000 patients is available before M5 for every performance requirement | Medium | PRD open item |

## 18. Open questions

- [ ] Availability, RPO and RTO values (REQ-145, deferred with PERF-12)
- [ ] Voice turn latency (REQ-146, set at M9)
- [x] All thirteen sections confirmed 25 Sep 2026; verification methods accepted
