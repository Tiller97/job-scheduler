"""
app.py
Build a few jobs, register them, run them, print a summary.
"""


from models import PriorityJob
from factory import JobFactory

from task_manager import TaskManager

from executor import Executor


def build_jobs():
    """建立範例 jobs(模擬從外部 config 讀取資料)"""
    # 模擬從 API 或資料庫讀進來的 job 設定
    job_configs = [
        {"type": "email",    "job_id": 1, "recipient": "user@example.com"},
        {"type": "data",     "job_id": 2, "dataset": "dataset_A"},
        {"type": "priority", "job_id": 3, "description": "Send urgent system alert", "priority": 1},
        {"type": "priority", "job_id": 4, "description": "Backup database",           "priority": 8},
        {"type": "priority", "job_id": 5, "description": "Send daily newsletter",     "priority": 5},
    ]

    # 用 Factory 建立 jobs - 我們不用 import 任何具體的 Job class
    jobs = [JobFactory.create(cfg.pop("type"), **cfg) for cfg in job_configs]

    # 把 PriorityJob 排序到前面
    priority_jobs = [j for j in jobs if isinstance(j, PriorityJob)]
    other_jobs = [j for j in jobs if not isinstance(j, PriorityJob)]
    priority_jobs.sort()

    return priority_jobs + other_jobs


if __name__ == "__main__":

    jobs = build_jobs()


    manager = TaskManager()

    for job in jobs:

        manager.add_job(job)  # all start as 'pending'


    # FIX (app.py): pass 'manager' to Executor so it can update statuses.
    # Previously Executor(jobs).run() had no manager reference — statuses never changed.
    Executor(jobs, manager).run()


    print("\n=== SUMMARY ===")

    print(f"Pending:   {len(manager.get_jobs_by_status('pending'))}")

    print(f"Completed: {len(manager.get_jobs_by_status('completed'))}")

    # FIX (app.py): added 'failed' count to summary so failures are visible.
    print(f"Failed:    {len(manager.get_jobs_by_status('failed'))}")

    print("\n=== JOB LOGS ===")
    for job in jobs:
        print(f"\n-- Job {job.job_id} ({job.description}) --")
        for log in job.get_logs():
            print(f"  {log}")
