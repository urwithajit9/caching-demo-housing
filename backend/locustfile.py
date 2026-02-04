from locust import HttpUser, task, between


# class HousingUser(HttpUser):
#     # Wait between 1-2 seconds between requests to mimic real users
#     wait_time = between(1, 2)

#     @task
#     def get_properties(self):
#         self.client.get("/api/properties/")


class NaiveUser(HttpUser):
    """
    Simulates a user hitting the unoptimized endpoint.
    This is the baseline — no cache, no query optimization.
    """

    wait_time = between(1, 2)  # Wait 1-2 seconds between requests

    @task
    def get_properties(self):
        self.client.get("/api/properties/live/naive/", name="Naive (No Cache)")


class CachedUser(HttpUser):
    """
    Simulates a user hitting the cached endpoint.
    First request is a cache miss. Subsequent requests are cache hits.
    """

    wait_time = between(1, 2)

    @task
    def get_properties(self):
        self.client.get("/api/properties/cached/", name="Cached (Redis)")
