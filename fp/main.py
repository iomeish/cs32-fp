from load_data import load_facilities
from triage import choose_care_level, explain_care_level
from helpers import ask_yes_no
from filters import recommend_facilities
from map_visualization import create_facility_map


CITY_COORDS = {
    "boston": (42.3601, -71.0589),
    "cambridge": (42.3736, -71.1097),
    "somerville": (42.3876, -71.0995),
    "brookline": (42.3318, -71.1212),
    "malden": (42.4251, -71.0662),
    "chelsea": (42.3918, -71.0328)
}


def get_user_location(desired_city):
    """
    Optionally get an approximate user location for proximity ranking and mapping.
    The user can use a supported city center or enter custom coordinates.
    """
    city_key = desired_city.strip().lower()

    if city_key in CITY_COORDS:
        use_city_center = ask_yes_no(
            f"Use {desired_city} city center as your approximate location for ranking and mapping? (y/n): "
        )
        if use_city_center:
            return CITY_COORDS[city_key], f"{desired_city} city center"

    use_custom = ask_yes_no(
        "Do you want to enter custom latitude and longitude for ranking and mapping? (y/n): "
    )
    if not use_custom:
        return None, None

    while True:
        try:
            lat = float(input("Enter your latitude: ").strip())
            lon = float(input("Enter your longitude: ").strip())
            return (lat, lon), "Your entered location"
        except ValueError:
            print("Please enter valid numeric latitude and longitude values.")


def print_ranked_table(ranked):
    """
    Print a simple ranked table of facility recommendations.
    """
    print(
        f"{'Rank':<5}{'Score':<8}{'Name':<40}{'City':<15}{'Walk-in':<10}{'Cost':<6}{'Distance(mi)':<12}"
    )
    print("-" * 110)

    for i, (score, facility, reasons, dist) in enumerate(ranked[:5], start=1):
        if dist is None:
            dist_text = "-"
        else:
            dist_text = f"{dist:.1f}"

        print(
            f"{i:<5}{score:<8}{facility.name[:37]:<40}{facility.city:<15}{facility.walk_in:<10}{facility.cost_level:<6}{dist_text:<12}"
        )


def main():
    facilities = load_facilities("facilities.csv")

    desired_category = choose_care_level()

    print("\nRecommended care level:", desired_category)
    print(explain_care_level(desired_category))

    print("\nOptional filters (press Enter to skip a filter).")
    desired_city = input("City (example: Cambridge): ").strip()
    need_walk_in = ask_yes_no("Do you need walk-in availability? (y/n): ")

    user_location, user_label = get_user_location(desired_city)

    match_type, ranked = recommend_facilities(
        facilities, desired_category, desired_city, need_walk_in, user_location
    )

    print("\nRecommended options:\n")

    if len(ranked) == 0:
        print("No facilities found for that care level.")
        return

    if match_type == "fallback":
        print("No exact matches found for all selected filters.")
        print("Showing the best available alternatives in the same care category.\n")

    print_ranked_table(ranked)

    map_file = create_facility_map(
        ranked, user_location=user_location, user_label=user_label
    )

    if map_file is not None:
        print(f"\nSaved recommendation map to: {map_file}")
        print("Open that HTML file in a browser for the full interactive map.")

    print("\nTop recommendation details:\n")
    for score, facility, reasons, dist in ranked[:3]:
        facility.show()
        print(f"  score: {score}")
        if dist is not None:
            print(f"  distance: {dist:.1f} miles")
        print(f"  why: {', '.join(reasons)}")
        print()


if __name__ == "__main__":
    main()