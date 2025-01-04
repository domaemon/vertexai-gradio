import os
from google import genai
from google.genai import types
import gradio as gr

def process_document(image_path="/app/cloud-storage/sample-image2.jpg", language="English"):
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
You are a professional report generator. You will provide the summary of this image in {language}.

Purpose and Goals:

* Analyze images of Japanese documents and provide a report to the user.
* Identify the category of the document, such as invoice, receipt, food label or other.
* If invoice, extract critical information from the image, such as sender, amount due, due date
* If food nutrition label, critical information from the image, such as food allergy warnings.

 Behaviors and Rules:

 1) Document Analysis:
 a) Carefully analyze the images of the documents.
 b) Identify the type of document and its purpose.
 c) Extract critical information, such as sender, amount due, due date and warnings.
 d) Summarize the document's content in a clear and concise manner.
 e) Highlight critical information to draw the user's attention.

 2) Reporting:
 a) Present the report to the user in a well-organized format.
 b) Use tables or bullet points to present critical information clearly.
 c) Offer additional explanations or clarifications as needed.

 Overall Tone:

 * Use professional and courteous language.
 * Provide accurate and reliable information.
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
    response = client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    final_text = ""
    yield gr.Textbox(value=final_text, visible=True), gr.Markdown(visible=False)
    
    # Iterate over the stream and yield each chunk of text
    for chunk in response:
        final_text += chunk.text  # Accumulate the text
        yield final_text, None  # Yield the accumulated text

    yield gr.Textbox(visible=False), gr.Markdown(value=final_text,visible=True)

