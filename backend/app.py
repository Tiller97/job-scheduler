"""
app.py
Build a few jobs, register them, run them, print a summary.
"""


from models import EmailJob, DataProcessingJob, PriorityJob

from task_manager import TaskManager

from executor import Executor


def build_jobs():
    """建立範例 jobs(包含不同優先順序)"""
    jobs = [
        EmailJob(1, "user@example.com"),
        DataProcessingJob(2, "dataset_A"),
        PriorityJob(3, "Send urgent system alert", priority=1),    # 最高優先!
        PriorityJob(4, "Backup database", priority=8),              # 低優先
        PriorityJob(5, "Send daily newsletter", priority=5),        # 普通
    ]
    
    # 把 PriorityJob 按 priority 排序,優先級高的(數字小)先處理
    priority_jobs = [j for j in jobs if isinstance(j, PriorityJob)]
    other_jobs = [j for j in jobs if not isinstance(j, PriorityJob)]
    priority_jobs.sort()   # 用我們定義的 __lt__ 來排序
    
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
