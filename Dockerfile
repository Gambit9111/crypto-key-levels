# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

ADD ./bot /app/bot
ADD .env /app/.env
ADD requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENV NAME TELEGRAM_BOT_TOKEN
ENV NAME TELEGRAM_ADMIN_ID
ENV NAME POSTGRES_DB_URL

CMD ["python", "-m", "bot"]