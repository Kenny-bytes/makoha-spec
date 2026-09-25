<phase_instructions phase="6" document="Validation Activities">

## What this document is for

The plan and record of validating every requirement: the activity, the method, where the evidence lives, whether it is complete (yes/no), and whether validation showed something upstream must change (yes/no → a change request naming the target document and item). This is the loop-back that makes the pipeline re-iterative; it is finalised per validation cycle, not once.

First cycle: plan — every requirement gets an activity, complete = no. Later cycles: record outcomes and raise change requests as evidence arrives.

## What downstream must be able to derive from it

- Phase 7 (Approvals) needs the completion counts, the open change requests, and the residual risks.
- `docpipe update` needs each change request to name one target document and one target item.

## Read upstream this way

Every requirement → one validation entry minimum, inheriting its verification method and acceptance criterion. Draft the whole register mechanically first; do not ask the user to enumerate it. Group activities: many Test-method requirements share one suite or one demonstration session; one activity may cover several entries, but each entry references exactly one requirement. TechSpec targets give the pass threshold.

## Material a validation record commonly draws on

Validation register (entry, requirement reference, activity, method, evidence location, complete y/n, modification required y/n, change request) · change requests (raised by, target document and item, change, status open/applied/rejected) · summary counts · residual risks and known limitations · assumptions · open questions.

## Question bank

1. Planning cycle: for the grouped activities, where will evidence live.
2. Which activities need a person or environment not yet available — name the blocker.
3. Recording cycle: for each activity with evidence, pass or fail. Fail → fault in the build (complete = no, retest) or in the requirement or design (modification = yes, raise a change request).
4. For each change request: which document and item, changed to what, and does it cascade.
5. What is validated only by analysis or inspection rather than test, and is that acceptable for the intended purpose.

## Change-request discipline

One target document and one target item per change request; a change touching three items is three requests. Status is open until the upstream document is edited and re-finalised; the approver of that document sets applied or rejected here. After changes are applied upstream, `docpipe update` marks downstream documents stale and, with `--apply`, revises them for review.

## Closure specifics

Finalise a cycle when `docpipe check 6` is clean (every requirement covered, when an identifier convention is set), every modification = yes carries a change request, every complete = yes has an evidence location, and the summary counts are counted, not estimated. Re-open by editing and re-running `docpipe finalise 6` after the next cycle.

</phase_instructions>
