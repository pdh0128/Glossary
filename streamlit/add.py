import streamlit as st
import requests

def render_add():
    st.title("📚 용어집 생성기")

    title = st.text_input("제목")
    description = st.text_area("설명")

    st.markdown("## 📝 용어 목록 입력")

    if "word_list" not in st.session_state:
        st.session_state.word_list = [{}]

    col1, col2 = st.columns(2)
    if col1.button("➕ 행 추가"):
        st.session_state.word_list.append({})
    if col2.button("➖ 마지막 행 제거") and len(st.session_state.word_list) > 1:
        st.session_state.word_list.pop()

    for i, word in enumerate(st.session_state.word_list):
        with st.expander(f"용어 {i+1}"):
            st.session_state.word_list[i]["kr"] = st.text_input(f"[{i+1}] 한국어", key=f"kr_{i}")
            st.session_state.word_list[i]["en"] = st.text_input(f"[{i+1}] 영어", key=f"en_{i}")
            st.session_state.word_list[i]["zh"] = st.text_input(f"[{i+1}] 중국어", key=f"zh_{i}")
            st.session_state.word_list[i]["ja"] = st.text_input(f"[{i+1}] 일본어", key=f"ja_{i}")
            st.session_state.word_list[i]["de"] = st.text_input(f"[{i+1}] 독일어", key=f"de_{i}")
            st.session_state.word_list[i]["fr"] = st.text_input(f"[{i+1}] 프랑스어", key=f"fr_{i}")
            st.session_state.word_list[i]["es"] = st.text_input(f"[{i+1}] 스페인어", key=f"es_{i}")

    cleaned_words = []
    for word in st.session_state.word_list:
        cleaned = {k: v for k, v in word.items() if v.strip() != ""}
        cleaned_words.append(cleaned)

    if st.button("📤 /glossary로 전송"):
        payload = {
            "title": title,
            "description": description,
            "word": cleaned_words
        }
        try:
            res = requests.post("http://localhost:8000/glossary", json=payload)
            if res.status_code == 200:
                st.success("전송 성공 ✅")
                st.json(res.json())
            else:
                st.error(f"전송 실패 ❌: {res.status_code}")
                st.text(res.text)
        except Exception as e:
            st.error(f"요청 실패 ❌: {e}")
