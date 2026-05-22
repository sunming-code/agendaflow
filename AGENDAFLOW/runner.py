"""Lightweight AgendaFlow runner."""

from __future__ import annotations

from .llm import build_chat, invoke_with_retry
from .models import (
    AgendaFlowResult,
    AgentContribution,
    FinalAnswer,
    PhaseArtifact,
    Protocol,
    RoleSet,
    RouteResult,
)
from .prompts import (
    contribution_messages,
    final_messages,
    role_messages,
    route_messages,
    synthesis_messages,
)
from .protocols import get_protocol_phases
from .storage import save_result


def clamp_role_count(value: int | None) -> int:
    if value is None:
        return 4
    return max(2, min(8, int(value)))


class AgendaFlowRunner:
    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        model: str,
        role_count: int | None = None,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.role_count = clamp_role_count(role_count)
        self.routing_llm = build_chat(
            api_key=api_key,
            base_url=base_url,
            model=model,
            temperature=0.0,
        )
        self.creative_llm = build_chat(
            api_key=api_key,
            base_url=base_url,
            model=model,
            temperature=0.5,
        )
        self.reasoning_llm = build_chat(
            api_key=api_key,
            base_url=base_url,
            model=model,
            temperature=0.2,
        )

    def route_task(self, task: str) -> RouteResult:
        chain = self.routing_llm.with_structured_output(RouteResult)
        try:
            return invoke_with_retry(chain, route_messages(task), "Task routing")
        except Exception:
            return RouteResult(
                protocol=Protocol.PROBLEM_SOLVING,
                justification="Routing failed, so AgendaFlow used the default problem_solving protocol.",
            )

    def generate_roles(self, task: str, protocol: Protocol) -> RoleSet:
        chain = self.creative_llm.with_structured_output(RoleSet)
        result: RoleSet = invoke_with_retry(
            chain,
            role_messages(task, protocol, self.role_count),
            "Role generation",
        )
        roles = result.roles[: self.role_count]
        if len(roles) < self.role_count:
            raise ValueError(
                f"Role generation returned {len(roles)} roles, expected {self.role_count}."
            )
        return RoleSet(roles=roles)

    def run_phase(
        self,
        *,
        task: str,
        protocol: Protocol,
        phase: dict[str, str],
        roles: RoleSet,
        artifacts: list[PhaseArtifact],
        unresolved_issues: list[str],
        transcript: list[dict],
    ) -> PhaseArtifact:
        contribution_chain = self.reasoning_llm.with_structured_output(AgentContribution)
        contributions: list[AgentContribution] = []
        for role in roles.roles:
            contribution: AgentContribution = invoke_with_retry(
                contribution_chain,
                contribution_messages(
                    task=task,
                    protocol=protocol,
                    phase=phase,
                    role=role,
                    artifacts=artifacts,
                    unresolved_issues=unresolved_issues,
                ),
                f"{phase['name']} / {role.name}",
            )
            contributions.append(contribution)
            transcript.append({
                "type": "agent_contribution",
                "phase": phase["name"],
                "role": role.name,
                "content": contribution.model_dump(),
            })

        synthesis_chain = self.reasoning_llm.with_structured_output(PhaseArtifact)
        artifact: PhaseArtifact = invoke_with_retry(
            synthesis_chain,
            synthesis_messages(
                task=task,
                protocol=protocol,
                phase=phase,
                contributions=contributions,
                previous_artifacts=artifacts,
                unresolved_issues=unresolved_issues,
            ),
            f"{phase['name']} synthesis",
        )
        artifact.phase_name = phase["name"]
        transcript.append({
            "type": "phase_artifact",
            "phase": phase["name"],
            "content": artifact.model_dump(),
        })
        return artifact

    def generate_final_answer(
        self,
        *,
        task: str,
        protocol: Protocol,
        artifacts: list[PhaseArtifact],
        unresolved_issues: list[str],
    ) -> FinalAnswer:
        chain = self.reasoning_llm.with_structured_output(FinalAnswer)
        return invoke_with_retry(
            chain,
            final_messages(
                task=task,
                protocol=protocol,
                artifacts=artifacts,
                unresolved_issues=unresolved_issues,
            ),
            "Final answer",
        )

    def run(self, task: str) -> AgendaFlowResult:
        route = self.route_task(task)
        print(f"\nSelected protocol: {route.protocol.value}")
        print(f"Reason: {route.justification}")

        roles = self.generate_roles(task, route.protocol)
        print("\nGenerated roles:")
        for index, role in enumerate(roles.roles, 1):
            print(f"  {index}. {role.name} - {role.function}")

        transcript: list[dict] = [
            {
                "type": "routing",
                "protocol": route.protocol.value,
                "justification": route.justification,
            },
            {
                "type": "roles",
                "roles": [role.model_dump() for role in roles.roles],
            },
        ]
        artifacts: list[PhaseArtifact] = []
        unresolved_issues: list[str] = []

        for phase in get_protocol_phases(route.protocol):
            print(f"\nPhase: {phase['name']}")
            artifact = self.run_phase(
                task=task,
                protocol=route.protocol,
                phase=phase,
                roles=roles,
                artifacts=artifacts,
                unresolved_issues=unresolved_issues,
                transcript=transcript,
            )
            artifacts.append(artifact)
            unresolved_issues = artifact.open_issues
            print(f"Artifact: {artifact.summary}")

        final_answer = self.generate_final_answer(
            task=task,
            protocol=route.protocol,
            artifacts=artifacts,
            unresolved_issues=unresolved_issues,
        )

        result = AgendaFlowResult(
            task=task,
            protocol=route.protocol,
            routing_justification=route.justification,
            roles=roles.roles,
            phase_artifacts=artifacts,
            unresolved_issues=unresolved_issues,
            final_answer=final_answer.answer,
            transcript=transcript,
        )
        result_dict = result.model_dump(mode="json")
        saved_path = save_result(result_dict)
        result.saved_path = saved_path
        return result


def run_agendaflow(
    *,
    task: str,
    api_key: str,
    base_url: str,
    model: str,
    role_count: int | None = None,
) -> AgendaFlowResult:
    runner = AgendaFlowRunner(
        api_key=api_key,
        base_url=base_url,
        model=model,
        role_count=role_count,
    )
    return runner.run(task)
