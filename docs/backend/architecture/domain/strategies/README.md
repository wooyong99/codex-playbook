# Domain Strategies

이 프로젝트에서 `domain` 단위에 실제로 사용 중인 구현 전략 요약.

## 핵심 전략

- 도메인 모델은 정적 팩토리로 생성 경로를 구분하고 행위 메서드로 상태 전이를 캡슐화한다.
- Entity는 식별자 기반 동등성, Value Object는 값 기반 동등성을 사용한다.
- 비즈니스 규칙 위반은 도메인별 ErrorCode와 `CoreException`으로 표현한다.
- HTTP 의미는 `CoreErrorType` 같은 프레임워크 미의존 분류까지만 둔다.

## 근거가 된 코드 패턴

- `companion object.create`, `reconstitute` - 신규 생성과 DB 복원 경로 분리
- `{Domain}ErrorCode`, `ErrorCode`, `CoreException` - 도메인 예외 계층
- 도메인 행위 메서드 - Tell, Don't Ask 방식의 상태 변경 캡슐화

## 세부 문서

- [domain-model-convention](domain-model-convention.md) - Entity, Value Object, 팩토리, 행위 메서드를 작성할 때
- [exception-convention](exception-convention.md) - 도메인 ErrorCode와 CoreException을 작성할 때
