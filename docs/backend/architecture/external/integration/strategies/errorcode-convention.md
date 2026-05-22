# ErrorCode 컨벤션

이 문서는 외부 API error code를 Provider enum으로 관리하고 Port ErrorCode로 번역하는 전략을 정리한다.

## 목적

- 외부 error code 문자열 비교를 한곳에 모은다.
- 외부 code와 Port ErrorCode 번역을 명시적으로 관리한다.
- 외부 API code 추가 시 누락을 컴파일 단계에서 찾기 쉽게 한다.

## 적용 범위

- `{Provider}ErrorCode`
- `{Provider}{Function}ErrorCode`
- `fromCode(code: String)`
- Adapter 내부 `toPortErrorCode()`

## 책임

- 외부 error code 문자열을 Provider enum으로 표현한다.
- 미매핑 외부 code의 fallback 정책을 둔다.
- Port ErrorCode 번역을 Adapter 경계에 둔다.

## 전체 흐름

```text
{Provider}ApiException.code
  -> {Provider}ErrorCode.fromCode(code)
    -> Adapter private toPortErrorCode()
      -> Port ErrorCode
```

## 세부 규칙

### 네이밍

| 항목 | 패턴 |
|------|------|
| 기본 ErrorCode | `{Provider}ErrorCode` |
| 기능별 ErrorCode | `{Provider}{Function}ErrorCode` |
| 조회 메서드 | `fromCode(code: String)` |
| 번역 메서드 | `toPortErrorCode()` |

### 파일 위치

- ErrorCode enum은 DTO 파일과 분리해 `{Provider}ErrorCode.kt`로 둔다.
- 기능별 code 집합이 완전히 다르면 `{Provider}{Function}ErrorCode.kt`로 분리할 수 있다.

### enum 구조

- enum 항목은 외부 code 문자열을 담는 `code` 필드를 가진다.
- `fromCode()`는 매핑되지 않는 코드를 `null`로 반환한다.
- `fromCode()`에서 예외를 던지지 않는다.

### Port ErrorCode 번역

- Port ErrorCode 번역은 Adapter 파일 안의 private extension으로 둔다.
- `when` 분기에 모든 enum 항목을 명시한다.
- `else`를 사용하지 않는다.
- `null`은 fallback Port ErrorCode로 처리한다.
- ErrorCode enum 파일이 application Port 타입에 의존하지 않게 한다.

## 금지 규칙

- 외부 error code 문자열을 Adapter에서 직접 비교하지 않는다.
- `fromCode()`에서 예외를 던지지 않는다.
- ErrorCode enum을 DTO 파일 안에 포함하지 않는다.
- `toPortErrorCode()`에서 `else` 분기를 사용하지 않는다.
- `toPortErrorCode()`를 ErrorCode enum 파일에 정의하지 않는다.
- 미매핑 code fallback 없이 null을 그대로 방치하지 않는다.

## 예외와 경계

- 외부 code가 불안정하면 raw code를 Port Result의 `code` 필드에 함께 보존한다.
- Port가 별도 ErrorCode를 갖지 않는 단순 연동이면 status와 raw code만 반환할 수 있다.
- 여러 API가 같은 code 의미를 공유하면 Provider 공통 enum을 재사용할 수 있다.

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] 외부 error code가 Provider enum으로 표현된다.
- [ ] Adapter가 `fromCode()`와 `toPortErrorCode()`를 거쳐 Port ErrorCode를 반환한다.
- [ ] 신규 enum 추가 시 Port ErrorCode 번역 누락이 테스트, 컴파일, 또는 명시적 리뷰 체크 항목에서 검출된다.
