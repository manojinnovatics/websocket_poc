
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from chat_manage1 import ChatManager

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
chatgpt_api_url = "http://your-chatgpt-api-endpoint"
chat_manager = ChatManager(chatgpt_api_url)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    client_id = await chat_manager.add_client(websocket)

    try:
        while True:
            message = await websocket.receive_text()

            # Check if the message is from admin or user
            if message.startswith("/admin"):
                admin_response = message[len("/admin"):].strip()
                await chat_manager.handle_admin_response(admin_response)
            else:
                await chat_manager.handle_user_message(message)

    finally:
        await chat_manager.remove_client(client_id)




# from fastapi import FastAPI, WebSocket,Request
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from typing import List

# app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

# templates = Jinja2Templates(directory="templates")

# clients: List[WebSocket] = []
# client_counter = 0 

# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     global client_counter
#     await websocket.accept()
#     client_id = client_counter
#     client_counter += 1
#     clients.append((client_id, websocket))  # Add the new client to the list with its ID
#     try:
#         while True:
#             data = await websocket.receive_text()
#             for client in clients:
#                 await client[1].send_text(f"Client {client[0]}: {data}")
#     finally:
#         clients.remove((client_id, websocket)) 
#         await websocket.close()
