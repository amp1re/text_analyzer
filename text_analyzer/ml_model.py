# from transformers import pipeline
import logging

from transformers import logging as hf_logging
from transformers import pipeline

# Set the logging level using Hugging Face's logging utility
hf_logging.set_verbosity_error()

# Optionally, set the logging level using Python's logging library
logging.getLogger("transformers").setLevel(logging.ERROR)


class MLModel:
    def __init__(self, top_k: int = 5):
        self.model = pipeline(
            task="text-classification",
            model="SamLowe/roberta-base-go_emotions",
            top_k=top_k,
        )

    def classify_text(self, text: str) -> list[dict]:
        try:
            model_outputs = self.model(text)
            results = [
                {"name": x["label"], "score": round(x["score"], 2)}
                for x in model_outputs[0]
            ]
            return results
        except Exception as e:
            return [{"error": str(e)}]
