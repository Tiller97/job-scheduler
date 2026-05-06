"""
errors.py
Custom exception classes for job execution failures.

Using a custom exception (instead of generic Exception) makes it easy
to catch job-related errors specifically, without accidentally swallowing
unrelated bugs.
"""


class JobExecutionError(Exception):
    """Raised when a job fails to execute properly."""

    def __init__(self, job_id, message: str = "Job execution failed") -> None:
        self.job_id = job_id
        super().__init__(message)
