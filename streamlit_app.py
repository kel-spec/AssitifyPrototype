import datetime
import time
import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Assistify 🛒", layout="wide")

# Load pre-trained sentiment analysis pipeline
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis")

sentiment_analyzer = load_sentiment_model()

# Function to analyze sentiment using BERT
def analyze_sentiment_bert(text):
    result = sentiment_analyzer(text)[0]
    sentiment = result['label'].lower()  # 'positive' or 'negative'
    score = result['score']  # Confidence score
    return sentiment, score

# Bot response dictionary
responses = {
    "greeting": "Hello! Here's a list of questions you can ask me: Payment, Return, Shipping, Order Status.",
    "payment": "You can pay using credit cards, GCash, or other online payment methods.",
    "return": "Our return policy allows returns within 30 days with a receipt.",
    "shipping": "We offer free shipping on orders over ₱300!",
    "default": "I'm sorry, I didn't quite understand that. Can you please rephrase?"
}

# Function to get chatbot response based on user input
def get_response(user_input):
    user_input = user_input.lower()
    sentiment, score = analyze_sentiment_bert(user_input)

    # Time-based greeting
    current_hour = datetime.datetime.now().hour
    if "hello" in user_input or "hi" in user_input:
        return responses["greeting"], sentiment, score
    elif "payment" in user_input:
        return responses["payment"], sentiment, score
    elif "return" in user_input or "refund" in user_input:
        return responses["return"], sentiment, score
    elif "shipping" in user_input:
        return responses["shipping"], sentiment, score
    else:
        return responses["default"], sentiment, score

# Streamlit app setup
st.title("Assistify 🛒")
st.subheader("Your personal shopping assistant!")

# Initialize session state for chat history and 'new_query' if not already initialized
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [("Assistify", "Hi! How can I help you today?")]

if "new_query" not in st.session_state:
    st.session_state["new_query"] = ""

# Input field for user query
user_query = st.text_input("", key="new_query", label_visibility="collapsed")

# Button to submit the query
if st.button("Submit Query"):
    if user_query:
        # Add user message to chat history
        st.session_state["chat_history"].append(("You", user_query))

        # Get the bot's response and sentiment
        response, sentiment, score = get_response(user_query)

        # Typing animation placeholder
        typing_placeholder = st.empty()
        typing_placeholder.markdown("**Bot is typing...**")

        # Simulate typing animation
        for i in range(1, len(response) + 1):
            typing_placeholder.markdown(f"**Bot:** {response[:i]}")
            time.sleep(0.05)

        # Remove the typing placeholder and add bot response to chat history
        typing_placeholder.empty()
        st.session_state["chat_history"].append(("Bot", response))

        # Add sentiment analysis result to chat history
        st.session_state["chat_history"].append(("Sentiment", f"{sentiment.capitalize()} (Confidence: {score:.2f})"))

        # Clear input box after processing the query
        st.session_state["new_query"] = ""

# Display the chat history
for sender, message in st.session_state["chat_history"]:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    elif sender == "Bot":
        st.markdown(f"**Bot:** {message}")
    elif sender == "Sentiment":
        st.markdown(f"*Sentiment: {message}*")

# Sidebar with app info
with st.sidebar:
    st.markdown("## Assistify")
    st.info(
        """
        Assistify helps you with shopping questions like payment, returns, and shipping. 
        Get personalized responses based on your input sentiment.
        """
    )
