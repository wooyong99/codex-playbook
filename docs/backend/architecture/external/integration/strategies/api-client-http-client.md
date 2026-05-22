# ApiClient HTTP 클라이언트 컨벤션

이 문서는 ApiClient가 Provider 전용 HTTP client bean을 주입받아 사용하는 전략을 정리한다.

## 목적

- Provider별 baseUrl, timeout, header, interceptor 설정을 분리한다.
- ApiClient가 HTTP client를 직접 생성하지 않게 한다.
- 외부 호출 설정 변경의 영향을 Provider 경계 안에 둔다.

## 적용 범위

- Provider 전용 HTTP client bean
- `@Qualifier` 기반 주입
- ApiClient의 HTTP client 사용 방식

HTTP client bean 생성은 [config-convention](config-convention.md)이 소유한다.

## 책임

- ApiClient가 사용할 HTTP client 주입 방식을 정의한다.
- Provider별 HTTP client 재사용 원칙을 정의한다.
- 메서드 내부 client 생성과 공용 client 공유를 금지한다.

## 전체 흐름

```text
{Provider}Config
  -> @Bean("{provider}ServiceRestClient")
    -> {Provider}ApiClient(@Qualifier)
      -> external endpoint
```

## 세부 규칙

### HTTP client 선택

- 프로젝트 기본 HTTP client는 Provider별 Config 문서에서 정한다.
- 같은 Provider 안에서는 하나의 client bean을 재사용한다.
- Provider마다 baseUrl, timeout, header가 다르면 별도 bean을 둔다.

### 빈 주입 방식

- ApiClient는 생성자에서 `@Qualifier`로 Provider 전용 bean을 주입받는다.
- qualifier 값은 Config의 bean 이름과 동일해야 한다.
- 여러 Provider가 같은 bean을 공유하지 않는다.

### 사용 위치

- HTTP client는 ApiClient에서만 직접 사용한다.
- Adapter는 ApiClient를 통해 외부 호출을 수행한다.
- Mock Adapter는 HTTP client를 주입받지 않는다.

## 금지 규칙

- 메서드 내부에서 HTTP client를 매번 생성하지 않는다.
- Provider별 qualifier 없이 타입만으로 HTTP client를 주입받지 않는다.
- 두 Provider가 같은 HTTP client bean을 공유하지 않는다.
- Adapter나 Service가 HTTP client를 직접 주입받지 않는다.
- Mock Adapter가 HTTP client를 주입받지 않는다.

## 예외와 경계

- Provider가 여러 baseUrl을 사용하면 기능별 client bean을 둘 수 있다.
- 단일 Provider의 모든 API가 같은 baseUrl과 timeout을 쓰면 하나의 client bean을 공유한다.
- HTTP client 종류가 `RestClient`, `RestTemplate`, `WebClient` 중 무엇이든 Provider 전용 bean 원칙을 유지한다.

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] ApiClient가 Provider 전용 HTTP client bean을 qualifier로 주입받는다.
- [ ] client 생성과 timeout 설정이 Config로 분리되어 있다.
- [ ] 외부 호출 코드 안에 client 생성 코드가 반복되지 않는다.
