# Review Routing

## 목적

이 문서는 변경 파일 유형에 따라 어떤 reviewer가 어떤 문서를 기준으로 검토하는지 정의한다.

## Reviewer Matrix

| Reviewer | 대상 변경 | Source of Truth | 주요 관심사 |
|----------|-----------|-----------------|-------------|
| `backend-architecture-reviewer` | 백엔드 코드와 `docs/backend/**` | `docs/backend/architecture/**`, `docs/backend/policies/**`, 관련 TDD | 백엔드 아키텍처 경계, 정책 준수, TDD 결정 준수 |
| `frontend-architecture-reviewer` | 프론트엔드 코드와 `docs/frontend/**` | `docs/frontend/architecture/**`, `docs/frontend/conventions/**`, `docs/frontend/performance/**`, `docs/frontend/ui-ux/**` | FSD 의존 방향, 컴포넌트/API/상태/성능/UI 규칙 |

## Routing Rules

- backend 코드 변경은 기본적으로 `backend-architecture-reviewer`가 검토한다.
- frontend 코드 변경은 `frontend-architecture-reviewer`가 검토한다.
- 한 변경이 여러 영역에 걸치면 reviewer를 중복 적용하고, 최종 보고에서 reviewer별 pass/violation을 분리한다.

## Common Review Result

모든 reviewer는 위반을 보고할 때 [Rule ID and metadata](../rules/README.md) 형식을 따른다.

```yaml
violations:
  - rule_id: BACKEND-APP-DTO-001
    severity: major
    file: /abs/path/ProductController.kt
    rule: app-guidelines.md:Controller checklist
    source_path: docs/backend/architecture/app/app-guidelines.md
    line_range: 52-56
    reason: Request DTO contains command conversion logic.
```

## 운영 원칙

- reviewer는 자신에게 할당된 영역의 명시 규칙만 근거로 삼는다.
- 기능 정확성, 제품 요구사항 충족 여부, 성능 측정 결과는 별도 검증으로 다룬다.
- 문서에 없는 개인 선호는 violation으로 보고하지 않는다.
- `severity: blocker` 위반은 자동 통과 처리하지 않는다.
