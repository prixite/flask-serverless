FROM amazon/aws-lambda-python:3.8

WORKDIR /var/task

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . ./

CMD [ "wsgi_handler.handler" ]
