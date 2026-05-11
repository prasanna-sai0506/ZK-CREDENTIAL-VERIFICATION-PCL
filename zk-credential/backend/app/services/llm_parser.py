"""
LLM Claim Extraction Service
- Primary: GPT-4o via OpenAI + Instructor
- Fallback: LLaMA 3.1-70B via Groq
- Retry: max 3 attempts with tenacity
- Security: document wrapped in XML delimiters; never concatenated raw
"""

import logging
import re
from datetime import date

from app.config import settings
from app.models.schemas import ClaimSet
from app.services.document_parser import parse_document_profile

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are an identity claim extractor. "
    "Respond ONLY with a JSON object matching the ClaimSet schema. "
    "Extract only claims explicitly supported by document text. "
    "If a field is not explicitly present, return null for optional fields. "
    "Never infer education, employment, or institution unless directly stated. "
    "No preamble. No explanation. No markdown fences.\n\n"
    "ClaimSet schema:\n"
    "{\n"
    '  "over_18": bool | null,\n'
    '  "nationality": string | null,\n'
    '  "has_degree": string | null,\n'
    '  "degree_institution": string | null,\n'
    '  "employment_verified": bool | null,\n'
    '  "custom_claims": {}\n'
    "}"
)


def _detect_doc_type(text: str) -> str:
    if any(k in text for k in ["aadhaar", "uidai", "government of india"]):
        return "aadhaar"
    return "generic"


def _extract_age_over_18(text: str) -> bool | None:
    if re.search(r"\bover\s*18\b", text):
        return True

    age_match = re.search(r"\bage\s*[:\-]?\s*(\d{1,3})\b", text)
    if age_match:
        try:
            return int(age_match.group(1)) >= 18
        except ValueError:
            pass

    yob_match = re.search(r"\b(?:year\s*of\s*birth|yob)\s*[:\-]?\s*(\d{4})\b", text)
    if yob_match:
        year = int(yob_match.group(1))
        return (date.today().year - year) >= 18

    dob_match = re.search(
        r"\b(?:dob|date\s*of\s*birth)\s*[:\-]?\s*(\d{1,2})[\-/](\d{1,2})[\-/](\d{2,4})\b",
        text,
    )
    if dob_match:
        day = int(dob_match.group(1))
        month = int(dob_match.group(2))
        year = int(dob_match.group(3))
        if year < 100:
            year += 1900 if year > 30 else 2000
        try:
            born = date(year, month, day)
            today = date.today()
            age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            return age >= 18
        except ValueError:
            pass

    # Age evidence missing: do not guess.
    return None


def _extract_nationality(text: str, doc_type: str) -> str | None:
    if doc_type == "aadhaar":
        # Aadhaar is issued only in India; keep deterministic output for this doc class.
        return "Indian"

    labelled = re.search(r"\bnationality\s*[:\-]\s*([a-z ]{3,40})\b", text)
    if labelled:
        return labelled.group(1).strip().title()

    if re.search(r"\b(india|indian|bharat|government of india)\b", text):
        return "Indian"

    for n in [
        "indian",
        "american",
        "british",
        "canadian",
        "australian",
        "german",
        "french",
        "chinese",
        "japanese",
        "brazilian",
    ]:
        if re.search(rf"\bcitizen\s+of\s+{re.escape(n)}\b", text):
            return n.title()

    return None


def _extract_degree_fields(text: str) -> tuple[str | None, str | None]:
    # Conservative by design: require explicit labels to avoid hallucinated education claims.
    degree_match = re.search(
        r"\b(?:degree|qualification|education)\s*[:\-]\s*([a-z0-9 .,&'\-/]{2,80})\b",
        text,
    )
    institution_match = re.search(
        r"\b(?:institution|university|college|institute)\s*[:\-]\s*([a-z0-9 .,&'\-/]{2,80})\b",
        text,
    )

    has_degree = degree_match.group(1).strip().title() if degree_match else None
    degree_institution = institution_match.group(1).strip().title() if institution_match else None
    return has_degree, degree_institution


def _extract_employment(text: str) -> bool | None:
    positive = re.search(
        r"\b(?:employment\s*verified|employment\s*status|currently\s*employed)\s*[:\-]?\s*(yes|true|verified|employed)\b",
        text,
    )
    if positive:
        return True

    negative = re.search(
        r"\b(?:employment\s*verified|employment\s*status)\s*[:\-]?\s*(no|false|not\s*verified|unemployed)\b",
        text,
    )
    if negative:
        return False

    return None

def _build_user_message(document_text: str) -> str:
    """Wraps document in XML delimiters — never raw concatenation."""
    return f"<document>\n{document_text}\n</document>\n\nExtract claims now."


def _parse_with_openai(document_text: str) -> ClaimSet:
    import instructor
    from openai import OpenAI

    client = instructor.from_openai(OpenAI(api_key=settings.OPENAI_API_KEY))
    return client.chat.completions.create(
        model="gpt-4o",
        response_model=ClaimSet,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _build_user_message(document_text)},
        ],
        max_retries=3,
    )


def _parse_with_groq(document_text: str) -> ClaimSet:
    import instructor
    from groq import Groq

    client = instructor.from_groq(Groq(api_key=settings.GROQ_API_KEY))
    return client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        response_model=ClaimSet,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _build_user_message(document_text)},
        ],
        max_retries=3,
    )


def _parse_with_heuristics(document_text: str) -> ClaimSet:
    """
    Local deterministic fallback when external LLM APIs are unavailable.
    This keeps the async proof pipeline operational in dev/demo setups.
    """
    text = document_text.lower()
    doc_type = _detect_doc_type(text)

    over_18 = _extract_age_over_18(text)
    nationality = _extract_nationality(text, doc_type)

    has_degree, degree_institution = _extract_degree_fields(text)
    employment_verified = _extract_employment(text)

    if doc_type == "aadhaar" and (has_degree or degree_institution or employment_verified is not None):
        logger.warning("Aadhaar doc detected with non-identity fields; keeping only explicit labelled values.")

    return ClaimSet(
        over_18=over_18,
        nationality=nationality,
        has_degree=has_degree,
        degree_institution=degree_institution,
        employment_verified=employment_verified,
        custom_claims={
            "extraction_mode": "heuristic",
            "doc_type": doc_type,
            "strict_mode": True,
        },
    )


def _claimset_from_document_profile(profile: dict) -> ClaimSet | None:
    doc_type = profile.get("doc_type")
    fields = profile.get("fields", {})
    confidence = profile.get("confidence", 0.0)

    if doc_type not in {"aadhaar", "passport", "marksheet"}:
        return None

    over_18 = fields.get("over_18")
    if over_18 is not None:
        over_18 = bool(over_18)
    nationality = fields.get("nationality")

    has_degree = None
    degree_institution = None
    if doc_type == "marksheet":
        has_degree = fields.get("qualification")
        degree_institution = fields.get("institution")

    return ClaimSet(
        over_18=over_18,
        nationality=nationality,
        has_degree=has_degree,
        degree_institution=degree_institution,
        employment_verified=None,
        custom_claims={
            "extraction_mode": "document_parser",
            "doc_type": doc_type,
            "confidence": confidence,
            "extracted_fields": fields,
        },
    )


def extract_claims(document_text: str) -> ClaimSet:
    """
    Extract structured claims from document text.
    Tries OpenAI first, falls back to Groq.
    """
    if not document_text or not document_text.strip():
        raise ValueError("Empty document text provided to claim extractor")

    profile = parse_document_profile(document_text)
    parsed_claims = _claimset_from_document_profile(profile)
    if parsed_claims is not None:
        logger.info(
            "Using deterministic document parser for %s (confidence=%s)",
            profile.get("doc_type"),
            profile.get("confidence"),
        )
        return parsed_claims

    # Try primary model first.
    if settings.OPENAI_API_KEY:
        try:
            logger.info("Extracting claims with GPT-4o")
            return _parse_with_openai(document_text)
        except Exception as e:
            logger.warning(f"OpenAI extraction failed: {e}. Falling back to Groq/local parser.")

    # Try fallback model.
    if settings.GROQ_API_KEY:
        try:
            logger.info("Extracting claims with LLaMA 3.1-70B via Groq")
            return _parse_with_groq(document_text)
        except Exception as e:
            logger.warning(f"Groq extraction failed: {e}. Falling back to local heuristic parser.")

    if settings.HEURISTIC_FALLBACK_ENABLED:
        logger.warning("Using local heuristic claim parser as emergency fallback")
        return _parse_with_heuristics(document_text)

    raise RuntimeError(
        "LLM extraction unavailable and heuristic fallback is disabled. "
        "Set HEURISTIC_FALLBACK_ENABLED=true only for emergency/dev usage."
    )
