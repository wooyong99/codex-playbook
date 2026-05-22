# Core Architecture

## 목적

`backend/core` 하위 핵심 업무 모듈의 책임과 문서 위치를 안내한다.

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
