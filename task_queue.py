import asyncio
from models import SBOMReviewJob

class TaskQueue:
    def __init__(self, maxsize: int, put_timeout: int, get_timeout: int):
        self._queue = asyncio.Queue(maxsize=maxsize)
        self._put_timeout = put_timeout



async def submit(self, job: SBOMReviewJob) -> None:
    try:
        async with asyncio.timeout(self._put_timeout):
            await self._queue.put(job)

    except TimeoutError as exc:
        raise TimeoutError("Task queue timed out") from exc


async def dequeue(self,) -> SBOMReviewJob:
     return await self._queue.get()
         


async def mark_complete(self,):
    ## mark the status of the queue
    return

