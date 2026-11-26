from uuid import UUID
from models import JobRecord, SBOMReviewJob, Status
import time
from config import JOB_TTL


class JobStore:
    def __init__(self):
        self._jobs: dict[UUID, JobRecord] = {}

    def register(self, job: SBOMReviewJob) -> None:
        id = job.job_id
        record = JobRecord(
            job_id = id,
            repository_id= job.repostiry_id
        )
        self._jobs[id] = record
        
    def get(self, job_id: UUID) -> JobRecord | None:
        return self._jobs.get(job_id)

    def remove(self, job_id: UUID) -> None:
        self._jobs.pop(job_id, None)

    def complete(self, job_id: UUID, result: str) -> None:
        record = self._jobs[job_id]

        record.result = result
        record.status = Status.COMPLETED
        record.exp_at = int(time.time()) + JOB_TTL

    def fail(self, job_id: UUID, error: str) -> None:
        record = self._jobs[job_id]

        record.error = error
        record.status = Status.FAILED
        record.exp_at = int(time.time()) + JOB_TTL