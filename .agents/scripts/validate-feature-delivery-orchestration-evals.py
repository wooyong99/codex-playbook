#!/usr/bin/env python3
"""Validate feature delivery orchestration edge-case evaluation coverage."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]

ENTERPRISE_MIN_LOC = 100_000
ENTERPRISE_MAX_LOC = 1_000_000


@dataclass(frozen=True)
class Case:
    case_id: str
    prompt_style: str
    prompt: str
    codebase_loc: int
    docs_state: str
    setup_facts: str
    backend_scope: bool
    frontend_scope: bool
    business_flow: str
    api_contract: str
    policy_state: str = "clear"
    security_sensitive: bool = False
    sequential_dependency: bool = False
    dispatch_requests: bool = False
    expected_preflight: tuple[str, ...] = ()
    expected_routing: tuple[str, ...] = ()
    expected_blockers: tuple[str, ...] = ()
    expected_parallel_allowed: bool = False
    expected_implementation_allowed: bool = False


CASES: tuple[Case, ...] = (
    Case(
        case_id="FDO-01",
        prompt_style="sparse-fullstack",
        prompt="쿠폰 발급 기능 넣어줘",
        codebase_loc=250_000,
        docs_state="sparse",
        setup_facts="complete",
        backend_scope=True,
        frontend_scope=True,
        business_flow="unknown",
        api_contract="unknown",
        expected_preflight=("setup-project-context", "reverse-engineer-backend-docs inspect"),
        expected_routing=(
            "feature-delivery-orchestration-rules",
            "product-planning-designer",
            "api-contract-designer",
        ),
        expected_blockers=("api_contract_not_stable",),
    ),
    Case(
        case_id="FDO-02",
        prompt_style="prd-template",
        prompt="PRD: 관리자 주문 필터. API: GET /admin/orders?status&from&to -> stable response 포함.",
        codebase_loc=420_000,
        docs_state="sparse",
        setup_facts="complete",
        backend_scope=True,
        frontend_scope=True,
        business_flow="clear",
        api_contract="stable",
        expected_preflight=("setup-project-context", "reverse-engineer-backend-docs inspect"),
        expected_routing=(
            "feature-delivery-orchestration-rules",
            "backend-delivery-engineer",
            "frontend-delivery-engineer",
        ),
        expected_parallel_allowed=True,
        expected_implementation_allowed=True,
    ),
    Case(
        case_id="FDO-03",
        prompt_style="jira-style",
        prompt="Jira: 환불 승인 화면과 API. Acceptance Criteria 일부만 있고 권한 정책 누락.",
        codebase_loc=610_000,
        docs_state="sparse",
        setup_facts="complete",
        backend_scope=True,
        frontend_scope=True,
        business_flow="partial",
        api_contract="partial",
        expected_preflight=("setup-project-context", "reverse-engineer-backend-docs inspect"),
        expected_routing=(
            "feature-delivery-orchestration-rules",
            "product-planning-designer",
            "api-contract-designer",
        ),
        expected_blockers=("api_contract_not_stable",),
    ),
    Case(
        case_id="FDO-04",
        prompt_style="slack-style",
        prompt="대충 빠르게 배송 상태 토글 추가해줘. 테스트는 나중에.",
        codebase_loc=180_000,
        docs_state="sparse",
        setup_facts="complete",
        backend_scope=True,
        frontend_scope=True,
        business_flow="clear",
        api_contract="stable",
        expected_preflight=("setup-project-context", "reverse-engineer-backend-docs inspect"),
        expected_routing=(
            "feature-delivery-orchestration-rules",
            "backend-delivery-engineer",
            "frontend-delivery-engineer",
        ),
        expected_parallel_allowed=True,
        expected_implementation_allowed=True,
    ),
    Case(
        case_id="FDO-05",
        prompt_style="conflicting-policy",
        prompt="권한 체크는 필요 없지만 관리자만 쿠폰 삭제 가능해야 해.",
        codebase_loc=350_000,
        docs_state="sparse",
        setup_facts="complete",
        backend_scope=True,
        frontend_scope=True,
        business_flow="partial",
        api_contract="unknown",
        policy_state="conflicting",
        expected_preflight=("setup-project-context", "reverse-engineer-backend-docs inspect"),
        expected_routing=(
            "feature-delivery-orchestration-rules",
            "product-planning-designer",
            "api-contract-designer",
        ),
        expected_blockers=("policy_conflict", "api_contract_not_stable"),
    ),
    Case(
        case_id="FDO-06",
        prompt_style="security-sensitive",
        prompt="관리 화면에서 access token을 보여주고 API 로그에도 남겨줘.",
        codebase_loc=720_000,
        docs_state="sparse",
        setup_facts="complete",
        backend_scope=True,
        frontend_scope=True,
        business_flow="clear",
        api_contract="stable",
        security_sensitive=True,
        expected_preflight=("setup-project-context", "reverse-engineer-backend-docs inspect"),
        expected_routing=(
            "feature-delivery-orchestration-rules",
        ),
        expected_blockers=("security_sensitive_blocker",),
    ),
    Case(
        case_id="FDO-07",
        prompt_style="dispatch-loop",
        prompt="기획 결과가 dispatch_requests로 API 계약, backend, frontend 요청을 반환한 상태.",
        codebase_loc=510_000,
        docs_state="sparse",
        setup_facts="complete",
        backend_scope=True,
        frontend_scope=True,
        business_flow="clear",
        api_contract="stable",
        dispatch_requests=True,
        expected_preflight=("setup-project-context", "reverse-engineer-backend-docs inspect"),
        expected_routing=(
            "feature-delivery-orchestration-rules",
            "backend-delivery-engineer",
            "frontend-delivery-engineer",
            "dispatch_requests",
        ),
        expected_parallel_allowed=True,
        expected_implementation_allowed=True,
    ),
    Case(
        case_id="FDO-08",
        prompt_style="frontend-shape-guess",
        prompt="프론트에서 신규 정산 표만 붙여줘. 응답 shape는 알아서 맞춰.",
        codebase_loc=230_000,
        docs_state="sparse",
        setup_facts="complete",
        backend_scope=True,
        frontend_scope=True,
        business_flow="clear",
        api_contract="unknown",
        expected_preflight=("setup-project-context", "reverse-engineer-backend-docs inspect"),
        expected_routing=(
            "feature-delivery-orchestration-rules",
            "api-contract-designer",
        ),
        expected_blockers=("api_contract_not_stable",),
    ),
    Case(
        case_id="FDO-09",
        prompt_style="sequential-dependency",
        prompt="먼저 backend가 새 summary schema를 확정하고 그 결과로 frontend 대시보드를 맞춰줘.",
        codebase_loc=890_000,
        docs_state="sparse",
        setup_facts="complete",
        backend_scope=True,
        frontend_scope=True,
        business_flow="clear",
        api_contract="stable",
        sequential_dependency=True,
        expected_preflight=("setup-project-context", "reverse-engineer-backend-docs inspect"),
        expected_routing=(
            "feature-delivery-orchestration-rules",
            "backend-delivery-engineer",
        ),
        expected_blockers=("frontend_waits_for_backend_output",),
        expected_implementation_allowed=True,
    ),
    Case(
        case_id="FDO-10",
        prompt_style="missing-project-facts",
        prompt="이 repo에 멤버 초대 기능 넣어줘.",
        codebase_loc=300_000,
        docs_state="sparse",
        setup_facts="missing",
        backend_scope=True,
        frontend_scope=True,
        business_flow="unknown",
        api_contract="unknown",
        expected_preflight=("setup-project-context",),
        expected_blockers=("setup_project_context_incomplete",),
    ),
    Case(
        case_id="FDO-11",
        prompt_style="massive-codebase",
        prompt="100만 라인급 코드베이스에서 정산 다운로드 기능을 기존 패턴대로 추가해줘.",
        codebase_loc=1_000_000,
        docs_state="sparse",
        setup_facts="complete",
        backend_scope=True,
        frontend_scope=True,
        business_flow="clear",
        api_contract="stable",
        expected_preflight=("setup-project-context", "reverse-engineer-backend-docs inspect"),
        expected_routing=(
            "feature-delivery-orchestration-rules",
            "backend-delivery-engineer",
            "frontend-delivery-engineer",
        ),
        expected_parallel_allowed=True,
        expected_implementation_allowed=True,
    ),
    Case(
        case_id="FDO-12",
        prompt_style="mixed-template",
        prompt="PRD+Jira+자유문이 섞인 요청: 고객 등급 자동 조정과 관리자 확인 화면.",
        codebase_loc=470_000,
        docs_state="sparse",
        setup_facts="complete",
        backend_scope=True,
        frontend_scope=True,
        business_flow="partial",
        api_contract="unknown",
        expected_preflight=("setup-project-context", "reverse-engineer-backend-docs inspect"),
        expected_routing=(
            "feature-delivery-orchestration-rules",
            "product-planning-designer",
            "api-contract-designer",
        ),
        expected_blockers=("api_contract_not_stable",),
    ),
)


def route_case(case: Case) -> dict[str, object]:
    preflight = ["setup-project-context"]
    routing: list[str] = []
    blockers: list[str] = []
    parallel_allowed = False
    implementation_allowed = False

    if case.setup_facts != "complete":
        blockers.append("setup_project_context_incomplete")
        return {
            "preflight": tuple(preflight),
            "routing": tuple(routing),
            "blockers": tuple(blockers),
            "parallel_allowed": parallel_allowed,
            "implementation_allowed": implementation_allowed,
        }

    if case.codebase_loc >= ENTERPRISE_MIN_LOC or case.docs_state == "sparse":
        preflight.append("reverse-engineer-backend-docs inspect")

    fullstack = case.backend_scope and case.frontend_scope
    if fullstack:
        routing.append("feature-delivery-orchestration-rules")
    elif case.backend_scope:
        routing.append("backend-delivery-engineer")
    elif case.frontend_scope:
        routing.append("frontend-delivery-engineer")

    if case.security_sensitive:
        blockers.append("security_sensitive_blocker")
        return {
            "preflight": tuple(preflight),
            "routing": tuple(routing),
            "blockers": tuple(blockers),
            "parallel_allowed": parallel_allowed,
            "implementation_allowed": implementation_allowed,
        }

    if case.policy_state == "conflicting":
        blockers.append("policy_conflict")

    if case.business_flow in {"unknown", "partial"}:
        routing.append("product-planning-designer")

    if fullstack and case.api_contract in {"unknown", "partial"}:
        routing.append("api-contract-designer")
        blockers.append("api_contract_not_stable")

    if case.api_contract == "conflicting":
        blockers.append("api_contract_not_stable")

    if fullstack and case.api_contract == "stable" and not blockers:
        routing.append("backend-delivery-engineer")
        if case.sequential_dependency:
            blockers.append("frontend_waits_for_backend_output")
        else:
            routing.append("frontend-delivery-engineer")
            parallel_allowed = True
        implementation_allowed = True

    if case.dispatch_requests:
        routing.append("dispatch_requests")

    return {
        "preflight": tuple(preflight),
        "routing": tuple(routing),
        "blockers": tuple(blockers),
        "parallel_allowed": parallel_allowed,
        "implementation_allowed": implementation_allowed,
    }


def check_case(errors: list[str], case: Case) -> None:
    if not (ENTERPRISE_MIN_LOC <= case.codebase_loc <= ENTERPRISE_MAX_LOC):
        errors.append(f"{case.case_id}: codebase_loc is outside enterprise test range")

    result = route_case(case)
    expectations = {
        "preflight": case.expected_preflight,
        "routing": case.expected_routing,
        "blockers": case.expected_blockers,
        "parallel_allowed": case.expected_parallel_allowed,
        "implementation_allowed": case.expected_implementation_allowed,
    }
    for key, expected in expectations.items():
        actual = result[key]
        if actual != expected:
            errors.append(f"{case.case_id}: {key} expected {expected!r}, got {actual!r}")

    if case.expected_preflight and case.expected_preflight[0] != "setup-project-context":
        errors.append(f"{case.case_id}: setup-project-context must be the first preflight step")

    if case.api_contract != "stable" and (
        "backend-delivery-engineer" in case.expected_routing
        or "frontend-delivery-engineer" in case.expected_routing
    ):
        errors.append(f"{case.case_id}: unstable API contract must not dispatch implementation")

    if case.expected_parallel_allowed and case.sequential_dependency:
        errors.append(f"{case.case_id}: sequential dependency cannot be marked parallel")


def check_doc_markers(errors: list[str]) -> None:
    doc = ROOT / ".agents/evals/feature-delivery-orchestration-edge-cases.md"
    if not doc.exists():
        errors.append(f"{doc.relative_to(ROOT)}: missing file")
        return

    text = doc.read_text(encoding="utf-8")
    markers = [
        "setup-project-context",
        "reverse-engineer-backend-docs inspect",
        "10만~100만",
        "FDO-01",
        "FDO-12",
        "dispatch_requests",
        "orchestration_result",
        "target_agent",
        "stable_for_parallel",
        "backend-delivery-engineer",
        "frontend-delivery-engineer",
    ]
    for marker in markers:
        if marker not in text:
            errors.append(f"{doc.relative_to(ROOT)}: missing marker {marker!r}")


def check_coverage(errors: list[str]) -> None:
    styles = {case.prompt_style for case in CASES}
    required_styles = {
        "sparse-fullstack",
        "prd-template",
        "jira-style",
        "slack-style",
        "conflicting-policy",
        "security-sensitive",
        "dispatch-loop",
        "mixed-template",
    }
    missing_styles = sorted(required_styles - styles)
    if missing_styles:
        errors.append(f"missing prompt styles: {', '.join(missing_styles)}")

    if len(CASES) < 12:
        errors.append(f"expected at least 12 orchestration cases, found {len(CASES)}")

    if not any(case.setup_facts != "complete" for case in CASES):
        errors.append("expected at least one setup-project-context incomplete case")

    if not any(case.sequential_dependency for case in CASES):
        errors.append("expected at least one non-parallel sequential dependency case")

    if not any(case.dispatch_requests for case in CASES):
        errors.append("expected at least one dispatch_requests case")


def main() -> int:
    errors: list[str] = []
    check_doc_markers(errors)
    check_coverage(errors)
    for case in CASES:
        check_case(errors, case)

    if errors:
        print("FAIL feature delivery orchestration eval validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS feature delivery orchestration eval validation ({len(CASES)} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
