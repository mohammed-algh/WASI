import streamlit as st
import re
import os
from streamlit_cookies_manager import EncryptedCookieManager

st.set_page_config(
    page_title="History"
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


st.title("History")


matches = re.findall(r"\{(.*?)\}",str(cookies.keys()))
keys = str(matches[0]).split(",")
if len(keys)>1:
    cleand_keys = []
    print(keys)
    for i in keys:
        between_quotes = i.split("'")[1]
        before_colon = between_quotes.split("':")[0]
        cleand_keys.append(before_colon)
    cleand_keys.pop(0)
    for i in cleand_keys:
        st.write(cookies[str(i)])
else:
    st.write("No History")