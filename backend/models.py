"""
models.py
Defines the Job hierarchy with encapsulated logs.
"""

from datetime import datetime


class Job:
    """Parent/base class shared by all job types."""
    def __init__(self, job_id: int, description: str) -> None:
        self.job_id = job_id
        self.description = description
        # Private attributes (single underscore = "please don't touch directly")
        self._status = "pending"
        self._logs = []
        self._add_log(f"Job created: {description}")

    # ----- Public methods to access private data (Encapsulation) -----
    def get_status(self) -> str:
        return self._status

    def set_status(self, new_status: str) -> None:
        old = self._status
        self._status = new_status
        self._add_log(f"Status changed: {old} -> {new_status}")

    def get_logs(self) -> list:
        # Return a copy so external code can't mutate internal list
        return list(self._logs)

    def _add_log(self, message: str) -> None:
        """Internal helper to append a timestamped log entry."""
        ts = datetime.now().strftime("%H:%M:%S")
        self._logs.append(f"[{ts}] {message}")

    # ----- Backward compatibility -----
    @property
    def status(self) -> str:
        """Allow `job.status` for read-only access (compatibility)."""
        return self._status

    def execute(self) -> None:
        raise NotImplementedError("Each job must implement its own execution logic.")

    def mark_done(self) -> None:
        self.set_status("completed")

    def __repr__(self) -> str:
        return f"<Job id={self.job_id} status={self._status} desc='{self.description}'>"


class EmailJob(Job):
    """Child class: sends an email."""
    def __init__(self, job_id: int, recipient: str) -> None:
        super().__init__(job_id, f"Send email to {recipient}")
        self.recipient = recipient

    def execute(self) -> None:
        self._add_log(f"Executing EmailJob to {self.recipient}")
        print(f"Sending email to {self.recipient}...")


class DataProcessingJob(Job):
    """Child class: processes a dataset."""
    def __init__(self, job_id: int, dataset: str) -> None:
        super().__init__(job_id, f"Process dataset {dataset}")
        self.dataset = dataset

    def execute(self) -> None:
        self._add_log(f"Executing DataProcessingJob on {self.dataset}")
        print(f"Processing dataset {self.dataset}...")


class PriorityJob(Job):
    """Child class: a job with priority. Smaller number = higher priority."""
    def __init__(self, job_id: int, description: str, priority: int = 5) -> None:
        super().__init__(job_id, description)
        self.priority = priority
        self._add_log(f"Priority set to {priority}")

    def execute(self) -> None:
        self._add_log(f"Executing PriorityJob (priority={self.priority})")
        print(f"[PRIORITY={self.priority}] Running priority job: {self.description}")

    def __lt__(self, other) -> bool:
        return self.priority < other.priority
