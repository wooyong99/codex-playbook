# Domain Strategies

이 문서는 `domain` 단위의 역할형 전략 문서 맵을 소유한다.

## 목적

- domain 내부 모델과 예외의 책임을 전략별로 분리한다.
- `Domain Model`, `Domain Exception`의 선택 기준을 한곳에서 찾게 한다.
- 레거시 템플릿 대신 현재 전략 문서의 용어를 기준으로 domain 구조를 설명한다.

## 적용 범위

- Entity, Value Object, 상태 enum, 도메인 행위 메서드
- 정적 팩토리, 복원 경로, 불변식 보호
- 도메인 ErrorCode, CoreException, framework-independent error type

## 전략 문서

| 전략 | 문서 | 책임 |
|------|------|------|
| Domain Model | [domain-model-convention](domain-model-convention.md) | Entity, Value Object, 팩토리, 상태 전이, Tell Don't Ask 규칙 |
| Domain Exception | [exception-convention](exception-convention.md) | 도메인 ErrorCode, CoreException, 예외 선택 기준 |

## 공통 의존 흐름

```text
application
  -> Domain Model
    -> Domain behavior
    -> Domain exception

app
  -> GlobalExceptionHandler
    -> CoreErrorType mapping
```
