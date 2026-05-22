# ApiClient 컨벤션

이 문서는 external ApiClient가 외부 HTTP 호출과 Provider 예외 변환을 담당하는 전략을 정리한다.

## 목적

- HTTP 호출 세부사항을 ApiClient 안에 캡슐화한다.
- Spring/JDK 네트워크 예외를 Provider 전용 예외 계층으로 통일한다.
- Adapter가 HTTP client와 외부 기술 예외를 알지 않게 한다.

## 적용 범위

- `{Provider}ApiClient`
- 외부 endpoint 호출 메서드
- `handleErrors(apiName, call)`
- `executeWithToken(apiName, call)`
- `{Provider}TokenHolder`
- 공통 응답 wrapper payload 처리

HTTP client bean 구성은 [api-client-http-client](api-client-http-client.md)이, 호출 로그 세부 기준은 [api-client-logging](api-client-logging.md)이 소유한다.

## 책임

- 외부 endpoint를 호출한다.
- 요청/응답 DTO와 공통 wrapper를 처리한다.
- HTTP, 인증, 서버, 네트워크, 파싱 오류를 Provider 예외로 변환한다.
- token 인증이 필요한 Provider의 token 재발급 흐름을 캡슐화한다.

## 전체 흐름

```text
Adapter
  -> {Provider}ApiClient.publicMethod()
    -> executeWithToken optional
    -> handleErrors
      -> HTTP client
      -> {Provider}Exception
```

## 세부 규칙

### 네이밍

| 항목 | 패턴 |
|------|------|
| ApiClient | `{Provider}ApiClient` |
| 예외 변환 헬퍼 | `handleErrors(apiName, call)` |
| token 인증 헬퍼 | `executeWithToken(apiName, call)` |
| endpoint 상수 | `{FUNCTION}_ENDPOINT` |
| response type 상수 | `{FUNCTION}_RESPONSE_TYPE` |

- `{Provider}ServiceApiClient`처럼 `Service` 접미사를 붙이지 않는다.
- 메서드 하나가 endpoint 하나를 담당한다.

### 메서드 시그니처

- public method는 해당 endpoint의 Request DTO 또는 path/query 값을 입력으로 받는다.
- 반환 타입은 Response DTO 또는 Provider 공통 wrapper이다.
- 한 메서드에서 여러 endpoint를 type 분기로 호출하지 않는다.

### 예외 변환

- 모든 외부 호출은 `handleErrors(apiName, call)`을 거친다.
- `HttpClientErrorException.Unauthorized`는 `{Provider}AuthException`으로 변환한다.
- 401을 제외한 4xx는 `{Provider}ApiException`으로 변환하고 외부 error code를 보존한다.
- 5xx는 `{Provider}ServerException`으로 변환하고 HTTP status를 보존한다.
- timeout, socket, DNS 실패는 `{Provider}NetworkException`으로 변환한다.
- 이미 변환된 `{Provider}Exception`은 그대로 다시 던진다.
- 역직렬화와 payload 누락은 `{Provider}ResponseParsingException`으로 변환한다.

### Bearer Token

- Bearer Token이 필요한 호출은 `executeWithToken`을 사용한다.
- token 발급 자체는 token이 없으므로 `handleErrors`만 사용한다.
- 401 발생 시 token을 invalidate하고 1회만 재시도한다.
- token 캐싱과 만료 관리는 `{Provider}TokenHolder`가 담당한다.
- TokenHolder는 동시성 제어와 만료 buffer를 가진다.

### 공통 응답 wrapper

- 외부 응답이 `{ result, payload }` 같은 wrapper를 사용하면 payload 추출 책임을 명확히 한다.
- payload가 필수인데 null이면 ResponseParsingException으로 승격한다.
- Adapter가 wrapper 전체를 받아야 하는 API는 Adapter가 payload 접근을 담당할 수 있다.

## 금지 규칙

- 메서드마다 try/catch를 반복 작성하지 않는다.
- HTTP client를 메서드 내부에서 매번 생성하지 않는다.
- Spring HTTP 예외나 JDK 네트워크 예외를 ApiClient 밖으로 전파하지 않는다.
- endpoint URL을 메서드 내부 문자열 literal로 흩뜨리지 않는다.
- 로깅 없이 외부 호출 public method를 추가하지 않는다.
- 한 public method 안에서 여러 endpoint 호출을 조건 분기로 바꾸지 않는다.
- token을 ApiClient 일반 필드에서 직접 관리하지 않는다.
- 인증 실패 재시도를 무제한으로 수행하지 않는다.

## 예외와 경계

- Provider가 token 인증을 쓰지 않으면 `executeWithToken`과 TokenHolder를 만들지 않는다.
- Provider가 공통 wrapper를 쓰지 않으면 endpoint별 Response DTO를 바로 반환할 수 있다.
- HTTP client 종류는 프로젝트별 선택 사항이지만 Provider 전용 bean 주입 원칙은 유지한다.

## 완료 기준

- 모든 public 외부 호출이 단일 예외 변환 흐름을 통과한다.
- Adapter는 Provider 예외 계층만 알면 Result 변환을 수행할 수 있다.
- token 인증 흐름이 TokenHolder와 executeWithToken으로 격리되어 있다.
- 외부 호출 로그와 endpoint 상수가 누락되지 않는다.
