from queue import Queue
from threading import Thread, Event
import time
import os


# done, running, error
statuses = ['done', 'running', 'error']
jobs_list = ['states_mean', 'state_mean', 'best5', 'worst5', 'get_results', 'jobs', 'num_jobs']
# w_data_store = webserver.data_ingestor.data_store

class ThreadPool:
    def __init__(self, q_jobs : Queue, data_ingestor):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task


        # self.nr_threads = int(os.getenv('TP_NUM_OF_THREADS', os.cpu_count()))
        self.nr_threads = 2
        self.threads = []
        self.q_jobs = q_jobs
        self.data_ingestor = data_ingestor
        self.q_results = Queue()

        # for _ in range(self.nr_threads):
        #     thread = TaskRunner(self.q_jobs)
        #     thread.start()
        #     self.threads.append(thread)
        for i in range(self.nr_threads):
            thread = TaskRunner(i, self.q_jobs, self.data_ingestor, self.q_results)
            thread.start()
            self.threads.append(thread)

    def add_task(self, task):
        self.q_jobs.put(task)
    
    def get_last_task(self):
        return self.q_jobs.get()
    
    def get_all_tasks(self):
        return list(self.q_jobs.queue)
    
    def find_tasks(self, job_id: str):
        for task in self.q_jobs.queue:
            print(task.job_id)
            print(type(task.job_id))
            if task.job_id == int(job_id):
                return task
        for task in self.q_results.queue:
            if task.job_id == int(job_id):
                return task
                
        return None
    
    def get_nr_tasks(self):
        return self.q_jobs.qsize()
    
    # TODO: Implement graceful shutdown
    def shutdown(self):
        for thread in self.threads:
            thread.graceful_shutdown()
            thread.join()

        pass

class Task:
    def __init__(self, job_id, status, request_question, job_type, working_data):
        self.job_id = job_id
        self.status = status
        self.request_question = request_question
        self.job_type = job_type
        self.working_data = working_data

    def run(self, thread_id, data_ingestor):
        # TODO
        data = data_ingestor.data_store.data[self.request_question]
        header = data_ingestor.data_store.header
        print(f"--- Running task {self.job_id} from Thread {thread_id} ---")
        if self.job_type == 'states_mean':
            answer = []
            for state in data:
                rows = data[state]
                total = 0
                nr_entries = 0
                for row in rows:
                    # check if the data is empty
                    if row[header.index('Data_Value')] == '':
                        continue
                    total += float(row[header.index('Data_Value')])
                    nr_entries += 1
                    # print("state: ", row[header.index('LocationDesc')], "data: ", row[header.index('Data_Value')])
                mean = total / nr_entries
                answer.append({'state': state, 'mean': mean})
        
        self.data = answer
                
        pass

class TaskRunner(Thread):
    def __init__(self, thread_id, q_jobs : Queue, data_ingestor, q_results : Queue):
        # TODO: init necessary data structures
        super().__init__()
        self.q_jobs = q_jobs
        self.thread_id = thread_id
        self.data_ingestor = data_ingestor
        self.q_results = q_results
        # pass

    def run(self):
        while True:
            # TODO
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            while True:
                task = self.q_jobs.get()
             
                if task is None:
                    break
                task.run(self.thread_id, self.data_ingestor)
                # modify status to DONE
                task.status = statuses[0]
                self.q_results.put(task)
                self.q_jobs.task_done()
                pass
            pass
