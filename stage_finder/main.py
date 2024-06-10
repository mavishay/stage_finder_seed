import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("stage_finder.main:app", host="0.0.0.0", port=9090, reload=True, reload_dirs=["stage_finder"])
