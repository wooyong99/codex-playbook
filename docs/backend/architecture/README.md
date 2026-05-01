# Backend Architecture

백엔드 아키텍처 문서의 단일 진입점.

이 디렉토리는 백엔드 코드베이스의 아키텍처 단위, 의존 경계, 구현 전략을 설명한다. 백엔드 문서 홈(`docs/backend/README.md`)은 개별 아키텍처 문서가 아니라 이 README를 참조한다.

## 현재 상태

현재 문서 구조는 codex-playbook의 개념 레이어(`app`, `application`, `domain`, `storage`, `external`)를 기준으로 구성되어 있다. 실제 코드베이스 기반 문서로 전환할 때는 `$reverse-engineer-strategies`의 `migrate` 모드를 사용해 실제 모듈·패키지·책임 단위 중심 구조로 교체한다.

## 문서 맵

| 영역 | 진입점 | 설명 |
|------|--------|------|
| 문서 작성 규칙 | [documentation-convention.md](documentation-convention.md) | 아키텍처 문서 작성·관리 규칙 |
| 표현 계층 | [app/app-layer-guidelines.md](app/app-layer-guidelines.md) | Controller, DTO, 예외 처리 |
| 응용 계층 | [application/application-layer-guidelines.md](application/application-layer-guidelines.md) | UseCase, Flow, Validator |
| 도메인 계층 | [domain/domain-layer-guidelines.md](domain/domain-layer-guidelines.md) | Entity, Value Object, 도메인 규칙 |
| 저장소 계층 | [storage/storage-layer-guidelines.md](storage/storage-layer-guidelines.md) | DB 어댑터, Repository, DDL |
| 외부 연동 계층 | [external/external-layer-guidelines.md](external/external-layer-guidelines.md) | 외부 API 어댑터, ApiClient |

## Strategies

각 영역의 `strategies/README.md`는 해당 영역에서 관찰되거나 정의된 세부 구현 전략의 진입점이다.

- [app/strategies/README.md](app/strategies/README.md)
- [application/strategies/README.md](application/strategies/README.md)
- [domain/strategies/README.md](domain/strategies/README.md)
- [storage/strategies/README.md](storage/strategies/README.md)
- [external/strategies/README.md](external/strategies/README.md)

## Migration 방침

`$reverse-engineer-strategies`를 사용할 때는 먼저 `inspect` 수준의 사전 판단을 수행한다.

- 기존 구조가 실제 코드 구조와 충돌하지 않으면 `merge`로 보강한다.
- 기존 구조가 플레이북 개념 레이어 중심이고 실제 코드 구조와 충돌하면 `migrate`로 전환한다.
- `generate`는 비어 있거나 충돌 없는 문서 트리에만 새 문서를 추가한다.
- `migrate`가 실행되면 이 README는 실제 아키텍처 단위, 코드 위치, 책임, 의존 방향, 하위 단위 링크를 포함하는 아키텍처 맵 중심으로 갱신된다.

## 운영 원칙

- 아키텍처 하위 디렉토리나 세부 전략 문서가 추가·삭제·개편되면 이 README의 문서 맵을 갱신한다.
- 백엔드 문서 홈은 이 README만 참조하고, 아키텍처 내부 세부 링크는 이 README가 소유한다.
