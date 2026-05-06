"""
executor.py
Runs jobs concurrently using threads to simulate a real scheduler.

Features:
- Each job runs in its own thread (concurrency).
- Random delay simulates real work (1-3 seconds).
- Random failure (~20%) exercises exception handling.
- Lifecycle hooks job.start() and job.end() are always called.
"""

import threading
import time
import random
from datetime import datetime
from typing import List
from errors import JobExecutionError
from models import Job


class Executor:
    """Runs a list of jobs concurrently and updates statuses via TaskManager."""

    def __init__(self, jobs: List[Job], manager) -> None:
        self.jobs = jobs
        self.manager = manager

    def _ts(self) -> str:
        """Return current time as a short string for log output."""
        return datetime.now().strftime("%H:%M:%S")

    def run_job(self, job: Job) -> None:
        """Execute a single job with simulated delay and possible failure."""
        # Lifecycle: record start time before doing anything
        job.start()
        try:
            print(f"[{self._ts()}] Executing job {job.job_id} ({job.description})...")
            time.sleep(random.uniform(1, 3))

            # ~20% chance of simulated transient failure
            if random.random() < 0.2:
                raise JobExecutionError(job.job_id)

            job.execute()
            self.manager.update_status(job, "completed")
            print(f"[{self._ts()}] Completed job {job.job_id}.")
        except JobExecutionError as e:
            self.manager.update_status(job, "failed")
            print(f"[{self._ts()}] Error in job {e.job_id}: {e}")
        finally:
            # Lifecycle: always record end time, success or failure
            job.end()

    def run(self) -> None:
        """Start one thread per job and wait for all of them to finish."""
        threads: List[threading.Thread] = []
        for job in self.jobs:
            t = threading.Thread(target=self.run_job, args=(job,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
