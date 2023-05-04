import streamlit as st
import re
import os
from streamlit_cookies_manager import EncryptedCookieManager
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from Website import img_to_html


def history():
    st.set_page_config(
        page_title="History | WASI",
        initial_sidebar_state="collapsed", layout="wide"
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

    col1, col2, col3 = st.columns((2.5, 5, 2.5))
    with col2:
        st.markdown("<p style='text-align: center; color: grey;'>" + img_to_html('images/Wasi Logo.png') + "</p>",
                    unsafe_allow_html=True)  # Centered Logo

        st.markdown("<h3 style='text-align: center;'>WASI | Arabic Youtube Recommender</h3>", unsafe_allow_html=True)
        # horizontal Menu
        selected2 = option_menu(None, ["WASI", "History", "Logout"],
                                icons=['youtube', 'clock-history', 'box-arrow-left'],
                                menu_icon="cast", default_index=1, orientation="horizontal")
        if selected2 == "WASI":
            switch_page("Website")
        if selected2 == "Logout":
            switch_page("login")

        df = pd.DataFrame(columns=["Title", "Percentage", "Classifier", "Date"])
        matches = re.findall(r"\{(.*?)\}", str(cookies.keys()))
        keys = str(matches[0]).split(",")
        if len(keys) > 1:
            cleand_keys = []
            for i in keys:
                between_quotes = i.split("'")[1]
                before_colon = between_quotes.split("':")[0]
                cleand_keys.append(before_colon)
            cleand_keys.pop(0)
            for i in cleand_keys[::-1]:
                data = cookies[str(i)].split(";")
                df = df.append({"Title": str(data[0]), "Percentage": str(data[1]) + "%", "Classifier": data[2],
                                "Date": data[3][:19]}, ignore_index=True)
            df.index += 1
            st.table(df)

        else:
            st.write("No History")

    st.markdown("<p style='text-align: center; color: grey;'>" + img_to_html('images/Uni Logo.png') + "</p>",
                unsafe_allow_html=True)  # Centered Logo
    # Remove hamburger menu + header+  footer

    styles = """
        <style>
            div[data-testid="stSidebarNav"] {display: none;}
            .css-1iyw2u1 {
            display: none;
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


if __name__ == '__main__':
    history()
