# Storefront Domain Access Backend TDD

> 작성일: 2026-05-22
> 상태: Draft
> 대상 모듈: `backend/app/api/user`, `backend/core/application`, `backend/core/domain`

## 1. 설계 배경 및 목적

### 1.1 배경

PRD는 쇼핑몰 방문자가 회원가입 시 입력된 `domainVariable`을 path variable로 사용해 SSR 쇼핑몰에 접속해야 한다고 정의한다. 현재 backend는 `PlatformAuthService.register`에서 `PlatformAccount`를 생성하며, 계정 안에 `PUBLISHED` 기본 스킨과 `ACTIVE` 쇼핑몰을 함께 저장한다. 그러나 외부 방문자 또는 frontend/server runtime이 `domainVariable`로 활성 쇼핑몰을 조회하고 `activeSkinId`가 가리키는 스킨 HTML을 얻을 application/API 계약은 아직 없다.

이번 설계는 SSR 렌더링 엔진을 backend에 넣지 않고, SSR runtime이 사용할 수 있는 HTML payload 조회 계약을 backend에 추가하는 것을 목표로 한다.

### 1.2 설계 목표

1. **`domainVariable` 기반 storefront 조회 계약 제공**: visitor 경로를 처리하는 runtime이 backend에서 활성 쇼핑몰과 활성 스킨 HTML을 조회할 수 있어야 한다.
2. **계층 경계 유지**: HTTP path variable 검증과 응답 envelope은 `app/api/user`에 두고, 쇼핑몰/스킨 조회 정책은 `core/application`에 둔다.
3. **현재 InMemory 저장소 제약 안에서 구현**: 영속 DB, asset 저장소, FsNode, 퍼블리시 흐름은 제외하고 현재 `PlatformAccountStore`를 확장해 조회한다.
4. **정보 노출 제한**: 존재하지 않거나 비활성인 storefront는 owner, email, 내부 계정 상태를 노출하지 않는 공통 오류로 응답한다.

### 1.3 설계 비목표

- 플랫폼 관리자 스킨 등록/수정/삭제는 제외한다.
- 플랫폼 사용자 스킨 CRUD, 다운로드, 실시간 미리보기, 퍼블리시는 제외한다.
- FsNode 생성 또는 FsNode 기반 SSR 재현은 제외한다.
- 영속 DB 저장소, migration, 외부 object storage, 외부 domain/DNS 연결은 제외한다.
- frontend 화면과 SSR 렌더링 엔진 구현은 제외한다.

### 1.4 기술적 제약사항

- **아키텍처 제약**: Controller는 request binding, syntactic validation, application 호출, response 변환만 담당한다. Domain 모델을 response DTO로 직접 노출하지 않는다.
- **Application 제약**: 조회 유스케이스는 `core/application`에서 `PlatformAccountStore` 계약을 통해 domain 객체를 조회하고, storage 구현체를 직접 참조하지 않는다.
- **Domain 제약**: `PlatformAccount`, `Shop`, `Skin`은 framework-independent 모델로 유지한다. HTTP status나 응답 메시지는 domain에 들어가지 않는다.
- **인프라 제약**: 현재 저장소는 `InMemoryPlatformAccountStore`이며, 신규 DB schema나 migration은 만들지 않는다.
- **비기능 요구사항**: M1 범위에서는 단일 in-memory map 조회를 기준으로 한다. 캐시, 분산 락, asset streaming은 도입하지 않는다.

## 2. 현행 시스템 분석

### 2.1 관련 도메인 구조

```text
PlatformAccount
  -> PlatformUser
  -> Skin(defaultSkin)
  -> Shop(activeSkinId -> Skin.id)
```

현재 `PlatformAccount`가 사용자, 기본 스킨, 쇼핑몰을 하나의 in-memory 저장 단위로 보유한다. `Shop.activeSkinId`는 같은 account의 `defaultSkin.id`를 참조한다.

### 2.2 현재 처리 흐름

```text
POST /api/v1/platform/auth/signup
  -> PlatformAuthController
  -> PlatformAuthService.register
  -> PlatformAccount 생성
  -> PlatformAccountStore.register
  -> InMemoryPlatformAccountStore(accountsByEmail, accountsByDomainVariable)에 저장
```

현재 public contract로 노출된 저장소 조회는 `findByEmail(email)`뿐이다. `accountsByDomainVariable` map은 중복 검증과 저장에만 쓰이고 storefront 조회 계약으로는 노출되지 않는다.

### 2.3 현행 스키마 분석

| 테이블 | 주요 필드 | 현재 역할 | 변경 필요성 |
|--------|-----------|-----------|-------------|
| 해당 없음 | 해당 없음 | 영속 DB를 사용하지 않고 in-memory domain 객체를 저장한다. | 이번 마일스톤에서는 schema 변경 없음 |

## 3. 아키텍처 설계

### 3.1 계층별 책임 분배

| 계층 | 구성 요소 | 책임 | 설계 근거 |
|------|-----------|------|-----------|
| App | `StorefrontController` | `GET /api/v1/storefronts/{domainVariable}/ssr-payload` 수신, path variable 전달, `ApiResponse` 반환 | visitor-facing SSR payload는 HTTP 표현 계약이므로 app/api가 소유 |
| App | `StorefrontSsrPayloadResponse` | `domainVariable`, `skinId`, `templateKey`, `html` 응답 DTO | Domain 모델 직접 노출 금지 기준 준수 |
| Application | `StorefrontQueryService` | `domainVariable` 정규화/검증, account 조회, active shop 및 published skin 검증, 결과 조립 | application은 domain과 store를 조합해 유스케이스 완성 |
| Application | `GetStorefrontSsrPayloadQuery`, `StorefrontSsrPayloadResult` | API 입력/출력과 분리된 application 계약 | Controller가 application command/query 타입을 HTTP binding에 직접 쓰지 않게 함 |
| Application | `PlatformAccountStore.findByDomainVariable` | 기존 in-memory 저장소의 domainVariable 조회 계약 추가 | 현재 store가 domainVariable index를 이미 갖고 있으므로 최소 변경 |
| Domain | `Shop`, `Skin`, `ShopStatus`, `SkinStatus` | 활성 쇼핑몰과 게시 스킨 상태의 원천 데이터 | 상태 값은 domain 소유, HTTP 매핑은 app에서 처리 |
| Storage | `InMemoryPlatformAccountStore` | normalized domainVariable로 account 반환 | 영속 DB 도입 제외 조건 준수 |

### 3.2 처리 흐름

```text
GET /api/v1/storefronts/{domainVariable}/ssr-payload
  -> StorefrontController
  -> GetStorefrontSsrPayloadQuery(domainVariable)
  -> StorefrontQueryService.getSsrPayload
  -> PlatformAccountStore.findByDomainVariable(normalizedDomainVariable)
  -> Shop ACTIVE 확인
  -> account.defaultSkin.id == shop.activeSkinId 확인
  -> Skin PUBLISHED 확인
  -> StorefrontSsrPayloadResult
  -> StorefrontSsrPayloadResponse
  -> ApiResponse.success(...)
```

### 3.3 설계 대안 분석

| 대안 | 장점 | 단점 | 채택 여부 | 사유 |
|------|------|------|-----------|------|
| `PlatformAuthService`에 storefront 조회 메서드 추가 | 기존 store와 validation helper를 재사용하기 쉽다 | 인증/회원가입 책임과 visitor storefront 조회 책임이 섞인다 | 기각 | service 책임이 커지고 app endpoint 의미가 흐려진다 |
| 별도 `StorefrontQueryService` 추가 | visitor 조회 책임이 명확하고 향후 DB/퍼블리시 조회로 분리하기 쉽다 | 작은 클래스가 하나 추가된다 | 채택 | 계층 책임과 future migration 경계를 가장 덜 흔든다 |
| `/{domainVariable}`를 backend API endpoint로 직접 제공 | PRD의 visitor path와 유사하다 | `/api`, `/login` 등 platform route와 충돌하고 SSR runtime 책임과 backend API 책임이 섞인다 | 기각 | backend는 SSR payload API를 제공하고 visitor path 라우팅은 frontend/server runtime이 맡는 것이 요구사항에 맞다 |
| `GET /api/v1/storefronts/{domainVariable}/ssr-payload` 제공 | API versioning과 resource path가 명확하고 visitor path 충돌을 피한다 | SSR runtime이 별도 backend API를 호출해야 한다 | 채택 | app/api resource convention과 SSR runtime 분리 요구를 동시에 만족한다 |

## 4. 도메인 모델 설계

### 4.1 애그리거트 경계

이번 마일스톤에서는 기존 `PlatformAccount` 저장 단위를 유지한다. `Shop.activeSkinId`는 같은 account 안의 `Skin.id`를 참조하며, application이 조회 시 두 값을 조합한다.

별도 `Storefront` domain aggregate는 만들지 않는다. 현재 요구는 상태 변경이 없는 조회이며, 신규 aggregate를 만들면 영속 모델이 없는 상태에서 개념만 늘어난다.

### 4.2 도메인 모델 상세

#### `Shop`

- 역할: 쇼핑몰 방문자가 접근할 storefront 식별자와 활성 스킨 참조를 보유한다.
- 불변식: `domainVariable`은 회원가입 시 정규화/검증된 값이어야 한다. `activeSkinId`는 렌더링에 사용할 스킨 ID를 가리켜야 한다.
- 주요 행위: 이번 마일스톤에서는 상태 변경 행위를 추가하지 않는다.
- 상태 전이: 현재 `ACTIVE`만 존재한다. 조회 시 `ACTIVE`가 아니면 visitor에게 노출하지 않는다.

#### `Skin`

- 역할: SSR runtime에 전달할 HTML source와 template key를 보유한다.
- 불변식: storefront 조회에 사용할 스킨은 `PUBLISHED` 상태여야 한다.
- 주요 행위: 이번 마일스톤에서는 HTML 편집, 다운로드, 퍼블리시 행위를 추가하지 않는다.
- 상태 전이: 현재 `PUBLISHED`만 존재한다. 조회 시 `PUBLISHED`가 아니면 visitor에게 노출하지 않는다.

#### `StorefrontSsrPayloadResult`

- 역할: application 조회 결과를 app response DTO로 넘기는 read model이다.
- 포함 값: `domainVariable`, `skinId`, `templateKey`, `html`.
- 제외 값: owner user id, email, password hash, shop 내부 id.

### 4.3 데이터 스키마 설계

해당 없음. 이번 마일스톤은 영속 DB 저장소 도입을 명시적으로 제외한다.

### 4.4 데이터 변환 흐름

```text
HTTP path variable
  -> GetStorefrontSsrPayloadQuery
  -> normalized domainVariable
  -> PlatformAccount domain object
  -> StorefrontSsrPayloadResult
  -> StorefrontSsrPayloadResponse
```

Domain 객체는 response DTO에 직접 노출하지 않는다. HTML 문자열은 현재 `SkinSource.html`에서 그대로 반환하되, sanitization이나 asset rewrite는 관리자 스킨 등록/퍼블리시 마일스톤에서 다룬다.

## 5. 트랜잭션 설계

### 5.1 트랜잭션 경계

| 연산 | 시작점 | 범위 | 격리 수준 | 사유 |
|------|--------|------|-----------|------|
| storefront SSR payload 조회 | `StorefrontQueryService.getSsrPayload` | normalized `domainVariable`로 account 1건 조회 후 in-memory 검증 | 해당 없음 | in-memory 조회이며 상태 변경이 없다 |

향후 DB 저장소로 전환하면 이 유스케이스는 읽기 전용 트랜잭션을 기본으로 한다.

### 5.2 정합성 보장 전략

이번 조회는 `Shop.activeSkinId`와 `Skin.id`의 일치, `ShopStatus.ACTIVE`, `SkinStatus.PUBLISHED`를 같은 account snapshot에서 확인한다. 불일치하면 partially valid payload를 반환하지 않고 storefront 미노출 오류로 처리한다.

### 5.3 이벤트 처리

해당 없음. 상태 변경과 외부 부수 효과가 없는 query 흐름이다.

## 6. 예외 및 실패 처리

### 6.1 예외 분류

| 예외 유형 | ErrorCode | 발생 조건 | Error Type | 사용자 메시지 |
|-----------|-----------|-----------|------------|---------------|
| validation | `VALIDATION_ERROR` | path variable이 domainVariable 형식에 맞지 않음 | 400 BAD_REQUEST | 입력값이 올바르지 않습니다. |
| not found | `STOREFRONT_NOT_FOUND` | domainVariable에 해당하는 account가 없음 | 404 NOT_FOUND | 요청한 쇼핑몰을 찾을 수 없습니다. |
| unavailable | `STOREFRONT_NOT_FOUND` | shop이 active가 아니거나 activeSkinId가 published skin과 연결되지 않음 | 404 NOT_FOUND | 요청한 쇼핑몰을 찾을 수 없습니다. |

비활성 shop, 미게시 skin, activeSkinId 불일치는 visitor에게 내부 상태를 구분해 노출하지 않는다.

### 6.2 실패 시나리오 및 복구 전략

| 시나리오 | 발생 가능성 | 영향 범위 | 복구 전략 |
|----------|-------------|-----------|-----------|
| domainVariable 대소문자 혼용 | 중간 | 정상 storefront를 못 찾을 수 있음 | application에서 trim/lowercase 정규화 후 조회 |
| 존재하지 않는 domainVariable 요청 | 높음 | visitor 1건 | 404 공통 오류 반환 |
| activeSkinId와 defaultSkin.id 불일치 | 낮음 | 해당 storefront | payload 반환 중단, 404로 내부 정합성 노출 차단 |
| HTML이 비어 있거나 잘못된 문서 | 낮음 | SSR runtime 렌더링 품질 | 이번 마일스톤에서는 저장된 HTML을 그대로 반환한다. 관리자 스킨 등록 검증 마일스톤에서 보완 |

### 6.3 멱등성 보장

조회 API이므로 멱등성 저장소나 idempotency key를 사용하지 않는다. 동일한 `domainVariable`과 같은 in-memory 상태에서는 같은 payload를 반환한다.

## 7. 동시성 및 성능

### 7.1 동시성 제어

| 경합 지점 | 제어 방식 | 구현 방법 | 사유 |
|-----------|-----------|-----------|------|
| `accountsByDomainVariable` 조회와 회원가입 저장 | 기존 store synchronization 유지 | `InMemoryPlatformAccountStore`의 public method에 `@Synchronized` 적용 | 현재 store는 map을 직접 사용하므로 같은 monitor로 읽기/쓰기를 보호한다 |

분산 락이나 낙관적 잠금은 도입하지 않는다. 멀티 인스턴스와 영속 DB가 이번 범위 밖이기 때문이다.

### 7.2 성능 고려사항

| 항목 | 우려 사항 | 대응 전략 | 측정 기준 |
|------|-----------|-----------|-----------|
| domainVariable 조회 | 선형 검색이면 가입자 수에 비례해 느려질 수 있음 | 이미 존재하는 `accountsByDomainVariable` map을 public 조회 계약으로 사용 | 단일 map lookup |
| HTML payload 크기 | 큰 HTML 응답 시 latency 증가 | 현재 기본 HTML만 반환. asset과 대용량 HTML 제한은 후속 스킨 관리 마일스톤에서 정의 | 확인 필요 |
| 캐시 | stale storefront HTML 가능성 | 이번 마일스톤에서는 캐시 미도입 | 해당 없음 |

### 7.3 확장 가능성

- `PlatformAccountStore.findByDomainVariable`는 향후 DB repository adapter로 대체 가능한 application port 역할을 한다.
- `StorefrontQueryService`는 후속 M6에서 `activeSkinId`가 default skin이 아니라 published FsNode 또는 user skin을 가리키도록 바뀌어도 app endpoint 계약을 유지할 수 있다.
- asset URL rewrite, HTML sanitization, version rollback은 이번 마일스톤에서 의도적으로 닫아 둔다.

## 8. 변경 파일 목록

| 파일 | 모듈 | 변경 유형 | 설명 |
|------|------|-----------|------|
| `backend/core/application/src/main/kotlin/com/wooyong/themeforge/core/application/platform/PlatformAuthService.kt` | core/application | 수정 | `PlatformAccountStore.findByDomainVariable` 추가 및 in-memory 구현 확장 |
| `backend/core/application/src/main/kotlin/com/wooyong/themeforge/core/application/storefront/StorefrontQueryService.kt` | core/application | 생성 | storefront SSR payload 조회 유스케이스와 error code 정의 |
| `backend/app/api/user/src/main/kotlin/com/wooyong/themeforge/app/api/user/storefront/StorefrontController.kt` | app/api/user | 생성 | public SSR payload endpoint와 DTO/exception mapping 추가 |
| `backend/app/api/user/src/main/kotlin/com/wooyong/themeforge/app/api/user/platform/PlatformAuthConfiguration.kt` | app/api/user | 수정 | `StorefrontQueryService` bean 등록 |
| `backend/core/application/src/test/kotlin/com/wooyong/themeforge/core/application/storefront/StorefrontQueryServiceTest.kt` | core/application test | 생성 | 정상 조회, validation, not found, inactive/mismatched skin 검증 |
| `backend/app/api/user/src/test/kotlin/com/wooyong/themeforge/app/api/user/storefront/StorefrontControllerTest.kt` | app/api/user test | 생성 | response envelope와 error mapping 검증 |

## 9. 검증 계획

| 시나리오 | 유형 | 검증 내용 | 예상 결과 |
|----------|------|-----------|-----------|
| 가입된 domainVariable로 SSR payload 조회 | unit/integration | 회원가입 후 `my-shop` 조회 | `domainVariable`, `skinId`, `templateKey`, `html` 반환 |
| 대문자 domainVariable 조회 | unit | `MY-SHOP` 조회 시 normalize 적용 | `my-shop` payload 반환 |
| invalid domainVariable 조회 | unit/integration | 형식에 맞지 않는 path variable | 400 `VALIDATION_ERROR` |
| 존재하지 않는 domainVariable 조회 | unit/integration | store에 account 없음 | 404 `STOREFRONT_NOT_FOUND` |
| activeSkinId 불일치 | unit | account의 shop activeSkinId가 defaultSkin.id와 다름 | 404 `STOREFRONT_NOT_FOUND` |
| controller response envelope | integration | API 응답 body 구조 | `ApiResponse.success(data=...)` 형식 |

## 10. 리스크와 미결정 사항

- `domainVariable` 예약어와 변경 가능 여부는 PRD에서 확인 필요로 남아 있다. 이번 마일스톤은 기존 회원가입 검증 규칙을 재사용한다.
- HTML sanitization, script 제한, asset 경로 rewrite는 관리자 스킨 등록과 퍼블리시 설계에서 결정해야 한다.
- 향후 DB 전환 시 `domainVariable` unique index와 active skin 참조 정합성 제약을 migration에서 별도로 설계해야 한다.
- SSR runtime이 backend API를 호출하는 내부 URL과 외부 visitor path `/{domainVariable}` 라우팅은 frontend/server runtime 설계에서 확정해야 한다.
