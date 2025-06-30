from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate

from core.translator import Translator
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

template = """
당신은 원어민 수준의 언어 감각을 가진 전문 번역가입니다.  
아래 문장을 {target_lang}로 원어민처럼 자연스럽고 유창하게 번역해 주세요.

단, [관련 용어]에 명시된 단어들은 반드시 지정된 번역어로 일관되게 사용해야 하며, 이 단어들의 의미가 흐트러지지 않도록 자연스럽게 문맥에 녹여내야 합니다.

[관련 용어]
{term}

[입력 문장]
{input}

[번역된 문장]
"""


class ChatGPT(Translator):
    def __init__(self):
        llm = ChatOpenAI(
            temperature=0,
            model="gpt-3.5-turbo"
        )

        prompt = PromptTemplate.from_template(template)
        chain = LLMChain(llm=llm, prompt=prompt)
        super().__init__(model=chain)

    async def translate(self, sentence, words, resource_lang, target_lang):
        term = ""
        for word in words:
            term += f"- {word[resource_lang]} → {word[target_lang]}\n"

        target_lang_name = Translator.get_lang_name(target_lang)
        return self.model.run({
            "input": sentence,
            "target_lang": target_lang_name,
            "term": term
        })

