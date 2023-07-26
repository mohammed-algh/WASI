from YoutubeExtractor import startGet, get_video_info, get_video_id_no_bar
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
        page_title="واصي | تسجيل الدخول", initial_sidebar_state="collapsed"
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
    st.markdown("<p style='text-align: center; color: grey;'>" + img_to_html('images/Wasi Logo.png') + "</p>",
                unsafe_allow_html=True)  # Centered Logo
    st.markdown("<h3 style='text-align: center;'><br></h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns((2.5, 5, 2.5))
    with col2:
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password")
            spinner_placeholder = st.empty()
            status_placeholder = st.empty()

            in1, in2, in3, = st.columns((3.7, 4, 2.3))
            with in2:
                if st.form_submit_button("دخول"):
                    with spinner_placeholder:
                        with st.spinner("توثيق الحساب..."):
                            time.sleep(1)
                            if authenticate(username, password):
                                spinner_placeholder.empty()
                                status_placeholder.success("تم التوثيق بنجاح! يتم الآن نقلك لواصي...")
                                time.sleep(1)
                                switch_page("Website")
                            else:
                                status_placeholder.error("اسم المستخدم أو كلمة المرور غير صحيحان.")
    st.markdown("<p style='text-align: center; color: grey;'>" + img_to_html('images/Uni Logo.png') + "</p>",
                unsafe_allow_html=True)  # Centered Logo

    # Remove hamburger menu + header+  footer
    styles = """
        <style>
        @font-face {
            font-family: 'arabic';
            font-style: normal;
            font-weight: 400;
            src: url("https://db.onlinewebfonts.com/t/7712e50ecac759e968ac145c0c4a6d33.woff2")format("woff2");
        }

        html, body, [class*="css"]  {
            font-family: 'arabic';
            direction: rtl;
            text-align: right;
        }
        [data-testid="collapsedControl"] {
            display: none
        }
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                .stProgress > div > div > div > div {
                    background-image: radial-gradient(ellipse at center, #ff6464, #ff0000);
                }
        </style>
    """
    st.markdown(styles, unsafe_allow_html=True)
    # Initialize a session state variable that tracks the sidebar state (either 'expanded' or 'collapsed').


if __name__ == '__main__':
    Login()
