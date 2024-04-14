"""
Main module of the server file
"""
from queue import Queue
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
import logging
import logging.handlers
import os

q_jobs = Queue()
results_list = []
webserver = Flask(__name__)

# check if there is a results folder, if it isn't create one
if not os.path.exists('results'):
    os.makedirs('results')

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
webserver.tasks_runner = ThreadPool(q_jobs, results_list, webserver.data_ingestor)

webserver.job_counter = 1
# initialize logger
webserver.logger = logging.getLogger(__name__)
webserver.logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler('webserver.log', maxBytes=100000, backupCount=1)
webserver.logger.addHandler(handler)

from app import routes