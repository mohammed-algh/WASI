import streamlit as st
from YoutubeExtractor import startGet
import os
import re
import base64
from pathlib import Path
from word_cloud import generate_word_cloud
from streamlit_cookies_manager import EncryptedCookieManager
import datetime


st.set_page_config(
    page_title="WASI"
)


cookies = EncryptedCookieManager(
    # This prefix will get added to all your cookie names.
    # This way you can run your app on Streamlit Cloud without cookie name clashes with other apps.
    prefix="ktosiek/streamlit-cookies-manager/",
    # You should really setup a long COOKIES_PASSWORD secret if you're running on Streamlit Cloud.
    password=os.environ.get("COOKIES_PASSWORD", "a^#V3xpk[`YUkG8>"),
)
if not cookies.ready():
    # Wait for the component to load and send us current cookies.
    st.stop()



def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' style='max-width: 230px;' class='img-fluid'>".format(
      img_to_bytes(img_path)
    )
    return img_html




def analyze(link:str, classifier:str, progress_bar):
    try:
        if link.strip():  # check if the link parameter is not empty or whitespace
            recommendation, percentage, df = startGet(link, classifier, progress_bar)  # pass the progress bar object to the startGet function

            wordcloud_image = generate_word_cloud(df,percentage)
            st.image(wordcloud_image, width=300)

            if percentage > 60:
                with st.container():
                    st.success(f"{recommendation}")
            elif percentage >=50:
                st.warning(f"{recommendation}")
            else:
                st.error(f"{recommendation}")
            cookies[str(datetime.datetime.now())] = f"{str(percentage)};{str(classifier)};{str(datetime.datetime.now())}"
            cookies.save()
            progress_bar.empty()  # clear the progress bar once analysis is done
        else:
            return "Invalid link"

    except Exception as e:
        return str(e)

st.markdown("<p style='text-align: center; color: grey;'>"+img_to_html('Wasi Logo.png')+"</p>", unsafe_allow_html=True) #Centered Logo

st.markdown("<h3 style='text-align: center;'>WASI | Arabic Youtube Recommender</h3>", unsafe_allow_html=True)

link = st.text_input("Enter Youtube Link Here", placeholder="E.g. https://www.youtube.com")

with st.expander("Advance Settings"):
    radio = st.radio("Choose Classifier:", options=("Naive Bayes (Recommended)","SVM","Random Forest","Decision Tree","KNN", "Logistic Regression"), horizontal=True )

message_placeholder = st.empty()  # initialize the message placeholder

progress_placeholder = st.empty()  # initialize the progress placeholder

if st.button("Analyze"):
    if link.strip():
        progress_bar = progress_placeholder.progress(0)  # initialize the progress bar with 0% inside the progress_placeholder

        message_message = analyze(link, radio,progress_bar)
        if message_message:
            message_placeholder.write("<span style='color: #f9c13c;'>"+message_message+"</span>", unsafe_allow_html=True)
        else:
            message_placeholder.empty()  # clear the error message if there are no errors
        progress_placeholder.empty()  # clear the progress_placeholder once analysis is done
        progress_bar.empty()  # clear the progress bar once analysis is done
    else:
         message_placeholder.write("<span style='color: #f9c13c;'>Invalid link</span>", unsafe_allow_html=True)



st.markdown("<p style='text-align: center; color: grey;'>"+img_to_html('Uni Logo.png')+"</p>", unsafe_allow_html=True) #Centered Logo
#Remove hamburger menu + header+  footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stProgress > div > div > div > div {
                background-image: radial-gradient(ellipse at center, #ff6464, #ff0000);
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


