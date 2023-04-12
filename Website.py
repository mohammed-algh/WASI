import streamlit as st
from YoutubeExtractor import startGet
def analyze(link:str, classifier:str):
    try:
        recommendation = startGet(link, classifier)
        st.write(f"{recommendation}")
    except Exception as e:
        st.write(f"{e}")


st.title("WASI | Arabic Youtube Recommender")
st.markdown("---")
link = st.text_input("Enter Youtube Link Here", placeholder="E.g. https://www.youtube.com")
radio = st.radio("Choose Classifier:", options=("Naive Bayes (Recommended)","SVM","Random Forest","Decision Tree","KNN", "Logistic Regression"), )
btn_analyze = st.button("Analyze",on_click=analyze(link,radio))
