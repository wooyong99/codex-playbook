# DTO 컨벤션

이 문서는 external Provider의 요청/응답 DTO가 외부 API 스키마를 표현하는 전략을 정리한다.

## 목적

- 외부 API 스키마를 Provider 경계 안에 가둔다.
- DTO가 외부 JSON 구조를 명확히 반영하게 한다.
- 외부 스키마 확장으로 인한 역직렬화 실패를 줄인다.

## 적용 범위

- `{Provider}Dtos.kt`
- Request DTO
- Response DTO
- 공통 응답 wrapper
- payload, data DTO

## 책임

- 외부 요청과 응답 JSON 스키마를 1:1로 표현한다.
- JSON property 이름을 명시한다.
- 원 스키마 타입을 보존하고 도메인 타입 변환은 Adapter로 넘긴다.

## 전체 흐름

```text
external JSON
  -> {Provider}Dtos
    -> {Provider}ApiClient
      -> Adapter mapping
        -> Port type
```

## 세부 규칙

### 네이밍

| 항목 | 패턴 |
|------|------|
| DTO 파일 | `{Provider}Dtos.kt` |
| 요청 DTO | `{Provider}{Function}Request` |
| 응답 DTO | `{Provider}{Function}Response` |
| 응답 data payload | `{Provider}{Function}Data` |
| 공통 wrapper | `{Provider}ApiResponse<T>` |
| 공통 결과 | `{Provider}ResponseResult` |

### JSON 어노테이션

- 모든 DTO에 `@JsonIgnoreProperties(ignoreUnknown = true)`를 붙인다.
- 모든 프로퍼티에 `@get:JsonProperty("...")`를 명시한다.
- 외부 API가 camelCase를 쓰면 해당 key를 그대로 명시한다.

### 스키마 구조

- 외부 응답의 중첩 구조를 DTO에서 그대로 표현한다.
- 공통 wrapper와 payload를 플랫하게 합치지 않는다.
- payload 내부에 data 계층이 있으면 별도 data DTO로 표현한다.

### 타입 선택

- 외부 스키마의 원 타입을 유지한다.
- 금액이 Long으로 오면 DTO는 Long을 유지하고 Adapter에서 BigDecimal로 변환한다.
- 날짜가 String으로 오면 DTO는 String을 유지하고 Adapter에서 LocalDate로 변환한다.
- 필수로 기대하지만 null이 오면 ResponseParsingException으로 승격한다.

### 배치

- Provider의 DTO는 한 파일에 모은다.
- ErrorCode enum과 Exception 계층은 DTO 파일에 넣지 않는다.

## 금지 규칙

- `@JsonIgnoreProperties(ignoreUnknown = true)`를 생략하지 않는다.
- `@JsonProperty`를 일부 필드에만 붙이지 않는다.
- 외부 스키마에 없는 필드를 DTO에 임의로 추가하지 않는다.
- DTO에 비즈니스 메서드를 추가하지 않는다.
- 외부 응답 구조를 플랫하게 병합하지 않는다.
- ErrorCode enum이나 Exception을 DTO 파일 안에 포함하지 않는다.
- DTO에서 도메인 타입 변환을 수행하지 않는다.

## 예외와 경계

- 외부 스키마가 매우 큰 경우 기능별 DTO 파일 분리를 검토할 수 있다.
- nullable 여부가 문서와 실제 응답에서 다르면 실제 관찰과 parsing failure 정책을 문서화한다.
- 내부 Port 타입과 이름이 비슷해도 external DTO와 application DTO는 분리한다.

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] Provider DTO가 외부 JSON 구조를 그대로 표현한다.
- [ ] JSON property와 unknown field 허용 정책이 모든 DTO에 일관 적용되어 있다.
- [ ] 도메인 타입 변환이 DTO가 아니라 Adapter에서 수행된다.
