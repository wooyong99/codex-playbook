# Backend

{프로젝트명} 백엔드 문서. 아키텍처, 정책, 설계 문서, 실행 안내로 구성된다.

## 문서 맵

| 영역 | 진입점 | 설명 |
|------|--------|------|
| 시작하기 | [getting-started.md](getting-started.md) | 기술 스택, 로컬 실행, 프로필 |
| 아키텍처 | [architecture/README.md](architecture/README.md) | 백엔드 아키텍처 단위, 의존 경계, 구현 전략 |
| 정책 | [policies/README.md](policies/README.md) | 모든 레이어에 걸쳐 적용되는 기술 정책 |
| 설계 문서 | [design/README.md](design/README.md) | 기술설계문서 목록과 예시 |

## 문서 경계

정책 원문은 `policies`, 실제 코드 구조는 `architecture`, 반복 구현 방식은 `architecture/{actual-unit}/strategies`가 소유한다.
