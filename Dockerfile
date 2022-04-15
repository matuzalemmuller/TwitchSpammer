FROM python:3.10.4-alpine3.15

COPY twitchspammer.py /app/
COPY requirements.txt /app/

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD if [[ -n "$INTERVAL" && -d /log ]]; then   \
        python3 twitchspammer.py               \
            --username=$USERNAME               \
            --oauth=$OAUTH                     \
            --channel=$CHANNEL                 \
            --messages=/messages/messages.txt  \
            --interval=$INTERVAL               \
            --log=/log/twitchspammer.log       \
            2>&1;                              \
     elif [ -d /log ]; then                    \
        python3 twitchspammer.py               \
            --username=$USERNAME               \
            --oauth=$OAUTH                     \
            --channel=$CHANNEL                 \
            --messages=/messages/messages.txt  \
            --log=/log/twitchspammer.log       \
            2>&1;                              \
    elif [ -n "$INTERVAL" ]; then              \
        python3 twitchspammer.py               \
            --username=$USERNAME               \
            --oauth=$OAUTH                     \
            --channel=$CHANNEL                 \
            --messages=/messages/messages.txt; \
            --interval=$INTERVAL               \
            2>&1;                              \
    else                                       \
        python3 twitchspammer.py               \
            --username=$USERNAME               \
            --oauth=$OAUTH                     \
            --channel=$CHANNEL                 \
            --messages=/messages/messages.txt  \
            2>&1;                              \
    fi