# Rule ID And Metadata

이 문서는 codex-playbook에서 사용하는 규칙 ID와 metadata 형식을 정의한다. 규칙 ID는 에이전트 검토 결과, 문서 체크리스트, CI 검증, 작업 리포트가 같은 규칙을 가리키도록 만드는 안정적인 식별자다.

## Rule ID 형식

```text
{AREA}-{UNIT}-{TOPIC}-{NNN}
```

| 파트 | 설명 | 예시 |
|------|------|------|
| `AREA` | 규칙이 적용되는 큰 영역 | `AGENT`, `DOCS`, `BACKEND`, `FRONTEND`, `SECURITY` |
| `UNIT` | 아키텍처 단위나 문서 단위 | `HANDOFF`, `MAP`, `APP`, `FSD`, `API` |
| `TOPIC` | 세부 주제 | `SCHEMA`, `LINK`, `DTO`, `IMPORT`, `SECRET` |
| `NNN` | 3자리 일련번호 | `001`, `002` |

예시:

- `AGENT-HANDOFF-SCHEMA-001`
- `DOCS-MAP-LINK-001`
- `BACKEND-APP-DTO-001`
- `FRONTEND-FSD-IMPORT-001`
- `SECURITY-SECRET-LOG-001`

## Metadata 형식

규칙 원문을 새로 만들거나 기존 규칙을 검토 가능한 단위로 승격할 때 아래 metadata를 함께 둔다.

```yaml
rule_id: BACKEND-APP-DTO-001
title: Request DTO must not contain command conversion logic
area: BACKEND
unit: APP
topic: DTO
severity: major
status: active
source: docs/backend/architecture/app/app-guidelines.md
applies_to:
  - backend app layer
  - request dto
```

## Severity

| Severity | 의미 | 기본 처리 |
|----------|------|-----------|
| `blocker` | 보안, 데이터 정합성, 빌드 실패처럼 반드시 막아야 하는 위반 | 자동 수정 또는 작업 중단 |
| `major` | 아키텍처 경계, 공통 정책, 반복 구현 전략 위반 | 수정 후 재검토 |
| `minor` | 네이밍, 문서 위치, 작은 일관성 위반 | 가능하면 수정 |
| `info` | 관찰 또는 참고 사항 | 실패로 보지 않음 |

## Reviewer 출력 규칙

에이전트가 규칙 위반을 보고할 때는 사람이 읽는 `rule` 문자열과 함께 안정적인 `rule_id`를 반드시 남긴다.

Reviewer는 호출 input으로 전달받은 Source of Truth만 기준으로 위반을 보고한다. reviewer 서브에이전트 TOML이나 전역 review routing 문서는 고정 Source of Truth를 소유하지 않는다.

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

- 한 번 공개된 `rule_id`는 의미를 바꾸지 않는다. 의미가 바뀌면 새 ID를 만든다.
- 규칙을 삭제하지 않고 `status: deprecated`로 표시한다.
- 같은 규칙 원문을 여러 문서에 복사하지 않는다. 다른 문서에서는 `rule_id`와 원문 링크만 참조한다.
- `rule_id` 없이 발견된 반복 위반은 먼저 후보 규칙으로 정리한 뒤 active 규칙으로 승격한다.
