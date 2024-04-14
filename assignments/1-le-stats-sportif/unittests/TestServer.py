import unittest
import requests

class TestServer(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_states_mean_request(self):
        sender = requests.post(f"http://127.0.0.1:5000/api/states_mean", json={"question": "Percent of adults aged 18 years and older who have an overweight classification"})
        # Check if the response is correct
        received = requests.get(f"http://127.0.0.1:5000/api/get_results/1")
        response_data = sender.json()
        self.assertEqual(received.json()["data"]["Missouri"], 32.76268656716418)
        
    def test_state_mean_request(self):
        response = requests.post(f"http://127.0.0.1:5000/api/state_mean", json={"question": "Percent of adults aged 18 years and older who have an overweight classification",
                                                                                "state": "South Carolina"})
        # Check if the response is correct
        response_data = response.json()
        received = requests.get(f"http://127.0.0.1:5000/api/get_results/" + str(response_data["job_id"]))
        self.assertEqual(received.json()["data"]["South Carolina"], 33.25909090909091)
        
    def test_best5_request(self):
        response = requests.post(f"http://127.0.0.1:5000/api/best5", json={"question": "Percent of adults aged 18 years and older who have an overweight classification"})
        response_data = response.json()
        received = received = requests.get(f"http://127.0.0.1:5000/api/get_results/" + str(response_data["job_id"]))
        received_data = received.json()["data"]
        expected_data = {'Arkansas': 32.99516129032258, 'District of Columbia': 30.746875, 
                         'Kentucky': 33.071641791044776, 'Missouri': 32.76268656716418, 
                         'Vermont': 33.11818181818182}
        self.assertEqual(received_data, expected_data)
        
    def test_worst5_request(self):
        response = requests.post(f"http://127.0.0.1:5000/api/worst5", json={"question": "Percent of adults aged 18 years and older who have an overweight classification"})
        response_data = response.json()
        received = received = requests.get(f"http://127.0.0.1:5000/api/get_results/" + str(response_data["job_id"]))
        received_data = received.json()["data"]
        expected_data = {'Alaska': 35.902777777777786, 'Montana': 36.17826086956522,
                         'Nevada': 36.358333333333334, 'New Jersey': 36.08059701492537,
                         'Puerto Rico': 36.98636363636363}
        self.assertEqual(received_data, expected_data)

        
    def test_global_mean_request(self):
        response = requests.post(f"http://127.0.0.1:5000/api/global_mean", json={"question": "Percent of adults aged 18 years and older who have an overweight classification"})
        response_data = response.json()
        received = requests.get(f"http://localhost:5000/api/get_results/" + str(response_data["job_id"]))
        self.assertEqual(received.json()["data"]["global_mean"], 34.48276141583355)

        
    def test_diff_from_mean_request(self):
        # check if the data from Ohio is correct
        response = requests.post(f"http://127.0.0.1:5000/api/diff_from_mean", json={"question": "Percent of adults aged 18 years and older who have an overweight classification"})
        response_data = response.json()
        received = requests.get(f"http://localhost:5000/api/get_results/" + str(response_data["job_id"]))
        self.assertEqual(received.json()["data"]["Ohio"], 1.2252271692582184)

        
    def test_state_diff_from_mean_request(self):
        response = requests.post(f"http://127.0.0.1:5000/api/state_diff_from_mean", json={"question": "Percent of adults aged 18 years and older who have an overweight classification",
                                                                                "state": "South Carolina"})
        response_data = response.json()
        received = requests.get(f"http://localhost:5000/api/get_results/" + str(response_data["job_id"]))
        self.assertEqual(received.json()["data"]["South Carolina"], 1.2236705067426428)

        
    def test_mean_by_category_request(self):
        response = requests.post(f"http://127.0.0.1:5000/api/mean_by_category", json={"question": "Percent of adults aged 18 years and older who have an overweight classification"})
        
        
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
        response_data = response.json()
        self.assertIsInstance(response_data["data"], list)
        self.assertEqual(response.status_code, 200)
        # Check if the response is an empty list, because we have not added any jobs yet
        self.assertEqual(response_data["data"], [])
        
    def test_num_jobs_request(self):
        # Compare to 0 because we have not added any jobs yet
        response = requests.get(f"http://127.0.0.1:5000/api/num_jobs")
        self.assertEqual(response.json()["num_jobs"], 0)
        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIsInstance(response_data["num_jobs"], int)

    def test_get_result_invalid_job_id(self):
        response = requests.get(f"http://127.0.0.1:5000/api/get_results/1000")
        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['reason'], 'Invalid job_id')

    def test_get_result_task_done(self):
        # random task
        request = requests.post("http://localhost:5000/api/states_mean", json={"question": "Percent of adults aged 18 years and older who have an overweight classification"})
        response = requests.get("http://127.0.0.1:5000/api/get_results/1")
        data = response.json()
        self.assertEqual(data['status'], 'done')