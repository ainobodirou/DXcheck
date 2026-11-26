from pydantic.dataclasses import dataclass
from pydantic import BaseModel,Field
from enum import Enum
from uuid import uuid4, UUID

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
