# External Guidelines

이 문서는 `external` 단위의 실제 코드 위치, 책임, 의존 경계, 구현 전략을 정리한다.

## 코드 위치

- `external` infrastructure module/package - 외부 시스템 Port 구현, ApiClient, DTO, 예외 번역, Mock Adapter를 담당한다.

## 책임

- application 계층이 선언한 outbound Port를 구현한다.
- 외부 API 응답, 오류, 스키마를 내부 Port Result와 ErrorCode로 번역한다.
- Provider별 구성 요소를 한 경계 안에 모아 외부 변경 영향을 격리한다.
- 로컬 개발용 Mock Adapter로 실제 외부 시스템 의존을 분리한다.

## 의존 경계

- depends on: `application`, external systems
- used by: `application`
- 금지되는 방향: 외부 DTO의 Port 시그니처 노출, HTTP/네트워크 예외의 application 전파, Provider 간 패키지 혼재

## 핵심 원칙

- 외부 시스템 변경은 Adapter와 ApiClient 경계 안에서 흡수한다.
- 외부 예외는 Provider 전용 예외 계층을 거쳐 내부 표현으로 번역한다.
- 한 Provider의 Adapter, ApiClient, DTO, ErrorCode, Exception, Config, Mock은 한 패키지 경계 안에 둔다.
- 로깅과 설정은 Provider별로 분리해 장애 범위와 민감 정보 노출을 제어한다.

## 관련 정책

- [security](../../policies/security.md) - 외부 인증 토큰과 민감 정보 처리
- [logging](../../policies/logging.md) - 외부 호출 로깅과 민감 정보 차단
- [concurrency-and-performance](../../policies/concurrency-and-performance.md) - 타임아웃, 재시도, 성능 경계

## 금지 규칙

- HTTP/네트워크 예외를 Adapter 밖으로 그대로 전파하지 않는다.
- 외부 DTO를 Port 입력/출력 타입으로 노출하지 않는다.
- 여러 Provider가 같은 패키지를 공유하지 않는다.
- Mock Adapter가 실제 외부 호출이나 실 credentials에 의존하지 않는다.
- ApiClient 로깅에서 토큰, 개인정보, 원문 payload를 그대로 남기지 않는다.
- Provider별 설정과 DTO를 공용 패키지에 섞지 않는다.

## 주요 컴포넌트

- Adapter: `{Provider}{Function}Adapter`
- Mock Adapter: `Mock{Function}Adapter`
- ApiClient: `{Provider}ApiClient`
- Token cache: `{Provider}TokenHolder`
- DTO: `{Provider}Dtos.kt`
- ErrorCode / Exception: `{Provider}ErrorCode`, `{Provider}Exception`
- Config / Properties: `{Provider}Config`, `{Provider}Properties`

## 전략 문서

- [Strategies](./strategies/README.md)

## 완료 기준

- 외부 시스템별 변경 영향이 Provider 패키지 경계 안에 갇혀 있다.
- application Port에는 외부 DTO와 HTTP 예외가 노출되지 않는다.
- 로컬 개발에서 실제 외부 시스템 없이 주요 흐름을 재현할 수 있다.

## Playbook compatibility

- 이 단위는 기존 playbook의 `external` 개념 계층과 동일하다.
- 실제 프로젝트에서 Provider별 모듈이 분리되어 있으면 Provider를 architecture unit으로 승격할 수 있다.
