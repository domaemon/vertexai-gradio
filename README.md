# System Architecture

Cloud Load Balancer <- Load Balancer Backend -> Cloud Run (Gradio App)

# Local envrionment setup

$ python -m venv .venv

$ . .venv/bin/activate

$ pip install gradio

$ pip install google_genai

# Access Google Cloud

Set up your local development environment to access Google Cloud APIs:

$ gcloud auth application-default login

# Test locally

Develop a Gradio Python app. Run it locally using the gradio command:

$ gradio app.py

# Create a repository in Artifact Registry

$ gcloud artifacts repositories create ${REPOSITORY} --repository-format=docker \
       --location=${REGION} --description="Docker registry"

# Build the container image and push it to Artifact Registry

gcloud run deploy ${SERVICE} \
       --image ${IMAGE_URL}:latest \
       --platform managed \
       --project ${PROJECT} \
       --min-instances=1 \
       --region ${REGION} \
       --allow-unauthenticated \
       --ingress=internal-and-cloud-load-balancing # This line is for the laod balancer scenario

## Domain Restricted Sharing

To allow unauthenticated access to the Cloud Run instance, you need to unrestrict Domain Restricted Sharing (DRS). This is because you must assign the Cloud Invoker role to allUsers.

Domain Restricted Sharing limits resource sharing based on a domain or organization. When active, only principals belonging to allowed domains or organizations can be granted IAM roles in your Google Cloud organization. To assign the Cloud Invoker role to allUsers, you must unrestrict DRS in the Organization Policy settings page.

# Mount Cloud Storage

Mounting a Cloud Storage bucket as a volume in Cloud Run makes its content accessible as files in the container's file system. You can then access the bucket like a local directory, using your programming language's file system operations instead of Google API Client Libraries.

After deploying the app to Cloud Run, run the following command:

gcloud beta run services update ${SERVICE} \
       --region ${REGION} \
       --execution-environment gen2 \
       --add-volume=name=v_mount,type=cloud-storage,bucket=${BUCKET} \
       --add-volume-mount=volume=v_mount,mount-path=${MOUNT_PATH}

## Serverless NEG

A network endpoint group (NEG) specifies backend endpoints for a load balancer. A serverless NEG points to a Cloud Run, App Engine, Cloud Functions, or API Gateway service.

# Setup the Load Balancer

Create the frontend and backend. Select Serverless NEG as the backend.

