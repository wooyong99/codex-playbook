---
name: reverse-engineer-strategies
description: Analyze an existing backend codebase, infer the real implementation strategies used in each architecture layer, and generate `docs/backend/architecture/*/strategies/` documents that reflect the codebase's actual conventions. Use this when applying codex-playbook to a legacy Kotlin + Spring Boot backend, when `strategies/` folders are empty or generic, or when a user asks to reverse-engineer architecture strategy documents from existing code.
---

# Reverse Engineer Strategies

기존 백엔드 코드베이스를 읽어 각 아키텍처 레이어의 실제 구현 전략을 파악하고, `docs/backend/architecture/*/strategies/` 하위 문서를 생성하거나 갱신한다.

## 먼저 읽을 자료

- [references/layer-analysis-guide.md](references/layer-analysis-guide.md)
- [references/strategies-doc-templates.md](references/strategies-doc-templates.md)

## 작업 흐름

### 1. 입력 범위 확인

아래 항목을 먼저 정리한다.

- 분석 대상 코드베이스 경로
- 문서 출력 경로
- 분석할 레이어 범위
- 기존 `strategies/` 문서가 있을 때 병합할지 덮어쓸지

사용자가 경로를 생략하면 현재 작업 디렉토리를 기본값으로 본다.

### 2. 구조 탐색

- 먼저 대상 코드베이스가 **멀티 모듈인지 단일 모듈인지 식별**한다.
- 멀티 모듈이면 `settings.gradle.kts`, 각 모듈의 `build.gradle.kts`, `src/main` 구조를 읽어 **레이어별 모듈 후보**를 식별한다.
- 단일 모듈이면 `src/main/kotlin` 이하 패키지와 디렉토리 구조를 읽어 **레이어별 디렉토리 후보**를 식별한다.
- 이때 `domain`, `application`, `storage`, `external`, `app` 같은 플레이북 개념 레이어를 먼저 떠올리되, 실제 프로젝트가 쓰는 **로컬 레이어 이름과 경계**를 우선 기록한다.
- 플레이북에 적힌 예시 레이어명과 정확히 일치하지 않더라도, **실제 코드에서 드러나는 역할과 책임**을 기준으로 식별한 로컬 레이어를 플레이북의 개념 레이어에 매핑한다.
- 예를 들어 `app` 대신 `api`, `presentation`, `bootstrap`을 쓸 수 있고, `storage`와 `external`을 `infra` 또는 `infrastructure` 하위에 둘 수도 있다.
- 추측하지 말고 실제 클래스 역할, 어노테이션, 네이밍 패턴, 의존 방향을 근거로 판단한다.

### 3. 레이어별 역공학

- 역공학은 **고정된 폴더명 기준**이 아니라, 구조 탐색 단계에서 식별한 **프로젝트 로컬 레이어 맵**을 기준으로 수행한다.
- 먼저 프로젝트의 로컬 레이어를 플레이북의 개념 레이어에 매핑한다.
- 이때 매핑 기준은 **이름 유사성**이 아니라 **레이어의 역할, 책임, 의존 방향, 포함된 클래스 종류**다.
  - 예: `bootstrap` -> `app`
  - 예: `api` -> `app`
  - 예: `presentation` -> `app`
  - 예: `infra` -> `infrastructure`
  - 예: `infrastructure/storage` -> `storage`
  - 예: `infrastructure/external` -> `external`
- `infrastructure`처럼 상위 묶음 레이어가 있으면, 그 하위에서 `storage`, `external`, `messaging`, `security` 같은 하위 전략 단위를 다시 분리해 분석한다.
- 분석 순서는 보통 `domain -> application -> infrastructure 계열 -> app 계열`이 이해하기 쉽지만, 실제 프로젝트 의존 방향이 더 명확하면 그 순서를 따른다.

각 식별된 레이어 또는 하위 레이어에서 다음을 찾는다.

- 실제로 쓰이는 핵심 패턴
- 반복되는 클래스 역할과 네이밍
- 어노테이션, 베이스 클래스, 인터페이스 조합
- 예외 처리, 매핑, 트랜잭션, 외부 연동, 쿼리 방식 같은 구현 전략

레이어 이름이 플레이북과 다르더라도, 문서 생성 시에는

- 실제 프로젝트가 부르는 이름
- 플레이북 개념 레이어 중 어디에 대응되는지

를 함께 정리해서 독자가 매핑을 이해할 수 있게 한다.

### 4. 문서 생성 또는 갱신

- 각 레이어의 `strategies/README.md`는 항상 만든다.
- 세부 컨벤션 문서는 코드에서 패턴이 확인된 경우에만 만든다.
- 병합 모드라면 기존 문서의 커스터마이징된 설명은 보존하고, 비어 있거나 일반적인 부분만 갱신한다.
- 덮어쓰기 모드라면 기존 `strategies/` 문서를 기준 코드 분석 결과로 다시 작성한다.

### 5. 완료 전 검증

- 생성한 문서가 실제 코드 패턴과 연결되는지 샘플 클래스 기준으로 다시 확인한다.
- 코드에서 발견되지 않은 패턴 문서를 새로 만들지 않았는지 확인한다.
- 각 레이어 README에서 세부 문서 링크가 맞는지 확인한다.

## 작성 규칙

- 사실 기반으로만 쓴다. 추측 금지.
- "이 프로젝트는 보통 이럴 것" 같은 일반론 대신, "코드에서 확인된 패턴"만 적는다.
- 클래스명, 어노테이션, 폴더 구조, 인터페이스 관계 등 관찰 가능한 근거를 남긴다.
- 문서는 코드베이스에 맞는 설명이어야지, 플레이북 일반론의 복사본이 되면 안 된다.

## 언제 질문할지

아래 경우에는 문서 생성 전에 사용자에게 확인한다.

- 출력 경로 후보가 둘 이상이라 어느 쪽에 써야 할지 불명확할 때
- 특정 레이어가 혼재되어 있어 주 분석 단위를 모듈 기준으로 볼지 패키지 기준으로 볼지 애매할 때
- `infra`, `bootstrap`, `api`, `presentation`처럼 플레이북 표준 레이어명과 다른 이름이 많아 매핑 기준을 먼저 확인해야 할 때
- 레이어 이름은 다르지만 역할이 겹쳐 보여, 이름이 아니라 책임 기준으로 매핑해야 하는지 확인이 필요할 때
- 기존 `strategies/` 문서에 사람이 손으로 써둔 내용이 많아 병합/덮어쓰기 선택이 중요할 때
