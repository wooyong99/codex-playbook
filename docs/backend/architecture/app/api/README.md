# App API Architecture

이 문서는 `backend/app/api` 아키텍처 단위의 책임, 하위 API 애플리케이션 문서, 의존 경계를 안내한다.

## 목적

- HTTP API 애플리케이션 진입점의 공통 책임과 전략 문서 위치를 정리한다.
- `admin`, `operator`, `user` API가 같은 Controller, DTO, resource, versioning 기준을 사용하게 한다.
- API 공통 지원 경계와 application 계약 호출 경계를 문서로 분리한다.

## 적용 범위

- `backend/app/api/admin`
- `backend/app/api/operator`
- `backend/app/api/user`
- Controller, Request/Response DTO, API resource, API 문서화, versioning

공통 응답 envelope, 예외 응답, trace, tenant, rate limit 같은 API 공통 지원은 [support/api](../../support/api/api-guidelines.md)가 소유한다.

## 모듈 맵

| 모듈 | 문서 | 책임 |
|------|------|------|
| `app/api` | [api-guidelines](./api-guidelines.md) | API 애플리케이션 공통 경계 |
| `app/api/admin` | 전용 문서 없음 | 관리자 API 진입점 |
| `app/api/operator` | 전용 문서 없음 | 운영자 API 진입점 |
| `app/api/user` | 전용 문서 없음 | 플랫폼 사용자 API 진입점 |
| `app/api/strategies` | [strategies](./strategies/README.md) | Controller, DTO, resource, API 문서화 전략 |

## 의존 경계

```text
app/api/* -> support/api -> core/application -> core/domain
app/api/* -> core/application -> core/domain
```

`app/api`는 HTTP 표현 계층을 application 계약으로 변환하는 경계를 소유한다. 공통 응답 envelope, 예외 응답, trace, tenant, rate limit은 `support/api` 규약을 따른다.

## 문서 운영 원칙

- API 애플리케이션이 추가되면 이 README의 모듈 맵을 먼저 갱신한다.
- API 공통 책임과 완료 체크리스트는 `api-guidelines.md`가 소유한다.
- Controller, DTO, resource, 문서화, versioning 반복 구현 방식은 `strategies/README.md`가 소유한다.
