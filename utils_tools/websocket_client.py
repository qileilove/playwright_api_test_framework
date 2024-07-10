from playwright.sync_api import sync_playwright
from config.config import Config

class WebSocketClient:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        self.websocket = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page()
        return self

    def connect(self):
        self.websocket = self.page.evaluate_handle(f"() => new WebSocket('{Config.WS_URL}')")
        self.page.evaluate("ws => ws.onopen = () => console.log('WebSocket connected');", self.websocket)
        self.page.evaluate("ws => ws.onerror = event => console.error('WebSocket error:', event);", self.websocket)

    def send_message(self, message):
        self.page.evaluate("ws => ws.send(arguments[1])", self.websocket, message)

    def receive_message(self):
        return self.page.evaluate_handle("ws => new Promise(resolve => ws.onmessage = event => resolve(event.data));", self.websocket)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.websocket:
            self.page.evaluate("ws => ws.close()", self.websocket)
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
