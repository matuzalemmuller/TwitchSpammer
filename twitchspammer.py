import datetime
import json
import logging
import os
import random
import requests
import socket
import sys
import time
from logging.handlers import RotatingFileHandler

# Twitch endpoint and interval between messages to be sent
HOST = "irc.chat.twitch.tv"  # twitch irc server
PORT = 6667  # port
MESSAGE_INTERVAL_MIN = 35  # message interval in minutes
MESSAGE_INTERVAL_SEC = MESSAGE_INTERVAL_MIN * 60  # message interval in seconds

# Starts logging handler
def start_logger():
    formatter = '%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s'
    log_formatter = logging.Formatter(formatter)
    logFile = 'log.log'

    my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                     backupCount=2, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)

    app_log = logging.getLogger('root')
    app_log.setLevel(logging.DEBUG)

    app_log.addHandler(my_handler)

    return app_log

# Checks if twitch channel exists and if it is live
def is_channel_live(clientId, channel, logger):
    id_url = str('https://api.twitch.tv/helix/users?login=' + channel)
    header = {'Client-ID' : clientId}

    try:
        requests_id = requests.get(id_url, headers=header)
        json_data = json.loads(requests_id.content)
        channel_exists = len(json_data['data'])
        if channel_exists == 0:
            logger.error("Channel does not exist!")
            print("Channel does not exist!")
            sys.exit(1)

        list_data = json_data['data'][0]
        login_id = list_data.get('id', "0")

        stream_url = 'https://api.twitch.tv/helix/streams?user_id=' + login_id
        requests_stream = requests.get(stream_url, headers=header)
        json_data = json.loads(requests_stream.content)
        is_online = len(json_data['data'])
        if is_online > 0:
            return 1
        else:
            return 0
    except requests.exceptions.RequestException as e:
        logger.error(e)
        print(e)
        return -1

# Connects to Twitch chat and sends message to twitch chat through socket
def send_message(message, channel, token, username, logger):
    s = socket.socket()
    channel = "#"+channel
    text = "PRIVMSG {} :{}".format(channel, message)
    text = text + "\r\n"
    try:
        s.connect((HOST, PORT))
        s.send("PASS {}\r\n".format(token).encode("utf-8"))
        s.send("NICK {}\r\n".format(username).encode("utf-8"))
        s.send("JOIN {}\r\n".format(channel).encode("utf-8"))
        s.send(text.encode('utf-8'))
        s.close()
        return True
    except socket.error as e:
        logger.error(e)
        print(e)
        return False

def main():
    logger = start_logger()
    logger.info("Starting TwitchSpammer")
    
    if len(sys.argv) != 5:
        print("Only " + str(len(sys.argv)) + " arguments were given! \
              Usage: twitchspammer <username> <client_id> <token> <channel>")
        logger.error("Invalid arguments")
        sys.exit(1)

    username = sys.argv[1]
    clientId = sys.argv[2]
    if sys.argv[3][:6] != "oauth:":
        token = "oauth:" + sys.argv[3]
    else:
        token = sys.argv[3]
    channel = sys.argv[4].lower()

    # Loads messages from messages.txt file
    try:
        text_file = open("data/messages.txt", 'r')
        data = text_file.read()
        messages = data.split("\n")
        logger.info("Messages loaded from messages.txt file")
        print("Messages loaded from messages.txt file")
    except IOError:
        logger.error("File messages.txt is not available")
        print("File messages.txt is not available")
        sys.exit(1)

    # Replaces "Octavian", "Kripp" and "Kripparian" in messages by
    # channel name if channel is not nl_Kripp
    if channel != "nl_kripp":
        messages=[m.replace('Octavian', channel) for m in messages]
        messages=[m.replace('"Kripparrian"','"'+channel+'"') for m in messages]
        messages=[m.replace('Kripp', channel) for m in messages]

    # Sends a random message from messages every MESSAGE_INTERVAL_SEC if 
    # streamer is online
    while True:
        channel_live = is_channel_live(clientId, channel, logger)
        if channel_live > 0:
            logger.info("Channel " + channel + " is online")
            print("Channel " + channel + " is online")
            message = random.choice(messages)
            if send_message(message, channel, token, username, logger):
                logger.info("Sent message: " + message)
                print("Sent message: " + message)
        elif channel_live == 0:
            logger.info("Channel " + channel + " is offline")
            print("Channel " + channel + " is offline")
        else:
            pass

        # Wait to send another message
        logger.info("Waiting " + str(MESSAGE_INTERVAL_MIN) + " minutes...")
        print("Waiting " + str(MESSAGE_INTERVAL_MIN) + " minutes...")
        time.sleep(MESSAGE_INTERVAL_SEC)
        logger.info("Time to send message!")
        print("Time to send message!")

if __name__ == "__main__":
    main()
