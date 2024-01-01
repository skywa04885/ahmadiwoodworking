FROM python:3.11.6-alpine

ENV DJANGO_DEVELOPMENT=true

RUN ["apk", "add", "build-base", "linux-headers", "bash", "nginx"]

COPY "./entrypoint" "/bin/entrypoint"

WORKDIR "/etc/nginx"

COPY "./nginx" "./"

#
WORKDIR "/usr/src/app"

# Copy the app.
COPY "./app" "./"

# Install all the requirements.
RUN ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]

# Collect all the static files and compress them.
RUN ["python", "manage.py", "collectstatic", "--noinput"]
RUN ["python", "manage.py", "compress"]

# Run the entrypoint script.
CMD ["bash", "/bin/entrypoint"]
