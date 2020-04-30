"""
CSE 3461 Project 1: Instant Messaging Platform - Using STREAM
By: Mike Yandam (yandam.4)

Note: Used the sample2_client.py on Carmen and Section 2.7.2 (Socket Programming with TCP) as a starting point
"""
import select, socket, sys, Queue

#### CLIENT SETUP BEGIN ####
#Create client socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Get IP Address of server
ip_of_server = raw_input("What is the IP address of the server you wish to connect to?: ")

#Port Number 
port_of_server = 5001

#Initiate the TCP connection between the client and server
client.connect((ip_of_server, port_of_server))

#### CLIENT SETUP END ####

#maintains a list of possible input streams
inputs = [sys.stdin, client]

print("Enter 0 if you would like to see a list of commands!")
sys.stdout.write("Enter your command -> ")
sys.stdout.flush()

while inputs: 
    readable, writeable, exceptional = select.select(inputs, inputs, inputs)
    for sockets in readable:
        #Got something from the netwwork/server
        if sockets is client:
            #Took me forever to understand why my protocol was printing weird. I had to upgrade from size from 1024->4096
            message = client.recv(4096)
            #Valid data recieved 
            if message:
                print(message)
                print("Enter 0 if you would like to see a list of commands!")
                sys.stdout.write("Enter your command -> ")
                sys.stdout.flush()
            #Case if server is ended while client is still connected
            else:
                print("\n\n**Issue with server encountered! Ending application.**\n\n")
                sys.exit()
        #Get client input
        else:
            message = sys.stdin.readline()
            #Client sending data to server
            if (message != "6\n"):
                client.send(message) 
            #Client wants to exit
            else: 
                print("\n***Thanks for using Mike's Instant Messaging Platform! Exiting now***\n")
                sys.exit()
client.close()