import streamlit as st
from src.data.downloader import RemoteDataGetter
import random
import yaml
import warnings
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from src.imgs.paths import cms_logo
import requests
import pandas as pd
import re
from st_aggrid import AgGrid

data_downloader = RemoteDataGetter()

##########################################
warnings.filterwarnings("ignore")
st.set_option("deprecation.showPyplotGlobalUse", False)
st.set_page_config(page_title="History Explorer", page_icon="📈")
st.markdown(" # History Explorer")

##########################################
with open("./users.yaml") as file:
    streamlit_cofig = yaml.load(file, Loader=SafeLoader)
users_config = streamlit_cofig["credentials"]
names = list(users_config["usernames"].keys())
usernames = list(users_config["usernames"].keys())
hashed_passwords = [user["password"] for user in users_config["usernames"].values()]
authenticator = stauth.authenticate(
    names,
    usernames,
    hashed_passwords,
    "cookie_name",
    "signature_key",
    cookie_expiry_days=30,
)
name, authentication_status = authenticator.login("Login", "sidebar")
##########################################


def get_host_content(host_path="https://delannoy.web.cern.ch/plt-scaler/"):
    contents = requests.get(host_path).content
    fill_nums = list(set(re.findall(r"\d+.pkl", str(contents))))
    fill_dates = re.findall(r" \d{4}-\d+-\d+ \d+:\d+\s", str(contents))
    sizes = re.findall(r" \d+.?\d+?[MK]", str(contents))
    st.write("Files in the database ", len(fill_nums))
    return pd.DataFrame(
        {"fill_number": fill_nums, "Uploading date": fill_dates, "size": sizes,}
    )


def page_display():
    contents = get_host_content()
    AgGrid(contents)


def main_page():
    if authentication_status:
        page_display()
        st.sidebar.write("Logged in as: " + name)
        # st.sidebar.image(cms_logo)
    elif authentication_status == False:
        st.error("Username/password is incorrect")
    elif authentication_status == None:
        st.warning("Please add your Username/password")


main_page()
