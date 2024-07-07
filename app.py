import InvokeAgent as agenthelper
import streamlit as st
import json
import pandas as pd
from PIL import Image, ImageOps, ImageDraw

# Streamlit page configuration
st.set_page_config(page_title="Virtual Marketing Assistant", page_icon=":robot_face:", layout="wide")


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
# st.session_state['history'].append({"role": "assistant", "content": "Hello! I'm your personal marketing assistant. How can I assist you today?"})
display_chat_history()
prompt = st.chat_input("What's up?")

# Sidebar for user input
st.sidebar.title("Trace Data")


# Handling user input and responses
if prompt:
    event = {
        "sessionId": "MYSESSION115",
        "question": prompt
    }
    st.session_state['history'].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    response = agenthelper.lambda_handler(event, None)

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
    st.session_state['history'].append({"role": "assistant", "content": the_response})
    with st.chat_message("assistant"):
        st.markdown(the_response)
    st.session_state['trace_data'] = the_response
  

if end_session_button:
    st.session_state['history'].append({"role": "user", "content": "Session Ended"})
    st.session_state['history'].append({"role": "assistant", "content": "Thank your for using AnyCompany Support Agent!"})
    
    event = {
        "sessionId": "MYSESSION115",
        "question": "placeholder to end session",
        "endSession": True
    }
    agenthelper.lambda_handler(event, None)
    st.session_state['history'].clear()
    display_chat_history()

