import socket
import time
import sys
import random
import requests
import json
import os
import datetime


# Twitch endpoint and interval between messages to be sent
HOST = "irc.chat.twitch.tv"  # twitch irc server
PORT = 6667  # port
MESSAGE_INTERVAL_MIN = 20  # message interval in minutes
MESSAGE_INTERVAL_SEC = MESSAGE_INTERVAL_MIN * 60  # message interval in seconds

def write_to_log(message):
    # Writes messages to log file
    try:
        with open('log.log', 'a') as file:
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(date + " - " + message + "\n")
    except IOError:
        print("File tanner.txt is not available")
        sys.exit(1)
    pass


# Checks if twitch channel is live
def is_channel_live(clientId, channel):
    url = str('https://api.twitch.tv/kraken/streams?client_id=' +
              clientId + "&channel=" + channel[1:])
    try:
        streamer_html = requests.get(url)
        streamer = json.loads(streamer_html.content)
        return streamer["_total"]
    except requests.exceptions.RequestException as e:
        print(e)
        return -1


# Checks is twitch channel exists
def does_channel_exists(clientId, channel):
    url = str('https://api.twitch.tv/kraken/channels/' +
              channel[1:] + "?client_id=" + clientId)
    try:
        response = requests.get(url)
        response_content = json.loads(response.content)
        code = response_content["status"]
        return code
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


# Sends message to twitch chat through socket
def send_message(s, message, channel):
    text = "PRIVMSG {} :{}".format(channel, message)
    text = text + "\r\n"
    try:
        s.send(text.encode('utf-8'))
        return True
    except socket.error as e:
        print(e)
        return False


def main():
    if len(sys.argv) != 5:
        print("Only " + str(len(sys.argv)) + " arguments were given! \
              Usage: tannerbot <username> <client_id> <token> <channel>")
        sys.exit(1)

    username = sys.argv[1]
    clientId = sys.argv[2]
    if sys.argv[3][:6] != "oauth:":
        token = "oauth:" + sys.argv[3]
    else:
        token = sys.argv[3]
    channel = "#" + sys.argv[4].lower()

    channel_exists = does_channel_exists(clientId, channel)

    if channel_exists == 404:
        write_to_log("Channel does not exist!")
        print("Channel does not exist!")
        sys.exit(1)
    elif channel_exists == -1:
        sys.exit(1)
    else:
        write_to_log("Channel located!")
        print("Channel located!")

    s = connect(username, token, channel)

    # Loads Tanner pastas from tanner.txt file
    try:
        text_file = open("resources/tanner.txt", 'r')
        data = text_file.read()
        messages = data.split("\n")
        write_to_log("Messages loaded from tanner.txt file")
        print("Messages loaded from tanner.txt file")
    except IOError:
        print("File tanner.txt is not available")
        sys.exit(1)

    # Replaces "Octavian", "Kripp" and "Kripparian" in Tanner pastas by
    # channel name if channel is not nl_Kripp
    if channel != "#nl_Kripp" and channel != "#nl_kripp":
        messages = [m.replace('Octavian', channel[1:]) for m in messages]
        messages = [m.replace('Kripparian', channel[1:]) for m in messages]
        messages = [m.replace('Kripp', channel[1:]) for m in messages]

    # Sends a random message from messages every MESSAGE_INTERVAL_SEC if 
    # streamer is online
    while True:
        channel_live = is_channel_live(clientId, channel)
        if channel_live > 0:
            print("Channel " + channel + " is online")
            message = random.choice(messages)
            if send_message(s, message, channel):
                write_to_log("Sent message: " + message)
                print("Sent message: " + message)
        elif channel_live == 0:
            write_to_log("Channel " + channel + " is offline")
            print("Channel " + channel + " is offline")
        else:
            pass

        # Test condition for CI/CD integration
        if os.environ.get("TEST") == "1":
            print("This was a successful test")
            sys.exit(0)

        # Wait to send another message
        write_to_log("Waiting " + str(MESSAGE_INTERVAL_MIN) + " minutes...")
        print("Waiting " + str(MESSAGE_INTERVAL_MIN) + " minutes...")
        time.sleep(MESSAGE_INTERVAL_SEC)
        write_to_log("Time to send message!")
        print("Time to send message!")


if __name__ == "__main__":
    main()
