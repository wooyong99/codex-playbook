# App Architecture

이 문서는 `backend/app` 아키텍처 단위의 책임, 하위 애플리케이션 문서, 의존 경계를 안내한다.

## 목적

- 외부 요청, 배치, worker 실행 트리거를 application 계약으로 넘기는 진입점 경계를 고정한다.
- API, batch, worker 애플리케이션의 문서 위치를 안내한다.
- 신규 애플리케이션 진입점을 추가할 때 문서 위치와 의존 방향을 같은 기준으로 판단하게 한다.

## 적용 범위

- `backend/app/api/admin`
- `backend/app/api/operator`
- `backend/app/api/user`
- `backend/app/batch`
- `backend/app/worker`

## 모듈 맵

| 모듈 | 문서 | 책임 |
|------|------|------|
| `app/api` | [api](./api/README.md) | HTTP API 애플리케이션 공통 전략 |
| `app/api/admin` | 전용 문서 없음 | 관리자 API 진입점 |
| `app/api/operator` | 전용 문서 없음 | 운영자 API 진입점 |
| `app/api/user` | 전용 문서 없음 | 플랫폼 사용자 API 진입점 |
| `app/batch` | 전용 문서 없음 | 배치 Job 애플리케이션 |
| `app/worker` | 전용 문서 없음 | 비동기 worker 애플리케이션 |

## 의존 경계

```text
app/* -> support/api -> core/application -> core/domain
app/* -> core/application -> core/domain
```

`app` 모듈은 외부 요청이나 실행 트리거를 받아 `core/application` 계약으로 넘기는 진입점이다. API 공통 응답, 예외, 필터는 `support/api`를 차용한다.

## 문서 운영 원칙

- 하위 애플리케이션이 추가되면 이 README의 모듈 맵을 먼저 갱신한다.
- API 공통 계약과 완료 기준은 `app/api/api-guidelines.md`가 소유한다.
- Controller, DTO, resource 같은 반복 구현 방식은 `app/api/strategies/README.md`가 소유한다.
