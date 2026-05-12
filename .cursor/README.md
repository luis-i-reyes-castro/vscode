# README

## Code Style Guidelines

* Python (for all projects):
  * Read `~/vscode/.cursor/rules.mdc`.
  * Python venv is in `~/pe`
* TypeScript (currently only for `~/customer-loyalty/`):
  * Read `~/vscode/.cursor/typescript.md`.
  * Skip for all other projects.

## Git Usage

* You may use `git` to print and list files and changes, but **DO NOT** execute any command with permanent effects (e.g., staging, committing, pushing, pulling, etc.).
* I will sometimes ask you to read or review staged code.
  * When editing/fixing the code, leave your changes unstaged so that I can stage them manually while checking your work.
  * If there is no staged code it probably means I forgot to stage my changes, so look in the working area.
* **IMPORTANT:** Trailing whitespace rules:
  * If line is non-empty: Trim
  * If line is empty: LEAVE UNTOUCHED, i.e., DO NOT TRIM.

## Working Style

* Bias toward terse, elegant code.
* Prefer minimal code over defensive abstraction.
* Keep implementations short, direct, and local.
* Read nearby files before editing.
* Do not rename files or move modules unless necessary.
* Reuse existing utilities before adding new helpers.
* Avoid helper proliferation, speculative generalization, and multi-step refactors unless they clearly reduce complexity.
* Do not add extra helpers, wrappers, or normalization layers unless they remove duplication in a meaningful way.
* When fixing a bug, prefer the smallest coherent change that preserves readability.
* If two solutions are correct, choose the one with fewer moving parts.
* Reuse built-in pandas operations when they keep the code simpler.
* Favor straightforward pandas transformations over custom row-processing utilities.
* If you think we need to add any new environment variables, API routes, backend functions, or database tables or columns, then clearly propose the structure of the new code and ask for permission to implement.

## Safety Rules

* Do not invent missing files, APIs, database tables, or workflows.
* If something is unclear, inspect the repo or ask instead of guessing.
* Prefer "not found in repo" over fabricating structure.

## Commonly Used Custom Packages

* `~/sofia-utils/`: Utility functions (mostly wrappers for I/O ops).
* `~/wa-agents/`: Package for implementing WhatsApp chatbots with or without (OpenRouter) LLMs models.
