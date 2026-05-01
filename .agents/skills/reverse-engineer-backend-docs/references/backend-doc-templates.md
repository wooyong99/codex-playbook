# Backend Doc Templates

실제 코드베이스 기반으로 `docs/backend` 하위 문서를 생성·갱신할 때 사용하는 최소 템플릿과 작성 규칙.

## 핵심 원칙

- 템플릿은 실제 코드에서 관찰한 사실을 담는 최소 구조로 사용한다.
- 각 문서는 하나의 소유권과 추상화 수준을 유지한다.
- 상위 문서는 안정적인 진입점만 연결하고, 세부 문서 목록은 가장 가까운 소유 문서가 관리한다.
- 같은 개념이 정책, 구현 아키텍처, 구현 전략, 설계 의도로 분리되면 각 관심사에 맞는 템플릿을 사용하고 링크로 연결한다.
- 규칙 원문은 한 문서에만 작성하고, 다른 문서는 링크와 해당 문맥에서의 적용 방식만 작성한다.
- 새 파일로 분리할 기준이 약하면 기존 소유 문서의 섹션으로 작성한다.

## 금지 규칙

- 코드에서 확인되지 않은 내용을 템플릿 placeholder에 채우지 않는다.
- 상위 README 템플릿에 하위 디렉토리의 세부 구현 문서나 전략 문서 목록을 직접 나열하지 않는다.
- `금지 규칙`과 `안티패턴`을 하나의 섹션으로 합쳐 작성하지 않는다.
- 정책 문서에 클래스 목록, 패키지 구조, 구현 절차, 모듈 의존 구조를 쓰지 않는다.
- architecture guideline이나 strategy 문서에 정책 원문을 재기술하지 않는다.
- 플레이북 개념 레이어명을 실제 코드 근거 없이 출력 디렉토리명이나 문서 단위명으로 사용하지 않는다.

## 안티패턴

- 문서 맵 과노출: 상위 README가 하위 세부 링크를 계속 직접 들고 있다.
- 이름만 분리된 중복 문서: 같은 규칙을 policy, guideline, strategy에 거의 같은 문장으로 반복한다.
- 추상화 수준 혼합: 전체 지도 문서에 클래스 수준 구현 근거를 쓰거나, strategy 문서에 전역 정책 원칙을 길게 쓴다.
- 전략 덤핑: `{actual-unit}-guidelines.md`에 반복 구현 방식과 체크리스트를 모두 넣고 `strategies/`를 비워둔다.
- 과도한 파일 분리: 소유자, 변경 주기, 독자, 추상화 수준이 같은 내용을 여러 파일로 쪼갠다.
- 낡은 내비게이션: 문서를 이동·삭제했지만 가장 가까운 `README.md` 문서 맵을 갱신하지 않는다.

## Backend README

`docs/backend/README.md`는 backend 문서 홈이다. 하위 세부 문서를 직접 모두 나열하지 않고 각 영역의 단일 진입점만 연결한다.

```md
# Backend

{프로젝트명} 백엔드 문서. 아키텍처, 정책, 설계 문서, 실행 안내로 구성된다.

## 문서 맵

| 영역 | 진입점 | 설명 |
|------|--------|------|
| 시작하기 | [getting-started.md](getting-started.md) | 기술 스택, 로컬 실행, 프로필 |
| 아키텍처 | [architecture/README.md](architecture/README.md) | 백엔드 아키텍처 단위, 의존 경계, 구현 전략 |
| 정책 | [policies/README.md](policies/README.md) | 모든 레이어에 걸쳐 적용되는 기술 정책 |
| 설계 문서 | [design/README.md](design/README.md) | 기술설계문서 목록과 예시 |

## 문서 경계

정책 원문은 `policies`, 실제 코드 구조는 `architecture`, 반복 구현 방식은 `architecture/{actual-unit}/strategies`가 소유한다.
```

## Getting Started

`docs/backend/getting-started.md`는 코드와 설정에서 확인한 실행 정보를 담는다. 확인되지 않은 값을 추측하지 않는다.

````md
# Backend Getting Started

## 기술 스택

- {코드에서 확인한 언어/프레임워크/DB}

## 로컬 실행

```bash
{확인된 실행 명령}
```

## 테스트

```bash
{확인된 테스트 명령}
```

## 프로필 / 환경 변수

| 항목 | 설명 | 근거 |
|------|------|------|
| `{ENV_NAME}` | {용도} | `{파일 경로}` |

## 확인 필요

- {코드에서 확인되지 않은 실행 조건}
````

## Policy README

`docs/backend/policies/README.md`는 전역 정책 문서 목록을 소유한다.

```md
# Backend Policies

백엔드 전 레이어에 공통 적용되는 크로스커팅 정책 문서 모음.

## 문서 목록

- [{policy}](./{policy}.md): {언제 읽는지}

## 운영 원칙

- 정책 문서를 추가/수정할 때 이 README의 문서 목록을 함께 갱신한다.
- 정책 문서는 전역 핵심 원칙, 금지 규칙, 안티패턴만 소유한다. 실제 코드 구조와 반복 구현 방식은 `docs/backend/architecture` 하위 문서에서 정책을 링크해 설명한다.
```

## Policy Detail

정책 문서는 모든 아키텍처 단위가 따라야 하는 전역 핵심 원칙, 금지 규칙, 안티패턴만 담는다.

```md
# {Policy Name} Policy

## 적용 범위

- {적용되는 코드 영역 또는 상황}

## 핵심 원칙

- {전역 원칙}

## 금지 규칙

- {절대 금지되는 전역 행동. 없으면 "없음"}

## 안티패턴

- {자주 발생하는 나쁜 사례. 없으면 "없음"}

## 코드 근거

- `{파일 또는 패키지}` - {정책을 도출한 관찰 근거}

## 관련 아키텍처 문서

- [architecture/{actual-unit}](../architecture/{actual-unit}/{actual-unit}-guidelines.md) - {정책을 구현하는 구조}
```

## Architecture README

`docs/backend/architecture/README.md`는 architecture 단일 진입점이자 실제 코드 구조의 전체 지도를 제공한다. 별도 `architecture-map.md`는 생성하지 않는다.

````md
# Backend Architecture

백엔드 아키텍처 문서의 단일 진입점.

## 아키텍처 단위

| 단위 | 코드 위치 | 주요 책임 | 의존 대상 | 사용 주체 |
|------|-----------|-----------|-----------|-----------|
| `{actual-unit}` | `{module/package}` | {책임 요약} | {depends on} | {used by} |

## 의존 방향

```text
{actual-unit-a} -> {actual-unit-b}
```

## 문서 구조

- [{actual-unit}](./{actual-unit}/{actual-unit}-guidelines.md) - {언제 읽는지}

## 관련 정책

- [policies/{policy}](../policies/{policy}.md) - {이 아키텍처 문서와 연결되는 전역 정책. 없으면 "없음"}

## 운영 원칙

- architecture 단위가 추가·삭제·개편되면 이 README를 먼저 갱신한다.
- 세부 전략 문서 목록은 각 단위의 `{actual-unit}-guidelines.md`와 `strategies/README.md`가 소유한다.
- 백엔드 문서 홈은 이 README만 참조하고, 아키텍처 단위 내부 세부 링크는 각 단위 문서가 소유한다.

## Playbook compatibility

- {필요할 때만 실제 구조와 플레이북 개념의 차이를 설명. 없으면 "없음"}
````

## Architecture Unit Guidelines

각 실제 아키텍처 단위의 본문 문서는 `{actual-unit}/{actual-unit}-guidelines.md` 구조를 따른다.

```md
# {Actual Unit Name} Guidelines

이 문서는 `{actual-unit}` 단위의 실제 코드 위치, 책임, 의존 경계, 구현 전략을 정리한다.

## 코드 위치

- `{module/package path}` - {역할}

## 책임

- {책임 1}
- {책임 2}

## 의존 경계

- depends on: {단위 목록}
- used by: {단위 목록}
- 금지되는 방향: {확인된 경우 작성}

## 핵심 원칙

- {이 단위가 반드시 유지해야 하는 설계 방향. 정책 원문을 재기술하지 말고 단위 관점의 적용 방향만 작성}

## 관련 정책

- [policies/{policy}](../../policies/{policy}.md) - {이 단위가 따라야 하는 전역 정책. 정책 원문은 재기술하지 않음}

## 금지 규칙

- {이 단위에서 절대 금지되는 의존, 호출, 데이터 접근, 트랜잭션 경계 침범 등. 없으면 "없음"}
- 근거: `{예시 클래스 또는 패키지}` - {관찰 근거. 없으면 "없음"}

## 안티패턴

- {이 단위에서 자주 발생하는 나쁜 구현 사례. 없으면 "없음"}
- 근거: `{예시 클래스 또는 패키지}` - {관찰 근거. 없으면 "없음"}

## 주요 컴포넌트

- {역할}: `{예시 클래스 또는 패키지}`

## 전략 문서

- [Strategies](./strategies/README.md)

## Playbook compatibility

- {필요할 때만 작성. 없으면 "없음"}
```

## Strategies README

각 실제 아키텍처 단위의 `strategies/README.md`는 아래 구조를 따른다.

```md
# {Actual Unit Name} Strategies

이 프로젝트에서 `{actual-unit}` 단위에 실제로 사용 중인 구현 전략 요약.

## 핵심 전략

- {전략 1}

## 근거가 된 코드 패턴

- `{클래스/패키지/어노테이션 근거}` - {관찰 내용}

## 세부 문서

- [{문서명}]({파일명}.md) - {언제 이 문서를 참고해야 하는지}
```

## Strategy Detail

반복 구현 패턴이 확인된 경우에만 세부 전략 문서를 만든다.

```md
# {Strategy Title}

이 문서는 `{actual-unit}` 단위에서 `{컴포넌트/패턴}`을 구현하는 실제 방식을 정리한다.

## 언제 사용하는가

- {사용 시점}

## 코드 위치

- `{경로}` - {역할}

## 구조

- {구성 요소 1}

## 핵심 원칙

- {이 전략이 반드시 지켜야 하는 구현 방향}

## 코드에서 관찰된 규칙

1. {규칙 1}

## 의존 및 책임 경계

- {허용되는 의존}
- {주의할 의존 또는 경계 조건}

## 관련 정책 / 상위 규칙

- [policies/{policy}](../../../policies/{policy}.md) - {이 전략과 연결되는 전역 정책. 없으면 "없음"}
- [{actual-unit} guidelines](../{actual-unit}-guidelines.md) - {이 전략이 따르는 상위 아키텍처 단위 규칙}

## 금지 규칙

- {이 전략에서 절대 금지되는 구현 방식. 없으면 "없음"}

## 안티패턴

- {이 전략에서 자주 발생하는 나쁜 구현 사례. 없으면 "없음"}

## 체크 리스트

- [ ] {검증 항목 1}

## 예시 코드

- `{저장소 상대 경로}` - {역할 설명}
```

## Design README

`docs/backend/design/README.md`는 실제 기술설계문서(TDD) 목록만 소유한다. TDD 작성 규칙 원문은 이 템플릿 문서가 소유하므로 `docs/backend/design` 아래 별도 작성 가이드 파일을 생성하지 않는다.

```md
# Design Documents (TDD)

기능·서브시스템의 기술설계문서 모음.

## 문서 목록

- [{tdd-file}](./{tdd-file}.md): {언제 읽는지}

## 운영 원칙

- TDD 파일 추가·삭제·이름 변경 시 이 README의 문서 목록을 함께 갱신한다.
- 상위 문서(예: `docs/backend/README.md`)는 개별 설계 파일이 아닌 이 README를 참조한다.
- 이 디렉토리는 실제 설계 문서만 소유한다. 작성 가이드 파일을 별도로 만들지 않는다.
```

## TDD Document

기능·서브시스템의 기술 설계 문서(Technical Design Document)는 아키텍처 판단 근거, 계층 분리, 트랜잭션 경계, 예외·실패 처리, 동시성·정합성, 확장 가능성 등 코드만으로는 읽히지 않는 설계 의도를 담는다.

작성 시점:

- 여러 도메인·모듈에 걸친 새 기능을 설계할 때
- 기존 기능의 중대한 구조 변경이 필요할 때
- 동시성·정합성·트랜잭션 경계에 비자명한 선택이 필요한 때
- 향후 유지보수·확장 시 결정의 맥락을 남겨야 할 때

단일 CRUD·단순 UseCase 추가에는 작성하지 않는다. 새 기능 구현 전 TDD 작성은 별도 TDD 작성 스킬의 책임이며, `$reverse-engineer-backend-docs`는 기존 코드의 설계 의도 문서화를 사용자가 요청한 경우에만 `docs/backend/design` 하위 문서를 작성한다.

파일명 규칙:

```text
tdd-<feature-slug>.md
```

예: `tdd-product-wishlist.md`, `tdd-payment-settlement.md`

````md
# {Feature/System} 기술설계문서 (TDD)

> 작성일: YYYY-MM-DD
> 상태: Draft | Reviewing | Approved | Superseded
> 대상 모듈: {module list}

## 1. 설계 배경 및 목적

### 1.1 배경

- {코드에서 확인한 문제 또는 설계 목적}

### 1.2 설계 목표

1. {목표 1}

### 1.3 설계 비목표

- {의도적으로 다루지 않는 범위}

### 1.4 기술적 제약사항

- {프레임워크, 모듈, 운영, 데이터 제약}

## 2. 현행 시스템 분석

### 2.1 관련 도메인 구조

```text
{ASCII 다이어그램}
```

### 2.2 현재 처리 흐름

1. {현재 흐름}

### 2.3 현행 스키마 분석

- `{schema/table}` - {역할 또는 한계}

## 3. 아키텍처 설계

### 3.1 계층별 책임 분배

| 계층 | 구성 요소 | 책임 | 설계 근거 |
|------|-----------|------|-----------|
| {layer} | `{component}` | {responsibility} | {reason} |

### 3.2 처리 흐름

1. {처리 단계 또는 의사코드}

### 3.3 설계 대안 분석

| 대안 | 장점 | 단점 | 채택 여부 | 사유 |
|------|------|------|-----------|------|
| {alternative} | {pros} | {cons} | {selected?} | {reason} |

## 4. 도메인 모델 설계

### 4.1 애그리거트 경계

- {aggregate} - {boundary reason}

### 4.2 도메인 모델 상세

- {aggregate/entity}: 역할, 불변식, 주요 행위, 상태 전이

### 4.3 데이터 스키마 설계

```sql
-- {DDL snippet}
```

### 4.4 데이터 변환 흐름

```text
HTTP -> DTO -> Command -> Domain -> Entity -> DB
```

## 5. 트랜잭션 설계

### 5.1 트랜잭션 경계

| 연산 | 시작점 | 범위 | 격리 수준 | 사유 |
|------|--------|------|-----------|------|
| {operation} | `{entry}` | {scope} | {isolation} | {reason} |

### 5.2 정합성 보장 전략

- {consistency strategy}

### 5.3 이벤트 처리

- {event strategy}

## 6. 예외 및 실패 처리

### 6.1 예외 분류

| 예외 유형 | ErrorCode | 발생 조건 | HTTP 상태 | 사용자 메시지 |
|-----------|-----------|-----------|-----------|---------------|
| {type} | `{code}` | {condition} | {status} | {message} |

### 6.2 실패 시나리오 및 복구 전략

| 시나리오 | 발생 가능성 | 영향 | 복구 |
|----------|-------------|------|------|
| {scenario} | {probability} | {impact} | {recovery} |

### 6.3 멱등성 보장

- {idempotency strategy}

## 7. 동시성 및 성능

### 7.1 동시성 제어

- {경합 지점}: {제어 방식}

### 7.2 성능 고려사항

- {performance consideration}

### 7.3 확장 가능성

- 열어둔 포인트: {extension point}
- 의도적으로 닫아둔 제약: {closed constraint}

## 8. 변경 파일 목록

| 파일 경로 | 모듈 | 변경 유형 | 설명 |
|-----------|------|-----------|------|
| `{path}` | {module} | 신규/수정 | {description} |

## 9. 검증 계획

| 시나리오 | 테스트 유형 | 검증 내용 | 예상 결과 |
|----------|-------------|-----------|-----------|
| {scenario} | 단위/통합 | {verification} | {expected} |

## 부록

- {요청/응답 예시, 추가 다이어그램, 외부 인용 등}
````

검토 에이전트의 취급:

- `architecture-reviewer`는 `docs/backend/design`을 Source of Truth에서 제외한다.
- 설계 의도는 참고하되 준수 규칙으로 강제하지 않는다.
- 강제할 규칙은 `architecture/*` 또는 `policies/*`에 규정으로 승격한다.
