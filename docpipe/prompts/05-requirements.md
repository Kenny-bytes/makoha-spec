<phase_instructions phase="5" document="Specific Requirements">

## What this document is for

The deterministic, atomic, testable requirement set: what the build is measured against and what validation walks item by item. Each requirement is one sentence with one obligation, an upward trace to what it derives from, a verification method, and an acceptance criterion a tester applies without asking anyone. If the set's conventions fixed an identifier pattern and a requirement syntax, use them exactly; if not, establish the minimum this document needs (a way to refer to each requirement from phase 6) and record it with `docpipe set`.

## What downstream must be able to derive from it

- Phase 6 (Validation) needs one referenceable requirement per obligation, its verification method, and its acceptance criterion.
- Phase 7 (Approvals) needs the count and the withdrawn list.

## Derive before asking

This phase is mostly derivation. Before asking the user anything, draft the set mechanically:

1. Every OpsCon scenario step where the system acts → a requirement triggered by the prior step.
2. Every scenario variation or exception → an unwanted-behaviour requirement (condition → required response).
3. Every mode → requirements for behaviour that differs while in that mode.
4. Every engineering target → a non-functional requirement quoting the TechSpec number verbatim.
5. Every technical interface → an interface requirement.
6. Every PRD constraint, ConOps policy and OpsCon "must never" → a safety, security or regulatory requirement.
7. Optional or configuration-dependent capabilities → conditional requirements.

Present the drafted set in batches of ten or fewer, grouped by scenario, and ask the user to confirm, correct or cut each batch. Then ask only for what derivation could not reach.

## If the convention is EARS

Ubiquitous: "The <system> shall <response>". Event: "When <trigger>, the <system> shall …". State: "While <state>, the <system> shall …". Unwanted: "If <condition>, then the <system> shall …". Optional: "Where <feature>, the <system> shall …". Complex combines them. One "shall" per requirement; no "and/or", "etc.", "appropriate", "user-friendly", "fast", "as needed" — replace with the number, the enumeration, or a TBD. The system name is always "{{SYSTEM_NAME}}", never "it".

## Question bank (after derivation)

1. Steps that yielded no requirement: passive, or missed behaviour?
2. Every number: from the TechSpec, or new? New numbers need a source or a TBD.
3. Every unwanted-behaviour requirement: the response — reject, log, alert, degrade, halt?
4. Verification method per requirement: Test, Inspection, Analysis, Demonstration. Default Test; challenge anything else.
5. Acceptance criterion per requirement: the observable a tester checks. If it cannot be written, split the requirement.

## Closure specifics

Finalise only when `docpipe check 5` is clean, every batch has been confirmed, every TechSpec target is quoted by a requirement, and every OpsCon "must never" has one. Expect tens to low hundreds of requirements for a real product; fewer than fifteen usually means the OpsCon was thin — raise a change request rather than pad.

</phase_instructions>
