# Backend Input Output And Checkpoint Protocol

이 문서는 `implement-backend` 스킬의 backend Markdown input artifact, output artifact, 체크포인트 파일, 결과 신호, 검증 절차를 소유한다. 세부 Case와 역할별 Markdown 섹션은 backend 계약 문서가 단일 출처다.

## 문서 역할

이 문서는 저수준 실행 규격이다.

- 전체 책임 경계는 [orchestration-boundaries.md](orchestration-boundaries.md)를 따른다.
- design/implementation/review 호출 순서는 [milestone-execution-workflow.md](milestone-execution-workflow.md)를 따른다.
- 역할별 Case, Markdown input/output 섹션, 체크포인트 판단 기준은 각 `*-contract.md`를 따른다.
- 이 문서는 `.agents/runs/{run_id}` 하위 파일 구조, 결과 신호 검증, 체크포인트 복구 절차를 정의한다.

## 저장 위치

backend 입력, 출력, 체크포인트는 run과 backend 마일스톤 단위로 저장한다.

```text
.agents/runs/{run_id}/
├── inputs/
│   └── M{n}/
│       ├── 001-design-r00-input.v1.md
│       ├── 002-implementation-r00-input.v1.md
│       ├── 003-architecture-review-r01-input.v1.md
│       ├── 004-implementation-r01-input.v1.md
│       └── 005-architecture-review-r02-input.v1.md
├── outputs/
│   └── M{n}/
│       ├── 001-design-r00-result.v1.md
│       ├── 002-implementation-r00-result.v1.md
│       ├── 003-architecture-review-r01-result.v1.md
│       ├── 004-implementation-r01-fix-result.v1.md
│       └── 005-architecture-review-r02-result.v1.md
└── checkpoints/
    └── M{n}/
        ├── design-r00-v001.md
        ├── implementation-r00-v001.md
        └── architecture-review-r01-v001.md
```

파일명 규칙:

- `{seq}`: 마일스톤별 append-only 3자리 순번. `implement-backend`가 할당하며 서브에이전트가 임의 생성하지 않는다.
- `{role_slug}`: `design`, `implementation`, `architecture-review`
- `r{iter}`: 설계와 최초 구현은 `r00`, 첫 검토는 `r01`, 이후 implementation-review 루프마다 증가한다.
- `{kind}`: input 파일은 `input`, output 파일은 `result` 또는 `fix-result`
- `v1`: input/output artifact 파일명 스키마 버전. 파일 내용의 `Metadata` 섹션에 있는 `schema_version`은 각 backend 계약 문서가 정한다.
- 정상 결과를 다시 받아야 하면 새 `{seq}`를 할당한다. 같은 파일 경로 재사용은 동일 호출의 저장 실패 복구에만 허용한다.

## Backend Input Artifact 처리

`implement-backend`는 서브에이전트 호출 전에 `[입력 파일]` Markdown을 저장하고, 호출 프롬프트에는 `[입력 파일]` 절대 경로와 계약 파일 경로만 전달한다. 긴 입력 본문을 프롬프트에 직접 복사하지 않는다.

처리 절차:

1. 서브에이전트 호출 전에 `[입력 파일]`, `[출력 파일]`, `[체크포인트 파일]` 절대 경로를 할당한다.
2. `[입력 파일]`에는 요구사항, 명시적 제외사항, 선행 output artifact 경로, 선별된 Source of Truth, 출력 파일 경로, 체크포인트 파일 경로, 출력 규격, 체크포인트 규격을 저장한다.
3. 메인 에이전트는 계약 문서의 해당 Case에서 출력 규격과 체크포인트 규격을 가져와 입력 파일에 포함한다.
4. 서브에이전트에는 `[입력 파일]`을 읽고 입력 파일의 출력 규격에 따라 작업하라는 짧은 프롬프트만 전달한다.
5. 체크포인트 재호출도 같은 `[입력 파일]`을 기준으로 하되, 기존 `[체크포인트 파일]`을 먼저 읽고 이어서 수행하게 한다.

## Backend Output Artifact 처리

서브에이전트는 `[출력 파일]`에 Markdown output artifact를 저장하고, 같은 호출의 `[체크포인트 파일]`에도 완료 snapshot을 저장한 뒤 첫 줄에 결과 신호와 파일 경로만 반환한다.

`implement-backend`의 처리 절차:

1. 정상 결과 신호의 경로가 이번 호출에서 전달한 `[출력 파일]`과 일치하는지 확인한다.
2. 해당 파일이 존재하고 비어 있지 않은지 확인한다.
3. `Metadata`, `상태`, 역할별 필수 섹션이 있는지 확인한다.
4. backend 구현 결과는 `변경 파일`, `검증 결과` 섹션을 확인한다.
5. backend 검토 결과는 `판정`, `위반 사항` 섹션을 확인하고, `blocker` 또는 `major` 위반이 있으면 수정 루프로 보낸다.
6. 정상 완료 경로에서도 이번 호출의 `[체크포인트 파일]`이 존재하고 비어 있지 않으며, 계약 문서의 체크포인트 파일 스키마에 있는 제목과 핵심 섹션이 포함됐는지 검증한다.
7. 다음 backend 에이전트의 input artifact에는 필요한 output 원문을 복사하지 않고 선행 output artifact 경로만 기록한다.

## 체크포인트 처리

서브에이전트 응답 첫 줄이 `CONTEXT_CHECKPOINT:` 인 경우, 이를 완료 응답으로 파싱하지 않는다. 체크포인트는 같은 backend 마일스톤 안에서 재개하기 위한 복구 절차다.

처리 절차:

1. 첫 줄의 경로가 현재 호출에서 전달한 `[체크포인트 파일]` 경로와 일치하는지 확인한다.
2. 해당 파일이 존재하고 비어 있지 않은지 확인한다.
3. 계약 문서의 체크포인트 파일 스키마에 있는 제목과 핵심 섹션이 포함됐는지 확인한다.
4. 검증이 실패하면 같은 서브에이전트에게 한 번만 재호출하여 체크포인트 파일 저장부터 다시 수행하게 한다.
5. 두 번째도 실패하면 자동 루프를 멈추고 사용자에게 backend 체크포인트 프로토콜 실패를 보고한다.
6. 검증이 통과하면 체크포인트 파일을 읽은 뒤, 계약 문서의 체크포인트 재호출 규격으로 같은 서브에이전트를 재호출한다.

역할별 체크포인트 판단 기준은 backend 계약 문서가 단일 출처로 가진다. `implement-backend`는 해당 기준을 input artifact의 `체크포인트 규격` 섹션으로 전달하고, `CONTEXT_CHECKPOINT:` 응답을 복구 절차로 처리한다.

## 검증 스크립트

backend 실행 규약, 계약 문서, 서브에이전트 정의를 수정한 뒤에는 아래 명령으로 필수 항목을 검증한다.

```bash
python3 .agents/scripts/validate-context-checkpoints.py
```
