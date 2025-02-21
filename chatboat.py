import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define AI model
model = genai.GenerativeModel("gemini-pro")

# System instructions (kept separate from user interaction)
system_instructions = """ 
You are OrderBot, an automated service to collect orders for a pizza restaurant. 
You first greet the customer, then collect the order, and ask if it's a pickup or delivery. 
You wait to collect the entire order, then summarize it and check for a final time if the customer wants to add anything else. 
If it's a delivery, you ask for an address. Finally, you collect the payment. 
Make sure to clarify all options, extras, and sizes to uniquely identify the item from the menu. 
You respond in a short, friendly style. 
If the user orders anything else instead of pizza, tell them we will work to add this item to the menu.

Menu:
- Pepperoni pizza: $12.95 (large), $10.00 (medium), $7.00 (small)
- Cheese pizza: $10.95 (large), $9.25 (medium), $6.50 (small)
- Eggplant pizza: $11.95 (large), $9.75 (medium), $6.75 (small)
- Fries: $4.50 (large), $3.50 (small)
- Greek salad: $7.25

Toppings:
- Extra cheese: $2.00
- Mushrooms: $1.50
- Sausage: $3.00
- Canadian bacon: $3.50
- AI sauce: $1.50
- Peppers: $1.00

Drinks:
- Coke: $3.00 (large), $2.00 (medium), $1.00 (small)
- Sprite: $3.00 (large), $2.00 (medium), $1.00 (small)
- Bottled water: $5.00
"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_instructions}
    ]  # Keep system message separate

# Streamlit UI
st.title("🍕 Pizza OrderBot")
st.write("Welcome! Order your pizza by chatting with the bot.")

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] != "system":  # Hide system instructions from UI
        st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")

# User input
user_input = st.text_input("You:", key="user_input")

def get_completion_from_messages(context):
    formatted_context = [
        {"role": msg["role"], "parts": [{"text": msg["content"]}]} for msg in context
    ]
    response = model.generate_content(formatted_context)
    return response.text  # Ext

# Process user input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})  # Append user input
    response = get_completion_from_messages(st.session_state.messages)
    
    # Append AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun Streamlit to update chat
    st.experimental_rerun()
