import streamlit as st
import requests

def render_add():
    st.title("📚 용어집 생성기")

    title = st.text_input("제목")
    description = st.text_area("설명")

    if "languages" not in st.session_state:
        st.session_state.languages = ["kr", "en"]

    if "word_list" not in st.session_state:
        st.session_state.word_list = [{lang: "" for lang in st.session_state.languages}]

    st.sidebar.subheader("🌐 언어 설정")
    new_lang = st.sidebar.text_input("새 언어 코드 추가 (예: zh, ja, fr, es)")
    if st.sidebar.button("언어 추가"):
        if new_lang and new_lang not in st.session_state.languages:
            st.session_state.languages.append(new_lang)
            for word in st.session_state.word_list:
                word[new_lang] = ""

    if len(st.session_state.languages) > 1:
        remove_lang = st.sidebar.selectbox("삭제할 언어", st.session_state.languages)
        if st.sidebar.button("언어 삭제"):
            st.session_state.languages.remove(remove_lang)
            for word in st.session_state.word_list:
                word.pop(remove_lang, None)

    st.sidebar.markdown("---")
    st.sidebar.markdown("**현재 사용 언어:**")
    st.sidebar.write(", ".join(st.session_state.languages))

    st.markdown("## 📝 용어 목록 입력")

    col1, col2 = st.columns(2)
    if col1.button("➕ 행 추가"):
        new_word = {lang: "" for lang in st.session_state.languages}
        st.session_state.word_list.append(new_word)
    if col2.button("➖ 마지막 행 제거") and len(st.session_state.word_list) > 1:
        st.session_state.word_list.pop()

    for i, word in enumerate(st.session_state.word_list):
        with st.expander(f"용어 {i+1}"):
            for lang in st.session_state.languages:
                label = f"[{i+1}] {lang.upper()}"
                key = f"{lang}_{i}"
                word[lang] = st.text_input(label, value=word.get(lang, ""), key=key)

    cleaned_words = []
    for word in st.session_state.word_list:
        cleaned = {k: v for k, v in word.items() if v.strip() != ""}
        if cleaned:
            cleaned_words.append(cleaned)

    if st.button("용어집 등록"):
        payload = {
            "title": title,
            "description": description,
            "word": cleaned_words
        }
        try:
            res = requests.post("http://localhost:8000/glossary", json=payload)
            if res.status_code == 200:
                st.success("전송 성공")
                st.json(res.json())
            else:
                st.error(f"전송 실패 ❌: {res.status_code}")
                st.text(res.text)
        except Exception as e:
            st.error(f"요청 실패 ❌: {e}")
