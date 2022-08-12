import streamlit as st
from src.utils.ech_plotter import TimeLinePlotterTool
from src.data.downloader import RemoteDataGetter
import random
import yaml
import warnings
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from src.imgs.paths import cms_logo

data_downloader = RemoteDataGetter()

##########################################
warnings.filterwarnings("ignore")
st.set_option("deprecation.showPyplotGlobalUse", False)
st.set_page_config(page_title="Data Plotting", page_icon="📈")
st.markdown(" # Data Plotting 📈")

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


def select_data_type():
    data_type = st.multiselect(
        "Select data type", ["s", "d", "dc", "ldc"], ["s", "d", "dc", "ldc"]
    )
    return data_type


def select_channel():
    st.header("Select a channel")
    channel = st.slider("Select a channel", min_value=1, max_value=16, value=1, step=1)
    return channel


def _get_fill_number():
    st.sidebar.header("Select a fill")
    fill_number = st.sidebar.number_input(
        "Fill number", value=3815, min_value=3815, max_value=8114
    )
    with st.expander("Help", expanded=False):
        st.sidebar.write("Fill number is the number of the fill in the fill list")
        available_fills = data_downloader.get_available_fills()
        if st.sidebar.button("Get a random fill number"):
            fill_number = random.choice(available_fills)
            st.sidebar.write(f"Displaying fill number {fill_number}")
        if st.sidebar.button("Select from all available fills"):
            st.sidebar.write(f"We have {len(available_fills)} fills available")
            fill_number = st.selectbox(available_fills)

    return fill_number


def page_display():
    fill_number = _get_fill_number()
    data_types = select_data_type()
    channel = select_channel()
    fill_df = data_downloader.get_fill_df(taget_fill=fill_number)
    for mode in data_types:
        time_line_plotter = TimeLinePlotterTool(title=f"Mode {mode}")
        col_modes = [
            c
            for c in fill_df.columns
            if c.split(mode)[-1].isnumeric() and not c.split(mode)[0]
        ]
        foo_df = fill_df.query(f"ch == {channel}")[col_modes + ["dt"]]
        time_line_plotter.timeplot(foo_df, time_axis="dt", cols=col_modes)


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
