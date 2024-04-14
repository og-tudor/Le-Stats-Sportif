"""
Main module of the server file
"""
from queue import Queue
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
import logging
import logging.handlers



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
webserver.job_counter = 1
webserver.logger = logging.getLogger(__name__)
webserver.logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler('webserver.log', maxBytes=100000, backupCount=1)
webserver.logger.addHandler(handler)

from app import routes