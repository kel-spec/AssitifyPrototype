import time
import streamlit as st
from transformers import pipeline

# Set page config to make it more chat-like
st.set_page_config(page_title="Assistify 🛒", layout="wide")

# Load BERT sentiment analysis pipeline from Hugging Face
@st.cache_resource
def load_bert_model():
    sentiment_analyzer = pipeline("sentiment-analysis")
    return sentiment_analyzer

sentiment_analyzer = load_bert_model()

# Define chatbot responses
responses = {
    "greeting": "Hello! How can I assist you with your shopping today?",
    "payment": "You can pay using credit cards, PayPal, or other online payment methods.",
    "return": "Our return policy allows returns within 30 days with a receipt.",
    "shipping": "We offer free shipping on orders over $50!",
    "positive_feedback": "Thank you for your positive feedback! We are happy you had a good experience.",
    "negative_feedback": "We're sorry to hear about your experience. We'll try to improve.",
    "neutral_feedback": "Thank you for your feedback. We'll take note of it.",
    "default": "I'm sorry, I didn't quite understand that. Can you please rephrase?",
}

# Function to get chatbot response based on user input
def get_response(user_input):
    user_input = user_input.lower()
    sentiment = analyze_sentiment(user_input)
    
    if "hello" in user_input or "hi" in user_input:
        return responses["greeting"], sentiment
    elif "payment" in user_input:
        return responses["payment"], sentiment
    elif "return" in user_input or "refund" in user_input:
        return responses["return"], sentiment
    elif "shipping" in user_input:
        return responses["shipping"], sentiment
    elif sentiment == "positive":
        return responses["positive_feedback"], sentiment
    elif sentiment == "negative":
        return responses["negative_feedback"], sentiment
    elif sentiment == "neutral":
        return responses["neutral_feedback"], sentiment
    else:
        return responses["default"], sentiment

# Function to analyze sentiment using BERT
def analyze_sentiment(text):
    result = sentiment_analyzer(text)
    label = result[0]['label']
    if label == 'LABEL_1':  # Positive
        return "positive"
    elif label == 'LABEL_0':  # Negative
        return "negative"
    else:
        return "neutral"

# Streamlit app setup
st.title("Assistify")
st.subheader("Your personal shopping assistant!")

# Initialize the session state for conversation history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [("Assistify", "Hi! How can I help you today?")]
    
# Initialize previous conversations list in session state
if "previous_conversations" not in st.session_state:
    st.session_state["previous_conversations"] = []

# Function to start a new conversation
def start_new_conversation():
    # Save current conversation to previous conversations
    st.session_state["previous_conversations"].append(list(st.session_state["chat_history"]))
    # Clear current conversation history
    st.session_state["chat_history"] = [("Assistify", "Hi! How can I help you today?")]

# Capture the new user input
if "new_query" in st.session_state:
    user_query = st.session_state["new_query"]
else:
    user_query = ""

if user_query:
    # Add user message to the chat history
    st.session_state["chat_history"].append(("You", user_query))
    
    # Get the bot's response and sentiment after the user input
    response, sentiment = get_response(user_query)
    
    # Add bot response and sentiment to chat history
    st.session_state["chat_history"].append(("Bot", response))
    st.session_state["chat_history"].append(("Sentiment", f"Sentiment: {sentiment.capitalize()}"))

    # Clear the input box after submitting
    st.session_state["new_query"] = ""  # Reset new_query

# Sidebar for previous prompts with collapsible feature
with st.sidebar:
    st.markdown("## Assistify")  # App name in the sidebar
    st.markdown("### Previous Conversations")
    
    # Button to start a new conversation
    if st.button("Start New Conversation"):
        start_new_conversation()
    
    # Display previous conversations as clickable items
    with st.expander("Previous Conversations"):
        for idx, conversation in enumerate(st.session_state["previous_conversations"]):
            if st.button(f"Conversation {idx + 1}", key=f"conv_{idx}"):
                # Load selected conversation into chat history
                st.session_state["chat_history"] = conversation

# Main chat container
st.markdown("")

# Display chat history in main chat area
for sender, message in st.session_state["chat_history"]:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    elif sender == "Bot":
        st.markdown(f"**Bot:** {message}")
    elif sender == "Sentiment":
        st.markdown(f"*{message}*")

# Input field at the bottom
with st.container():
    user_input = st.text_input("Type your message here:", key="new_query", label_visibility="collapsed")
