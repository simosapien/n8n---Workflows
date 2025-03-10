import streamlit as st
import requests
import uuid
import base64

# Constants
#===========

# n8nWebhook for TEST:
#---------------------
#WEBHOOK_URL = "https://handigeni.app.n8n.cloud/webhook-test/6161a7bd-526a-4f9f-a50f-48b6aa3142e6"

# n8n Webhook for PRODUCTION:
#----------------------------
WEBHOOK_URL = "https://handigeni.app.n8n.cloud/webhook/6161a7bd-526a-4f9f-a50f-48b6aa3142e6"

def generate_session_id():
    return str(uuid.uuid4())

def send_message_to_llm(session_id, message):
    headers = {
        "Authorization": "__n8n_BLANK_VALUE_e5362baf-c777-4d57-a609-6eaf1f9e87f6",
        "Content-Type": "application/json"
    }
    payload = {
        "sessionId": session_id,
        "chatInput": message
    }
    
    print("=== DEBUG INFO ===")
    print(f"URL being called: {WEBHOOK_URL}")
    print(f"Headers being sent: {headers}")
    print(f"Payload being sent: {payload}")
    
    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Complete Response: {response.text}")
    print(f"Response Headers: {dict(response.headers)}")
    print("=== END DEBUG ===")
    
    if response.status_code == 200:
        if response.text:
            try:
                return response.json()["output"]
            except Exception as e:
                return f"Error parsing response: {str(e)}\nResponse text: {response.text}"
        else:
            return "Received empty response from server. Please check your n8n workflow configuration."
    else:
        return f"Error: {response.status_code} - {response.text}"

def main():
    st.title("Handigeni Chat with LLM")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = generate_session_id()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Get LLM response
        llm_response = send_message_to_llm(st.session_state.session_id, user_input)

        # Add LLM response to chat history
        st.session_state.messages.append({"role": "assistant", "content": llm_response})
        with st.chat_message("assistant"):
            st.write(llm_response)

if __name__ == "__main__":
    main()