"""
Module for running tasks asynchronously using threads.
"""
from queue import Queue
from threading import Thread
import os

# done, running, error
statuses = ['done', 'running', 'error']
jobs_list = ['states_mean', 'state_mean', 'best5', 'worst5', 'global_mean',
             'diff_from_mean', 'state_diff_from_mean', 'mean_by_category', 'state_mean_by_category']

class ThreadPool:
    """
    Class for managing the thread pool.
    """
    def __init__(self, q_jobs : Queue, data_ingestor):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task


        self.nr_threads = int(os.getenv('TP_NUM_OF_THREADS', os.cpu_count()))
        # self.nr_threads = 2
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
        """ Function to add a task to the queue """
        self.q_jobs.put(task)

    def get_last_task(self):
        """ Function to get the last task from the queue"""
        return self.q_jobs.get()

    def get_all_tasks(self):
        """ Function to get all the tasks from the queue"""
        return list(self.q_jobs.queue)

    def get_all_results(self):
        """ Function to get all the results from the queue"""
        return list(self.q_results.queue)

    def find_tasks(self, job_id: str):
        """ Function to find a task in the queue"""
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
        """ Function to get the number of tasks in the queue"""
        return self.q_jobs.qsize()

    def shutdown(self):
        """ Function to shutdown the thread pool"""
        for thread in self.threads:
            thread.graceful_shutdown()
            thread.join()

class Task:
    """
    Class for running
    """
    def __init__(self, job_id, request_question, job_type, state):
        self.job_id = job_id
        self.request_question = request_question
        self.job_type = job_type
        self.state = state
        self.result = None

    def state_mean_f(self, data, header, state):
        """ Function to calculate the mean of a state"""
        result = {}
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
        else:
            result = None
        return result

    def global_mean_f(self, data, header):
        """ Function to calculate the global mean"""
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
        result['global_mean'] = total / nr_entries
        return result

    def diff_from_mean_f(self, data, header):
        """ Function to calculate the difference from the global mean"""
        global_mean_data = self.global_mean_f(data, header)
        result = {}
        for state in data:
            state_mean_data = self.state_mean_f(data, header, state)
            if state_mean_data is not None:
                result[state] = global_mean_data['global_mean'] - state_mean_data[state]
            else :
                result[state] = float('nan')
        return result

    def state_diff_from_mean_f(self, data, header, state):
        """ Function to calculate the difference from the global mean"""
        result = {}
        global_mean_data = self.global_mean_f(data, header)
        state_mean_data = self.state_mean_f(data, header, state)
        if state_mean_data is not None:
            result[state] = global_mean_data['global_mean'] - state_mean_data[state]
        else:
            result[state] = float('nan')
        return result

    def states_mean_f(self, data, header):
        """ Function to calculate the mean of all the states"""
        result = {}
        for state in data:
            state_mean_data = self.state_mean_f(data, header, state)
            if state_mean_data is not None:
                result[state] = state_mean_data[state]
            else:
                result[state] = float('nan')
        return result
            
    def state_mean_category_f(self, data, header, state):
        """ Function to calculate the mean of a state for each category"""
        result = {}
        category_result = {}
        category_data = {}
        rows = data[state]
        for row in rows:
            category = row[header.index('StratificationCategory1')]
            value_category = row[header.index('Stratification1')]
            key = "(\'" + category + "\'" + ", " + "\'" + value_category + "\')"
            if key not in category_data:
                category_data[key] = []
            category_data[key].append(row)
        for key in category_data:
            total = 0
            nr_entries = 0
            for row in category_data[key]:
                # check if the data is empty
                if row[header.index('Data_Value')] == '':
                    continue
                total += float(row[header.index('Data_Value')])
                nr_entries += 1
            if nr_entries != 0:
                mean = total / nr_entries
                category_result[key] = mean
        # sort category_result in ascending order by key
        category_result = dict(sorted(category_result.items(), key=lambda item: item[0]))
        result[state] = category_result
        return result
        
    def mean_by_category_f(self, data, header):
        result = {}
        category_result = {}
        category_data = {}
        for state in data:
            state_data = self.state_mean_category_f(data, header, state)
            for key in state_data:
                if key not in category_data:
                    category_data[key] = []
                category_data[key].append(state_data[key])
        return category_data            

    def run(self, thread_id, data_ingestor):
        """ Function to run the task and choose the appropriate function to run based on the job"""
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
                result = self.states_mean_f(data, header)
                # result = {}
                # for state in data:
                #     rows = data[state]
                #     total = 0
                #     nr_entries = 0
                #     for row in rows:
                #         # check if the data is empty
                #         if row[header.index('Data_Value')] == '':
                #             continue
                #         total += float(row[header.index('Data_Value')])
                #         nr_entries += 1
                #     if nr_entries != 0:
                #         mean = total / nr_entries
                #         result[state] = mean

            case 'state_mean':
                result = self.state_mean_f(data, header, self.state)

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
                result = self.global_mean_f(data, header)
            # endcase
            case 'diff_from_mean':
                result = self.diff_from_mean_f(data, header)

            case 'state_diff_from_mean':
               result = self.state_diff_from_mean_f(data, header, self.state)

            case 'mean_by_category':
                result = self.mean_by_category_f(data, header)

            case 'state_mean_by_category':
                result = self.state_mean_category_f(data, header, self.state)

        # end task
        self.result = result

class TaskRunner(Thread):
    """
    Class for running
    """
    def __init__(self, thread_id, q_jobs : Queue, data_ingestor, q_results : Queue):
        super().__init__()
        self.q_jobs = q_jobs
        self.thread_id = thread_id
        self.data_ingestor = data_ingestor
        self.q_results = q_results
        # pass

    def run(self):
        """ Function to run the task runner and run the tasks in the queue"""
        while True:
            # TODO stop using busy waiting
            while True:
                task = self.q_jobs.get()

                if task is None:
                    break
                task.run(self.thread_id, self.data_ingestor)
                # modify status to DONE
                task.status = statuses[0]
                self.q_results.put(task)
                self.q_jobs.task_done()