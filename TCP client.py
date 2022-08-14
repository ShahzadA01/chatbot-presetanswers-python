import socket
import time
import threading
import sys
from bot import botResponse                                     #importing the bot functions from bot.py

nickname = ""                                                   #initializing nickname that the user chooses

bots = ["cooper", "chase", "frank", "oliver"]                   #bot-list to keep track of the chatbots
host = ""                                                       #initializing host parameter
port = 0                                                        #initializing port parameter
bot = ""                                                        #initializing bot parameter


#taking in parameters for when client.py gets ran - sys.argv[1] is the ip, while 2 is the port and 3 is the optional "bot"
#using len() to check if the field for parameters was left empty or if it has anything in it.

if len(sys.argv[1]) > 1:
    host = str(sys.argv[1])


if len(sys.argv[2]) > 1:
    port = int(sys.argv[2])


try:                                                            #try/except where we're checking if the bot parameter was given
    len(sys.argv[3]) > 1                                        #if no value was given, the client connecting is not a bot.

except:
    bot = ""

else:
    bot = sys.argv[3]

if bot.lower() in bots:
    nickname = bot                                              #checks if the bot parameter is given by checking in the bots list
                                                                #if it's found, we know the bot joining the client is a bot, therefore
                                                                #the nickname is whatever the bot joining is called
else:
    nickname = input("Choose a nickname: ")  # asks user to give their username to display in the chatroom


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #creating a client socket and connecting to the server
client.connect((host, port))

client.send(nickname.encode('utf-8'))                           #sends the clients nickname to the server, that way the server can keep track of clients



#receive function that takes in messages coming from the server, decodes it and prints it for the user to see
def receive():
    #tries to receive a message, prints for client
    while True:
        try:

            message = client.recv(1024).decode('utf-8')
            print(message)

            #splitting the string to look for nicknames
            first_word = (message.lower()).split()

            #checking if the nickname is in bots, if not we ask for the bot's response
            if nickname.lower() in bots and first_word[0] not in bots:

                #gets result from botResponse() and sends result to the server.
                result = botResponse(message, nickname.lower())
                result = result.encode('utf-8')
                client.send(result)

        #exception for if receiving messages goes wrong, closes connection with client
        except:
            if 'SHUTDOWN' in client.recv(1024).decode('utf-8'):
                print("Chatroom has shutdown")

            print("An error has occurred!")
            client.close()
            break


#write function. only sends a message to the server if the person trying to send a message isn't a bot.
def write():

    while True:

        #checks if person trying to send message is a bot, only allows non-bots to send messages
        if nickname.lower() not in bots:

            message = input(f'{nickname} : ')

            #if user types in the command /shutdown, will tell the server to shut down.
            if "/shutdown" in message.split(" : "):
                client.send('SHUTDOWN'.encode('utf-8'))
            else:
                client.send(f'{nickname}: {message}'.encode('utf-8'))
            time.sleep(1)




#threads that handles receiving and writing messages in parallel so that we don't have to wait for actions to finish.
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

