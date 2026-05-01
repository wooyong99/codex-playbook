---
name: reverse-engineer-strategies
description: Analyze an existing backend codebase, infer its real architecture units, dependency boundaries, and implementation strategies, then create or migrate `docs/backend/architecture` documents so they mirror the actual codebase rather than forcing codex-playbook concept layers. Use when applying codex-playbook to a legacy Kotlin + Spring Boot backend, when architecture docs are empty/generic/misaligned with code, or when a user asks to reverse-engineer backend architecture or strategy documents from existing code.
---

# Reverse Engineer Strategies

기존 백엔드 코드베이스를 읽어 실제 아키텍처 단위, 의존 경계, 구현 전략을 파악하고, `docs/backend/architecture` 하위 문서를 실제 코드 구조에 맞게 생성·갱신·이전한다.

## 먼저 읽을 자료

- [references/layer-analysis-guide.md](references/layer-analysis-guide.md)
- [references/strategies-doc-templates.md](references/strategies-doc-templates.md)

## 작업 흐름

### 1. 입력 범위 확인

아래 항목을 먼저 정리한다.

- 분석 대상 코드베이스 경로
- 문서 출력 경로
- 실행 모드: `inspect`, `generate`, `migrate`, `merge` 중 하나
- 분석할 모듈·패키지·아키텍처 단위 범위
- 기존 `docs/backend/architecture` 문서를 보존·병합·이전할지

사용자가 경로를 생략하면 현재 작업 디렉토리를 기본값으로 본다. 실행 모드를 생략하면 먼저 `inspect`로 구조와 문서화 계획을 제안한 뒤, 문서 변경이 필요한 경우 사용자의 진행 의사를 확인한다.

모든 실행 모드는 먼저 `inspect` 수준의 사전 판단을 수행한다. 즉, 코드 구조와 기존 `docs/backend/architecture` 상태를 확인하지 않은 채 파일을 생성·수정·삭제하지 않는다.

### 2. 구조 탐색

- 먼저 대상 코드베이스가 **멀티 모듈인지 단일 모듈인지 식별**한다.
- 멀티 모듈이면 `settings.gradle.kts`, 각 모듈의 `build.gradle.kts`, 모듈 간 의존 관계, `src/main` 구조를 읽어 **실제 아키텍처 단위 후보**를 식별한다.
- 단일 모듈이면 `src/main/kotlin` 이하 패키지와 디렉토리 구조, 패키지 간 의존 방향, 클래스 역할을 읽어 **실제 아키텍처 단위 후보**를 식별한다.
- 단위 이름은 코드베이스가 실제로 쓰는 이름을 우선한다. 예: `admin`, `api`, `core`, `groupware-backend`, `infrastructure`, `batch`, `notification`.
- `domain`, `application`, `storage`, `external`, `app` 같은 플레이북 개념 레이어는 출력 구조를 정하는 기준이 아니라, 필요한 경우 호환성 메모로만 사용한다.
- 추측하지 말고 실제 모듈명, 패키지명, 클래스 역할, 어노테이션, 네이밍 패턴, 의존 방향을 근거로 판단한다.

### 3. 아키텍처 단위별 역공학

- 역공학은 **플레이북 폴더명 기준**이 아니라, 구조 탐색 단계에서 식별한 **실제 아키텍처 단위 맵**을 기준으로 수행한다.
- 각 단위의 이름, 코드 위치, 책임, 포함 컴포넌트, 외부에 노출하는 계약, 의존 방향을 먼저 정리한다.
- `infrastructure`처럼 상위 묶음 단위가 있으면, 코드에서 확인되는 하위 책임 단위(`persistence`, `client`, `messaging`, `security`, `config` 등)로 다시 나눠 분석한다.
- 분석 순서는 실제 의존 방향을 따른다. 의존 방향이 불명확하면 가장 독립적인 단위에서 시작해 진입점 단위로 이동한다.

각 식별된 아키텍처 단위 또는 하위 책임 단위에서 다음을 찾는다.

- 실제로 쓰이는 핵심 패턴
- 반복되는 클래스 역할과 네이밍
- 어노테이션, 베이스 클래스, 인터페이스 조합
- 예외 처리, 매핑, 트랜잭션, 외부 연동, 쿼리 방식, 설정 방식 같은 구현 전략
- 다른 단위가 이 단위를 사용하는 방식과 금지해야 할 의존 방향

플레이북 개념 레이어와의 관계는 문서 구조가 아니라 보조 메모로만 남긴다.

- 예: `Playbook compatibility: 이 단위는 app/application 성격을 함께 가진다.`
- 예: `Playbook compatibility: 직접 대응 없음. 프로젝트 고유의 batch 단위다.`

### 4. 문서 생성 또는 갱신

실행 모드별로 처리한다.

- `inspect`: 파일을 수정하지 않는 분석 모드다. 코드 구조, 실제 아키텍처 단위 맵, 기존 문서 상태, 제안 문서 구조, 보존·이전·삭제 후보, 추천 후속 모드를 보고한다.
- `generate`: 비어 있거나 충돌 없는 `docs/backend/architecture`에 실제 코드 기반 문서를 안전하게 추가 생성한다. 기존 문서가 실제 코드 구조와 충돌하면 파일을 쓰지 않고 중단한 뒤 `migrate`를 제안한다.
- `migrate`: 기존 architecture 문서 체계를 실제 코드 기반 체계로 교체한다. 기존 문서를 유지·이전·삭제 후보로 분류하고, 플레이북 개념 레이어 중심 문서가 실제 코드와 맞지 않으면 active architecture tree에서 제거하거나 active path 밖으로 이전한다. 큰 구조 변경 전에는 계획을 먼저 제시한다.
- `merge`: 기존 문서 체계를 유지하면서 실제 코드 근거를 덧입힌다. 기존 구조가 실제 코드와 크게 충돌하지 않을 때만 사용하고, 사람이 작성한 설명은 보존하며, 비어 있거나 일반론인 부분만 보강한다.

모드 선택 규칙:

```text
항상 inspect 수준의 사전 판단 수행
→ docs/backend/architecture 없음/placeholder 수준
  → generate

→ 기존 문서가 실제 코드 구조와 대체로 일치
  → merge

→ 기존 문서가 플레이북 개념 레이어 중심이고 실제 코드 구조와 충돌
  → migrate

→ 판단이 애매하거나 삭제/이전 영향이 큼
  → 사용자 확인 후 migrate 또는 merge
```

`generate`는 충돌을 만들지 않는다. 기존 architecture 구조가 새 실제 코드 구조와 충돌하면 no-op으로 멈추고 `migrate`를 제안한다. `migrate`만 active architecture tree의 제거·이전·재구성을 수행한다.

문서 구조는 실제 코드 이름을 우선한다.

```text
docs/backend/architecture/
├── README.md
├── architecture-map.md
├── {actual-unit}/
│   ├── README.md
│   └── strategies/
│       ├── README.md
│       └── {observed-pattern}.md
└── {another-actual-unit}/
    └── ...
```

세부 전략 문서는 코드에서 반복 패턴이 확인된 경우에만 만든다. architecture 하위 디렉토리를 추가·삭제·개편하면 먼저 `docs/backend/architecture/README.md`를 갱신한다. `docs/backend/README.md`는 architecture 진입점 경로가 바뀔 때만 갱신하고, `AGENTS.md`는 최상위 Backend 문서 홈 경로가 바뀔 때만 갱신한다.

### 5. 완료 전 검증

- 생성한 문서가 실제 코드 패턴과 연결되는지 샘플 클래스 기준으로 다시 확인한다.
- 코드에서 발견되지 않은 패턴 문서를 새로 만들지 않았는지 확인한다.
- 각 아키텍처 단위 README에서 세부 문서 링크가 맞는지 확인한다.
- `architecture-map.md`가 실제 모듈·패키지·의존 방향과 어긋나지 않는지 확인한다.
- 문서 맵 갱신이 필요한 경우 누락되지 않았는지 확인한다.

## 작성 규칙

- 사실 기반으로만 쓴다. 추측 금지.
- "이 프로젝트는 보통 이럴 것" 같은 일반론 대신, "코드에서 확인된 패턴"만 적는다.
- 클래스명, 어노테이션, 폴더 구조, 인터페이스 관계 등 관찰 가능한 근거를 남긴다.
- 문서는 코드베이스에 맞는 설명이어야지, 플레이북 일반론이나 개념 레이어 구조의 복사본이 되면 안 된다.
- 플레이북 개념 레이어명은 출력 디렉토리명을 정하는 기본값으로 쓰지 않는다.

## 언제 질문할지

아래 경우에는 문서 생성 전에 사용자에게 확인한다.

- 출력 경로 후보가 둘 이상이라 어느 쪽에 써야 할지 불명확할 때
- 특정 아키텍처 단위가 혼재되어 있어 주 분석 단위를 모듈 기준으로 볼지 패키지 기준으로 볼지 애매할 때
- 실제 코드 단위명이 문서 디렉토리명으로 쓰기에 너무 구현 세부적이거나 임시적일 때
- 기존 `docs/backend/architecture` 구조를 유지할지 실제 코드 구조로 이전할지 선택이 필요할 때
- 기존 문서에 사람이 손으로 써둔 내용이 많아 병합/이전/삭제 후보 판단이 중요할 때
- 새 구조 적용이 최상위 Backend 문서 홈 경로 변경까지 요구할 때
