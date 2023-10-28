FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip 
RUN pip install --upgrade setuptools
WORKDIR /app

COPY requirements.txt /app/

RUN pip install  -r requirements.txt

COPY . /app/

EXPOSE 8000

ENV NAME World

CMD ["python", "manage.py", "runserver" , "0.0.0.0:8000"]
