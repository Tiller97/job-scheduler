"""
models.py
Defines the Job hierarchy with encapsulated logs and lifecycle timing.
"""

from datetime import datetime


class Job:
    """Parent/base class shared by all job types."""
    def __init__(self, job_id: int, description: str) -> None:
        self.job_id = job_id
        self.description = description
        # Encapsulated state
        self._status = "pending"
        self._logs = []
        # Lifecycle timestamps (Activity 5)
        self._start_time = None
        self._end_time = None
        self._add_log(f"Job created: {description}")

    # ----- Lifecycle methods (Activity 5) -----
    def start(self) -> None:
        """Called by the executor right before execute()."""
        self._start_time = datetime.now()
        self._add_log(f"Job started")

    def end(self) -> None:
        """Called by the executor right after execute() (success or failure)."""
        self._end_time = datetime.now()
        self._add_log(f"Job ended (duration: {self.get_duration():.3f}s)")

    def get_duration(self) -> float:
        """Return execution duration in seconds. Returns 0 if not finished."""
        if self._start_time is None or self._end_time is None:
            return 0.0
        return (self._end_time - self._start_time).total_seconds()

    def get_start_time(self):
        return self._start_time

    def get_end_time(self):
        return self._end_time

    # ----- Encapsulated status & logs -----
    def get_status(self) -> str:
        return self._status

    def set_status(self, new_status: str) -> None:
        old = self._status
        self._status = new_status
        self._add_log(f"Status changed: {old} -> {new_status}")

    def get_logs(self) -> list:
        return list(self._logs)

    def _add_log(self, message: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        self._logs.append(f"[{ts}] {message}")

    @property
    def status(self) -> str:
        return self._status

    def execute(self) -> None:
        raise NotImplementedError("Each job must implement its own execution logic.")

    def mark_done(self) -> None:
        self.set_status("completed")

    def __repr__(self) -> str:
        return f"<Job id={self.job_id} status={self._status} desc='{self.description}'>"


class EmailJob(Job):
    def __init__(self, job_id: int, recipient: str) -> None:
        super().__init__(job_id, f"Send email to {recipient}")
        self.recipient = recipient

    def execute(self) -> None:
        self._add_log(f"Executing EmailJob to {self.recipient}")
        print(f"Sending email to {self.recipient}...")


class DataProcessingJob(Job):
    def __init__(self, job_id: int, dataset: str) -> None:
        super().__init__(job_id, f"Process dataset {dataset}")
        self.dataset = dataset

    def execute(self) -> None:
        self._add_log(f"Executing DataProcessingJob on {self.dataset}")
        print(f"Processing dataset {self.dataset}...")


class PriorityJob(Job):
    def __init__(self, job_id: int, description: str, priority: int = 5) -> None:
        super().__init__(job_id, description)
        self.priority = priority
        self._add_log(f"Priority set to {priority}")

    def execute(self) -> None:
        self._add_log(f"Executing PriorityJob (priority={self.priority})")
        print(f"[PRIORITY={self.priority}] Running priority job: {self.description}")

    def __lt__(self, other) -> bool:
        return self.priority < other.priority


class RetryableJob(Job):
    """
    A job that wraps another job and retries it on failure.
    Demonstrates resilience patterns common in distributed systems.
    """
    def __init__(self, job_id: int, inner_job: Job, max_retries: int = 3) -> None:
        super().__init__(job_id, f"Retryable wrapper for: {inner_job.description}")
        self.inner_job = inner_job
        self.max_retries = max_retries
        self._attempts = 0
        self._add_log(f"RetryableJob created (max_retries={max_retries})")

    def execute(self) -> None:
        """
        Try inner_job.execute() up to max_retries times.
        Each attempt has a 50% chance of failing (simulated).
        Re-raises the last exception if all attempts fail.
        """
        import random
        last_error = None

        for attempt in range(1, self.max_retries + 1):
            self._attempts = attempt
            self._add_log(f"Attempt {attempt}/{self.max_retries}")
            print(f"  [Retry] Job {self.job_id} attempt {attempt}/{self.max_retries}...")
            try:
                # Simulate transient failure 50% of the time
                if random.random() < 0.5:
                    raise RuntimeError("Simulated transient failure")
                self.inner_job.execute()
                self._add_log(f"Succeeded on attempt {attempt}")
                print(f"  [Retry] Job {self.job_id} succeeded on attempt {attempt} ✓")
                return
            except Exception as e:
                last_error = e
                self._add_log(f"Attempt {attempt} failed: {e}")
                print(f"  [Retry] Job {self.job_id} attempt {attempt} failed: {e}")

        # All attempts exhausted - re-raise so executor marks it as failed
        self._add_log(f"All {self.max_retries} attempts exhausted")
        raise last_error

    def get_attempts(self) -> int:
        return self._attempts
