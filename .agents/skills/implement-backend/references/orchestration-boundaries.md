# Backend Orchestration Boundaries

이 문서는 `implement-backend` 스킬에서 메인 에이전트와 backend D/A/B 서브에이전트가 맡는 책임 경계를 정리한다. 실행 루프의 상세 단계는 [milestone-execution-workflow.md](milestone-execution-workflow.md)가 소유하고, 입출력 포맷은 각 backend 계약 문서가 소유한다.

## 참여 주체

| 주체 | 책임 | 계약 문서 |
|------|------|-----------|
| 메인 에이전트 | backend 요구사항 분석, 마일스톤 분할, D/A/B 호출, handoff 검증, 반복 종료 판단, 사용자 보고 | 이 문서와 `SKILL.md` |
| Agent D `backend-technical-design-writer` | backend 마일스톤별 TDD 작성 또는 스킵 근거 작성 | [backend-technical-design-writer-contract.md](backend-technical-design-writer-contract.md) |
| Agent A `backend-implementation-engineer` | backend 코드 작성·수정, compile/test 확인, 구현 결과 파일 작성 | [backend-implementation-engineer-contract.md](backend-implementation-engineer-contract.md) |
| Agent B `backend-architecture-reviewer` | 입력으로 전달된 backend 아키텍처 기준과 TDD 결정 준수 여부 검토 | [backend-architecture-reviewer-contract.md](backend-architecture-reviewer-contract.md) |
| Supplemental reviewers | 문서, 보안 민감 변경 검토 | [review routing](../../../../docs/review/README.md) |

서브에이전트 정의 파일:

- [backend-technical-design-writer.toml](../../../../.codex/agents/backend-technical-design-writer.toml)
- [backend-implementation-engineer.toml](../../../../.codex/agents/backend-implementation-engineer.toml)
- [backend-architecture-reviewer.toml](../../../../.codex/agents/backend-architecture-reviewer.toml)
- [documentation-governance-reviewer.toml](../../../../.codex/agents/documentation-governance-reviewer.toml)
- [security-policy-reviewer.toml](../../../../.codex/agents/security-policy-reviewer.toml)

각 `.toml` 파일은 역할, 판단 철학, 기본 금지사항만 가진다. 어떤 기준 문서를 읽을지, 어떤 출력 규격을 따를지, handoff artifact 스키마, 프롬프트 필드 이름, 결과 신호, 체크포인트 판단 기준, 체크포인트 파일 템플릿은 backend workflow와 계약 문서가 단일 출처다.

## 메인 에이전트 제약

- 일반 경로에서 backend 구현 파일을 직접 수정하지 않는다.
- backend 코드 작업은 A에게, backend 설계 문서는 D에게, backend 아키텍처 검토는 B에게 위임한다.
- 요구사항 이해에 필요한 경우 `docs/backend/README.md` 같은 맵 문서와 관련 Source of Truth 후보를 읽을 수 있다.
- 정상 산출물 전달과 체크포인트 복구를 위해 `[결과 파일]`과 `[체크포인트 파일]`을 읽고 존재 여부와 스키마를 검증할 수 있다.
- B의 검토를 직접 대체하지 않는다. B의 결과를 읽어 반복 종료 여부만 판단한다.
- 변경 파일이 문서 또는 보안 민감 영역을 포함하면 [review routing](../../../../docs/review/README.md)에 따라 supplemental reviewer 결과도 함께 확인한다.
- D/A/B는 서로 호출하지 않는다. 모든 통신은 메인 에이전트를 경유한다.

## Agent D 라우팅

- backend 코드, backend 문서, DB/schema, 서버 설정 변경이 필요한 마일스톤은 `backend-technical-design-writer`를 호출한다.
- 단순 오타, 테스트 fixture 보정, 이미 TDD가 충분한 작은 수정은 D가 `TDD_SKIPPED`를 반환할 수 있다.
- frontend 화면, route, component, client cache 변경은 D 범위에 포함하지 않는다.

## Agent A 라우팅

- backend 코드나 `docs/backend/**` 구현 영향이 있는 마일스톤은 `backend-implementation-engineer`를 호출한다.
- frontend 변경이 필요하면 직접 구현하지 않고 `implement-frontend` 마일스톤으로 넘길 계약 또는 미해결 사항을 남긴다.
- 위반 수정은 같은 backend A 인스턴스에 다시 맡긴다.

## Agent B 라우팅

- backend 변경 파일은 `backend-architecture-reviewer`가 검토한다.
- B는 자신에게 할당된 backend 변경 파일만 검토한다. frontend 위반을 추측하거나 대신 판정하지 않는다.
- 문서 구조 변경은 `documentation-governance-reviewer`, 보안 민감 변경은 `security-policy-reviewer`를 supplemental reviewer로 추가한다.
- 마일스톤 완료는 backend B와 blocker/major supplemental reviewer가 통과해야 한다.

## 인스턴스 생명주기

- D 호출은 매번 새 인스턴스로 수행한다.
- B 호출은 매번 새 인스턴스로 수행한다.
- A 호출은 마일스톤 첫 구현에서 새 인스턴스로 수행한다.
- 같은 마일스톤 안의 위반 수정과 체크포인트 재개는 동일 A 인스턴스를 이어서 사용한다.
- 마일스톤이 바뀌면 A도 새 인스턴스로 시작한다.

## 판단 원칙

- B의 `status: pass`는 backend 문서 준수 통과를 뜻한다. 기능 정확성, 성능, 운영 안정성 전체를 보증하는 의미가 아니다.
- D/A/B 프롬프트의 `[프로젝트 컨텍스트]`는 현재 저장소 문서와 코드에서 확인한 사실로 채운다.
- 계약 문서의 예시 문구를 프로젝트 사실처럼 복사하지 않는다.
- 정상 산출물 전달의 표준 경로는 handoff artifact 파일과 결과 신호다.
- 체크포인트 복구의 표준 경로는 체크포인트 파일과 `CONTEXT_CHECKPOINT:` 신호다.
- 정상 완료 경로에서도 각 역할은 호출별 `[체크포인트 파일]`을 반드시 남긴다.
