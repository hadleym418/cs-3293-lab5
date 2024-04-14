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
        
    #TODO: Implement this function
    def send_request_get_reply(self, request):
        #TODO: encode the request
        #TODO: send the request on the connection
        #TODO recieve the reply with RECV_BUFFER_SIZE
        #TODO: decode the reply
        #TODO: return the decoded reply
        pass
        
        
    def send_login(self, username, password):
        self.conn.connect((self.server_addr, self.port))
        request = #TODO: construct login request string 
        reply = self.send_request_get_reply(request)
    
        if reply == #TODO: Check if login was successful by checking the reply 
            # TODO: set logged_in to True
            # TODO: set username of client
            print("Login successful")
        else:
            print("Login failed. Try again..")

            
    def fetch_messages(self):
        request = #TODO: Construct fetch request message
        reply = self.send_request_get_reply(request)
        parts = reply.split(':')
        if parts[0] == #TODO: Check if reply was for "FETCH"
            #TODO: Print all the messages recieved
        else:
            print("Error fetching messages")

    #TODO: Implement message validation according to spec.
    def validate_message(self, message):
        # checks that no special characters, and len is less than 1024
        return False

    def send_message(self):
        message = input("Enter message: ")
        valid = self.validate_message(message)
        if valid:
            request = #TODO: Construct request for message, hint: use self.get_time() to get current time
            reply = self.send_request_get_reply(request)
    
            # STUDENT
            if reply == #TODO: Check the correct reply code for success
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