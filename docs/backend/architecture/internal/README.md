# Internal Architecture

## 목적

`backend/internal` 하위 내부 인프라 모듈의 책임과 문서 위치를 안내한다.

## 적용 범위

- `backend/internal/cache`
- `backend/internal/messaging`
- `backend/internal/observability`
- `backend/internal/object-storage`
- `backend/internal/persistence`
- `backend/internal/security`

## 모듈 맵

| 모듈 | 문서 | 책임 |
|------|------|------|
| `internal/cache` | [cache](./cache/cache-guidelines.md) | 캐시 adapter 후보 모듈 |
| `internal/messaging` | [messaging](./messaging/messaging-guidelines.md) | 메시징 adapter 후보 모듈 |
| `internal/observability` | [observability](./observability/observability-guidelines.md) | 관측성 adapter 후보 모듈 |
| `internal/object-storage` | [object-storage](./object-storage/object-storage-guidelines.md) | 객체 저장소 adapter 후보 모듈 |
| `internal/persistence` | [persistence](./persistence/persistence-guidelines.md) | JPA, QueryDsl, 저장소 adapter |
| `internal/security` | [security](./security/security-guidelines.md) | 보안 adapter 후보 모듈 |

## 의존 경계

`internal/*` 모듈은 `core/application`이 선언한 포트나 `core/domain` 모델을 구현 세부사항으로 연결하는 방향을 기본으로 한다.
