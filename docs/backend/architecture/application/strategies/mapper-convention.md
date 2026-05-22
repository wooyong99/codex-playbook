# Mapper 컨벤션

이 문서는 application 내부 DTO와 Domain 객체 사이의 변환을 담당하는 `Mapper` 전략을 정리한다.

## 목적

- application DTO와 Domain 객체 사이의 변환 규칙을 한곳에 모은다.
- UseCase 구현체에 인라인 매핑이 흩어지지 않게 한다.
- 변환 책임과 비즈니스 판단 책임을 분리한다.

## 적용 범위

- `Command` 또는 내부 DTO를 Domain 생성 입력으로 변환하는 로직
- Domain 객체를 `Result` 또는 내부 DTO로 변환하는 로직
- 여러 Domain 객체를 조합해 application 결과 DTO를 구성하는 로직

HTTP Request/Response DTO 변환은 app 계층이 소유한다. 외부 API DTO 번역은 external adapter가 소유한다.
하위 컴포넌트 간 DTO 생성 기준은 [component-dto-convention](component-dto-convention.md)을 따른다.

## 책임

- `Application DTO -> Domain` 변환을 수행한다.
- `Domain -> Application DTO` 변환을 수행한다.
- 변환에 필요한 단순 필드 조합과 포맷 조립만 담당한다.

## 전체 흐름

```text
UseCase implementation
  -> Mapper
    -> Application DTO
    -> Domain
```

## 세부 규칙

### 변환 방향

- Command 또는 내부 DTO에서 Domain 생성 입력을 만든다.
- Domain 객체에서 Result 또는 내부 DTO를 만든다.
- 여러 Domain 객체를 하나의 Result로 조립할 수 있다.

### 의존성

- Mapper는 Port를 주입받지 않는다.
- Mapper는 Service, Strategy를 호출하지 않는다.
- Mapper는 Domain 객체와 application DTO에만 의존한다.

### 사용 위치

- UseCase 구현체는 결과 반환 전에 Mapper를 호출한다.
- Service는 Domain 객체 반환을 기본으로 하고, DTO 변환은 UseCase 구현체에서 Mapper로 처리한다.
- 단순 변환이라도 일관성을 위해 Mapper에 둔다.
- 예외 승인 내부 DTO 변환도 Mapper 또는 해당 내부 DTO 소유 컴포넌트의 private 변환으로 제한한다.

## 금지 규칙

- Mapper에 Port, repository, 외부 API client를 주입하지 않는다.
- Mapper가 Service, Strategy를 호출하지 않는다.
- Mapper에서 데이터 조회, 저장, 외부 호출, 상태 변경을 수행하지 않는다.
- Mapper에 비즈니스 규칙 검증이나 정책 판단을 넣지 않는다.
- UseCase 구현체 파일 하단에 `private` 변환 함수를 추가해 Mapper를 우회하지 않는다.
- Service, Validator, Strategy 전용 DTO 체인을 만들기 위해 Mapper를 사용하지 않는다.
- Mapper가 app 계층 Response DTO, 외부 API DTO, persistence Entity 변환을 application 내부 변환처럼 소유하지 않는다.

## 예외와 경계

- 조건에 따라 다른 비즈니스 판단이 필요하면 호출 측에서 판단한 뒤 Mapper에 넘긴다.
- 변환 중 데이터 조회가 필요하면 Mapper가 아니라 호출 측 또는 Service 책임으로 분리한다.

## 완료 기준

- application DTO와 Domain 사이의 변환이 Mapper에 모여 있다.
- Mapper는 조회, 저장, 외부 호출, 상태 변경을 수행하지 않는다.
- UseCase 구현체에 인라인 DTO 조립이 남아 있지 않다.
