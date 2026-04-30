def normalize(text):
    """
    Normalize text for easier comparison.
    """
    return text.strip().lower()


def filter_by_category(facilities, desired_category):
    """
    Return facilities matching the desired care category.
    """
    matches = []
    for facility in facilities:
        if facility.category == desired_category:
            matches.append(facility)
    return matches


def filter_by_city(facilities, desired_city):
    """
    Return facilities in the requested city.
    If the city is blank, return all facilities.
    Remote telehealth options are allowed regardless of city.
    """
    if desired_city.strip() == "":
        return facilities

    matches = []
    for facility in facilities:
        if normalize(facility.city) == "remote":
            matches.append(facility)
        elif normalize(facility.city) == normalize(desired_city):
            matches.append(facility)

    return matches


def filter_by_walk_in(facilities, need_walk_in):
    """
    If walk-in is required, return only walk-in facilities.
    Otherwise return the original list.
    """
    if not need_walk_in:
        return facilities

    matches = []
    for facility in facilities:
        if normalize(facility.walk_in) == "yes":
            matches.append(facility)

    return matches


def score_facility(facility, desired_city, need_walk_in):
    """
    Assign a recommendation score.

    Scoring factors:
    - city match
    - walk-in match
    - lower cost level
    """
    score = 0
    reasons = []

    if desired_city.strip() != "":
        if normalize(facility.city) == normalize(desired_city):
            score += 30
            reasons.append("city match")
        elif normalize(facility.city) == "remote":
            score += 10
            reasons.append("remote option")

    if need_walk_in:
        if normalize(facility.walk_in) == "yes":
            score += 25
            reasons.append("walk-in available")
    else:
        reasons.append("walk-in not required")

    try:
        cost = int(facility.cost_level)
        score += max(0, 10 - 2 * cost)
        reasons.append("cost considered")
    except ValueError:
        pass

    return score, reasons


def rank_facilities(facilities, desired_city, need_walk_in):
    """
    Return a ranked list of tuples:
    (score, facility, reasons)
    """
    ranked = []

    for facility in facilities:
        score, reasons = score_facility(facility, desired_city, need_walk_in)
        ranked.append((score, facility, reasons))

    ranked.sort(key=lambda item: (-item[0], item[1].name))
    return ranked


def recommend_facilities(facilities, desired_category, desired_city, need_walk_in):
    """
    First try exact matches with category, city, and walk-in.
    If no exact match exists, fall back to the same care category
    and rank the alternatives.
    """
    category_matches = filter_by_category(facilities, desired_category)
    city_matches = filter_by_city(category_matches, desired_city)
    exact_matches = filter_by_walk_in(city_matches, need_walk_in)

    if len(exact_matches) > 0:
        return "exact", rank_facilities(exact_matches, desired_city, need_walk_in)

    fallback_matches = rank_facilities(category_matches, desired_city, need_walk_in)
    return "fallback", fallback_matches