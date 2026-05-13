# Router Input Output And Checkpoint Protocol

이 문서는 `implement` 라우터가 backend/frontend 실행 스킬을 조율할 때 사용하는 통합 run id, 영역별 input/output 경계, 체크포인트 확인 절차를 소유한다. D/A/B 세부 input/output payload 스키마와 체크포인트 템플릿은 `implement-backend/references`와 `implement-frontend/references`가 각각 소유한다.

## 저장 위치

라우터는 하나의 사용자 요청에 하나의 `run_id`를 만들고, 영역별 실행 스킬이 같은 run 아래에 자기 마일스톤 산출물을 저장하게 한다.

```text
.agents/runs/{run_id}/
├── inputs/
│   ├── M1-backend/
│   └── M2-frontend/
├── outputs/
│   ├── M1-backend/
│   └── M2-frontend/
└── checkpoints/
    ├── M1-backend/
    └── M2-frontend/
```

경로 규칙:

- `run_id`: 상위 `implement`가 생성하고 backend/frontend 실행 스킬에 전달한다.
- `M{n}-{area}`: 라우터가 분해한 영역별 마일스톤 식별자. `area`는 `backend` 또는 `frontend`다.
- 영역 내부의 D/A/B 파일명과 결과 신호는 각 실행 스킬의 [input-output-checkpoint-protocol.md](../../implement-backend/references/input-output-checkpoint-protocol.md) 또는 [input-output-checkpoint-protocol.md](../../implement-frontend/references/input-output-checkpoint-protocol.md)를 따른다.
- 라우터는 영역 내부 파일명을 재정의하지 않는다.

## Router Output 처리

라우터는 backend/frontend 실행 스킬의 결과를 통합하기 위해 필요한 최소 정보만 읽는다.

처리 절차:

1. 영역별 실행 전에 `run_id`, 마일스톤 id, 명시적 제외사항, 성공 기준을 고정한다.
2. backend 산출물이 frontend 입력이 되면 backend 실행 결과에서 API 계약, 미해결 사항, 변경 파일 요약만 읽어 frontend 마일스톤 입력으로 넘긴다.
3. frontend 산출물이 backend 선행 작업 필요성을 드러내면 새 backend 마일스톤을 만들거나 사용자에게 계약 불확실성을 보고한다.
4. 영역별 실행 스킬이 반환한 D/A/B output 파일 경로가 실제로 존재하고 비어 있지 않은지 확인한다.
5. 영역 내부 payload 원문을 불필요하게 복사하지 않고, 통합 보고에 필요한 요약 필드만 읽는다.
6. backend/frontend 중 하나가 실패하면 다른 영역의 완료 상태와 분리해 보고한다.

## Router Checkpoint 처리

라우터는 영역별 실행 스킬이 남긴 체크포인트를 직접 해석해 수정하지 않는다. 체크포인트 재개는 해당 실행 스킬의 프로토콜로 되돌려 보낸다.

처리 절차:

1. 영역별 실행 중 `CONTEXT_CHECKPOINT:` 신호가 반환되면 해당 경로가 현재 영역 마일스톤의 checkpoint 경로인지 확인한다.
2. 파일 존재 여부와 비어 있지 않은지만 확인한다.
3. 체크포인트 파일의 세부 섹션 검증과 재호출 형식은 해당 영역 실행 스킬의 프로토콜을 따른다.
4. 같은 영역의 실행 스킬로 재개하고, 다른 영역 마일스톤에는 체크포인트 내용을 복사하지 않는다.
5. 체크포인트 복구가 두 번 실패하면 자동 루프를 멈추고 사용자에게 영역, 마일스톤, 실패 경로를 보고한다.

## 통합 보고

최종 보고에는 아래 항목을 영역별로 분리해 포함한다.

- 완료한 backend/frontend 마일스톤 수
- 영역별 D/A/B input/output 파일 경로
- 영역별 검증 명령과 결과
- 남은 API 계약, UI 계약, 데이터 계약 불확실성
- 자동 수렴 실패 또는 사용자 확인이 필요한 항목

## 검증 스크립트

라우터 프로토콜이나 영역별 실행 프로토콜을 수정한 뒤에는 아래 명령으로 필수 항목을 검증한다.

```bash
python3 .agents/skills/implement/scripts/validate-context-checkpoints.py
```
