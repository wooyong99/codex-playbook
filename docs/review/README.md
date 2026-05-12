# Review Routing

이 문서는 변경 파일 유형에 따라 어떤 reviewer가 어떤 문서를 기준으로 검토하는지 정의한다.

## Reviewer Matrix

| Reviewer | 대상 변경 | Source of Truth | 주요 관심사 |
|----------|-----------|-----------------|-------------|
| `backend-architecture-reviewer` | 백엔드 코드와 `docs/backend/**` | `docs/backend/architecture/**`, `docs/backend/policies/**`, 관련 TDD | 백엔드 아키텍처 경계, 정책 준수, TDD 결정 준수 |
| `frontend-architecture-reviewer` | 프론트엔드 코드와 `docs/frontend/**` | `docs/frontend/architecture/**`, `docs/frontend/conventions/**`, `docs/frontend/performance/**`, `docs/frontend/ui-ux/**` | FSD 의존 방향, 컴포넌트/API/상태/성능/UI 규칙 |
| `documentation-governance-reviewer` | `AGENTS.md`, `README.md`, `docs/**`, `.agents/skills/**` 문서 | `AGENTS.md`, `docs/rules/README.md`, 가장 가까운 `README.md` 문서 맵 | 문서 맵, 링크, 단일 출처, 플레이스홀더, 적용 가이드 일관성 |
| `security-policy-reviewer` | 인증, 권한, secret, 로그, 외부 연동, 설정 파일 | `docs/backend/policies/security.md`, `docs/backend/policies/logging.md`, `docs/rules/README.md` | 민감 정보 노출, secret 하드코딩, 권한 우회, 로깅 마스킹 |

## Routing Rules

- backend 코드 변경은 기본적으로 `backend-architecture-reviewer`가 검토한다.
- frontend 코드 변경은 `frontend-architecture-reviewer`가 검토한다.
- 문서 구조, 스킬, 에이전트 계약 변경은 `documentation-governance-reviewer`가 검토한다.
- 보안 민감 키워드가 포함된 변경은 기존 reviewer와 별개로 `security-policy-reviewer`를 추가 검토자로 붙인다.
- 한 변경이 여러 영역에 걸치면 reviewer를 중복 적용하고, 최종 보고에서 reviewer별 pass/violation을 분리한다.

## Security-Sensitive Signals

아래 신호가 변경 diff나 파일 경로에 있으면 `security-policy-reviewer`를 추가한다.

- `password`, `secret`, `token`, `credential`, `apiKey`, `authorization`
- 인증/인가 필터, 인터셉터, 미들웨어, security config
- 외부 API client, webhook, callback, signature 검증
- 로그 포맷, MDC, PII/개인정보/결제정보 마스킹
- `.env`, `application*.yml`, CI secret, deploy config

## Common Review Result

모든 reviewer는 위반을 보고할 때 [Rule ID and metadata](../rules/README.md) 형식을 따른다.

```yaml
violations:
  - rule_id: SECURITY-SECRET-LOG-001
    severity: blocker
    file: /abs/path/file.kt
    rule: security.md:Secret handling
    source_path: docs/backend/policies/security.md
    line_range: 10-12
    reason: Secret-like value is written to logs.
```

## 운영 원칙

- reviewer는 자신에게 할당된 영역의 명시 규칙만 근거로 삼는다.
- 기능 정확성, 제품 요구사항 충족 여부, 성능 측정 결과는 별도 검증으로 다룬다.
- 문서에 없는 개인 선호는 violation으로 보고하지 않는다.
- `severity: blocker` 위반은 자동 통과 처리하지 않는다.
