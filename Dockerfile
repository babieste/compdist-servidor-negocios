FROM python:3-alpine

RUN apk add --no-cache make

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 5001

CMD make run-prd-serv-1
