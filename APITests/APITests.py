import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PetAPI:
    BASE_URL = 'https://petstore.swagger.io/v2/pet'

    def log_response(self, action, response):
        logging.info(f"{action}:")
        logging.info("Status code: %s", response.status_code)
        try:
            logging.info("Response body: %s", response.json())
        except ValueError:
            logging.info("Response body: %s", response.text)

    def add_pet(self, data):
        response = requests.post(self.BASE_URL, json=data)
        self.log_response("POST /pet", response)
        return response

    def get_pet(self, pet_id):
        response = requests.get(f"{self.BASE_URL}/{pet_id}")
        self.log_response("GET /pet/{petID}", response)
        return response

    def update_pet(self, data):
        response = requests.put(self.BASE_URL, json=data)
        self.log_response("PUT /pet", response)
        return response

    def delete_pet(self, pet_id):
        response = requests.delete(f"{self.BASE_URL}/{pet_id}")
        self.log_response("DELETE /pet/{petID}", response)
        return response


class TestPetAPI:
    def __init__(self):
        self.api = PetAPI()
        self.pet_id = None

    def run_test(self, test_func):
        """Run a test function and handle assertion errors."""
        try:
            test_func()
        except AssertionError as e:
            logging.error(f"Test {test_func.__name__} failed: {e}")

    def test_post_pet_positive(self):
        data = {
            "id": 0,
            "name": "dog1",
            "category": {"id": 1, "name": "myDogs"},
            "photoUrls": ["http://test.com/test.jpg"],
            "tags": [{"id": 1, "name": "tagName"}],
            "status": "available"
        }
        response = self.api.add_pet(data)
        assert response.status_code == 200, "Expected status code 200"
        self.pet_id = response.json().get("id")
        logging.info("Created pet ID: %s", self.pet_id)

    def test_post_pet_negative(self):
        data = {
            "name": "dog1",
            "category": {"id": 1, "name": "myDogs"},
            "photoUrls": ["http://test.com/test.jpg"],
            "tags": [{"id": 1, "name": "tagName"}],
            "status": "available"
        }
        response = self.api.add_pet(data)
        assert response.status_code == 400, "Expected status code 400 for invalid data"

    def test_get_pet_positive(self):
        assert self.pet_id is not None, "Pet ID should not be None"
        response = self.api.get_pet(self.pet_id)
        assert response.status_code == 200, "Expected status code 200"
        assert response.json().get("id") == self.pet_id, "Returned pet ID does not match"

    def test_get_pet_negative(self):
        response = self.api.get_pet(0)
        assert response.status_code == 404, "Expected status code 404 for non-existent pet ID"

    def test_put_pet_positive(self):
        assert self.pet_id is not None, "Pet ID should not be None"
        data = {
            "id": self.pet_id,
            "name": "updated dog1",
            "category": {"id": 1, "name": "myDogs"},
            "photoUrls": ["http://test.com/test.jpg"],
            "tags": [{"id": 1, "name": "tagName"}],
            "status": "available"
        }
        response = self.api.update_pet(data)
        assert response.status_code == 200, "Expected status code 200"

    def test_put_pet_negative(self):
        data = {
            "id": 0,
            "name": "updated dog1",
            "category": {"id": 1, "name": "myDogs"},
            "photoUrls": ["http://test.com/test.jpg"],
            "tags": [{"id": 1, "name": "tagName"}],
            "status": "available"
        }
        response = self.api.update_pet(data)
        assert response.status_code == 400, "Expected status code 400 for invalid pet ID"

    def test_delete_pet_positive(self):
        assert self.pet_id is not None, "Pet ID should not be None"
        response = self.api.delete_pet(self.pet_id)
        assert response.status_code == 200, "Expected status code 200"

    def test_delete_pet_negative(self):
        response = self.api.delete_pet(0)
        assert response.status_code == 404, "Expected status code 404 for non-existent pet ID"


if __name__ == "__main__":
    tester = TestPetAPI()
    tester.run_test(tester.test_post_pet_positive)
    tester.run_test(tester.test_post_pet_negative)
    tester.run_test(tester.test_get_pet_positive)
    tester.run_test(tester.test_get_pet_negative)
    tester.run_test(tester.test_put_pet_positive)
    tester.run_test(tester.test_put_pet_negative)
    tester.run_test(tester.test_delete_pet_positive)
    tester.run_test(tester.test_delete_pet_negative)
