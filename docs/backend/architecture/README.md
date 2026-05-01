# Backend Architecture

백엔드 아키텍처 문서의 단일 진입점.

## 아키텍처 단위

| 단위 | 코드 위치 | 주요 책임 | 의존 대상 | 사용 주체 |
|------|-----------|-----------|-----------|-----------|
| `app` | `app` module/package | HTTP 진입점, Request/Response 변환, 예외 응답 | `application` | Client / API caller |
| `application` | `application` module/package | UseCase 실행, 흐름 조율, 트랜잭션 경계 | `domain`, outbound port | `app`, event/CLI entry |
| `domain` | `domain` module/package | 비즈니스 개념, 불변식, 도메인 예외 | 없음 | `application` |
| `storage` | `storage` infrastructure module/package | 저장소 Port 구현, Entity 변환, DDL | `application`, `domain`, database | `application` |
| `external` | `external` infrastructure module/package | 외부 API Port 구현, 외부 오류/응답 번역 | `application`, external systems | `application` |

## 의존 방향

```text
app -> application -> domain
storage -> application -> domain
external -> application -> domain
```

## 문서 구조

- [app](./app/app-guidelines.md) - HTTP 표현 계층 경계와 Controller/DTO 전략을 확인할 때
- [application](./application/application-guidelines.md) - UseCase, Flow, Validator, Handler, Policy 경계를 확인할 때
- [domain](./domain/domain-guidelines.md) - 도메인 모델, 불변식, 도메인 예외 경계를 확인할 때
- [storage](./storage/storage-guidelines.md) - 저장소 Adapter, Entity, DDL, QueryDsl 전략을 확인할 때
- [external](./external/external-guidelines.md) - 외부 API Adapter, ApiClient, Mock 전략을 확인할 때

## 관련 정책

- [policies/security](../policies/security.md) - 인증/인가와 민감 정보 처리
- [policies/logging](../policies/logging.md) - 로깅 형식과 민감 정보 차단
- [policies/transaction-and-consistency](../policies/transaction-and-consistency.md) - 트랜잭션 경계와 정합성
- [policies/concurrency-and-performance](../policies/concurrency-and-performance.md) - 동시성 제어와 성능

## 운영 원칙

- architecture 단위가 추가·삭제·개편되면 이 README를 먼저 갱신한다.
- 세부 전략 문서 목록은 각 단위의 `{actual-unit}-guidelines.md`와 `strategies/README.md`가 소유한다.
- 백엔드 문서 홈은 이 README만 참조하고, 아키텍처 단위 내부 세부 링크는 각 단위 문서가 소유한다.

## Playbook compatibility

- 현재 구조는 codex-playbook의 기본 개념 단위(`app`, `application`, `domain`, `storage`, `external`)를 사용한다.
- 실제 프로젝트에 적용할 때는 `$reverse-engineer-backend-docs`의 `migrate` 모드로 실제 모듈·패키지·책임 단위 중심 구조로 교체한다.
