# Architecture Unit Analysis Guide

실제 코드베이스를 기준으로 `docs/backend/architecture` 문서 구조와 전략 문서를 설계하기 위한 분석 가이드.

## 목차

- [핵심 원칙](#핵심-원칙)
- [1. Architecture Unit Discovery](#1-architecture-unit-discovery)
- [2. Responsibility Classification](#2-responsibility-classification)
- [3. Dependency Boundary Analysis](#3-dependency-boundary-analysis)
- [4. Pattern Extraction By Local Unit](#4-pattern-extraction-by-local-unit)
- [5. Documentation Structure Decision](#5-documentation-structure-decision)
- [6. Optional Playbook Compatibility Notes](#6-optional-playbook-compatibility-notes)
- [분석 메모 형식](#분석-메모-형식)

## 핵심 원칙

`docs/backend/architecture`는 플레이북 개념 레이어의 복제본이 아니라, 현재 프로젝트 코드베이스의 지식 시스템이어야 한다.

- 출력 문서 구조는 실제 코드의 모듈, 패키지, 책임 경계, 의존 방향을 따른다.
- `domain`, `application`, `storage`, `external`, `app` 같은 플레이북 개념 레이어는 분석 보조 렌즈로만 사용한다.
- 실제 코드에 없는 레이어명이나 전략 문서를 새로 만들지 않는다.
- 코드에서 확인한 클래스명, 패키지명, 어노테이션, 인터페이스, 의존 관계를 근거로 남긴다.
- 이름보다 책임과 의존 방향을 우선하지만, 최종 문서 디렉토리명은 프로젝트가 실제로 쓰는 이름을 우선한다.

## 1. Architecture Unit Discovery

먼저 실제 아키텍처 단위를 찾는다. 이 단계에서는 플레이북 레이어에 끼워 맞추지 않는다.

### 멀티 모듈 프로젝트

우선적으로 볼 대상:

- `settings.gradle.kts`
- 루트 및 각 모듈의 `build.gradle.kts`
- 모듈 간 project dependency
- 각 모듈의 `src/main/kotlin`, `src/test/kotlin`
- Spring Boot application entrypoint, configuration, component scan 범위

추출할 신호:

- 모듈명이 드러내는 실제 책임: `admin`, `api`, `core`, `batch`, `infrastructure`, `storage`, `notification`
- 의존 방향: 어떤 모듈이 어떤 모듈을 참조하는가
- 외부로 노출되는 계약: Controller, UseCase interface, Repository interface, Client port
- 모듈 내부에 섞인 하위 책임: persistence, client, messaging, security, config

### 단일 모듈 프로젝트

우선적으로 볼 대상:

- `src/main/kotlin` 이하 최상위 패키지 구조
- 패키지별 클래스 역할과 import 방향
- Spring stereotype annotation 분포
- 테스트 패키지 구조

추출할 신호:

- 패키지가 실제로 나누는 책임
- 패키지 이름과 클래스 역할이 충돌하는 지점
- 독립 문서 단위로 분리할 만큼 반복되는 하위 책임
- 진입점, 유스케이스, 도메인 모델, 영속성, 외부 연동, 배치 같은 책임의 배치 방식

## 2. Responsibility Classification

각 아키텍처 단위의 책임을 실제 코드 언어로 분류한다.

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

- 이름이 `core`여도 실제로 domain만 담는지, application service까지 포함하는지 확인한다.
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

## 4. Pattern Extraction By Local Unit

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

문서화하지 말아야 할 것:

- 코드에서 확인되지 않은 이상적 구조
- 플레이북 예시 문서 목록에만 있는 패턴
- 한 파일에만 우연히 있는 구현
- 리팩토링 희망사항

## 5. Documentation Structure Decision

분석 후 문서 구조를 먼저 제안한다. 모든 쓰기 모드는 먼저 기존 `docs/backend/architecture` 상태를 확인한다. 기존 구조와 충돌하면 `generate`는 중단하고, `migrate` 계획을 제시한다.

권장 구조:

```text
docs/backend/architecture/
├── README.md
├── {actual-unit}/
│   ├── README.md
│   └── strategies/
│       ├── README.md
│       └── {observed-pattern}.md
└── {another-actual-unit}/
    └── ...
```

결정 기준:

- 실제 모듈이 명확하고 책임이 응집되어 있으면 모듈명을 문서 단위로 사용한다.
- 하나의 모듈에 여러 책임이 섞여 있으면 패키지 또는 책임 단위로 문서 단위를 나눈다.
- 실제 이름이 너무 기술 세부적이면 사용자에게 문서명 후보를 확인한다.
- 기존 플레이북 구조가 코드와 맞지 않으면 `generate`로 새 문서를 추가하지 말고 `migrate` 계획을 먼저 제시한다.

실행 모드별 판단:

- `inspect`: 파일을 수정하지 않는다. 실제 아키텍처 단위 맵, 기존 문서 분류, 제안 구조, 추천 모드를 보고한다.
- `generate`: 기존 architecture 문서가 없거나 placeholder 수준이거나 새 구조와 충돌하지 않을 때만 문서를 추가한다. 충돌하면 no-op으로 멈추고 `migrate`를 제안한다.
- `migrate`: 기존 active architecture tree를 실제 코드 기반 구조로 교체한다. 기존 문서는 유지·이전·삭제 후보로 분류하고, 코드와 맞지 않는 플레이북 기반 문서는 active path에서 제거한다.
- `merge`: 기존 구조가 실제 코드와 크게 충돌하지 않을 때만 보강한다. 기존 사람이 쓴 설명은 보존하고, 코드 근거가 약한 부분만 채운다.

기존 문서 분류:

- `keep`: 실제 코드 구조와 맞고 계속 active 문서로 둘 수 있다.
- `merge`: 사람이 쓴 설명은 유효하지만 코드 근거가 부족해 보강한다.
- `migrate`: 내용 일부를 새 실제 단위 문서로 옮긴다.
- `remove`: 플레이북 일반론이거나 실제 코드와 충돌해 active architecture tree에서 제거한다.
- `archive`: 보존 가치는 있지만 active 문서로 두면 혼선을 만든다. 필요한 경우 `docs/archive`처럼 active architecture path 밖으로 이동한다.

반드시 갱신할 수 있는 문서:

- `docs/backend/architecture/README.md`: 전체 아키텍처 단위 진입점, 실제 단위 맵, 위치, 책임, 의존 방향 요약
- 각 `{actual-unit}/README.md`: 단위별 책임과 하위 전략 링크
- 각 `{actual-unit}/strategies/README.md`: 관찰된 전략 목록
- `docs/backend/README.md`: architecture 단일 진입점 경로가 바뀔 때만 갱신
- `AGENTS.md`: 최상위 Backend 문서 홈 경로가 바뀔 때만 갱신

## 6. Optional Playbook Compatibility Notes

플레이북 개념 레이어와의 대응은 필요할 때만 보조 정보로 남긴다.

사용할 때:

- 기존 문서가 플레이북 구조로 되어 있어 이전 근거가 필요할 때
- 사용자가 플레이북 기준과 실제 구조의 차이를 알고 싶어 할 때
- 특정 실제 단위가 여러 플레이북 개념을 함께 포함해 주의가 필요할 때

쓰는 방식:

```text
Playbook compatibility:
- 이 프로젝트의 `core`는 domain model과 application usecase를 함께 포함한다.
- 따라서 문서 구조는 `core`를 유지하되, strategies 하위에서 `domain-model`, `usecase-flow` 전략을 분리한다.
```

하지 말아야 할 것:

- 실제 코드 단위명을 숨기고 플레이북 개념 레이어명만 노출하기
- 플레이북 개념 레이어에 맞추기 위해 실제 구조와 다른 디렉토리 만들기
- 코드에서 섞여 있는 책임을 문서에서만 억지로 분리하기

## 분석 메모 형식

분석 중에는 최소 아래 형태로 메모한다.

```text
[ARCHITECTURE UNIT] {실제 단위명}
코드 위치:
- {모듈 또는 패키지 경로}

책임:
- {실제 코드에서 확인한 책임}

의존 방향:
- depends on: {단위 목록}
- used by: {단위 목록}

주요 컴포넌트:
- {역할}: {예시 클래스}

관찰된 전략:
- {전략명}: {근거 클래스/패키지/어노테이션}

문서 구조 제안:
- docs/backend/architecture/{actual-unit}/README.md
- docs/backend/architecture/{actual-unit}/strategies/{pattern}.md

Playbook compatibility:
- {필요할 때만 작성. 없으면 "없음"}

불확실한 부분:
- {있다면 기록, 없으면 없음}
```
