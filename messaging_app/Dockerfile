# Using a base image
FROM python:3.10

# Setting up environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Setting the working directory inside the container
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Django project
COPY . .

# Expose Django a default port
EXPOSE 8000

#Run server
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]