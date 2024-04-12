from queue import Queue
from threading import Thread, Event
import time
import os


# done, running, error
statuses = ['done', 'running', 'error']
jobs_list = ['states_mean', 'state_mean', 'best5', 'worst5', 'global_mean', 
             'diff_from_mean', 'state_diff_from_mean', 'mean_by_category', 'state_mean_by_category']
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
    
    def get_all_results(self):
        return list(self.q_results.queue)
    
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
    def __init__(self, job_id, request_question, job_type, state):
        self.job_id = job_id
        self.request_question = request_question
        self.job_type = job_type
        self.state = state
        self.result = None

    def run(self, thread_id, data_ingestor):
        # TODO
        data = data_ingestor.data_store.data[self.request_question]
        header = data_ingestor.data_store.header
        print(f"--- Running task {self.job_id} from Thread {thread_id} ---")
        result = []
        # True if the data is in ascending order
        # False if the data is in descending order
        sorting_order = True
        if self.request_question in data_ingestor.questions_best_is_min:
            sorting_order = False
        
        match self.job_type:
            case 'states_mean':
                result = {}
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
                    if nr_entries != 0:
                        mean = total / nr_entries
                        result[state] = mean

            case 'state_mean':
                result = None
                state = self.state
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
                result = {'state': state, 'mean': mean}

            case 'best5':
                result = {}
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
                    if nr_entries != 0:
                        mean = total / nr_entries
                        result[state] = mean
                # sort the result
                if sorting_order:
                    result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
                else:
                    result = dict(sorted(result.items(), key=lambda item: item[1]))
                result = dict(list(result.items())[:5])

            case 'worst5':
                result = {}
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
                    # check if nr_entries is 0
                    if nr_entries != 0:
                        mean = total / nr_entries
                        # result.append({'state': state, 'mean': mean})
                        result[state] = mean
                # sort the result
                if sorting_order:
                    # result.sort(key=lambda x: x['mean'])
                    result = dict(sorted(result.items(), key=lambda item: item[1]))
                else:
                    # result.sort(key=lambda x: x['mean'], reverse=True)
                    result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
                # result = result[:5]
                result = dict(list(result.items())[:5])

            case 'global_mean':
                result = {}
                total = 0
                nr_entries = 0
                for state in data:
                    rows = data[state]
                    for row in rows:
                        # check if the data is empty
                        if row[header.index('Data_Value')] == '':
                            continue
                        total += float(row[header.index('Data_Value')])
                        nr_entries += 1
                result = {'global_mean': total / nr_entries}
    
        # end task
        self.result = result        

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
