 FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN apt update
 RUN apt install entr --yes
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install -r requirements.txt
 ADD . /code/
