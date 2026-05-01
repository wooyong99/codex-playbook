# Frontend Architecture

프론트엔드 아키텍처 문서의 단일 진입점.

## 문서 목록

- [frontend-architecture](frontend-architecture.md): FSD 개요, 레이어 정의, 단방향 의존성 규칙
- [folder-structure](folder-structure.md): 패키지 구조, 세그먼트 역할, 네이밍 규칙
- [state-management](state-management.md): 전역 상태 기준, props drilling 방지, derived state, 캐시 invalidation

## 운영 원칙

- 아키텍처 문서를 추가·수정할 때 이 README의 문서 목록을 함께 갱신한다.
- 상위 문서(예: `docs/frontend/README.md`)는 개별 아키텍처 파일이 아닌 이 README를 참조한다.
