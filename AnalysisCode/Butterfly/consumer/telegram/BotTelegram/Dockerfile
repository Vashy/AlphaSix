FROM python:alpine3.7
WORKDIR /app
COPY sender.py requirements.txt ./app/
RUN pip3 install --upgrade pip ; pip3 install -r ./app/requirements.txt
EXPOSE 5000
CMD python ./app/sender.py
