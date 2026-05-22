# Config / Properties 컨벤션

이 문서는 Provider별 설정값과 HTTP client bean을 구성하는 전략을 정리한다.

## 목적

- Provider별 baseUrl, timeout, 인증 값을 외부 설정으로 분리한다.
- Provider 전용 HTTP client bean을 구성한다.
- 환경별 외부 시스템 연결 설정을 코드 변경 없이 바꿀 수 있게 한다.

## 적용 범위

- `{Provider}Properties`
- `{Provider}Config`
- `@ConfigurationProperties`
- Provider 전용 HTTP client bean
- auto configuration 등록

## 책임

- Provider 설정 prefix와 property 구조를 정의한다.
- HTTP client bean 이름과 qualifier를 고정한다.
- timeout과 인증 정보 기본값 정책을 정의한다.

## 전체 흐름

```text
application.yml
  -> {Provider}Properties
    -> {Provider}Config
      -> @Bean("{provider}ServiceRestClient")
        -> {Provider}ApiClient
```

## 세부 규칙

### 네이밍

| 항목 | 패턴 |
|------|------|
| Config 클래스 | `{Provider}Config` |
| Properties 클래스 | `{Provider}Properties` |
| properties prefix | `{provider}.service` 또는 kebab-case |
| HTTP client bean | `{provider}ServiceRestClient` 또는 `{provider}ServiceClient` |
| Qualifier | HTTP client bean 이름과 동일 |

- `{Provider}ServiceConfig`, `{Provider}ServiceProperties`처럼 `Service` 접미사를 붙이지 않는다.

### Properties

- Properties는 `@ConfigurationProperties`가 붙은 `data class`로 선언한다.
- 기본 필드는 `baseUrl`, `connectTimeout`, `readTimeout`이다.
- 인증이 필요하면 `apiKey`, `clientId`, `secret` 같은 Provider 전용 필드를 추가한다.
- timeout은 `Duration`을 사용한다.
- 기본값은 로컬 개발 환경 기준으로 둔다.
- 실제 운영 secret을 기본값에 넣지 않는다.

### Config

- Config는 `@Configuration`으로 선언한다.
- `@EnableConfigurationProperties({Provider}Properties::class)`로 Properties를 활성화한다.
- Provider 전용 HTTP client bean을 만든다.
- baseUrl, default header, timeout은 Properties에서 읽는다.

### Timeout

- `connectTimeout`과 `readTimeout`을 모두 설정한다.
- connect timeout은 짧게, read timeout은 API 특성에 맞게 둔다.
- 무한 대기 기본값에 의존하지 않는다.

### AutoConfiguration

- external 모듈이 자동 등록을 사용하면 `ExternalAutoConfiguration`과 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`를 함께 관리한다.
- 신규 Provider Config가 자동 등록 대상에 포함되는지 확인한다.

## 금지 규칙

- HTTP client를 Config 없이 ApiClient 내부에서 직접 생성하지 않는다.
- Properties 없이 `@Value`로 개별 값을 흩어 주입하지 않는다.
- timeout 설정을 생략하지 않는다.
- 두 Provider가 같은 HTTP client bean을 공유하지 않는다.
- 하드코딩된 운영 baseUrl을 코드에 남기지 않는다.
- 민감 정보 실제 값을 Properties 기본값에 채우지 않는다.

## 예외와 경계

- Provider가 여러 baseUrl을 쓰면 기능별 Properties 또는 client bean 분리를 검토한다.
- local mock만 사용하는 Provider는 실 HTTP client bean이 불필요할 수 있다.
- 프로젝트가 별도 secret manager를 사용하면 Properties에는 secret key 참조만 둔다.

## 완료 기준

- Provider 설정이 `@ConfigurationProperties`로 바인딩된다.
- ApiClient가 Provider 전용 HTTP client bean을 qualifier로 주입받는다.
- timeout과 민감 정보 기본값 정책이 명확하다.
