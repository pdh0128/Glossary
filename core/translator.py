from abc import ABC, abstractmethod
import langcodes

class Translator(ABC):
    def __init__(self, model):
        self.model = model

    @abstractmethod
    def translate(self, *args):
        pass

    @staticmethod
    def get_lang_name(lang_code: str, display_lang: str = "ko") -> str:
        if lang_code == 'kr':
            lang_code = 'ko'
        """lang_code: zh en 같은 ISO 코드"""
        try:
            return langcodes.Language.get(lang_code).display_name(display_lang)
        except:
            return f"{lang_code} 언어"
