# from flask import Flask, render_template, request, jsonify
# from flask_socketio import SocketIO, send

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'
# socketio = SocketIO(app, cors_allowed_origins="*")

# # Store user sessions
# users = {}  # Maps user IDs to their connection info

# @app.route('/')
# def index():
#     return render_template('index.html')

# @socketio.on('connect')
# def on_connect():
#     send("User connected")

# @socketio.on('disconnect')
# def on_disconnect():
#     send("User disconnected")

# @socketio.on('message')
# def handle_message(data):
#     if not all(key in data for key in ('sender', 'receiver', 'message')):
#         send("Invalid message format", to=request.sid)
#         return


#     sender = data['sender']
#     receiver = data['receiver']
#     message = data['message']

#     if receiver in users:
#         send({"sender": sender, "message": message}, to=users[receiver])
#     else:
#         send("Receiver not connected", to=request.sid)

# @socketio.on('register')
# def register_user(data):
#     username = data['username']
#     users[username] = request.sid
#     send(f"{username} registered successfully")

# if __name__ == '__main__':
#     socketio.run(app, debug=True,port=5001)




# import asyncio
# import websockets
# # from websockets.asyncio.server import serve

# async def hello(websocket):
#     name = await websocket.recv()
#     print(f"<<< {name}")

#     greeting = f"Hello {name}!"

#     await websocket.send(greeting)
#     print(f">>> {greeting}")

# async def main():
#     async with websockets.serve(hello, "localhost", 8765):
#         await asyncio.get_running_loop().create_future()  # run forever

# if __name__ == "__main__":
#     asyncio.run(main())


# import asyncio
# import websockets

# # A set to keep track of connected clients
# connected_clients = set()

# async def handle_connection(websocket, path):
#     # Register new client
#     connected_clients.add(websocket)
#     print(f"Client connected: {websocket.remote_address}")
#     print(connected_clients)
    
#     try:
#         async for message in websocket:
#             print(f"Message received: {message}")
#             # Echo the message back to all connected clients
#             for client in connected_clients:
#                 if client == websocket:
#                     print('running...')
#                     await client.send(f"Echo: {message}")
#     except websockets.exceptions.ConnectionClosed as e:
#         print(f"Client disconnected: {e}")
#     finally:
#         # Remove the client from the set on disconnect
#         connected_clients.remove(websocket)

# # Start the WebSocket server
# async def main():
#     async with websockets.serve(handle_connection, "localhost", 8765):
#         print("WebSocket server running on ws://localhost:8765")
#         await asyncio.Future()  # Run forever

# if __name__ == "__main__":
#     asyncio.run(main())




# import asyncio
# import websockets
# import json

# # A dictionary to store connections with the associated username
# connected_clients = {}

# async def handle_connection(websocket, path):
#     # Receive the username from the client upon connection
#     data = await websocket.recv()
#     user = json.loads(data)
#     print(f"{user} connected.")
#     print(f"{user['id']}")
#     connected_clients[user['id']] = websocket
#     print(connected_clients)
#     print(f"{user['name']} connected.")

#     try:
#         while True:
#             # Receive message from the client
#             data = await websocket.recv()

#             # Parse the message (assume it's a JSON object with "to" and "message" keys)
#             msg_data = json.loads(data)
#             reciver_recipient = msg_data["to"]
#             msg = msg_data["message"]
#             sender = msg_data["sender"]
#             print(f"Message from {sender['name']}: {msg}")

#             # Send the message to the recipient if they are connected
#             if reciver_recipient['id'] in connected_clients:
#                 reciver_recipient_ws = connected_clients[reciver_recipient['id']]
#                 await reciver_recipient_ws.send(json.dumps({"from": sender, "message": msg}))
#             else:
#                 print(f"User {reciver_recipient} is not connected.")
#     except websockets.exceptions.ConnectionClosed:
#         print(f"{user} disconnected.")
#     finally:
#         del connected_clients[user['id']]

# # Start the WebSocket server
# async def main():
#     async with websockets.serve(handle_connection, "localhost", 8765):
#         print("Server is running on ws://localhost:8765")
#         await asyncio.Future()  # Run forever

# if __name__ == "__main__":
#     asyncio.run(main())





# ===============================================================================================================================================


# import asyncio
# import websockets
# import json
# import os

# PORT = int(os.environ.get("PORT", 10000))
# # Dictionaries to store connections and offline messages
# connected_clients = {}
# offline_messages = {}

# async def handle_connection(websocket, path):
#     # Receive the username from the client upon connection
#     data = await websocket.recv()
#     user = json.loads(data)
#     print(f"{user} connected.")
#     connected_clients[user['id']] = websocket
#     print(f"{user['name']} connected.")
#     print(f"Connected clients: {connected_clients}")

#     # Send offline messages if any
#     if user['id'] in offline_messages:
#         print(f"Sending offline messages to {user['name']}")
#         for message in offline_messages[user['id']]:
#             await websocket.send(json.dumps(message))
#         # Clear the offline messages after sending
#         del offline_messages[user['id']]

#     try:
#         while True:
#             # Receive message from the client
#             data = await websocket.recv()
#             msg_data = json.loads(data)

#             reciver_recipient = msg_data["to"]
#             msg = msg_data["message"]
#             sender = msg_data["sender"]
#             print(f"Message from {sender['name']} to {reciver_recipient['name']}: {msg}")

#             # Check if the recipient is connected
#             if reciver_recipient['id'] in connected_clients:
#                 reciver_recipient_ws = connected_clients[reciver_recipient['id']]
#                 await reciver_recipient_ws.send(json.dumps({"from": sender, "message": msg}))
#             else:
#                 print(f"User {reciver_recipient['name']} is offline. Storing message.")
#                 # Store the message in offline_messages
#                 if reciver_recipient['id'] not in offline_messages:
#                     offline_messages[reciver_recipient['id']] = []
#                 offline_messages[reciver_recipient['id']].append({"from": sender, "message": msg})
#     except websockets.exceptions.ConnectionClosed:
#         print(f"{user['name']} disconnected.")
#     finally:
#         # Remove the user from connected clients
#         if user['id'] in connected_clients:
#             del connected_clients[user['id']]
#         print(f"Connected clients after disconnection: {connected_clients}")

# # Start the WebSocket server
# async def main():
#     # async with websockets.serve(handle_connection, "0.0.0.0", 8775):
#     async with websockets.serve(handle_connection, "0.0.0.0", PORT):
#         # print("Server is running on ws://localhost:8775")
#         print(f"Running on ws://0.0.0.0:{PORT}")
#         await asyncio.Future()  # Run forever

# if __name__ == "__main__":
#     asyncio.run(main())
# ================================================================================================================

import asyncio
import websockets
import json
from datetime import datetime
import requests
import os

PORT = int(os.environ.get("PORT", 10000))
connected_clients = {}         # user_id -> websocket
offline_messages = {}          # user_id -> list of messages



async def handle_connection(websocket):
    try:
        # Initial user connection handshake
        data = await websocket.recv()
        print("Initial connection data:", data)

        user = json.loads(data)
        user_id = user.get("id")
        user_role = user.get("role")

        if not user_id or not user_role:
            await websocket.send(json.dumps({"error": "Missing id or role"}))
            return

        user_name = f"{user_role.capitalize()}-{user_id}"
        connected_clients[user_id] = websocket
        print(f"{user_role} {user_name} connected.")
        print(f"Connected clients: {list(connected_clients.keys())}")

        # Send any stored offline messages
        if user_id in offline_messages:
            for msg in offline_messages[user_id]:
                await websocket.send(json.dumps(msg))
            del offline_messages[user_id]  # Clear after sending

        # Message receive loop
        while True:
            try:
                data = await websocket.recv()
                print("Received message:", data)

                msg_data = json.loads(data)
                msg_type = msg_data.get("type")

                if not msg_type:
                    await websocket.send(json.dumps({"error": "Missing message type"}))
                    continue

                
                # === Handle Chat Message ===
                if msg_type == "chat":
                    sender = msg_data.get("sender")
                    receiver = msg_data.get("to")
                    message_text = msg_data.get("message")

                    if not sender or not receiver or not message_text:
                        await websocket.send(json.dumps({"error": "Incomplete chat message"}))
                        continue

                    
                    try:
                        res = requests.post(
                            # "http://127.0.0.1:5004/chat",
                            "https://sports-backend-j4bp.onrender.com/chat",
                            json={
                                "athlete_id": sender["id"] if sender["role"] == "athlete" else receiver["id"],
                                "coach_id": sender["id"] if sender["role"] == "coach" else receiver["id"],
                                "message": message_text
                            }
                        )
                        if res.status_code != 201:
                            print("Failed to save chat:", res.json())
                            await websocket.send(json.dumps({"error": "Failed to save chat message"}))
                            continue

                        chat_response = res.json()
                        timestamp = datetime.utcnow().isoformat()

                    except Exception as e:
                        print("Error while sending chat to backend:", e)
                        await websocket.send(json.dumps({"error": "Could not contact backend"}))
                        continue

                    # Continue with WebSocket delivery
                    response_payload = {
                        "type": "chat",
                        "from": sender,
                        "message": message_text,
                        "timestamp": timestamp
                    }

                    recipient_ws = connected_clients.get(receiver["id"])
                    if recipient_ws:
                        await recipient_ws.send(json.dumps(response_payload))
                    else:
                        print(f"User {receiver['id']} is offline. Storing message.")
                        offline_messages.setdefault(receiver["id"], []).append(response_payload)


                elif msg_type == "typing":
                    sender = msg_data.get("sender")
                    receiver = msg_data.get("to")
                    if not sender or not receiver:
                        continue

                    recipient_ws = connected_clients.get(receiver["id"])
                    if recipient_ws:
                        await recipient_ws.send(json.dumps({
                            "type": "typing",
                            "from": sender
                        }))

            except json.JSONDecodeError:
                await websocket.send(json.dumps({"error": "Invalid JSON"}))
            except Exception as err:
                print("Error during message processing:", err)

    except websockets.exceptions.ConnectionClosed:
        print(f"{user_name if 'user_name' in locals() else 'A user'} disconnected.")
    except Exception as outer_exc:
        print("Connection error:", outer_exc)
    finally:
        if 'user_id' in locals() and user_id in connected_clients:
            del connected_clients[user_id]
        print(f"Connected clients after disconnection: {list(connected_clients.keys())}")

async def main():
    # async with websockets.serve(handle_connection, "localhost", 8775):
    async with websockets.serve(handle_connection, "0.0.0.0", PORT):
        # print("WebSocket server running at ws://localhost:8775")
        print(f"Running on ws://0.0.0.0:{PORT}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
