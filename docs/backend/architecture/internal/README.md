# Internal Architecture

이 문서는 `backend/internal` 아키텍처 단위의 책임, 하위 모듈 문서, 의존 경계를 안내한다.

## 목적

- 내부 인프라 구현을 application Port 계약 밖으로 새지 않게 격리한다.
- persistence와 내부 adapter 후보 모듈의 문서 위치를 안내한다.
- 신규 내부 인프라 모듈을 추가할 때 문서 위치와 의존 방향을 같은 기준으로 판단하게 한다.

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

```text
internal/* -> core/application -> core/domain
internal/* -> infrastructure providers
```

`internal/*` 모듈은 `core/application`이 선언한 Port나 `core/domain` 모델을 구현 세부사항으로 연결하는 방향을 기본으로 한다. 인프라 모델, provider SDK 타입, 저장 기술 세부사항은 application Port 시그니처로 노출하지 않는다.

## 문서 운영 원칙

- 하위 모듈이 추가되면 이 README의 모듈 맵을 먼저 갱신한다.
- 모듈별 책임과 완료 기준은 각 `{module}-guidelines.md`가 소유한다.
- 반복 구현 방식과 인프라별 선택 기준은 가장 가까운 `strategies/README.md`가 소유한다.
