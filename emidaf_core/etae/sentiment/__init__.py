"""
ETAE sentiment analysis components.
"""

from .lexicon_sentiment import (
    DocumentSentiment,
    LexiconSentimentAnalyzer,
    SentimentAnalysisResult,
    SentimentDistribution,
)

__all__ = [
    "DocumentSentiment",
    "LexiconSentimentAnalyzer",
    "SentimentAnalysisResult",
    "SentimentDistribution",
]
