from typing import Dict, List
from pydantic import BaseModel

class GlossaryRequest(BaseModel):
    title : str
    description : str
    word : List[Dict[str, str]]

    def to_dict(self):
        result = {
            "title": self.title,
            "description": self.description,
            "word": self.word
        }

        return result

class Glossary(GlossaryRequest):
    mongo_id : str

    def to_dict(self):
        result = {
            "mongo_id": self.mongo_id,
            "title": self.title,
            "description": self.description,
            "word": self.word
        }

        return result


class SttRequest(BaseModel):
    text : str
    mongo_id : str
    source_lang : str
    target_lang : str

    def to_dict(self):
        result = {
            "text": self.text,
            "mongo_id": self.mongo_id,
        }
        return result
