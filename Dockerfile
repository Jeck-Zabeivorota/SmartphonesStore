FROM python:3.11.7

WORKDIR /app
COPY . /app/
EXPOSE 8000

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]