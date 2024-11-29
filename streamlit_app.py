import streamlit as st
from textblob import TextBlob

# Set page config to make it more chat-like
st.set_page_config(page_title="Assistify", layout="wide")

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

# CSS styling for customization (Background color, font, etc.)
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f9;  /* Background color */
        font-family: 'Arial', sans-serif;  /* Font */
        color: #333333;  /* Font color */
    }

    .sidebar .sidebar-content {
        background-color: #ffffff;
        padding: 15px;
        font-family: 'Arial', sans-serif;
        color: #333333;
    }

    .streamlit-expanderHeader {
        font-size: 18px;
        font-weight: bold;
        color: #333333;
    }

    .streamlit-expanderContent {
        font-size: 14px;
        color: #555555;
    }

    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 5px;
    }

    .stButton>button:hover {
        background-color: #0056b3;
    }

    .stTextInput>div>input {
        background-color: #ffffff;
        border: 1px solid #cccccc;
        border-radius: 5px;
    }

    .stTextInput>div>input:focus {
        border-color: #007bff;
    }

    </style>
    """, unsafe_allow_html=True
)

# Streamlit app setup
st.title("Assistify")
st.subheader("Your personal shopping assistant!")

# Initialize chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [("Assistify", "Hi! How can I help you today?")]

# Process user input and update chat history
if "new_query" in st.session_state:
    user_query = st.session_state["new_query"]
else:
    user_query = ""

if user_query:
    response, sentiment = get_response(user_query)
    
    # Add user message and bot response to the chat history
    st.session_state["chat_history"].append(("You", user_query))
    st.session_state["chat_history"].append(("Bot", response))
    st.session_state["chat_history"].append(("Sentiment", f"Sentiment: {sentiment.capitalize()}"))

    # Clear the input box after submitting
    st.session_state["new_query"] = ""

# Sidebar for previous prompts with collapsible feature
with st.sidebar:
    st.markdown("## Assistify")  # App name in the sidebar
    with st.expander("Previous Conversations"):
        for i, (sender, message) in enumerate(st.session_state["chat_history"]):
            if sender == "You":
                st.markdown(f"**You:** {message}")
            elif sender == "Bot":
                st.markdown(f"**Bot:** {message}")
            elif sender == "Sentiment":
                st.markdown(f"*{message}*")

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
