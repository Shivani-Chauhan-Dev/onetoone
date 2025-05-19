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








import asyncio
import websockets
import json

# Dictionaries to store connections and offline messages
connected_clients = {}
offline_messages = {}

async def handle_connection(websocket, path):
    # Receive the username from the client upon connection
    data = await websocket.recv()
    user = json.loads(data)
    print(f"{user} connected.")
    connected_clients[user['id']] = websocket
    print(f"{user['name']} connected.")
    print(f"Connected clients: {connected_clients}")

    # Send offline messages if any
    if user['id'] in offline_messages:
        print(f"Sending offline messages to {user['name']}")
        for message in offline_messages[user['id']]:
            await websocket.send(json.dumps(message))
        # Clear the offline messages after sending
        del offline_messages[user['id']]

    try:
        while True:
            # Receive message from the client
            data = await websocket.recv()
            msg_data = json.loads(data)

            reciver_recipient = msg_data["to"]
            msg = msg_data["message"]
            sender = msg_data["sender"]
            print(f"Message from {sender['name']} to {reciver_recipient['name']}: {msg}")

            # Check if the recipient is connected
            if reciver_recipient['id'] in connected_clients:
                reciver_recipient_ws = connected_clients[reciver_recipient['id']]
                await reciver_recipient_ws.send(json.dumps({"from": sender, "message": msg}))
            else:
                print(f"User {reciver_recipient['name']} is offline. Storing message.")
                # Store the message in offline_messages
                if reciver_recipient['id'] not in offline_messages:
                    offline_messages[reciver_recipient['id']] = []
                offline_messages[reciver_recipient['id']].append({"from": sender, "message": msg})
    except websockets.exceptions.ConnectionClosed:
        print(f"{user['name']} disconnected.")
    finally:
        # Remove the user from connected clients
        if user['id'] in connected_clients:
            del connected_clients[user['id']]
        print(f"Connected clients after disconnection: {connected_clients}")

# Start the WebSocket server
async def main():
    async with websockets.serve(handle_connection, "localhost", 875):
        print("Server is running on ws://localhost:8775")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
