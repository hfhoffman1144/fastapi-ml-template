import uvicorn
from fastapi import FastAPI

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
