<phase_instructions phase="7" document="Completion and Approvals">

## What this document is for

The record that the set is complete, consistent, and approved for the stated intended purpose — with the exact versions approved pinned. It is the shortest document and the one with the least room for open markers.

## Read upstream this way

Run `python3 {{DOCPIPE}} status` and `python3 {{DOCPIPE}} build`. The status table is the completion evidence; the register in PSD.md (versions and hashes) is what gets pasted into this document at sign-off. Validation's change requests feed the completion checklist and any follow-up actions; validation's residual risks must be accepted by a named approver or become actions.

## Material an approval record commonly draws on

Scope of approval (what, for which release or milestone, for the intended purpose) · completion checklist answered from tool output (all phases final and none stale; zero open markers; every requirement covered by validation; all change requests closed; residual risks accepted) · document register at approval · approvals by role, name, decision (approve / approve with conditions / reject), conditions, date · release decision · conditions and follow-up actions with owner and due date.

## Question bank

1. What exactly is being approved, and for what use.
2. Who must approve, by role; any approval conditional on something outside this set.
3. For each checklist item that is not met: blocker, or condition to carry.
4. Go / no-go, and what the decision authorises next.

## Closure specifics

Finalise only when every checklist item is met or carried as a named condition, every approver has a decision and a date, and the release decision is a sentence. After finalising, run `docpipe build` once more so PSD.md carries the approval.

</phase_instructions>
