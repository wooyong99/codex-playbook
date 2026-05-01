# Backend Doc Templates

실제 코드베이스 기반으로 `docs/backend` 하위 문서를 생성·갱신할 때 사용하는 최소 템플릿과 작성 규칙.

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
| 설계 문서 | [design/README.md](design/README.md) | 기술설계문서 작성 규칙과 예시 |

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
- 정책 문서는 전역 원칙과 금지 규칙만 소유한다. 실제 코드 구조와 반복 구현 방식은 `docs/backend/architecture` 하위 문서에서 정책을 링크해 설명한다.
```

## Policy Detail

정책 문서는 모든 아키텍처 단위가 따라야 하는 원칙과 금지 규칙만 담는다.

```md
# {Policy Name} Policy

## 적용 범위

- {적용되는 코드 영역 또는 상황}

## 핵심 원칙

- {전역 원칙}

## 금지 규칙 / 안티패턴

- {금지 규칙}

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

- architecture 하위 디렉토리나 전략 문서가 추가·삭제·개편되면 이 README를 먼저 갱신한다.
- 백엔드 문서 홈은 이 README만 참조하고, 아키텍처 내부 세부 링크는 이 README가 소유한다.

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

## 관련 정책

- [policies/{policy}](../../policies/{policy}.md) - {이 단위가 따라야 하는 전역 정책. 정책 원문은 재기술하지 않음}

## 금지 규칙 / 안티패턴

- 금지 규칙: {이 단위에서 금지되는 의존, 호출, 데이터 접근, 트랜잭션 경계 침범 등}
- 안티패턴: {반복해서 피해야 할 구현 방식. 없으면 "없음"}
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

## 코드에서 관찰된 규칙

1. {규칙 1}

## 의존 및 책임 경계

- {허용되는 의존}
- {금지되거나 주의할 의존}

## 관련 정책 / 상위 규칙

- [policies/{policy}](../../../policies/{policy}.md) - {이 전략과 연결되는 전역 정책. 없으면 "없음"}
- [{actual-unit} guidelines](../{actual-unit}-guidelines.md) - {이 전략이 따르는 상위 아키텍처 단위 규칙}

## 금지 사항 / 안티패턴

- {금지 사항 1}

## 체크 리스트

- [ ] {검증 항목 1}

## 예시 코드

- `{저장소 상대 경로}` - {역할 설명}
```

## Design Note

기존 코드의 설계 의도 문서화를 사용자가 요청한 경우에만 `docs/backend/design` 하위에 작성한다. 새 기능 구현 전 TDD 작성은 별도 TDD 작성 스킬의 책임이다.

```md
# {Feature/System} Design Note

## 배경

- {코드에서 확인한 문제 또는 설계 목적}

## 현재 구조

- `{코드 위치}` - {역할}

## 주요 결정

- {결정}: {코드 근거}

## 관련 문서

- [architecture/{actual-unit}](../architecture/{actual-unit}/{actual-unit}-guidelines.md)
- [policies/{policy}](../policies/{policy}.md)
```

## 작성 원칙

- 일반적인 아키텍처 교과서 설명을 쓰지 않는다.
- 실제 클래스명, 패키지 구조, 어노테이션, 구현 방식 같은 관찰 결과를 중심으로 쓴다.
- 근거가 약한 내용은 문서에서 제외한다.
- 코드에서 더 이상 보이지 않는 패턴 문서는 병합 모드에서도 제거 후보로 본다.
- 정책, 구현 아키텍처, 구현 전략에 걸친 같은 규칙을 중복 서술하지 않는다.
