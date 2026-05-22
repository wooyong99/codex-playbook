# App API Architecture

## 목적

`backend/app/api` 하위 HTTP API 애플리케이션의 공통 책임과 전략 문서 위치를 정리한다.

## 적용 범위

- `backend/app/api/admin`
- `backend/app/api/operator`
- `backend/app/api/user`
- Controller, Request/Response DTO, API resource, API 문서화, versioning

공통 응답 envelope, 예외 응답, trace, tenant, rate limit 같은 API 공통 지원은 [support/api](../../support/api/api-guidelines.md)가 소유한다.

## 문서 맵

- [api-guidelines](./api-guidelines.md) - API 애플리케이션 공통 경계
- `admin` - 관리자 API 모듈 전용 문서 없음
- `operator` - 운영자 API 모듈 전용 문서 없음
- `user` - 플랫폼 사용자 API 모듈 전용 문서 없음
- [strategies](./strategies/README.md) - Controller, DTO, resource, API 문서화 전략
