from .base_handler import BaseAPIHandler

class FastShipHandler(BaseAPIHandler):
    def __init__(self, api_key):
        super().__init__('https://api.fastship.com', api_key)

    def get_shipping_cost(self, origin, destination, weight):
        endpoint = 'shipping/cost'
        params = {
            'origin': origin,
            'destination': destination,
            'weight': weight
        }
        response = self.make_request(endpoint, params=params)
        return self.parse_response(response)

    def parse_response(self, response):
        if not response:
            return None

        parsed_data = []
        for service in response.get('services', []):
            parsed_data.append({
                'service': service['name'],
                'cost': service['cost'],
                'estimated_days': service['estimated_delivery_time']
            })
        return parsed_data