from transformers import pipeline


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
