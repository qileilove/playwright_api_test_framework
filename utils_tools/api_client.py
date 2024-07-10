from playwright.sync_api import sync_playwright
from config.config import Config

class APIClient:
    def __init__(self):
        self.playwright = None
        self.request_context = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.request_context = self.playwright.request.new_context(
            base_url=Config.BASE_URL,
            extra_http_headers={'Authorization': f'Bearer {Config.API_TOKEN}'}
        )
        return self

    def get(self, endpoint):
        response = self.request_context.get(endpoint)
        return self._process_response(response)

    def post(self, endpoint, data):
        response = self.request_context.post(endpoint, json=data)
        return self._process_response(response)

    def put(self, endpoint, data):
        response = self.request_context.put(endpoint, json=data)
        return self._process_response(response)

    def delete(self, endpoint):
        response = self.request_context.delete(endpoint)
        return self._process_response(response)

    def _process_response(self, response):
        if response.status >= 400:
            print(f"Request failed: {response.status} {response.status_text}")
            return {
                'status': response.status,
                'error': response.status_text
            }
        try:
            return {
                'status': response.status,
                'json': response.json()
            }
        except Exception as e:
            print(f"Failed to process response: {e}")
            return {
                'status': response.status,
                'error': str(e)
            }

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.request_context:
            self.request_context.dispose()
        if self.playwright:
            self.playwright.stop()
