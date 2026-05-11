# Backend Codebase Analysis Guide

이 문서는 기존 백엔드 코드베이스를 읽어 `docs/backend`에 기록할 실제 구조, 정책 신호, 구현 전략, 실행 정보를 찾는 세부 분석 기준이다. `SKILL.md`의 "코드베이스를 역공학한다" 단계에서 사용한다.

## 분석 목표

`docs/backend`는 플레이북 예시의 복제본이 아니라 현재 프로젝트의 지식 시스템이어야 한다. 분석 단계에서는 실제 코드의 모듈, 패키지, 책임 경계, 의존 방향, 반복 패턴을 관찰하고 문서 후보로 정리한다. 이름보다 책임과 의존 방향을 우선하되, 최종 문서 단위명은 프로젝트가 실제로 쓰는 이름을 우선한다.

## 분석 원칙

- 코드에서 확인한 사실만 문서 후보로 삼는다.
- 클래스명, 패키지명, 어노테이션, 인터페이스, 설정 파일, 테스트 구조처럼 관찰 가능한 근거를 남긴다.
- 플레이북 개념 레이어는 분석 보조 렌즈로만 사용하고 출력 디렉토리명으로 강제하지 않는다.
- 단발성 구현과 반복 구현 전략을 구분한다.
- 불확실한 부분은 추측해서 채우지 않고 분석 메모의 "불확실한 부분"에 남긴다.
- 대형 코드베이스에서는 전체 정독보다 repo census, 우선순위화, 계층화 샘플링, 신뢰도 표기를 우선한다.

## 0. 규모별 분석 운영

코드베이스 크기에 따라 분석 방식을 다르게 잡는다. 라인 수는 대략적인 의사결정 기준이며, 파일 수·모듈 수·언어 혼재도·generated code 비율이 높으면 한 단계 큰 규모로 취급한다.

| 규모 | 기본 방식 | 완료 기준 |
|------|-----------|-----------|
| 10~1,000 LOC | 후보 파일 대부분을 직접 읽는다. | 모든 주요 파일을 확인하고 근거 제한이 있으면 명시한다. |
| 1,000~10,000 LOC | 전체 파일 목록을 만든 뒤 단위별 대표 파일을 읽는다. | 모든 아키텍처 단위가 최소 1개 이상 근거를 가진다. |
| 10,000~100,000 LOC | repo census와 suffix/annotation/import 검색으로 후보를 만든 뒤 계층화 샘플링한다. | 주요 단위와 shared abstraction을 우선 문서화하고 coverage를 남긴다. |
| 100,000~1,000,000 LOC | 전체 정독을 금지한다. census -> 우선순위화 -> 제한 샘플 -> confidence report 순서로 진행한다. | high-confidence 영역만 규칙화하고 나머지는 backlog/확인 필요로 둔다. |

대형 저장소의 표준 절차:

1. 제외 경로를 먼저 정한다.
2. `rg --files` 기반으로 실제 소스, 테스트, 설정, migration, generated 후보를 분리한다.
3. build file, module file, package root, entrypoint, public contract, shared abstraction을 census로 요약한다.
4. fan-in/fan-out이 큰 공통 모듈, 외부 노출 entrypoint, transaction/persistence 중심 흐름, 테스트 지원 코드를 우선순위로 둔다.
5. 각 아키텍처 단위는 샘플링 예산 안에서 읽고, 문서마다 coverage/confidence를 남긴다.
6. 샘플 밖의 영역은 추측하지 않고 "미분석 영역" 또는 "확인 필요"로 둔다.

기본 제외 경로:

- VCS/IDE/build: `.git`, `.idea`, `.gradle`, `build`, `target`, `out`, `dist`
- dependency/vendor: `node_modules`, `vendor`, `.m2`, `.npm`, `.yarn`, `Pods`
- generated: `generated`, `generated-sources`, `build/generated`, `openapi/generated`, `graphql/generated`
- binary/report: `coverage`, `reports`, `*.class`, `*.jar`, `*.war`, `*.zip`

주의:

- generated code가 public contract의 원천이면 제외하지 말고 "generated contract"로 별도 표시한다.
- migration, fixture, snapshot은 기본 구현 전략 근거로 쓰지 않는다. 데이터 관리 정책이나 테스트 전략을 볼 때만 제한적으로 샘플링한다.
- 언어·프레임워크가 섞인 저장소는 한 번에 통합 패턴을 만들지 말고 runtime 또는 service boundary별로 나눈다.

샘플링 예산:

- 단위별 entrypoint: 최대 3개. 서로 다른 업무 흐름을 우선한다.
- application/usecase/service 흐름: 단순 조회 1개, 상태 변경 1개, 복합 트랜잭션 또는 외부 연동 1개.
- persistence/external adapter: read/write 또는 성공/실패 흐름이 다르면 각각 1~2개.
- cross-cutting: transaction, validation, exception, logging, security, config는 각 축별 central abstraction 1~2개.
- tests: 단위 테스트 1~2개, 통합 또는 slice 테스트 1~2개, test support/fixture 1개.
- 100만 라인급에서는 첫 pass에서 상위 5~8개 아키텍처 단위만 high-confidence 후보로 다루고 나머지는 follow-up backlog로 둔다.

신뢰도 기준:

| 신뢰도 | 기준 | 문서화 방식 |
|--------|------|-------------|
| High | 여러 업무 영역과 테스트/공통 추상화에서 같은 패턴이 확인된다. | 규칙·체크리스트로 작성 가능 |
| Medium | 2개 이상 근거가 있으나 특정 모듈이나 업무에 편중된다. | 적용 범위와 예외를 명확히 제한 |
| Low | 근거가 1개이거나 샘플 밖 영향이 크다. | 규칙화하지 않고 확인 필요로 기록 |

## 1. 프로젝트 형태 파악

가장 먼저 프로젝트가 멀티 모듈인지 단일 모듈인지 판단한다. 이 판단은 이후 문서 단위를 모듈 기준으로 둘지, 패키지·책임 기준으로 둘지 결정하는 출발점이다.

멀티 모듈 프로젝트에서 확인할 대상:

- `settings.gradle.kts`
- 루트 및 각 모듈의 `build.gradle.kts`
- 모듈 간 `project(...)` dependency
- 각 모듈의 `src/main/kotlin`, `src/test/kotlin`
- Spring Boot application entrypoint, configuration, component scan 범위

단일 모듈 프로젝트에서 확인할 대상:

- `src/main/kotlin` 이하 최상위 패키지 구조
- 패키지별 클래스 역할과 import 방향
- Spring stereotype annotation 분포
- 테스트 패키지 구조

추출할 신호:

- 실제 책임을 드러내는 모듈명: `admin`, `api`, `core`, `batch`, `infrastructure`, `storage`, `notification`
- 의존 방향: 어떤 모듈 또는 패키지가 어떤 단위를 참조하는가
- 외부로 노출되는 계약: Controller, UseCase interface, Repository interface, Client port
- 모듈 내부에 섞인 하위 책임: persistence, client, messaging, security, config

## 2. 아키텍처 단위 식별

아키텍처 단위는 실제 코드가 가진 책임 경계다. `domain`, `application`, `storage`, `external`, `app` 같은 개념 레이어에 억지로 맞추지 않는다.

확인할 항목:

- 이 단위가 사용자 요청, 내부 유스케이스, 도메인 규칙, 저장소 구현, 외부 연동, 배치 실행, 설정 중 무엇을 담당하는가
- 이 단위가 외부에 제공하는 public contract는 무엇인가
- 이 단위가 내부 구현으로 숨기는 세부사항은 무엇인가
- 이 단위 내부에서 다시 쪼갤 수 있는 하위 책임은 무엇인가

관찰 가능한 근거:

- 클래스 suffix: `Controller`, `Request`, `Response`, `UseCase`, `Service`, `Flow`, `Policy`, `Validator`, `Entity`, `Repository`, `Adapter`, `Client`, `Config`
- annotation: `@RestController`, `@Service`, `@Component`, `@Transactional`, `@Entity`, `@Configuration`
- interface와 implementation의 위치
- DTO, Command, Result, Event, Exception, ErrorCode의 위치와 변환 흐름

판단 시 주의할 사례:

- 이름이 `core`여도 domain만 담는지, application service까지 포함하는지 확인한다.
- 이름이 `infrastructure`여도 persistence와 external client가 섞여 있으면 하위 책임 단위로 다시 나눈다.
- 이름이 `api`여도 controller만 있는지, service orchestration까지 포함하는지 확인한다.

## 3. 의존 경계 분석

문서 구조는 책임뿐 아니라 의존 방향을 반영해야 한다. 의존 경계가 실제 코드와 다르게 기록되면 이후 설계와 구현 판단을 잘못 이끈다.

확인할 항목:

- 모듈 또는 패키지 간 import 방향
- framework annotation이 어느 단위까지 침투하는가
- domain model이 persistence entity나 web DTO를 참조하는가
- application/usecase가 infrastructure implementation을 직접 참조하는가
- adapter implementation이 port interface를 구현하는가
- 테스트가 어떤 단위의 public contract를 기준으로 작성되는가

분석 결과에 포함할 판단:

- 허용되는 의존 방향
- 현재 코드에서 반복되는 의존 경계
- 경계가 흐릿한 영역과 문서화 시 주의점
- 문서 구조를 모듈 기준으로 할지 책임 기준으로 할지

## 4. 전역 정책 신호 추출

여러 아키텍처 단위가 함께 따라야 하는 규칙은 `policies` 후보로 본다. 정책은 특정 구현 위치보다 넓은 적용 범위를 가진다.

확인할 신호:

- 보안: 인증/인가, 비밀번호, 민감 정보, 세션·토큰, 권한 검증
- 로깅: 로그 레벨, 필드, 추적 ID, 민감 정보 마스킹
- 트랜잭션·정합성: transaction boundary, outbox, 이벤트 발행, retry, idempotency
- 동시성·성능: lock, cache, pagination, batch, rate limit
- 데이터 관리: tenant boundary, DDL/migration, soft delete, audit

정책 후보로 인정할 기준:

- 둘 이상의 실제 단위에 영향을 준다.
- 구현 위치와 무관하게 지켜야 하는 원칙 또는 금지 규칙이다.
- 새 기능을 추가할 때 반복적으로 확인해야 한다.

정책으로 쓰지 말아야 할 것:

- 특정 클래스 배치
- 특정 framework 설정의 세부 구현
- 한 단위에서만 우연히 보이는 코드 스타일

## 5. 구현 전략 추출

구현 전략은 특정 아키텍처 단위 안에서 반복되는 구현 방식이다. 새로운 기능을 추가할 때 참고할 수 있는 패턴이어야 하며, 단발성 코드나 우연한 예외는 전략 문서 후보가 아니다. 단, 레거시 코드베이스에서는 "좋은 패턴"만 찾으면 실제 협업에 도움이 되지 않는다. 주류 패턴, 상황별 변형, 부분 마이그레이션 흔적, 레거시 허용 구간, 반복되는 안티패턴을 함께 분류한다.

공통으로 확인할 패턴:

- 파일 및 패키지 구조
- public API 또는 public interface 배치
- 입력·출력 DTO와 내부 command/result 변환
- 예외와 error code 구조
- 트랜잭션 경계
- validation 위치
- mapper/converter 책임
- 테스트 fixture와 테스트 스타일
- 로깅, 설정, profile, bean wiring 방식

### 5.1 추출 절차

아키텍처 단위마다 아래 순서로 전략 후보를 만든다.

1. 진입점과 계약을 인벤토리화한다.
   - Controller, Handler, Listener, Job, UseCase interface, Service, Repository, Adapter, Client, Config, Test suffix를 먼저 찾는다.
   - 이름이 같은 suffix라도 책임이 다르면 별도 후보로 분리한다.
2. 서로 다른 업무 흐름을 샘플링한다.
   - 단순 조회, 상태 변경, 복합 트랜잭션, 외부 연동, 배치/비동기, 실패 처리 중 해당 단위에 존재하는 흐름을 나눠 본다.
   - 같은 패키지의 첫 번째 예시만 읽고 전체 전략으로 일반화하지 않는다.
3. 구현 축별로 후보를 묶는다.
   - 요청 수신, orchestration, transaction boundary, persistence access, external call, event/batch, validation, mapping, error handling, security, test style, configuration으로 나눠 반복성을 확인한다.
4. 변형과 예외를 분류한다.
   - 주류 패턴인지, 특정 상황에서만 쓰는 변형인지, 과거 코드와 공존하는 레거시인지, 단발성 예외인지 구분한다.
5. 문서화 수준을 결정한다.
   - 넓게 반복되거나 central abstraction으로 쓰이면 세부 strategy 문서 후보로 둔다.
   - 단위 전반의 원칙이지만 세부 구현 흐름은 아니면 `{actual-unit}-guidelines.md` 후보로 둔다.
   - 여러 단위에 적용되는 강제 원칙이면 `policies` 후보로 둔다.
   - 단발성이거나 의도가 불분명하면 "불확실한 부분"에 남기고 strategy 문서를 만들지 않는다.

### 5.2 샘플링 폭

대규모 또는 레거시 코드베이스에서는 아래 샘플을 우선 확인한다. 전체 파일을 다 읽지 못하더라도 한 업무 영역만 보고 결론 내리지 않는다. 샘플 수는 "0. 규모별 분석 운영"의 예산을 우선 따른다.

- public entrypoint: 서로 다른 업무 도메인의 Controller/Handler/Job/Listener 2개 이상
- application flow: 단순 흐름과 복합 흐름을 각각 대표하는 UseCase/Service
- persistence: read/write repository, query builder, entity mapping, migration 또는 audit 관련 코드
- external integration: Client/Adapter, retry/error mapping, timeout/profile 설정
- cross-cutting: transaction, validation, exception, logging, security annotation/filter/config
- tests: 단위 테스트와 통합 테스트의 fixture, mocking, transaction, profile 사용 방식
- shared abstraction: base class, common module, annotation, utility, factory, mapper, error code, test support

코드가 작아 샘플 수를 채울 수 없으면 가능한 근거를 모두 보고 "작은 코드베이스라 근거가 제한됨"을 남긴다.

### 5.3 전략 후보 분류

| 분류 | 인정 기준 | 문서화 방식 |
|------|-----------|-------------|
| 권장 주류 | 여러 기능에서 반복되고 테스트 또는 central abstraction과 연결된다. | strategy detail에 기본 흐름과 체크리스트를 쓴다. |
| 상황별 변형 | 특정 업무, 기술 제약, 성능/정합성 요구에서 반복된다. | strategy detail에 적용 조건과 기본 패턴과의 차이를 쓴다. |
| 레거시 허용 | 오래된 패키지나 부분 마이그레이션 구간에서 반복되며 아직 active code가 의존한다. | strategy detail 또는 guideline에 "레거시/혼재 구간"으로 기록하고 새 코드 적용 여부를 명시한다. |
| 충돌/확인 필요 | 둘 이상의 active 패턴이 공존하지만 우선순위를 코드만으로 판단하기 어렵다. | 두 패턴과 근거를 모두 남기고 사용자 확인 항목으로 둔다. |
| 단발성 제외 | 한 기능에만 있고 공통 추상화나 반복 근거가 없다. | strategy 문서를 만들지 않고 분석 메모의 제외 근거로 남긴다. |

반복 패턴으로 인정할 기준:

- 여러 클래스나 여러 기능에서 반복된다.
- 새로운 기능을 추가할 때 따라야 할 구현 전략으로 볼 수 있다.
- 코드 근거를 2개 이상 제시할 수 있거나, 1개뿐이어도 central abstraction으로 쓰인다.

### 5.4 세부 전략 문서 승격 기준

전략 후보를 모두 세부 문서로 만들지 않는다. 대형 코드베이스에서는 `strategies/README.md`가 전체 후보 지도를 소유하고, 세부 문서는 실제로 새 기능 구현 판단을 바꾸는 패턴만 승격한다.

세부 strategy detail로 승격하는 경우:

- High confidence이고 여러 기능에서 새 코드가 따라야 할 반복 구현 방식이다.
- Medium confidence이지만 central abstraction, public contract, transaction boundary, persistence/external adapter처럼 변경 영향이 크다.
- 레거시 허용 또는 충돌/확인 필요 상태라도 새 코드 작성자가 반드시 피해야 하거나 구분해야 하는 공존 패턴이다.

세부 문서로 승격하지 않는 경우:

- Low confidence 후보
- 단발성 제외 후보
- 같은 추상화 수준의 다른 전략 문서에 포함해도 충분한 작은 변형
- generated/vendor에서만 관찰된 패턴. test fixture에서만 관찰된 패턴은 테스트 전략을 문서화할 때만 승격한다.

문서 수 제어:

- 한 아키텍처 단위의 첫 pass에서는 세부 전략 문서를 3~5개 이내로 제한한다.
- 나머지 후보는 `strategies/README.md`의 전략 지도에 `README only`, `backlog`, `확인 필요`로 남긴다.
- 사용자가 특정 영역의 심층 문서화를 요청하면 그때 추가 승격한다.

### 5.5 레거시·혼재 코드에서 추가로 볼 신호

복잡한 협업 환경에서는 같은 책임에도 여러 방식이 섞인다. 아래 신호가 보이면 하나의 깔끔한 전략으로 합치지 말고 공존 상태를 문서화한다.

- `v1`/`v2`, `legacy`, `old`, `new`, `deprecated`, `migration`, `adapter` 같은 이름 또는 주석
- 같은 책임을 가진 Controller/Service/Repository가 패키지나 suffix만 다르게 존재함
- 일부 코드는 interface/port를 쓰고 일부 코드는 구현체나 framework API를 직접 참조함
- transaction, validation, exception mapping, DTO 변환 위치가 업무 영역마다 다름
- 테스트 방식이 mock 중심, slice test, integration test로 나뉘며 대상 코드와 함께 반복됨
- TODO/FIXME, deprecated annotation, suppressed warning, feature flag, profile 분기가 특정 구현 방식을 감쌈

새 코드가 어떤 방식을 따라야 하는지 코드만으로 명확하지 않으면 임의로 정하지 않는다. 대신 `권장 주류`, `레거시 허용`, `충돌/확인 필요`를 구분하고 사용자 확인 항목에 남긴다.

### 5.6 전략 근거 기록 방식

전략 후보는 단순 파일 목록이 아니라 적용 범위와 반복성을 함께 기록한다.

```text
[STRATEGY CANDIDATE] {strategy-name}
아키텍처 단위: {actual-unit}
분류: {권장 주류|상황별 변형|레거시 허용|충돌/확인 필요|단발성 제외}
적용 범위: {새 기능 전체|특정 업무|특정 adapter|레거시 패키지 등}
신뢰도: {High|Medium|Low}
반복 근거:
- {파일 또는 패키지}: {관찰한 구현 방식}
샘플 범위:
- {읽은 경로 수/대표 경로/제외한 경로}
변형/예외:
- {있다면 기록}
테스트 근거:
- {테스트 파일 또는 fixture. 없으면 "확인되지 않음"}
문서화 결정:
- {strategy detail|strategies README 요약|unit guideline|policy|no-doc}
승격 사유:
- {왜 세부 문서로 만들거나 만들지 않는지}
불확실한 부분:
- {있다면 기록, 없으면 없음}
```

## 6. 실행 정보 추출

`docs/backend/getting-started.md` 후보 정보는 코드와 설정에서 확인한다. 확인되지 않은 실행 절차는 추측으로 완성하지 않고 "확인 필요"로 남긴다.

확인할 항목:

- Gradle/Maven task, application module, local profile
- required environment variables
- DB, Redis, external service 같은 local dependency
- test command, migration command
- active profile, port, health endpoint

## 7. 설계 문서 신호 추출

`docs/backend/design`은 설계 의도와 의사결정 문서 영역이다. 기존 코드만 보고 새 기능 TDD를 임의 생성하지 않는다.

사용 가능한 경우:

- 사용자가 기존 기능의 설계 의도 문서화를 명시적으로 요청했다.
- 코드만으로는 의사결정 맥락을 파악하기 어려운 기능·서브시스템이 있다.
- 설계 의도는 참고 정보로 두고, 강제 규칙은 `architecture` 또는 `policies`에 둔다.

사용하지 말아야 할 경우:

- 단순히 코드 구조를 설명하면 충분한 경우
- 사용자 요청 없이 신규 기능 TDD를 만들어야 하는 경우
- 전역 정책이나 구현 규칙을 design 문서에만 둘 위험이 있는 경우

## 분석 메모 형식

```text
[BACKEND AREA] {architecture|policies|getting-started|design}
문서 후보:
- {docs/backend 하위 경로}

분석 범위:
- included: {읽은 모듈/패키지}
- excluded: {제외한 generated/vendor/build/test fixture 등}
- coverage/confidence: {High|Medium|Low 및 이유}

코드 근거:
- {모듈 또는 패키지 경로}: {관찰 내용}

책임 / 정책 / 전략:
- {실제 코드에서 확인한 내용}

전략 후보:
- {전략명}: {분류, 적용 범위, confidence, 문서화 결정}

의존 방향:
- depends on: {단위 목록}
- used by: {단위 목록}

불확실한 부분:
- {있다면 기록, 없으면 없음}
```

## 분석 완료 조건

- 문서 후보마다 최소 하나 이상의 코드 근거가 있다.
- 대형 코드베이스에서는 제외 경로, 샘플링 범위, coverage/confidence가 문서 후보마다 기록되어 있다.
- 실제 아키텍처 단위와 플레이북 개념 레이어를 혼동하지 않았다.
- 정책 후보와 구현 전략 후보가 분리되어 있다.
- 구현 전략 후보가 한 업무 영역이나 첫 번째 예시에 과도하게 편향되지 않았다.
- 주류 패턴, 변형, 레거시 허용, 충돌/확인 필요, 단발성 제외가 구분되어 있다.
- 세부 전략 문서 승격 기준이 적용되어 문서 수가 후보 수만큼 폭증하지 않는다.
- 실행 정보는 설정 파일이나 빌드 스크립트 근거와 연결되어 있다.
- 불확실한 항목은 추측으로 채우지 않고 별도로 표시했다.
