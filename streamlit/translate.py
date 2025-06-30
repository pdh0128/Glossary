import streamlit as st
import requests

def render_translate():
    API_BASE = "http://localhost:8000"

    st.title("용어집 검색 및 번역")

    lang_options = {
        "한국어 (kr)": "kr",
        "영어 (en)": "en",
        "중국어 (zh)": "zh",
        "일본어 (ja)": "ja",
        "독일어 (de)": "de",
        "프랑스어 (fr)": "fr",
        "스페인어 (es)": "es",
    }

    source_lang_label = st.selectbox("원본 언어 선택", list(lang_options.keys()), index=0)
    target_lang_label = st.selectbox("번역 언어 선택", list(lang_options.keys()), index=1)

    source_lang = lang_options[source_lang_label]
    target_lang = lang_options[target_lang_label]

    input_text = st.text_input("STT data입니다.", "")

    if "selected_mongo_id" not in st.session_state:
        st.session_state.selected_mongo_id = None

    if "glossary_items" not in st.session_state:
        st.session_state.glossary_items = []

    if st.button("입력"):
        if input_text.strip() == "":
            st.warning("문장을 입력해주세요.")
        else:
            params = {"text": input_text, "size": 10}
            response = requests.get(f"{API_BASE}/glossary", params=params)

            if response.status_code == 200:
                st.session_state.glossary_items = response.json()
                st.session_state.selected_mongo_id = None
            else:
                st.error("용어집 검색 요청에 실패했습니다.")

    if st.session_state.glossary_items:
        st.subheader("추천 용어집 (하나 선택):")

        glossary_options = {
            f"{item['metadata'].get('title', '제목 없음')} - {item['metadata'].get('description', '')}": item['metadata']['mongo_id']
            for item in st.session_state.glossary_items
        }

        selected_option = st.radio("용어집 선택", list(glossary_options.keys()))
        st.session_state.selected_mongo_id = glossary_options[selected_option]

        if st.button("번역"):
            if st.session_state.selected_mongo_id:
                translate_payload = {
                    "text": input_text,
                    "mongo_id": st.session_state.selected_mongo_id,
                    "source_lang": source_lang,
                    "target_lang": target_lang
                }
                translate_response = requests.post(f"{API_BASE}/glossary/translate", json=translate_payload)

                if translate_response.status_code == 200:
                    st.success("번역 결과:")
                    st.write(translate_response.text)
                else:
                    st.error("번역 요청에 실패했습니다.")
            else:
                st.warning("용어집을 선택해주세요.")
