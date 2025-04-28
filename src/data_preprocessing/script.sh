#!/bin/bash

# Movie Recommendation System - Spark Jobs Runner
# This script runs a Spark job using Docker

# Function to display usage information
usage() {
    echo "Usage: $0 <job_file>"
    echo "  <job_file>     Specific job file to run with Docker"
    exit 1
}

# Check if a job file is provided
if [ $# -eq 0 ]; then
    usage
fi

# Check if spark-local image exists, build if not
if ! docker image inspect spark-local:latest &>/dev/null; then
    echo "Building spark-local:latest image..."
    # Get the directory of the current script
    script_dir=$(dirname "$(realpath "$0")")
    
    # Build Docker image from Dockerfile.spark
    if [ -f "$script_dir/Dockerfile.spark" ]; then
        docker build -t spark-local:latest -f "$script_dir/Dockerfile.spark" "$script_dir"
    else
        echo "Error: Dockerfile.spark not found in $script_dir"
        exit 1
    fi
fi

job_file="/home/spark_jobs/$1"
echo "Running Spark job with Docker: $job_file"

# Run the docker job
# Get absolute paths for mounting
current_dir=$(pwd)/spark_jobs
data_dir=$(realpath "$current_dir/../../backend/data")
echo "Data directory: $data_dir"
echo "Current directory: $current_dir"

docker run \
    -v "$data_dir:/home/data/" \
    -v "$current_dir:/home/spark_jobs" \
    spark-local:latest \
    spark-submit \
    --conf spark.executor.memory=6g \
    --conf spark.driver.memory=6g \
    "$job_file"

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Job completed successfully: $job_file"
else
    echo "Error running job: $job_file"
    exit 1
fi
