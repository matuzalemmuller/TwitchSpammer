FROM python:3.7.2-alpine

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

CMD python3 twitchspammer.py $USERNAME $CLIENT_ID $OAUTH $CHANNEL