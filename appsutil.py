import os
import logging
from google import genai
from google.genai import types

def process_document(image_path, language="English"):

    vertex_summary = process_vertex(image_path, language)

    return vertex_summary

def process_vertex(image_path, language):
    client = genai.Client(
        vertexai=True,
        project=os.environ.get('PROJECT'),
        location='us-central1'
    )

    with open(image_path, 'rb') as image_file:
        # Read the image content
        image_content = image_file.read()

        # Create the request payload
        image1 = types.Part.from_bytes(
            data=image_content,  # Use the image content directly
            mime_type="image/jpeg",
        )

        prompt = f"""
Provide the summary of this image in ${language}. Do not greet, acknowledge or confirm. Just provide the report.

Purpose and Goals:

* Analyze images of Japanese documents and provide a summary report to the user.
* Identify the category of the document, such as invoice, receipt, or other.
* Extract critical information from the document, such as sender, amount due, and due date.
* Highlight critical information to help the user avoid penalties.

 Behaviors and Rules:

 1) Document Analysis:

 a) Carefully analyze the images of the documents.
 b) Identify the type of document and its purpose.
 c) Extract critical information, such as sender, amount due, and due date.
 d) Summarize the document's content in a clear and concise manner.
 e) Highlight critical information to draw the user's attention.

 2) Reporting:
 a) Present the summary report to the user in a well-organized format.
 b) Use tables or bullet points to present critical information clearly.
 c) Offer additional explanations or clarifications as needed.
 d) Answer the user's questions about the documents and their analysis.

 Overall Tone:

 * Use professional and courteous language.
 * Provide accurate and reliable information.
 * Maintain confidentiality and respect for the user's documents.
"""
        model = "gemini-2.0-flash-exp"
        contents = [
            types.Content(
                role="user",
                parts=[
                    image1,
                    types.Part.from_text(
                        prompt
                    )
                ]
            )
        ]
        generate_content_config = types.GenerateContentConfig(
            temperature = 1,
            top_p = 0.95,
            max_output_tokens = 8192,
            response_modalities = ["TEXT"],
            safety_settings = [types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="OFF"
            ),types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="OFF"
            ),types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="OFF"
            ),types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="OFF"
            )],
        )

        # Use generate_content instead of generate_content_stream
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )

        # Print the entire response text
        return response.text, response.text

