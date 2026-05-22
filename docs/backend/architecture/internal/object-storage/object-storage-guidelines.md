# Object Storage Guidelines

## 목적

`backend/internal/object-storage` 모듈의 책임과 경계를 정리한다.

## 적용 범위

- asset, HTML, 스킨 소스 같은 객체 저장소 adapter 후보 모듈

## 책임

- object storage provider와 파일 저장 세부사항을 내부 인프라 경계에 둔다.
- application 계약에는 저장소 provider SDK 타입이 노출되지 않게 한다.

## 의존 경계

`build.gradle.kts` 기준 의존 대상은 `core/application`, `core/domain`이다.

## 확인 필요

- 현재 소스 파일이 없어 bucket/key 정책, 버전 보존, 서명 URL 정책은 구현 추가 시 문서화한다.
