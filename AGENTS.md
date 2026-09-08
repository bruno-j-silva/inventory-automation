# Repository Guidelines

## Project Structure & Module Organization

This repository currently contains documentation only. Read `docs/spec.md` for requirements, then `docs/architecture.md`, `docs/db.md`, `docs/api.md`, and `docs/ui.md`. Technical choices remain proposals until consolidated.

The planned structure is `backend/app/modules/<module>/`, `backend/migrations/`, `backend/tests/`, `frontend/src/features/<module>/`, and `frontend/src/shared/`. Source code, tests, and application assets do not exist yet. Keep inventory, governance, operations, identity, and audit responsibilities separate.

## Build, Test, and Development Commands

No application build, test, or development commands are configured yet. Do not report hypothetical commands as working.

- `rg --files`: inspect available files.
- `rg -n 'E0-' docs/implementation-plan.md`: locate initial decision tasks.

During foundation work, document verified installation, startup, migration, lint, test, and build commands in `docs/development.md`. Pin dependencies and provide configuration examples without real credentials.

## Coding Style & Naming Conventions

For the proposed Python/TypeScript stack, use four-space Python indentation and two-space TypeScript indentation. Use `snake_case` for Python functions, database fields, and JSON contracts; use PascalCase for React components. Keep UI text and domain documentation in Brazilian Portuguese.

No formatter or linter is installed. Select and configure tooling during foundation work. Keep HTTP handling, business rules, and persistence separate; use versioned migrations.

## Testing Guidelines

Testing frameworks and numerical coverage thresholds are not yet selected. Require meaningful coverage of business rules, RBAC, transactional auditing, concurrency, and soft deletion. Add API/database integration tests and critical interface journeys.

Use descriptive names such as `test_critical_automation_requires_backup_owner`. Record commands actually executed and their results; distinguish unrun tests from passing tests.

## Commit & Pull Request Guidelines

Git history is unavailable in this workspace, so no existing convention can be inferred. Use concise imperative subjects, optionally scoped: `docs: clarify review acceptance`.

PRs should explain behavior, reference plan IDs and relevant issues, report validation, and identify migration impacts. Include screenshots for UI changes. Keep changes focused and documentation synchronized.

## Progress & Security

Follow `docs/implementation-plan.md`. Every additional plan must include stable checklist IDs, dependencies, acceptance criteria, and evidence. Mark `[x]` only after verification; update counts/history and present completed items, remaining work, blockers, and the next step each cycle.

Store credential references only. Enforce authorization in the backend, preserve immutable audit history, and never implement automation execution or code editing within this platform.
