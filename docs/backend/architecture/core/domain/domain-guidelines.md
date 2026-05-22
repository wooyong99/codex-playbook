# Domain Guidelines

이 문서는 `backend/core/domain` 모듈의 실제 코드 위치, 책임, 의존 경계, 구현 전략을 정리한다.

## 코드 위치

- `backend/core/domain` - 비즈니스 개념, 불변식, 도메인 행위, 도메인 예외를 담당한다.

## 책임

- 도메인 언어로 비즈니스 개념과 관계를 표현한다.
- 도메인 객체가 생성과 상태 변경을 스스로 통제해 잘못된 상태를 막는다.
- 비즈니스 규칙 위반을 도메인 소유 예외 계층으로 표현한다.
- 외부 프레임워크, 저장소 모델, HTTP 표현 방식으로부터 비즈니스 규칙을 격리한다.

## 의존 경계

- depends on: 없음
- used by: `core/application`, infrastructure adapter
- 금지되는 방향: Spring, JPA, Jackson, HTTP 개념, infrastructure 모델 의존

## 핵심 원칙

- Domain은 외부 프레임워크에 의존하지 않는 순수 비즈니스 모델이어야 한다.
- 도메인 객체는 생성 경로와 상태 전이를 캡슐화해 불변식을 보호한다.
- 다른 도메인의 객체를 직접 포함하지 않고 ID 참조 또는 application 조합으로 경계를 유지한다.
- 도메인 예외는 HTTP 상태가 아니라 domain error code와 framework-independent error type으로 표현한다.

## 관련 정책

- [security](../../../policies/security.md) - 민감 정보가 도메인에 들어오는 방식
- [transaction-and-consistency](../../../policies/transaction-and-consistency.md) - 도메인 행위와 정합성 경계

## 금지 규칙

- Domain에서 `@Entity`, `@Component`, `@JsonProperty`, `HttpStatus` 같은 외부 타입을 import하지 않는다.
- 도메인 상태 판단을 application의 `if` / `else`에 흩어 놓지 않는다.
- DB 복원 경로와 신규 생성 경로가 같은 불변식을 무조건 재실행하게 만들지 않는다.
- 도메인 예외가 HTTP 상태나 응답 메시지 포맷을 직접 소유하지 않는다.
- 범용 `CommonErrorCode`로 여러 도메인의 예외를 뭉뚱그리지 않는다.
- 외부에서 도메인 불변식을 우회할 수 있는 public setter나 무의미한 생성자를 열어 두지 않는다.

## 주요 컴포넌트

- Entity: `{Entity}.kt`
- Value Object: `{ValueObject}.kt`
- State enum: `{Entity}Status.kt`
- ErrorCode: `{Domain}ErrorCode.kt`
- Base exception: `CoreException`

## 전략 문서

- [Strategies](./strategies/README.md)

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] 도메인 모델이 framework-independent 타입만 사용한다.
- [ ] 생성, 복원, 상태 변경 경로가 도메인 객체 내부 public 메서드로 제공되고 public setter로 우회되지 않는다.
- [ ] 도메인별 error code와 exception 경계가 app 계층 응답 처리와 분리되어 있다.
