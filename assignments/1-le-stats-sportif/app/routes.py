"""
Main file for defining the routes of the webserver.
"""
from flask import request, jsonify
from app import webserver
from app.task_runner import Task, statuses, jobs_list
from threading import Lock

lock = Lock()

thread_pool = webserver.tasks_runner

def increment_job_id():
    """Function to increment the job_id."""
    with lock:
        webserver.job_counter += 1
        return webserver.job_counter

def find_task_in_queue(job_id: str):
    """Function to find a task in the queue based on the job_id."""
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
    """Function to handle POST requests to the '/api/post_endpoint' endpoint."""
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    # Method Not Allowed
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs():
    """Function to handle GET requests to the '/api/num_jobs' endpoint."""
    nr_jobs = thread_pool.get_nr_tasks()
    webserver.logger.info(f"Number of jobs are {nr_jobs}")
    return jsonify({'status': 'done', 'num_jobs': nr_jobs})

@webserver.route('/api/jobs', methods=['GET'])
def jobs():
    """Function to handle GET requests to the '/api/jobs' endpoint."""
    jobs_aux = []
    tasks = thread_pool.get_all_tasks()
    for task in tasks:
        jobs_aux.append({task.job_id: task.status})
    webserver.logger.info(f"Jobs are {jobs_aux}")
    return jsonify({'status': 'done', 'data': jobs_aux})

# returns a list of all the jobs completed
@webserver.route('/api/results', methods=['GET'])
def results():
    """Function to handle GET requests to the '/api/results' endpoint."""
    jobs_aux = []
    tasks = thread_pool.get_all_results()
    for task in tasks:
        jobs_aux.append({task.job_id: task.status})
    webserver.logger.info(f"Results are {jobs_aux}")
    return jsonify({'status': 'done', 'data': jobs_aux})

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """Function to handle GET requests to the '/api/get_results/<job_id>' endpoint."""
    print(f"JobID is {job_id}")
    print(type(job_id))
    if int(job_id) > webserver.job_counter:
        return jsonify({"status": "error", "reason": "Invalid job_id"})
    # get the task from the queue
    # task = find_task_in_queue(job_id)
    task = thread_pool.find_tasks(job_id)
    # if the task is not found
    if task is None:
        return jsonify({"status": "error", "reason": "Task not found"})
    if task.status == statuses[2]:
        return jsonify({"status": "error", "reason": "Error in task"})

    if task.status == statuses[1]:
        return jsonify({"status": "running"})

    # if the task is done
    if task.status == statuses[0]:
        data = task.result
        # log the data
        webserver.logger.info(f"Data for job_id {job_id} is {task.result}")
        return jsonify({"status": "done", "data": data})
    
    return jsonify({'status': 'error', 'reason': 'Unknown error'})

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """Function to handle POST requests to the '/api/states_mean' endpoint."""
    # Get request data
    request_q = request.json['question']
    print(f"Got request {request_q}")
    # creating a Task object
    job = Task(webserver.job_counter, request_q, jobs_list[0], None)
    # incrementing the job counter
    webserver.job_counter = increment_job_id()
    # adding the job to the queue
    # q_jobs.put(job)
    thread_pool.add_task(job)
    webserver.logger.info(f"Job {job.job_id} added to the queue --- states_mean_request")
    # returning the job id
    return jsonify({'job_id': job.job_id})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """Function to handle POST requests to the '/api/state_mean' endpoint."""
    # Get request data
    request_q = request.json['question']
    state = request.json['state']
    print(f"Got request {request_q}")
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    job = Task(webserver.job_counter, request_q, jobs_list[1], state)
    webserver.job_counter = increment_job_id()
    thread_pool.add_task(job)
    webserver.logger.info(f"Job {job.job_id} added to the queue --- state_mean_request")
    return jsonify({"job_id": job.job_id})

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """Function to handle POST requests to the '/api/best5' endpoint."""
    request_q = request.json['question']
    print(f"Got request {request_q}")
    job = Task(webserver.job_counter, request_q, jobs_list[2], None)
    webserver.job_counter = increment_job_id()
    thread_pool.add_task(job)
    webserver.logger.info(f"Job {job.job_id} added to the queue --- best5_request")
    return jsonify({"job_id": job.job_id})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """Function to handle POST requests to the '/api/worst5' endpoint."""
    request_q = request.json['question']
    print(f"Got request {request_q}")
    job = Task(webserver.job_counter, request_q, jobs_list[3], None)
    webserver.job_counter = increment_job_id()
    thread_pool.add_task(job)
    webserver.logger.info(f"Job {job.job_id} added to the queue --- worst5_request")
    return jsonify({"job_id": job.job_id})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """Function to handle POST requests to the '/api/global_mean' endpoint."""
    request_q = request.json['question']
    print(f"Got request {request_q}")
    job = Task(webserver.job_counter, request_q, jobs_list[4], None)
    webserver.job_counter = increment_job_id()
    thread_pool.add_task(job)
    webserver.logger.info(f"Job {job.job_id} added to the queue --- global_mean_request")
    return jsonify({"job_id": job.job_id})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """Function to handle POST requests to the '/api/diff_from_mean' endpoint."""
    request_q = request.json['question']
    print(f"Got request {request_q}")
    job = Task(webserver.job_counter, request_q, jobs_list[5], None)
    webserver.job_counter = increment_job_id()
    thread_pool.add_task(job)
    webserver.logger.info(f"Job {job.job_id} added to the queue --- diff_from_mean_request")
    return jsonify({"job_id": job.job_id})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """Function to handle POST requests to the '/api/state_diff_from_mean' endpoint."""
    request_q = request.json['question']
    state = request.json['state']
    print(f"Got request {request_q}")
    job = Task(webserver.job_counter, request_q, jobs_list[6], state)
    webserver.job_counter = increment_job_id()
    thread_pool.add_task(job)
    webserver.logger.info(f"Job {job.job_id} added to the queue --- state_diff_from_mean_request")
    return jsonify({"job_id": job.job_id})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """Function to handle POST requests to the '/api/mean_by_category' endpoint."""
    request_q = request.json['question']
    print(f"Got request {request_q}")
    job = Task(webserver.job_counter, request_q, jobs_list[7], None)
    webserver.job_counter = increment_job_id()
    thread_pool.add_task(job)
    webserver.logger.info(f"Job {job.job_id} added to the queue --- mean_by_category_request")
    return jsonify({"job_id": job.job_id})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """Function to handle POST requests to the '/api/state_mean_by_category' endpoint."""
    request_q = request.json['question']
    state = request.json['state']
    print(f"Got request {request_q}")
    job = Task(webserver.job_counter, request_q, jobs_list[8], state)
    webserver.job_counter = increment_job_id()
    thread_pool.add_task(job)
    webserver.logger.info(f"Job {job.job_id} added to the queue --- state_mean_by_category_request")
    return jsonify({"job_id": job.job_id})

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    """Function to handle GET requests to the '/' and '/index' endpoints."""
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    """Function to get all defined routes in the webserver."""
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
