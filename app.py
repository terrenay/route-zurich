import streamlit as st
import komoot

uploaded_file = st.file_uploader("Upload a GPX file", type="gpx")

if uploaded_file:
    fig = komoot.highlight_unsafe_segments(uploaded_file)
    st.pyplot(fig)