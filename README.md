# TwitchSpammer
*Hosted at [GitHub](https://github.com/matuzalemmuller/twitchspammer) and mirrored to [GitLab](https://gitlab.com/matuzalemmuller/twitchspammer).*

## Description

This project sends pre-defined messages to a Twitch channel using your account. The messages are sent every 35 minutes to not flood the chat.

Watch out for Twitch's [Command & Message Limits](https://dev.twitch.tv/docs/irc/guide#command--message-limits)!

## Requirements

* Python 3
* Twitch account to register the application and send messages

## Instructions

In order to run this code, you need to register an application in Twitch to get the client information and connect the bot to your account. More information on what is needed to run the bot below.

To run TwitchSpammer, simply download this repo, install the dependencies and run the code.

```
pip3 install -r requirements.txt
python3 twitchspammer.py <username> <client_id> <token> <channel>
```

* Username: Your Twitch username.
* Client_Id: You need to create an app in the Twitch developer portal to get a `client_id`. More information in the [docs](https://dev.twitch.tv/docs/v5/#getting-a-client-id).
* OAuth token: You can use [this page](https://twitchapps.com/tmi/) to get an OAuth token or check the [docs](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/) to learn how to manually create one.
* Channel: Channel that you wish to send messages to.

You can also customize the messages sent by modifying the file `data/messages.txt`.

----

Example:

```
python3 twitchspammer.py my_twitch_username xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx oauth:yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy channel_name
```
