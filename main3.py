import os
from datetime import datetime

from google import genai
from google.genai import types
from PIL import Image


def analyze_hybrid_image(image_path: str, question: str, output_path: str):
    vertex_api_key = os.environ.get("GOOGLE_CLOUD_API_KEY")

    client = genai.Client(
        vertexai=True,
        api_key=vertex_api_key,
    )

    model = "gemini-3-pro-preview"

    image = Image.open(image_path)

    system_prompt = """You are an expert in visual perception and optical illusions.
This is a hybrid illusion image - it contains TWO superimposed images:
1. A HIGH frequency image (visible up close) - contains fine details and edges
2. A LOW frequency image (hidden in background) - visible when you blur your vision, squint, or view from a distance

Your task is to identify the HIDDEN entity in the LOW frequency background layer, NOT the obvious foreground image.
To find it, mentally blur the image or focus on the overall shapes and shadows rather than fine details.

CRITICAL: You MUST respond with ONLY the name of the hidden entity. No explanations, no reasoning, no bullet points, no markdown formatting, no extra words. Just the name itself."""

    response = client.models.generate_content(
        model=model,
        contents=[question, image],
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7,
            top_p=0.95,
            max_output_tokens=16384,
            response_modalities=["TEXT"],
            thinking_config=types.ThinkingConfig(
                thinking_budget=4096,
            ),
        ),
    )

    # Collect all text parts
    output_text = ""
    if response.candidates and len(response.candidates) > 0:
        candidate = response.candidates[0]
        if candidate.content and candidate.content.parts:
            for part in candidate.content.parts:
                if hasattr(part, "text") and part.text is not None:
                    output_text += part.text

    if not output_text:
        print("Warning: No text response received from the API")
        print(f"Response: {response}")
        return

    # Generate timestamp up to minute
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Format as markdown with timestamp
    markdown_content = f"## {timestamp}\n\n{output_text}\n\n---\n\n"

    # Append to markdown file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "a", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"Output appended to: {output_path}")


if __name__ == "__main__":
    image_path = "C:/Users/Admin/Documents/Workbench/Computational Visual Perception/projects/2/ref/hybrid.jpeg"

    question = """Analyze this hybrid illusion image carefully.
Ignore the obvious foreground image with sharp details.
Focus on the blurry, low-frequency background layer - what hidden entity do you see in the shadows and overall shapes?
The hidden entity could be a famous person (celebrity, politician, scientist), a landmark (monument, building), or another recognizable figure.
Reply with ONLY the name, nothing else."""

    output_path = "C:/Users/Admin/Documents/Workbench/Computational Visual Perception/projects/2/output/hybrid_analysis.md"

    analyze_hybrid_image(image_path, question, output_path)
