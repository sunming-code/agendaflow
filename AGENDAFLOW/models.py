"""Data models for the lightweight AgendaFlow runner."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Protocol(str, Enum):
    PLANNING = "planning"
    PROBLEM_SOLVING = "problem_solving"
    VERIFICATION = "verification"
    DECISION_SELECTION = "decision_selection"


class RouteResult(BaseModel):
    protocol: Protocol = Field(description="Selected reasoning protocol.")
    justification: str = Field(description="Short reason for the selected protocol.")


class AgentRole(BaseModel):
    name: str = Field(description="Concise role name.")
    function: str = Field(description="The reasoning function this role covers.")
    style: str = Field(description="How this role should think and respond.")
    responsibility: str = Field(description="Primary contribution expected from this role.")


class RoleSet(BaseModel):
    roles: list[AgentRole] = Field(description="Generated role list.")


class AgentContribution(BaseModel):
    role_name: str = Field(description="Role name.")
    contribution: str = Field(description="Role-specific contribution for the current phase.")
    issues: list[str] = Field(default_factory=list, description="Open issues raised by this role.")
    artifact_update: str = Field(description="Concise update to be considered in the phase artifact.")


class PhaseArtifact(BaseModel):
    phase_name: str = Field(description="Current phase name.")
    summary: str = Field(description="Consolidated phase result.")
    supported_points: list[str] = Field(default_factory=list)
    open_issues: list[str] = Field(default_factory=list)
    next_focus: str = Field(default="", description="What later phases should preserve or address.")


class FinalAnswer(BaseModel):
    answer: str = Field(description="Final answer to the original task.")


class AgendaFlowResult(BaseModel):
    task: str
    protocol: Protocol
    routing_justification: str
    roles: list[AgentRole]
    phase_artifacts: list[PhaseArtifact]
    unresolved_issues: list[str]
    final_answer: str
    transcript: list[dict[str, Any]]
    saved_path: str = ""
