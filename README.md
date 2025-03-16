# goit-pythonweb-hw-03

## Project Description

This project is a simple web application built with Python. It has three main pages:

- **Home Page**: Describes the available Python training packages.
- **Send Message**: Allows users to send a message with their name and message content.
- **Read Messages**: Displays the messages that have been sent.

## Running the Project in a Docker Container

Build the image using command:

```sh
docker build --no-cache . -t hw3
```

To run the project in a Docker container for the first time, use the following command:

```sh
docker run -d -p 3000:3000 -v ./storage:/app/storage --name hw3c hw3
```

To stop container use:

```sh
docker stop hw3c
```

To start existing container use:

```sh
docker start hw3c
```
