"""Deterministic parser for OCR text from identity/education documents."""

from __future__ import annotations

import re
from datetime import date


def _clean_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _normalize_ocr_digits(token: str) -> str:
    # Common OCR confusions in numeric fields.
    table = str.maketrans(
        {
            "I": "1",
            "i": "1",
            "l": "1",
            "|": "1",
            "!": "1",
            "O": "0",
            "o": "0",
            "D": "0",
            "Q": "0",
            "S": "5",
            "s": "5",
            "B": "8",
            "Z": "2",
            "G": "6",
        }
    )
    return token.translate(table)


def _title_or_none(value: str | None) -> str | None:
    if not value:
        return None
    return _clean_spaces(value).title()


def _extract_date(
    text: str,
    labels: list[str],
    year_min: int = 1900,
    year_max: int | None = None,
) -> tuple[date | None, str | None]:
    if year_max is None:
        year_max = date.today().year

    for label in labels:
        m = re.search(
            rf"\b{label}\b\s*[:\-]?\s*(\d{{1,2}})[\-/](\d{{1,2}})[\-/](\d{{2,4}})",
            text,
            flags=re.IGNORECASE,
        )
        if not m:
            continue
        day, month, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if year < 100:
            year += 1900 if year > 30 else 2000
        if year < year_min or year > year_max:
            continue
        try:
            parsed = date(year, month, day)
            return parsed, f"{day:02d}/{month:02d}/{year:04d}"
        except ValueError:
            continue
    return None, None


def _extract_year(text: str, labels: list[str]) -> int | None:
    for label in labels:
        m = re.search(
            rf"\b{label}\b\s*[:\-]?\s*([12IilOo][09Oo][0-9IilOo]{{2}})",
            text,
            flags=re.IGNORECASE,
        )
        if m:
            raw = _normalize_ocr_digits(m.group(1))
            try:
                year = int(raw)
            except ValueError:
                continue
            if 1900 <= year <= date.today().year:
                return year
    return None


def _extract_any_plausible_birth_date(text: str) -> tuple[date | None, str | None]:
    # Capture noisy OCR date tokens like 09/09/I981, 09-09-1981, 09.09.1981.
    dates: list[date] = []
    for m in re.finditer(r"\b(\d{1,2})[\-\./](\d{1,2})[\-\./]([0-9A-Za-z!|]{4})\b", text):
        # Do not use issue/expiry dates as DOB candidates.
        left = text[max(0, m.start() - 20):m.start()].lower()
        if any(k in left for k in ["issue", "expiry", "valid", "date of issue"]):
            continue

        day = int(m.group(1))
        month = int(m.group(2))
        year_token = _normalize_ocr_digits(m.group(3))
        try:
            year = int(year_token)
        except ValueError:
            continue
        if not (1900 <= year <= date.today().year):
            continue
        try:
            parsed = date(year, month, day)
        except ValueError:
            continue
        dates.append(parsed)

    if not dates:
        return None, None

    # Aadhaar usually includes issue date + DOB; DOB is typically the oldest date on card.
    best = min(dates)
    return best, f"{best.day:02d}/{best.month:02d}/{best.year:04d}"
    return None, None


def _extract_any_plausible_birth_year(text: str) -> int | None:
    years: list[int] = []
    for m in re.finditer(r"\b([12IilOo][09Oo][0-9A-Za-z!|]{2})\b", text):
        ctx_left = text[max(0, m.start() - 24):m.start()].lower()
        ctx_right = text[m.end():min(len(text), m.end() + 12)].lower()
        ctx = f"{ctx_left} {ctx_right}"
        if any(k in ctx for k in ["issue", "expiry", "valid", "issued"]):
            continue

        raw = _normalize_ocr_digits(m.group(1))
        try:
            year = int(raw)
        except ValueError:
            continue
        if 1900 <= year <= date.today().year:
            years.append(year)
    if not years:
        return None
    # Prefer older plausible birth year over recent issue years.
    return min(years)


def _compute_over_18(dob: date | None, yob: int | None) -> bool | None:
    today = date.today()
    if dob:
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age >= 18
    if yob:
        return (today.year - yob) >= 18
    return None


def _compute_age_years(dob: date | None, yob: int | None) -> int | None:
    today = date.today()
    if dob:
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if yob:
        return today.year - yob
    return None


def _find_labeled_value(text: str, labels: list[str], max_len: int = 80) -> str | None:
    for label in labels:
        m = re.search(
            rf"(?im)^\s*{label}\s*[:\-]?\s*([^\n\r]{{2,{max_len}}})\s*$",
            text,
            flags=re.IGNORECASE,
        )
        if m:
            return _clean_spaces(m.group(1))
    return None


def _detect_type(text: str) -> tuple[str, float]:
    lower = text.lower()

    aadhaar_patterns = [
        r"aadh?a+a?r",
        r"uid[ai1l]",
        r"unique\s+identification",
        r"government\s+of\s+india",
    ]
    aadhaar_score = sum(1 for p in aadhaar_patterns if re.search(p, lower))
    if re.search(r"\b\d{4}\s?\d{4}\s?\d{4}\b", text):
        aadhaar_score += 1

    passport_patterns = [
        r"passp[o0]rt",
        r"republic\s+of\s+india",
        r"passport\s*(?:no|number)",
        r"nationality",
        r"date\s+of\s+birth",
    ]
    passport_score = sum(1 for p in passport_patterns if re.search(p, lower))
    if re.search(r"\b[A-Z][0-9]{7}\b", text):
        passport_score += 1

    marksheet_patterns = [
        r"mark\s*sheet|marksheet",
        r"statement\s+of\s+marks",
        r"grade\s*sheet",
        r"semester",
        r"subject",
        r"percentage|cgpa|aggregate",
        r"roll\s*(?:no|number)",
    ]
    marksheet_score = sum(1 for p in marksheet_patterns if re.search(p, lower))

    best = max(aadhaar_score, passport_score, marksheet_score)
    if best == 0:
        return "generic", 0.0
    if best == aadhaar_score:
        return "aadhaar", min(1.0, 0.35 + 0.15 * aadhaar_score)
    if best == passport_score:
        return "passport", min(1.0, 0.35 + 0.15 * passport_score)
    return "marksheet", min(1.0, 0.35 + 0.12 * marksheet_score)


def _parse_aadhaar(text: str) -> dict:
    aadhaar_no_match = re.search(r"\b(\d{4}\s?\d{4}\s?\d{4})\b", text)
    aadhaar_no = aadhaar_no_match.group(1).replace(" ", "") if aadhaar_no_match else None

    name = _find_labeled_value(text, ["name"])
    # Handle OCR variants like D0B / DOB / Date of Birth.
    dob, dob_raw = _extract_date(
        text,
        ["dob", "d0b", "date of birth", "birth"],
    )

    if not dob:
        # Tolerant direct scan for DOB labels with OCR substitutions.
        dob_label_match = re.search(
            r"(?:d\s*[0o]?\s*b|date\s*of\s*birth)\s*[:\-]?\s*(\d{1,2})[\-\./](\d{1,2})[\-\./]([0-9A-Za-z!|]{4})",
            text,
            flags=re.IGNORECASE,
        )
        if dob_label_match:
            day = int(dob_label_match.group(1))
            month = int(dob_label_match.group(2))
            year_token = _normalize_ocr_digits(dob_label_match.group(3))
            try:
                year = int(year_token)
                if 1900 <= year <= date.today().year:
                    dob = date(year, month, day)
                    dob_raw = f"{day:02d}/{month:02d}/{year:04d}"
            except ValueError:
                pass

    yob = _extract_year(text, ["year of birth", "yob"])

    over_18 = _compute_over_18(dob, yob)

    return {
        "name": _title_or_none(name),
        "aadhaar_number": aadhaar_no,
        "dob": dob_raw,
        "year_of_birth": yob,
        "nationality": "Indian",
        "over_18": over_18,
    }


def _parse_passport(text: str) -> dict:
    passport_no_match = re.search(r"\b([A-Z][0-9]{7})\b", text)
    passport_no = passport_no_match.group(1) if passport_no_match else None

    surname = _find_labeled_value(text, ["surname", "last name"])
    given_names = _find_labeled_value(text, ["given name", "given names", "first name"])
    full_name = _title_or_none(" ".join(p for p in [given_names, surname] if p))

    dob, dob_raw = _extract_date(text, ["date of birth", "dob", "birth"], year_min=1900, year_max=date.today().year)
    _, expiry_raw = _extract_date(
        text,
        ["date of expiry", "expiry", "expires"],
        year_min=2000,
        year_max=date.today().year + 20,
    )

    if not dob_raw:
        # OCR sometimes reads 1992 as 1092 on passports; repair for DOB labels only.
        m = re.search(
            r"\b(?:date\s+of\s+birth|dob|birth)\b\s*[:\-]?\s*(\d{1,2})[\-/](\d{1,2})[\-/](\d{4})",
            text,
            flags=re.IGNORECASE,
        )
        if m:
            day, month, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
            if 1000 <= year <= 1299:
                year = 1900 + (year % 100)
            try:
                parsed_dob = date(year, month, day)
                if 1900 <= parsed_dob.year <= date.today().year:
                    dob = parsed_dob
                    dob_raw = f"{day:02d}/{month:02d}/{year:04d}"
            except ValueError:
                pass

    nationality = _find_labeled_value(text, ["nationality"]) or "Indian"

    return {
        "name": full_name,
        "passport_number": passport_no,
        "dob": dob_raw,
        "expiry_date": expiry_raw,
        "nationality": _title_or_none(nationality),
        "over_18": _compute_over_18(dob, None),
    }


def _parse_marksheet(text: str) -> dict:
    student_name = _find_labeled_value(text, ["name", "student name", "candidate name"])
    institution = _find_labeled_value(text, ["institution", "university", "college", "board"])
    course = _find_labeled_value(text, ["course", "program", "qualification", "degree"])
    percentage = _find_labeled_value(text, ["percentage", "overall", "aggregate", "cgpa"], max_len=24)
    roll_no = _find_labeled_value(text, ["roll no", "roll number", "registration no", "enrollment no"], max_len=30)

    return {
        "name": _title_or_none(student_name),
        "institution": _title_or_none(institution),
        "qualification": _title_or_none(course),
        "score": percentage,
        "roll_number": roll_no,
    }


def parse_document_profile(document_text: str) -> dict:
    """Parse OCR text into document type and extracted fields."""
    text = document_text or ""
    doc_type, confidence = _detect_type(text)

    if doc_type == "aadhaar":
        fields = _parse_aadhaar(text)
    elif doc_type == "passport":
        fields = _parse_passport(text)
    elif doc_type == "marksheet":
        fields = _parse_marksheet(text)
    else:
        fields = {}

    return {
        "doc_type": doc_type,
        "confidence": round(confidence, 2),
        "fields": fields,
    }
