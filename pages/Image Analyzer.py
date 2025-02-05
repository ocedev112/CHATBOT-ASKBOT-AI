#Packages
import streamlit as st
import os
import base64
from groq import Groq
from PIL import Image
import pathlib
from dotenv import load_dotenv
import os


load_dotenv()

def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

css_path = pathlib.Path("./pages/style.css")
load_css(css_path)


# Parameters
with st.sidebar.expander("⚙ Developer settings"):
    temp = st.slider("Temperature", 0.0, 2.0, value=1.0, help="randomness of response")
    max_tokens = st.slider("Max Tokens", 0, 1024, value=300, help="unit of word for characters for input and output")

    top_p = st.slider("Top P", 0.0, 1.0, help="It's not recommended to alter both the temperature and the top-p, cummulative probability.")
    stop_seq = st.text_input("Stop Sequence", help="word to stop generation of output")
    


st.title("Image Analysis")


#LLM for analyzing image
img_client = Groq(
    api_key= "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"
)



#prompt to analyze image
prompt= st.text_input("Analysis field", value="Describe an image")
with st.popover("Import Image"):
  
    uploaded_file = st.file_uploader("Upload an image", type=["png","jpg"])



def encode_image(image_path):
   with open(image_path, "rb") as image_file:
      return  base64.b64encode(image_file.read()).decode('utf-8')

def image_to_text(valuex,base64_image):
   prompt

 
   chat_completion = img_client.chat.completions.create(
      messages =[{
            "role": "user",
            "content": [{"type":"text","text":valuex},{"type":"image_url",
               "image_url":{"url": f"data:image;base64,{base64_image}"}}]
         }  ],
      model = "llama-3.2-11b-vision-preview",
    
       temperature=temp,
       max_tokens=max_tokens,
       stop=stop_seq,
       top_p=top_p
    )
   print(chat_completion.choices[0].message.content)
   return chat_completion.choices[0].message.content
if uploaded_file is not None and prompt:

    # Open the image

    image = Image.open(uploaded_file)



    # Define save directory

    save_folder = "uploads"

    os.makedirs(save_folder, exist_ok=True)  # Ensure the folder exists



    # Save image with the original filename

    save_path = os.path.join(save_folder, uploaded_file.name)

    image.save(save_path)
    base64_image = encode_image(save_path)
    described_img = image_to_text(prompt,base64_image)
    st.write(f"output: {described_img}")
elif uploaded_file is not None:
   st.write("Please Input a prompt, then press enter in the analysis field")

 
