# API Versioning 컨벤션

이 문서는 app 계층 REST API version 관리 규칙을 정리한다.

## 목적

- breaking change가 기존 클라이언트 계약을 조용히 깨지 않게 한다.
- version path, Controller package, DTO 분리 기준을 일관되게 만든다.
- additive change와 breaking change를 구분한다.

## 적용 범위

- REST API path version
- version별 Controller와 DTO 공존
- deprecation, migration, compatibility 정책
- OpenAPI version 문서화

URI resource 설계는 [resource-design-convention](resource-design-convention.md)이 소유한다.
Version별 package 배치는 [package-structure](package-structure.md)가 소유한다.

## 책임

- API version을 path로 노출하는 기준을 정한다.
- breaking change 시 새 version을 만드는 기준을 정한다.
- version 공존 기간에 Controller와 DTO를 어떻게 분리할지 정한다.
- deprecated endpoint의 문서화와 제거 조건을 정한다.

## 전체 흐름

```text
API 변경 요청
  -> additive change 여부 판단
  -> breaking change면 새 /api/v{N} 설계
  -> version별 Controller/DTO 분리
  -> OpenAPI deprecation and migration 문서화
```

## 세부 규칙

### Version 형식

- REST API version은 path prefix `/api/v{N}`으로 표현한다.
- 현재 기본 version은 `/api/v1`이다.
- `Accept` header versioning, query parameter versioning은 사용하지 않는다.
- admin API도 `/api/v{N}/admin/...` 형식을 따른다.

### Additive change

아래 변경은 기존 version 안에서 처리할 수 있다.

- response에 optional field 추가
- 기존 enum에 하위 호환 가능한 값 추가
- 신규 endpoint 추가
- 기존 request에 optional query parameter 추가
- OpenAPI description, example, error documentation 보강

### Breaking change

아래 변경은 새 version을 검토한다.

- 기존 response field 제거 또는 의미 변경
- required request field 추가
- 기존 field type, enum 의미, date format 변경
- HTTP method 또는 URI resource 의미 변경
- pagination 방식 변경
- error code 의미 변경
- nullable contract 변경

### Version 공존

- v1과 v2가 동시에 운영되면 app 계층 Controller와 DTO를 version별로 분리한다.
- application UseCase는 API version을 직접 알지 않는다.
- version별 차이는 app DTO와 mapping Extension에서 흡수한다.
- 공통 business behavior는 같은 UseCase를 호출한다.

### Deprecation

- deprecated endpoint는 OpenAPI에 표시한다.
- 대체 endpoint와 migration deadline을 문서화한다.
- 제거 전에는 사용량과 client migration 상태를 확인한다.

## 금지 규칙

- breaking change를 기존 `/api/v1` endpoint에 덮어쓰지 않는다.
- API version을 query parameter나 `Accept` header로 관리하지 않는다.
- application UseCase 이름이나 package에 API version을 전파하지 않는다.
- 하나의 DTO에 v1/v2 조건 분기를 누적하지 않는다.
- deprecated endpoint를 OpenAPI에서 먼저 삭제하지 않는다.
- response field 의미를 바꾸면서 version을 올리지 않는 방식으로 호환성을 깨지 않는다.

## 예외와 경계

- 아직 외부 client가 없는 내부 개발 endpoint는 version bump 대신 기존 endpoint를 정리할 수 있다.
- 보안 취약점 대응처럼 즉시 변경이 필요한 경우 migration 기간 없이 breaking fix를 적용할 수 있지만 변경 기록을 남긴다.
- provider callback API는 provider version 정책을 우선할 수 있다.

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] 변경이 additive인지 breaking인지 PR, 설계 문서, 또는 변경 문서에 명시되어 있다.
- [ ] breaking change는 새 version path 또는 명시된 예외 기록을 가진다.
- [ ] version별 Controller와 DTO 차이가 app 계층 안에 격리되어 있다.
