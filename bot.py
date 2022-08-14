import random


#defining bots and what their outputs will be. these functions are called upon through botResponse when a call for their name is made
def cooper (a, b = None):
    nickname = "Cooper"

    if "Hei" in a:

        return nickname + " : Sup"

    else:

        # loops through the actions list and tries to find the action in the string a
        for action in actions:

            #if an action is found, saves in verb and returns a statement with the suggested action from user
            if action in a:
                verb = action

                return nickname + " : I think {} sounds great!".format(verb + "ing")

        #no match for action found or misinterpreted, sends generic statement instead.
        else:
            return nickname + " : Sorry I didn't catch that."



def chase (a, b = None):

    nickname = "Chase"

    if "Hei" in a:
        return nickname + " : Hello"
    else:

        for action in actions:
            if action in a:
                verb = action

                return nickname + " : Hell no! You will never see me {}!".format(verb + "ing")

        else:
            return nickname + " : I don't understand."

def frank (a, b = None):
    nickname = "Frank"

    #alternative to what user suggested
    b = random.choice(actions)

    if "Hei" in a:
        return nickname + " : Hello"
    else:

        #same loop that checks if it can find an action in a that matches anything in the actions list
        for action in actions:
            if action in a:

                #in this case, if the randomly picked action from b matches a, we find another random one
                verb = action
                if b == verb:
                    b = random.choice(actions)

                return nickname + " : Nah, I'm not a fan of {} honestly, I'd rather do some {}".format(verb + "ing",b + "ing")

        else:
            return nickname + " : What did you mean?"

def oliver (a, b = None):
    nickname = "Oliver"

    if "Hei" in a:
        return nickname + " : Hello"
    else:

        for action in actions:
            if action in a:
                verb = action

                return nickname + " : Yeah I would like to do some {}.".format(verb + "ing")

        else:
            return nickname + " : Sorry what did you say?"


#returns the requested bot's response. the response goes to the result variable in client.py which is then sent to the server.
def botResponse(message, botName):
    if botName == "cooper":
        cooperResponse = cooper(message, None) + "\n"
        return cooperResponse

    if botName == "chase":
        chaseResponse = chase(message, None) +"\n"
        return chaseResponse

    if botName == "frank":
        frankResponse = frank(message, None) + "\n"
        return frankResponse

    if botName == "oliver":
        oliverResponse = oliver(message, None) + "\n"
        return oliverResponse


#list of verbs/actions that are pre-determined. used to find actions in strings from clients that are then used to give a response.
actions = ["sleep", "play", "fight", "hear", "yell", "complain", "chill", "sing", "kill",
           "party", "exist", "look", "eat", "cry", "scream", "design", "fly", "laugh", "hang",
           "marry", "protect", "adopt", "collect", "drink", "train", "work", "shoot", "construct",
           "arrest", "bother", "succeed", "fail", "earn", "attack", "shout", "feed", "own"]




