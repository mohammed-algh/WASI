from YoutubeExtractor import startGet,get_video_info,get_video_id_no_bar
import os
import base64
from pathlib import Path
from word_cloud import generate_word_cloud
from streamlit_cookies_manager import EncryptedCookieManager
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
import streamlit as st
import time

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' style='max-width: 230px;' class='img-fluid'>".format(
      img_to_bytes(img_path)
    )
    return img_html
def authenticate(username, password):
    return username == "admin" and password == "123321"

def Login():
    st.set_page_config(
        page_title="WASI | Login", initial_sidebar_state="collapsed"
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
    st.markdown("<p style='text-align: center; color: grey;'>"+img_to_html('Wasi Logo.png')+"</p>", unsafe_allow_html=True) #Centered Logo
    st.markdown("<h3 style='text-align: center;'>WASI | Arabic Youtube Recommender</h3>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        spinner_placeholder = st.empty()
        status_placeholder = st.empty()
        
        if st.form_submit_button("Login"):
            with spinner_placeholder:
                with st.spinner("Authenticating..."):
                    time.sleep(1)
                    if authenticate(username, password):
                        spinner_placeholder.empty()
                        status_placeholder.success("Correct credentials, you will be redirected shortly...")
                        time.sleep(1)
                        switch_page("Website")
                    else:
                        status_placeholder.error("Incorrect username or password")
    st.markdown("<p style='text-align: center; color: grey;'>"+img_to_html('Uni Logo.png')+"</p>", unsafe_allow_html=True) #Centered Logo



    # Initialize a session state variable that tracks the sidebar state (either 'expanded' or 'collapsed').
if __name__ == '__main__':
    Login()