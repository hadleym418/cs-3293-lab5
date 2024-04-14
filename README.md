## Lab 5 Phase 2: Chat Room
Now that we have built a local echo server, let's move on to something more exciting. In the phase 2 of this lab, we will be building the client side of a global chat room. The chat room allows each user to log in, write their message to the chat room, and see other users' messages listed on the board. It's basically a big group chat for CS E326! 

By end of this lab, each team of students can connect to a privately hosted chat server 
using the chat client they will build, and chat with other students on the server.

_Goal of this project_: Building a multithreaded chat client that can connect to a globally hosted chat server. Each student will be expected to write up the client as per the specification provided.


## Preparation
(Same as phase 1).

Create a Python venv for this project using `mkdir venv && python3 -m venv venv/`.  
If you don't have python3 -m venv --upgradeled, you can install it using  `python3 -m pip install venv` and then run the above command.  
You should then activate the venv using `source venv/bin/activate`.  
Then, install the required packages using `pip install -r requirements.txt`.  

You are now ready to start coding. All the best!

## Implementation Details
 All the code you will implement is in the `client.py` file, which is located in the `lab5` folder. Complete all the TODOs. Here are some specific details about the code: 

### Username and Password
In order to begin the project, make sure the fill in the [Google form](https://docs.google.com/forms/d/e/1FAIpQLSeZbkBc257gDkOqkwN_neAHkyn-kgC9qqp0PocvH60OfP2q_w/viewform?pli=1), where you will provide your username and password for the client. MAKE SURE TO DO SO BEFORE YOU START THE PROJECT! 

### Server Port Number and IP
In the lab, you will be asked to enter the server port number and the server IP. Port numebr is 8326, and IP is [TBD]. Make sure the enter the exact port number and IP address!

### Request Format
Your client code will send three types of requests to the server. The first is the request for user login, the second one is the request to fetch the message board, and last but not lease, the request to send a new message. The requests need to follow the exact fomat: 

- For login: "LOGIN:\<username\>:\<password\>"
- For fetch the message board: "FETCH:"
- for sending new message: "MESSAGE:\<username\>:\<message\>:time"
 

### Testing: 

TO test your code, open a terminal and run the command  `python lab5/client.py <ip_addr>` to start your client. The client should then be connected to the server. __The immediate thing after that is to log in with your uername and password__. The username and password should be the one you wrote in the google form. __Make sure to log in first!__ Otherwise the fetch and send message functions won't work. Contact the TAs immediately if the uername and password does not work for you. 

After logging in, you can type messages in the terminal. __Make sure to not type any special characters! (Things like !@#$%^&*())__. 

After typing the message, you will see not only your own messages, but your classmates' message history in the terminal.
	
