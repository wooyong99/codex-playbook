# Security Guidelines

## 목적

`backend/internal/security` 모듈의 책임과 경계를 정리한다.

## 적용 범위

- 인증, 인가, 암호화, 토큰 adapter 후보 모듈

## 책임

- security provider와 crypto 구현 세부사항을 내부 인프라 경계에 둔다.
- application과 domain에는 provider SDK 타입이나 HTTP security 세부 구현이 노출되지 않게 한다.

## 의존 경계

`build.gradle.kts` 기준 의존 대상은 `core/application`, `core/domain`이다.

## 확인 필요

- 현재 소스 파일이 없어 인증 방식, 권한 모델, password/token 정책은 구현 추가 시 문서화한다.
