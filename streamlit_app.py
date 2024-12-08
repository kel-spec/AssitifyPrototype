import time
import streamlit as st
import pickle
import os

# Set page config to make it more chat-like
st.set_page_config(page_title="Assistify 🛒", layout="wide")

# Load the pre-trained model and vectorizer
@st.cache_resource
def load_models():
    with open(os.path.join("models", "log_reg_model.pkl"), "rb") as model_file:
        log_reg_model = pickle.load(model_file)
    with open(os.path.join("models", "tfidf_vectorizer.pkl"), "rb") as vectorizer_file:
        tfidf_vectorizer = pickle.load(vectorizer_file)
    return log_reg_model, tfidf_vectorizer

log_reg_model, tfidf_vectorizer = load_models()

# Chatbot response dictionary
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

# Analyze sentiment using the trained model
def analyze_sentiment(text):
    text_vectorized = tfidf_vectorizer.transform([text])
    prediction = log_reg_model.predict(text_vectorized)[0]
    return prediction

# Generate chatbot responses
def generate_response(user_input):
    user_input = user_input.lower()
    sentiment = analyze_sentiment(user_input)
    
    if "hello" in user_input or "hi" in user_input:
        return responses["greeting"], "Sentiment analysis was not needed for this response."
    elif "payment" in user_input:
        return responses["payment"], "Sentiment analysis was not needed for this response."
    elif "return" in user_input or "refund" in user_input:
        return responses["return"], "Sentiment analysis was not needed for this response."
    elif "shipping" in user_input:
        return responses["shipping"], "Sentiment analysis was not needed for this response."
    elif sentiment == "positive":
        return responses["positive_feedback"], "The sentiment of your input was classified as Positive."
    elif sentiment == "negative":
        return responses["negative_feedback"], "The sentiment of your input was classified as Negative."
    elif sentiment == "neutral":
        return responses["neutral_feedback"], "The sentiment of your input was classified as Neutral."
    else:
        return responses["default"], "The bot could not determine the sentiment for this response."

# Initialize the session state for conversation history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [("Assistify", "Hi! How can I help you today?")]

# Initialize user input in session state
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Sidebar for previous prompts
with st.sidebar:
    st.markdown("## Assistify 🛒")
    st.markdown("### About")
    st.write("Assistify is your personalized shopping assistant, here to answer your queries and provide sentiment-based feedback.")

# Display chat history
st.title("Assistify 🛒")
st.markdown("Your personalized shopping assistant!")
st.markdown("---")

# Display chat messages
for sender, message in st.session_state["chat_history"]:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    elif sender == "Assistify":
        st.markdown(f"**Assistify:** {message}")
    elif sender == "Explanation":
        st.markdown(f"*{message}*")

# User input section
user_input = st.text_input("Type your message:", key="user_input")

if user_input:
    # Get response and explanation
    response, explanation = generate_response(user_input)
    
    # Add user and bot messages to the chat history
    st.session_state["chat_history"].append(("You", user_input))
    st.session_state["chat_history"].append(("Assistify", response))
    st.session_state["chat_history"].append(("Explanation", explanation))
    
    # Clear the input box
    st.session_state["user_input"] = ""
