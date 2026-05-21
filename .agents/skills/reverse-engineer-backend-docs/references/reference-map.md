# Reverse Engineer Backend Docs Reference Map

이 디렉토리는 `reverse-engineer-backend-docs` 스킬이 기존 backend codebase를 분석해 `docs/backend` 지식 시스템으로 변환할 때 쓰는 세부 기준을 계층별로 나눈다.

읽는 순서는 상위 개념에서 세부 작성 규칙 순서로 고정한다.

## 문서 계층

| 계층 | 문서 | 목적 |
|------|------|------|
| L0 | [../SKILL.md](../SKILL.md) | 스킬의 목적, 적용 범위, 실행 모드, 전체 흐름 |
| L1 | [codebase-analysis-guide.md](codebase-analysis-guide.md) | 코드에서 문서 후보를 찾는 분석 모델과 샘플링 기준 |
| L1 | [backend-document-routing.md](backend-document-routing.md) | 분석 결과를 `docs/backend` 어느 문서가 소유할지 결정하는 기준 |
| L2 | [backend-doc-templates.md](backend-doc-templates.md) | 선택된 문서를 실제로 작성할 때의 파일별 템플릿 |

## 전체 모델

```text
Codebase evidence
  -> analysis candidates
  -> routing decision
  -> docs/backend document templates
  -> validation against code evidence
```

핵심 원칙:

- 분석 기준, 라우팅 기준, 작성 템플릿을 섞지 않는다.
- 코드 분석 결과는 곧바로 문서가 되지 않는다. 먼저 문서 소유권과 confidence를 판단한다.
- 템플릿은 구조를 제공할 뿐, 코드에서 확인되지 않은 내용을 채우는 근거가 아니다.
- 기존 문서의 삭제·이전은 항상 보존 가치와 사용자 확인 필요 여부를 먼저 판단한다.

## 문서별 소유권

- `SKILL.md`: public entrypoint. 실행 모드, 전체 흐름, 완료 산출물만 소유한다.
- `codebase-analysis-guide.md`: repo census, 샘플링, confidence, 전략 후보 분류, 분석 메모 형식을 소유한다.
- `backend-document-routing.md`: 문서 위치, 소유권, 실행 모드 선택, 기존 문서 분류, 금지 규칙을 소유한다.
- `backend-doc-templates.md`: 선택된 `docs/backend` 파일을 어떤 섹션 구조로 작성할지 소유한다.

## 변경 가이드

- 분석할 코드 신호나 샘플링 기준이 바뀌면 `codebase-analysis-guide.md`를 수정한다.
- `docs/backend` 내 문서 위치나 소유권 기준이 바뀌면 `backend-document-routing.md`를 수정한다.
- 생성되는 문서의 섹션 구조나 완료 전 검증 기준이 바뀌면 `backend-doc-templates.md`를 수정한다.
- 사용자가 이 스킬을 언제 어떻게 호출해야 하는지 바뀌면 `SKILL.md`를 수정한다.
