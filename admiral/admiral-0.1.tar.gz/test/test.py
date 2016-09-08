from admiral import jobmanagers
import time

cluster = jobmanagers.SLURM_Jobmanager(batch_dir="test", log_dir="test")
jobs = []
for i in range(5):
    job = cluster.make_job("echo 1234; sleep 10", queue="owners")
    job.run()
    print job.job_id
    jobs.append(job)
    time.sleep(3)

print jobmanagers.wait_for_jobs(jobs, progress=True)
