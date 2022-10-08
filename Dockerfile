FROM python:3.6
ADD . /blueprint
WORKDIR /blueprint
COPY . .
RUN pip install Flask
RUN pip install flask_wtf
RUN pip install wtForms
RUN pip install flask_SQLAlchemy
CMD [ "python", "./app.py" ]
EXPOSE 5000