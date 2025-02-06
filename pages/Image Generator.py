#packages
import streamlit as st
import os
import base64
from together import Together
import pathlib 
from PIL import Image
from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()


#load css file
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

css_path = pathlib.Path("./pages/style.css")
load_css(css_path)

#header
st.title("Image Generator")
st.subheader("Powered by Flux")

#prompt to generate image
prompt = st.text_input("Generate an Image")

#LLM for generating images
client = Together(api_key="9e69fff99bc0746ded11efa211ed6054c071fe54e28a1c67764e5704ef7ddddd")


st.divider()

#store different height of an image in a session state
if "height" not in st.session_state:
    st.session_state["height"] = ""

#store different height of an image in a session state
st.session_state.height = st.sidebar.selectbox("Select Resolution", [
   #all values must be a multiple of 16
    [1024,768],[720,480],[640,360],[320,240]
], index=0)




@st.cache_data
def load_image(image_file):
   img = Image.open(image_file)
   return img



#generate image after proving the prompt
if prompt:
  with st.spinner("Generating image"):
    #Model parameters for generating images
    response = client.images.generate(
       prompt = prompt,
        model = "black-forest-labs/FLUX.1-dev",
        width=st.session_state.height[0],
        height=st.session_state.height[1],
        steps = 28,
        n=1,
       response_format ="b64_json"
    )
    #converting the response to base64json 
    image_data = response.data[0].b64_json
    #converting image json values to bytes that can be interepreted
    image_bytes = base64.b64decode(image_data)
    #make a directory called images in the environment
    os.makedirs("images", exist_ok=True)
    #index for all the files generated
    image_index =1 
    #set the path of each file to images folder
    image_path = os.path.join("images",f"generated_image {image_index}.png")
    while os.path.exists(image_path):
       image_index+=1
       image_path = os.path.join("images",f"generated_image {image_index}.png")
    #open the file then
    with open(image_path, "wb") as image_file:
       image_file.write(image_bytes)



   #display the generated image
    st.image(image_path, caption="Generated Image")
    

 





