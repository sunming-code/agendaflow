"""Small protocol templates used by the lightweight AgendaFlow runner."""

from __future__ import annotations

from .models import Protocol


PROTOCOL_PHASES: dict[Protocol, list[dict[str, str]]] = {
    Protocol.PLANNING: [
        {
            "name": "Goal and constraint framing",
            "objective": "Clarify the desired outcome, hard constraints, available resources, and success criteria.",
        },
        {
            "name": "Plan construction",
            "objective": "Build a feasible sequence of actions that respects the known constraints.",
        },
        {
            "name": "Feasibility review",
            "objective": "Stress-test the plan for timing, dependencies, risks, and missing prerequisites.",
        },
        {
            "name": "Plan closure",
            "objective": "Produce the final plan with important conditions and fallback notes.",
        },
    ],
    Protocol.PROBLEM_SOLVING: [
        {
            "name": "Problem framing",
            "objective": "Define the problem, symptoms, affected scope, and what would count as resolution.",
        },
        {
            "name": "Cause exploration",
            "objective": "Identify plausible causes, evidence, contradictions, and missing information.",
        },
        {
            "name": "Solution design",
            "objective": "Map corrective actions to likely causes and separate immediate fixes from preventive measures.",
        },
        {
            "name": "Answer convergence",
            "objective": "Synthesize the most useful diagnosis and action recommendation.",
        },
    ],
    Protocol.VERIFICATION: [
        {
            "name": "Inference target",
            "objective": "Clarify the claim, question, rule, or state that must be verified.",
        },
        {
            "name": "Evidence organization",
            "objective": "Collect and organize relevant facts, rules, clues, or constraints from the task text.",
        },
        {
            "name": "Consistency check",
            "objective": "Check whether the evidence supports, contradicts, or leaves ambiguity around the target.",
        },
        {
            "name": "Grounded judgment",
            "objective": "Produce the best supported conclusion without adding outside facts.",
        },
    ],
    Protocol.DECISION_SELECTION: [
        {
            "name": "Decision boundary",
            "objective": "Clarify the exact decision, candidate options, and decision owner or context.",
        },
        {
            "name": "Criteria anchoring",
            "objective": "Separate hard constraints, soft preferences, risks, and evaluation criteria.",
        },
        {
            "name": "Option comparison",
            "objective": "Compare candidates under the same criteria and expose major trade-offs.",
        },
        {
            "name": "Conditional closure",
            "objective": "Select the best option and state conditions, caveats, or reopening triggers.",
        },
    ],
}


def get_protocol_phases(protocol: Protocol) -> list[dict[str, str]]:
    return PROTOCOL_PHASES.get(protocol, PROTOCOL_PHASES[Protocol.PROBLEM_SOLVING])
