from fastapi import FastAPI
from model.glossary import GlossaryRequest
from service import glossary_service
from core.mongo_watcher import start_change_stream_in_thread

app = FastAPI()
start_change_stream_in_thread()

# 용어집 등록
@app.post("/glossary")
async def bag_of_word(word_zip: GlossaryRequest):
    await glossary_service.upload_glossary(word_zip)
    return {"message" : "upload glossary"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)