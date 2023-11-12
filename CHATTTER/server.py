# import socket
# import threading

# # Server configuration
# host = 'localhost'
# port = 55555
# usernames = {"test": "test2", "dies" : "dies", "ripan" : "ripan"} # Usernames list for login {username: password}
# rooms = {'main_room' : [] }

# #! Main Room Handler
# def main_handler(client,room,username):
#   rooms['main_room'].append((username,client))
#   bc_message = f"SERVER ~ {username} has joined the chat."
#   broadcast(client,bc_message, room)
#   handler_thread = threading.Thread(target=handler, args=(client,room,username))
#   handler_thread.start()

# #! Handler Function
# def handler(client, room, username):
#   while True:
#     message = client.recv(2048).decode('utf-8')
#     if message != '' :
#       final_msg = f"{username} ~ {message}"
#       broadcast(client,final_msg, room)    

# #! Broadcast
# def broadcast(client, message, room):
#   for user in rooms[room]:
#       user[1].send(message.encode('utf-8'))

# #! Sign In Options
# def sign_in(client):
#   while True:
#     response = client.recv(2048).decode('utf-8')
#     if response == "login":
#       login(client)
#     elif response == "register":
#       register(client)
    

# #! Login
# def login(client):
#   while True:
#     username = client.recv(2048).decode('utf-8')
#     password = client.recv(2048).decode('utf-8')
#     if usernames.get(username) == password:
#       client.sendall("Login successful.".encode('utf-8'))
#       main_handler_thread = threading.Thread(target=main_handler, args=(client,'main_room',username))
#       main_handler_thread.start()
#       break
#     else:
#       client.sendall("Login failed.".encode('utf-8'))
#   print("login success from " + username)

# #! Register
# def register(client):
#   while True:
#     username = client.recv(2048).decode('utf-8')
#     password = client.recv(2048).decode('utf-8')
#     if usernames.get(username) == None:
#       usernames[username] = password
#       client.sendall("Register successful.".encode('utf-8'))
#       break
#     else:
#       client.sendall("Register failed.".encode('utf-8'))
#   print("register success from " + username)

# #! Main server loop
# def main():
#   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP IPv4 socket
#   try :
#     server.bind((host, port)) # Bind the socket to the host and port
#     print(f"Server started on {host}:{port}")
#   except socket.error as e:
#     print(str(e))
#   server.listen() # Listen for incoming connections
#   while True:
#     client, address = server.accept()
#     print(f"New client connected : {address[0]} : {address[1]}")
#     sign_in_thread = threading.Thread(target=sign_in, args=(client,))
#     sign_in_thread.start()

# if __name__ == "__main__":
#   main()

import socket
import threading

# Server configuration
host = 'localhost'
port = 55555
usernames = {"test": "test2", "dies": "dies", "ripan": "ripan"}  # Usernames list for login {username: password}
rooms = {'main_room': []}
activeclients = []

def main_handler(client, room, username):
    try :
        rooms[room].append((username, client))
        bc_message = f"SERVER ~ {username} has joined the chat."
        broadcast(client, bc_message, room)
        while True:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                final_msg = f"{username} ~ {message}"
                broadcast(client, final_msg, room)
            if message == "//ConnClosed//":
                rooms[room].remove((username, client))
                break
    except ConnectionAbortedError:
        print(f"Connection to {username} was aborted.")
    except Exception as e:
        print(f"Error in handler for {username}: {e}")
    finally:
        rooms[room].remove((username, client))
        

def broadcast(sender, message, room):
    for user in rooms[room]:
      user[1].sendall(message.encode('utf-8'))

def sign_in(client):
    while True:
        response = client.recv(2048).decode('utf-8')
        if response == "login":
            login(client)
        elif response == "register":
            register(client)

def login(client):
    while True:
        username = client.recv(2048).decode('utf-8')
        password = client.recv(2048).decode('utf-8')
        if usernames.get(username) == password and username not in activeclients:
            client.sendall("Login successful.".encode('utf-8'))
            activeclients.append(username)
            main_handler(client, 'main_room', username)
            break
        elif username in activeclients:
            client.sendall("Login failed. User already logged in.".encode('utf-8'))
        else:
            client.sendall("Login failed.".encode('utf-8'))

    print("login success from " + username)
    print(usernames)

def register(client):
    while True:
        username = client.recv(2048).decode('utf-8')
        password = client.recv(2048).decode('utf-8')
        print(f"{username} {password}")
        if usernames.get(username) == None and username != "SERVER":
            usernames[username] = (password)  # Simpan informasi klien
            client.sendall("Register successful.".encode('utf-8'))
            print(69)
            sign_in(client)
            break
        else:
            client.sendall("Register failed.".encode('utf-8'))
            print(420)
        
    print("register success from " + username + password)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((host, port))
        print(f"Server started on {host}:{port}")
    except socket.error as e:
        print(str(e))
    server.listen()

    while True:
        client, address = server.accept()
        print(f"New client connected : {address[0]} : {address[1]}")
        sign_in_thread = threading.Thread(target=sign_in, args=(client,))
        sign_in_thread.start()

if __name__ == "__main__":
    main()