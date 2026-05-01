# Domain Guidelines

이 문서는 `domain` 단위의 실제 코드 위치, 책임, 의존 경계, 구현 전략을 정리한다.

## 코드 위치

- `domain` module/package - 비즈니스 개념, 불변식, 도메인 행위, 도메인 예외를 담당한다.

## 책임

- 도메인 언어로 비즈니스 개념과 관계를 표현한다.
- 도메인 객체가 생성과 상태 변경을 스스로 통제해 잘못된 상태를 막는다.
- 비즈니스 규칙 위반을 도메인 소유 예외 계층으로 표현한다.

## 의존 경계

- depends on: 없음
- used by: `application`
- 금지되는 방향: Spring, JPA, Jackson, HTTP 개념, 인프라 모델 의존

## 핵심 원칙

- Domain은 외부 프레임워크에 의존하지 않는 순수 비즈니스 모델이어야 한다.
- 도메인 객체는 생성 경로와 상태 전이를 캡슐화해 불변식을 보호한다.
- 다른 도메인의 객체를 직접 포함하지 않고 ID 참조로 경계를 유지한다.

## 관련 정책

- [security](../../policies/security.md) - 민감 정보가 도메인에 들어오는 방식
- [transaction-and-consistency](../../policies/transaction-and-consistency.md) - 도메인 행위와 정합성 경계

## 금지 규칙

- Domain에서 `@Entity`, `@Component`, `@JsonProperty`, `HttpStatus` 같은 외부 타입을 import하지 않는다.
- 범용 `CommonErrorCode`로 여러 도메인의 예외를 뭉뚱그리지 않는다.
- 외부에서 도메인 불변식을 우회할 수 있는 public setter나 무의미한 생성자를 열어 두지 않는다.

## 안티패턴

- 도메인 상태 판단을 application의 if/else에 흩어 놓는다.
- DB 복원 경로와 신규 생성 경로가 같은 불변식을 무조건 재실행한다.
- 도메인 예외가 HTTP 상태나 메시지 포맷을 직접 소유한다.

## 주요 컴포넌트

- Entity: `{Entity}.kt`
- Value Object: `{ValueObject}.kt`
- State enum: `{Entity}Status.kt`
- ErrorCode: `{Domain}ErrorCode.kt`
- Base exception: `CoreException`

## 전략 문서

- [Strategies](./strategies/README.md)

## Playbook compatibility

- 이 단위는 기존 playbook의 `domain` 개념 계층과 동일하다.
- 실제 프로젝트에서 도메인 모듈이 bounded context별로 나뉘면 각 실제 모듈을 별도 architecture unit으로 분리한다.
