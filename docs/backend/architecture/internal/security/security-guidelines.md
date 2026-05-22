# Security Guidelines

이 문서는 `backend/internal/security` 모듈의 실제 코드 위치, 책임, 의존 경계, 구현 전략 보강 기준을 정리한다.

## 코드 위치

- `backend/internal/security` - 인증, 인가, 암호화, 토큰 adapter 후보를 담당한다.

## 책임

- security provider와 crypto 구현 세부사항을 내부 인프라 경계에 둔다.
- application과 domain에는 provider SDK 타입이나 HTTP security 세부 구현이 노출되지 않게 한다.
- 인증 방식, 권한 모델, password/token 정책이 필요한 경우 provider 구현과 함께 문서화한다.

## 의존 경계

- depends on: `core/application`, `core/domain`, security provider
- used by: Spring runtime, app/support security configuration
- 금지되는 방향: provider SDK 타입의 application/domain 노출, HTTP security 세부 구현의 domain 침투

## 핵심 원칙

- security 구현은 인증/인가와 암호화 기술을 캡슐화하고 application에는 식별자와 권한 판단 결과만 드러낸다.
- 민감 정보는 저장, 로그, 예외 메시지, 응답 DTO에서 같은 기준으로 보호한다.
- 토큰, password, secret 정책은 만료, 회전, 검증 실패 처리를 함께 정의한다.

## 관련 정책

- [security](../../../policies/security.md) - 인증/인가와 민감 정보 처리
- [logging](../../../policies/logging.md) - 보안 이벤트 로깅과 민감 정보 차단

## 금지 규칙

- application/domain 타입이 provider SDK, servlet security type, token parser 구현에 직접 의존하지 않는다.
- password, token, secret, 개인정보를 로그나 예외 메시지에 원문으로 남기지 않는다.
- 인증 방식, 권한 모델, token 만료와 회전 기준 없이 보안 adapter를 추가하지 않는다.

## 주요 컴포넌트

- Security adapter: `{Provider}SecurityAdapter`
- Token verifier: `{Provider}TokenVerifier`
- Crypto service: `{Provider}CryptoService`
- Security properties: `{Provider}SecurityProperties`
- Security config: `{Provider}SecurityConfig`

## 전략 문서

- 전용 전략 문서 없음

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] 구현 추가 시 인증 방식, 권한 모델, password/token 정책이 이 문서 또는 `strategies` 문서에 명시되어 있다.
- [ ] application과 domain은 provider SDK나 HTTP security 세부 구현에 의존하지 않는다.
- [ ] 민감 정보 보호, token 만료, 검증 실패 처리 기준이 문서 또는 테스트에서 확인된다.
