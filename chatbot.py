import socket
import time
import sys
import urllib.request
import random

# Twitch endpoint and interval between messages to be sent
HOST = "irc.chat.twitch.tv"  # twitch irc server
PORT = 6667  # port 
MESSAGE_INTERVAL = 1200 # message interval in seconds


# Checks if twitch channel is live
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
    if sys.argv[3][:6] != "oauth:":
        token = "oauth:" + sys.argv[3]
    else:
        token = sys.argv[3]
    channel   = "#" + sys.argv[4]

    socket = connect(username, token, channel)

    # Loads Tanner pastas from tanner.txt file
    text_file = open("tanner.txt",'r')
    data = text_file.read()
    messages = data.split("\n")

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
            text = "PRIVMSG {} :{}".format(channel, random.choice(messages))
            text = text + "\r\n"
            socket.send(text.encode('utf-8'))
        time.sleep(MESSAGE_INTERVAL)


if __name__ == "__main__":
    main()