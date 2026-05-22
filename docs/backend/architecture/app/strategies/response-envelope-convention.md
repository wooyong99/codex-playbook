# Response Envelope 컨벤션

이 문서는 app 계층의 공통 응답 DTO와 pagination envelope 전략을 정리한다.

## 목적

- 성공 응답과 오류 응답의 최상위 JSON 구조를 일관되게 유지한다.
- Controller와 exception handler가 같은 response wrapper를 사용하게 한다.
- pagination metadata를 endpoint마다 다른 형태로 만들지 않게 한다.

## 적용 범위

- `BaseResponse<T>` 또는 프로젝트의 동등한 공통 응답 DTO
- `BaseError`
- cursor pagination, offset pagination response DTO
- 성공, 실패, empty response의 body 규칙

도메인별 Response DTO field는 [dto-convention](dto-convention.md)이 소유한다.
예외 매핑과 error code 선택은 [exception-response-convention](exception-response-convention.md)이 소유한다.

## 책임

- 최상위 response JSON shape를 정의한다.
- success body와 error body가 상호 배타적으로 존재하게 한다.
- pagination 응답의 공통 metadata 구조를 정의한다.
- HTTP status와 response body의 역할을 분리한다.

## 전체 흐름

```text
Success
  -> BaseResponse.success(data)
  -> { "data": ... }

Failure
  -> BaseResponse.error(error)
  -> { "error": { "code": "...", "message": "..." } }
```

## 세부 규칙

### 기본 응답 구조

성공 응답은 `data`를 가진다.

```json
{
  "data": {
    "id": 1,
    "name": "order"
  }
}
```

오류 응답은 `error`를 가진다.

```json
{
  "error": {
    "code": "ORDER_NOT_FOUND",
    "message": "주문을 찾을 수 없습니다."
  }
}
```

- `data`와 `error`는 동시에 존재하지 않는다.
- 성공 여부는 HTTP status로 판단한다.
- 별도 `success` boolean field는 두지 않는다.
- null field serialization은 프로젝트 Jackson 정책으로 통일한다.

### Empty 응답

- body가 필요 없는 삭제나 idempotent command는 `204 No Content`를 사용할 수 있다.
- body를 반환한다면 `BaseResponse.success(Unit)` 같은 프로젝트 표준을 하나로 정한다.
- 같은 API group 안에서 `204`와 empty envelope를 무작위로 섞지 않는다.

### Cursor pagination

```json
{
  "data": {
    "content": [],
    "page": {
      "size": 20,
      "nextCursor": "opaque-token",
      "hasNext": true
    }
  }
}
```

- cursor는 클라이언트가 해석하지 않는 opaque token이다.
- cursor pagination은 기본적으로 total count를 제공하지 않는다.
- `hasNext`와 `nextCursor` 의미를 endpoint마다 바꾸지 않는다.

### Offset pagination

```json
{
  "data": {
    "content": [],
    "page": {
      "page": 0,
      "size": 20,
      "totalElements": 100,
      "totalPages": 5
    }
  }
}
```

- `page`는 0부터 시작한다.
- `size`는 request size가 아니라 실제 적용된 size를 담는다.
- total count 비용이 큰 endpoint는 offset pagination을 신중히 선택한다.

## 금지 규칙

- 성공 응답에 `error`를 함께 담지 않는다.
- 오류 응답에 `data`를 함께 담지 않는다.
- HTTP status를 무시하고 body의 `success` field로 성공 여부를 표현하지 않는다.
- endpoint마다 page metadata field 이름을 다르게 만들지 않는다.
- cursor response에 `totalElements`를 기본으로 포함하지 않는다.
- error body에 stack trace, exception class, 내부 message를 포함하지 않는다.
- 도메인별 Response DTO가 `BaseResponse`를 직접 중첩해서 들고 있지 않게 한다.

## 예외와 경계

- streaming, file download, redirect, server-sent events는 envelope 적용 예외가 될 수 있다.
- 외부 provider callback response는 provider protocol을 우선할 수 있다.
- public API 호환성 때문에 기존 envelope를 유지해야 하면 versioning 문서에 예외를 기록한다.

## 완료 기준

- 모든 business API 성공 응답과 오류 응답의 최상위 구조가 통일되어 있다.
- pagination response가 cursor 또는 offset 중 하나의 표준 envelope를 따른다.
- Controller와 exception handler가 같은 공통 응답 DTO를 사용한다.
