import base64
import mimetypes
import os

import numpy as np
import tifffile
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

    image2 = Image.open(
        "C:/Users/Admin/Documents/Workbench/Computational Visual Perception/projects/2/ref/escher_waterfall.png"
    )
    # Convert 16-bit grayscale to 8-bit for API compatibility
    if image2.mode == "I;16":
        arr = np.array(image2, dtype=np.uint16)
        arr = (arr / 256).astype(np.uint8)
        image2 = Image.fromarray(arr, mode="L")
    elif image2.mode == "I":
        image2 = image2.convert("L")

    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    file_index = 0

    response = client.models.generate_content(
        model=model,
        contents=[prompt, image2],
        config=types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            max_output_tokens=32768,
            response_modalities=["Image"],
            image_config=types.ImageConfig(
                aspect_ratio="2:3",
                image_size="1K",
                output_mime_type="image/png",
            ),
        ),
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
    topic = "waterfall"

    # Enhanced depth cues
    prompt = """A photorealistic CGI rendering of the Waterfall optical illusion, maintaining the exact geometry of image2. An ancient stone aqueduct carries rushing, transparent water that appears to flow uphill before crashing down onto a wet wooden water wheel. Strong, dramatic directional sunlight casts deep, realistic shadows that emphasize volumetric form and depth on the stone pillars. Realistic textures of wet mossy stone, splashing water physics, and atmospheric haze."""

    # Reduced depth cues
    # prompt = """A minimalist, flat line-art drawing of the Escher's Waterfall optical illusion, maintaining the exact geometry of image2. The aqueduct, flowing water, and water wheel are rendered only as simple black outlines on a plain white background. No shading, no shadows, no stone texture, no water ripples, uniform line weight throughout. The structure appears as a technical blueprint or wireframe model rather than a solid object."""

    # prompt = """A detailed lithograph drawing in the LSD version of M.C. Escher's "Waterfall". A stone aqueduct carries water in a zigzag path that appears to flow constantly downhill around corners, yet the water ends up two stories higher than where it started. The water falls from the top level onto a wooden waterwheel, which drives the flow back into the bottom of the impossible channel. Cross-hatching texture, impossible architecture, isometric perspective, non-Euclidean geometry."""

    # prompt = """A detailed lithograph drawing in the cartoon style of M.C. Escher's "Waterfall". A stone aqueduct carries water in a zigzag path that appears to flow constantly downhill around corners, yet the water ends up two stories higher than where it started. The water falls from the top level onto a wooden waterwheel, which drives the flow back into the bottom of the impossible channel. Cross-hatching texture, impossible architecture, isometric perspective, non-Euclidean geometry."""

    # prompt = """A detailed lithograph drawing in the cartoon style of M.C. Escher's "Waterfall". A stone aqueduct carries water in a zigzag path that appears to flow constantly downhill around corners, yet the water ends up two stories higher than where it started. The water falls from the top level onto a wooden waterwheel, which drives the flow back into the bottom of the impossible channel. Black and white, cross-hatching texture, impossible architecture, isometric perspective, non-Euclidean geometry."""

    generate(prompt, topic)
