import streamlit as st
from src.utils.ech_plotter import TimeLinePlotterTool
from src.data.downloader import RemoteDataGetter
import random
import yaml
import warnings
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from src.imgs.paths import cms_logo
from streamlit_pandas_profiling import st_profile_report
import pandas_profiling
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import io
import os

data_downloader = RemoteDataGetter()

##########################################
warnings.filterwarnings("ignore")
st.set_option("deprecation.showPyplotGlobalUse", False)
st.set_page_config(page_title="Data Exploration", page_icon="🔎")
st.markdown(" # Data Exploration")

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
    with st.expander("Filter by type", expanded=False):
        st.write(
            """
            You can filter the dataframe by selecting the data you want to explore.
            For example `s`stands for single plane rates, while `dc` for double coincedences
            """
        )
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
    with st.sidebar.expander("More", expanded=False):
        st.sidebar.write("Fill number is the number of the fill in the fill list")
        available_fills = data_downloader.get_available_fills()
        if st.sidebar.button("Get a random fill number"):
            fill_number = random.choice(available_fills)
            st.sidebar.write(f"Displaying fill number {fill_number}")
        if st.sidebar.button("Select from all available fills"):
            st.sidebar.write(f"We have {len(available_fills)} fills available")
            fill_number = st.selectbox("List of Fills", available_fills)

    return fill_number


def page_display():
    st.write(
        """
             Tool to explore BRIL data. Select the channel you wold like to explore 
             in the left sidebar. 
             """
    )
    fill_number = _get_fill_number()
    data_types = select_data_type()
    st.write("")
    fill_df = data_downloader.get_fill_df(taget_fill=fill_number)
    cols = st.columns(2)
    with cols[0]:
        with st.expander("Help", expanded=False):
            st.write(
                """
            This utility allows you to explore the dataframe with statistical propieties
            of each one of the columns
            """
            )
    with cols[1]:
        with st.expander("Query Dataframe", expanded=False):
            st.write(
                """
                You can give a query in the traditional SQL style
                to the dataframe and it will return the results.
                
                For example, if you only want to explore the data from the channel
                number 10, you can write:
                `ch == 10`
                """
            )
            query_st = st.text_input("Enter a query", "")
            if st.button("Submit Query"):
                if query_st:
                    fill_df = fill_df.query(query_st)
            if st.button("Reset Query"):
                query_st = ""

    if st.button(f"Profile Fill {fill_number}"):
        col_modes = [
            c
            for c in fill_df.columns
            for mode in data_types
            if c.split(mode)[-1].isnumeric() and not c.split(mode)[0]
        ]
        pr = fill_df[col_modes].profile_report()
        with st.spinner(f"We are analyzing the Fill... {fill_number}"):
            with st.expander("Report results", expanded=True):
                st_profile_report(pr)
    with st.expander("Raw data Exploration", expanded=False):
        st.write(
            """You can move and resize the table below.
                    Also, click in the column name to filter or sort.
                    """
        )
        AgGrid(
            fill_df, allow_unsafe_jscode=True, width="100%",
        )

    with st.expander("Download file", expanded=False):
        st.write(f"Downloading data for fill {fill_number} as a hdf file")
        st.warning("The query will be applied to the dataframe")
        fill_df.to_hdf("foo.h5", index=False, mode="w", key="df")
        with open("foo.h5", "rb") as f:
            st.download_button("Download", f, file_name=f"fill_{fill_number}.h5")
        os.system("rm foo.h5")


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
