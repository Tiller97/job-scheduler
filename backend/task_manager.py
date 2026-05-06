"""
task_manager.py
Tracks jobs by status using defaultdict(list).
Provides a clean API to query and update job status buckets.
"""

from collections import defaultdict
from typing import Dict, List
from models import Job


class TaskManager:
    """Organises jobs by their current status."""

    def __init__(self) -> None:
        self.jobs_by_status: Dict[str, List[Job]] = defaultdict(list)

    def add_job(self, job: Job) -> None:
        """Add a job to the bucket matching its current status."""
        self.jobs_by_status[job.get_status()].append(job)

    def get_all(self) -> Dict[str, List[Job]]:
        return self.jobs_by_status

    def get_jobs_by_status(self, status: str) -> List[Job]:
        return list(self.jobs_by_status.get(status, []))

    def update_status(self, job: Job, new_status: str) -> None:
        """
        Move a job from its current status bucket to a new one.
        Uses the encapsulated setter so the change is logged automatically.
        """
        old_bucket = self.jobs_by_status.get(job.get_status(), [])
        if job in old_bucket:
            old_bucket.remove(job)
        job.set_status(new_status)
        self.jobs_by_status[new_status].append(job)
