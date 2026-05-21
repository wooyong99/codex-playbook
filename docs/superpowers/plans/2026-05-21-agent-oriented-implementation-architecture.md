# Agent-Oriented Implementation Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align implementation playbook components around feature delivery orchestration skill, workflow-specific delivery engineer subagents, and stage-specific rule skills.

**Architecture:** Feature delivery orchestration is owned by a skill. Backend and frontend delivery engineer subagents execute domain design, implementation, and architecture review stages. Stage-specific skills provide concise rules. Docs remain knowledge resources.

**Tech Stack:** Codex subagent TOML, Codex skill Markdown, repository validation scripts.

---

## 목적

이 계획은 agent-oriented implementation architecture 리팩토링의 완료 항목과 검증 명령을 짧게 기록한다.

## Tasks

- [x] Add `feature-delivery-orchestration-rules`.
- [x] Add `backend-delivery-engineer`.
- [x] Add `frontend-delivery-engineer`.
- [x] Remove generic `implementation-orchestrator` and unused `infra-implementation-engineer`.
- [x] Fold feature delivery readiness criteria into `feature-delivery-orchestration-rules`.
- [x] Rename planning skill to `product-requirements-planning-rules`.
- [x] Rename API spec skill to `api-contract-design-rules`.
- [x] Rename backend TDD skill to `backend-technical-design-writing-rules`.
- [x] Add `backend-code-implementation-rules`.
- [x] Add `backend-architecture-review-rules`.
- [x] Rename frontend TDD skill to `frontend-technical-design-writing-rules`.
- [x] Add `frontend-code-implementation-rules`.
- [x] Add `frontend-architecture-review-rules`.
- [x] Remove broad `implement`, `implement-backend`, and `implement-frontend` skill entrypoints.
- [x] Move validation scripts to `.agents/scripts`.
- [x] Update docs that referenced old component names.
- [x] Run skill, structure, architecture, and playbook validation.

## Verification

- `python3 .agents/scripts/validate-agent-workflow-architecture.py`
- `python3 .agents/scripts/check-playbook.py`
- `python3 /Users/a1004/.codex/skills/.system/skill-creator/scripts/quick_validate.py <new skill>`
- `python3 .agents/skills/write-structured-artifact/scripts/check_structured_artifact.py <changed docs>`
