# Use an official Python 3.10 runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Install dependencies for Tkinter
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Define environment variable
ENV NAME World

# Run harvest_main.py when the container launches
CMD ["python", "harvest_main.py"]