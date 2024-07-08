import InvokeAgent as agenthelper
import streamlit as st
import json
import pandas as pd
from PIL import Image, ImageOps, ImageDraw

# Streamlit page configuration
st.set_page_config(page_title="Virtual Marketing Assistant", page_icon=":robot_face:", layout="wide")
st.logo('images/punyani.ai.logo.png', link=None, icon_image=None)

context = {
    "agentId": "SHKT53XCLU",
    "agentAliasId": "ZS6I2EJZXI"
}

####
# Functions
####
def initialize_session():
    if 'history' not in st.session_state:
        st.session_state['history'] = []

        
        
def display_chat_history():
    """
    Displays the chat history.
    """
    for message in st.session_state['history']:
        if message["agent"] == "vma":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
       
# Function to parse and format response
def format_response(response_body):
    try:
        # Try to load the response as JSON
        data = json.loads(response_body)
        # If it's a list, convert it to a DataFrame for better visualization
        if isinstance(data, list):
            return pd.DataFrame(data)
        else:
            return response_body
    except json.JSONDecodeError:
        # If response is not JSON, return as is
        return response_body


####
# Code Execution starts here
####

## initialize session
initialize_session()

###### Create Layout
# Title
st.title("Virtual Marketing Assistant")
st.markdown('Powered by Bedrock')
# Display a button to end the session
end_session_button = st.button("End Session")
display_chat_history()
prompt = st.chat_input("What's up?")
with st.sidebar:
    st.markdown("# Few Sample Prompts")
    st.markdown("show leads information")
    st.markdown("how many of them are from south india")
    st.markdown("show lead score")
    st.markdown("show lead score of leads from south india")
    st.markdown("show lead score with reason")
    st.markdown("show lead score in descending order of lead score")
    st.markdown("recommend offers for them")
    st.markdown("show leads with email")
    st.markdown("send personalized email to leads with low lead score")
    


# Sidebar for user input
st.sidebar.title("Trace Data")


# Handling user input and responses
if prompt:
    event = {
        "sessionId": "MYSESSION115",
        "question": prompt
    }
    st.session_state['history'].append({"agent" : "vma", "role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    response = agenthelper.lambda_handler(event, context)

    try:
        # Parse the JSON string
        if response and 'body' in response and response['body']:
            response_data = json.loads(response['body'])
            print("TRACE & RESPONSE DATA ->  ", response_data)
        else:
            print("Invalid or empty response received")
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
        response_data = None 
    
    try:
        # Extract the response and trace data
        all_data = format_response(response_data['response'])
        the_response = response_data['trace_data']
    except:
        all_data = "..." 
        the_response = "Apologies, but an error occurred. Please rerun the application" 

    # Use trace_data and formatted_response as needed
    st.sidebar.text_area("", value=all_data, height=300)
    st.session_state['history'].append({"agent" : "vma", "role": "assistant", "content": the_response})
    with st.chat_message("assistant"):
        st.markdown(the_response)
    st.session_state['trace_data'] = the_response
  

if end_session_button:
    with st.chat_message("user"):
        st.markdown("End Session")
        
    with st.chat_message("assistant"):
        st.markdown("Thank your for using Virtual Marketing Assistant!")
        
    event = {
        "sessionId": "MYSESSION115",
        "question": "placeholder to end session",
        "endSession": True
    }
    agenthelper.lambda_handler(event, context)
    st.session_state['history'] = []
    st.experimental_rerun()
    

