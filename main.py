import base64
import mimetypes
import os

from google import genai
from google.genai import types
from PIL import Image


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
    # model = "imagen-4.0-generate-001"

    image1 = Image.open(
        "C:/Users/Admin/Documents/Workbench/Computational Visual Perception/projects/2/ref/penrose_stairway.png"
    )

    # contents = [
    #     types.Content(
    #         role="user",
    #         parts=[
    #             # types.Part.from_image(image1),
    #             types.Part.from_text(text=prompt),
    #         ],
    #     ),
    # ]

    tools = [
        types.Tool(googleSearch=types.GoogleSearch()),
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=32768,
        # response_modalities=["TEXT", "IMAGE"],
        response_modalities=["IMAGE"],
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"
            ),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
        image_config=types.ImageConfig(
            aspect_ratio="1:1",
            image_size="1K",
            output_mime_type="image/png",
            # number_of_images = 4
        ),
        # tools=tools,
    )

    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    file_index = 0

    response = client.models.generate_content(
        model=model,
        contents=[prompt, image1],
        config=types.GenerateContentConfig(response_modalities=["Image"]),
    )

    for part in response.parts:
        if part.text is not None:
            print(part.text, end="")
        elif part.inline_data is not None:
            while True:
                file_name = f"{topic}_{file_index}-ref.png"
                file_path = os.path.join(output_folder, file_name)
                if not os.path.exists(file_path):
                    break
                file_index += 1
            image = part.as_image()
            image.save(file_path)
            file_index += 1


if __name__ == "__main__":
    topic = "penrose"

    prompt = """A minimalist, flat line-art drawing of the Penrose stairs optical illusion, increasing the complexity of geometry of image1 with few additional intricate connections of continuous loops of steps. Isometric perspective, pure wireframe aesthetic, no shading, no shadows, no stone texture, uniform line weight, flat two-dimensional black ink on plain white paper."""

    # FAILED
    # prompt = """A minimalist, flat line-art drawing of the Penrose stairs optical illusion, increasing the complexity of geometry of image1 with multiple intricate connections of continuous loops of steps more than image1. Isometric perspective, pure wireframe aesthetic, no shading, no shadows, no stone texture, uniform line weight, flat two-dimensional black ink on plain white paper."""

    # prompt = """A minimalist, flat line-art drawing of the Penrose stairs optical illusion, maintaining the exact geometry of image1. A continuous loop of steps arranged in a square. Robed figures are drawn only as simple outlines walking upwards. Isometric perspective, pure wireframe aesthetic, no shading, no shadows, no stone texture, uniform line weight, flat two-dimensional black ink on plain white paper."""

    # prompt = """A high-detailed LSD style drawing of the Penrose stairs optical illusion, similar to the image1. A continuous, infinite loop of green pipes steps arranged instead of squares. Mario-related figures are walking endlessly along those stairs upwards in a clockwise direction with tiny mushrooms scattered along the way. Isometric perspective, impossible geometry, paradoxical architecture in the more modern style of M.C. Escher, intricate line work, high contrast."""

    # prompt = """A high-detailed Penrose stairway optical illusion based on image1."""

    # FAILED
    # prompt = """A high-detailed modern Penrose stairway optical illusion."""

    # FAILED
    # prompt = """A high-detailed modern style Penrose stairway optical illusion based on image1."""

    # 2nd BEST
    # prompt = """A high-detailed Penrose stairway optical illusion."""

    # FAILED
    # prompt = """A perfect isometric projection of a Penrose square stairway. The stairs make four 90-degree turns to form a continuous closed loop. Visually, the steps rise continuously but return to the start. Minimalist concrete texture, clean lines, white background, impossible object, mathematical diagram, distinct stair treads, high geometric precision."""

    # FAILED
    # prompt = """A photorealistic, cinematic render of the Penrose infinite staircase. Ancient grey stone architecture, a square staircase that loops back onto itself seamlessly. The stairs appear to ascend forever on all four sides. Isometric view, 45-degree angle, dramatic sunlight casting long shadows, unreal engine 5 render, architectural visualization, optical illusion, non-Euclidean geometry, 8k resolution."""

    # BEST
    # prompt = """A high-detailed lithograph style drawing of the Penrose stairs optical illusion, similar to the image1. A continuous, infinite loop of stone steps arranged in a square. Robed figures are walking endlessly along those stairs upwards in a clockwise direction. Isometric perspective, impossible geometry, paradoxical architecture in the more modern style of M.C. Escher, intricate line work, high contrast, mathematical art."""

    # prompt = """A high-detailed lithograph style drawing of the Penrose stairs optical illusion, similar to the image1. A continuous, infinite loop of stone steps arranged in a square. Robed figures are walking endlessly upwards in a clockwise direction. Isometric perspective, impossible geometry, paradoxical architecture in the more modern style of M.C. Escher, intricate line work, high contrast, mathematical art."""

    # prompt = """A high-detailed lithograph style drawing of the Penrose stairs optical illusion, similar to the image1. A continuous, infinite loop of stone steps arranged in a square. Robed figures are walking endlessly upwards in a clockwise direction. Isometric perspective, impossible geometry, paradoxical architecture in the style of M.C. Escher, intricate line work, high contrast, mathematical art."""

    generate(prompt, topic)
