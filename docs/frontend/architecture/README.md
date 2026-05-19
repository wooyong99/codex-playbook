# Frontend Architecture

## 목적

이 디렉토리는 프론트엔드 코드를 **Feature-Sliced Design(FSD)** 원칙으로 설계·리뷰·리팩토링하기 위한 아키텍처 기준을 소유한다.

현재 코드베이스의 레거시 구조를 설명하는 문서가 아니라, 앞으로의 설계 판단과 구조 개선에 사용할 목표 아키텍처 문서다.

## 적용 범위

포함:

- FSD 레이어, 슬라이스, 세그먼트 책임
- Public API, import, shared 사용 규칙
- 상태 관리, 서버 캐시, mutation, query key 전략
- 라우팅, composition, 비즈니스 로직 위치, error/loading 전략
- 테스트, 성능 최적화, 구조 분리 의사결정 기준

제외:

- 현재 레거시 코드의 파일별 설명
- 특정 UI 라이브러리 사용법
- 백엔드 API 계약의 상세 스펙
- 화면별 기능 요구사항

## 문서 소유권

- [frontend-architecture](frontend-architecture.md): FSD 레이어·슬라이스·세그먼트·Public API·import 규칙의 단일 기준
- [folder-structure](folder-structure.md): 표준 폴더 구조, naming, barrel export, 파일 배치 예시
- [state-management](state-management.md): local state, Zustand, React Query, query key, mutation 전략
- [routing-and-composition](routing-and-composition.md): AppRouter, route ownership, lazy loading, layout route, composition 패턴
- [runtime-strategies](runtime-strategies.md): 비즈니스 로직 위치, API error, auth 만료, toast, form error, loading/empty/retry
- [testing-and-performance](testing-and-performance.md): slice 테스트, MSW, integration 기준, memoization, virtualization, code splitting
- [decision-guide](decision-guide.md): 언제 분리·추상화·shared 승격·entity/feature/widget/page 선택을 하는지 판단 기준

## 읽는 순서

1. `frontend-architecture.md`에서 FSD 경계와 import 규칙을 먼저 확인한다.
2. `folder-structure.md`에서 실제 파일 배치와 naming을 확인한다.
3. 상태나 서버 데이터가 관련되면 `state-management.md`를 확인한다.
4. route/page/widget 조합 문제는 `routing-and-composition.md`를 확인한다.
5. API 실패, loading, form, toast 기준은 `runtime-strategies.md`를 확인한다.
6. 테스트·성능 판단은 `testing-and-performance.md`를 확인한다.
7. 구조 판단이 애매하면 `decision-guide.md`의 체크리스트로 결정한다.

## 운영 원칙

- 이 디렉토리의 문서는 현재 코드 형태보다 목표 구조와 판단 기준을 우선한다.
- 같은 규칙을 여러 문서에 반복하지 않는다. 한 문서가 소유하고 다른 문서는 링크한다.
- 신규 architecture 문서를 추가하면 이 README의 문서 소유권과 읽는 순서를 갱신한다.
- 상세 구현 예시는 원칙을 설명하는 범위에서만 둔다. 화면별 구현 절차는 feature 설계 문서가 소유한다.
