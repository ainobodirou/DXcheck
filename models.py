from pydantic.dataclasses import dataclass
from pydantic import BaseModel,Field
from enum import Enum
from uuid import uuid4, UUID

## Dependancy Graph
@dataclass
class Component:
    bom_ref: str
    purl: str
    name: str
    version: str

@dataclass
class DependencyGraph:
    nodes: dict[str, Component]
    edges: set[tuple[str,str]]

## Dependancy Graph changes
class ChangeType(str, Enum):
    ADDED = "added"
    REMOVED = "removed"
    UPDATED = "updated"


@dataclass(frozen=True)
class NodeChanges:
    name: str
    purl: str
    change_type: ChangeType
    previous_version: str | None = None
    new_version: str | None = None

@dataclass(frozen=True)
class EdgeChanges:
    source: str
    target: str
    change_type: ChangeType

@dataclass
class GraphDiff:
    node_changes: list[NodeChanges] | None = None
    edge_changes: list[EdgeChanges] | None = None

## SBOM Review Jobs and Job records for store
class Status(Enum):

    QUEUED = "queued"
    PROCESSING = "processing"
    FAILED = "failed"
    COMPLETED = "comleted"


class SBOMReviewJob(BaseModel):
    job_id: UUID = Field(default_factory=uuid4)
    repostiry_id: str
    base_sbom: dict
    head_sbom: dict

class SBOMReviewRequest(BaseModel):
    base_sbom: dict
    head_sbom: dict

class JobRecord(BaseModel):
    job_id: UUID 
    repository_id: str
    status: Status.QUEUED
    result: str | None = None
    error: str | None = None
    exp_at: int | None = None
