import pytest
from utils.websocket_client import WebSocketClient

WS_URL = "wss://your-websocket-endpoint.com"

@pytest.fixture(scope="module")
def ws_client():
    client = WebSocketClient(url=WS_URL)
    client.connect()
    yield client
    client.close()

def test_websocket_connection(ws_client):
    ws_client.send_message("Hello, WebSocket!")
    response = ws_client.receive_message()
    assert response == "Expected response from server"

def test_websocket_another_message(ws_client):
    ws_client.send_message("Another message")
    response = ws_client.receive_message()
    assert response == "Expected another response from server"
