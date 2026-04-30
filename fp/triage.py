from helpers import ask_yes_no


def determine_care_level(emergency, urgent, ongoing):
    """
    Return a care level from three boolean values.
    This helper makes the triage logic easier to test.
    """
    if emergency:
        return "ER"
    if urgent:
        return "URGENT_CARE"
    if ongoing:
        return "PRIMARY_CARE"
    return "TELEHEALTH"


def explain_care_level(care_level):
    """
    Return a short user-facing explanation of the care level.
    """
    if care_level == "ER":
        return "Based on your answers, emergency care may be appropriate."
    if care_level == "URGENT_CARE":
        return "Based on your answers, same-day non-emergency care may be appropriate."
    if care_level == "PRIMARY_CARE":
        return "Based on your answers, routine or ongoing care may be appropriate."
    return "Based on your answers, telehealth may be a reasonable non-emergency option."


def choose_care_level():
    """
    Ask the user triage questions and return a recommended care level.
    """
    print("\nThis project is for educational purposes only and is not medical advice.\n")

    emergency = ask_yes_no(
        "Emergency warning signs (chest pain, severe trouble breathing, heavy bleeding, fainting)? (y/n): "
    )
    if emergency:
        return determine_care_level(True, False, False)

    urgent = ask_yes_no(
        "Do you think you need care today (new issue, worsening symptoms, concerning pain, fever, or injury)? (y/n): "
    )
    if urgent:
        return determine_care_level(False, True, False)

    ongoing = ask_yes_no(
        "Is this an ongoing or routine issue (checkup, prescription refill, chronic problem)? (y/n): "
    )
    return determine_care_level(False, False, ongoing)