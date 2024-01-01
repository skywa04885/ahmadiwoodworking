FROM python:3.11.6-alpine

# Sets the environment variables.
ENV DJANGO_DEVELOPMENT=true

# Installs the build dependencies, linux headers is needed for uwsgi.
RUN ["apk", "add", "build-base", "linux-headers", "bash"]

# Set the working directory.
WORKDIR "/usr/src/app"

# Copy the files.
COPY "./" "./"

# Install all the dependencies.
RUN ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]

# Collects the static files.
RUN ["python", "manage.py", "collectstatic", "--noinput"]

# Runs the entrypoint.
CMD ["bash", "entrypoint.sh"]
