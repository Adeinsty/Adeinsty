import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

class ChatClient:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

        self.username = None
        self.room = None

        self.gui_init()

    def gui_init(self):
        self.root = tk.Tk()
        self.root.title("Chat Room")

        self.text_area = scrolledtext.ScrolledText(self.root)
        self.text_area.pack(padx=10, pady=10)

        self.input_area = tk.Entry(self.root)
        self.input_area.pack(pady=10)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack()

        self.join_button = tk.Button(self.root, text="Join Room", command=self.join_room)
        self.join_button.pack()

        self.private_message_button = tk.Button(self.root, text="Private Message", command=self.private_message)
        self.private_message_button.pack()

        self.login()

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        self.root.mainloop()

    def login(self):
        self.username = simpledialog.askstring("Login", "Enter your username:")
        self.room = simpledialog.askstring("Room", "Enter chat room (room1 or room2):").lower()

        if self.room not in ['room1', 'room2']:
            print("Invalid chat room.")
            self.root.destroy()
        else:
            self.client.send(self.room.encode('utf-8'))
            self.client.send(f"/login {self.username}".encode('utf-8'))

    def send_message(self):
        message = self.input_area.get()
        if message:
            self.client.send(message.encode('utf-8'))
            self.input_area.delete(0, tk.END)

    def join_room(self):
        new_room = simpledialog.askstring("Join Room", "Enter room name:")
        if new_room:
            self.client.send(f"/join {new_room}".encode('utf-8'))

    def private_message(self):
        target_username = simpledialog.askstring("Private Message", "Enter username to chat with:")
        if target_username:
            message = simpledialog.askstring("Private Message", "Enter your message:")
            if message:
                self.client.send(f"/pm {target_username} {message}".encode('utf-8'))

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                self.text_area.insert(tk.END, f"{message}\n")
                self.text_area.yview(tk.END)
            except Exception as e:
                print(e)
                break

if __name__ == "__main__":
    host = 'localhost'
    port = 5555
    client = ChatClient(host, port)
