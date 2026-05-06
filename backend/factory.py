"""
factory.py
Factory pattern for creating Job objects from configuration data.
"""

from models import EmailJob, DataProcessingJob, PriorityJob, RetryableJob, Job


class JobFactory:
    _registry = {
        "email": EmailJob,
        "data": DataProcessingJob,
        "priority": PriorityJob,
        "retry": RetryableJob,
    }

    @classmethod
    def create(cls, job_type: str, **kwargs) -> Job:
        job_type = job_type.lower()
        if job_type not in cls._registry:
            raise ValueError(
                f"Unknown job type: '{job_type}'. "
                f"Available types: {list(cls._registry.keys())}"
            )
        job_class = cls._registry[job_type]
        return job_class(**kwargs)

    @classmethod
    def register(cls, job_type: str, job_class) -> None:
        cls._registry[job_type.lower()] = job_class

    @classmethod
    def available_types(cls) -> list:
        return list(cls._registry.keys())
