import time
import streamlit as st
import pickle
import re
from textblob import TextBlob  # Using TextBlob for sentiment analysis

# Set Streamlit page configuration
st.set_page_config(page_title="Assistify 🛒", layout="wide")

# Load pre-trained models and vectorizer
@st.cache_resource
def load_models():
    with open("models/log_reg_model.pkl", "rb") as model_file:
        log_reg_model = pickle.load(model_file)
    with open("models/tfidf_vectorizer.pkl", "rb") as vectorizer_file:
        tfidf_vectorizer = pickle.load(vectorizer_file)
    return log_reg_model, tfidf_vectorizer

log_reg_model, tfidf_vectorizer = load_models()

# Basic preprocessing function
def preprocess_text_basic(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove non-alphabet characters
    return text

# Function to analyze sentiment using TextBlob
def analyze_sentiment(text):
    text = preprocess_text_basic(text)
    blob = TextBlob(text)
    
    # Classify the sentiment
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"

# Define chatbot responses
responses = {
    "greeting": "Hello! How can I assist you with your shopping today?",
    "payment": "You can pay using credit cards, PayPal, or other online payment methods.",
    "return": "Our return policy allows returns within 30 days with a receipt.",
    "shipping": "We offer free shipping on orders over $50!",
    "order_status": "You can track your order in the 'Orders' section of your account.",
    "positive_feedback": "Thank you for your positive feedback! We are happy you had a good experience.",
    "negative_feedback": "We're sorry to hear about your experience. We'll try to improve.",
    "neutral_feedback": "Thank you for your feedback. We'll take note of it.",
    "default": "I'm sorry, I didn't quite understand that. Can you please rephrase?",
}

# Function to get chatbot response based on user input and sentiment
def get_response(user_input):
    user_input = user_input.lower()
    sentiment = analyze_sentiment(user_input)
    
    # Intent matching based on more comprehensive keyword checks
    if "hello" in user_input or "hi" in user_input:
        return responses["greeting"], sentiment
    elif "payment" in user_input or "how to pay" in user_input:
        return responses["payment"], sentiment
    elif "return" in user_input or "refund" in user_input:
        return responses["return"], sentiment
    elif "shipping" in user_input or "shipping fee" in user_input or "delivery" in user_input:
        return responses["shipping"], sentiment
    elif "order" in user_input or "track" in user_input:
        return responses["order_status"], sentiment
    elif sentiment == "positive":
        return responses["positive_feedback"], sentiment
    elif sentiment == "negative":
        return responses["negative_feedback"], sentiment
    elif sentiment == "neutral":
        return responses["neutral_feedback"], sentiment
    else:
        return responses["default"], sentiment
        
# Streamlit app setup
st.title("Assistify 🛒")
st.subheader("Your personal shopping assistant!")

# Initialize the session state for conversation history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [("Assistify", "Hi! How can I help you today?")]
    
# Initialize previous conversations list in session state
if "previous_conversations" not in st.session_state:
    st.session_state["previous_conversations"] = []

# Function to start a new conversation
def start_new_conversation():
    st.session_state["previous_conversations"].append(list(st.session_state["chat_history"]))
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
    
    # Show typing animation
    typing_placeholder = st.empty()  # Placeholder for typing animation
    typing_placeholder.markdown("**Bot is typing...**")
    
    # Add a delay to simulate typing animation with smooth character-by-character effect
    for i in range(1, len(response) + 1):
        typing_placeholder.markdown(f"**Bot:** {response[:i]}")
        time.sleep(0.05)  # Adjust the speed here for smoother typing
    
    # After typing animation, add the bot response and sentiment to chat history
    st.session_state["chat_history"].append(("Bot", response))
    st.session_state["chat_history"].append(("Sentiment", f"Sentiment: {sentiment.capitalize()}"))
    
    # Clear the input box after submitting
    st.session_state["new_query"] = ""  # Reset new_query

# Sidebar for previous prompts with collapsible feature
with st.sidebar:
    st.markdown("## Assistify")  # App name in the sidebar
    st.markdown("### About")
    st.info(
        """
        Assistify helps you with shopping questions like payment, returns, and shipping.
        Get personalized responses based on your input sentiment.
        """
    )
    st.markdown("### Previous Conversations")
    
    # Button to start a new conversation
    if st.button("Start New Conversation"):
        start_new_conversation()
    
    # Display previous conversations as clickable items
    with st.expander("Previous Conversations"):
        for idx, conversation in enumerate(st.session_state["previous_conversations"]):
            if st.button(f"Conversation {idx + 1}", key=f"conv_{idx}"):
                st.session_state["chat_history"] = conversation

# Custom CSS to fix input box below the title and prevent overlap
st.markdown("""
    <style>
        .stTextInput input {
            width: 100%;
            font-size: 16px;
            padding: 10px;
        }
        .chat-history {
            max-height: 400px;
            overflow-y: scroll;
            padding-right: 10px;
        }
        .stTextInput {
            position: fixed;
            top: 200px;  /* Adjust to place input box below the title */
            left: 0;
            right: 1;
            z-index: 10;
            padding: 10px;
            background-color: transparent; /* Remove the white box */
        }
    </style>
""", unsafe_allow_html=True)

# Main container with scrollable chat history
st.markdown("<div class='chat-history'>", unsafe_allow_html=True)
for sender, message in st.session_state["chat_history"]:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    elif sender == "Bot":
        st.markdown(f"**Bot:** {message}")
    elif sender == "Sentiment":
        st.markdown(f"*{message}*")
st.markdown("</div>", unsafe_allow_html=True)

# Input box that stays fixed below the title
with st.container():
    user_input = st.text_input("Type your message here:", key="new_query")
