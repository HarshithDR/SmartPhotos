import os
import google.generativeai as genai
# genai.configure(api_key="AIzaSyDaLv2iR9W5E17I7hrj8i4ijlCJpQUMdzA")

# # Set up the model
# generation_config = {
#     "temperature": 0.2,
#     "top_p": 0.8,
#     "top_k": 64,
#     "max_output_tokens": 8192,
# }
#
# model = genai.GenerativeModel(
#     model_name="gemini-1.5-pro",
#     generation_config=generation_config,
# )
#
# response = model.generate_content("What is the chemical formula of glucose?")
#
# try:
#     print(response.text)
# except Exception as e:
#     print("Exception:\n", e, "\n")
#     print("Response:\n", response.candidates)
#
# Chat with files

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
    genai.upload_file("Screenshot 2023-11-25 121717.png"),
    "Describe the image."
]

response = model.generate_content(prompt_parts)

try:
    print(response.text)
except Exception as e:
    print("Exception:\n", e, "\n")
    print("Response:\n", response.candidates)