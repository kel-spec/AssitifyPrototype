import streamlit as st
from textblob import TextBlob

# Set page config to make it more chat-like
st.set_page_config(page_title="Assistify - E-commerce Chatbot", layout="centered")

# Add custom CSS for styling
st.markdown("""
    <style>
    .chatbox {
        max-width: 600px;
        margin: 0 auto;
        background-color: #F9F9F9;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .user-msg, .bot-msg {
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
    }
    .user-msg {
        background-color: #D4F1F4;
        text-align: right;
    }
    .bot-msg {
        background-color: #E0E0E0;
        text-align: left;
    }
    .sentiment-msg {
        font-style: italic;
        color: #888;
    }
    </style>
    """, unsafe_allow_html=True)

# Define chatbot responses
responses = {
    "greeting": "Hello! How can I assist you with your shopping today?",
    "payment": "You can pay using credit cards, PayPal, or other online payment methods.",
    "return": "Our return policy allows returns within 30 days with a receipt.",
    "shipping": "We offer free shipping on orders over $50!",
    "positive_feedback": "Thank you for the positive feedback! We are happy you had a good experience.",
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
    else:
        return responses["default"], sentiment

# Function to analyze sentiment using TextBlob
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity  # Range: -1 (negative) to 1 (positive)
    
    if sentiment_score > 0.2:
        return "positive"
    elif sentiment_score < -0.2:
        return "negative"
    else:
        return "neutral"

# Streamlit app setup
st.title("Assistify - E-commerce Chatbot")
st.subheader("Your personal shopping assistant!")

# Input box for user query
user_query = st.text_input("Type your message here:", key="user_query")

# Initialize chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [("Bot", "Hi! How can I help you today?")]

# Process user input and update chat history
if user_query:
    response, sentiment = get_response(user_query)
    
    # Add user message and bot response to the chat history
    st.session_state["chat_history"].append(("You", user_query))
    st.session_state["chat_history"].append(("Bot", response))
    st.session_state["chat_history"].append(("Sentiment", f"Sentiment: {sentiment.capitalize()}"))

    # Clear the input box after submitting
    st.text_input("Type your message here:", value="", key="new_query")  # Reset input

# Display the chat history
for sender, message in st.session_state["chat_history"]:
    if sender == "You":
        st.markdown(f'<div class="chatbox"><div class="user-msg">{message}</div></div>', unsafe_allow_html=True)
    elif sender == "Bot":
        st.markdown(f'<div class="chatbox"><div class="bot-msg">{message}</div></div>', unsafe_allow_html=True)
    elif sender == "Sentiment":
        st.markdown(f'<div class="sentiment-msg">{message}</div>', unsafe_allow_html=True)
