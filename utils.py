import re

SENIOR_TITLE_PATTERN = r"\b(senior|sr|lead|manager|head|principal|staff|director|vp)\b"
EXPLICIT_SENIOR_EXP = r"\b([2-9]|\d{2})\+\s*years?\b|\b([3-9]|\d{2})\s*years?\b"
ENTRY_EXP_PATTERN = r"\b(0|1)\s*(?:-\s*\d+)?\s*years?\b|\b(fresher|entry[- ]level|intern(?:ship)?)\b"

SOFTWARE_PATTERN = r"\b(software|sde|swe)\b"

def is_global_fresher_job(context) :

    if re.search(SENIOR_TITLE_PATTERN, context):
        return False

    if re.search(EXPLICIT_SENIOR_EXP, context):
        return False

    if re.search(ENTRY_EXP_PATTERN, context):
        return True

    return True

def is_global_software_job(context) :
    if re.search(SOFTWARE_PATTERN, context) :
        return True

    return False