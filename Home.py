import streamlit as st
from streamlit.logger import get_logger
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from src.imgs.paths import bril_logo, cms_logo

LOGGER = get_logger(__name__)
st.set_page_config(
    page_title="PLT Plotting tools", page_icon="🤖📈",
)

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
name, authentication_status = authenticator.login("Login", "main")


def display_home():

    st.markdown(
        """
        ## PLT Plotter, a fast and versatile vizualizator and explorer for 
        Scalar Data hosted Online
        """
    )
    col1, col2 = st.columns(2)

    with col1:
        st.header("")
        st.image(cms_logo)

    with col2:
        st.header("")
        st.image(bril_logo)


def run():
    if authentication_status:
        display_home()
        st.sidebar.subheader("You are logged in as: " + name)
        st.sidebar.image(bril_logo)
    elif authentication_status == False:
        st.error("Username/password Incorrect")
    elif authentication_status == None:
        st.warning("Please add a correct username and password")


if __name__ == "__main__":
    run()
