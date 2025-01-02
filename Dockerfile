FROM python:3.12-slim

# Create app directory
WORKDIR /app

# Bundle app source
COPY . /app

# Install app dependencies
RUN pip install -r requirements.txt

ARG PROJECT
ARG MOUNT_PATH

RUN mkdir "${MOUNT_PATH}"

ENV GRADIO_SERVER_NAME=0.0.0.0 \
    GRADIO_SERVER_PORT=8080 \
    PROJECT="${PROJECT}" \
    MOUNT_PATH="${MOUNT_PATH}"

EXPOSE 8080

CMD [ "python", "app.py"]
