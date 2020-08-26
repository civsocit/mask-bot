FROM python:3.8-buster

COPY ./src /app

COPY ./config.py /app/config.py

COPY ./logos /app/logos

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "bot.py" ]
