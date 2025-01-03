import gradio as gr
from appsutil import process_document

with gr.Blocks() as demo:
    input_image = gr.Image(type='filepath')  # Removed extra comma
    input_radio = gr.Radio(["English", "French", "Vietnamese", "Portuguese", "Chinese", "Japanese"], label="Language", info="Choose your Language")

    inputs = [input_image, input_radio]

    examples = gr.Examples(examples=[
        ["/app/cloud-storage/sample-image1.jpg", "English"],
        ["/app/cloud-storage/sample-image2.jpg", "Japanese"]
    ], inputs=inputs)
    submit_button = gr.Button("Submit")

    output_text = gr.Textbox(label="vertex-summary")
    output_markdown = gr.Markdown(label="vertex-summary")  # Using only Markdown output
    outputs = [output_text, output_markdown]  # Or [output_markdown] if you only want one
    submit_button.click(process_document, inputs=inputs, outputs=outputs)

demo.launch(share=True, allowed_paths=["/app/cloud-storage"])
