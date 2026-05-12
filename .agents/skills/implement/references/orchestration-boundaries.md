# Orchestration Boundaries

이 문서는 `implement` 스킬 패밀리에서 메인 에이전트와 D/A/B 서브에이전트가 맡는 책임 경계를 정리한다. 실행 루프의 상세 단계는 [milestone-execution-workflow.md](milestone-execution-workflow.md)가 소유하고, 입출력 포맷은 각 계약 문서가 소유한다.

## 참여 주체

| 주체 | 책임 | 계약 문서 |
|------|------|-----------|
| 메인 에이전트 | 요구사항 분석, 마일스톤 분할, D/A/B 호출, handoff 검증, 반복 종료 판단, 사용자 보고 | 이 문서와 `SKILL.md` |
| Agent D `backend-technical-design-writer` | 백엔드 마일스톤별 TDD 작성 또는 스킵 근거 작성 | `implement-backend/references`의 D 계약 |
| Agent D `frontend-technical-design-writer` | 프론트엔드 마일스톤별 TDD 작성 또는 스킵 근거 작성 | `implement-frontend/references`의 D 계약 |
| Agent A `backend-implementation-engineer` | 백엔드 코드 작성·수정, 테스트, 빌드 확인, 구현 결과 파일 작성 | `implement-backend/references`의 A 계약 |
| Agent A `frontend-implementation-engineer` | 프론트엔드 코드 작성·수정, 테스트, 빌드 확인, 구현 결과 파일 작성 | `implement-frontend/references`의 A 계약 |
| Agent B `backend-architecture-reviewer` | 입력으로 전달된 백엔드 아키텍처 기준과 관련 TDD 결정 준수 여부 검토 | `implement-backend/references`의 B 계약 |
| Agent B `frontend-architecture-reviewer` | 입력으로 전달된 프론트엔드 아키텍처 기준과 관련 TDD 결정 준수 여부 검토 | `implement-frontend/references`의 B 계약 |
| Supplemental reviewers | 문서, 보안 민감 변경 검토 | [review routing](../../../../docs/review/README.md) |

서브에이전트 정의 파일:

- [backend-technical-design-writer.toml](../../../../.codex/agents/backend-technical-design-writer.toml)
- [frontend-technical-design-writer.toml](../../../../.codex/agents/frontend-technical-design-writer.toml)
- [backend-implementation-engineer.toml](../../../../.codex/agents/backend-implementation-engineer.toml)
- [frontend-implementation-engineer.toml](../../../../.codex/agents/frontend-implementation-engineer.toml)
- [backend-architecture-reviewer.toml](../../../../.codex/agents/backend-architecture-reviewer.toml)
- [frontend-architecture-reviewer.toml](../../../../.codex/agents/frontend-architecture-reviewer.toml)
- [documentation-governance-reviewer.toml](../../../../.codex/agents/documentation-governance-reviewer.toml)
- [security-policy-reviewer.toml](../../../../.codex/agents/security-policy-reviewer.toml)

각 `.toml` 파일은 역할, 판단 철학, 기본 금지사항만 가진다. 어떤 기준 문서를 읽을지, 어떤 출력 규격을 따를지, handoff artifact 스키마, 프롬프트 필드 이름, 결과 신호, 체크포인트 판단 기준, 체크포인트 파일 템플릿은 실행 workflow와 계약 문서가 단일 출처다.

## 메인 에이전트 제약

- 메인 에이전트는 일반 경로에서 구현 파일을 직접 수정하지 않는다.
- 코드 작업은 변경 영역에 맞는 A에게, 설계 문서는 D에게, 아키텍처 검토는 변경 영역에 맞는 B에게 위임한다.
- 요구사항 이해에 필요한 경우 `docs/backend/README.md` 같은 맵 문서 하나 정도는 읽을 수 있다.
- 정상 산출물 전달과 체크포인트 복구를 위해 `[결과 파일]`과 `[체크포인트 파일]`을 읽고 존재 여부와 스키마를 검증할 수 있다.
- 검토를 직접 수행하지 않는다. B의 결과를 읽어 반복 종료 여부만 판단한다.
- 변경 파일이 문서 또는 보안 민감 영역을 포함하면 [review routing](../../../../docs/review/README.md)에 따라 supplemental reviewer 결과도 함께 확인한다.
- D/A/B는 서로 호출하지 않는다. 모든 통신은 메인 에이전트를 경유한다.

## Agent D 라우팅

- 백엔드 코드, backend 문서, DB/schema, 서버 설정 변경이 필요한 마일스톤은 `backend-technical-design-writer`를 호출한다.
- 프론트엔드 코드, frontend 문서, UI/상태/API client/cache/rendering 변경이 필요한 마일스톤은 `frontend-technical-design-writer`를 호출한다.
- 백엔드와 프론트엔드가 모두 필요한 요청은 마일스톤을 가능한 한 영역별로 분리하고, 각 영역의 D 결과 파일을 따로 생성한다.
- 단일 마일스톤 안에서 분리할 수 없으면 backend D와 frontend D를 각각 별도 `[결과 파일]`, `[체크포인트 파일]`로 호출하고, 각 영역 A에게 자기 D 결과 파일만 전달한다.

## Agent A 라우팅

- 백엔드 코드나 `docs/backend/**` 구현 영향이 있는 마일스톤은 `backend-implementation-engineer`를 호출한다.
- 프론트엔드 코드나 `docs/frontend/**` 구현 영향이 있는 마일스톤은 `frontend-implementation-engineer`를 호출한다.
- 백엔드와 프론트엔드가 모두 필요한 요청은 마일스톤을 가능한 한 영역별로 분리한다.
- 분리할 수 없는 단일 사용자 흐름이면 backend A와 frontend A를 각각 별도 결과 파일로 호출하고, 변경 파일 집합과 검증 결과를 합쳐 다음 검토 단계로 넘긴다.
- 위반 수정은 해당 위반 파일을 수정한 A 인스턴스에 다시 맡긴다. backend 위반은 backend A, frontend 위반은 frontend A가 수정한다.

## Agent B 라우팅

- 백엔드 변경 파일은 `backend-architecture-reviewer`가 검토한다.
- 프론트엔드 변경 파일은 `frontend-architecture-reviewer`가 검토한다.
- 백엔드와 프론트엔드 변경이 모두 있으면 각 B를 별도 결과 파일과 체크포인트 파일로 호출한다.
- 각 B는 자신에게 할당된 영역의 변경 파일만 검토한다. 다른 영역 위반을 추측하거나 대신 판정하지 않는다.
- 문서 구조 변경은 `documentation-governance-reviewer`, 보안 민감 변경은 `security-policy-reviewer`를 supplemental reviewer로 추가한다.
- 마일스톤 완료는 호출된 모든 B와 blocker/major supplemental reviewer가 통과해야 한다.

## 인스턴스 생명주기

- D 호출은 매번 새 인스턴스로 수행한다.
- B 호출은 매번 새 인스턴스로 수행한다.
- A 호출은 마일스톤 첫 구현에서 영역별 새 인스턴스로 수행한다.
- 같은 마일스톤 안의 위반 수정과 체크포인트 재개는 해당 영역의 동일 A 인스턴스를 이어서 사용한다.
- 마일스톤이 바뀌면 영역별 A도 새 인스턴스로 시작한다.

## 판단 원칙

- B의 `status: pass`는 문서 준수 통과를 뜻한다. 기능 정확성, 성능, 운영 안정성 전체를 보증하는 의미가 아니다.
- D/A/B 프롬프트의 `[프로젝트 컨텍스트]`는 현재 저장소 문서와 코드에서 확인한 사실로 채운다.
- 계약 문서의 예시 문구를 프로젝트 사실처럼 복사하지 않는다.
- 정상 산출물 전달의 표준 경로는 handoff artifact 파일과 결과 신호다.
- 체크포인트 복구의 표준 경로는 체크포인트 파일과 `CONTEXT_CHECKPOINT:` 신호다.
- 정상 완료 경로에서도 각 역할은 호출별 `[체크포인트 파일]`을 반드시 남긴다.
