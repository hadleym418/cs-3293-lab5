import socket
import sys
import time


# Client Design:
# Client Restrictions:
    # Messages should not contain any special characters, and should be less than 1024 characters.

# LOGIN PHASE:
    # Ask user for username and password -> should have registered earlier
    # Send username and password to server
    # Server will reply with "LOGIN:SUCCESS" or "LOGIN:FAILED"
    # If login fails, ask user to try again
    # If login succeeds, 
    #   store username
    #   move to next phase
    
# MESSAGE FETCH AND SEND PHASE:
    # Keep Looping between sending a message, and fetching messages.
    # Send message: 
    #   Take message as input from user, and send it to server, wait for reply.
    #   Server will reply with "MESSAGE:SUCCESS" or "MESSAGE:FAILED"
    
RECV_BUFFER_SIZE = 1024

class Client:
    def __init__(self, server_addr, port = 8326):
        self.server_addr = server_addr
        self.port = port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.logged_in = False
        self.username = None
        
    def get_time(self):
        # format time in Month/Day/Year Hour-Minute-Second
        return time.strftime("%m/%d/%Y %H-%M-%S")
        
    #Implement this function
    def send_request_get_reply(self, request):
        #encode the request
        encoded_req = request.encode()
        #send the request on the connection
        self.conn.send(encoded_req)
        #recieve the reply with RECV_BUFFER_SIZE
        reply = self.conn.recv(RECV_BUFFER_SIZE)
        #decode the reply
        decoded_reply = reply.decode()
        #return the decoded reply
        return decoded_reply
        
        
    def send_login(self, username, password):
        self.conn.connect((self.server_addr, self.port))
        #construct login request string 
        request = f"LOGIN:{username}:{password}"
        reply = self.send_request_get_reply(request)
        
        #Check if login was successful by checking the reply 
        if reply == "LOGIN:SUCCESS":
            #set logged_in to True
            self.logged_in = True
            #set username of client
            self.username = username
            print("Login successful")
        else:
            print("Login failed. Try again..")

            
    def fetch_messages(self):
        #Construct fetch request message
        request = f"FETCH:{self.username}"
        reply = self.send_request_get_reply(request)
        parts = reply.split(':')
        #Check if reply was for "FETCH"
        if parts[0] == "FETCH":
            #Print all the messages recieved
            messages = parts[1].split(';')
            print("Messages: ")
            for message in messages:
                print(message)
        else:
            print("Error fetching messages")

    #Implement message validation according to spec.
    def validate_message(self, message):
        # checks that no special characters, and len is less than 1024
        bad_chars = "~!@#$%^&*()_+{}|:\"<>?`-=[]\\;',./"
        valid_chars = True
        for c in message:
            if c not in bad_chars:
                valid_chars = True
            else:
                valid_chars = False
                break
        if (len(message) < 1024) and (valid_chars):
            return True
        else:
            return False

    def send_message(self):
        message = input("Enter message: ")
        valid = self.validate_message(message)
        if valid:
            #Construct request for message, hint: use self.get_time() to get current time
            curr_time = self.get_time()
            request = f"MESSAGE:{self.username}:{curr_time}:{message}"
            reply = self.send_request_get_reply(request)
    
            # STUDENT
            #Check the correct reply code for success
            if reply == "MESSAGE:SUCCESS":
                print("Message sent successfully") 
                print("==========================")
            else:
                print("Message failed to send") 
                print("==========================")
        

    def run(self):
        while True:
            if self.logged_in == False:
                username = input("Enter username: ")
                password = input("Enter password: ")
                self.send_login(username, password)
            else:
                self.fetch_messages()
                self.send_message()

def main():
    server_addr = sys.argv[1]
    client = Client(server_addr)
    client.run()



if __name__ == "__main__":
    main()

