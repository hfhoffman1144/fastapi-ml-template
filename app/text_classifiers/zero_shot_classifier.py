from transformers import pipeline
from transformers.pipelines.base import Pipeline


def initialize_zero_shot_classifier(model: str) -> Pipeline:
    """
    Initialize a transformers Pipeline object for zero-shot classification
    with a specified model.
    """
    return pipeline(task="zero-shot-classification", model=model)
