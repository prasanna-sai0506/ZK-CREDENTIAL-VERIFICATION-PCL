"""
Claim Validator
- Type-checks claims (Pydantic already does this, this adds business rules)
- Rejects contradictions
- Normalises values
"""

from app.models.schemas import ClaimSet
import logging

logger = logging.getLogger(__name__)

KNOWN_NATIONALITIES = {
    "indian": "Indian",
    "american": "American",
    "british": "British",
    "canadian": "Canadian",
    "australian": "Australian",
    "german": "German",
    "french": "French",
    "chinese": "Chinese",
    "japanese": "Japanese",
    "brazilian": "Brazilian",
}

KNOWN_DEGREES = {
    "cs": "CS", "computer science": "CS",
    "law": "Law",
    "medicine": "Medicine", "medical": "Medicine",
    "engineering": "Engineering",
    "business": "Business", "mba": "MBA",
    "arts": "Arts",
    "science": "Science",
    "economics": "Economics",
}


def validate_and_normalise(claim_set: ClaimSet) -> ClaimSet:
    """Apply business-rule validation and normalise string values."""

    # Normalise nationality
    if claim_set.nationality:
        normalised = KNOWN_NATIONALITIES.get(claim_set.nationality.lower())
        if normalised:
            claim_set = claim_set.model_copy(update={"nationality": normalised})
        else:
            # Accept unknown but capitalise
            claim_set = claim_set.model_copy(
                update={"nationality": claim_set.nationality.strip().title()}
            )

    # Normalise degree
    if claim_set.has_degree:
        normalised = KNOWN_DEGREES.get(claim_set.has_degree.lower())
        if normalised:
            claim_set = claim_set.model_copy(update={"has_degree": normalised})
        else:
            claim_set = claim_set.model_copy(
                update={"has_degree": claim_set.has_degree.strip().title()}
            )

    # Contradiction check: degree_institution without degree
    if claim_set.degree_institution and not claim_set.has_degree:
        logger.warning("degree_institution set but has_degree is None — clearing institution")
        claim_set = claim_set.model_copy(update={"degree_institution": None})

    logger.info(f"Validated claim set: {claim_set.model_dump()}")
    return claim_set


def build_bitmap(claim_set: ClaimSet) -> int:
    """
    Encode boolean claims as a bitmap integer.
    Bit 0: over_18
    Bit 1: nationality_present
    Bit 2: has_degree_present
    Bit 3: employment_verified
    """
    bitmap = 0
    if claim_set.over_18 is True:
        bitmap |= (1 << 0)
    if claim_set.nationality:
        bitmap |= (1 << 1)
    if claim_set.has_degree:
        bitmap |= (1 << 2)
    if claim_set.employment_verified:
        bitmap |= (1 << 3)
    return bitmap
