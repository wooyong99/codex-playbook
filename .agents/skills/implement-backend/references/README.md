# Implement Backend Reference Map

이 디렉토리는 `implement-backend` 스킬의 backend 실행 지식을 계층별로 나눈다.

읽는 순서는 상위 개념에서 세부 규격 순서로 고정한다.

## 문서 계층

| 계층 | 문서 | 목적 |
|------|------|------|
| L0 | [../SKILL.md](../SKILL.md) | 스킬의 목적, 적용 범위, 운영 모델 |
| L1 | [orchestration-boundaries.md](orchestration-boundaries.md) | 메인 에이전트와 D/A/B의 책임 경계 |
| L1 | [milestone-planning.md](milestone-planning.md) | backend 마일스톤을 나누는 기준 |
| L1 | [milestone-execution-workflow.md](milestone-execution-workflow.md) | backend 마일스톤 실행 흐름 |
| L2 | [input-output-checkpoint-protocol.md](input-output-checkpoint-protocol.md) | run artifact 저장 위치, 파일명, output 경로 검증, 체크포인트 복구 규칙 |
| L3 | [backend-technical-design-writer-contract.md](backend-technical-design-writer-contract.md) | D 입출력 계약 |
| L3 | [backend-implementation-engineer-contract.md](backend-implementation-engineer-contract.md) | A 입출력 계약 |
| L3 | [backend-architecture-reviewer-contract.md](backend-architecture-reviewer-contract.md) | B 입출력 계약 |

## 전체 모델

`implement-backend`는 prompt 본문을 길게 넘기는 방식이 아니라 파일 기반 입출력으로 서브에이전트를 호출한다.

```text
Main agent
  -> writes role input file
  -> calls subagent with input path and contract path
Subagent
  -> writes role output file
  -> writes checkpoint file
  -> returns result signal
Main agent
  -> validates output
  -> creates next role input file
```

핵심 원칙:

- 서브에이전트는 자신의 output을 다음 input으로 직접 변환하지 않는다.
- 메인 에이전트가 output을 읽고 다음 역할의 input으로 재구성한다.
- 이전 output의 본문을 복사하기보다 output artifact 경로를 다음 input에 기록한다.
- 체크포인트는 완료 응답이 아니라 같은 역할을 재개하기 위한 복구 신호다.

## 문서별 소유권

- `SKILL.md`: 스킬의 public entrypoint. 세부 YAML schema나 파일명 규칙을 소유하지 않는다.
- `orchestration-boundaries.md`: 누가 무엇을 판단하고 무엇을 판단하지 않는지 소유한다.
- `milestone-planning.md`: backend 작업을 어떤 단위로 나눌지 소유한다.
- `milestone-execution-workflow.md`: D/A/B 호출 순서와 output-to-input 변환 책임을 소유한다.
- `input-output-checkpoint-protocol.md`: `.agents/runs/{run_id}` 하위 파일 구조, 파일명 할당, output 경로 검증, 체크포인트 복구 절차를 소유한다.
- `*-contract.md`: 역할별 input schema, output schema, 정상 결과 신호, 체크포인트 판단 기준, 체크포인트 파일 템플릿을 소유한다.

## 변경 가이드

- 스킬의 목적이나 공개 사용법이 바뀌면 `SKILL.md`를 수정한다.
- 책임 경계가 바뀌면 `orchestration-boundaries.md`를 수정한다.
- 마일스톤 분할 기준이 바뀌면 `milestone-planning.md`를 수정한다.
- 실행 순서나 반복 종료 기준이 바뀌면 `milestone-execution-workflow.md`를 수정한다.
- 파일 저장 위치, 파일명, output 경로 검증, 체크포인트 복구 규칙이 바뀌면 `input-output-checkpoint-protocol.md`를 수정한다.
- 특정 서브에이전트의 입출력 필드, 정상 결과 신호, 체크포인트 판단 기준이 바뀌면 해당 `*-contract.md`를 수정한다.
