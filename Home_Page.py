
# CHATBOT SOLUTION
# To Run The Script Copy and Execute: streamlit run c:/Users/emman/OneDrive/Desktop/Python/GDSC/mainpage.py

#Packages
import streamlit as st
import pathlib 
import streamlit as st
import base64
from audio_recorder_streamlit import audio_recorder
from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()

#Package for Deepgram(Speech to Text Model)


#setting up the pages
st.set_page_config(
    page_title="Multipage App"
)

ImagePage = st.Page(
    page = "pages/Image Generator.py"
    
)

VoicePage = st.Page(
    page = "pages/Voice Assistant.py"
)

ImageAnalyzer = st.Page(
     page = "pages/Image Analyzer.py"
)


#output voice 
filename = "output.wav"

client = Groq(
    api_key= os.getenv("GROQ_API_key")
)

#import css file
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

css_path = pathlib.Path("./assets/style.css")
load_css(css_path)



# Initialize session state variables
# Store the chat messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.markdown("""
 <div class="load">
<div class="loader l1"></div>
<div class="loader l2"></div>
</div>""", unsafe_allow_html=True)

# Page Header
st.header("GENERATIVE AI MODEL")
st.title("ASKBOT", anchor=False )
st.subheader("Powered by Groq")




# Sidebar
st.sidebar.header("ASKBOT AI")
st.sidebar.success("select a page above")



def reset_chat():
    st.session_state.messages = []
    st.session_state.clear()
    
   





# Parameters
with st.sidebar.expander("⚙ Developer settings"):
    temp = st.slider("Temperature", 0.0, 2.0, value=1.0, help="randomness of response")
    max_tokens = st.slider("Max Tokens", 0, 1024, value=300, help="unit of word for characters for input and output")
    stream = st.toggle("Stream", value=True, help="ability to deliver generated content")
    
    top_p = st.slider("Top P", 0.0, 1.0, help="It's not recommended to alter both the temperature and the top-p, cummulative probability.")
    stop_seq = st.text_input("Stop Sequence", help="word to stop generation of output")
    

 
#recorded audio session state different from normal chat
if "recorded_audio" not in st.session_state:
    st.session_state.recorded_audio = None

#audio button and label with custom component
recorded_audio = audio_recorder(
    text="use audio",
    recording_color="#181a9e",
     neutral_color="#c2bfb8",
    icon_size="1px",
    key = "audio"
)

#transcribe the audio to text the process it with the LLM
def transcribe_audio(client, audio_path):
     #transcription history
    if "voicebxt" not in st.session_state:
       st.session_state["voicebxt"] = []
    
    with open(audio_path,"rb") as audio_file:   
           transcript = client.audio.transcriptions.create(model= "whisper-large-v3-Turbo",file=audio_file) 
           print(transcript.text)  
           prompt = transcript.text
                    
           with st.chat_message("user",  avatar = "./assets/images/user_avatar.png"):
            st.write(prompt)
        
        
           st.session_state.voicebxt.append(
              {"role": "user", "content": prompt}
           ) 
           st.write("mic response ")       
    # Make API call and show the model response
           with st.chat_message("assistant", avatar= "./assets/images/ai_avatarcom.png"):
        # create empty container for response
             response_text = st.empty()
        
        # Make the API call to Groq
           completion = client.chat.completions.create(
               model= "llama-3.1-8b-instant",
               messages =st.session_state.voicebxt,
               stream=stream,
               temperature=temp,
               max_tokens=max_tokens,
               stop=stop_seq,
              top_p=top_p
            )     
        # Display the full message
           full_response = ""
        
           if stream:
              for chunk in completion:
                full_response += chunk.choices[0].delta.content or ""
                response_text.write(full_response)
           else:
              with st.spinner("Generating"):
                completion.choices[0].messages.content

        # Add assistant message to the messages list
           st.session_state.voicebxt.append({"role": "assistant", "content": full_response})
           

#display the transcription and answer after
if recorded_audio:
    audio_file= "audio.mp3"
    with open( audio_file, "wb") as f:
        f.write(recorded_audio)
        transcribed_text = transcribe_audio(client, audio_file)

#reset the chat history and displayed chats
st.sidebar.button("reset chat", on_click=reset_chat)

for message in st.session_state.messages:
    # {"role": "user", "content": "hello world"}
    
    avatar = "./assets/images/user_avatar.png"  if message["role"]=="user" else "./assets/images/ai_avatarcom.png" if message["role"] == "assistant" else "👋"
    with  st.chat_message(message["role"], avatar = avatar):
        st.markdown(message["content"])
       




if prompt := st.chat_input(key="input",disabled=not input):   
    # add the message/prompt to the messages list
    # show the new user message
    recorded_audio = None
    with st.chat_message("user",  avatar = "./assets/images/user_avatar.png"):
        st.write(prompt)
        
       
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )     
       
     
    
        
    # Make API call and show the model response
    with st.chat_message("assistant", avatar= "./assets/images/ai_avatarcom.png"):
        # create empty container for response
        response_text = st.empty()
        
        # Make the API call to Groq
        completion = client.chat.completions.create(
            model= "llama-3.1-8b-instant",
            messages=st.session_state.messages,
            stream=stream,
            temperature=temp,
            max_tokens=max_tokens,
            stop=stop_seq,
            top_p=top_p
        )
        
        # Display the full message
        full_response = ""
        
        if stream:
            for chunk in completion:
                full_response += chunk.choices[0].delta.content or ""
                response_text.write(full_response)
        else:
            with st.spinner("Generating"):
                completion.choices[0].message.content
       
       
     
       


    
            
        # Add assistant message to the messages list
        st.session_state.messages.append({"role": "assistant", "content": full_response})
      



        

        
      
               



     

    




     
      
   