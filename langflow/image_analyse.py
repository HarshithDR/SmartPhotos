import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


google_api = os.getenv('Google_api')
genai.configure(api_key= google_api)


def image_describer(path):
    generation_config = {
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 64,
        "max_output_tokens": 8192,
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )

    prompt_parts = [
        genai.upload_file(path),
        "Describe the image in one paragraph and also give me keywords"
    ]

    response = model.generate_content(prompt_parts)
    return response


if __name__ == '__main__':
    try:
        path = input('input path = ')
        response = image_describer(path).text
        print(response)
    except Exception as e:
        print("Exception:\n", e, "\n")
        print("Response:\n", 'error')