# External Architecture

이 문서는 `backend/external` 아키텍처 단위의 책임, 하위 모듈 문서, 의존 경계를 안내한다.

## 목적

- 외부 시스템 연동 구현을 application Port 계약 밖으로 새지 않게 격리한다.
- Provider별 Adapter, ApiClient, DTO, Config, Exception 문서 위치를 안내한다.
- 신규 외부 연동 모듈을 추가할 때 문서 위치와 의존 방향을 같은 기준으로 판단하게 한다.

## 적용 범위

- `backend/external/integration`
- `backend/external/webhook`

## 모듈 맵

| 모듈 | 문서 | 책임 |
|------|------|------|
| `external/integration` | [integration](./integration/integration-guidelines.md) | 외부 API 연동 adapter 후보 모듈 |
| `external/webhook` | 전용 문서 없음 | 외부 webhook 수신 또는 발행 후보 모듈 |

## 의존 경계

```text
external/* -> core/application -> core/domain
external/* -> external systems
```

`external/*` 모듈은 외부 시스템 스키마와 오류를 application Port 계약으로 번역하는 경계를 소유한다. 외부 DTO, provider SDK 타입, HTTP/네트워크 예외는 application Port 시그니처로 노출하지 않는다.

## 문서 운영 원칙

- 하위 모듈이 추가되면 이 README의 모듈 맵을 먼저 갱신한다.
- 모듈별 책임과 완료 체크리스트는 각 `{module}-guidelines.md`가 소유한다.
- 반복 구현 방식과 Provider별 선택 기준은 가장 가까운 `strategies/README.md`가 소유한다.
