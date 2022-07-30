FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

# copy startupp script
COPY ./compose/local/django/start /start
RUN chmod +x /start

# copy shell script
COPY ./compose/local/django/shell /bin/shell_start
RUN chmod +x /bin/shell_start