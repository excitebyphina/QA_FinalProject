FROM python:3.10-slim-buster
ADD . /students
WORKDIR /students
COPY .  .
RUN pip install flask
CMD [ "python", "app.py" ]

