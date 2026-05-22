"""Prompt builders for the lightweight AgendaFlow runner."""

from __future__ import annotations

import json

from .models import AgentContribution, AgentRole, PhaseArtifact, Protocol


ROUTING_SYSTEM = """You route a user task to one lightweight AgendaFlow protocol.

Choose exactly one:
- planning: build a plan, route, schedule, arrangement, or action sequence.
- problem_solving: diagnose a problem, failure, blockage, inconsistency, or underperformance and suggest fixes.
- verification: answer by checking rules, evidence, clues, states, claims, or internal consistency in the task text.
- decision_selection: choose among explicit options under criteria or constraints.

If uncertain, choose problem_solving.
Do not answer the task."""


ROLE_SYSTEM = """You generate functional reasoning roles for a lightweight multi-agent deliberation.

Each role must have:
- name
- function
- style
- responsibility

Roles should be complementary and should help solve the task through the selected protocol.
Do not include external lookup roles or human meeting-operation roles."""


CONTRIBUTION_SYSTEM = """You are one role in a structured multi-agent reasoning process.

Respond only for your assigned role and only for the current phase.
Use only the task, previous phase artifacts, and stated context. Do not introduce outside facts.
Keep the contribution concise and useful."""


SYNTHESIS_SYSTEM = """You are the moderator for a lightweight AgendaFlow process.

Synthesize the role contributions into one phase artifact.
Merge overlapping ideas, keep useful disagreements visible, and carry forward unresolved issues.
Do not add outside facts."""


FINAL_SYSTEM = """Generate the final answer to the original task.

Use only the completed phase artifacts and unresolved issues.
Do not mention internal roles, phases, or artifacts unless it is necessary for clarity.
Be direct and practical."""


def route_messages(task: str) -> list[tuple[str, str]]:
    return [
        ("system", ROUTING_SYSTEM),
        ("user", f"Task:\n{task}"),
    ]


def role_messages(task: str, protocol: Protocol, role_count: int) -> list[tuple[str, str]]:
    return [
        ("system", ROLE_SYSTEM),
        (
            "user",
            "\n".join([
                f"Task:\n{task}",
                "",
                f"Selected protocol: {protocol.value}",
                f"Generate exactly {role_count} roles.",
            ]),
        ),
    ]


def contribution_messages(
    *,
    task: str,
    protocol: Protocol,
    phase: dict[str, str],
    role: AgentRole,
    artifacts: list[PhaseArtifact],
    unresolved_issues: list[str],
) -> list[tuple[str, str]]:
    artifact_text = json.dumps(
        [artifact.model_dump() for artifact in artifacts],
        ensure_ascii=False,
        indent=2,
    )
    issues_text = json.dumps(unresolved_issues, ensure_ascii=False, indent=2)
    return [
        ("system", CONTRIBUTION_SYSTEM),
        (
            "user",
            "\n".join([
                f"Task:\n{task}",
                "",
                f"Protocol: {protocol.value}",
                f"Current phase: {phase['name']}",
                f"Phase objective: {phase['objective']}",
                "",
                "Your role:",
                role.model_dump_json(indent=2),
                "",
                "Previous phase artifacts:",
                artifact_text or "[]",
                "",
                "Unresolved issues:",
                issues_text,
            ]),
        ),
    ]


def synthesis_messages(
    *,
    task: str,
    protocol: Protocol,
    phase: dict[str, str],
    contributions: list[AgentContribution],
    previous_artifacts: list[PhaseArtifact],
    unresolved_issues: list[str],
) -> list[tuple[str, str]]:
    return [
        ("system", SYNTHESIS_SYSTEM),
        (
            "user",
            "\n".join([
                f"Task:\n{task}",
                "",
                f"Protocol: {protocol.value}",
                f"Current phase: {phase['name']}",
                f"Phase objective: {phase['objective']}",
                "",
                "Previous artifacts:",
                json.dumps([a.model_dump() for a in previous_artifacts], ensure_ascii=False, indent=2),
                "",
                "Current unresolved issues:",
                json.dumps(unresolved_issues, ensure_ascii=False, indent=2),
                "",
                "Role contributions:",
                json.dumps([c.model_dump() for c in contributions], ensure_ascii=False, indent=2),
            ]),
        ),
    ]


def final_messages(
    *,
    task: str,
    protocol: Protocol,
    artifacts: list[PhaseArtifact],
    unresolved_issues: list[str],
) -> list[tuple[str, str]]:
    return [
        ("system", FINAL_SYSTEM),
        (
            "user",
            "\n".join([
                f"Task:\n{task}",
                "",
                f"Protocol: {protocol.value}",
                "",
                "Completed phase artifacts:",
                json.dumps([a.model_dump() for a in artifacts], ensure_ascii=False, indent=2),
                "",
                "Remaining unresolved issues:",
                json.dumps(unresolved_issues, ensure_ascii=False, indent=2),
            ]),
        ),
    ]
