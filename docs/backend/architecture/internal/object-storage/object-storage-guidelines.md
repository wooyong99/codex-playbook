# Object Storage Guidelines

이 문서는 `backend/internal/object-storage` 모듈의 실제 코드 위치, 책임, 의존 경계, 구현 전략 보강 기준을 정리한다.

## 코드 위치

- `backend/internal/object-storage` - asset, HTML, 스킨 소스 같은 객체 저장소 adapter 후보를 담당한다.

## 책임

- object storage provider와 파일 저장 세부사항을 내부 인프라 경계에 둔다.
- application 계약에는 저장소 provider SDK 타입이 노출되지 않게 한다.
- bucket/key 정책, 버전 보존, 서명 URL 정책이 필요한 경우 provider 구현과 함께 문서화한다.

## 의존 경계

- depends on: `core/application`, `core/domain`, object storage provider
- used by: Spring runtime, `core/application` Port
- 금지되는 방향: provider SDK 타입의 application 노출, domain 모델의 bucket/key 정책 의존

## 핵심 원칙

- object storage는 파일 저장 기술을 캡슐화하고 application에는 저장 의도와 결과만 드러낸다.
- bucket, key, content type, retention, signed URL 정책은 provider 구현 경계에서 관리한다.
- 민감 파일 접근은 보안 정책과 감사 가능한 로그 기준을 따른다.

## 관련 정책

- [security](../../../policies/security.md) - 파일 접근 권한과 민감 정보 처리
- [logging](../../../policies/logging.md) - 파일 작업 감사와 실패 로깅
- [concurrency-and-performance](../../../policies/concurrency-and-performance.md) - 업로드/다운로드 성능 경계

## 금지 규칙

- application Port 시그니처에 provider object, bucket client, signed URL 구현 타입을 노출하지 않는다.
- domain 객체가 bucket 이름, key prefix, storage class를 알게 하지 않는다.
- 보존 기간, 접근 권한, 서명 URL 만료 기준 없이 파일을 저장하지 않는다.

## 주요 컴포넌트

- Storage adapter: `{Asset}StorageAdapter`
- Storage key factory: `{Asset}StorageKey`
- Storage properties: `{Provider}StorageProperties`
- Storage config: `{Provider}StorageConfig`

## 전략 문서

- 전용 전략 문서 없음

## 완료 기준

- 구현 추가 시 bucket/key 정책, 버전 보존, 서명 URL 기준이 이 문서 또는 `strategies` 문서에 설명된다.
- application은 object storage provider가 아니라 Port 계약에 의존한다.
- 파일 접근 권한, 만료, 삭제 또는 보존 정책을 설명할 수 있다.
