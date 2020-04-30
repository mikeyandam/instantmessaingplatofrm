"""
CSE 3461 Project 1: Instant Messaging Platform - Using STREAM
By: Mike Yandam (yandam.4)

Note: Used the sample2_server.py on Carmen and Section 2.7.2 (Socket Programming with TCP) as a starting point

The select.select.pdf was very helpful with figuring out how to handle multiple client requests. 
"""
import select, socket, sys, Queue

####SERVER SETUP BEGIN####

#List of ERROR Messages that will be used
error_message_general = "\n**ERROR: Command entered is not valid.**\n"
error_message_user_exists = "\n**ERROR: Username entered already exists. Choose a new one!**\n"
error_message_incorrect_login_credentials = "\n**ERROR: Login credentials are incorrect!**\n"
error_message_sender_and_recep_same = "\n**ERROR: You can't send a message to yourself!**\n"
error_message_sender_not_logged_in = "\n**ERROR: You must be signed in to send a message!**\n"
error_message_recep_not_logged_in = "\n**ERROR: Can't send message to user because they are not logged in!**\n"
error_message_client_not_logged_in = "\n**ERROR: You are currently not signed in!**\n"
error_message_login_twice = "\n**ERROR: You are already logged in! If you wish to login to another account please logout first.**\n"
error_message_user_does_not_exist = "\n**ERROR: This username does not exist!**\n"
error_message_client_is_already_logged_in = "\n**ERROR: This user is already logged in!**\n"

#Text file that will hold usernames and passwords
file_list_of_users = "list_of_clients.txt"

#Create server socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

#Get host's IP and choose a port
HOST_IP = socket.gethostbyname(socket.gethostname());
PORT = 5001

#Bind server socket
server.bind((HOST_IP, PORT))

#Server listen for TCP connection requests from the client
server.listen(5)

#List of client slients that we are going to read from
inputs = [server, sys.stdin]
queue_of_clients = {}
####SERVER SETUP END####

print("The server IP address is: {}".format(HOST_IP))
print("The server is ready to receive input from connected clients. ")

#A list of protocols I have defined that the clients will use to interact with the application
def print_protocol_to_client(s):
    message= "\nWeclome to Mike's Instant Messaging Platform! \n"\
    "---------------------------------------------\n"\
    "NOTE: Arguments found between [ ] will be provided by the user. DO NOT include the [ ]\n"\
    "--------------------------------------------------------------------------------------\n"\
    "If you are a new user please create an account by typing the following: \n"\
    "1 [your_user_name] [your_password]\n"\
    "-------------------------------------------------------------------------\n"\
    "If you're an exisiting user please login by typing the following: \n"\
    "2 [your_user_name] [your_password] \n"\
    "--------------------------------------------------------------------\n"\
    "If you would like to send a message to an individual user type the following: \n"\
    "3 [user_name] [message] \n"\
    "----------------------------------------------------------------------------\n"\
    "If you would like to see a list of current users type the following: \n"\
    "4\n"\
    "-------------------------------------------------------------------\n"\
    "If you would like to logout, type the following: \n"\
    "5\n"\
    "------------------------------------------------\n"\
    "Type 6 to exit the platform!\n"\
    "--------------------------------\n"

    s.send(message)

#Helper function used in order to determine if a username already exists
def does_user_exisit(user_name):
    try:
        with open(file_list_of_users) as x:
            for line in x:
                user_name_returned = line.split()
                if (user_name_returned[0]==user_name):
                    return True
        return False
    except IOError:
        #If the file doesn't exist it means that the username does not exist so return false
        return False;
    

#Helper function that checks to see if login creditionals are correct for authentication
def correct_login_credentials(user_name,password):
        with open(file_list_of_users) as x:
            for line in x:
                user_name_returned = line.split()
                if (user_name_returned[0]==user_name):
                    if(user_name_returned[1]==password):
                        return True
                    else:
                        return False

#Helper function to check if a user is logged in
def isClientLoggedIn(s):
    if (s in queue_of_clients):
        return True
    else:
        return False

#Function that adds the username and password to a file. Creates a file if the file doesn't exists. 
def create_new_user(user_name, password,s):
    try:
        #If the file that stores username/password exists, then append information to file
        file = open(file_list_of_users, "a+")
        if not does_user_exisit(user_name):
            file.write(user_name + " " + password + "\n")
            s.send("\nCongratulations! User " + user_name + " created.\n\nLog in in order to use other funcationality.\n\n")    
        else:
                s.send(error_message_user_exists)
        file.close()
    except: 
        #If file that stores username/password doesn't exists, then create the file and write to it
        file = open(file_list_of_users, 'w')
        file.write(user_name + " " + password + "\n")
        s.send("\nCongratulations! User " + user_name + " created.\n\nLog in in order to use other funcationality.\n\n")    
        file.close()

#Function that will login user
def login_user(user_name, password,s):
    if does_user_exisit(user_name) and correct_login_credentials(user_name,password):
        #Check to see if the user isn't already logged in. If they are already logged in on a different machine display error message
        for key, value in queue_of_clients.iteritems():
            if user_name == value:
                s.send(error_message_client_is_already_logged_in)
                return;
        queue_of_clients[s] = user_name
        print("\n*************************************************")
        print(user_name + " has successfully logged in!")
        print("Total amount of currently logged in users: " + str(len(queue_of_clients)))
        print("*************************************************\n")
        s.send("\n" + user_name + " has logged in successfully!\n\n")
    elif not does_user_exisit(user_name):
        s.send(error_message_user_does_not_exist)
    else:
        s.send(error_message_incorrect_login_credentials)


#Function that will print out an alphabetical list of currently logged in users and display the total amount of active users 
def list_all_online_clients(s):
    list_of_all_online = "\nThe following users are currently logged in!\n"\
    "--------------------------------------------\n"
    #Print out all client username's in alphabetical order for ease of use
    for key, value in sorted(queue_of_clients.iteritems(),key = lambda kv:(kv[1], kv[0])):
        list_of_all_online += value + "\n"
    list_of_all_online += "\nTotal amount of currently logged in users: " + str(len(queue_of_clients))
    list_of_all_online += "\n----------------------------------------------\n"

    s.send(list_of_all_online)

#Function that will send a message written by one client to another client
def client_to_client_message(s, recipient, message):
    complete_message = "\n\n<FROM "
    sender_username = queue_of_clients[s]
    #Prevent user from sending message to themselves
    if sender_username==recipient:
        s.send(error_message_sender_and_recep_same)
    else:
        recipient_socket = None
        #Find the socket for the recipient client 
        for key, value in queue_of_clients.iteritems():
            if recipient == value:
                recipient_socket = key
        #If recipient client sock has been found send message
        if recipient_socket is not None:
            complete_message+=sender_username + " >: " + message + "\n\n"
            recipient_socket.send(complete_message)
            s.send("Message to " + recipient + " has sent successfully!")
        #If the recipent is not logged in send error message
        else:
            s.send(error_message_recep_not_logged_in)
    
#Function that handles logout request or disconnect from client
def logout_or_disconnect(s,logout_requested):
    #Check to see if client is logged in
    if (isClientLoggedIn(s)):
        #Check to see if the logged in client has requested to logout
        if (logout_requested):
            print("\n*************************************************")
            print(queue_of_clients[s] + " has successfully logged out!")
            del queue_of_clients[s]
            print("Total amount of currently logged in users: " + str(len(queue_of_clients)))
            print("*************************************************\n")
            s.send("\nYou have logged out successfully!\n")
        #Logged in client unexecpted disconnected
        else:
            inputs.remove(s)
            s.close()
            print(queue_of_clients[s] + " has disconnected!")
            del queue_of_clients[s]
    #A client who is not logged in has disconnected unexpectedly
    else:
        s.close()
        inputs.remove(s)
        print("A client has discconected unexpectedly!")
       

#Function that parses the client's input and then calls the appropriate function     
def parse_client_input(command_entered,s):
    #Parse command if the length is 1
    if len(command_entered) == 1:
        if(command_entered[0]=="0"): #Print the protocol list
            print_protocol_to_client(s)
        elif command_entered[0]=="4": #lists all logged in users
            list_all_online_clients(s)
        elif command_entered[0] =="5": #Log out user
            #Client must be logged in first in order to log out 
            if (isClientLoggedIn(s)):
                logout_or_disconnect(s, True)
            else:
                s.send(error_message_client_not_logged_in)
        else:
                s.send(error_message_general)
    #Parse command if the length is 3
    elif len(command_entered)==3:
        if command_entered[0]=="1": #Create a new user
            create_new_user(command_entered[1], command_entered[2],s)
        elif command_entered[0]=="2": #login a user
            #Check to make sure the client doesn't log in twice
            if (not isClientLoggedIn(s)):
                login_user(command_entered[1],command_entered[2],s)
            else:
                s.send(error_message_login_twice)
        elif command_entered[0]=='3': #Send a message to a logged in client
            #Client must be logged in to send a message
            if (isClientLoggedIn(s)):
                client_to_client_message(s, command_entered[1], command_entered[2])
            else:
                s.send(error_message_sender_not_logged_in)
    #If command entered is larger 3 or more individual tokens
    elif (len(command_entered) > 3):
        #Send a message to a logged in client
        if command_entered[0]=='3': 
            #Client must be logged in to send a message
            if (isClientLoggedIn(s)):
                #Contructs the full message
                full_message = ""
                for y in range(2, len(command_entered)):
                    full_message += " " + command_entered[y]
                client_to_client_message(s, command_entered[1], full_message)
        else:
            s.send(error_message_general)
    #Return error message
    else:
        s.send(error_message_general)


while inputs:
    readable, writable, exceptional = select.select(
        inputs, inputs, inputs)
    # this stanza handles connection requests. 
    for s in readable:
        if (s is server):
            print "received a connect requst from a client "
            connectionSocket, clientAddress = s.accept()
            #initially sockets are set to blocking. Passing the value of 0 will set the socket to non-blocking mode.
            connectionSocket.setblocking(0)
            inputs.append(connectionSocket)
        else:
            data = s.recv(1024)
            if data:
                parse_client_input(data.split(),s)
            else:
                logout_or_disconnect(s, False)
    for s in exceptional:
        inputs.remove(s)
        s.close()