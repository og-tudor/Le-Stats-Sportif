import unittest
from app import webserver
import json
import time
import requests

class TestServer(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_states_mean_request(self):
        sender = requests.post(f"http://127.0.0.1:5000/api/states_mean", json={"question": "Percent of adults aged 18 years and older who have an overweight classification"})
        # Check if the response is correct
        self.assertEqual(sender.status_code, 200)
        received = requests.get(f"http://127.0.0.1:5000/api/get_results/1")

        response_data = sender.json()
        self.assertIn("job_id", response_data)
        # Check if the job_id is an integer
        self.assertIsInstance(response_data["job_id"], int)
        # assert the response is equal to 32.76268656716418
        self.assertEqual(received.json()["data"]["Missouri"], 32.76268656716418)
        
    def test_state_mean_request(self):
        response = requests.post(f"http://127.0.0.1:5000/api/state_mean", json={"question": "Percent of adults aged 18 years and older who have an overweight classification",
                                                                                "state": "South Carolina"})
        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("job_id", response_data)
        # Check if the job_id is an integer
        self.assertIsInstance(response_data["job_id"], int)
        
    def test_best5_request(self):
        response = requests.post(f"http://127.0.0.1:5000/api/best5", json={"question": "Percent of adults aged 18 years and older who have an overweight classification"})
        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("job_id", response_data)
        # Check if the job_id is an integer
        self.assertIsInstance(response_data["job_id"], int)
        
    def test_worst5_request(self):
        response = requests.post(f"http://127.0.0.1:5000/api/worst5", json={"question": "Percent of adults aged 18 years and older who have an overweight classification"})
        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("job_id", response_data)
        # Check if the job_id is an integer
        self.assertIsInstance(response_data["job_id"], int)
        
    def test_global_mean_request(self):
        response = requests.post(f"http://127.0.0.1:5000/api/global_mean", json={"question": "Percent of adults aged 18 years and older who have an overweight classification"})
        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("job_id", response_data)
        # Check if the job_id is an integer
        self.assertIsInstance(response_data["job_id"], int)
        
    def test_diff_from_mean_request(self):
        response = requests.post(f"http://127.0.0.1:5000/api/diff_from_mean", json={"question": "Percent of adults aged 18 years and older who have an overweight classification"})
        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("job_id", response_data)
        # Check if the job_id is an integer
        self.assertIsInstance(response_data["job_id"], int)
        
    def test_state_diff_from_mean_request(self):
        response = requests.post(f"http://127.0.0.1:5000/api/state_diff_from_mean", json={"question": "Percent of adults aged 18 years and older who have an overweight classification",
                                                                                "state": "South Carolina"})
        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("job_id", response_data)
        # Check if the job_id is an integer
        self.assertIsInstance(response_data["job_id"], int)
        
    def test_mean_by_category_request(self):
        response = requests.post(f"http://127.0.0.1:5000/api/mean_by_category", json={"question": "Percent of adults aged 18 years and older who have an overweight classification"})
        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("job_id", response_data)
        # Check if the job_id is an integer
        self.assertIsInstance(response_data["job_id"], int)
        
    def test_state_mean_by_category_request(self):
        response = requests.post(f"http://127.0.0.1:5000/api/state_mean_by_category", json={"question": "Percent of adults aged 18 years and older who have an overweight classification",
                                                                                "state": "South Carolina"})
        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("job_id", response_data)
        # Check if the job_id is an integer
        self.assertIsInstance(response_data["job_id"], int)
        
    def test_jobs_request(self):
        response = requests.get(f"http://127.0.0.1:5000/api/jobs")
        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIsInstance(response_data["data"], list)
        
    def test_num_jobs_request(self):
        response = requests.get(f"http://127.0.0.1:5000/api/num_jobs")
        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIsInstance(response_data["num_jobs"], int)
        
    def test_get_results_request(self):
        job_id = 1  # Replace with an actual job ID
        response = requests.get(f"http://127.0.0.1:5000/api/get_results/{job_id}")
        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        while response_data['status'] == "running":
            # Sleep for 1 second
            time.sleep(1)
            response = requests.get(f"http://127.0.0.1:5000/api/get_results/{job_id}")
            response_data = response.json()
        
        self.assertIsInstance(response_data["data"], dict)