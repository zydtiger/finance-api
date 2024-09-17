FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY ./src /app/src

# Declare the port that the app runs on
EXPOSE 3000

# Command to boot the FastAPI app
CMD ["fastapi", "run", "src/app.py", "--port", "3000"]
