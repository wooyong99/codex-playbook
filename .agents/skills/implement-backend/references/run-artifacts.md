# Backend Run Artifacts

## 목적

서브에이전트 오케스트레이션 결과를 최소한의 파일로 남긴다. 파일은 추적과 재개를 위한 증거이며, 문서 자체가 작업을 복잡하게 만들면 안 된다.

## 위치

```text
.agents/runs/{run_id}/
├── inputs/
│   ├── requirement-context.md
│   └── M1/
│       ├── 001-tdd-input.md
│       ├── 002-implementation-input.md
│       └── 003-review-input.md
├── outputs/
│   └── M1/
│       ├── 001-tdd-output.md
│       ├── 002-implementation-output.md
│       └── 003-review-output.md
└── checkpoints/
    └── M1/
        ├── tdd.md
        ├── implementation.md
        └── review.md
```

기존 `*.v1.md` 파일명을 쓰는 run도 허용한다. 중요한 것은 입력, 출력, 체크포인트가 서로 연결되는 것이다.

## Requirement Context

필수 내용:

- 요청 요약
- 목표
- 범위와 제외사항
- 확정된 정책
- 미결정 사항과 사용자 질문
- 검증 기준

## Role Input

필수 내용:

- 목표
- 명시적 제외사항
- Source of Truth와 선정 이유
- 선행 산출물 경로
- 출력 파일 경로
- 체크포인트 파일 경로
- 역할별 지시

## Role Output

필수 내용:

- 상태
- 변경 또는 판단 요약
- 생성/수정 파일
- 검증 결과
- 사용자 질문 또는 남은 위험

## Checkpoint

필수 내용:

- 현재 단계
- 완료된 작업
- 남은 작업
- 다음 호출이 이어받아야 할 주의사항

정상 완료 시에도 checkpoint를 남긴다. 체크포인트 신호만 보내고 파일을 남기지 않는 것은 실패다.
