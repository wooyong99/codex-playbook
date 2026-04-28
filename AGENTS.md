# AGENTS Guide

## 프로젝트 명

- {프로젝트명}

## 비즈니스 목표

- {비즈니스 목표 1}
- {비즈니스 목표 2}
- {비즈니스 목표 3}

## AI 에이전트 공통 작업 지침

### 1) 코딩하기 전에 먼저 생각하라

- 섣불리 가정하지 않는다.
- 헷갈리는 것은 숨기지 않고 질문한다.
- 선택지가 있을 때 각 장단점을 먼저 설명한다.

### 2) 먼저 단순하게 생각하라

- 문제 해결에 필요한 최소한의 코드만 작성·수정한다.
- 미래 요구를 상상해 불필요한 기능을 미리 구현하지 않는다.

### 3) 수술하듯 필요한 부분만 고쳐라

- 변경 범위를 반드시 필요한 부분으로 제한한다.
- 기존 동작을 불필요하게 건드리지 않는다.

### 4) 목표 중심으로 실행하라

- 성공 기준을 먼저 정의한다.
- 기준이 충족될 때까지 검증을 반복한다.

## 프로젝트 구조

```text
.
├── .agents/      # 에이전트 스킬 및 참조 문서
├── docs/         # 프로젝트 지식 시스템(백엔드/프론트엔드/PRD)
└── AGENTS.md     # 에이전트 작업 지침서
```

## 문서 맵

### 최상위

- [PRD](/Users/jeong-uyong/work/codex-playbook/docs/PRD.md)
- [Backend 문서 홈](/Users/jeong-uyong/work/codex-playbook/docs/backend/README.md)
- [Frontend 문서 홈](/Users/jeong-uyong/work/codex-playbook/docs/frontend/README.md)

### Backend

- [Getting Started](/Users/jeong-uyong/work/codex-playbook/docs/backend/getting-started.md)
- [아키텍처 개요 및 규칙](/Users/jeong-uyong/work/codex-playbook/docs/backend/architecture/documentation-convention.md)
- [App Layer 가이드](/Users/jeong-uyong/work/codex-playbook/docs/backend/architecture/app/app-layer-guidelines.md)
- [Application Layer 가이드](/Users/jeong-uyong/work/codex-playbook/docs/backend/architecture/application/application-layer-guidelines.md)
- [Domain Layer 가이드](/Users/jeong-uyong/work/codex-playbook/docs/backend/architecture/domain/domain-layer-guidelines.md)
- [Storage Layer 가이드](/Users/jeong-uyong/work/codex-playbook/docs/backend/architecture/storage/storage-layer-guidelines.md)
- [External Layer 가이드](/Users/jeong-uyong/work/codex-playbook/docs/backend/architecture/external/external-layer-guidelines.md)
- [DDL 관리](/Users/jeong-uyong/work/codex-playbook/docs/backend/architecture/storage/ddl-management.md)
- [정책: 보안](/Users/jeong-uyong/work/codex-playbook/docs/backend/policies/security.md)
- [정책: 로깅](/Users/jeong-uyong/work/codex-playbook/docs/backend/policies/logging.md)
- [정책: 트랜잭션/정합성](/Users/jeong-uyong/work/codex-playbook/docs/backend/policies/transaction-and-consistency.md)
- [정책: 동시성/성능](/Users/jeong-uyong/work/codex-playbook/docs/backend/policies/concurrency-and-performance.md)
- [기술설계 문서 가이드](/Users/jeong-uyong/work/codex-playbook/docs/backend/design/README.md)
- [기술설계 샘플](/Users/jeong-uyong/work/codex-playbook/docs/backend/design/sample-tdd.md)

### Frontend

- [Getting Started](/Users/jeong-uyong/work/codex-playbook/docs/frontend/getting-started.md)
- [아키텍처 개요](/Users/jeong-uyong/work/codex-playbook/docs/frontend/architecture/frontend-architecture.md)
- [폴더 구조](/Users/jeong-uyong/work/codex-playbook/docs/frontend/architecture/folder-structure.md)
- [상태 관리](/Users/jeong-uyong/work/codex-playbook/docs/frontend/architecture/state-management.md)
- [코드 컨벤션](/Users/jeong-uyong/work/codex-playbook/docs/frontend/conventions/code-conventions.md)
- [네이밍 컨벤션](/Users/jeong-uyong/work/codex-playbook/docs/frontend/conventions/naming-conventions.md)
- [컴포넌트 컨벤션](/Users/jeong-uyong/work/codex-playbook/docs/frontend/conventions/component-conventions.md)
- [API 컨벤션](/Users/jeong-uyong/work/codex-playbook/docs/frontend/conventions/api-conventions.md)
- [렌더링 가이드](/Users/jeong-uyong/work/codex-playbook/docs/frontend/performance/rendering-guidelines.md)
- [캐싱 전략](/Users/jeong-uyong/work/codex-playbook/docs/frontend/performance/caching-strategy.md)
- [리스트 최적화](/Users/jeong-uyong/work/codex-playbook/docs/frontend/performance/list-optimization.md)
- [UI 원칙](/Users/jeong-uyong/work/codex-playbook/docs/frontend/ui-ux/ui-principles.md)
- [UX 가이드](/Users/jeong-uyong/work/codex-playbook/docs/frontend/ui-ux/ux-guidelines.md)
- [로딩/피드백](/Users/jeong-uyong/work/codex-playbook/docs/frontend/ui-ux/loading-and-feedback.md)
- [모달/다이얼로그 가이드](/Users/jeong-uyong/work/codex-playbook/docs/frontend/ui-ux/modal-dialog-guidelines.md)
