# AGENTS Guide

## 프로젝트 명

- {프로젝트명}

## 비즈니스 목표

- {비즈니스 목표 1}
- {비즈니스 목표 2}
- {비즈니스 목표 3}

## AI 에이전트 공통 작업 지침

### 1) 코딩하기 전에 먼저 생각하라

- 섣불리 가정하지 않는다.
- 헷갈리는 것은 숨기지 않고 질문한다.
- 선택지가 있을 때 각 장단점을 먼저 설명한다.

### 2) 먼저 단순하게 생각하라

- 문제 해결에 필요한 최소한의 코드만 작성·수정한다.
- 미래 요구를 상상해 불필요한 기능을 미리 구현하지 않는다.

### 3) 수술하듯 필요한 부분만 고쳐라

- 변경 범위를 반드시 필요한 부분으로 제한한다.
- 기존 동작을 불필요하게 건드리지 않는다.

### 4) 목표 중심으로 실행하라

- 성공 기준을 먼저 정의한다.
- 기준이 충족될 때까지 검증을 반복한다.

### 5) 문서 맵 일관성을 유지하라

- `AGENTS.md`는 프로젝트 최상위 진입점만 가진다.
- `docs/backend` 하위 문서 맵은 `docs/backend/README.md`가 소유한다.
- `docs/frontend` 하위 문서 맵은 `docs/frontend/README.md`가 소유한다.
- 하위 디렉토리가 추가·삭제·개편되면 해당 영역의 `README.md`를 먼저 갱신하고, `AGENTS.md`는 최상위 진입점이 바뀔 때만 갱신한다.

## 프로젝트 구조

```text
.
├── .agents/      # 에이전트 스킬 및 참조 문서
├── docs/         # 프로젝트 지식 시스템(백엔드/프론트엔드/PRD)
└── AGENTS.md     # 에이전트 작업 지침서
```

## 문서 맵

- [PRD](/Users/jeong-uyong/work/codex-playbook/docs/PRD.md)
- [Backend 문서 홈](/Users/jeong-uyong/work/codex-playbook/docs/backend/README.md)
- [Frontend 문서 홈](/Users/jeong-uyong/work/codex-playbook/docs/frontend/README.md)
