# chat_manager.py

from typing import List
from fastapi import WebSocket
import requests

class ChatManager:
    def __init__(self, chatgpt_api_url):
        self.user_clients: List[WebSocket] = []
        # self.admin_chatgpt_clients: List[WebSocket] = []
        self.user_client_counter = 0
        self.admin_chatgpt_client_counter = 0
        self.chatgpt_api_url = chatgpt_api_url
        self.can_admin_chatgpt_respond = False

    async def add_user_client(self, websocket: WebSocket):
        await websocket.accept()
        user_client_id = self.user_client_counter
        self.user_client_counter += 1
        self.user_clients.append((user_client_id, websocket))
        return user_client_id

    async def add_admin_chatgpt_client(self, websocket: WebSocket):
        await websocket.accept()
        admin_chatgpt_client_id = self.admin_chatgpt_client_counter
        self.admin_chatgpt_client_counter += 1
        self.admin_chatgpt_clients.append((admin_chatgpt_client_id, websocket))
        return admin_chatgpt_client_id

    async def remove_user_client(self, user_client_id: int):
        user_client = next((c for c in self.user_clients if c[0] == user_client_id), None)
        if user_client:
            self.user_clients.remove(user_client)
            _, websocket = user_client
            await websocket.close()

    async def remove_admin_chatgpt_client(self, admin_chatgpt_client_id: int):
        admin_chatgpt_client = next((c for c in self.admin_chatgpt_clients if c[0] == admin_chatgpt_client_id), None)
        if admin_chatgpt_client:
            self.admin_chatgpt_clients.remove(admin_chatgpt_client)
            _, websocket = admin_chatgpt_client
            await websocket.close()

    async def broadcast_user_message(self, user_message: str, user:str):
        for client in self.user_clients:
            await client[1].send_text(f"{user}: {user_message}")
            
        self.can_admin_chatgpt_respond = True

    async def broadcast_admin_chatgpt_response(self, admin_chatgpt_response: str):
        for client in self.admin_chatgpt_clients:
            await client[1].send_text(f"Admin/ChatGPT {client[0]}: {admin_chatgpt_response}")
            
        self.can_admin_chatgpt_respond = False

    async def handle_user_message(self, user_message: str):
        await self.broadcast_user_message(user_message,user ="User")


    async def handle_admin_chatgpt_response(self, admin_chatgpt_response: str):
        # await self.broadcast_user_message(admin_chatgpt_response)
        if self.can_admin_chatgpt_respond:
            if admin_chatgpt_response:
                user = "Admin"
                await self.broadcast_user_message(admin_chatgpt_response,user)
            else:
                chatgpt_response = self.call_chatgpt_api(admin_chatgpt_response)
                # await self.broadcast_admin_chatgpt_response(chatgpt_response)
                user = "ChatGPT"
                await self.broadcast_user_message(chatgpt_response,user)
            self.can_admin_chatgpt_respond = False

    def call_chatgpt_api(self, user_message: str) -> str:
        api_endpoint = self.chatgpt_api_url
        # response = requests.post(api_endpoint, json={"user_message": user_message})
        # return response.json().get("chatgpt_response", "ChatGPT: Unable to generate response")
        return f"chatGPT : response - How can I help you?"
