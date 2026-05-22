# App Architecture

## 목적

`backend/app` 하위 애플리케이션 진입점의 책임과 문서 위치를 안내한다.

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

`app` 모듈은 외부 요청이나 실행 트리거를 받아 `core/application` 계약으로 넘기는 진입점이다. API 공통 응답, 예외, 필터는 `support/api`를 차용한다.
