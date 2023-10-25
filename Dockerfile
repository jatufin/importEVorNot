# Use an official Node.js runtime as a parent image for React
FROM node:16 as build

# Set the working directory for the React app
WORKDIR /app/frontend

# Copy frontend code into the container
COPY ./frontend .

# Install app dependencies and build the React app
RUN npm install
RUN npm run build

# Use a Python base image with Poetry pre-installed
FROM python:3.11

# Set environment variables to ensure Python outputs everything to stdout
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Create and set the working directory inside the container
WORKDIR /app

# Copy build into the container
COPY --from=build /app/frontend/build ./frontend/build

# Copy only the pyproject.toml and poetry.lock files to take advantage of Docker layer caching
COPY pyproject.toml poetry.lock /app/

# Install Poetry and project dependencies
RUN pip3 install poetry
RUN pip3 install waitress

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Copy the rest of the Flask app code into the container
ADD mobile_de /app/mobile_de
ADD nettiauto /app/nettiauto
ADD src /app
COPY mobile_de/mobilede_parser.py mobile_de/mobilede_utils.py /app/

# Expose the port your Flask app will run on (change if needed)
EXPOSE 5000

# Define the command to run the Flask app
CMD ["waitress-serve", "--host", "0.0.0.0", "--port", "5000", "app:app"]