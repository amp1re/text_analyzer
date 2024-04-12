"""
This module contains utility classes and functions for the text analyzer application.

It includes the definition of a Sentiment class, which represents the result of sentiment analysis
with a sentiment name and a confidence score.
"""


class Sentiment:  # pylint: disable=R0903
    """
    Represents a sentiment classification result with a name and a score.

    Attributes
    ----------
    name : str
        The name of the sentiment.
    score : float
        The confidence score of the sentiment.
    """

    def __init__(self, name: str, score: float):
        self.name = name
        self.score = score

    def __repr__(self):
        return f"Sentiment(name={self.name}, score={self.score})"
