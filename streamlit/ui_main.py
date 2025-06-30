import streamlit as st
from add import render_add
from translate import render_translate

if "page" not in st.session_state:
    st.session_state.page = "등록"

with st.sidebar:
    st.title("메뉴")
    selected = st.radio("페이지를 선택하세요", ["등록", "번역"])
    st.session_state.page = selected

if st.session_state.page == "등록":
    render_add()
elif st.session_state.page == "번역":
    render_translate()
