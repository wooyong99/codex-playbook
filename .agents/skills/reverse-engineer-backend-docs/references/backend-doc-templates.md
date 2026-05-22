# Backend Doc Templates

이 문서는 실제 코드베이스 기반으로 `docs/backend` 하위 문서를 생성·갱신할 때 사용하는 파일별 템플릿과 완료 전 검증 기준이다. 문서 위치 판단은 [backend-document-routing.md](backend-document-routing.md)가 소유하고, 이 문서는 파일을 실제로 작성할 때의 구조를 소유한다.

## 문서 역할

이 문서는 선택된 `docs/backend` 문서를 실제로 작성할 때의 섹션 구조와 완료 전 검증 기준만 소유한다.

- 코드 분석과 confidence 판단은 [codebase-analysis-guide.md](codebase-analysis-guide.md)가 소유한다.
- 문서 위치와 소유권 라우팅은 [backend-document-routing.md](backend-document-routing.md)가 소유한다.
- 이 문서의 템플릿은 코드 근거를 정리하는 구조이며, 확인되지 않은 내용을 채우는 근거가 아니다.
- 새 문서 생성 여부나 기존 문서 삭제·이전 판단을 이 문서에서 결정하지 않는다.

## 파일 작성 기준

템플릿은 실제 코드에서 관찰한 사실을 담는 최소 구조로 사용한다. 문서 위치와 소유권 판단은 [backend-document-routing.md](backend-document-routing.md)를 먼저 따르고, 이 문서에서는 선택된 파일에 어떤 섹션을 둘지만 결정한다.

공통 작성 방식:

- 확인되지 않은 내용은 placeholder에 채우지 않고 "확인 필요" 또는 "없음"으로 명시한다.
- 코드 근거가 필요한 섹션에는 파일, 패키지, 클래스, 설정 경로 중 하나 이상을 남긴다.
- 템플릿 섹션이 현재 코드에 맞지 않으면 억지로 채우지 않고 생략하거나 "없음"으로 둔다.
- `금지 규칙`과 `안티패턴`은 필요한 경우 별도 섹션으로 둔다.
- 새 문서를 추가하거나 이름을 바꾸면 가장 가까운 `README.md`의 문서 목록도 함께 갱신한다.

공통 체크리스트:

규칙, 정책, 전략, 설계 판단을 담는 `docs/backend` 하위 문서는 마지막에 `## 체크리스트`를 둔다. 단순 문서 맵만 소유하는 README는 `운영 원칙`이 같은 역할을 하면 별도 체크리스트를 생략할 수 있다.

```md
## 체크리스트

- [ ] 문서의 목적, 적용 범위, 소유 경계가 상단에 드러난다.
- [ ] 규칙, 패턴, 설계 판단은 코드 근거 또는 "확인 필요" 표기를 가진다.
- [ ] 이 문서가 소유하지 않는 정책, 전략, 설계 원문은 링크로 연결했다.
- [ ] 하위 문서 추가·삭제·이름 변경이 가장 가까운 `README.md` 문서 맵에 반영되었다.
```

## 템플릿 목록

| 문서 | 위치 | 사용 시점 |
|------|------|-----------|
| Backend README | `docs/backend/README.md` | backend 문서 홈을 만들거나 영역 진입점이 바뀔 때 |
| Getting Started | `docs/backend/getting-started.md` | 실행·빌드·테스트 정보를 코드와 설정에서 확인했을 때 |
| Policy README | `docs/backend/policies/README.md` | 정책 문서 목록이 추가·삭제·변경될 때 |
| Policy Detail | `docs/backend/policies/{policy}.md` | 여러 아키텍처 단위에 적용되는 전역 정책을 문서화할 때 |
| Architecture README | `docs/backend/architecture/README.md` | 실제 아키텍처 단위 맵을 만들거나 갱신할 때 |
| Architecture Unit Guidelines | `docs/backend/architecture/{actual-unit}/{actual-unit}-guidelines.md` | 특정 실제 코드 단위의 책임과 의존 경계를 정리할 때 |
| Strategies README | `docs/backend/architecture/{actual-unit}/strategies/README.md` | 해당 단위의 전략 문서 목록을 관리할 때 |
| Strategy Detail | `docs/backend/architecture/{actual-unit}/strategies/{pattern}.md` | 반복 구현 패턴이 확인되었을 때 |
| Design README | `docs/backend/design/README.md` | 기술설계문서 목록을 관리할 때 |
| TDD Document | `docs/backend/design/tdd-{feature}.md` | 사용자가 기존 기능의 설계 의도 문서화를 요청했을 때 |

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
| 설계 문서 | [design/README.md](design/README.md) | 기술설계문서 목록 |

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

- {전략 1} - {권장 주류|상황별 변형|레거시 허용|충돌/확인 필요}

## 전략 지도

| 전략 | 상태 | confidence | 적용 범위 | 대표 근거 | 세부 문서 |
|------|------|------------|-----------|-----------|-----------|
| {전략명} | {권장 주류|상황별 변형|레거시 허용|충돌/확인 필요} | {High|Medium|Low} | {적용 범위} | `{경로}` | [{문서명}]({파일명}.md) 또는 README only/확인 필요 |

## 근거가 된 코드 패턴

- `{클래스/패키지/어노테이션 근거}` - {관찰 내용}

## 분석 범위

- included: `{샘플링한 모듈/패키지}`
- excluded: `{제외한 generated/vendor/build/fixture 등. 없으면 "없음"}`
- coverage/confidence: {High|Medium|Low} - {이유}

## 레거시 / 혼재 구간

- {레거시 또는 상충 패턴이 있으면 적용 범위와 주의점. 없으면 "없음"}

## 세부 문서

- [{문서명}]({파일명}.md) - {언제 이 문서를 참고해야 하는지}

## 후속 후보

- {세부 문서로 승격하지 않은 Medium/Low confidence 후보와 이유. 없으면 "없음"}
```

## Strategy Detail

반복 구현 패턴이 확인된 경우에만 세부 전략 문서를 만든다.

```md
# {Strategy Title}

이 문서는 `{actual-unit}` 단위에서 `{컴포넌트/패턴}`을 구현하는 실제 방식을 정리한다.

## 언제 사용하는가

- {사용 시점}

## 적용 범위와 상태

- 상태: {권장 주류|상황별 변형|레거시 허용|충돌/확인 필요}
- 적용 범위: {새 기능 전체|특정 업무 흐름|특정 adapter|레거시 패키지 등}
- 새 코드 적용 여부: {따른다|조건부로 따른다|새 코드에는 적용하지 않는다|확인 필요}
- confidence: {High|Medium|Low} - {근거 폭과 한계}

## 코드 위치

- `{경로}` - {역할}

## 분석 범위

- included: `{읽은 대표 경로}`
- excluded: `{제외한 generated/vendor/build/fixture 등. 없으면 "없음"}`
- sampled but not generalized: `{봤지만 규칙화하지 않은 경로. 없으면 "없음"}`

## 대표 흐름

1. {흐름 1}

## 구조 / 구성 요소

- {구성 요소 1}

## 핵심 원칙

- {이 전략이 반드시 지켜야 하는 구현 방향}

## 코드에서 관찰된 규칙

1. {규칙 1}
   - 근거: `{경로}` - {관찰 내용}

## 변형과 예외

- {상황별 변형 또는 예외 흐름. 없으면 "없음"}

## 레거시 / 혼재 구간

- {레거시로 남아 있는 구현 방식, 공존 이유, 새 코드 적용 여부. 없으면 "없음"}

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

## 체크리스트

- [ ] 적용 범위, 상태, confidence가 실제 코드 근거와 일치한다.
- [ ] 대표 흐름과 규칙이 한 업무 예시를 전체 규칙으로 과도하게 일반화하지 않는다.
- [ ] 변형, 예외, 레거시/혼재 구간이 확인된 만큼 기록되어 있다.
- [ ] 관련 정책과 상위 guideline을 중복 서술하지 않고 링크로 연결했다.

## 예시 코드

- `{저장소 상대 경로}` - {역할 설명}

## 확인 필요

- {코드만으로 우선순위나 의도를 판단하기 어려운 항목. 없으면 "없음"}
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

## 10. 완료 체크리스트

- [ ] 설계 배경과 목표가 코드에서 관찰한 현재 구조와 연결된다.
- [ ] 아키텍처, 도메인, 트랜잭션, 예외, 동시성 판단에 근거가 있다.
- [ ] 새 규칙으로 강제해야 할 내용은 `architecture` 또는 `policies` 문서 승격 후보로 분리했다.
- [ ] TDD 파일 추가·삭제·이름 변경이 `docs/backend/design/README.md`에 반영되었다.

## 부록

- {요청/응답 예시, 추가 다이어그램, 외부 인용 등}
````

검토 에이전트의 취급:

- `backend-architecture-reviewer`는 `docs/backend/design`을 Source of Truth에서 제외한다.
- 설계 의도는 참고하되 준수 규칙으로 강제하지 않는다.
- 강제할 규칙은 `architecture/*` 또는 `policies/*`에 규정으로 승격한다.

## 완료 전 검증

문서 작성 후에는 아래 항목을 확인한다.

- 생성·수정한 문서가 실제 코드 패턴과 연결되는지 샘플 클래스 기준으로 확인했다.
- 코드에서 발견되지 않은 패턴, 정책, 실행 방법을 새로 만들지 않았다.
- strategy 문서가 적용 범위, 상태, 반복 근거, 변형, 예외, 레거시/혼재 구간을 필요한 만큼 기록한다.
- 대형 코드베이스의 strategy 문서가 included/excluded 범위와 confidence를 기록한다.
- strategy 문서가 한 업무 영역의 단일 예시를 전체 규칙으로 과도하게 일반화하지 않는다.
- `docs/backend/README.md`가 backend 하위 영역의 단일 진입점만 참조한다.
- `docs/backend/architecture/README.md`의 아키텍처 맵이 실제 모듈·패키지·의존 방향과 어긋나지 않는다.
- `docs/backend/architecture/README.md`가 단위 guideline 링크까지만 소유하고, 단위 내부 전략 목록을 직접 나열하지 않는다.
- 정책, 구현 아키텍처, 구현 전략 사이에 같은 규칙이 중복 서술되지 않고 링크로 연결된다.
- 각 문서가 하나의 추상화 수준과 관심사를 유지한다.
- 하위 디렉토리의 문서가 추가·삭제·개편되면 가장 가까운 `README.md` 문서 맵이 갱신되었다.
