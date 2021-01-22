FROM python:3.8-slim

RUN mkdir src
COPY . ./src
RUN pip3 install --upgrade pip
WORKDIR /src
RUN pip3 install --no-cache-dir -r requirements.txt

CMD  ["python", "./main.py"]