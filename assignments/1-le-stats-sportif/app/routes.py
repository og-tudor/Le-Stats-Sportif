from app import webserver
from flask import request, jsonify
from app.task_runner import Task, statuses, jobs_list

import os
import json

thread_pool = webserver.tasks_runner

def find_task_in_queue(job_id: str):
    # print all items in the queue
    for task in thread_pool.get_all_tasks():
        print(task.job_id)
        print(type(task.job_id))
        if task.job_id == int(job_id):
            return task
    return None

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs():
    nr_jobs = thread_pool.get_nr_tasks()
    return jsonify({'status': 'done', 'num_jobs': nr_jobs})

@webserver.route('/api/jobs', methods=['GET'])
def jobs():
    jobs_aux = []
    tasks = thread_pool.get_all_tasks()
    for task in tasks:
        jobs_aux.append({task.job_id: task.status})
    return jsonify({'status': 'done', 'data': jobs_aux})

# returns a list of all the jobs completed
@webserver.route('/api/results', methods=['GET'])
def results():
    jobs_aux = []
    tasks = thread_pool.get_all_results()
    for task in tasks:
        jobs_aux.append({task.job_id: task.status})
    return jsonify({'status': 'done', 'data': jobs_aux})

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    print(f"JobID is {job_id}")
    print(type(job_id))
    # TODO Mofify reason message
    if int(job_id) > webserver.job_counter:
        return jsonify({"status": "error", "reason": "Invalid job_id"})
    # get the task from the queue
    # task = find_task_in_queue(job_id)
    task = thread_pool.find_tasks(job_id)
    # if the task is not found
    if task == None:
        return jsonify({"status": "error", "reason": "Task not found"})
    if task.status == statuses[2]:
        return jsonify({"status": "error", "reason": "Error in task"})
    
    if task.status == statuses[1]:
       return jsonify({"status": "running"})
    
    # if the task is done
    if task.status == statuses[0]:
        data = task.result
        return jsonify({"status": "done", "data": data})

    # Check if job_id is done and return the result
    #    res = res_for(job_id)
    #    return jsonify({
    #        'status': 'done',
    #        'data': res
    #    })

    # If not, return running status
    return jsonify({'status': 'NotImplemented'})

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    # Get request data
    request_q = request.json['question']
    print(f"Got request {request_q}")
    # creating a Task object
    job = Task(webserver.job_counter, request_q, jobs_list[0], None)
    # incrementing the job counter
    webserver.job_counter += 1
    # adding the job to the queue
    # q_jobs.put(job)
    thread_pool.add_task(job)
    # returning the job id
    return jsonify({'job_id': job.job_id})
    # return jsonify({"status": "NotImplemented"})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    # TODO
    # Get request data
    request_q = request.json['question']
    state = request.json['state']
    print(f"Got request {request_q}")
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    job = Task(webserver.job_counter, request_q, jobs_list[1], state)
    webserver.job_counter += 1
    thread_pool.add_task(job)
    return jsonify({"job_id": job.job_id})

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    request_q = request.json['question']
    print(f"Got request {request_q}")
    job = Task(webserver.job_counter, request_q, jobs_list[2], None)
    webserver.job_counter += 1
    thread_pool.add_task(job)
    return jsonify({"job_id": job.job_id})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    request_q = request.json['question']
    print(f"Got request {request_q}")
    job = Task(webserver.job_counter, request_q, jobs_list[3], None)
    webserver.job_counter += 1
    thread_pool.add_task(job)
    return jsonify({"job_id": job.job_id})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    request_q = request.json['question']
    print(f"Got request {request_q}")
    job = Task(webserver.job_counter, request_q, jobs_list[4], None)
    webserver.job_counter += 1
    thread_pool.add_task(job)
    return jsonify({"job_id": job.job_id})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    request_q = request.json['question']
    print(f"Got request {request_q}")
    job = Task(webserver.job_counter, request_q, jobs_list[5], None)
    webserver.job_counter += 1
    thread_pool.add_task(job)
    return jsonify({"job_id": job.job_id})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    request_q = request.json['question']
    state = request.json['state']
    print(f"Got request {request_q}")
    job = Task(webserver.job_counter, request_q, jobs_list[6], state)
    webserver.job_counter += 1
    thread_pool.add_task(job)
    return jsonify({"job_id": job.job_id})

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
