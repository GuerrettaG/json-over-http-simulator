FROM python:3.13.5-alpine3.21

COPY src src

CMD [ "python","-u","src/main.py" ]