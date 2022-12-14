import streamlit as st
from src.utils.ech_plotter import LinePlotterTool
from src.data.downloader import RemoteDataGetter
import random
import yaml
import warnings
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from src.imgs.paths import cms_logo
import pandas as pd
import numpy as np

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
    opt_strings = [f"Ch {i+1}" for i in range(16)]
    channels = st.multiselect("Select a channel", opt_strings, opt_strings[0])
    return channels


def foo_channel_data():
    n = 1000
    Xdf = []
    for ch in range(1, 16):
        df = pd.DataFrame(
            {
                "dt": np.arange(n),
                "ch": np.ones(n) * ch,
                "s0": np.random.normal(0, 1, n) * n,
                "s1": np.random.normal(0, 1, n) * n,
                "s2": np.random.normal(0, 1, n) * n,
                "d0": np.random.normal(0, 1, n) * n,
                "d1": np.random.normal(0, 1, n) * n,
                "d2": np.random.normal(0, 1, n) * n,
            }
        )
        Xdf.append(df)
    return pd.concat(Xdf)


def _get_fill_number():
    st.sidebar.subheader("Select a fill number in the left sidebar")
    fill_number = st.sidebar.number_input(
        "Fill number", value=3815, min_value=3815, max_value=8114
    )
    with st.expander("More", expanded=False):
        st.sidebar.write("Fill number is the number of the fill in the fill list")
        available_fills = data_downloader.get_available_fills()
        if st.sidebar.button("Get a random fill number"):
            fill_number = random.choice(available_fills)
            st.sidebar.write(f"Displaying fill number {fill_number}")
        if st.sidebar.button("Select from all available fills"):
            st.sidebar.write(f"We have {len(available_fills)} fills available")
            fill_number = st.selectbox("available fills", available_fills)

    return fill_number


def page_display():
    tools_cols = st.columns(2)
    fill_number = _get_fill_number()
    # fill_number = np.random.randint(3000, 9000)

    with tools_cols[0]:
        with st.expander("Displayed Channels"):
            channel_list = select_channel()
    with tools_cols[1]:
        with st.expander("Displayed Data Type", expanded=False):
            data_types = select_data_type()

    main_cols = st.columns(len(channel_list))

    for channel_name, channel_col in zip(channel_list, main_cols):
        with channel_col:
            st.header(channel_name)
            fill_df = data_downloader.get_fill_df(taget_fill=fill_number)
            # fill_df = foo_channel_data()
            for mode in data_types:
                time_line_plotter = LinePlotterTool(title=f"Mode {mode}")
                col_modes = [
                    c
                    for c in fill_df.columns
                    if c.split(mode)[-1].isnumeric() and not c.split(mode)[0]
                ]
                channel_num = "".join([l for l in channel_name if l.isnumeric()])
                foo_df = fill_df.query(f"ch == {channel_num}")[col_modes + ["dt"]]
                line = time_line_plotter.lineplot(foo_df, x="dt", y=col_modes)
                time_line_plotter.st_show(line)


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
