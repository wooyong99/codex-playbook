# External Architecture

## 목적

`backend/external` 하위 외부 연동 모듈의 책임과 문서 위치를 안내한다.

## 적용 범위

- `backend/external/integration`
- `backend/external/webhook`

## 모듈 맵

| 모듈 | 문서 | 책임 |
|------|------|------|
| `external/integration` | [integration](./integration/integration-guidelines.md) | 외부 API 연동 adapter 후보 모듈 |
| `external/webhook` | 전용 문서 없음 | 외부 webhook 수신 또는 발행 후보 모듈 |

## 의존 경계

`external/*` 모듈은 외부 시스템 스키마와 오류를 내부 application 포트 계약으로 번역하는 경계를 소유한다.
