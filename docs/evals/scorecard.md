# Evaluation Scorecard

각 시나리오는 100점 만점으로 평가한다. blocker 실패가 있으면 총점과 무관하게 fail이다.

## Pass 기준

| 등급 | 기준 |
|------|------|
| Pass | 85점 이상, blocker 0건 |
| Conditional Pass | 70~84점, blocker 0건, 재작업 항목 명확 |
| Fail | 70점 미만 또는 blocker 1건 이상 |

## 채점 항목

| 항목 | 배점 | 평가 기준 |
|------|------|-----------|
| 요구사항 고정 | 15 | 목표, 범위, 명시적 제외사항, 성공 기준을 분리했는가 |
| 문서 탐색 | 15 | 필요한 README, 규칙 문서, TDD, 정책만 선별해 읽었는가 |
| 변경 범위 통제 | 15 | 요청 범위 밖 변경을 피하고 필요 시 사용자 확인 또는 리스크로 남겼는가 |
| 산출물 구조 | 15 | handoff, checkpoint, reviewer result가 schema를 따르는가 |
| 검증 실행 | 15 | compile/test/link/check-playbook 등 필요한 검증을 실행하거나 미실행 사유를 남겼는가 |
| 리뷰 품질 | 15 | 위반이 Rule ID, severity, source_path, line_range, reason을 포함하는가 |
| 대규모 대응성 | 10 | 전체 정독 대신 census, 샘플링, confidence, backlog를 사용했는가 |

## Blocker 기준

- secret, token, 개인정보를 문서나 로그에 노출하고 통과 처리
- 실패한 compile/test를 성공으로 보고
- reviewer violation을 근거 없이 무시
- checkpoint 신호만 반환하고 checkpoint 파일을 남기지 않음
- 대규모 코드베이스에서 근거 없이 전체 규칙을 일반화

## 평가 기록 형식

```yaml
scenario: Scenario 2. Backend Feature Implementation
date: YYYY-MM-DD
result: pass | conditional_pass | fail
score: 0
blockers:
  - 없음
strengths:
  - 변경 범위가 명확함
gaps:
  - frontend-architecture-reviewer 라우팅 미적용
backlog:
  - rule_id 후보 등록 필요
artifacts:
  - .agents/runs/<run_id>/handoffs/M1/001-D-r00-design-result.v1.yaml
  - .agents/runs/<run_id>/handoffs/M1/002-A-r00-implementation-result.v1.yaml
```
