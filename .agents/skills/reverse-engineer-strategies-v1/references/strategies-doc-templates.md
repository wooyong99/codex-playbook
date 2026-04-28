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

아래 문서는 코드에서 해당 패턴이 실제로 보일 때만 만든다.

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

## 4. 작성 원칙

- 일반적인 아키텍처 교과서 설명을 쓰지 않는다.
- 실제 클래스명, 패키지 구조, 어노테이션, 구현 방식 같은 관찰 결과를 중심으로 쓴다.
- 근거가 약한 내용은 문서에서 제외한다.
- 코드에서 더 이상 보이지 않는 패턴 문서는 병합 모드에서도 제거 후보로 본다.
