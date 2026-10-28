# 2004 Spring Beijing Arts Intake Registration Plan

> **For agentic workers:** Execute inline in the existing `feat/gaokao-phase0` worktree. This phase ends with a reviewed, phase-scoped commit.

**Goal:** Register the already transcribed 2004 Spring Beijing arts paper against its fixed local PDF while preserving the unresolved Q20 transcription and source identity limits.

**Architecture:** Use the existing `source_manifest.py register-papers` transaction to add the paper, batch, source binding, and Q20 blocker atomically. Move the two existing TikZ files into the paper project directory, update only this paper's source files, and refresh the normal report projections.

**Tech Stack:** Markdown, JSON, TikZ, and the repository's Python validation CLIs.

**Spec:** `math-gaokao-latex/source-manifest.json` and `math-gaokao-latex/tools/source_manifest.py` registration schema.

## Global Constraints

- Preserve the exact fixed source SHA-256 `4670b402354afd088d6993fbc473490158f27e232b1c54730e5989b64a21ec26`.
- Keep publisher, edition, source chain, and official-answer identity unverified; `official_answer` remains `null`.
- Preserve Q20's source wording “计算公以及” and register it as an open completion blocker.
- Keep the paper `blocked` and batch `planned`; do not create provenance or build/review receipts in this phase.
- Stage only the files changed for this phase, inspect `git diff --cached --check` and the full staged diff, then commit.

## Review Focus

- Wrong source binding: verify source ID, SHA, blob and PDF page count match the existing fixed record.
- Lost figure links: ensure both TikZ files are in the project directory and each Markdown figure link resolves.
- Lost uncertainty: ensure Q20 remains verbatim and its issue keeps the paper blocked.
- False provenance: ensure the internal canonical relation does not claim an official publisher, edition, source chain, or answer.
- Stale projections: ensure report and CSV projections match the post-registration manifest.

---

### Task 1: Register the paper and close the registration phase

**Files:**
- Modify: the 2004 Beijing arts question, answer, solution, and figure-list Markdown files.
- Create: `math-gaokao-latex/2004_春季北京文科/figures/` with the two existing TikZ sources.
- Modify: `source-manifest.json`, `missing-issues.md`, `PROGRESS.md`, and generated reports/CSV.
- Create: `reports/2004-beijing-spring-arts-registration.md`.

- [ ] Move the existing TikZ sources and update their paper-relative links.
- [ ] Generate the deterministic combined Markdown from the three canonical sources.
- [ ] Dry-run and write one `phase1-b52` registration for `gk-2004-spring-beijing-arts`, including the Q20 transcription blocker.
- [ ] Run source-manifest, issue, combined-source, report, and CSV currentness validators; do not run the test suite.
- [ ] Stage only this phase, inspect the staged diff and whitespace check, then commit.
