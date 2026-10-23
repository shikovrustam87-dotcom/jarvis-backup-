---
name: rigorous-development-workflow
description: Use when asked to build or fix. Test first.
---

# Rigorous Development Workflow

## Process

1. **Analyze** — Break down the task. Consider all sides and edge cases.
2. **Architect** — Design the solution before coding. Identify components, dependencies, risks.
3. **Delegate** — Assign to specialized agents (programmer, reviewer, security) via kanban.
4. **Monitor** — Track progress. Fix issues as they arise. Don't wait passively.
5. **Test** — Before declaring success, simulate at least 3 scenarios:
   - Happy path (normal usage)
   - Edge case (empty input, missing files, etc.)
   - Error case (what happens when something fails)
6. **Verify** — Run the actual code/command and confirm output matches expectations.
7. **Report** — Only say "done" after all scenarios pass. Show evidence (output, logs).

## Rules

- Never say "works" without running it.
- Never say "done" without testing.
- If a fix was applied, verify it actually fixed the issue.
- Show the user what was tested and the result.
- If something doesn't work, say so honestly and keep fixing.
- User communicates by voice (dictation) — commands are often garbled. Verify results by reading files, not trusting "done".
- User prefers step-by-step instructions without shell commands. Do mechanical steps yourself.
- User is frustrated by premature "it works" declarations. Always test first, report second.
