from fastapi import FastAPI
from fastapi.params import Query

from model.glossary import GlossaryRequest, SttRequest
from service import glossary_service
from core.mongo_watcher import start_change_stream_in_thread

app = FastAPI()
start_change_stream_in_thread()

# 용어집 등록
@app.post("/glossary")
async def bag_of_word(word_zip: GlossaryRequest):
    await glossary_service.upload_glossary(word_zip)
    return {"message" : "upload glossary"}

# 용어집 추천
@app.get("/glossary")
def glossary_recommend(text: str = Query(...), k : int = Query(10)):
    glossary_list =  glossary_service.recommend(text, k)
    return glossary_list

# 번역
@app.post("/glossary/translate")
async def glossary_translate(stt_request: SttRequest):
    translated_text = await glossary_service.translate(stt_request)
    return translated_text

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)