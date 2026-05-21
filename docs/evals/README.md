# Agent Evaluation Suite

이 디렉토리는 codex-playbook을 적용한 AI 에이전트가 일관된 품질로 작업하는지 확인하기 위한 평가 기준을 소유한다.

## 문서 목록

- [scenarios](scenarios.md): 대표 평가 시나리오와 기대 산출물
- [enterprise-agent-collaboration](enterprise-agent-collaboration.md): 대형 코드베이스와 모호한 프롬프트에서 subagent/skill 협력 품질을 검증하는 평가 매트릭스
- [scorecard](scorecard.md): 점수표, pass 기준, blocker 기준

## 평가 원칙

- 평가는 모델 성능 자체가 아니라 이 플레이북이 제공하는 작업 환경의 품질을 본다.
- 시나리오는 요구사항 분석, 문서 탐색, 구현 계획, 검토, 검증, 복구를 모두 관찰할 수 있어야 한다.
- 평가 결과는 pass/fail뿐 아니라 어떤 문서나 규칙이 부족했는지 backlog로 남긴다.
- 20만~100만 라인 코드베이스 대응성은 전체 정독 금지, 샘플링 근거, confidence report 품질로 평가한다.

## 기본 실행 흐름

1. [scenarios](scenarios.md)에서 평가 케이스를 고른다.
2. 대형 코드베이스나 모호한 프롬프트 평가는 [enterprise-agent-collaboration](enterprise-agent-collaboration.md)의 preflight를 먼저 적용한다.
3. 동일한 저장소 상태에서 에이전트에게 케이스를 실행하게 한다.
4. 산출물, 변경 파일, 검증 명령, reviewer 결과를 모은다.
5. [scorecard](scorecard.md) 기준으로 채점한다.
6. 실패 원인을 규칙, 문서, 스킬, reviewer, 검증 자동화 backlog로 분류한다.
