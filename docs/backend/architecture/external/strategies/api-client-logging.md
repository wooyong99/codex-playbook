# ApiClient 로깅 컨벤션

이 문서는 외부 API 호출 로그를 남기는 전략을 정리한다.

## 목적

- 외부 API 호출의 요청, 응답, 실패, 소요시간을 추적 가능하게 한다.
- Provider와 API 단위로 장애를 검색할 수 있게 한다.
- 민감 정보가 로그에 원문으로 남지 않게 한다.

## 적용 범위

- ApiClient public method 호출 로그
- Adapter 예외 변환 로그
- Mock Adapter 로컬 디버깅 로그
- token, 계좌번호, 핀번호, payload 같은 민감 정보 마스킹

민감 정보 처리 정책은 [logging policy](../../../policies/logging.md)와 [security policy](../../../policies/security.md)를 함께 따른다.

## 책임

- 외부 호출의 시작과 종료를 기록한다.
- 실패 원인과 Provider 예외 분류를 기록한다.
- 소요시간과 endpoint 정보를 기록한다.
- 민감 정보는 마스킹하거나 생략한다.

## 전체 흐름

```text
ApiClient public method
  -> request log
  -> external call
  -> response log with elapsed time
  -> exception log when failed
```

## 세부 규칙

### 필수 로깅 항목

| 항목 | 설명 |
|------|------|
| provider | 외부 시스템 식별자 |
| apiName | 호출 API 이름 |
| httpMethod | GET, POST, PUT 등 |
| endpoint | 호출 endpoint |
| request | 요청 요약 또는 body 없음 표시 |
| response | 성공/실패, 응답 code |
| elapsedTime | 호출 소요시간 |

### 로그 위치

- ApiClient는 외부 HTTP 호출 시작과 종료를 기록한다.
- Adapter는 Port Result 변환 시 비즈니스 식별자와 변환 결과를 기록한다.
- Mock Adapter는 `[MOCK-기능]` prefix로 실 호출 로그와 구분한다.

### 민감 정보

- token, API key, authorization header는 로그에 남기지 않는다.
- 핀번호, 카드번호, 계좌번호는 일부만 남기고 마스킹한다.
- 원문 request/response payload는 민감 정보 포함 가능성이 있으면 요약만 남긴다.

## 금지 규칙

- 외부 API를 호출하는 public method를 로깅 없이 추가하지 않는다.
- token, API key, authorization header를 로그에 남기지 않는다.
- 핀번호, 카드번호, 계좌번호 전체를 로그에 남기지 않는다.
- 원문 payload를 검토 없이 통째로 로그에 남기지 않는다.
- 실패 로그에서 cause를 완전히 숨겨 운영 추적이 불가능하게 만들지 않는다.

## 예외와 경계

- provider가 별도 감사 로그를 요구하면 보안 정책과 함께 별도 마스킹 기준을 둔다.
- Body가 없는 요청은 요청 본문 없음으로 명시한다.
- payload 전체 기록이 꼭 필요하면 샘플링과 마스킹 정책을 먼저 정의한다.

## 완료 기준

- 모든 외부 호출 public method에서 요청, 응답, 소요시간을 추적할 수 있다.
- 외부 호출 실패가 Provider와 API 이름으로 검색 가능하다.
- 민감 정보가 로그에 원문으로 남지 않는다.
