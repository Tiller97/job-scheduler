"""
models.py
Defines the Job class hierarchy with encapsulated logs and lifecycle timing.

OOP concepts demonstrated:
- Inheritance: Job (base) -> EmailJob, DataProcessingJob, PriorityJob
- Polymorphism: each subclass implements its own execute()
- Encapsulation: _status, _logs, _start_time, _end_time are private
- Lifecycle methods: start(), end(), get_duration()
"""

from datetime import datetime


class Job:
    """Base class shared by all job types."""

    def __init__(self, job_id: int, description: str) -> None:
        self.job_id = job_id
        self.description = description
        # Encapsulated state
        self._status = "pending"
        self._logs = []
        # Lifecycle timestamps
        self._start_time = None
        self._end_time = None
        self._add_log(f"Job created: {description}")

    # ----- Lifecycle methods -----
    def start(self) -> None:
        """Called by the executor right before execute()."""
        self._start_time = datetime.now()
        self._add_log("Job started")

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
        # Return a copy so external code cannot mutate the internal list
        return list(self._logs)

    def _add_log(self, message: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        self._logs.append(f"[{ts}] {message}")

    @property
    def status(self) -> str:
        """Read-only property for backward compatibility with `job.status`."""
        return self._status

    def execute(self) -> None:
        """Subclasses must override this method."""
        raise NotImplementedError("Each job must implement its own execution logic.")

    def mark_done(self) -> None:
        self.set_status("completed")

    def __repr__(self) -> str:
        return f"<Job id={self.job_id} status={self._status} desc='{self.description}'>"


class EmailJob(Job):
    """Sends an email to a recipient."""

    def __init__(self, job_id: int, recipient: str) -> None:
        super().__init__(job_id, f"Send email to {recipient}")
        self.recipient = recipient

    def execute(self) -> None:
        self._add_log(f"Executing EmailJob to {self.recipient}")
        print(f"Sending email to {self.recipient}...")


class DataProcessingJob(Job):
    """Processes a dataset."""

    def __init__(self, job_id: int, dataset: str) -> None:
        super().__init__(job_id, f"Process dataset {dataset}")
        self.dataset = dataset

    def execute(self) -> None:
        self._add_log(f"Executing DataProcessingJob on {self.dataset}")
        print(f"Processing dataset {self.dataset}...")


class PriorityJob(Job):
    """A job with a priority level. Smaller number = higher priority."""

    def __init__(self, job_id: int, description: str, priority: int = 5) -> None:
        super().__init__(job_id, description)
        self.priority = priority
        self._add_log(f"Priority set to {priority}")

    def execute(self) -> None:
        self._add_log(f"Executing PriorityJob (priority={self.priority})")
        print(f"[PRIORITY={self.priority}] Running priority job: {self.description}")

    def __lt__(self, other) -> bool:
        """Allow sorting by priority (smaller number = higher priority)."""
        return self.priority < other.priority
