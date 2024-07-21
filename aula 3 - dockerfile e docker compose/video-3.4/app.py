import streamlit as st
import pandas as pd
import joblib

model = joblib.load('model.pkl')
vectorizer = joblib.load('model-vectorizer.pkl')

LABELS = ["Negativa", "Neutra", "Positiva"]

def predict_sentiment(model, text, vectorizer, sentiment_labels):
    processed_text = vectorizer.transform([text])
    prediction = model.predict(processed_text)[0]
    sentiment = sentiment_labels[prediction]
    return sentiment, prediction

st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items={})
st.title('Análise de sentimento de tweets - Regressão logística e TF-IDF')
input_data = st.text_input('Insira o tweet em inglês para análise de sentimento')
if input_data:
    sentiment, prediction = predict_sentiment(
        model=model,
        text=input_data,
        vectorizer=vectorizer,
        sentiment_labels=LABELS
    )
    st.write('Predição:', sentiment)
