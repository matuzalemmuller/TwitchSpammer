# TannerBot
*Hosted at [GitHub](https://github.com/matuzalemmuller/TannerBot) and mirrored to [GitLab](https://gitlab.com/matuzalemmuller/tannerbot).*

## Description

This project sends Tanner messages to a Twitch channel using your account. The messages are by default addressed to [Kripparian](https://www.twitch.tv/nl_kripp), but they will be addressed to any other streamer by calling them by the channel name. Messages are sent every 20 minutes to not flood the chat.

## Who is Tanner?

Definitely not a streamer. Why tell you, when I can [show you](https://www.reddit.com/r/LivestreamFail/comments/9qb1f8/tanner_jebaits_kripp/)?

## Instructions

In order to run this code, you need to register an application in Twitch so you can get the client information to connect the bot to your account. More information on what is needed to run the bot below.

To run TannerBot, simply download this repo, install the dependencies and run the code.

```
pip3 install -r requirements.txt
python3 tannerbot.py <username> <client_id> <token> <channel>
```

* Username: Your Twitch username.
* Client_Id: You need to create an app in the Twitch developer portal to get a `client_id`. More information in the [docs](https://dev.twitch.tv/docs/v5/#getting-a-client-id).
* OAuth token: You can use [this page](https://twitchapps.com/tmi/) to get an OAuth token or check the [docs](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/) to learn how to manually create one.
* Channel: Channel that you wish to send messages to.

Example:

```
python3 tannerbot.py TannerBot xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx oauth:yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy channel_name
```

A container version of the app is also available in the [registry](https://gitlab.com/matuzalemmuller/tannerbot/container_registry). To run the container, you must run the following code:

```
docker run --env USERNAME=username \
           --env CLIENT_ID=client_id \
           --env OAUTH=token \
           --env CHANNEL=channel \
           -d matuzalemmuller/tannerbot:v0.1
```
