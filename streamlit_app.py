import streamlit as st
from textblob import TextBlob

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
st.title("E-commerce Chatbot")
st.subheader("Welcome to our shopping assistant chatbot!")

# Input box for user query
user_query = st.text_input("Type your question or feedback here:", key="user_query")

# Chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Process user input
if user_query:
    response, sentiment = get_response(user_query)
    
    # Add both the response and the sentiment to the chat history
    st.session_state["chat_history"].append(("You", user_query))
    st.session_state["chat_history"].append(("Chatbot", response))
    
    # Display sentiment analysis result
    st.session_state["chat_history"].append(("Sentiment", f"Sentiment: {sentiment.capitalize()}"))
    
    st.text_input("Type your question or feedback here:", value="", key="new_query")  # Clear input box

# Display chat history
for sender, message in st.session_state["chat_history"]:
    st.write(f"**{sender}:** {message}")
