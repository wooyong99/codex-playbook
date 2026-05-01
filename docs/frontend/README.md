# Frontend

{프로젝트명} 프론트엔드 문서. 아키텍처, 컨벤션, 성능, UI/UX 가이드라인으로 구성된다.

---

## 디렉토리 구조

```
docs/frontend/
├── getting-started.md  # 오리엔테이션 (기술 스택, 프로젝트 구성, 로컬 실행)
├── architecture/       # FSD 아키텍처, 폴더 구조, 상태 관리
├── conventions/        # 코드/네이밍/컴포넌트/API 컨벤션
├── performance/        # 렌더링/캐싱/리스트 최적화
└── ui-ux/              # UI 원칙, UX 가이드라인, 로딩·피드백, 모달
```

---

## 문서 맵

| 영역 | 진입점 | 설명 |
|------|--------|------|
| 시작하기 | [getting-started.md](getting-started.md) | 기술 스택, 프로젝트 구성, 로컬 실행 |
| 아키텍처 | [architecture/README.md](architecture/README.md) | FSD 아키텍처, 폴더 구조, 상태 관리 |
| 컨벤션 | [conventions/README.md](conventions/README.md) | 코드, 네이밍, 컴포넌트, API 컨벤션 |
| 성능 | [performance/README.md](performance/README.md) | 렌더링, 캐싱, 리스트 최적화 |
| UI / UX | [ui-ux/README.md](ui-ux/README.md) | UI 원칙, UX 가이드라인, 로딩·피드백, 모달 |

---

## 운영 원칙

- `docs/frontend` 바로 아래 새 영역이 생기면 이 README의 문서 맵을 갱신한다.
- 하위 영역의 세부 문서 목록은 각 하위 디렉토리의 `README.md`가 소유한다.
- `AGENTS.md`는 개별 프론트엔드 문서가 아니라 이 README를 참조한다.
