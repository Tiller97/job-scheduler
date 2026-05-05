"""
factory.py
Factory pattern for creating Job objects from configuration data.
Hides the concrete class names behind a single create() method.
"""

from models import EmailJob, DataProcessingJob, PriorityJob, Job


class JobFactory:
    """
    Creates Job instances from a 'type' string + keyword args.
    Adding a new Job type only requires registering it here —
    callers (app.py, REST API, etc.) don't need to change.
    """

    # Map of type-string -> concrete class
    _registry = {
        "email": EmailJob,
        "data": DataProcessingJob,
        "priority": PriorityJob,
        
    }

    @classmethod
    def create(cls, job_type: str, **kwargs) -> Job:
        """
        Create a Job from a type name and keyword arguments.
        Example:
            JobFactory.create("email", job_id=1, recipient="user@example.com")
        """
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
        """
        Register a new job type at runtime.
        Lets you extend the factory without modifying its code.
        """
        cls._registry[job_type.lower()] = job_class

    @classmethod
    def available_types(cls) -> list:
        return list(cls._registry.keys())
