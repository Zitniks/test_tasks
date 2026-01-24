import re


def add_trademark(text: str) -> str:
    pattern = r'\b([a-zA-Z]{6})\b'
    return re.sub(pattern, r'\1™', text)
