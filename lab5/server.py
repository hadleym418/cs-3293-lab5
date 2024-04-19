###############################################################################
# server-python.py
# Name:
# NetId:
###############################################################################

import sys
import socket
from threading import Thread
import csv
import numpy as np

from collections import deque

RECV_BUFFER_SIZE = 2048
QUEUE_LENGTH = 120


# Need Following API on Server for Tests:
    # start_server,
    # stop_server,
    # start_multithreaded_server,
    # start_server_with_auth,
    
    
# Design:
# Start server on a port
# Listen for incoming connections -> hold a backlog of about 120 connections
# Accept incoming connections and spawn a thread to handle the connection
# Server will have a MessageBoard object that holds a list of Messages.
# Server will also read from a student_id_password.csv file to authenticate users. [TODO: make google form, so students can register their id and password]

# Restrictions to apply at client side:
# 1. Make sure messages are not longer than 1024 characters, and are only text.


class Message:
    def __init__(self, user, message, time):
        self.user = user
        self.time = time
        self.message = message
        
    def __str__(self):
        return f"[{self.time}] {self.user}->  {self.message}"

class MessageBoard:
    def __init__(self, capacity = 10):
        self.messages = deque(maxlen=capacity)
        self.capacity = capacity
        
    def add_message(self, user, message, time):
        self.messages.append(Message(user, message, time))
        
    def get_messages(self, n = 5):
        if len(self.messages) > 0:
            messages = list(self.messages) 
            messages.sort(key=lambda x: x.time)
        else:
            messages = []
        return messages
        

class Server:
    def __init__(self, port = 8326):
        self.port = 8326
        self.message_board = MessageBoard()
        self.load_user_pass()
        self.connections = []
    
    def load_user_pass(self, filename="student_id_password.csv"):
        self.user_pass = {}
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                username = row[0].strip()
                password = row[1].strip()
                if username != "student_id" and username not in self.user_pass:
                    self.user_pass[username] = password
        print("Loaded user pass: ", self.user_pass)

    def check_login(self, username, password):
        if username in self.user_pass:
            return self.user_pass[username] == password
        return False
    

    def handle_client(self, conn):
        # "LOGIN:username:password"
        # "FETCH:"
        # "MESSAGE:username:message:time"
        data = 'dummy'
        client_logged_in = False
        while len(data) > 0:
            data = conn.recv(RECV_BUFFER_SIZE)
            data = data.decode()
            parts = data.split(':')
            print("Received: ", parts)
            reply = "ERROR:EMPTY"
            if parts[0] == "LOGIN" and client_logged_in == False:
                result = self.check_login(parts[1], parts[2])
                client_logged_in = result
                reply = "LOGIN:SUCCESS" if result else "LOGIN:FAILED"
            elif parts[0] == "FETCH":
                messages = self.message_board.get_messages()
                reply = "FETCH:" + ":".join([str(msg) for msg in messages])
            elif parts[0] == "MESSAGE":
                try:
                    assert len(parts) == 4
                    assert client_logged_in == True
                    reply = "MESSAGE:SUCCESS"
                    self.message_board.add_message(parts[1], parts[2], parts[3])
                except AssertionError:
                    reply = "ERROR:INVALID_MESSAGE"
            else:
                # discard the message
                reply = "ERROR:INVALID_COMMAND"
            
            conn.send(reply.encode())


    def server_run(self,):
        HOST = 'localhost'                 # Symbolic name meaning all available interfaces
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, self.port))
        s.listen(QUEUE_LENGTH) # Each server should maintain a short (5-10) client queue
        
        while True:
            try:
                conn, addr = s.accept()
                print(f"Client {conn} connected")
                thread = Thread(target = self.handle_client, args = (conn,))
                thread.start()
            except Exception as e:
                print("Error: ", e)
                continue
            except KeyboardInterrupt:
                print("Server shutting down")
                break
        


def main():
    server = Server()
    # server.load_user_pass()
    server.server_run()
    # """Parse command-line argument and call server function """
    # if len(sys.argv) != 2:
    #     sys.exit("Usage: python server-python.py [Server Port]")
    # server_port = int(sys.argv[1])
    # server(server_port)

if __name__ == "__main__":
    main()
