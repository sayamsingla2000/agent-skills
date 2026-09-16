# Prompt record file templates

Used by `prompt-optimization-loop`. Paths are relative to `docs/prompt-records/<slug>/` (verify the location isn't gitignored — see SKILL.md).

Examples below cover a classification prompt and a query-generation prompt to show the formats are task-agnostic.

## `current.md`

The live prompt text, nothing else — no frontmatter, no commentary — so it can be copied straight back into the codebase.

```text
<the exact current prompt text, verbatim>
```

## `history.md`

Append-only, newest at the bottom. Never edit or delete a past entry; if a revision is reverted, append a new entry saying so.

```markdown
## 2026-09-16 — v1 (initial)
Trigger: baseline, no prior record
Change: n/a (first version)
Score: n/a — not yet evaluated

## 2026-09-18 — v2
Trigger: 4 queries referenced a non-existent column (see failures.md #3-#6)
Change: added "only use columns listed in the provided schema block; never infer column names"
Score: 0.62 -> 0.85 executable-and-correct rate on 20 held-out questions
Status: accepted

## 2026-09-18 — v2b (rejected)
Trigger: attempt to also fix verbose output
Change: added "be terse" instruction
Score: 0.85 -> 0.71 — terseness instruction caused dropped GROUP BY clauses
Status: rejected, kept v2

## 2026-10-20 — v3
Trigger: new requirement — must support relative date ranges ("last quarter") (see failures.md #7-#9)
Change: added date-resolution step with explicit fiscal-quarter definition
Score: 0.85 -> 0.88 held-out
Status: accepted
```

## `failures.md`

Append-only, permanent regression set. Every case here should still pass on any future revision — check the whole file before accepting a new version, not just this round's failures. Redact secrets and customer data; this file is committed.

```markdown
## #1 — 2026-09-16 (classification example)
Input: "the food was fine i guess"
Got: positive
Expected: neutral
Reason: model defaults to positive when uncertain
Drove: v2 tie-break rule

## #3 — 2026-09-18 (query generation example)
Input: "revenue by region last month"
Got: SELECT region, SUM(revenue_total) FROM orders ...
Expected: SELECT region, SUM(net_revenue) FROM orders ...
Reason: hallucinated column `revenue_total`; schema has `net_revenue`
Drove: v2 schema-adherence rule

## #7 — 2026-10-20 (query generation, new requirement)
Input: "how did we do last quarter"
Got: date filter for previous 90 days
Expected: fiscal quarter boundaries (Q3: Jul 1 - Sep 30)
Reason: no fiscal-quarter definition in prompt
Drove: v3 date-resolution step
```

## `learnings.md`

Distilled rules, not a log. Short, generalizable, treated as hard constraints on future revisions. Add only when something genuinely reusable was learned.

```markdown
- Generation prompts hallucinate field names unless the allowed schema is inlined and marked as exhaustive — always state "only these columns exist".
- Terseness instructions on query generation cause dropped clauses (GROUP BY, date filters). Constrain verbosity in the output format section, never as a global "be brief".
- Relative time expressions ("last quarter", "recently") need an explicit resolution rule; the model silently picks rolling windows otherwise.
- Feedback rewrites without the "generalize, don't overfit" line hardcode surface tokens from the examples. Always keep that line.
```

## `harness.py`

Full-loop mode only. Plain Python — no external prompt-optimization library. Four functions sized to this prompt's actual input/output shape. Not a fixed template since shapes vary; structure to follow:

```python
"""Optimization harness for <slug>. Update only if input/output shape changes."""

def run(prompt: str, rows: list[dict]) -> list:
    """Call the LLM once per row with `prompt`; return outputs parsed to this task's shape."""
    ...

def score(outputs: list, targets: list) -> tuple[float, list[dict]]:
    """Return (aggregate_metric, per_row) where per_row carries passed/failed plus a reason.

    Reasons matter: they become the mistake context fed to next_prompt().
    """
    ...

def next_prompt(prompt: str, mistakes: list[dict], task: str, instructions: str = "") -> str:
    """Apply the feedback meta-prompt (SKILL.md). Raise if no <new_prompt> tag after one retry."""
    ...

def optimize(
    prompt: str,
    optimize_rows: list[dict],
    heldout_rows: list[dict],
    *,
    max_iterations: int,
    min_score_gain: float,
    target_score: float,
) -> tuple[str, float]:
    """Wire the three together with early stopping. Tracks best-so-far and returns it, not the last candidate."""
    ...
```

Next session: import this file and call `optimize(current_prompt, new_rows, heldout_rows, ...)` with the newly collected failures. Only rewrite the harness if the prompt's input or output shape changed.
