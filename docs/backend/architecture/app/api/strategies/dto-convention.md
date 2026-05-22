# DTO 컨벤션

이 문서는 app 계층의 Request/Response DTO, nullable, optional 처리 기준을 정리한다.

## 목적

- HTTP API 계약 DTO와 application `Command` / `Result` 계약을 분리한다.
- DTO field의 required, nullable, optional 의미를 명확하게 만든다.
- API 전용 response shape가 필요할 때만 Response DTO를 만들게 한다.

## 적용 범위

- `@RequestBody`, `@RequestParam`, `@PathVariable`로 들어오는 app Request DTO
- 클라이언트에 반환하는 app Response DTO
- Request DTO와 application Command 사이의 변환 Extension
- application Result와 Response DTO 사이의 변환 Extension

Application 내부 DTO는 [application component DTO convention](../../../core/application/strategies/component-dto-convention.md)이 소유한다.
공통 응답 envelope는 [support/api response envelope](../../../support/api/strategies/response-envelope-convention.md)이 소유한다.

## 책임

- API 계약 field의 존재 여부, null 허용, 기본값 정책을 정의한다.
- Request DTO가 syntactic validation만 갖도록 제한한다.
- Response DTO 생성 기준과 생략 기준을 정한다.
- DTO 변환 책임을 DTO 외부 Extension으로 분리한다.

## 전체 흐름

```text
Request DTO
  -> validation annotation
  -> {Domain}DtoExtension.toCommand()
  -> application Command

application Result
  -> {Domain}DtoExtension.toResponse() optional
  -> Response DTO | direct Result
  -> BaseResponse
```

## 세부 규칙

### Request DTO

- Request DTO는 app 계층의 외부 API 계약이다.
- 필수 입력은 non-null type으로 선언하고 validation annotation을 함께 둔다.
- 선택 입력은 nullable type으로 선언하되 null의 의미를 문서화한다.
- 변환 로직은 DTO 내부 method가 아니라 `{Domain}DtoExtension.kt`에 둔다.
- DB 조회, 중복, 권한, 상태 판단은 Request DTO validation에 넣지 않는다.

```kotlin
data class CreateOrderRequest(
    @field:NotBlank
    val name: String,

    @field:Size(max = 1000)
    val memo: String?,
)
```

### Nullable 기준

- required field는 non-null로 둔다.
- optional filter, optional memo, 아직 값이 없을 수 있는 response field만 nullable로 둔다.
- `null`이 "요청하지 않음", "값 삭제", "알 수 없음" 중 무엇인지 모호하면 nullable 하나로 표현하지 않는다.
- null field를 JSON에서 생략할지 포함할지는 response envelope와 serialization 정책으로 통일한다.

### Optional 처리 기준

부분 수정 API에서는 field가 빠진 경우와 명시적 null을 구분해야 한다.

- "변경하지 않음"과 "값 제거"를 구분해야 하면 `OptionalField<T>`, `JsonNullable<T>` 같은 명시 타입을 사용한다.
- 명시 타입을 도입하지 않으면 endpoint를 분리하거나 command resource를 분리한다.
- `String?` 하나로 absent와 null clear를 동시에 표현하지 않는다.

```text
PATCH /api/v1/users/{userId}

field absent  -> 변경하지 않음
field null    -> 값을 제거함
field value   -> 값 변경
```

### Response DTO

기본은 application `Result`를 공통 envelope로 반환한다. 아래 조건에 해당할 때만 app Response DTO를 만든다.

- API 전용 field 이름이나 shape가 필요하다.
- 특정 field를 숨기거나 조합해야 한다.
- 날짜, 금액, enum 등 serialization format을 API 계약으로 고정해야 한다.
- API version별 응답 차이가 존재한다.
- 여러 application Result를 하나의 API response로 조합한다.

### DTO 변환

- Request DTO -> Command 변환은 `{Domain}DtoExtension.kt`가 담당한다.
- Result -> Response DTO 변환도 `{Domain}DtoExtension.kt`가 담당한다.
- DTO 파일은 순수 data shape와 validation annotation만 가진다.
- 변환 Extension은 app 계층에 있고 application 또는 domain 내부로 이동하지 않는다.

## 금지 규칙

- application `Command`를 `@RequestBody`로 직접 받지 않는다.
- Request DTO 내부에 `toCommand()` method를 만들지 않는다.
- Request DTO에서 repository, Port, UseCase를 호출하지 않는다.
- DTO nullable field를 편의상 열어두고 계약 의미를 생략하지 않는다.
- PATCH 요청에서 absent와 explicit null을 `String?` 하나로 뭉개지 않는다.
- Response DTO에 domain Entity, JPA Entity, external API DTO를 직접 노출하지 않는다.
- 단순히 파일을 맞추기 위해 불필요한 Response DTO를 만들지 않는다.
- app Request/Response DTO를 application `dto/`에 두지 않는다.

## 예외와 경계

- 내부 admin API라도 외부 HTTP 계약이면 app DTO 규칙을 따른다.
- 파일 업로드나 multipart request는 DTO 대신 parameter binding을 사용할 수 있지만 Command 변환 경계는 유지한다.
- response가 application Result와 완전히 같아도 OpenAPI schema 이름을 분리해야 하면 Response DTO를 만들 수 있다.

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] Request DTO, application Command, Response DTO의 책임이 분리되어 있다.
- [ ] nullable과 optional field의 의미가 API 계약, DTO schema, 또는 OpenAPI 문서에 명시되어 있다.
- [ ] DTO 변환이 DTO 내부가 아니라 app Extension에 모여 있다.
