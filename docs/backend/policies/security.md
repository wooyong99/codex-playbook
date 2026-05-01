# Security Policy

## 적용 범위

- 인증/인가 경계
- 비밀번호와 credentials 처리
- API DTO, 로그, 저장소로 흐를 수 있는 민감 정보

## 핵심 원칙

- 평문 비밀번호는 API DTO 경계에서 종료하고, 해시만 도메인·영속 계층에 진입한다.
- 서로 다른 사용자 집합을 대상으로 하는 채널은 인증 컨텍스트를 분리한다.
- `.env`, credentials, 비밀키, 토큰, 카드 정보 같은 민감 정보는 코드와 로그에 남기지 않는다.

## 금지 규칙

- 평문 비밀번호를 domain, application, storage 단위로 전달하지 않는다.
- 일반 사용자 채널과 시스템 관리자 채널이 동일 사용자 테이블·권한 모델·인증 필터를 공유하지 않는다.
- 민감 정보가 포함된 파일을 커밋하지 않는다.

## 안티패턴

- 인증 컨텍스트를 공유해 권한 상승, 세션 오염, 감사 추적 단절 가능성을 만든다.
- DTO 전체를 로그로 남기면서 비밀번호, 토큰, 개인정보 마스킹을 누락한다.
- `.gitignore` 등록 없이 로컬 credentials 파일을 생성한다.

## 코드 근거

- `app` 인증 필터/보안 설정 - 요청 인증 경계
- `domain` 계정/자격 증명 모델 - 해시만 진입해야 하는 도메인 경계
- `logging` 정책 - 민감 정보 로그 차단

## 관련 아키텍처 문서

- [architecture/app](../architecture/app/app-guidelines.md) - 인증 필터와 HTTP 경계
- [architecture/domain](../architecture/domain/domain-guidelines.md) - 도메인으로 들어오는 민감 정보 경계
- [architecture/external](../architecture/external/external-guidelines.md) - 외부 인증 토큰과 credentials 경계
