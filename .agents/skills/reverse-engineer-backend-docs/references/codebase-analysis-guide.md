# Backend Codebase Analysis Guide

기존 백엔드 코드베이스를 기준으로 `docs/backend` 문서화 대상을 식별하기 위한 분석 가이드.

## 핵심 원칙

`docs/backend`는 플레이북 예시의 복제본이 아니라 현재 프로젝트 코드베이스의 지식 시스템이어야 한다.

- 출력 문서 구조는 실제 코드의 모듈, 패키지, 책임 경계, 의존 방향을 따른다.
- 플레이북 개념 레이어는 분석 보조 렌즈로만 사용한다.
- 코드에서 확인한 클래스명, 패키지명, 어노테이션, 인터페이스, 의존 관계를 근거로 남긴다.
- 이름보다 책임과 의존 방향을 우선하지만, 최종 문서 디렉토리명은 프로젝트가 실제로 쓰는 이름을 우선한다.

## 1. Backend Shape Discovery

먼저 프로젝트의 형태를 파악한다.

멀티 모듈 프로젝트에서 우선적으로 볼 대상:

- `settings.gradle.kts`
- 루트 및 각 모듈의 `build.gradle.kts`
- 모듈 간 project dependency
- 각 모듈의 `src/main/kotlin`, `src/test/kotlin`
- Spring Boot application entrypoint, configuration, component scan 범위

단일 모듈 프로젝트에서 우선적으로 볼 대상:

- `src/main/kotlin` 이하 최상위 패키지 구조
- 패키지별 클래스 역할과 import 방향
- Spring stereotype annotation 분포
- 테스트 패키지 구조

추출할 신호:

- 모듈명이 드러내는 실제 책임: `admin`, `api`, `core`, `batch`, `infrastructure`, `storage`, `notification`
- 의존 방향: 어떤 모듈 또는 패키지가 어떤 단위를 참조하는가
- 외부로 노출되는 계약: Controller, UseCase interface, Repository interface, Client port
- 모듈 내부에 섞인 하위 책임: persistence, client, messaging, security, config

## 2. Architecture Unit Discovery

실제 아키텍처 단위를 찾는다. 플레이북 레이어에 끼워 맞추지 않는다.

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

주의:

- 이름이 `core`여도 domain만 담는지, application service까지 포함하는지 확인한다.
- 이름이 `infrastructure`여도 persistence와 external client가 섞여 있으면 하위 책임 단위로 다시 나눈다.
- 이름이 `api`여도 controller만 있는지, service orchestration까지 포함하는지 확인한다.

## 3. Dependency Boundary Analysis

문서 구조는 책임뿐 아니라 의존 방향을 반영해야 한다.

확인할 항목:

- 모듈 또는 패키지 간 import 방향
- framework annotation이 어느 단위까지 침투하는가
- domain model이 persistence entity나 web DTO를 참조하는가
- application/usecase가 infrastructure implementation을 직접 참조하는가
- adapter implementation이 port interface를 구현하는가
- 테스트가 어떤 단위의 public contract를 기준으로 작성되는가

출력해야 할 판단:

- 허용되는 의존 방향
- 현재 코드에서 반복되는 의존 경계
- 경계가 흐릿한 영역과 문서화 시 주의점
- 문서 구조를 모듈 기준으로 할지 책임 기준으로 할지

## 4. Cross-Cutting Policy Signals

여러 아키텍처 단위가 함께 따라야 하는 규칙은 policy 후보로 본다.

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

## 5. Implementation Strategy Extraction

각 실제 아키텍처 단위별로 반복 패턴을 추출한다.

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
- 단발성 구현이나 우연한 예외가 아니다.
- 코드 근거를 2개 이상 제시할 수 있거나, 1개뿐이어도 central abstraction으로 쓰인다.

## 6. Getting Started Signals

`docs/backend/getting-started.md` 후보 정보는 코드와 설정에서 확인한다.

확인할 항목:

- Gradle/Maven task, application module, local profile
- required environment variables
- DB, Redis, external service 같은 local dependency
- test command, migration command
- active profile, port, health endpoint

추측으로 실행 절차를 만들지 않는다. 코드 또는 설정에서 확인되지 않으면 "확인 필요"로 남긴다.

## 7. Design Documentation Signals

`docs/backend/design`은 설계 의도와 의사결정 문서 영역이다.

- 기존 코드만 보고 새 기능 TDD를 임의 생성하지 않는다.
- 사용자가 "기존 기능의 설계 의도 문서화"를 요청한 경우에만 코드 근거 기반으로 작성한다.
- 강제 규칙은 design 문서가 아니라 `architecture` 또는 `policies`에 올린다.
- design README 링크는 design 문서가 추가·삭제될 때 갱신한다.

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
