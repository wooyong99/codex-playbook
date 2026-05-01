# External Strategies

이 프로젝트에서 `external` 단위에 실제로 사용 중인 구현 전략 요약.

## 핵심 전략

- Adapter는 application Port만 구현하고 외부 예외를 내부 Result/ErrorCode로 번역한다.
- ApiClient는 HTTP 호출과 Provider 예외 변환을 캡슐화한다.
- Provider별 DTO, Exception, ErrorCode, Config, Properties, Mock Adapter를 같은 경계에 둔다.
- Mock Adapter는 `local` 프로필에서 실 외부 시스템 의존을 대체한다.

## 근거가 된 코드 패턴

- `{Provider}{Function}Adapter`, `Mock{Function}Adapter` - 실 Adapter와 로컬 Mock 분리
- `{Provider}ApiClient`, `{Provider}Dtos` - 외부 API 호출과 스키마 캡슐화
- `{Provider}ErrorCode`, `{Provider}Exception` - 외부 오류의 내부 표현 번역
- `{Provider}Config`, `{Provider}Properties` - Provider별 HTTP 클라이언트 설정

## 세부 문서

- [adapter-convention](adapter-convention.md) - Outbound Port 구현 Adapter를 작성할 때
- [api-client-convention](api-client-convention.md) - HTTP 호출과 예외 변환을 작성할 때
- [api-client-http-client](api-client-http-client.md) - Provider 전용 HTTP 클라이언트를 구성할 때
- [api-client-logging](api-client-logging.md) - 외부 API 호출 로그를 남길 때
- [dto-convention](dto-convention.md) - 외부 요청/응답 DTO를 작성할 때
- [exception-convention](exception-convention.md) - Provider 예외 계층을 작성할 때
- [errorcode-convention](errorcode-convention.md) - 외부 에러코드를 내부 ErrorCode로 번역할 때
- [config-convention](config-convention.md) - Config/Properties를 작성할 때
- [mock-adapter-convention](mock-adapter-convention.md) - 로컬 Mock Adapter를 작성할 때
