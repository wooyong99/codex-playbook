# App Strategies

이 프로젝트에서 `app` 단위에 실제로 사용 중인 구현 전략 요약.

## 핵심 전략

- Controller는 Request DTO를 받고 Extension으로 Command를 만든 뒤 UseCase를 호출한다.
- REST URL은 복수형 명사, kebab-case, `/api/v{N}` prefix를 기본으로 한다.
- 예외 응답은 `GlobalExceptionHandler`와 `BaseResponse`로 단일화한다.
- 표현 계층 전역 관심사는 `common/`, 도메인별 표현 객체는 `{domain}/`에 둔다.
- 인증, 테넌트 컨텍스트, MDC 주입은 app 경계의 전역 관심사로 다룬다.

## 근거가 된 코드 패턴

- `Controller`, `Request`, `Response`, `DtoExtension` - HTTP 계약과 application 계약의 변환 경계
- `GlobalExceptionHandler`, `BaseResponse` - 예외 응답 단일화
- `common/security`, `common/logging` - 표현 계층 전역 관심사 배치

## 세부 문서

- [api-convention](api-convention.md) - Controller, DTO, Extension 구조를 작성할 때
- [rest-design-convention](rest-design-convention.md) - REST URL, ID 위치, pagination 규칙을 정할 때
- [exception-handling-convention](exception-handling-convention.md) - API 예외 응답과 HTTP 상태 매핑을 다룰 때
- [file-structure](file-structure.md) - app 모듈 파일 구조를 정할 때
- [common](common.md) - app 전역 관심사 패키지를 분류할 때
