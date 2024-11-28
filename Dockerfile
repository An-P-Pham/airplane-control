# Use the official Python 3.12 runtime as the base image
FROM python:3.12-slim

# Install dependencies for tkinter and GUI display
RUN apt-get update && \
    apt-get install -y \
    python3-tk \
    x11-apps \
    libx11-dev \
    libgtk-3-0 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Install any Python dependencies (if applicable)
RUN pip install --no-cache-dir -r requirements.txt

# Set the display environment variable to use the host's X server
ENV DISPLAY=:0

# Command to run the tkinter application
CMD ["python", "AirplaneControl.py"]