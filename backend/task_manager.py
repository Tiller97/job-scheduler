"""
task_manager.py
Tracks jobs by status using defaultdict(list).
"""
from collections import defaultdict
from typing import Dict, List
from models import Job


class TaskManager:
    def __init__(self) -> None:
        self.jobs_by_status: Dict[str, List[Job]] = defaultdict(list)

    def add_job(self, job: Job) -> None:
        self.jobs_by_status[job.get_status()].append(job)

    def get_all(self) -> Dict[str, List[Job]]:
        return self.jobs_by_status

    def get_jobs_by_status(self, status: str) -> List[Job]:
        return list(self.jobs_by_status.get(status, []))

    def update_status(self, job: Job, new_status: str) -> None:
        """Move a job between status buckets and update its internal status."""
        old_bucket = self.jobs_by_status.get(job.get_status(), [])
        if job in old_bucket:
            old_bucket.remove(job)
        # Use the encapsulated setter (auto-logs the status change)
        job.set_status(new_status)
        self.jobs_by_status[new_status].append(job)
