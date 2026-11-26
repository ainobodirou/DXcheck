from fastapi import FastAPI, HTTPException
from config import Q_PUT_TIMEOUT,Q_SIZE
from models import SBOMReviewJob, SBOMReviewRequest
from jobstore import JobStore
from task_queue import TaskQueue
from fastapi import Depends, HTTPException
from auth import authenticate
import asyncio

task_queue = TaskQueue(Q_SIZE,Q_PUT_TIMEOUT)
job_store = JobStore()
app = FastAPI()

@app.post("/reviews", status_code=202)
async def submit_review(
    request: SBOMReviewRequest,
    claims: dict = Depends(authenticate)
    ):
    job = SBOMReviewJob(
        repository_id = claims["repository_id"],
        base_sbom=request.base_sbom,
        head_sbom=request.head_sbom
    )

    job_store.register(job)

    try:
        await task_queue.submit(job)
    except TimeoutError:
        job_store.remove(job.job_id)
        raise HTTPException(503,"Job queue is full")
    except asyncio.CancelledError:
        job_store.remove(job.job_id)
        raise
    return{
        "job_id": job.job_id,
        "status": "queued"
    }

    


    

