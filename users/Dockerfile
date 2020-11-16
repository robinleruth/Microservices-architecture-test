FROM python:3.7-alpine

RUN apk add --no-cache gcc musl-dev make build-base libffi-dev
RUN apk add build-base libtool automake

RUN adduser -D userService

WORKDIR /home/userService

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN venv/bin/python -m pip install --upgrade pip
RUN venv/bin/pip install wheel
RUN venv/bin/pip install -r requirements.txt

COPY app app
# COPY tests tests
COPY app.py run_app.sh ./

RUN chmod +x run_app.sh

RUN chown -R userService:userService ./
USER userService
EXPOSE 8080

ENTRYPOINT ["./run_app.sh"]
