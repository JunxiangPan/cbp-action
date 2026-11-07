"""Experimental CEL implementation of the slop-comment detection layer."""
from __future__ import annotations

from .cel_policy import evaluate_context

EXPRESSION = 'text.matches("(?m).*(#\\s*(This is|It is|This function|This method|This class)).*")'


def matches(text: str) -> bool:
    """Return true when the CEL expression flags a slop comment."""
    return evaluate_context(EXPRESSION, {"text": text})
