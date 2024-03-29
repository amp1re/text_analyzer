"""
This module defines the MLModel class for text classification using Hugging Face's Transformers.
"""

from transformers import pipeline

from .utils import Sentiment


class MLModel:  # pylint: disable=too-few-public-methods
    """
    A wrapper class for a text classification model from the Hugging Face Transformers library.

    Parameters
    ----------
    top_k : int, optional
        The number of top predictions to return (default is 5).
    """

    def __init__(self, top_k: int = 5):
        """
        Initializes the model with the specified parameters.
        """
        self.model = pipeline(
            task="text-classification",
            model="SamLowe/roberta-base-go_emotions",
            top_k=top_k,
        )

    def classify_text(self, text: str) -> list[Sentiment]:
        """
        Classifies the input text, returning the top_k classifications as Sentiment objects.

        Parameters
        ----------
        text : str
            The text to be classified.

        Returns
        -------
        list[Sentiment]
            A list of Sentiment objects containing the classification results.
        """
        try:
            model_outputs = self.model(text)
            return [
                Sentiment(x["label"], round(x["score"], 2)) for x in model_outputs[0]
            ]
        except Exception as e:
            print(f"An error occurred during classification: {str(e)}")
            raise
