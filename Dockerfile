FROM python:3.12.0a7-alpine3.18

RUN pip install --upgrade pip
RUN pip install fastapi
RUN pip install python-dotenv
RUN pip install pyjwt
RUN pip install pymongo
RUN pip install requests