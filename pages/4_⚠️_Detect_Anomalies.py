import streamlit as st
from src.utils.ech_plotter import TimeLinePlotterTool
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
st.set_page_config(page_title="Dectect Anomalies", page_icon="⚠️")
st.markdown(" # Dectect Anomalies ⚠️")

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



def main_page():
    if authentication_status:
        st.write("Should it be putted here?")
        st.write("If yes, please talk to Jose M Munoz")
    elif authentication_status == False:
        st.error("Username/password is incorrect")
    elif authentication_status == None:
        st.warning("Please add your Username/password")


main_page()
