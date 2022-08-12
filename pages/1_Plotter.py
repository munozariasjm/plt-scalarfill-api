import streamlit as st


def select_data_type():
    st.header("Select data type")
    data_type = st.selectbox("Select data type", ["s", "d", "dc", "ldc"])
    return data_type


def select_channel():
    st.header("Select a channel")
    channel = st.int_slider(
        "Select a channel", min_value=1, max_value=16, value=1, step=1
    )
    return channel
