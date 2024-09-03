import requests
from abc import ABC, abstractmethod

class BaseAPIHandler(ABC):
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()

    def make_request(self, endpoint, method='GET', params=None, data=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        try:
            response = self.session.request(method, url, headers=headers, params=params, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error making request to {url}: {e}")
            return None

    @abstractmethod
    def get_shipping_cost(self, origin, destination, weight):
        pass

    @abstractmethod
    def parse_response(self, response):
        pass

    def close_session(self):
        self.session.close()