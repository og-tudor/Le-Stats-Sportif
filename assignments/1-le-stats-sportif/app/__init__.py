from flask import Flask, request
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from queue import Queue

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

q_jobs = Queue()
webserver = Flask(__name__)

# webserver.task_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
webserver.tasks_runner = ThreadPool(q_jobs, webserver.data_ingestor)
# webserver.data_ingestor.ingest()

# makes a file test.csv to test if the data is being read correctly
# webserver.data_ingestor.test_ingestion(webserver.data_ingestor.questions_best_is_min[1], "Alabama")
webserver.data_ingestor.test_ingestion()
webserver.job_counter = 1

from app import routes
