# Exception 컨벤션

이 문서는 external Provider 예외 계층을 정의하는 전략을 정리한다.

## 목적

- HTTP client와 네트워크 예외를 Provider 전용 예외로 통일한다.
- Adapter가 외부 실패를 일관된 Result status로 변환할 수 있게 한다.
- Provider별 예외가 서로 섞이지 않게 한다.

## 적용 범위

- `{Provider}Exception`
- `{Provider}ApiException`
- `{Provider}AuthException`
- `{Provider}ServerException`
- `{Provider}NetworkException`
- `{Provider}ResponseParsingException`

## 책임

- Provider별 sealed exception root를 정의한다.
- API, 인증, 서버, 네트워크, 파싱 실패를 구분한다.
- 원시 예외의 cause와 외부 raw message를 보존한다.

## 전체 흐름

```text
HTTP client exception
  -> {Provider}ApiClient.handleErrors
    -> {Provider}Exception
      -> Adapter catch
      -> Port Result
```

## 세부 규칙

### 네이밍

| 항목 | 패턴 |
|------|------|
| 파일 | `{Provider}Exception.kt` |
| 루트 | `{Provider}Exception` |
| API 예외 | `{Provider}ApiException` |
| Auth 예외 | `{Provider}AuthException` |
| Server 예외 | `{Provider}ServerException` |
| Network 예외 | `{Provider}NetworkException` |
| Parsing 예외 | `{Provider}ResponseParsingException` |

- `{Provider}ServiceException`처럼 `Service` 접미사를 붙이지 않는다.

### 예외 계층

- 루트 예외는 `sealed class`로 선언하고 `RuntimeException`을 상속한다.
- 하위 예외는 API, Auth, Server, Network, ResponseParsing 5종을 기본으로 둔다.
- Provider 특수 분류가 필요하면 sealed root 아래 하위 클래스로 추가한다.

### 예외별 필수 정보

| 예외 | 필수 정보 | Adapter 매핑 |
|------|----------|--------------|
| `*ApiException` | `code`, `rawMessage`, `cause` | 비즈니스 실패 status와 raw code |
| `*AuthException` | `rawMessage`, `cause` | token 재발급 트리거 |
| `*ServerException` | `httpStatus`, `rawMessage`, `cause` | `HTTP_{status}` |
| `*NetworkException` | `rawMessage`, `cause` | `NETWORK_ERROR` |
| `*ResponseParsingException` | `rawMessage`, `cause` | `PARSING_ERROR` 또는 `EXTERNAL_ERROR` |

### 메시지와 cause

- message는 Provider, 분류, 식별자를 포함한다.
- 외부 원문 메시지는 `rawMessage`로 보존한다.
- 원시 예외를 Provider 예외로 감쌀 때 `cause`를 보존한다.
- 메시지와 rawMessage에 민감 정보를 넣지 않는다.

## 금지 규칙

- 루트 예외를 `sealed class` 외의 open class나 일반 class로 선언하지 않는다.
- 여러 Provider가 단일 공용 예외 계층을 공유하지 않는다.
- Provider 예외가 `Exception`이나 `Throwable`을 직접 상속하지 않는다.
- 예외 메시지에 민감 정보를 포함하지 않는다.
- 원시 예외를 cause 없이 래핑하지 않는다.
- `{Provider}ServiceException` 같은 Service prefix를 붙이지 않는다.
- Spring HTTP 예외를 Adapter까지 그대로 전파하지 않는다.

## 예외와 경계

- AuthException은 일반적으로 ApiClient 내부 token 재발급에 사용하고 Adapter까지 전파되지 않는다.
- Provider 특수 실패 분류가 필요해도 기본 5종을 제거하거나 이름을 바꾸지 않는다.
- 외부 error code와 Port ErrorCode 번역은 [errorcode-convention](errorcode-convention.md)이 소유한다.

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] Provider별 sealed exception 계층이 독립적으로 정의되어 있다.
- [ ] ApiClient가 원시 HTTP/네트워크 예외를 Provider 예외로 변환한다.
- [ ] Adapter가 Provider 예외만 catch해 Port Result로 바꿀 수 있다.
- [ ] cause와 rawMessage가 보존되고 민감 정보는 노출되지 않는다.
