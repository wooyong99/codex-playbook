# ApiClient HTTP 클라이언트 컨벤션

---

## 언제 사용하는가

- `external` 단위에서 ApiClient HTTP 클라이언트 컨벤션 전략을 적용하거나 검토할 때 사용한다.

## 코드 위치

- `external` 단위의 실제 프로젝트 적용 위치를 기준으로 작성한다.

## 구조

- 이 문서의 본문 섹션이 해당 전략의 구조와 세부 규칙을 설명한다.

## 핵심 원칙

**ApiClient는 Provider 전용 HTTP 클라이언트 빈을 `@Qualifier`로 주입받아 재사용한다.**

이 문서는 [api-client-convention.md](api-client-convention.md) "HTTP 클라이언트 사용" 섹션의 프로젝트별 세부 구현을 정의한다. HTTP 클라이언트 유형과 빈 구성 방식은 프로젝트마다 다를 수 있다.

---

## 코드에서 관찰된 규칙

1. 실제 프로젝트 적용 시 본문 규칙이 코드에서 반복되는지 확인한다.

## 사용 HTTP 클라이언트

> {이 프로젝트에서 사용하는 HTTP 클라이언트를 기술한다. 예: `RestClient`, `RestTemplate`, `WebClient`}

---

## 빈 주입 방식

**규칙: {빈 주입 방식 결론}**

> {Provider 전용 빈을 어떻게 등록하고 주입받는지 기술한다. 코드 예시 포함}

```kotlin
// 예시 작성
```

> 빈 구성은 [config-convention.md](config-convention.md) 참고

---

## 의존 및 책임 경계

- 허용되는 의존: `external` 단위의 상위 guideline이 허용한 의존 방향을 따른다.
- 주의할 의존 또는 경계 조건: 세부 경계는 본문 규칙과 상위 guideline을 함께 따른다.

## 관련 정책 / 상위 규칙

- [external guidelines](../external-guidelines.md) - 이 전략이 따르는 상위 아키텍처 단위 규칙
- 관련 전역 정책: 필요 시 [policies](../../../policies/README.md) 문서를 링크한다

## 금지 규칙

- 메서드 내부에서 HTTP 클라이언트를 매번 재생성하지 않는다.
- {프로젝트별 추가 금지 규칙을 기술한다}

---

## 안티패턴

- 없음

## 체크 리스트

- [ ] HTTP 클라이언트 빈을 `@Qualifier`로 주입받았는가?
- [ ] 메서드 내부에서 클라이언트를 재생성하지 않는가?
- [ ] 빈이 [config-convention.md](config-convention.md)에 따라 올바르게 구성됐는가?

## 예시 코드

- 본문의 예시 코드와 프로젝트 적용 시 실제 저장소 상대 경로를 함께 확인한다.
