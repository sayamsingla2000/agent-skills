# Working agreement

I am the reviewer of everything you write. Optimise for a diff I can verify quickly,
not for finishing fast.

## Before writing code

- Restate the task as a spec: files, real signatures, data shapes, edge cases, what is out of scope.
- If a decision changes behaviour I care about and the task does not settle it, ask once, then proceed.
- No code until the spec is acknowledged. `/plan` exists for this.

## While writing code

- Smallest working increment at a time. One behaviour per change.
- Tests land with the code that makes them pass, never in a batch at the end.
- Run the tests. Never report a result you did not observe — quote the actual output.
- Do not add dependencies, config files, scripts, or abstractions I did not ask for.
- Do not touch files outside the stated scope. If a fix requires it, say so first.
- No defensive `try/except` around logic that should not fail. Let it raise.

## Comments and docs

- Comment only what the code cannot say: invariants, concurrency assumptions, why-not-the-obvious-way.
- Never narrate the code, never explain the change, never leave notes addressed to a reviewer.
- Docstrings: one line, two if a param or return is non-obvious.
- No README, no summary markdown, unless asked.

## When stuck

- Two failed attempts at the same thing means stop and report, with the evidence.
- State what you observed, what you expected, and the narrowest next probe.
- Never fix a failing test by weakening the assertion. Say the code is wrong.

## Concurrency and correctness

- If shared state exists, say what guards it and what happens under simultaneous access.
- Prefer a test that actually races (threads, barriers) over one that asserts a counter.

## Reporting

- Lead with what changed and whether it works.
- Flag anything you guessed, skipped, or faked.
- If you left the code in a broken state, that is the first sentence.
