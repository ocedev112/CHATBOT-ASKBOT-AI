import streamlit as st
import pathlib 
import streamlit as st
import base64
from audio_recorder_streamlit import audio_recorder
from groq import Groq
import pathlib
from dotenv import load_dotenv
import os


load_dotenv()


def reset_chat():
    st.session_state.voicebot = []
    st.session_state.clear()

#load CSS File
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

css_path = pathlib.Path("./pages/style.css")
load_css(css_path)


#store different voices in a session state
if "voice" not in st.session_state:
    st.session_state["voice"] = ""

#voice option for changing voices
st.session_state.voice = st.sidebar.selectbox("Choose A Voice", [
    "aura-athena-en", "aura-asteria-en", "aura-stella-en","aura-luna-en","aura-orion-en","aura-perseus-en","aura-helios-en"
], index=0)


#header for page
st.header("Use Voice Assitant Aura")

#LLM for transcribing the audio and giving a resonse(Speech to Text, and LLM)
client = Groq(
    api_key="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"
)



#Package for Deepgram(Speech to Text Model)
from deepgram import(
    DeepgramClient,
    SpeakOptions,
)


#function for converting or transcribing audio to text
def audio_to_text(client, audio_path):
    with open(audio_path,"rb") as audio_file:   
           transcript = client.audio.transcriptions.create(model= "whisper-large-v3-Turbo",file=audio_file) 
           print(transcript.text)  
           prompt = transcript.text
           return prompt
    

#fucntion that will generate a response based on the text
def generate_response(input_text):
    if "voicebot" not in st.session_state:
      st.session_state["voicebot"] = []
      

     
    st.session_state.voicebot.append(
        {"role": "user", "content": input_text}
    )    
    completion = client.chat.completions.create(
            model= "llama3-8b-8192",
            messages= st.session_state.voicebot,
            stream=True,
            temperature=0.7,
            max_tokens=300,
            stop=None,
        
            top_p=1
    )
    
    response = " "
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""
       
    print(response)
   
  
    return response



filename = "output.mp3"


#function  get called to use text to speech model
def text2speech(text_input):
    try:
        SPEAK_OPTIONS = {"text": text_input}

        deepgram = DeepgramClient( api_key= os.getenv("DEEPGRAM_API_KEY"))
    

        options = SpeakOptions(
        #using session state so the user can change the voices
        model= st.session_state.voice ,
        encoding="linear16", container="wav"
       )

        response = deepgram.speak.rest.v("1").save(filename, SPEAK_OPTIONS, options)

        return response.content
    except Exception as e:
        print(f"Exception: {e}")




#autoplay the audio file after the text to speech model has evaluated it
def autoplay_audio(file_path: str):
   with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )


#load css file
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

css_path = pathlib.Path("./assets/style.css")
load_css(css_path)

#voice assitant Aura
with st.container(key="aura"):
   st.title("AURA")
  
   st.markdown("""<div class="spinner">
    <div class="spinner1"></div>
</div>""", unsafe_allow_html=True)
   voice = audio_recorder(text="",
          recording_color="#181a9e",
           neutral_color="#c2bfb8",
           icon_size="40px",
           key = "voiceai") 
#play voice when you hit the button
if voice:
    voice_file= "tovoice.mp3"
    with open( voice_file, "wb") as f:
        f.write(voice)
        stt = audio_to_text(client, voice_file)
        response = generate_response(stt)
        file = text2speech(response)
        hide_audio = """
           <style>
                audio { display : none !important; position: absolute !important;}
           </style>
        """
        st.markdown(hide_audio, unsafe_allow_html=True)
        #audio played
        st.button("Stop response", key="stop", on_click=reset_chat, type="primary", help="stoping response clears history")
        st.audio("output.mp3", format="audio/mp3", autoplay=True)
        translation = audio_to_text(client, voice_file)
     
