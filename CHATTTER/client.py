import socket
import threading
import customtkinter as ctk
import tkinter as tk

host = 'localhost'
port = 55555
# #! Sign In Options
# def sign_in(client):
#     while True:
#         print("1. Login")
#         print("2. Register")
#         choice = input("Enter your choice: ")
#         if choice == "1":
#             client.sendall("login".encode('utf-8'))
#             login(client)
#             break
#         elif choice == "2":
#             client.sendall("register".encode('utf-8'))
#             register(client)
#             break
#         else:
#             print("Invalid choice. Please try again.")

# #! Register
# def register(client):
#     while True:
#         username = input("Enter your username: ")
#         client.sendall(username.encode('utf-8'))
#         password = input("Enter your password: ")
#         client.sendall(password.encode('utf-8'))
#         try:
#             response = client.recv(2048).decode('utf-8')
#             print(response)
#             if response == "Register successful.":
#                 sign_in(client)
#             else:
#                 print("Please try again.")
#         except Exception as e:
#             print(e)
#             break

# #! Login
# def login(client):
#     while True:
#         username = input("Enter your username: ")
#         client.sendall(username.encode('utf-8'))
#         password = input("Enter your password: ")
#         client.sendall(password.encode('utf-8'))
#         try:
#             response = client.recv(2048).decode('utf-8')
#             print(response)
#             if response == "Login successful.":
#                 listening_thread = threading.Thread(target=listen, args=(client,))
#                 listening_thread.start()
#                 send(client)
#                 break
#             else:
#                 print("Please try again.")
#         except Exception as e:
#             print(e)
#             break

# #! Listening Message
# def listen(client):
#     while True:
#         message = client.recv(2048).decode('utf-8')
#         if message != '':
#             username = message.split(' ~ ')[0]
#             msg = message.split(' ~ ')[1]
#             print(f"[{username}] : {msg}\n")

# #! Sending Message
# def send(client):
#     while True:
#         message = input('Enter Message : ')
#         if message != '':
#             client.sendall(message.encode())

# #! Main Function
# def main():
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     try:
#         client.connect((host, port))
#         print(f"Connected to server {host}:{port}")
#     except socket.error as e:
#         print(str(e))
#     sign_in(client)

# if __name__ == "__main__":
#     main()


class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.login_valid = False
        self.register_valid = False
        self.chatbox = None
        try:
            self.client.connect((host, port))
            print(f"Connected to server {host}:{port}")
            self.setup_gui()
        except socket.error as e:
            print(str(e))
        

    def setup_gui(self):
        ctk.set_appearance_mode('system')
        ctk.set_default_color_theme('dark-blue')
        self.root = ctk.CTk()
        self.root.title('CHATTTER')
        self.root.geometry('600x440')
        self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.signin()

    def on_close(self):
    # Menutup koneksi soket
        self.client.send("//ConnClosed//".encode('utf-8'))
        self.client.close()
    # Menutup aplikasi
        self.root.destroy()
    
    def signin(self):
        if self.login_valid :
            self.login_frame.destroy()
            self.login_button.destroy()
            self.register_button.destroy()
        if self.register_valid :
            self.register_frame.destroy()
            self.register_button.destroy()
        self.signin_frame = ctk.CTkFrame(self.root, width=220, height=230,corner_radius=10)
        self.signin_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.signin_label = ctk.CTkLabel(self.signin_frame, text='Sign in to CHATTER', font=('Century Gothic', 20, 'bold'))
        self.signin_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.login_button = ctk.CTkButton(self.signin_frame, text='Log in', font=('Century Gothic', 12, 'bold'), command=self.login_clicked)
        self.login_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.register_button = ctk.CTkButton(self.signin_frame, text='Register', font=('Century Gothic', 12, 'bold'), command=self.register_clicked)
        self.register_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    
    def login_clicked(self):
        self.login_valid = True
        self.client.send("login".encode('utf-8'))
        self.signin_frame.destroy()
        self.register_button.destroy()
        self.login_frame = ctk.CTkFrame(self.root, width=320, height=360,corner_radius=10)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.login_label = ctk.CTkLabel(self.login_frame, text='Log in to CHATTER', font=('Century Gothic', 20, 'bold'))
        self.login_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.login_button = ctk.CTkButton(self.login_frame, text='Log in', font=('Century Gothic', 12, 'bold'), command=self.login)
        self.login_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        self.back_button = ctk.CTkButton(self.login_frame, text='Back', font=('Century Gothic', 12, 'bold'), command=self.signin)
        self.back_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        self.username = ctk.CTkEntry(self.login_frame, width=220, font=('Century Gothic', 12), placeholder_text='Username')
        self.username.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.password = ctk.CTkEntry(self.login_frame, width=220, font=('Century Gothic', 12), placeholder_text='Password', show='*')   
        self.password.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    def login(self):
        username = self.username.get()
        password = self.password.get()
        if username == "" or password == "":
            self.empty_label = ctk.CTkLabel(self.login_frame, text='**Please fill in all the fields', font=('Century Gothic', 12, 'bold'),text_color='white')
            self.empty_label.place(relx=0.4, rely=0.5, anchor=tk.CENTER)
        else :
            self.client.sendall(username.encode('utf-8'))
            self.client.sendall(password.encode('utf-8'))
            try : 
                response = self.client.recv(2048).decode('utf-8')
                print(response)
                if response == "Login successful.":
                    self.room = 'Main Room'
                    self.chat_room()
                    listening_thread = threading.Thread(target=self.listen)
                    listening_thread.start()
                
                elif response == "Login failed. User already logged in.":
                    self.wrong_label = ctk.CTkLabel(self.login_frame, text='**User already logged in', font=('Century Gothic', 12, 'bold'),text_color='red')
                    self.wrong_label.place(relx=0.4, rely=0.5, anchor=tk.CENTER)
                    print("Please try again.")
                      
                else:
                    self.wrong_label = ctk.CTkLabel(self.login_frame, text='**Wrong username or password', font=('Century Gothic', 12, 'bold'),text_color='red')
                    self.wrong_label.place(relx=0.4, rely=0.5, anchor=tk.CENTER)
                    print("Please try again.")
            except Exception as e:
                print(e)
                    

    def register_clicked(self):
        self.register_valid = True
        self.client.send("register".encode('utf-8'))
        self.signin_frame.destroy()
    
        self.register_frame = ctk.CTkFrame(self.root, width=320, height=360,corner_radius=10)
        self.register_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.register_label = ctk.CTkLabel(self.register_frame, text='Register to CHATTER', font=('Century Gothic', 20, 'bold'))
        self.register_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.new_username = ctk.CTkEntry(self.register_frame, width=220, font=('Century Gothic', 12), placeholder_text='Username')
        self.new_username.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.new_password = ctk.CTkEntry(self.register_frame, width=220, font=('Century Gothic', 12), placeholder_text='Password', show='*')    
        self.new_password.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        self.new_password_2 = ctk.CTkEntry(self.register_frame, width=220, font=('Century Gothic', 12), placeholder_text='Confirm Password', show='*')
        self.new_password_2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.register_button = ctk.CTkButton(self.register_frame, text='Register', font=('Century Gothic', 12, 'bold'), command=self.registration)
        self.register_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        self.back_button = ctk.CTkButton(self.register_frame, text='Back', font=('Century Gothic', 12, 'bold'), command=self.signin)
        self.back_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        
        pass

    def registration(self):
        username = self.new_username.get()
        password = self.new_password.get()
        password_2 = self.new_password_2.get()
        if password == password_2 and username != "" and password != "":
            self.client.sendall(username.encode('utf-8'))
            self.client.sendall(password.encode('utf-8'))
            try :
                response = self.client.recv(2048).decode('utf-8')
                print(response)
                if response == "Register successful.":
                    self.registrationsuccess_label = ctk.CTkLabel(self.register_frame, text='**Registration success', font=('Century Gothic', 12, 'bold'),text_color='white')
                    self.registrationsuccess_label.place(relx=0.4, rely=0.6, anchor=tk.CENTER)
                    self.registrationsuccess_label.after(2000, self.registrationsuccess_label.destroy)
                    self.registration_validation()
                    print("keren")
            
                else:
                    self.registrationfailed_label = ctk.CTkLabel(self.register_frame, 
                                                                 text='**Registration failed, username is not available or taken.', 
                                                                 font=('Century Gothic', 12, 'bold'),text_color='white', wraplength=200, anchor='w')
                    self.registrationfailed_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
                    print("Please try again.")
            except:
                print("Please try againddd.")
        if username == "" or password == "":
            self.empty_label = ctk.CTkLabel(self.register_frame, text='**Please fill in all the fields', font=('Century Gothic', 12, 'bold'),text_color='white')
            self.empty_label.place(relx=0.4, rely=0.6, anchor=tk.CENTER)
            self.empty_label.after(2000, self.empty_label.destroy)
        if password != password_2:
            self.mismatch_label = ctk.CTkLabel(self.register_frame, text='**Password does not match', font=('Century Gothic', 12, 'bold'),text_color='red')
            self.mismatch_label.place(relx=0.4, rely=0.6, anchor=tk.CENTER)
            self.mismatch_label.after(2000, self.mismatch_label.destroy)
    
    def registration_validation(self):
        self.register_frame.destroy()
        self.register_button.destroy()
        self.registration_validation_frame = ctk.CTkFrame(self.root, width=220, height=150,corner_radius=10)
        self.registration_validation_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.registration_validation_label = ctk.CTkLabel(self.registration_validation_frame, text='Registration Success!', font=('Century Gothic', 20, 'bold'))
        self.registration_validation_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.registration_validation_button = ctk.CTkButton(self.registration_validation_frame, text='Log in', font=('Century Gothic', 12, 'bold'), command=self.login_clicked)
        self.registration_validation_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        self.registration_validation_button = ctk.CTkButton(self.registration_validation_frame, text='Back', font=('Century Gothic', 12, 'bold'), command=self.signin)
        self.registration_validation_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)


    def chat_room(self):
        self.signin_frame.destroy()
        self.main_frame = ctk.CTkFrame(self.root,corner_radius=10)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)
        
        self.chat_room_frame = ctk.CTkFrame(self.main_frame,corner_radius=10)
        self.chat_room_frame.place(relx= 0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.8, relheight=0.8)
        self.chat_label = ctk.CTkLabel(self.main_frame, text='CHATTTER', font=('Century Gothic', 20, 'bold'),bg_color="transparent",fg_color=None)
        self.chat_label.lift()
        self.chat_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
        
        self.chatbox = ctk.CTkTextbox(self.chat_room_frame, font=('Century Gothic', 12))
        self.chatbox.place(relx=0.5, rely=0.4, anchor=tk.CENTER, relwidth=0.9, relheight=0.7)
        self.chatbox.configure(state='disabled')
        # self.chatscrollbar = ctk.CTkScrollbar(self.chat_room_frame, command=self.chatbox.yview)
        # self.chatscrollbar.place(relx=0.95, rely=0.4, anchor=tk.CENTER, relheight=0.7)

        self.chat_room_label = ctk.CTkLabel(self.chat_room_frame, text=self.room, font=('Century Gothic', 14, 'bold'),corner_radius=10,)
        self.chat_room_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
        self.chat_room_label.lift()

        self.entry_message = ctk.CTkEntry(self.chat_room_frame, font=('Century Gothic', 12), placeholder_text='Enter Message..')
        self.entry_message.place(relx=0.05, rely=0.9, anchor = "w", relwidth=0.75, relheight=0.1)
        self.entry_message.focus()

        self.send_button = ctk.CTkButton(self.chat_room_frame, text='Send', font=('Century Gothic', 12, 'bold'), command=self.send)
        self.send_button.place(relx=0.9, rely=0.9, anchor=tk.CENTER, relwidth=0.1, relheight=0.1)

    
    def listen(self):
        while True:
            try :
                message = self.client.recv(2048).decode('utf-8')
                if message != '':
                    username = message.split(' ~ ')[0]
                    if username == self.username.get() :
                        username = "You"
                    msg = message.split(' ~ ')[1]
                    self.chatbox.configure(state='normal')
                    self.chatbox.insert(tk.END, f"[{username}] : {msg}\n")
                    self.chatbox.configure(state='disabled')
                    self.chatbox.see(tk.END)

                    print(f"[{username}] : {msg}\n")
            except Exception as e:
                print(e)
                print("error")
                break

    def send(self):
        message = self.entry_message.get()
        if message != '':
            self.client.sendall(message.encode())
            self.entry_message.delete(0, tk.END)

if __name__ == "__main__":
    chat_client = ChatClient(host, port)
    chat_client.root.mainloop()


