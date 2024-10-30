from locust import HttpUser, between, task, constant_throughput


class WebsiteUser(HttpUser):
    wait_time = constant_throughput(1)
        
    @task
    def index(self):
        self.client.get("/")
        
