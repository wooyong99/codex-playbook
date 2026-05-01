# Backend Policies

백엔드 전 레이어에 공통 적용되는 크로스커팅 정책 문서 모음.

## 문서 목록

- [security](./security.md): 인증/인가, 민감 정보 처리, 보안 기본 원칙을 확인할 때
- [logging](./logging.md): 로그 레벨, 필드 표준, 운영 관측성 규칙을 확인할 때
- [transaction-and-consistency](./transaction-and-consistency.md): 트랜잭션 경계, 정합성 모델, 이벤트 기반 처리 규칙을 확인할 때
- [concurrency-and-performance](./concurrency-and-performance.md): 동시성 제어, 성능 최적화, 병목 대응 원칙을 확인할 때

## 운영 원칙

- 정책 문서를 추가/수정할 때 이 README의 문서 목록을 함께 갱신한다.
- 정책 문서는 전역 핵심 원칙, 금지 규칙, 안티패턴만 소유한다.
- 실제 코드 구조와 반복 구현 방식은 `docs/backend/architecture` 하위 문서에서 정책을 링크해 설명한다.
