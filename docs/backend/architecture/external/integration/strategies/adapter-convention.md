# Adapter 컨벤션

이 문서는 external Adapter가 application outbound Port를 구현하고 외부 결과를 내부 표현으로 번역하는 전략을 정리한다.

## 목적

- Adapter가 외부 시스템과 application Port 사이의 유일한 번역 경계가 되게 한다.
- 외부 예외를 Port Result, status, code로 변환한다.
- 외부 DTO와 Provider 세부사항이 application으로 새지 않게 한다.

## 적용 범위

- `{Provider}{Function}Adapter`
- `Mock{Function}Adapter`와의 profile 대칭
- Provider 예외에서 Port Result로의 변환
- Port 타입과 외부 DTO 간 매핑

ErrorCode 번역 세부 규칙은 [errorcode-convention](errorcode-convention.md)이 소유한다.

## 책임

- application Port 인터페이스를 구현한다.
- ApiClient를 호출하고 Provider 예외 계층만 catch한다.
- 외부 DTO를 Port 타입으로 변환한다.
- 요청, 응답, 예외 로그에 비즈니스 식별자를 남기되 민감 정보는 마스킹한다.

## 전체 흐름

```text
application Port
  -> {Provider}{Function}Adapter
    -> {Provider}ApiClient
      -> external API
    -> {Provider}Exception catch
    -> {Provider}ErrorCode translation
    -> Port Result
```

## 세부 규칙

### 네이밍

| 항목 | 패턴 |
|------|------|
| 실 Adapter | `{Provider}{Function}Adapter` |
| Mock Adapter | `Mock{Function}Adapter` |
| 구현 대상 Port | `{Provider}{Function}Port` 또는 `{Capability}Port` |

- 한 외부 서비스에서 여러 기능을 사용하면 기능별 Adapter로 분리한다.
- Adapter 하나는 하나의 Port 구현을 기본으로 한다.
- application outbound Port 인터페이스는 반드시 `*Port`로 끝낸다.
- Port 이름을 `Client`, `Provider`, `Gateway`만으로 끝내지 않는다. 이 이름들은 외부 구현체나 provider 세부사항으로 오해될 수 있다.

### 의존성

- Adapter는 ApiClient와 Port 타입만 의존한다.
- Repository, UseCase, 다른 Adapter를 주입받지 않는다.
- Provider가 같고 Request/Response만 다르면 Adapter는 분리하고 ApiClient는 공유할 수 있다.

### 예외 변환

- Adapter는 Provider 예외 계층을 구체 타입부터 부모 타입 순서로 catch한다.
- `{Provider}ApiException`은 비즈니스 실패 status와 외부 code로 매핑한다.
- `{Provider}ServerException`은 `HTTP_{status}` code로 매핑한다.
- `{Provider}NetworkException`은 `NETWORK_ERROR` code로 매핑한다.
- `{Provider}ResponseParsingException`은 `PARSING_ERROR` 또는 `EXTERNAL_ERROR` code로 매핑한다.
- 마지막 Provider 부모 예외는 `EXTERNAL_ERROR` 같은 폴백으로 매핑한다.

### DTO 매핑

- Port 타입과 외부 DTO 매핑은 Adapter 내부에서 수행한다.
- 복잡한 매핑은 Adapter 파일 내부의 private function 또는 extension으로 분리한다.
- Port 타입은 외부 API 스키마 세부사항을 노출하지 않는다.

### 로깅

- 요청 시작, 응답 수신, 예외 발생 지점에 로그를 남긴다.
- 로그 태그는 `[Provider - 기능]` 형식을 사용한다.
- 핀번호, 카드번호, 계좌번호, token, 원문 payload는 마스킹한다.

## 금지 규칙

- 다른 Adapter, Repository, UseCase를 주입받지 않는다.
- 외부 예외를 Adapter 밖으로 그대로 전파하지 않는다.
- Spring HTTP 예외를 Adapter에서 직접 catch하지 않는다. ApiClient가 Provider 예외로 감싸야 한다.
- Result 타입을 우회해 Port 시그니처 밖으로 예외를 던지지 않는다.
- 외부 연동 Port 인터페이스를 `*Port` suffix 없이 정의하지 않는다.
- Port 타입에 외부 DTO를 직접 노출하지 않는다.
- 로그에 민감 정보를 원문으로 출력하지 않는다.
- 하나의 Adapter에 여러 Port 구현을 기본값으로 합치지 않는다.

## 예외와 경계

- Mock이 필요한 Adapter는 실 Adapter `@Profile("!local")`, Mock Adapter `@Profile("local")`로 대칭 구성한다.
- Mock이 필요 없는 Adapter는 profile 제약 없이 기본 bean으로 등록할 수 있다.
- 외부 API code를 내부 Port ErrorCode로 변환해야 하면 Adapter 내부 private extension으로 둔다.

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] Adapter가 구현하는 application outbound 인터페이스 이름이 `*Port`로 끝난다.
- [ ] Adapter 클래스가 정확히 하나의 outbound Port 인터페이스를 구현한다.
- [ ] 외부 예외가 Port Result로 변환되어 application에 노출된다.
- [ ] 외부 DTO와 Provider 예외 타입이 Port 시그니처로 새지 않는다.
- [ ] 민감 정보가 Adapter 로그에 원문으로 남지 않는다.
