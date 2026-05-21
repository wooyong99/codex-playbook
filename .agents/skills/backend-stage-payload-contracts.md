# Backend Stage Payload Contracts

## 목적

backend rule skill들이 서로의 이름, 실행 순서, 호출 주체에 의존하지 않고 stage 간 산출물을 주고받기 위한 payload 계약을 정의한다.

## 적용 범위

이 문서는 backend 기술 설계, 코드 구현, architecture review, remediation 사이에서 공유되는 payload 이름과 최소 필드를 소유한다.

범위 밖:

- subagent identity, lifecycle, retry, scheduling
- feature delivery orchestration
- backend architecture rule 원문과 rule id metadata

Rule id 형식과 severity 의미는 [Rule metadata](../../docs/rules/README.md)가 소유한다.

## 소유권

- 각 rule skill은 자기 stage의 판단 기준만 소유한다.
- 이 문서는 stage 간 payload의 이름과 최소 구조만 소유한다.
- payload 생산자와 소비자는 skill 이름이 아니라 payload 의미로 연결한다.

## Payload 흐름

```text
backend_design_basis
  -> implementation_result
  -> architecture_review_result
  -> remediation_input
```

각 payload는 독립 입력으로 취급할 수 있어야 한다. 특정 skill이 먼저 실행됐다는 사실만으로 payload가 유효하다고 보지 않는다.

## backend_design_basis

backend 설계 판단 또는 설계 skip 근거를 담는다.

최소 필드:

- `scope`: 설계 범위와 제외 범위
- `source_of_truth`: 확인한 docs/backend 경로와 코드 근거
- `decisions`: 주요 아키텍처 판단, 선택 이유, 대안
- `layer_responsibilities`: domain, application, storage, external, app 책임 분리
- `runtime_policies`: transaction, consistency, failure handling, concurrency, security 영향
- `verification_plan`: 구현 후 실행할 compile/test/typecheck 후보
- `open_questions`: 설계 단계에서 해소하지 못한 불확실성
- `skip_reason`: 설계 문서를 만들지 않는 경우의 근거

## implementation_result

backend 코드 변경과 구현 검증 evidence를 담는다.

최소 필드:

- `changed_files`: 변경 파일 목록
- `change_reasons`: 파일별 변경 이유
- `applied_design_basis`: 반영한 설계 판단 또는 skip 근거
- `validation_evidence`: compile/test/typecheck 실행 결과
- `contract_uncertainties`: frontend 또는 infra로 넘길 계약 불확실성
- `blocked_by`: 구현 완료를 막는 실패나 불확실성

## architecture_review_result

backend 변경을 Source of Truth 기준으로 검토한 결과를 담는다.

최소 필드:

- `result`: `pass`, `violation`, `blocked` 중 하나
- `source_of_truth`: 검토 기준으로 사용한 문서와 코드 근거
- `checked_files`: 검토한 변경 파일
- `implementation_evidence`: 확인한 구현 검증 evidence
- `violations`: violation payload 목록
- `residual_risks`: pass 또는 blocked 판단에 남긴 잔여 위험
- `rerun_required`: remediation 후 다시 실행할 검증

## violation payload

architecture review가 발견한 개별 위반을 담는다.

최소 필드:

- `rule_id`: 안정적인 규칙 식별자. 없으면 후보 규칙임을 명시한다.
- `severity`: `blocker`, `major`, `minor`, `info` 중 하나.
- `source_path`: 위반 근거가 되는 Source of Truth 경로.
- `line_range`: 근거 문서 또는 변경 파일의 관련 줄 범위.
- `violated_rule`: 위반한 규칙 원문 또는 체크리스트 항목.
- `affected_files`: 수정이 필요한 파일 목록.
- `reason`: 왜 위반인지에 대한 근거.
- `requested_action`: 특정 구현 방식을 강제하지 않는 수정 방향.
- `rerun_required`: 수정 후 다시 실행해야 할 검증.

## remediation_input

implementation stage가 재작업 입력으로 소비하는 payload다.

최소 필드:

- `architecture_review_result`: 원본 review 결과
- `violations`: 수정 대상 violation payload 목록
- `allowed_scope`: 재작업 가능한 파일과 행위 범위
- `blocked_by`: 구현 재작업만으로 해결할 수 없는 설계 충돌이나 정책 공백
- `rerun_required`: 수정 후 다시 실행해야 할 검증

## 검증

- backend rule skill은 다른 backend rule skill 이름을 필수 입력으로 요구하지 않는다.
- shared field를 추가하거나 의미를 바꾸면 이 문서를 먼저 갱신한다.
- skill 본문에는 payload schema를 복사하지 않고 이 문서를 참조한다.
