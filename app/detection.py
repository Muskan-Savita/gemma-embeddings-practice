import re

RULES = {
    "CREDIT_CARD": re.compile(r"\b(?:\d[ -]?){12,18}\d\b"),
    "EMAIL": re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
    "SSN":   re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "PHONE": re.compile(r"(?<!\d)\+?\d[\d\s-]{8,}\d(?!\d)"),
    "IPV4":  re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
}

def luhn_valid(number: str) -> bool:
    digits = [int(c) for c in number if c.isdigit()]
    if not 13 <= len(digits) <= 19:
        return False
    total = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0

def detect(text: str) -> list[tuple[str, int, int]]:
    out = []
    for label, pat in RULES.items():
        for m in pat.finditer(text):
            if label == "CREDIT_CARD" and not luhn_valid(m.group(0)):
                continue
            out.append((label, m.start(), m.end()))

    out.sort(key=lambda x: (x[1], -(x[2] - x[1])))
    result, last_end = [], -1
    for f in out:
        if f[1] >= last_end:
            result.append(f)
            last_end = f[2]
    return result

def sanitize(text: str) -> str:
    for label, s, e in sorted(detect(text), key=lambda x: x[1], reverse=True):
        text = text[:s] + f"<{label}>" + text[e:]
    return text
