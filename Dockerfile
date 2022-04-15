FROM python:3.10.4-alpine3.15

COPY twitchspammer.py /app/
COPY requirements.txt /app/

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD if [ -n "$INTERVAL" ]; then               \
        python3 twitchspammer.py              \
            --username=$USERNAME              \
            --oauth=$OAUTH                    \
            --channel=$CHANNEL                \
            --interval=$INTERVAL              \
            --messages=/messages/messages.txt;\
    else                                      \
        python3 twitchspammer.py              \
            --username=$USERNAME              \
            --oauth=$OAUTH                    \
            --channel=$CHANNEL                \
            --messages=/messages/messages.txt;\
    fi