<revision_mode>
This is a headless revision, not an interview. There is no user to ask. The `<upstream_changes>` block shows the exact diff between the upstream documents as they were when this document was finalised and as they are now.

Do this and only this:

1. Read each diff. For every upstream item that was added, changed or withdrawn, find every place in `{{DOC_PATH}}` that derives from it (search for its identifier if the set uses them, and for the content).
2. Make the minimal edit that restores consistency: update derived text; add entries for new upstream items following this document's existing structure and, if identifiers are in use, the next free one; record entries whose upstream item was withdrawn as withdrawn with reason "upstream <item> withdrawn".
3. Where the change makes something undecidable without a human, do not guess: replace the affected content with `{{TBD: upstream <item> changed — <one-line question>}}` and add it to "Open questions".
4. Do not renumber. Do not restructure. Do not edit sections the diff does not touch. Do not edit the frontmatter.
5. Append one line to "Open questions": `- Revised by docpipe update on <today>: <n> edits, <m> TBDs raised.`

Edit `{{DOC_PATH}}` in place with the Edit tool. When done, print a three-line summary: items updated, items added, TBDs raised.
</revision_mode>
