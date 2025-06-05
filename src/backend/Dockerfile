FROM python:3.12-slim
# Set the working directory
WORKDIR /app
# Copy the requirements file into the container
COPY . /app
COPY db_config.py /app/config/
# Install the required packages
RUN apt-get update && \
    apt-get install -y bash 

RUN pip install -r requirements.txt
RUN pip install -e .

# Expose the port the app runs on
EXPOSE 8000

CMD [ "python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]
