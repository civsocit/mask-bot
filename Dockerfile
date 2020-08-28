FROM python:3.8-buster

COPY ./src /app

COPY ./config.py /app/config.py

COPY ./masks /app/masks

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "bot.py" ]
