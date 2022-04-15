#!/usr/bin/env python3
import argparse
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

HOST = "irc.chat.twitch.tv"  # twitch irc server
PORT = 6667  # port
MESSAGE_INTERVAL_MIN = 30  # message interval in minutes
MESSAGE_INTERVAL_SEC = MESSAGE_INTERVAL_MIN * 60  # message interval in seconds

# Start logging handler
def start_logger(logfile: str = None):
    formatter = (
        "%(asctime)s\t- %(levelname)s\t- %(funcName)s(%(lineno)d)\t- %(message)s"
    )
    log_formatter = logging.Formatter(formatter)

    log_handler = RotatingFileHandler(
        logfile,
        mode="a",
        maxBytes=5 * 1024 * 1024,
        backupCount=2,
        encoding=None,
        delay=0,
    )
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)

    app_log = logging.getLogger("root")
    app_log.setLevel(logging.DEBUG)
    app_log.addHandler(log_handler)

    return app_log


# Call /validate to confirm that credentials are valid and extend oauth token
def validate_credentials(username: str, oauth_token: str):
    headers = {"Authorization": "OAuth " + oauth_token}
    try:
        # https://dev.twitch.tv/docs/authentication/validate-tokens
        r = requests.get("https://id.twitch.tv/oauth2/validate", headers=headers)
        keys = r.json()

        if "client_id" in keys:
            return {
                "result": True,
                "log": "Valid credentials",
                "client_id": keys["client_id"],
            }
        else:
            return {"result": False, "log": keys["message"]}
    except requests.exceptions.RequestException as e:
        return {"result": False, "log": "Error: " + str(e)}


# Check if twitch channel exists and if it is live
def is_channel_live(client_id: str, oauth_token: str, channel: str):
    try:
        headers = {"Client-ID": client_id, "Authorization": "Bearer " + oauth_token}
        # https://dev.twitch.tv/docs/api/reference#get-streams
        stream = requests.get(
            "https://api.twitch.tv/helix/streams?user_login=" + channel,
            headers=headers,
        )
        stream_data = stream.json()

        if len(stream_data["data"]) == 1:
            return {"result": 1, "log": "Channel " + channel + " is live"}
        else:
            return {"result": 0, "log": "Channel " + channel + " is offline"}
    except requests.exceptions.RequestException as e:
        return {"result": -1, "log": "Error: " + str(e)}


# Select a message to be sent
def select_message(filepath: str):
    try:
        with open(filepath, "r") as f:
            data = f.read()
        messages = data.split("\n")
        message = random.choice(messages)
        for i in range(10):
            if message.replace(" ", "") == "":
                message = random.choice(messages)
            else:
                break
        if message.replace(" ", "") == "":
            return {"result": False, "log": "Error: No valid messages"}
        else:
            return {"result": True, "log": "Message loaded", "message": message}
    except IOError as e:
        print(e)
        return {"result": False, "log": "Error: " + str(e)}


# Send message to channel using IRC via socket
def send_message(message, channel, oauth_token, username):
    s = socket.socket()
    channel = "#" + channel
    text = "PRIVMSG {} :{}".format(channel, message)
    text = text + "\r\n"
    token = "oauth:" + oauth_token
    try:
        s.connect((HOST, PORT))
        s.send("PASS {}\r\n".format(token).encode("utf-8"))
        s.send("NICK {}\r\n".format(username).encode("utf-8"))
        s.send("JOIN {}\r\n".format(channel).encode("utf-8"))
        s.send(text.encode("utf-8"))
        s.close()
        return {"result": True, "log": "Message sent"}
    except socket.error as e:
        return {"result": False, "log": "Error: " + str(e)}


# Main loop
def main():
    # Parse arguments
    all_args = argparse.ArgumentParser()
    all_args.add_argument(
        "--oauth_token", required=True, help="OAuth token for twitch account"
    )
    all_args.add_argument(
        "--username", required=True, help="Twitch account username"
    )
    all_args.add_argument(
        "--channel", required=True, help="Name of the channel to send messages"
    )
    all_args.add_argument(
        "--messages", required=True, help="Location of file with messages to be sent"
    )
    all_args.add_argument(
        "--interval", required=False, help="Interval to send messages"
    )
    all_args.add_argument(
        "--log", required=False, help="Location of log file"
    )
    args = vars(all_args.parse_args())

    oauth_token = str(args["oauth_token"])
    username = str(args["username"])
    channel = str(args["channel"])
    filepath = str(args["messages"])
    if args["log"] != None:
        logpath = args["log"]
    else:
        logpath = "twitchspammer.log"
    if args["interval"] != None:
        global MESSAGE_INTERVAL_MIN
        MESSAGE_INTERVAL_MIN = int(args["interval"])

    # Start logger
    logger = start_logger(logpath)
    logger.info("Starting TwitchSpammer")

    # Confirm that message file exists and is not empty
    validate_messages_file = select_message(filepath=filepath)
    if validate_messages_file["result"]:
        logger.info(validate_messages_file["log"])
        print(str(datetime.datetime.now()) + " - " + validate_messages_file["log"])
    else:
        logger.error(validate_messages_file["log"])
        print(str(datetime.datetime.now()) + " - " + validate_messages_file["log"])
        sys.exit(-1)

    while True:
        # Validate/extend oauth token
        check_credentials = validate_credentials(
            username=username, oauth_token=oauth_token
        )
        if check_credentials["result"]:
            logger.info(check_credentials["log"])
            print(str(datetime.datetime.now()) + " - " + check_credentials["log"])
        else:
            logger.error(check_credentials["log"])
            print(str(datetime.datetime.now()) + " - " + check_credentials["log"])
            sys.exit(-1)
        client_id = check_credentials["client_id"]

        logger.info("Time to send message")
        print(str(datetime.datetime.now()) + " - " + "Time to send message")

        # If channel is live, send message
        channel_live = is_channel_live(
            client_id=client_id, oauth_token=oauth_token, channel=channel
        )
        if channel_live["result"] > 0:
            logger.info(channel_live["log"])
            print(str(datetime.datetime.now()) + " - " + channel_live["log"])
            message = select_message(filepath=filepath)
            if not message["result"]:
                print(str(datetime.datetime.now()) + " - " + message["log"])
                logger.error(message["log"])
                sys.exit(-1)
            logger.info(message["log"] + ": " + message["message"])
            print(
                str(datetime.datetime.now())
                + " - "
                + message["log"]
                + ": "
                + message["message"]
            )
            result = send_message(
                message=message["message"],
                username=username,
                oauth_token=oauth_token,
                channel=channel,
            )
            if result["result"]:
                logger.info(result["log"])
                print(str(datetime.datetime.now()) + " - " + result["log"])
            else:
                logger.error(result["log"])
                print(str(datetime.datetime.now()) + " - " + result["log"])
                sys.exit(1)
        elif channel_live["result"] == 0:
            logger.info(channel_live["log"])
            print(str(datetime.datetime.now()) + " - " + channel_live["log"])
        else:
            logger.error(channel_live["log"])
            print(str(datetime.datetime.now()) + " - " + channel_live["log"])
            sys.exit(-1)

        # Wait to send another message
        print(
            str(datetime.datetime.now())
            + " - "
            + "Waiting "
            + str(MESSAGE_INTERVAL_MIN)
            + " minutes..."
        )
        logger.info("Waiting " + str(MESSAGE_INTERVAL_MIN) + " minutes...")
        time.sleep(MESSAGE_INTERVAL_SEC)


if __name__ == "__main__":
    main()
