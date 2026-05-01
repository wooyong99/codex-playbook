---
name: reverse-engineer-backend-docs
description: Analyze an existing backend codebase, infer its real modules, architecture units, cross-cutting policies, implementation strategies, and backend documentation needs, then create, update, migrate, or merge the `docs/backend` knowledge system so it reflects actual code instead of generic playbook assumptions. Use when applying codex-playbook to an existing backend, when `docs/backend` is empty/generic/misaligned with code, or when asked to reverse-engineer backend architecture, policies, strategies, getting-started notes, or backend design documentation from existing code.
---

# Reverse Engineer Backend Docs

기존 백엔드 코드베이스를 읽어 실제 모듈, 아키텍처 단위, 정책, 구현 전략, 실행 정보를 파악하고 `docs/backend` 하위 지식 시스템을 실제 코드 구조에 맞게 생성·갱신·이전한다.

## 먼저 읽을 자료

- 구조 탐색과 분석 기준: [references/codebase-analysis-guide.md](references/codebase-analysis-guide.md)
- 문서 위치와 실행 모드 판단: [references/backend-document-routing.md](references/backend-document-routing.md)
- 문서 작성 템플릿: [references/backend-doc-templates.md](references/backend-doc-templates.md)

## 책임 범위

이 스킬의 출력 범위는 `docs/backend` 전체다.

- `docs/backend/README.md`: backend 문서 홈, 영역별 단일 진입점, 문서 경계
- `docs/backend/getting-started.md`: 코드에서 확인한 빌드·실행·테스트·프로필 정보
- `docs/backend/architecture/**`: 실제 코드 단위, 책임, 의존 경계, 구현 전략
- `docs/backend/policies/**`: 여러 단위가 공통으로 따라야 하는 전역 정책과 금지 규칙
- `docs/backend/design/**`: 기술설계문서 가이드와 요청된 설계 문서. 기존 코드만 보고 임의의 신규 TDD를 만들지 않는다.

프론트엔드, PRD, 구현 코드 변경은 이 스킬의 기본 범위가 아니다.

## 작업 흐름

### 1. 입력 범위 확인

아래 항목을 먼저 정리한다.

- 분석 대상 코드베이스 경로
- 문서 출력 경로. 생략하면 `docs/backend`를 기본값으로 본다.
- 실행 모드: `inspect`, `generate`, `migrate`, `merge` 중 하나
- 분석할 모듈·패키지·아키텍처 단위 범위
- 기존 `docs/backend` 문서를 보존·병합·이전할지

사용자가 경로를 생략하면 현재 작업 디렉토리를 기본값으로 본다. 실행 모드를 생략하면 먼저 `inspect`로 구조와 문서화 계획을 제안한 뒤, 문서 변경이 필요한 경우 사용자의 진행 의사를 확인한다.

모든 실행 모드는 먼저 `inspect` 수준의 사전 판단을 수행한다. 코드 구조와 기존 `docs/backend` 상태를 확인하지 않은 채 파일을 생성·수정·삭제하지 않는다.

### 2. 코드베이스 역공학

먼저 대상 코드베이스가 멀티 모듈인지 단일 모듈인지 식별한다.

- 멀티 모듈이면 `settings.gradle.kts`, 각 모듈의 `build.gradle.kts`, 모듈 간 의존 관계, `src/main` 구조를 읽는다.
- 단일 모듈이면 `src/main/kotlin` 이하 패키지와 디렉토리 구조, import 방향, 클래스 역할을 읽는다.
- 단위 이름은 코드베이스가 실제로 쓰는 이름을 우선한다. 예: `admin`, `api`, `core`, `infrastructure`, `batch`, `notification`.
- `domain`, `application`, `storage`, `external`, `app` 같은 플레이북 개념 레이어는 출력 구조 기준이 아니라 분석 보조 렌즈로만 사용한다.
- 추측하지 말고 실제 모듈명, 패키지명, 클래스 역할, 어노테이션, 네이밍 패턴, 의존 방향을 근거로 판단한다.

자세한 분석 기준은 [codebase-analysis-guide.md](references/codebase-analysis-guide.md)를 따른다.

### 3. 문서 위치 결정

분석한 내용을 `docs/backend`의 어느 영역이 소유해야 하는지 먼저 결정한다.

| 구분 | 위치 | 작성 내용 |
|------|------|-----------|
| Backend 홈 | `docs/backend/README.md` | 영역별 진입점, 문서 경계, 어디서 시작할지 |
| 실행 안내 | `docs/backend/getting-started.md` | 빌드·실행·테스트·프로필·로컬 환경 |
| 정책 | `docs/backend/policies/{concept}.md` | 모든 아키텍처 단위가 지켜야 하는 원칙, 금지 규칙, 민감 정보·정합성·운영 기준 |
| 구현 아키텍처 | `docs/backend/architecture/{actual-unit}/{actual-unit}-guidelines.md` | 실제 코드 단위, 책임, 컴포넌트, 의존 경계, 정책을 만족하는 구조 |
| 구현 전략 | `docs/backend/architecture/{actual-unit}/strategies/{observed-pattern}.md` | 특정 단위 안에서 반복되는 구현 방식, 패턴, 체크리스트, 코드 근거 |
| 설계 문서 | `docs/backend/design/{topic}.md` | 사용자가 요청한 기능·서브시스템의 설계 의도. 기존 코드 근거 없이 임의 생성하지 않음 |

같은 개념이 정책, 구현 아키텍처, 구현 전략으로 나뉘면 문서 위치를 분리하고 중복 서술하지 않는다. 정책 문서에는 코드 배치나 클래스 구조를 쓰지 않는다. architecture 문서와 strategy 문서는 정책 원문을 재기술하지 않고 관련 정책을 링크한 뒤, 실제 코드가 그 정책을 어떻게 만족하는지만 작성한다.

문서 위치와 실행 모드 판단은 [backend-document-routing.md](references/backend-document-routing.md)를 따른다.

### 4. 문서 생성 또는 갱신

실행 모드별로 처리한다.

- `inspect`: 파일을 수정하지 않는다. 코드 구조, 기존 문서 상태, 제안 문서 구조, 보존·이전·삭제 후보, 추천 후속 모드를 보고한다.
- `generate`: 비어 있거나 충돌 없는 `docs/backend` 영역에 실제 코드 기반 문서를 안전하게 추가 생성한다. 기존 문서가 실제 코드 구조와 충돌하면 파일을 쓰지 않고 중단한 뒤 `migrate`를 제안한다.
- `migrate`: 기존 backend 문서 체계를 실제 코드 기반 체계로 교체한다. 기존 문서를 유지·이전·삭제 후보로 분류하고, 코드와 맞지 않는 플레이북 기반 문서는 active path에서 제거하거나 active path 밖으로 이전한다. 큰 구조 변경 전에는 계획을 먼저 제시한다.
- `merge`: 기존 문서 체계를 유지하면서 실제 코드 근거를 덧입힌다. 사람이 작성한 설명은 보존하고, 비어 있거나 일반론인 부분만 보강한다.

문서 템플릿은 [backend-doc-templates.md](references/backend-doc-templates.md)를 따른다.

### 5. 완료 전 검증

- 생성·수정한 문서가 실제 코드 패턴과 연결되는지 샘플 클래스 기준으로 다시 확인한다.
- 코드에서 발견되지 않은 패턴, 정책, 실행 방법을 새로 만들지 않았는지 확인한다.
- `docs/backend/README.md`가 backend 하위 영역의 단일 진입점만 참조하는지 확인한다.
- `docs/backend/architecture/README.md`의 아키텍처 맵이 실제 모듈·패키지·의존 방향과 어긋나지 않는지 확인한다.
- 정책, 구현 아키텍처, 구현 전략 사이에 같은 규칙이 중복 서술되지 않고 링크로 연결되는지 확인한다.
- 하위 디렉토리의 문서가 추가·삭제·개편되면 가장 가까운 `README.md` 문서 맵이 갱신되었는지 확인한다.

## 작성 규칙

- 사실 기반으로만 쓴다. 추측 금지.
- "이 프로젝트는 보통 이럴 것" 같은 일반론 대신, 코드에서 확인된 패턴만 적는다.
- 클래스명, 어노테이션, 폴더 구조, 인터페이스 관계 등 관찰 가능한 근거를 남긴다.
- 문서는 코드베이스에 맞는 설명이어야지, 플레이북 일반론이나 개념 레이어 구조의 복사본이 되면 안 된다.
- 플레이북 개념 레이어명은 출력 디렉토리명을 정하는 기본값으로 쓰지 않는다.

## 언제 질문할지

아래 경우에는 문서 생성 전에 사용자에게 확인한다.

- 출력 경로 후보가 둘 이상이라 어느 쪽에 써야 할지 불명확할 때
- 특정 아키텍처 단위가 혼재되어 있어 주 분석 단위를 모듈 기준으로 볼지 패키지 기준으로 볼지 애매할 때
- 실제 코드 단위명이 문서 디렉토리명으로 쓰기에 너무 구현 세부적이거나 임시적일 때
- 기존 `docs/backend` 구조를 유지할지 실제 코드 구조로 이전할지 선택이 필요할 때
- 기존 문서에 사람이 손으로 써둔 내용이 많아 병합/이전/삭제 후보 판단이 중요할 때
- 새 구조 적용이 최상위 Backend 문서 홈 경로 변경까지 요구할 때
