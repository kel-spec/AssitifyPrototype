import time
import streamlit as st
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer

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
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove non-alphabet characters
    return text

# Function to analyze sentiment using the logistic regression model
def analyze_sentiment(text):
    text = preprocess_text_basic(text)
    input_tfidf = tfidf_vectorizer.transform([text])
    sentiment = log_reg_model.predict(input_tfidf)
    
    sentiment_map = {0: "negative", 4: "positive"}
    return sentiment_map.get(sentiment[0], "neutral")

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

# Function to get chatbot response based on user input and sentiment
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

# Initialize the session state for chat history and input management
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [("Assistify", "Hi! How can I help you today?")]

# Define a function to handle new user input
def handle_new_input(user_input):
    if user_input:
        # Add user input to chat history
        st.session_state["chat_history"].append(("You", user_input))
        
        # Get chatbot response and sentiment
        response, sentiment = get_response(user_input)
        
        # Add response and sentiment to chat history
        st.session_state["chat_history"].append(("Assistify", response))
        st.session_state["chat_history"].append(("Sentiment", f"Sentiment: {sentiment.capitalize()}"))

# Sidebar with About Section
with st.sidebar:
    st.markdown("## Assistify")
    st.markdown("### About")
    st.info(
        """
        **Assistify** is your personalized shopping assistant powered by machine learning.
        It analyzes your feedback and provides tailored responses. Feel free to explore our features
        like sentiment analysis and contextual responses to improve your shopping experience!
        """
    )
    st.markdown("### Previous Conversations")
    
    # Button to start a new conversation
    if st.button("Start New Conversation"):
        st.session_state["chat_history"] = [("Assistify", "Hi! How can I help you today?")]

# Main Chat Interface
st.title("Assistify 🛒")
st.markdown("Your personalized shopping assistant!")

# Display chat history
for sender, message in st.session_state["chat_history"]:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    elif sender == "Assistify":
        st.markdown(f"**Assistify:** {message}")
    elif sender == "Sentiment":
        st.markdown(f"*{message}*")

# User input section
user_input = st.text_input("Type your message here:", key="new_query")

# Handle user input on Enter
if user_input:
    handle_new_input(user_input)
    st.session_state["new_query"] = ""  # Reset the input field (not user_input)
