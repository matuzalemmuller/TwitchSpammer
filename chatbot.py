import socket
import time
import sys
import urllib.request
import json
import ast
import random

# Account parameters used to connect to Twitch
HOST = "irc.chat.twitch.tv"  # the twitch irc server
PORT = 6667  # always use port 6667

def isChannelLive(clientId, channel):
    url = str('https://api.twitch.tv/kraken/streams?client_id='+
              clientId + "&channel=" + channel[1:])
    try:
        result = urllib.request.urlopen(url)
        result_decoded = result.read().decode("utf-8")
        return int(result_decoded[10])
    except urllib.error.URLError as e:
        print(e.reason)
        return -1


# Connects to Twitch IRC
def connect(username, token, channel):
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send("PASS {}\r\n".format(token).encode("utf-8"))
    s.send("NICK {}\r\n".format(username).encode("utf-8"))
    s.send("JOIN {}\r\n".format(channel).encode("utf-8"))
    return s


def main():
    if len(sys.argv) != 5:
        print("Usage: twitchbot <username> <token> <channel>")
        sys.exit(1)

    username  = sys.argv[1]
    clientId = sys.argv[2]
    token     = "oauth:" + sys.argv[3]
    channel   = "#" + sys.argv[4]

    socket = connect(username, token, channel)

    # Loads tanner pastas from tanner.txt file
    text_file = open("tanner.txt",'r')
    data = text_file.read()
    messages = data.split("\n")

    # Replaces "Octavian", "Kripp" and "Kripparian" from Tanner pastas
    if channel != "#nl_Kripp":
        messages = [s.replace('Octavian', channel[1:]) for s in messages]
        messages = [s.replace('Kripparian', channel[1:]) for s in messages]
        messages = [s.replace('Kripp', channel[1:]) for s in messages]

    while True:
        if isChannelLive(clientId, channel) > 0:
            text = "PRIVMSG {} :{}".format(channel, random.choice(messages))
            text = text + "\r\n"
            socket.send(text.encode('utf-8'))
        time.sleep(1200)


if __name__ == "__main__":
    main()