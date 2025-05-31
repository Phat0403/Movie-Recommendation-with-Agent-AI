FROM ghcr.io/astral-sh/uv:debian
# Set the working directory
WORKDIR /app
# Copy the requirements file into the container
COPY . /app
# Install the required packages
RUN apt-get update && \
    apt-get install -y bash
# Install Python
RUN uv python install 3.12.