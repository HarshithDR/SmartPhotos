import db
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
google_api = os.getenv('Google_api')
genai.configure(api_key= google_api)

# Main function to describe the image
def image_describer(image_id):
    image_data = db.get_image_from_mongodb(image_id)
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

    image_file_path = db.convert_image_data_to_file(image_data)

    prompt_parts = [
        genai.upload_file(image_file_path),
        "Describe the image in one paragraph and also give me keywords"
    ]

    response = model.generate_content(prompt_parts)
    return response

if __name__ == '__main__':
    try:
        image_id = input('Input image ID: ')
        # image_data = get_image_from_mongodb(image_id)
        response = image_describer(image_id).text
        print(response)
    except Exception as e:
        print("Exception:\n", e, "\n")
        print("Response:\n", 'error')