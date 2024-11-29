# Use Python 3.10.11 as base image
FROM python:3.10.11

# Set working directory in the container
WORKDIR /usr/src/app

# Install required Python packages
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port (Heroku assigns this dynamically)
EXPOSE $PORT

# Run the application using Waitress
CMD ["sh", "-c", "waitress-serve --listen=0.0.0.0:$PORT MusicPractice.wsgi:application"]
