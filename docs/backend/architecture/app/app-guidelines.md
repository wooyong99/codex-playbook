# App Guidelines

이 문서는 `app` 단위의 실제 코드 위치, 책임, 의존 경계, 구현 전략을 정리한다.

## 코드 위치

- `app` module/package - HTTP 요청 수신, Request/Response 변환, 예외 응답 변환을 담당한다.

## 책임

- HTTP 진입점 제공: Controller가 Request DTO를 수신하고 application 계층에 위임한다.
- HTTP 관심사 격리: Spring·Jakarta·HTTP 상태 코드 같은 표현 계층 관심사를 app 단위 안에 가둔다.
- 예외 응답 단일화: 모든 예외를 `GlobalExceptionHandler`에서 HTTP 응답으로 변환한다.
- 변환 책임 분리: Request DTO와 Command, Result와 Response 사이의 변환 경계를 명확히 둔다.

## 의존 경계

- depends on: `application`
- used by: Client / API caller
- 금지되는 방향: `domain` 모델 직접 노출, `application` Command 직접 HTTP 바인딩, Controller 내부 비즈니스 로직

## 핵심 원칙

- app 단위는 HTTP 계약을 application 계약으로 변환하는 경계다.
- Controller는 흐름을 조율하지 않고 UseCase 호출과 응답 반환만 수행한다.
- 예외 응답 형식과 HTTP 상태 매핑은 한 곳에서 일관되게 처리한다.

## 관련 정책

- [security](../../policies/security.md) - 인증 컨텍스트와 민감 정보 처리
- [logging](../../policies/logging.md) - 요청 추적과 예외 로깅

## 금지 규칙

- Controller 안에 비즈니스 규칙, 계산, 상태 판단을 구현하지 않는다.
- application 계층 Command를 `@RequestBody`로 직접 수신하지 않는다.
- Controller별 `try-catch`나 분산된 `@ExceptionHandler`를 만들지 않는다.
- Response DTO에 domain Entity나 Value Object를 직접 노출하지 않는다.

## 안티패턴

- DTO 내부에 `toCommand()` 같은 변환 메서드를 넣어 HTTP DTO가 application 계약을 직접 알게 만든다.
- 인증/테넌트/로깅 같은 전역 표현 관심사를 도메인별 Controller에 흩어 둔다.
- HTTP 상태나 Spring 어노테이션이 domain 또는 application 내부로 새어 들어간다.

## 주요 컴포넌트

- Controller: `{Domain}Controller`
- Request/Response DTO: `{Domain}Requests.kt`, `{Domain}Responses.kt`
- DTO 변환: `{Domain}DtoExtension.kt`
- 전역 예외 처리: `GlobalExceptionHandler`
- 공통 응답: `BaseResponse`

## 전략 문서

- [Strategies](./strategies/README.md)

## Playbook compatibility

- 이 단위는 기존 playbook의 `app` 개념 계층과 동일하다.
- 실제 프로젝트에서 app 모듈명이 `api`, `admin`, `web`처럼 나뉘면 `$reverse-engineer-backend-docs`의 `migrate` 모드에서 실제 진입점 단위로 분리한다.
