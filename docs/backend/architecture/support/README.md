# Support Architecture

이 문서는 `backend/support` 아키텍처 단위의 책임, 하위 지원 모듈 문서, 의존 경계를 안내한다.

## 목적

- 여러 애플리케이션이 공유하는 기술 지원 경계를 업무 로직과 분리한다.
- API 공통 응답, 예외, 필터, trace, tenant 같은 지원 모듈의 문서 위치를 안내한다.
- 신규 support 모듈을 추가할 때 문서 위치와 의존 방향을 같은 기준으로 판단하게 한다.

## 적용 범위

- `backend/support/api`

## 모듈 맵

| 모듈 | 문서 | 책임 |
|------|------|------|
| `support/api` | [api](./api/api-guidelines.md) | API 공통 응답, 예외, 필터, tenant, trace, rate limit |

## 의존 경계

```text
support/api -> core/application -> core/domain
```

`support` 모듈은 여러 app 진입점이 공유하는 기술 관심사를 소유한다. 도메인별 업무 흐름, Controller별 계약, 외부 시스템 연동 구현은 support 경계에 두지 않는다.

## 문서 운영 원칙

- 하위 지원 모듈이 추가되면 이 README의 모듈 맵을 먼저 갱신한다.
- 모듈별 책임과 완료 기준은 각 `{module}-guidelines.md`가 소유한다.
- 반복 구현 방식과 공통 관심사 배치 기준은 가장 가까운 `strategies/README.md`가 소유한다.
