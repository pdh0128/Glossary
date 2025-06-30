from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate

from core.translator import Translator
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

template = """
[관련 용어]
{term}

[입력 문장]
{input}

위 문장을 {target_lang}로 자연스럽고 문맥에 맞게 번역해줘.  
특히 [관련 용어]는 번역 시 일관되게 반영해줘.
가능하다면 원어민처럼 자연스러운 표현으로 번역해줘.
"""


class ChatGPT(Translator):
    def __init__(self):
        llm = ChatOpenAI(
            temperature=0.7,
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

