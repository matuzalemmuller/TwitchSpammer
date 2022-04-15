# TwitchSpammer

This project sends pre-defined messages to a Twitch channel using your account. The messages are sent every 30 minutes, and only if the channel is live.

Watch out for Twitch's [Rate Limits](https://dev.twitch.tv/docs/irc/guide#rate-limits)!

*Disclaimer: because the communication happens over IRC, there is no way to confirm whether messages are published to the chat or not. Depending on the automod policies of the channel, rate limiting, and other factors, messages may not be published, although the logs report that messages are being sent.* 

---

## Requirements

* Python 3
* Twitch account

## Instructions

To run TwitchSpammer, simply download this repository, install the necessary dependencies, and run the code.

```
# Install dependencies
pip3 install -r requirements.txt

# Run TwitchSpammer
python3 twitchspammer.py --username=<twitch_username> \
                         --oauth_token=<oauth_token>  \
                         --channel=<channel_name>     \
                         --interval=<interval_min>    \
                         --messages=<filepath>        \
                         --log=<path_to_logfile>
```

* `username`: the Twitch username;
* `oauth_token`: the OAuth token. You can use [this page](https://twitchapps.com/tmi/) to get an OAuth token for your account or check the [official Twitch developer documentation](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/) to learn how to manually create one. The token must **not** include the `oauth:` prefix;
* `channel`: channel that you wish to send messages to;
* `messages`: file that has the messages to be sent to the channel chat. See an example on [`data/messages.txt`](./data/messages.txt);
* `interval` (optional): interval between sending messages, in minutes;
* `log` (optional): log file location. Example: `/tmp/log.log`.

---

### DockerHub

A container version of the app is also available in [DockerHub](https://hub.docker.com/r/matuzalemmuller/twitchspammer).

```
docker run --name twitchspammer                             \
           --env USERNAME=<twitch_username>                 \
           --env OAUTH=<oauth_token>                        \
           --env CHANNEL=<channel_name>                     \
           --env INTERVAL=<interval_min>                    \
           --mount type=bind,src=<src_folder>,dst=/messages \
           --mount type=bind,src=<src_folder>,dst=/log      \
           matuzalemmuller/twitchspammer:latest
```

Environment variables:

* `USERNAME`: the Twitch username;
* `OAUTH`: the OAuth token. You can use [this page](https://twitchapps.com/tmi/) to get an OAuth token for your account or check the [official Twitch developer documentation](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/) to learn how to manually create one. The token must **not** include the `oauth:` prefix;
* `CHANNEL`: channel that you wish to send messages to;
* `INTERVAL` (optional): the interval between sending messages, in minutes.

Mounts:

* `/messages`: the directory that contains the file with messages to be sent (`messages.txt`);
* `/log`(optional): the directory where the logs will be saved.