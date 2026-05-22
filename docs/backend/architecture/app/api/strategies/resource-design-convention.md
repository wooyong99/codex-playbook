# Resource Design 컨벤션

이 문서는 REST URI 네이밍과 resource 단위 설계 기준을 정리한다.

## 목적

- API URL을 행위 중심이 아니라 resource 중심으로 설계한다.
- path, query, HTTP method의 의미를 일관되게 만든다.
- version, pagination, tenant context 같은 반복 결정을 endpoint마다 다르게 하지 않게 한다.

## 적용 범위

- REST API public endpoint path
- resource collection, item, sub-resource 설계
- path variable, query parameter, HTTP method 선택
- list endpoint의 pagination request parameter

API version의 생명주기와 breaking change 기준은 [api-versioning-convention](api-versioning-convention.md)이 소유한다.
Pagination response 구조는 [support/api response envelope](../../../support/api/strategies/response-envelope-convention.md)이 소유한다.

## 책임

- resource 이름과 URI segment 형식을 정한다.
- 행위성 operation을 resource로 표현할지 별도 endpoint로 둘지 판단한다.
- 식별자와 filter를 path와 query로 구분한다.
- HTTP method와 status의 기본 의미를 정한다.

## 전체 흐름

```text
업무 기능
  -> resource 식별
  -> collection/item/sub-resource 결정
  -> HTTP method 선택
  -> path/query parameter 분리
  -> version prefix 적용
```

## 세부 규칙

### URI 기본 형식

- 기본 path는 `/api/v{N}/{resources}`다.
- resource segment는 복수형 명사와 kebab-case를 사용한다.
- admin 전용 API는 `/api/v{N}/admin/{resources}`를 사용한다.
- singleton resource만 단수형을 허용한다.

```text
GET  /api/v1/orders
GET  /api/v1/orders/{orderId}
POST /api/v1/orders
GET  /api/v1/order-items
GET  /api/v1/me
```

### HTTP method

| Method | 의미 | 예시 |
|--------|------|------|
| `GET` | 조회 | `GET /api/v1/orders/{orderId}` |
| `POST` | 생성 또는 command resource 생성 | `POST /api/v1/orders` |
| `PUT` | 전체 대체 | `PUT /api/v1/orders/{orderId}` |
| `PATCH` | 부분 변경 | `PATCH /api/v1/orders/{orderId}` |
| `DELETE` | 삭제 | `DELETE /api/v1/orders/{orderId}` |

### 행위와 상태 전이

URL에 동사를 직접 노출하지 않는다. 상태 전이와 command성 행위는 하위 resource로 표현한다.

```text
POST /api/v1/orders/{orderId}/cancellations
POST /api/v1/orders/{orderId}/confirmations
POST /api/v1/files/{fileId}/moves
```

아래 방식은 사용하지 않는다.

```text
POST /api/v1/orders/{orderId}/cancel
GET  /api/v1/orders/get-detail/{orderId}
POST /api/v1/do-something
```

### Path와 Query

- resource를 고유하게 식별하는 값은 path parameter로 둔다.
- filter, search, sort, pagination은 query parameter로 둔다.
- 복수 ID 일괄 조회는 query parameter를 사용한다.
- tenant ID는 URL path에 노출하지 않고 header, token, session context로 해석한다.

```text
GET /api/v1/orders/{orderId}/items/{itemId}
GET /api/v1/orders?status=PENDING&sort=createdAt,desc
GET /api/v1/orders?ids=1,2,3
```

### Pagination request

- list endpoint에만 pagination을 적용한다.
- 기본은 cursor 기반을 우선 검토한다.
- 총 개수와 page jump가 필요한 관리자 테이블은 offset 기반을 사용할 수 있다.
- 하나의 endpoint에서 cursor와 offset 방식을 동시에 제공하지 않는다.
- `size` 기본값은 20, 상한은 100으로 제한한다.

## 금지 규칙

- URI에 동사를 노출하지 않는다.
- URI segment에 snake_case, camelCase, PascalCase를 사용하지 않는다.
- collection resource를 단수형으로 만들지 않는다. singleton 예외만 허용한다.
- resource 고유 식별자를 query parameter로 받지 않는다.
- filter, sort, pagination을 path variable로 받지 않는다.
- URL path에 `tenantId`, tenant slug 같은 tenant 식별자를 노출하지 않는다.
- `Accept` header versioning으로 API version을 관리하지 않는다.
- 하나의 endpoint에서 cursor pagination과 offset pagination을 섞지 않는다.

## 예외와 경계

- `/api/v1/me`, `/api/v1/current-tenant`처럼 요청 context에서 하나만 존재하는 singleton은 단수형을 허용한다.
- Webhook, OAuth callback, 파일 download처럼 외부 protocol이 path를 요구하면 protocol path를 우선할 수 있다.
- 검색 자체가 독립 resource로 관리되면 `/search-results` 같은 resource를 둘 수 있다.

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] URL path만으로 resource와 상위 관계가 식별된다.
- [ ] path와 query의 역할이 구분되어 있다.
- [ ] 상태 전이 operation이 동사 URL이 아니라 resource로 표현되어 있다.
- [ ] version prefix가 [api-versioning-convention](api-versioning-convention.md)을 따른다.
