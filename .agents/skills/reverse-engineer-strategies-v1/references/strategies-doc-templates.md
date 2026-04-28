# Strategies Doc Templates

생성할 문서의 최소 구조와 작성 규칙.

## 1. 레이어 README 템플릿

각 레이어의 `strategies/README.md`는 아래 구조를 따른다.

```md
# {Layer} Strategies

이 프로젝트에서 {layer} 레이어에 실제로 사용 중인 전략 요약.

## 핵심 전략

- {전략 1}
- {전략 2}

## 근거가 된 코드 패턴

- {클래스/패키지/어노테이션 근거 1}
- {클래스/패키지/어노테이션 근거 2}

## 세부 문서

- [{문서명}]({파일명}.md) - {언제 이 문서를 참고해야 하는지}
```

## 2. 세부 컨벤션 문서 템플릿

세부 문서는 아래 구조를 기본으로 한다.

```md
# {Convention Title}

이 프로젝트에서 {컴포넌트/패턴}를 구현하는 실제 방식 정리.

## 언제 사용하는가

- {사용 시점}

## 구조

- {구성 요소 1}
- {구성 요소 2}

## 코드에서 관찰된 규칙

1. {규칙 1}
2. {규칙 2}
3. {규칙 3}

## 예시 클래스

- `{절대 또는 저장소 상대 경로}` - {역할 설명}
- `{절대 또는 저장소 상대 경로}` - {역할 설명}
```

## 3. 세부 문서를 만들 조건

기본 원칙:

- 아래 예시 문서들은 코드에서 해당 패턴이 실제로 보일 때만 만든다.
- 아래 목록에 없는 패턴이라도, 기존 코드베이스에서 **반복적으로 사용되는 새로운 구현 패턴**이 확인되면 그 패턴에 맞는 새 전략 문서를 추가로 만든다.
- 즉, 문서 생성 기준은 **플레이북 예시 목록**이 아니라 **실제 코드에서 관찰된 구현 전략**이다.

예시 문서 목록:

- `app/strategies/api-convention.md`
- `app/strategies/rest-design-convention.md`
- `app/strategies/exception-handling-convention.md`
- `application/strategies/use-case-convention.md`
- `application/strategies/flow-convention.md`
- `application/strategies/validator-convention.md`
- `application/strategies/handler-convention.md`
- `application/strategies/policy-convention.md`
- `application/strategies/mapper-convention.md`
- `domain/strategies/domain-model-convention.md`
- `domain/strategies/exception-convention.md`
- `storage/strategies/storage-adapter-convention.md`
- `storage/strategies/querydsl-convention.md`
- `external/strategies/api-client-http-client.md`
- `external/strategies/api-client-logging.md`

새 패턴 문서화 규칙:

- 새 문서 이름은 해당 패턴의 책임이 드러나게 짓는다.
- README에는 예시 문서와 새로 발견한 문서를 함께 연결한다.
- 단발성 구현이나 한두 클래스에만 우연히 보이는 패턴은 새 문서로 만들지 않는다.
- 여러 클래스/모듈에서 반복되고, 팀의 구현 전략으로 볼 수 있을 때만 새 문서를 만든다.

## 4. 작성 원칙

- 일반적인 아키텍처 교과서 설명을 쓰지 않는다.
- 실제 클래스명, 패키지 구조, 어노테이션, 구현 방식 같은 관찰 결과를 중심으로 쓴다.
- 근거가 약한 내용은 문서에서 제외한다.
- 코드에서 더 이상 보이지 않는 패턴 문서는 병합 모드에서도 제거 후보로 본다.
