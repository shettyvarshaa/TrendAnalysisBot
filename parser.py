import re


MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}


def parse_date(text):
    text = re.sub(r'\[\d{1,2}/\d{1,2},\s*\d{1,2}:\d{2}\]\s*[^:]+:\s*', '', text.strip())

    numeric_date = re.search(r'\b(\d{1,2})\s*[/-]\s*(\d{1,2})\s*[/-]\s*(\d{2,4})\b', text)
    if numeric_date:
        day, month, year = map(int, numeric_date.groups())
        if year < 100:
            year += 2000
        return f"{day:02d}/{month:02d}/{str(year)[-2:]}"

    named_date = re.search(
        r'\b(\d{1,2})(?:st|nd|rd|th)?\s+'
        r'(January|February|March|April|May|June|July|August|September|October|November|December)'
        r'(?:\s+(\d{2,4}))?\b',
        text,
        re.IGNORECASE,
    )
    if named_date:
        day = int(named_date.group(1))
        month = MONTHS[named_date.group(2).lower()]
        year = int(named_date.group(3) or 2026)
        if year < 100:
            year += 2000
        return f"{day:02d}/{month:02d}/{str(year)[-2:]}"

    return None


def parse_amount(text):
    if not text:
        return None

    text = text.replace(",", "")
    numbers = re.findall(r'\d+(?:\.\d+)?', text)
    if not numbers:
        return None

    if "=" in text:
        after_equal = text.rsplit("=", 1)[1]
        match = re.search(r'\d+(?:\.\d+)?', after_equal)
        if match:
            return float(match.group())

    return float(numbers[0])


def split_reports(text):
    parts = re.split(r"(?i)(?:sale['’]?s?\s+report)", text)
    return [part.strip() for part in parts if part.strip()]


def parse_report(block):
    block = re.sub(r'\[\d{1,2}/\d{1,2},\s*\d{1,2}:\d{2}\]\s*[^:]+:\s*', '', block)
    block = re.sub(r'^[;\s]+', '', block)

    date = parse_date(block)
    ms_match = re.search(r'(?im)^\s*MS\s*[-:;=]\s*(.+)$', block)
    hsd_match = re.search(r'(?im)^\s*HSD\s*[-:;=]\s*(.+)$', block)
    total_match = re.search(r'(?im)^\s*Total(?:\s+sales?)?\s*[-:;=.]*\s*(.+)$', block)

    ms = parse_amount(ms_match.group(1)) if ms_match else None
    hsd = parse_amount(hsd_match.group(1)) if hsd_match else None
    total = parse_amount(total_match.group(1)) if total_match else None

    if date is None:
        return None
    ms = ms or 0.0
    hsd = hsd or 0.0
    total = total if total is not None else ms + hsd

    return {
        "date": date,
        "ms": round(ms, 2),
        "hsd": round(hsd, 2),
        "total": round(total, 2),
    }


def parse_multi(text):
    if not text or not text.strip():
        raise ValueError("No text was provided.")

    parsed_items = [item for item in (parse_report(report) for report in split_reports(text)) if item]
    if not parsed_items:
        raise ValueError(
            "No valid sales reports found. Please check that each report contains a date, MS and HSD."
        )
    return parsed_items
