import socket
import time
import sys
import random
import requests
import json

# Twitch endpoint and interval between messages to be sent
HOST = "irc.chat.twitch.tv"  # twitch irc server
PORT = 6667  # port
MESSAGE_INTERVAL = 1200  # message interval in seconds


# Checks if twitch channel is live
def isChannelLive(clientId, channel):
    url = str('https://api.twitch.tv/kraken/streams?client_id=' +
              clientId + "&channel=" + channel[1:])
    try:
        streamer_html = requests.get(url)
        streamer = json.loads(streamer_html.content)
        return streamer["_total"]
    except requests.exceptions.RequestException as e:
        print(e)
        return -1


# Connects to Twitch IRC
def connect(username, token, channel):
    s = socket.socket()
    try:
        s.connect((HOST, PORT))
        s.send("PASS {}\r\n".format(token).encode("utf-8"))
        s.send("NICK {}\r\n".format(username).encode("utf-8"))
        s.send("JOIN {}\r\n".format(channel).encode("utf-8"))
        print("Connected to twitch channel " + channel + " as " + username)
    except socket.error as e:
        print(e)
        sys.exit(1)
    return s


def main():
    if len(sys.argv) != 5:
        print("Usage: twitchbot <username> <token> <channel>")
        sys.exit(1)

    username = sys.argv[1]
    clientId = sys.argv[2]
    if sys.argv[3][:6] != "oauth:":
        token = "oauth:" + sys.argv[3]
    else:
        token = sys.argv[3]
    channel = "#" + sys.argv[4]

    s = connect(username, token, channel)

    # Loads Tanner pastas from tanner.txt file
    try:
        text_file = open("resources/tanner.txt", 'r')
        data = text_file.read()
        messages = data.split("\n")
        print("Messages loaded from tanner.txt file")
    except IOError:
        print("File tanner.txt is not available")
        sys.exit(1)

    # Replaces "Octavian", "Kripp" and "Kripparian" in Tanner pastas by
    # channel name if chanel is not nl_Kripp
    if channel != "#nl_Kripp":
        messages = [s.replace('Octavian', channel[1:]) for s in messages]
        messages = [s.replace('Kripparian', channel[1:]) for s in messages]
        messages = [s.replace('Kripp', channel[1:]) for s in messages]

    # Sends a random message from messages every MESSAGE_INTERVAL if streamer
    # is online
    while True:
        if isChannelLive(clientId, channel) > 0:
            print("Channel " + channel + " is online")
            message = random.choice(messages)
            text = "PRIVMSG {} :{}".format(channel, message)
            text = text + "\r\n"
            try:
                s.send(text.encode('utf-8'))
                print("Sent message: " + message)
            except socket.error as e:
                print(e)
        else:
            print("Channel " + channel + " is offline")

        print("Waiting " + str(MESSAGE_INTERVAL) + " seconds...")
        time.sleep(MESSAGE_INTERVAL)
        print("Time to send message!")


if __name__ == "__main__":
    main()
