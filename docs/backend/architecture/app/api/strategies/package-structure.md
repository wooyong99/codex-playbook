# Package Structure 컨벤션

이 문서는 `app` 단위의 패키지 구조와 파일 배치 기준을 정리한다.

## 목적

- 표현 계층 전역 관심사와 도메인별 API 계약을 분리한다.
- Controller, DTO, 변환 Extension이 같은 resource 단위 안에서 찾히게 한다.
- 파일 수가 늘어도 루트 패키지가 Request/Response DTO로 포화되지 않게 한다.

## 적용 범위

- app module/package 내부 구조
- `common/` 또는 이에 준하는 전역 관심사 패키지
- 도메인별 Controller, DTO, 변환 Extension 배치
- API version 공존 시 패키지 분리 기준

각 컴포넌트의 세부 설계 규칙은 개별 전략 문서가 소유한다.

## 책임

- app 하위 패키지를 전역 관심사와 도메인별 API로 나눈다.
- DTO를 도메인 패키지 루트가 아니라 `dto/` 아래에 둔다.
- version 공존 시 package 분리 기준을 정한다.

## 전체 구조

```text
app/
  ├── common/
  │   ├── response/
  │   ├── exception/
  │   ├── openapi/
  │   ├── web/
  │   ├── security/
  │   └── logging/
  └── {domain}/
      ├── {Entity}Controller.kt
      ├── {Domain}DtoExtension.kt
      └── dto/
          ├── {Domain}Requests.kt
          └── {Domain}Responses.kt
```

Version이 둘 이상 공존하면 도메인 패키지 아래 version 하위 패키지를 둔다.

```text
app/
  └── order/
      ├── v1/
      │   ├── OrderController.kt
      │   ├── OrderDtoExtension.kt
      │   └── dto/
      └── v2/
          ├── OrderController.kt
          ├── OrderDtoExtension.kt
          └── dto/
```

## 세부 규칙

### common 패키지

- `common/`은 표현 계층 전역 관심사만 담는다.
- response envelope, exception handler, OpenAPI config, web config, security, logging 같은 cross-cutting API 구성요소를 둔다.
- 도메인별 DTO, Controller, 변환 로직은 `common/`에 두지 않는다.

### 도메인 패키지

- `{domain}`은 소문자 단수형을 기본값으로 한다.
- Controller와 DTO 변환 Extension은 도메인 패키지 루트에 둔다.
- Request/Response DTO는 `dto/` 하위에 둔다.
- 도메인 패키지 간 직접 참조를 피한다.

### DTO 패키지

- `{Domain}Requests.kt`는 같은 도메인의 request DTO를 모은다.
- `{Domain}Responses.kt`는 API 전용 response DTO가 필요할 때만 만든다.
- DTO 내부에 변환 함수를 넣지 않는다.
- DTO 변환은 `{Domain}DtoExtension.kt`가 소유한다.

### Version 패키지

- `v1`만 존재하면 version package를 만들지 않아도 된다.
- `v1`과 `v2`가 동시에 운영되면 version 하위 패키지로 Controller와 DTO를 분리한다.
- version package는 app 계층에만 둔다. application UseCase는 API version을 직접 알지 않는다.

## 금지 규칙

- app 루트에 Request/Response DTO 파일을 계속 쌓아두지 않는다.
- 도메인 패키지 없이 `controller/`, `dto/` 같은 역할 패키지만 최상위에 나열하지 않는다.
- `common`, `shared`, `util`에 도메인별 API 계약을 넣지 않는다.
- `{Domain}DtoExtension.kt`를 `dto/` 패키지 안에 두지 않는다.
- app DTO를 application `dto/`에 두지 않는다.
- API version 차이를 하나의 DTO에 nullable field와 조건 분기로 누적하지 않는다.
- version package를 application, domain, storage, external로 전파하지 않는다.

## 예외와 경계

- admin API가 별도 모듈이면 app module 자체가 분리될 수 있다.
- GraphQL, batch callback, webhook처럼 REST resource 구조와 다른 protocol은 별도 package를 둘 수 있다.
- 프로젝트의 기존 전역 관심사 패키지명이 `global`, `shared`, `support`라면 역할 기준만 동일하게 적용한다.

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] 신규 Controller와 DTO 위치가 resource 도메인과 version 기준에 맞게 배치되어 있다.
- [ ] DTO 파일이 도메인 `dto/` 아래에 모여 있다.
- [ ] common 패키지가 표현 계층 전역 관심사만 담고 있다.
