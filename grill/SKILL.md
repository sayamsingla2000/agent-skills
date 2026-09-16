---
name: grill
description: Interview the user relentlessly about a plan or coding task until reaching shared understanding at the level of files, signatures, and edge cases, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, align before implementation, or mentions "grill me".
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

If a question can be answered by exploring the codebase, explore the codebase instead.

## How to ask

Batch the questions. Use the `AskQuestion` tool with every independent question in a single call, recommended answer as the first option labelled `(Recommended)`.

Hold back only questions whose wording genuinely depends on an answer you do not have yet, and ask those in a follow-up batch.

Options must be concrete — real file paths, real function names, real field names. Never "option A / option B".

Drop any question whose answer would not change the code that gets written.

## What to grill on

Walk these branches, skipping what does not apply. Answers to earlier ones often kill later ones.

| Branch | Resolve |
|---|---|
| Contract | Exact function/endpoint/CLI signature; inputs, outputs, return type |
| Data shape | Field names, types, nullability, where state lives |
| Placement | Which file; extend existing utility vs new module; naming |
| Edge cases | Empty, missing, duplicate, concurrent, oversized input |
| Failure mode | Raise vs return error vs silent default; logging; retries |
| Scope boundary | What is explicitly **not** in this change |
| Verification | How the user confirms it works; tests expected or not |
| Migration | Backwards compatibility; existing callers or data |

## When the branches are resolved

State the agreed spec back: files touched, real signatures, data shapes, numbered behaviour, edge case → handling, out of scope, verification steps. Then ask for a go-ahead.

If the user defers — "you decide", "not sure", or a skipped question — stop asking. Fill every open decision with your recommended answer, list those under **Assumptions**, and ask for a single yes/no.

Skip all of this for a trivial ask: one-line fix, rename, or a change with exactly one sensible implementation. Just do it.

Once implementing, build exactly the agreed spec. If a fork appears that the spec did not cover and it changes behaviour the user cares about, stop and ask once rather than guessing.
