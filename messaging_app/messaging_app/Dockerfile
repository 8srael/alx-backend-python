# Use a base Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django app into the container
COPY . /app/

# Expose the port the app will run on
EXPOSE 8000

# Run Django server by default (replace 'messaging' with your project name if different)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Build the Docker image
# docker build -t messaging-app .
# Run the Docker container
# docker run -d -p 8000:8000 --name messaging-container messaging-app