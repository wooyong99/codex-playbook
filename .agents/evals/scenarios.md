# Evaluation Scenarios

## Scenario 1. Project Context Setup

목표: 새 프로젝트에 codex-playbook을 적용할 때 핵심 플레이스홀더와 PRD가 일관되게 채워지는지 확인한다.

입력:

- 프로젝트명
- 비즈니스 목표 3개
- 제품 한 줄 설명

기대 산출물:

- `AGENTS.md` 프로젝트명과 비즈니스 목표 갱신
- `docs/PRD.md` 핵심 섹션 갱신
- backend/frontend README 프로젝트명 갱신
- `check-playbook.py` 통과

주요 실패 신호:

- 문서별 프로젝트명이 서로 다름
- PRD에 `{...}` 플레이스홀더 잔존
- 문서 맵 링크 누락

## Scenario 2. Backend Feature Implementation

목표: 백엔드 기능 추가 작업에서 설계, 구현, 아키텍처 검토, 검증 결과가 누락 없이 남는지 확인한다.

입력:

- 상태 변경을 포함한 UseCase 추가 요청
- 트랜잭션 경계와 예외 처리가 필요한 요구사항

기대 산출물:

- 마일스톤 계획
- `implement-backend` 실행 경로 선택
- 필요 시 TDD 또는 TDD skip 근거
- `backend-implementation-engineer` 구현 결과 output artifact
- backend-architecture-reviewer 결과
- compile/test 검증 결과

주요 실패 신호:

- 변경 파일만 있고 설계 또는 skip 근거가 없음
- 테스트 미실행 사유가 없음
- reviewer 위반을 기능 버그나 개인 선호로 보고

## Scenario 3. Frontend Feature Review

목표: 프론트엔드 변경이 FSD, API, 상태, 성능, UI/UX 문서 기준으로 검토되는지 확인한다.

입력:

- `frontend` 코드에 feature와 entity import가 섞인 변경
- React Query invalidation 누락이 있는 변경

기대 산출물:

- `implement-frontend` 실행 경로 선택
- 필요 시 상태관리 구조, API 연동 방식, 컴포넌트 구조, 라우팅, 캐싱 전략, 에러 처리, 폴더 구조를 포함한 frontend TDD
- `frontend-implementation-engineer` 구현 결과 output artifact
- `frontend-architecture-reviewer`가 docs/frontend 기준으로 위반 보고
- 위반에 reviewer contract 형식의 `rule_id`, `severity`, `source_path` 포함
- 기능 정확성 추측 없이 문서 근거만 제시

주요 실패 신호:

- backend reviewer만 실행됨
- docs/frontend를 읽지 않음
- reviewer contract의 rule metadata 누락

## Scenario 4. Large Codebase Reverse Engineering

목표: 20만~100만 라인 코드베이스에서 전체 정독 없이 문서화 계획을 만들 수 있는지 확인한다.

입력:

- 대규모 백엔드 코드베이스 경로
- `reverse-engineer-backend-docs inspect` 요청

기대 산출물:

- LOC, 파일 수, 모듈 수, 제외 경로
- census 결과
- 샘플링 예산과 우선순위
- confidence report
- 1차 migrate 범위와 backlog

주요 실패 신호:

- 전체 파일 정독 시도
- 근거 하나로 전체 규칙 일반화
- 미분석 영역을 명시하지 않음

## Scenario 5. Context Checkpoint Recovery

목표: 긴 작업에서 checkpoint artifact를 남기고 재호출 시 같은 상태에서 이어갈 수 있는지 확인한다.

입력:

- 10개 이상 파일 변경이 예상되는 리팩토링
- 중간에 컨텍스트 전환 또는 checkpoint 강제 조건 부여

기대 산출물:

- checkpoint 파일 생성
- 정상 완료 시에도 완료 snapshot 생성
- 재호출 시 완료된 작업 건너뛰기
- `validate-context-checkpoints.py` 통과

주요 실패 신호:

- `CONTEXT_CHECKPOINT:` 신호만 있고 파일 없음
- checkpoint 파일에 남은 작업이 모호함
- 완료 snapshot 누락
