---
name: prompt-optimization-loop
description: >-
  Tune a user's own LLM prompt when its output doesn't match the required
  result — drive revisions from observed failures and feedback instead of
  rewording blind. Works for any prompt type: classification/LLM-judge,
  structured extraction, query or code generation, summarization, free-text
  generation. Covers a quick manual pass (a few bad outputs, revise now) and
  a full automated loop (eval set, held-out scoring, early stopping, multiple
  starts), and keeps a per-prompt record so a session months later resumes
  instead of restarting. Use when a prompt isn't producing the needed result,
  when wrong-vs-expected outputs are available for it, or when a prompt needs
  systematic improvement against an eval set.
---

# Prompt Optimization Loop

Technique source: [Evidently AI — automated prompt optimization](https://www.evidentlyai.com/blog/automated-prompt-optimization). The idea is borrowed, the implementation is local — do not import or depend on their library.

Instead of hand-tweaking wording, feed the LLM its own failures and ask it to generalize a fix.

## When to use

- A prompt already in use produces output that doesn't match what's needed, and there are concrete bad outputs to learn from
- The user can paste or point to wrong-vs-expected output pairs and wants a revised prompt
- A prompt needs systematic improvement against an eval set, repeatable as requirements change

## When NOT to use

- There's no way to tell a good output from a bad one, and no rubric or judge can be constructed — feedback has nothing to anchor on
- No failure examples exist at all and none can be produced — that's a cold rewrite, not this technique

## Task types — this is not classification-only

The loop is identical across task types; only the scorer and the definition of "mistake" change.

| Task type | Example | Scorer | A "mistake" is |
|---|---|---|---|
| Classification / LLM-judge | sentiment, pass-fail, intent routing | exact match vs label → accuracy | `output != target_label` |
| Structured extraction | pull fields into JSON | per-field match, schema validity | any wrong/missing/extra field |
| Query or code generation | NL → analytics query, NL → SQL | execute it: does it run, and does the result set match expected? plus schema/field-name validity | fails to execute, or wrong result set, or hallucinated field |
| Summarization / free-text | data story, narrative summary | rubric LLM-judge scoring named criteria (coverage, no invented numbers, tone) | any row scoring below the pass bar |
| Multi-constraint output | must hit format + tone + length | checklist scorer, one boolean per constraint | any violated constraint |

For non-exact-match tasks, a mistake carries the **scorer's reason**, not just a wrong value — feed that reason into the feedback prompt. "Judge said: invented a revenue figure not present in input" improves a prompt far more than a bare low score.

## Two modes

**Quick/manual — default for a one-off "fix my prompt" ask.** No dataset, no harness, no code. Take the current prompt plus whatever bad outputs exist (1–3 is enough), apply the feedback meta-prompt below, hand back the revised prompt, ask the user to re-test. Repeat once or twice. Still write the record files (below) — cheap, and it's what makes the next session resumable.

**Full automated loop — when the user wants a repeatable optimizer, not a single fix.** Needs an eval set (~10+ rows) and a programmatic scorer. Build the harness described below.

## Persistent record — resume across sessions

Every session for a given prompt reads and writes one record directory, so a session months later with new failures resumes instead of re-litigating fixed problems.

**Location**: `docs/prompt-records/<slug>/` at the repo root. `<slug>` is a kebab-case id for the prompt, derived from its purpose or source file (e.g. `query-generation`, `d2c-mini-system-prompt`).

Before creating it, confirm the path is not ignored:
```bash
git check-ignore -v docs/prompt-records/<slug>/current.md   # must print nothing
```
Do **not** put records under `.cursor/` — it is gitignored in many repos (including agent-service, via `.cursor/*`), which silently makes the record untracked and defeats the purpose. If the chosen path is ignored, pick a tracked one and say which was used.

**Files** (templates: [reference-records.md](reference-records.md)):

| File | Purpose | When to write |
|---|---|---|
| `current.md` | The live prompt text right now | Overwrite when a revision is accepted |
| `history.md` | Append-only: one entry per iteration — timestamp, trigger, what changed, score, accepted/rejected | Append every iteration, never edit past entries |
| `failures.md` | Every failure case ever observed, dated, with which iteration it drove | Append; never delete, even once fixed — this is the regression set |
| `learnings.md` | Distilled generalizable rules ("always pin the output schema or it drifts to prose") | Only when something reusable is learned |
| `harness.py` | This prompt's actual `run`/`score`/`next_prompt`/`optimize` code (full-loop mode only) | Once when built; update only if input/output shape changes |

**Start of every session** — check whether the record directory exists:

- **Exists**: read `current.md` and `learnings.md` in full, plus the last 3–5 `history.md` entries. Treat `learnings.md` as hard constraints; don't reintroduce something it documents as fixed. Treat `failures.md` as a regression set — a new candidate must still handle the old cases, not just today's. If `harness.py` exists, reuse it and feed it the new rows; only modify it if the input/output shape itself changed.
- **Doesn't exist**: create the directory and seed `current.md` with today's starting prompt; create `history.md`, `failures.md`, `learnings.md` empty; add `harness.py` only in full-loop mode.

**Drift check (do this before iterating)**: compare `current.md` against the prompt actually live in the codebase. They diverge whenever someone hand-edited the prompt outside this loop. If they differ, treat the **codebase** as truth, append a `history.md` entry recording the out-of-band edit, overwrite `current.md`, and only then start iterating. Never silently optimize a stale prompt.

**Every iteration**: append to `history.md` as it happens (don't batch at the end), append new failures to `failures.md`, and update `current.md` only when a revision is actually accepted — not for every candidate generated.

## Architecture

A pattern to implement per prompt, not a library to import. Write small plain functions sized to *this* prompt's shapes:

| Role | Job |
|---|---|
| `run(prompt, rows) -> outputs` | Call the LLM once per row with the candidate prompt, parse to this task's output shape |
| `score(outputs, targets) -> (metric, per_row_results)` | Return the aggregate number **and** per-row pass/fail with reasons, since mistakes drive the next step |
| `next_prompt(prompt, mistakes, task, instructions) -> str` | Generate the next candidate via the feedback meta-prompt |

Loop:
```
1. outputs = run(current_prompt, rows)
2. metric, per_row = score(outputs, targets)
3. append iteration + new failures to the record
4. stop? (see Early stopping) -> yes: return best-scoring prompt so far
5. mistakes = rows failing in per_row  ->  next_prompt(...)  ->  back to 1
```

Keep a `best_prompt`/`best_score` pair across iterations and return that, never just the last candidate — candidates can regress.

## Feedback meta-prompt

```text
I ran LLM for some inputs to do {task} and it made some mistakes.
Here is my original prompt <prompt>
{prompt}
</prompt>
And here are rows where LLM made mistakes:
<rows>
{rows}
</rows>.
Please update my prompt to improve LLM quality.
Generalize examples to not overfit on them.
{instructions}
Return new prompt inside <new_prompt> tag
```

Placeholders:
- `{task}` — one line describing the job ("generate an analytics query from a natural-language question").
- `{rows}` — mistake examples: input, expected, what came out, and the scorer's reason. Cap at ~10–20; dumping everything undercuts the generalize instruction.
- `{instructions}` — task-specific constraints the rewrite must not break: output contract ("must stay valid JSON matching this schema"), sections that must survive verbatim, length limits, tone. Leave empty only if there are genuinely no invariants.
- The "generalize, do not overfit" line is load-bearing. Without it, the rewrite hardcodes surface patterns from the examples ("if text contains 🚀, output 1").

## Held-out scoring and small datasets

| Eval set size | What to do |
|---|---|
| < 10 rows | Skip formal splits — they'd be 2/2/1 and meaningless. Iterate on all rows, then sanity-check the final prompt on fresh examples the loop never saw. State plainly that the result is directional, not measured. |
| 10–30 rows | Two-way split (e.g. 60/40 optimize/held-out), or leave-one-out if labels are expensive. Select on held-out, not on the rows being optimized against. |
| 30+ rows | 40/40/20 train/validation/test. Optimize on train, select the best prompt on validation, report the final number on test only. Never let the loop see test rows. |

The point of a held-out set: a prompt that memorized the examples scores well on them and visibly fails elsewhere, so it gets discarded.

## Early stopping

Set all three; stop on whichever hits first.

| Param | Meaning |
|---|---|
| `max_iterations` | Hard cap on attempts (also the cost ceiling) |
| `min_score_gain` | Minimum improvement to count as progress; below it, treat as converged |
| `target_score` | Stop once the held-out score reaches this (e.g. 0.97) |

## Multiple starts

LLM generation is stochastic — the same starting prompt can converge differently. Repeat the whole run N times and keep the best held-out scorer. Worth it when a single run plateaus below target.

## Edge cases and failure modes

Handle these explicitly; each one is a real way the loop breaks.

| Situation | Handling |
|---|---|
| Response has no `<new_prompt>` tag | Don't regex-guess the whole response into a prompt. Retry once with the same input; if it fails again, fall back to the previous prompt, log it in `history.md`, and report the parse failure rather than shipping garbage. |
| Candidate scores **worse** than current | Reject it, keep `best_prompt`, and log the rejection with its score. A rejected candidate is still useful history — it records what doesn't work. |
| Score moves but the change is noise | Fix temperature low (0 where supported) for scoring runs. If scores still fluctuate across identical runs, average over 2–3 runs before comparing, and set `min_score_gain` above the observed noise band. |
| Zero mistakes on the first pass | Nothing to optimize — stop and say so. Either the prompt is already fine or the eval set is too easy; suggest harder examples instead of iterating. |
| Every row fails | Usually not a wording problem — check for a broken output contract, wrong model, or a parsing bug in `run()` before asking for a prompt rewrite. |
| Rate limits / cost blowup | Throttle concurrency, cache per `(prompt, row)` so re-scored rows don't re-bill, and treat `max_iterations` as a budget. Route LLM calls through the existing client and cost-tracking wrapper (see the `track-claude-cost` skill), never a raw client. |
| `current.md` disagrees with the codebase | Drift check above — codebase wins, record the out-of-band edit, then iterate. |
| Slug already exists for a different prompt | Don't append to someone else's record. Pick a more specific slug and note the sibling in `history.md`. |
| Prompt contains secrets or customer data in examples | Redact before writing to `failures.md` — the record is committed to the repo. |

## Implementation checklist (full loop only)

- [ ] Define the eval row schema for *this* task: `input`, expected value (`target_label` / `target_json` / `target_result_set` / rubric criteria), optional `reasoning`
- [ ] Choose the scorer from the task-type table; make it return per-row reasons, not just an aggregate
- [ ] Split per the size table above (or explicitly skip splits and say why)
- [ ] Write `run()`, parsing to this task's output shape; batch/async if the SDK supports it
- [ ] Write `score()` returning `(metric, per_row_results)`
- [ ] Write `next_prompt()` using the meta-prompt, with `{instructions}` filled from the prompt's real invariants
- [ ] Write `optimize()` wiring them with early stopping and best-so-far tracking
- [ ] Save the code as `harness.py` in the record directory so the next session reuses it
- [ ] Write every iteration to `history.md` / `failures.md` as it happens
- [ ] Add multiple starts as an outer loop if a single run plateaus
- [ ] Report the final score on held-out data only, and state which rows it was measured on

Before building new scaffolding, check whether this repo already has judge, eval, or prompt-harness code to extend instead (`agent_utils/`, pattern engine, eval harness) — extend it rather than adding a parallel implementation.

## Other approaches (context)

| Approach | Why not the default |
|---|---|
| Search-based (grid/random/genetic/Bayesian) | Slow and eval-hungry; rarely worth it at prompt scale |
| Model-internals (gradients, soft prompts) | Needs weight access — impossible against API-only models |
| Self-improvement with no failure context | Works, but weaker: nothing grounds the rewrite in real errors |
| Example-based / few-shot selection | Improves demonstrations, not instructions — complementary, not a replacement |

The approach above is a hybrid: self-improvement grounded in held-out evaluation and real mistake context.
