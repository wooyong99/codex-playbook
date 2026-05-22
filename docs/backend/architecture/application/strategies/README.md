# Application Strategies

이 문서는 `application` 단위의 역할형 전략 문서 맵을 소유한다.

## 목적

- application 내부 컴포넌트의 책임을 전략별로 분리한다.
- `UseCase`, `Facade`, `Coordinator`, `Service`, `Validator`, `Strategy`, `Handler`, `Port`, `Mapper`의 선택 기준을 한곳에서 찾게 한다.
- 레거시 명칭 대신 현재 전략 문서의 용어를 기준으로 application 구조를 설명한다.

## 적용 범위

- 외부 진입 계약과 UseCase 구현체 책임
- aggregate command 처리, 트랜잭션 조합, 이벤트 및 외부 시스템 연동
- 규칙 검증, 정책 분기, 경계 보호, Port 추상화, DTO 변환

## 전략 문서

| 전략 | 문서 | 책임 |
|------|------|------|
| UseCase | [use-case-convention](use-case-convention.md) | 외부 호출자가 의존하는 추상 인터페이스 계약 |
| Facade | [facade-convention](facade-convention.md) | 여러 도메인 또는 하위 컴포넌트 뒤의 복잡도 은닉 |
| Coordinator | [coordinator-convention](coordinator-convention.md) | 여러 트랜잭션 흐름, 이벤트, 외부 시스템 호출 조합 |
| Service | [service-convention](service-convention.md) | aggregate command의 원자적 처리 |
| Validator | [validator-convention](validator-convention.md) | 조회된 데이터 기반 비즈니스 규칙 검증 |
| Strategy | [strategy-convention](strategy-convention.md) | 정책별 처리 방식 캡슐화 |
| Handler | [handler-convention](handler-convention.md) | 여러 개념 영역에서 재사용되는 로직과 경계 보호 |
| Port | [port-convention](port-convention.md) | repository, external system 등 외부 자원 추상 인터페이스 |
| Mapper | [mapper-convention](mapper-convention.md) | application 내부 DTO와 Domain 객체 간 변환 |

## 공통 의존 흐름

```text
app / event / CLI
  -> UseCase interface
    -> Facade | Coordinator | Service
      -> Validator
      -> Strategy
      -> Handler
      -> Port interface
      -> Mapper
        -> Domain

storage / external
  -> Port implementation
```
