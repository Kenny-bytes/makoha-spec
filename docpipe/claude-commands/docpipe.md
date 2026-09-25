---
description: Run a docpipe phase interview (1–7) in this session. Usage: /docpipe <n>
allowed-tools: Bash(python3 docpipe/docpipe.py *), Read, Edit, Glob, Grep
---

Phase status:
!`python3 docpipe/docpipe.py status`

Assembled phase prompt (upstream documents injected):
!`python3 docpipe/docpipe.py prompt $ARGUMENTS --stdout`

Begin phase $ARGUMENTS. Follow the instructions above exactly: mine upstream first, one question per turn, write every answer into the document before the next question.
