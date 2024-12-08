import streamlit as st
import pickle

# Load model and vectorizer
@st.cache_resource
def load_models():
    with open("models/log_reg_model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    with open("models/tfidf_vectorizer.pkl", "rb") as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    return model, vectorizer

log_reg_model, tfidf_vectorizer = load_models()

# Enhanced response logic
responses = {
    "positive": [
        "That's fantastic to hear! We're thrilled you had a great experience.",
        "Thank you for the positive feedback! We appreciate your kind words.",
        "We're so happy to hear that! Your satisfaction means everything to us."
    ],
    "negative": [
        "We're sorry to hear about your experience. Could you share more details so we can improve?",
        "We apologize for any inconvenience caused. We're here to make things right.",
        "Thank you for your feedback. We'll work on improving the areas where we fell short."
    ],
    "neutral": [
        "Thank you for your feedback. We value your input and will keep it in mind.",
        "We appreciate your thoughts. If you have more details, feel free to share.",
        "Thanks for reaching out. Let us know how we can assist further!"
    ],
}

# Function to analyze sentiment using the custom model
def analyze_sentiment(text):
    text_transformed = tfidf_vectorizer.transform([text])
    prediction = log_reg_model.predict(text_transformed)[0]
    if prediction == 4:  # Positive sentiment in dataset
        return "positive"
    elif prediction == 0:  # Negative sentiment in dataset
        return "negative"
    else:
        return "neutral"

# Function to generate a chatbot response
def generate_response(user_input):
    sentiment = analyze_sentiment(user_input)
    if sentiment == "positive":
        response = st.session_state.responses[sentiment][0]
    elif sentiment == "negative":
        response = st.session_state.responses[sentiment][0]
    else:
        response = st.session_state.responses[sentiment][0]

    # Optional: Explanation of the sentiment detection
    explanation = f"The sentiment was analyzed as **{sentiment.upper()}**."
    return response, explanation

# Streamlit app
st.title("Assistify")
st.subheader("Your shopping assistant, powered by AI!")

# Initialize responses in session state
if "responses" not in st.session_state:
    st.session_state.responses = responses

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [("Assistify", "Hi! How can I assist you today?")]

# User input
user_input = st.text_input("Type your message:", key="user_input")
if user_input:
    response, explanation = generate_response(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Assistify", response))
    st.session_state.chat_history.append(("Explanation", explanation))
    st.session_state.user_input = ""

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    elif sender == "Assistify":
        st.markdown(f"**Bot:** {message}")
    elif sender == "Explanation":
        st.markdown(f"*{message}*")
