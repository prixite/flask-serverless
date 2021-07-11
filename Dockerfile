FROM public.ecr.aws/lambda/python:3.8

WORKDIR /var/task/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD [ "app.app" ]
