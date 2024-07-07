import InvokeAgent as agenthelper
import streamlit as st
import json
import pandas as pd
from PIL import Image, ImageOps, ImageDraw

# Streamlit page configuration
st.set_page_config(page_title="Virtual Marketing Assistant", page_icon=":robot_face:", layout="wide")


context = {
    "agentId": "Q9OA0BIDVV",
    "agentAliasId": "ZD6FMDRHMJ"
}

####
# Functions
####
def initialize_session():
    if 'history' not in st.session_state:
        st.session_state['history'] = []

        
        
                
def display_chat_history(col1, col2):
    """
    Displays the chat history.
    """
    with col1:
        for message in st.session_state['history']:
            if message["role"] == "user":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            
    with col2:
        for message in st.session_state['history']:
            if message["role"] == "assistant":
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
st.title("Virtual Maths Tutor")
st.markdown('Powered by Bedrock')
# Display a button to end the session
end_session_button = st.button("End Session")

col1, col2 = st.columns(2)
display_chat_history(col1, col2)
prompt = st.chat_input("What's up?")

# Sidebar for user input
st.sidebar.title("Trace Data")


# Handling user input and responses
if prompt:
    event = {
        "sessionId": "MYSESSION101",
        "question": prompt
    }
    st.session_state['history'].append({"role": "user", "content": prompt})
    
    # Display the prompt in chat
    with col1:
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
    st.session_state['history'].append({"role": "assistant", "content": the_response})
    
    # Display the response in chat
    with col2:
        with st.chat_message("assistant"):
            st.markdown(the_response)
            
    st.session_state['trace_data'] = the_response
  

if end_session_button:
    with st.chat_message("user"):
        st.markdown("End Session")
        
    with st.chat_message("assistant"):
        st.markdown("Thank your for using Virtual Maths Tutor!")
        
    event = {
        "sessionId": "MYSESSION115",
        "question": "placeholder to end session",
        "endSession": True
    }
    agenthelper.lambda_handler(event, context)
    st.session_state['history'] = []
    st.experimental_rerun()
    

