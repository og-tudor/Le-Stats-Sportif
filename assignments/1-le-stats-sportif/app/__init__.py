"""
Main module of the server file
"""
from queue import Queue
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
import logging



q_jobs = Queue()
webserver = Flask(__name__)

# webserver.task_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
webserver.tasks_runner = ThreadPool(q_jobs, webserver.data_ingestor)
# webserver.data_ingestor.ingest()

# makes a file test.csv to test if the data is being read correctly
webserver.job_counter = 1
webserver.logger = logging.getLogger(__name__)
logging.basicConfig(filename='myapp.log', level=logging.INFO)
from app import routes