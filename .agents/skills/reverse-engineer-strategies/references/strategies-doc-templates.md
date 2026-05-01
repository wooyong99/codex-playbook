# Architecture Strategy Doc Templates

실제 코드베이스 기반으로 `docs/backend/architecture` 하위 문서를 생성할 때 사용하는 최소 템플릿과 작성 규칙.

## 목차

- [1. Architecture README](#1-architecture-readme)
- [2. Architecture Unit README](#2-architecture-unit-readme)
- [3. Strategies README](#3-strategies-readme)
- [4. Strategy Detail](#4-strategy-detail)
- [5. 문서 생성 조건](#5-문서-생성-조건)
- [6. 작성 원칙](#6-작성-원칙)

## 1. Architecture README

`docs/backend/architecture/README.md`는 architecture 단일 진입점이자 실제 코드 구조의 전체 지도를 제공한다. 별도 `architecture-map.md`는 생성하지 않는다.

````md
# Backend Architecture

백엔드 아키텍처 문서의 단일 진입점.

이 문서는 현재 코드베이스에서 확인한 실제 아키텍처 단위, 코드 위치, 책임, 의존 방향, 하위 문서 링크를 요약한다.

## 언제 읽을지

- {이 문서를 읽어야 하는 상황}

## 아키텍처 단위

| 단위 | 코드 위치 | 주요 책임 | 의존 대상 | 사용 주체 |
|------|-----------|-----------|-----------|-----------|
| `{actual-unit}` | `{module/package}` | {책임 요약} | {depends on} | {used by} |

## 의존 방향

```text
{actual-unit-a} -> {actual-unit-b}
```

## 문서 구조

- [{actual-unit}](./{actual-unit}/README.md) - {언제 읽는지}

## 운영 원칙

- architecture 하위 디렉토리나 전략 문서가 추가·삭제·개편되면 이 README를 먼저 갱신한다.
- 백엔드 문서 홈은 이 README만 참조하고, 아키텍처 내부 세부 링크는 이 README가 소유한다.

## Playbook compatibility

- {필요할 때만 실제 구조와 플레이북 개념의 차이를 설명. 없으면 "없음"}
````

## 2. Architecture Unit README

각 실제 아키텍처 단위의 `README.md`는 아래 구조를 따른다.

```md
# {Actual Unit Name}

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

## 주요 컴포넌트

- {역할}: `{예시 클래스 또는 패키지}`

## 전략 문서

- [Strategies](./strategies/README.md)

## Playbook compatibility

- {필요할 때만 작성. 없으면 "없음"}
```

## 3. Strategies README

각 실제 아키텍처 단위의 `strategies/README.md`는 아래 구조를 따른다.

```md
# {Actual Unit Name} Strategies

이 프로젝트에서 `{actual-unit}` 단위에 실제로 사용 중인 구현 전략 요약.

## 핵심 전략

- {전략 1}
- {전략 2}

## 근거가 된 코드 패턴

- `{클래스/패키지/어노테이션 근거}` - {관찰 내용}

## 세부 문서

- [{문서명}]({파일명}.md) - {언제 이 문서를 참고해야 하는지}
```

## 4. Strategy Detail

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
- {구성 요소 2}

## 코드에서 관찰된 규칙

1. {규칙 1}
2. {규칙 2}
3. {규칙 3}

## 의존 및 책임 경계

- {허용되는 의존}
- {금지되거나 주의할 의존}

## 금지 사항 / 안티패턴

- {금지 사항 1}
- {안티패턴 1}

## 체크 리스트

- [ ] {검증 항목 1}
- [ ] {검증 항목 2}

## 예시 코드

- `{저장소 상대 경로}` - {역할 설명}
```

## 5. 문서 생성 조건

기본 원칙:

- 문서 단위와 디렉토리명은 실제 코드의 아키텍처 단위명을 우선한다.
- 세부 전략 문서는 코드에서 해당 패턴이 실제로 보일 때만 만든다.
- 플레이북 예시 목록에 있다는 이유만으로 문서를 만들지 않는다.
- 기존 문서가 실제 코드 구조와 맞지 않으면 `generate`로 문서를 추가하지 말고 `migrate` 계획을 먼저 제시한다.
- 아래 목록에 없는 패턴이라도, 기존 코드베이스에서 반복적으로 사용되는 새로운 구현 패턴이 확인되면 그 패턴에 맞는 전략 문서를 추가한다.

모드별 생성 규칙:

- `inspect`: 아래 템플릿을 적용할 문서 계획만 제안하고 파일은 수정하지 않는다.
- `generate`: 기존 문서가 없거나 충돌하지 않을 때만 아래 템플릿으로 새 문서를 생성한다. 충돌하면 아무 파일도 쓰지 않는다.
- `migrate`: 기존 문서를 `keep`, `merge`, `migrate`, `remove`, `archive` 후보로 나눈 뒤 실제 코드 기반 구조로 재작성한다.
- `merge`: 기존 문서의 제목과 구조를 가능한 한 유지하되, 실제 코드 근거와 누락된 전략 링크를 보강한다.

세부 문서로 만들 수 있는 패턴 예시:

- API endpoint/request/response 전략
- UseCase 또는 service orchestration 전략
- domain model/state transition 전략
- persistence adapter/repository 전략
- query builder 또는 custom query 전략
- external client/adapter 전략
- event handler/messaging 전략
- batch/scheduler 전략
- security/authentication 전략
- error code/exception mapping 전략
- transaction boundary 전략
- test fixture/test style 전략

새 패턴 문서화 규칙:

- 새 문서 이름은 해당 패턴의 책임이 드러나게 짓는다.
- README에는 새로 발견한 문서를 연결한다.
- 단발성 구현이나 한두 클래스에만 우연히 보이는 패턴은 새 문서로 만들지 않는다.
- 여러 클래스/모듈에서 반복되고, 팀의 구현 전략으로 볼 수 있을 때만 새 문서를 만든다.

## 6. 작성 원칙

- 일반적인 아키텍처 교과서 설명을 쓰지 않는다.
- 실제 클래스명, 패키지 구조, 어노테이션, 구현 방식 같은 관찰 결과를 중심으로 쓴다.
- 근거가 약한 내용은 문서에서 제외한다.
- 코드에서 더 이상 보이지 않는 패턴 문서는 병합 모드에서도 제거 후보로 본다.
- 플레이북 개념 레이어는 필요할 때만 `Playbook compatibility` 섹션에 보조 정보로 기록한다.
- architecture 하위 디렉토리 추가·삭제·개편이 있으면 `docs/backend/architecture/README.md`를 갱신한다. `docs/backend/README.md`와 `AGENTS.md`는 각각 architecture 진입점 또는 최상위 Backend 문서 홈 경로가 바뀔 때만 갱신한다.
