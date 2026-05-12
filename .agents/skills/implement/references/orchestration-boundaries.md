# Orchestration Boundaries

이 문서는 `implement` 스킬에서 메인 에이전트와 D/A/B 서브에이전트가 맡는 책임 경계를 정리한다. 실행 루프의 상세 단계는 [milestone-execution-workflow.md](milestone-execution-workflow.md)가 소유하고, 입출력 포맷은 각 계약 문서가 소유한다.

## 참여 주체

| 주체 | 책임 | 계약 문서 |
|------|------|-----------|
| 메인 에이전트 | 요구사항 분석, 마일스톤 분할, D/A/B 호출, handoff 검증, 반복 종료 판단, 사용자 보고 | 이 문서와 `SKILL.md` |
| Agent D `design-writer` | 마일스톤별 TDD 작성 또는 스킵 근거 작성 | [design-writer-contract.md](design-writer-contract.md) |
| Agent A `code-writer` | 코드 작성·수정, 테스트, 빌드 확인, 구현 결과 파일 작성 | [code-writer-contract.md](code-writer-contract.md) |
| Agent B `architecture-reviewer` | `docs/backend/architecture/*`, `docs/backend/policies/*`, 관련 TDD 결정 준수 여부 검토 | [architecture-reviewer-contract.md](architecture-reviewer-contract.md) |
| Supplemental reviewers | 프론트엔드, 문서, 보안 민감 변경 검토 | [review routing](../../../../docs/review/README.md) |

서브에이전트 정의 파일:

- [design-writer.toml](../../../../.codex/agents/design-writer.toml)
- [code-writer.toml](../../../../.codex/agents/code-writer.toml)
- [architecture-reviewer.toml](../../../../.codex/agents/architecture-reviewer.toml)
- [frontend-reviewer.toml](../../../../.codex/agents/frontend-reviewer.toml)
- [docs-reviewer.toml](../../../../.codex/agents/docs-reviewer.toml)
- [security-reviewer.toml](../../../../.codex/agents/security-reviewer.toml)

각 `.toml` 파일은 역할과 실행 제약만 가진다. handoff artifact 스키마, 프롬프트 필드 이름, 결과 신호, 체크포인트 판단 기준, 체크포인트 파일 템플릿은 계약 문서가 단일 출처다.

## 메인 에이전트 제약

- 메인 에이전트는 일반 경로에서 구현 파일을 직접 수정하지 않는다.
- 코드 작업은 A에게, 설계 문서는 D에게, 아키텍처 검토는 B에게 위임한다.
- 요구사항 이해에 필요한 경우 `docs/backend/README.md` 같은 맵 문서 하나 정도는 읽을 수 있다.
- 정상 산출물 전달과 체크포인트 복구를 위해 `[결과 파일]`과 `[체크포인트 파일]`을 읽고 존재 여부와 스키마를 검증할 수 있다.
- 검토를 직접 수행하지 않는다. B의 결과를 읽어 반복 종료 여부만 판단한다.
- 변경 파일이 프론트엔드, 문서, 보안 민감 영역을 포함하면 [review routing](../../../../docs/review/README.md)에 따라 supplemental reviewer 결과도 함께 확인한다.
- D/A/B는 서로 호출하지 않는다. 모든 통신은 메인 에이전트를 경유한다.

## 인스턴스 생명주기

- D 호출은 매번 새 인스턴스로 수행한다.
- B 호출은 매번 새 인스턴스로 수행한다.
- A 호출은 마일스톤 첫 구현에서 새 인스턴스로 수행한다.
- 같은 마일스톤 안의 위반 수정과 체크포인트 재개는 동일 A 인스턴스를 이어서 사용한다.
- 마일스톤이 바뀌면 A도 새 인스턴스로 시작한다.

## 판단 원칙

- B의 `status: pass`는 문서 준수 통과를 뜻한다. 기능 정확성, 성능, 운영 안정성 전체를 보증하는 의미가 아니다.
- D/A/B 프롬프트의 `[프로젝트 컨텍스트]`는 현재 저장소 문서와 코드에서 확인한 사실로 채운다.
- 계약 문서의 예시 문구를 프로젝트 사실처럼 복사하지 않는다.
- 정상 산출물 전달의 표준 경로는 handoff artifact 파일과 결과 신호다.
- 체크포인트 복구의 표준 경로는 체크포인트 파일과 `CONTEXT_CHECKPOINT:` 신호다.
- 정상 완료 경로에서도 각 역할은 호출별 `[체크포인트 파일]`을 반드시 남긴다.
