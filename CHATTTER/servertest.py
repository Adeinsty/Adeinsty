
# import socket
# import threading

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(('localhost', 5555))
# server.listen()

# chat_rooms = {"room1": [], "room2": []}
# usernames = {}

# def broadcast(message, room):
#     for client in chat_rooms[room]:
#         try:
#             client.send(message)
#         except:
#             continue

# def private_message(client, target_username, message):
#     target_client = find_client_by_username(target_username)

#     if target_client:
#         try:
#             target_room = get_client_room(target_client)
#             sender_room = get_client_room(client)

#             if target_room and sender_room and target_room == sender_room:
#                 target_client.send(message)
#                 client.send(message)
#         except:
#             pass

# def find_client_by_username(username):
#     for clients in chat_rooms.values():
#         for client in clients:
#             if usernames.get(client) == username:
#                 return client
#     return None

# def join_room(client, new_room):
#     current_room = get_client_room(client)
    
#     if current_room:
#         chat_rooms[current_room].remove(client)

#     if new_room not in chat_rooms:
#         chat_rooms[new_room] = [client]
#     else:
#         chat_rooms[new_room].append(client)

#     usernames[client] = f"Guest{len(usernames)+1}"  # Assign a guest username for the new room
#     broadcast(f"{usernames[client]} has joined the chat.", new_room)

# def get_client_room(client):
#     for room, clients in chat_rooms.items():
#         if client in clients:
#             return room
#     return None

# def handle(client, room):
#     while True:
#         try:
#             message = client.recv(1024)
#             if message.startswith('/join'):
#                 new_room = message.split(' ')[1]
#                 join_room(client, new_room)
#             elif message.startswith('/pm'):
#                 _, target_username, pm_message = message.split(' ', 2)
#                 private_message(client, target_username, f"PM from {usernames[client]}: {pm_message}".encode('utf-8'))
#             else:
#                 broadcast(message, room)
#         except:
#             index = chat_rooms[room].index(client)
#             chat_rooms[room].remove(client)
#             username = usernames[client]
#             broadcast(f"{username} has left the chat.", room)
#             del usernames[client]
#             break

# def receive():
#     while True:
#         client, address = server.accept()
#         print(f"Connection established with {str(address)}")

#         client.send("Welcome to the chat! To login, use '/login <username>' or '/guest' for guest access.".encode('utf-8'))

#         room = client.recv(1024).decode('utf-8').lower()
#         if room not in chat_rooms:
#             client.send("Invalid chat room.".encode('utf-8'))
#             client.close()
#         else:
#             thread = threading.Thread(target=handle, args=(client, room))
#             thread.start()
#             chat_rooms[room].append(client)

# def main():
#     receive()

# if __name__ == "__main__":
#     main()


dict = {1 : 2, 3 : 4}
a = 1
print(dict.get(a))