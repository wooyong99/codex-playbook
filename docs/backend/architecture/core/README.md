# Core Architecture

이 문서는 `backend/core` 아키텍처 단위의 책임, 하위 모듈 문서, 의존 경계를 안내한다.

## 목적

- 핵심 업무 규칙과 유스케이스 조합 경계를 다른 아키텍처 단위와 분리한다.
- application과 domain의 책임 차이를 하위 Guidelines 문서로 연결한다.
- 신규 핵심 모듈을 추가할 때 문서 위치와 의존 방향을 같은 기준으로 판단하게 한다.

## 적용 범위

- `backend/core/application`
- `backend/core/domain`

## 모듈 맵

| 모듈 | 문서 | 책임 |
|------|------|------|
| `core/application` | [application](./application/application-guidelines.md) | 업무 흐름 조합, 서비스, 포트 계약 |
| `core/domain` | [domain](./domain/domain-guidelines.md) | 도메인 모델과 비즈니스 규칙 |

## 의존 경계

```text
core/application -> core/domain
core/domain -> no project module
```

`core`는 외부 진입점, 저장 기술, 외부 시스템 스키마를 직접 소유하지 않는다. 외부 자원 접근은 `core/application`의 Port 계약과 adapter 구현 경계로 분리한다.

## 문서 운영 원칙

- 하위 모듈이 추가되면 이 README의 모듈 맵을 먼저 갱신한다.
- 모듈별 책임과 완료 기준은 각 `{module}-guidelines.md`가 소유한다.
- 반복 구현 방식과 역할별 선택 기준은 가장 가까운 `strategies/README.md`가 소유한다.
