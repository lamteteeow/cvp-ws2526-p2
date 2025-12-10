import base64
import mimetypes
import os
from google import genai
from google.genai import types


def save_binary_file(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()
    print(f"File saved to: {file_name}")


def generate(prompt: str, topic: str):
    vertex_api_key = os.environ.get("GOOGLE_CLOUD_API_KEY")
    # gemini_api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(
        vertexai=True,
        api_key=vertex_api_key,
        # api_key=gemini_api_key,
    )

    model = "gemini-3-pro-image-preview"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch()),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=32768,
        response_modalities=["TEXT", "IMAGE"],
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
        image_config=types.ImageConfig(
            aspect_ratio="1:1",
            image_size="1K",
            output_mime_type="image/png",
        ),
        # tools=tools,
    )

    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    file_index = 0
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue
        if (
            chunk.candidates[0].content.parts[0].inline_data
            and chunk.candidates[0].content.parts[0].inline_data.data
        ):
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)

            # Find the next available file index
            while True:
                file_name = f"{topic}_{file_index}{file_extension}"
                file_path = os.path.join(output_folder, file_name)
                if not os.path.exists(file_path):
                    break
                file_index += 1

            save_binary_file(file_path, data_buffer)
            file_index += 1
        else:
            print(chunk.text)

if __name__ == "__main__":
    topic = "penrose"
    prompt = """Generate Penrose stairs illusion."""
    generate(prompt, topic)
