# Agent Skills Operational Directive (High Priority)

## Mandatory Skill Identification & Proactive Invocation

Whenever a project, feature, or task is started, you MUST immediately analyze the requirements against the installed **Agent Skills** catalog (`addyosmani/agent-skills`) and proactively activate the appropriate skill(s) to guide your execution.

### The 25 Core Skills & When to Use Them:

1. **New Projects & Feature Scoping:**
   - `spec-driven-development`: Write structured specifications before writing code. Use for new projects, ambiguous requirements, or architectural decisions.
   - `idea-refine`: Clarify and sharpen raw concepts into actionable product hypotheses.
   - `interview-me`: Conduct structured interviews to extract domain requirements and design intent.

2. **Architecture, Planning & Task Breakdown:**
   - `planning-and-task-breakdown`: Map dependencies and vertically slice tasks before implementing.
   - `constraint-driven-development`: Define and enforce system constraints (latency, memory, platforms).
   - `api-and-interface-design`: Design ergonomic, robust contracts and APIs before implementation.
   - `context-engineering`: Keep context clean, select relevant files, and prevent token bloat.

3. **Implementation & Code Quality:**
   - `incremental-implementation`: Deliver small, verified changes one commit/step at a time.
   - `test-driven-development` (TDD): Write failing tests first, make them pass, refactor.
   - `code-review-and-quality`: Run systematic code health checks, enforce linting, and catch anti-patterns.
   - `code-simplification`: Refactor, deduplicate, and eliminate unnecessary complexity.
   - `source-driven-development`: Verify against ground-truth source code rather than assumptions.
   - `doubt-driven-development`: Actively stress-test edge cases, assumptions, and failure modes.

4. **UI, Testing & Debugging:**
   - `frontend-ui-engineering`: Build accessible, high-performance, polished user interfaces.
   - `browser-testing-with-devtools`: Validate DOM, console logs, responsive layout, and network requests.
   - `debugging-and-error-recovery`: Root-cause errors systematically using stack traces and logs.

5. **Security, Performance & Operations:**
   - `security-and-hardening`: Audit input validation, secrets management, authentication, and CVEs.
   - `performance-optimization`: Benchmark, profile, identify bottlenecks, and optimize algorithms.
   - `observability-and-instrumentation`: Add metrics, structured logs, and health endpoints.
   - `ci-cd-and-automation`: Configure CI pipelines, build scripts, and automated quality gates.
   - `git-workflow-and-versioning`: Clean atomic commits, semantic versioning, and branch management.
   - `deprecation-and-migration`: Safely retire legacy APIs and execute schema/data migrations.
   - `documentation-and-adrs`: Record Architecture Decision Records (ADRs) and living documentation.
   - `shipping-and-launch`: Pre-flight verification checklist before production release.
   - `using-agent-skills`: Meta-skill for discovering and combining skills across the workflow.

## Operational Workflow

1. **Step 1: Identify Relevant Skills** — At the onset of any task, check which skills match the objective.
2. **Step 2: Proactive Activation** — Explicitly invoke and read the `SKILL.md` instructions for the selected skill.
3. **Step 3: Execute in Lockstep** — Follow the skill's gated process, checklist, and verification requirements.
4. **Step 4: Quality Gate** — Verify that the skill's definition of "Done" is fully satisfied before concluding.
