import hashlib


def parse_tokens(text: bytes) -> str:
    tokens = text.split(b"\x01")
    return " ".join([t.decode() for t in tokens])
