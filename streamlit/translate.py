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

    if "clicked_mongo_id" not in st.session_state:
        st.session_state.clicked_mongo_id = None

    if "glossary_items" not in st.session_state:
        st.session_state.glossary_items = []

    if st.button("검색"):
        if input_text.strip() == "":
            st.warning("검색어를 입력해주세요.")
        else:
            params = {"text": input_text, "size": 10}
            response = requests.get(f"{API_BASE}/glossary", params=params)

            if response.status_code == 200:
                st.session_state.glossary_items = response.json()
                st.session_state.clicked_mongo_id = None
            else:
                st.error("검색 요청에 실패했습니다.")

    if st.session_state.glossary_items:
        st.subheader("검색 결과:")
        for item in st.session_state.glossary_items:
            meta = item["metadata"]
            title = meta.get("title", "제목 없음")
            description = meta.get("description", "")
            mongo_id = meta.get("mongo_id")

            with st.container():
                st.markdown(f"**{title}**")
                st.caption(description)

                if st.button(f"번역 요청: {title}", key=mongo_id):
                    st.session_state.clicked_mongo_id = mongo_id

    if st.session_state.clicked_mongo_id:
        selected_item = next(
            (item for item in st.session_state.glossary_items if item["metadata"]["mongo_id"] == st.session_state.clicked_mongo_id),
            None
        )
        if selected_item:
            translate_payload = {
                "text": input_text,
                "mongo_id": st.session_state.clicked_mongo_id,
                "source_lang": source_lang,
                "target_lang": target_lang
            }
            translate_response = requests.post(f"{API_BASE}/glossary/translate", json=translate_payload)

            if translate_response.status_code == 200:
                st.success("번역 결과:")
                st.write(translate_response.text)
            else:
                st.error("번역 요청에 실패했습니다.")
