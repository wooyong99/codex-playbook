# Logging Policy

## 적용 범위

- API 요청·응답 흐름의 운영 로그
- application 상태 변경과 실패 로그
- 외부 API 호출 로그
- MDC 기반 요청 추적

## 핵심 원칙

- 4xx 응답은 `WARN`, 5xx 응답은 `ERROR`와 stacktrace로 기록한다.
- 정상 요청은 필요한 범위에서 `INFO` 이하로만 남긴다.
- 요청 스코프에는 `tenantId`, `requestId`를 MDC로 전파한다.
- 로그 메시지는 `[SCOPE] 행위 설명 - key=value` 형식을 따른다.
- Grafana + Loki 환경에서는 logfmt 스타일 평문을 기본으로 사용한다.
- 개인정보, 비밀번호, 토큰, 카드 정보 등 민감 데이터는 로그에 남기지 않는다.

## 금지 규칙

- 민감 데이터를 원문으로 로깅하지 않는다.
- `[SCOPE]` 태그 없이 도메인 추적이 어려운 로그를 남기지 않는다.
- 파라미터를 자연어 문장에 섞어 logfmt 파싱이 불가능하게 만들지 않는다.
- ` - ` 구분자 없이 설명과 파라미터 경계를 흐리지 않는다.

## 안티패턴

- 클래스마다 raw logger 선언을 반복해 지연 평가와 logger 이름 일관성을 잃는다.
- 예외를 삼키고 로그만 남긴다.
- DTO 전체를 출력하면서 민감 필드 마스킹을 누락한다.
- 로그 레벨 기준 없이 모든 실패를 `ERROR`로 남긴다.

## 코드 근거

- `app` filter/interceptor - `requestId`, `tenantId` MDC 주입
- `application` 상태 변경 처리 - 성공 직후와 반환 직전 로그
- `external` ApiClient - 외부 호출 성공/실패 로그
- `logback-spring.xml` - 출력 패턴과 MDC 키

## 관련 아키텍처 문서

- [architecture/app](../architecture/app/app-guidelines.md) - 요청 추적과 전역 예외 처리
- [architecture/application](../architecture/application/application-guidelines.md) - 상태 변경 흐름의 로그 위치
- [architecture/external](../architecture/external/external-guidelines.md) - 외부 API 호출 로그
