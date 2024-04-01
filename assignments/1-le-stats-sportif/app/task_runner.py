from queue import Queue
from threading import Thread, Event
import time
import os

# done, running, error
statuses = ['done', 'running', 'error']
jobs_list = ['states_mean', 'state_mean', 'best5', 'worst5', 'get_results', 'jobs', 'num_jobs']
q_jobs = Queue()

class ThreadPool:
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        pass

class Task:
    def __init__(self, job_id, status, data, job_type):
        self.job_id = job_id
        self.status = status
        self.data = data
        self.job_type = job_type

    def run(self):
        pass

class TaskRunner(Thread):
    def __init__(self, q_jobs : Queue):
        # TODO: init necessary data structures
        self.q_jobs = q_jobs
        pass

    def run(self):
        while True:
            # TODO
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            pass
