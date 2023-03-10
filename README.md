# Start the application

## Create .env file

Based out of .env.example create your own .env file.

Recommended setting for allowed hosts is "0.0.0.0" since this is used in Dockerfile itself when running the application.

## Creating image and running container

Position yourself in a folder where Dockerfile is located, after that run these commands:

```$
    docker build -t shipgame:latest .
```

After this is finished and the docker image is created, run the following command

```$
    docker run -d --rm -p 8000:8000 shipgame:latest
```
After this visit the http://0.0.0.0:8000/api/schema/swagger-ui/
