---
name: write-api-spec
description: 기획 산출물, 업무 흐름, 도메인 상태, 화면 설계를 바탕으로 backend와 frontend가 병렬 구현할 수 있는 API 스펙을 작성하는 스킬. `plan-implementation-requirements` 결과를 구현 실행 스킬에 넘기기 전에 endpoint, request/response, error, auth, pagination, idempotency, cache, frontend 소비 계약을 확정해야 할 때 사용한다.
---

# Write API Spec

## 목적

`write-api-spec`는 기획 산출물을 backend/frontend 병렬 구현이 가능한 API 스펙으로 변환한다.

이 스킬은 API를 구현하지 않는다. backend 구현자는 서버 계약을, frontend 구현자는 소비 계약을 같은 artifact에서 읽을 수 있도록 endpoint, DTO, 오류, 권한, 상태, cache, 검증 기준을 고정한다.

이 스킬은 `api-contract-designer`가 직접 로드하는 역할 지침이 아니라, 메인 오케스트레이터가 `api-contract-designer`를 호출할 때 사용하는 workflow, input/output 계약, checkpoint schema의 단일 출처다.

## 적용 대상

포함:

- fullstack 기능 구현 전 API 계약이 필요한 경우
- frontend가 backend 응답을 소비해야 하는 경우
- backend API 변경이 화면 상태, 오류 처리, cache 갱신과 연결되는 경우
- 기존 API를 리팩토링하면서 request/response/error 계약을 다시 맞춰야 하는 경우

제외:

- backend handler, use case, storage 구현
- frontend API client, query hook, component 구현
- 제품 정책 자체를 새로 정하는 기획 작업

제품 정책과 화면 흐름이 불명확하면 먼저 `plan-implementation-requirements`로 돌아간다.

## 참조 문서

- API 계약 서브에이전트 계약: [references/api-contract-designer-contract.md](references/api-contract-designer-contract.md)
- API 스펙 템플릿: [references/api-spec-template.md](references/api-spec-template.md)

## 작업 흐름

### 1. 입력 산출물을 확인한다

- 기획 산출물의 목표, 업무 흐름, 정책, 상태, 화면 설계를 읽는다.
- API 스펙에 영향을 주는 open question이 남아 있는지 확인한다.
- backend와 frontend가 공유해야 할 도메인 용어와 데이터 의미를 추출한다.
- 기존 API 규칙이나 프로젝트 컨벤션이 있으면 source 후보로 포함한다.

차단 조건:

- 상태 전이 조건이 API side effect를 바꿀 정도로 불명확하다.
- 권한 또는 사용자 유형이 endpoint 접근 정책을 바꿀 정도로 불명확하다.
- 화면에서 필요한 데이터와 backend가 제공해야 할 데이터 의미가 충돌한다.
- 실패·재시도·취소 정책이 response/error 계약을 바꿀 수 있다.

### 2. API 스펙을 작성한다

메인 오케스트레이터는 [api-contract-designer-contract.md](references/api-contract-designer-contract.md)에 따라 input artifact를 만들고 `api-contract-designer` 서브에이전트를 호출한다.

호출 프롬프트에는 입력 파일 경로와 계약 파일 경로만 전달한다. `api-contract-designer` TOML에는 이 스킬 경로를 고정하지 않는다.

서브에이전트를 사용할 수 없으면 메인 오케스트레이터가 같은 계약과 템플릿을 따라 API 스펙을 직접 작성한다.

반드시 다룰 항목:

- operation id, method, path, 목적
- request path/query/body schema
- response schema와 상태 코드
- error code와 사용자 복구 가능성
- 인증·인가 정책
- pagination, sorting, filtering
- idempotency, concurrency, retry
- cache와 invalidation 힌트
- frontend loading, empty, success, error 소비 계약
- backend use case, transaction, side effect 힌트
- contract test 또는 mock scenario

### 3. 병렬 구현 가능성을 판정한다

- API 스펙의 `stable_for_parallel`이 `true`인 경우 backend/frontend 마일스톤을 같은 API artifact 기준으로 병렬 실행할 수 있다.
- `false`이면 backend 선행 구현 또는 사용자 확인이 필요한 blocker를 남긴다.
- 부분 안정화된 경우 operation 단위로 병렬 가능 여부를 나눈다.

### 4. 실행 스킬 입력으로 넘긴다

완료된 API 스펙은 아래 입력으로 전달한다.

- `implement-backend`: endpoint, auth, request/response, error, transaction, side effect, contract test
- `implement-frontend`: operation id, DTO, UI state mapping, loading/error/empty/success, cache, mock scenario

## 검증

- `api-contract-designer` 계약 문서와 템플릿 링크가 실제 파일을 가리키는지 확인한다.
- output artifact에 operation, request, response, error, auth, cache, mock, contract test 후보가 있는지 확인한다.
- `stable_for_parallel`이 `false`인 operation은 blocker와 후속 처리 방향을 포함하는지 확인한다.
- 스킬 수정 후 `quick_validate.py`와 `check_structured_artifact.py`를 실행한다.

## 완료 기준

- backend와 frontend가 같은 operation id와 DTO 의미를 사용한다.
- request, response, error, auth, 상태 코드가 endpoint별로 명확하다.
- 화면 상태와 API 성공·실패·빈 응답이 연결되어 있다.
- backend side effect와 frontend cache 갱신 조건이 드러난다.
- 병렬 구현 가능 여부와 blocker가 operation 단위로 표시되어 있다.
