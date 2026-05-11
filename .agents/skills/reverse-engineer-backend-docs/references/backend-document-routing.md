# Backend Document Routing

이 문서는 코드 분석 결과를 `docs/backend`의 어느 문서가 소유해야 하는지 결정하는 세부 기준이다. `SKILL.md`의 입력 모드 정리, 기존 문서 분류, 문서 소유 경계 설계 단계에서 사용한다.

## 라우팅 목표

문서 구조는 실제 코드의 책임 경계와 변경 경계를 따라야 한다. 상위 문서는 안정적인 진입점만 제공하고, 세부 구현 목록은 가장 가까운 소유 문서가 관리한다. 같은 규칙이나 설명은 한 문서에만 원문으로 두고 다른 문서에서는 링크와 적용 맥락만 남긴다.

## 1. 문서 소유권

| 영역 | 위치 | 소유 내용 |
|------|------|-----------|
| Backend 홈 | `docs/backend/README.md` | backend 하위 문서 맵, 문서 경계, 각 영역 단일 진입점 |
| Getting Started | `docs/backend/getting-started.md` | 로컬 실행, 빌드, 테스트, 프로필, 의존 서비스 |
| Architecture | `docs/backend/architecture/README.md` | 실제 아키텍처 단위 맵, 단위별 guideline 링크 |
| Policies | `docs/backend/policies/README.md` | 전역 정책 목록과 링크 |
| Design | `docs/backend/design/README.md` | 기술설계문서 목록과 운영 원칙 |

소유권 규칙:

- `AGENTS.md`는 최상위 `docs/backend/README.md`만 참조한다.
- 하위 영역의 세부 문서 목록은 가장 가까운 `README.md`가 소유한다.
- `docs/backend/architecture/README.md`는 아키텍처 단위 목록까지만 소유한다.
- 각 아키텍처 단위 내부 전략 문서 목록은 해당 단위의 `{actual-unit}-guidelines.md`와 `strategies/README.md`가 소유한다.
- 하위 구현 변경이 상위 README 수정을 강제하지 않도록 링크 경계를 설계한다.

## 2. 관심사별 위치 결정

| 구분 | 위치 | 판단 기준 |
|------|------|-----------|
| 정책 | `docs/backend/policies/{concept}.md` | 여러 아키텍처 단위가 공통으로 지켜야 하는 원칙, 금지 규칙, 민감 정보·정합성·운영 기준 |
| 구현 아키텍처 | `docs/backend/architecture/{actual-unit}/{actual-unit}-guidelines.md` | 실제 코드 단위의 책임, 컴포넌트, 의존 경계, 정책을 만족하는 구조 |
| 구현 전략 | `docs/backend/architecture/{actual-unit}/strategies/{observed-pattern}.md` | 특정 단위 안에서 반복되는 구현 방식, 패턴, 체크리스트, 코드 근거 |
| 설계 의도 | `docs/backend/design/{topic}.md` | 사용자가 요청한 기능·서브시스템의 설계 의도와 의사결정 맥락 |

같은 개념도 관심사에 따라 여러 위치에 걸쳐 나타날 수 있다. 예를 들어 인증/인가는 `policies/security.md`에 전역 보안 원칙을 두고, 실제 인증 코드가 독립 단위이면 `architecture/security/security-guidelines.md`에 구조를 쓴다. JWT 검증이나 필터 체인처럼 반복 구현 방식이 확인되면 해당 단위의 `strategies/` 하위에 전략 문서를 둔다.

중복 방지 기준:

- 정책 문서에는 코드 배치, 클래스 목록, 모듈 의존 구조를 쓰지 않는다.
- architecture guideline에는 정책 원문을 재기술하지 않고 관련 정책을 링크한다.
- strategy 문서에는 상위 guideline과 정책을 링크하고, 반복 구현 패턴과 코드 근거만 쓴다.
- design 문서에 강제 규칙을 숨기지 않는다. 강제할 규칙은 `architecture` 또는 `policies`로 승격한다.

## 3. Architecture 구조 결정

권장 구조:

```text
docs/backend/architecture/
├── README.md
├── {actual-unit}/
│   ├── {actual-unit}-guidelines.md
│   └── strategies/
│       ├── README.md
│       └── {observed-pattern}.md
└── {another-actual-unit}/
    └── ...
```

결정 기준:

- 실제 모듈이 명확하고 책임이 응집되어 있으면 모듈명을 문서 단위로 사용한다.
- 하나의 모듈에 여러 책임이 섞여 있으면 패키지 또는 책임 단위로 문서 단위를 나눈다.
- 아키텍처 단위 본문 파일은 `{actual-unit}-guidelines.md`로 만들고, `{actual-unit}`은 실제 코드 단위명을 kebab-case로 정규화한다.
- 단위 디렉토리의 `README.md`는 기본 생성하지 않는다. 한 단위 안의 문서가 많아져 로컬 인덱스가 필요할 때만 예외적으로 만든다.
- 실제 이름이 너무 기술 세부적이면 사용자에게 문서명 후보를 확인한다.

## 4. 실행 모드 선택

모든 모드는 먼저 `inspect` 수준의 사전 판단을 수행한다. 코드 구조와 기존 `docs/backend` 상태를 확인하지 않은 채 파일을 생성·수정·삭제하지 않는다.

| 모드 | 처리 방식 |
|------|-----------|
| `inspect` | 파일을 수정하지 않는다. 실제 문서 후보, 기존 문서 분류, 제안 구조, 추천 후속 모드를 보고한다. |
| `generate` | 기존 문서가 없거나 placeholder 수준이거나 새 구조와 충돌하지 않을 때만 문서를 추가한다. 충돌하면 no-op으로 멈추고 `migrate`를 제안한다. |
| `migrate` | 기존 active backend docs를 실제 코드 기반 구조로 교체한다. 기존 문서는 유지·이전·삭제 후보로 분류하고, 코드와 맞지 않는 플레이북 기반 문서는 active path에서 제거한다. |
| `merge` | 기존 구조가 실제 코드와 크게 충돌하지 않을 때만 보강한다. 기존 사람이 쓴 설명은 보존하고, 코드 근거가 약한 부분만 채운다. |

모드 선택 흐름:

```text
항상 inspect 수준의 사전 판단 수행
→ docs/backend 없음/placeholder 수준
  → generate

→ 기존 docs/backend가 실제 코드 구조와 대체로 일치
  → merge

→ 기존 docs/backend가 플레이북 일반론 중심이고 실제 코드 구조와 충돌
  → migrate

→ 판단이 애매하거나 삭제/이전 영향이 큼
  → 사용자 확인 후 migrate 또는 merge
```

## 5. 기존 문서 분류

| 분류 | 의미 |
|------|------|
| `keep` | 실제 코드 구조와 맞고 계속 active 문서로 둘 수 있다. |
| `merge` | 사람이 쓴 설명은 유효하지만 코드 근거가 부족해 보강한다. |
| `migrate` | 내용 일부를 새 실제 단위 또는 새 영역 문서로 옮긴다. |
| `remove` | 플레이북 일반론이거나 실제 코드와 충돌해 active docs에서 제거한다. |
| `archive` | 보존 가치는 있지만 active 문서로 두면 혼선을 만든다. 필요한 경우 `docs/archive`처럼 active backend path 밖으로 이동한다. |

분류 시 주의점:

- 보존 가치가 큰 사람이 작성한 문서는 사용자 확인 없이 삭제하거나 active path 밖으로 이전하지 않는다.
- 오래된 플레이북식 문서가 active path에 남아 실제 코드 기반 문서와 충돌하지 않도록 처리한다.
- 기존 문서가 일반론인지, 실제 코드 근거가 있는지, 새 구조와 충돌하는지 분리해 판단한다.

## 6. 갱신 범위

- `docs/backend` 바로 아래 새 영역을 추가·삭제·개편하면 `docs/backend/README.md`를 갱신한다.
- architecture 하위 단위를 추가·삭제·개편하면 `docs/backend/architecture/README.md`를 갱신한다.
- architecture 단위 내부 전략 문서를 추가·삭제·개편하면 해당 단위의 `{actual-unit}-guidelines.md` 또는 `strategies/README.md`를 갱신한다.
- policy 문서를 추가·삭제·개편하면 `docs/backend/policies/README.md`를 갱신한다.
- design 문서를 추가·삭제·개편하면 `docs/backend/design/README.md`를 갱신한다.
- `AGENTS.md`는 최상위 Backend 문서 홈 경로가 바뀔 때만 갱신한다.

## 7. 금지 규칙

- 상위 README에 하위 디렉토리의 개별 전략 문서, 세부 구현 문서, 내부 파일 목록을 직접 나열하지 않는다.
- 같은 규칙, 정책, 구조 설명을 여러 문서에 원문으로 중복 작성하지 않는다.
- 코드에서 확인되지 않은 아키텍처 단위, 정책, 실행 방법, 구현 패턴을 만들어내지 않는다.
- 플레이북 개념 레이어명을 실제 출력 디렉토리명이나 문서 단위명의 기본값으로 사용하지 않는다.
- 정책 문서에 클래스 목록, 패키지 구조, 구현 절차, 모듈 의존 구조를 쓰지 않는다.
- strategy 문서에 정책 원문, 아키텍처 단위의 전체 책임, 상위 문서의 설명을 재기술하지 않는다.
- `migrate` 후에도 실제 코드 구조와 충돌하는 오래된 플레이북식 문서를 active path에 그대로 남기지 않는다.

## 8. 안티패턴

- 문서 맵 과노출: `AGENTS.md`, `docs/backend/README.md`, `docs/backend/architecture/README.md`가 하위 세부 링크를 계속 직접 들고 있다.
- 이름만 분리된 중복 문서: 같은 개념을 policy, guideline, strategy에 거의 같은 문장으로 반복한다.
- 추상화 수준 혼합: 전체 지도 문서에 클래스 수준 구현 근거를 쓰거나, strategy 문서에 전역 정책 원칙을 길게 쓴다.
- 플레이북 레이어 강제 매핑: 실제 모듈·패키지 구조를 무시하고 `app`, `application`, `domain`, `storage`, `external` 같은 개념 레이어에 억지로 맞춘다.
- 전략 덤핑: `{actual-unit}-guidelines.md`에 반복 구현 방식과 체크리스트를 모두 넣고 `strategies/`를 비워둔다.
- 정책 오염: `policies` 문서가 전역 원칙 대신 특정 클래스 배치나 구현 순서를 소유한다.
- 과도한 파일 분리: 소유자, 변경 주기, 독자, 추상화 수준이 같음에도 작은 섹션을 여러 파일로 쪼갠다.
- 낡은 내비게이션: 문서를 이동·삭제했지만 가장 가까운 `README.md`의 문서 맵을 갱신하지 않는다.

## 9. 질문해야 하는 경우

- 출력 경로 후보가 둘 이상이라 어느 쪽에 써야 할지 불명확할 때
- 특정 책임이 architecture unit인지 policy인지 판단이 애매할 때
- 특정 아키텍처 단위가 혼재되어 있어 주 분석 단위를 모듈 기준으로 볼지 패키지 기준으로 볼지 애매할 때
- 실제 코드 단위명이 문서 디렉토리명으로 쓰기에 너무 구현 세부적이거나 임시적일 때
- 기존 `docs/backend` 구조를 유지할지 실제 코드 구조로 이전할지 선택이 필요할 때
- 기존 사람이 쓴 문서를 삭제·이전해야 하는데 보존 가치 판단이 중요한 때
- `docs/backend/design`에 기존 기능 설계 문서를 새로 만들지 사용자의 의도가 불명확할 때
- 새 구조 적용이 최상위 Backend 문서 홈 경로 변경까지 요구할 때
