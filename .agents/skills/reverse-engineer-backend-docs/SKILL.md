---
name: reverse-engineer-backend-docs
description: Analyze an existing backend codebase, infer its real modules, architecture units, cross-cutting policies, implementation strategies, and backend documentation needs, then create, update, migrate, or merge the `docs/backend` knowledge system so it reflects actual code instead of generic playbook assumptions. Use when applying codex-playbook to an existing backend, when `docs/backend` is empty/generic/misaligned with code, or when asked to reverse-engineer backend architecture, policies, strategies, getting-started notes, or backend design documentation from existing code.
---

# Reverse Engineer Backend Docs

## 목적

기존 백엔드 코드베이스를 분석해 실제 코드 구조와 반복 구현 방식을 `docs/backend` 지식 시스템에 반영한다.

이 스킬은 플레이북 일반론을 복제하지 않는다. 실제 모듈, 패키지, 책임 경계, 의존 방향, 정책 신호, 구현 전략, 레거시·혼재 구간을 코드 근거와 함께 문서화한다.

## 적용 범위

포함:

- `docs/backend/README.md`
- `docs/backend/getting-started.md`
- `docs/backend/architecture/**`
- `docs/backend/policies/**`
- `docs/backend/design/**`

제외:

- frontend 문서
- PRD
- 구현 코드 변경
- 코드 근거 없이 만드는 새 정책 또는 새 아키텍처 규칙

예외:

- 최상위 Backend 문서 홈 경로가 바뀔 때만 `AGENTS.md` 문서 맵을 갱신한다.

## 운영 모델

`reverse-engineer-backend-docs`는 코드 분석 결과를 문서 후보로 만들고, 문서 라우팅 기준에 따라 `docs/backend`를 생성·갱신한다.

```text
요청 범위 확인
  -> 실행 모드 결정
  -> 코드베이스 census와 샘플링
  -> 기존 docs/backend 분류
  -> 문서 소유 경계 설계
  -> mode별 생성·갱신·이전·병합
  -> 코드 근거와 문서 맵 검증
```

핵심 원칙:

- 코드에서 확인한 사실만 문서화한다.
- 실제 프로젝트의 이름과 책임 경계를 우선한다.
- 플레이북 레이어명은 분석 렌즈로만 쓰고 출력 구조로 강제하지 않는다.
- 상위 문서는 안정적인 진입점만 소유하고, 세부 구현 목록은 가장 가까운 README나 strategy 문서가 소유한다.
- 정책, 구현 아키텍처, 구현 전략, 설계 의도를 다른 위치에 둔다.
- 대형 코드베이스에서는 전체 정독보다 census, 우선순위화, 제한 샘플링, confidence report를 우선한다.

## 참조 문서

먼저 [references/README.md](references/README.md)를 읽고 문서 계층을 확인한다.

핵심 참조:

- 코드 구조 분석 기준: [references/codebase-analysis-guide.md](references/codebase-analysis-guide.md)
- 문서 위치와 실행 모드 라우팅: [references/backend-document-routing.md](references/backend-document-routing.md)
- `docs/backend` 파일별 작성 템플릿: [references/backend-doc-templates.md](references/backend-doc-templates.md)

## 실행 모드

모든 모드는 먼저 `inspect` 수준의 사전 판단을 수행한다.

| 모드 | 목적 | 파일 변경 |
|------|------|-----------|
| `inspect` | 코드 구조, 문서 후보, 기존 문서 분류, 추천 후속 모드를 보고한다. | 없음 |
| `generate` | 비어 있거나 충돌 없는 영역에 실제 코드 기반 문서를 새로 만든다. | 추가 중심 |
| `migrate` | 실제 코드와 충돌하는 기존 backend 문서 체계를 코드 기반 구조로 이전한다. | 이동·삭제 후보 포함 |
| `merge` | 기존 구조를 보존하면서 코드 근거가 약한 부분을 보강한다. | 보강 중심 |

10만 라인 이상 또는 모듈 수가 많은 저장소는 사용자가 `migrate`를 직접 요청해도 즉시 파일을 바꾸지 않는다. 먼저 `inspect` 계획서를 작성하고 단계별 migrate 실행 확인을 받는다.

모드 선택과 질문 기준은 [backend-document-routing.md](references/backend-document-routing.md)를 따른다.

## 작업 흐름

### 1. 입력 범위와 실행 모드 정리

- 분석 대상 코드베이스 경로를 정한다. 생략되면 현재 작업 디렉토리를 기본값으로 본다.
- 문서 출력 경로를 정한다. 생략되면 `docs/backend`를 기본값으로 본다.
- 실행 모드를 `inspect`, `generate`, `migrate`, `merge` 중 하나로 정한다.
- 모드가 생략되면 먼저 `inspect`로 구조와 문서화 계획을 보고한다.
- 대형 저장소의 `inspect` 계획서에는 규모 산정, 제외 경로, 우선순위, 샘플링 예산, 1차 migrate 범위, 후속 migrate/backlog 범위를 포함한다.

### 2. 코드베이스를 역공학한다

- 멀티 모듈인지 단일 모듈인지 먼저 구분한다.
- 실제 모듈명, 패키지명, 클래스 역할, 어노테이션, 인터페이스, 의존 방향을 근거로 기록한다.
- 안정적인 코드, 레거시 코드, 부분 마이그레이션, 팀별 관습 차이, 혼재된 구현 방식을 구분한다.
- 구현 전략 후보는 `권장 주류`, `상황별 변형`, `레거시 허용`, `충돌/확인 필요`, `단발성 제외`로 분류한다.
- 분석 절차와 메모 형식은 [codebase-analysis-guide.md](references/codebase-analysis-guide.md)를 따른다.

### 3. 기존 backend 문서를 분류한다

- 기존 `docs/backend`가 없는지, placeholder 수준인지, 실제 코드와 일치하는지, 플레이북 일반론과 충돌하는지 판단한다.
- 기존 문서를 `keep`, `merge`, `migrate`, `remove`, `archive` 후보로 분류한다.
- 사람이 작성한 보존 가치가 큰 문서는 삭제하거나 active path 밖으로 옮기기 전에 사용자 확인을 받는다.
- 분류 기준은 [backend-document-routing.md](references/backend-document-routing.md)를 따른다.

### 4. 문서 소유 경계를 설계한다

- `docs/backend/README.md`는 backend 하위 영역의 단일 진입점만 소유한다.
- `architecture/README.md`, `policies/README.md`, `design/README.md`는 각 영역의 가장 가까운 문서 맵을 소유한다.
- 정책, 구현 아키텍처, 구현 전략, 설계 의도는 관심사별로 다른 위치에 둔다.
- 같은 규칙이나 설명은 한 문서에만 원문으로 두고 다른 문서에서는 링크와 적용 맥락만 쓴다.
- 문서 라우팅 기준은 [backend-document-routing.md](references/backend-document-routing.md)를 따른다.

### 5. 실행 모드에 맞게 생성 또는 갱신한다

- `inspect`: 파일을 수정하지 않고 분석 결과, 문서 후보, 기존 문서 분류, 추천 후속 모드를 보고한다.
- `generate`: 비어 있거나 충돌 없는 영역에 실제 코드 기반 문서를 새로 만든다.
- `migrate`: 실제 코드와 충돌하는 기존 backend 문서 체계를 코드 기반 구조로 이전한다.
- `merge`: 기존 구조를 보존하면서 코드 근거가 약한 부분을 보강한다.
- 파일별 작성 구조는 [backend-doc-templates.md](references/backend-doc-templates.md)를 따른다.

## 검증

완료 전 아래 항목을 확인한다.

- 생성·수정한 문서가 실제 코드 근거와 연결되는지 샘플 기준으로 확인했다.
- 구현 전략 문서가 단일 예시만 설명하지 않고 적용 범위, 반복 근거, 변형, 예외, 레거시 주의점을 함께 담는다.
- 코드에서 확인되지 않은 정책, 실행 방법, 구현 패턴을 만들지 않았다.
- 가장 가까운 `README.md` 문서 맵이 추가·삭제·이동된 하위 문서를 반영한다.
- 상위 README가 하위 전략 문서나 내부 파일 목록을 직접 소유하지 않는다.
- 정책, architecture guideline, strategy 사이에 원문 중복이 남아 있지 않다.

스킬 문서 자체를 수정한 뒤에는 아래 검증을 수행한다.

- `python3 /Users/a1004/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/reverse-engineer-backend-docs`
- `python3 .agents/skills/write-structured-artifact/scripts/check_structured_artifact.py .agents/skills/reverse-engineer-backend-docs/SKILL.md .agents/skills/reverse-engineer-backend-docs/references/*.md`

## 완료 산출물

- 변경한 문서 경로 목록
- 코드 근거와 연결된 주요 문서화 판단
- 분석 범위, 제외 범위, coverage/confidence, 남은 미분석 영역
- 유지·병합·이전·삭제·archive 처리 결과
- 남은 불확실성과 사용자 확인이 필요한 항목
