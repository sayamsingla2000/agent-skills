# Skill Index

Lookup table for all skills in `~/.cursor/skills/`. Skills stay flat on disk (Cursor discovers `<name>/SKILL.md` one level deep) — this file is the bucket view for picking by requirement. Read this instead of re-deriving categories from scratch.

To use: name the bucket or skill and ask for it explicitly, e.g. "use orch-add-feature" or "give me the research bucket."

---

## Research & Intelligence
| Skill | Purpose |
|---|---|
| `deep-research` | Multi-source web research via firecrawl/exa MCPs, cited report output |
| `research-ops` | Evidence-first current-state research workflow (facts, comparisons, recommendations) |
| `exa-search` | Neural search (web, code, company, people) via Exa MCP |
| `iterative-retrieval` | Progressive context retrieval refinement for subagents that lack context |
| `search-first` | Search for existing tools/libs/patterns before writing custom code |
| `scientific-thinking-literature-review` | Systematic academic/technical literature review workflow |
| `scientific-thinking-scholar-evaluation` | Evaluate papers/proposals/methods against a rubric |
| `knowledge-ops` | Manage/sync/dedupe a knowledge base across files, MCP memory, vector stores |
| `competitive-platform-analysis` | Scope and tier a competitor set before benchmarking |
| `market-research` | Market sizing, competitor comparison, investor due diligence |
| `prompt-optimization-loop` | Tune any LLM prompt (classification, extraction, query/code gen, summarization) from observed failures — quick manual pass or full eval-set loop, with a per-prompt record for resuming later |

## Software Dev — Core / Cross-Language
| Skill | Purpose |
|---|---|
| `coding-standards` | Baseline naming/readability/immutability conventions (no framework match) |
| `api-design` | REST API design: resource naming, status codes, pagination, versioning |
| `architecture-decision-records` | Capture ADRs — context, alternatives, rationale |
| `contract-first` | Evolve API/event schemas across consumers without drift |
| `hexagonal-architecture` | Ports & Adapters design, dependency inversion, testable use cases |
| `error-handling` | Typed errors, retries, circuit breakers, error boundaries (TS/Python/Go) |
| `backend-patterns` | Backend architecture, API design, DB access (Node/Express/Next.js) |
| `database-migrations` | Schema/data migrations, rollbacks, zero-downtime deploys |
| `code-tour` | Persona-targeted step-by-step code walkthroughs with file/line anchors |
| `codebase-onboarding` | Generate architecture map + onboarding guide for an unfamiliar repo |
| `repo-scan` | Installer pointer for cross-stack source-code asset audit |

## Language / Framework Specific (this repo's stack)
| Skill | Purpose |
|---|---|
| `python-patterns` | Pythonic idioms, PEP 8, type hints |
| `python-testing` | pytest strategies — fixtures, mocking, parametrization, coverage |
| `fastapi-patterns` | FastAPI structure, Pydantic v2, DI, async handlers, auth, testing |
| `postgres-patterns` | PostgreSQL schema, indexing, query optimization, RLS |
| `redis-patterns` | Redis caching, distributed locks, rate limiting, pub/sub |
| `mcp-server-patterns` | Build MCP servers (Node/TS SDK) — tools, resources, prompts |
| `bun-runtime` | Bun as runtime/bundler/test runner, vs Node |
| `nextjs-turbopack` | Next.js 16+ and Turbopack bundling/dev speed |

## Testing & Quality
| Skill | Purpose |
|---|---|
| `tdd-workflow` | Enforce TDD with 80%+ coverage (unit/integration/E2E) |
| `e2e-testing` | Playwright patterns — Page Object Model, CI integration, flaky tests |
| `verification-loop` | Verify a session's work before claiming it complete |
| `production-audit` | Local-evidence production-readiness audit, pre-launch/post-merge |
| `security-review` | Security checklist for auth, user input, secrets, payments |
| `security-scan` | Scan `.claude/` config for injection risks/misconfigurations |

## DevOps & Infra
| Skill | Purpose |
|---|---|
| `docker-patterns` | Docker/Compose for local dev, hardened installers, multi-service orchestration |
| `deployment-patterns` | CI/CD pipelines, containerization, health checks, rollback strategies |
| `kubernetes-patterns` | K8s workloads, RBAC, probes, autoscaling, kubectl debugging |
| `git-workflow` | Branching strategy, commit conventions, merge vs rebase |
| `github-ops` | Issue/PR triage, CI status, releases via `gh` CLI |

## Agent Building & Debugging
| Skill | Purpose |
|---|---|
| `agent-architecture-audit` | 12-layer diagnostic for misbehaving agent/LLM stacks |
| `agent-harness-construction` | Design agent tool sets, action space, observation format |
| `agent-introspection-debugging` | Structured post-mortem for a failed agent run |
| `agent-eval` | Benchmark coding agents head-to-head (pass rate, cost, time) |
| `agent-self-evaluation` | Self-score completed output on 5 axes with evidence |
| `agent-sort` | Sort ECC skills/commands into DAILY vs LIBRARY for a specific repo |

## Agent Ops & Autonomous Loops
| Skill | Purpose |
|---|---|
| `continuous-agent-loop` | Self-checking agent loop with eval gates and failure recovery |
| `continuous-learning-v2` | Extract session lessons into confidence-scored "instincts" |
| `enterprise-agent-ops` | Long-lived agent workloads — observability, security, lifecycle |
| `dynamic-workflow-mode` | Task-local harnesses, eval gates, reusable skill extraction |
| `agentic-engineering` | Eval-first, decomposed, cost-aware execution model for agent work |
| `ai-first-engineering` | Team process/review gates for AI-majority-written codebases |
| `safety-guard` | Block destructive ops during autonomous agent runs |
| `operator-approval-loop` | Human approval gate for agent-drafted outbound messages |
| `recursive-decision-ledger` | Repeated rollouts / search with a visible decision trail |
| `parallel-execution-optimizer` | Speed up tasks via parallel agents/batched calls/worktrees |
| `token-budget-advisor` | Let user control response depth/token spend |
| `strategic-compact` | Suggest manual context compaction at natural task-phase boundaries |
| `cost-aware-llm-pipeline` | Model routing by task complexity, budget tracking, prompt caching |

## Multi-Agent Orchestration
| Skill | Purpose |
|---|---|
| `orch-pipeline` | Shared Research→Plan→TDD→Review→Commit engine behind `orch-*` (not called directly) |
| `orch-add-feature` | Build a brand-new feature end to end via the gated pipeline |
| `orch-build-mvp` | Turn a design/PRD into a running MVP via vertical slices |
| `orch-change-feature` | Change existing behavior: update tests to new spec, then implementation |
| `orch-fix-defect` | Fix a bug via failing regression test → green |
| `orch-refine-code` | Behavior-preserving refactor with tests staying green |
| `team-agent-orchestration` | Coordinate an agent squad — work items, Kanban, merge gates |
| `team-builder` | Interactive picker for composing a parallel agent team |
| `dev-team` | Simulate PM/Architect/Developer/QA personas on one problem |
| `santa-method` | Two independent adversarial reviewers must both pass before shipping |
| `blueprint` | One-line objective → multi-session, multi-agent construction plan with review gates |

## Content & Business (non-dev)
| Skill | Purpose |
|---|---|
| `article-writing` | Long-form content — articles, guides, blog posts in a given voice |
| `content-engine` | Platform-native content systems (X, LinkedIn, TikTok, YouTube, newsletters) |
| `frontend-slides` | Animation-rich HTML presentations, PPT conversion |
| `investor-materials` | Pitch decks, one-pagers, investor memos, financial models |
| `investor-outreach` | Cold emails, warm intros, investor communications |
| `documentation-lookup` | Up-to-date library/framework docs via Context7 MCP |

## Personal / Meta
| Skill | Purpose |
|---|---|
| `bootstrap` | Scaffold a new Python project — pytest harness, git, Makefile |
| `grill` | Interview the user relentlessly to pin down a plan before coding |
| `unified-memory` | Share durable context/handoffs across Claude, Codex, Cursor, etc. |
| `prompt-optimizer` | Rewrite a rough prompt into an optimized, component-mapped prompt. **Manual-invoke only** — use your own prompt/inputs first; fall back to this only when you don't have one |
| `skill-stocktake` | Audit installed skills/commands for quality (Quick Scan or Full Stocktake) |
