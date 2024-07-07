import streamlit as st

st.set_page_config(
    page_title="Bedrock Agents Use Cases",
    page_icon='💬',
    layout='wide'
)

st.header("Bedrock Agents Use Cases")

st.write("""
Bedrock Agents is a versatile framework designed to facilitate the development of applications leveraging Language Models (LLMs). It offers seamless integration of different components, making it easier to build sophisticated applications.

With Bedrock Agents, deploying chatbots and workflows tailored to specific needs is straightforward. Below are examples of use cases that can be explored in this project:

- **Virtual Marketing Assistant**: A chatbot designed to assist with marketing queries and tasks. [Explore](pages/1_💬_virtual_marketing_assistant.py)
- **Customer Support Agent**: Provides support by answering common customer questions. [Coming Soon]
- **Survey Bot**: Collects feedback or data from users through interactive sessions. [Coming Soon]
- **Event Reminder Bot**: Helps users remember important dates and events. [Coming Soon]
- **Personal Finance Assistant**: Offers advice and information on personal finance. [Coming Soon]

Navigate to the corresponding section to see these chatbots in action.
""")