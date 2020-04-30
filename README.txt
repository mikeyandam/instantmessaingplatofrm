By: Mike (Micheal) Yandam.4

****List of Files****:
1)client.py: Code that handles connection to server and send/receive messages from server.
2)server.py: Code that handles client connection and manage incoming client requests.
3)list_of_clients.txt: File that holds a list of client's username and password. Stored in the plain text. RIP to client security :(.
This txt file is generated if it does not exist initially. 

****List of Features****: 
1)Multi-user IM platform: Server is able to handle multiple connections from multiple clients.
2)Client registry: Server registers clients with [username] and [password]. If client with [username]
exists then the server will send an error message. Server keeps track of clients by adding them to a file "list_of_clients.txt"
3)Online clients: User can see a list of LOGGED in clients
3a)List of online users will be in alphabetical order so it's easy to read 
4)Logged in clients can send messages to other logged in clients
5)Useful information is displayed in the server's terminal: It will print a message to the server's console if a user logged in or out and then displays the current logged in user count. 
7)Helpful error messages to guide user through application

****How to run****
NOTE: 
-In order to run this application, machines must be on the same network. 
-Server must be running first.
-Clients must use the IP address displayed in server's terminal.
-IP address that client enters is assumed to be correct.

1)SERVER:
To run the server, type the following in the terminal:
python server.py

The server will then print out an IP address that the server will be hosted on. Have the user who runs 
the server send theis IP address to the clients who plan to use the IM application. 

2)CLIENT:
To run the client, type the following in the terminal:
python client.py

The application will then ask for the IP address which was printed when the server.py was run. 
Paste this IP address in the client terminal. 

To see a list of the accepted commands type 0 in the client terminal and you will see the following:

Weclome to Mike's Instant Messaging Platform! 
---------------------------------------------
NOTE: Arguments found between [ ] will be provided by the user. DO NOT include the [ ]
--------------------------------------------------------------------------------------
If you are a new user please create an account by typing the following: 
1 [your_user_name] [your_password]
-------------------------------------------------------------------------
If you're an exisiting user please login by typing the following: 
2 [your_user_name] [your_password] 
--------------------------------------------------------------------
If you would like to send a message to an individual user type the following: 
3 [user_name] [message] 
----------------------------------------------------------------------------
If you would like to see a list of current users type the following: 
4
-------------------------------------------------------------------
If you would like to logout, type the following: 
5
------------------------------------------------
Type 6 to exit the platform!
--------------------------------
