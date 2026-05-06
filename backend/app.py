"""
app.py
Entry point: builds sample jobs, executes them concurrently, and prints
a status summary, per-job logs, and a timing summary.
"""

from models import PriorityJob
from factory import JobFactory
from task_manager import TaskManager
from executor import Executor


def build_jobs():
    """
    Build sample jobs from a config-style list. This simulates loading
    job definitions from an API, database, or YAML config file.
    """
    job_configs = [
        {"type": "email",    "job_id": 1, "recipient": "user@example.com"},
        {"type": "data",     "job_id": 2, "dataset": "dataset_A"},
        {"type": "priority", "job_id": 3, "description": "Send urgent system alert", "priority": 1},
        {"type": "priority", "job_id": 4, "description": "Backup database",          "priority": 8},
        {"type": "priority", "job_id": 5, "description": "Send daily newsletter",    "priority": 5},
    ]

    # Build jobs through the factory; we never import concrete Job classes here.
    jobs = [JobFactory.create(cfg.pop("type"), **cfg) for cfg in job_configs]

    # Place PriorityJobs in priority order before any non-priority jobs.
    priority_jobs = [j for j in jobs if isinstance(j, PriorityJob)]
    other_jobs = [j for j in jobs if not isinstance(j, PriorityJob)]
    priority_jobs.sort()
    return priority_jobs + other_jobs


if __name__ == "__main__":
    jobs = build_jobs()

    # Register all jobs in the manager (all start as 'pending').
    manager = TaskManager()
    for job in jobs:
        manager.add_job(job)

    # Pass manager into the executor so statuses are kept in sync.
    Executor(jobs, manager).run()

    # ----- Status summary -----
    print("\n=== SUMMARY ===")
    print(f"Pending:   {len(manager.get_jobs_by_status('pending'))}")
    print(f"Completed: {len(manager.get_jobs_by_status('completed'))}")
    print(f"Failed:    {len(manager.get_jobs_by_status('failed'))}")

    # ----- Per-job logs (Encapsulation: read via get_logs()) -----
    print("\n=== JOB LOGS ===")
    for job in jobs:
        print(f"\n-- Job {job.job_id} ({job.description}) --")
        for log in job.get_logs():
            print(f"  {log}")

    # ----- Timing summary (Lifecycle tracking) -----
    print("\n=== TIMING SUMMARY ===")
    durations = [(j.job_id, j.description, j.get_duration()) for j in jobs]
    # Sort from slowest to fastest
    durations.sort(key=lambda x: x[2], reverse=True)
    for job_id, desc, duration in durations:
        # Visual bar: one block per 0.1 second
        bar = "█" * int(duration * 10)
        print(f"  Job {job_id}: {duration:.3f}s  {bar} ({desc})")

    total = sum(d for _, _, d in durations)
    avg = total / len(durations) if durations else 0
    print(f"\n  Total CPU time:    {total:.3f}s")
    print(f"  Average duration:  {avg:.3f}s")
    print(f"  Slowest job:       Job {durations[0][0]} ({durations[0][2]:.3f}s)")
