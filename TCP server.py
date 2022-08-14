import sys
import socket
import threading
import time

#declaring host IP for clients to connect to, port is a parameter that is chosen when starting server.py it's therefore just declared
host='127.0.0.1'

port = 0

#checking for the port parameter
if len(sys.argv[1]) > 1:
    port = int(sys.argv[1])

#create list to keep track of clients, nicknames and which sockets are bots. also have a list over what the bots are called
bots = ["cooper", "chase", "frank", "oliver"]
clients = []
nicknames = []
botSockets = []

#creating a server socket, binding the host address and the port to it and start listening for connections.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

server.listen()


#function that takes in a message sent from a client and sends it to all other clients except for the client who sent it.
def broadcast (message, clientSock):

    #sends message to everyone except client
    if clientSock in clients:
        for client in clients:
            if client is not clientSock:
                client.send(message)

    if clientSock in clients:
        for client in botSockets:
            if client is not clientSock:
                client.send(message)

    if clientSock in botSockets:
        for client in clients:
            if client is not clientSock:
                client.send(message)




#function that handles messages, gets message from client and sends it to all other clients through broadcast()
def handle(client):
    while True:
        try:
            message = client.recv(1024)

            #if server receives "SHUTDOWN" it will shut down the server by ending connections with all clients.
            if 'SHUTDOWN' in message.decode('utf-8'):
                shutdownmsg = 'SHUTDOWN'
                broadcast(shutdownmsg.encode('utf-8'), client)
                print("Chatroom closing")

                for client in clients:
                    client.close()
                    break
            else:
                broadcast(message, client)

        #exception for if anything were to happen while sending messages, will cut the connection with the client and broadcast their departure.
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat...'.encode('utf-8'), client)
            nicknames.remove(nickname)
            break


#receives and accepts client connection, receives nickname from client and adds it to the nicknames list
def receive():
    while True:
        client, addr = server.accept()
        print (f"Connected with {str(addr)}")

        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        #registering client as bot
        if nickname in bots:
            botSockets.append(client)

        #prints nickname of client to server and tells other clients that a new client has joined the chatroom.
        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} has joined the chat!'.encode('utf-8'), client)


        #thread that handles messages from client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

#prints that the server is operational and is waiting for client connections, runs receive function to receive messages from client/bot.
print("Chatroom is waiting for chatters")
receive()
