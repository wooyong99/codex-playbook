# Application Strategies

이 프로젝트에서 `application` 단위에 실제로 사용 중인 구현 전략 요약.

## 핵심 전략

- UseCase는 외부 요청의 진입점이며 Flow 조합과 결과 반환을 담당한다.
- Flow는 재사용 가능한 업무 흐름과 트랜잭션 경계를 캡슐화한다.
- Validator, Handler, Policy, EventHandler, Mapper는 책임이 실제로 분리될 때만 둔다.
- Port는 application이 소유하고 infrastructure 단위가 구현한다.
- 패키지는 도메인/역할 기준으로 구성하되 실제 코드 탐색성이 우선이다.

## 근거가 된 코드 패턴

- `UseCase`, `Flow`, `Validator`, `Handler`, `Policy`, `EventHandler`, `Mapper` - application 내부 역할 분리
- `Port` interface - infrastructure 구현과 application 경계 분리
- `Command`, `Result` - 외부 계약과 도메인 행위 사이의 입출력 계약

## 세부 문서

- [package-structure](package-structure.md) - application 패키지 구조를 정할 때
- [use-case-convention](use-case-convention.md) - UseCase 진입점을 작성할 때
- [flow-convention](flow-convention.md) - 재사용 가능한 업무 흐름을 분리할 때
- [validator-convention](validator-convention.md) - 조회된 데이터 기반 규칙 검증을 분리할 때
- [handler-convention](handler-convention.md) - 경계 보호나 공통 조율 로직을 분리할 때
- [policy-convention](policy-convention.md) - 확장 가능한 행위 분기를 외부화할 때
- [event-handler-convention](event-handler-convention.md) - 커밋 후 부수 효과를 처리할 때
- [mapper-convention](mapper-convention.md) - 도메인 결과를 외부 응답으로 조립할 때
