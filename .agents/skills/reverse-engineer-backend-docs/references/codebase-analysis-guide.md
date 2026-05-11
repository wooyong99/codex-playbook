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

구현 전략은 특정 아키텍처 단위 안에서 반복되는 구현 방식이다. 새로운 기능을 추가할 때 참고할 수 있는 패턴이어야 하며, 단발성 코드나 우연한 예외는 전략 문서 후보가 아니다.

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

반복 패턴으로 인정할 기준:

- 여러 클래스나 여러 기능에서 반복된다.
- 새로운 기능을 추가할 때 따라야 할 구현 전략으로 볼 수 있다.
- 코드 근거를 2개 이상 제시할 수 있거나, 1개뿐이어도 central abstraction으로 쓰인다.

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

코드 근거:
- {모듈 또는 패키지 경로}: {관찰 내용}

책임 / 정책 / 전략:
- {실제 코드에서 확인한 내용}

의존 방향:
- depends on: {단위 목록}
- used by: {단위 목록}

불확실한 부분:
- {있다면 기록, 없으면 없음}
```

## 분석 완료 조건

- 문서 후보마다 최소 하나 이상의 코드 근거가 있다.
- 실제 아키텍처 단위와 플레이북 개념 레이어를 혼동하지 않았다.
- 정책 후보와 구현 전략 후보가 분리되어 있다.
- 실행 정보는 설정 파일이나 빌드 스크립트 근거와 연결되어 있다.
- 불확실한 항목은 추측으로 채우지 않고 별도로 표시했다.
