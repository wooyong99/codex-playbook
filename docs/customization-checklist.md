# 커스터마이징 체크리스트

이 저장소를 다른 프로젝트에 가져갔을 때 최소한 점검해야 하는 항목들.

## 프로젝트 컨텍스트

- [ ] `AGENTS.md`의 프로젝트명 채움
- [ ] `AGENTS.md`의 비즈니스 목표 채움
- [ ] `docs/backend/README.md`의 프로젝트명 채움
- [ ] `docs/frontend/README.md`의 프로젝트명 채움

## 문서 구조

- [ ] `docs/backend`를 실제 백엔드 구조에 맞게 유지
- [ ] `docs/frontend`를 실제 프론트엔드 구조에 맞게 유지
- [ ] `docs/backend/policies/README.md` 링크 최신화
- [ ] `docs/backend/design/README.md` 링크 최신화
- [ ] 새 디렉토리가 생기면 해당 영역의 가장 가까운 `README.md` 문서 맵 갱신
- [ ] `AGENTS.md`는 `docs/backend/README.md`, `docs/frontend/README.md` 같은 최상위 진입점 경로가 바뀔 때만 갱신

## 스킬

- [ ] `.agents/skills/setup-project-context`가 현재 프로젝트에도 맞는지 확인
- [ ] `.agents/skills/implement`의 계약 문서와 지시가 현재 프로젝트 규칙에 맞는지 확인
- [ ] 기존 코드베이스가 있다면 `reverse-engineer-backend-docs` 적용 여부 결정
- [ ] 프로젝트에 필요 없는 스킬은 제거 또는 수정

## 서브에이전트

- [ ] `.codex/agents/design-writer.toml` 검토
- [ ] `.codex/agents/code-writer.toml` 검토
- [ ] `.codex/agents/architecture-reviewer.toml` 검토
- [ ] 계약 문서 경로와 참조 문서 경로가 현재 저장소와 일치하는지 확인
- [ ] sandbox 설정이 현재 프로젝트 작업 방식과 맞는지 확인

## 백엔드

- [ ] 백엔드 문서가 실제 코드 구조, 실행 방법, 정책, 아키텍처 단위를 반영하는지 확인
- [ ] 정책 문서가 실제 보안/로깅/트랜잭션 규칙과 맞는지 확인
- [ ] 설계 문서 작성 규칙이 팀 방식과 맞는지 확인

## 프론트엔드

- [ ] 아키텍처 문서가 실제 폴더 구조와 맞는지 확인
- [ ] 컨벤션 문서가 실제 기술 스택과 맞는지 확인
- [ ] 성능/UI-UX 가이드가 실제 제품 성격과 맞는지 확인
