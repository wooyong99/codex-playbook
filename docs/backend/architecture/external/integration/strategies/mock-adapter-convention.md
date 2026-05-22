# Mock Adapter 컨벤션

이 문서는 local profile에서 실제 외부 시스템 호출을 대체하는 Mock Adapter 전략을 정리한다.

## 목적

- 로컬 개발에서 외부 시스템 없이 application 흐름을 재현한다.
- 실 Adapter와 동일한 Port 계약을 유지한다.
- 성공, 실패, 불확정 시나리오를 입력 토큰으로 재현한다.

## 적용 범위

- `Mock{Function}Adapter`
- 실 Adapter와 Mock Adapter의 profile 분기
- local scenario token
- mock response 고정값과 로깅

## 책임

- 실 Adapter와 동일한 Port를 구현한다.
- local profile에서만 bean으로 등록된다.
- 외부 호출 없이 deterministic response를 반환한다.
- 테스트 가능한 실패와 불확정 분기를 제공한다.

## 전체 흐름

```text
local profile
  -> Mock{Function}Adapter
    -> scenario token
    -> Port Result

non-local profile
  -> {Provider}{Function}Adapter
    -> external API
```

## 세부 규칙

### 네이밍

| 항목 | 패턴 |
|------|------|
| Mock Adapter | `Mock{Function}Adapter` |
| 구현 Port | 실 Adapter와 동일한 Port |
| 파일 위치 | 실 Adapter와 같은 Provider 패키지 |

- Mock 이름에는 Provider prefix를 기본값으로 붙이지 않는다.

### Profile 분기

- 실 Adapter는 `@Profile("!local")`로 둔다.
- Mock Adapter는 `@Profile("local")`로 둔다.
- profile 정책이 바뀌면 실 Adapter와 Mock Adapter를 함께 수정한다.
- Mock이 필요 없는 Adapter는 profile 제약 없이 둘 수 있다.

### 시나리오 분기

- 입력 문자열에 포함된 token으로 시나리오를 분기한다.
- token 검사는 `ignoreCase = true`를 사용한다.
- 기본값은 성공 시나리오다.
- 실패 시나리오는 `*_FAIL`, `INVALID`, `NOT_FOUND`, `MISMATCH`, `SUSPENDED` 같은 token을 사용한다.
- 불확정 시나리오는 `*_UNKNOWN`, `UNAVAILABLE` 같은 token을 사용한다.

### Mock 응답

- 성공 응답은 현실 범위의 고정값을 사용한다.
- 날짜는 `LocalDate.now()` 기준 상대값을 사용한다.
- 무작위 값이나 만료된 고정 날짜를 쓰지 않는다.
- Mock 로그는 `[MOCK-기능]` prefix를 사용한다.

### 의존성

- Mock Adapter는 ApiClient, Repository, 다른 Port를 주입받지 않는다.
- 내부 ErrorCode enum처럼 순수 값 변환에 필요한 타입 참조는 허용한다.

## 금지 규칙

- 실 Adapter와 Mock Adapter의 profile을 비대칭으로 두지 않는다.
- Mock Adapter에 ApiClient, Repository, 다른 Port를 주입하지 않는다.
- Mock이 항상 성공만 반환하게 만들지 않는다.
- 만료될 수 있는 고정 날짜나 무작위 값을 Mock 응답에 넣지 않는다.
- Mock 전용 scenario token 로직을 실 Adapter에 포함하지 않는다.
- Mock Adapter가 실제 credentials나 외부 endpoint에 의존하지 않는다.

## 예외와 경계

- 로컬에서 실 API 호출이 자유롭고 비용과 보안 문제가 없으면 Mock Adapter를 만들지 않을 수 있다.
- 통합 테스트 전용 Fake가 필요하면 `src/test`에 별도 Fake를 두고 main Mock Adapter와 분리한다.
- Mock scenario token은 테스트 편의를 위한 계약이므로 사용자 API 계약으로 노출하지 않는다.

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] local profile에서 동일 Port에 Mock Adapter가 주입되고 실 외부 호출 bean은 선택되지 않는다.
- [ ] 성공, 실패, 불확정 시나리오가 입력 token만으로 재현된다.
- [ ] Mock이 외부 시스템과 persistence에 의존하지 않는다.
