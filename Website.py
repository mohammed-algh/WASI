from YoutubeExtractor import startGet, get_video_info, get_video_id_no_bar
import os
import base64
from pathlib import Path
from word_cloud import generate_word_cloud
from streamlit_cookies_manager import EncryptedCookieManager
import datetime
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
import streamlit as st
from streamlit.components.v1 import iframe
import time

wordcloud_image = None


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' style='max-width: 230px;' class='img-fluid'>".format(
        img_to_bytes(img_path)
    )
    return img_html


def wasi():
    st.set_page_config(
        page_title="WASI | Arabic Youtube Recommender", initial_sidebar_state="collapsed", layout="wide"
    )

    cookies = EncryptedCookieManager(
        # This prefix will get added to all your cookie names.
        # This way you can run your app on Streamlit Cloud without cookie name clashes with other apps.
        prefix="WASI/History/",
        # You should really setup a long COOKIES_PASSWORD secret if you're running on Streamlit Cloud.
        password=os.environ.get("COOKIES_PASSWORD", "a^#V3xpk[`YUkG8>"),

    )
    if not cookies.ready():
        # Wait for the component to load and send us current cookies.
        st.stop()

    def analyze(link: str, classifier: str, progress_bar):
        try:
            if link.strip():  # check if the link parameter is not empty or whitespace
                recommendation, percentage, df, video_title = startGet(link, classifier,
                                                                       progress_bar)  # pass the progress bar object to the startGet function
                global wordcloud_image
                video_id = get_video_id_no_bar(link)
                video_info = get_video_info(video_id)
                progress_bar.progress(90)
                wordcloud_image = generate_word_cloud(df, percentage)
                progress_bar.progress(100)
                time.sleep(0.5)
                if percentage > 60:
                    with st.container():
                        st.success(f"{recommendation}", icon="❇️")
                elif percentage >= 50:
                    st.warning(f"{recommendation}", icon="⚖️")
                else:
                    st.error(f"{recommendation}", icon="❤️‍🩹")
                with st.expander("**Display Video Details**"):
                    if video_info:
                        st.write('**Title:**', video_info['title'])
                        st.write('**Number of Comments:**', video_info['comment_count'])
                        st.write('**Channel Name:**', video_info['channel_name'])
                        st.write('**Publish Date:**', video_info['publish_date'])
                        #Generate embed code
                        embed_code = f"https://www.youtube.com/embed/{video_id}"

                        #Display the embedded video
                        st.components.v1.iframe(embed_code)
                    else:
                        st.write('Could not retrieve video information.')
                with st.expander("**Display Most Used Words**"):
                    st.image(wordcloud_image)
                cookies[
                    str(datetime.datetime.now())] = f"{str(video_title)};{str(percentage)};{str(classifier)};{str(datetime.datetime.now())}"
                cookies.save()
                progress_bar.empty()  # clear the progress bar once analysis is done
            else:
                return "Invalid link"

        except Exception as e:
            return str(e)

    st.markdown("<p style='text-align: center; color: grey;'>" + img_to_html("images/Wasi Logo.png") + "</p>",
                unsafe_allow_html=True)  # Centered Logo

    st.markdown("<h3 style='text-align: center;'>WASI | Arabic Youtube Recommender</h3>", unsafe_allow_html=True)

    # horizontal Menu
    if 'session_state' not in st.session_state:
        st.session_state['session_state'] = {}
    col1, col2, col3 = st.columns((2.5, 5, 2.5))
    with col2:

        selected2 = option_menu(None, ["WASI", "History", "Logout"],
                                icons=['youtube', 'clock-history', 'box-arrow-left'],
                                menu_icon="cast", default_index=0, orientation="horizontal")

        if selected2 == "History":
            switch_page("history")
        if selected2 == "Logout":
            switch_page("login")
        st.text("Sample Videos:")
        b1,b2,b3= st.columns((0.33,0.33,0.33))
        with b1:
            if st.button("Positive"):
                st.session_state.session_state['link'] = "https://youtu.be/fUxLgISJqCI"  # Set the link to ٍSample 1
            
        with b2:   
            if st.button("Neutral"):
                st.session_state.session_state['link'] = "https://youtu.be/6Nm3y0A8Fqk"  # Set the link to Sample 2
        with b3:
            if st.button("Negative"):
                st.session_state.session_state['link'] = "https://youtu.be/igIdKdjU5WE"  # Set the link to Sample 3
        
        
        with st.form("analysis"):
            link = st.text_input("Enter Youtube Link Here", value=st.session_state['session_state'].get('link', ''),  placeholder="E.g. https://www.youtube.com")

            with st.expander("Advance Settings"):
                radio = st.radio("Choose Classifier:", options=(
                "Naive Bayes (Recommended)", "SVM", "Random Forest", "Decision Tree", "KNN", "Logistic Regression"),
                                 horizontal=True)
                radio = radio if radio != "Naive Bayes (Recommended)" else "Naive Bayes"
            progress_placeholder = st.empty()  # initialize the progress placeholder
            in1, in2, in3, = st.columns((2.3, 2.2, 2.5))
            with in2:

                message_placeholder = st.empty()  # initialize the message placeholder
                button = st.form_submit_button("Analyze")
            in1, in2, in3, = st.columns((1.2, 8, 1.5))
            with in2:
                if button:
                    if link.strip():
                        progress_bar = progress_placeholder.progress(
                            0)  # initialize the progress bar with 0% inside the progress_placeholder

                        message_message = analyze(link, radio, progress_bar)
                        if message_message:
                            message_placeholder.write("<span style='color: #f9c13c;'>" + message_message + "</span>",
                                                      unsafe_allow_html=True)
                        else:
                            message_placeholder.empty()  # clear the error message if there are no errors
                        progress_placeholder.empty()  # clear the progress_placeholder once analysis is done
                        progress_bar.empty()  # clear the progress bar once analysis is done
                    else:
                        message_placeholder.write("<span style='color: #f9c13c;'>Invalid link</span>",
                                                  unsafe_allow_html=True)

    st.markdown("<p style='text-align: center; color: grey;'>" + img_to_html('images/Uni Logo.png') + "</p>",
                unsafe_allow_html=True)  # Centered Logo
    # Remove hamburger menu + header+  footer

    styles = """
        <style>
        [data-testid="collapsedControl"] {
            display: none
        }
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                .stProgress > div > div > div > div {
                    background-image: radial-gradient(ellipse at center, #ff6464, #ff0000);
                }
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.egzxvld5 > div.block-container.css-z5fcl4.egzxvld4 > div:nth-child(1) > div > div.css-ocqkz7.e1tzin5v3 > div.css-keje6w.e1tzin5v1 > div:nth-child(1) > div > div.css-ocqkz7.e1tzin5v3 > div:nth-child(1) > div:nth-child(1) > div > div > div > button
                { background:#28a745; color:white;}
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.egzxvld5 > div.block-container.css-z5fcl4.egzxvld4 > div:nth-child(1) > div > div.css-ocqkz7.e1tzin5v3 > div.css-keje6w.e1tzin5v1 > div:nth-child(1) > div > div.css-ocqkz7.e1tzin5v3 > div:nth-child(2) > div:nth-child(1) > div > div > div > button
                { background:#eea236; color:white;}
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.egzxvld5 > div.block-container.css-z5fcl4.egzxvld4 > div:nth-child(1) > div > div.css-ocqkz7.e1tzin5v3 > div.css-keje6w.e1tzin5v1 > div:nth-child(1) > div > div.css-ocqkz7.e1tzin5v3 > div:nth-child(3) > div:nth-child(1) > div > div > div > button
                { background:#f44336; color:white;}
        </style>
    """
    st.markdown(styles, unsafe_allow_html=True)

    # Initialize a session state variable that tracks the sidebar state (either 'expanded' or 'collapsed').


if __name__ == '__main__':
    wasi()
