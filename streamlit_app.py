import time
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sqlite3

# Set page config to make it more chat-like
st.set_page_config(page_title="Assistify 🛒", layout="wide")

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Database connection setup
conn = sqlite3.connect("chat_history.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        message TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

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

# Function to analyze sentiment using VADER
def analyze_sentiment(text):
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores["compound"]
    
    if compound_score > 0.2:
        return "positive"
    elif compound_score < -0.2:
        return "negative"
    else:
        return "neutral"

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

# Save chat to database
def save_to_db(sender, message):
    cursor.execute("INSERT INTO chat_history (sender, message) VALUES (?, ?)", (sender, message))
    conn.commit()

# Load chat history from database
def load_history():
    cursor.execute("SELECT sender, message FROM chat_history")
    return cursor.fetchall()

# Display typing animation
def display_typing(bot_message, text):
    for i in range(len(text) + 1):
        bot_message.markdown(f"**Bot:** {text[:i]}")
        time.sleep(0.05)

# Initialize session state variables
if "new_query" not in st.session_state:
    st.session_state["new_query"] = ""

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [("Assistify", "Hi! How can I help you today?")]

# Streamlit app setup
st.title("Assistify")
st.subheader("Your personal shopping assistant!")

# Load chat history
for sender, message in st.session_state["chat_history"]:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    elif sender == "Bot":
        st.markdown(f"**Bot:** {message}")
    elif sender == "Sentiment":
        st.markdown(f"*{message}*")

# Input for user queries
with st.container():
    user_input = st.text_input("Type your message here:", key="new_query", label_visibility="collapsed")

response, sentiment = None, None  # Initialize variables to avoid errors

if user_input:
    # Add user message to the chat history
    st.session_state["chat_history"].append(("You", user_input))
    save_to_db("You", user_input)

    # Display bot typing animation
    bot_message = st.empty()
    display_typing(bot_message, "...")

    # Get chatbot response
    response, sentiment = get_response(user_input)
    st.session_state["chat_history"].append(("Bot", response))
    save_to_db("Bot", response)

    # Display sentiment analysis result
    sentiment_message = f"Sentiment: {sentiment.capitalize()}"
    st.session_state["chat_history"].append(("Sentiment", sentiment_message))
    save_to_db("Sentiment", sentiment_message)

    # Clear input box safely
    st.session_state["new_query"] = ""

# Feedback feature
if response:  # Check if response is defined
    feedback = st.radio(
        "Was this response helpful?",
        ["Yes", "No"],
        key=f"feedback_{len(st.session_state['chat_history'])}"
    )
    save_to_db("Feedback", feedback)

# Sidebar for previous prompts
with st.sidebar:
    st.markdown("## Assistify")
    with st.expander("Previous Conversations"):
        for sender, message in st.session_state["chat_history"]:
            if sender == "You":
                st.markdown(f"**You:** {message}")
            elif sender == "Bot":
                st.markdown(f"**Bot:** {message}")
            elif sender == "Sentiment":
                st.markdown(f"*{message}*")
