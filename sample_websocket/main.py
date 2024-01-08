# main.py

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from chat_manager import ChatManager

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
chatgpt_api_url = "http://chatgpt-api-endpoint"  # Replace with your actual ChatGPT API endpoint
chat_manager = ChatManager(chatgpt_api_url)

@app.get("/user", response_class=HTMLResponse)
async def read_user(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
async def read_admin_chatgpt(request: Request):
    return templates.TemplateResponse("admin_gpt.html", {"request": request})

@app.websocket("/ws/user")
async def user_websocket_endpoint(websocket: WebSocket):
    user_client_id = await chat_manager.add_user_client(websocket)
    try:
        while True:
            user_message = await websocket.receive_text()
            await chat_manager.handle_user_message(user_message)
    finally:
        await chat_manager.remove_user_client(user_client_id)

@app.websocket("/ws/admin")
async def admin_chatgpt_websocket_endpoint(websocket: WebSocket):
    # admin_chatgpt_client_id = await chat_manager.add_admin_chatgpt_client(websocket)
    admin_chatgpt_client_id = await chat_manager.add_user_client(websocket)
    try:
        while True:
            admin_chatgpt_message = await websocket.receive_text()
            await chat_manager.handle_admin_chatgpt_response(admin_chatgpt_message)
    finally:
        await chat_manager.remove_admin_chatgpt_client(admin_chatgpt_client_id)
