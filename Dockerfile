# Use the specified Docker Compose image based on Alpine Linux
FROM docker/compose:alpine-1.29.2

# 1. Clear the inherited ENTRYPOINT from the base image.
# The base image's ENTRYPOINT is set to 'docker-compose', which would cause it to exit immediately
# unless a docker-compose command is passed. Clearing it lets our CMD run.
ENTRYPOINT []

# Set the working directory inside the container
WORKDIR /app

# Copy the local 'app' folder into the working directory (/app) in the container
# This assumes your Dockerfile is in the same directory as the 'app' folder.
COPY app /app

# 2. Use a command that keeps the container running indefinitely in the background.
# 'tail -f /dev/null' is the most common and resource-efficient way to do this.
CMD ["tail", "-f", "/dev/null"]