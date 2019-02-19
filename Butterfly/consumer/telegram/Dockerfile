FROM python:alpine3.7
WORKDIR /app
COPY ./TelegramConsumer.py /app
RUN pip3 install --upgrade pip ; pip3 install telepot ; pip3 install kafka
EXPOSE 5000
CMD python3 TelegramConsumer.py
