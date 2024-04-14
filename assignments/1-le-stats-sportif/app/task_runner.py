"""
Module for running tasks asynchronously using threads.
"""
from queue import Queue
from threading import Thread
import os
import json

# done, running, error
statuses = ['done', 'running', 'error']
jobs_list = ['states_mean', 'state_mean', 'best5', 'worst5', 'global_mean',
             'diff_from_mean', 'state_diff_from_mean', 'mean_by_category', 'state_mean_by_category']

class ThreadPool:
    """
    Class for managing the thread pool.
    """
    def __init__(self, q_jobs : Queue, results_list, data_ingestor):
        self.nr_threads = int(os.getenv('TP_NUM_OF_THREADS', os.cpu_count()))
        self.threads = []
        self.q_jobs = q_jobs
        self.data_ingestor = data_ingestor
        self.shutdown_event = False
        self.results_list = results_list

        for i in range(self.nr_threads):
            thread = TaskRunner(i, self.q_jobs, self.data_ingestor, self.results_list)
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
        return self.results_list

    def find_tasks(self, job_id: str):
        """ Function to find a task in the job_queue or results_queue by job_id"""
        job = None
        for result in self.results_list:
            if result['job_id'] == int(job_id):
                job = result
                return job
        return job


    def get_nr_tasks(self):
        """ Function to get the number of tasks in the queue"""
        return self.q_jobs.qsize()
    
    def graceful_shutdown(self):
        """ Function to gracefully shutdown the threads"""
        self.shutdown_event = True
        for thread in self.threads:
            thread.shutdown_event = True
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
    
    def best5_f(self, data, header, sorting_order):
        """ Function to calculate the best 5 states"""
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
        return result
    
    def worst5_f(self, data, header, sorting_order):
        """ Function to calculate the worst 5 states"""
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
            for row in data[state]:
                category = row[header.index('StratificationCategory1')]
                value_category = row[header.index('Stratification1')]
                # check if the category is empty and skip the row
                if category == '' or value_category == '':
                    continue
                key = "(\'" + state + "\', \'"+ category + "\'" + ", " + "\'" + value_category + "\')"
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
        result = category_result
        return result    

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

            case 'state_mean':
                result = self.state_mean_f(data, header, self.state)

            case 'best5':
                result = self.best5_f(data, header, sorting_order)

            case 'worst5':
                result = self.worst5_f(data, header, sorting_order)

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
        # write in a results/{job_id}.json file
        with open(f"results/{self.job_id}.json", "w") as file:
            json.dump(result, file)

class TaskRunner(Thread):
    """
    Class for running
    """
    def __init__(self, thread_id, q_jobs : Queue, data_ingestor, results_list):
        super().__init__()
        self.q_jobs = q_jobs
        self.thread_id = thread_id
        self.data_ingestor = data_ingestor
        self.shutdown_event = False
        self.results_list = results_list
        # pass

    def run(self):
        """ Function to run the task runner and run the tasks in the queue"""
        while True:
            try:
                task = self.q_jobs.get(block=True, timeout=1)
            # timeout happened, no task available, queue is empty
            except Exception as e:
                if self.shutdown_event:
                    print(f"Thread {self.thread_id} is shutting down")
                    break
                continue
            # Failsafe in case the task is None (it should never be None, but just in case)
            if task is None:
                continue
            task.run(self.thread_id, self.data_ingestor)
            # modify status to DONE
            task.status = statuses[0]
            self.results_list.append({'job_id': task.job_id, 'status': statuses[0]})
            self.q_jobs.task_done()