FROM python:3.10

WORKDIR /usr/src/app

# buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y install cron

# Copy hello-cron file to the cron.d directory
COPY cron_updates/updates-cron /etc/cron.d/updates-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/updates-cron

# Apply cron job
RUN crontab /etc/cron.d/updates-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app

RUN pip install -r requirements.txt

COPY . /usr/src/app
