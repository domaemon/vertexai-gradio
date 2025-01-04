# System Architecture

Cloud Load Balancer <- Load Balancer Backend -> Cloud Run (Gradio App)

# Deployment Steps

1. Local environment setup
2. Cloud access
3. Testing locally
4. Building the container and submitting to Artifact Registry
5. Deploying to Cloud Run
6. Mount the Cloud Storage
7. Setting up Load Balancer

# Local envrionment setup

$ python -m venv .venv

$ . .venv/bin/activate

$ pip install gradio

$ pip install google_genai

# Cloud access

Then set up your local development environment to easily access Google Cloud APIs.

$ gcloud auth application-default login

# Testing locally

Develop a gradio python app. Run locally with gradio command.

$ gradio app.py

# Create a repository in Artifact Registry

$ gcloud artifacts repositories create ${REPOSITORY} --repository-format=docker \
       --location=${REGION} --description="Docker registry"

# Building container and submitting to Artifact Registry

gcloud run deploy ${SERVICE} \
       --image ${IMAGE_URL}:latest \
       --platform managed \
       --project ${PROJECT} \
       --min-instances=1 \
       --region ${REGION} \
       --allow-unauthenticated \
       --ingress=internal-and-cloud-load-balancing # This line is for the laod balancer scenario

## Domain Restricted Sharing

To allow unauthenticated access to Cloud Run instance, you need to unrestrict the Domain Restricted Sharing (DRS). This is because you must assing cloud invoker role to allUsers. Domain restricted sharing lets you limit resource sharing based on a domain or organization resource. When domain restricted sharing is active, only principals that belong to allowed domains or organizations can be granted IAM roles in your Google Cloud organization. To assing cloud invoker role to allUsers, you must unrestrict the DRS in the organizaiton policy setting page.

# Cloud Run Volume mount

Mounting the bucket as a volume in Cloud Run presents the bucket content as files in the container file system. After you mount the bucket as a volume, you access the bucket as if it were a directory on your local file system, using your programming language's file system operations and libraries instead of using Google API Client Libraries.

After deploying the app to Cloud Run, you should the following command 

gcloud beta run services update ${SERVICE} \
       --region ${REGION} \
       --execution-environment gen2 \
       --add-volume=name=v_mount,type=cloud-storage,bucket=${BUCKET} \
       --add-volume-mount=volume=v_mount,mount-path=${MOUNT_PATH}

## Serverless NEG

A network endpoint group (NEG) specifies a group of backend endpoints for a load balancer. A serverless NEG is a backend that points to a Cloud Run, App Engine, Cloud Run functions, or API Gateway service.

# Load Balancer setup

