# Backend

{프로젝트명} 백엔드 문서. 아키텍처 가이드라인, 정책, 설계 문서로 구성된다.

---

## 디렉토리 구조

```
docs/backend/
├── getting-started.md # 오리엔테이션 (기술 스택, 로컬 실행)
├── architecture/      # 백엔드 아키텍처 지식 시스템
├── policies/          # 레이어를 관통하는 규칙·전략 (멀티테넌트, 보안, 로깅, DDL)
└── design/            # 기술 설계 문서 (TDD)
```

**어디로 가야 할지 모르겠다면**

| 작업 | 출발점 |
|------|-------|
| 아키텍처 단위·의존 경계·구현 전략 확인 | [architecture/README.md](architecture/README.md) |
| 테넌트/보안/로깅/DDL 등 전역 규칙 확인 | [policies/README.md](policies/README.md) |
| 새 기능/서브시스템 설계 | [design/README.md](design/README.md) |
| 로컬 환경 세팅 | [getting-started.md](getting-started.md) |

---

## 문서 맵

| 영역 | 진입점 | 설명 |
|------|--------|------|
| 시작하기 | [getting-started.md](getting-started.md) | 기술 스택, 로컬 실행, 프로필 |
| 아키텍처 | [architecture/README.md](architecture/README.md) | 백엔드 아키텍처 단위, 의존 경계, 구현 전략 |
| 정책 | [policies/README.md](policies/README.md) | 모든 레이어에 걸쳐 적용되는 기술 정책 |
| 설계 문서 | [design/README.md](design/README.md) | 기술설계문서 작성 규칙과 예시 |

---

## 아키텍처

아키텍처 문서의 단일 진입점은 [architecture/README.md](architecture/README.md)다. 세부 아키텍처 단위, 전략 문서, migration 상태는 해당 README가 소유한다.

---

## 크로스커팅 정책

프로젝트 도메인·아키텍처 선택과 무관하게, 모든 레이어에 걸쳐 일반적으로 적용되는 기술 정책은 [policies/README.md](policies/README.md)에서 관리한다.

---

## 설계 문서

기능·서브시스템의 기술 설계 문서(Technical Design Document)는 [design/README.md](design/README.md)에서 관리한다.

## 운영 원칙

- `docs/backend` 바로 아래 새 영역이 생기면 이 README의 문서 맵을 갱신한다.
- 하위 영역의 세부 문서 목록은 각 하위 디렉토리의 `README.md`가 소유한다.
- `AGENTS.md`는 개별 백엔드 문서가 아니라 이 README를 참조한다.
