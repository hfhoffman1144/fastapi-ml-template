import uvicorn
from config import Config
from fastapi import FastAPI
from pydantic import BaseModel
from text_classifiers.zero_shot_classifier import initialize_zero_shot_classifier

config = Config()

TEXT_CLASSIFIER = initialize_zero_shot_classifier(config.text_model)

app = FastAPI()


class ZeroShotTextInput(BaseModel):
    text: str
    labels: list[str]
    multi_label: bool = True


class ZeroShotTextResponse(BaseModel):
    id: str
    sequence: str
    labels: list[str]
    scores: list[float]


@app.post("/zero-shot-text-classifier", response_model=ZeroShotTextResponse)
async def classify_text(payload: ZeroShotTextInput) -> ZeroShotTextResponse:
    """
    Classify text with a zero-shot text classifier.
    """

    # TODO: Get ID and add to DB
    id = "1"
    response = TEXT_CLASSIFIER(
        payload.text, payload.labels, multi_label=payload.multi_label
    )
    response["id"] = id

    return ZeroShotTextResponse.model_validate(response)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
