#!/usr/bin/env python3
"""Print and persist safe Korean progress traces for delivery stage skills."""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TRACE_DIR = ROOT / ".agents/runs/skill-traces"
SAFE_LABEL_RE = re.compile(r"^[\w가-힣./:-]{1,64}$")
SENSITIVE_RE = re.compile(
    r"token|secret|password|passwd|credential|authorization|cookie|api[_-]?key|"
    r"주민|비밀번호|인증|토큰|시크릿|이메일|전화|휴대폰|주소",
    re.IGNORECASE,
)


def trace_dir() -> Path:
    override = os.environ.get("CODEX_PLAYBOOK_TRACE_DIR")
    return Path(override) if override else DEFAULT_TRACE_DIR


def agent_dir(agent: str) -> Path:
    safe_agent = sanitize_label(agent)
    directory = trace_dir() / safe_agent
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def current_run_file(agent: str) -> Path:
    return agent_dir(agent) / "current.run"


def new_run_id(agent: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{stamp}-{sanitize_label(agent)}"


def resolve_run_id(agent: str, explicit_run: str | None, new_run: bool) -> str:
    if explicit_run:
        run_id = sanitize_label(explicit_run)
        current_run_file(agent).write_text(run_id, encoding="utf-8")
        return run_id

    marker = current_run_file(agent)
    if new_run or not marker.exists():
        run_id = new_run_id(agent)
        marker.write_text(run_id, encoding="utf-8")
        return run_id

    existing = marker.read_text(encoding="utf-8").strip()
    if existing:
        return sanitize_label(existing)

    run_id = new_run_id(agent)
    marker.write_text(run_id, encoding="utf-8")
    return run_id


def sanitize_label(value: str) -> str:
    value = value.strip()
    if not value or SENSITIVE_RE.search(value) or not SAFE_LABEL_RE.match(value):
        return "비표시"
    return value


def sanitize_labels(values: list[str]) -> list[str]:
    labels: list[str] = []
    for value in values:
        for part in value.split(","):
            label = sanitize_label(part)
            if label and label not in labels:
                labels.append(label)
    return labels or ["없음"]


def event_path(agent: str, run_id: str) -> Path:
    return agent_dir(agent) / f"{run_id}.jsonl"


def read_events(agent: str, run_id: str) -> list[dict[str, object]]:
    path = event_path(agent, run_id)
    if not path.exists():
        return []
    events: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        events.append(json.loads(line))
    return events


def next_call_number(agent: str, run_id: str, skill: str) -> int:
    events = read_events(agent, run_id)
    starts = [
        event
        for event in events
        if event.get("phase") == "start" and event.get("skill") == skill
    ]
    return len(starts) + 1


def append_event(agent: str, run_id: str, event: dict[str, object]) -> None:
    path = event_path(agent, run_id)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def print_start(args: argparse.Namespace, run_id: str) -> None:
    agent = sanitize_label(args.agent)
    skill = sanitize_label(args.skill)
    labels = sanitize_labels(args.input)
    call = next_call_number(agent, run_id, skill)
    event = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "phase": "start",
        "agent": agent,
        "skill": skill,
        "call": call,
        "input": labels,
    }
    append_event(agent, run_id, event)
    print(
        f"[스킬 진행] 실행={run_id} | 담당={agent} | 스킬={skill} | "
        f"{call}번째 호출 시작 | 입력={', '.join(labels)}"
    )


def print_end(args: argparse.Namespace, run_id: str) -> None:
    agent = sanitize_label(args.agent)
    skill = sanitize_label(args.skill)
    labels = sanitize_labels(args.output)
    status = sanitize_label(args.status)
    call = max(next_call_number(agent, run_id, skill) - 1, 1)
    event = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "phase": "end",
        "agent": agent,
        "skill": skill,
        "call": call,
        "output": labels,
        "status": status,
    }
    append_event(agent, run_id, event)
    print(
        f"[스킬 진행] 실행={run_id} | 담당={agent} | 스킬={skill} | "
        f"{call}번째 호출 종료 | 출력={', '.join(labels)} | 상태={status}"
    )


def print_summary(args: argparse.Namespace, run_id: str) -> None:
    agent = sanitize_label(args.agent)
    events = read_events(agent, run_id)
    counts = Counter(
        str(event.get("skill"))
        for event in events
        if event.get("phase") == "start" and event.get("skill")
    )
    print(f"[스킬 요약] 실행={run_id} | 담당={agent}")
    if not counts:
        print("- 호출 기록 없음")
        return
    for skill, count in sorted(counts.items()):
        print(f"- {skill}: {count}회 호출")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="delivery skill 진행 상황을 한글로 출력한다.")
    parser.add_argument("phase", choices=["start", "end", "summary"])
    parser.add_argument("--agent", required=True)
    parser.add_argument("--skill")
    parser.add_argument("--run")
    parser.add_argument("--new-run", action="store_true")
    parser.add_argument("--input", action="append", default=[])
    parser.add_argument("--output", action="append", default=[])
    parser.add_argument("--status", default="완료")
    args = parser.parse_args()
    if args.phase in {"start", "end"} and not args.skill:
        parser.error("--skill is required for start/end")
    return args


def main() -> int:
    args = parse_args()
    agent = sanitize_label(args.agent)
    run_id = resolve_run_id(agent, args.run, args.new_run)
    if args.phase == "start":
        print_start(args, run_id)
    elif args.phase == "end":
        print_end(args, run_id)
    else:
        print_summary(args, run_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
