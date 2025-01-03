# vertexai-gradio

# System Architecture

Cloud Load Balancer <- Load Balancer Backend -> Cloud Run (Gradio App)

# Local envrionment

$ python -m venv .venv
$ pip install gradio
$ pip install google_genai

Then set up your local development environment to easily access Google Cloud APIs.

$ gcloud auth application-default login

Develop a gradio python app. Run locally with

$ gradio app.py

# Infra setup

## Domain Restricted Sharing

To allow unauthenticated access to Cloud Run instance, you need to unrestrict the Domain Restricted Sharing (DRS)

Domain restricted sharing lets you limit resource sharing based on a domain or organization resource. When domain restricted sharing is active, only principals that belong to allowed domains or organizations can be granted IAM roles in your Google Cloud organization.

## Cloud Run Volume mount

Mounting the bucket as a volume in Cloud Run presents the bucket content as files in the container file system. After you mount the bucket as a volume, you access the bucket as if it were a directory on your local file system, using your programming language's file system operations and libraries instead of using Google API Client Libraries.

## Serverless NEG

A network endpoint group (NEG) specifies a group of backend endpoints for a load balancer. A serverless NEG is a backend that points to a Cloud Run, App Engine, Cloud Run functions, or API Gateway service.