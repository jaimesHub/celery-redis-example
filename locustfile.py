from locust import HttpUser, TaskSet, task, between
import random
"""
This defines the behavior of the simulated users for the load test. 
We’ll create a task where each user will send a request to the /process-doc/ endpoint with a document ID.
"""

class UserBehavior(TaskSet):
    @task
    def process_doc(self):
        # Example document IDs, you could randomize or select one as needed
        doc_ids = ["doc_1", "doc_2", "doc_3", "doc_4"]
        
        # Randomly select a document ID
        doc_id = random.choice(doc_ids)

        # Send POST request to /process-doc/ endpoint
        with self.client.post("/process-doc/", json={"doc_id": doc_id}, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to process document {doc_id}: {response.status_code}")

    @task
    def get_task_status(self):
        # Example task IDs, you could randomize or select one as needed
        task_ids = ["task_1", "task_2", "task_3", "task_4"]

        # retrieve the task id from redis and celery
        
        
        # Randomly select a task ID
        task_id = random.choice(task_ids)

        # Send GET request to /task-status/{task_id} endpoint
        with self.client.get(f"/task-status/{task_id}", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to get status for task {task_id}: {response.status_code}")

class WebsiteUser(HttpUser):
    """
    Adds a wait_time to mimic real user behavior, 
    so each simulated user waits 1-3 seconds between requests.
    """
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Users wait between 1-3 seconds between tasks
