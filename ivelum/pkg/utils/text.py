"""Утилиты для модификации текста (™ после слов из 6 букв)."""

import re


def add_trademark(text: str) -> str:
    """Добавляет символ ™ после каждого слова ровно из 6 латинских букв."""
    pattern = r"\b([a-zA-Z]{6})\b"
    return re.sub(pattern, r"\1™", text)
