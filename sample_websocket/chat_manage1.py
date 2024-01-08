
from typing import List
from fastapi import WebSocket
import requests

class ChatManager:
    def __init__(self, chatgpt_api_url):
        self.clients: List[WebSocket] = []
        self.client_counter = 0
        self.chatgpt_api_url = chatgpt_api_url

    async def add_client(self, websocket: WebSocket):
        await websocket.accept()
        client_id = self.client_counter
        self.client_counter += 1
        self.clients.append((client_id, websocket))
        return client_id

    async def remove_client(self, client_id: int):
        client = next((c for c in self.clients if c[0] == client_id), None)
        if client:
            self.clients.remove(client)
            _, websocket = client
            await websocket.close()

    async def broadcast_user_message(self, user_message: str):
        for client in self.clients:
            await client[1].send_text(f"Client {client[0]}: {user_message}")

    async def broadcast_admin_response(self, admin_response: str):
        for client in self.clients:
            await client[1].send_text(f"Admin: {admin_response}")

    async def handle_user_message(self, user_message: str):
        await self.broadcast_user_message(user_message)

        chatgpt_response = self.call_chatgpt_api(user_message)
        await self.broadcast_chatbot_response(chatgpt_response)

    async def handle_admin_response(self, admin_response: str):
        await self.broadcast_admin_response(admin_response)
        
    async def broadcast_chatbot_response(self, chatbot_response: str):
        for client in self.clients:
            await client[1].send_text(chatbot_response)

    def call_chatgpt_api(self, user_message: str) -> str:
        api_endpoint = self.chatgpt_api_url
        # response = requests.post(api_endpoint, json={"user_message": user_message})
        response = "chatGPT : How can I help you?"
        return response #.json().get("chatgpt_response", "ChatGPT: Unable to generate response")
