# API Spec Template

이 문서는 API 스펙 작성 시 포함할 항목과 품질 기준을 정의한다.

## 목적

API 스펙은 backend와 frontend가 같은 계약을 보고 독립적으로 작업할 수 있게 만드는 실행 계약이다.

## 스펙 작성 순서

1. 기획 산출물에서 사용자 흐름과 상태 전이를 읽는다.
2. command, query, event 후보를 operation으로 분류한다.
3. 화면에 필요한 데이터와 backend가 보장해야 할 도메인 의미를 맞춘다.
4. request, response, error, auth, side effect를 endpoint별로 쓴다.
5. cache, idempotency, pagination, filtering, sorting을 필요한 operation에만 붙인다.
6. mock scenario와 contract test 후보를 만든다.
7. operation별 병렬 구현 가능 여부를 표시한다.

## Operation 필수 항목

- operation id
- HTTP method와 path
- 업무 목적과 연결된 사용자 흐름
- 인증·인가 정책
- request path/query/body schema
- validation rule
- response status와 body schema
- error status, error code, message policy, recovery
- side effect
- cache key와 invalidation 조건
- idempotency 또는 conflict 정책
- backend 구현 힌트
- frontend 소비 힌트
- contract test와 mock scenario

## 공통 정책

### 오류

- 사용자에게 보여줄 수 있는 메시지와 내부 로그용 메시지를 구분한다.
- 권한 실패, 검증 실패, 상태 충돌, 중복 요청, 외부 연동 실패를 분리한다.
- frontend가 복구 액션을 보여줄 수 있는 오류에는 recovery를 적는다.

### 목록 조회

- pagination, filtering, sorting은 프로젝트 컨벤션이 있으면 따른다.
- empty response가 오류인지 빈 상태인지 명확히 쓴다.
- 검색 조건의 기본값과 최대 제한을 적는다.

### 변경 요청

- 상태 변경 operation은 전이 전 상태, 전이 후 상태, guard, side effect를 적는다.
- 중복 제출 위험이 있으면 idempotency key 또는 conflict policy를 적는다.
- optimistic update 가능 여부와 실패 시 rollback 방식을 적는다.

### 캐시

- frontend cache key 힌트는 도메인 식별자와 query 조건을 포함한다.
- 변경 operation은 무효화해야 할 query 또는 detail cache를 적는다.
- 실시간 동기화, polling, refresh가 필요하면 조건을 적는다.

## 완료 점검

- backend 구현자는 endpoint별 use case와 transaction 경계를 알 수 있다.
- frontend 구현자는 화면 상태별 API 소비 방식을 알 수 있다.
- request/response/error shape가 mock으로 구현 가능하다.
- 모든 operation에 병렬 구현 가능 여부가 있다.
- blocker가 있으면 사용자 질문 또는 backend 선행 작업으로 분리되어 있다.
