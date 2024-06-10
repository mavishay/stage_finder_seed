import uvicorn
from fastapi import FastAPI

from stage_finder.langchain.views import router as langchain_router
from stage_finder.llama_index.views import router as llama_index_router

app = FastAPI()

app.include_router(langchain_router, prefix="/langchain", tags=["Langchain"])
app.include_router(llama_index_router, prefix="/llama_index", tags=["Llama index"])


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("stage_finder.main:app", host="0.0.0.0", port=9090, reload=True, reload_dirs=["stage_finder"])
