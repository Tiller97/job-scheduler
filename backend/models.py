"""
models.py
Defines the Job hierarchy (parent + child classes).
Polymorphism: each subclass implements its own execute().
"""


class Job:
    """Parent/base class shared by all job types."""
    def __init__(self, job_id: int, description: str) -> None:
        self.job_id = job_id
        self.description = description
        self.status = "pending"

    def execute(self) -> None:
        """Must be overridden by subclasses."""
        raise NotImplementedError("Each job must implement its own execution logic.")

    def mark_done(self) -> None:
        self.status = "completed"

    def __repr__(self) -> str:
        return f"<Job id={self.job_id} status={self.status} desc='{self.description}'>"


class EmailJob(Job):
    """Child class: sends an email."""
    def __init__(self, job_id: int, recipient: str) -> None:
        super().__init__(job_id, f"Send email to {recipient}")
        self.recipient = recipient

    def execute(self) -> None:
        print(f"Sending email to {self.recipient}...")


class DataProcessingJob(Job):
    """Child class: processes a dataset."""
    def __init__(self, job_id: int, dataset: str) -> None:
        super().__init__(job_id, f"Process dataset {dataset}")
        self.dataset = dataset

    def execute(self) -> None:
        print(f"Processing dataset {self.dataset}...")


class PriorityJob(Job):
    """Child class: a job with priority. Smaller number = higher priority."""
    def __init__(self, job_id: int, description: str, priority: int = 5) -> None:
        super().__init__(job_id, description)
        self.priority = priority

    def execute(self) -> None:
        print(f"[PRIORITY={self.priority}] Running priority job: {self.description}")

    def __lt__(self, other) -> bool:
        """Allow sorting by priority."""
        return self.priority < other.priority
